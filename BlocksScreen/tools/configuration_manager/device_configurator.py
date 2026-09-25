"""Device-aware configuration manager.

`DeviceConfigManager` is `ConfigManager` (configurator.py, left unchanged)
plus device templates (device_profiles.py):

- At startup it syncs ~/printer_data/config from the config repo as before,
  then applies the templates of the devices plugged in right now. So
  printer.cfg always equals the repo's version plus what the connected
  devices require - an AMU unplugged since the last boot is reverted too.
- While running, `apply_devices()` applies templates for devices reported by
  the discovery daemon (see device_watcher.py).
"""

from __future__ import annotations

import logging
import pathlib
from collections.abc import Sequence

from devices.discovery.serial_devices import Device, SerialScanner

from .configurator import ConfigManager
from .device_profiles import DeviceProfile, apply_device_profiles, load_profiles

_logger = logging.getLogger(__name__)

PRINTER_CFG = "printer.cfg"
# The boot scan runs before the UI exists. A healthy daemon answers in
# milliseconds; this bounds how long a hung one can delay startup before the
# legacy /dev/serial/by-id scan is used instead.
BOOT_SCAN_TIMEOUT = 1.0


class DeviceConfigManager(ConfigManager):
    """ConfigManager that edits printer.cfg for the devices that are plugged in."""

    def __init__(self, config, profiles: Sequence[DeviceProfile] | None = None) -> None:
        # ConfigManager.__init__ ends by calling sync(), which needs these.
        self._profiles: list[DeviceProfile] = list(
            load_profiles() if profiles is None else profiles
        )
        self._devices: list[Device] = []
        self._merging: str | None = None
        _logger.info(
            "Device profiles: %s", ", ".join(p.name for p in self._profiles) or "none"
        )
        super().__init__(config)

    @property
    def printer_cfg(self) -> pathlib.Path:
        """The machine's printer.cfg"""
        return self.config_dir / PRINTER_CFG

    @staticmethod
    def scan_devices() -> list[Device]:
        """Serial devices plugged in now (daemon, or the legacy scan as fallback)"""
        try:
            return SerialScanner(timeout=BOOT_SCAN_TIMEOUT).scan()
        except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
            # Never let a scan problem stop the config sync at boot.
            _logger.error("Device scan failed: %s", e)
            return []

    def sync(self) -> None:
        """Sync the machine configuration with the repo, then apply device templates.

        Runs every step unconditionally: each one only writes when something
        differs. (ConfigManager.sync skips syncing when every copied file
        differs from the repo, which is exactly when it's needed.)
        """
        self._devices = self.scan_devices()
        _logger.info(
            "Devices at sync: %s",
            ", ".join(d.symlink_name for d in self._devices) or "none",
        )
        try:
            missing = self._get_missing_symlinks(self.config_dir, self.repo)
            if self.check_nested():
                self._cleanup_nested()
            self.cleanup_broken_symlinks(self.config_dir)
            self._symlink_config(missing)
            self._cpy_cfg_files()
        except (NotADirectoryError, FileNotFoundError) as e:
            _logger.error("%s", e)
        except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
            _logger.error("Caught exception during sync: %s", e)
        # printer.cfg may have been skipped above (already equal to the repo's
        # copy), so make sure the templates are applied either way.
        try:
            self.apply_devices(self._devices)
        except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
            _logger.error("Applying device templates failed: %s", e)

    def merge_cfg(self, src_file, target_file, marker="") -> bool:
        """ConfigManager.merge_cfg, remembering which file is being merged"""
        self._merging = pathlib.Path(target_file).name
        try:
            return super().merge_cfg(src_file, target_file, marker)
        finally:
            self._merging = None

    def _fix_beacon_serial(self, config_text: str) -> str:
        # Hook ConfigManager.merge_cfg calls on every merged file before
        # writing it. Applying the templates here (printer.cfg only) means
        # a boot with an AMU plugged in writes printer.cfg once, instead of
        # writing the repo layout and then the AMU layout. Beacon is one of
        # the templates, so the old beacon lookup isn't needed.
        if self._merging != PRINTER_CFG:
            return config_text
        text, _ = apply_device_profiles(config_text, self._profiles, self._devices)
        return text

    def apply_devices(self, devices: Sequence[Device]) -> list[str]:
        """Apply the templates matching devices to printer.cfg.

        Returns the names of the profiles that changed the file (empty when
        nothing had to change or printer.cfg couldn't be read/written).
        """
        if not devices or not self._profiles:
            return []
        path = self.printer_cfg
        with self.mergeLock:
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as e:
                _logger.error("Cannot read %s: %s", path, e)
                return []
            new_text, changed = apply_device_profiles(text, self._profiles, devices)
            if not changed:
                return []
            try:
                path.write_text(new_text, encoding="utf-8")
            except OSError as e:
                _logger.error("Cannot write %s: %s", path, e)
                return []
        _logger.info("printer.cfg updated for: %s", ", ".join(changed))
        return changed
