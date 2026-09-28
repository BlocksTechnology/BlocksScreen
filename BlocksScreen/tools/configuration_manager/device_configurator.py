"""Device-aware configuration manager.

`DeviceConfigManager` is `ConfigManager` (configurator.py, left unchanged)
plus device templates (device_profiles.py):

- At startup it syncs ~/printer_data/config from the config repo as before,
  then applies the templates of the devices plugged in right now. So
  printer.cfg always equals the repo's version plus what the connected
  devices require - an AMU unplugged since the last boot is reverted too.
- While running, `apply_devices()` applies templates for devices reported by
  the discovery daemon (see device_watcher.py).

Profiles marked `confirm: true` (the AMU) are only applied once the user has
accepted them (`accept()`, persisted in `DeviceConsent`). Until then boot
leaves printer.cfg alone for them and `pending_confirmation()` reports them,
so the UI can ask.
"""

from __future__ import annotations

import json
import logging
import os
import pathlib
import shutil
import tempfile
from collections.abc import Iterable, Sequence

from devices.discovery.serial_devices import Device, SerialScanner

from .configurator import ConfigManager
from .device_profiles import (
    DeviceProfile,
    apply_device_profiles,
    load_profiles,
    match_devices,
)

_logger = logging.getLogger(__name__)

PRINTER_CFG = "printer.cfg"
# The boot scan runs before the UI exists. A healthy daemon answers in
# milliseconds; this bounds how long a hung one can delay startup before the
# legacy /dev/serial/by-id scan is used instead.
BOOT_SCAN_TIMEOUT = 1.0

CONSENT_PATH = pathlib.Path.home() / ".config" / "blockscreen" / "device_consent.json"


def atomic_write_text(path: pathlib.Path, text: str) -> None:
    """Replace path's content in one step: readers see the old or the new file.

    Klipper may read printer.cfg at any moment (its own start, a restart), and
    a power cut mid-write must not leave a truncated file - the next boot's
    merge would then rebuild it from the repo and lose the SAVE_CONFIG block.
    Symlinks are followed so the link itself is kept.
    """
    target = path.resolve()
    fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        if target.exists():
            shutil.copymode(target, tmp)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


class DeviceConsent:
    """Profile names the user accepted, kept across reboots."""

    def __init__(self, path: pathlib.Path | None = CONSENT_PATH) -> None:
        self._path = path
        self._accepted: set[str] = set()
        if path is None:
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self._accepted = {str(n) for n in data.get("accepted", [])}
        except FileNotFoundError:
            pass
        except (OSError, ValueError, AttributeError, TypeError) as e:
            _logger.error("Ignoring unreadable device consent file %s: %s", path, e)

    def is_accepted(self, name: str) -> bool:
        """Whether the user accepted the profile called name"""
        return name in self._accepted

    def accept(self, names: Iterable[str]) -> None:
        """Remember names as accepted (saved immediately)"""
        new = set(names) - self._accepted
        if not new:
            return
        self._accepted |= new
        if self._path is None:
            return
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            atomic_write_text(
                self._path, json.dumps({"accepted": sorted(self._accepted)}) + "\n"
            )
        except OSError as e:
            # Still accepted for this session; boot will just ask again.
            _logger.error("Cannot save device consent to %s: %s", self._path, e)


class DeviceConfigManager(ConfigManager):
    """ConfigManager that edits printer.cfg for the devices that are plugged in."""

    def __init__(
        self,
        config,
        profiles: Sequence[DeviceProfile] | None = None,
        consent: DeviceConsent | None = None,
    ) -> None:
        # ConfigManager.__init__ ends by calling sync(), which needs these.
        self._profiles: list[DeviceProfile] = list(
            load_profiles() if profiles is None else profiles
        )
        self._consent = consent if consent is not None else DeviceConsent()
        self._devices: list[Device] = []
        self._merging: str | None = None
        # Set by sync(): printer.cfg differs from what it was before this
        # boot's sync, so a Klipper that already loaded it must restart.
        self.boot_changed = False
        _logger.info(
            "Device profiles: %s", ", ".join(p.name for p in self._profiles) or "none"
        )
        super().__init__(config)

    @property
    def printer_cfg(self) -> pathlib.Path:
        """The machine's printer.cfg"""
        return self.config_dir / PRINTER_CFG

    def _allowed_profiles(self) -> list[DeviceProfile]:
        return [
            p
            for p in self._profiles
            if not p.confirm or self._consent.is_accepted(p.name)
        ]

    @staticmethod
    def scan_devices() -> list[Device]:
        """Serial devices plugged in now: the daemon's view plus /dev/serial/by-id.

        Both are consulted because the daemon can answer before it has
        enumerated a board udev already linked (early boot), and a device
        missing here gets its config stripped from printer.cfg.
        """
        devices: list[Device] = []
        try:
            devices = SerialScanner(timeout=BOOT_SCAN_TIMEOUT).scan()
        except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
            # Never let a scan problem stop the config sync at boot.
            _logger.error("Device scan failed: %s", e)
        try:
            seen = {d.symlink_name for d in devices}
            devices += [
                d for d in SerialScanner.legacy_scan() if d.symlink_name not in seen
            ]
        except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
            _logger.error("Legacy device scan failed: %s", e)
        return devices

    def _read_printer_cfg(self) -> str | None:
        try:
            return self.printer_cfg.read_text(encoding="utf-8")
        except OSError:
            return None

    def sync(self) -> None:
        """Sync the machine configuration with the repo, then apply device templates.

        Runs every step unconditionally: each one only writes when something
        differs. (ConfigManager.sync skips syncing when every copied file
        differs from the repo, which is exactly when it's needed.)
        """
        before = self._read_printer_cfg()
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
        self.boot_changed = self._read_printer_cfg() != before
        if self.boot_changed:
            _logger.info("printer.cfg changed during boot sync")

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
        text, _ = apply_device_profiles(
            config_text, self._allowed_profiles(), self._devices
        )
        return text

    def matching_profiles(self, device: Device) -> list[str]:
        """Names of the profiles that recognise device (for logging)"""
        return [p.name for p in self._profiles if p.matches(device)]

    def pending_confirmation(self, devices: Sequence[Device]) -> list[str]:
        """Matched profiles waiting for the user's OK that would change printer.cfg"""
        waiting = [
            p
            for p in self._profiles
            if p.confirm and not self._consent.is_accepted(p.name)
        ]
        if not devices or not waiting:
            return []
        text = self._read_printer_cfg()
        if text is None:
            _logger.warning(
                "Cannot read %s to check device templates", self.printer_cfg
            )
            return []
        names = []
        for profile, device in match_devices(waiting, devices):
            _, changed = apply_device_profiles(text, [profile], [device])
            if changed:
                names.append(profile.name)
            else:
                _logger.info(
                    "%s matches %s but printer.cfg already has its layout",
                    device.symlink_name,
                    profile.name,
                )
        return names

    def accept(self, names: Iterable[str]) -> None:
        """Record that the user accepted these profiles (then call apply_devices)."""
        self._consent.accept(names)

    def apply_devices(self, devices: Sequence[Device]) -> list[str]:
        """Apply the allowed templates matching devices to printer.cfg.

        Returns the names of the profiles that changed the file (empty when
        nothing had to change or printer.cfg couldn't be read/written).
        """
        profiles = self._allowed_profiles()
        if not devices or not profiles:
            return []
        path = self.printer_cfg
        with self.mergeLock:
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as e:
                _logger.error("Cannot read %s: %s", path, e)
                return []
            new_text, changed = apply_device_profiles(text, profiles, devices)
            if not changed:
                return []
            try:
                atomic_write_text(path, new_text)
            except OSError as e:
                _logger.error("Cannot write %s: %s", path, e)
                return []
        _logger.info("printer.cfg updated for: %s", ", ".join(changed))
        return changed
