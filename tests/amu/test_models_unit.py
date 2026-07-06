"""Unit tests for BlocksScreen.devices.amu.models."""

from BlocksScreen.devices.amu.models import (
    FilamentPos,
    GateInfo,
    GateStatus,
    MMUState,
    SpoolmanSupport,
)


class TestGateStatus:
    def test_values(self) -> None:
        assert GateStatus.UNKNOWN == 0
        assert GateStatus.AVAILABLE == 1
        assert GateStatus.AVAILABLE_FROM_BUFFER == 2
        assert GateStatus.EMPTY == -1

    def test_is_int_enum(self) -> None:
        assert isinstance(GateStatus.AVAILABLE, int)


class TestFilamentPos:
    def test_values(self) -> None:
        assert FilamentPos.UNKNOWN == -1
        assert FilamentPos.UNLOADED == 0
        assert FilamentPos.LOADED == 10

    def test_is_int_enum(self) -> None:
        assert isinstance(FilamentPos.LOADED, int)

    def test_roundtrip_from_int(self) -> None:
        assert FilamentPos(10) is FilamentPos.LOADED
        assert FilamentPos(-1) is FilamentPos.UNKNOWN


class TestSpoolmanSupport:
    def test_values(self) -> None:
        assert SpoolmanSupport.OFF == "off"
        assert SpoolmanSupport.READONLY == "readonly"
        assert SpoolmanSupport.PUSH == "push"
        assert SpoolmanSupport.PULL == "pull"

    def test_is_str(self) -> None:
        assert isinstance(SpoolmanSupport.PUSH, str)

    def test_roundtrip_from_str(self) -> None:
        assert SpoolmanSupport("pull") is SpoolmanSupport.PULL


class TestGateInfo:
    def _make(self, status: GateStatus) -> GateInfo:
        return GateInfo(
            index=0,
            status=status,
            material="PLA",
            color="ff0000",
            color_rgb=(1.0, 0.0, 0.0),
            spool_id=1,
        )

    def test_is_available_true_for_available(self) -> None:
        assert self._make(GateStatus.AVAILABLE).is_available is True

    def test_is_available_true_for_buffer(self) -> None:
        assert self._make(GateStatus.AVAILABLE_FROM_BUFFER).is_available is True

    def test_is_available_false_for_empty(self) -> None:
        assert self._make(GateStatus.EMPTY).is_available is False

    def test_is_available_false_for_unknown(self) -> None:
        assert self._make(GateStatus.UNKNOWN).is_available is False

    def test_gate_info_default_weight_is_gone(self) -> None:
        gate = self._make(GateStatus.AVAILABLE)
        assert gate.weight_g is None

    def test_gate_info_default_mid_usage_is_false(self) -> None:
        gate = self._make(GateStatus.AVAILABLE)
        assert gate.mid_usage is False

    def test_gate_info_weight_and_mid_usage_set(self) -> None:
        gate = GateInfo(
            index=0,
            status=GateStatus.AVAILABLE,
            material="PLA",
            color="ff0000",
            color_rgb=(1.0, 0.0, 0.0),
            spool_id=1,
            weight_g=245.5,
            mid_usage=True,
        )
        assert gate.weight_g == 245.5
        assert gate.mid_usage is True

    def test_gate_info_default_filament_name(self) -> None:
        assert self._make(GateStatus.AVAILABLE).filament_name == ""

    def test_gate_info_default_temperature_is_none(self) -> None:
        assert self._make(GateStatus.AVAILABLE).temperature is None


class TestMMUState:
    def _full_status(self, num_gates=2) -> dict:
        return {
            "enabled": True,
            "is_homed": True,
            "num_gates": num_gates,
            "tool": 0,
            "gate": 0,
            "filament": "Loaded",
            "filament_pos": 10,
            "action": "Idle",
            "print_state": "printing",
            "reason_for_pause": "",
            "has_bypass": False,
            "spoolman_support": "push",
            "gate_status": [1, -1],
            "gate_material": ["PLA", ""],
            "gate_color": ["ff0000", ""],
            "gate_color_rgb": [(1.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
            "gate_spool_id": [42, -1],
            "ttg_map": [0, 1],
        }

    def _full_status_extended(self, num_gates: int = 2) -> dict:
        """Full status including all new HH fields."""
        return {
            **self._full_status(num_gates),
            "gate_filament_name": ["Bambu PLA Basic", ""],
            "gate_temperature": [215.0, 0.0],
            "pending_spool_id": 7,
            "operation": "loading",
            "sensors": {
                "pre_gate_0": True,
                "gate": False,
            },
        }

    def test_from_status_builds_correctly(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        assert state.num_gates == 2
        assert state.enabled
        assert len(state.gates) == 2
        assert state.gates[0].material == "PLA"
        assert state.gates[1].status == GateStatus.EMPTY
        assert state.ttg_map == (0, 1)

    def test_from_status_empty_dict_uses_default(self) -> None:
        state: MMUState = MMUState.from_status({})
        assert state.num_gates == 0
        assert state.enabled is False
        assert state.gates == ()
        assert state.filament_pos is FilamentPos.UNKNOWN
        assert state.has_bypass is False
        assert state.spoolman_support is SpoolmanSupport.OFF

    def test_is_paused_true(self) -> None:
        state: MMUState = MMUState.from_status(
            {**self._full_status(), "print_state": "pause"}
        )
        assert state.is_paused is True

    def test_is_paused_false(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        assert state.is_paused is False

    def test_current_gate_info(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        assert state.current_gate_info is state.gates[0]

    def test_currrent_gate_info_none_when_no_gate(self) -> None:
        state: MMUState = MMUState.from_status({**self._full_status(), "gate": -1})
        assert state.current_gate_info is None

    def test_gate_for_tool(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        assert state.gate_for_tool(0) == 0
        assert state.gate_for_tool(1) == 1

    def test_gate_for_tool_out_of_range(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        assert state.gate_for_tool(99) == -1

    def test_apply_diff_scalar(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        updated: MMUState = state.apply_diff({"tool": 1, "filament": "Unloaded"})
        assert updated.tool == 1
        assert updated.filament == "Unloaded"
        assert updated.gates == state.gates

    def test_from_status_new_fields(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        assert state.filament_pos is FilamentPos.LOADED
        assert state.has_bypass is False
        assert state.spoolman_support is SpoolmanSupport.PUSH

    def test_from_status_has_bypass_true(self) -> None:
        state: MMUState = MMUState.from_status(
            {**self._full_status(), "has_bypass": True}
        )
        assert state.has_bypass is True

    def test_apply_diff_filament_pos_coerced(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        updated: MMUState = state.apply_diff({"filament_pos": 0})
        assert updated.filament_pos is FilamentPos.UNLOADED
        assert isinstance(updated.filament_pos, FilamentPos)

    def test_apply_diff_spoolman_support_coerced(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        updated: MMUState = state.apply_diff({"spoolman_support": "pull"})
        assert updated.spoolman_support is SpoolmanSupport.PULL
        assert isinstance(updated.spoolman_support, SpoolmanSupport)

    def test_apply_diff_gate_keys(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        updated: MMUState = state.apply_diff({"gate_status": [1, 1]})
        assert updated.gates[1].status == GateStatus.AVAILABLE

    def test_from_status_parse_gate_filament_name(self) -> None:
        state = MMUState.from_status(self._full_status_extended())
        assert state.gates[0].filament_name == "Bambu PLA Basic"
        assert state.gates[1].filament_name == ""

    def test_from_status_parse_gate_temperature(self) -> None:
        state = MMUState.from_status(self._full_status_extended())
        assert state.gates[0].temperature == 215.0

    def test_from_status_parses_pending_spool_id(self) -> None:
        state = MMUState.from_status(self._full_status_extended())
        assert state.pending_spool_id == 7

    def test_from_status_parses_operation(self) -> None:
        state = MMUState.from_status(self._full_status_extended())
        assert state.operation == "loading"

    def test_from_status_parse_sensors(self) -> None:
        state = MMUState.from_status(self._full_status_extended())
        assert state.sensors == {"pre_gate_0": True, "gate": False}

    def test_from_status_new_field_defaults(self) -> None:
        state = MMUState.from_status(self._full_status())
        assert state.pending_spool_id == -1
        assert state.operation == ""
        assert state.sensors == {}

    def test_apply_diff_updates_gate_filament_name(self) -> None:
        state = MMUState.from_status(self._full_status_extended())
        updated = state.apply_diff({"gate_filament_name": ["Updated PLA", ""]})
        assert updated.gates[0].filament_name == "Updated PLA"

    def test_apply_diff_replaces_sensors(self) -> None:
        state = MMUState.from_status(self._full_status_extended())

        updated = state.apply_diff({"sensors": {"pre_gate_0": False}})
        assert updated.sensors == {"pre_gate_0": False}
