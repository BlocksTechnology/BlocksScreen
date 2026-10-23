"""Tests for the per-component shell hooks in updater/hooks/."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[2] / "updater" / "hooks" / "DeviceDiscovery.sh"


def _run_hook(
    tmp_path: Path, repo: Path, load_state: str
) -> subprocess.CompletedProcess:
    """Run the hook with a stub systemctl that reports load_state."""
    stub_bin = tmp_path / "stub-bin"
    stub_bin.mkdir()
    systemctl = stub_bin / "systemctl"
    systemctl.write_text(f"#!/bin/bash\necho {load_state}\n")
    systemctl.chmod(0o755)
    env = {
        "PATH": f"{stub_bin}:{os.environ['PATH']}",
        "COMPONENT_PATH": str(repo),
        "BS_UPDATER_SELF_UPDATE": "1",
        "BS_UPDATER_RESTART_SENTINEL": str(tmp_path / "run" / "sentinel"),
    }
    return subprocess.run(
        ["bash", str(HOOK)], env=env, capture_output=True, text=True, check=False
    )


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    repo = tmp_path / "DeviceDiscovery"
    (repo / "scripts").mkdir(parents=True)
    build = repo / "scripts" / "build.sh"
    build.write_text(f"#!/bin/bash\ntouch {repo}/built\n")
    build.chmod(0o755)
    return repo


def _install_binary(repo: Path) -> None:
    (repo / "bin").mkdir()
    binary = repo / "bin" / "device_discoveryd"
    binary.write_text("")
    binary.chmod(0o755)


class TestDeviceDiscoveryHook:
    def test_fresh_clone_defers_setup_to_install_updater(self, tmp_path, repo):
        result = _run_hook(tmp_path, repo, "not-found")
        assert result.returncode == 0, result.stderr
        assert (tmp_path / "run" / "sentinel").read_text().split() == ["install"]
        assert not (repo / "built").exists()

    def test_binary_without_unit_still_defers(self, tmp_path, repo):
        _install_binary(repo)
        result = _run_hook(tmp_path, repo, "not-found")
        assert result.returncode == 0, result.stderr
        assert (tmp_path / "run" / "sentinel").exists()
        assert not (repo / "built").exists()

    def test_set_up_machine_rebuilds(self, tmp_path, repo):
        _install_binary(repo)
        result = _run_hook(tmp_path, repo, "loaded")
        assert result.returncode == 0, result.stderr
        assert (repo / "built").exists()
        assert not (tmp_path / "run" / "sentinel").exists()


UI_HOOK = HOOK.with_name("BlocksScreen.sh")


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def _commit(repo: Path, files: dict[str, str]) -> str:
    for rel, text in files.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text)
    _git(repo, "add", "-A")
    _git(
        repo,
        "-c",
        "user.name=t",
        "-c",
        "user.email=t@t",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-qm",
        "c",
    )
    return _git(repo, "rev-parse", "HEAD")


class TestBlocksScreenHook:
    """Updater code or manifest changes must reach the daemon within the same Update."""

    @pytest.fixture
    def ui_repo(self, tmp_path: Path) -> Path:
        repo = tmp_path / "BlocksScreen"
        repo.mkdir()
        _git(repo, "init", "-q")
        return repo

    def _run(self, tmp_path: Path, repo: Path, prev: str, new: str, **extra: str):
        env = {
            "PATH": os.environ["PATH"],
            "HOME": str(tmp_path),
            "COMPONENT_PATH": str(repo),
            "PREV_HASH": prev,
            "NEW_HASH": new,
            "BS_UPDATER_SELF_UPDATE": "1",
            "BS_UPDATER_RESTART_SENTINEL": str(tmp_path / "run" / "sentinel"),
            **extra,
        }
        result = subprocess.run(
            ["bash", str(UI_HOOK)], env=env, capture_output=True, text=True, check=False
        )
        assert result.returncode == 0, result.stderr
        followup = tmp_path / ".cache" / "blockscreen" / "updater_followup"
        return tmp_path / "run" / "sentinel", followup

    def test_manifest_change_queues_followup_and_restart(self, tmp_path, ui_repo):
        prev = _commit(ui_repo, {"updater/components.yaml": "a: 1\n"})
        new = _commit(ui_repo, {"updater/components.yaml": "a: 2\n"})
        sentinel, followup = self._run(tmp_path, ui_repo, prev, new)
        assert sentinel.read_text().split() == ["code"]
        assert followup.read_text().strip() == prev

    def test_code_only_change_restarts_without_followup(self, tmp_path, ui_repo):
        prev = _commit(ui_repo, {"updater/service.py": "x = 1\n"})
        new = _commit(ui_repo, {"updater/service.py": "x = 2\n"})
        sentinel, followup = self._run(tmp_path, ui_repo, prev, new)
        assert sentinel.read_text().split() == ["code"]
        assert not followup.exists()

    def test_non_updater_change_does_nothing(self, tmp_path, ui_repo):
        prev = _commit(ui_repo, {"BlocksScreen/a.py": "1\n"})
        new = _commit(ui_repo, {"BlocksScreen/a.py": "2\n"})
        sentinel, followup = self._run(tmp_path, ui_repo, prev, new)
        assert not sentinel.exists()
        assert not followup.exists()

    def test_chained_updates_keep_oldest_base(self, tmp_path, ui_repo):
        first = _commit(ui_repo, {"updater/components.yaml": "a: 1\n"})
        mid = _commit(ui_repo, {"updater/components.yaml": "a: 2\n"})
        last = _commit(ui_repo, {"updater/components.yaml": "a: 3\n"})
        self._run(tmp_path, ui_repo, first, mid)
        _, followup = self._run(tmp_path, ui_repo, mid, last)
        assert followup.read_text().strip() == first

    def test_outside_updater_no_restart_sentinel(self, tmp_path, ui_repo):
        # CLI/manual runs: nothing defers the restart, so none is requested.
        prev = _commit(ui_repo, {"updater/components.yaml": "a: 1\n"})
        new = _commit(ui_repo, {"updater/components.yaml": "a: 2\n"})
        sentinel, followup = self._run(
            tmp_path, ui_repo, prev, new, BS_UPDATER_SELF_UPDATE=""
        )
        assert not sentinel.exists()
        assert followup.exists()
