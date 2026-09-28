"""AMU plug-in, end to end, with the real DeviceConfigManager and watcher.

Walks the whole checklist: the daemon reports a serial device whose by-id name
says nothing about AMU, its USB ID (0x1d50:0xb001, USB_IDS.md) is read from
sysfs, the user is asked, printer.cfg only changes after they accept, the
restart request follows, and a reboot with the AMU still plugged keeps the
config without asking again.
"""

import os
import shutil

import pytest

from devices.discovery import serial_devices as sd
from devices.discovery.client import DeviceDiscoveryClient
from tools.configuration_manager.device_configurator import (
    DeviceConfigManager,
    DeviceConsent,
)
from tools.configuration_manager.device_profiles import load_profiles
from tools.configuration_manager.device_watcher import DeviceConfigWatcher

from .conftest import FakeDaemon

SYMLINK = "usb-Klipper_stm32h723xx_2B0012000851333235363233-if00"
AMU_REPORT = {
    "connection": "Serial",
    "firmware": "Klipper",
    "symlink_name": SYMLINK,
    "device_path": "/dev/ttyACM1",
    "vendor_id": 0,  # what device_discoveryd sends for Serial entries
    "product_id": 0,
}

# Fallback when no RF50-Klipper checkout is around: same shape as its printer.cfg.
MINI_PRINTER_CFG = """\
#[include config/variant_mmu/base/*.cfg]
[include config/variant_sync_single/*.cfg ]

[mcu]
canbus_uuid:

[mcu pi]
serial: /tmp/klipper_host_mcu

[printer]
kinematics: corexy
"""


def _rf50_printer_cfg():
    for d in (
        os.environ.get("RF50_KLIPPER_DIR"),
        os.path.expanduser("~/RF50-Klipper"),
        os.path.expanduser("~/github/RF50-Klipper"),
    ):
        if d and os.path.isfile(os.path.join(d, "printer.cfg")):
            return os.path.join(d, "printer.cfg")
    return None


class _Section:
    def __init__(self, values):
        self._values = values

    def get(self, key, default=None):
        return self._values.get(key, default)

    def getlists(self, key, default=None):
        return default


class _Config:
    def __init__(self, values):
        self._section = _Section(values)

    def get_section(self, name, fallback=None):
        return self._section


@pytest.fixture
def machine(tmp_path, monkeypatch):
    repo = tmp_path / "RF50-Klipper"
    config_dir = tmp_path / "printer_data" / "config"
    (repo / ".git").mkdir(parents=True)
    config_dir.mkdir(parents=True)
    src = _rf50_printer_cfg()
    if src:
        shutil.copy(src, repo / "printer.cfg")
    else:
        (repo / "printer.cfg").write_text(MINI_PRINTER_CFG)

    # sysfs: ttyACM1 -> USB interface -> USB device 1d50:b001
    usb_dev = tmp_path / "sys" / "devices" / "usb1" / "1-1"
    (usb_dev / "1-1:1.0").mkdir(parents=True)
    (usb_dev / "idVendor").write_text("1d50\n")
    (usb_dev / "idProduct").write_text("b001\n")
    tty = tmp_path / "sys" / "class" / "tty" / "ttyACM1"
    tty.mkdir(parents=True)
    (tty / "device").symlink_to(usb_dev / "1-1:1.0")
    monkeypatch.setattr(sd, "SYSFS_TTY_PATH", str(tmp_path / "sys" / "class" / "tty"))

    plugged = []
    monkeypatch.setattr(
        DeviceConfigManager,
        "scan_devices",
        staticmethod(lambda: [sd.device_from_json(r) for r in plugged]),
    )
    consent_path = tmp_path / "home" / ".config" / "blockscreen" / "consent.json"

    def boot():
        return DeviceConfigManager(
            _Config(
                {
                    "config_repo": str(repo),
                    "config_dir": str(config_dir),
                    "backup_dir": str(tmp_path / "backup"),
                    "copy_files": None,
                }
            ),
            profiles=load_profiles(override=None),
            consent=DeviceConsent(consent_path),
        )

    return boot, plugged, config_dir / "printer.cfg"


def test_amu_plug_in_end_to_end(qtbot, sock_path, machine):
    boot, plugged, printer_cfg = machine
    manager = boot()  # first boot, nothing plugged
    repo_text = printer_cfg.read_text()
    assert "[mcu mmu]" not in repo_text

    daemon = FakeDaemon(
        sock_path,
        [
            {"type": "hello", "proto": 1, "pid": 1},
            {"type": "snapshot", "devices": []},
            {"type": "added", "device": AMU_REPORT},
        ],
    )
    watcher = DeviceConfigWatcher(manager, client=DeviceDiscoveryClient(sock_path))
    try:
        # 1+2: plug-in noticed and identified as AMU by USB ID -> user is asked
        with qtbot.waitSignal(watcher.confirmation_required, timeout=5000) as ask:
            watcher.start()
        assert ask.args == [["amu"]]
        assert printer_cfg.read_text() == repo_text  # nothing written yet

        # 3: accepting writes the Happy Hare layout; 4: restart is requested
        with qtbot.waitSignal(watcher.config_changed, timeout=2000) as changed:
            watcher.accept(["amu"])
        assert changed.args == [["amu"]]
    finally:
        watcher.stop()
        daemon.close()

    text = printer_cfg.read_text()
    assert f"[mcu mmu]\nserial: /dev/serial/by-id/{SYMLINK}\n" in text
    assert "\n[include config/variant_mmu/base/*.cfg]" in text
    assert "\n#[include config/variant_sync_single/*.cfg" in text
    # the serial comes after the include so it overrides mmu.cfg's placeholder
    assert text.index("[include config/variant_mmu/base/*.cfg]") < text.index(
        "[mcu mmu]"
    )

    # 5: reboot with the AMU still plugged - same file, no question, no restart
    plugged.append(AMU_REPORT)
    rebooted = boot()
    assert printer_cfg.read_text() == text
    assert rebooted.boot_changed is False
    assert rebooted.pending_confirmation(
        [sd.device_from_json(AMU_REPORT)]
    ) == []

    # unplugged while off: reverted at boot, and flagged for a Klipper restart
    plugged.clear()
    rebooted = boot()
    assert printer_cfg.read_text() == repo_text
    assert rebooted.boot_changed is True


def test_decline_writes_nothing(qtbot, sock_path, machine):
    boot, _, printer_cfg = machine
    manager = boot()
    before = printer_cfg.read_text()
    daemon = FakeDaemon(
        sock_path,
        [{"type": "hello", "proto": 1, "pid": 1}, {"type": "added", "device": AMU_REPORT}],
    )
    watcher = DeviceConfigWatcher(manager, client=DeviceDiscoveryClient(sock_path))
    try:
        with qtbot.waitSignal(watcher.confirmation_required, timeout=5000):
            watcher.start()
        with qtbot.assertNotEmitted(watcher.config_changed, wait=500):
            watcher.decline(["amu"])
    finally:
        watcher.stop()
        daemon.close()
    assert printer_cfg.read_text() == before
