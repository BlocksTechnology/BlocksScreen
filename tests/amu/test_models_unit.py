"""Unit tests for BlocksScreen.devices.amu.models."""

from BlocksScreen.devices.amu.models import GateInfo, GateStatus, MMUState

class TestGateStatus:
    def test_values(self):
        assert GateStatus.UNKNOWN == 0
        assert GateStatus.AVAILABLE == 1
        assert GateStatus.AVAILABLE_FROM_BUFFER == 2
        assert GateStatus.EMPTY == -1

    def test_is_int_enum(self):
        assert isinstance(GateStatus.AVAILABLE, int)

class TestGateInfo:
    def _make(self, status: GateStatus) -> GateInfo:
        return GateInfo(index=0, status=status, material="PLA", color="ff0000", color_rgb=(1.0,0.0,0.0), spool_id=1)
    def test_is_available_true_for_available(self):
        assert self._make(GateStatus.AVAILABLE).is_available is True
    def test_is_available_true_for_buffer(self):
        assert self._make(GateStatus.AVAILABLE_FROM_BUFFER).is_available is True
    def test_is_available_false_for_empty(self):
        assert self._make(GateStatus.EMPTY).is_available is False
    def test_is_available_false_for_unknown(self):
        assert self._make(GateStatus.UNKNOWN).is_available is False

class TestMMUState:
    def _full_status(self, num_gates=2) -> dict:
        return {
            "enabled": True,
            "is_homed": True,
            "num_gates": num_gates,
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
    def test_from_status_builds_correctly(self):
        state = MMUState.from_status(self._full_status())
        assert state.num_gates == 2
        assert state.enabled == True
        assert len(state.gates) == 2
        assert state.gates[0].material == "PLA"
        assert state.gates[1].status == GateStatus.EMPTY
        assert state.ttg_map == (0, 1)
    def test_from_status_empty_dict_uses_default(self):
        state = MMUState.from_status({})
        assert state.num_gates == 0
        assert state.enabled ==  False
        assert state.gates == ()
    def test_is_paused_true(self):
        state = MMUState.from_status({**self._full_status(),"print_state": "pause"})
        assert state.is_paused is True
    def test_is_paused_false(self):
        state = MMUState.from_status(self._full_status())
        assert state.is_paused is False
    def test_current_gate_info(self):
        state = MMUState.from_status(self._full_status())
        assert state.current_gate_info is state.gates[0]
    def test_currrent_gate_info_none_when_no_gate(self):
        state = MMUState.from_status({**self._full_status(), "gate": -1})
        assert state.current_gate_info is None
    def test_gate_for_tool(self):
        state = MMUState.from_status(self._full_status())
        assert state.gate_for_tool(0) == 0
        assert state.gate_for_tool(1) == 1
    def test_gate_for_tool_out_of_range(self):
        state = MMUState.from_status(self._full_status())
        assert state.gate_for_tool(99) == -1
    def test_apply_diff_scalar(self):
        state = MMUState.from_status(self._full_status())
        updated = state.apply_diff({"tool": 1, "filament": "Unloaded"})
        assert updated.tool == 1
        assert updated.filament == "Unloaded"
        assert updated.gates == state.gates
    def test_apply_diff_gate_keys(self):
        state = MMUState.from_status(self._full_status())
        updated = state.apply_diff({"gate_status": [1, 1]})
        assert updated.gates[1].status == GateStatus.AVAILABLE
