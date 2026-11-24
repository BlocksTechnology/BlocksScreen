"""Tests for scripts/bs-tree-guard.sh against a real git repo with power-cut-emptied files."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="needs git")

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "bs-tree-guard.sh"
_FILES = {
    "scripts/start.sh": "#!/bin/bash\necho start\n",
    "BlocksScreen/__init__.py": "",
    "a[1].txt": "glob name\n",
    "a1.txt": "sibling\n",
}


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout


@pytest.fixture
def env(tmp_path: Path) -> dict[str, str]:
    """PATH with a systemctl stub that logs its arguments."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    stub = bindir / "systemctl"
    stub.write_text(f'#!/bin/sh\necho "$*" >> {tmp_path / "systemctl.log"}\n')
    stub.chmod(0o755)
    return {
        **os.environ,
        "PATH": f"{bindir}:{os.environ['PATH']}",
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@t",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@t",
        "GIT_CONFIG_GLOBAL": "/dev/null",
    }


@pytest.fixture
def repo(tmp_path: Path, env: dict[str, str]) -> Path:
    """A committed tree with a legitimately empty file and a glob-like name."""
    repo = tmp_path / "BlocksScreen"
    for name, text in _FILES.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text)
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "init"]):
        subprocess.run(["git", "-C", str(repo), *args], check=True, env=env)
    return repo


def _run(repo: Path, home: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(_SCRIPT), str(repo), str(home)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )


def _flag(home: Path) -> Path:
    return home / ".config" / "blockscreen" / ".run-install-updater"


def test_clean_tree_is_untouched(repo, tmp_path, env):
    res = _run(repo, tmp_path / "home", env)
    assert res.returncode == 0
    assert not _flag(tmp_path / "home").exists()
    assert not (tmp_path / "systemctl.log").exists()


def test_restores_emptied_files_and_rearms_deploy(repo, tmp_path, env):
    (repo / "scripts/start.sh").write_text("")
    (repo / "a[1].txt").write_text("")
    (repo / "a1.txt").write_text("local edit\n")
    res = _run(repo, tmp_path / "home", env)
    assert res.returncode == 0, res.stderr
    assert (repo / "scripts/start.sh").read_text() == _FILES["scripts/start.sh"]
    assert (repo / "a[1].txt").read_text() == _FILES["a[1].txt"]
    # Literal pathspec: the glob name must not reset its sibling.
    assert (repo / "a1.txt").read_text() == "local edit\n"
    assert (repo / "BlocksScreen/__init__.py").read_text() == ""
    assert _flag(tmp_path / "home").exists()
    assert "daemon-reload" in (tmp_path / "systemctl.log").read_text()


def test_heal_outside_scripts_skips_redeploy(repo, tmp_path, env):
    (repo / "a[1].txt").write_text("")
    res = _run(repo, tmp_path / "home", env)
    assert res.returncode == 0, res.stderr
    assert (repo / "a[1].txt").read_text() == _FILES["a[1].txt"]
    assert not _flag(tmp_path / "home").exists()
    assert not (tmp_path / "systemctl.log").exists()


def test_rebuilds_a_truncated_index(repo, tmp_path, env):
    (repo / "scripts/start.sh").write_text("")
    (repo / ".git/index").write_bytes(b"")
    res = _run(repo, tmp_path / "home", env)
    assert res.returncode == 0, res.stderr
    assert (repo / "scripts/start.sh").read_text() == _FILES["scripts/start.sh"]
    assert _git(repo, "status", "--porcelain") == ""


def test_unreadable_head_resets_to_last_good(repo, tmp_path, env):
    good = _git(repo, "rev-parse", "HEAD").strip()
    (repo / "scripts/start.sh").write_text("#!/bin/bash\necho v2\n")
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-qam", "v2"], check=True, env=env
    )
    bad = _git(repo, "rev-parse", "HEAD").strip()
    (repo / ".git/objects" / bad[:2] / bad[2:]).chmod(0o644)
    (repo / ".git/objects" / bad[:2] / bad[2:]).write_bytes(b"")
    (repo / "scripts/start.sh").write_text("")
    cache = tmp_path / "home" / ".cache" / "blockscreen"
    cache.mkdir(parents=True)
    (cache / "last_good_commit").write_text(f"{good}\n")
    res = _run(repo, tmp_path / "home", env)
    assert res.returncode == 0, res.stderr
    assert _git(repo, "rev-parse", "HEAD").strip() == good
    assert (repo / "scripts/start.sh").read_text() == _FILES["scripts/start.sh"]
    assert _flag(tmp_path / "home").exists()


def test_emptied_branch_ref_resets_to_local_remote_ref_offline(repo, tmp_path, env):
    head = _git(repo, "rev-parse", "HEAD").strip()
    branch = _git(repo, "symbolic-ref", "--short", "HEAD").strip()
    _git(repo, "update-ref", f"refs/remotes/origin/{branch}", head)
    (repo / ".git/refs/heads" / branch).write_bytes(b"")  # cut mid ref update
    (repo / "scripts/start.sh").write_text("")
    res = _run(repo, tmp_path / "home", env)  # no last_good, no reachable remote
    assert res.returncode == 0, res.stderr
    assert f"reset to local origin/{branch}" in res.stdout
    assert "No such file" not in res.stderr
    assert _git(repo, "rev-parse", "HEAD").strip() == head
    assert (repo / "scripts/start.sh").read_text() == _FILES["scripts/start.sh"]
    assert _flag(tmp_path / "home").exists()


_V2 = "#!/bin/bash\necho v2\n"


def _commit_v2(repo: Path, env: dict[str, str]) -> tuple[str, str]:
    """Commit a second version of start.sh; returns (v1, v2) hashes."""
    v1 = _git(repo, "rev-parse", "HEAD").strip()
    (repo / "scripts/start.sh").write_text(_V2)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-qam", "v2"], check=True, env=env
    )
    return v1, _git(repo, "rev-parse", "HEAD").strip()


def _last_good(home: Path, commit: str) -> None:
    cache = home / ".cache" / "blockscreen"
    cache.mkdir(parents=True)
    (cache / "last_good_commit").write_text(f"{commit}\n")


def test_emptied_loose_ref_does_not_fall_back_to_packed_ref(repo, tmp_path, env):
    # Packed at v1, as after gc --auto.
    subprocess.run(["git", "-C", str(repo), "pack-refs", "--all"], check=True, env=env)
    _, v2 = _commit_v2(repo, env)
    branch = _git(repo, "symbolic-ref", "--short", "HEAD").strip()
    (repo / ".git/refs/heads" / branch).write_bytes(b"")
    (repo / "scripts/start.sh").write_text("")
    _last_good(tmp_path / "home", v2)
    res = _run(repo, tmp_path / "home", env)
    assert res.returncode == 0, res.stderr
    assert _git(repo, "rev-parse", "HEAD").strip() == v2
    assert (repo / "scripts/start.sh").read_text() == _V2


def test_emptied_ref_and_index_still_reset(repo, tmp_path, env):
    head = _git(repo, "rev-parse", "HEAD").strip()
    branch = _git(repo, "symbolic-ref", "--short", "HEAD").strip()
    (repo / ".git/refs/heads" / branch).write_bytes(b"")
    (repo / ".git/index").write_bytes(b"")
    (repo / "scripts/start.sh").write_text("")
    _last_good(tmp_path / "home", head)
    res = _run(repo, tmp_path / "home", env)
    assert res.returncode == 0, res.stderr
    assert _git(repo, "rev-parse", "HEAD").strip() == head
    assert (repo / "scripts/start.sh").read_text() == _FILES["scripts/start.sh"]
    assert _git(repo, "status", "--porcelain") == ""


def test_emptied_blob_falls_back_to_last_good(repo, tmp_path, env):
    v1, _ = _commit_v2(repo, env)
    blob = _git(repo, "rev-parse", "HEAD:scripts/start.sh").strip()
    obj = repo / ".git/objects" / blob[:2] / blob[2:]
    obj.chmod(0o644)
    obj.write_bytes(b"")  # loose objects are not fsynced by default
    (repo / "scripts/start.sh").write_text("")
    _last_good(tmp_path / "home", v1)
    res = _run(repo, tmp_path / "home", env)
    assert res.returncode == 0, res.stderr
    assert "restore failed, resetting" in res.stdout
    assert _git(repo, "rev-parse", "HEAD").strip() == v1
    assert (repo / "scripts/start.sh").read_text() == _FILES["scripts/start.sh"]
    assert _flag(tmp_path / "home").exists()


def test_emptied_orig_head_is_removed_so_the_next_pull_works(repo, tmp_path, env):
    (repo / ".git/ORIG_HEAD").write_bytes(b"")  # cut right after a pull
    res = _run(repo, tmp_path / "home", env)
    assert res.returncode == 0, res.stderr
    assert not (repo / ".git/ORIG_HEAD").exists()
    # Every pull and reset writes ORIG_HEAD first; an empty one fails this as "broken".
    _git(repo, "update-ref", "ORIG_HEAD", "HEAD")
    assert not _flag(tmp_path / "home").exists()


def test_unit_ordered_before_moonraker():
    unit = _SCRIPT.with_name("BlocksScreen-tree-guard.service").read_text()
    assert "Before=moonraker.service" in unit


def test_post_merge_syncs_the_tree_on_a_moonraker_pull(tmp_path: Path) -> None:
    """Moonraker pulls exit post-merge early; the new tree must still be synced first."""
    scripts = tmp_path / "repo" / "scripts"
    scripts.mkdir(parents=True)
    hook = scripts / "post-merge"
    shutil.copy(_SCRIPT.parent / "post-merge", hook)
    (scripts / "bs-common.sh").write_text("bs_in_moonraker_cgroup() { return 0; }\n")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "sync.log"
    stub = bindir / "sync"
    stub.write_text(f'#!/bin/sh\necho "$*" >> {log}\n')
    stub.chmod(0o755)
    getent = bindir / "getent"
    getent.write_text(f"#!/bin/sh\necho blocks:x:1000:1000::{tmp_path}:/bin/bash\n")
    getent.chmod(0o755)
    res = subprocess.run(
        ["bash", str(hook)],
        capture_output=True,
        check=False,
        env={**os.environ, "PATH": f"{bindir}:{os.environ['PATH']}"},
        text=True,
        timeout=20,
    )
    assert res.returncode == 0, res.stderr
    assert "under moonraker" in res.stdout
    assert log.read_text().split() == ["-f", str(tmp_path / "repo")]
