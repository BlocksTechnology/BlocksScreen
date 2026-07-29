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
