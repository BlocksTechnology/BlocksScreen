import logging
import re

from pathlib import Path

logger = logging.getLogger(__name__)

AMU_FILES: list[str] = [
    "mmu/base/*.cfg",
    "mmu/optional/client_macros.cfg",
    "filament_manager.cfg",
]

_AMU_PATTERNS: list[re.Pattern[str]] = [
    re.compile(rf"^(#?)(\[include {re.escape(f)}\])", re.MULTILINE) for f in AMU_FILES
]


class ConfigToggler:
    """Manages commenting/uncommenting AMU cfg includes in printer.cfg"""

    def __init__(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("Config File not found %s", config_path)

    def _detect_state(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(re.search(rf"^\[include {re.escape(f)}\]", text, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def toggle(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate,e
            )
            return False
    
    def is_configured(self) -> bool:
        """Return True if AMU includes are currently uncommented"""
        return self._state
