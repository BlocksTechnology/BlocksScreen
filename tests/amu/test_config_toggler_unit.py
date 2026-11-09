"""Unit tests for BlocksScreen.devices.amu.config_toggler."""

import os
from pathlib import Path

import pytest

from BlocksScreen.devices.amu.config_toggler import (
    AMU_INCLUDE,
    SINGLE_INCLUDE,
    ConfigToggler,
    ToggleResult,
)
from tests.amu.conftest import COMMENTED_CFG, UNCOMMENTED_CFG

# Sibling RF50-Klipper checkout, absent in CI.
_REAL_PRINTER_CFG = Path(__file__).parents[2].parent / "RF50-Klipper" / "printer.cfg"

# root bypasses file modes, so the chmod-based failures never happen.
_not_root = pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file modes")


class TestConfigTogglerInit:
    def test_missing_file_sets_path_none(self, tmp_path) -> None:
        ct = ConfigToggler(tmp_path / "nonexistent.cfg")
        assert ct._path is None
        assert ct.is_configured() is False

    def test_unreadable_file_is_not_configured(self, tmp_path) -> None:
        unreadable = tmp_path / "printer.cfg"
        unreadable.mkdir()
        assert ConfigToggler(unreadable).is_configured() is False

    def test_commented_file_is_not_configured(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        assert ConfigToggler(cfg).is_configured() is False

    def test_uncommented_file_is_configured(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(UNCOMMENTED_CFG)
        assert ConfigToggler(cfg).is_configured() is True


class TestConfigTogglerToggle:
    def test_no_file_fails(self, tmp_path) -> None:
        ct = ConfigToggler(tmp_path / "nonexistent.cfg")
        assert ct.toggle(True) is ToggleResult.FAILED

    # toggle() never reaches _write() without a path; pin the guard anyway.
    def test_write_without_a_path_refuses(self, tmp_path) -> None:
        ct = ConfigToggler(tmp_path / "nonexistent.cfg")
        assert ct._write("anything") is False
        assert not list(tmp_path.iterdir())

    def test_activate_uncomments_includes(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        assert ct.toggle(True) is ToggleResult.CHANGED
        assert cfg.read_text() == UNCOMMENTED_CFG

    def test_deactivate_comments_includes(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(UNCOMMENTED_CFG)
        ct = ConfigToggler(cfg)
        assert ct.toggle(False) is ToggleResult.CHANGED
        assert cfg.read_text() == COMMENTED_CFG

    # UNCHANGED, not FAILED: an already-correct config is not an error.
    def test_same_state_is_unchanged(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        assert ct.toggle(False) is ToggleResult.UNCHANGED

    def test_toggle_keeps_symlink(self, tmp_path) -> None:
        """os.replace() would swap a symlinked printer.cfg for a regular file."""
        real = tmp_path / "real.cfg"
        real.write_text(COMMENTED_CFG)
        link = tmp_path / "printer.cfg"
        link.symlink_to(real)
        assert ConfigToggler(link).toggle(True) is ToggleResult.CHANGED
        assert link.is_symlink()
        assert real.read_text() == UNCOMMENTED_CFG

    def test_non_ascii_config_round_trips(self, tmp_path) -> None:
        """read_text() without encoding raises UnicodeDecodeError under LC_ALL=C."""
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG + "# nozzle 220ºC\n", encoding="utf-8")
        assert ConfigToggler(cfg).toggle(True) is ToggleResult.CHANGED
        assert cfg.read_text(encoding="utf-8").endswith("# nozzle 220ºC\n")

    def test_undecodable_byte_round_trips(self, tmp_path) -> None:
        """A Latin-1 byte raises ValueError, which no OSError handler would catch."""
        cfg = tmp_path / "printer.cfg"
        cfg.write_bytes(COMMENTED_CFG.encode() + b"# nozzle 220\xbaC\n")
        assert ConfigToggler(cfg).toggle(True) is ToggleResult.CHANGED
        assert cfg.read_bytes().endswith(b"# nozzle 220\xbaC\n")

    def test_crlf_config_keeps_its_line_endings(self, tmp_path) -> None:
        """Default newline handling rewrites a whole CRLF printer.cfg as LF."""
        cfg = tmp_path / "printer.cfg"
        cfg.write_bytes(COMMENTED_CFG.replace("\n", "\r\n").encode())
        assert ConfigToggler(cfg).toggle(True) is ToggleResult.CHANGED
        assert cfg.read_bytes() == UNCOMMENTED_CFG.replace("\n", "\r\n").encode()

    def test_external_rewrite_does_not_wedge_toggle(self, tmp_path) -> None:
        """The configurator and Mainsail rewrite printer.cfg behind a live toggler."""
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        cfg.write_text(UNCOMMENTED_CFG)
        assert ct.toggle(False) is ToggleResult.CHANGED
        assert cfg.read_text() == COMMENTED_CFG

    @_not_root
    def test_oserror_fails(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        cfg.chmod(0o000)
        try:
            assert ct.toggle(True) is ToggleResult.FAILED
        finally:
            cfg.chmod(0o644)

    def test_round_trip_is_byte_identical(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        ct.toggle(True)
        ct.toggle(False)
        assert cfg.read_text() == COMMENTED_CFG


class TestConfigTogglerRefusesBadWrites:
    """The defects that let the wrong include paths ship unnoticed for months."""

    def test_missing_include_returns_false_and_does_not_write(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text("[include config/variant_sync_single/*.cfg ]\n")
        ct = ConfigToggler(cfg)
        assert ct.toggle(True) is ToggleResult.FAILED
        assert cfg.read_text() == "[include config/variant_sync_single/*.cfg ]\n"

    def test_empty_file_returns_false(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text("")
        ct = ConfigToggler(cfg)
        assert ct.toggle(True) is ToggleResult.FAILED

    def test_duplicate_include_returns_false(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG + f"#[include {AMU_INCLUDE}]\n")
        ct = ConfigToggler(cfg)
        assert ct.toggle(True) is ToggleResult.FAILED

    def test_never_leaves_both_variants_active(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        for activate in (True, False, True, False):
            ct.toggle(activate)
            text = cfg.read_text()
            active = [
                inc
                for inc in (AMU_INCLUDE, SINGLE_INCLUDE)
                if ConfigToggler._is_active(text, inc)
            ]
            assert len(active) == 1, (
                f"variants active after toggle({activate}): {active}"
            )

    def test_write_leaves_no_temp_file(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ConfigToggler(cfg).toggle(True)
        assert list(tmp_path.iterdir()) == [cfg]

    def test_dir_sync_failure_still_changed(self, tmp_path, monkeypatch) -> None:
        """The rename already landed, so FAILED here would skip the FIRMWARE_RESTART."""

        def _boom(*_args, **_kwargs):
            raise OSError("no fd")

        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        toggler = ConfigToggler(cfg)
        # os.open is only reached by the parent-directory fsync.
        monkeypatch.setattr(os, "open", _boom)
        assert toggler.toggle(True) is ToggleResult.CHANGED
        assert cfg.read_text() == UNCOMMENTED_CFG

    @_not_root
    def test_preserves_file_mode(self, tmp_path) -> None:
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        cfg.chmod(0o640)
        ConfigToggler(cfg).toggle(True)
        assert cfg.stat().st_mode & 0o777 == 0o640

    @_not_root
    def test_unwritable_dir_leaves_config_intact(self, tmp_path) -> None:
        """A read-only config dir must fail the toggle, not half-write printer.cfg."""
        d = tmp_path / "cfgdir"
        d.mkdir()
        cfg = d / "printer.cfg"
        cfg.write_text(COMMENTED_CFG)
        ct = ConfigToggler(cfg)
        d.chmod(0o500)
        try:
            assert ct.toggle(True) is ToggleResult.FAILED
            assert cfg.read_text() == COMMENTED_CFG
        finally:
            d.chmod(0o700)
        assert list(d.iterdir()) == [cfg]


@pytest.mark.skipif(
    not _REAL_PRINTER_CFG.exists(), reason="sibling RF50-Klipper checkout not present"
)
class TestAgainstRealPrinterCfg:
    """Guards cross-repo coupling: fixtures only test the regex against itself."""

    def test_both_variant_includes_resolve(self) -> None:
        text = _REAL_PRINTER_CFG.read_text()
        for include in (AMU_INCLUDE, SINGLE_INCLUDE):
            assert (
                ConfigToggler._is_active(text, include) or f"[include {include}" in text
            )

    def test_exactly_one_variant_active_on_disk(self) -> None:
        text = _REAL_PRINTER_CFG.read_text()
        active = [
            inc
            for inc in (AMU_INCLUDE, SINGLE_INCLUDE)
            if ConfigToggler._is_active(text, inc)
        ]
        assert len(active) == 1, f"variants active in real printer.cfg: {active}"

    def test_toggle_round_trips_the_real_file(self, tmp_path) -> None:
        original = _REAL_PRINTER_CFG.read_text()
        cfg = tmp_path / "printer.cfg"
        cfg.write_text(original)
        ct = ConfigToggler(cfg)
        assert ct.toggle(True) is ToggleResult.CHANGED
        assert ct.toggle(False) is ToggleResult.CHANGED
        assert cfg.read_text() == original
