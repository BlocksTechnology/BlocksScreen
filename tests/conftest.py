"""Sets QT_QPA_PLATFORM=offscreen so Qt-based tests work headlessly"""

import importlib
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# Bind both import names to one module before collection, or a test that puts
# BlocksScreen/ on sys.path loads a second cache and identity asserts diverge.
_blocks_pixmap = importlib.import_module("BlocksScreen.lib.utils.blocks_pixmap")
sys.modules.setdefault("lib.utils.blocks_pixmap", _blocks_pixmap)
