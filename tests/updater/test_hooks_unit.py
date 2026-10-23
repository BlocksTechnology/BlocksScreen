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


HH_HOOK = HOOK.parent / "Happy-Hare.sh"
_MOONRAKER_CONF = (
    "[server]\nhost: 0.0.0.0\n\n[mmu_server]\nenable_file_preprocessor: True\n"
)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@t",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


@pytest.fixture
def hh_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    hh = home / "Happy-Hare"
    (hh / "components").mkdir(parents=True)
    (hh / "components" / "mmu_server.py").write_text("v1\n")
    _git(hh, "init", "-q")
    _git(hh, "add", ".")
    _git(hh, "commit", "-qm", "v1")
    components = home / "moonraker" / "moonraker" / "components"
    components.mkdir(parents=True)
    _git(home / "moonraker", "init", "-q")
    conf = home / "printer_data" / "config" / "moonraker.conf"
    conf.parent.mkdir(parents=True)
    conf.write_text(_MOONRAKER_CONF)
    return home


def _run_hh_hook(
    tmp_path: Path, home: Path, prev: str = "", new: str = ""
) -> subprocess.CompletedProcess:
    """Run the Happy-Hare hook with a stub sudo that records its argv."""
    stub_bin = tmp_path / "stub-bin"
    stub_bin.mkdir(exist_ok=True)
    sudo = stub_bin / "sudo"
    sudo.write_text(f'#!/bin/bash\necho "$*" >>{tmp_path}/sudo.log\n')
    sudo.chmod(0o755)
    env = {
        "PATH": f"{stub_bin}:{os.environ['PATH']}",
        "HOME": str(home),
        "COMPONENT_PATH": str(home / "Happy-Hare"),
        "PREV_HASH": prev,
        "NEW_HASH": new,
    }
    return subprocess.run(
        ["bash", str(HH_HOOK)], env=env, capture_output=True, text=True, check=False
    )


def _sudo_calls(tmp_path: Path) -> list[str]:
    log = tmp_path / "sudo.log"
    return log.read_text().splitlines() if log.exists() else []


def _exclude(home: Path) -> list[str]:
    return (home / "moonraker" / ".git" / "info" / "exclude").read_text().splitlines()


class TestHappyHareHook:
    def test_provision_links_excludes_and_restarts(self, tmp_path, hh_home):
        result = _run_hh_hook(tmp_path, hh_home)
        assert result.returncode == 0, result.stderr
        dst = hh_home / "moonraker" / "moonraker" / "components" / "mmu_server.py"
        assert dst.resolve() == hh_home / "Happy-Hare" / "components" / "mmu_server.py"
        assert "/moonraker/components/mmu_server.py" in _exclude(hh_home)
        assert _git(hh_home / "moonraker", "status", "--porcelain") == ""
        assert _sudo_calls(tmp_path) == [
            "systemctl restart --no-block moonraker.service"
        ]

    def test_unchanged_update_is_idempotent(self, tmp_path, hh_home):
        _run_hh_hook(tmp_path, hh_home)
        head = _git(hh_home / "Happy-Hare", "rev-parse", "HEAD")
        result = _run_hh_hook(tmp_path, hh_home, head, head)
        assert result.returncode == 0, result.stderr
        assert _exclude(hh_home).count("/moonraker/components/mmu_server.py") == 1
        assert len(_sudo_calls(tmp_path)) == 1

    def test_changed_mmu_server_restarts(self, tmp_path, hh_home):
        _run_hh_hook(tmp_path, hh_home)
        hh = hh_home / "Happy-Hare"
        prev = _git(hh, "rev-parse", "HEAD")
        (hh / "components" / "mmu_server.py").write_text("v2\n")
        _git(hh, "commit", "-qam", "v2")
        result = _run_hh_hook(tmp_path, hh_home, prev, _git(hh, "rev-parse", "HEAD"))
        assert result.returncode == 0, result.stderr
        assert len(_sudo_calls(tmp_path)) == 2

    def test_no_mmu_server_section_skips_restart(self, tmp_path, hh_home):
        (hh_home / "printer_data" / "config" / "moonraker.conf").write_text(
            "[server]\n"
        )
        result = _run_hh_hook(tmp_path, hh_home)
        assert result.returncode == 0, result.stderr
        assert (
            hh_home / "moonraker" / "moonraker" / "components" / "mmu_server.py"
        ).is_symlink()
        assert _sudo_calls(tmp_path) == []

    def test_replaces_copied_file(self, tmp_path, hh_home):
        dst = hh_home / "moonraker" / "moonraker" / "components" / "mmu_server.py"
        dst.write_text("old copy\n")
        result = _run_hh_hook(tmp_path, hh_home)
        assert result.returncode == 0, result.stderr
        assert dst.is_symlink()

    def test_exclude_without_trailing_newline(self, tmp_path, hh_home):
        exclude = hh_home / "moonraker" / ".git" / "info" / "exclude"
        exclude.write_text("*.pyc")
        _run_hh_hook(tmp_path, hh_home)
        assert _exclude(hh_home) == ["*.pyc", "/moonraker/components/mmu_server.py"]

    def test_missing_moonraker_skips(self, tmp_path, hh_home):
        subprocess.run(["rm", "-rf", str(hh_home / "moonraker")], check=True)
        result = _run_hh_hook(tmp_path, hh_home)
        assert result.returncode == 0, result.stderr
        assert _sudo_calls(tmp_path) == []

    def test_missing_source_fails(self, tmp_path, hh_home):
        (hh_home / "Happy-Hare" / "components" / "mmu_server.py").unlink()
        result = _run_hh_hook(tmp_path, hh_home)
        assert result.returncode == 1
