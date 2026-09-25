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
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .client import fetch_snapshot

_logger = logging.getLogger(__name__)

SERIAL_BY_ID_PATH = "/dev/serial/by-id/"


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


def device_from_json(data: dict[str, Any]) -> Device:
    """Build a Device from one device object of the daemon's protocol."""
    dev = Device(**{f: str(data.get(f) or "") for f in _DEVICE_FIELDS})
    dev.firmware = _firmware(str(data.get("firmware") or ""))
    dev.vendor_id = _usb_id(data.get("vendor_id"))
    dev.product_id = _usb_id(data.get("product_id"))
    return dev


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
            return self._legacy_scan()
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
    def _legacy_scan() -> list[Device]:
        # Imported lazily: once every machine runs the daemon, this fallback
        # and tools/serial_scanner.py can be deleted together.
        from tools.serial_scanner import (  # pylint: disable=import-outside-toplevel
            SerialScanner as LegacySerialScanner,
        )

        result = []
        for old in LegacySerialScanner().scan():
            dev = Device(**{f: getattr(old, f) for f in _DEVICE_FIELDS})
            dev.firmware = _firmware(old.firmware.value)
            result.append(dev)
        return result
