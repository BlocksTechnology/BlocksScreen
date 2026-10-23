"""Unit tests for BlocksScreen.devices.amu.manager."""

import shlex
from unittest.mock import MagicMock, patch

import pytest
from PyQt6 import QtCore

from BlocksScreen.devices.amu.manager import AMUManager
from BlocksScreen.devices.amu.models import MMUState
from tests.amu.conftest import (
    COMMENTED_CFG as _COMMENTED_CFG,
)
from tests.amu.conftest import (
    UNCOMMENTED_CFG as _UNCOMMENTED_CFG,
)


def _klipper_parse(rawparams: str) -> dict[str, str]:
    """Klipper's _get_extended_params (gcode.py:266); its ';' cut only derives cmd."""
    lexer = shlex.shlex(rawparams, posix=True)
    lexer.whitespace_split = True
    lexer.commenters = "#;"
    return {k.upper(): v for k, v in (arg.split("=", 1) for arg in lexer)}


_FULL_STATUS: dict = {
    "enabled": True,
    "is_homed": True,
    "num_gates": 2,
    "tool": 0,
    "gate": 0,
    "filament": "Loaded",
    "action": "Idle",
    "print_state": "standby",
    "reason_for_pause": "",
    "gate_status": [1, -1],
    "gate_material": ["PLA", ""],
    "gate_color": ["ff0000", ""],
    # Lists, not tuples: the status arrives as JSON.
    "gate_color_rgb": [[1.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    "gate_spool_id": [42, -1],
    "ttg_map": [0, 1],
}

_FULL_STATUS_WITH_SPOOLMAN: dict = {
    **_FULL_STATUS,
    "filament_pos": 10,
    "has_bypass": False,
    "spoolman_support": "push",
}


def _status(**overrides: object) -> dict:
    """Full MMU status with per-test overrides."""
    return {**_FULL_STATUS_WITH_SPOOLMAN, **overrides}


_SPOOL_DATA: dict = {
    "id": 42,
    "used_weight": 50.0,
    "remaining_weight": 950.0,
    "filament": {
        "name": "PLA Basic",
        "material": "PLA",
        "color_hex": "ff0000",
        "settings_extruder_temp": 215,
        "settings_bed_temp": 60,
    },
}


# qapp is required: most tests take manager without qtbot.
@pytest.fixture
def manager(tmp_path, qapp):
    """AMUManager with no config file (patched to a non-existent path)."""
    missing = tmp_path / "nonexistent.cfg"
    mock_ws = MagicMock()
    with patch("BlocksScreen.devices.amu.manager.CONFIG_PATH", missing):
        yield AMUManager(ws=mock_ws)


@pytest.fixture
def manager_with_cfg(tmp_path, qapp):
    """AMUManager pointing at a temp printer.cfg with commented includes."""
    cfg = tmp_path / "printer.cfg"
    cfg.write_text(_COMMENTED_CFG)
    mock_ws = MagicMock()
    with patch("BlocksScreen.devices.amu.manager.CONFIG_PATH", cfg):
        yield AMUManager(ws=mock_ws), cfg


class TestAMUManagerInit:
    def test_initial_state_is_none(self, manager) -> None:
        assert manager.get_state() is None

    def test_initial_amu_not_configured(self, manager) -> None:
        assert manager.is_amu_active() is False

    # Qt ownership keeps the manager alive once the caller drops its ref.
    def test_takes_a_qt_parent(self, tmp_path, qapp) -> None:
        parent = QtCore.QObject()
        with patch("BlocksScreen.devices.amu.manager.CONFIG_PATH", tmp_path / "a.cfg"):
            assert AMUManager(ws=MagicMock(), parent=parent).parent() is parent


class TestToggleAMUSystem:
    def test_no_config_emits_false(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.amu_toggled) as blocker:
            manager.toggle_amu_system(True)
        assert blocker.args == [False]

    # An already-correct config is a success, not a failed toggle.
    def test_same_state_emits_true(self, manager_with_cfg, qtbot) -> None:
        mgr, _ = manager_with_cfg
        with qtbot.waitSignal(mgr.amu_toggled) as blocker:
            mgr.toggle_amu_system(False)
        assert blocker.args == [True]

    def test_same_state_does_not_restart_firmware(
        self, manager_with_cfg, qtbot
    ) -> None:
        mgr, _ = manager_with_cfg
        with qtbot.assertNotEmitted(mgr.run_gcode_signal):
            mgr.toggle_amu_system(False)
        mgr._ws.api.firmware_restart.assert_not_called()

    # A config swap restarts the firmware, which would kill the running print.
    @pytest.mark.parametrize("print_state", ["printing", "paused"])
    def test_refused_during_a_print(self, manager_with_cfg, qtbot, print_state) -> None:
        mgr, cfg = manager_with_cfg
        mgr.on_object_updated("print_stats", "print_stats", {"state": print_state})
        with qtbot.waitSignal(mgr.amu_toggled) as blocker:
            mgr.toggle_amu_system(True)
        assert blocker.args == [False]
        assert cfg.read_text() == _COMMENTED_CFG
        mgr._ws.api.firmware_restart.assert_not_called()

    def test_allowed_once_the_print_ends(self, manager_with_cfg, qtbot) -> None:
        mgr, cfg = manager_with_cfg
        mgr.on_object_updated("print_stats", "print_stats", {"state": "printing"})
        mgr.on_object_updated("print_stats", "print_stats", {"state": "complete"})
        with qtbot.waitSignal(mgr.amu_toggled) as blocker:
            mgr.toggle_amu_system(True)
        assert blocker.args == [True]
        assert cfg.read_text() == _UNCOMMENTED_CFG

    # print_stats diffs without "state" must not reset the tracked state.
    def test_print_stats_diff_without_state_is_ignored(
        self, manager_with_cfg, qtbot
    ) -> None:
        mgr, _ = manager_with_cfg
        mgr.on_object_updated("print_stats", "print_stats", {"state": "printing"})
        mgr.on_object_updated("print_stats", "print_stats", {"print_duration": 5.0})
        with qtbot.waitSignal(mgr.amu_toggled) as blocker:
            mgr.toggle_amu_system(True)
        assert blocker.args == [False]

    def test_activate_uncomments_includes(self, manager_with_cfg, qtbot) -> None:
        mgr, cfg = manager_with_cfg
        with qtbot.waitSignal(mgr.amu_toggled) as blocker:
            mgr.toggle_amu_system(True)
        assert blocker.args == [True]
        assert cfg.read_text() == _UNCOMMENTED_CFG

    def test_deactivate_comments_includes(self, manager_with_cfg, qtbot) -> None:
        mgr, cfg = manager_with_cfg
        cfg.write_text(_UNCOMMENTED_CFG)
        with qtbot.waitSignal(mgr.amu_toggled) as blocker:
            mgr.toggle_amu_system(False)
        assert blocker.args == [True]
        assert cfg.read_text() == _COMMENTED_CFG

    def test_activate_sets_amu_configured(self, manager_with_cfg, qtbot) -> None:
        mgr, _ = manager_with_cfg
        with qtbot.waitSignal(mgr.amu_toggled):
            mgr.toggle_amu_system(True)
        assert mgr.is_amu_configured() is True
        assert mgr.is_amu_active() is False


class TestUpdateMMUState:
    def test_first_call_emits_and_stores_state(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.mmu_state_changed) as blocker:
            manager.update_mmu_state(_FULL_STATUS)
        assert blocker.args[0] is manager.get_state()
        assert isinstance(blocker.args[0], MMUState)
        assert blocker.args[0].num_gates == 2

    # A diff-seeded state is gateless and blanks the carousel.
    def test_diff_cannot_seed_state(self, manager, qtbot) -> None:
        with qtbot.assertNotEmitted(manager.mmu_state_changed):
            manager.update_mmu_state({"tool": 1, "filament": "Unloaded"})
        assert manager.get_state() is None

    def test_full_status_after_clear_reseeds(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        manager.on_klippy_state("disconnect")
        manager.update_mmu_state({"tool": 1})
        assert manager.get_state() is None
        manager.update_mmu_state(_FULL_STATUS)
        assert manager.get_state().num_gates == 2

    def test_diff_updates_scalar(self, manager, qtbot) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        with qtbot.waitSignal(manager.mmu_state_changed) as blocker:
            manager.update_mmu_state({"tool": 1, "filament": "Unloaded"})
        state = blocker.args[0]
        assert state.tool == 1
        assert state.filament == "Unloaded"

    def test_diff_preserves_unchanged_fields(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        manager.update_mmu_state({"tool": 1})
        assert manager.get_state().num_gates == 2
        assert manager.get_state().gates[0].material == "PLA"

    # filament_position streams during moves but is not part of the state.
    @pytest.mark.parametrize("diff", [{"filament_position": 12.5}, {"tool": 0}])
    def test_no_op_diff_emits_nothing(self, manager, qtbot, diff) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        with qtbot.assertNotEmitted(manager.mmu_state_changed):
            manager.update_mmu_state(diff)

    def test_same_status_after_restart_emits(self, manager, qtbot) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        manager.on_klippy_state("disconnect")
        with qtbot.waitSignal(manager.mmu_state_changed):
            manager.update_mmu_state(_FULL_STATUS)

    def test_from_status_parses_endless_spool_groups(self, manager) -> None:
        data = {**_FULL_STATUS, "endless_spool_groups": [0, 1, 3, 0]}
        manager.update_mmu_state(data)
        assert manager.get_state().endless_spool_groups == (0, 1, 3, 0)

    def test_from_status_endless_spool_groups_defaults_to_empty(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        assert manager.get_state().endless_spool_groups == ()

    def test_apply_diff_updates_endless_spool_groups(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        manager.update_mmu_state({"endless_spool_groups": [0, 0, 1, 1]})
        assert manager.get_state().endless_spool_groups == (0, 0, 1, 1)


class TestGcodeSignals:
    def test_set_gate_info_without_temp_lets_happy_hare_default_it(
        self, manager, qtbot
    ) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_info(2, "ABS", "0000ff", 3, filament_name="ABS BLACK")
        assert blocker.args == [
            "MMU_GATE_MAP GATE=2 NAME='ABS BLACK' MATERIAL=ABS COLOR=0000ff "
            "SPOOLID=3 QUIET=1"
        ]

    def test_set_gate_info_with_temperature(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_info(
                1,
                "PETG",
                "00ff00",
                7,
                filament_name="PETG Transparent",
                temperature=240,
            )
        assert blocker.args == [
            "MMU_GATE_MAP GATE=1 NAME='PETG Transparent' MATERIAL=PETG COLOR=00ff00 "
            "SPOOLID=7 TEMP=240 QUIET=1"
        ]

    def test_clear_gate(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.clear_gate(1)
        assert blocker.args == [
            "MMU_GATE_MAP GATE=1 NAME='' MATERIAL='' COLOR='' SPOOLID=-1 QUIET=1"
        ]

    def test_set_gate_material(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_material(1, "PETG")
        assert blocker.args == ["MMU_GATE_MAP GATE=1 MATERIAL=PETG TEMP=0 QUIET=1"]

    def test_set_gate_color(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_color(2, "00ff00")
        assert blocker.args == ["MMU_GATE_MAP GATE=2 COLOR=00ff00 TEMP=0 QUIET=1"]

    @pytest.mark.parametrize(("loaded", "flag"), [(True, 1), (False, 0)])
    def test_recover_single_gate(self, manager, qtbot, loaded, flag) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.recover_single_gate(loaded)
        assert blocker.args == [f"MMU_RECOVER GATE=0 LOADED={flag}"]

    # Happy-Hare wants rrggbb or a W3C name, never a '#' prefix.
    @pytest.mark.parametrize("method", ["set_gate_color", "set_gate_info"])
    def test_hash_prefixed_colour_is_stripped(self, manager, qtbot, method) -> None:
        args = (
            (2, "#00ff00") if method == "set_gate_color" else (2, "PLA", "#00ff00", 3)
        )
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            getattr(manager, method)(*args)
        assert "COLOR=00ff00" in blocker.args[0]

    def test_set_gate_temp(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_temp(1, 240)
        assert blocker.args == ["MMU_GATE_MAP GATE=1 TEMP=240 QUIET=1"]

    # Happy-Hare reads TEMP with get_int, which rejects "215.0".
    @pytest.mark.parametrize("temp", [215.0, 214.6])
    def test_float_temp_is_sent_as_an_int(self, manager, qtbot, temp) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_temp(1, temp)
        assert blocker.args == [f"MMU_GATE_MAP GATE=1 TEMP={round(temp)} QUIET=1"]

    @pytest.mark.parametrize("temp", [0, -1, 0.4, float("inf"), float("nan")])
    def test_invalid_temp_emits_no_gcode(self, manager, qtbot, temp) -> None:
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            manager.set_gate_temp(1, temp)

    # Happy-Hare ignores TEMP when Spoolman pull mode owns the gate map.
    def test_temp_skipped_in_pull_mode(self, manager, qtbot) -> None:
        manager.update_mmu_state(_status(spoolman_support="pull"))
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            manager.set_gate_temp(1, 240)

    # Omitted TEMP resets the gate to default_extruder_temp (mmu.py:8627).
    @pytest.mark.parametrize(
        ("method", "args"),
        [
            ("set_gate_material", (1, "PETG")),
            ("set_gate_color", (1, "00ff00")),
            ("set_gate_spool", (1, 7)),
        ],
    )
    def test_partial_edit_keeps_the_gate_temp(
        self, manager, qtbot, method, args
    ) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            getattr(manager, method)(*args)
        assert " TEMP=0 " in blocker.args[0]

    def test_set_gate_spool(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_spool(0, 7)
        assert blocker.args == ["MMU_GATE_MAP GATE=0 SPOOLID=7 TEMP=0 QUIET=1"]

    # GATE=-1 fails Happy-Hare's minval=0.
    @pytest.mark.parametrize(
        ("method", "args"),
        [
            ("set_gate_info", (-1, "PLA", "ff0000", 42)),
            ("clear_gate", (-1,)),
            ("set_gate_material", (-1, "PETG")),
            ("set_gate_temp", (-1, 240)),
            ("set_gate_color", (-1, "00ff00")),
            ("set_gate_spool", (-1, 7)),
        ],
    )
    def test_unselected_gate_emits_no_gcode(self, manager, qtbot, method, args) -> None:
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            getattr(manager, method)(*args)

    # Without state the loaded guard cannot run, and bare MMU_HOME means TOOL=0.
    def test_home_mmu_without_state_sends_nothing(self, manager, qtbot) -> None:
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            manager.home_mmu()

    def test_home_mmu_without_a_tool_is_bare(self, manager, qtbot) -> None:
        manager.update_mmu_state(_status(tool=-1, filament_pos=0))
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.home_mmu()
        assert blocker.args == ["MMU_HOME"]

    # Bare MMU_HOME defaults to TOOL=0 (mmu.py:6706).
    def test_home_mmu_keeps_the_selected_tool(self, manager, qtbot) -> None:
        manager.update_mmu_state(_status(tool=1, filament_pos=0))
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.home_mmu()
        assert blocker.args == ["MMU_HOME TOOL=1"]

    # home() has no check_if_loaded (mmu.py:6394), unlike MMU_SELECT.
    @pytest.mark.parametrize("filament_pos", [3, 10])
    def test_home_mmu_refused_while_loaded(self, manager, qtbot, filament_pos) -> None:
        manager.update_mmu_state(_status(tool=1, filament_pos=filament_pos))
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            manager.home_mmu()

    # MMU_HOME is the post-restart recovery, exactly when filament_pos is UNKNOWN.
    def test_home_mmu_allowed_when_position_unknown(self, manager, qtbot) -> None:
        manager.update_mmu_state(_status(tool=1, filament_pos=-1))
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.home_mmu()
        assert blocker.args == ["MMU_HOME TOOL=1"]

    # Happy-Hare ignores a bare MMU_RESET (mmu.py:4197).
    def test_reset_mmu(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.reset_mmu()
        assert blocker.args == ["MMU_RESET CONFIRM=1"]

    def test_load_gate(self, manager, qtbot) -> None:
        manager.update_mmu_state(_status(filament_pos=0))
        assert manager.load_refusal() == ""
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            assert manager.load_gate() is True
        assert blocker.args == ["MMU_LOAD"]

    # Happy-Hare drops MMU_LOAD when disabled or unhomed (mmu.py:6936).
    @pytest.mark.parametrize(
        "overrides",
        [
            None,
            {"filament_pos": 10},
            {"filament_pos": 0, "gate": -1},
            {"filament_pos": 0, "enabled": False},
            {"filament_pos": 0, "is_homed": False},
            {"filament_pos": 0, "action": "Checking"},
        ],
    )
    def test_load_gate_refused(self, manager, qtbot, overrides) -> None:
        if overrides is not None:
            manager.update_mmu_state(_status(**overrides))
        assert manager.load_refusal()
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            assert manager.load_gate() is False

    @pytest.mark.parametrize(
        ("eject", "gcode"), [(False, "MMU_UNLOAD"), (True, "MMU_EJECT")]
    )
    def test_unload(self, manager, qtbot, eject, gcode) -> None:
        manager.update_mmu_state(_FULL_STATUS_WITH_SPOOLMAN)
        assert manager.unload_refusal() == ""
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            assert manager.unload(eject=eject) is True
        assert blocker.args == [gcode]

    # Happy-Hare drops MMU_UNLOAD when disabled or already unloaded (mmu.py:6981).
    @pytest.mark.parametrize(
        "overrides",
        [
            None,
            {"filament_pos": 0},
            {"enabled": False},
            {"action": "Loading"},
        ],
    )
    def test_unload_refused(self, manager, qtbot, overrides) -> None:
        if overrides is not None:
            manager.update_mmu_state(_status(**overrides))
        assert manager.unload_refusal()
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            assert manager.unload(eject=True) is False

    # A paused print is where a failed swap gets recovered by hand.
    @pytest.mark.parametrize("print_state", ["paused", "pause_locked"])
    def test_unload_allowed_while_paused(self, manager, qtbot, print_state) -> None:
        manager.update_mmu_state(_status(print_state=print_state))
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            assert manager.unload() is True
        assert blocker.args == ["MMU_UNLOAD"]

    # "Unknown" is the action Happy-Hare reports after an error, not a running action.
    def test_unload_allowed_after_an_action_error(self, manager, qtbot) -> None:
        manager.update_mmu_state(_status(action="Unknown"))
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            assert manager.unload() is True
        assert blocker.args == ["MMU_UNLOAD"]

    def test_eject_gate(self, manager, qtbot) -> None:
        manager.update_mmu_state(_status(filament_pos=0))
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.eject_gate()
        assert blocker.args == ["MMU_EJECT"]

    # MMU_EJECT only ejects the selected gate, and only when UNLOADED (mmu.py:7000).
    @pytest.mark.parametrize(
        "overrides",
        [
            None,
            {"filament_pos": 10},
            {"filament_pos": 0, "gate": -1},
            {"filament_pos": 0, "gate_status": [0, 1]},
            {"filament_pos": 0, "action": "Homing"},
        ],
    )
    def test_eject_gate_refused(self, manager, qtbot, overrides) -> None:
        if overrides is not None:
            manager.update_mmu_state(_status(**overrides))
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            manager.eject_gate()

    def test_check_gate_allows_an_empty_gate(self, manager, qtbot) -> None:
        manager.update_mmu_state(_status(filament_pos=0, gate_status=[0, 1]))
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.check_gate()
        assert blocker.args == ["MMU_CHECK_GATE"]

    # HH v3 unloads first, then reloads a LOADED tool after the check (mmu.py:8897).
    @pytest.mark.parametrize("filament_pos", [10, 3, -1])
    def test_check_gate_allowed_from_any_position(
        self, manager, qtbot, filament_pos
    ) -> None:
        manager.update_mmu_state(_status(filament_pos=filament_pos))
        assert manager.check_refusal() == ""
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.check_gate()
        assert blocker.args == ["MMU_CHECK_GATE"]

    @pytest.mark.parametrize(
        "overrides",
        [
            None,
            {"gate": -2},
            {"enabled": False},
            {"is_homed": False},
            {"action": "Checking"},
        ],
    )
    def test_check_gate_refused(self, manager, qtbot, overrides) -> None:
        if overrides is not None:
            manager.update_mmu_state(_status(**overrides))
        assert manager.check_refusal()
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            manager.check_gate()

    def test_select_gate(self, manager, qtbot) -> None:
        manager.update_mmu_state(_status(filament_pos=0))
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.select_gate(1)
        assert blocker.args == ["MMU_SELECT GATE=1"]

    # Happy-Hare refuses MMU_SELECT while loaded (mmu.py:6722).
    @pytest.mark.parametrize(
        ("overrides", "gate"),
        [
            (None, 1),
            ({"filament_pos": 0}, 0),
            ({"filament_pos": 0}, 2),
            ({"filament_pos": 0}, -1),
            ({"filament_pos": 10}, 1),
            ({"filament_pos": 0, "enabled": False}, 1),
            ({"filament_pos": 0, "is_homed": False}, 1),
            ({"filament_pos": 0, "action": "Selecting"}, 1),
        ],
    )
    def test_select_gate_skipped(self, manager, qtbot, overrides, gate) -> None:
        if overrides is not None:
            manager.update_mmu_state(_status(**overrides))
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            manager.select_gate(gate)

    # HH v3 parks and restores the toolhead around these; only MMU_PRELOAD checks
    # for a print (mmu.py:9040), so the manager must not block them mid-print.
    @pytest.mark.parametrize("print_state", ["printing", "started"])
    @pytest.mark.parametrize(
        ("filament_pos", "send", "gcode"),
        [
            (0, lambda m: m.load_gate(), "MMU_LOAD"),
            (10, lambda m: m.unload(), "MMU_UNLOAD"),
            (10, lambda m: m.check_gate(), "MMU_CHECK_GATE"),
            (0, lambda m: m.select_gate(1), "MMU_SELECT GATE=1"),
        ],
    )
    def test_allowed_while_printing(
        self, manager, qtbot, print_state, filament_pos, send, gcode
    ) -> None:
        manager.update_mmu_state(
            _status(filament_pos=filament_pos, print_state=print_state)
        )
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            send(manager)
        assert blocker.args == [gcode]

    @pytest.mark.parametrize("print_state", ["printing", "started"])
    def test_eject_refused_while_printing(self, manager, qtbot, print_state) -> None:
        manager.update_mmu_state(_status(filament_pos=0, print_state=print_state))
        with qtbot.assertNotEmitted(manager.run_gcode_signal):
            manager.eject_gate()

    # TOOL, not GATE: the ttg map may not map tool N to gate N.
    def test_change_tool(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.change_tool(1)
        assert blocker.args == ["MMU_CHANGE_TOOL TOOL=1"]

    def test_klippy_disconnected_to_connected(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        manager.on_klippy_state("disconnect")
        assert manager.get_state() is None
        manager.on_klippy_state("ready")
        manager.update_mmu_state(_FULL_STATUS)
        assert manager.get_state() is not None

    # FIRMWARE_RESTART drops the state; the panels must be told.
    def test_klippy_disconnect_emits_none_state(self, manager, qtbot) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        with qtbot.waitSignal(manager.mmu_state_changed) as blocker:
            manager.on_klippy_state("disconnect")
        assert blocker.args == [None]

    def test_repeated_disconnect_emits_once(self, manager, qtbot) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        manager.on_klippy_state("disconnect")
        with qtbot.assertNotEmitted(manager.mmu_state_changed):
            manager.on_klippy_state("shutdown")
            manager.on_klippy_state("disconnect")

    def test_klippy_ready_emits_nothing(self, manager, qtbot) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        with qtbot.assertNotEmitted(manager.mmu_state_changed):
            manager.on_klippy_state("ready")

    # The gcode form drops the socket mid-reply and reports a false 503.
    def test_activate_calls_the_firmware_restart_rpc(
        self, manager_with_cfg, qtbot
    ) -> None:
        mgr, _ = manager_with_cfg
        with qtbot.assertNotEmitted(mgr.run_gcode_signal):
            mgr.toggle_amu_system(True)
        mgr._ws.api.firmware_restart.assert_called_once_with()


class TestPregateSensors:
    def test_pre_gate_happy_path(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        data: dict[str, bool] = {"filament_detected": True}
        manager.on_pre_gate_update(data, "mmu_pre_gate_0")
        manager.on_pre_gate_update(data, "mmu_pre_gate_1")
        manager.on_pre_gate_update(data, "mmu_pre_gate_2")
        manager.on_pre_gate_update(data, "mmu_pre_gate_3")
        assert manager.get_pre_gate_sensors() == {0: True, 1: True, 2: True, 3: True}

    def test_pre_gate_emits_signal(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.pre_gate_changed) as blocker:
            manager.on_pre_gate_update({"filament_detected": True}, "mmu_pre_gate_0")
        assert blocker.args == [0, True]

    # Moonraker sends only changed keys; a missing reading is not an empty gate.
    @pytest.mark.parametrize("data", [{}, {"enabled": False}, {"enabled": True}])
    def test_enabled_only_diff_is_ignored(self, manager, qtbot, data) -> None:
        with qtbot.assertNotEmitted(manager.pre_gate_changed):
            manager.on_pre_gate_update(data, "mmu_pre_gate_0")
        assert manager.get_pre_gate_sensors() == {}

    def test_enabled_only_diff_keeps_the_last_reading(self, manager) -> None:
        manager.on_pre_gate_update({"filament_detected": True}, "mmu_pre_gate_0")
        manager.on_pre_gate_update({"enabled": False}, "mmu_pre_gate_0")
        assert manager.get_pre_gate_sensors() == {0: True}

    def test_non_mmu_sensor_ignored(self, manager, qtbot) -> None:
        with qtbot.assertNotEmitted(manager.pre_gate_changed):
            manager.on_pre_gate_update({"filament_detected": True}, "Toolhead Sensor")

    # int() on a bad suffix would raise into Qt.
    @pytest.mark.parametrize("name", ["mmu_pre_gate_", "mmu_pre_gate_left"])
    def test_unparsable_gate_index_ignored(self, manager, qtbot, name) -> None:
        with qtbot.assertNotEmitted(manager.pre_gate_changed):
            manager.on_pre_gate_update({"filament_detected": True}, name)
        assert manager.get_pre_gate_sensors() == {}

    def test_pre_gate_filament_not_detected(self, manager) -> None:
        manager.on_pre_gate_update({"filament_detected": True}, "mmu_pre_gate_0")
        manager.on_pre_gate_update({"filament_detected": False}, "mmu_pre_gate_1")
        manager.on_pre_gate_update({"filament_detected": True}, "mmu_pre_gate_2")
        manager.on_pre_gate_update({"filament_detected": False}, "mmu_pre_gate_3")
        assert manager.get_pre_gate_sensors() == {0: True, 1: False, 2: True, 3: False}

    def test_pre_gate_emits_each_reading(self, manager) -> None:
        seen = []
        manager.pre_gate_changed.connect(lambda *args: seen.append(args))
        for gate, detected in enumerate([False, True, False, True]):
            manager.on_pre_gate_update(
                {"filament_detected": detected}, f"mmu_pre_gate_{gate}"
            )
        assert seen == [(0, False), (1, True), (2, False), (3, True)]

    def test_klippy_disconnect_clears_pre_gate_sensors(self, manager) -> None:
        manager.on_pre_gate_update({"filament_detected": True}, "mmu_pre_gate_0")
        manager.on_klippy_state("disconnect")
        assert manager.get_pre_gate_sensors() == {}


class TestIsAMUActive:
    def test_false_when_configured_but_no_mmu_state(
        self, manager_with_cfg, qtbot
    ) -> None:
        mgr, _ = manager_with_cfg
        with qtbot.waitSignal(mgr.amu_toggled):
            mgr.toggle_amu_system(True)
        assert mgr.is_amu_active() is False

    def test_true_when_configured_and_mmu_state(self, manager_with_cfg, qtbot) -> None:
        mgr, _ = manager_with_cfg
        with qtbot.waitSignal(mgr.amu_toggled):
            mgr.toggle_amu_system(True)
        mgr.update_mmu_state(_FULL_STATUS)
        assert mgr.is_amu_active() is True

    # MMU ENABLE=0 rejects every MMU_* command (mmu.py:3584).
    def test_false_when_mmu_disabled(self, manager_with_cfg, qtbot) -> None:
        mgr, _ = manager_with_cfg
        with qtbot.waitSignal(mgr.amu_toggled):
            mgr.toggle_amu_system(True)
        mgr.update_mmu_state(_status(enabled=False))
        assert mgr.is_amu_active() is False


class TestObjectRouting:
    """on_object_updated is the only entry point Printer calls; each branch matters."""

    def test_mmu_type_updates_state(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.mmu_state_changed):
            manager.on_object_updated("mmu", "mmu", _FULL_STATUS)
        assert manager.get_state().num_gates == 2

    def test_filament_switch_sensor_routes_to_pre_gate(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.pre_gate_changed) as blocker:
            manager.on_object_updated(
                "filament_switch_sensor",
                "mmu_pre_gate_1",
                {"filament_detected": True},
            )
        assert blocker.args == [1, True]
        assert manager.get_pre_gate_sensors() == {1: True}

    # The object name, not the type, carries the gate index.
    def test_non_pre_gate_switch_sensor_ignored(self, manager, qtbot) -> None:
        with qtbot.assertNotEmitted(manager.pre_gate_changed):
            manager.on_object_updated(
                "filament_switch_sensor", "toolhead_sensor", {"filament_detected": True}
            )


class TestLoadCellUpdate:
    # RF50-Klipper has no [load_cell]; the old handler also read the wrong key.
    def test_load_cell_updates_are_ignored(self, manager, qtbot) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        with qtbot.assertNotEmitted(manager.mmu_state_changed):
            manager.on_object_updated(
                "load_cell", "load_cell_mmu_0", {"force_g": 150.0}
            )


class TestGcodeQuoting:
    # User-typed Spoolman text must survive Klipper's shlex parse as one value.
    @pytest.mark.parametrize(
        ("name", "color"),
        [
            ("PLA Basic", "ff0000"),
            ("Bob's PLA", "#ff0000"),
            ('He said "hi"', ""),
            ("PLA", "ff0000"),
            ("a;b#c", "0"),
            ("multi\nline", "ff0000"),
        ],
    )
    def test_emitted_gcode_survives_klipper_parser(
        self, manager, qtbot, name, color
    ) -> None:
        manager.update_mmu_state(_FULL_STATUS_WITH_SPOOLMAN)
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_info(0, "PLA", color, 42, filament_name=name)
        gcode = blocker.args[0]
        assert "\n" not in gcode
        params = _klipper_parse(gcode.removeprefix("MMU_GATE_MAP "))
        assert params["NAME"] == " ".join(name.split())
        assert params["COLOR"] == color.lstrip("#")
        assert params["SPOOLID"] == "42"

    # Klipper's save_variables configparser shuts Klippy down on a '%'.
    @pytest.mark.parametrize("name", ["50%", "%(x)s"])
    def test_percent_is_stripped(self, manager, qtbot, name) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_info(0, "PLA", "ff0000", 42, filament_name=name)
        assert "%" not in blocker.args[0]


class TestAssignSpool:
    @staticmethod
    def _gcode(manager, gate, spool) -> list[str]:
        manager.update_mmu_state(_FULL_STATUS_WITH_SPOOLMAN)
        signals = []
        manager.run_gcode_signal.connect(signals.append)
        manager.assign_spool(gate, spool)
        return signals

    def test_maps_gate_from_payload(self, manager) -> None:
        assert self._gcode(manager, 1, _SPOOL_DATA) == [
            "MMU_GATE_MAP GATE=1 NAME='PLA Basic' MATERIAL=PLA COLOR=ff0000 "
            "SPOOLID=42 TEMP=215 QUIET=1"
        ]

    # Spoolman sends null for an unset extruder temp.
    def test_null_temp_lets_happy_hare_default_it(self, manager) -> None:
        filament = {**_SPOOL_DATA["filament"], "settings_extruder_temp": None}
        (gcode,) = self._gcode(manager, 1, {**_SPOOL_DATA, "filament": filament})
        assert "TEMP" not in gcode

    def test_unselected_gate_emits_nothing(self, manager) -> None:
        assert self._gcode(manager, -1, _SPOOL_DATA) == []


class TestStaleMMUJob:
    @staticmethod
    def _run(manager, qtbot, *events: tuple[str, str]) -> list[str]:
        manager._stale_job_timer.setInterval(10)
        manager.update_mmu_state(_FULL_STATUS_WITH_SPOOLMAN)
        signals: list[str] = []
        manager.run_gcode_signal.connect(signals.append)
        for obj, state in events:
            if obj == "mmu":
                manager.update_mmu_state({"print_state": state})
            else:
                manager.on_object_updated(
                    "print_stats", "print_stats", {"state": state}
                )
        qtbot.wait(50)
        return signals

    # .151 2026-10-21 11:10:20: PRINT_START raised, then HH's deferred auto-start re-opened the job.
    def test_job_reopened_after_cancel_is_ended(self, manager, qtbot) -> None:
        events = [
            ("print_stats", "printing"),
            ("mmu", "printing"),
            ("mmu", "cancelled"),
            ("print_stats", "cancelled"),
            ("mmu", "printing"),
        ]
        assert self._run(manager, qtbot, *events) == ["MMU_PRINT_END STATE=cancelled"]

    def test_standby_with_open_job_is_ended(self, manager, qtbot) -> None:
        events = [("print_stats", "standby"), ("mmu", "started")]
        assert self._run(manager, qtbot, *events) == ["MMU_PRINT_END STATE=standby"]

    @pytest.mark.parametrize("ps_state", ["printing", "paused", "complete", "error"])
    def test_other_print_stats_states_are_left_to_hh(
        self, manager, qtbot, ps_state
    ) -> None:
        events = [("print_stats", ps_state), ("mmu", "printing")]
        assert self._run(manager, qtbot, *events) == []

    def test_normal_cancel_emits_nothing(self, manager, qtbot) -> None:
        events = [
            ("mmu", "printing"),
            ("print_stats", "cancelled"),
            ("mmu", "cancelled"),
        ]
        assert self._run(manager, qtbot, *events) == []

    # A print start reports print_stats=printing after HH's started diff.
    def test_states_agreeing_within_grace_disarms(self, manager, qtbot) -> None:
        events = [
            ("print_stats", "standby"),
            ("mmu", "started"),
            ("print_stats", "printing"),
        ]
        assert self._run(manager, qtbot, *events) == []


class TestPrintStartRefusal:
    def test_no_state_allows(self, manager) -> None:
        assert manager.print_start_refusal() == ""

    @pytest.mark.parametrize(
        "sensors",
        [
            {},
            {"toolhead": True, "mmu_pre_gate": True},
            {"toolhead": None, "mmu_pre_gate": None},
        ],
    )
    def test_loaded_missing_or_disabled_allows(self, manager, sensors) -> None:
        manager.update_mmu_state(_status(sensors=sensors))
        assert manager.print_start_refusal() == ""

    # .151 2026-10-21 11:10:20: toolhead False with both pre-gates True raised PRINT_START.
    def test_toolhead_empty_refuses(self, manager) -> None:
        manager.update_mmu_state(
            _status(sensors={"toolhead": False, "mmu_pre_gate": True})
        )
        assert "toolhead" in manager.print_start_refusal()

    def test_pre_gate_empty_refuses(self, manager) -> None:
        manager.update_mmu_state(
            _status(sensors={"toolhead": None, "mmu_pre_gate": False})
        )
        assert "gate" in manager.print_start_refusal()

    def test_klippy_disconnect_drops_refusal(self, manager) -> None:
        manager.update_mmu_state(_status(sensors={"toolhead": False}))
        manager.on_klippy_state("shutdown")
        assert manager.print_start_refusal() == ""
