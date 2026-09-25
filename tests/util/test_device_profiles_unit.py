"""Device templates (tools/configuration_manager/device_profiles.py): loading and text transforms."""

import os
import re
import sys
import textwrap

import pytest

# App modules import top-level packages; appended so the `BlocksScreen`
# package isn't shadowed by the BlocksScreen/BlocksScreen.py entry script.
_BS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "BlocksScreen")
)
if _BS_DIR not in sys.path:
    sys.path.append(_BS_DIR)

from devices.discovery.serial_devices import Device  # noqa: E402
from tools.configuration_manager import device_profiles as dp  # noqa: E402
from tools.configuration_manager.configurator import SV_CONFIG_MARKER  # noqa: E402

BEACON = Device(symlink_name="usb-Beacon_Beacon_RevH_ABC123-if00")
AMU = Device(symlink_name="usb-Klipper_stm32f446xx_AMU0001-if00")
KLIPPER = Device(symlink_name="usb-Klipper_stm32h723xx_29003A00-if00")

# Shaped like RF50-Klipper's printer.cfg: banners around the variant
# includes, a trailing space inside one include, [mcu]/[beacon]/[mcu pi].
PRINTER_CFG = textwrap.dedent(
    f"""\
    [include hardware/*.cfg]
    ##############################################################################################
    #######################################     Amu System   #####################################
    ##############################################################################################
    #[include config/variant_mmu/base/*.cfg]
    ##############################################################################################
    ####################################### Normal system    #####################################
    ##############################################################################################
    [include config/variant_sync_single/*.cfg ]
    ##############################################################################################

    [mcu]
    canbus_uuid:
    canbus_interface: can0

    [mcu Toolhead] # In the RF50 case it's the EBB-36
    canbus_uuid:

    [beacon]
    serial:

    [mcu pi]
    serial: /tmp/klipper_host_mcu

    ##############################################################################################
    ######################################### KINEMATICS #########################################
    [printer]
    kinematics: corexy

    {SV_CONFIG_MARKER}
    #*# DO NOT EDIT THIS BLOCK OR BELOW. The contents are auto-generated.
    #*#
    #*# [beacon model default]
    #*# model_coef = 1.0
    """
)


@pytest.fixture
def profiles():
    return dp.load_profiles(override=None)


def _by_name(profiles, name):
    return next(p for p in profiles if p.name == name)


class TestLoadProfiles:
    def test_bundled(self, profiles):
        assert [p.name for p in profiles] == ["beacon", "amu"]
        amu = _by_name(profiles, "amu")
        assert amu.section == "mcu AMU"
        assert amu.enable_includes == ("config/variant_mmu/base/*.cfg",)
        assert amu.disable_includes == ("config/variant_sync_single/*.cfg",)

    def _override(self, tmp_path, body, mode=0o644):
        path = tmp_path / "blockscreen_devices.yaml"
        path.write_text(textwrap.dedent(body))
        os.chmod(path, mode)
        return path

    def test_override_merges_by_name_and_adds(self, tmp_path):
        path = self._override(
            tmp_path,
            """\
            profiles:
              - name: amu
                match: 'MyAMU'
              - name: fps
                match: 'FPS'
                section: mcu fps
                options: {serial: '${serial}'}
            """,
        )
        profiles = dp.load_profiles(override=path)
        amu = _by_name(profiles, "amu")
        assert amu.match.pattern == "MyAMU"
        assert amu.section == "mcu AMU"  # untouched keys come from the bundle
        assert _by_name(profiles, "fps").section == "mcu fps"

    def test_override_can_disable(self, tmp_path):
        path = self._override(tmp_path, "profiles: [{name: beacon, enabled: false}]\n")
        assert [p.name for p in dp.load_profiles(override=path)] == ["amu"]

    def test_group_writable_override_is_ignored(self, tmp_path):
        path = self._override(
            tmp_path, "profiles: [{name: beacon, enabled: false}]\n", mode=0o664
        )
        assert [p.name for p in dp.load_profiles(override=path)] == ["beacon", "amu"]

    def test_invalid_entries_are_skipped(self, tmp_path):
        path = self._override(
            tmp_path,
            """\
            profiles:
              - name: nosection
                match: 'x'
              - name: badregex
                match: '('
                section: foo
            """,
        )
        assert [p.name for p in dp.load_profiles(override=path)] == ["beacon", "amu"]

    def test_missing_bundle_gives_no_profiles(self, tmp_path):
        assert dp.load_profiles(bundled=tmp_path / "nope.yaml", override=None) == []

    def test_vendor_id_accepts_hex_string_and_int(self, tmp_path):
        path = self._override(
            tmp_path,
            """\
            profiles:
              - name: amu
                vendor_id: '0x1d50'
                product_id: 24577
            """,
        )
        amu = _by_name(dp.load_profiles(override=path), "amu")
        assert amu.vendor_id == 0x1D50
        assert amu.product_id == 24577  # == 0x6001

    def test_product_id_without_vendor_id_is_rejected(self, tmp_path):
        path = self._override(
            tmp_path,
            """\
            profiles:
              - name: fps
                match: 'FPS'
                section: mcu fps
                product_id: '0x6001'
            """,
        )
        assert [p.name for p in dp.load_profiles(override=path)] == ["beacon", "amu"]

    def test_bad_vendor_id_string_is_rejected(self, tmp_path):
        path = self._override(
            tmp_path,
            """\
            profiles:
              - name: fps
                match: 'FPS'
                section: mcu fps
                vendor_id: 'nonsense'
            """,
        )
        assert [p.name for p in dp.load_profiles(override=path)] == ["beacon", "amu"]

    def test_duplicate_ids_across_profiles_are_logged(self, tmp_path, caplog):
        path = self._override(
            tmp_path,
            """\
            profiles:
              - name: fps
                match: 'FPS'
                section: mcu fps
                vendor_id: '0x1d50'
                product_id: '0xb001'
            """,
        )
        with caplog.at_level("ERROR"):
            profiles = dp.load_profiles(override=path)
        # Both profiles are still loaded - misconfiguration is surfaced, not silently fixed.
        assert {p.name for p in profiles} == {"beacon", "amu", "fps"}
        assert "amu" in caplog.text and "fps" in caplog.text and "0xb001" in caplog.text


class TestMatch:
    def test_case_insensitive_on_by_id_name(self, profiles):
        pairs = dp.match_devices(profiles, [KLIPPER, AMU, BEACON])
        assert [(p.name, d.symlink_name) for p, d in pairs] == [
            ("beacon", BEACON.symlink_name),
            ("amu", AMU.symlink_name),
        ]

    def test_unknown_devices_match_nothing(self, profiles):
        assert dp.match_devices(profiles, [KLIPPER]) == []

    def test_two_devices_matching_one_profile_uses_first_and_logs(
        self, profiles, caplog
    ):
        amu2 = Device(symlink_name="usb-Klipper_stm32f446xx_AMU0002-if00")
        with caplog.at_level("WARNING"):
            pairs = dp.match_devices(profiles, [AMU, amu2])
        assert [(p.name, d.symlink_name) for p, d in pairs] == [
            ("amu", AMU.symlink_name)
        ]
        assert "amu" in caplog.text
        assert AMU.symlink_name in caplog.text and amu2.symlink_name in caplog.text


class TestMatchByUsbId:
    PROFILE = dp.DeviceProfile(
        name="amu",
        match=re.compile("AMU"),
        section="mcu AMU",
        vendor_id=0x1D50,
        product_id=0x6001,
    )

    def test_matches_on_id_even_without_symlink_hint(self):
        # No "AMU" anywhere in the symlink - only the USB IDs identify it.
        device = Device(
            symlink_name="usb-Klipper_stm32f446xx_XYZ-if00",
            vendor_id=0x1D50,
            product_id=0x6001,
        )
        assert self.PROFILE.matches(device)

    def test_wrong_product_id_does_not_match_even_with_symlink_hint(self):
        # Regex would match ("AMU" in the name), but the ID says otherwise -
        # ID wins once the device reports one, so a mislabeled/spoofed
        # symlink can't masquerade as the real board.
        device = Device(
            symlink_name="usb-Klipper_stm32f446xx_AMU0001-if00",
            vendor_id=0x1D50,
            product_id=0x9999,
        )
        assert not self.PROFILE.matches(device)

    def test_wrong_vendor_id_does_not_match(self):
        device = Device(
            symlink_name="usb-Klipper_stm32f446xx_AMU0001-if00",
            vendor_id=0x0483,
            product_id=0x6001,
        )
        assert not self.PROFILE.matches(device)

    def test_falls_back_to_regex_when_device_reports_no_id(self):
        # device.vendor_id == 0: legacy scanner, or a daemon that doesn't
        # send USB IDs yet - unchanged regex behaviour.
        assert self.PROFILE.matches(AMU)
        assert not self.PROFILE.matches(KLIPPER)

    def test_profile_without_vendor_id_ignores_device_ids(self):
        profile = dp.DeviceProfile(
            name="amu", match=re.compile("AMU"), section="mcu AMU"
        )
        device = Device(
            symlink_name=KLIPPER.symlink_name, vendor_id=0x1D50, product_id=0x6001
        )
        assert not profile.matches(
            device
        )  # no "AMU" in the symlink, no vendor_id to check

    def test_vendor_id_only_profile_accepts_any_product_id(self):
        profile = dp.DeviceProfile(
            name="amu", match=re.compile("AMU"), section="mcu AMU", vendor_id=0x1D50
        )
        device = Device(symlink_name="whatever", vendor_id=0x1D50, product_id=0xBEEF)
        assert profile.matches(device)


class TestApply:
    def test_amu(self, profiles):
        out = dp.apply_profile(PRINTER_CFG, _by_name(profiles, "amu"), AMU)
        assert "\n[include config/variant_mmu/base/*.cfg]\n" in out
        assert "\n#[include config/variant_sync_single/*.cfg ]\n" in out
        # banners around the includes are untouched
        assert out.count("#" * 94) == PRINTER_CFG.count("#" * 94)
        # new section at a block boundary, just before the last [mcu ...]
        assert (
            "[beacon]\nserial:\n\n"
            "[mcu AMU]\nserial: /dev/serial/by-id/"
            "usb-Klipper_stm32f446xx_AMU0001-if00\n\n"
            "[mcu pi]\nserial: /tmp/klipper_host_mcu\n\n####"
        ) in out

    def test_beacon_fills_existing_section(self, profiles):
        out = dp.apply_profile(PRINTER_CFG, _by_name(profiles, "beacon"), BEACON)
        assert (
            "[beacon]\nserial: /dev/serial/by-id/usb-Beacon_Beacon_RevH_ABC123-if00\n"
            in out
        )
        assert out.count("[beacon]") == 1

    def test_beacon_replaces_stale_serial(self, profiles):
        stale = PRINTER_CFG.replace(
            "[beacon]\nserial:\n", "[beacon]\nserial: /dev/serial/by-id/old  # note\n"
        )
        out = dp.apply_profile(stale, _by_name(profiles, "beacon"), BEACON)
        assert "old" not in out
        assert BEACON.symlink in out

    @pytest.mark.parametrize("devices", [[AMU], [BEACON], [AMU, BEACON]])
    def test_idempotent(self, profiles, devices):
        once, changed = dp.apply_device_profiles(PRINTER_CFG, profiles, devices)
        twice, changed_again = dp.apply_device_profiles(once, profiles, devices)
        assert changed and once != PRINTER_CFG
        assert twice == once and changed_again == []

    def test_save_config_block_untouched(self, profiles):
        cfg = (
            PRINTER_CFG
            + "#*# [mcu AMU]\n#*# [include config/variant_sync_single/*.cfg]\n"
        )
        out, _ = dp.apply_device_profiles(cfg, profiles, [AMU])
        tail = cfg[cfg.index(SV_CONFIG_MARKER) :]
        assert out.endswith(tail)
        assert out.count("[mcu AMU]") == 2  # one new section + the untouched #*# line

    def test_no_marker_and_no_mcu_appends(self, profiles):
        out = dp.apply_profile(
            "[printer]\nkinematics: corexy", _by_name(profiles, "amu"), AMU
        )
        assert out.endswith(f"\n[mcu AMU]\nserial: {AMU.symlink}\n")

    def test_template_placeholders(self):
        profile = dp.DeviceProfile(
            name="x",
            match=re.compile("AMU"),
            section="mcu x",
            options=(("serial", "${serial}"), ("note", "${name} ${unknown}")),
        )
        dev = Device(symlink_name=AMU.symlink_name, name="Klipper stm32f446xx")
        opts = dict(profile.render_options(dev))
        assert opts == {"serial": AMU.symlink, "note": "Klipper stm32f446xx ${unknown}"}

    def test_device_name_cannot_inject_a_config_line(self):
        # device.name is built from the device's own USB manufacturer/product
        # descriptor strings - fully attacker/corruption-controlled. A
        # newline there must never become a newline in printer.cfg.
        profile = dp.DeviceProfile(
            name="x",
            match=re.compile("AMU"),
            section="mcu x",
            options=(("note", "${name}"),),
        )
        dev = Device(
            symlink_name=AMU.symlink_name,
            name="Evil\n[virtual_sdcard]\npath: /root\n#",
        )
        opts = dict(profile.render_options(dev))
        assert "\n" not in opts["note"]
        assert opts["note"] == "Evil[virtual_sdcard]path: /root#"

    def test_apply_profile_with_corrupt_device_name_stays_one_line(self):
        profile = dp.DeviceProfile(
            name="x",
            match=re.compile("AMU"),
            section="mcu x",
            options=(("note", "${name}"),),
        )
        dev = Device(
            symlink_name=AMU.symlink_name, name="Bad\n[printer]\nkinematics: none"
        )
        out = dp.apply_profile("[printer]\nkinematics: corexy", profile, dev)
        lines = out.splitlines()
        # Injected text lands inline in the note value's line - never as its
        # own standalone line/section.
        assert "note: Bad[printer]kinematics: none" in lines
        assert lines.count("[printer]") == 1
        assert "kinematics: none" not in lines
        assert "kinematics: corexy" in lines


class TestSetInclude:
    def test_round_trip(self):
        path = "config/variant_sync_single/*.cfg"
        off = dp.set_include(PRINTER_CFG, path, False)
        assert off != PRINTER_CFG
        assert dp.set_include(off, path, True) == PRINTER_CFG

    def test_banner_line_above_is_not_treated_as_comment(self):
        # regression: `#*` + `\s*` used to swallow the "####" line above
        text = "#####\n[include a.cfg]\n"
        assert dp.set_include(text, "a.cfg", False) == "#####\n#[include a.cfg]\n"
        assert dp.set_include("#####\n#[include a.cfg]\n", "a.cfg", True) == text
