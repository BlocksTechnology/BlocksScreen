"""tests/panels/conftest.py — stub MainWindow's heavy dependency tree.

MainWindow pulls in nearly every subsystem (devices, tabs, updater, D-Bus
comms, generated UI/resource modules) purely to build the widget tree.
None of that is needed to unit-test a single guard condition in
``_on_klippy_state``, so every non-PyQt6 import is stubbed as a MagicMock
module before the real module is imported.
"""

import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

_project_root = Path(__file__).resolve().parent.parent.parent

# Other test directories (e.g. tests/lib/conftest.py) leak a bare
# ``MagicMock()`` stub for "lib.utils" into sys.modules with no teardown,
# which breaks the real ``lib.utils.*`` imports below on a full-suite run.
# Clear any stale "lib"/"lib.*" entries before rebuilding our own stubs.
for _stale in list(sys.modules):
    if _stale == "lib" or _stale.startswith("lib."):
        del sys.modules[_stale]

_STUB_MODULES = (
    "events",
    "configfile",
    "devices",
    "devices.amu",
    "devices.storage",
    "lib",
    "lib.files",
    "lib.klipper_message_filter",
    "lib.machine",
    "lib.moonrakerComm",
    "lib.network",
    "lib.panels",
    "lib.panels.controlTab",
    "lib.panels.filamentTab",
    "lib.panels.networkWindow",
    "lib.panels.printTab",
    "lib.panels.utilitiesTab",
    "lib.panels.widgets",
    "lib.panels.widgets.basePopup",
    "lib.panels.widgets.MainWindow.cancelPage",
    "lib.panels.widgets.MainWindow.connectionPage",
    "lib.panels.widgets.loadWidget",
    "lib.panels.widgets.MainWindow.notificationPage",
    "lib.panels.widgets.MainWindow.updatePage",
    "lib.printer",
    "lib.ui",
    "lib.ui.mainWindow_ui",
    "lib.ui.resources",
    "lib.ui.resources.background_resources_rc",
    "lib.ui.resources.font_rc",
    "lib.ui.resources.graphic_resources_rc",
    "lib.ui.resources.icon_resources_rc",
    "lib.ui.resources.main_menu_resources_rc",
    "lib.ui.resources.system_resources_rc",
    "lib.ui.resources.top_bar_resources_rc",
    "lib.updater_worker",
    "screensaver",
)

for _name in _STUB_MODULES:
    _mod = types.ModuleType(_name)
    _mod.__path__ = []  # marks it as a package so submodule imports resolve
    sys.modules[_name] = _mod

# "lib.utils" is deliberately NOT in _STUB_MODULES: blocks_tabwidget,
# display_button, and icon_button are plain PyQt6 widgets with no heavy
# deps, so let them load for real from disk instead of stubbing them.
sys.modules["lib"].__path__ = [str(_project_root / "BlocksScreen" / "lib")]

# events.* is referenced as a bare attribute in type annotations
# (e.g. ``event: events.WebSocketMessageReceived``), evaluated eagerly at
# class-definition time — needs to resolve any attribute, not just a fixed set.
sys.modules["events"] = MagicMock()

sys.modules["configfile"].BlocksScreenConfig = MagicMock
sys.modules["configfile"].get_configparser = MagicMock(return_value=MagicMock())
sys.modules["devices.amu"].AMUManager = MagicMock
sys.modules["devices.storage"].USBManager = MagicMock
sys.modules["lib.files"].Files = MagicMock
sys.modules["lib.klipper_message_filter"].MessageSource = MagicMock()
sys.modules["lib.klipper_message_filter"].Severity = MagicMock()
sys.modules["lib.klipper_message_filter"].match_message = MagicMock()
sys.modules["lib.machine"].MachineControl = MagicMock
sys.modules["lib.moonrakerComm"].MoonWebSocket = MagicMock
sys.modules["lib.network"].WifiIconKey = MagicMock()
sys.modules["lib.panels.controlTab"].ControlTab = MagicMock
sys.modules["lib.panels.filamentTab"].FilamentTab = MagicMock
sys.modules["lib.panels.networkWindow"].NetworkControlWindow = MagicMock
sys.modules["lib.panels.networkWindow"].PixmapCache = MagicMock
sys.modules["lib.panels.printTab"].PrintTab = MagicMock
sys.modules["lib.panels.utilitiesTab"].UtilitiesTab = MagicMock
sys.modules["lib.panels.widgets.basePopup"].BasePopup = MagicMock
sys.modules["lib.panels.widgets.MainWindow.cancelPage"].CancelPage = MagicMock
sys.modules["lib.panels.widgets.MainWindow.connectionPage"].ConnectionPage = MagicMock
sys.modules["lib.panels.widgets.loadWidget"].LoadingOverlayWidget = MagicMock
sys.modules["lib.panels.widgets.MainWindow.notificationPage"].NotificationPage = MagicMock
sys.modules["lib.panels.widgets.MainWindow.updatePage"].UpdatePage = MagicMock
sys.modules["lib.printer"].Printer = MagicMock
sys.modules["lib.ui.mainWindow_ui"].Ui_MainWindow = MagicMock
sys.modules["lib.updater_worker"].UpdaterWorker = MagicMock
sys.modules["screensaver"].ScreenSaver = MagicMock
