#!/usr/bin/env python3
"""Repair a venv truncated by a power cut; run as `$BSENV/bin/python3.11 -I`."""

import argparse
import csv
import importlib.metadata
import logging
import os
import re
import shutil
import subprocess  # nosec B404 - argv lists of sys.executable only
import sys
from pathlib import Path

_LOG = logging.getLogger("bs-venv-heal")
_PIN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([^\s;#]+)")
_CFG_HOME = re.compile(r"^home\s*=\s*\S", re.M)
_CFG_ISOLATED = re.compile(r"^include-system-site-packages\s*=\s*false\s*$", re.M)
# pip's AdjacentTempDirectory rollback names for `pip/` and `pip-X.dist-info` (`~ip`, `~-p-X.dist-info`).
_PIP_STASH = re.compile(r"^~[-~.=%0-9]*(?:pip|ip|p)(?:-[^-]+\.dist-info)?$")


def _site_packages() -> Path:
    """The venv's purelib dir."""
    return Path(
        sys.prefix,
        "lib",
        f"python{sys.version_info[0]}.{sys.version_info[1]}",
        "site-packages",
    )


def _record_damaged(dist_info: Path) -> bool:
    """True when a RECORD file listed with a size is missing or shorter on disk."""
    record = dist_info / "RECORD"
    try:
        text = record.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    if not text.strip() or "\0" in text:
        return True
    for row in csv.reader(text.splitlines()):
        if len(row) < 3 or not row[2].isdigit() or row[2] == "0":
            continue
        try:
            if (dist_info.parent / row[0]).stat().st_size < int(row[2]):
                return True
        except OSError:
            return True
    return False


def _metadata_damaged(dist_info: Path) -> bool:
    """True when METADATA lost its Name header (empty or NUL-filled after a cut)."""
    try:
        head = (dist_info / "METADATA").read_bytes()[:4096]
    except OSError:
        return True
    return b"\nName:" not in b"\n" + head


def broken_dists(site: Path) -> list[tuple[str, Path]]:
    """`name==version` and dist-info dir of every distribution with truncated files."""
    found = []
    for dist_info in sorted(site.glob("[A-Za-z0-9]*.dist-info")):
        # `~name` dirs are pip's rollback stash; their RECORD rows name the live dist's files.
        if _metadata_damaged(dist_info) or _record_damaged(dist_info):
            # Spec dir name: `{name}-{version}.dist-info`, `-` escaped as `_` in both parts.
            name, _, version = dist_info.name[: -len(".dist-info")].partition("-")
            found.append((f"{name}=={version}" if version else name, dist_info))
    return found


def _pip_works() -> bool:
    """Run pip itself: a 0-byte pip exits 0 and prints nothing."""
    script = Path(sys.prefix, "bin", "pip")
    try:
        res = subprocess.run(  # nosec B603
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return (
        res.returncode == 0
        and res.stdout.startswith("pip ")
        and script.is_file()
        and script.stat().st_size > 0
    )


def _uninstall(dist_info: Path) -> None:
    """Remove a dist's RECORD-listed files, then its dist-info, like `pip uninstall`."""
    site = dist_info.parent
    prefix = os.path.normpath(sys.prefix) + os.sep
    dirs: set[Path] = set()
    try:
        rows = list(csv.reader((dist_info / "RECORD").read_text("utf-8").splitlines()))
    except (OSError, UnicodeDecodeError):
        rows = []
    for row in rows:
        path = Path(os.path.normpath(site / row[0])) if row else None
        if path is None or not str(path).startswith(prefix) or path.is_dir():
            continue
        path.unlink(missing_ok=True)
        dirs.update(d for d in path.parents if site in d.parents)
    shutil.rmtree(dist_info, ignore_errors=True)
    # Deepest first; a left-over file from the newer version would shadow the reinstalled one.
    for d in sorted(dirs, key=lambda d: len(d.parts), reverse=True):
        shutil.rmtree(d / "__pycache__", ignore_errors=True)
        try:
            d.rmdir()
        except OSError:
            pass


def _repair_pip(site: Path) -> bool:
    """Reinstall pip offline from the interpreter's bundled wheel, as `python -m venv` does."""
    for dist_info in site.glob("pip-*.dist-info"):
        _uninstall(dist_info)
    # A cut can empty RECORD too; a newer pip's unlisted package dir then shadows the older wheel's module.
    shutil.rmtree(site / "pip", ignore_errors=True)
    # With a stale stash present, the next `pip install pip` of itself keeps the old dist-info and files.
    for stash in site.glob("~*"):
        if stash.is_dir() and _PIP_STASH.match(stash.name):
            shutil.rmtree(stash, ignore_errors=True)
    res = subprocess.run(  # nosec B603
        [sys.executable, "-m", "ensurepip", "--upgrade", "--default-pip"],
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    if _pip_works():
        return True
    _LOG.error("ensurepip rc=%s: %s", res.returncode, (res.stderr or "").strip()[-400:])
    return False


def _venv_cfg_ok() -> bool:
    """True while pyvenv.cfg isolates the venv; emptied by a cut, it lets system dists leak in."""
    try:
        text = Path(sys.prefix, "pyvenv.cfg").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return bool(_CFG_HOME.search(text) and _CFG_ISOLATED.search(text))


def _repair_venv_cfg() -> bool:
    """Rewrite pyvenv.cfg with CPython's own `venv --upgrade`, which leaves site-packages alone."""
    subprocess.run(  # nosec B603
        [
            os.path.realpath(sys.executable),
            "-m",
            "venv",
            "--upgrade",
            "--without-pip",
            sys.prefix,
        ],
        capture_output=True,
        timeout=300,
        check=False,
    )
    return _venv_cfg_ok()


def _pending_file() -> Path:
    """Survives a failed (offline) reinstall: the broken dist-info is already gone by then."""
    return Path(sys.prefix, ".blockscreen-venv-reinstall")


def _read_pending() -> list[str]:
    """Reinstalls a previous run could not finish."""
    try:
        return [
            ln
            for ln in _pending_file().read_text(encoding="utf-8").splitlines()
            if _PIN.match(ln)
        ]
    except OSError:
        return []


def _write_pending(reqs: list[str]) -> None:
    """Durably record the reinstall list before the dist-info dirs it names are removed."""
    tmp = _pending_file().with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        fh.write("".join(f"{r}\n" for r in reqs))
        fh.flush()
        os.fsync(fh.fileno())
    tmp.replace(_pending_file())
    # The rename is only durable once its directory is synced (pip PR #12859).
    dir_fd = os.open(tmp.parent, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


def heal() -> int:
    """0 = intact; 1 = damage handled this run (caller reinstalls its pins); 2 = repair still pending."""
    if sys.prefix == sys.base_prefix:
        _LOG.error(
            "not inside a venv (pyvenv.cfg missing?) - refusing to touch %s", sys.prefix
        )
        return 2
    rc = 0
    if not _venv_cfg_ok():
        _LOG.warning("pyvenv.cfg damaged - rewriting it")
        if not _repair_venv_cfg():
            _LOG.error("pyvenv.cfg repair failed")
            return 2
        rc = 1
    site = _site_packages()
    broken = broken_dists(site)
    pending = _read_pending()
    for req, dist_info in broken:
        _LOG.warning("truncated distribution %s (%s)", req, dist_info.name)
        if _PIN.match(req) and req not in pending:
            pending.append(req)
    if broken:
        _write_pending(pending)
        # A working pip skips a dist-info with no valid METADATA and cannot uninstall one without RECORD.
        for _, dist_info in broken:
            _uninstall(dist_info)
    if broken:
        rc = 1
    if not _pip_works():
        _LOG.warning("pip unusable - reinstalling it from the bundled wheel")
        if not _repair_pip(site):
            _LOG.error("pip repair failed")
            return 2
        rc = 1
    if pending:
        res = subprocess.run(  # nosec B603 - pending lines all match _PIN
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--quiet",
                "--no-deps",
                "--force-reinstall",
                "--no-cache-dir",
                *pending,
            ],
            timeout=1800,
            check=False,
        )
        if res.returncode != 0:
            _LOG.warning("reinstall of %s deferred (offline?)", " ".join(pending))
            return rc or 2
        _pending_file().unlink(missing_ok=True)
        _LOG.info("reinstalled %s", " ".join(pending))
        rc = 1
    return rc


def pins_installed(reqs: Path) -> int:
    """0 when every `name==version` pin in REQS is the installed version (pip's exit code is not proof)."""
    wrong = []
    for line in reqs.read_text(encoding="utf-8").splitlines():
        m = _PIN.match(line.strip())
        if not m:
            continue
        try:
            have = importlib.metadata.version(m[1])
        except importlib.metadata.PackageNotFoundError:
            have = None
        if have != m[2]:
            wrong.append(f"{m[1]}=={m[2]} (have {have})")
    for w in wrong:
        _LOG.error("pin not installed: %s", w)
    return 1 if wrong else 0


def main() -> int:
    """CLI entry: heal by default, `--pins REQS` to verify an install."""
    logging.basicConfig(
        stream=sys.stdout, level=logging.INFO, format="[bs-venv-heal] %(message)s"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pins", type=Path, help="verify these pins instead of healing"
    )
    args = parser.parse_args()
    return pins_installed(args.pins) if args.pins else heal()


if __name__ == "__main__":
    sys.exit(main())
