from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import re
import signal
import sys
import tempfile
import time
from collections.abc import Sequence
from pathlib import Path

from updater.locking import restart_sentinel_path
from updater.models import ComponentStatus

logger = logging.getLogger(__name__)

UPDATER_SERVICE = "BlocksScreen-updater.service"

# Hook budget: a deps-heavy hook (Spoolman uv sync) runs minutes; timeout = abort.
HOOK_TIMEOUT = 600.0

GIT = "/usr/bin/git"
PIP = "/usr/bin/pip3"
APT = "/usr/bin/apt"
APT_MARK = "/usr/bin/apt-mark"
SUDO = "/usr/bin/sudo"
SYSTEMCTL = "/usr/bin/systemctl"
DPKG = "/usr/bin/dpkg"
# Root-owned fixed-argv apt wrapper (owns the -o opts); installed pre-restart.
APT_HELPER = Path("/usr/local/sbin/bs-apt-helper")

_SERVICE_RE = re.compile(r"^[a-zA-Z0-9@:._-]+\.service$")
_GIT_SHA_RE = re.compile(r"^[a-f0-9]{7,40}$")
_GIT_SYMREF_RE = re.compile(r"^origin/[a-zA-Z0-9._-]+$")
_GIT_BRANCH_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._/-]*$")
_GIT_TAG_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._/-]*$")
_PACKAGE_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9+\-.]*$")

_HOOKS_DIR = Path(__file__).parent / "hooks"
_STALE_LOCK_AGE_THRESHOLD_S = 10.0


def _clear_stale_git_index_lock(path: Path) -> bool:
    """Remove .git/index.lock only if it is stale (older than threshold).

    A stale lock is left by a SIGKILL'd or interrupted git operation. Only
    remove if mtime indicates lock is NOT held by a live git process (age >=
    threshold). At runtime, a fresh lock may indicate a concurrent legitimate
    git op; yanking it would corrupt that op. Returns True if lock was
    removed or did not exist; False if lock exists but is too fresh to safely
    remove.
    """
    lock_path = path / ".git" / "index.lock"
    if not lock_path.exists():
        return True
    try:
        age_s = time.time() - lock_path.stat().st_mtime
        if age_s >= _STALE_LOCK_AGE_THRESHOLD_S:
            logger.warning("clearing stale index.lock (age %.1fs) from %s", age_s, path)
            lock_path.unlink()
            return True
        logger.debug(
            "index.lock is fresh (age %.1fs < %.1fs threshold), not removing to avoid "
            "corrupting concurrent git op",
            age_s,
            _STALE_LOCK_AGE_THRESHOLD_S,
        )
        return False
    except OSError as exc:
        logger.warning("could not age-check index.lock at %s: %s", lock_path, exc)
        return False


def _kill_proc_group(proc, sig):
    """Kill a process group; suppress errors if already gone."""
    try:
        os.killpg(os.getpgid(proc.pid), sig)
    except (ProcessLookupError, PermissionError):
        pass  # process already gone


def _make_clean_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for key in (
        "PATH",
        "HOME",
        "USER",
        # SEC: session bus + XDG runtime vars excluded; hooks must not use them.
        "TMPDIR",
    ):
        val = os.environ.get(key)
        if val is not None:
            env[key] = val
    env["GIT_TERMINAL_PROMPT"] = "0"
    # git_fetch's broken-ref self-heal and the apt parser match English messages
    env["LC_ALL"] = "C"
    # SEC: only copy safe SUDO_ vars; reject SUDO_ASKPASS and others
    safe_sudo = {"SUDO_USER", "SUDO_UID", "SUDO_GID"}
    for key, val in os.environ.items():
        if key in safe_sudo:
            env[key] = val
    # Tells hooks they run mid-batch: defer daemon restarts to the sentinel.
    env["BS_UPDATER_SELF_UPDATE"] = "1"
    with contextlib.suppress(OSError):
        env["BS_UPDATER_RESTART_SENTINEL"] = str(restart_sentinel_path())
    return env


async def _run(
    cmd: Sequence[str | Path],
    *,
    timeout: float,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> tuple[bool, str]:
    """Run a subprocess, return (success, stdout_or_stderr).

    On timeout: SIGTERM → 5s grace → SIGKILL.
    On CancelledError: SIGKILL → 2s grace, then re-raise.
    """
    proc = await asyncio.create_subprocess_exec(
        *[str(c) for c in cmd],
        cwd=cwd,
        env=env if env is not None else _make_clean_env(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        start_new_session=True,
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        if proc.returncode == 0:
            return True, stdout.decode(errors="replace")
        return False, stderr.decode(errors="replace")
    except asyncio.TimeoutError:
        if proc.returncode is None:
            _kill_proc_group(proc, signal.SIGTERM)
        try:
            await asyncio.wait_for(proc.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            if proc.returncode is None:
                _kill_proc_group(proc, signal.SIGKILL)
            await proc.wait()
        return False, f"timed out after {timeout}s"
    except asyncio.CancelledError:
        if proc.returncode is None:
            _kill_proc_group(proc, signal.SIGKILL)
            with contextlib.suppress(asyncio.TimeoutError):
                await asyncio.wait_for(proc.wait(), timeout=2.0)
        raise


def _validate_git_ref(ref: str) -> bool:
    """Return True if ref is a valid SHA, origin/ symref, or git tag/branch name."""
    return bool(
        _GIT_SHA_RE.match(ref) or _GIT_SYMREF_RE.match(ref) or _GIT_TAG_RE.match(ref)
    )


def _resolve_component_pip(path: Path | None) -> str:
    """Find the pip binary for a component's venv; falls back to system pip if none found.

    SEC: Validate venv paths are under component or parent; reject symlinks to prevent
    arbitrary venv hijacking.
    """
    if path is None:
        logger.warning("Path not found, using system pip")
        return PIP
    try:
        resolved_path = path.resolve()
    except (OSError, RuntimeError):
        logger.warning("Could not resolve component path, using system pip")
        return PIP
    possible_paths = [
        path.parent / f".{path.name}-env" / "bin" / "pip",
        path.parent / f"{path.name}-env" / "bin" / "pip",
        path.parent / ".venv" / "bin" / "pip",
        path / ".venv" / "bin" / "pip",
        path / "venv" / "bin" / "pip",
    ]
    for pip_path in possible_paths:
        if not pip_path.exists():
            continue
        try:
            resolved_pip = pip_path.resolve()
            resolved_pip.relative_to(resolved_path.parent)
        except (OSError, ValueError):
            logger.warning(
                "Rejected venv pip at %s (path escape or unresolvable)", pip_path
            )
            continue
        return str(pip_path)
    logger.warning("No venv found for %s, falling back to system pip", path)
    return PIP


async def _list_upgradable_packages() -> tuple[bool, list[str]]:
    """Return (success, list_of_package_names) from apt list --upgradable.

    SEC: Validate package names against Debian naming rules to prevent
    injection attacks even if apt output is malformed.
    """
    ok, output = await _run([APT, "list", "--upgradable"], timeout=30.0)
    if not ok:
        return False, []
    pkgs = []
    for line in output.splitlines():
        if "/" not in line or line.startswith("Listing"):
            continue
        pkg_name = line.split("/")[0].strip()
        if not pkg_name:
            continue
        if not _PACKAGE_NAME_RE.match(pkg_name):
            logger.warning("skipping suspiciously-named package: %r", pkg_name)
            continue
        pkgs.append(pkg_name)
    return True, pkgs


def _compile_exclude_patterns(exclude: tuple[str, ...]) -> list[re.Pattern]:
    """Compile apt exclude regexes; log and skip invalid patterns."""
    compiled = []
    for pat in exclude:
        try:
            compiled.append(re.compile(pat))
        except re.error:
            logger.warning("invalid apt_exclude regex %r - skipping", pat)
    return compiled


def _apply_exclude_patterns(pkgs: list[str], exclude: tuple[str, ...]) -> list[str]:
    if not exclude:
        return pkgs
    compiled = _compile_exclude_patterns(exclude)
    return [p for p in pkgs if not any(r.search(p) for r in compiled)]


async def _count_apt_upgradable(exclude: tuple[str, ...] = ()) -> int:
    ok, pkgs = await _list_upgradable_packages()
    if not ok:
        return -1
    pkgs = _apply_exclude_patterns(pkgs, exclude)
    return len(pkgs)


async def check_git_status(
    name: str,
    path: Path | None,
    branch: str | None = None,
    version: str | None = None,
    skip_fetch: bool = False,
) -> ComponentStatus:
    """Return a ComponentStatus snapshot for a git-based component."""
    if path is None or not path.exists():
        return ComponentStatus(name=name, error=f"path {path} does not exist")
    if not skip_fetch:
        result, output = await git_fetch(path, prune_remotes=False)
        if not result:
            logger.error("Failed at git_fetch operation, %s", output)
            return ComponentStatus(name=name, error=output)
    current_hash = await git_get_hash(path)
    if current_hash == "":
        logger.error("Failed at git_hash operation")
        return ComponentStatus(name=name, error="Failed at git_hash operation")
    current_branch = await git_get_current_branch(path)
    if branch:
        remote_ref = f"origin/{branch}"
    else:
        remote_ref = f"origin/{current_branch}" if current_branch else "origin/HEAD"
    # Configured branch != checked-out branch: needs an update to switch.
    branch_mismatch = bool(branch) and current_branch != branch
    if version:
        commits_behind = 0
    else:
        commits_behind = await git_commits_behind(path, remote_ref)
    if commits_behind == -1:
        logger.error("Failed at git_commits_behind operation")
        return ComponentStatus(
            name=name, error="Failed at git_commits_behind operation"
        )
    (
        remote_url,
        has_local_changes,
        current_version,
        remote_version,
    ) = await asyncio.gather(
        git_remote_url(path),
        git_is_dirty(path),
        git_describe(path),
        git_describe(path, remote_ref),
    )
    if remote_url == "":
        logger.error("Failed at git_remote_url operation")
        return ComponentStatus(
            name=name,
            current_hash=current_hash,
            commits_behind=commits_behind,
            current_version=current_version,
            remote_version=remote_version,
            has_local_changes=has_local_changes,
            error="Failed at git_remote_url operation",
        )
    return ComponentStatus(
        name=name,
        current_hash=current_hash,
        commits_behind=commits_behind,
        remote_url=remote_url,
        has_local_changes=has_local_changes,
        current_version=current_version,
        remote_version=remote_version,
        branch_mismatch=branch_mismatch,
        current_branch=current_branch,
    )


def is_git_repo(path: Path | None) -> bool:
    """True if path exists and has a .git entry (a non-repo dir can never fetch)."""
    return path is not None and (path / ".git").exists()


async def git_is_dirty(path: Path) -> bool:
    ok, output = await _run(
        [GIT, "status", "--porcelain", "--untracked-files=no"],
        cwd=path,
        timeout=10.0,
    )
    return ok and bool(output.strip())


async def git_prune_extra_remotes(path: Path) -> None:
    ok, output = await _run([GIT, "remote"], cwd=path, timeout=10.0)
    if not ok:
        return
    extras = [r for r in output.splitlines() if r and r != "origin"]
    if not extras:
        return  # No extra remotes to remove
    for remote in extras:
        ok, err = await _run([GIT, "remote", "remove", remote], cwd=path, timeout=10.0)
        if ok:
            logger.info("pruned extra remote %r from %s", remote, path)
        else:
            logger.warning("failed to remove remote %r from %s: %s", remote, path, err)


_BROKEN_REF_RE = re.compile(r"cannot lock ref '([^']+)'")


def _remove_broken_loose_ref(path: Path, ref: str) -> None:
    """Delete a corrupt loose ref and its reflog when `update-ref -d` cannot."""
    git_dir = path / ".git"
    for p in (git_dir / ref, git_dir / "logs" / ref):
        with contextlib.suppress(OSError):
            p.unlink()


async def _prune_broken_refs(path: Path, output: str) -> bool:
    """Delete corrupt refs named in a failed fetch. Returns True if any were."""
    pruned = False
    for ref in dict.fromkeys(_BROKEN_REF_RE.findall(output)):
        if not ref.startswith("refs/") or any(c.isspace() for c in ref):
            continue
        ok, _ = await _run([GIT, "update-ref", "-d", ref], cwd=path, timeout=10.0)
        if not ok:
            await asyncio.to_thread(_remove_broken_loose_ref, path, ref)
        logger.warning("git_fetch: pruned broken ref %r in %s", ref, path)
        pruned = True
    return pruned


async def git_fetch(
    path: Path | None, *, prune_remotes: bool = True
) -> tuple[bool, str]:
    """Fetch all remotes for the repo at path.

    prune_remotes=False skips the extra-remote cleanup; pass False during status
    checks where pruning is unnecessary and adds ~2 subprocess spawns per repo.

    A corrupt local ref (null SHA from an interrupted write) makes --prune abort
    the whole fetch and silently disables every update; on that failure the
    named ref is deleted and the fetch retried once.
    """
    if path is None:
        return (False, "path does not exist")
    if prune_remotes:
        await git_prune_extra_remotes(path)
    cmd = [GIT, "fetch", "--all", "--atomic", "--prune"]
    ok, out = await _run(cmd, cwd=path, timeout=60.0)
    if ok or "reference broken" not in out:
        return (ok, out)
    if not await _prune_broken_refs(path, out):
        return (ok, out)
    return await _run(cmd, cwd=path, timeout=60.0)


async def git_pull(path: Path | None) -> tuple[bool, str]:
    """Fast-forward pull for the repo at path."""
    if path is None:
        return (False, "path does not exist")
    return await _run([GIT, "pull", "--ff-only"], cwd=path, timeout=60.0)


_GIT_URL_RE = re.compile(r"^https://[a-zA-Z0-9._~:/?#\[\]@!$&'()*+,;=%-]+$")


async def git_clone(
    url: str, path: Path | None, branch: str | None = None
) -> tuple[bool, str]:
    """Clone url into path (https-only), optionally at branch. Returns (ok, message).

    Large repos (klipper, moonraker) can take a while, so the timeout is generous.
    git creates the leaf directory; the parent (home) must already exist.
    """
    if not path:
        return (False, "path error")
    if not _GIT_URL_RE.match(url):
        return (False, f"invalid or non-https clone url: {url!r}")
    if branch is not None and not _GIT_BRANCH_RE.match(branch):
        return (False, f"invalid branch name: {branch!r}")
    cmd = [GIT, "clone"]
    if branch:
        cmd += ["--branch", branch]
    cmd += [url, str(path)]
    return await _run(cmd, timeout=300.0)


async def git_reset_to_hash(path: Path | None, prev_hash: str = "") -> tuple[bool, str]:
    """Hard-reset repo at path directly to prev_hash without fetching.

    This is the rollback/heal primitive (abort, boot revert, recover), so the
    timeout is generous: a reset across a large delta on a slow SD card must
    not be SIGTERM'd mid-checkout in exactly the path meant to fix things.
    If reset fails with an index.lock error, clears it and retries once.
    """
    if not path:
        return (False, "path error")
    if prev_hash == "":
        return (False, "prev_hash does not exist")
    if not _validate_git_ref(prev_hash):
        return (False, f"invalid git ref: {prev_hash!r}")
    ok, err = await _run([GIT, "reset", "--hard", prev_hash], cwd=path, timeout=60.0)
    if ok:
        return (ok, err)
    if "index.lock" in err and _clear_stale_git_index_lock(path):
        return await _run([GIT, "reset", "--hard", prev_hash], cwd=path, timeout=60.0)
    return (ok, err)


# Narrow corruption signatures: "not a git repository" etc. must not match.
_GIT_CORRUPT_SIGNATURES = (
    "corrupt",
    "is empty",
    "cannot read",
    "invalid index-pack",
    "missing blob",
    "missing tree",
    "missing commit",
    "unable to unpack",
    "inflate: data stream error",
)

# Quarantine dir inside .git/objects so it never appears as untracked.
_QUARANTINE_DIRNAME = "objects-corrupt"
# fsck names corrupt objects by path (.git/objects/ab/<38hex>) or 40-hex SHA.
_GIT_OBJ_PATH_RE = re.compile(r"objects/([0-9a-f]{2})/([0-9a-f]{38})")
_GIT_OBJ_SHA_RE = re.compile(r"\b([0-9a-f]{40})\b")


async def git_has_corruption(path: Path | None, hint: str = "") -> bool:
    """True if `hint` or git fsck shows object corruption.

    `hint` (e.g. a failed fetch's stderr) is checked first: `git fsck
    --connectivity-only` validates reachability, not object content, so it can
    miss a corrupt blob that already broke the fetch. The fetch error is the
    reliable signal in that case.
    """
    if path is None:
        return False
    if any(k in hint for k in _GIT_CORRUPT_SIGNATURES):
        return True
    ok, out = await _run(
        [GIT, "fsck", "--connectivity-only", "--no-progress"], cwd=path, timeout=60.0
    )
    if ok:
        return False
    return any(k in out for k in _GIT_CORRUPT_SIGNATURES)


def _prune_empty_loose_objects(objects: Path) -> int:
    """Delete 0-byte loose objects (the classic power-loss signature). Returns count."""
    removed = 0
    for sub in objects.iterdir():
        if len(sub.name) != 2 or not sub.is_dir():
            continue  # loose objects live in 2-hex-char subdirs only
        for obj in sub.iterdir():
            try:
                if obj.is_file() and obj.stat().st_size == 0:
                    obj.unlink()
                    removed += 1
            except OSError:
                continue
    return removed


async def _quarantine_corrupt_objects(path: Path) -> int:
    """Move loose objects that `git fsck --full` flags as corrupt out of the way.

    `git_has_corruption` uses `fsck --connectivity-only`, which never reads blob
    content and so cannot see a non-empty object with a bad zlib header - exactly
    what a power cut mid-write produces. A plain re-fetch will NOT replace such an
    object because git still finds a file at that name. `fsck --full` reads object
    content and names the bad ones; we move (not delete) them so a re-fetch
    re-downloads them, and a misdiagnosis stays recoverable. Returns count moved.
    """
    ok, out = await _run(
        [GIT, "fsck", "--full", "--no-dangling", "--no-progress"],
        cwd=path,
        timeout=120.0,
    )
    if ok:
        return 0  # fsck --full clean: corruption is elsewhere (e.g. a packfile)
    objects = path / ".git" / "objects"
    quarantine = objects / _QUARANTINE_DIRNAME
    candidates: set[Path] = set()
    for line in out.splitlines():
        m = _GIT_OBJ_PATH_RE.search(line)
        if m:
            candidates.add(objects / m.group(1) / m.group(2))
            continue
        if any(k in line for k in ("corrupt", "unable to unpack", "missing", "empty")):
            sha = _GIT_OBJ_SHA_RE.search(line)
            if sha:
                s = sha.group(1)
                candidates.add(objects / s[:2] / s[2:])
    moved = 0
    for obj in candidates:
        if not obj.is_file():
            continue  # e.g. a "missing blob" object that does not exist on disk
        try:
            dest = quarantine / obj.parent.name
            dest.mkdir(parents=True, exist_ok=True)
            obj.replace(dest / obj.name)
            moved += 1
        except OSError as exc:
            logger.warning("git_repair: could not quarantine %s: %s", obj, exc)
    logger.warning("git_repair: quarantined %d corrupt object(s) from %s", moved, path)
    return moved


async def git_repair(path: Path, branch: str = "main") -> tuple[bool, str]:
    """Prune 0-byte loose objects, re-fetch, and re-verify. Mirrors start.sh recovery.

    If empty-object pruning plus a fetch does not clear the corruption, escalate to
    quarantining non-empty corrupt loose objects (`fsck --full`) and re-fetch once
    more. Working tree is untouched (delete/move + fetch only), so tracked-but-
    modified files survive. If fetch fails with index.lock error, clears lock and
    retries. Branch parameter is used to repair corrupt HEAD (fallback to "main").
    Returns (ok, message).
    """
    _clear_stale_git_index_lock(path)
    objects = path / ".git" / "objects"
    if not objects.is_dir():
        return (False, "no .git/objects directory")
    removed = _prune_empty_loose_objects(objects)
    logger.warning("git_repair: removed %d empty object(s) from %s", removed, path)
    ok, out = await git_fetch(path, prune_remotes=False)
    if not ok and "index.lock" in out:
        _clear_stale_git_index_lock(path)
        ok, out = await git_fetch(path, prune_remotes=False)
    if not ok:
        return (False, f"fetch after cleanup failed: {out}")
    if not await git_has_corruption(path):
        if not await _repair_corrupt_head(path, branch):
            return (False, "repaired objects but HEAD still unreadable")
        return (True, f"repaired ({removed} empty objects removed)")
    quarantined = await _quarantine_corrupt_objects(path)
    if quarantined == 0:
        return (False, "still corrupt after fetch (no quarantinable objects found)")
    ok, out = await git_fetch(path, prune_remotes=False)
    if not ok:
        return (False, f"fetch after quarantine failed: {out}")
    if await git_has_corruption(path):
        return (False, "still corrupt after quarantine + fetch")
    if not await _repair_corrupt_head(path, branch):
        return (False, "repaired objects but HEAD still unreadable")
    return (
        True,
        f"repaired ({removed} empty + {quarantined} corrupt object(s) removed)",
    )


async def git_get_hash(path: Path | None) -> str:
    """Return the current HEAD commit hash, or empty string on failure."""
    if path is None:
        return ""
    ok, output = await _run([GIT, "rev-parse", "HEAD"], cwd=path, timeout=10.0)
    return output.strip() if ok else ""


async def _is_head_readable(path: Path) -> bool:
    """Return True if HEAD is readable and points to a valid commit."""
    ok, _out = await _run([GIT, "rev-parse", "HEAD"], cwd=path, timeout=10.0)
    return ok


async def _repair_corrupt_head(path: Path, branch: str = "main") -> bool:
    """Try to repair a corrupt HEAD by rewriting it to a valid symbolic ref.

    Returns True if HEAD was repaired or is already readable.
    """
    if await _is_head_readable(path):
        return True
    ok, _msg = await _run(
        [GIT, "symbolic-ref", "HEAD", f"refs/heads/{branch}"],
        cwd=path,
        timeout=10.0,
    )
    if ok:
        logger.warning("repair_corrupt_head: rewrote HEAD for %s", path)
        return True
    logger.warning("repair_corrupt_head: failed to rewrite HEAD for %s", path)
    return False


async def git_ref_hash(path: Path | None, ref: str) -> str:
    """Resolve an arbitrary ref (e.g. origin/main) to its commit hash, or empty."""
    if path is None:
        return ""
    ok, output = await _run([GIT, "rev-parse", ref], cwd=path, timeout=10.0)
    return output.strip() if ok else ""


async def git_commits_behind(path: Path, remote_ref: str = "origin/HEAD") -> int:
    """Return how many commits the local branch is behind remote_ref."""
    ok, output = await _run(
        [GIT, "rev-list", f"HEAD..{remote_ref}", "--count"],
        cwd=path,
        timeout=10.0,
    )
    if ok:
        try:
            return int(output.strip())
        except ValueError:
            return -1
    return -1


async def git_remote_url(path: Path) -> str:
    """Return the fetch URL for the origin remote, or empty string on failure."""
    ok, output = await _run(
        [GIT, "remote", "get-url", "origin"], cwd=path, timeout=10.0
    )
    return output.strip() if ok else ""


async def _assert_https_remote(path: Path | None) -> tuple[bool, str]:
    """Reject non-https origin remotes to guard against supply-chain attacks."""
    if path is None:
        return False, "path does not exist"
    url = await git_remote_url(path)
    if not url:
        return False, "could not read origin remote URL"
    if not url.startswith("https://"):
        return False, f"origin remote uses non-https URL {url!r}"
    return True, url


async def git_get_current_branch(path: Path) -> str:
    ok, output = await _run(
        [GIT, "rev-parse", "--abbrev-ref", "HEAD"], cwd=path, timeout=10.0
    )
    return output.strip() if ok else ""


async def git_describe(path: Path, ref: str | None = None) -> str:
    cmd = [GIT, "describe", "--tags", "--abbrev=0"]
    if ref:
        cmd.append(ref)
    ok, output = await _run(cmd, cwd=path, timeout=10.0)
    return output.strip() if ok else ""


async def git_checkout(
    path: Path | None, branch: str, *, force: bool = False
) -> tuple[bool, str]:
    if path is None:
        return (False, "path not found")

    if branch == "":
        return (False, "branch name is empty")

    if not _GIT_BRANCH_RE.match(branch):
        return (False, f"branch {branch} has an invalid name")
    current_branch = await git_get_current_branch(path)
    if current_branch == branch:
        return (True, "already on branch")

    # force: overwrite untracked collisions (e.g. build artifacts) that block a switch.
    cmd = [GIT, "checkout", "-f", branch] if force else [GIT, "checkout", branch]
    # Generous: a big checkout on slow SD can pass 10s; SIGTERM = half-written tree.
    return await _run(cmd, cwd=path, timeout=60.0)


async def check_apt_status(
    cache_ttl_seconds: int = 86_400, exclude: tuple[str, ...] = ()
) -> ComponentStatus:
    """Return apt ComponentStatus from cache, refreshing via apt-get if older than cache_ttl_seconds.

    SEC: Validate cache file ownership and permissions to prevent privilege escalation.
    """
    path = Path.home() / ".cache" / "blockscreen" / "apt_status_cache.json"
    exclude_key = "|".join(sorted(exclude))
    packages_upgradable = -1
    try:
        if path.exists():
            stat = path.stat()
            if stat.st_mode & 0o077:
                raise ValueError("cache has excessive permissions")
            if stat.st_uid != os.getuid():
                raise ValueError("cache not owned by current user")
            with open(path) as f:
                parsed_json = json.load(f)
            age = time.time() - parsed_json.get("cached_ts", 0)
            if (
                age >= 0
                and age < cache_ttl_seconds
                and parsed_json.get("exclude_key") == exclude_key
            ):
                packages_upgradable = parsed_json.get("packages_upgradable", -1)
                return ComponentStatus(
                    name="system", kind="apt", packages_upgradable=packages_upgradable
                )
    except (json.JSONDecodeError, IOError, ValueError) as e:
        logger.warning("apt cache miss %s", e)

    packages_upgradable = await _count_apt_upgradable(exclude=exclude)
    if packages_upgradable >= 0:
        tmp_path = None
        try:
            path.parent.mkdir(parents=True, mode=0o0700, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                dir=path.parent,
                delete=False,
                prefix=".apt_cache_",
                suffix=".tmp",
            ) as f:
                json.dump(
                    {
                        "packages_upgradable": packages_upgradable,
                        "exclude_key": exclude_key,
                        "cached_ts": time.time(),
                    },
                    f,
                )
                tmp_path = Path(f.name)
            tmp_path.chmod(0o600)
            tmp_path.replace(path)
        except (json.JSONDecodeError, IOError, ValueError) as e:
            if tmp_path is not None and tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
            logger.error("writing cache apt data: %s", e)

    if packages_upgradable < 0:
        return ComponentStatus(
            name="system",
            kind="apt",
            packages_upgradable=-1,
            error="apt status check failed",
        )
    return ComponentStatus(
        name="system", kind="apt", packages_upgradable=packages_upgradable
    )


def _apt_env() -> dict[str, str]:
    env = _make_clean_env()
    env["DEBIAN_FRONTEND"] = "noninteractive"
    # needrestart can otherwise open an interactive prompt mid-upgrade and hang.
    env["NEEDRESTART_MODE"] = "a"
    return env


def _apt_cmd(verb: str, pkgs: Sequence[str] = ()) -> list[str]:
    """Build the sudo apt argv via the root-owned wrapper.

    The wrapper is the only apt command sudoers grants. bs-bootstrap reinstalls it
    when missing (an old-installer box can have the service but not the wrapper); until
    that self-heal runs a missing wrapper surfaces as a plain 'command not found'.
    """
    return [SUDO, str(APT_HELPER), verb, *pkgs]


async def _apt_snapshot_packages() -> tuple[bool, Path | None]:
    """Snapshot current package state with dpkg --get-selections to temp file.

    Returns (success, snapshot_path).
    Path is stored at ~/.cache/blockscreen/apt_pre_upgrade_snapshot.txt.
    No sudo required for dpkg --get-selections.
    """
    snapshot_path = (
        Path.home() / ".cache" / "blockscreen" / "apt_pre_upgrade_snapshot.txt"
    )
    try:
        snapshot_path.parent.mkdir(parents=True, mode=0o0700, exist_ok=True)
        ok, output = await _run([DPKG, "--get-selections"], timeout=15.0)
        if not ok:
            logger.warning("dpkg --get-selections failed: %s", output)
            return False, None
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=snapshot_path.parent,
            delete=False,
            prefix=".apt_snapshot_",
        ) as f:
            f.write(output)
            tmp = Path(f.name)
        tmp.chmod(0o600)
        tmp.replace(snapshot_path)
        logger.info("apt snapshot saved to %s", snapshot_path)
        return True, snapshot_path
    except (IOError, ValueError) as e:
        logger.error("apt snapshot error: %s", e)
        return False, None


async def _apt_get_fix_broken() -> tuple[bool, str]:
    """Run apt-get -f install -y to fix broken package state.

    Best-effort rollback after failed upgrade. May not fully restore state,
    but aims to unbreak the system. Called only on apt_upgrade failure.
    """
    return await _run(_apt_cmd("fix-broken"), timeout=120.0, env=_apt_env())


async def _apt_restore_packages(snapshot_path: Path) -> tuple[bool, str]:
    """Restore dpkg package *selections* from the pre-upgrade snapshot, then dselect-upgrade.

    This re-asserts which packages should be installed; it does NOT reliably
    downgrade versions, since the prior .debs may no longer be in the apt cache.
    Treat it as an unbreak step (keep the set consistent), not a true rollback.
    Kernel/firmware are excluded from upgrades, bounding the blast radius.
    """
    try:
        stdin_data = snapshot_path.read_bytes()
    except OSError as e:
        logger.error("apt restore: cannot read snapshot %s: %s", snapshot_path, e)
        return False, str(e)
    proc = await asyncio.create_subprocess_exec(
        SUDO,
        str(APT_HELPER),
        "set-selections",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        start_new_session=True,
        env=_make_clean_env(),
    )
    try:
        _, stderr = await asyncio.wait_for(
            proc.communicate(input=stdin_data), timeout=60.0
        )
    except asyncio.TimeoutError:
        _kill_proc_group(proc, signal.SIGKILL)
        await proc.wait()
        return False, "dpkg --set-selections timed out"
    except asyncio.CancelledError:
        if proc.returncode is None:
            _kill_proc_group(proc, signal.SIGKILL)
            with contextlib.suppress(asyncio.TimeoutError):
                await asyncio.wait_for(proc.wait(), timeout=2.0)
        raise
    if proc.returncode != 0:
        msg = stderr.decode(errors="replace")
        logger.error("dpkg --set-selections failed: %s", msg)
        return False, msg
    return await _run(_apt_cmd("dselect-upgrade"), timeout=120.0, env=_apt_env())


def classify_apt_error(err: str) -> str:
    """Classify an apt failure: 'permanent' won't clear by retrying, 'transient' might."""
    lowered = err.lower()
    # A missing apt helper self-heals once bootstrap installs it: retry, never a 1h cooldown.
    if str(APT_HELPER).lower() in lowered and (
        "command not found" in lowered or "no such file" in lowered
    ):
        return "transient"
    permanent = (
        "command not found",
        "no such file or directory",
        "a password is required",
        "permission denied",
        "not allowed to execute",
    )
    return "permanent" if any(p in lowered for p in permanent) else "transient"


async def apt_update() -> tuple[bool, str]:
    """Run apt-get update to refresh package lists."""
    return await _run(_apt_cmd("update"), timeout=120.0, env=_apt_env())


async def apt_upgrade(exclude: tuple[str, ...] = ()) -> tuple[bool, str]:
    """Run apt-get upgrade via explicit package list to limit blast radius.

    Always lists upgradable packages first; applies exclude regexes if any.
    Uses 'install --only-upgrade' so only already-installed packages are touched.
    """
    ok, pkgs = await _list_upgradable_packages()
    if not ok:
        return False, "failed to list upgradable packages"

    pkgs = _apply_exclude_patterns(pkgs, exclude)

    if not pkgs:
        return True, "no packages to upgrade"

    return await _run(_apt_cmd("upgrade", pkgs), timeout=300.0, env=_apt_env())


async def apt_autoremove() -> tuple[bool, str]:
    """Run apt-get autoremove -y to remove orphaned packages after an upgrade."""
    return await _run(_apt_cmd("autoremove"), timeout=120.0, env=_apt_env())


async def run_hook(
    name: str,
    path: Path | None,
    new_hash: str,
    prev_hash: str,
    timeout: float = 60.0,
) -> tuple[bool, str]:
    """Run the per-component update hook if it exists.

    The 60s default suits tests and trivial hooks; the update and provisioning
    flows pass HOOK_TIMEOUT since a hook may sync a full dependency set (e.g.
    Spoolman's `uv sync` after its deps changed).
    """
    hook = (_HOOKS_DIR / f"{name}.sh").resolve()  # SEC: resolve symlinks
    try:
        hook.relative_to(_HOOKS_DIR.resolve())  # SEC: prevent path traversal
    except ValueError:
        return (False, "hook path escapes hooks directory")
    if not hook.exists():
        return (True, "no hook")
    env = _make_clean_env()
    env.update(
        {
            "COMPONENT_NAME": name,
            "COMPONENT_PATH": str(path) if path else "",
            "NEW_HASH": new_hash,
            "PREV_HASH": prev_hash,
        }
    )
    return await _run([str(hook)], env=env, timeout=timeout)


async def enable_service(name: str | None) -> tuple[bool, str]:
    """Enable a systemd unit so a newly provisioned service survives reboot."""
    if name is None:
        return (False, "service name is None")
    if not _SERVICE_RE.match(name):
        return (False, f"service name {name!r} is invalid")
    return await _run([SUDO, SYSTEMCTL, "enable", name], timeout=15.0)


async def wait_for_service_active(name: str, timeout: float = 90.0) -> bool:
    """Poll systemctl is-active until the service is active or timeout expires.

    `systemctl is-active --wait` does not exist (--wait applies only to
    start/restart/is-system-running/kill and is silently ignored here), so an
    explicit poll loop is required to ride out 'activating' after a restart.
    """
    if not _SERVICE_RE.match(name):
        logger.warning("wait_for_service_active: invalid service name %r", name)
        return False
    deadline = asyncio.get_running_loop().time() + timeout
    output = ""
    while True:
        ok, output = await _run([SYSTEMCTL, "is-active", name], timeout=10.0)
        if ok:
            logger.info("service %r is active", name)
            return True
        if asyncio.get_running_loop().time() >= deadline:
            break
        await asyncio.sleep(2.0)
    logger.warning(
        "service %r did not become active within %.0fs: %s",
        name,
        timeout,
        output.strip(),
    )
    return False


async def restart_service_noblock(name: str | None) -> tuple[bool, str]:
    """Queue a service restart without waiting (systemctl --no-block).

    For the UI service that hosts the updater's D-Bus client: a blocking restart
    tears down that client, and a slow restart could time out and abort the
    in-flight update. Fire-and-forget and let it reload on its own.
    """
    if name is None:
        return (False, "service name is None")
    if not _SERVICE_RE.match(name):
        return (False, f"service name {name!r} is invalid")
    return await _run([SUDO, SYSTEMCTL, "--no-block", "restart", name], timeout=15.0)


async def verify_updater_importable(component_path: Path | None) -> bool:
    """Self-test the new on-disk updater code before restarting into it.

    Imports the updater package in a fresh interpreter from component_path. A
    new updater that fails to import must never restart the daemon onto itself:
    that would take down the only field update path. On failure the caller keeps
    the running (old) daemon and lets the next reboot adopt the new code.
    """
    if component_path is None or not component_path.exists():
        return False
    ok, out = await _run(
        [sys.executable, "-c", "import updater.dbus_service"],
        cwd=component_path,
        timeout=30.0,
    )
    if not ok:
        logger.error("updater import self-test failed: %s", out.strip())
    return ok


async def restart_service(name: str | None) -> tuple[bool, str]:
    """Restart a systemd service, recovering from a start-limit hit.

    If `restart` fails (commonly "start request repeated too quickly"), clear the
    rate-limit/failed state with `reset-failed` and retry once. `systemctl kill`
    is NOT used as a fallback: it does not clear a start-limit and is not covered
    by the scoped NOPASSWD sudoers rules, so it would prompt for a password.
    """
    if name is None:
        return (False, "service name is None")
    if not _SERVICE_RE.match(name):
        return (False, f"service name {name!r} is invalid")
    ok, err = await _run([SUDO, SYSTEMCTL, "restart", name], timeout=30.0)
    if ok:
        return (True, "")
    logger.warning("systemctl restart %s failed (%s); reset-failed + retry", name, err)
    await _run([SUDO, SYSTEMCTL, "reset-failed", name], timeout=10.0)
    ok, err2 = await _run([SUDO, SYSTEMCTL, "restart", name], timeout=30.0)
    if ok:
        return (True, f"recovered via reset-failed (first error: {err})")
    return (False, err2)
