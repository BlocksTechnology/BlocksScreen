"""UpdaterDbusService end to end: busy/overlay contract, boot pass, deploy hold, cancel."""

import asyncio
import os
from unittest.mock import AsyncMock

import pytest

UI_FILES = {
    "updater/dbus_service.py": "# marker\n",
    "scripts/install-updater.sh": "v1\n",
}


def _idle(d) -> bool:
    """No update/recover task is still running on the daemon."""
    return not any(
        t.get_name().startswith(("update_", "recover_")) and not t.done()
        for t in d.iface._background_tasks
    )


async def _booted(daemon, wait_for):
    """Start a daemon and wait for its first status emit."""
    d = daemon()
    await wait_for(lambda: d.statuses(), what="boot status")
    return d


async def test_update_all_round_trip(harness, daemon, wait_for):
    origin = harness.remote("klipper")
    harness.install(origin)
    new = origin.commit({"klippy.py": "v2\n"})
    harness.component("klipper", service="klipper.service")
    d = await _booted(daemon, wait_for)
    assert d.statuses()[0]["klipper"]["commits_behind"] == 1

    assert await d.iface.update_all() is True
    assert await d.iface.update_all() is False  # busy rejects a second run
    await wait_for(lambda: d.busy_trace() == [True, False], what="busy release")

    assert harness.head("klipper") == new
    steps = [a for a in d.signals("step_complete") if a[0] == "klipper"]
    assert steps == [("klipper", n, 4) for n in (1, 2, 3, 4)]
    assert d.signals("component_done") == [("klipper", True)]
    await wait_for(lambda: harness.apt_upgrade.await_count == 1, what="apt upgrade")

    seen = len(d.statuses())
    await d.iface.request_status()
    await wait_for(lambda: len(d.statuses()) > seen, what="fresh status")
    assert d.statuses()[-1]["klipper"]["commits_behind"] == 0


async def test_nothing_dirty_still_releases_busy(harness, daemon, wait_for):
    harness.install(harness.remote("klipper"))
    harness.component("klipper", service="klipper.service")
    d = await _booted(daemon, wait_for)

    assert await d.iface.update_all() is True
    await wait_for(lambda: d.busy_trace() == [True, False], what="busy release")

    assert d.signals("step_complete") == []


async def test_print_started_after_confirm_refuses_update(
    harness, daemon, wait_for, monkeypatch
):
    origin = harness.remote("klipper")
    harness.install(origin)
    old = harness.head("klipper")
    origin.commit({"klippy.py": "v2\n"})
    harness.component("klipper", service="klipper.service")
    d = await _booted(daemon, wait_for)
    monkeypatch.setitem(
        harness.dbus_g, "klipper_printing", AsyncMock(return_value=True)
    )

    assert await d.iface.update_all() is True
    await wait_for(lambda: d.busy_trace() == [True, False], what="busy release")

    assert harness.head("klipper") == old
    assert d.signals("error") == [("updater", harness.dbus_g["PRINTER_BUSY"])]
    assert d.signals("step_complete") == []


async def test_failed_update_releases_busy_and_reports(harness, daemon, wait_for):
    origin = harness.remote("klipper")
    harness.install(origin)
    old = harness.head("klipper")
    origin.commit({"klippy.py": "v2\n"})
    harness.component("klipper", service="klipper.service")
    harness.hook("klipper", "exit 1\n")
    d = await _booted(daemon, wait_for)

    assert await d.iface.update_all() is True
    await wait_for(lambda: d.busy_trace() == [True, False], what="busy release")

    assert harness.head("klipper") == old
    assert d.signals("error") == [("klipper", "hook")]
    assert d.signals("rollback") == [("klipper", True)]
    assert d.signals("component_done") == [("klipper", False)]


async def test_install_update_holds_overlay_until_deploy_finishes(
    harness, daemon, wait_for
):
    origin = harness.remote("BlocksScreen", UI_FILES)
    harness.install(origin)
    origin.commit({"scripts/install-updater.sh": "v2\n"})
    harness.component("BlocksScreen", service="BlocksScreen.service")
    harness.real_hook("BlocksScreen")
    d = await _booted(daemon, wait_for)

    assert await d.iface.update_all() is True
    await wait_for(harness.deploy_flag.exists, what="deploy flag")
    await wait_for(lambda: _idle(d), what="batch end")
    await asyncio.sleep(0.3)  # several hold polls

    # Batch done, install-updater still running: the overlay must not drop.
    assert d.busy_trace() == [True]
    assert await d.iface.get_busy() is True
    assert await d.iface.update_all() is False
    harness.apt_upgrade.assert_not_awaited()

    harness.deploy_flag.unlink()  # install-updater's ExecStopPost
    await wait_for(lambda: d.busy_trace() == [True, False], what="hold release")


async def test_deploy_hold_is_capped(harness, daemon, wait_for):
    harness.mp.setitem(harness.dbus_g, "_DEPLOY_HOLD_CAP_S", 0.3)
    harness.deploy_flag.parent.mkdir(parents=True)
    harness.deploy_flag.touch()  # a hung install-updater never clears it

    d = daemon()
    assert await d.iface.get_busy() is True

    await wait_for(lambda: d.busy_trace() == [False], timeout=5.0, what="cap")
    assert harness.deploy_flag.exists()

    origin = harness.remote("klipper")
    harness.install(origin)
    origin.commit({"klippy.py": "v2\n"})
    harness.component("klipper", service="klipper.service")
    assert await d.iface.update_all() is True
    # The same stuck flag must not re-hold at the end of every update.
    await wait_for(lambda: d.busy_trace() == [False, True, False], what="no re-hold")
    assert d.iface._deploy_hold is None


async def test_stale_flag_under_dead_deploy_units_does_not_hold(
    harness, daemon, wait_for
):
    harness.deploy_flag.parent.mkdir(parents=True)
    harness.deploy_flag.touch()
    for unit in ("BlocksScreen-deploy.path", "BlocksScreen-deploy.service"):
        (harness.state / f"inactive-{unit}").touch()  # path unit failed/stopped

    d = daemon()
    await wait_for(lambda: d.busy_trace() == [False], what="stale flag release")
    assert harness.deploy_flag.exists()


async def test_restarted_daemon_resumes_hold_silently(harness, daemon, wait_for):
    harness.deploy_flag.parent.mkdir(parents=True)
    harness.deploy_flag.touch()  # install-updater restarted us mid-run

    d = daemon()
    # Not exported yet at __init__: clients read it via get_busy, no signal.
    assert d.busy_trace() == []
    assert await d.iface.get_busy() is True

    harness.deploy_flag.unlink()
    await wait_for(lambda: d.busy_trace() == [False], what="hold release")


async def test_boot_provisioning_raises_overlay(harness, daemon, wait_for):
    origin = harness.remote("klipper")
    harness.component("klipper", service="klipper.service", install_if_missing=True)

    d = await _booted(daemon, wait_for)

    assert [a[0] for a in d.signals("provisioning_changed")] == [True, False]
    assert d.busy_trace() == [True, False]
    assert await d.iface.get_provisioning() is False
    assert harness.head("klipper") == harness.git("rev-parse", "HEAD", cwd=origin.bare)
    assert d.statuses()[0]["klipper"]["commits_behind"] == 0


async def test_boot_reconcile_reverts_power_cut(harness, daemon, wait_for):
    old = harness.power_cut()

    await _booted(daemon, wait_for)

    assert harness.head("klipper") == old
    assert "boot_rollback" in harness.events("klipper")
    assert not harness.inflight.exists()


async def test_boot_revert_restarts_service_on_reverted_code(harness, daemon, wait_for):
    old = harness.power_cut()

    await _booted(daemon, wait_for)

    assert harness.head("klipper") == old
    assert "systemctl --no-block restart klipper.service" in harness.calls()


async def test_boot_revert_mid_print_defers_restart(harness, daemon, wait_for):
    old = harness.power_cut()
    harness.printing.return_value = True

    await _booted(daemon, wait_for)

    assert harness.head("klipper") == old
    assert not any("restart klipper.service" in c for c in harness.calls())


async def test_cancel_mid_hook_reverts_and_releases(harness, daemon, wait_for):
    origin = harness.remote("klipper")
    harness.install(origin)
    old = harness.head("klipper")
    origin.commit({"klippy.py": "v2\n"})
    harness.component("klipper", service="klipper.service")
    pid_file = harness.state / "hook.pid"
    harness.hook("klipper", f'echo $$ >"{pid_file}"\nexec sleep 20\n')
    d = await _booted(daemon, wait_for)

    assert await d.iface.update_all() is True
    # The step signal fires before the hook spawns; only the pid file proves it runs.
    await wait_for(lambda: pid_file.exists() and pid_file.read_text(), what="hook")
    await d.iface.cancel()

    with pytest.raises(ProcessLookupError):
        os.kill(int(pid_file.read_text()), 0)  # cancel killed and reaped the hook

    assert harness.head("klipper") == old
    assert d.signals("rollback") == [("klipper", True)]
    assert d.busy_trace() == [True, False]
    assert not harness.inflight.exists()
