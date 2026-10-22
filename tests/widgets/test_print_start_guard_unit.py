"""PrintTab.start_print blocks a print PRINT_START would refuse as unloaded."""

import sys
import types
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

# Same stubbing and eviction as test_slider_page_request_unit.py, see there for why.
for _name in ("configfile", "lib.files", "lib.printer"):
    sys.modules[_name] = types.ModuleType(_name)
sys.modules["configfile"].BlocksScreenConfig = MagicMock
sys.modules["configfile"].get_configparser = MagicMock(return_value=MagicMock())
sys.modules["lib.files"].Files = MagicMock
sys.modules["lib.printer"].Printer = MagicMock
sys.modules.pop("lib.utils.icon_button", None)
sys.modules.pop("lib.panels.printTab", None)
sys.modules.pop("lib.ui", None)
for _stubbed in [_m for _m in sys.modules if _m.startswith("lib.panels.widgets")]:
    sys.modules.pop(_stubbed, None)

from lib.panels.printTab import PrintTab  # noqa: E402


def _tab(amu_manager: object) -> SimpleNamespace:
    return SimpleNamespace(
        amu_manager=amu_manager,
        notify=MagicMock(),
        jobStatusPage_widget=MagicMock(),
    )


class TestStartPrint:
    @pytest.mark.parametrize("refusal", [None, ""])
    def test_starts_without_amu_or_refusal(self, refusal) -> None:
        amu = None if refusal is None else MagicMock()
        if amu is not None:
            amu.print_start_refusal.return_value = refusal
        tab = _tab(amu)
        PrintTab.start_print(tab, "cube.gcode")
        tab.jobStatusPage_widget.on_print_start.assert_called_once_with("cube.gcode")
        tab.notify.emit.assert_not_called()

    def test_refusal_blocks_and_notifies(self) -> None:
        amu = MagicMock()
        amu.print_start_refusal.return_value = "No filament at the toolhead."
        tab = _tab(amu)
        PrintTab.start_print(tab, "cube.gcode")
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        tab.notify.emit.assert_called_once_with(
            "PrintTab", "No filament at the toolhead.", 2, True
        )
