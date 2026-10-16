"""UpdaterDbusService end to end: busy/overlay contract, boot pass, deploy hold, cancel."""

import asyncio

from conftest import wait_for

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


async def _booted(daemon):
    """Start a daemon and wait for its first status emit."""
    d = daemon()
    await wait_for(lambda: d.statuses(), what="boot status")
    return d


async def test_update_all_round_trip(harness, daemon):
    origin = harness.remote("klipper")
    harness.install(origin)
    new = origin.commit({"klippy.py": "v2\n"})
    harness.component("klipper", service="klipper.service")
    d = await _booted(daemon)
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


async def test_nothing_dirty_still_releases_busy(harness, daemon):
    harness.install(harness.remote("klipper"))
    harness.component("klipper", service="klipper.service")
    d = await _booted(daemon)

    assert await d.iface.update_all() is True
    await wait_for(lambda: d.busy_trace() == [True, False], what="busy release")

    assert d.signals("step_complete") == []


async def test_failed_update_releases_busy_and_reports(harness, daemon):
    origin = harness.remote("klipper")
    harness.install(origin)
    old = harness.head("klipper")
    origin.commit({"klippy.py": "v2\n"})
    harness.component("klipper", service="klipper.service")
    harness.hook("klipper", "exit 1\n")
    d = await _booted(daemon)

    assert await d.iface.update_all() is True
    await wait_for(lambda: d.busy_trace() == [True, False], what="busy release")

    assert harness.head("klipper") == old
    assert d.signals("error") == [("klipper", "hook")]
    assert d.signals("rollback") == [("klipper", True)]
    assert d.signals("component_done") == [("klipper", False)]


async def test_install_update_holds_overlay_until_deploy_finishes(harness, daemon):
    origin = harness.remote("BlocksScreen", UI_FILES)
    harness.install(origin)
    origin.commit({"scripts/install-updater.sh": "v2\n"})
    harness.component("BlocksScreen", service="BlocksScreen.service")
    harness.real_hook("BlocksScreen")
    d = await _booted(daemon)

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


async def test_deploy_hold_is_capped(harness, daemon):
    harness.mp.setitem(harness.dbus_g, "_DEPLOY_HOLD_CAP_S", 0.3)
    harness.deploy_flag.parent.mkdir(parents=True)
    harness.deploy_flag.touch()  # a hung install-updater never clears it

    d = daemon()
    assert await d.iface.get_busy() is True

    await wait_for(lambda: d.busy_trace() == [False], timeout=5.0, what="cap")
    assert harness.deploy_flag.exists()


async def test_restarted_daemon_resumes_hold_silently(harness, daemon):
    harness.deploy_flag.parent.mkdir(parents=True)
    harness.deploy_flag.touch()  # install-updater restarted us mid-run

    d = daemon()
    # Not exported yet at __init__: clients read it via get_busy, no signal.
    assert d.busy_trace() == []
    assert await d.iface.get_busy() is True

    harness.deploy_flag.unlink()
    await wait_for(lambda: d.busy_trace() == [False], what="hold release")


async def test_boot_provisioning_raises_overlay(harness, daemon):
    origin = harness.remote("klipper")
    harness.component("klipper", service="klipper.service", install_if_missing=True)

    d = await _booted(daemon)

    assert [a[0] for a in d.signals("provisioning_changed")] == [True, False]
    assert d.busy_trace() == [True, False]
    assert await d.iface.get_provisioning() is False
    assert harness.head("klipper") == harness.git("rev-parse", "HEAD", cwd=origin.bare)
    assert d.statuses()[0]["klipper"]["commits_behind"] == 0


async def test_boot_reconcile_reverts_power_cut(harness, daemon):
    origin = harness.remote("klipper")
    harness.install(origin)
    old = harness.head("klipper")
    origin.commit({"klippy.py": "v2\n"})
    harness.git("pull", "-q", cwd=harness.home / "klipper")
    harness.inflight.parent.mkdir(parents=True, exist_ok=True)
    harness.inflight.write_text(f'{{"klipper": "{old}"}}')
    harness.component("klipper", service="klipper.service")

    await _booted(daemon)

    assert harness.head("klipper") == old
    assert "boot_rollback" in harness.events("klipper")
    assert not harness.inflight.exists()


async def test_cancel_mid_hook_reverts_and_releases(harness, daemon):
    origin = harness.remote("klipper")
    harness.install(origin)
    old = harness.head("klipper")
    origin.commit({"klippy.py": "v2\n"})
    harness.component("klipper", service="klipper.service")
    harness.hook("klipper", "sleep 20\n")
    d = await _booted(daemon)

    assert await d.iface.update_all() is True
    await wait_for(
        lambda: ("klipper", 3, 4) in d.signals("step_complete"), what="hook start"
    )
    await d.iface.cancel()

    assert harness.head("klipper") == old
    assert d.signals("rollback") == [("klipper", True)]
    assert d.busy_trace() == [True, False]
    assert not harness.inflight.exists()
