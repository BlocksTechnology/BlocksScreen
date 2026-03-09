import typing

from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

_LOWERCASE = list("qwertyuiopasdfghjklzxcvbnm")
_UPPERCASE = list("QWERTYUIOPASDFGHJKLZXCVBNM")
_NUMBERS = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "@",
    "#",
    "$",
    '"',
    "&&",
    "*",
    "-",
    "+",
    "=",
    "(",
    ")",
    "!",
    ":",
    ";",
    "'",
    "?",
]
_SYMBOLS = [
    "~",
    "`",
    "|",
    "%",
    "^",
    "°",
    "_",
    "{",
    "}",
    "[",
    "]",
    "<",
    ">",
    "/",
    "\\",
    ",",
    ".",
    "-",
    "+",
    "=",
    "!",
    "?",
    ":",
    ";",
    "'",
    "#",
]

_NUM_KEYS = 26


def _make_key_font(size: int = 29) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setFamily("Modern")
    font.setPointSize(size)
    return font


class CustomQwertyKeyboard(QtWidgets.QWidget):
    """Custom on-screen QWERTY keyboard for touch input."""

    value_selected: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="value_selected"
    )
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.current_value: str = ""
        self.symbolsrun: bool = False
        self._key_buttons: list[QtWidgets.QPushButton] = []

        self._setup_ui()
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

        for btn in self._key_buttons:
            btn.clicked.connect(lambda _, b=btn: self.value_inserted(b.text()))

        self.K_dot.clicked.connect(lambda: self.value_inserted("."))
        self.K_space.clicked.connect(lambda: self.value_inserted(" "))
        self.k_Enter.clicked.connect(lambda: self.value_inserted("enter"))
        self.k_delete.clicked.connect(lambda: self.value_inserted("clear"))
        self.K_keychange.clicked.connect(self.handle_keyboard_layout)
        self.K_shift.clicked.connect(self.handle_keyboard_layout)
        self.numpad_back_btn.clicked.connect(self.request_back.emit)

        self.inserted_value.setText("")

        self.setStyleSheet(
            "QPushButton {"
            "  background-color: #dfdfdf;"
            "  border-radius: 10px;"
            "  padding: 6px;"
            "  font-size: 25px;"
            "}"
            "QPushButton:pressed {"
            "  background-color: lightgrey;"
            "  color: black;"
            "}"
            "QPushButton:checked {"
            "  background-color: #212120;"
            "  color: white;"
            "}"
        )
        self.handle_keyboard_layout()

    def handle_keyboard_layout(self) -> None:
        """Update key labels based on current shift/keychange state."""
        shift = self.K_shift.isChecked()
        keychange = self.K_keychange.isChecked()

        if not keychange and not shift:
            layout = _LOWERCASE
        elif not keychange and shift:
            if self.symbolsrun:
                layout = _LOWERCASE
                self.K_shift.setChecked(False)
                self.symbolsrun = False
            else:
                layout = _UPPERCASE
        elif keychange and not shift:
            layout = _NUMBERS
        elif keychange and shift:
            layout = _SYMBOLS
            self.symbolsrun = True
        else:
            layout = _LOWERCASE

        for btn, txt in zip(self._key_buttons, layout):
            btn.setText(txt)

        self.K_shift.setText("#+=") if keychange else self.K_shift.setText("⇧")

    def value_inserted(self, value: str) -> None:
        """Handle key press: append char, delete, or submit on enter."""
        if value == "&&":
            value = "&"

        if value == "enter":
            self.value_selected.emit(self.current_value)
            self.current_value = ""
            self.inserted_value.setText("")
            return

        if value == "clear":
            if len(self.current_value) > 1:
                self.current_value = self.current_value[:-1]
            else:
                self.current_value = ""
        else:
            self.current_value += value

        self.inserted_value.setText(self.current_value)

    def set_value(self, value: str) -> None:
        """Pre-fill keyboard input with an existing value."""
        self.current_value = value
        self.inserted_value.setText(value)

    def _create_key_button(
        self,
        parent: QtWidgets.QWidget,
        name: str,
        *,
        min_w: int = 75,
        min_h: int = 50,
        max_h: int = 50,
        h_policy: QtWidgets.QSizePolicy.Policy = (
            QtWidgets.QSizePolicy.Policy.Expanding
        ),
        v_policy: QtWidgets.QSizePolicy.Policy = (QtWidgets.QSizePolicy.Policy.Fixed),
    ) -> QtWidgets.QPushButton:
        """Create a styled key button with consistent appearance."""
        btn = QtWidgets.QPushButton(parent=parent)
        policy = QtWidgets.QSizePolicy(h_policy, v_policy)
        btn.setSizePolicy(policy)
        btn.setMinimumSize(QtCore.QSize(min_w, min_h))
        btn.setMaximumSize(QtCore.QSize(16777215, max_h))
        btn.setFont(_make_key_font())
        btn.setTabletTracking(False)
        btn.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        btn.setFlat(True)
        btn.setObjectName(name)
        return btn

    def _setup_ui(self) -> None:
        self.setObjectName("self")
        self.resize(800, 480)
        self.setMaximumSize(QtCore.QSize(800, 480))
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        # Row 1: qwertyuiop (grid layout)
        row1_widget = QtWidgets.QWidget(parent=self)
        row1_widget.setGeometry(QtCore.QRect(10, 150, 781, 52))
        row1_layout = QtWidgets.QGridLayout(row1_widget)
        row1_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        row1_layout.setContentsMargins(0, 0, 0, 0)
        row1_layout.setHorizontalSpacing(2)
        row1_layout.setVerticalSpacing(5)

        row1_keys = "qwertyuiop"
        for col, letter in enumerate(row1_keys):
            btn = self._create_key_button(
                row1_widget,
                f"K_{letter}",
                v_policy=QtWidgets.QSizePolicy.Policy.Expanding,
            )
            row1_layout.addWidget(
                btn, 0, col, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
            )
            self._key_buttons.append(btn)

        # Row 2: asdfghjkl (hbox layout)
        row2_widget = QtWidgets.QWidget(parent=self)
        row2_widget.setGeometry(QtCore.QRect(50, 220, 701, 52))
        row2_widget.setMinimumSize(QtCore.QSize(64, 0))
        row2_layout = QtWidgets.QHBoxLayout(row2_widget)
        row2_layout.setContentsMargins(0, 0, 0, 0)
        row2_layout.setSpacing(2)

        for letter in "asdfghjkl":
            btn = self._create_key_button(row2_widget, f"K_{letter}")
            row2_layout.addWidget(btn)
            self._key_buttons.append(btn)

        # Row 3: zxcvbnm (hbox layout)
        row3_widget = QtWidgets.QWidget(parent=self)
        row3_widget.setGeometry(QtCore.QRect(100, 290, 591, 52))
        row3_layout = QtWidgets.QHBoxLayout(row3_widget)
        row3_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        row3_layout.setContentsMargins(0, 0, 0, 0)
        row3_layout.setSpacing(2)

        for letter in "zxcvbnm":
            btn = self._create_key_button(row3_widget, f"K_{letter}", min_w=60)
            row3_layout.addWidget(btn)
            self._key_buttons.append(btn)

        # Shift button (left of row 3)
        self.K_shift = QtWidgets.QPushButton(parent=self)
        self.K_shift.setGeometry(QtCore.QRect(10, 280, 81, 51))
        self.K_shift.setCheckable(True)
        self.K_shift.setText("Shift")
        self.K_shift.setObjectName("K_shift")

        # Delete button (right of row 3)
        self.k_delete = QtWidgets.QPushButton(parent=self)
        self.k_delete.setGeometry(QtCore.QRect(700, 280, 81, 51))
        self.k_delete.setText("\u232b")
        self.k_delete.setObjectName("k_delete")

        # Bottom row: [123] [.] [    space    ] [enter]
        self.K_keychange = QtWidgets.QPushButton(parent=self)
        self.K_keychange.setGeometry(QtCore.QRect(20, 350, 93, 60))
        self.K_keychange.setCheckable(True)
        self.K_keychange.setText("123")
        self.K_keychange.setObjectName("K_keychange")

        self.K_dot = QtWidgets.QPushButton(parent=self)
        self.K_dot.setGeometry(QtCore.QRect(120, 362, 55, 60))
        self.K_dot.setFont(_make_key_font())
        self.K_dot.setText(".")
        self.K_dot.setFlat(True)
        self.K_dot.setObjectName("K_dot")

        self.K_space = QtWidgets.QPushButton(parent=self)
        self.K_space.setGeometry(QtCore.QRect(177, 362, 494, 60))
        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.K_space.setSizePolicy(policy)
        self.K_space.setMinimumSize(QtCore.QSize(0, 60))
        self.K_space.setMaximumSize(QtCore.QSize(16777215, 60))
        self.K_space.setObjectName("K_space")

        self.k_Enter = QtWidgets.QPushButton(parent=self)
        self.k_Enter.setGeometry(QtCore.QRect(680, 350, 93, 60))
        self.k_Enter.setText("\u23ce")
        self.k_Enter.setAutoRepeat(False)
        self.k_Enter.setObjectName("k_Enter")

        # Back button (top-right)
        self.numpad_back_btn = IconButton(parent=self)
        self.numpad_back_btn.setGeometry(QtCore.QRect(720, 20, 60, 60))
        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        policy.setHorizontalStretch(1)
        policy.setVerticalStretch(1)
        self.numpad_back_btn.setSizePolicy(policy)
        self.numpad_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.numpad_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.numpad_back_btn.setIconSize(QtCore.QSize(16, 16))
        self.numpad_back_btn.setFlat(True)
        self.numpad_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.numpad_back_btn.setProperty("button_type", "icon")
        self.numpad_back_btn.setObjectName("numpad_back_btn")

        # Input display area
        input_widget = QtWidgets.QWidget(parent=self)
        input_widget.setGeometry(QtCore.QRect(10, 90, 781, 48))
        input_layout = QtWidgets.QVBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)

        self.inserted_value = QtWidgets.QLabel(parent=input_widget)
        self.inserted_value.setMinimumSize(QtCore.QSize(500, 0))
        self.inserted_value.setMaximumSize(QtCore.QSize(16777215, 50))
        self.inserted_value.setFont(_make_key_font(18))
        self.inserted_value.setStyleSheet("color: white;")
        self.inserted_value.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.inserted_value.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.inserted_value.setLineWidth(0)
        self.inserted_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.inserted_value.setObjectName("inserted_value")
        input_layout.addWidget(self.inserted_value)

        line = QtWidgets.QFrame(parent=input_widget)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        input_layout.addWidget(line)
