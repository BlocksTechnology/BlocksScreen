import logging
import re
import typing
from pathlib import Path

from PyQt6 import QtCore

from .models import MMUState

logger: logging.Logger = logging.getLogger(__name__)

CONFIG_PATH: Path = Path("~/printer_data/config/printer.cfg").expanduser()
AMU_FILES: list[str] = [
    "mmu/base/*.cfg",
    "mmu/optional/client_macros.cfg",
    "filament_manager.cfg",
]

AMU_PATTERNS: list[re.Pattern[str]] = [
    re.compile(rf"^(#?)(\[include {re.escape(f)}\])", re.MULTILINE) for f in AMU_FILES
]


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

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._amu_state = False
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}
        self.__setup_configfile()

    def __setup_configfile(self) -> None:
        """Sets up local configfile variable"""
        self._config_filename: Path | None = CONFIG_PATH
        if not self._config_filename.exists():
            logger.warning("Config file not found %s", self._config_filename)
            self._config_filename = None

    def _apply_patterns(self, state: bool) -> bool:
        """Method that comments/uncomments the AMU_FILES from the printer.cfg according with state value

        Args:
            state (bool): True: Uncomment, False: Comment

        Returns:
            bool: True: Success, False: Failed
        """
        if self._config_filename is None:
            logger.warning("_apply_patterns called but no config file available")
            return False

        if self._amu_state == state:
            return False

        replacement = r"\2"
        if not state:
            replacement = r"#\2"
        try:
            text: str = self._config_filename.read_text()
            for file in AMU_PATTERNS:
                text = file.sub(replacement, text)
            self._config_filename.write_text(text)
            self._amu_state = state
            return True
        except OSError as e:
            logger.error(
                "Failed to apply(state=%s) AMU System: could not read/write %s\n%s",
                state,
                self._config_filename,
                e,
            )
            return False

    def toggle_amu_system(self, activate: bool) -> None:
        """Enable or disable the AMU system by commenting/uncommenting config includes.

        Emits:
            amu_toggled (bool): True if the operation succeeded, False otherwise.

        Args:
            activate (bool): True to enable the AMU, False to disable it.

        """
        result: bool = self._apply_patterns(activate)
        self.amu_toggled.emit(result)

    def get_state(self) -> MMUState | None:
        """Returns current MMU state, None if not yet received.

        Returns:
            MMUState: Latest state received from Moonraker
            None: If no state has been received yet.

        """
        return self._mmu_state

    def get_pre_gate_sensors(self) -> dict[int, bool]:
        return dict(self._pre_gate_sensors)

    def is_amu_active(self) -> bool:
        """Returns whether AMU includes are currently uncommented in printer.cfg"""
        return self._amu_state

    def set_gate_info(
        self, gate: int, material: str, color: str, spool_id: int
    ) -> None:
        """Sets all gate attributes for a single MMU_GATE

        Args:
            gate (int): Gate index (0-based).
            material (str): Filament material name, e.g. ``"PLA"``.
            color (str): Filament color as hex string, e.g. ``"ff56e0"``.
            spool_id (int): Spoolman spool ID, or -1 if not tracked.
        """
        self.run_gcode_signal.emit(
            f"MMU_GATE_MAP gate={gate} MATERIAL={material} COLOR={color} SPOOLID={spool_id}"
        )

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
        """Fully eject filament from all gates sequentially(amu_manager.get_state().num_gates)

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

    def on_pre_gate_update(self, values: dict, name: str) -> None:
        if not name.startswith("Mmu Pre Gate "):
            return
        try:
            gate = int(name.removeprefix("Mmu Pre Gate "))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        detected = bool(values.get("filament_detected", False))
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

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

    def on_klippy_state(self, state: str) -> None:
        """React to changes in klippy states"""
        if state.lower() != "ready":
            self._mmu_state = None
