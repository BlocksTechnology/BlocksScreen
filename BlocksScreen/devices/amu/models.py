"""Immutable value types mirroring the MMU status Happy-Hare publishes to Moonraker."""

from __future__ import annotations

import dataclasses
import logging
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import IntEnum, StrEnum

logger = logging.getLogger(__name__)


def _rgb(value: Sequence[float]) -> tuple[float, float, float]:
    """Coerce a colour sequence to a fixed 3-tuple, padding a short one with zeroes."""
    r, g, b = [*value, 0.0, 0.0, 0.0][:3]
    return (float(r), float(g), float(b))


class GateStatus(IntEnum):
    """Gate filament availability, matching Happy-Hare's GATE_* codes (mmu.py:59)."""

    UNKNOWN = -1
    EMPTY = 0
    AVAILABLE = 1
    AVAILABLE_FROM_BUFFER = 2

    @classmethod
    def _missing_(cls, value: object) -> GateStatus:
        """Firmware can ship new codes; an unhandled ValueError would qFatal the GUI."""
        logger.warning("Unknown GateStatus %r, treating as UNKNOWN", value)
        return cls.UNKNOWN


class FilamentPos(IntEnum):
    """State-machine position of the filament inside the MMU/extruder path."""

    UNKNOWN = -1
    UNLOADED = 0
    HOMED_GATE = 1
    START_BOWDEN = 2
    IN_BOWDEN = 3
    END_BOWDEN = 4
    HOMED_ENTRY = 5
    HOMED_EXTRUDER = 6
    EXTRUDER_ENTRY = 7
    HOMED_TS = 8
    IN_EXTRUDER = 9
    LOADED = 10

    @classmethod
    def _missing_(cls, value: object) -> FilamentPos:
        """Firmware can ship new codes; an unhandled ValueError would qFatal the GUI."""
        logger.warning("Unknown FilamentPos %r, treating as UNKNOWN", value)
        return cls.UNKNOWN


class SpoolmanSupport(StrEnum):
    """Level of Spoolman integration configured in Happy-Hare."""

    OFF = "off"
    READONLY = "readonly"
    PUSH = "push"
    PULL = "pull"

    @classmethod
    def _missing_(cls, value: object) -> SpoolmanSupport:
        """OFF is the safe default: it suppresses Spoolman writes, not guesses."""
        logger.warning("Unknown SpoolmanSupport %r, treating as OFF", value)
        return cls.OFF


_GATE_ARRAYS: dict[str, str] = {
    "gate_status": "status",
    "gate_material": "material",
    "gate_color": "color",
    "gate_color_rgb": "color_rgb",
    "gate_spool_id": "spool_id",
    "gate_filament_name": "filament_name",
    "gate_temperature": "temperature",
    "gate_speed_override": "speed_override",
    "drying_state": "drying_state",
}

_GATE_COERCE: dict[str, Callable] = {
    "status": GateStatus,
    "color_rgb": _rgb,
}

_GATE_DIFF_KEYS: frozenset[str] = frozenset(_GATE_ARRAYS) | {"num_gates"}

_SCALAR_COERCE: dict[str, Callable] = {
    "ttg_map": tuple,
    "endless_spool_groups": tuple,
    "filament_pos": FilamentPos,
    "spoolman_support": SpoolmanSupport,
    "sensors": dict,
}


@dataclass(frozen=True, slots=True)
class GateInfo:
    """One gate as Happy-Hare publishes it."""

    index: int
    status: GateStatus = GateStatus.UNKNOWN
    material: str = ""
    color: str = ""
    color_rgb: tuple[float, float, float] = (0.0, 0.0, 0.0)
    spool_id: int = -1
    filament_name: str = ""
    temperature: float | None = None
    speed_override: int = 100
    drying_state: str = ""

    @property
    def is_available(self) -> bool:
        """Return True if the gate has filament available to load."""
        return self.status in (GateStatus.AVAILABLE, GateStatus.AVAILABLE_FROM_BUFFER)


def _gates(arrays: Mapping[str, Sequence], num_gates: int) -> tuple[GateInfo, ...]:
    """Build the gate tuple from parallel arrays, leaving short ones defaulted."""
    return tuple(
        GateInfo(
            index=i,
            **{
                f: _GATE_COERCE[f](v[i]) if f in _GATE_COERCE else v[i]
                for f, v in arrays.items()
                if i < len(v)
            },
        )
        for i in range(num_gates)
    )


@dataclass(frozen=True, slots=True)
class MMUState:
    """A full snapshot of the MMU; rebuilt, never mutated, on every status update."""

    enabled: bool
    is_homed: bool
    num_gates: int
    tool: int
    gate: int
    filament: str  # "Loaded" | "Unloaded" | "Unknown"
    filament_pos: FilamentPos
    action: str
    bowden_progress: float
    print_state: str
    reason_for_pause: str
    has_bypass: bool
    spoolman_support: SpoolmanSupport
    gates: tuple[GateInfo, ...]
    ttg_map: tuple[int, ...]
    pending_spool_id: int = -1
    operation: str = ""
    sensors: dict[str, bool | None] = dataclasses.field(default_factory=dict)
    endless_spool_groups: tuple[int, ...] = dataclasses.field(default_factory=tuple)

    @property
    def is_paused(self) -> bool:
        """Return True if the MMU is in a paused/error state."""
        return self.print_state in ("paused", "pause_locked")

    @property
    def current_gate_info(self) -> GateInfo | None:
        """Return the GateInfo for the selected gate, or None when none is selected."""
        if 0 <= self.gate < len(self.gates):
            return self.gates[self.gate]
        return None

    @classmethod
    def from_status(cls, data: dict) -> MMUState:
        """Build an MMUState from a full Moonraker mmu status dict."""
        num_gates = data.get("num_gates", 0)
        arrays = {field: data.get(key, ()) for key, field in _GATE_ARRAYS.items()}
        return cls(
            enabled=data.get("enabled", False),
            is_homed=data.get("is_homed", False),
            num_gates=num_gates,
            tool=data.get("tool", -1),
            gate=data.get("gate", -1),
            filament=data.get("filament", "Unknown"),
            filament_pos=FilamentPos(data.get("filament_pos", FilamentPos.UNKNOWN)),
            action=data.get("action", ""),
            bowden_progress=data.get("bowden_progress", -1),
            print_state=data.get("print_state", ""),
            reason_for_pause=data.get("reason_for_pause", ""),
            has_bypass=data.get("has_bypass", False),
            spoolman_support=SpoolmanSupport(
                data.get("spoolman_support", SpoolmanSupport.OFF)
            ),
            gates=_gates(arrays, num_gates),
            ttg_map=tuple(data.get("ttg_map", [])),
            pending_spool_id=data.get("pending_spool_id", -1),
            operation=data.get("operation", ""),
            sensors=dict(data.get("sensors", {})),
            endless_spool_groups=tuple(data.get("endless_spool_groups", [])),
        )

    def gate_for_tool(self, tool: int) -> int:
        """Return the gate mapped to *tool*, or -1 if unmapped."""
        if 0 <= tool < len(self.ttg_map):
            return self.ttg_map[tool]
        return -1

    def apply_diff(self, diff: dict) -> MMUState:
        """Return a new MMUState with a notify_status_update diff applied."""
        changed = {
            k: _SCALAR_COERCE[k](v) if k in _SCALAR_COERCE else v
            for k, v in diff.items()
            if k in _STATE_FIELDS
        }
        if _GATE_DIFF_KEYS.isdisjoint(diff):
            return dataclasses.replace(self, **changed)
        arrays = {
            f: diff[key] if key in diff else [getattr(g, f) for g in self.gates]
            for key, f in _GATE_ARRAYS.items()
        }
        num_gates = changed.get("num_gates", self.num_gates)
        return dataclasses.replace(self, **changed, gates=_gates(arrays, num_gates))


_STATE_FIELDS: frozenset[str] = frozenset(f.name for f in dataclasses.fields(MMUState))
