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
    "lib.panels.widgets.common.basePopup",
    "lib.panels.widgets.common.loadWidget",
    "lib.panels.widgets.MainWindow",
    "lib.panels.widgets.MainWindow.cancelPage",
    "lib.panels.widgets.MainWindow.connectionPage",
    "lib.panels.widgets.MainWindow.notificationPage",
    "lib.panels.widgets.MainWindow.updatePage",
    "lib.printer",
    "lib.ui",
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

# MainWindow builds pure-PyQt6 widgets from lib.utils directly, so those stay
# real: re-point lib.utils at the source tree (earlier suites may have left a
# MagicMock there, which is not importable as a package).
_utils = types.ModuleType("lib.utils")
_utils.__path__ = [str(Path(__file__).parents[2] / "BlocksScreen" / "lib" / "utils")]
sys.modules["lib.utils"] = _utils

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
sys.modules["lib.panels.widgets.common.basePopup"].BasePopup = MagicMock
sys.modules["lib.panels.widgets.common.loadWidget"].LoadingOverlayWidget = MagicMock
_MW = "lib.panels.widgets.MainWindow"
sys.modules[f"{_MW}.cancelPage"].CancelPage = MagicMock
sys.modules[f"{_MW}.connectionPage"].ConnectionPage = MagicMock
sys.modules[f"{_MW}.notificationPage"].NotificationPage = MagicMock
sys.modules[f"{_MW}.updatePage"].UpdatePage = MagicMock
sys.modules["lib.printer"].Printer = MagicMock
sys.modules["lib.updater_worker"].UpdaterWorker = MagicMock
sys.modules["screensaver"].ScreenSaver = MagicMock
