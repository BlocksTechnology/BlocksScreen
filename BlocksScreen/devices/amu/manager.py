"""Qt-side facade for the AMU: owns MMU state and issues Happy-Hare gcode."""

from __future__ import annotations

import logging
import shlex
import typing
from pathlib import Path

from PyQt6 import QtCore

from .config_toggler import ConfigToggler, ToggleResult
from .models import (
    FilamentPos,
    GateInfo,
    GateStatus,
    MMUState,
    SpoolmanSupport,
)

if typing.TYPE_CHECKING:
    from BlocksScreen.lib.moonrakerComm import MoonWebSocket


logger: logging.Logger = logging.getLogger(__name__)

CONFIG_PATH: Path = Path("~/printer_data/config/printer.cfg").expanduser()


def _gcode_value(value: object) -> str:
    """Quote a value for Klipper's shlex-based extended gcode parser."""
    if isinstance(value, float):
        value = round(value)
    # A raw newline would end the gcode line.
    text = " ".join(str(value).split())
    return shlex.quote(text)


class AMUManager(QtCore.QObject):
    """Owns the MMU state and turns UI intents into guarded Happy-Hare gcode."""

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )

    mmu_state_changed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        object, name="mmu-state-changed"
    )

    amu_toggled: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="amu-toggled"
    )

    pre_gate_changed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, bool, name="pre-gate-changed"
    )

    def __init__(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = ConfigToggler(CONFIG_PATH)
        self._ws = ws
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}

    def _gate_map(self, gate: int, **params: object) -> bool:
        """Emit MMU_GATE_MAP for one gate; False when no gate is selected yet."""
        if gate < 0:
            logger.warning("Ignoring gate command for unselected gate %d", gate)
            return False
        # TEMP=0 keeps the current temp; TEMP=None omits it, resetting to the default.
        params.setdefault("TEMP", 0)
        args = "".join(
            f" {key}={_gcode_value(value)}"
            for key, value in params.items()
            if value is not None
        )
        self.run_gcode_signal.emit(f"MMU_GATE_MAP GATE={gate}{args} QUIET=1")
        return True

    def toggle_amu_system(self, activate: bool) -> None:
        """Swap the printer.cfg variant, restarting on change; emits amu_toggled."""
        result = self._config_toggler.toggle(activate)
        self.amu_toggled.emit(result is not ToggleResult.FAILED)
        if result is ToggleResult.CHANGED:
            self.run_gcode_signal.emit("FIRMWARE_RESTART")

    def get_state(self) -> MMUState | None:
        """Return the latest MMU state, or None before the first status arrives."""
        return self._mmu_state

    def get_pre_gate_sensors(self) -> dict[int, bool]:
        """Return a copy of the per-gate pre-gate switch states, keyed by gate index."""
        return dict(self._pre_gate_sensors)

    def is_amu_configured(self) -> bool:
        """Return True if AMU includes are uncommented in printer.cfg."""
        return self._config_toggler.is_configured()

    def is_amu_active(self) -> bool:
        """Return True if the AMU is configured, reporting, and not MMU-disabled."""
        state = self._mmu_state
        return self.is_amu_configured() and state is not None and state.enabled

    def set_gate_info(
        self,
        gate: int,
        material: str,
        color: str,
        spool_id: int,
        filament_name: str = "",
        temperature: int | None = None,
    ) -> bool:
        """Map every field of *gate*; a None temperature takes Happy-Hare's default."""
        return self._gate_map(
            gate,
            NAME=filament_name,
            MATERIAL=material,
            COLOR=color.lstrip("#"),
            SPOOLID=spool_id,
            TEMP=temperature,
        )

    def clear_gate(self, gate: int) -> None:
        """Blank a gate's map entry the way Happy-Hare resets one."""
        self._gate_map(gate, NAME="", MATERIAL="", COLOR="", SPOOLID=-1, TEMP=None)

    def set_gate_material(self, gate: int, material: str) -> None:
        """Set the material of *gate*, keeping its temperature."""
        self._gate_map(gate, MATERIAL=material)

    def set_gate_temp(self, gate: int, temp: int) -> None:
        """Set the extruder temperature of *gate*."""
        self._gate_map(gate, TEMP=temp)

    def set_gate_color(self, gate: int, color: str) -> None:
        """Set the hex colour of *gate*, with or without a leading #."""
        self._gate_map(gate, COLOR=color.lstrip("#"))

    def set_gate_spool(self, gate: int, spool_id: int) -> None:
        """Bind *gate* to a Spoolman spool; -1 unbinds."""
        self._gate_map(gate, SPOOLID=spool_id)

    def assign_spool(self, gate: int, spool: dict) -> None:
        """Map *gate* from a Spoolman spool payload."""
        filament = spool.get("filament") or {}
        self.set_gate_info(
            gate,
            filament.get("material") or "",
            filament.get("color_hex") or "",
            spool.get("id", -1),
            filament_name=filament.get("name") or "",
            temperature=filament.get("settings_extruder_temp"),
        )

    def update_spool_weight(self, gate: int, used_weight: float) -> None:
        """Push *used_weight* to Spoolman for the spool at *gate*."""
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if not 0 <= gate < len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def home_mmu(self) -> None:
        """Re-select the current tool via MMU_HOME; refused while filament is loaded."""
        state = self._mmu_state
        # Bare MMU_HOME defaults to TOOL=0 with no loaded guard.
        if state is not None and state.filament_pos not in (
            FilamentPos.UNLOADED,
            FilamentPos.UNKNOWN,
        ):
            logger.warning(
                "Ignoring MMU_HOME while filament is %s", state.filament_pos.name
            )
            return
        tool = state.tool if state is not None else -1
        self.run_gcode_signal.emit(f"MMU_HOME TOOL={tool}" if tool >= 0 else "MMU_HOME")

    def reset_mmu(self) -> None:
        """Erase all persisted MMU state (gate map, TTG map, statistics) and re-init."""
        self.run_gcode_signal.emit("MMU_RESET CONFIRM=1")

    def _selected_gate_unloaded(self) -> GateInfo | None:
        """Return the selected gate when the MMU is enabled, homed and unloaded."""
        state = self._mmu_state
        if (
            state is None
            or not (state.enabled and state.is_homed)
            or state.filament_pos != FilamentPos.UNLOADED
        ):
            return None
        return state.current_gate_info

    def load_gate(self) -> bool:
        """Load filament from the selected gate by sending MMU_LOAD; True if sent."""
        if self._selected_gate_unloaded() is None:
            logger.warning("Ignoring MMU_LOAD: no homed, unloaded gate selected")
            return False
        self.run_gcode_signal.emit("MMU_LOAD")
        return True

    def unload(self) -> bool:
        """Unload the currently loaded filament by sending MMU_UNLOAD; True if sent."""
        state = self._mmu_state
        if (
            state is None
            or not state.enabled
            or state.filament_pos == FilamentPos.UNLOADED
        ):
            logger.warning("Ignoring MMU_UNLOAD: MMU disabled or nothing loaded")
            return False
        self.run_gcode_signal.emit("MMU_UNLOAD")
        return True

    def select_gate(self, gate: int) -> None:
        """Send MMU_SELECT unless invalid, already selected, or filament is loaded."""
        state = self._mmu_state
        if state is None or not 0 <= gate < state.num_gates or gate == state.gate:
            return
        if state.filament_pos != FilamentPos.UNLOADED:
            logger.warning(
                "Ignoring MMU_SELECT while filament is %s", state.filament_pos.name
            )
            return
        self.run_gcode_signal.emit(f"MMU_SELECT GATE={gate}")

    def eject_gate(self) -> None:
        """Fully eject filament from the selected gate, the only gate that can eject."""
        gate = self._selected_gate_unloaded()
        if gate is None or gate.status == GateStatus.EMPTY:
            logger.warning("Ignoring MMU_EJECT: no unloaded, non-empty gate selected")
            return
        self.run_gcode_signal.emit("MMU_EJECT")

    def check_gate(self) -> None:
        """Check the selected gate for filament by sending MMU_CHECK_GATE."""
        # Happy-Hare runs a full unload first when not UNLOADED.
        if self._selected_gate_unloaded() is None:
            logger.warning("Ignoring MMU_CHECK_GATE: no unloaded gate selected")
            return
        self.run_gcode_signal.emit("MMU_CHECK_GATE")

    def recover_single_gate(self, loaded: bool) -> None:
        """Tell Happy-Hare whether the single-gate filament path is loaded."""
        self.run_gcode_signal.emit(f"MMU_RECOVER TOOL=0 GATE=0 LOADED={int(loaded)}")

    def change_tool(self, tool: int) -> None:
        """Select *tool* with MMU_CHANGE_TOOL, swapping filament if needed."""
        self.run_gcode_signal.emit(f"MMU_CHANGE_TOOL TOOL={tool}")

    def update_mmu_state(self, data: dict) -> None:
        """Build state from a full status or apply a diff; emit mmu_state_changed."""
        if self._mmu_state is None:
            if "num_gates" not in data:
                return
            self._mmu_state = MMUState.from_status(data)
        else:
            self._mmu_state = self._mmu_state.apply_diff(data)
        self.mmu_state_changed.emit(self._mmu_state)

    def on_object_updated(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)

    def on_pre_gate_update(self, values: dict, name: str) -> None:
        """Track one pre-gate switch; the mmu aggregate hides unselected gates."""
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        # Enabled-only diffs omit it; reading False would invent empty gates.
        if "filament_detected" not in values:
            return
        detected = bool(values["filament_detected"])
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    @QtCore.pyqtSlot(str)
    def on_klippy_state(self, state: str) -> None:
        """Drop cached MMU state when klippy leaves ready and tell the UI it is gone."""
        if state.lower() == "ready":
            return
        self._pre_gate_sensors = {}
        if self._mmu_state is None:
            return
        self._mmu_state = None
        self.mmu_state_changed.emit(None)
