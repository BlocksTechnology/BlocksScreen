"""The updater CLI (status/update/recover) must import without sdbus present."""

from __future__ import annotations

import asyncio
import builtins
import fcntl
import sys

import pytest


@pytest.fixture
def _no_sdbus(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "sdbus" or name.startswith("sdbus."):
            raise ModuleNotFoundError("No module named 'sdbus'")
        return real_import(name, *args, **kwargs)

    for mod in [m for m in sys.modules if m == "updater" or m.startswith("updater.")]:
        monkeypatch.delitem(sys.modules, mod, raising=False)
    monkeypatch.delitem(sys.modules, "sdbus", raising=False)
    monkeypatch.setattr(builtins, "__import__", fake_import)
    yield


def test_cli_module_imports_without_sdbus(_no_sdbus):
    import updater  # noqa: F401
    import updater.__main__ as cli

    assert hasattr(cli, "main")
    # The non-daemon subcommands must be constructible without sdbus.
    parser = cli.build_parser()
    args = parser.parse_args(["status"])
    assert args.command == "status"


def test_package_does_not_pull_in_sdbus(_no_sdbus):
    import updater  # noqa: F401

    assert "sdbus" not in sys.modules


def test_cli_lock_rejects_concurrent_run(monkeypatch, tmp_path):
    """A second mutating CLI run exits when the lock is already held."""
    # Local import: this module's other tests mask sdbus before importing updater.
    from updater import __main__ as cli
    from updater import locking

    lock_file = tmp_path / "updater.lock"
    monkeypatch.setattr(locking, "lock_path", lambda: lock_file)
    holder = open(lock_file, "w")
    fcntl.flock(holder, fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        with pytest.raises(SystemExit):
            with cli._cli_lock():
                pass
    finally:
        fcntl.flock(holder, fcntl.LOCK_UN)
        holder.close()


def test_status_surfaces_branch_mismatch(monkeypatch, capsys):
    """CLI status must report a branch_mismatch component, not print 'up to date'."""
    from updater import __main__ as cli
    from updater.models import ComponentStatus

    async def fake_check_status(self):
        return {
            "RF50-Klipper": ComponentStatus(name="RF50-Klipper", branch_mismatch=True)
        }

    monkeypatch.setattr(cli.UpdateService, "check_status", fake_check_status)
    monkeypatch.setattr(sys, "argv", ["updater", "status"])
    asyncio.run(cli.main())
    out = capsys.readouterr().out
    assert "RF50-Klipper: branch switch needed" in out


class TestWatchdogPingInterval:
    """The watchdog heartbeat reads WatchdogSec from the environment (sd_notify(3))."""

    def test_reads_half_of_watchdog_usec(self, monkeypatch):
        from updater.__main__ import _watchdog_ping_interval

        monkeypatch.setenv("WATCHDOG_USEC", "30000000")  # 30s
        assert _watchdog_ping_interval() == 15.0

    def test_falls_back_to_15s_when_unset(self, monkeypatch):
        from updater.__main__ import _watchdog_ping_interval

        monkeypatch.delenv("WATCHDOG_USEC", raising=False)
        assert _watchdog_ping_interval() == 15.0

    def test_falls_back_to_15s_when_invalid(self, monkeypatch):
        from updater.__main__ import _watchdog_ping_interval

        monkeypatch.setenv("WATCHDOG_USEC", "not-a-number")
        assert _watchdog_ping_interval() == 15.0
