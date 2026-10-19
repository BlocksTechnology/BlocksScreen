"""Cancel + standby must not offer to save a Z-offset on a true-zero printer.

Calls PrintTab's unbound methods against a minimal stand-in ``self``, like
test_slider_page_request_unit.py: a full PrintTab pulls in heavy UI deps.
"""

import sys
import types
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

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
# Other tests leave stand-ins for these session-wide; PrintTab needs the real ones.
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


def _tab(*, true_zero: bool) -> SimpleNamespace:
    tab = SimpleNamespace(
        printer=SimpleNamespace(uses_true_zero_offset=true_zero),
        babystepPage=SimpleNamespace(baby_stepchange=True),
        ws=MagicMock(),
        call_load_panel=MagicMock(),
        on_cancel_print=MagicMock(),
        BasePopup=MagicMock(),
        BasePopup_z_offset=MagicMock(),
        save_config_btn=MagicMock(),
        update_configuration_file=MagicMock(),
        _finish_print_handled=False,
        _active_z_offset=0.05,
        _cancel_z_snapshot=0.0,
    )
    tab.save_config = lambda: PrintTab.save_config(tab)
    return tab


def _cancel_then_standby(tab: SimpleNamespace) -> None:
    PrintTab.handle_cancel_print(tab)
    PrintTab.on_print_stats_update(tab, "state", "standby")


@pytest.mark.parametrize("true_zero", [True, False])
def test_cancel_then_standby_offers_save_only_without_true_zero(true_zero):
    tab = _tab(true_zero=true_zero)
    _cancel_then_standby(tab)
    if true_zero:
        tab.BasePopup_z_offset.open.assert_not_called()
        assert all(
            c.args != (True,) for c in tab.save_config_btn.setVisible.call_args_list
        )
    else:
        tab.BasePopup_z_offset.open.assert_called_once_with()
        tab.save_config_btn.setVisible.assert_called_with(True)
