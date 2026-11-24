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


def test_unit_ordered_before_moonraker():
    unit = _SCRIPT.with_name("BlocksScreen-tree-guard.service").read_text()
    assert "Before=moonraker.service" in unit
