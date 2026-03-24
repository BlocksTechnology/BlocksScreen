import logging
import re
from pathlib import Path

from PyQt6 import QtCore

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

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._amu_state = False
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
            bool: True: Sucess, False: Failed
        """
        # signal to say that it was changed AMU para mainwindow
        if self._amu_state == state:
            return

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
                "Failed to apply(state=%s) AMU System: could not read/write %s\n%e",
                state,
                self._config_filename,
                e,
            )
            return False

    def toggle_amu_system(self, activate: bool) -> bool:
        """Method that comments/uncomments the AMU_FILES from the printer.cfg according with state value

        Args:
            state (bool): True: Uncomment, False: Comment

        Returns:
            bool: True: Sucess, False: Failed
        """
        return self._apply_patterns(activate)


if __name__ == "__main__":
    manager = AMUManager()
    print(manager.toggle_amu_system(True))
