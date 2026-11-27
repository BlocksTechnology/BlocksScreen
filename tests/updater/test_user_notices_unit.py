"""Reboot-required detection, apt cooldown reason and apt history events."""

import json
import os
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from updater import executor
from updater.models import APT_COOLING_DOWN, ComponentConfig, ComponentStatus
from updater.service import UpdateService

_BOOT = time.mktime(time.strptime("2026-11-26 12:00:00", "%Y-%m-%d %H:%M:%S"))


@pytest.fixture
def dpkg_log(tmp_path, monkeypatch):
    """Point the detector at a tmp dpkg.log written after a fixed boot time."""
    log = tmp_path / "dpkg.log"
    monkeypatch.setattr(executor, "_DPKG_LOGS", (log,))
    monkeypatch.setattr(executor, "_REBOOT_REQUIRED_FLAG", tmp_path / "reboot-flag")
    monkeypatch.setattr(executor, "_boot_wall_time", lambda: _BOOT)
    return log


def _write(log, line: str, mtime: float = _BOOT + 3600) -> None:
    log.write_text(line + "\n", encoding="utf-8")
    os.utime(log, (mtime, mtime))


class TestRebootRequired:
    @pytest.mark.parametrize(
        ("line", "expected"),
        [
            (
                "2026-11-26 13:00:00 upgrade libc6:arm64 2.36-9+deb12u8 2.36-9+deb12u9",
                True,
            ),
            (
                "2026-11-26 13:00:00 install linux-image-6.6.62+rpt-rpi-v8:arm64 <none> 1:6.6.62-1",
                True,
            ),
            (
                "2026-11-26 13:00:00 status installed dbus:arm64 1.14.10-1~deb12u1",
                False,
            ),
            ("2026-11-26 13:00:00 upgrade systemd:arm64 252.30-1 252.30-1", False),
            (
                "2026-11-26 11:00:00 upgrade libc6:arm64 2.36-9+deb12u8 2.36-9+deb12u9",
                False,
            ),
            ("2026-11-26 13:00:00 upgrade nano:arm64 7.2-1 7.2-2", False),
            ("not a dpkg line", False),
        ],
        ids=["libc", "kernel", "trigger", "reinstall", "before-boot", "other", "junk"],
    )
    def test_core_upgrade_after_boot(self, dpkg_log, line, expected) -> None:
        _write(dpkg_log, line)
        assert executor.reboot_required() is expected

    def test_log_untouched_since_boot_is_skipped(self, dpkg_log) -> None:
        _write(dpkg_log, "2026-11-26 13:00:00 upgrade libc6:arm64 a b", _BOOT - 60)
        assert executor.reboot_required() is False

    def test_debian_flag_file_counts(self, dpkg_log, tmp_path) -> None:
        (tmp_path / "reboot-flag").touch()
        assert executor.reboot_required() is True


class TestRebootFlagInStatus:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("pending", "trusted", "expected"),
        [(True, True, True), (True, False, False), (False, True, False)],
        ids=["pending", "clock-untrusted", "none"],
    )
    async def test_flag_needs_trusted_clock(
        self, reboot_required, pending, trusted, expected
    ) -> None:
        reboot_required.return_value = pending
        component = ComponentConfig(name="system", kind="apt")
        apt = ComponentStatus(name="system", kind="apt")
        with (
            patch(
                "updater.service.load_components", return_value=([component], 3600.0)
            ),
            patch("updater.service.check_apt_status", AsyncMock(return_value=apt)),
            patch("updater.service.apt_update", AsyncMock(return_value=(True, ""))),
            patch("updater.service.clock_trusted", AsyncMock(return_value=trusted)),
        ):
            status = await UpdateService().check_status()
        assert status["system"].reboot_required is expected


def _events(svc: UpdateService) -> list[dict]:
    if not svc._history_path.exists():
        return []
    lines = svc._history_path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


class TestAptCooldownAndHistory:
    @pytest.mark.asyncio
    async def test_cooldown_press_says_when_to_retry(self) -> None:
        cb = MagicMock()
        svc = UpdateService(callback=cb)
        svc._apt_backoff.trip()
        assert await svc.update_component("system") is False
        cb.on_error.assert_called_once_with("system", f"{APT_COOLING_DOWN}: 1 min")
        assert _events(svc)[-1] | {"ts": ""} == {
            "ts": "",
            "event": "apt_upgrade",
            "component": "system",
            "ok": False,
        }

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("update", "upgrade", "expected"),
        [
            ((True, ""), (True, ""), True),
            ((True, ""), (False, "E: x"), False),
            ((False, "net"), None, False),
        ],
        ids=["ok", "upgrade-fails", "update-fails"],
    )
    async def test_sweep_run_is_recorded(self, update, upgrade, expected) -> None:
        svc = UpdateService()
        with (
            patch("updater.service.apt_update", AsyncMock(return_value=update)),
            patch("updater.service.apt_upgrade", AsyncMock(return_value=upgrade)),
            patch("updater.service.apt_autoremove", AsyncMock(return_value=(True, ""))),
        ):
            await svc.background_apt_upgrade()
        sweeps = [e for e in _events(svc) if e["event"] == "apt_sweep"]
        assert [e["ok"] for e in sweeps] == [expected]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("skip", ["printing", "cooldown"])
    async def test_skipped_sweep_is_not_recorded(self, printing, skip) -> None:
        svc = UpdateService()
        if skip == "printing":
            printing.return_value = True
        else:
            svc._apt_backoff.trip()
        with patch("updater.service.apt_update", AsyncMock()) as mock_update:
            await svc.background_apt_upgrade()
        mock_update.assert_not_called()
        assert not [e for e in _events(svc) if e["event"] == "apt_sweep"]
