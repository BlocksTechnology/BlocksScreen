import typing
from functools import partial

from configfile import get_configparser
from lib.panels.widgets.Common.basePopup import BasePopup
from lib.panels.widgets.Common.keyboardPage import CustomQwertyKeyboard
from lib.panels.widgets.Common.numpadPage import CustomNumpad
from lib.utils.blocks_field import BlocksField
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_Scrollbar import CustomScrollBar
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

# Boolean spellings shown as a toggle, saved back in the same style (on, off)
_BOOL_WORDS = {
    "true": ("true", "false"),
    "false": ("true", "false"),
    "yes": ("yes", "no"),
    "no": ("yes", "no"),
}

_HIDDEN_ON = {on for on, _off in _BOOL_WORDS.values()}

# TODO: find a better way to hide sections, hardcoded is kinda meh;
# a section with "hidden: true/yes" is hidden too, without hardcoding
_HIDDEN_SECTIONS = frozenset(
    {
        "filament_presence",
        "usb_manager",
        "hotspot",
        "configuration_manager",
    }
)

# Sections shown but not editable
_READ_ONLY_SECTIONS = frozenset({"server"})


def _pretty(name: str) -> str:
    words = name.replace("_", " ").split()
    text = " ".join(words)
    return text[:1].upper() + text[1:]


class ConfigPage(QtWidgets.QWidget):
    """Config page of the utilities tab, built from the BlocksScreen config file."""

    request_back_button = QtCore.pyqtSignal(name="request-back-button")
    request_restart = QtCore.pyqtSignal(name="request-restart")

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super().__init__(parent)

        self._setup_ui()
        self._input_field: BlocksField | None = None

        self._numpad = CustomNumpad(self)
        self._numpad.hide()
        self._numpad_popup = BasePopup(self, False, False)
        self._numpad_popup.add_widget(self._numpad)
        self._numpad.request_back.connect(self._numpad_popup.hide)
        self._numpad.value_selected.connect(
            lambda _name, value: self._apply_input(str(value))
        )

        self._qwerty = CustomQwertyKeyboard(self)
        self._qwerty.hide()
        self._qwerty.request_back.connect(self._qwerty.hide)
        self._qwerty.value_selected.connect(self._on_qwerty_value_selected)
        self.config_back_btn.clicked.connect(self.request_back_button.emit)

        self._restart_popup = BasePopup(self, floating=True)
        self._restart_popup.confirm_button_text("Restart")
        self._restart_popup.cancel_button_text("Later")
        self._restart_popup.accepted.connect(self.request_restart.emit)
        self.config_restart_btn.clicked.connect(
            lambda: self._ask_restart("Restart the screen?\n\nMay take a few seconds.")
        )

    def setup_config_rows(self) -> None:
        """Build one titled group per config section, one row per option."""
        self._cfg = get_configparser()
        self._bool_words: dict[tuple[str, str], tuple[str, str]] = {}
        column_rows = [0] * len(self._columns)

        for section, options in self._visible_sections():
            frame = self._build_section(section, options)
            col = column_rows.index(min(column_rows))
            # +1 weighs in the group's title
            column_rows[col] += len(options) + 1
            self._columns[col].addWidget(frame)
        for column in self._columns:
            column.addStretch(1)

    def _visible_sections(self) -> typing.Iterator[tuple[str, list[str]]]:
        for section in self._cfg.sections():
            if section in _HIDDEN_SECTIONS:
                continue
            hidden = self._cfg.config.get(section, "hidden", fallback="") or ""
            if hidden.strip().lower() in _HIDDEN_ON:
                continue
            options = [o for o in self._cfg.config.options(section) if o != "hidden"]
            if options:
                yield section, options

    def _build_section(self, section: str, options: list[str]) -> BlocksCustomFrame:
        title = _pretty(section)
        frame = BlocksCustomFrame(parent=self._rows_container)
        frame.setProperty("text", title)
        frame.setMinimumHeight(0)
        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.setContentsMargins(16, 30, 16, 6)
        frame_layout.setSpacing(0)

        last = len(options) - 1
        for i, option in enumerate(options):
            field = self._build_row(frame, title, section, option, i < last)
            frame_layout.addWidget(field)
        return frame

    def _build_row(
        self,
        frame: BlocksCustomFrame,
        title: str,
        section: str,
        option: str,
        has_line: bool,
    ) -> BlocksField:
        value = self._cfg.config.get(section, option, fallback="") or ""
        label = _pretty(option)
        bool_words = _BOOL_WORDS.get(value.strip().lower())
        if section in _READ_ONLY_SECTIONS:
            editable = None
        elif bool_words:
            editable = "Toggle"
            self._bool_words[(section, option)] = bool_words
        else:
            editable = "LineEdit"

        field = BlocksField(
            frame, f"{label}:", "bottom" if has_line else None, editable
        )
        field.setFixedHeight(70)
        field.set_right_text(value)
        if editable:
            field.on_edit.connect(partial(self._save_option, section, option, field))
        if editable == "LineEdit":
            field.clicked.connect(partial(self._open_input, f"{title} {label}", field))
        return field

    def _open_input(self, name: str, field: BlocksField) -> None:
        self._input_field = field
        value = field.text().strip()
        if value.isdigit():
            self._numpad.set_name(name)
            self._numpad.set_value(int(value))
            self._numpad_popup.show()
            self._numpad.set_enforce_range(False)
            return
        self._qwerty.set_value(value)
        self._qwerty.show()

    def _on_qwerty_value_selected(self, value: str) -> None:
        self._qwerty.hide()
        self._apply_input(value)

    def _apply_input(self, value: str) -> None:
        field, self._input_field = self._input_field, None
        if field is None:
            return
        field.set_right_text(value)
        field.on_edit.emit()

    def _save_option(self, section: str, option: str, field: BlocksField) -> None:
        value = field.text()
        if (section, option) in self._bool_words:
            on, off = self._bool_words[(section, option)]
            value = on if field.is_checked() else off
        self._cfg.update_option(section, option, value)
        self._cfg.save_configuration()
        self._ask_restart("Setting saved.\n\nRestart the screen to apply it.")

    def _ask_restart(self, message: str) -> None:
        if self._restart_popup.isVisible():
            return
        self._restart_popup.set_message(message)
        self._restart_popup.open()

    def _setup_ui(self) -> None:
        self.setObjectName("config_page")

        spacerItem = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addItem(spacerItem)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.config_header_layout = QtWidgets.QHBoxLayout()
        self.config_header_layout.setObjectName("config_header_layout")

        self.config_restart_btn = IconButton(parent=self)
        self.config_restart_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.config_restart_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.config_restart_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/refresh.svg")
        )
        self.config_header_layout.addWidget(self.config_restart_btn)

        self.config_title_label = QtWidgets.QLabel(parent=self)
        self.config_title_label.setSizePolicy(sizePolicy)
        self.config_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.config_title_label.setFont(font)
        self.config_title_label.setStyleSheet("background: transparent; color: white;")
        self.config_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.config_header_layout.addWidget(self.config_title_label)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )

        self.config_back_btn = IconButton(parent=self)
        self.config_back_btn.setSizePolicy(sizePolicy)
        self.config_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.config_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.config_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.config_header_layout.addWidget(self.config_back_btn)
        self.verticalLayout_2.addLayout(self.config_header_layout)

        self._scroll_area = QtWidgets.QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self._scroll_area.setStyleSheet(
            "QScrollArea, QScrollArea > QWidget { background: transparent; }"
        )
        self._scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll_area.setVerticalScrollBar(CustomScrollBar())

        self._rows_container = QtWidgets.QWidget()
        self._rows_container.setObjectName("config_rows")
        self._rows_container.setStyleSheet("#config_rows { background: transparent; }")
        rows_layout = QtWidgets.QHBoxLayout(self._rows_container)
        rows_layout.setContentsMargins(12, 0, 12, 0)
        rows_layout.setSpacing(10)
        self._columns: list[QtWidgets.QVBoxLayout] = []
        for _ in range(1):
            column = QtWidgets.QVBoxLayout()
            column.setSpacing(10)
            rows_layout.addLayout(column, 1)
            self._columns.append(column)
        self._scroll_area.setWidget(self._rows_container)
        viewport = self._scroll_area.viewport()
        QtWidgets.QScroller.grabGesture(
            viewport, QtWidgets.QScroller.ScrollerGestureType.TouchGesture
        )
        QtWidgets.QScroller.grabGesture(
            viewport, QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture
        )
        self.setup_config_rows()
        self.verticalLayout_2.addWidget(self._scroll_area)

        _translate = QtCore.QCoreApplication.translate

        self.config_title_label.setText(_translate("self", "Settings Page"))
