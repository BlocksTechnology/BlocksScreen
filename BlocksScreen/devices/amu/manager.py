from __future__ import annotations

import dataclasses
import logging
import typing
from pathlib import Path

from PyQt6 import QtCore

from .config_toggler import ConfigToggler
from .models import MMUState, SpoolmanSupport

if typing.TYPE_CHECKING:
    from BlocksScreen.lib.moonrakerComm import MoonWebSocket


logger: logging.Logger = logging.getLogger(__name__)

# Spool Weight threshold for heavy-filament speed profile (grams)
HEAVY_SPOOL_THRESHOLD_G: float = 1000.0
# Absolute target speed (mm/s) for heavy spools - used to calculate SPEED % for MMU_GATE_MAP
HEAVY_SPEED_MM_S: float = 100.0
# Base gear stepper max_velocity (mm/s) - must match mmu_gear max_velocity in printer.cfg
BASE_GEAR_SPEED_MM_S: float = 300.0
# Precomputed speed percentage for heavy spools (avoids repeated division at runtime)
_HEAVY_SPEED_PERCENT: int = max(1, round(HEAVY_SPEED_MM_S / BASE_GEAR_SPEED_MM_S * 100))

CONFIG_PATH: Path = Path("~/printer_data/config/printer.cfg").expanduser()


class AMUManager(QtCore.QObject):
    """Main manager of the AMU system"""

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
    spool_fetched: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, dict, name="spool-fetched"
    )
    gate_weight_updated: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, float, name="gate-weight-updated"
    )

    def __init__(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = ConfigToggler(CONFIG_PATH)
        self._ws = ws
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}
        self.spool_fetched.connect(self._apply_spool_data)

    def _apply_spool_data(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "")
        filament_name = filament.get("name", "")
        temperature = filament.get("settings_extruder_temp")
        bed_temp = filament.get("settings_bed_temp")
        spool_id = data.get("id", -1)
        weight = data.get("used_weight")
        remaining_weight = data.get("remaining_weight")
        self.set_gate_info(
            gate,
            material,
            color,
            spool_id,
            filament_name=filament_name,
            temperature=temperature,
        )
        gates = list(self._mmu_state.gates)
        if gate >= len(gates):
            logger.warning("Gate index %d out of range (%d gate)", gate, len(gates))
            return
        updates = {}
        if weight is not None:
            updates["weight_g"] = float(weight)
        if remaining_weight is not None:
            updates["remaining_weight"] = float(remaining_weight)
            self._emit_speed_gcode(gate, remaining_weight)
        if filament_name:
            updates["filament_name"] = filament_name
        if temperature is not None:
            updates["temperature"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def _emit_speed_gcode(self, gate: int, remaining_weight: float) -> None:
        """Emit MMU_GATE_MAP SPEED=x for the gate based on the spool weight profile."""
        if remaining_weight > HEAVY_SPOOL_THRESHOLD_G:
            self.run_gcode_signal.emit(
                f"MMU_GATE_MAP gate={gate} SPEED={_HEAVY_SPEED_PERCENT}"
            )

    def toggle_amu_system(self, activate: bool) -> None:
        """Enable or disable the AMU system by commenting/uncommenting config includes.

        Emits:
            amu_toggled (bool): True if the operation succeeded, False otherwise.

        Args:
            activate (bool): True to enable the AMU, False to disable it.

        """
        result: bool = self._config_toggler.toggle(activate)
        self.amu_toggled.emit(result)
        if result:
            self.run_gcode_signal.emit("FIRMWARE_RESTART")

    def get_state(self) -> MMUState | None:
        """Returns current MMU state, None if not yet received.

        Returns:
            MMUState: Latest state received from Moonraker
            None: If no state has been received yet.

        """
        return self._mmu_state

    def get_pre_gate_sensors(self) -> dict[int, bool]:
        return dict(self._pre_gate_sensors)

    def is_amu_configured(self) -> bool:
        """Return True if AMU includes are uncommented in printer.cfg."""
        return self._config_toggler.is_configured()

    def is_amu_active(self) -> bool:
        """Returns whether AMU includes are currently uncommented in printer.cfg"""
        return self.is_amu_configured() and self._mmu_state is not None

    def fetch_spool(self, gate: int, spool_id: int) -> None:
        """Request spool data from Moonraker via WebSocket.

        No-op if MMU state not received or spoolman_support is OFF.
        Emits spool_fetched(gate, data) on success; logs and emits nothing on error.
        """

        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support is SpoolmanSupport.OFF:
            return
        if spool_id == -1:
            return

        def _on_result(result: dict | None) -> None:
            if result is not None:
                self.spool_fetched.emit(gate, result)

        self._ws.api.get_spool(spool_id, _on_result)

    def set_gate_info(
        self,
        gate: int,
        material: str,
        color: str,
        spool_id: int,
        filament_name: str = "",
        temperature: int | None = None,
    ) -> None:
        """Sets all gate attributes for a single MMU_GATE

        Args:
            gate (int): Gate index (0-based).
            material (str): Filament material name, e.g. ``"PLA"``.
            color (str): Filament color as hex string, e.g. ``"ff56e0"``.
            spool_id (int): Spoolman spool ID, or -1 if not tracked.
            filament_name (str): Filament display name from Spoolman.
            temperature (int | None): Extruder temperature, omitted if None.
        """
        gcode = f"MMU_GATE_MAP gate={gate} MATERIAL={material} COLOR={color} SPOOLID={spool_id}"
        if filament_name:
            gcode = f"MMU_GATE_MAP gate={gate} NAME={filament_name} MATERIAL={material} COLOR={color} SPOOLID={spool_id}"
        if temperature is not None:
            gcode += f" TEMP={temperature}"
        self.run_gcode_signal.emit(gcode)

    def set_gate_material(self, gate: int, material: str) -> None:
        """Set the `material` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            material (str): Filament material name, e.g. ``"PLA"``.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} MATERIAL={material}")

    def set_gate_color(self, gate: int, color: str) -> None:
        """Set the `color` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            color (str): Filament color, e.g. ``"ff56e0"``.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} COLOR={color}")

    def set_gate_spool(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} SPOOLID={spool_id}")
        if spool_id != -1:
            self.fetch_spool(gate, spool_id)

    def home_mmu(self) -> None:
        """Home the MMU selector by sending MMU_HOME."""
        self.run_gcode_signal.emit("MMU_HOME")

    def reset_mmu(self) -> None:
        """Reset the MMU and clear any pause or error state by sending MMU_RESET."""
        self.run_gcode_signal.emit("MMU_RESET")

    def load_gate(self, gate: int) -> None:
        """Load filament from the specified gate by sending MMU_LOAD

        Args:
            gate (int): Gate index to select (0-based)
        """
        self.run_gcode_signal.emit(f"MMU_SELECT gate={gate}\nMMU_LOAD")

    def unload(self) -> None:
        """Unload the currently loaded filament by sending MMU_UNLOAD."""
        self.run_gcode_signal.emit("MMU_UNLOAD")

    def eject_gate(self, gate: int) -> None:
        """Fully eject filament from gate, releasing from MMU gear.

        Args:
            gate: Gate index to eject from, on None to use currently selected gate.
        """
        self.run_gcode_signal.emit(f"MMU_EJECT GATE={gate}")

    def eject_all_gates(self, num_gates: int) -> None:
        """Fully eject filament from all gates sequentially

        Args:
           num_gates: Total number of gates(from MMUState.num_gates)
        """
        cmd: str = "\n".join(f"MMU_EJECT GATE={i}" for i in range(num_gates))
        self.run_gcode_signal.emit(cmd)

    def select_tool(self, tool: int) -> None:
        """Select a tool, triggering a filament change if needed.

        Args:
            tool (int): Tool index to select (0-based).
        """
        self.run_gcode_signal.emit(f"MMU_CHANGE_TOOL TOOL={tool}")

    def update_mmu_state(self, data: dict, name: str = "") -> None:
        """Receive an MMU status dict from Moonraker and update internal state.

        Called with either a full status response (on connect) or a diff
        (from notify_status_update). Builds or updates the MMUState and
        emits mmu_state_changed.

        Args:
            data: Raw MMU status or diff dict from Moonraker.
            name: Moonraker object name suffix (always empty for ``mmu``).
        """
        if self._mmu_state is None:
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
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def on_pre_gate_update(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def on_load_cell_update(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", name)
            return

        weight = float(values.get("force") or 0)
        if gate >= len(self._mmu_state.gates):
            logger.warning(
                "Gate index %d out of range (%d gates)",
                gate,
                len(self._mmu_state.gates),
            )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def on_klippy_state(self, state: str) -> None:
        """React to changes in klippy states"""
        if state.lower() != "ready":
            self._mmu_state = None
            self._pre_gate_sensors = {}
