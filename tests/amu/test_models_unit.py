"""Unit tests for BlocksScreen.devices.amu.models."""

import dataclasses

import pytest

from BlocksScreen.devices.amu.models import (
    FilamentPos,
    GateInfo,
    GateStatus,
    MMUState,
    SpoolInfo,
    SpoolmanSupport,
)


class TestGateStatus:
    def test_values(self) -> None:
        # Must match Happy-Hare's GATE_* codes (mmu.py:59-62).
        assert GateStatus.UNKNOWN == -1
        assert GateStatus.EMPTY == 0
        assert GateStatus.AVAILABLE == 1
        assert GateStatus.AVAILABLE_FROM_BUFFER == 2

    def test_unknown_value_does_not_raise(self) -> None:
        assert GateStatus(99) is GateStatus.UNKNOWN

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

    def test_gate_info_has_no_spoolman_local_fields(self) -> None:
        # Happy-Hare publishes no weight or bed_temp gate arrays.
        fields = {f.name for f in dataclasses.fields(GateInfo)}
        assert fields.isdisjoint({"weight_g", "remaining_weight", "bed_temp"})

    def test_gate_info_default_speed_override_is_100(self) -> None:
        assert self._make(GateStatus.AVAILABLE).speed_override == 100

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
            "gate_status": [1, 0],
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
            "gate_speed_override": [100, 80],
            "drying_state": ["active", ""],
            "pending_spool_id": 7,
            "operation": "loading",
            # Key names from a live RF50 (mmu_sensor_manager.py:100).
            "sensors": {
                "mmu_pre_gate": True,
                "mmu_gate": False,
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

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ([], (0.0, 0.0, 0.0)),
            ([0.5], (0.5, 0.0, 0.0)),
            ([0.1, 0.2, 0.3, 0.4], (0.1, 0.2, 0.3)),
        ],
    )
    def test_short_colour_array_pads_with_zeroes(self, raw, expected) -> None:
        status = {**self._full_status(), "gate_color_rgb": [raw, (0.0, 0.0, 0.0)]}
        assert MMUState.from_status(status).gates[0].color_rgb == expected

    def test_from_status_empty_dict_uses_default(self) -> None:
        state: MMUState = MMUState.from_status({})
        assert state.num_gates == 0
        assert state.enabled is False
        assert state.gates == ()
        assert state.filament_pos is FilamentPos.UNKNOWN
        assert state.has_bypass is False
        assert state.spoolman_support is SpoolmanSupport.OFF

    # The only values Happy-Hare's is_mmu_paused() accepts (mmu.py:3040).
    @pytest.mark.parametrize("print_state", ["paused", "pause_locked"])
    def test_is_paused_true(self, print_state: str) -> None:
        state: MMUState = MMUState.from_status(
            {**self._full_status(), "print_state": print_state}
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

    # Happy-Hare publishes 0-100 during a bowden move, else -1 (mmu.py:1433).
    def test_bowden_progress_defaults_to_idle(self) -> None:
        assert MMUState.from_status(self._full_status()).bowden_progress == -1

    def test_apply_diff_updates_bowden_progress(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status())
        assert state.apply_diff({"bowden_progress": 42}).bowden_progress == 42

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

    def test_gate_array_diff_preserves_untouched_arrays(self) -> None:
        """A diff carries only the arrays that changed; the rest must survive it."""
        state = MMUState.from_status(self._full_status_extended())
        updated = state.apply_diff({"gate_status": [2, 0]})
        assert updated.gates[0] == dataclasses.replace(
            state.gates[0], status=GateStatus.AVAILABLE_FROM_BUFFER
        )
        assert updated.gates[1] == state.gates[1]

    def test_gate_array_diff_leaves_spools_alone(self) -> None:
        """Spoolman data is keyed by spool id, so no gate array can invalidate it."""
        state = MMUState.from_status(self._full_status())
        spools = {42: SpoolInfo(spool_id=42, used_weight_g=50.0, bed_temp=60)}
        state = dataclasses.replace(state, spools=spools)
        assert state.apply_diff({"gate_status": [2, 0]}).spools == spools

    def test_from_status_parses_speed_override_per_gate(self) -> None:
        state = MMUState.from_status(self._full_status_extended())
        assert (state.gates[0].speed_override, state.gates[1].speed_override) == (
            100,
            80,
        )

    # drying_state is per-gate despite having no gate_ prefix.
    def test_from_status_parses_drying_state_per_gate(self) -> None:
        state = MMUState.from_status(self._full_status_extended())
        assert (state.gates[0].drying_state, state.gates[1].drying_state) == (
            "active",
            "",
        )

    def test_apply_diff_updates_drying_state(self) -> None:
        state = MMUState.from_status(self._full_status_extended())
        state = state.apply_diff({"drying_state": ["complete", "queued"]})
        assert [g.drying_state for g in state.gates] == ["complete", "queued"]
        assert state.gates[0].speed_override == 100

    def test_spool_for_gate(self) -> None:
        state = MMUState.from_status(self._full_status())
        spool = SpoolInfo(spool_id=42, used_weight_g=50.0)
        state = dataclasses.replace(state, spools={42: spool})
        assert state.spool_for_gate(0) is spool

    # gates[-1] wraps and gate 1 holds spool_id -1, so both must miss.
    @pytest.mark.parametrize("gate", [-1, 1, 99])
    def test_spool_for_gate_none(self, gate: int) -> None:
        state = MMUState.from_status(self._full_status())
        state = dataclasses.replace(
            state, spools={42: SpoolInfo(spool_id=42, used_weight_g=50.0)}
        )
        assert state.spool_for_gate(gate) is None

    def test_apply_diff_num_gates_resizes_gates(self) -> None:
        """A variant switch resizes gates without touching any gate_* array."""
        state: MMUState = MMUState.from_status(self._full_status())
        assert len(state.apply_diff({"num_gates": 1}).gates) == 1
        grown = state.apply_diff({"num_gates": 4})
        assert len(grown.gates) == 4
        assert grown.gates[3].status is GateStatus.UNKNOWN

    # A 1->4 variant switch grows num_gates before the gate arrays catch up.
    def test_from_status_short_gate_arrays_default_the_tail(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status_extended(4))
        assert len(state.gates) == 4
        tail = state.gates[2:]
        assert [g.index for g in tail] == [2, 3]
        assert all(g.status is GateStatus.UNKNOWN for g in tail)
        assert all(g.spool_id == -1 for g in tail)
        assert all(g.speed_override == 100 for g in tail)

    def test_from_status_long_gate_arrays_are_truncated(self) -> None:
        state: MMUState = MMUState.from_status(self._full_status_extended(1))
        assert len(state.gates) == 1
        assert state.gates[0].status is GateStatus.AVAILABLE

    def test_apply_diff_does_not_alias_sensors(self) -> None:
        """The frozen dataclass must not hand out a reference to the caller's dict."""
        state: MMUState = MMUState.from_status(self._full_status())
        diff = {"sensors": {"mmu_gate": True}}
        updated = state.apply_diff(diff)
        diff["sensors"]["extruder"] = False
        assert updated.sensors == {"mmu_gate": True}

    def test_unknown_enum_values_do_not_raise(self) -> None:
        """PyQt6 turns a ValueError inside a slot into qFatal, killing the whole GUI."""
        state = MMUState.from_status(
            {
                **self._full_status(),
                "gate_status": [99, 0],
                "filament_pos": 42,
                "spoolman_support": "readwrite",
            }
        )
        assert state.gates[0].status is GateStatus.UNKNOWN
        assert state.filament_pos is FilamentPos.UNKNOWN
        assert state.spoolman_support is SpoolmanSupport.OFF

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
        assert state.sensors == {"mmu_pre_gate": True, "mmu_gate": False}

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

        updated = state.apply_diff({"sensors": {"mmu_pre_gate": False}})
        assert updated.sensors == {"mmu_pre_gate": False}
