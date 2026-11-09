"""Expose blocks_pixmap under the runtime `lib.utils` name the modules under test import."""

import importlib
import sys

# Pure-PyQt6 leaf, so sharing the real module is safe; mirrors tests/network/conftest.py.
sys.modules.setdefault(
    "lib.utils.blocks_pixmap",
    importlib.import_module("BlocksScreen.lib.utils.blocks_pixmap"),
)
