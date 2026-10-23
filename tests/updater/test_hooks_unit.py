"""Tests for the per-component shell hooks in updater/hooks/."""

from __future__ import annotations

import os
import re
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
_NOT_ROOT = pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file modes")
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
    tmp_path: Path,
    home: Path,
    prev: str = "",
    new: str = "",
    hook: Path = HH_HOOK,
    **extra: str,
) -> subprocess.CompletedProcess:
    """Run a Happy-Hare/Moonraker hook with a stub sudo that records its argv."""
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
        **extra,
    }
    return subprocess.run(
        ["bash", str(hook)], env=env, capture_output=True, text=True, check=False
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
            "-n systemctl --no-block restart moonraker.service"
        ]

    def test_restart_argv_matches_sudoers_rule(self, tmp_path, hh_home):
        _run_hh_hook(tmp_path, hh_home)
        root = HOOK.parents[2]
        rule = re.search(
            r"NOPASSWD: /usr/bin/(systemctl --no-block restart) %s",
            (root / "scripts" / "install-updater.sh").read_text(),
        )
        assert rule is not None
        manifest = (root / "updater" / "components.yaml").read_text()
        assert re.search(r"^\s*service: moonraker\.service$", manifest, re.M)
        assert _sudo_calls(tmp_path) == [f"-n {rule[1]} moonraker.service"]

    def test_pending_moonraker_restart_skips_restart(self, tmp_path, hh_home):
        result = _run_hh_hook(
            tmp_path,
            hh_home,
            BS_UPDATER_PENDING_RESTARTS="klipper.service moonraker.service",
        )
        assert result.returncode == 0, result.stderr
        assert _sudo_calls(tmp_path) == []

    def test_other_pending_restarts_still_restart(self, tmp_path, hh_home):
        result = _run_hh_hook(
            tmp_path, hh_home, BS_UPDATER_PENDING_RESTARTS="klipper.service"
        )
        assert result.returncode == 0, result.stderr
        assert len(_sudo_calls(tmp_path)) == 1

    def test_link_only_skips_restart(self, tmp_path, hh_home):
        result = _run_hh_hook(tmp_path, hh_home, HH_LINK_ONLY="1")
        assert result.returncode == 0, result.stderr
        assert (
            hh_home / "moonraker" / "moonraker" / "components" / "mmu_server.py"
        ).is_symlink()
        assert _sudo_calls(tmp_path) == []

    def test_printing_links_without_restart(self, tmp_path, hh_home):
        result = _run_hh_hook(tmp_path, hh_home, BS_UPDATER_PRINTING="1")
        assert result.returncode == 0, result.stderr
        assert (
            hh_home / "moonraker" / "moonraker" / "components" / "mmu_server.py"
        ).is_symlink()
        assert _sudo_calls(tmp_path) == []

    @_NOT_ROOT
    def test_unwritable_exclude_warns_and_links(self, tmp_path, hh_home):
        info = hh_home / "moonraker" / ".git" / "info"
        info.mkdir(exist_ok=True)
        (info / "exclude").write_text("*.pyc\n")
        (info / "exclude").chmod(0o444)
        try:
            result = _run_hh_hook(tmp_path, hh_home)
        finally:
            (info / "exclude").chmod(0o644)
        assert result.returncode == 0, result.stderr
        assert "WARN" in result.stdout
        assert (
            hh_home / "moonraker" / "moonraker" / "components" / "mmu_server.py"
        ).is_symlink()

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


MR_HOOK = HOOK.with_name("moonraker.sh")
_EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


class TestMoonrakerHook:
    """A Moonraker reclone must get the mmu_server link back."""

    def _run(self, tmp_path: Path, home: Path, prev: str = "abc"):
        return _run_hh_hook(
            tmp_path,
            home,
            prev,
            hook=MR_HOOK,
            COMPONENT_PATH=str(home / "moonraker"),
        )

    def _dst(self, home: Path) -> Path:
        return home / "moonraker" / "moonraker" / "components" / "mmu_server.py"

    def test_update_relinks_without_restart(self, tmp_path, hh_home):
        result = self._run(tmp_path, hh_home)
        assert result.returncode == 0, result.stderr
        assert self._dst(hh_home).is_symlink()
        assert "/moonraker/components/mmu_server.py" in _exclude(hh_home)
        assert _sudo_calls(tmp_path) == []

    def test_boot_reclone_relinks_and_restarts(self, tmp_path, hh_home):
        result = self._run(tmp_path, hh_home, _EMPTY_TREE)
        assert result.returncode == 0, result.stderr
        assert self._dst(hh_home).is_symlink()
        assert _sudo_calls(tmp_path) == [
            "-n systemctl --no-block restart moonraker.service"
        ]

    def test_intact_link_restores_exclude_without_restart(self, tmp_path, hh_home):
        _run_hh_hook(tmp_path, hh_home)
        exclude = hh_home / "moonraker" / ".git" / "info" / "exclude"
        exclude.write_text("")
        result = self._run(tmp_path, hh_home, _EMPTY_TREE)
        assert result.returncode == 0, result.stderr
        assert self._dst(hh_home).is_symlink()
        assert "/moonraker/components/mmu_server.py" in _exclude(hh_home)
        assert len(_sudo_calls(tmp_path)) == 1

    def test_no_happy_hare_skips(self, tmp_path, hh_home):
        subprocess.run(["rm", "-rf", str(hh_home / "Happy-Hare")], check=True)
        result = self._run(tmp_path, hh_home)
        assert result.returncode == 0, result.stderr
        assert not self._dst(hh_home).exists()

    def test_removes_link_left_by_failed_provision(self, tmp_path, hh_home):
        _run_hh_hook(tmp_path, hh_home)
        subprocess.run(["rm", "-rf", str(hh_home / "Happy-Hare")], check=True)
        result = self._run(tmp_path, hh_home)
        assert result.returncode == 0, result.stderr
        assert not self._dst(hh_home).is_symlink()

    def test_keeps_foreign_link_without_happy_hare(self, tmp_path, hh_home):
        subprocess.run(["rm", "-rf", str(hh_home / "Happy-Hare")], check=True)
        self._dst(hh_home).symlink_to(tmp_path / "elsewhere.py")
        result = self._run(tmp_path, hh_home)
        assert result.returncode == 0, result.stderr
        assert self._dst(hh_home).is_symlink()

    @_NOT_ROOT
    def test_relink_failure_never_fails_hook(self, tmp_path, hh_home):
        components = self._dst(hh_home).parent
        components.chmod(0o555)
        try:
            result = self._run(tmp_path, hh_home)
        finally:
            components.chmod(0o755)
        assert result.returncode == 0, result.stderr
        assert "WARN" in result.stdout


UI_HOOK = HOOK.with_name("BlocksScreen.sh")


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
