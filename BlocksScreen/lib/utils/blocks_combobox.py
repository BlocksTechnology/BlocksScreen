from __future__ import annotations

from PyQt6 import QtCore, QtGui, QtWidgets

# BlocksScreen accent (#1A8FBF)
_ACCENT = "26, 143, 191"

_STYLE = f"""
    QComboBox {{
        background-color: white;
        color: black;
        border: 1px solid rgba(0, 0, 0, 60);
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 22px;
        font-weight: 600;
    }}
    QComboBox QAbstractItemView::item {{ font-size: 22px; }}
    QComboBox::drop-down {{ border: none; width: 34px; }}
    QComboBox::down-arrow {{
        image: url(:/arrow_icons/media/btn_icons/arrow_down.svg);
        width: 18px;
        height: 18px;
    }}
    QComboBox QAbstractItemView {{
        background-color: white;
        color: black;
        selection-background-color: rgba({_ACCENT}, 0.6);
        selection-color: white;
        outline: none;
    }}
"""


class _TouchRowDelegate(QtWidgets.QStyledItemDelegate):
    """Enlarges popup rows so they meet touch-target sizing."""

    def sizeHint(self, option, index):
        """Row height at least 48px for finger taps."""
        size = super().sizeHint(option, index)
        size.setHeight(max(size.height(), 48))
        return size

    def initStyleOption(self, option, index):
        """Center popup row text horizontally."""
        super().initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter


class BlocksComboBox(QtWidgets.QComboBox):
    """QComboBox skinned to the app theme with touch-sized popup rows."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(_STYLE)
        self.setItemDelegate(_TouchRowDelegate(self))
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.setMaximumHeight(50)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Paint the combo with its current text horizontally centered."""
        painter = QtWidgets.QStylePainter(self)
        painter.setPen(QtCore.Qt.GlobalColor.black)
        opt = QtWidgets.QStyleOptionComboBox()
        self.initStyleOption(opt)
        text = opt.currentText
        opt.currentText = ""
        painter.drawComplexControl(QtWidgets.QStyle.ComplexControl.CC_ComboBox, opt)
        rect = self.style().subControlRect(
            QtWidgets.QStyle.ComplexControl.CC_ComboBox,
            opt,
            QtWidgets.QStyle.SubControl.SC_ComboBoxEditField,
            self,
        )
        painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, text)

    def set_options(self, options: list[str]) -> None:
        """Repopulate options, preserving the current selection when still present."""
        current = self.currentText()
        with QtCore.QSignalBlocker(self):
            self.clear()
            self.addItems(options)
            self.setCurrentIndex(max(self.findText(current), 0))
