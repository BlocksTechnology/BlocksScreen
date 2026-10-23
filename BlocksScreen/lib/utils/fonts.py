"""Single registration point for the bundled Momcake faces.

Qt files both Momcake-Thin.ttf and Momcake-Bold.ttf under one family whose real
name matches neither file: "Momcake Pro". Asking for "Momcake-Thin" or "Momcake"
silently resolves to the system default, which is how every topbar filament icon
ended up rendering in a fallback face. Registration is also process-global and
permanent, so doing it once here removes the ordering race that came from three
page constructors each registering on first visit.
"""

import functools
import logging

from PyQt6 import QtGui

_logger = logging.getLogger(__name__)

# Must stay in sync with the font-family the topbar .svg assets declare;
# tests/ui/test_resource_keys_unit.py fails if the two ever drift apart.
MOMCAKE_FAMILY = "Momcake Pro"

_FONT_PATHS = (
    ":/font/media/fonts for text/Momcake-Thin.ttf",
    ":/font/media/fonts for text/Momcake-Bold.ttf",
)


@functools.cache
def register_momcake() -> str:
    """Register the bundled Momcake faces once and return the family Qt filed them under."""
    families: list[str] = []
    for path in _FONT_PATHS:
        font_id = QtGui.QFontDatabase.addApplicationFont(path)
        if font_id == -1:
            _logger.warning("bundled font failed to load: %s", path)
            continue
        families.extend(QtGui.QFontDatabase.applicationFontFamilies(font_id))
    if not families:
        _logger.error("no bundled font loaded, text falls back to the system face")
        return ""
    if MOMCAKE_FAMILY not in families:
        _logger.warning(
            "bundled font family is %s, expected %s", families, MOMCAKE_FAMILY
        )
    return families[0]
