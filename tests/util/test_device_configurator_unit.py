"""DeviceConfigManager: boot-time sync with device templates, and hotplug apply."""

import os
import pathlib
import sys

import pytest

_BS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "BlocksScreen")
)
if _BS_DIR not in sys.path:
    sys.path.append(_BS_DIR)

from devices.discovery.serial_devices import Device  # noqa: E402
from tools.configuration_manager import device_configurator as dc  # noqa: E402
from tools.configuration_manager.device_configurator import (  # noqa: E402
    DeviceConfigManager,
    DeviceConsent,
)
from tools.configuration_manager.device_profiles import load_profiles  # noqa: E402

from .test_device_profiles_unit import AMU, BEACON, PRINTER_CFG  # noqa: E402

VARIABLES_CFG = "[Variables]\nspeed = 100\n"


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
def dirs(tmp_path):
    repo = tmp_path / "RF50-Klipper"
    config_dir = tmp_path / "config"
    (repo / ".git").mkdir(parents=True)
    config_dir.mkdir()
    (repo / "printer.cfg").write_text(PRINTER_CFG)
    (repo / "variables.cfg").write_text(VARIABLES_CFG)
    return repo, config_dir, tmp_path / "backup"


@pytest.fixture
def consent_path(tmp_path):
    return tmp_path / "state" / "device_consent.json"


def _accept_amu(consent_path):
    DeviceConsent(consent_path).accept(["amu"])


def _boot(dirs, monkeypatch, devices, consent_path=None, accepted=True):
    """Construct the manager like the app does at startup (runs sync()).

    accepted: the user already said yes to the AMU prompt on an earlier run
    (the default, so the layout tests below see the AMU template applied).
    """
    repo, config_dir, backup = dirs
    if consent_path is None:
        consent_path = repo.parent / "state" / "device_consent.json"
    if accepted:
        _accept_amu(consent_path)
    monkeypatch.setattr(
        DeviceConfigManager, "scan_devices", staticmethod(lambda: list(devices))
    )
    return DeviceConfigManager(
        _Config(
            {
                "config_repo": str(repo),
                "config_dir": str(config_dir),
                "backup_dir": str(backup),
                "copy_files": None,
            }
        ),
        profiles=load_profiles(override=None),
        consent=DeviceConsent(consent_path),
    )


def _printer_cfg(dirs) -> str:
    return (dirs[1] / "printer.cfg").read_text()


def _assert_amu_layout(text: str):
    assert f"[mcu mmu]\nserial: {AMU.symlink}\n" in text
    assert "\n[include config/variant_mmu/base/*.cfg]\n" in text
    assert "\n#[include config/variant_sync_single/*.cfg ]\n" in text


def _assert_repo_layout(text: str):
    assert "[mcu mmu]" not in text
    assert "\n#[include config/variant_mmu/base/*.cfg]\n" in text
    assert "\n[include config/variant_sync_single/*.cfg ]\n" in text


class TestBoot:
    def test_fresh_machine_with_amu(self, dirs, monkeypatch):
        _boot(dirs, monkeypatch, [AMU, BEACON])
        text = _printer_cfg(dirs)
        _assert_amu_layout(text)
        assert f"[beacon]\nserial: {BEACON.symlink}\n" in text

    def test_fresh_machine_without_devices_equals_repo(self, dirs, monkeypatch):
        _boot(dirs, monkeypatch, [])
        assert _printer_cfg(dirs) == PRINTER_CFG

    def test_amu_unplugged_since_last_boot_is_reverted(self, dirs, monkeypatch):
        _boot(dirs, monkeypatch, [AMU, BEACON])
        _assert_amu_layout(_printer_cfg(dirs))
        _boot(dirs, monkeypatch, [BEACON])
        text = _printer_cfg(dirs)
        _assert_repo_layout(text)
        # byte-for-byte the repo file apart from the beacon serial - no
        # banner or blank line lost around where [mcu mmu] was
        assert text == PRINTER_CFG.replace(
            "[beacon]\nserial:\n", f"[beacon]\nserial: {BEACON.symlink}\n"
        )

    def test_repo_changes_still_sync_with_amu(self, dirs, monkeypatch):
        repo = dirs[0]
        _boot(dirs, monkeypatch, [AMU])
        (repo / "printer.cfg").write_text(
            PRINTER_CFG.replace(
                "kinematics: corexy", "kinematics: corexy\nmax_velocity: 500"
            )
        )
        _boot(dirs, monkeypatch, [AMU])
        text = _printer_cfg(dirs)
        assert "max_velocity: 500" in text
        _assert_amu_layout(text)
        assert text.count("[mcu mmu]") == 1

    def test_templates_only_touch_printer_cfg(self, dirs, monkeypatch):
        repo, config_dir, _ = dirs
        (config_dir / "variables.cfg").write_text("[Variables]\nspeed = 50\n")
        _boot(dirs, monkeypatch, [AMU, BEACON])
        variables = (config_dir / "variables.cfg").read_text()
        assert "AMU" not in variables and "beacon" not in variables.lower()


class TestApplyDevices:
    def test_hotplug_amu(self, dirs, monkeypatch):
        manager = _boot(dirs, monkeypatch, [])
        assert manager.apply_devices([AMU]) == ["amu"]
        _assert_amu_layout(_printer_cfg(dirs))
        assert manager.apply_devices([AMU]) == []  # already applied

    def test_unknown_device_changes_nothing(self, dirs, monkeypatch):
        manager = _boot(dirs, monkeypatch, [])
        before = _printer_cfg(dirs)
        assert (
            manager.apply_devices(
                [Device(symlink_name="usb-1a86_USB_Serial-if00-port0")]
            )
            == []
        )
        assert _printer_cfg(dirs) == before

    def test_missing_printer_cfg(self, dirs, monkeypatch):
        manager = _boot(dirs, monkeypatch, [])
        (dirs[1] / "printer.cfg").unlink()
        assert manager.apply_devices([AMU]) == []
        assert not pathlib.Path(dirs[1] / "printer.cfg").exists()


class TestConfirmation:
    """The AMU template asks first: nothing is written before the user accepts."""

    def test_boot_leaves_unaccepted_amu_alone(self, dirs, monkeypatch, consent_path):
        manager = _boot(dirs, monkeypatch, [AMU], consent_path, accepted=False)
        assert _printer_cfg(dirs) == PRINTER_CFG
        assert manager.pending_confirmation([AMU]) == ["amu"]

    def test_hotplug_unaccepted_amu_is_not_applied(
        self, dirs, monkeypatch, consent_path
    ):
        manager = _boot(dirs, monkeypatch, [], consent_path, accepted=False)
        assert manager.apply_devices([AMU]) == []
        assert _printer_cfg(dirs) == PRINTER_CFG
        assert manager.pending_confirmation([AMU]) == ["amu"]

    def test_beacon_needs_no_confirmation(self, dirs, monkeypatch, consent_path):
        manager = _boot(dirs, monkeypatch, [], consent_path, accepted=False)
        assert manager.pending_confirmation([BEACON]) == []
        assert manager.apply_devices([BEACON]) == ["beacon"]

    def test_accept_applies_and_persists_across_reboot(
        self, dirs, monkeypatch, consent_path
    ):
        manager = _boot(dirs, monkeypatch, [], consent_path, accepted=False)
        manager.accept(["amu"])
        assert manager.apply_devices([AMU]) == ["amu"]
        _assert_amu_layout(_printer_cfg(dirs))
        assert manager.pending_confirmation([AMU]) == []
        # Reboot with the AMU still plugged: consent was saved, config stays,
        # and printer.cfg is not rewritten.
        before = _printer_cfg(dirs)
        rebooted = _boot(dirs, monkeypatch, [AMU], consent_path, accepted=False)
        assert _printer_cfg(dirs) == before
        assert rebooted.boot_changed is False
        assert rebooted.pending_confirmation([AMU]) == []

    def test_consent_file_survives_garbage(self, consent_path):
        consent_path.parent.mkdir(parents=True)
        consent_path.write_text("{not json")
        consent = DeviceConsent(consent_path)
        assert not consent.is_accepted("amu")
        consent.accept(["amu"])
        assert DeviceConsent(consent_path).is_accepted("amu")


class TestBootChanged:
    def test_unchanged_boot(self, dirs, monkeypatch):
        _boot(dirs, monkeypatch, [AMU])
        assert _boot(dirs, monkeypatch, [AMU]).boot_changed is False

    def test_amu_plugged_while_off(self, dirs, monkeypatch):
        _boot(dirs, monkeypatch, [])
        assert _boot(dirs, monkeypatch, [AMU]).boot_changed is True

    def test_amu_removed_while_off(self, dirs, monkeypatch):
        _boot(dirs, monkeypatch, [AMU])
        assert _boot(dirs, monkeypatch, []).boot_changed is True


class TestScanDevices:
    def test_by_id_listing_fills_in_what_the_daemon_missed(self, monkeypatch):
        other = Device(symlink_name="usb-Klipper_stm32h723xx_29003A00-if00")
        monkeypatch.setattr(
            dc.SerialScanner, "scan", lambda self: [other]
        )  # daemon answered, without the AMU
        monkeypatch.setattr(
            dc.SerialScanner, "legacy_scan", staticmethod(lambda: [other, AMU])
        )
        names = [d.symlink_name for d in DeviceConfigManager.scan_devices()]
        assert names == [other.symlink_name, AMU.symlink_name]

    def test_scan_errors_never_raise(self, monkeypatch):
        def boom(*_):
            raise RuntimeError("scan bug")

        monkeypatch.setattr(dc.SerialScanner, "scan", boom)
        monkeypatch.setattr(dc.SerialScanner, "legacy_scan", staticmethod(boom))
        assert DeviceConfigManager.scan_devices() == []


class TestAtomicWrite:
    def test_keeps_mode_and_symlink(self, tmp_path):
        real = tmp_path / "real.cfg"
        real.write_text("old\n")
        os.chmod(real, 0o640)
        link = tmp_path / "printer.cfg"
        link.symlink_to(real)
        dc.atomic_write_text(link, "new\n")
        assert link.is_symlink()
        assert real.read_text() == "new\n"
        assert real.stat().st_mode & 0o777 == 0o640
        assert [p.name for p in tmp_path.iterdir() if p.name.startswith(".")] == []

    def test_failed_write_leaves_file_untouched(self, tmp_path, monkeypatch):
        target = tmp_path / "printer.cfg"
        target.write_text("old\n")

        def fail(*_):
            raise OSError("disk full")

        monkeypatch.setattr(dc.os, "replace", fail)
        with pytest.raises(OSError):
            dc.atomic_write_text(target, "new\n")
        assert target.read_text() == "old\n"
        assert [p.name for p in tmp_path.iterdir()] == ["printer.cfg"]
