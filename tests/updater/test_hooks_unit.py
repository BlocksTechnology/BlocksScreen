"""Tests for the per-component shell hooks in updater/hooks/."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[2] / "updater" / "hooks" / "DeviceDiscovery.sh"


def _run_hook(tmp_path: Path, repo: Path, load_state: str) -> subprocess.CompletedProcess:
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
