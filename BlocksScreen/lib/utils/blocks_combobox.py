from __future__ import annotations

from PyQt6 import QtCore, QtGui, QtWidgets

_ACCENT = "26, 143, 191"
# Shared by the title and the popup rows.
_FONT_PX = 22

_STYLE = f"""
    QComboBox {{
        background-color: rgba({_ACCENT}, 0.20);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 4px 12px;
        font-size: {_FONT_PX}px;
    }}
    QComboBox QAbstractItemView::item {{
        font-size: {_FONT_PX}px;
        border-radius: 12px;
        padding: 6px;
        margin: 2px 4px;
        color: white;
        background-color: transparent;
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: rgba({_ACCENT}, 0.90);
    }}
    QComboBox::drop-down {{ border: none; width: 0px; }}
    QComboBox::down-arrow {{ image: none; }}
    QComboBox QAbstractItemView {{
        background-color: #10242E;
        color: white;
        border: none;
        padding: 4px;
        selection-background-color: rgba({_ACCENT}, 0.90);
        selection-color: white;
        outline: none;
    }}
    QComboBox QAbstractItemView QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0px;
    }}
    QComboBox QAbstractItemView QScrollBar::handle:vertical {{
        background: rgba({_ACCENT}, 0.8);
        border-radius: 4px;
        min-height: 24px;
    }}
    QComboBox QAbstractItemView QScrollBar::add-line:vertical,
    QComboBox QAbstractItemView QScrollBar::sub-line:vertical {{ height: 0px; }}
"""


class _TouchRowDelegate(QtWidgets.QStyledItemDelegate):
    """Touch-sized popup rows."""

    def sizeHint(self, option, index):
        """At least 48px tall for finger taps."""
        size = super().sizeHint(option, index)
        size.setHeight(max(size.height(), 48))
        return size

    def initStyleOption(self, option, index):
        """Center rows at the title's font size."""
        super().initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter
        option.font.setPixelSize(_FONT_PX)


class BlocksComboBox(QtWidgets.QComboBox):
    """Themed QComboBox with touch-sized rows."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        # ::item stylesheet rules need a real QListView.
        self.setView(QtWidgets.QListView(self))
        self.setStyleSheet(_STYLE)
        self.setItemDelegate(_TouchRowDelegate(self))
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.setMaximumHeight(50)

    def showPopup(self) -> None:
        """Open the list below the button, never above."""
        super().showPopup()
        popup = self.findChild(QtWidgets.QFrame)
        if popup is not None:
            # Opaque square fill: no white corners without a compositor.
            popup.setStyleSheet("background: #10242E;")
            below = self.mapToGlobal(self.rect().bottomLeft()).y()
            popup.move(popup.x(), below)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Paint with the current text centered."""
        painter = QtWidgets.QStylePainter(self)
        painter.setPen(QtCore.Qt.GlobalColor.white)
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
        """Replace options, keeping the selection if still present."""
        current = self.currentText()
        with QtCore.QSignalBlocker(self):
            self.clear()
            self.addItems(options)
            self.setCurrentIndex(max(self.findText(current), 0))
