import json
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from updater.models import ComponentStatus


@pytest.fixture
def page(qapp):
    """UpdatePage instance with all heavy UI deps mocked."""
    patches = [
        patch("BlocksScreen.lib.panels.widgets.updatePage.LoadingOverlayWidget"),
        patch("BlocksScreen.lib.panels.widgets.updatePage.BlocksCustomButton"),
        patch("BlocksScreen.lib.panels.widgets.updatePage.IconButton"),
    ]
    for p in patches:
        p.start()

    from BlocksScreen.lib.panels.widgets.updatePage import UpdatePage

    def _mock_setup(self):
        for attr in (
            "reload_btn",
            "update_all_btn",
            "update_back_btn",
            "_loadwidget",
            "_scroll_area",
            "_cards_layout",
            "_elapsed_time_label",
            "_progress_label",
            "_cancel_btn",
        ):
            setattr(self, attr, MagicMock())
        # build_cards() uses `while self._cards_layout.count():` to clear;
        # default MagicMock() is truthy, so force 0 to avoid infinite loop.
        self._cards_layout.count.return_value = 0
        self._font_family = "Arial"
        self._chevron_right = MagicMock()
        self._chevron_down = MagicMock()

    setup_patch = patch.object(UpdatePage, "_setupUI", _mock_setup)
    setup_patch.start()
    pg = UpdatePage()
    setup_patch.stop()
    pg._statuses = {}
    from PyQt6.QtWidgets import QFrame, QWidget

    pg._make_summary_row = MagicMock(return_value=QFrame())
    pg._make_details_widget = MagicMock(return_value=QWidget())

    yield pg

    for p in patches:
        p.stop()


def _make_payload(**overrides):
    defaults = dict(
        name="klipper",
        kind="git",
        commits_behind=0,
        current_hash="abc12345",
        current_version="v0.1.0",
        remote_version="v0.1.0",
        remote_url="",
        packages_upgradable=0,
        error=None,
        has_local_changes=False,
    )
    defaults.update(overrides)
    return json.dumps({"klipper": defaults})


def _make_status(**overrides: Any) -> ComponentStatus:
    defaults: dict[str, Any] = dict(
        name="klipper",
        kind="git",
        commits_behind=0,
        current_hash="abc12345",
        current_version="v0.1.0",
        remote_version="v0.1.1",
        remote_url="",
        packages_upgradable=0,
        error=None,
        has_local_changes=False,
    )
    defaults.update(overrides)
    return ComponentStatus(**defaults)


class TestNeedsUpdate:
    def test_commits_behind(self, page):
        assert page._needs_update(_make_status(commits_behind=1)) is True

    def test_packages_upgradable(self, page):
        assert page._needs_update(_make_status(packages_upgradable=5)) is True

    def test_errored_git_is_updatable(self, page):
        # An errored git repo (e.g. a corrupt repo) is now updatable: pressing
        # the one Update button heals it via the update flow.
        assert page._needs_update(_make_status(error="boom")) is True

    def test_errored_apt_not_updatable(self, page):
        s = _make_status(kind="apt", error="boom")
        assert page._needs_update(s) is False

    def test_has_local_changes(self, page):
        assert page._needs_update(_make_status(has_local_changes=True)) is True

    def test_up_to_date(self, page):
        assert page._needs_update(_make_status()) is False

    def test_apt_check_failed_not_updatable(self, page):
        # packages_upgradable == -1 means the apt status check failed; it must
        # not show as an available update (mirrors the daemon dirty-set's > 0).
        s = _make_status(kind="apt", packages_upgradable=-1)
        assert page._needs_update(s) is False


class TestVersionString:
    def test_git_current_and_remote(self, page):
        s = _make_status(current_version="v0.1.0", remote_version="v0.1.1")
        assert page._version_string(s) == "v0.1.0 → v0.1.1"

    def test_git_falls_back_to_hash_when_no_current_version(self, page):
        s = _make_status(
            current_version="", current_hash="deadbeef", remote_version="v0.1.1"
        )
        assert page._version_string(s) == "deadbeef → v0.1.1"

    def test_git_falls_back_to_unknown_when_no_remote(self, page):
        s = _make_status(current_version="v0.1.0", remote_version="")
        assert page._version_string(s) == "v0.1.0 → unknown"

    def test_system_returns_updates_available(self, page):
        s = _make_status(kind="system", packages_upgradable=12)
        assert page._version_string(s) == "updates available"


class TestBuildCards:
    def test_no_statuses_shows_no_information_label(self, page):
        page._statuses = {}
        page.build_cards()
        page._cards_layout.addWidget.assert_called_once()
        args = page._cards_layout.addWidget.call_args[0]
        from PyQt6.QtWidgets import QLabel

        assert isinstance(args[0], QLabel)
        assert "no update information" in args[0].text().lower()

    def test_all_clean_shows_up_to_date_label(self, page):
        page._statuses = {"klipper": _make_status(), "moonraker": _make_status()}
        page.build_cards()
        page._cards_layout.addWidget.assert_called_once()
        args = page._cards_layout.addWidget.call_args[0]
        from PyQt6.QtWidgets import QLabel

        assert isinstance(args[0], QLabel)
        assert "up to date" in args[0].text().lower()

    def test_no_statuses_hides_update_all_btn(self, page):
        page._statuses = {}
        page.build_cards()
        page.update_all_btn.setVisible.assert_called_with(False)

    def test_updatable_component_shows_update_all_btn(self, page):

        page._statuses = {"klipper": _make_status(commits_behind=3)}
        page.build_cards()
        page.update_all_btn.setVisible.assert_called_with(True)

    def test_card_added_per_updatable_component(self, page):
        from PyQt6.QtWidgets import QFrame

        page._statuses = {
            "klipper": _make_status(commits_behind=3),
            "moonraker": _make_status(commits_behind=1),
            "firmware": _make_status(),
        }
        page.build_cards()
        calls = [
            c
            for c in page._cards_layout.addWidget.call_args_list
            if isinstance(c[0][0], QFrame)
        ]
        assert len(calls) == 1

    def test_error_component_gets_card(self, page):
        from PyQt6.QtWidgets import QFrame

        page._statuses = {"klipper": _make_status(error="git error")}
        page.build_cards()
        calls = [
            c
            for c in page._cards_layout.addWidget.call_args_list
            if isinstance(c[0][0], QFrame)
        ]
        assert len(calls) == 1


class TestShowLoading:
    def test_loading_true_shows_loadwidget(self, page):
        page.show_loading(True)
        page._loadwidget.setVisible.assert_called_with(True)

    def test_loading_true_hides_scroll_area(self, page):
        page.show_loading(True)
        page._scroll_area.setVisible.assert_called_with(False)

    def test_loading_true_hides_update_all_btn(self, page):
        page.show_loading(True)
        page.update_all_btn.setVisible.assert_called_with(False)

    def test_loading_false_hides_loadwidget(self, page):
        page.show_loading(False)
        page._loadwidget.setVisible.assert_called_with(False)

    def test_loading_false_shows_scroll_area(self, page):
        page.show_loading(False)
        page._scroll_area.setVisible.assert_called_with(True)

    def test_loading_false_shows_btn_only_when_updates_avail(self, page):
        page._update_avail = True
        page.show_loading(False)
        page.update_all_btn.setVisible.assert_called_with(True)

    def test_loading_false_hides_btn_when_no_updates(self, page):
        page._update_avail = False
        page.show_loading(False)
        page.update_all_btn.setVisible.assert_called_with(False)


class TestHandleStatusReady:
    def test_updates_statuses_dict(self, page):
        page.build_cards = MagicMock()
        page.handle_status_ready(_make_payload(commits_behind=3))
        assert page._statuses["klipper"].commits_behind == 3

    def test_calls_build_cards(self, page):
        page.build_cards = MagicMock()
        page.handle_status_ready(_make_payload())
        page.build_cards.assert_called_once()

    def test_emits_update_available_true_when_commits_behind(self, page, qtbot):
        page.build_cards = MagicMock()
        with qtbot.waitSignal(page.update_available, timeout=200) as blocker:
            page.handle_status_ready(_make_payload(commits_behind=1))
        assert blocker.args == [True]

    def test_emits_update_available_false_when_up_to_date(self, page, qtbot):
        page.build_cards = MagicMock()
        with qtbot.waitSignal(page.update_available, timeout=200) as blocker:
            page.handle_status_ready(_make_payload())
        assert blocker.args == [False]

    def test_update_all_btn_show_when_updates_available(self, page):
        page.build_cards = MagicMock()
        page.handle_status_ready(_make_payload(commits_behind=1))
        page.update_all_btn.setVisible.assert_called_with(True)

    def test_update_all_btn_hidden_when_up_to_date(self, page):
        page.build_cards = MagicMock()
        page.handle_status_ready(_make_payload())
        page.update_all_btn.setVisible.assert_called_with(False)

    def test_emits_call_load_panel_false_after_update(self, page, qtbot):
        page.build_cards = MagicMock()
        page._post_update_status_pending = True
        with qtbot.waitSignal(page.call_load_panel, timeout=200) as blocker:
            page.handle_status_ready(_make_payload())
        assert blocker.args == [False, ""]
        assert page._post_update_status_pending is False

    def test_does_not_emit_call_load_panel_on_normal_refresh(self, page, qtbot):
        page.build_cards = MagicMock()
        page._post_update_status_pending = False
        with qtbot.assertNotEmitted(page.call_load_panel):
            page.handle_status_ready(_make_payload())


class TestHandleBusyChanged:
    def test_true_shows_loading(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page.show_loading.assert_called_once_with(True)

    def test_false_hides_loading(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(False)
        page.show_loading.assert_called_once_with(False)

    def test_false_emits_request_status(self, page, qtbot):
        page.show_loading = MagicMock()
        with qtbot.waitSignal(page.request_status, timeout=700):
            page.handle_busy_changed(False)

    def test_true_does_not_emit_request_status(self, page, qtbot):
        page.show_loading = MagicMock()
        with qtbot.assertNotEmitted(page.request_status):
            page.handle_busy_changed(True)

    def test_false_does_not_emit_call_load_panel_when_no_overlay(self, page, qtbot):
        page.show_loading = MagicMock()
        page._overlay_shown = False
        with qtbot.assertNotEmitted(page.call_load_panel, wait=200):
            page.handle_busy_changed(False)

    def test_false_emits_call_load_panel_when_overlay_shown(self, page, qtbot):
        page.show_loading = MagicMock()
        page._overlay_shown = True
        with qtbot.waitSignal(page.call_load_panel, timeout=200) as blocker:
            page.handle_busy_changed(False)
        assert blocker.args == [False, ""]
        assert page._overlay_shown is False

    def test_true_starts_elapsed_timer(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        assert page._elapsed_timer.isActive()
        assert page._elapsed_time_seconds == 0

    def test_true_shows_elapsed_time_label_and_cancel_btn(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page._elapsed_time_label.show.assert_called_once()
        page._cancel_btn.show.assert_called_once()

    def test_false_stops_elapsed_timer(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page.handle_busy_changed(False)
        assert not page._elapsed_timer.isActive()

    def test_false_hides_elapsed_time_label_and_cancel_btn(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page._elapsed_time_label.reset_mock()
        page._cancel_btn.reset_mock()
        page.handle_busy_changed(False)
        page._elapsed_time_label.hide.assert_called_once()
        page._cancel_btn.hide.assert_called_once()

    def test_true_starts_busy_timeout_timer(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        assert page._busy_timeout_timer.isActive()

    def test_false_stops_busy_timeout_timer(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page.handle_busy_changed(False)
        assert not page._busy_timeout_timer.isActive()


class TestUpdateAllClicked:
    def test_emits_request_update_with_empty_string(self, page, qtbot):
        # on_update_all_clicked shows a confirm dialog; _do_update fires the signal
        with qtbot.waitSignal(page.request_update, timeout=200) as blocker:
            page._do_update()
        assert blocker.args == [""]


class TestCancelButton:
    def test_cancel_btn_emits_request_cancel(self, page, qtbot):
        with qtbot.waitSignal(page.request_cancel, timeout=200):
            page._on_cancel_clicked()

    def test_cancel_btn_visible_only_when_busy(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page._cancel_btn.show.assert_called()
        page._cancel_btn.reset_mock()
        page.handle_busy_changed(False)
        page._cancel_btn.hide.assert_called()


class TestElapsedTimeCounter:
    def test_update_elapsed_time_increments_seconds(self, page):
        page._elapsed_time_seconds = 0
        page._update_elapsed_time()
        assert page._elapsed_time_seconds == 1

    def test_update_elapsed_time_formats_display(self, page):
        page._elapsed_time_seconds = (
            124  # Will be incremented to 125 (2 minutes, 5 seconds)
        )
        page._update_elapsed_time()
        page._elapsed_time_label.setText.assert_called_with("02:05")

    def test_elapsed_timer_starts_on_busy(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        assert page._elapsed_timer.isActive()

    def test_elapsed_timer_stops_on_not_busy(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page.handle_busy_changed(False)
        assert not page._elapsed_timer.isActive()

    def test_elapsed_time_resets_on_new_update(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page._elapsed_time_seconds = 100
        page.handle_busy_changed(False)
        page.handle_busy_changed(True)
        assert page._elapsed_time_seconds == 0


class TestHandleStepComplete:
    def test_emits_call_load_panel_with_step_message(self, page, qtbot):
        with qtbot.waitSignal(page.call_load_panel, timeout=200) as blocker:
            page.handle_step_complete("klipper", 1, 4)
        assert blocker.args == [True, "klipper: fetching"]
        page._progress_label.setText.assert_called_with("Step 1/4")

    def test_unknown_steps_falls_back_to_working(self, page, qtbot):
        with qtbot.waitSignal(page.call_load_panel, timeout=200) as blocker:
            page.handle_step_complete("moonraker", 99, 4)
        assert blocker.args == [True, "moonraker: working"]
        page._progress_label.setText.assert_called_with("Step 99/4")


class TestDaemonUnavailable:
    def test_daemon_unavailable_shows_toast(self, page, qtbot):
        page.show_loading = MagicMock()
        page._show_toast = MagicMock()
        page.handle_daemon_unavailable()
        page._show_toast.assert_called_once()
        args = page._show_toast.call_args[0]
        assert "unavailable" in args[0].lower()
        assert "restart" in args[0].lower()

    def test_daemon_unavailable_disables_update_btn(self, page):
        page.show_loading = MagicMock()
        page._show_toast = MagicMock()
        page.handle_daemon_unavailable()
        page.update_all_btn.setEnabled.assert_called_with(False)

    def test_daemon_unavailable_hides_loading(self, page):
        page.show_loading = MagicMock()
        page._show_toast = MagicMock()
        page.handle_daemon_unavailable()
        page.show_loading.assert_called_once_with(False)

    def test_daemon_unavailable_sets_busy_false(self, page):
        page.show_loading = MagicMock()
        page._show_toast = MagicMock()
        page._busy = True
        page.handle_daemon_unavailable()
        assert page._busy is False


class TestProgressLabelDisplay:
    def test_progress_label_shown_when_busy(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page._progress_label.show.assert_called_once()

    def test_progress_label_hidden_when_not_busy(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page._progress_label.reset_mock()
        page.handle_busy_changed(False)
        page._progress_label.hide.assert_called_once()

    def test_progress_label_cleared_at_start(self, page):
        page.show_loading = MagicMock()
        page.handle_busy_changed(True)
        page._progress_label.setText.assert_called_with("")


class TestErrorMessageActionability:
    def test_error_message_includes_retry_hint(self, page):
        page._show_toast = MagicMock()
        page.handle_error_occurred("klipper", "git connection timeout")
        msg = page._show_toast.call_args[0][0]
        assert "retry" in msg.lower()
        assert "klipper" in msg.lower()

    def test_error_toast_shows_failure_state(self, page):
        page._show_toast = MagicMock()
        page.handle_error_occurred("firmware", "checksum mismatch")
        msg = page._show_toast.call_args[0][0]
        assert "failed" in msg.lower()


class TestBadStatusPayload:
    def test_bad_payload_keeps_statuses_and_toasts(self, page):
        page._statuses = {"klipper": ComponentStatus(name="klipper")}
        page._show_toast = MagicMock()
        page.handle_status_ready("{not json")
        assert "klipper" in page._statuses
        page._show_toast.assert_called_once()


class TestConfirmPopupCleanup:
    def test_second_confirm_deletes_previous_popup(self, page):
        with patch("BlocksScreen.lib.panels.widgets.updatePage.BasePopup") as popup_cls:
            first = MagicMock()
            second = MagicMock()
            popup_cls.side_effect = [first, second]
            page._show_update_confirm()
            page._show_update_confirm()
        first.deleteLater.assert_called_once()
        second.deleteLater.assert_not_called()
