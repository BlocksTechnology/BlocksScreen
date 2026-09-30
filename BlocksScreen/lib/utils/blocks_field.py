import typing

from lib.utils.blocks_combobox import BlocksComboBox
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksField(QtWidgets.QWidget):
    """Label row whose right side is a label, line edit or dropdown."""

    on_edit = QtCore.pyqtSignal(name="on-edit")

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        left_text: str = "",
        line: typing.Literal["bottom", "upper"] | None = None,
        editable: typing.Literal["LineEdit", "DropDownMenu"] | None = None,
    ) -> None:
        super().__init__(parent)
        self.line = line
        self.editable = editable
        self.default_stylesheet = "color: rgb(255,255,255);"
        self._setup_field(left_text)

    def _create_right_widget(self) -> QtWidgets.QWidget:
        if self.editable == "LineEdit":
            lineedit = BlocksCustomLinEdit(self)
            lineedit.editingFinished.connect(self.on_edit)
            return lineedit
        if self.editable == "DropDownMenu":
            combo = BlocksComboBox(self, open_up=True)
            combo.setMinimumSize(QtCore.QSize(150, 50))
            combo.activated.connect(self.on_edit)
            return combo
        lbl = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(13)
        lbl.setFont(font)
        lbl.setStyleSheet(self.default_stylesheet)
        return lbl

    def _setup_field(self, left_text: str) -> None:
        box = QtWidgets.QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)

        font = QtGui.QFont()
        font.setPointSize(15)
        self._left_lbl = QtWidgets.QLabel(left_text, self)
        self._left_lbl.setFont(font)
        self._left_lbl.setStyleSheet(self.default_stylesheet)

        self._right = self._create_right_widget()

        center = QtCore.Qt.AlignmentFlag.AlignCenter
        self._left_lbl.setAlignment(center)
        if isinstance(self._right, QtWidgets.QLabel):
            self._right.setAlignment(center)

        row = QtWidgets.QHBoxLayout()
        row.addWidget(self._left_lbl, 1, center)
        row.addWidget(self._right, 1, center)

        sep = None
        if self.line is not None:
            sep = QtWidgets.QFrame(self)
            sep.setFrameShape(QtWidgets.QFrame.Shape.HLine)
            sep.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        if sep and self.line == "upper":
            box.addWidget(sep)
        box.addLayout(row, 1)
        if sep and self.line == "bottom":
            box.addWidget(sep)

    def _require(self, kind: str | None, method: str) -> None:
        if self.editable != kind:
            raise TypeError(
                f"{method}() needs editable={kind!r}, got {self.editable!r}"
            )

    def set_left_text(self, text: str) -> None:
        """Set the text of the left label."""
        self._left_lbl.setText(text)

    def set_right_text(self, text: str) -> None:
        """Set the right text"""
        if self.editable == "DropDownMenu":
            raise TypeError("set_right_text() is not supported for DropDownMenu")
        self._right.setText(text)

    def set_right_stylesheet(self, stylesheet: str) -> None:
        """Set the stylesheet of the right-hand label ."""
        self._require(None, "set_right_stylesheet")
        self._right.setStyleSheet(stylesheet)

    def set_options(self, options: list[str]) -> None:
        """Replace the dropdown's options."""
        self._require("DropDownMenu", "set_options")
        self._right.set_options(options)

    def set_placeholder(self, text: str) -> None:
        """Show text when nothing is selected."""
        self._require("DropDownMenu", "set_placeholder")
        self._right.setPlaceholderText(text)

    def text(self) -> str:
        """Return the current right-hand value."""
        if isinstance(self._right, QtWidgets.QComboBox):
            return self._right.currentText()
        return self._right.text()

    def select_option(self, text: str) -> bool:
        """Select the dropdown option matching text."""
        self._require("DropDownMenu", "select_option")
        return self._right.select_option(text)
