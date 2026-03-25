import dataclasses
from dataclasses import dataclass
from enum import IntEnum


class GateStatus(IntEnum):
    UNKNOWN = 0
    AVAILABLE = 1
    AVAILABLE_FROM_BUFFER = 2
    EMPTY = -1


@dataclass(frozen=True, slots=True)
class GateInfo:
    index: int
    status: GateStatus
    material: str
    color: str
    color_rgb: tuple[float, float, float]
    spool_id: int

    @property
    def is_available(self) -> bool:
        """Return True if the gate has filament available to load."""
        return self.status in (GateStatus.AVAILABLE, GateStatus.AVAILABLE_FROM_BUFFER)


@dataclass(frozen=True, slots=True)
class MMUState:
    enabled: bool
    is_homed: bool
    num_gates: int
    tool: int
    gate: int
    filament: str  # "Loaded" | "Unloaded" | "Unknown"
    action: str
    print_state: str
    reason_for_pause: str
    gates: tuple[GateInfo, ...]
    ttg_map: tuple[int, ...]

    @property
    def is_paused(self) -> bool:
        """Return True if the MMU is in a paused/error state."""
        return self.print_state == "pause"

    @property
    def current_gate_info(self) -> GateInfo | None:
        """Return the GateInfo for the currently selected gate, or None if no gate is selected."""
        if 0 <= self.gate < len(self.gates):
            return self.gates[self.gate]
        return None

    @classmethod
    def from_status(cls, data: dict) -> "MMUState":
        """Build an MMUState from a full Moonraker mmu status dict.

        Args:
            data (dict): Full status dict from printer.objects.query or the initial notify_status_update payload.

        Returns:
            MMUState: New instance populated from *data*
        """
        num_gates = data.get("num_gates", 0)

        statuses = data.get("gate_status", [GateStatus.UNKNOWN] * num_gates)
        material = data.get("gate_material", [""] * num_gates)
        colors = data.get("gate_color", [""] * num_gates)
        rgbs = data.get("gate_color_rgb", [(0.0, 0.0, 0.0)] * num_gates)
        spool_ids = data.get("gate_spool_id", [-1] * num_gates)

        gates: tuple[GateInfo, ...] = tuple(
            GateInfo(
                index=i,
                status=GateStatus(statuses[i]),
                material=material[i],
                color=colors[i],
                color_rgb=tuple(rgbs[i]),
                spool_id=spool_ids[i],
            )
            for i in range(num_gates)
        )
        return cls(
            enabled=data.get("enabled", False),
            is_homed=data.get("is_homed", False),
            num_gates=num_gates,
            tool=data.get("tool", -1),
            gate=data.get("gate", -1),
            filament=data.get("filament", "Unknown"),
            action=data.get("action", ""),
            print_state=data.get("print_state", ""),
            reason_for_pause=data.get("reason_for_pause", ""),
            gates=gates,
            ttg_map=tuple(data.get("ttg_map", [])),
        )

    def gate_for_tool(self, tool: int) -> int:
        """Returns the gate mapped to *tool*, or -1 if unmapped."""
        if 0 <= tool < len(self.ttg_map):
            return self.ttg_map[tool]
        return -1

    def apply_diff(self, diff: dict) -> "MMUState":
        """Apply a Moonraker status diff and return an updated MMUState.

        Args:
            diff (dict): Partial status dict from notify_status_update.

        Returns:
            MMUState: New instance with updated fields
        """
        gate_keys: set[str] = {
            "gate_status",
            "gate_material",
            "gate_color",
            "gate_color_rgb",
            "gate_spool_id",
        }
        if gate_keys.isdisjoint(diff):
            # No changes
            scalar_fields = {
                k: v for k, v in diff.items() if k in MMUState.__dataclass_fields__
            }
            if "ttg_map" in scalar_fields:
                scalar_fields["ttg_map"] = tuple(scalar_fields["ttg_map"])
            return dataclasses.replace(self, **scalar_fields)
        # Gate arrays changed — need full rebuild, but we lost the raw arrays
        # Pass current gate data + diff into from_status
        gate_data = {
            "gate_status": [g.status for g in self.gates],
            "gate_material": [g.material for g in self.gates],
            "gate_color": [g.color for g in self.gates],
            "gate_color_rgb": [g.color_rgb for g in self.gates],
            "gate_spool_id": [g.spool_id for g in self.gates],
        }
        merged = {**dataclasses.asdict(self), **gate_data, **diff}
        return MMUState.from_status(merged)
