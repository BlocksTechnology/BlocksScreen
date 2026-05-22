import typing

from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class AddFilamentPage(QtWidgets.QWidget):
    request_add_filament: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="request-add-filament"
    )
    accepted: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(name="accepted")
    cancelled: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(name="cancelled")

    def __init__(
        self, keyboard_parent: QtWidgets.QWidget | None = None, parent=None
    ) -> None:
        super().__init__(parent)
        self._keyboard_field: QtWidgets.QLineEdit | None = None

        self._build_ui()

        self._keyboard = CustomQwertyKeyboard(keyboard_parent)
        self._keyboard.hide()
        self._keyboard.numpad_back_btn.clicked.connect(self._keyboard.hide)
        self._keyboard.value_selected.connect(self._on_keyboard_done)

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

        def _key_lbl(text: str) -> QtWidgets.QLabel:
            lbl = QtWidgets.QLabel(text, self)
            lbl.setFont(_f(12))
            lbl.setStyleSheet("color: rgb(180,180,180); background: transparent;")
            lbl.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft
            )
            return lbl

        def _make_field() -> BlocksCustomLinEdit:
            fld = BlocksCustomLinEdit(self)
            fld.setFont(_f(14))
            fld.setFixedHeight(44)
            return fld

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(4)

        hdr = QtWidgets.QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.setSpacing(0)
        back_btn = IconButton(self)
        back_btn.setFixedSize(QtCore.QSize(60, 60))
        back_btn.setFlat(True)
        back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        back_btn.clicked.connect(self.cancelled)
        hdr.addWidget(back_btn)
        title_lbl = QtWidgets.QLabel("Add Filament", self)
        title_lbl.setFont(_f(22))
        title_lbl.setFixedHeight(60)
        title_lbl.setStyleSheet("color: white; background: transparent;")
        title_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(title_lbl, 1)
        root.addLayout(hdr)

        grid_w = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(grid_w)
        grid.setContentsMargins(8, 2, 8, 2)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(4)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(4, 1)

        self._name_field = _make_field()
        self._material_field = _make_field()
        self._color_field = _make_field()
        self._ext_temp_field = _make_field()
        self._bed_temp_field = _make_field()
        self._density_field = _make_field()
        self._diameter_field = _make_field()

        self._color_swatch = QtWidgets.QLabel(self)
        self._color_swatch.setFixedSize(44, 44)
        self._color_swatch.setStyleSheet(
            "border-radius: 8px; background: #ffffff; border: 2px solid rgba(255,255,255,80);"
        )

        # rows = [
        #     ("Name:", self._name_field, None),
        #     ("Material:", self._material_field, None),
        #     ("Color:", self._color_field, self._color_swatch),
        #     ("Ext Temp:", self._ext_temp_field, None),
        #     ("Bed Temp:", self._bed_temp_field, None),
        #     ("Density:", self._density_field, None),
        #     ("Diameter:", self._diameter_field, None),
        # ]
        # for i, (label, field, extra) in enumerate(rows):
        #    grid.addWidget(_key_lbl(label), i, 0)
        #    grid.addWidget(field, i, 1)
        #    if extra is not None:
        #        grid.addWidget(extra, i, 2)

        grid.addWidget(_key_lbl("Name:"), 0, 0)
        grid.addWidget(self._name_field, 0, 1, 1, 2)
        grid.addWidget(_key_lbl("Material:"), 0, 3)
        grid.addWidget(self._material_field, 0, 4)
        
        grid.addWidget(_key_lbl("Color:"), 1, 0)
        grid.addWidget(self._color_field, 1, 1)
        self._color_field.setMaximumWidth(70)

        grid.addWidget(self._color_swatch, 1, 2)

        grid.addWidget(_key_lbl("Ext Temp:"), 2, 0)
        grid.addWidget(self._ext_temp_field, 2, 1)
        self._ext_temp_field.setMaximumWidth(60)
        grid.addWidget(_key_lbl("Bed Temp:"), 2, 2)
        grid.addWidget(self._bed_temp_field, 2, 3)
        self._bed_temp_field.setMaximumWidth(60)

        grid.addWidget(_key_lbl("Density:"), 3, 0)
        grid.addWidget(self._density_field, 3, 1)
        self._density_field.setMaximumWidth(65)

        grid.addWidget(_key_lbl("Diameter:"), 3, 2)
        grid.addWidget(self._diameter_field, 3, 3)
        self._diameter_field.setMaximumWidth(65)


        root.addWidget(grid_w, 1)

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
        self._color_field.clicked.connect(
            lambda: self._show_keyboard(self._color_field, prefix="#", max_char=6)
        )
        self._ext_temp_field.clicked.connect(
            lambda: self._show_keyboard(self._ext_temp_field, pattern="int", max_char=3)
        )
        self._bed_temp_field.clicked.connect(
            lambda: self._show_keyboard(self._bed_temp_field, pattern="int", max_char=3)
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
        submit_btn.setFixedSize(200, 80)
        submit_btn.setFont(_f(16))
        submit_btn.setText("Save Filament")
        submit_btn.clicked.connect(self._on_submit)
        root.addWidget(submit_btn)
