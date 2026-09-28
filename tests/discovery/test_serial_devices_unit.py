"""devices.discovery.serial_devices: daemon-backed drop-in for tools.serial_scanner."""

import os

import pytest

from devices.discovery import client as dd_client
from devices.discovery import serial_devices as sd

from .conftest import FakeDaemon

KLIPPER = {
    "connection": "Serial",
    "firmware": "Klipper",
    "name": "Klipper stm32h723xx",
    "manufacturer": "Klipper",
    "product": "stm32h723xx",
    "serial_number": "29003A000851323235363233",
    "mcu_type": "stm32h723xx",
    "symlink_name": "usb-Klipper_stm32h723xx_29003A000851323235363233-if00",
    "device_path": "/dev/ttyACM0",
    "interface": "00",
    "usb_class": "Unknown",
    "vendor_id": 0,
}
KATAPULT = {
    **KLIPPER,
    "firmware": "Katapult",
    "name": "Katapult rp2040",
    "symlink_name": "usb-Katapult_rp2040_E6625C05E7-if00",
}
CH340 = {
    **KLIPPER,
    "firmware": "Unflashed",
    "name": "1a86 USB",
    "mcu_type": "",
    "symlink_name": "usb-1a86_USB_Serial-if00-port0",
}
BEACON = {
    **KLIPPER,
    "firmware": "Unknown",
    "name": "Beacon Beacon_RevH",
    "mcu_type": "",
    "symlink_name": "usb-Beacon_Beacon_RevH_ABC123-if00",
}
WEBCAM = {"connection": "USB", "usb_class": "Video", "name": "Chicony HD Webcam"}


def _hello(proto=1):
    return {"type": "hello", "proto": proto, "pid": 1}


@pytest.fixture
def daemon(sock_path):
    started = []

    def _start(messages):
        d = FakeDaemon(sock_path, messages)
        started.append(d)
        return d

    yield _start
    for d in started:
        d.close()


class TestDeviceFromJson:
    def test_maps_every_field(self):
        dev = sd.device_from_json(KLIPPER)
        assert dev.name == "Klipper stm32h723xx"
        assert dev.firmware is sd.FirmwareState.Klipper
        assert dev.mcu_type == "stm32h723xx"
        assert dev.interface == "00"
        assert dev.device_path == "/dev/ttyACM0"
        assert dev.symlink == "/dev/serial/by-id/" + KLIPPER["symlink_name"]
        assert dev.is_klipper and not dev.is_katapult and not dev.is_unflashed

    def test_unknown_or_missing_firmware(self):
        assert sd.device_from_json({"firmware": "Bogus"}).firmware is (
            sd.FirmwareState.Unknown
        )
        assert sd.device_from_json({}).firmware is sd.FirmwareState.Unknown

    def test_missing_usb_ids_default_to_zero(self):
        dev = sd.device_from_json(KLIPPER)  # KLIPPER["vendor_id"] is 0
        assert dev.vendor_id == 0
        assert dev.product_id == 0
        assert dev.vid_hex == "" and dev.pid_hex == ""

    def test_usb_ids_are_parsed(self):
        dev = sd.device_from_json(
            {**KLIPPER, "vendor_id": 0x1D50, "product_id": 0x614E}
        )
        assert dev.vendor_id == 0x1D50
        assert dev.product_id == 0x614E
        assert dev.vid_hex == "0x1d50"
        assert dev.pid_hex == "0x614e"

    def test_garbage_usb_ids_default_to_zero(self):
        dev = sd.device_from_json({**KLIPPER, "vendor_id": "not-a-number"})
        assert dev.vendor_id == 0

    def test_repr_matches_legacy_format(self):
        dev = sd.device_from_json(KLIPPER)
        assert repr(dev) == (
            "<Device [Klipper] Klipper stm32h723xx -> /dev/ttyACM0> "
            f"{KLIPPER['symlink_name']} "
        )


class TestScanViaDaemon:
    def test_only_serial_entries(self, daemon, sock_path):
        daemon([_hello(), {"type": "snapshot", "devices": [KLIPPER, WEBCAM, BEACON]}])
        devs = sd.SerialScanner(sock_path).scan()
        assert [d.symlink_name for d in devs] == [
            KLIPPER["symlink_name"],
            BEACON["symlink_name"],
        ]

    @pytest.mark.parametrize(
        ("method", "expected"),
        [
            ("scan_klipper", KLIPPER),
            ("scan_katapult", KATAPULT),
            ("scan_unflashed", CH340),
        ],
    )
    def test_filters(self, daemon, sock_path, method, expected):
        # Unknown (BEACON) must not count as unflashed - legacy semantics.
        daemon(
            [
                _hello(),
                {"type": "snapshot", "devices": [KLIPPER, KATAPULT, CH340, BEACON]},
            ]
        )
        devs = getattr(sd.SerialScanner(sock_path), method)()
        assert [d.symlink_name for d in devs] == [expected["symlink_name"]]

    def test_empty_snapshot_is_not_a_fallback(self, daemon, sock_path, monkeypatch):
        daemon([_hello(), {"type": "snapshot", "devices": []}])
        monkeypatch.setattr(sd.SerialScanner, "legacy_scan", staticmethod(pytest.fail))
        assert sd.SerialScanner(sock_path).scan() == []


@pytest.fixture
def legacy_by_id(tmp_path, monkeypatch):
    """Point the legacy scanner at a fake /dev/serial/by-id."""
    from tools import serial_scanner as legacy

    by_id = tmp_path / "by-id"
    by_id.mkdir()
    for name in (KLIPPER["symlink_name"], BEACON["symlink_name"]):
        os.symlink("/dev/null", by_id / name)
    monkeypatch.setattr(legacy.SerialScanner, "SERIAL_PATH", str(by_id))
    return by_id


class TestFallback:
    def test_no_daemon_uses_legacy_scan(self, sock_path, legacy_by_id):
        devs = sd.SerialScanner(sock_path).scan()  # nothing listening
        by_name = {d.symlink_name: d for d in devs}
        assert set(by_name) == {KLIPPER["symlink_name"], BEACON["symlink_name"]}
        klipper = by_name[KLIPPER["symlink_name"]]
        # Converted to this module's types, not the legacy ones.
        assert isinstance(klipper, sd.Device)
        assert klipper.firmware is sd.FirmwareState.Klipper
        assert klipper.mcu_type == "stm32h723xx"

    def test_protocol_mismatch_uses_legacy_scan(self, daemon, sock_path, legacy_by_id):
        daemon([_hello(proto=99), {"type": "snapshot", "devices": [WEBCAM]}])
        devs = sd.SerialScanner(sock_path).scan()
        assert len(devs) == 2

    def test_silent_daemon_times_out(self, daemon, sock_path, legacy_by_id):
        daemon([])  # accepts, never sends
        devs = sd.SerialScanner(sock_path, timeout=0.3).scan()
        assert len(devs) == 2


class TestFetchSnapshot:
    def test_returns_devices(self, daemon, sock_path):
        daemon([_hello(), {"type": "snapshot", "devices": [KLIPPER]}])
        assert dd_client.fetch_snapshot(sock_path) == [KLIPPER]

    def test_garbage_returns_none(self, daemon, sock_path):
        daemon([b"not json"])
        assert dd_client.fetch_snapshot(sock_path, timeout=1.0) is None

    def test_missing_socket_returns_none(self, sock_path):
        assert dd_client.fetch_snapshot(sock_path) is None


class TestSysfsUsbIds:
    """IDs read from sysfs when the daemon reports none (it never does for Serial)."""

    @pytest.fixture
    def sysfs(self, tmp_path, monkeypatch):
        # /sys/class/tty/ttyACM1/device -> .../usb1/1-1/1-1:1.0 (interface);
        # idVendor/idProduct live on the parent USB device 1-1.
        usb_dev = tmp_path / "devices" / "usb1" / "1-1"
        iface = usb_dev / "1-1:1.0"
        iface.mkdir(parents=True)
        (usb_dev / "idVendor").write_text("1d50\n")
        (usb_dev / "idProduct").write_text("b001\n")
        tty = tmp_path / "class" / "tty" / "ttyACM1"
        tty.mkdir(parents=True)
        (tty / "device").symlink_to(iface)
        monkeypatch.setattr(sd, "SYSFS_TTY_PATH", str(tmp_path / "class" / "tty"))
        return tmp_path

    def test_daemon_serial_entry_gets_ids_from_sysfs(self, sysfs):
        dev = sd.device_from_json(
            {
                "connection": "Serial",
                "symlink_name": "usb-Klipper_stm32h723xx_2B00-if00",
                "device_path": "/dev/ttyACM1",
                "vendor_id": 0,
                "product_id": 0,
            }
        )
        assert (dev.vendor_id, dev.product_id) == (0x1D50, 0xB001)

    def test_reported_ids_win_over_sysfs(self, sysfs):
        dev = sd.device_from_json(
            {"device_path": "/dev/ttyACM1", "vendor_id": 0x1234, "product_id": 1}
        )
        assert (dev.vendor_id, dev.product_id) == (0x1234, 1)

    def test_unknown_tty_stays_zero(self, sysfs):
        dev = sd.device_from_json({"device_path": "/dev/ttyACM9"})
        assert (dev.vendor_id, dev.product_id) == (0, 0)

    def test_non_tty_path_is_ignored(self, sysfs):
        assert sd.usb_ids_from_sysfs(sd.Device(device_path="/etc/passwd")) == (0, 0)

    def test_amu_matched_by_id_without_amu_in_name(self, sysfs):
        from tools.configuration_manager.device_profiles import load_profiles

        amu = next(p for p in load_profiles(override=None) if p.name == "amu")
        dev = sd.device_from_json(
            {
                "symlink_name": "usb-Klipper_stm32h723xx_2B00-if00",
                "device_path": "/dev/ttyACM1",
            }
        )
        assert amu.matches(dev)
        stock = sd.Device(
            symlink_name="usb-Klipper_AMU_stock-if00", vendor_id=0x1D50, product_id=0x614E
        )
        assert not amu.matches(stock)  # stock Klipper ID: ID mismatch is final
