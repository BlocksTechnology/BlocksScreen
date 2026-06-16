"""Widget test configuration.

Ensures ``BlocksScreen/`` is on sys.path so ``from lib.xxx`` imports
resolve correctly, and clears any empty ``lib.*`` stub packages that
the network conftest may have registered before this directory is loaded.
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

from PyQt6 import QtWidgets

_bs_dir = Path(__file__).resolve().parent.parent.parent / "BlocksScreen"
if str(_bs_dir) not in sys.path:
    sys.path.insert(0, str(_bs_dir))

# The network conftest registers empty namespace stubs for lib, lib.panels,
# lib.panels.widgets, and lib.utils. Clear them so the real packages
# from _bs_dir are importable.
for _pkg in ("lib", "lib.panels", "lib.panels.widgets", "lib.utils"):
    mod = sys.modules.get(_pkg)
    if mod is not None and not getattr(mod, "__file__", None):
        del sys.modules[_pkg]

# Load real events module from its app-side location.
_events_path = Path(__file__).parents[2] / "BlocksScreen" / "events.py"
_spec = importlib.util.spec_from_file_location("events", _events_path)
_events_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_events_mod)  # type: ignore[union-attr]
sys.modules["events"] = _events_mod

# Stub bare lib.* imports — connectionPage uses these without the BlocksScreen
# prefix (app is run from inside BlocksScreen/).  Tests use BlocksScreen.* paths
# so these bare names are never on sys.path.
_moonraker_stub = MagicMock()
_moonraker_stub.MoonWebSocket = MagicMock
sys.modules.setdefault("lib.moonrakerComm", _moonraker_stub)

_frame_stub = MagicMock()
_frame_stub.BlocksCustomFrame = QtWidgets.QFrame
sys.modules.setdefault("lib.utils.blocks_frame", _frame_stub)

_icon_btn_stub = MagicMock()
_icon_btn_stub.IconButton = QtWidgets.QPushButton
sys.modules.setdefault("lib.utils.icon_button", _icon_btn_stub)
