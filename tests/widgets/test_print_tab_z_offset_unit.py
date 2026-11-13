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
        _cancel_pending=False,
        _cancel_saw_busy=False,
        _cancel_timer=MagicMock(),
        _cancel_settle=MagicMock(),
        _cancel_returned=False,
        _cancel_gen=0,
        _print_state="printing",
        _idle_state="Printing",
        _usb_pending=False,
    )
    tab.save_config = lambda: PrintTab.save_config(tab)
    tab._maybe_finish_cancel = lambda: PrintTab._maybe_finish_cancel(tab)
    tab._clear_cancel = lambda: PrintTab._clear_cancel(tab)
    tab._finish_cancel = lambda: PrintTab._finish_cancel(tab)
    tab._on_cancel_reply = lambda gen, reply: PrintTab._on_cancel_reply(tab, gen, reply)
    return tab


def _cancel_reply(tab: SimpleNamespace):
    """The callback handle_cancel_print gave printer.print.cancel."""
    return tab.ws.api.cancel_print.call_args.kwargs["callback"]


def _hides(tab: SimpleNamespace) -> int:
    return sum(c.args[0] is False for c in tab.call_load_panel.emit.call_args_list)


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


def test_cancel_loadscreen_waits_for_cancel_macro_to_finish():
    tab = _tab(true_zero=True)
    PrintTab.handle_cancel_print(tab)

    PrintTab.on_print_stats_update(tab, "state", "cancelled")
    assert _hides(tab) == 0

    PrintTab.on_idle_timeout_update(tab, "state", "Ready")
    assert _hides(tab) == 1
    assert tab._cancel_pending is False
    assert tab.call_load_panel.emit.call_args.args == (False, "", True)
    tab._cancel_timer.stop.assert_called()


def test_cancel_from_pause_waits_for_the_macro_to_turn_idle_busy():
    tab = _tab(true_zero=True)
    tab._idle_state = "Ready"
    PrintTab.handle_cancel_print(tab)

    PrintTab.on_print_stats_update(tab, "state", "cancelled")
    assert _hides(tab) == 0

    PrintTab.on_idle_timeout_update(tab, "state", "Printing")
    PrintTab.on_idle_timeout_update(tab, "state", "Ready")
    assert _hides(tab) == 1


def test_cancel_timeout_drops_loadscreen_when_idle_never_arrives():
    tab = _tab(true_zero=True)
    PrintTab.handle_cancel_print(tab)
    tab._cancel_timer.start.assert_called_once_with()
    tab._print_state = "cancelled"

    PrintTab._on_cancel_timeout(tab)

    assert tab.call_load_panel.emit.call_args.args == (False, "", True)
    assert tab._cancel_pending is False


@pytest.mark.parametrize("state", ["printing", "paused"])
def test_cancel_timeout_keeps_waiting_while_cancel_is_queued(state):
    tab = _tab(true_zero=True)
    PrintTab.handle_cancel_print(tab)
    tab._print_state = state

    PrintTab._on_cancel_timeout(tab)

    assert _hides(tab) == 0
    assert tab._cancel_pending is True
    assert tab._cancel_timer.start.call_count == 2


def test_cancel_by_other_client_leaves_loadscreen_alone():
    tab = _tab(true_zero=True)
    tab._idle_state = "Ready"
    PrintTab.on_print_stats_update(tab, "state", "cancelled")
    assert _hides(tab) == 0


def test_shutdown_during_cancel_clears_loadscreen():
    tab = _tab(true_zero=True)
    PrintTab.handle_cancel_print(tab)

    PrintTab.on_klippy_state(tab, "shutdown")

    assert _hides(tab) == 1
    assert tab._cancel_pending is False


@pytest.mark.parametrize("late_busy", [False, True])
def test_fast_cancel_from_pause_ends_on_the_macro_reply(late_busy):
    tab = _tab(true_zero=True)
    tab._idle_state = "Ready"
    PrintTab.handle_cancel_print(tab)
    _cancel_reply(tab)({})
    tab._cancel_settle.start.assert_called_once_with()
    assert _hides(tab) == 0
    if late_busy:  # the macro's Printing update landed during the settle
        PrintTab.on_idle_timeout_update(tab, "state", "Printing")
    PrintTab._on_cancel_settled(tab)
    assert _hides(tab) == (0 if late_busy else 1)
    PrintTab.on_idle_timeout_update(tab, "state", "Ready")
    assert tab.call_load_panel.emit.call_args.args == (False, "", True)
    assert tab._cancel_pending is False


def test_failed_cancel_reply_releases_loadscreen():
    tab = _tab(true_zero=True)
    PrintTab.handle_cancel_print(tab)
    _cancel_reply(tab)({"error": {"code": 400, "message": "Must home axis first"}})
    assert tab.call_load_panel.emit.call_args.args == (False, "", True)
    assert tab._cancel_pending is False


def test_unsent_cancel_releases_loadscreen():
    tab = _tab(true_zero=True)
    tab.ws.api.cancel_print.return_value = False
    PrintTab.handle_cancel_print(tab)
    assert tab.call_load_panel.emit.call_args.args == (False, "", True)
    assert tab._cancel_pending is False


def test_reply_of_an_earlier_cancel_is_ignored():
    tab = _tab(true_zero=True)
    PrintTab.handle_cancel_print(tab)
    stale = _cancel_reply(tab)
    PrintTab._on_cancel_timeout(tab)
    PrintTab.handle_cancel_print(tab)
    stale({"error": {"code": -1, "message": "not connected"}})
    assert tab._cancel_pending is True
