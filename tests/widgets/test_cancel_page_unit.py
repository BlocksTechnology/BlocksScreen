"""Unit tests for CancelPage reason headers (cancelPage.py)"""

import pytest
from PyQt6 import QtWidgets

from BlocksScreen.lib.panels.widgets.MainWindow.cancelPage import CancelPage


@pytest.fixture
def page(qtbot):
    parent = QtWidgets.QWidget()
    qtbot.addWidget(parent)
    yield CancelPage(parent)


@pytest.mark.parametrize(
    ("state", "text"),
    [
        ("complete", "Print Finished"),
        ("error", "Print Error"),
        ("cancelled", "Print Cancelled"),
    ],
)
def test_finish_state_sets_reason(page, state, text):
    page.on_print_stats_update("state", state)
    assert page.cf_info_tf.text() == text


def test_printing_clears_previous_reason(page):
    page.on_print_stats_update("state", "complete")
    page.on_print_stats_update("state", "printing")
    assert page.cf_info_tf.text() == ""


@pytest.mark.parametrize("state", ["paused", "standby"])
def test_other_states_keep_reason(page, state):
    page.on_print_stats_update("state", "error")
    page.on_print_stats_update("state", state)
    assert page.cf_info_tf.text() == "Print Error"


def test_filename_update_does_not_touch_reason(page):
    page.on_print_stats_update("state", "cancelled")
    page.on_print_stats_update("filename", "part.gcode")
    assert page.filename == "part.gcode"
    assert page.cf_info_tf.text() == "Print Cancelled"


@pytest.mark.parametrize("button", ["confirm_button", "refuse_button"])
def test_close_resets_the_file_before_signalling_hidden(page, button):
    # MainWindow restarts Klipper on hidden; SDCARD_RESET_FILE must go out first.
    page.parentWidget().show()
    page.show()
    events = []
    page.run_gcode.connect(lambda g: events.append(g))
    page.hidden.connect(lambda: events.append("hidden"))
    getattr(page, button).click()
    assert events == ["SDCARD_RESET_FILE", "hidden"]
