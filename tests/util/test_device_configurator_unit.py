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
from tools.configuration_manager.device_configurator import (  # noqa: E402
    DeviceConfigManager,
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


def _boot(dirs, monkeypatch, devices):
    """Construct the manager like the app does at startup (runs sync())."""
    repo, config_dir, backup = dirs
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
    )


def _printer_cfg(dirs) -> str:
    return (dirs[1] / "printer.cfg").read_text()


def _assert_amu_layout(text: str):
    assert f"[mcu AMU]\nserial: {AMU.symlink}\n" in text
    assert "\n[include config/variant_mmu/base/*.cfg]\n" in text
    assert "\n#[include config/variant_sync_single/*.cfg ]\n" in text


def _assert_repo_layout(text: str):
    assert "[mcu AMU]" not in text
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
        # banner or blank line lost around where [mcu AMU] was
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
        assert text.count("[mcu AMU]") == 1

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
