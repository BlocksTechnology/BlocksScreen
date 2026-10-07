"""EntryDelegate press/release: drag slop, expand arrow, selection."""

import importlib.util
import sys
from pathlib import Path

import pytest
from PyQt6 import QtCore, QtGui, QtWidgets

# tests/network/conftest.py stubs list_model; load the real file.
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
    return _event(QtCore.QEvent.Type.MouseButtonPress, x, y)


def _release(x, y):
    return _event(QtCore.QEvent.Type.MouseButtonRelease, x, y)


def _option(row=0):
    """Style option the view passes for *row*."""
    option = QtWidgets.QStyleOptionViewItem()
    option.rect = QtCore.QRect(0, row * ROW_H, ROW_W, ROW_H)
    return option


def _arrow_center(option):
    """Arrow centre, mirroring the _toggle_expand hit-test."""
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
    """Press and release at one point; returns the release result."""
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
        # A release with no recorded press (the view took it) still counts.
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


class TestNeedsExpansion:
    def _size_hint(self, delegate, text):
        item = ListItem(text=text, height=ROW_H)
        model = EntryListModel([item])
        delegate.sizeHint(_option(0), model.index(0))
        return item

    def test_short_single_line_fits(self, delegate):
        assert self._size_hint(delegate, "A").needs_expansion is False

    def test_more_lines_than_row_holds_needs_expansion(self, delegate):
        text = "\n".join("line" for _ in range(20))
        assert self._size_hint(delegate, text).needs_expansion is True

    def test_overflow_uses_paint_text_width(self, delegate):
        item = ListItem(text="", height=ROW_H, left_icon=QtGui.QPixmap(1, 1))
        row = QtCore.QRect(0, 0, ROW_W, int(ROW_H * 1.1))
        width = int(EntryDelegate._text_rect(item, row, 0).width())
        fm = _option(0).fontMetrics
        fits = "x"
        while fm.horizontalAdvance(fits + "x") <= width:
            fits += "x"
        model = EntryListModel([item])
        for text, expected in ((fits, False), (fits + "x", True)):
            item.text = text
            delegate.sizeHint(_option(0), model.index(0))
            assert item.needs_expansion is expected

    @pytest.mark.parametrize(
        "option_rect",
        [
            QtCore.QRect(0, 0, ROW_W, ROW_H),
            # A real QListView passes the whole viewport, not the row.
            QtCore.QRect(0, 0, 498, 284),
        ],
    )
    def test_line_count_limit_is_the_collapsed_row(self, delegate, option_rect):
        option = QtWidgets.QStyleOptionViewItem()
        option.rect = option_rect
        item = ListItem(text="", height=ROW_H)
        row = QtCore.QRect(0, 0, option_rect.width(), int(ROW_H * 1.1))
        text_h = int(EntryDelegate._text_rect(item, row, 0).height())
        max_lines = max(1, text_h // option.fontMetrics.lineSpacing())
        model = EntryListModel([item])
        for count, expected in ((max_lines, False), (max_lines + 1, True)):
            item.text = "\n".join("x" * count)
            delegate.sizeHint(option, model.index(0))
            assert item.needs_expansion is expected


class TestCollapsedLines:
    def test_lines_that_fit_are_kept(self):
        assert EntryDelegate._collapsed_lines("a\nb", 2) == ["a", "b"]

    def test_overflow_folds_into_last_line(self):
        assert EntryDelegate._collapsed_lines("a\nb\nc\nd", 2) == ["a", "b c d"]

    def test_single_line_row_joins_everything(self):
        assert EntryDelegate._collapsed_lines("a\nb", 1) == ["a b"]

    def test_blank_overflow_lines_are_dropped(self):
        assert EntryDelegate._collapsed_lines("a\n\n\nb", 1) == ["a b"]
        assert EntryDelegate._collapsed_lines("a\nb\n \nc", 2) == ["a", "b c"]


class _RecordingPainter(QtGui.QPainter):
    """Real painter that also records every drawText call."""

    def __init__(self, device):
        super().__init__(device)
        self.calls = []

    def drawText(self, *args):
        self.calls.append(args)
        super().drawText(*args)


def _paint(delegate, item):
    """Paint *item* at its sizeHint size; return the recorded drawText calls."""
    model = EntryListModel([item])
    size = delegate.sizeHint(_option(0), model.index(0))
    option = QtWidgets.QStyleOptionViewItem()
    option.rect = QtCore.QRect(QtCore.QPoint(0, 0), size)
    image = QtGui.QImage(size, QtGui.QImage.Format.Format_ARGB32)
    painter = _RecordingPainter(image)
    try:
        delegate.paint(painter, option, model.index(0))
    finally:
        painter.end()
    return painter.calls


class TestPaint:
    def test_collapsed_row_folds_overflow_into_elided_last_line(self, delegate):
        item = ListItem(text="\n".join(f"line {i}" for i in range(20)), height=ROW_H)
        [(rect, _flags, text)] = _paint(delegate, item)
        drawn = text.split("\n")
        max_lines = max(
            1, int(rect.height()) // QtGui.QFontMetrics(QtGui.QFont()).lineSpacing()
        )
        assert item.needs_expansion is True
        assert len(drawn) == max_lines
        assert drawn[:-1] == [f"line {i}" for i in range(max_lines - 1)]
        assert drawn[-1].endswith("…")

    def test_right_text_clears_the_elided_main_text(self, delegate):
        # Narrow glyphs elide flush to the rect edge, so only the gap separates them.
        item = ListItem(
            text="i" * 500,
            right_text="123 KB",
            height=ROW_H,
            left_icon=QtGui.QPixmap(1, 1),
        )
        [(rect, _flags, text), (x, _y, right)] = _paint(delegate, item)
        fm = QtGui.QFontMetrics(QtGui.QFont())
        assert right == "123 KB"
        assert text.endswith("…")
        assert x - (rect.left() + fm.horizontalAdvance(text)) >= 5

    def test_right_text_keeps_its_dev_position(self, delegate):
        item = ListItem(text="A", right_text="123 KB", height=ROW_H)
        [_main, (x, _y, _right)] = _paint(delegate, item)
        rt_w = QtGui.QFontMetrics(QtGui.QFont()).horizontalAdvance("123 KB")
        # Row inset 2, arrow slot 0.9 * height, 10px margin.
        assert x == pytest.approx(ROW_W - 1 - 2 - 0.9 * ROW_H - rt_w - 10, abs=1)

    def test_text_size_hint_fits_is_painted_whole(self, delegate):
        # Left font set, right font not: both must derive the right font the same way.
        item = ListItem(text="", right_text="123 KB", _lfontsize=20, height=ROW_H)
        model = EntryListModel([item])
        fits = ""
        while True:
            item.text = fits + "x"
            delegate.sizeHint(_option(0), model.index(0))
            if item.needs_expansion:
                break
            fits += "x"
        item.text = fits
        [(_rect, _flags, painted), _right] = _paint(delegate, item)
        assert painted == fits
