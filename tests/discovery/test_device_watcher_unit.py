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

    def pending_confirmation(self, devices):
        return []


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

    def pending_confirmation(self, devices):
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

    def __init__(self, accepted=("amu",)):
        from tools.configuration_manager.device_profiles import load_profiles

        self.profiles = load_profiles(override=None)
        self.accepted = set(accepted)
        self.text = PRINTER_CFG

    def _allowed(self):
        return [p for p in self.profiles if not p.confirm or p.name in self.accepted]

    def apply_devices(self, devices):
        from tools.configuration_manager.device_profiles import (
            apply_device_profiles,
        )

        self.text, changed = apply_device_profiles(self.text, self._allowed(), devices)
        return changed

    def pending_confirmation(self, devices):
        from tools.configuration_manager.device_profiles import (
            apply_device_profiles,
            match_devices,
        )

        waiting = [p for p in self.profiles if p.confirm and p.name not in self.accepted]
        return [
            p.name
            for p, d in match_devices(waiting, devices)
            if apply_device_profiles(self.text, [p], [d])[1]
        ]

    def accept(self, names):
        self.accepted.update(names)


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
    assert "[mcu mmu]" in manager.text
    assert f"serial: /dev/serial/by-id/{AMU_SERIAL_BY_ID['symlink_name']}" in manager.text


def test_amu_without_reported_id_is_not_recognised(qtbot, sock_path):
    # No ID from the daemon and none in sysfs (see the autouse fixture), and
    # a by-id name without "AMU": nothing identifies it as an AMU.
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


class TestConfirmation:
    """AMU (confirm: true): ask first, write only after accept()."""

    MESSAGES = [
        {"type": "hello", "proto": 1, "pid": 1},
        {"type": "snapshot", "devices": []},
        {"type": "added", "device": AMU_SERIAL_BY_ID},
    ]

    @pytest.fixture
    def setup(self, sock_path):
        made = []

        def _make(messages=None):
            daemon = FakeDaemon(sock_path, messages or self.MESSAGES)
            manager = ProfileManager(accepted=())
            watcher = DeviceConfigWatcher(
                manager, client=DeviceDiscoveryClient(sock_path)
            )
            made.append((daemon, watcher))
            return watcher, manager

        yield _make
        for daemon, watcher in made:
            watcher.stop()
            daemon.close()

    def test_asks_before_writing(self, qtbot, setup):
        watcher, manager = setup()
        with qtbot.assertNotEmitted(watcher.config_changed, wait=0):
            with qtbot.waitSignal(watcher.confirmation_required, timeout=5000) as b:
                watcher.start()
        assert b.args == [["amu"]]
        assert manager.text == PRINTER_CFG

    def test_accept_writes_and_emits_config_changed(self, qtbot, setup):
        watcher, manager = setup()
        with qtbot.waitSignal(watcher.confirmation_required, timeout=5000):
            watcher.start()
        with qtbot.waitSignal(watcher.config_changed, timeout=1000) as b:
            watcher.accept(["amu"])
        assert b.args == [["amu"]]
        assert "[mcu mmu]" in manager.text
        assert manager.accepted == {"amu"}

    def test_decline_leaves_config_and_does_not_ask_again(self, qtbot, setup):
        watcher, manager = setup()
        with qtbot.waitSignal(watcher.confirmation_required, timeout=5000):
            watcher.start()
        watcher.decline(["amu"])
        # A later snapshot (daemon reconnect) with the same AMU: no new question.
        with qtbot.assertNotEmitted(watcher.confirmation_required, wait=600):
            watcher._on_snapshot([AMU_SERIAL_BY_ID])
        assert manager.text == PRINTER_CFG

    def test_replug_after_decline_asks_again(self, qtbot, setup):
        watcher, manager = setup()
        with qtbot.waitSignal(watcher.confirmation_required, timeout=5000):
            watcher.start()
        watcher.decline(["amu"])
        watcher._on_device_removed(AMU_SERIAL_BY_ID)
        with qtbot.waitSignal(watcher.confirmation_required, timeout=2000) as b:
            watcher._on_device_added(AMU_SERIAL_BY_ID)
        assert b.args == [["amu"]]

    def test_no_second_question_while_one_is_open(self, qtbot, setup):
        watcher, _ = setup()
        with qtbot.waitSignal(watcher.confirmation_required, timeout=5000):
            watcher.start()
        with qtbot.assertNotEmitted(watcher.confirmation_required, wait=600):
            watcher._on_device_added(AMU_SERIAL_BY_ID)


class TestPollFallback:
    """No daemon: /dev/serial/by-id is polled so hotplug still works."""

    def test_polls_when_daemon_unreachable(self, qtbot, sock_path, monkeypatch):
        from devices.discovery import serial_devices as sd

        found = []
        monkeypatch.setattr(sd.SerialScanner, "legacy_scan", staticmethod(lambda: found))
        manager = ProfileManager()
        watcher = DeviceConfigWatcher(manager, client=DeviceDiscoveryClient(sock_path))
        monkeypatch.setattr(watcher, "POLL_MS", 50)
        watcher._poll_timer.setInterval(50)
        try:
            watcher.start()  # nothing listens on sock_path
            qtbot.waitUntil(watcher._poll_timer.isActive, timeout=5000)
            found.append(
                sd.Device(
                    symlink_name=AMU_SERIAL_BY_ID["symlink_name"],
                    vendor_id=0x1D50,
                    product_id=0xB001,
                )
            )
            with qtbot.waitSignal(watcher.config_changed, timeout=3000) as b:
                pass
        finally:
            watcher.stop()
        assert b.args == [["amu"]]
        assert "[mcu mmu]" in manager.text

    def test_daemon_connect_stops_polling(self, qtbot, sock_path):
        watcher = DeviceConfigWatcher(
            ProfileManager(), client=DeviceDiscoveryClient(sock_path)
        )
        watcher._on_daemon_disconnected()
        assert watcher._poll_timer.isActive()
        watcher._on_daemon_connected()
        assert not watcher._poll_timer.isActive()
        watcher.stop()
