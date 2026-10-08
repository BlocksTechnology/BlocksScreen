import typing

from lib.utils.blocks_combobox import BlocksComboBox
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.toggleAnimatedButton import ToggleAnimatedButton
from PyQt6 import QtCore, QtGui, QtWidgets

BOOLEAN_STATES = {
    "1": True,
    "yes": True,
    "true": True,
    "on": True,
    "0": False,
    "no": False,
    "false": False,
    "off": False,
}


class BlocksField(QtWidgets.QWidget):
    """Label row whose right side is a label, line edit, dropdown or toggle."""

    on_edit = QtCore.pyqtSignal(name="on-edit")
    clicked = QtCore.pyqtSignal(name="clicked")

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        left_text: str = "",
        line: typing.Literal["bottom", "upper"] | None = None,
        editable: typing.Literal["LineEdit", "DropDownMenu", "Toggle"] | None = None,
    ) -> None:
        super().__init__(parent)
        self.line = line
        self.editable = editable
        self.default_stylesheet = "color: rgb(255,255,255);"
        self._setup_field(left_text)

    def _create_right_widget(self) -> QtWidgets.QWidget:
        if self.editable == "LineEdit":
            font = QtGui.QFont()
            font.setPointSize(13)
            lineedit = BlocksCustomLinEdit(self)
            lineedit.editingFinished.connect(self.on_edit)
            lineedit.clicked.connect(self.clicked)
            lineedit.setMinimumSize(QtCore.QSize(150, 50))
            lineedit.setFont(font)
            lineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            lineedit.textChanged.connect(self._sync_static_label)
            return lineedit
        if self.editable == "DropDownMenu":
            combo = BlocksComboBox(self, open_up=True)
            combo.setMinimumSize(QtCore.QSize(150, 50))
            combo.activated.connect(self.on_edit)
            combo.currentIndexChanged.connect(self._sync_static_label)
            return combo
        if self.editable == "Toggle":
            toggle = ToggleAnimatedButton(self)
            toggle.setMinimumSize(QtCore.QSize(100, 50))
            toggle.stateChange.connect(self.on_edit)
            toggle.stateChange.connect(self._sync_static_label)
            return toggle
        return self._create_label()

    def _create_label(self) -> QtWidgets.QLabel:
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

        # Read-only stand-in shown instead of the editor when not editable.
        self._static_lbl = None
        self._right = self._create_right_widget()
        if self.editable is not None:
            self._static_lbl = self._create_label()
            self._static_lbl.hide()

        center = QtCore.Qt.AlignmentFlag.AlignCenter
        self._left_lbl.setAlignment(center)
        for lbl in (self._right, self._static_lbl):
            if isinstance(lbl, QtWidgets.QLabel):
                lbl.setAlignment(center)

        row = QtWidgets.QHBoxLayout()
        row.addWidget(self._left_lbl, 1, center)
        row.addWidget(self._right, 1, center)
        if self._static_lbl is not None:
            row.addWidget(self._static_lbl, 1, center)

        sep = None
        if self.line is not None:
            sep = QtWidgets.QFrame(self)
            sep.setFixedHeight(1)
            sep.setStyleSheet("background-color: rgba(255, 255, 255, 50);")

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
        """Set the right text; a Toggle takes config booleans like "true"/"off"."""
        if self.editable == "DropDownMenu":
            raise TypeError("set_right_text() is not supported for DropDownMenu")
        if self.editable == "Toggle":
            states = BOOLEAN_STATES
            self.set_checked(states.get(text.strip().lower(), False))
            return
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

    def set_checked(self, checked: bool) -> None:
        """Set the toggle state without emitting on_edit."""
        self._require("Toggle", "set_checked")
        with QtCore.QSignalBlocker(self._right):
            self._right.state = ToggleAnimatedButton.State(checked)
        self._sync_static_label()

    def is_checked(self) -> bool:
        """Return True when the toggle is on."""
        self._require("Toggle", "is_checked")
        return self._right.state.value

    def text(self) -> str:
        """Return the current right-hand value; a Toggle gives "true"/"false"."""
        if isinstance(self._right, ToggleAnimatedButton):
            return "true" if self._right.state.value else "false"
        if isinstance(self._right, QtWidgets.QComboBox):
            return self._right.currentText()
        return self._right.text()

    def _sync_static_label(self) -> None:
        if self._static_lbl is None:
            return
        text = self.text()
        if isinstance(self._right, ToggleAnimatedButton):
            text = "On" if self._right.state.value else "Off"
        if not text and isinstance(self._right, QtWidgets.QComboBox):
            text = self._right.placeholderText()
        self._static_lbl.setText(text)

    def set_editable(self, editable: bool) -> None:
        """set editable true or false (changes widget to label if False)"""
        if self._static_lbl is None:
            return
        self._sync_static_label()
        self._right.setVisible(editable)
        self._static_lbl.setVisible(not editable)

    def select_option(self, text: str) -> bool:
        """Select the dropdown option matching text."""
        self._require("DropDownMenu", "select_option")
        return self._right.select_option(text)
