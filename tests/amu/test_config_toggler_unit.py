"""Unit tests for BlocksScreen.devices.amu.config_toggler."""

import pytest
from BlocksScreen.devices.amu.config_toggler import ConfigToggler
from tests.amu.conftest import COMMENTED_CFG, UNCOMMENTED_CFG


class TestConfigTogglerInit:
    def test_missing_file_sets_path_none(self, tmp_path) -> None:
        ct = ConfigToggler(tmp_path / "nonexistent.cfg")
        assert ct._path is None

    def test_commented_file_is_not_configured(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        assert ConfigToggler(cfg).is_configured() is False

    def test_uncommented_file_is_configured(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(UNCOMMENTED_CFG)
        assert ConfigToggler(cfg).is_configured() is True


class TestConfigTogglerToggle:
    def test_no_file_returns_false(self, tmp_path) -> None:
        ct = ConfigToggler(tmp_path / "nonexistent.cfg")
        assert ct.toggle(True) is False

    def test_activate_uncomments_includes(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        assert ct.toggle(True) is True
        assert cfg.read_text() == UNCOMMENTED_CFG

    def test_deactivate_comments_includes(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(UNCOMMENTED_CFG)
        ct = ConfigToggler(cfg)
        assert ct.toggle(False) is True
        assert cfg.read_text() == COMMENTED_CFG

    def test_same_state_returns_false(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        assert ct.toggle(False) is False

    def test_oserror_returns_false(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        cfg.chmod(0o000)
        try:
            assert ct.toggle(True) is False
        finally:
            cfg.chmod(0o644)
