import os
import logging
import glob
from dataclasses import dataclass
from enum import Enum

_logger = logging.getLogger(__name__)


class FirmwareState(Enum):
    Klipper = "Klipper"
    Katapult = "Katapult"
    Unflashed = "Unflashed"
    Unknown = "Unknown"


@dataclass
class Device:
    name: str = ""
    manufacturer: str = ""
    product: str = ""
    serial_number: str = ""
    mcu_type: str = ""
    firmware: FirmwareState = FirmwareState.Unknown

    symlink_name: str = ""
    device_path: str = ""
    interface: str = ""

    @property
    def symlink(self) -> str:
        """Full /dev/serial/by-id path"""
        return f"/dev/serial/by-id/{self.symlink_name}"

    @property
    def is_klipper(self) -> bool:
        return self.firmware == FirmwareState.Klipper

    @property
    def is_katapult(self) -> bool:
        return self.firmware == FirmwareState.Katapult

    @property
    def is_unflashed(self) -> bool:
        return self.firmware == FirmwareState.Unflashed

    def __repr__(self) -> str:
        return f"<Device [{self.firmware.value}] {self.name} -> {self.device_path}> {self.symlink_name} "


class SerialScanner:
    SERIAL_PATH = "/dev/serial/by-id/"

    def _detect_firmware(self, name: str) -> FirmwareState:
        if "Klipper" in name:
            return FirmwareState.Klipper
        if "Katapult" in name:
            return FirmwareState.Katapult
        if "CanBoot" in name:
            return FirmwareState.Katapult

        if any(x in name for x in ("1a86", "FTDI", "Silicon_Labs", "Prolific")):
            return FirmwareState.Unflashed

        return FirmwareState.Unknown

    def extract_mcu(self, product: str) -> str:
        """Extract mcu information"""
        return product.split("_")[0] if product else ""

    def _parse_symlink(self, symlink_name: str, resolved: str) -> Device:

        d = Device()

        d.symlink_name = symlink_name
        d.device_path = resolved
        d.firmware = self._detect_firmware(symlink_name)

        s = symlink_name
        if s.startswith("usb-"):
            s = s[4:]

        if "-if" in s:
            if_pos = s.rfind("-if")
            d.interface = s[if_pos + 3 :].split("-")[0]
            s = s[:if_pos]

        parts = s.split("_")
        if len(parts) >= 3:
            d.manufacturer = parts[0]
            d.serial_number = parts[-1]
            d.product = "_".join(parts[1:-1])
        elif len(parts) == 2:
            d.manufacturer = parts[0]
            d.product = parts[1]
        else:
            d.manufacturer = s

        if d.firmware in (FirmwareState.Klipper, FirmwareState.Katapult):
            d.mcu_type = self.extract_mcu(d.product)

        d.name = f"{d.manufacturer} {d.mcu_type or d.product}".strip()

        return d

    def scan(self) -> list[Device]:
        """Scan for serial devices compatible with klipper
        Equivalent to ls /dev/serial/by-id/*
        """
        if not os.path.exists(self.SERIAL_PATH):
            return []

        devs = []
        for path in glob.glob(f"{self.SERIAL_PATH}/*"):
            try:
                symlink_name = os.path.basename(path)
                resolved = os.path.realpath(path)
                devs.append(self._parse_symlink(symlink_name, resolved))
            except OSError as e:
                _logger.info("[SerialScanner] Skipping: %s: %s" % (path, e))

        return devs

    def scan_klipper(self) -> list[Device]:
        """Scans for Klipper serial devices"""
        return [d for d in self.scan() if d.is_klipper]

    def scan_katapult(self) -> list[Device]:
        """Scans for katapult serial devices"""
        return [d for d in self.scan() if d.is_katapult]

    def scan_unflashed(self) -> list[Device]:
        """Scans for unflashed serial devices"""
        return [d for d in self.scan() if d.is_unflashed]
