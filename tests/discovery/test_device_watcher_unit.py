"""DeviceConfigWatcher: daemon events -> DeviceConfigManager.apply_devices -> config_changed."""

import pytest

from devices.discovery.client import DeviceDiscoveryClient
from tools.configuration_manager.device_watcher import DeviceConfigWatcher

from .conftest import FakeDaemon

AMU = {
    "connection": "Serial",
    "firmware": "Klipper",
    "symlink_name": "usb-Klipper_stm32f446xx_AMU0001-if00",
}
WEBCAM = {"connection": "USB", "usb_class": "Video", "name": "Chicony HD Webcam"}


class FakeManager:
    """Records apply_devices calls; 'changes' the config once per profile."""

    def __init__(self):
        self.calls = []
        self._applied = set()

    def apply_devices(self, devices):
        self.calls.append([d.symlink_name for d in devices])
        changed = []
        for d in devices:
            if "AMU" in d.symlink_name and "amu" not in self._applied:
                self._applied.add("amu")
                changed.append("amu")
        return changed


@pytest.fixture
def watcher_for(sock_path):
    started = []

    def _make(messages):
        daemon = FakeDaemon(sock_path, messages)
        manager = FakeManager()
        watcher = DeviceConfigWatcher(manager, client=DeviceDiscoveryClient(sock_path))
        started.append((daemon, watcher))
        return watcher, manager

    yield _make
    for daemon, watcher in started:
        watcher.stop()
        daemon.close()


def test_hotplug_amu_emits_once(qtbot, watcher_for):
    watcher, manager = watcher_for(
        [
            {"type": "hello", "proto": 1, "pid": 1},
            {"type": "snapshot", "devices": []},
            {"type": "added", "device": WEBCAM},
            {"type": "added", "device": AMU},
            {"type": "added", "device": AMU},  # e.g. replug before restart
        ]
    )
    with qtbot.waitSignal(watcher.config_changed, timeout=5000) as blocker:
        watcher.start()
    assert blocker.args == [["amu"]]
    # The burst is coalesced into one apply; USB-only entries and the empty
    # snapshot never reach the manager.
    assert manager.calls == [[AMU["symlink_name"]]]


def test_snapshot_devices_are_applied(qtbot, watcher_for):
    watcher, manager = watcher_for(
        [
            {"type": "hello", "proto": 1, "pid": 1},
            {"type": "snapshot", "devices": [WEBCAM, AMU]},
        ]
    )
    with qtbot.waitSignal(watcher.config_changed, timeout=5000) as blocker:
        watcher.start()
    assert blocker.args == [["amu"]]
    assert manager.calls == [[AMU["symlink_name"]]]


def test_removed_is_only_logged(qtbot, watcher_for):
    watcher, manager = watcher_for(
        [
            {"type": "hello", "proto": 1, "pid": 1},
            {"type": "removed", "device": AMU},
        ]
    )
    with qtbot.assertNotEmitted(watcher.config_changed, wait=500):
        watcher.start()
    assert manager.calls == []


class ExplodingManager:
    def apply_devices(self, devices):
        raise RuntimeError("template bug")


def test_manager_error_does_not_escape_the_slot(qtbot, sock_path):
    # pytest-qt fails the test if an exception escapes a Qt slot, which in
    # the app would reach CrashHandler and exit BlocksScreen.
    daemon = FakeDaemon(
        sock_path,
        [{"type": "hello", "proto": 1, "pid": 1}, {"type": "added", "device": AMU}],
    )
    watcher = DeviceConfigWatcher(
        ExplodingManager(), client=DeviceDiscoveryClient(sock_path)
    )
    try:
        with qtbot.assertNotEmitted(watcher.config_changed, wait=1000):
            watcher.start()
    finally:
        watcher.stop()
        daemon.close()
