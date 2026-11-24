"""Unit tests for NotificationPage's unread-notification dot signal."""

import importlib.machinery
import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PyQt6 import QtWidgets

# tests/panels/conftest.py and tests/network/conftest.py stub sys.modules
# entries under "lib.*" with fakes (no teardown) when collected in the same
# xdist worker; evict notificationPage's whole dependency closure first so
# we load the real BlocksScreen/lib modules instead of another file's stubs.
for _stale_key in (
    "lib",
    "lib.panels",
    "lib.panels.widgets",
    "lib.panels.widgets.MainWindow.notificationPage",
    "lib.panels.widgets.Common.popupDialogWidget",
    "lib.utils",
    "lib.utils.blocks_button",
    "lib.utils.blocks_frame",
    "lib.utils.icon_button",
    "lib.utils.list_model",
):
    sys.modules.pop(_stale_key, None)

_bs_lib_dir = Path(__file__).resolve().parent.parent.parent / "BlocksScreen" / "lib"
_lib_spec = importlib.machinery.ModuleSpec("lib", loader=None, is_package=True)
_lib_spec.submodule_search_locations = [str(_bs_lib_dir)]
sys.modules["lib"] = importlib.util.module_from_spec(_lib_spec)

from lib.panels.widgets.MainWindow.notificationPage import NotificationPage  # noqa: E402

_notification_page_module = sys.modules[NotificationPage.__module__]


def _mock_setup(self) -> None:
    self.notification_list_view = QtWidgets.QListView()
    for attr in (
        "back_btn",
        "delete_btn",
        "delete_all_btn",
        "header_title",
        "type_label",
        "time_label",
    ):
        setattr(self, attr, MagicMock())


@pytest.fixture
def page(qtbot):
    with (
        patch.object(_notification_page_module, "Popup", MagicMock()),
        patch.object(NotificationPage, "_setup_ui", _mock_setup),
    ):
        pg = NotificationPage()
    qtbot.addWidget(pg)
    return pg


def test_new_notification_sets_dot(page, qtbot):
    with qtbot.waitSignal(page.has_new_notification, timeout=200) as blocker:
        page.new_notication("test", "hello", 1, False)
    assert blocker.args == [True]


def test_show_notification_panel_clears_dot(page, qtbot):
    # show_notification_panel() no-ops without a parent; stub one out.
    page.parent = MagicMock(return_value=MagicMock())
    with qtbot.waitSignal(page.has_new_notification, timeout=200) as blocker:
        page.show_notification_panel()
    assert blocker.args == [False]


def test_new_notification_while_open_does_not_set_dot(page, qtbot):
    page.show()
    with qtbot.waitSignal(page.has_new_notification, timeout=200) as blocker:
        page.new_notication("test", "hello", 1, False)
    assert blocker.args == [False]


def test_reset_view_model_clears_dot(page, qtbot):
    page.new_notication("test", "hello", 1, False)
    with qtbot.waitSignal(page.has_new_notification, timeout=200) as blocker:
        page.reset_view_model()
    assert blocker.args == [False]


def test_retract_removes_entry_and_clears_dot(page, qtbot):
    page.new_notication("amu", "gone", 2, False)
    with qtbot.waitSignal(page.has_new_notification, timeout=200) as blocker:
        page.retract_notification("gone")
    assert blocker.args == [False]
    assert page.model.entries == []


def test_retract_keeps_other_entries_and_selection(page):
    page.show()
    page.new_notication("x", "stay", 1, False)
    page.new_notication("amu", "gone", 2, False)
    page.new_notication("x", "newest", 1, False)
    page._select_row(2)
    selected = page.selected_item
    page.retract_notification("gone")
    page.retract_notification("missing")
    assert [e.text for e in page.model.entries] == ["newest", "stay"]
    assert page.selected_item is selected
    assert page.entry_delegate.prev_index == 1


def test_retract_selected_entry_selects_newest(page):
    page.show()
    page.new_notication("amu", "gone", 2, False)
    page.new_notication("x", "stay", 1, False)
    page._select_row(1)
    page.retract_notification("gone")
    assert page.selected_item is page.model.entries[0]


def test_delete_selected_selects_newest(page):
    page.show()
    page.new_notication("x", "old", 1, False)
    page.new_notication("x", "mid", 1, False)
    page.new_notication("x", "new", 1, False)
    page._select_row(1)
    page.delete_selected_item()
    assert [e.text for e in page.model.entries] == ["new", "old"]
    assert page.selected_item is page.model.entries[0]
    assert page.entry_delegate.prev_index == 0


def test_error_popup_stays_longer_than_info(page):
    page.new_notication(message="boom", priority=3, popup=True)
    page.new_notication(message="hello", priority=1, popup=True)
    timeouts = [c.kwargs["timeout"] for c in page.popup.new_message.call_args_list]
    assert timeouts == [10000, 3000]


_Popup = sys.modules["lib.panels.widgets.Common.popupDialogWidget"].Popup


@pytest.fixture
def popup(qtbot):
    p = _Popup(None)
    qtbot.addWidget(p)
    return p


def test_popup_repeat_while_shown_is_dropped(popup):
    popup.new_message(message="Print Not Started")
    popup.new_message(message="Print Not Started")
    assert popup.isShown
    assert len(popup.messages) == 0


def test_popup_repeat_while_queued_is_dropped(popup):
    popup.new_message(message="first")
    popup.new_message(message="second")
    popup.new_message(message="second")
    assert [m["message"] for m in popup.messages] == ["second"]


def test_popup_same_message_after_dismiss_shows_again(popup):
    popup.new_message(message="Print Not Started")
    popup.slide_in_animation.stop()  # slide-out only runs after slide-in ends
    popup.hide()
    assert not popup.isShown
    popup.new_message(message="Print Not Started")
    assert popup.isShown
    assert popup.text_label.text() == "Print Not Started"


def test_popup_repeat_while_sliding_out_shows_after_hide(popup, qtbot):
    popup.new_message(message="Print Not Started")
    popup.slide_in_animation.stop()
    popup.slide_out_animation.start()
    popup.new_message(message="Print Not Started")
    assert [m["message"] for m in popup.messages] == ["Print Not Started"]
    popup.hide()
    qtbot.waitUntil(lambda: popup.isShown, timeout=1000)
    assert popup.text_label.text() == "Print Not Started"


def test_popup_outside_tap_close_then_repeat_shows(popup):
    popup.new_message(message="Print Not Started")
    popup.close()  # Qt closes a WindowType.Popup on any tap outside it
    assert not popup.isShown
    popup.new_message(message="Print Not Started")
    assert popup.isVisible()
    assert popup.text_label.text() == "Print Not Started"


def test_popup_repeat_while_shown_rearms_timeout(popup):
    popup.new_message(message="Print Not Started", timeout=10000)
    popup.timeout_timer = MagicMock()
    popup.timeout_timer.isActive.return_value = False  # still sliding in
    popup.new_message(message="Print Not Started")
    popup.timeout_timer.start.assert_not_called()
    popup.timeout_timer.isActive.return_value = True
    popup.new_message(message="Print Not Started")
    popup.timeout_timer.start.assert_called_once_with()


def test_popup_queued_message_waits_after_outside_tap_close(popup, qtbot):
    popup.new_message(_Popup.MessageType.ERROR, "A")
    popup.new_message(_Popup.MessageType.ERROR, "B")
    popup.close()  # the tap that closes A must not also close B
    QtWidgets.QApplication.processEvents()
    assert not popup.isShown
    qtbot.waitUntil(lambda: popup.isShown, timeout=2000)
    assert popup.text_label.text() == "B"


def test_popup_message_arriving_in_delay_window_waits(popup, qtbot):
    popup.new_message(_Popup.MessageType.ERROR, "A")
    popup.new_message(_Popup.MessageType.ERROR, "B")
    popup.close()
    popup.new_message(_Popup.MessageType.ERROR, "C")
    assert not popup.isShown
    qtbot.waitUntil(lambda: popup.isShown, timeout=2000)
    assert popup.text_label.text() == "B"
    assert [m["message"] for m in popup.messages] == ["C"]
