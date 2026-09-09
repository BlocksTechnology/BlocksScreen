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
    "lib.panels.widgets.notificationPage",
    "lib.panels.widgets.popupDialogWidget",
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

from lib.panels.widgets.notificationPage import NotificationPage  # noqa: E402

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
        patch.object(NotificationPage, "_setupUI", _mock_setup),
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
