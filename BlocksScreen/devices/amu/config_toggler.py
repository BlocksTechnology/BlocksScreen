"""Swap printer.cfg between the AMU and single-filament variant includes."""

import contextlib
import logging
import os
import re
from enum import StrEnum
from pathlib import Path

logger = logging.getLogger(__name__)

AMU_INCLUDE: str = "config/variant_mmu/base/*.cfg"
SINGLE_INCLUDE: str = "config/variant_sync_single/*.cfg"


class ToggleResult(StrEnum):
    """Outcome of a toggle; only FAILED is an error and only CHANGED needs a restart."""

    CHANGED = "changed"
    UNCHANGED = "unchanged"
    FAILED = "failed"


def _include_pattern(include: str) -> re.Pattern[str]:
    """Match the include commented or not, tolerating stray spaces in the brackets."""
    body = rf"\[include[ \t]+{re.escape(include)}[ \t]*\]"
    return re.compile(rf"^([ \t]*)(#*)[ \t]*({body})[ \t]*(\r?)$", re.MULTILINE)


_PATTERNS: dict[str, re.Pattern[str]] = {
    AMU_INCLUDE: _include_pattern(AMU_INCLUDE),
    SINGLE_INCLUDE: _include_pattern(SINGLE_INCLUDE),
}


class ConfigToggler:
    """Swaps printer.cfg between the AMU and single-filament variant includes."""

    def __init__(self, config_path: Path) -> None:
        """Resolve printer.cfg and read the active variant from it."""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            # os.replace() would swap a symlinked printer.cfg for a regular file.
            self._path = config_path.resolve()
            self._state = self._detect_state()
        else:
            logger.warning("Config File not found %s", config_path)

    def _read(self) -> str | None:
        """Return printer.cfg contents, or None when there is no readable file."""
        if self._path is None:
            return None
        try:
            # newline="" keeps CRLF intact; surrogateescape survives non-UTF-8 bytes.
            with self._path.open(
                encoding="utf-8", errors="surrogateescape", newline=""
            ) as f:
                return f.read()
        except OSError as e:
            logger.error("ConfigToggler: read of %s failed: %s", self._path, e)
            return None

    def _write(self, text: str) -> bool:
        """Write through a sibling temp file so a crash cannot truncate printer.cfg."""
        if self._path is None:
            return False
        tmp = self._path.with_name(self._path.name + ".tmp")
        try:
            with tmp.open(
                "w", encoding="utf-8", errors="surrogateescape", newline=""
            ) as f:
                f.write(text)
                f.flush()
                os.fsync(f.fileno())
            os.chmod(tmp, self._path.stat().st_mode & 0o777)
            os.replace(tmp, self._path)
        except OSError as e:
            logger.error("ConfigToggler: write of %s failed: %s", self._path, e)
            with contextlib.suppress(OSError):
                tmp.unlink(missing_ok=True)
            return False
        try:
            dir_fd = os.open(self._path.parent, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError as e:
            logger.warning("ConfigToggler: dir fsync of %s failed: %s", self._path, e)
        return True

    @staticmethod
    def _is_active(text: str, include: str) -> bool:
        """True when the include is present and not commented out."""
        match = _PATTERNS[include].search(text)
        return match is not None and not match.group(2)

    def _detect_state(self) -> bool:
        """Read the AMU variant include state straight off disk."""
        text = self._read()
        return False if text is None else self._is_active(text, AMU_INCLUDE)

    def toggle(self, activate: bool) -> ToggleResult:
        """Activate one variant include and comment the other, atomically."""
        text = self._read()
        if text is None:
            logger.warning("No Config File available")
            return ToggleResult.FAILED
        self._state = self._is_active(text, AMU_INCLUDE)
        if self._state == activate:
            return ToggleResult.UNCHANGED

        enable = AMU_INCLUDE if activate else SINGLE_INCLUDE
        disable = SINGLE_INCLUDE if activate else AMU_INCLUDE
        new_text, enabled = _PATTERNS[enable].subn(r"\1\3\4", text)
        new_text, disabled = _PATTERNS[disable].subn(r"\1#\3\4", new_text)

        if enabled != 1 or disabled != 1:
            logger.error(
                "ConfigToggler.toggle(activate=%s): expected one match each, got "
                "%d for %s and %d for %s",
                activate,
                enabled,
                enable,
                disabled,
                disable,
            )
            return ToggleResult.FAILED

        if not self._is_active(new_text, enable) or self._is_active(new_text, disable):
            logger.error(
                "ConfigToggler.toggle(activate=%s): result would not leave exactly one "
                "variant active, refusing to write",
                activate,
            )
            return ToggleResult.FAILED

        if not self._write(new_text):
            return ToggleResult.FAILED
        self._state = activate
        return ToggleResult.CHANGED

    def is_configured(self) -> bool:
        """Return True if the AMU variant include is uncommented."""
        return self._state
