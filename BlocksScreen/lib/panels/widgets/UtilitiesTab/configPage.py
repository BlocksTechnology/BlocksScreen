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

# TODO: find a better way to hide sections, hardcoded is kinda meh;
# a section with "hidden: true/yes" is hidden too, without hardcoding

# TODO: screensaver is currenly hidden for numpad dosent have option for float (miliseconds to minutes works)

_BOOL_WORDS = {
    "true": ("true", "false"),
    "false": ("true", "false"),
    "yes": ("yes", "no"),
    "no": ("yes", "no"),
}

_HIDDEN_ON = {on for on, _off in _BOOL_WORDS.values()}


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
_DISPLAY_UNITS = {
    ("screensaver", "timeout"): (60_000, "minutes"),
}


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

        self._leave_popup = BasePopup(self, floating=True)
        self._leave_popup.confirm_button_text("Restart")
        self._leave_popup.cancel_button_text("Discard")
        self._leave_popup.accepted.connect(self._save_and_restart)
        self._leave_popup.rejected.connect(self._discard_pending)

    def setup_config_rows(self) -> None:
        """Build one titled group per config section, one row per option."""
        self._cfg = get_configparser()
        self._bool_words: dict[tuple[str, str], tuple[str, str]] = {}
        self._saved: dict[tuple[str, str], str] = {}
        self._pending: dict[tuple[str, str], BlocksField] = {}
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
        unit = _DISPLAY_UNITS.get((section, option))
        if unit:
            label = f"{label} ({unit[1]})"
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
        field.set_right_text(self._to_display(section, option, value))
        if editable:
            self._saved[(section, option)] = self._field_value(section, option, field)
            field.on_edit.connect(partial(self._stage_option, section, option, field))
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

    def _field_value(self, section: str, option: str, field: BlocksField) -> str:
        if (section, option) in self._bool_words:
            on, off = self._bool_words[(section, option)]
            return on if field.is_checked() else off
        return self._to_stored(section, option, field.text())

    def _to_display(self, section: str, option: str, value: str) -> str:
        unit = _DISPLAY_UNITS.get((section, option))
        if not unit:
            return value
        try:
            shown = int(value) / unit[0]
        except ValueError:
            return value
        return f"{round(shown, 2):g}"

    def _to_stored(self, section: str, option: str, text: str) -> str:
        unit = _DISPLAY_UNITS.get((section, option))
        if not unit:
            return text
        try:
            return str(round(float(text) * unit[0]))
        except ValueError:
            return text

    def _stage_option(self, section: str, option: str, field: BlocksField) -> None:
        key = (section, option)
        if self._field_value(section, option, field) == self._saved[key]:
            self._pending.pop(key, None)
        else:
            self._pending[key] = field

    def _save_pending(self) -> None:
        if not self._pending:
            return
        for (section, option), field in self._pending.items():
            value = self._field_value(section, option, field)
            self._cfg.update_option(section, option, value)
            self._saved[(section, option)] = value
        self._cfg.save_configuration()
        self._pending.clear()

    def _discard_pending(self) -> None:
        for (section, option), field in self._pending.items():
            saved = self._saved[(section, option)]
            field.set_right_text(self._to_display(section, option, saved))
        self._pending.clear()

    def _save_and_restart(self) -> None:
        self._save_pending()
        self.request_restart.emit()

    def hideEvent(self, a0: QtGui.QHideEvent | None) -> None:
        """Ask to apply or discard pending edits when the page is left."""
        super().hideEvent(a0)
        if a0 is not None and a0.spontaneous():
            return
        if not self._pending or self._leave_popup.isVisible():
            return
        self._leave_popup.set_message(
            f"{len(self._pending)} unsaved change(s).\n\n"
            "Restart the screen to apply them?"
        )
        self._leave_popup.open()

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

        self.config_header_layout.addSpacing(60)

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
