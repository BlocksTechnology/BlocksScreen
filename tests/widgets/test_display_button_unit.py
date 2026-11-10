"""Unit tests for DisplayButton text setters (display_button.py)"""

import pytest

from BlocksScreen.lib.utils.display_button import DisplayButton


@pytest.fixture()
def button(qtbot, monkeypatch):
    """DisplayButton whose update() calls are counted in button.calls."""
    w = DisplayButton()
    qtbot.addWidget(w)
    w.calls = []
    monkeypatch.setattr(w, "update", lambda: w.calls.append(1))
    return w


@pytest.mark.parametrize("setter", ["setText", "setSecondaryText", "secondary_text"])
def test_unchanged_text_skips_update(button, setter):
    def put(value):
        if setter == "secondary_text":
            button.secondary_text = value
        else:
            getattr(button, setter)(value)

    put("215")
    put("215")
    assert button.calls == [1]
    put("216")
    assert button.calls == [1, 1]


def test_set_text_keeps_qt_text_in_sync(button):
    button.setText("12")
    assert button.text() == "12"
    assert super(DisplayButton, button).text() == "12"
