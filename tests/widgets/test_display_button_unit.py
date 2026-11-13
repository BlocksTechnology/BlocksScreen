"""Unit tests for DisplayButton text setters (display_button.py)"""

import importlib.util
from pathlib import Path

import pytest

from BlocksScreen.lib.utils.display_button import DisplayButton

_UTILS = Path(__file__).resolve().parents[2] / "BlocksScreen" / "lib" / "utils"


def _real(mod: str):
    """Load a utils module by path, since other test files stub it in sys.modules."""
    spec = importlib.util.spec_from_file_location(f"_db_{mod}", _UTILS / f"{mod}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


@pytest.mark.parametrize("name", ["icon_pixmap", "secondary_pixmap", "display_format"])
def test_visual_properties_repaint(button, name):
    button.setProperty(name, None)
    assert button.calls == [1]


def test_inner_pixmap_repaints_without_progress(qtbot, monkeypatch):
    from PyQt6 import QtGui

    bar = _real("blocks_progressbar").CustomProgressBar()
    qtbot.addWidget(bar)
    calls = []
    monkeypatch.setattr(bar, "update", lambda: calls.append(1))
    pix = QtGui.QPixmap(8, 8)
    bar.set_inner_pixmap(pix)
    assert calls == [1]


def test_label_background_follows_margins(qtbot):
    label = _real("blocks_label").BlocksLabel(None)
    qtbot.addWidget(label)
    label.resize(100, 40)
    label.grab()
    first = label._path_rect
    label.setContentsMargins(5, 5, 5, 5)
    label.grab()
    assert label._path_rect == first.adjusted(5, 5, -5, -5)
