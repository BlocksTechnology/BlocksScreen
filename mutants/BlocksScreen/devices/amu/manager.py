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
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


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
        args = [ws, parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁ__init____mutmut_orig(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = ConfigToggler(CONFIG_PATH)
        self._ws = ws
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}
        self.spool_fetched.connect(self._apply_spool_data)

    def xǁAMUManagerǁ__init____mutmut_1(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(None)
        self._config_toggler = ConfigToggler(CONFIG_PATH)
        self._ws = ws
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}
        self.spool_fetched.connect(self._apply_spool_data)

    def xǁAMUManagerǁ__init____mutmut_2(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = None
        self._ws = ws
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}
        self.spool_fetched.connect(self._apply_spool_data)

    def xǁAMUManagerǁ__init____mutmut_3(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = ConfigToggler(None)
        self._ws = ws
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}
        self.spool_fetched.connect(self._apply_spool_data)

    def xǁAMUManagerǁ__init____mutmut_4(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = ConfigToggler(CONFIG_PATH)
        self._ws = None
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}
        self.spool_fetched.connect(self._apply_spool_data)

    def xǁAMUManagerǁ__init____mutmut_5(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = ConfigToggler(CONFIG_PATH)
        self._ws = ws
        self._mmu_state: MMUState | None = ""
        self._pre_gate_sensors: dict[int, bool] = {}
        self.spool_fetched.connect(self._apply_spool_data)

    def xǁAMUManagerǁ__init____mutmut_6(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = ConfigToggler(CONFIG_PATH)
        self._ws = ws
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = None
        self.spool_fetched.connect(self._apply_spool_data)

    def xǁAMUManagerǁ__init____mutmut_7(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = ConfigToggler(CONFIG_PATH)
        self._ws = ws
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}
        self.spool_fetched.connect(None)
    
    xǁAMUManagerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁ__init____mutmut_1': xǁAMUManagerǁ__init____mutmut_1, 
        'xǁAMUManagerǁ__init____mutmut_2': xǁAMUManagerǁ__init____mutmut_2, 
        'xǁAMUManagerǁ__init____mutmut_3': xǁAMUManagerǁ__init____mutmut_3, 
        'xǁAMUManagerǁ__init____mutmut_4': xǁAMUManagerǁ__init____mutmut_4, 
        'xǁAMUManagerǁ__init____mutmut_5': xǁAMUManagerǁ__init____mutmut_5, 
        'xǁAMUManagerǁ__init____mutmut_6': xǁAMUManagerǁ__init____mutmut_6, 
        'xǁAMUManagerǁ__init____mutmut_7': xǁAMUManagerǁ__init____mutmut_7
    }
    xǁAMUManagerǁ__init____mutmut_orig.__name__ = 'xǁAMUManagerǁ__init__'

    def _apply_spool_data(self, gate: int, data: dict) -> None:
        args = [gate, data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁ_apply_spool_data__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁ_apply_spool_data__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁ_apply_spool_data__mutmut_orig(self, gate: int, data: dict) -> None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_1(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is not None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_2(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_3(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get(None, {})
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_4(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_5(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get({})
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_6(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", )
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_7(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("XXfilamentXX", {})
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_8(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("FILAMENT", {})
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_9(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_10(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get(None, "")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_11(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_12(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_13(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", )
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_14(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("XXmaterialXX", "")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_15(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("MATERIAL", "")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_16(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "XXXX")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_17(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_18(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get(None, "")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_19(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_20(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_21(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", )
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_22(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("XXcolor_hexXX", "")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_23(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("COLOR_HEX", "")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_24(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "XXXX")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_25(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "")
        filament_name = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_26(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "")
        filament_name = filament.get(None, "")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_27(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "")
        filament_name = filament.get("name", None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_28(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "")
        filament_name = filament.get("")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_29(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "")
        filament_name = filament.get("name", )
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_30(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "")
        filament_name = filament.get("XXnameXX", "")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_31(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "")
        filament_name = filament.get("NAME", "")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_32(self, gate: int, data: dict) -> None:
        """Apply Spoolman spool data to local gate state and sync to Klipper.

        Extracts material, color, weight from the Spoolman response dict,
        emits MMU_GATE_MAP gcode to sync Klipper, and updates the local GateInfo weight.
        """
        if self._mmu_state is None:
            return
        filament = data.get("filament", {})
        material = filament.get("material", "")
        color = filament.get("color_hex", "")
        filament_name = filament.get("name", "XXXX")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_33(self, gate: int, data: dict) -> None:
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
        temperature = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_34(self, gate: int, data: dict) -> None:
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
        temperature = filament.get(None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_35(self, gate: int, data: dict) -> None:
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
        temperature = filament.get("XXsettings_extruder_tempXX")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_36(self, gate: int, data: dict) -> None:
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
        temperature = filament.get("SETTINGS_EXTRUDER_TEMP")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_37(self, gate: int, data: dict) -> None:
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
        bed_temp = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_38(self, gate: int, data: dict) -> None:
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
        bed_temp = filament.get(None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_39(self, gate: int, data: dict) -> None:
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
        bed_temp = filament.get("XXsettings_bed_tempXX")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_40(self, gate: int, data: dict) -> None:
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
        bed_temp = filament.get("SETTINGS_BED_TEMP")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_41(self, gate: int, data: dict) -> None:
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
        spool_id = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_42(self, gate: int, data: dict) -> None:
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
        spool_id = data.get(None, -1)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_43(self, gate: int, data: dict) -> None:
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
        spool_id = data.get("id", None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_44(self, gate: int, data: dict) -> None:
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
        spool_id = data.get(-1)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_45(self, gate: int, data: dict) -> None:
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
        spool_id = data.get("id", )
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_46(self, gate: int, data: dict) -> None:
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
        spool_id = data.get("XXidXX", -1)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_47(self, gate: int, data: dict) -> None:
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
        spool_id = data.get("ID", -1)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_48(self, gate: int, data: dict) -> None:
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
        spool_id = data.get("id", +1)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_49(self, gate: int, data: dict) -> None:
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
        spool_id = data.get("id", -2)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_50(self, gate: int, data: dict) -> None:
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
        weight = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_51(self, gate: int, data: dict) -> None:
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
        weight = data.get(None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_52(self, gate: int, data: dict) -> None:
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
        weight = data.get("XXused_weightXX")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_53(self, gate: int, data: dict) -> None:
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
        weight = data.get("USED_WEIGHT")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_54(self, gate: int, data: dict) -> None:
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
        remaining_weight = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_55(self, gate: int, data: dict) -> None:
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
        remaining_weight = data.get(None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_56(self, gate: int, data: dict) -> None:
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
        remaining_weight = data.get("XXremaining_weightXX")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_57(self, gate: int, data: dict) -> None:
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
        remaining_weight = data.get("REMAINING_WEIGHT")
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_58(self, gate: int, data: dict) -> None:
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
            None,
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_59(self, gate: int, data: dict) -> None:
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
            None,
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_60(self, gate: int, data: dict) -> None:
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
            None,
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_61(self, gate: int, data: dict) -> None:
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
            None,
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_62(self, gate: int, data: dict) -> None:
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
            filament_name=None,
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_63(self, gate: int, data: dict) -> None:
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
            temperature=None,
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_64(self, gate: int, data: dict) -> None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_65(self, gate: int, data: dict) -> None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_66(self, gate: int, data: dict) -> None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_67(self, gate: int, data: dict) -> None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_68(self, gate: int, data: dict) -> None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_69(self, gate: int, data: dict) -> None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_70(self, gate: int, data: dict) -> None:
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
        gates = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_71(self, gate: int, data: dict) -> None:
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
        gates = list(None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_72(self, gate: int, data: dict) -> None:
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
        if gate > len(gates):
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_73(self, gate: int, data: dict) -> None:
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
            logger.warning(None, gate, len(gates))
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_74(self, gate: int, data: dict) -> None:
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
            logger.warning("Gate index %d out of range (%d gate)", None, len(gates))
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_75(self, gate: int, data: dict) -> None:
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
            logger.warning("Gate index %d out of range (%d gate)", gate, None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_76(self, gate: int, data: dict) -> None:
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
            logger.warning(gate, len(gates))
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_77(self, gate: int, data: dict) -> None:
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
            logger.warning("Gate index %d out of range (%d gate)", len(gates))
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_78(self, gate: int, data: dict) -> None:
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
            logger.warning("Gate index %d out of range (%d gate)", gate, )
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_79(self, gate: int, data: dict) -> None:
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
            logger.warning("XXGate index %d out of range (%d gate)XX", gate, len(gates))
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_80(self, gate: int, data: dict) -> None:
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
            logger.warning("gate index %d out of range (%d gate)", gate, len(gates))
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_81(self, gate: int, data: dict) -> None:
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
            logger.warning("GATE INDEX %D OUT OF RANGE (%D GATE)", gate, len(gates))
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_82(self, gate: int, data: dict) -> None:
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
        updates = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_83(self, gate: int, data: dict) -> None:
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
        if weight is None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_84(self, gate: int, data: dict) -> None:
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
            updates["weight_g"] = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_85(self, gate: int, data: dict) -> None:
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
            updates["XXweight_gXX"] = float(weight)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_86(self, gate: int, data: dict) -> None:
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
            updates["WEIGHT_G"] = float(weight)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_87(self, gate: int, data: dict) -> None:
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
            updates["weight_g"] = float(None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_88(self, gate: int, data: dict) -> None:
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
        if remaining_weight is None:
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_89(self, gate: int, data: dict) -> None:
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
            updates["remaining_weight"] = None
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_90(self, gate: int, data: dict) -> None:
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
            updates["XXremaining_weightXX"] = float(remaining_weight)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_91(self, gate: int, data: dict) -> None:
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
            updates["REMAINING_WEIGHT"] = float(remaining_weight)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_92(self, gate: int, data: dict) -> None:
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
            updates["remaining_weight"] = float(None)
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

    def xǁAMUManagerǁ_apply_spool_data__mutmut_93(self, gate: int, data: dict) -> None:
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
            self._emit_speed_gcode(None, remaining_weight)
        if filament_name:
            updates["filament_name"] = filament_name
        if temperature is not None:
            updates["temperature"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_94(self, gate: int, data: dict) -> None:
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
            self._emit_speed_gcode(gate, None)
        if filament_name:
            updates["filament_name"] = filament_name
        if temperature is not None:
            updates["temperature"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_95(self, gate: int, data: dict) -> None:
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
            self._emit_speed_gcode(remaining_weight)
        if filament_name:
            updates["filament_name"] = filament_name
        if temperature is not None:
            updates["temperature"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_96(self, gate: int, data: dict) -> None:
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
            self._emit_speed_gcode(gate, )
        if filament_name:
            updates["filament_name"] = filament_name
        if temperature is not None:
            updates["temperature"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_97(self, gate: int, data: dict) -> None:
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
            updates["filament_name"] = None
        if temperature is not None:
            updates["temperature"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_98(self, gate: int, data: dict) -> None:
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
            updates["XXfilament_nameXX"] = filament_name
        if temperature is not None:
            updates["temperature"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_99(self, gate: int, data: dict) -> None:
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
            updates["FILAMENT_NAME"] = filament_name
        if temperature is not None:
            updates["temperature"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_100(self, gate: int, data: dict) -> None:
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
        if temperature is None:
            updates["temperature"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_101(self, gate: int, data: dict) -> None:
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
            updates["temperature"] = None
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_102(self, gate: int, data: dict) -> None:
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
            updates["XXtemperatureXX"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_103(self, gate: int, data: dict) -> None:
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
            updates["TEMPERATURE"] = float(temperature)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_104(self, gate: int, data: dict) -> None:
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
            updates["temperature"] = float(None)
        if bed_temp is not None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_105(self, gate: int, data: dict) -> None:
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
        if bed_temp is None:
            updates["bed_temp"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_106(self, gate: int, data: dict) -> None:
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
            updates["bed_temp"] = None
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_107(self, gate: int, data: dict) -> None:
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
            updates["XXbed_tempXX"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_108(self, gate: int, data: dict) -> None:
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
            updates["BED_TEMP"] = int(bed_temp)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_109(self, gate: int, data: dict) -> None:
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
            updates["bed_temp"] = int(None)
        if updates:
            gates[gate] = dataclasses.replace(gates[gate], **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_110(self, gate: int, data: dict) -> None:
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
            gates[gate] = None
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_111(self, gate: int, data: dict) -> None:
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
            gates[gate] = dataclasses.replace(None, **updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_112(self, gate: int, data: dict) -> None:
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
            gates[gate] = dataclasses.replace(**updates)
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_113(self, gate: int, data: dict) -> None:
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
            gates[gate] = dataclasses.replace(gates[gate], )
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_114(self, gate: int, data: dict) -> None:
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
            self._mmu_state = None

    def xǁAMUManagerǁ_apply_spool_data__mutmut_115(self, gate: int, data: dict) -> None:
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
            self._mmu_state = dataclasses.replace(None, gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_116(self, gate: int, data: dict) -> None:
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
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=None)

    def xǁAMUManagerǁ_apply_spool_data__mutmut_117(self, gate: int, data: dict) -> None:
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
            self._mmu_state = dataclasses.replace(gates=tuple(gates))

    def xǁAMUManagerǁ_apply_spool_data__mutmut_118(self, gate: int, data: dict) -> None:
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
            self._mmu_state = dataclasses.replace(self._mmu_state, )

    def xǁAMUManagerǁ_apply_spool_data__mutmut_119(self, gate: int, data: dict) -> None:
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
            self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(None))
    
    xǁAMUManagerǁ_apply_spool_data__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁ_apply_spool_data__mutmut_1': xǁAMUManagerǁ_apply_spool_data__mutmut_1, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_2': xǁAMUManagerǁ_apply_spool_data__mutmut_2, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_3': xǁAMUManagerǁ_apply_spool_data__mutmut_3, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_4': xǁAMUManagerǁ_apply_spool_data__mutmut_4, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_5': xǁAMUManagerǁ_apply_spool_data__mutmut_5, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_6': xǁAMUManagerǁ_apply_spool_data__mutmut_6, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_7': xǁAMUManagerǁ_apply_spool_data__mutmut_7, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_8': xǁAMUManagerǁ_apply_spool_data__mutmut_8, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_9': xǁAMUManagerǁ_apply_spool_data__mutmut_9, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_10': xǁAMUManagerǁ_apply_spool_data__mutmut_10, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_11': xǁAMUManagerǁ_apply_spool_data__mutmut_11, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_12': xǁAMUManagerǁ_apply_spool_data__mutmut_12, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_13': xǁAMUManagerǁ_apply_spool_data__mutmut_13, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_14': xǁAMUManagerǁ_apply_spool_data__mutmut_14, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_15': xǁAMUManagerǁ_apply_spool_data__mutmut_15, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_16': xǁAMUManagerǁ_apply_spool_data__mutmut_16, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_17': xǁAMUManagerǁ_apply_spool_data__mutmut_17, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_18': xǁAMUManagerǁ_apply_spool_data__mutmut_18, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_19': xǁAMUManagerǁ_apply_spool_data__mutmut_19, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_20': xǁAMUManagerǁ_apply_spool_data__mutmut_20, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_21': xǁAMUManagerǁ_apply_spool_data__mutmut_21, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_22': xǁAMUManagerǁ_apply_spool_data__mutmut_22, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_23': xǁAMUManagerǁ_apply_spool_data__mutmut_23, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_24': xǁAMUManagerǁ_apply_spool_data__mutmut_24, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_25': xǁAMUManagerǁ_apply_spool_data__mutmut_25, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_26': xǁAMUManagerǁ_apply_spool_data__mutmut_26, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_27': xǁAMUManagerǁ_apply_spool_data__mutmut_27, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_28': xǁAMUManagerǁ_apply_spool_data__mutmut_28, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_29': xǁAMUManagerǁ_apply_spool_data__mutmut_29, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_30': xǁAMUManagerǁ_apply_spool_data__mutmut_30, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_31': xǁAMUManagerǁ_apply_spool_data__mutmut_31, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_32': xǁAMUManagerǁ_apply_spool_data__mutmut_32, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_33': xǁAMUManagerǁ_apply_spool_data__mutmut_33, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_34': xǁAMUManagerǁ_apply_spool_data__mutmut_34, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_35': xǁAMUManagerǁ_apply_spool_data__mutmut_35, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_36': xǁAMUManagerǁ_apply_spool_data__mutmut_36, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_37': xǁAMUManagerǁ_apply_spool_data__mutmut_37, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_38': xǁAMUManagerǁ_apply_spool_data__mutmut_38, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_39': xǁAMUManagerǁ_apply_spool_data__mutmut_39, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_40': xǁAMUManagerǁ_apply_spool_data__mutmut_40, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_41': xǁAMUManagerǁ_apply_spool_data__mutmut_41, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_42': xǁAMUManagerǁ_apply_spool_data__mutmut_42, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_43': xǁAMUManagerǁ_apply_spool_data__mutmut_43, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_44': xǁAMUManagerǁ_apply_spool_data__mutmut_44, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_45': xǁAMUManagerǁ_apply_spool_data__mutmut_45, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_46': xǁAMUManagerǁ_apply_spool_data__mutmut_46, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_47': xǁAMUManagerǁ_apply_spool_data__mutmut_47, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_48': xǁAMUManagerǁ_apply_spool_data__mutmut_48, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_49': xǁAMUManagerǁ_apply_spool_data__mutmut_49, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_50': xǁAMUManagerǁ_apply_spool_data__mutmut_50, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_51': xǁAMUManagerǁ_apply_spool_data__mutmut_51, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_52': xǁAMUManagerǁ_apply_spool_data__mutmut_52, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_53': xǁAMUManagerǁ_apply_spool_data__mutmut_53, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_54': xǁAMUManagerǁ_apply_spool_data__mutmut_54, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_55': xǁAMUManagerǁ_apply_spool_data__mutmut_55, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_56': xǁAMUManagerǁ_apply_spool_data__mutmut_56, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_57': xǁAMUManagerǁ_apply_spool_data__mutmut_57, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_58': xǁAMUManagerǁ_apply_spool_data__mutmut_58, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_59': xǁAMUManagerǁ_apply_spool_data__mutmut_59, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_60': xǁAMUManagerǁ_apply_spool_data__mutmut_60, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_61': xǁAMUManagerǁ_apply_spool_data__mutmut_61, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_62': xǁAMUManagerǁ_apply_spool_data__mutmut_62, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_63': xǁAMUManagerǁ_apply_spool_data__mutmut_63, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_64': xǁAMUManagerǁ_apply_spool_data__mutmut_64, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_65': xǁAMUManagerǁ_apply_spool_data__mutmut_65, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_66': xǁAMUManagerǁ_apply_spool_data__mutmut_66, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_67': xǁAMUManagerǁ_apply_spool_data__mutmut_67, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_68': xǁAMUManagerǁ_apply_spool_data__mutmut_68, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_69': xǁAMUManagerǁ_apply_spool_data__mutmut_69, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_70': xǁAMUManagerǁ_apply_spool_data__mutmut_70, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_71': xǁAMUManagerǁ_apply_spool_data__mutmut_71, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_72': xǁAMUManagerǁ_apply_spool_data__mutmut_72, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_73': xǁAMUManagerǁ_apply_spool_data__mutmut_73, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_74': xǁAMUManagerǁ_apply_spool_data__mutmut_74, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_75': xǁAMUManagerǁ_apply_spool_data__mutmut_75, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_76': xǁAMUManagerǁ_apply_spool_data__mutmut_76, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_77': xǁAMUManagerǁ_apply_spool_data__mutmut_77, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_78': xǁAMUManagerǁ_apply_spool_data__mutmut_78, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_79': xǁAMUManagerǁ_apply_spool_data__mutmut_79, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_80': xǁAMUManagerǁ_apply_spool_data__mutmut_80, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_81': xǁAMUManagerǁ_apply_spool_data__mutmut_81, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_82': xǁAMUManagerǁ_apply_spool_data__mutmut_82, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_83': xǁAMUManagerǁ_apply_spool_data__mutmut_83, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_84': xǁAMUManagerǁ_apply_spool_data__mutmut_84, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_85': xǁAMUManagerǁ_apply_spool_data__mutmut_85, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_86': xǁAMUManagerǁ_apply_spool_data__mutmut_86, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_87': xǁAMUManagerǁ_apply_spool_data__mutmut_87, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_88': xǁAMUManagerǁ_apply_spool_data__mutmut_88, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_89': xǁAMUManagerǁ_apply_spool_data__mutmut_89, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_90': xǁAMUManagerǁ_apply_spool_data__mutmut_90, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_91': xǁAMUManagerǁ_apply_spool_data__mutmut_91, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_92': xǁAMUManagerǁ_apply_spool_data__mutmut_92, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_93': xǁAMUManagerǁ_apply_spool_data__mutmut_93, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_94': xǁAMUManagerǁ_apply_spool_data__mutmut_94, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_95': xǁAMUManagerǁ_apply_spool_data__mutmut_95, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_96': xǁAMUManagerǁ_apply_spool_data__mutmut_96, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_97': xǁAMUManagerǁ_apply_spool_data__mutmut_97, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_98': xǁAMUManagerǁ_apply_spool_data__mutmut_98, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_99': xǁAMUManagerǁ_apply_spool_data__mutmut_99, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_100': xǁAMUManagerǁ_apply_spool_data__mutmut_100, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_101': xǁAMUManagerǁ_apply_spool_data__mutmut_101, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_102': xǁAMUManagerǁ_apply_spool_data__mutmut_102, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_103': xǁAMUManagerǁ_apply_spool_data__mutmut_103, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_104': xǁAMUManagerǁ_apply_spool_data__mutmut_104, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_105': xǁAMUManagerǁ_apply_spool_data__mutmut_105, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_106': xǁAMUManagerǁ_apply_spool_data__mutmut_106, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_107': xǁAMUManagerǁ_apply_spool_data__mutmut_107, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_108': xǁAMUManagerǁ_apply_spool_data__mutmut_108, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_109': xǁAMUManagerǁ_apply_spool_data__mutmut_109, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_110': xǁAMUManagerǁ_apply_spool_data__mutmut_110, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_111': xǁAMUManagerǁ_apply_spool_data__mutmut_111, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_112': xǁAMUManagerǁ_apply_spool_data__mutmut_112, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_113': xǁAMUManagerǁ_apply_spool_data__mutmut_113, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_114': xǁAMUManagerǁ_apply_spool_data__mutmut_114, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_115': xǁAMUManagerǁ_apply_spool_data__mutmut_115, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_116': xǁAMUManagerǁ_apply_spool_data__mutmut_116, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_117': xǁAMUManagerǁ_apply_spool_data__mutmut_117, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_118': xǁAMUManagerǁ_apply_spool_data__mutmut_118, 
        'xǁAMUManagerǁ_apply_spool_data__mutmut_119': xǁAMUManagerǁ_apply_spool_data__mutmut_119
    }
    xǁAMUManagerǁ_apply_spool_data__mutmut_orig.__name__ = 'xǁAMUManagerǁ_apply_spool_data'

    def _emit_speed_gcode(self, gate: int, remaining_weight: float) -> None:
        args = [gate, remaining_weight]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁ_emit_speed_gcode__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁ_emit_speed_gcode__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁ_emit_speed_gcode__mutmut_orig(self, gate: int, remaining_weight: float) -> None:
        """Emit MMU_GATE_MAP SPEED=x for the gate based on the spool weight profile."""
        if remaining_weight > HEAVY_SPOOL_THRESHOLD_G:
            self.run_gcode_signal.emit(
                f"MMU_GATE_MAP gate={gate} SPEED={_HEAVY_SPEED_PERCENT}"
            )

    def xǁAMUManagerǁ_emit_speed_gcode__mutmut_1(self, gate: int, remaining_weight: float) -> None:
        """Emit MMU_GATE_MAP SPEED=x for the gate based on the spool weight profile."""
        if remaining_weight >= HEAVY_SPOOL_THRESHOLD_G:
            self.run_gcode_signal.emit(
                f"MMU_GATE_MAP gate={gate} SPEED={_HEAVY_SPEED_PERCENT}"
            )

    def xǁAMUManagerǁ_emit_speed_gcode__mutmut_2(self, gate: int, remaining_weight: float) -> None:
        """Emit MMU_GATE_MAP SPEED=x for the gate based on the spool weight profile."""
        if remaining_weight > HEAVY_SPOOL_THRESHOLD_G:
            self.run_gcode_signal.emit(
                None
            )
    
    xǁAMUManagerǁ_emit_speed_gcode__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁ_emit_speed_gcode__mutmut_1': xǁAMUManagerǁ_emit_speed_gcode__mutmut_1, 
        'xǁAMUManagerǁ_emit_speed_gcode__mutmut_2': xǁAMUManagerǁ_emit_speed_gcode__mutmut_2
    }
    xǁAMUManagerǁ_emit_speed_gcode__mutmut_orig.__name__ = 'xǁAMUManagerǁ_emit_speed_gcode'

    def toggle_amu_system(self, activate: bool) -> None:
        args = [activate]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁtoggle_amu_system__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁtoggle_amu_system__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁtoggle_amu_system__mutmut_orig(self, activate: bool) -> None:
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

    def xǁAMUManagerǁtoggle_amu_system__mutmut_1(self, activate: bool) -> None:
        """Enable or disable the AMU system by commenting/uncommenting config includes.

        Emits:
            amu_toggled (bool): True if the operation succeeded, False otherwise.

        Args:
            activate (bool): True to enable the AMU, False to disable it.

        """
        result: bool = None
        self.amu_toggled.emit(result)
        if result:
            self.run_gcode_signal.emit("FIRMWARE_RESTART")

    def xǁAMUManagerǁtoggle_amu_system__mutmut_2(self, activate: bool) -> None:
        """Enable or disable the AMU system by commenting/uncommenting config includes.

        Emits:
            amu_toggled (bool): True if the operation succeeded, False otherwise.

        Args:
            activate (bool): True to enable the AMU, False to disable it.

        """
        result: bool = self._config_toggler.toggle(None)
        self.amu_toggled.emit(result)
        if result:
            self.run_gcode_signal.emit("FIRMWARE_RESTART")

    def xǁAMUManagerǁtoggle_amu_system__mutmut_3(self, activate: bool) -> None:
        """Enable or disable the AMU system by commenting/uncommenting config includes.

        Emits:
            amu_toggled (bool): True if the operation succeeded, False otherwise.

        Args:
            activate (bool): True to enable the AMU, False to disable it.

        """
        result: bool = self._config_toggler.toggle(activate)
        self.amu_toggled.emit(None)
        if result:
            self.run_gcode_signal.emit("FIRMWARE_RESTART")

    def xǁAMUManagerǁtoggle_amu_system__mutmut_4(self, activate: bool) -> None:
        """Enable or disable the AMU system by commenting/uncommenting config includes.

        Emits:
            amu_toggled (bool): True if the operation succeeded, False otherwise.

        Args:
            activate (bool): True to enable the AMU, False to disable it.

        """
        result: bool = self._config_toggler.toggle(activate)
        self.amu_toggled.emit(result)
        if result:
            self.run_gcode_signal.emit(None)

    def xǁAMUManagerǁtoggle_amu_system__mutmut_5(self, activate: bool) -> None:
        """Enable or disable the AMU system by commenting/uncommenting config includes.

        Emits:
            amu_toggled (bool): True if the operation succeeded, False otherwise.

        Args:
            activate (bool): True to enable the AMU, False to disable it.

        """
        result: bool = self._config_toggler.toggle(activate)
        self.amu_toggled.emit(result)
        if result:
            self.run_gcode_signal.emit("XXFIRMWARE_RESTARTXX")

    def xǁAMUManagerǁtoggle_amu_system__mutmut_6(self, activate: bool) -> None:
        """Enable or disable the AMU system by commenting/uncommenting config includes.

        Emits:
            amu_toggled (bool): True if the operation succeeded, False otherwise.

        Args:
            activate (bool): True to enable the AMU, False to disable it.

        """
        result: bool = self._config_toggler.toggle(activate)
        self.amu_toggled.emit(result)
        if result:
            self.run_gcode_signal.emit("firmware_restart")
    
    xǁAMUManagerǁtoggle_amu_system__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁtoggle_amu_system__mutmut_1': xǁAMUManagerǁtoggle_amu_system__mutmut_1, 
        'xǁAMUManagerǁtoggle_amu_system__mutmut_2': xǁAMUManagerǁtoggle_amu_system__mutmut_2, 
        'xǁAMUManagerǁtoggle_amu_system__mutmut_3': xǁAMUManagerǁtoggle_amu_system__mutmut_3, 
        'xǁAMUManagerǁtoggle_amu_system__mutmut_4': xǁAMUManagerǁtoggle_amu_system__mutmut_4, 
        'xǁAMUManagerǁtoggle_amu_system__mutmut_5': xǁAMUManagerǁtoggle_amu_system__mutmut_5, 
        'xǁAMUManagerǁtoggle_amu_system__mutmut_6': xǁAMUManagerǁtoggle_amu_system__mutmut_6
    }
    xǁAMUManagerǁtoggle_amu_system__mutmut_orig.__name__ = 'xǁAMUManagerǁtoggle_amu_system'

    def get_state(self) -> MMUState | None:
        """Returns current MMU state, None if not yet received.

        Returns:
            MMUState: Latest state received from Moonraker
            None: If no state has been received yet.

        """
        return self._mmu_state

    def get_pre_gate_sensors(self) -> dict[int, bool]:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁget_pre_gate_sensors__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁget_pre_gate_sensors__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁget_pre_gate_sensors__mutmut_orig(self) -> dict[int, bool]:
        return dict(self._pre_gate_sensors)

    def xǁAMUManagerǁget_pre_gate_sensors__mutmut_1(self) -> dict[int, bool]:
        return dict(None)
    
    xǁAMUManagerǁget_pre_gate_sensors__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁget_pre_gate_sensors__mutmut_1': xǁAMUManagerǁget_pre_gate_sensors__mutmut_1
    }
    xǁAMUManagerǁget_pre_gate_sensors__mutmut_orig.__name__ = 'xǁAMUManagerǁget_pre_gate_sensors'

    def is_amu_configured(self) -> bool:
        """Return True if AMU includes are uncommented in printer.cfg."""
        return self._config_toggler.is_configured()

    def is_amu_active(self) -> bool:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁis_amu_active__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁis_amu_active__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁis_amu_active__mutmut_orig(self) -> bool:
        """Returns whether AMU includes are currently uncommented in printer.cfg"""
        return self.is_amu_configured() and self._mmu_state is not None

    def xǁAMUManagerǁis_amu_active__mutmut_1(self) -> bool:
        """Returns whether AMU includes are currently uncommented in printer.cfg"""
        return self.is_amu_configured() or self._mmu_state is not None

    def xǁAMUManagerǁis_amu_active__mutmut_2(self) -> bool:
        """Returns whether AMU includes are currently uncommented in printer.cfg"""
        return self.is_amu_configured() and self._mmu_state is None
    
    xǁAMUManagerǁis_amu_active__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁis_amu_active__mutmut_1': xǁAMUManagerǁis_amu_active__mutmut_1, 
        'xǁAMUManagerǁis_amu_active__mutmut_2': xǁAMUManagerǁis_amu_active__mutmut_2
    }
    xǁAMUManagerǁis_amu_active__mutmut_orig.__name__ = 'xǁAMUManagerǁis_amu_active'

    def fetch_spool(self, gate: int, spool_id: int) -> None:
        args = [gate, spool_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁfetch_spool__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁfetch_spool__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁfetch_spool__mutmut_orig(self, gate: int, spool_id: int) -> None:
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

    def xǁAMUManagerǁfetch_spool__mutmut_1(self, gate: int, spool_id: int) -> None:
        """Request spool data from Moonraker via WebSocket.

        No-op if MMU state not received or spoolman_support is OFF.
        Emits spool_fetched(gate, data) on success; logs and emits nothing on error.
        """

        if self._mmu_state is not None:
            return
        if self._mmu_state.spoolman_support is SpoolmanSupport.OFF:
            return
        if spool_id == -1:
            return

        def _on_result(result: dict | None) -> None:
            if result is not None:
                self.spool_fetched.emit(gate, result)

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_2(self, gate: int, spool_id: int) -> None:
        """Request spool data from Moonraker via WebSocket.

        No-op if MMU state not received or spoolman_support is OFF.
        Emits spool_fetched(gate, data) on success; logs and emits nothing on error.
        """

        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support is not SpoolmanSupport.OFF:
            return
        if spool_id == -1:
            return

        def _on_result(result: dict | None) -> None:
            if result is not None:
                self.spool_fetched.emit(gate, result)

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_3(self, gate: int, spool_id: int) -> None:
        """Request spool data from Moonraker via WebSocket.

        No-op if MMU state not received or spoolman_support is OFF.
        Emits spool_fetched(gate, data) on success; logs and emits nothing on error.
        """

        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support is SpoolmanSupport.OFF:
            return
        if spool_id != -1:
            return

        def _on_result(result: dict | None) -> None:
            if result is not None:
                self.spool_fetched.emit(gate, result)

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_4(self, gate: int, spool_id: int) -> None:
        """Request spool data from Moonraker via WebSocket.

        No-op if MMU state not received or spoolman_support is OFF.
        Emits spool_fetched(gate, data) on success; logs and emits nothing on error.
        """

        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support is SpoolmanSupport.OFF:
            return
        if spool_id == +1:
            return

        def _on_result(result: dict | None) -> None:
            if result is not None:
                self.spool_fetched.emit(gate, result)

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_5(self, gate: int, spool_id: int) -> None:
        """Request spool data from Moonraker via WebSocket.

        No-op if MMU state not received or spoolman_support is OFF.
        Emits spool_fetched(gate, data) on success; logs and emits nothing on error.
        """

        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support is SpoolmanSupport.OFF:
            return
        if spool_id == -2:
            return

        def _on_result(result: dict | None) -> None:
            if result is not None:
                self.spool_fetched.emit(gate, result)

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_6(self, gate: int, spool_id: int) -> None:
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
            if result is None:
                self.spool_fetched.emit(gate, result)

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_7(self, gate: int, spool_id: int) -> None:
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
                self.spool_fetched.emit(None, result)

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_8(self, gate: int, spool_id: int) -> None:
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
                self.spool_fetched.emit(gate, None)

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_9(self, gate: int, spool_id: int) -> None:
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
                self.spool_fetched.emit(result)

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_10(self, gate: int, spool_id: int) -> None:
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
                self.spool_fetched.emit(gate, )

        self._ws.api.get_spool(spool_id, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_11(self, gate: int, spool_id: int) -> None:
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

        self._ws.api.get_spool(None, _on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_12(self, gate: int, spool_id: int) -> None:
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

        self._ws.api.get_spool(spool_id, None)

    def xǁAMUManagerǁfetch_spool__mutmut_13(self, gate: int, spool_id: int) -> None:
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

        self._ws.api.get_spool(_on_result)

    def xǁAMUManagerǁfetch_spool__mutmut_14(self, gate: int, spool_id: int) -> None:
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

        self._ws.api.get_spool(spool_id, )
    
    xǁAMUManagerǁfetch_spool__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁfetch_spool__mutmut_1': xǁAMUManagerǁfetch_spool__mutmut_1, 
        'xǁAMUManagerǁfetch_spool__mutmut_2': xǁAMUManagerǁfetch_spool__mutmut_2, 
        'xǁAMUManagerǁfetch_spool__mutmut_3': xǁAMUManagerǁfetch_spool__mutmut_3, 
        'xǁAMUManagerǁfetch_spool__mutmut_4': xǁAMUManagerǁfetch_spool__mutmut_4, 
        'xǁAMUManagerǁfetch_spool__mutmut_5': xǁAMUManagerǁfetch_spool__mutmut_5, 
        'xǁAMUManagerǁfetch_spool__mutmut_6': xǁAMUManagerǁfetch_spool__mutmut_6, 
        'xǁAMUManagerǁfetch_spool__mutmut_7': xǁAMUManagerǁfetch_spool__mutmut_7, 
        'xǁAMUManagerǁfetch_spool__mutmut_8': xǁAMUManagerǁfetch_spool__mutmut_8, 
        'xǁAMUManagerǁfetch_spool__mutmut_9': xǁAMUManagerǁfetch_spool__mutmut_9, 
        'xǁAMUManagerǁfetch_spool__mutmut_10': xǁAMUManagerǁfetch_spool__mutmut_10, 
        'xǁAMUManagerǁfetch_spool__mutmut_11': xǁAMUManagerǁfetch_spool__mutmut_11, 
        'xǁAMUManagerǁfetch_spool__mutmut_12': xǁAMUManagerǁfetch_spool__mutmut_12, 
        'xǁAMUManagerǁfetch_spool__mutmut_13': xǁAMUManagerǁfetch_spool__mutmut_13, 
        'xǁAMUManagerǁfetch_spool__mutmut_14': xǁAMUManagerǁfetch_spool__mutmut_14
    }
    xǁAMUManagerǁfetch_spool__mutmut_orig.__name__ = 'xǁAMUManagerǁfetch_spool'

    def set_gate_info(
        self,
        gate: int,
        material: str,
        color: str,
        spool_id: int,
        filament_name: str = "",
        temperature: int | None = None,
    ) -> None:
        args = [gate, material, color, spool_id, filament_name, temperature]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁset_gate_info__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁset_gate_info__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁset_gate_info__mutmut_orig(
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

    def xǁAMUManagerǁset_gate_info__mutmut_1(
        self,
        gate: int,
        material: str,
        color: str,
        spool_id: int,
        filament_name: str = "XXXX",
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

    def xǁAMUManagerǁset_gate_info__mutmut_2(
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
        gcode = None
        if filament_name:
            gcode = f"MMU_GATE_MAP gate={gate} NAME={filament_name} MATERIAL={material} COLOR={color} SPOOLID={spool_id}"
        if temperature is not None:
            gcode += f" TEMP={temperature}"
        self.run_gcode_signal.emit(gcode)

    def xǁAMUManagerǁset_gate_info__mutmut_3(
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
            gcode = None
        if temperature is not None:
            gcode += f" TEMP={temperature}"
        self.run_gcode_signal.emit(gcode)

    def xǁAMUManagerǁset_gate_info__mutmut_4(
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
        if temperature is None:
            gcode += f" TEMP={temperature}"
        self.run_gcode_signal.emit(gcode)

    def xǁAMUManagerǁset_gate_info__mutmut_5(
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
            gcode = f" TEMP={temperature}"
        self.run_gcode_signal.emit(gcode)

    def xǁAMUManagerǁset_gate_info__mutmut_6(
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
            gcode -= f" TEMP={temperature}"
        self.run_gcode_signal.emit(gcode)

    def xǁAMUManagerǁset_gate_info__mutmut_7(
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
        self.run_gcode_signal.emit(None)
    
    xǁAMUManagerǁset_gate_info__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁset_gate_info__mutmut_1': xǁAMUManagerǁset_gate_info__mutmut_1, 
        'xǁAMUManagerǁset_gate_info__mutmut_2': xǁAMUManagerǁset_gate_info__mutmut_2, 
        'xǁAMUManagerǁset_gate_info__mutmut_3': xǁAMUManagerǁset_gate_info__mutmut_3, 
        'xǁAMUManagerǁset_gate_info__mutmut_4': xǁAMUManagerǁset_gate_info__mutmut_4, 
        'xǁAMUManagerǁset_gate_info__mutmut_5': xǁAMUManagerǁset_gate_info__mutmut_5, 
        'xǁAMUManagerǁset_gate_info__mutmut_6': xǁAMUManagerǁset_gate_info__mutmut_6, 
        'xǁAMUManagerǁset_gate_info__mutmut_7': xǁAMUManagerǁset_gate_info__mutmut_7
    }
    xǁAMUManagerǁset_gate_info__mutmut_orig.__name__ = 'xǁAMUManagerǁset_gate_info'

    def set_gate_material(self, gate: int, material: str) -> None:
        args = [gate, material]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁset_gate_material__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁset_gate_material__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁset_gate_material__mutmut_orig(self, gate: int, material: str) -> None:
        """Set the `material` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            material (str): Filament material name, e.g. ``"PLA"``.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} MATERIAL={material}")

    def xǁAMUManagerǁset_gate_material__mutmut_1(self, gate: int, material: str) -> None:
        """Set the `material` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            material (str): Filament material name, e.g. ``"PLA"``.
        """
        self.run_gcode_signal.emit(None)
    
    xǁAMUManagerǁset_gate_material__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁset_gate_material__mutmut_1': xǁAMUManagerǁset_gate_material__mutmut_1
    }
    xǁAMUManagerǁset_gate_material__mutmut_orig.__name__ = 'xǁAMUManagerǁset_gate_material'

    def set_gate_temp(self, gate: int, temp: int):
        args = [gate, temp]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁset_gate_temp__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁset_gate_temp__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁset_gate_temp__mutmut_orig(self, gate: int, temp: int):
        """Set the `temperature` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            temp (int): Filament temperature, e.g. ``"220"``.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} TEMP={temp}")

    def xǁAMUManagerǁset_gate_temp__mutmut_1(self, gate: int, temp: int):
        """Set the `temperature` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            temp (int): Filament temperature, e.g. ``"220"``.
        """
        self.run_gcode_signal.emit(None)
    
    xǁAMUManagerǁset_gate_temp__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁset_gate_temp__mutmut_1': xǁAMUManagerǁset_gate_temp__mutmut_1
    }
    xǁAMUManagerǁset_gate_temp__mutmut_orig.__name__ = 'xǁAMUManagerǁset_gate_temp'

    def set_gate_color(self, gate: int, color: str) -> None:
        args = [gate, color]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁset_gate_color__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁset_gate_color__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁset_gate_color__mutmut_orig(self, gate: int, color: str) -> None:
        """Set the `color` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            color (str): Filament color, e.g. ``"ff56e0"``.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} COLOR={color}")

    def xǁAMUManagerǁset_gate_color__mutmut_1(self, gate: int, color: str) -> None:
        """Set the `color` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            color (str): Filament color, e.g. ``"ff56e0"``.
        """
        self.run_gcode_signal.emit(None)
    
    xǁAMUManagerǁset_gate_color__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁset_gate_color__mutmut_1': xǁAMUManagerǁset_gate_color__mutmut_1
    }
    xǁAMUManagerǁset_gate_color__mutmut_orig.__name__ = 'xǁAMUManagerǁset_gate_color'

    def set_gate_spool(self, gate: int, spool_id: int) -> None:
        args = [gate, spool_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁset_gate_spool__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁset_gate_spool__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁset_gate_spool__mutmut_orig(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} SPOOLID={spool_id}")
        if spool_id != -1:
            self.fetch_spool(gate, spool_id)

    def xǁAMUManagerǁset_gate_spool__mutmut_1(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(None)
        if spool_id != -1:
            self.fetch_spool(gate, spool_id)

    def xǁAMUManagerǁset_gate_spool__mutmut_2(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} SPOOLID={spool_id}")
        if spool_id == -1:
            self.fetch_spool(gate, spool_id)

    def xǁAMUManagerǁset_gate_spool__mutmut_3(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} SPOOLID={spool_id}")
        if spool_id != +1:
            self.fetch_spool(gate, spool_id)

    def xǁAMUManagerǁset_gate_spool__mutmut_4(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} SPOOLID={spool_id}")
        if spool_id != -2:
            self.fetch_spool(gate, spool_id)

    def xǁAMUManagerǁset_gate_spool__mutmut_5(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} SPOOLID={spool_id}")
        if spool_id != -1:
            self.fetch_spool(None, spool_id)

    def xǁAMUManagerǁset_gate_spool__mutmut_6(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} SPOOLID={spool_id}")
        if spool_id != -1:
            self.fetch_spool(gate, None)

    def xǁAMUManagerǁset_gate_spool__mutmut_7(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} SPOOLID={spool_id}")
        if spool_id != -1:
            self.fetch_spool(spool_id)

    def xǁAMUManagerǁset_gate_spool__mutmut_8(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """
        self.run_gcode_signal.emit(f"MMU_GATE_MAP gate={gate} SPOOLID={spool_id}")
        if spool_id != -1:
            self.fetch_spool(gate, )
    
    xǁAMUManagerǁset_gate_spool__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁset_gate_spool__mutmut_1': xǁAMUManagerǁset_gate_spool__mutmut_1, 
        'xǁAMUManagerǁset_gate_spool__mutmut_2': xǁAMUManagerǁset_gate_spool__mutmut_2, 
        'xǁAMUManagerǁset_gate_spool__mutmut_3': xǁAMUManagerǁset_gate_spool__mutmut_3, 
        'xǁAMUManagerǁset_gate_spool__mutmut_4': xǁAMUManagerǁset_gate_spool__mutmut_4, 
        'xǁAMUManagerǁset_gate_spool__mutmut_5': xǁAMUManagerǁset_gate_spool__mutmut_5, 
        'xǁAMUManagerǁset_gate_spool__mutmut_6': xǁAMUManagerǁset_gate_spool__mutmut_6, 
        'xǁAMUManagerǁset_gate_spool__mutmut_7': xǁAMUManagerǁset_gate_spool__mutmut_7, 
        'xǁAMUManagerǁset_gate_spool__mutmut_8': xǁAMUManagerǁset_gate_spool__mutmut_8
    }
    xǁAMUManagerǁset_gate_spool__mutmut_orig.__name__ = 'xǁAMUManagerǁset_gate_spool'

    def update_spool_weight(self, gate: int, used_weight: float) -> None:
        args = [gate, used_weight]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁupdate_spool_weight__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁupdate_spool_weight__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁupdate_spool_weight__mutmut_orig(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_1(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is not None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_2(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support not in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_3(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate > len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_4(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning(None, gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_5(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", None)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_6(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning(gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_7(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", )
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_8(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("XXupdate_spool_weight: gate %d out of rangeXX", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_9(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("UPDATE_SPOOL_WEIGHT: GATE %D OUT OF RANGE", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_10(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = None
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_11(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id != -1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_12(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == +1:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_13(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -2:
            return
        self._ws.api.update_spool(spool_id, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_14(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(None, {"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_15(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, None)

    def xǁAMUManagerǁupdate_spool_weight__mutmut_16(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool({"used_weight": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_17(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, )

    def xǁAMUManagerǁupdate_spool_weight__mutmut_18(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"XXused_weightXX": used_weight})

    def xǁAMUManagerǁupdate_spool_weight__mutmut_19(self, gate: int, used_weight: float) -> None:
        """Push updated used_weight to Spoolman for the spool at `gate`.

        No-op if MMU state not received, spoolman is off or read-only, gate is
        out of range, of the gate has no spool assigned.
        """
        if self._mmu_state is None:
            return
        if self._mmu_state.spoolman_support in (
            SpoolmanSupport.OFF,
            SpoolmanSupport.READONLY,
        ):
            return
        if gate >= len(self._mmu_state.gates):
            logger.warning("update_spool_weight: gate %d out of range", gate)
            return
        spool_id = self._mmu_state.gates[gate].spool_id
        if spool_id == -1:
            return
        self._ws.api.update_spool(spool_id, {"USED_WEIGHT": used_weight})
    
    xǁAMUManagerǁupdate_spool_weight__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁupdate_spool_weight__mutmut_1': xǁAMUManagerǁupdate_spool_weight__mutmut_1, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_2': xǁAMUManagerǁupdate_spool_weight__mutmut_2, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_3': xǁAMUManagerǁupdate_spool_weight__mutmut_3, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_4': xǁAMUManagerǁupdate_spool_weight__mutmut_4, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_5': xǁAMUManagerǁupdate_spool_weight__mutmut_5, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_6': xǁAMUManagerǁupdate_spool_weight__mutmut_6, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_7': xǁAMUManagerǁupdate_spool_weight__mutmut_7, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_8': xǁAMUManagerǁupdate_spool_weight__mutmut_8, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_9': xǁAMUManagerǁupdate_spool_weight__mutmut_9, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_10': xǁAMUManagerǁupdate_spool_weight__mutmut_10, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_11': xǁAMUManagerǁupdate_spool_weight__mutmut_11, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_12': xǁAMUManagerǁupdate_spool_weight__mutmut_12, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_13': xǁAMUManagerǁupdate_spool_weight__mutmut_13, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_14': xǁAMUManagerǁupdate_spool_weight__mutmut_14, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_15': xǁAMUManagerǁupdate_spool_weight__mutmut_15, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_16': xǁAMUManagerǁupdate_spool_weight__mutmut_16, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_17': xǁAMUManagerǁupdate_spool_weight__mutmut_17, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_18': xǁAMUManagerǁupdate_spool_weight__mutmut_18, 
        'xǁAMUManagerǁupdate_spool_weight__mutmut_19': xǁAMUManagerǁupdate_spool_weight__mutmut_19
    }
    xǁAMUManagerǁupdate_spool_weight__mutmut_orig.__name__ = 'xǁAMUManagerǁupdate_spool_weight'

    def home_mmu(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁhome_mmu__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁhome_mmu__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁhome_mmu__mutmut_orig(self) -> None:
        """Home the MMU selector by sending MMU_HOME."""
        self.run_gcode_signal.emit("MMU_HOME")

    def xǁAMUManagerǁhome_mmu__mutmut_1(self) -> None:
        """Home the MMU selector by sending MMU_HOME."""
        self.run_gcode_signal.emit(None)

    def xǁAMUManagerǁhome_mmu__mutmut_2(self) -> None:
        """Home the MMU selector by sending MMU_HOME."""
        self.run_gcode_signal.emit("XXMMU_HOMEXX")

    def xǁAMUManagerǁhome_mmu__mutmut_3(self) -> None:
        """Home the MMU selector by sending MMU_HOME."""
        self.run_gcode_signal.emit("mmu_home")
    
    xǁAMUManagerǁhome_mmu__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁhome_mmu__mutmut_1': xǁAMUManagerǁhome_mmu__mutmut_1, 
        'xǁAMUManagerǁhome_mmu__mutmut_2': xǁAMUManagerǁhome_mmu__mutmut_2, 
        'xǁAMUManagerǁhome_mmu__mutmut_3': xǁAMUManagerǁhome_mmu__mutmut_3
    }
    xǁAMUManagerǁhome_mmu__mutmut_orig.__name__ = 'xǁAMUManagerǁhome_mmu'

    def reset_mmu(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁreset_mmu__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁreset_mmu__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁreset_mmu__mutmut_orig(self) -> None:
        """Reset the MMU and clear any pause or error state by sending MMU_RESET."""
        self.run_gcode_signal.emit("MMU_RESET")

    def xǁAMUManagerǁreset_mmu__mutmut_1(self) -> None:
        """Reset the MMU and clear any pause or error state by sending MMU_RESET."""
        self.run_gcode_signal.emit(None)

    def xǁAMUManagerǁreset_mmu__mutmut_2(self) -> None:
        """Reset the MMU and clear any pause or error state by sending MMU_RESET."""
        self.run_gcode_signal.emit("XXMMU_RESETXX")

    def xǁAMUManagerǁreset_mmu__mutmut_3(self) -> None:
        """Reset the MMU and clear any pause or error state by sending MMU_RESET."""
        self.run_gcode_signal.emit("mmu_reset")
    
    xǁAMUManagerǁreset_mmu__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁreset_mmu__mutmut_1': xǁAMUManagerǁreset_mmu__mutmut_1, 
        'xǁAMUManagerǁreset_mmu__mutmut_2': xǁAMUManagerǁreset_mmu__mutmut_2, 
        'xǁAMUManagerǁreset_mmu__mutmut_3': xǁAMUManagerǁreset_mmu__mutmut_3
    }
    xǁAMUManagerǁreset_mmu__mutmut_orig.__name__ = 'xǁAMUManagerǁreset_mmu'

    def load_gate(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁload_gate__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁload_gate__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁload_gate__mutmut_orig(self) -> None:
        """Load filament from the specified gate by sending MMU_LOAD"""
        self.run_gcode_signal.emit("MMU_LOAD")

    def xǁAMUManagerǁload_gate__mutmut_1(self) -> None:
        """Load filament from the specified gate by sending MMU_LOAD"""
        self.run_gcode_signal.emit(None)

    def xǁAMUManagerǁload_gate__mutmut_2(self) -> None:
        """Load filament from the specified gate by sending MMU_LOAD"""
        self.run_gcode_signal.emit("XXMMU_LOADXX")

    def xǁAMUManagerǁload_gate__mutmut_3(self) -> None:
        """Load filament from the specified gate by sending MMU_LOAD"""
        self.run_gcode_signal.emit("mmu_load")
    
    xǁAMUManagerǁload_gate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁload_gate__mutmut_1': xǁAMUManagerǁload_gate__mutmut_1, 
        'xǁAMUManagerǁload_gate__mutmut_2': xǁAMUManagerǁload_gate__mutmut_2, 
        'xǁAMUManagerǁload_gate__mutmut_3': xǁAMUManagerǁload_gate__mutmut_3
    }
    xǁAMUManagerǁload_gate__mutmut_orig.__name__ = 'xǁAMUManagerǁload_gate'

    def unload(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁunload__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁunload__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁunload__mutmut_orig(self) -> None:
        """Unload the currently loaded filament by sending MMU_UNLOAD."""
        self.run_gcode_signal.emit("MMU_UNLOAD")

    def xǁAMUManagerǁunload__mutmut_1(self) -> None:
        """Unload the currently loaded filament by sending MMU_UNLOAD."""
        self.run_gcode_signal.emit(None)

    def xǁAMUManagerǁunload__mutmut_2(self) -> None:
        """Unload the currently loaded filament by sending MMU_UNLOAD."""
        self.run_gcode_signal.emit("XXMMU_UNLOADXX")

    def xǁAMUManagerǁunload__mutmut_3(self) -> None:
        """Unload the currently loaded filament by sending MMU_UNLOAD."""
        self.run_gcode_signal.emit("mmu_unload")
    
    xǁAMUManagerǁunload__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁunload__mutmut_1': xǁAMUManagerǁunload__mutmut_1, 
        'xǁAMUManagerǁunload__mutmut_2': xǁAMUManagerǁunload__mutmut_2, 
        'xǁAMUManagerǁunload__mutmut_3': xǁAMUManagerǁunload__mutmut_3
    }
    xǁAMUManagerǁunload__mutmut_orig.__name__ = 'xǁAMUManagerǁunload'

    def select_gate(self, gate: int) -> None:
        args = [gate]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁselect_gate__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁselect_gate__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁselect_gate__mutmut_orig(self, gate: int) -> None:
        """select the specified tool by sending MMU_SELECT

        Args:
            gate (int): gate index to select (0-based)
        """
        self.run_gcode_signal.emit(f"MMU_SELECT GATE={gate}")

    def xǁAMUManagerǁselect_gate__mutmut_1(self, gate: int) -> None:
        """select the specified tool by sending MMU_SELECT

        Args:
            gate (int): gate index to select (0-based)
        """
        self.run_gcode_signal.emit(None)
    
    xǁAMUManagerǁselect_gate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁselect_gate__mutmut_1': xǁAMUManagerǁselect_gate__mutmut_1
    }
    xǁAMUManagerǁselect_gate__mutmut_orig.__name__ = 'xǁAMUManagerǁselect_gate'

    def eject_gate(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁeject_gate__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁeject_gate__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁeject_gate__mutmut_orig(self) -> None:
        """Fully eject filament from gate, releasing from MMU gear."""
        self.run_gcode_signal.emit("MMU_EJECT")

    def xǁAMUManagerǁeject_gate__mutmut_1(self) -> None:
        """Fully eject filament from gate, releasing from MMU gear."""
        self.run_gcode_signal.emit(None)

    def xǁAMUManagerǁeject_gate__mutmut_2(self) -> None:
        """Fully eject filament from gate, releasing from MMU gear."""
        self.run_gcode_signal.emit("XXMMU_EJECTXX")

    def xǁAMUManagerǁeject_gate__mutmut_3(self) -> None:
        """Fully eject filament from gate, releasing from MMU gear."""
        self.run_gcode_signal.emit("mmu_eject")
    
    xǁAMUManagerǁeject_gate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁeject_gate__mutmut_1': xǁAMUManagerǁeject_gate__mutmut_1, 
        'xǁAMUManagerǁeject_gate__mutmut_2': xǁAMUManagerǁeject_gate__mutmut_2, 
        'xǁAMUManagerǁeject_gate__mutmut_3': xǁAMUManagerǁeject_gate__mutmut_3
    }
    xǁAMUManagerǁeject_gate__mutmut_orig.__name__ = 'xǁAMUManagerǁeject_gate'

    def check_gate(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁcheck_gate__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁcheck_gate__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁcheck_gate__mutmut_orig(self) -> None:
        """Check the current gate for filament presence by sending MMU_CHECK_GATE."""
        self.run_gcode_signal.emit("MMU_CHECK_GATE")

    def xǁAMUManagerǁcheck_gate__mutmut_1(self) -> None:
        """Check the current gate for filament presence by sending MMU_CHECK_GATE."""
        self.run_gcode_signal.emit(None)

    def xǁAMUManagerǁcheck_gate__mutmut_2(self) -> None:
        """Check the current gate for filament presence by sending MMU_CHECK_GATE."""
        self.run_gcode_signal.emit("XXMMU_CHECK_GATEXX")

    def xǁAMUManagerǁcheck_gate__mutmut_3(self) -> None:
        """Check the current gate for filament presence by sending MMU_CHECK_GATE."""
        self.run_gcode_signal.emit("mmu_check_gate")
    
    xǁAMUManagerǁcheck_gate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁcheck_gate__mutmut_1': xǁAMUManagerǁcheck_gate__mutmut_1, 
        'xǁAMUManagerǁcheck_gate__mutmut_2': xǁAMUManagerǁcheck_gate__mutmut_2, 
        'xǁAMUManagerǁcheck_gate__mutmut_3': xǁAMUManagerǁcheck_gate__mutmut_3
    }
    xǁAMUManagerǁcheck_gate__mutmut_orig.__name__ = 'xǁAMUManagerǁcheck_gate'

    def eject_all_gates(self, num_gates: int) -> None:
        args = [num_gates]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁeject_all_gates__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁeject_all_gates__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁeject_all_gates__mutmut_orig(self, num_gates: int) -> None:
        """Fully eject filament from all gates sequentially

        Args:
           num_gates: Total number of gates(from MMUState.num_gates)
        """
        cmd: str = "\n".join(f"MMU_EJECT GATE={i}" for i in range(num_gates))
        self.run_gcode_signal.emit(cmd)

    def xǁAMUManagerǁeject_all_gates__mutmut_1(self, num_gates: int) -> None:
        """Fully eject filament from all gates sequentially

        Args:
           num_gates: Total number of gates(from MMUState.num_gates)
        """
        cmd: str = None
        self.run_gcode_signal.emit(cmd)

    def xǁAMUManagerǁeject_all_gates__mutmut_2(self, num_gates: int) -> None:
        """Fully eject filament from all gates sequentially

        Args:
           num_gates: Total number of gates(from MMUState.num_gates)
        """
        cmd: str = "\n".join(None)
        self.run_gcode_signal.emit(cmd)

    def xǁAMUManagerǁeject_all_gates__mutmut_3(self, num_gates: int) -> None:
        """Fully eject filament from all gates sequentially

        Args:
           num_gates: Total number of gates(from MMUState.num_gates)
        """
        cmd: str = "XX\nXX".join(f"MMU_EJECT GATE={i}" for i in range(num_gates))
        self.run_gcode_signal.emit(cmd)

    def xǁAMUManagerǁeject_all_gates__mutmut_4(self, num_gates: int) -> None:
        """Fully eject filament from all gates sequentially

        Args:
           num_gates: Total number of gates(from MMUState.num_gates)
        """
        cmd: str = "\n".join(f"MMU_EJECT GATE={i}" for i in range(None))
        self.run_gcode_signal.emit(cmd)

    def xǁAMUManagerǁeject_all_gates__mutmut_5(self, num_gates: int) -> None:
        """Fully eject filament from all gates sequentially

        Args:
           num_gates: Total number of gates(from MMUState.num_gates)
        """
        cmd: str = "\n".join(f"MMU_EJECT GATE={i}" for i in range(num_gates))
        self.run_gcode_signal.emit(None)
    
    xǁAMUManagerǁeject_all_gates__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁeject_all_gates__mutmut_1': xǁAMUManagerǁeject_all_gates__mutmut_1, 
        'xǁAMUManagerǁeject_all_gates__mutmut_2': xǁAMUManagerǁeject_all_gates__mutmut_2, 
        'xǁAMUManagerǁeject_all_gates__mutmut_3': xǁAMUManagerǁeject_all_gates__mutmut_3, 
        'xǁAMUManagerǁeject_all_gates__mutmut_4': xǁAMUManagerǁeject_all_gates__mutmut_4, 
        'xǁAMUManagerǁeject_all_gates__mutmut_5': xǁAMUManagerǁeject_all_gates__mutmut_5
    }
    xǁAMUManagerǁeject_all_gates__mutmut_orig.__name__ = 'xǁAMUManagerǁeject_all_gates'

    def change_tool(self, tool: int) -> None:
        args = [tool]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁchange_tool__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁchange_tool__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁchange_tool__mutmut_orig(self, tool: int) -> None:
        """Select a tool, triggering a filament change if needed.

        Args:
            tool (int): Tool index to select (0-based).
        """
        self.run_gcode_signal.emit(f"MMU_CHANGE_TOOL TOOL={tool}")

    def xǁAMUManagerǁchange_tool__mutmut_1(self, tool: int) -> None:
        """Select a tool, triggering a filament change if needed.

        Args:
            tool (int): Tool index to select (0-based).
        """
        self.run_gcode_signal.emit(None)
    
    xǁAMUManagerǁchange_tool__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁchange_tool__mutmut_1': xǁAMUManagerǁchange_tool__mutmut_1
    }
    xǁAMUManagerǁchange_tool__mutmut_orig.__name__ = 'xǁAMUManagerǁchange_tool'

    def update_mmu_state(self, data: dict, name: str = "") -> None:
        args = [data, name]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁupdate_mmu_state__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁupdate_mmu_state__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁupdate_mmu_state__mutmut_orig(self, data: dict, name: str = "") -> None:
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

    def xǁAMUManagerǁupdate_mmu_state__mutmut_1(self, data: dict, name: str = "XXXX") -> None:
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

    def xǁAMUManagerǁupdate_mmu_state__mutmut_2(self, data: dict, name: str = "") -> None:
        """Receive an MMU status dict from Moonraker and update internal state.

        Called with either a full status response (on connect) or a diff
        (from notify_status_update). Builds or updates the MMUState and
        emits mmu_state_changed.

        Args:
            data: Raw MMU status or diff dict from Moonraker.
            name: Moonraker object name suffix (always empty for ``mmu``).
        """
        if self._mmu_state is not None:
            self._mmu_state = MMUState.from_status(data)
        else:
            self._mmu_state = self._mmu_state.apply_diff(data)
        self.mmu_state_changed.emit(self._mmu_state)

    def xǁAMUManagerǁupdate_mmu_state__mutmut_3(self, data: dict, name: str = "") -> None:
        """Receive an MMU status dict from Moonraker and update internal state.

        Called with either a full status response (on connect) or a diff
        (from notify_status_update). Builds or updates the MMUState and
        emits mmu_state_changed.

        Args:
            data: Raw MMU status or diff dict from Moonraker.
            name: Moonraker object name suffix (always empty for ``mmu``).
        """
        if self._mmu_state is None:
            self._mmu_state = None
        else:
            self._mmu_state = self._mmu_state.apply_diff(data)
        self.mmu_state_changed.emit(self._mmu_state)

    def xǁAMUManagerǁupdate_mmu_state__mutmut_4(self, data: dict, name: str = "") -> None:
        """Receive an MMU status dict from Moonraker and update internal state.

        Called with either a full status response (on connect) or a diff
        (from notify_status_update). Builds or updates the MMUState and
        emits mmu_state_changed.

        Args:
            data: Raw MMU status or diff dict from Moonraker.
            name: Moonraker object name suffix (always empty for ``mmu``).
        """
        if self._mmu_state is None:
            self._mmu_state = MMUState.from_status(None)
        else:
            self._mmu_state = self._mmu_state.apply_diff(data)
        self.mmu_state_changed.emit(self._mmu_state)

    def xǁAMUManagerǁupdate_mmu_state__mutmut_5(self, data: dict, name: str = "") -> None:
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
            self._mmu_state = None
        self.mmu_state_changed.emit(self._mmu_state)

    def xǁAMUManagerǁupdate_mmu_state__mutmut_6(self, data: dict, name: str = "") -> None:
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
            self._mmu_state = self._mmu_state.apply_diff(None)
        self.mmu_state_changed.emit(self._mmu_state)

    def xǁAMUManagerǁupdate_mmu_state__mutmut_7(self, data: dict, name: str = "") -> None:
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
        self.mmu_state_changed.emit(None)
    
    xǁAMUManagerǁupdate_mmu_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁupdate_mmu_state__mutmut_1': xǁAMUManagerǁupdate_mmu_state__mutmut_1, 
        'xǁAMUManagerǁupdate_mmu_state__mutmut_2': xǁAMUManagerǁupdate_mmu_state__mutmut_2, 
        'xǁAMUManagerǁupdate_mmu_state__mutmut_3': xǁAMUManagerǁupdate_mmu_state__mutmut_3, 
        'xǁAMUManagerǁupdate_mmu_state__mutmut_4': xǁAMUManagerǁupdate_mmu_state__mutmut_4, 
        'xǁAMUManagerǁupdate_mmu_state__mutmut_5': xǁAMUManagerǁupdate_mmu_state__mutmut_5, 
        'xǁAMUManagerǁupdate_mmu_state__mutmut_6': xǁAMUManagerǁupdate_mmu_state__mutmut_6, 
        'xǁAMUManagerǁupdate_mmu_state__mutmut_7': xǁAMUManagerǁupdate_mmu_state__mutmut_7
    }
    xǁAMUManagerǁupdate_mmu_state__mutmut_orig.__name__ = 'xǁAMUManagerǁupdate_mmu_state'

    def on_object_updated(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        args = [object_type, object_name, values]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁon_object_updated__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁon_object_updated__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁon_object_updated__mutmut_orig(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_1(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type != "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_2(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "XXmmuXX":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_3(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "MMU":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_4(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(None)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_5(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type != "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_6(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "XXfilament_switch_sensorXX":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_7(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "FILAMENT_SWITCH_SENSOR":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_8(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(None, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_9(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, None)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_10(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_11(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, )
        elif object_type == "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_12(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type != "load_cell":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_13(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "XXload_cellXX":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_14(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "LOAD_CELL":
            self.on_load_cell_update(values, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_15(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(None, object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_16(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, None)

    def xǁAMUManagerǁon_object_updated__mutmut_17(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(object_name)

    def xǁAMUManagerǁon_object_updated__mutmut_18(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "load_cell":
            self.on_load_cell_update(values, )
    
    xǁAMUManagerǁon_object_updated__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁon_object_updated__mutmut_1': xǁAMUManagerǁon_object_updated__mutmut_1, 
        'xǁAMUManagerǁon_object_updated__mutmut_2': xǁAMUManagerǁon_object_updated__mutmut_2, 
        'xǁAMUManagerǁon_object_updated__mutmut_3': xǁAMUManagerǁon_object_updated__mutmut_3, 
        'xǁAMUManagerǁon_object_updated__mutmut_4': xǁAMUManagerǁon_object_updated__mutmut_4, 
        'xǁAMUManagerǁon_object_updated__mutmut_5': xǁAMUManagerǁon_object_updated__mutmut_5, 
        'xǁAMUManagerǁon_object_updated__mutmut_6': xǁAMUManagerǁon_object_updated__mutmut_6, 
        'xǁAMUManagerǁon_object_updated__mutmut_7': xǁAMUManagerǁon_object_updated__mutmut_7, 
        'xǁAMUManagerǁon_object_updated__mutmut_8': xǁAMUManagerǁon_object_updated__mutmut_8, 
        'xǁAMUManagerǁon_object_updated__mutmut_9': xǁAMUManagerǁon_object_updated__mutmut_9, 
        'xǁAMUManagerǁon_object_updated__mutmut_10': xǁAMUManagerǁon_object_updated__mutmut_10, 
        'xǁAMUManagerǁon_object_updated__mutmut_11': xǁAMUManagerǁon_object_updated__mutmut_11, 
        'xǁAMUManagerǁon_object_updated__mutmut_12': xǁAMUManagerǁon_object_updated__mutmut_12, 
        'xǁAMUManagerǁon_object_updated__mutmut_13': xǁAMUManagerǁon_object_updated__mutmut_13, 
        'xǁAMUManagerǁon_object_updated__mutmut_14': xǁAMUManagerǁon_object_updated__mutmut_14, 
        'xǁAMUManagerǁon_object_updated__mutmut_15': xǁAMUManagerǁon_object_updated__mutmut_15, 
        'xǁAMUManagerǁon_object_updated__mutmut_16': xǁAMUManagerǁon_object_updated__mutmut_16, 
        'xǁAMUManagerǁon_object_updated__mutmut_17': xǁAMUManagerǁon_object_updated__mutmut_17, 
        'xǁAMUManagerǁon_object_updated__mutmut_18': xǁAMUManagerǁon_object_updated__mutmut_18
    }
    xǁAMUManagerǁon_object_updated__mutmut_orig.__name__ = 'xǁAMUManagerǁon_object_updated'

    def on_pre_gate_update(self, values: dict, name: str) -> None:
        args = [values, name]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁon_pre_gate_update__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁon_pre_gate_update__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_orig(self, values: dict, name: str) -> None:
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

    def xǁAMUManagerǁon_pre_gate_update__mutmut_1(self, values: dict, name: str) -> None:
        if name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_2(self, values: dict, name: str) -> None:
        if not name.startswith(None):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_3(self, values: dict, name: str) -> None:
        if not name.startswith("XXmmu_pre_gate_XX"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_4(self, values: dict, name: str) -> None:
        if not name.startswith("MMU_PRE_GATE_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_5(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = None
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_6(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(None)
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_7(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix(None))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_8(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removesuffix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_9(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("XXmmu_pre_gate_XX"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_10(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("MMU_PRE_GATE_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_11(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error(None, name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_12(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", None)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_13(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error(name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_14(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", )
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_15(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("XXFailed to parse Pre-Gate: %sXX", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_16(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("failed to parse pre-gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_17(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("FAILED TO PARSE PRE-GATE: %S", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_18(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = None
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_19(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(None)
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_20(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get(None, False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_21(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", None))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_22(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get(False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_23(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", ))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_24(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("XXfilament_detectedXX", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_25(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("FILAMENT_DETECTED", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_26(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", True))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_27(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = None
        self.pre_gate_changed.emit(gate, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_28(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(None, detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_29(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, None)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_30(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(detected)

    def xǁAMUManagerǁon_pre_gate_update__mutmut_31(self, values: dict, name: str) -> None:
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, )
    
    xǁAMUManagerǁon_pre_gate_update__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁon_pre_gate_update__mutmut_1': xǁAMUManagerǁon_pre_gate_update__mutmut_1, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_2': xǁAMUManagerǁon_pre_gate_update__mutmut_2, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_3': xǁAMUManagerǁon_pre_gate_update__mutmut_3, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_4': xǁAMUManagerǁon_pre_gate_update__mutmut_4, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_5': xǁAMUManagerǁon_pre_gate_update__mutmut_5, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_6': xǁAMUManagerǁon_pre_gate_update__mutmut_6, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_7': xǁAMUManagerǁon_pre_gate_update__mutmut_7, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_8': xǁAMUManagerǁon_pre_gate_update__mutmut_8, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_9': xǁAMUManagerǁon_pre_gate_update__mutmut_9, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_10': xǁAMUManagerǁon_pre_gate_update__mutmut_10, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_11': xǁAMUManagerǁon_pre_gate_update__mutmut_11, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_12': xǁAMUManagerǁon_pre_gate_update__mutmut_12, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_13': xǁAMUManagerǁon_pre_gate_update__mutmut_13, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_14': xǁAMUManagerǁon_pre_gate_update__mutmut_14, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_15': xǁAMUManagerǁon_pre_gate_update__mutmut_15, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_16': xǁAMUManagerǁon_pre_gate_update__mutmut_16, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_17': xǁAMUManagerǁon_pre_gate_update__mutmut_17, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_18': xǁAMUManagerǁon_pre_gate_update__mutmut_18, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_19': xǁAMUManagerǁon_pre_gate_update__mutmut_19, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_20': xǁAMUManagerǁon_pre_gate_update__mutmut_20, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_21': xǁAMUManagerǁon_pre_gate_update__mutmut_21, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_22': xǁAMUManagerǁon_pre_gate_update__mutmut_22, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_23': xǁAMUManagerǁon_pre_gate_update__mutmut_23, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_24': xǁAMUManagerǁon_pre_gate_update__mutmut_24, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_25': xǁAMUManagerǁon_pre_gate_update__mutmut_25, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_26': xǁAMUManagerǁon_pre_gate_update__mutmut_26, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_27': xǁAMUManagerǁon_pre_gate_update__mutmut_27, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_28': xǁAMUManagerǁon_pre_gate_update__mutmut_28, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_29': xǁAMUManagerǁon_pre_gate_update__mutmut_29, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_30': xǁAMUManagerǁon_pre_gate_update__mutmut_30, 
        'xǁAMUManagerǁon_pre_gate_update__mutmut_31': xǁAMUManagerǁon_pre_gate_update__mutmut_31
    }
    xǁAMUManagerǁon_pre_gate_update__mutmut_orig.__name__ = 'xǁAMUManagerǁon_pre_gate_update'

    def on_load_cell_update(self, values: dict, name: str) -> None:
        args = [values, name]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁon_load_cell_update__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁon_load_cell_update__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁon_load_cell_update__mutmut_orig(self, values: dict, name: str) -> None:
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_1(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None and not name.startswith("load_cell_mmu_"):
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_2(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is not None or not name.startswith("load_cell_mmu_"):
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_3(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or name.startswith("load_cell_mmu_"):
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_4(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith(None):
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_5(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("XXload_cell_mmu_XX"):
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_6(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("LOAD_CELL_MMU_"):
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_7(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = None
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_8(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(None)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_9(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix(None))
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_10(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removesuffix("load_cell_mmu_"))
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_11(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("XXload_cell_mmu_XX"))
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_12(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("LOAD_CELL_MMU_"))
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_13(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error(None, name)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_14(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", None)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_15(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error(name)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_16(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", )
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_17(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("XXFailed parsing %s Load cellXX", name)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_18(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("failed parsing %s load cell", name)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_19(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("FAILED PARSING %S LOAD CELL", name)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_20(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", name)
            return

        weight = None
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_21(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", name)
            return

        weight = float(None)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_22(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", name)
            return

        weight = float(values.get("force") and 0)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_23(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", name)
            return

        weight = float(values.get(None) or 0)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_24(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", name)
            return

        weight = float(values.get("XXforceXX") or 0)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_25(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", name)
            return

        weight = float(values.get("FORCE") or 0)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_26(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", name)
            return

        weight = float(values.get("force") or 1)
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_27(self, values: dict, name: str) -> None:
        """Update gate weight from a Klipper load_cell sensor reading"""
        if self._mmu_state is None or not name.startswith("load_cell_mmu_"):
            return
        try:
            gate = int(name.removeprefix("load_cell_mmu_"))
        except ValueError:
            logger.error("Failed parsing %s Load cell", name)
            return

        weight = float(values.get("force") or 0)
        if gate > len(self._mmu_state.gates):
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

    def xǁAMUManagerǁon_load_cell_update__mutmut_28(self, values: dict, name: str) -> None:
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
                None,
                gate,
                len(self._mmu_state.gates),
            )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_29(self, values: dict, name: str) -> None:
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
                None,
                len(self._mmu_state.gates),
            )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_30(self, values: dict, name: str) -> None:
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
                None,
            )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_31(self, values: dict, name: str) -> None:
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
                gate,
                len(self._mmu_state.gates),
            )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_32(self, values: dict, name: str) -> None:
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
                len(self._mmu_state.gates),
            )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_33(self, values: dict, name: str) -> None:
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
                )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_34(self, values: dict, name: str) -> None:
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
                "XXGate index %d out of range (%d gates)XX",
                gate,
                len(self._mmu_state.gates),
            )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_35(self, values: dict, name: str) -> None:
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
                "gate index %d out of range (%d gates)",
                gate,
                len(self._mmu_state.gates),
            )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_36(self, values: dict, name: str) -> None:
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
                "GATE INDEX %D OUT OF RANGE (%D GATES)",
                gate,
                len(self._mmu_state.gates),
            )
            return
        gates = list(self._mmu_state.gates)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_37(self, values: dict, name: str) -> None:
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
        gates = None
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_38(self, values: dict, name: str) -> None:
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
        gates = list(None)
        gates[gate] = dataclasses.replace(gates[gate], weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_39(self, values: dict, name: str) -> None:
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
        gates[gate] = None
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_40(self, values: dict, name: str) -> None:
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
        gates[gate] = dataclasses.replace(None, weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_41(self, values: dict, name: str) -> None:
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
        gates[gate] = dataclasses.replace(gates[gate], weight_g=None)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_42(self, values: dict, name: str) -> None:
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
        gates[gate] = dataclasses.replace(weight_g=weight)
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_43(self, values: dict, name: str) -> None:
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
        gates[gate] = dataclasses.replace(gates[gate], )
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_44(self, values: dict, name: str) -> None:
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
        self._mmu_state = None
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_45(self, values: dict, name: str) -> None:
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
        self._mmu_state = dataclasses.replace(None, gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_46(self, values: dict, name: str) -> None:
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
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=None)
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_47(self, values: dict, name: str) -> None:
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
        self._mmu_state = dataclasses.replace(gates=tuple(gates))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_48(self, values: dict, name: str) -> None:
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
        self._mmu_state = dataclasses.replace(self._mmu_state, )
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_49(self, values: dict, name: str) -> None:
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
        self._mmu_state = dataclasses.replace(self._mmu_state, gates=tuple(None))
        self.gate_weight_updated.emit(gate, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_50(self, values: dict, name: str) -> None:
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
        self.gate_weight_updated.emit(None, weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_51(self, values: dict, name: str) -> None:
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
        self.gate_weight_updated.emit(gate, None)

    def xǁAMUManagerǁon_load_cell_update__mutmut_52(self, values: dict, name: str) -> None:
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
        self.gate_weight_updated.emit(weight)

    def xǁAMUManagerǁon_load_cell_update__mutmut_53(self, values: dict, name: str) -> None:
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
        self.gate_weight_updated.emit(gate, )
    
    xǁAMUManagerǁon_load_cell_update__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁon_load_cell_update__mutmut_1': xǁAMUManagerǁon_load_cell_update__mutmut_1, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_2': xǁAMUManagerǁon_load_cell_update__mutmut_2, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_3': xǁAMUManagerǁon_load_cell_update__mutmut_3, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_4': xǁAMUManagerǁon_load_cell_update__mutmut_4, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_5': xǁAMUManagerǁon_load_cell_update__mutmut_5, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_6': xǁAMUManagerǁon_load_cell_update__mutmut_6, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_7': xǁAMUManagerǁon_load_cell_update__mutmut_7, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_8': xǁAMUManagerǁon_load_cell_update__mutmut_8, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_9': xǁAMUManagerǁon_load_cell_update__mutmut_9, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_10': xǁAMUManagerǁon_load_cell_update__mutmut_10, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_11': xǁAMUManagerǁon_load_cell_update__mutmut_11, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_12': xǁAMUManagerǁon_load_cell_update__mutmut_12, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_13': xǁAMUManagerǁon_load_cell_update__mutmut_13, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_14': xǁAMUManagerǁon_load_cell_update__mutmut_14, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_15': xǁAMUManagerǁon_load_cell_update__mutmut_15, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_16': xǁAMUManagerǁon_load_cell_update__mutmut_16, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_17': xǁAMUManagerǁon_load_cell_update__mutmut_17, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_18': xǁAMUManagerǁon_load_cell_update__mutmut_18, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_19': xǁAMUManagerǁon_load_cell_update__mutmut_19, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_20': xǁAMUManagerǁon_load_cell_update__mutmut_20, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_21': xǁAMUManagerǁon_load_cell_update__mutmut_21, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_22': xǁAMUManagerǁon_load_cell_update__mutmut_22, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_23': xǁAMUManagerǁon_load_cell_update__mutmut_23, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_24': xǁAMUManagerǁon_load_cell_update__mutmut_24, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_25': xǁAMUManagerǁon_load_cell_update__mutmut_25, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_26': xǁAMUManagerǁon_load_cell_update__mutmut_26, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_27': xǁAMUManagerǁon_load_cell_update__mutmut_27, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_28': xǁAMUManagerǁon_load_cell_update__mutmut_28, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_29': xǁAMUManagerǁon_load_cell_update__mutmut_29, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_30': xǁAMUManagerǁon_load_cell_update__mutmut_30, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_31': xǁAMUManagerǁon_load_cell_update__mutmut_31, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_32': xǁAMUManagerǁon_load_cell_update__mutmut_32, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_33': xǁAMUManagerǁon_load_cell_update__mutmut_33, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_34': xǁAMUManagerǁon_load_cell_update__mutmut_34, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_35': xǁAMUManagerǁon_load_cell_update__mutmut_35, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_36': xǁAMUManagerǁon_load_cell_update__mutmut_36, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_37': xǁAMUManagerǁon_load_cell_update__mutmut_37, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_38': xǁAMUManagerǁon_load_cell_update__mutmut_38, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_39': xǁAMUManagerǁon_load_cell_update__mutmut_39, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_40': xǁAMUManagerǁon_load_cell_update__mutmut_40, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_41': xǁAMUManagerǁon_load_cell_update__mutmut_41, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_42': xǁAMUManagerǁon_load_cell_update__mutmut_42, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_43': xǁAMUManagerǁon_load_cell_update__mutmut_43, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_44': xǁAMUManagerǁon_load_cell_update__mutmut_44, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_45': xǁAMUManagerǁon_load_cell_update__mutmut_45, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_46': xǁAMUManagerǁon_load_cell_update__mutmut_46, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_47': xǁAMUManagerǁon_load_cell_update__mutmut_47, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_48': xǁAMUManagerǁon_load_cell_update__mutmut_48, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_49': xǁAMUManagerǁon_load_cell_update__mutmut_49, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_50': xǁAMUManagerǁon_load_cell_update__mutmut_50, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_51': xǁAMUManagerǁon_load_cell_update__mutmut_51, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_52': xǁAMUManagerǁon_load_cell_update__mutmut_52, 
        'xǁAMUManagerǁon_load_cell_update__mutmut_53': xǁAMUManagerǁon_load_cell_update__mutmut_53
    }
    xǁAMUManagerǁon_load_cell_update__mutmut_orig.__name__ = 'xǁAMUManagerǁon_load_cell_update'

    def on_klippy_state(self, state: str) -> None:
        args = [state]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁAMUManagerǁon_klippy_state__mutmut_orig'), object.__getattribute__(self, 'xǁAMUManagerǁon_klippy_state__mutmut_mutants'), args, kwargs, self)

    def xǁAMUManagerǁon_klippy_state__mutmut_orig(self, state: str) -> None:
        """React to changes in klippy states"""
        if state.lower() != "ready":
            self._mmu_state = None
            self._pre_gate_sensors = {}

    def xǁAMUManagerǁon_klippy_state__mutmut_1(self, state: str) -> None:
        """React to changes in klippy states"""
        if state.upper() != "ready":
            self._mmu_state = None
            self._pre_gate_sensors = {}

    def xǁAMUManagerǁon_klippy_state__mutmut_2(self, state: str) -> None:
        """React to changes in klippy states"""
        if state.lower() == "ready":
            self._mmu_state = None
            self._pre_gate_sensors = {}

    def xǁAMUManagerǁon_klippy_state__mutmut_3(self, state: str) -> None:
        """React to changes in klippy states"""
        if state.lower() != "XXreadyXX":
            self._mmu_state = None
            self._pre_gate_sensors = {}

    def xǁAMUManagerǁon_klippy_state__mutmut_4(self, state: str) -> None:
        """React to changes in klippy states"""
        if state.lower() != "READY":
            self._mmu_state = None
            self._pre_gate_sensors = {}

    def xǁAMUManagerǁon_klippy_state__mutmut_5(self, state: str) -> None:
        """React to changes in klippy states"""
        if state.lower() != "ready":
            self._mmu_state = ""
            self._pre_gate_sensors = {}

    def xǁAMUManagerǁon_klippy_state__mutmut_6(self, state: str) -> None:
        """React to changes in klippy states"""
        if state.lower() != "ready":
            self._mmu_state = None
            self._pre_gate_sensors = None
    
    xǁAMUManagerǁon_klippy_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁAMUManagerǁon_klippy_state__mutmut_1': xǁAMUManagerǁon_klippy_state__mutmut_1, 
        'xǁAMUManagerǁon_klippy_state__mutmut_2': xǁAMUManagerǁon_klippy_state__mutmut_2, 
        'xǁAMUManagerǁon_klippy_state__mutmut_3': xǁAMUManagerǁon_klippy_state__mutmut_3, 
        'xǁAMUManagerǁon_klippy_state__mutmut_4': xǁAMUManagerǁon_klippy_state__mutmut_4, 
        'xǁAMUManagerǁon_klippy_state__mutmut_5': xǁAMUManagerǁon_klippy_state__mutmut_5, 
        'xǁAMUManagerǁon_klippy_state__mutmut_6': xǁAMUManagerǁon_klippy_state__mutmut_6
    }
    xǁAMUManagerǁon_klippy_state__mutmut_orig.__name__ = 'xǁAMUManagerǁon_klippy_state'
