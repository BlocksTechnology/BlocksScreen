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

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._amu_state = False
        self._mmu_state: MMUState | None = None
        self.__setup_configfile()

    def __setup_configfile(self) -> None:
        """
        Sets up local configfile variable

        Raises:
            FileNotFoundError: File Not Found
        """
        self._config_filename = CONFIG_PATH
        if not self._config_filename.exists():
            raise FileNotFoundError(("Config file not found %s", self._config_filename))

    def _apply_patterns(self, state: bool) -> bool:
        """Method that comments/uncomments the AMU_FILES from the printer.cfg according with state value

        Args:
            state (bool): True: Uncomment, False: Comment

        Returns:
            bool: True: Success, False: Failed
        """
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
        ...

    def set_gate_material(self, gate: int, material: str) -> None:
        """Set the `material` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            material (str): Filament material name, e.g. ``"PLA"``.
        """

    def set_gate_color(self, gate: int, color: str) -> None:
        """Set the `color` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            color (str): Filament color, e.g. ``"ff56e0"``.
        """

    def set_gate_spool(self, gate: int, spool_id: int) -> None:
        """Set the `spool_id` at the gate `gate`

        Args:
            gate (int): Gate index (0-based).
            spool_id (int): Spoolman spool ID, or -1 to clear.
        """

    def home_mmu(self) -> None:
        """Home the MMU selector by sending MMU_HOME."""

    def reset_mmu(self) -> None:
        """Reset the MMU and clear any pause or error state by sending MMU_RESET."""

    def load_gate(self, gate: int) -> None:
        """Load filament from the specified gate by sending MMU_LOAD

        Args:
            gate (int): Gate index to select (0-based)
        """

    def unload(self) -> None:
        """Unload the currently loaded filament by sending MMU_UNLOAD."""
        ...

    def select_tool(self, tool: int) -> None:
        """Select a tool, triggering a filament change if needed.

        Args:
            tool (int): Tool index to select (0-based).
        """
        ...

    @QtCore.pyqtSlot(dict, name="update_mmu_state")
    def update_mmu_state(self, data: dict) -> None:
        """Receive an MMU status dict from Moonraker and update internal state.

        Called with either a full status response (on connect) or a diff
        (from notify_status_update). Builds or updates the MMUState and
        emits mmu_state_changed

        Args:
            data (dict): Raw MMU status or diff dict from Moonraker
        """
        ...


if __name__ == "__main__":
    manager = AMUManager()
    print(manager.toggle_amu_system(True))
