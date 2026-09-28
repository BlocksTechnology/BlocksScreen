"""Serial-device scanning backed by device_discoveryd.

Drop-in replacement for tools/serial_scanner.py during the move to the
discovery daemon: same `SerialScanner` API (`scan`, `scan_klipper`,
`scan_katapult`, `scan_unflashed`) and the same `Device` fields, properties
and repr, so callers only change their import.

Devices come from the daemon's snapshot (only `connection == "Serial"`
entries - the daemon also reports USB devices, which the legacy scanner
never did). When the daemon can't be used - not installed on this machine,
not running yet, or speaking an unsupported protocol - scanning falls back
to the legacy tools.serial_scanner, so behaviour is unchanged either way.

USB vendor/product IDs: the daemon only reports them for its `USB` entries
(0 for `Serial` ones), and the legacy scan never did. So whenever a serial
device arrives without an ID, it is read here from sysfs - the idVendor /
idProduct of the USB device behind the tty - which is what lets device
profiles match on the IDs from USB_IDS.md instead of the by-id name.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .client import fetch_snapshot

_logger = logging.getLogger(__name__)

SERIAL_BY_ID_PATH = "/dev/serial/by-id/"
SYSFS_TTY_PATH = "/sys/class/tty"
# tty -> USB interface -> USB device is two levels; the extra headroom covers
# drivers that add a level (usb-serial adapters: ttyUSB0/.../port/interface).
_SYSFS_MAX_DEPTH = 4


class FirmwareState(Enum):
    """Firmware a serial device appears to run, guessed from its by-id name.

    Member names match tools/serial_scanner.py for drop-in compatibility.
    """

    # pylint: disable=invalid-name
    Klipper = "Klipper"
    Katapult = "Katapult"
    Unflashed = "Unflashed"
    Unknown = "Unknown"


@dataclass
class Device:  # pylint: disable=too-many-instance-attributes
    """A serial device under /dev/serial/by-id (same shape as the legacy one)."""

    name: str = ""
    manufacturer: str = ""
    product: str = ""
    serial_number: str = ""
    mcu_type: str = ""
    firmware: FirmwareState = FirmwareState.Unknown

    symlink_name: str = ""
    device_path: str = ""
    interface: str = ""

    # USB vendor/product ID of the device's parent USB interface, as set by
    # the MCU firmware's Kconfig USB_VENDOR_ID/USB_DEVICE_ID at build time.
    # 0 means "not reported" (legacy scanner, or a daemon/protocol version
    # that doesn't send it yet) - never treat 0 as a real ID.
    vendor_id: int = 0
    product_id: int = 0

    @property
    def symlink(self) -> str:
        """Full /dev/serial/by-id path"""
        return f"{SERIAL_BY_ID_PATH}{self.symlink_name}"

    @property
    def vid_hex(self) -> str:
        """Vendor ID as '0x1d50', or '' if not reported"""
        return f"0x{self.vendor_id:04x}" if self.vendor_id else ""

    @property
    def pid_hex(self) -> str:
        """Product ID as '0x614e', or '' if not reported"""
        return f"0x{self.product_id:04x}" if self.product_id else ""

    @property
    def is_klipper(self) -> bool:
        """Whether the device runs Klipper firmware"""
        return self.firmware == FirmwareState.Klipper

    @property
    def is_katapult(self) -> bool:
        """Whether the device is in the Katapult (CanBoot) bootloader"""
        return self.firmware == FirmwareState.Katapult

    @property
    def is_unflashed(self) -> bool:
        """Whether the device is a bare USB-serial adapter with no firmware"""
        return self.firmware == FirmwareState.Unflashed

    def __repr__(self) -> str:
        return (
            f"<Device [{self.firmware.value}] {self.name} -> {self.device_path}> "
            f"{self.symlink_name} "
        )


_DEVICE_FIELDS = (
    "name",
    "manufacturer",
    "product",
    "serial_number",
    "mcu_type",
    "symlink_name",
    "device_path",
    "interface",
)


def _firmware(value: str) -> FirmwareState:
    try:
        return FirmwareState(value)
    except ValueError:
        return FirmwareState.Unknown


def _usb_id(value: Any) -> int:
    """Parse a vendor_id/product_id value from the daemon (int, or absent/0)."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _read_hex(path: str) -> int:
    try:
        with open(path, encoding="ascii") as f:
            return int(f.read().strip(), 16)
    except (OSError, ValueError):
        return 0


def usb_ids_from_sysfs(dev: Device) -> tuple[int, int]:
    """(vendor_id, product_id) of the USB device behind dev's tty, (0, 0) if unknown.

    /sys/class/tty/<tty>/device is the USB interface the tty belongs to; the
    idVendor/idProduct files live on its parent USB device.
    """
    tty_path = dev.device_path
    if not tty_path and dev.symlink_name:
        tty_path = os.path.realpath(dev.symlink)
    tty = os.path.basename(tty_path)
    if not tty.startswith("tty"):
        return 0, 0
    node = os.path.realpath(os.path.join(SYSFS_TTY_PATH, tty, "device"))
    for _ in range(_SYSFS_MAX_DEPTH):
        vendor_id = _read_hex(os.path.join(node, "idVendor"))
        if vendor_id:
            return vendor_id, _read_hex(os.path.join(node, "idProduct"))
        parent = os.path.dirname(node)
        if parent == node:
            break
        node = parent
    return 0, 0


def fill_usb_ids(dev: Device) -> Device:
    """Fill dev's vendor/product ID from sysfs when nothing reported one."""
    if not dev.vendor_id:
        dev.vendor_id, dev.product_id = usb_ids_from_sysfs(dev)
    return dev


def device_from_json(data: dict[str, Any]) -> Device:
    """Build a Device from one device object of the daemon's protocol."""
    dev = Device(**{f: str(data.get(f) or "") for f in _DEVICE_FIELDS})
    dev.firmware = _firmware(str(data.get("firmware") or ""))
    dev.vendor_id = _usb_id(data.get("vendor_id"))
    dev.product_id = _usb_id(data.get("product_id"))
    return fill_usb_ids(dev)


class SerialScanner:
    """Lists /dev/serial/by-id devices via device_discoveryd.

    Falls back to tools.serial_scanner when the daemon is unavailable.
    """

    def __init__(self, socket_path: str | None = None, timeout: float = 2.0) -> None:
        self._socket_path = socket_path
        self._timeout = timeout

    def scan(self) -> list[Device]:
        """All serial devices - equivalent to ls /dev/serial/by-id/*"""
        devices = fetch_snapshot(self._socket_path, self._timeout)
        if devices is None:
            _logger.info(
                "device_discoveryd unavailable, using legacy /dev/serial/by-id scan"
            )
            return self.legacy_scan()
        return [
            device_from_json(d)
            for d in devices
            if isinstance(d, dict) and d.get("connection") == "Serial"
        ]

    def scan_klipper(self) -> list[Device]:
        """Devices running Klipper"""
        return [d for d in self.scan() if d.is_klipper]

    def scan_katapult(self) -> list[Device]:
        """Devices in the Katapult bootloader"""
        return [d for d in self.scan() if d.is_katapult]

    def scan_unflashed(self) -> list[Device]:
        """Bare USB-serial adapters (CH340, FTDI, CP210x, PL2303)"""
        return [d for d in self.scan() if d.is_unflashed]

    @staticmethod
    def legacy_scan() -> list[Device]:
        """Plain /dev/serial/by-id listing, without the daemon"""
        # Imported lazily: once every machine runs the daemon, this fallback
        # and tools/serial_scanner.py can be deleted together.
        from tools.serial_scanner import (  # pylint: disable=import-outside-toplevel
            SerialScanner as LegacySerialScanner,
        )

        result = []
        for old in LegacySerialScanner().scan():
            dev = Device(**{f: getattr(old, f) for f in _DEVICE_FIELDS})
            dev.firmware = _firmware(old.firmware.value)
            result.append(fill_usb_ids(dev))
        return result
