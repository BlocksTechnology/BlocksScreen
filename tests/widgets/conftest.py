import importlib.util
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PyQt6 import QtWidgets

_project_root = Path(__file__).resolve().parent.parent.parent
# Add project root (not BlocksScreen/) - adding BlocksScreen/ would cause
# BlocksScreen.py to shadow the BlocksScreen namespace package.
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

for _pkg in ("lib", "lib.panels", "lib.panels.widgets", "lib.utils"):
    sys.modules.pop(_pkg, None)

_lib_mod = types.ModuleType("lib")
_lib_mod.__path__ = [str(_project_root / "BlocksScreen" / "lib")]
_lib_mod.__package__ = "lib"
sys.modules["lib"] = _lib_mod

for _mod_name in ("events", "helper_methods"):
    _mod_path = _project_root / "BlocksScreen" / f"{_mod_name}.py"
    _spec = importlib.util.spec_from_file_location(_mod_name, _mod_path)
    _mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
    _spec.loader.exec_module(_mod)  # type: ignore[union-attr]
    sys.modules[_mod_name] = _mod

_moonraker_stub = MagicMock()
_moonraker_stub.MoonWebSocket = MagicMock
sys.modules.setdefault("lib.moonrakerComm", _moonraker_stub)

_frame_stub = MagicMock()
_frame_stub.BlocksCustomFrame = QtWidgets.QFrame
sys.modules.setdefault("lib.utils.blocks_frame", _frame_stub)

_icon_btn_stub = MagicMock()
_icon_btn_stub.IconButton = QtWidgets.QPushButton
sys.modules.setdefault("lib.utils.icon_button", _icon_btn_stub)


@pytest.fixture(scope="module", autouse=True)
def mock_heavy_deps():
    with pytest.MonkeyPatch.context() as mp:
        for key in ("configfile", "BlocksScreen.lib.panels.widgets.loadWidget"):
            mp.delitem(sys.modules, key, raising=False)
        mp.setitem(sys.modules, "configfile", MagicMock())
        yield
