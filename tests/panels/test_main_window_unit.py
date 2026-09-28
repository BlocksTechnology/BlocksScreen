"""Unit test for MainWindow._on_klippy_state auto-restart guard"""

from types import MethodType, SimpleNamespace
from unittest.mock import MagicMock

import pytest

from BlocksScreen.lib.panels.mainWindow import MainWindow


def _make_fake_window(*, manual_restart_pending: bool) -> SimpleNamespace:
    return SimpleNamespace(
        _klippy_ready=False,
        _update_in_progress=False,
        _klipper_auto_restart_pending=False,
        _post_update_reconnect=False,
        _klipper_restart_timeout=MagicMock(),
        updater_worker=MagicMock(),
        conn_window=SimpleNamespace(manual_restart_pending=manual_restart_pending),
        loadwidget=MagicMock(),
        loadscreen=MagicMock(),
        ws=MagicMock(),
        _try_device_config_restart=MagicMock(),
        _prompt_device_confirmation=MagicMock(),
    )


class TestKlippyDisconnectedAutoRestartGuard:
    def test_auto_restarts_when_no_manual_restart_pending(self) -> None:
        fake_window = _make_fake_window(manual_restart_pending=False)

        MainWindow._on_klippy_state(fake_window, "disconnected")

        fake_window.ws.api.restart_service.assert_called_once_with("klipper")
        fake_window.loadscreen.show.assert_called_once()
        assert fake_window._klipper_auto_restart_pending is True

    def test_skips_auto_restart_when_manual_restart_pending(self) -> None:
        fake_window = _make_fake_window(manual_restart_pending=True)

        MainWindow._on_klippy_state(fake_window, "disconnected")

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
        ui=SimpleNamespace(main_content_widget=main_content, printTab=print_tab),
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
        _print_state="standby",
        _print_state_known=True,
        print_status="idle",
        _popup_toggle=False,
        _update_in_progress=False,
        _klipper_auto_restart_pending=False,
        _device_restart_pending=False,
        _pending_device_confirm=[],
        _device_confirm_names=[],
        _klipper_restart_timeout=MagicMock(),
        loadwidget=MagicMock(),
        loadscreen=MagicMock(),
        ws=MagicMock(),
        device_config_accepted=MagicMock(),
        device_config_declined=MagicMock(),
        _show_device_confirmation=MagicMock(),
    )
    win.__dict__.update(state)
    for name in (
        "_is_job_active",
        "request_klipper_restart",
        "_device_restart_blocked",
        "_try_device_config_restart",
        "on_device_config_changed",
        "on_device_confirmation_required",
        "_device_prompt_blocked",
        "_prompt_device_confirmation",
        "_on_device_config_accept",
        "_on_device_config_decline",
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
        win = _make_device_window(_print_state="printing")
        win.request_klipper_restart()
        win.ws.api.restart_service.assert_not_called()
        win._print_state = "complete"
        win.ws.api.restart_service.return_value = True
        win._try_device_config_restart()
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

    # conftest stubs lib.panels.widgets.basePopup; load the real widget here.
    path = (
        pathlib.Path(__file__).parents[2]
        / "BlocksScreen/lib/panels/widgets/basePopup.py"
    )
    spec = importlib.util.spec_from_file_location("_real_basePopup", path)
    real = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(real)
    monkeypatch.setattr(
        sys.modules[MainWindow.__module__], "BasePopup", real.BasePopup
    )

    class _Host(QtWidgets.QMainWindow):
        # BasePopup needs a real widget parent; borrow the real method.
        _show_device_confirmation = MainWindow._show_device_confirmation

    host = _Host()
    qtbot.addWidget(host)
    host._device_config_popup = None
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
