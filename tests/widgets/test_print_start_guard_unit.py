"""PrintTab.start_print blocks a print PRINT_START would refuse as unloaded."""

import sys
import threading
import types
from types import MethodType, SimpleNamespace
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

from lib.panels.printTab import USB_UNINDEXED_MAX, PrintTab  # noqa: E402

# Put the stand-ins back so this import leaves sys.modules as found.
for _name in [
    m
    for m in sys.modules
    if m in _STUBS or m in _EVICT or m.startswith("lib.panels.widgets")
]:
    del sys.modules[_name]
sys.modules.update(_saved)


def _bind(tab: SimpleNamespace, *names: str) -> SimpleNamespace:
    for name in names:
        setattr(tab, name, MethodType(getattr(PrintTab, name), tab))
    return tab


def _tab(amu_manager: object, printing_state: str = "standby") -> SimpleNamespace:
    tab = SimpleNamespace(
        amu_manager=amu_manager,
        _print_state=printing_state,
        _klippy_state="",
        _usb_pending=False,
        _usb_from_console=False,
        _cancel_pending=False,
        notify=MagicMock(),
        jobStatusPage_widget=MagicMock(),
        run_gcode_signal=MagicMock(),
    )
    return _bind(tab, "_print_refusal", "_begin_print", "_console_error")


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

    @pytest.mark.parametrize(
        ("state", "pending", "reason"),
        [
            ("printing", False, "A print is already running."),
            ("paused", False, "A print is already running."),
            ("standby", True, "A USB file is still being prepared for printing."),
            ("standby", None, "The last print is still being cancelled."),
        ],
    )
    def test_busy_printer_blocks(self, state, pending, reason) -> None:
        tab = _tab(None, state)
        tab._usb_pending = bool(pending)
        tab._cancel_pending = pending is None  # cancel sent, state still printing
        tab._start_usb_import = MagicMock()
        assert tab._begin_print("USB-STICK/cube.gcode") == reason
        tab._start_usb_import.assert_not_called()
        tab.notify.emit.assert_called_once_with("PrintTab", reason, 2, True)

    @pytest.mark.parametrize("state", ["shutdown", "error", "startup"])
    def test_klipper_not_ready_blocks_before_the_copy(self, state) -> None:
        tab = _tab(None)
        tab._klippy_state = state
        tab._start_usb_import = MagicMock()
        assert tab._begin_print("USB-STICK/cube.gcode") == "Klipper is not ready."
        tab._start_usb_import.assert_not_called()

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
        (
            ["// action:blocks_usb_print USB-STICK/cube.gcode\r\n"],
            "USB-STICK/cube.gcode",
        ),
        (["// blocks_usb_print USB-STICK/cube.gcode", "ok"], None),
    ],
)
def test_usb_print_action_from_macro(lines, started) -> None:
    tab = SimpleNamespace(
        _begin_print=MagicMock(return_value=""), run_gcode_signal=MagicMock()
    )
    PrintTab._on_gcode_response(tab, lines)
    if started is None:
        tab._begin_print.assert_not_called()
        tab.run_gcode_signal.emit.assert_not_called()
    else:
        tab._begin_print.assert_called_once_with(started, from_console=True)
        tab.run_gcode_signal.emit.assert_called_once_with(
            "SET_GCODE_VARIABLE MACRO=SDCARD_PRINT_FILE"
            " VARIABLE=usb_pending VALUE='\"\"'"
        )


@pytest.mark.parametrize("pending_from_console", [True, False])
def test_refused_start_keeps_pending_import_origin(pending_from_console) -> None:
    # The refusal belongs to the new request; the running import keeps its origin.
    tab = _tab(None)
    tab._usb_pending = True
    tab._usb_from_console = pending_from_console
    tab._start_usb_import = MagicMock()
    assert tab._begin_print("USB-STICK/b.gcode", from_console=not pending_from_console)
    assert tab._usb_from_console is pending_from_console


def test_refused_hand_off_is_acked_and_reported_to_console() -> None:
    # Unacked, the macro's fallback would print from USB past the same refusal.
    tab = _tab(None, "printing")
    tab.run_gcode_signal = MagicMock()
    PrintTab._on_gcode_response(tab, ["// action:blocks_usb_print USB-STICK/c.gcode"])
    sent = [c.args[0] for c in tab.run_gcode_signal.emit.call_args_list]
    assert sent[0].endswith("VARIABLE=usb_pending VALUE='\"\"'")
    assert sent[1] == (
        'RESPOND TYPE=error MSG="USB print refused: A print is already running."'
    )
    tab.notify.emit.assert_called_once()


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
        tab._usb_pending = True
        tab._usb_token = 1
        tab._usb_key = tab._usb_local = ""
        tab._usb_created = set()
        tab._usb_cancel = threading.Event()
        tab._usb_unindexed = {}
        tab._usb_settle_timer = MagicMock()
        tab._cancel_pending = False
        tab._cancel_timer = tab._cancel_settle = MagicMock()
        tab.gcode_path = "/tmp/gcodes"
        tab.call_load_panel = MagicMock()
        tab.ws = MagicMock()
        _bind(
            tab,
            "_usb_print_local_copy",
            "_end_usb_print",
            "_clear_cancel",
            "_mark_unindexed",
            "_index_when_processed",
        )
        tab.remember = MagicMock()
        # printTab was evicted from sys.modules, so patch the function's globals.
        monkeypatch.setitem(
            PrintTab._usb_print_local_copy.__globals__,
            "remember_import_async",
            tab.remember,
        )
        return tab

    @staticmethod
    def _done(tab, local="cube.gcode", reused=False, error="", token=1) -> None:
        PrintTab._on_usb_import_done(
            tab, token, "USB-STICK/cube.gcode", local, "k", reused, error
        )

    @staticmethod
    def _responds(tab) -> list[str]:
        return [
            c.args[0]
            for c in tab.run_gcode_signal.emit.call_args_list
            if c.args[0].startswith("RESPOND")
        ]

    def _printed(self, tab: SimpleNamespace) -> None:
        assert tab._usb_pending is False
        tab.call_load_panel.emit.assert_called_with(False, "", False)
        tab.jobStatusPage_widget.on_print_start.assert_called_once_with("cube.gcode")
        tab.remember.assert_called_once()
        assert tab.remember.call_args.args[1:] == ("k", "cube.gcode")

    def test_reused_copy_prints_at_once(self, tab) -> None:
        self._done(tab, reused=True)
        self._printed(tab)

    def test_new_copy_waits_for_moonraker(self, tab) -> None:
        self._done(tab)
        tab._usb_settle_timer.start.assert_called_once()
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        PrintTab._on_usb_file_added(tab, {"path": "other.gcode"})
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        self._printed(tab)

    def test_klipper_drop_while_processing_still_indexes_the_copy(self, tab) -> None:
        self._done(tab)
        tab.BasePopup_z_offset = MagicMock()
        tab.save_config_btn = tab.babystepPage = MagicMock()
        PrintTab.on_klippy_state(tab, "shutdown")
        assert tab._usb_pending is False
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        assert tab.remember.call_args.args[1:] == ("k", "cube.gcode")

    def test_create_before_done_prints_at_once(self, tab) -> None:
        PrintTab._on_usb_file_added(tab, {"path": "/cube.gcode"})
        self._done(tab)
        tab._usb_settle_timer.start.assert_not_called()
        self._printed(tab)

    @staticmethod
    def _timeout(tab, sent: bool = True) -> list:
        replies: list = []

        def send_request(method, params, callback):
            assert (method, params) == (
                "server.files.metadata",
                {"filename": "cube.gcode"},
            )
            replies.append(callback)
            return sent

        tab.ws = SimpleNamespace(send_request=send_request)
        PrintTab._on_usb_settle_timeout(tab)
        return replies

    def test_timeout_prints_once_metadata_exists(self, tab) -> None:
        # Moonraker stores metadata only after its processors, Happy Hare's included.
        self._done(tab)
        self._timeout(tab)[0]({"filename": "cube.gcode", "size": 4})
        self._printed(tab)

    @pytest.mark.parametrize("sent", [True, False])
    def test_timeout_without_metadata_gives_up(self, tab, sent) -> None:
        self._done(tab)
        replies = self._timeout(tab, sent)
        if sent:
            replies[0]({"error": {"code": 404, "message": "Metadata not available"}})
        assert tab._usb_pending is False
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        tab.remember.assert_not_called()  # never processed, so never reusable
        assert "Start it from the file list" in tab.notify.emit.call_args.args[1]

    def test_metadata_reply_after_abort_is_dropped(self, tab) -> None:
        self._done(tab)
        reply = self._timeout(tab)[0]
        tab._end_usb_print("cancelled")
        reply({"filename": "cube.gcode"})
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        tab.notify.emit.assert_called_once()

    def test_job_started_meanwhile_blocks_the_copy(self, tab) -> None:
        self._done(tab)
        tab._print_state = "printing"  # another client, during the wait
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        tab.notify.emit.assert_called_once_with(
            "PrintTab", "A print is already running.", 2, True
        )

    def test_result_after_abort_is_dropped(self, tab) -> None:
        tab._end_usb_print("cancelled")
        self._done(tab, reused=True, token=1)
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        tab.remember.assert_not_called()

    def test_file_added_ignored_when_idle(self, tab) -> None:
        tab._usb_pending = False
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        assert tab._usb_created == set()
        tab.remember.assert_not_called()

    def test_abort_stops_the_running_copy(self, tab) -> None:
        tab._end_usb_print("cancelled")
        assert tab._usb_cancel.is_set()

    def test_copy_committed_after_abort_is_indexed_once_announced(self, tab) -> None:
        tab._end_usb_print("cancelled")
        self._done(tab, token=1)
        tab.remember.assert_not_called()  # Moonraker has not processed it yet
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        assert tab.remember.call_args.args[1:] == ("k", "cube.gcode")
        assert tab._usb_unindexed == {}

    def test_copy_announced_before_abort_is_indexed_at_once(self, tab) -> None:
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        tab._end_usb_print("cancelled")
        self._done(tab, token=1)
        assert tab.remember.call_args.args[1:] == ("k", "cube.gcode")

    def test_copy_processed_before_a_late_abort_result_is_indexed(self, tab) -> None:
        # Moonraker announced it while nothing was pending, so only metadata knows
        tab._end_usb_print("cancelled")
        self._done(tab, token=1)
        method, params = tab.ws.send_request.call_args.args
        assert (method, params) == ("server.files.metadata", {"filename": "cube.gcode"})
        tab.ws.send_request.call_args.kwargs["callback"]({"filename": "cube.gcode"})
        assert tab.remember.call_args.args[1:] == ("k", "cube.gcode")
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        tab.remember.assert_called_once()

    def test_unindexed_copies_stay_bounded(self, tab) -> None:
        for n in range(USB_UNINDEXED_MAX + 5):
            tab._mark_unindexed(f"c{n}.gcode", "k")
        assert len(tab._usb_unindexed) == USB_UNINDEXED_MAX
        assert "c0.gcode" not in tab._usb_unindexed

    def test_copy_announced_after_settle_timeout_is_indexed(self, tab) -> None:
        self._done(tab)
        self._timeout(tab, sent=False)
        tab.remember.assert_not_called()
        PrintTab._on_usb_file_added(tab, {"path": "cube.gcode"})
        assert tab.remember.call_args.args[1:] == ("k", "cube.gcode")
        tab.jobStatusPage_widget.on_print_start.assert_not_called()

    def test_error_notifies_and_does_not_print(self, tab) -> None:
        self._done(tab, local="", error="Bad")
        assert tab._usb_pending is False
        tab.jobStatusPage_widget.on_print_start.assert_not_called()
        tab.notify.emit.assert_called_once_with(
            "PrintTab", "USB print failed: Bad", 2, True
        )

    @pytest.mark.parametrize(("from_console", "sent"), [(True, 1), (False, 0)])
    def test_import_error_reaches_console_only_if_started_there(
        self, tab, from_console, sent
    ) -> None:
        tab._usb_from_console = from_console
        self._done(tab, local="", error='No "space"')
        assert (
            self._responds(tab)
            == ["RESPOND TYPE=error MSG=\"USB print failed: No 'space'\""][:sent]
        )
        assert tab._usb_from_console is False

    def test_console_message_stays_one_gcode_line(self, tab) -> None:
        tab._usb_from_console = True
        self._done(tab, local="", error="a;b\nc")
        assert self._responds(tab) == [
            'RESPOND TYPE=error MSG="USB print failed: a,b c"'
        ]

    def test_refusal_after_copy_reaches_console(self, tab) -> None:
        tab._usb_from_console = True
        tab._print_state = "printing"
        self._done(tab, reused=True)
        assert self._responds(tab) == [
            'RESPOND TYPE=error MSG="USB print refused: A print is already running."'
        ]

    def test_klipper_shutdown_skips_console(self, tab) -> None:
        tab._usb_from_console = True
        tab.BasePopup_z_offset = MagicMock()
        tab.save_config_btn = MagicMock()
        tab.babystepPage = MagicMock()
        PrintTab.on_klippy_state(tab, "shutdown")
        assert self._responds(tab) == []

    @pytest.mark.parametrize("state", ["shutdown", "error", "disconnected"])
    def test_klipper_leaving_ready_aborts(self, tab, state) -> None:
        tab.BasePopup_z_offset = MagicMock()
        tab.save_config_btn = MagicMock()
        tab.babystepPage = MagicMock()
        PrintTab.on_klippy_state(tab, state)
        assert tab._usb_pending is False
        tab._usb_settle_timer.stop.assert_called_once()
        assert tab._usb_token == 2
        tab.notify.emit.assert_called_once_with(
            "PrintTab", f"USB print cancelled: Klipper is {state}.", 2, True
        )

    def test_standby_keeps_the_copy_loadscreen(self, tab) -> None:
        tab.on_cancel_print = MagicMock()
        tab._finish_print_handled = True
        tab._cancel_z_snapshot = 0.0
        PrintTab.on_print_stats_update(tab, "state", "standby")
        tab.call_load_panel.emit.assert_not_called()


class TestUsbRemovedLeavesStalePages:
    """Pulling the stick backs out of pages showing a file that is now gone."""

    def _tab(self, stack: list[str], confirm_dir: str, meta_path: str = ""):
        pages = {n: SimpleNamespace(name=n) for n in ("files", "confirm", "meta")}
        pages["confirm"].directory = confirm_dir
        pages["meta"].shown_path = meta_path
        tab = SimpleNamespace(
            confirmPage_widget=pages["confirm"],
            metadataPage_widget=pages["meta"],
            filesPage_widget=pages["files"],
            stack=[pages[n] for n in stack],
            isVisible=lambda: True,
            request_forget_pages=MagicMock(),
            _on_gone_drive=PrintTab._on_gone_drive,
        )
        tab.currentWidget = lambda: tab.stack[-1]
        tab.back_button = lambda: tab.stack.pop()
        tab.indexOf = lambda page: page.name
        tab.setCurrentIndex = MagicMock()
        return tab

    def _top(self, tab: SimpleNamespace) -> str:
        return tab.currentWidget().name

    def test_confirm_of_usb_file_goes_back(self) -> None:
        tab = self._tab(["files", "confirm"], "USB-BLOCKS")
        PrintTab.on_usb_removed(tab, "/home/blocks/printer_data/gcodes/USB-BLOCKS")
        assert self._top(tab) == "files"
        tab.request_forget_pages.emit.assert_called_once_with(0, ["confirm"])

    def test_metadata_over_usb_confirm_goes_back_twice(self) -> None:
        tab = self._tab(
            ["files", "confirm", "meta"], "USB-BLOCKS/sub", "USB-BLOCKS/sub/a.gcode"
        )
        PrintTab.on_usb_removed(tab, "")
        assert self._top(tab) == "files"
        tab.request_forget_pages.emit.assert_called_once_with(0, ["confirm", "meta"])

    @pytest.mark.parametrize(
        ("confirm_dir", "symlink"),
        [("", "USB-BLOCKS"), ("cubes", "USB-BLOCKS"), ("USB-OTHER", "USB-BLOCKS")],
    )
    def test_other_files_stay(self, confirm_dir, symlink) -> None:
        tab = self._tab(["files", "confirm"], confirm_dir)
        PrintTab.on_usb_removed(tab, symlink)
        assert self._top(tab) == "confirm"
        tab.request_forget_pages.emit.assert_not_called()

    def test_job_metadata_stays_over_stale_confirm(self) -> None:
        tab = self._tab(["files", "confirm", "meta"], "USB-BLOCKS", "cube.gcode")
        PrintTab.on_usb_removed(tab, "USB-BLOCKS")
        assert self._top(tab) == "meta"
        tab.request_forget_pages.emit.assert_called_once_with(0, ["confirm"])

    def test_left_via_header_shortcut_forgets_history(self) -> None:
        # Leaving the tab reset it, but global history still holds the confirm page.
        tab = self._tab(["files"], "USB-BLOCKS")
        tab.isVisible = lambda: False
        PrintTab.on_usb_removed(tab, "USB-BLOCKS")
        tab.setCurrentIndex.assert_not_called()
        tab.request_forget_pages.emit.assert_called_once_with(0, ["confirm"])

    def test_hidden_tab_resets_and_forgets_history(self) -> None:
        tab = self._tab(["files", "confirm"], "USB-BLOCKS")
        tab.isVisible = lambda: False
        PrintTab.on_usb_removed(tab, "USB-BLOCKS")
        tab.setCurrentIndex.assert_called_once_with("files")
        assert self._top(tab) == "confirm"
        tab.request_forget_pages.emit.assert_called_once_with(0, ["confirm"])
