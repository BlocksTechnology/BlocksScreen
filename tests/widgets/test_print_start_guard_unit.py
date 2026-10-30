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

    def test_usb_file_is_imported_not_printed(self) -> None:
        tab = _tab(None)
        tab._start_usb_import = MagicMock()
        PrintTab.start_print(tab, "USB-STICK/cube.gcode")
        tab._start_usb_import.assert_called_once_with("USB-STICK/cube.gcode")
        tab.jobStatusPage_widget.on_print_start.assert_not_called()


@pytest.mark.parametrize(
    ("lines", "started"),
    [
        (
            ["// action:blocks_usb_print USB-STICK/my cube.gcode"],
            "USB-STICK/my cube.gcode",
        ),
        (["// action:blocks_usb_print cube.gcode"], None),
        (["// blocks_usb_print USB-STICK/cube.gcode", "ok"], None),
    ],
)
def test_usb_print_action_from_macro(lines, started) -> None:
    tab = SimpleNamespace(start_print=MagicMock())
    PrintTab._on_gcode_response(tab, lines)
    if started is None:
        tab.start_print.assert_not_called()
    else:
        tab.start_print.assert_called_once_with(started)


@pytest.mark.parametrize(
    ("name", "values", "sent"),
    [
        ("SDCARD_PRINT_FILE", {"blocksscreen_usb": False}, True),
        ("SDCARD_PRINT_FILE", {"blocksscreen_usb": True}, False),
        ("SDCARD_PRINT_FILE", {}, False),  # another override, no flag to set
        ("PRINT_START", {"blocksscreen_usb": False}, False),
    ],
)
def test_usb_flag_set_only_on_flagged_override(name, values, sent) -> None:
    tab = SimpleNamespace(run_gcode_signal=MagicMock())
    PrintTab._on_gcode_macro_update(tab, name, values)
    assert tab.run_gcode_signal.emit.called is sent


class TestUsbImportDone:
    @pytest.fixture
    def tab(self, monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
        tab = _tab(None)
        tab._usb_import_task = object()
        tab._usb_key = tab._usb_local = ""
        tab._usb_created = set()
        tab._usb_settle_timer = MagicMock()
        tab.gcode_path = "/tmp/gcodes"
        tab.call_load_panel = MagicMock()
        tab._usb_print_local_copy = lambda: PrintTab._usb_print_local_copy(tab)
        tab.remember = MagicMock()
        # printTab was evicted from sys.modules, so patch the function's globals.
        monkeypatch.setitem(
            PrintTab._usb_print_local_copy.__globals__, "remember_import", tab.remember
        )
        return tab

    def _printed(self, tab: SimpleNamespace) -> None:
        assert tab._usb_import_task is None
        tab.call_load_panel.emit.assert_called_once_with(False, "", False)
        tab.jobStatusPage_widget.on_print_start.assert_called_once_with("cube.gcode")
        tab.remember.assert_called_once()
        assert tab.remember.call_args.args[1:] == ("k", "cube.gcode")

    def test_reused_copy_prints_at_once(self, tab) -> None:
        PrintTab._on_usb_import_done(
            tab, "USB-STICK/cube.gcode", "cube.gcode", "k", True, ""
        )
        self._printed(tab)

    def test_new_copy_waits_for_moonraker(self, tab) -> None:
        PrintTab._on_usb_import_done(
            tab, "USB-STICK/cube.gcode", "cube.gcode", "k", False, ""
        )
        tab._usb_settle_timer.start.assert_called_once()
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        PrintTab._on_usb_file_added(tab, {"path": "other.gcode"})
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        self._printed(tab)

    def test_create_before_done_prints_at_once(self, tab) -> None:
        PrintTab._on_usb_file_added(tab, {"path": "/cube.gcode"})
        PrintTab._on_usb_import_done(
            tab, "USB-STICK/cube.gcode", "cube.gcode", "k", False, ""
        )
        tab._usb_settle_timer.start.assert_not_called()
        self._printed(tab)

    def test_timeout_prints_anyway(self, tab) -> None:
        PrintTab._on_usb_import_done(
            tab, "USB-STICK/cube.gcode", "cube.gcode", "k", False, ""
        )
        PrintTab._on_usb_settle_timeout(tab)
        self._printed(tab)

    def test_index_failure_still_prints(self, tab) -> None:
        tab.remember.side_effect = OSError("read-only")
        PrintTab._on_usb_import_done(
            tab, "USB-STICK/cube.gcode", "cube.gcode", "k", True, ""
        )
        tab.jobStatusPage_widget.on_print_start.assert_called_once_with("cube.gcode")

    def test_file_added_ignored_when_idle(self, tab) -> None:
        tab._usb_import_task = None
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        assert tab._usb_created == set()

    def test_error_notifies_and_does_not_print(self, tab) -> None:
        PrintTab._on_usb_import_done(tab, "USB-STICK/cube.gcode", "", "", False, "Bad")
        assert tab._usb_import_task is None
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        tab.notify.emit.assert_called_once_with(
            "PrintTab", "USB print failed: Bad", 2, True
        )
