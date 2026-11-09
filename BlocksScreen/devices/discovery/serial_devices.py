"""Serial-device scanning backed by device_discoveryd.

Devices come from the daemon's snapshot (only `connection == "Serial"`
entries - the daemon also reports plain USB devices). When the daemon can't
be used - not installed on this machine, not running yet, or speaking an
unsupported protocol - scanning falls back to listing /dev/serial/by-id.

USB vendor/product IDs: the daemon only reports them for its `USB` entries
(0 for `Serial` ones), and the by-id name never carries them. So whenever a
serial device arrives without an ID, it is read here from sysfs - the
idVendor / idProduct of the USB device behind the tty - which is what lets
device profiles match on the IDs from USB_IDS.md instead of the by-id name.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Iterable
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
    """Firmware a serial device appears to run, guessed from its by-id name."""

    # pylint: disable=invalid-name
    Klipper = "Klipper"
    Katapult = "Katapult"
    Unflashed = "Unflashed"
    Unknown = "Unknown"


@dataclass
class Device:  # pylint: disable=too-many-instance-attributes
    """A serial device under /dev/serial/by-id"""

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
    # 0 means "not reported" (by-id scan, or a daemon/protocol version
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
    dev = Device(
        firmware=_firmware(str(data.get("firmware") or "")),
        vendor_id=_usb_id(data.get("vendor_id")),
        product_id=_usb_id(data.get("product_id")),
    )
    for f in _DEVICE_FIELDS:
        setattr(dev, f, str(data.get(f) or ""))
    return fill_usb_ids(dev)


def serial_from_json(devices: Iterable[Any]) -> list[Device]:
    """The daemon's Serial devices (it also reports plain USB ones)"""
    return [
        device_from_json(d)
        for d in devices
        if isinstance(d, dict) and d.get("connection") == "Serial"
    ]


def _detect_firmware(symlink_name: str) -> FirmwareState:
    if "Klipper" in symlink_name:
        return FirmwareState.Klipper
    if "Katapult" in symlink_name or "CanBoot" in symlink_name:
        return FirmwareState.Katapult
    if any(m in symlink_name for m in ("1a86", "FTDI", "Silicon_Labs", "Prolific")):
        return FirmwareState.Unflashed
    return FirmwareState.Unknown


def device_from_symlink(symlink_name: str, device_path: str) -> Device:
    """Parse a by-id name like usb-Klipper_stm32h723xx_<serial>-if00 into a Device"""
    dev = Device(
        symlink_name=symlink_name,
        device_path=device_path,
        firmware=_detect_firmware(symlink_name),
    )
    rest = symlink_name.removeprefix("usb-")
    head, sep, tail = rest.rpartition("-if")
    if sep:
        rest, dev.interface = head, tail.split("-")[0]
    parts = rest.split("_")
    if len(parts) >= 3:
        dev.manufacturer, dev.serial_number = parts[0], parts[-1]
        dev.product = "_".join(parts[1:-1])
    elif len(parts) == 2:
        dev.manufacturer, dev.product = parts
    else:
        dev.manufacturer = rest
    if dev.is_klipper or dev.is_katapult:
        dev.mcu_type = dev.product.split("_")[0]
    dev.name = f"{dev.manufacturer} {dev.mcu_type or dev.product}".strip()
    return fill_usb_ids(dev)


class SerialScanner:
    """Lists /dev/serial/by-id devices via device_discoveryd.

    Falls back to reading /dev/serial/by-id when the daemon is unavailable.
    """

    def __init__(self, socket_path: str | None = None, timeout: float = 2.0) -> None:
        self._socket_path = socket_path
        self._timeout = timeout

    def daemon_scan(self) -> list[Device] | None:
        """Serial devices from device_discoveryd, None when it can't be used"""
        devices = fetch_snapshot(self._socket_path, self._timeout)
        return None if devices is None else serial_from_json(devices)

    def scan(self) -> list[Device]:
        """All serial devices - equivalent to ls /dev/serial/by-id/*"""
        devices = self.daemon_scan()
        if devices is None:
            _logger.info("device_discoveryd unavailable, scanning /dev/serial/by-id")
            return self.legacy_scan()
        return devices

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
        try:
            with os.scandir(SERIAL_BY_ID_PATH) as entries:
                return [
                    device_from_symlink(e.name, os.path.realpath(e.path))
                    for e in entries
                ]
        except OSError:  # udev removes by-id when no serial device is plugged in
            return []
