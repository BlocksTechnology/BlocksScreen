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


# What the daemon reports for an AMU on its own USB ID (USB_IDS.md): the
# by-id name carries no "AMU", only the serial entry's vendor/product ID does.
AMU_SERIAL_BY_ID = {
    "connection": "Serial",
    "firmware": "Klipper",
    "name": "Klipper stm32h723xx",
    "symlink_name": "usb-Klipper_stm32h723xx_2B0012000851333235363233-if00",
    "device_path": "/dev/ttyACM1",
    "vendor_id": 0x1D50,
    "product_id": 0xB001,
}
AMU_USB_BY_ID = {
    "connection": "USB",
    "usb_class": "CDCSerial",
    "vendor_id": 0x1D50,
    "product_id": 0xB001,
}
PRINTER_CFG = "[printer]\nkinematics: corexy\n\n[mcu]\nserial: /dev/ttyACM0\n"


class ProfileManager:
    """apply_devices through the real bundled profiles, on in-memory printer.cfg."""

    def __init__(self):
        from tools.configuration_manager.device_profiles import load_profiles

        self.profiles = load_profiles(override=None)
        self.text = PRINTER_CFG

    def apply_devices(self, devices):
        from tools.configuration_manager.device_profiles import (
            apply_device_profiles,
        )

        self.text, changed = apply_device_profiles(self.text, self.profiles, devices)
        return changed


def test_amu_identified_by_usb_id_updates_config(qtbot, sock_path):
    daemon = FakeDaemon(
        sock_path,
        [
            {"type": "hello", "proto": 1, "pid": 1},
            {"type": "snapshot", "devices": []},
            {"type": "added", "device": AMU_SERIAL_BY_ID},
            {"type": "added", "device": AMU_USB_BY_ID},
        ],
    )
    manager = ProfileManager()
    watcher = DeviceConfigWatcher(manager, client=DeviceDiscoveryClient(sock_path))
    try:
        with qtbot.waitSignal(watcher.config_changed, timeout=5000) as blocker:
            watcher.start()
    finally:
        watcher.stop()
        daemon.close()
    assert blocker.args == [["amu"]]
    assert "[mcu AMU]" in manager.text
    assert f"serial: /dev/serial/by-id/{AMU_SERIAL_BY_ID['symlink_name']}" in manager.text


def test_amu_without_reported_id_is_not_recognised(qtbot, sock_path):
    # Daemons before the sysfs ID lookup sent 0 for serial entries, so an
    # AMU whose by-id name lacks "AMU" was never matched: no prompt.
    daemon = FakeDaemon(
        sock_path,
        [
            {"type": "hello", "proto": 1, "pid": 1},
            {
                "type": "added",
                "device": {**AMU_SERIAL_BY_ID, "vendor_id": 0, "product_id": 0},
            },
        ],
    )
    manager = ProfileManager()
    watcher = DeviceConfigWatcher(manager, client=DeviceDiscoveryClient(sock_path))
    try:
        with qtbot.assertNotEmitted(watcher.config_changed, wait=800):
            watcher.start()
    finally:
        watcher.stop()
        daemon.close()
    assert manager.text == PRINTER_CFG
