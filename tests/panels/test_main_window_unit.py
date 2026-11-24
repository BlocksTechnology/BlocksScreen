"""Unit test for MainWindow._on_klippy_state auto-restart guard"""

from collections import deque
from types import MethodType, SimpleNamespace
from unittest.mock import MagicMock

import pytest

from BlocksScreen.lib.panels.mainWindow import MainWindow


def _make_fake_window(
    *, manual_restart_pending: bool = False, ws_connected: bool = True
) -> SimpleNamespace:
    win = SimpleNamespace(
        _klippy_ready=False,
        _klippy_state=None,
        _klippy_settled_state=None,
        _update_in_progress=False,
        _klipper_auto_restart_pending=False,
        _post_update_reconnect=False,
        _klipper_restart_timeout=MagicMock(),
        _klipper_disconnect_grace=MagicMock(),
        updater_worker=MagicMock(),
        conn_window=SimpleNamespace(manual_restart_pending=manual_restart_pending),
        loadwidget=MagicMock(),
        loadscreen=MagicMock(),
        ws=MagicMock(connected=ws_connected),
        _try_device_config_restart=MagicMock(),
        _prompt_device_confirmation=MagicMock(),
        _device_restart_pending=False,
        _config_reload_on_ready=False,
    )
    win._begin_klipper_restart = MethodType(MainWindow._begin_klipper_restart, win)
    return win


class TestEstopCancelsUpdate:
    @pytest.mark.parametrize(
        ("states", "cancels"),
        [
            (["ready", "shutdown"], True),
            (["ready", "disconnected", "startup", "shutdown"], True),
            (["shutdown", "disconnected", "shutdown"], False),
            (["shutdown", "startup", "shutdown"], False),
            (["shutdown"], False),
        ],
    )
    def test_only_ready_to_shutdown_cancels(self, states, cancels) -> None:
        win = _make_fake_window()
        win._update_in_progress = True
        for state in states:
            MainWindow._on_klippy_state(win, state)
        assert win.updater_worker.trigger_cancel.called is cancels


class TestKlippyDisconnectedAutoRestartGuard:
    def test_disconnected_only_arms_grace(self) -> None:
        # RESTART and SAVE_CONFIG pass through disconnected for about a second
        fake_window = _make_fake_window()

        MainWindow._on_klippy_state(fake_window, "disconnected")

        fake_window._klipper_disconnect_grace.start.assert_called_once()
        fake_window.ws.api.restart_service.assert_not_called()

    @pytest.mark.parametrize("state", ["startup", "ready", "shutdown", "error"])
    def test_leaving_disconnected_cancels_grace(self, state) -> None:
        fake_window = _make_fake_window()

        MainWindow._on_klippy_state(fake_window, state)

        fake_window._klipper_disconnect_grace.stop.assert_called_once()
        fake_window._klipper_disconnect_grace.start.assert_not_called()

    def test_auto_restarts_once_grace_expires(self) -> None:
        fake_window = _make_fake_window()

        MainWindow._auto_restart_klipper(fake_window)

        fake_window.ws.api.restart_service.assert_called_once_with("klipper")
        fake_window.loadscreen.show.assert_called_once()
        assert fake_window._klipper_auto_restart_pending is True

    @pytest.mark.parametrize(
        ("manual_restart_pending", "ws_connected"), [(True, True), (False, False)]
    )
    def test_skips_auto_restart(self, manual_restart_pending, ws_connected) -> None:
        fake_window = _make_fake_window(
            manual_restart_pending=manual_restart_pending, ws_connected=ws_connected
        )

        MainWindow._auto_restart_klipper(fake_window)

        fake_window.ws.api.restart_service.assert_not_called()
        fake_window.loadscreen.show.assert_not_called()
        assert fake_window._klipper_auto_restart_pending is False


# Panel indices used by the print-tab invariant fixtures.
_MAIN_PAGE_IDX = 0
_JOB_STATUS_IDX = 3


def _make_nav_window(print_state: str) -> SimpleNamespace:
    """Fake window wired so the print-tab navigation guards run against it."""
    print_panel = MagicMock()
    print_panel.indexOf.side_effect = lambda w: {
        print_panel.print_page: _MAIN_PAGE_IDX,
        print_panel.jobStatusPage_widget: _JOB_STATUS_IDX,
    }[w]
    print_tab = object()
    main_content = MagicMock()
    main_content.indexOf.side_effect = lambda w: 0 if w is print_tab else -1
    win = SimpleNamespace(
        _print_state=print_state,
        printPanel=print_panel,
        filamentPanel=MagicMock(),
        main_content_widget=main_content,
        printTab=print_tab,
    )
    for name in (
        "_is_job_active",
        "_print_tab_index",
        "_job_status_index",
        "_main_print_index",
        "_guard_print_panel",
        "reset_tab_indexes",
    ):
        setattr(win, name, MethodType(getattr(MainWindow, name), win))
    return win


class TestPrintTabInvariant:
    """A job (printing OR paused) must keep the print tab off the main page."""

    @pytest.mark.parametrize(
        ("state", "expected"),
        [("printing", True), ("paused", True), ("standby", False), ("complete", False)],
    )
    def test_is_job_active(self, state, expected) -> None:
        assert _make_nav_window(state)._is_job_active() is expected

    def test_guard_redirects_main_page_when_paused(self) -> None:
        win = _make_nav_window("paused")
        assert win._guard_print_panel(0, _MAIN_PAGE_IDX) == _JOB_STATUS_IDX

    def test_guard_keeps_main_page_when_idle(self) -> None:
        win = _make_nav_window("standby")
        assert win._guard_print_panel(0, _MAIN_PAGE_IDX) == _MAIN_PAGE_IDX

    def test_guard_leaves_other_pages_untouched(self) -> None:
        win = _make_nav_window("paused")
        assert win._guard_print_panel(0, _JOB_STATUS_IDX) == _JOB_STATUS_IDX

    def test_reset_tab_indexes_holds_job_status_when_paused(self) -> None:
        win = _make_nav_window("paused")
        win.reset_tab_indexes()
        win.printPanel.setCurrentIndex.assert_called_once_with(_JOB_STATUS_IDX)


def _make_device_window(**state) -> SimpleNamespace:
    """Fake window running the real device-config prompt/restart methods."""
    win = SimpleNamespace(
        _klippy_state="ready",
        _klippy_settled_state="ready",
        _print_state="standby",
        _print_state_known=True,
        print_status="idle",
        _popup_toggle=False,
        _update_in_progress=False,
        _klipper_auto_restart_pending=False,
        _device_restart_pending=False,
        _finish_screen_hold=False,
        _reprint_hold=MagicMock(**{"isActive.return_value": False}),
        _config_reload_on_ready=False,
        _klippy_ready=True,
        _post_update_reconnect=False,
        _klipper_disconnect_grace=MagicMock(),
        updater_worker=MagicMock(),
        _pending_device_confirm=[],
        _device_confirm_names=[],
        _klipper_restart_timeout=MagicMock(),
        loadwidget=MagicMock(),
        loadscreen=MagicMock(),
        ws=MagicMock(),
        device_config_accepted=MagicMock(),
        device_config_declined=MagicMock(),
        _show_device_confirmation=MagicMock(),
        cancelpage=MagicMock(),
        width=lambda: 800,
        height=lambda: 480,
    )
    win.__dict__.update(state)
    for name in (
        "_is_job_active",
        "request_klipper_restart",
        "_device_restart_blocked",
        "_try_device_config_restart",
        "_begin_klipper_restart",
        "on_device_config_changed",
        "on_device_confirmation_required",
        "_device_prompt_blocked",
        "_prompt_device_confirmation",
        "_on_device_config_accept",
        "_on_device_config_decline",
        "_track_print_state",
        "_on_klippy_state",
        "_on_reprint_requested",
        "_release_finish_screen_hold",
        "_show_cancel_page_if_operational",
        "handle_cancel_print",
    ):
        setattr(win, name, MethodType(getattr(MainWindow, name), win))
    return win


class TestDeviceConfigRestart:
    def test_restarts_klipper_service_when_idle(self) -> None:
        win = _make_device_window()
        win.ws.api.restart_service.return_value = True
        win.on_device_config_changed(["amu"])
        win.ws.api.restart_service.assert_called_once_with("klipper")
        assert win._device_restart_pending is False
        # marked like the auto-restart so "disconnected" doesn't restart again
        assert win._klipper_auto_restart_pending is True

    @pytest.mark.parametrize(
        "state",
        [
            {"_print_state": "printing"},
            {"_print_state": "paused"},
            {"print_status": "printing"},
            {"_klippy_state": None},
            {"_print_state_known": False},
            {"_update_in_progress": True},
            {"_klipper_auto_restart_pending": True},
        ],
    )
    def test_deferred_while_unsafe(self, state) -> None:
        win = _make_device_window(**state)
        win.request_klipper_restart()
        win.ws.api.restart_service.assert_not_called()
        assert win._device_restart_pending is True

    def test_klipper_not_ready_needs_no_print_state(self) -> None:
        win = _make_device_window(_klippy_state="error", _print_state_known=False)
        win.ws.api.restart_service.return_value = True
        win.request_klipper_restart()
        win.ws.api.restart_service.assert_called_once_with("klipper")

    def test_retried_after_moonraker_was_disconnected(self) -> None:
        win = _make_device_window()
        win.ws.api.restart_service.return_value = False
        win.request_klipper_restart()
        assert win._device_restart_pending is True
        win.ws.api.restart_service.return_value = True
        win._try_device_config_restart()  # e.g. on websocket connected
        assert win._device_restart_pending is False
        assert win.ws.api.restart_service.call_count == 2

    def test_deferred_restart_runs_when_print_ends(self) -> None:
        win = _make_device_window(_print_state="complete")
        win.request_klipper_restart()
        win.ws.api.restart_service.assert_called_once_with("klipper")


class TestDeviceRestartAfterJob:
    """A job's end must keep its finished screen; the restart waits until it closes."""

    @pytest.fixture(autouse=True)
    def _sync_single_shot(self, monkeypatch) -> None:
        monkeypatch.setattr(
            "BlocksScreen.lib.panels.mainWindow.QtCore.QTimer.singleShot",
            lambda _ms, fn: fn(),
        )

    def _finished(self, end_state: str = "complete") -> SimpleNamespace:
        win = _make_device_window(_print_state="printing")
        win.ws.api.restart_service.return_value = True
        win.request_klipper_restart()
        if end_state != "cancelled":
            # jobStatusPage asks for the screen before MainWindow sees the state.
            win.handle_cancel_print(True)
        win._track_print_state("state", end_state)
        return win

    @pytest.mark.parametrize("end_state", ["complete", "error"])
    def test_held_while_finished_screen_open(self, end_state) -> None:
        win = self._finished(end_state)
        win.cancelpage.show.assert_called_once()
        win._try_device_config_restart()  # e.g. the PrintComplete event retry
        win._track_print_state("state", "standby")  # another client's reset
        win.ws.api.restart_service.assert_not_called()

    def test_cancelled_opens_no_screen_restarts_at_once(self) -> None:
        win = self._finished("cancelled")
        win.ws.api.restart_service.assert_called_once_with("klipper")

    def test_screen_skipped_while_klippy_not_ready_releases_hold(self) -> None:
        win = _make_device_window(_print_state="printing", _klippy_ready=False)
        win.ws.api.restart_service.return_value = True
        win.request_klipper_restart()
        win.handle_cancel_print(True)
        win._track_print_state("state", "error")
        win.cancelpage.show.assert_not_called()
        win.ws.api.restart_service.assert_called_once_with("klipper")
        assert win._finish_screen_hold is False

    def test_runs_once_screen_closes(self) -> None:
        win = self._finished()
        win._release_finish_screen_hold()  # cancelpage.hidden
        win._release_finish_screen_hold()
        win.ws.api.restart_service.assert_called_once_with("klipper")
        assert win._device_restart_pending is False

    def test_hide_request_closes_the_page(self) -> None:
        win = self._finished()
        win.handle_cancel_print(False)
        win.cancelpage.hide.assert_called_once()

    def test_reprint_does_not_restart_under_new_job(self) -> None:
        win = self._finished()
        win._reprint_hold.isActive.return_value = True
        win._on_reprint_requested("cube.gcode")
        win._reprint_hold.start.assert_called_once()
        win._release_finish_screen_hold()
        win._track_print_state("state", "standby")
        win._track_print_state("state", "printing")
        win._reprint_hold.stop.assert_called_once()
        win.ws.api.restart_service.assert_not_called()

    def test_refused_reprint_restarts_after_hold(self) -> None:
        win = self._finished()
        win._reprint_hold.isActive.return_value = True
        win._on_reprint_requested("cube.gcode")
        win._release_finish_screen_hold()
        win.ws.api.restart_service.assert_not_called()
        win._reprint_hold.isActive.return_value = False
        win._try_device_config_restart()  # hold timeout
        win.ws.api.restart_service.assert_called_once_with("klipper")

    def test_job_not_seen_running_restarts_at_once(self) -> None:
        # UI started on a finished job: jobStatusPage opens no screen.
        win = _make_device_window(_print_state="standby")
        win.ws.api.restart_service.return_value = True
        win._track_print_state("state", "complete")
        win.request_klipper_restart()
        win.ws.api.restart_service.assert_called_once_with("klipper")

    @pytest.mark.parametrize("held, says", [(True, True), (False, False)])
    def test_prompt_says_restart_waits_for_screen(self, held, says) -> None:
        win = _make_device_window(_finish_screen_hold=held, _device_config_popup=None)
        win._pending_device_confirm = ["amu"]
        popup = MagicMock(**{"isVisible.return_value": False})
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "BlocksScreen.lib.panels.mainWindow.BasePopup", lambda *a, **k: popup
            )
            MainWindow._show_device_confirmation(win)
        msg = popup.set_message.call_args.args[0]
        assert ("print-finished screen is closed" in msg) is says


class TestDeviceRestartAfterShutdown:
    """A service restart cannot clear an MCU shutdown; the operator's Firmware Restart reloads the config."""

    @pytest.mark.parametrize("change_first", [True, False])
    def test_firmware_restart_loads_config_no_second_restart(
        self, change_first
    ) -> None:
        win = _make_device_window()
        win.ws.api.restart_service.return_value = True
        if change_first:
            win._print_state = "printing"
            win.request_klipper_restart()
            win._on_klippy_state("shutdown")
        else:
            win._on_klippy_state("shutdown")
            win.request_klipper_restart()
        win._print_state = "error"
        win._try_device_config_restart()
        for state in ("disconnected", "startup", "ready"):
            win._on_klippy_state(state)
        win.ws.api.restart_service.assert_not_called()
        assert win._device_restart_pending is False

    def test_change_during_startup_still_restarts(self) -> None:
        # Klipper may have read printer.cfg before the write: restart once ready.
        win = _make_device_window()
        win.ws.api.restart_service.return_value = True
        win._on_klippy_state("shutdown")
        win._on_klippy_state("startup")
        win.request_klipper_restart()
        win.ws.api.restart_service.assert_called_once_with("klipper")


class TestDeviceConfirmationPrompt:
    def test_prompt_shown_when_idle(self) -> None:
        win = _make_device_window()
        win.on_device_confirmation_required(["amu"])
        win._show_device_confirmation.assert_called_once()

    @pytest.mark.parametrize(
        "state",
        [
            {"_print_state": "printing"},
            {"_popup_toggle": True},
            {"_update_in_progress": True},
        ],
    )
    def test_prompt_held_while_blocked(self, state) -> None:
        win = _make_device_window(**state)
        win.on_device_confirmation_required(["amu"])
        win._show_device_confirmation.assert_not_called()
        assert win._pending_device_confirm == ["amu"]

    def test_accept_and_decline_emit_the_asked_names(self) -> None:
        win = _make_device_window(_device_confirm_names=["amu"])
        win._on_device_config_accept()
        win.device_config_accepted.emit.assert_called_once_with(["amu"])
        assert win._device_confirm_names == []
        win._device_confirm_names = ["amu"]
        win._on_device_config_decline()
        win.device_config_declined.emit.assert_called_once_with(["amu"])


def test_real_confirmation_popup_opens_and_accepts(qtbot, monkeypatch) -> None:
    import importlib.util
    import pathlib
    import sys

    from PyQt6 import QtWidgets

    # conftest stubs lib.panels.widgets.Common.basePopup; load the real widget here.
    path = (
        pathlib.Path(__file__).parents[2]
        / "BlocksScreen/lib/panels/widgets/Common/basePopup.py"
    )
    spec = importlib.util.spec_from_file_location("_real_basePopup", path)
    real = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(real)
    monkeypatch.setattr(sys.modules[MainWindow.__module__], "BasePopup", real.BasePopup)

    class _Host(QtWidgets.QMainWindow):
        # BasePopup needs a real widget parent; borrow the real method.
        _show_device_confirmation = MainWindow._show_device_confirmation

    host = _Host()
    qtbot.addWidget(host)
    host._device_config_popup = None
    host._finish_screen_hold = False
    host._device_confirm_names = []
    host._pending_device_confirm = ["amu"]
    host._on_device_config_accept = MagicMock()
    host._on_device_config_decline = MagicMock()

    host._show_device_confirmation()
    popup = host._device_config_popup
    assert popup.isVisible()
    assert host._device_confirm_names == ["amu"]
    assert host._pending_device_confirm == []
    # another device while it's open: same popup, names appended, not replaced
    host._pending_device_confirm = ["beacon"]
    host._show_device_confirmation()
    assert host._device_config_popup is popup
    assert host._device_confirm_names == ["amu", "beacon"]
    popup.accept()
    host._on_device_config_accept.assert_called_once()
    host._on_device_config_decline.assert_not_called()


def test_cancel_page_leaves_loadscreen_alone() -> None:
    # The page doubles as the reprint prompt; an end-of-print macro may still own the loadscreen.
    win = SimpleNamespace(
        _klippy_ready=True,
        cancelpage=MagicMock(),
        loadscreen=MagicMock(),
        width=lambda: 800,
        height=lambda: 480,
    )

    MainWindow._show_cancel_page_if_operational(win)

    win.loadscreen.hide.assert_not_called()
    win.cancelpage.show.assert_called_once()


def _make_update_overlay_window() -> SimpleNamespace:
    update_page = object()
    win = _make_device_window(
        _update_in_progress=True,
        _post_update_reconnect=False,
        update_page=update_page,
        sender=lambda: update_page,
        filamentPanel=None,
        controlPanel=None,
        printPanel=None,
        utilitiesPanel=None,
        isVisible=lambda: True,
        _early_loadscreen=None,
    )
    win._apply_loadscreen = MethodType(MainWindow._apply_loadscreen, win)
    win.ws.api.restart_service.return_value = True
    return win


@pytest.mark.parametrize("show, restarts", [(False, 1), (True, 0)])
def test_update_overlay_dismiss_retries_deferred_restart(
    monkeypatch, show, restarts
) -> None:
    # On the first update the boot sync's restart is deferred and nothing else retries it.
    monkeypatch.setattr(
        "BlocksScreen.lib.panels.mainWindow.QtCore.QTimer.singleShot",
        lambda _ms, fn: fn(),
    )
    win = _make_update_overlay_window()
    win.request_klipper_restart()
    win.ws.api.restart_service.assert_not_called()

    MainWindow.show_loadscreen(win, show, "")

    assert win.ws.api.restart_service.call_count == restarts
    assert win._device_restart_pending is (restarts == 0)


def test_update_overlay_before_first_show_waits_for_window() -> None:
    # UI started mid-update: the busy replay lands before main_window.show().
    win = _make_update_overlay_window()
    visible = False
    win.isVisible = lambda: visible
    win._flush_early_loadscreen = MethodType(MainWindow._flush_early_loadscreen, win)

    MainWindow.show_loadscreen(win, True, "Update in progress ...")
    win.loadscreen.show.assert_not_called()

    visible = True
    win._flush_early_loadscreen()
    win.loadwidget.set_status_message.assert_called_once_with("Update in progress ...")
    win.loadscreen.show.assert_called_once()

    # A request made after the show wins over a stale pre-show one.
    win._early_loadscreen = (False, "")
    MainWindow.show_loadscreen(win, True, "Finishing installation ...")
    win._flush_early_loadscreen()
    win.loadscreen.hide.assert_not_called()


@pytest.mark.parametrize("state", ["ready", "shutdown", "disconnected"])
def test_notify_klippy_reaches_klippy_status(state) -> None:
    # Old route rebound api_reference to a str, so [0] gave "n": _handle_n_message
    win = SimpleNamespace(klippy_status=MagicMock())
    win._handle_notify_klippy_message = MethodType(
        MainWindow._handle_notify_klippy_message, win
    )
    method = f"notify_klippy_{state}"
    event = SimpleNamespace(method=method, data={"method": method}, metadata=None)

    MainWindow.messageReceivedEvent(win, event)

    win.klippy_status.on_klippy_notify.assert_called_once_with(state)


def _route_win() -> SimpleNamespace:
    win = SimpleNamespace(klippy_status=MagicMock(), _handle_server_message=MagicMock())
    win._handle_notify_klippy_message = MethodType(
        MainWindow._handle_notify_klippy_message, win
    )
    return win


def test_notify_klippy_routes_without_data() -> None:
    win = _route_win()
    event = SimpleNamespace(method="notify_klippy_ready", data={}, metadata=None)
    MainWindow.messageReceivedEvent(win, event)
    win.klippy_status.on_klippy_notify.assert_called_once_with("ready")


def test_other_methods_route_by_namespace() -> None:
    win = _route_win()
    event = SimpleNamespace(method="server.files.list", data={"x": 1}, metadata="m")
    MainWindow.messageReceivedEvent(win, event)
    win._handle_server_message.assert_called_once_with(
        "server.files.list", {"x": 1}, "m"
    )
    win.klippy_status.on_klippy_notify.assert_not_called()


def test_klippy_status_error_does_not_escape_the_event() -> None:
    win = _route_win()
    win.klippy_status.on_klippy_notify.side_effect = RuntimeError("render")
    event = SimpleNamespace(method="notify_klippy_shutdown", data={}, metadata=None)
    MainWindow.messageReceivedEvent(win, event)


def test_forget_pages_drops_only_that_tabs_entries() -> None:
    win = SimpleNamespace(index_stack=deque([[0, 1], [2, 3], [0, 3], [0, 4]], maxlen=4))
    MainWindow.forget_pages(win, 0, [3, 4])
    assert list(win.index_stack) == [[0, 1], [2, 3]]
    assert win.index_stack.maxlen == 4


def test_forget_pages_collapses_back_to_the_same_page() -> None:
    win = SimpleNamespace(index_stack=deque([[0, 1], [0, 3], [0, 1], [2, 0]], maxlen=4))
    MainWindow.forget_pages(win, 0, [3])
    assert list(win.index_stack) == [[0, 1], [2, 0]]


@pytest.mark.parametrize(
    ("method", "emits"),
    [("machine.update.status", True), ("machine.update.refresh", False)],
)
def test_only_status_reply_emits(method, emits) -> None:
    # Pins the old ("status" or "refresh") behaviour, which never matched refresh
    win = SimpleNamespace(on_update_message=MagicMock())
    MainWindow._handle_machine_message(win, method, {"version_info": {}}, None)
    assert win.on_update_message.emit.called is emits


@pytest.mark.parametrize(
    ("active_state", "sub_state", "notifies"),
    [
        ("active", "running", False),
        ("inactive", "dead", False),
        ("failed", "failed", True),
    ],
)
def test_service_state_notifies_only_on_failure(
    active_state, sub_state, notifies
) -> None:
    win = SimpleNamespace(_popup_toggle=False, show_notifications=MagicMock())
    params = [{"klipper": {"active_state": active_state, "sub_state": sub_state}}]
    MainWindow._handle_notify_service_state_changed_message(
        win, "notify_service_state_changed", {"params": params}, None
    )
    assert win.show_notifications.emit.called is notifies


@pytest.mark.parametrize(
    ("line", "pops"),
    [
        ("!! BlocksScreen: USB print refused: No filament", False),
        ("!! Machine is unloaded, please load the machine", True),
    ],
)
def test_own_console_echo_is_not_shown_twice(line, pops) -> None:
    # PrintTab already showed what it echoes; other clients still get the `!!` line.
    win = SimpleNamespace(
        gcode_response={list: MagicMock()},
        _popup_toggle=False,
        _emit_filtered_notification=MagicMock(),
    )
    MainWindow._handle_notify_gcode_response_message(
        win, "notify_gcode_response", {"params": [line]}, None
    )
    assert win._emit_filtered_notification.called is pops


@pytest.mark.parametrize(
    ("update", "reconnect", "drops"),
    [(False, False, True), (True, False, False), (False, True, False)],
)
def test_error_keeps_the_update_overlay(update, reconnect, drops) -> None:
    win = SimpleNamespace(
        _update_in_progress=update,
        _post_update_reconnect=reconnect,
        show_loadscreen=MagicMock(),
        in_case_error=MagicMock(),
    )
    MainWindow._clear_overlay_for_error(win)
    assert win.show_loadscreen.called is drops
    win.in_case_error.emit.assert_called_once()
