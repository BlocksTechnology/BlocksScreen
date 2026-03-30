"""Unit tests for BlocksScreen.devices.amu.manager."""

from unittest.mock import MagicMock, patch

import pytest

from BlocksScreen.devices.amu.manager import AMUManager
from BlocksScreen.devices.amu.models import MMUState
from tests.amu.conftest import (
    COMMENTED_CFG as _COMMENTED_CFG,
)
from tests.amu.conftest import (
    UNCOMMENTED_CFG as _UNCOMMENTED_CFG,
)

_FULL_STATUS: dict = {
    "enabled": True,
    "is_homed": True,
    "num_gates": 2,
    "tool": 0,
    "gate": 0,
    "filament": "Loaded",
    "action": "Idle",
    "print_state": "printing",
    "reason_for_pause": "",
    "gate_status": [1, -1],
    "gate_material": ["PLA", ""],
    "gate_color": ["ff0000", ""],
    "gate_color_rgb": [(1.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
    "gate_spool_id": [42, -1],
    "ttg_map": [0, 1],
}

_FULL_STATUS_WITH_SPOOLMAN: dict = {
    **_FULL_STATUS,
    "filament_pos": 10,
    "has_bypass": False,
    "spoolman_support": "push",
}


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


class TestToggleAMUSystem:
    def test_no_config_emits_false(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.amu_toggled) as blocker:
            manager.toggle_amu_system(True)
        assert blocker.args == [False]

    def test_same_state_emits_false(self, manager_with_cfg, qtbot) -> None:
        mgr, _ = manager_with_cfg
        with qtbot.waitSignal(mgr.amu_toggled) as blocker:
            mgr.toggle_amu_system(False)
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
        mgr._config_toggler._state = True
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
    def test_first_call_emits_state(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.mmu_state_changed) as blocker:
            manager.update_mmu_state(_FULL_STATUS)
        assert isinstance(blocker.args[0], MMUState)

    def test_first_call_stores_state(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        state = manager.get_state()
        assert state is not None
        assert state.num_gates == 2
        assert state.enabled is True

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

    def test_each_call_emits_signal(self, manager, qtbot) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        with qtbot.waitSignal(manager.mmu_state_changed):
            manager.update_mmu_state({"tool": 1})


class TestGcodeSignals:
    def test_set_gate_info(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_info(0, "PLA", "ff0000", 42)
        assert blocker.args == [
            "MMU_GATE_MAP gate=0 MATERIAL=PLA COLOR=ff0000 SPOOLID=42"
        ]

    def test_set_gate_material(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_material(1, "PETG")
        assert blocker.args == ["MMU_GATE_MAP gate=1 MATERIAL=PETG"]

    def test_set_gate_color(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_color(2, "00ff00")
        assert blocker.args == ["MMU_GATE_MAP gate=2 COLOR=00ff00"]

    def test_set_gate_spool(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.set_gate_spool(0, 7)
        assert blocker.args == ["MMU_GATE_MAP gate=0 SPOOLID=7"]

    def test_home_mmu(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.home_mmu()
        assert blocker.args == ["MMU_HOME"]

    def test_reset_mmu(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.reset_mmu()
        assert blocker.args == ["MMU_RESET"]

    def test_load_gate(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.load_gate(3)
        assert blocker.args == ["MMU_SELECT gate=3\nMMU_LOAD"]

    def test_unload(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.unload()
        assert blocker.args == ["MMU_UNLOAD"]

    def test_eject_gate(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.eject_gate(1)
        assert blocker.args == ["MMU_EJECT GATE=1"]

    def test_eject_all_gates(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.eject_all_gates(3)
        assert blocker.args == ["MMU_EJECT GATE=0\nMMU_EJECT GATE=1\nMMU_EJECT GATE=2"]

    def test_select_tool(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.run_gcode_signal) as blocker:
            manager.select_tool(2)
        assert blocker.args == ["MMU_CHANGE_TOOL TOOL=2"]

    def test_klippy_disconnect(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        manager.on_klippy_state("disconnect")
        assert manager.get_state() is None

    def test_klippy_ready(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        manager.on_klippy_state("ready")
        assert manager.get_state() is not None

    def test_klippy_disconnected_to_connected(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        manager.on_klippy_state("disconnect")
        assert manager.get_state() is None
        manager.on_klippy_state("ready")
        manager.update_mmu_state(_FULL_STATUS)
        assert manager.get_state() is not None

    def test_acivate_emits_firmware_restart(self, manager_with_cfg, qtbot) -> None:
        mgr, _ = manager_with_cfg
        with qtbot.waitSignal(mgr.run_gcode_signal) as blocker:
            mgr.toggle_amu_system(True)
        assert blocker.args == ["FIRMWARE_RESTART"]


class TestPregateSensors:
    def test_pre_gate_happy_path(self, manager) -> None:
        manager.update_mmu_state(_FULL_STATUS)
        data: dict[str, bool] = {"filament_detected": True}
        manager.on_pre_gate_update(data, "Mmu Pre Gate 0")
        manager.on_pre_gate_update(data, "Mmu Pre Gate 1")
        manager.on_pre_gate_update(data, "Mmu Pre Gate 2")
        manager.on_pre_gate_update(data, "Mmu Pre Gate 3")
        assert manager.get_pre_gate_sensors() == {0: True, 1: True, 2: True, 3: True}

    def test_pre_gate_emits_signal(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.pre_gate_changed) as blocker:
            manager.on_pre_gate_update({"filament_detected": True}, "Mmu Pre Gate 0")
        assert blocker.args == [0, True]

    def test_non_mmu_sensor_ignored(self, manager, qtbot) -> None:
        with qtbot.assertNotEmitted(manager.pre_gate_changed):
            manager.on_pre_gate_update({"filament_detected": True}, "Toolhead Sensor")

    def test_pre_gate_stores_state(self, manager) -> None:
        manager.on_pre_gate_update({"filament_detected": True}, "Mmu Pre Gate 2")
        assert manager.get_pre_gate_sensors() == {2: True}

    def test_pre_gate_filament_not_detected(self, manager) -> None:
        manager.on_pre_gate_update({"filament_detected": True}, "Mmu Pre Gate 0")
        manager.on_pre_gate_update({"filament_detected": False}, "Mmu Pre Gate 1")
        manager.on_pre_gate_update({"filament_detected": True}, "Mmu Pre Gate 2")
        manager.on_pre_gate_update({"filament_detected": False}, "Mmu Pre Gate 3")
        assert manager.get_pre_gate_sensors() == {0: True, 1: False, 2: True, 3: False}

    def test_pre_gate_empty(self, manager) -> None:
        assert manager.get_pre_gate_sensors() == {}

    def test_pre_gate_multiple_emits(self, manager, qtbot) -> None:
        with qtbot.waitSignal(manager.pre_gate_changed) as blocker:
            manager.on_pre_gate_update({"filament_detected": False}, "Mmu Pre Gate 0")
        assert blocker.args == [0, False]
        with qtbot.waitSignal(manager.pre_gate_changed) as blocker:
            manager.on_pre_gate_update({"filament_detected": True}, "Mmu Pre Gate 1")
        assert blocker.args == [1, True]
        with qtbot.waitSignal(manager.pre_gate_changed) as blocker:
            manager.on_pre_gate_update({"filament_detected": False}, "Mmu Pre Gate 2")
        assert blocker.args == [2, False]
        with qtbot.waitSignal(manager.pre_gate_changed) as blocker:
            manager.on_pre_gate_update({"filament_detected": True}, "Mmu Pre Gate 3")
        assert blocker.args == [3, True]

    def test_pre_gate_update_is_dict(self, manager) -> None:
        assert isinstance(manager.get_pre_gate_sensors(), dict)

    def test_klippy_disconnect_clears_pre_gate_sensors(self, manager) -> None:
        manager.on_pre_gate_update({"filament_detected": True}, "Mmu Pre Gate 0")
        manager.on_klippy_state("disconnect")
        assert manager.get_pre_gate_sensors() == {}


class TestIsAMUActive:
    def test_false_when_not_configured(self, manager) -> None:
        assert manager.is_amu_active() is False

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


class TestSpoolManFetch:
    def test_noop_when_mmu_state_none(self, manager, qtbot) -> None:
        with qtbot.assertNotEmitted(manager.spool_fetched):
            manager.fetch_spool(0, 42)
        manager._ws.api.get_spool.assert_not_called()

    def test_noop_when_spoolman_off(self, manager, qtbot) -> None:
        status = {**_FULL_STATUS_WITH_SPOOLMAN, "spoolman_support": "off"}
        manager.update_mmu_state(status)
        with qtbot.assertNotEmitted(manager.spool_fetched):
            manager.fetch_spool(0, 42)
        manager._ws.api.get_spool.assert_not_called()

    def test_emit_spool_fetched_on_sucess(self, manager, qtbot) -> None:
        manager.update_mmu_state(_FULL_STATUS_WITH_SPOOLMAN)
        spool_data = {"id": 42, "filament": {"name": "PLA"}, "used_weight": 50.0}
        manager.fetch_spool(0, 42)
        callback = manager._ws.api.get_spool.call_args.args[1]
        with qtbot.waitSignal(manager.spool_fetched) as blocker:
            callback(spool_data)
        assert blocker.args[0] == 0
        assert blocker.args[1] == spool_data

    def test_no_emit_on_ws_failure(self, manager, qtbot) -> None:
        manager.update_mmu_state(_FULL_STATUS_WITH_SPOOLMAN)
        manager.fetch_spool(0, 42)
        callback = manager._ws.api.get_spool.call_args.args[1]
        with qtbot.assertNotEmitted(manager.spool_fetched):
            callback(None)
