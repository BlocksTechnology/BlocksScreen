import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

from PyQt6 import QtWidgets

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
