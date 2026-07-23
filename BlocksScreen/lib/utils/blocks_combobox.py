"""Themed, touch-friendly combobox matching the BlocksScreen accent theme."""

from __future__ import annotations

from PyQt6 import QtCore, QtWidgets

# BlocksScreen accent (#1A8FBF), matching the existing network VLAN selector.
_ACCENT = "26, 143, 191"

_STYLE = f"""
    QComboBox {{
        background-color: rgba({_ACCENT}, 0.05);
        color: rgba(255, 255, 255, 200);
        border: 1px solid rgba(255, 255, 255, 80);
        border-radius: 8px;
        padding: 4px 12px;
    }}
    QComboBox::drop-down {{ border: none; width: 34px; }}
    QComboBox::down-arrow {{
        image: url(:/arrow_icons/media/btn_icons/arrow_down.svg);
        width: 18px;
        height: 18px;
    }}
    QComboBox QAbstractItemView {{
        background-color: rgb(40, 40, 40);
        color: white;
        selection-background-color: rgba({_ACCENT}, 0.6);
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


class BlocksComboBox(QtWidgets.QComboBox):
    """QComboBox skinned to the app theme with touch-sized popup rows."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(_STYLE)
        self.setItemDelegate(_TouchRowDelegate(self))
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.setMaximumHeight(50)

    def set_options(self, options: list[str]) -> None:
        """Repopulate options, preserving the current selection when still present."""
        current = self.currentText()
        with QtCore.QSignalBlocker(self):
            self.clear()
            self.addItems(options)
            self.setCurrentIndex(max(self.findText(current), 0))
