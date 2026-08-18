"""Unit tests for EntryDelegate press/release handling: drag slop, expand arrow, row selection."""

import importlib.util
import sys
from pathlib import Path

import pytest
from PyQt6 import QtCore, QtGui, QtWidgets

# tests/network/conftest.py swaps in a list_model stub, so load the real file by path.
_MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "BlocksScreen"
    / "lib"
    / "utils"
    / "list_model.py"
)
_spec = importlib.util.spec_from_file_location("_list_model_under_test", _MODULE_PATH)
_list_model = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
sys.modules[_spec.name] = _list_model
_spec.loader.exec_module(_list_model)  # type: ignore[union-attr]

EntryDelegate = _list_model.EntryDelegate
EntryListModel = _list_model.EntryListModel
ListItem = _list_model.ListItem

ROW_H = 60
ROW_W = 480


def _event(kind, x, y):
    """A left-button mouse event at a widget-local point."""
    pos = QtCore.QPointF(x, y)
    return QtGui.QMouseEvent(
        kind,
        pos,
        pos,
        QtCore.Qt.MouseButton.LeftButton,
        QtCore.Qt.MouseButton.LeftButton,
        QtCore.Qt.KeyboardModifier.NoModifier,
    )


def _press(x, y):
    """Press at a point."""
    return _event(QtCore.QEvent.Type.MouseButtonPress, x, y)


def _release(x, y):
    """Release at a point."""
    return _event(QtCore.QEvent.Type.MouseButtonRelease, x, y)


def _option(row=0):
    """The style option the view would hand the delegate for a given row."""
    option = QtWidgets.QStyleOptionViewItem()
    option.rect = QtCore.QRect(0, row * ROW_H, ROW_W, ROW_H)
    return option


def _arrow_center(option):
    """Centre of the expand arrow, mirroring the hit-test geometry in _toggle_expand."""
    size = ROW_H * 0.8
    margin = (ROW_H - size) / 2
    return (option.rect.right() - margin - size / 2, option.rect.top() + ROW_H / 2)


@pytest.fixture
def delegate(qapp):
    d = EntryDelegate()
    yield d
    d.deleteLater()


@pytest.fixture
def model(qapp):
    items = [
        ListItem(text="A", height=ROW_H),
        ListItem(text="B", height=ROW_H),
    ]
    m = EntryListModel(items)
    yield m
    m.deleteLater()


def _tap(delegate, model, row, x, y, option=None):
    """Full press+release at one point, returning the editorEvent result of the release."""
    option = option or _option(row)
    index = model.index(row)
    delegate.editorEvent(_press(x, y), model, option, index)
    return delegate.editorEvent(_release(x, y), model, option, index)


class TestNotClickable:
    def test_press_and_release_swallowed(self, delegate, model):
        model.entries[0].not_clickable = True
        selected = []
        delegate.item_selected.connect(selected.append)
        option, index = _option(0), model.index(0)
        assert delegate.editorEvent(_press(10, 10), model, option, index) is True
        assert delegate.editorEvent(_release(10, 10), model, option, index) is True
        assert selected == []
        assert model.data(index, EntryListModel.EnableRole) is False


class TestSelection:
    def test_press_alone_does_not_select(self, delegate, model):
        selected = []
        delegate.item_selected.connect(selected.append)
        assert (
            delegate.editorEvent(_press(10, 10), model, _option(0), model.index(0))
            is False
        )
        assert selected == []

    def test_tap_selects_row_and_emits(self, delegate, model):
        selected = []
        delegate.item_selected.connect(selected.append)
        assert _tap(delegate, model, 0, 10, 10) is True
        assert [i.text for i in selected] == ["A"]
        assert model.data(model.index(0), EntryListModel.EnableRole) is True

    def test_tap_runs_callback(self, delegate, model):
        calls = []
        model.entries[0].callback = lambda: calls.append(1)
        _tap(delegate, model, 0, 10, 10)
        assert calls == [1]

    def test_selecting_second_row_deselects_first(self, delegate, model):
        _tap(delegate, model, 0, 10, 10)
        _tap(delegate, model, 1, 10, ROW_H + 10, _option(1))
        assert model.data(model.index(0), EntryListModel.EnableRole) is False
        assert model.data(model.index(1), EntryListModel.EnableRole) is True
        assert delegate.prev_index == 1


class TestDragSlop:
    def test_drag_release_is_not_a_tap(self, delegate, model):
        selected = []
        delegate.item_selected.connect(selected.append)
        calls = []
        model.entries[0].callback = lambda: calls.append(1)
        option, index = _option(0), model.index(0)
        slop = QtWidgets.QApplication.startDragDistance() * 2
        delegate.editorEvent(_press(10, 10), model, option, index)
        drag = _release(10, 10 + slop + 5)
        assert delegate.editorEvent(drag, model, option, index) is False
        assert selected == []
        assert calls == []

    def test_small_drift_still_taps(self, delegate, model):
        option, index = _option(0), model.index(0)
        delegate.editorEvent(_press(10, 10), model, option, index)
        assert delegate.editorEvent(_release(11, 11), model, option, index) is True

    def test_release_without_press_still_taps(self, delegate, model):
        # A release with no recorded origin (view stole the press) must not be dropped.
        assert (
            delegate.editorEvent(_release(10, 10), model, _option(0), model.index(0))
            is True
        )


class TestExpandArrow:
    def _expandable(self, model):
        """Mark row 0 as an expandable entry that actually overflows."""
        model.entries[0].allow_expand = True
        model.entries[0].needs_expansion = True

    def test_arrow_tap_toggles_and_skips_callback(self, delegate, model):
        self._expandable(model)
        calls = []
        model.entries[0].callback = lambda: calls.append(1)
        option = _option(0)
        x, y = _arrow_center(option)
        assert _tap(delegate, model, 0, x, y, option) is True
        assert model.data(model.index(0), EntryListModel.ExpandRole) is True
        assert calls == []

    def test_arrow_tap_toggles_back(self, delegate, model):
        self._expandable(model)
        option = _option(0)
        x, y = _arrow_center(option)
        _tap(delegate, model, 0, x, y, option)
        _tap(delegate, model, 0, x, y, option)
        assert model.data(model.index(0), EntryListModel.ExpandRole) is False

    def test_tap_off_arrow_selects_instead(self, delegate, model):
        self._expandable(model)
        selected = []
        delegate.item_selected.connect(selected.append)
        assert _tap(delegate, model, 0, 10, 10) is True
        assert model.data(model.index(0), EntryListModel.ExpandRole) is False
        assert [i.text for i in selected] == ["A"]

    def test_arrow_ignored_when_expansion_not_needed(self, delegate, model):
        model.entries[0].allow_expand = True
        model.entries[0].needs_expansion = False
        option = _option(0)
        x, y = _arrow_center(option)
        assert _tap(delegate, model, 0, x, y, option) is True
        assert model.data(model.index(0), EntryListModel.ExpandRole) is False
