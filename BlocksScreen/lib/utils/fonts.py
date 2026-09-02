"""Registers the bundled Momcake faces once; Qt files both .ttf under 'Momcake Pro'."""

import functools
import logging

from PyQt6 import QtGui

_logger = logging.getLogger(__name__)

# Must match the topbar .svg font-family; test_resource_keys_unit.py guards the drift.
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
