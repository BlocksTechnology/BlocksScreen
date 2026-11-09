"""PrintTab.start_print blocks a print PRINT_START would refuse as unloaded."""

import sys
import types
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

# Same stub/evict/restore as test_print_tab_z_offset_unit.py, see there for why.
_STUBS = ("configfile", "lib.files", "lib.printer")
_EVICT = ("lib.panels.printTab", "lib.ui", "lib.utils.icon_button")
_saved = {
    m: sys.modules[m]
    for m in list(sys.modules)
    if m in _STUBS or m in _EVICT or m.startswith("lib.panels.widgets")
}
for _name in _STUBS:
    sys.modules[_name] = types.ModuleType(_name)
sys.modules["configfile"].BlocksScreenConfig = MagicMock
sys.modules["configfile"].get_configparser = MagicMock(return_value=MagicMock())
sys.modules["lib.files"].Files = MagicMock
sys.modules["lib.printer"].Printer = MagicMock
for _name in [
    m for m in sys.modules if m in _EVICT or m.startswith("lib.panels.widgets")
]:
    sys.modules.pop(_name)

from lib.panels.printTab import PrintTab  # noqa: E402

# Put the stand-ins back so this import leaves sys.modules as found.
for _name in [
    m
    for m in sys.modules
    if m in _STUBS or m in _EVICT or m.startswith("lib.panels.widgets")
]:
    del sys.modules[_name]
sys.modules.update(_saved)


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
