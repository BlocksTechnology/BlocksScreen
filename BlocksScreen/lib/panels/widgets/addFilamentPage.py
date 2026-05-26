import typing

from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from lib.panels.widgets.numpadPage import CustomNumpad
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets
from lib.panels.widgets.basePopup import BasePopup
from lib.panels.widgets.colorWheelWidget import ColorWheelWidget


class AddFilamentPage(QtWidgets.QWidget):
    request_add_filament: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="request-add-filament"
    )
    accepted: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(name="accepted")
    cancelled: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(name="cancelled")
    request_numpad: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str, int, "PyQt_PyObject"],
        [str, int, "PyQt_PyObject", int, int],
        name="request-numpad",
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._keyboard_field: QtWidgets.QLineEdit | None = None

        self._build_ui()

        self._keyboard = CustomQwertyKeyboard(self)
        self._keyboard.hide()
        self._keyboard.numpad_back_btn.clicked.connect(self._keyboard.hide)
        self._keyboard.value_selected.connect(self._on_keyboard_done)

        self._numpad = CustomNumpad(self)
        self._numpad.hide()

        self._numpad_popup = BasePopup(self, False, False)
        self._numpad_popup.add_widget(self._numpad)
        self._numpad.numpad_back_btn.clicked.connect(self._numpad_popup.hide)

        self.color_whell = ColorWheelWidget(self)
        self.color_whell.hide()

        self._color_whell_popup = BasePopup(self, True, False)
        self._color_whell_popup.x_offset = 0.95
        self._color_whell_popup.y_offset = 0.95
        self._color_whell_popup.add_widget(self.color_whell)
        self.color_whell.request_back.connect(self._color_whell_popup.hide)
        self.color_whell.color_selected.connect(self._on_color_selected)

        self.request_numpad[str, int, "PyQt_PyObject", int, int].connect(
            self.on_numpad_request
        )

    @QtCore.pyqtSlot(dict, name="on-add-filament-result")
    def on_add_filament_result(self, result: dict) -> None:
        if result.get("error") is None:
            self.accepted.emit()
        else:
            ...
            # TODO: some responsiveness here

    def _show_keyboard(
        self,
        field: QtWidgets.QLineEdit,
        prefix: str = "",
        suffix: str = "",
        pattern: str = "",
        max_char: int = 0,
    ) -> None:
        self._keyboard_field = field
        self._keyboard.setPrefix(prefix)
        self._keyboard.setSuffix(suffix)
        self._keyboard.setPatern(pattern)
        self._keyboard.set_value(field.text().strip("#"))
        self._keyboard.setMaxLength(max_char)
        self._keyboard.show()

    @QtCore.pyqtSlot(str, name="on-keyboard-done")
    def _on_keyboard_done(self, value: str) -> None:
        self._keyboard.hide()
        if self._keyboard_field is not None:
            self._keyboard_field.setText(value)
            self._keyboard_field = None

    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", name="on-numpad-request")
    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", int, int, name="on-numpad-request")
    def on_numpad_request(
        self,
        name: str,
        current_value: int,
        callback,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        try:
            self._numpad.value_selected.disconnect()
        except TypeError:
            pass
        self._numpad.value_selected.connect(callback)
        self._numpad.set_name(name)
        self._numpad.set_value(current_value)
        self._numpad.set_min_value(min_value)
        self._numpad.set_max_value(max_value)
        self._numpad_popup.show()

    @QtCore.pyqtSlot(str, int, name="on-ext-temp-change")
    def _on_ext_temp_change(self, _name: str, value: int) -> None:
        self._numpad_popup.hide()
        self._ext_temp_field.setText(str(value))

    @QtCore.pyqtSlot(str, int, name="on-bed-temp-change")
    def _on_bed_temp_change(self, _name: str, value: int) -> None:
        self._numpad_popup.hide()
        self._bed_temp_field.setText(str(value))

    def _open_color_wheel(self) -> None:
        self.color_whell.set_color_hex(
            self._color_field.text().strip().lstrip("#") or "ffffff"
        )
        self._color_whell_popup.show()

    @QtCore.pyqtSlot(str, name="on-color-selected")
    def _on_color_selected(self, hex_str: str) -> None:
        self._color_field.setText(hex_str)

    def _update_swatch(self) -> None:
        hex_text = self._color_field.text().strip("#").strip()
        if len(hex_text) == 6:
            color = QtGui.QColor(f"#{hex_text}")
            self._color_swatch.setStyleSheet(
                f"border-radius: 8px;"
                f"background: rgb({color.red()},{color.green()},{color.blue()});"
                f"border: 2px solid rgba(255,255,255,80);"
            )

    def _on_submit(self) -> None:
        body: dict = {}
        name = self._name_field.text().strip()
        material = self._material_field.text().strip()
        color_hex = self._color_field.text().strip().strip("#")
        ext_temp = self._ext_temp_field.text().strip()
        bed_temp = self._bed_temp_field.text().strip()
        density_text = self._density_field.text().strip()
        diameter_text = self._diameter_field.text().strip()

        if name:
            body["name"] = name
        if material:
            body["material"] = material
        if color_hex:
            body["color_hex"] = color_hex
        try:
            body["settings_extruder_temp"] = int(ext_temp)
        except ValueError:
            pass
        try:
            body["settings_bed_temp"] = int(bed_temp)
        except ValueError:
            pass
        try:
            body["density"] = float(density_text)
        except ValueError:
            body["density"] = 1.24
        try:
            body["diameter"] = float(diameter_text)
        except ValueError:
            body["diameter"] = 1.75

        self.request_add_filament.emit(body)

    def _build_ui(self) -> None:
        def _f(pt: int) -> QtGui.QFont:
            font = QtGui.QFont()
            font.setPointSize(pt)
            return font

        def _key_lbl(text: str, parent: QtWidgets.QWidget) -> QtWidgets.QLabel:
            lbl = QtWidgets.QLabel(text, parent)
            lbl.setFont(_f(12))
            lbl.setFixedHeight(20)
            lbl.setStyleSheet("color: rgb(180,180,180); background: transparent;")
            return lbl

        def _make_field(parent: QtWidgets.QWidget) -> BlocksCustomLinEdit:
            fld = BlocksCustomLinEdit(parent)
            fld.setFont(_f(14))
            fld.setFixedHeight(46)
            return fld

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        # Header
        hdr = QtWidgets.QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.setSpacing(0)

        blank = QtWidgets.QWidget(self)
        blank.setFixedSize(60, 60)
        hdr.addWidget(blank)

        title_lbl = QtWidgets.QLabel("Add Filament", self)
        title_lbl.setFont(_f(22))
        title_lbl.setFixedHeight(60)
        title_lbl.setStyleSheet("color: white; background: transparent;")
        title_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(title_lbl)

        back_btn = IconButton(self)
        back_btn.setFixedSize(QtCore.QSize(60, 60))
        back_btn.setFlat(True)
        back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        back_btn.clicked.connect(self.cancelled)
        hdr.addWidget(back_btn)
        root.addLayout(hdr)

        body = QtWidgets.QHBoxLayout()
        body.setSpacing(8)

        left_frame = BlocksCustomFrame(self)
        left_lay = QtWidgets.QVBoxLayout(left_frame)
        left_lay.setContentsMargins(12, 10, 12, 10)
        left_lay.setSpacing(6)

        self._name_field = _make_field(left_frame)
        self._material_field = _make_field(left_frame)
        self._color_field = _make_field(left_frame)

        self._color_swatch = QtWidgets.QLabel(left_frame)
        self._color_swatch.setFixedSize(70, 70)
        self._color_swatch.setStyleSheet(
            "border-radius: 8px; background: #ffffff; border: 2px solid rgba(255,255,255,80);"
        )

        left_lay.addWidget(_key_lbl("Name:", left_frame))
        left_lay.addWidget(self._name_field)

        left_lay.addWidget(_key_lbl("Material:", left_frame))
        left_lay.addWidget(self._material_field)

        left_lay.addWidget(_key_lbl("Color (hex):", left_frame))
        color_row = QtWidgets.QHBoxLayout()
        color_row.setSpacing(30)
        color_row.setContentsMargins(0, 0, 0, 0)
        self._color_field.setMaximumWidth(100)
        color_row.addWidget(self._color_field)
        color_row.addWidget(self._color_swatch)
        color_row.addStretch(1)
        left_lay.addLayout(color_row)

        left_lay.addStretch(1)
        body.addWidget(left_frame, 1)

        right_frame = BlocksCustomFrame(self)
        right_lay = QtWidgets.QVBoxLayout(right_frame)
        right_lay.setContentsMargins(12, 10, 12, 10)
        right_lay.setSpacing(6)

        self._ext_temp_field = _make_field(right_frame)
        self._bed_temp_field = _make_field(right_frame)
        self._density_field = _make_field(right_frame)
        self._diameter_field = _make_field(right_frame)

        right_lay.addWidget(_key_lbl("Extruder Temp (°C):", right_frame))
        right_lay.addWidget(self._ext_temp_field)

        right_lay.addWidget(_key_lbl("Bed Temp (°C):", right_frame))
        right_lay.addWidget(self._bed_temp_field)

        dd_row = QtWidgets.QHBoxLayout()
        dd_row.setSpacing(8)
        dd_row.setContentsMargins(0, 0, 0, 0)

        dens_col = QtWidgets.QVBoxLayout()
        dens_col.setSpacing(4)
        dens_col.addWidget(_key_lbl("Density (g/cm³):", right_frame))
        dens_col.addWidget(self._density_field)
        dd_row.addLayout(dens_col)

        diam_col = QtWidgets.QVBoxLayout()
        diam_col.setSpacing(4)
        diam_col.addWidget(_key_lbl("Diameter (mm):", right_frame))
        diam_col.addWidget(self._diameter_field)
        dd_row.addLayout(diam_col)

        right_lay.addLayout(dd_row)
        right_lay.addStretch(1)
        body.addWidget(right_frame, 1)

        root.addLayout(body, 1)

        self._name_field.setPlaceholderText("e.g. PLA Generic")
        self._material_field.setText("PLA")
        self._color_field.setText("ffffff")
        self._ext_temp_field.setText("220")
        self._bed_temp_field.setText("60")
        self._density_field.setText("1.24")
        self._diameter_field.setText("1.75")

        self._name_field.clicked.connect(lambda: self._show_keyboard(self._name_field))
        self._material_field.clicked.connect(
            lambda: self._show_keyboard(self._material_field)
        )
        self._color_field.clicked.connect(self._open_color_wheel)
        self._ext_temp_field.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Extruder Temp",
                int(self._ext_temp_field.text().strip() or 0),
                self._on_ext_temp_change,
                0,
                330,
            )
        )
        self._bed_temp_field.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Bed Temp",
                int(self._bed_temp_field.text().strip() or 0),
                self._on_bed_temp_change,
                0,
                110,
            )
        )
        self._density_field.clicked.connect(
            lambda: self._show_keyboard(self._density_field, max_char=5)
        )
        self._diameter_field.clicked.connect(
            lambda: self._show_keyboard(self._diameter_field, max_char=4)
        )

        self._color_field.textChanged.connect(self._update_swatch)

        # Submit
        submit_btn = BlocksCustomButton(self)
        submit_btn.setFixedSize(220, 80)
        submit_btn.setFont(_f(16))
        submit_btn.setText("Save\nFilament")
        submit_btn.clicked.connect(self._on_submit)
        root.addWidget(submit_btn, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
