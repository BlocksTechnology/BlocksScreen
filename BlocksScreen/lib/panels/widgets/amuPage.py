import typing
from collections import deque
from typing import Deque

from devices.amu import AMUManager
from devices.amu.models import GateInfo, GateStatus
from lib.panels.widgets.amuWidgets import SpoolCarousel, SpoolInfoPanel
from lib.panels.widgets.basePopup import BasePopup
from lib.panels.widgets.colorWheelWidget import ColorWheelWidget
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from lib.panels.widgets.loadWidget import LoadingOverlayWidget
from lib.panels.widgets.numpadPage import CustomNumpad
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets


class AMUpage(QtWidgets.QStackedWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    request_spools: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-spools"
    )
    request_gate_map: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request-gate-map"
    )
    request_open_add_spoolman: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-open-spoolman"
    )
    request_numpad: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str, int, "PyQt_PyObject"],
        [str, int, "PyQt_PyObject", int, int],
        name="request-numpad",
    )

    def __init__(self, amu_manager, parent=None):
        super().__init__(parent)
        self._previous_gate_states: dict[int, bool] = {}
        self.current_index = -1
        self.pre_gate_idx = -1
        self.amu_manager: AMUManager = amu_manager
        self.popup_gates: Deque = deque()
        self._selected_spool_id: int = -1
        self._spool_id_map: dict[str, dict] = {}
        self._current_field: QtWidgets.QLineEdit | None = None
        self._build_ui()

        self._numpad = CustomNumpad(self)
        self._numpad.hide()

        self._numpad_popup = BasePopup(self, False, False)
        self._numpad_popup.add_widget(self._numpad)
        self._numpad.numpad_back_btn.clicked.connect(self._numpad_popup.hide)

        self.request_numpad[str, int, "PyQt_PyObject", int, int].connect(
            self.on_numpad_request
        )

        self.amu_manager.mmu_state_changed.connect(self.on_mmu_state_changed)
        self.on_mmu_state_changed(self.amu_manager.get_state())
        self.info_panel._lbl_color.editingFinished.connect(
            lambda: self.amu_manager.set_gate_color(
                self.current_index,
                self.info_panel._lbl_color.text().strip("#"),
            )
        )
        self.info_panel._lbl_color.clicked.connect(
            lambda: self._open_color_wheel(self.info_panel._lbl_color)
        )
        self.info_panel._lbl_mat.editingFinished.connect(
            lambda: self.amu_manager.set_gate_material(
                self.current_index, self.info_panel._lbl_mat.text().strip("º")
            )
        )
        self.info_panel._lbl_temp.editingFinished.connect(
            lambda: self.amu_manager.set_gate_temp(
                self.current_index,
                int(self.info_panel._lbl_temp.text().strip("º") or 0),
            )
        )
        self.info_panel._lbl_temp.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Temperature",
                int(self.info_panel._lbl_temp.text().strip("º")),
                self._on_gate_temp_change,
                0,
                500,
            )
        )
        self.info_panel._lbl_weight.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Weight",
                int(self.info_panel._lbl_weight.text().strip("g")),
                self._on_gate_weight_change,
                0,
                9999,
            )
        )

        self._qwerty = CustomQwertyKeyboard(self)
        self._qwerty.hide()
        self._qwerty.numpad_back_btn.clicked.connect(self._on_qwerty_go_back)
        self._qwerty.value_selected.connect(self._on_qwerty_value_selected)

        self.info_panel.request_keypad.connect(self._on_show_keyboard)
        self.info_panel.loadRequested.connect(self.amu_manager.load_gate)
        self.info_panel.unloadRequested.connect(self.amu_manager.unload)
        self.info_panel.ejectRequested.connect(self.amu_manager.eject_gate)
        self.info_panel.checkRequested.connect(self.amu_manager.check_gate)

        self.amu_manager.pre_gate_changed.connect(self.on_pre_gate)
        self.carousel.selectionChanged.connect(self._select_gate)

        self._setup_popup()
        self._setup_color_wheel()

    def _setup_popup(self):
        self._popup_stack = QtWidgets.QStackedWidget()
        self._popup_stack.addWidget(self._build_form_page())
        self._popup_stack.addWidget(self._build_spool_page())

        self.popup = BasePopup(self, False, False)
        self.popup.add_widget(self._popup_stack)

    def _build_form_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        root = QtWidgets.QVBoxLayout(page)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(8)

        self._popup_title_lbl = QtWidgets.QLabel("Filament Detected", page)
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        self._popup_title_lbl.setFont(title_font)
        self._popup_title_lbl.setStyleSheet("color: white; background: transparent;")
        self._popup_title_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._popup_title_lbl.setFixedHeight(50)
        root.addWidget(self._popup_title_lbl)

        grid_w = QtWidgets.QWidget(page)
        grid = QtWidgets.QGridLayout(grid_w)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(6)
        grid.setColumnStretch(1, 1)

        key_font = QtGui.QFont()
        key_font.setPointSize(13)
        val_font = QtGui.QFont()
        val_font.setPointSize(14)

        def _lbl(text):
            lbl = QtWidgets.QLabel(text, grid_w)
            lbl.setFont(key_font)
            lbl.setStyleSheet("color: rgb(180,180,180); background: transparent;")
            return lbl

        def _field():
            f = BlocksCustomLinEdit(page)
            f.setFont(val_font)
            f.setFixedHeight(50)
            return f

        self._popup_name = _field()
        self._popup_color = _field()
        self._popup_material = _field()
        self._popup_temp = _field()

        self._popup_swatch = QtWidgets.QLabel(page)
        self._popup_swatch.setFixedSize(50, 50)
        self._popup_swatch.setStyleSheet(
            "border-radius: 8px; background: #ffffff; border: 2px solid rgba(255,255,255,80);"
        )

        rows = [
            ("Name:", self._popup_name, None),
            ("Color:", self._popup_color, self._popup_swatch),
            ("Material:", self._popup_material, None),
            ("Temp:", self._popup_temp, None),
        ]
        for i, (lbl_text, field, extra) in enumerate(rows):
            grid.addWidget(_lbl(lbl_text), i, 0)
            grid.addWidget(field, i, 1)
            if extra:
                grid.addWidget(extra, i, 2)

        root.addWidget(grid_w, 1)

        self._popup_name.setPlaceholderText("e.g. PLA Generic")
        self._popup_color.setText("ffffff")
        self._popup_material.setText("PLA")
        self._popup_temp.setText("220")

        self._popup_name.clicked.connect(
            lambda: self._on_show_keyboard(self._popup_name)
        )
        self._popup_color.clicked.connect(
            lambda: self._open_color_wheel(self._popup_color)
        )
        self._popup_material.clicked.connect(
            lambda: self._on_show_keyboard(self._popup_material)
        )
        self._popup_temp.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Temperature",
                int(self._popup_temp.text().strip("º") or 0),
                self._on_popup_temp_change,
                0,
                500,
            )
        )

        def _update_swatch():
            hex_text = self._popup_color.text().strip("#").strip()
            if len(hex_text) == 6:
                c = QtGui.QColor(f"#{hex_text}")
                self._popup_swatch.setStyleSheet(
                    f"border-radius: 8px;"
                    f"background: rgb({c.red()},{c.green()},{c.blue()});"
                    f"border: 2px solid rgba(255,255,255,80);"
                )

        self._popup_color.textChanged.connect(_update_swatch)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(8)

        font = QtGui.QFont()
        font.setPointSize(15)

        spoolman_btn = BlocksCustomButton(page)
        spoolman_btn.setFixedSize(200, 80)
        spoolman_btn.setText("Spoolman")
        spoolman_btn.setFont(font)
        spoolman_btn.clicked.connect(self._on_spoolman_clicked)
        btn_row.addWidget(spoolman_btn)

        accept_btn = BlocksCustomButton(page)
        accept_btn.setFixedSize(200, 80)
        accept_btn.setText("Accept")
        accept_btn.setFont(font)
        accept_btn.clicked.connect(self.on_popup_accept)
        btn_row.addWidget(accept_btn)

        root.addLayout(btn_row)
        return page

    def _setup_color_wheel(self) -> None:
        self._color_wheel = ColorWheelWidget(self)
        self._color_wheel.hide()
        self._color_wheel_popup = BasePopup(self, True, False)
        self._color_wheel_popup.x_offset = 0.95
        self._color_wheel_popup.y_offset = 0.95
        self._color_wheel_popup.add_widget(self._color_wheel)
        self._color_wheel.request_back.connect(self._color_wheel_popup.hide)
        self._color_wheel.color_selected.connect(self._on_color_selected)

    def _open_color_wheel(self, field: "BlocksCustomLinEdit") -> None:
        self._color_target_field = field
        self._color_wheel.set_color_hex(field.text().strip("#") or "ffffff")
        self._color_wheel_popup.show()

    @QtCore.pyqtSlot(str, name="on-color-selected")
    def _on_color_selected(self, hex_str: str) -> None:
        if self._color_target_field is not None:
            self._color_target_field.setText(hex_str)
            self._color_target_field.editingFinished.emit()
            self._color_target_field = None

    def _build_spool_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        root = QtWidgets.QVBoxLayout(page)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        # Header
        hdr = QtWidgets.QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.setSpacing(0)
        back_btn = IconButton(page)
        back_btn.setFixedSize(QtCore.QSize(60, 60))
        back_btn.setFlat(True)
        back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        back_btn.clicked.connect(lambda: self._popup_stack.setCurrentIndex(0))
        hdr.addWidget(back_btn)

        title_font = QtGui.QFont()
        title_font.setPointSize(18)
        title_lbl = QtWidgets.QLabel("Select Spool", page)
        title_lbl.setFont(title_font)
        title_lbl.setFixedHeight(60)
        title_lbl.setStyleSheet("color: white; background: transparent;")
        title_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(title_lbl, 1)

        manage_btn = IconButton(page)
        manage_btn.setFixedSize(QtCore.QSize(60, 60))
        manage_btn.setFlat(True)
        manage_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/LCD_settings.svg"))
        manage_btn.clicked.connect(lambda: self.request_open_add_spoolman.emit())
        hdr.addWidget(manage_btn)

        root.addLayout(hdr)

        # List
        frame = BlocksCustomFrame(page)
        frame_lay = QtWidgets.QVBoxLayout(frame)
        frame_lay.setContentsMargins(4, 4, 4, 4)

        self._spool_list_view = QtWidgets.QListView(frame)
        self._spool_list_view.setMouseTracking(True)
        self._spool_list_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self._spool_list_view.setStyleSheet("background-color: transparent;")
        self._spool_list_view.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self._spool_list_view.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._spool_list_view.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._spool_list_view.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection
        )
        self._spool_list_view.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        QtWidgets.QScroller.grabGesture(
            self._spool_list_view, QtWidgets.QScroller.ScrollerGestureType.TouchGesture
        )
        QtWidgets.QScroller.grabGesture(
            self._spool_list_view,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        self._spool_model = EntryListModel()
        self._spool_model.setParent(self._spool_list_view)
        self._spool_delegate = EntryDelegate()
        self._spool_list_view.setModel(self._spool_model)
        self._spool_list_view.setItemDelegate(self._spool_delegate)
        self._spool_delegate.item_selected.connect(self._on_spool_selected)

        self._spool_load_widget = LoadingOverlayWidget(
            frame, LoadingOverlayWidget.AnimationGIF.DEFAULT
        )

        frame_lay.addWidget(self._spool_list_view, 1)
        frame_lay.addWidget(self._spool_load_widget, 1)
        self._spool_list_view.hide()

        root.addWidget(frame, 1)
        return page

    def on_mmu_state_changed(self, mmu_state):
        if mmu_state is None:
            return
        self.status = mmu_state
        if not self._previous_gate_states:
            for gate_info in mmu_state.gates:
                self._previous_gate_states[gate_info.index] = gate_info.status in [
                    GateStatus.AVAILABLE,
                    GateStatus.AVAILABLE_FROM_BUFFER,
                ]
        for i in range(len(mmu_state.gates)):
            self.addSpool(mmu_state.gates[i])
        self.update()
        self._on_selection(mmu_state.gate)

    def on_pre_gate(self, gate_index: int, detected: bool):
        previous_state = self._previous_gate_states.get(gate_index)
        self._previous_gate_states[gate_index] = detected
        if previous_state is False and detected is True:
            self.popup_gates.append({"gate": gate_index})
            self.handle_popup()

    def handle_popup(self):
        if self.popup.isVisible():
            return
        if not self.popup_gates:
            return
        self.pre_gate_idx = self.popup_gates.popleft()
        gate = self.pre_gate_idx["gate"]
        self._popup_title_lbl.setText(f"Filament Detected — Gate {gate}")
        self._popup_stack.setCurrentIndex(0)
        self._selected_spool_id = -1
        self.popup.show()

    def on_popup_accept(self):
        gate = self.pre_gate_idx["gate"]
        name = self._popup_name.text().strip()
        color = self._popup_color.text().strip("#").strip()
        material = self._popup_material.text().strip()
        try:
            temp = int(self._popup_temp.text().strip("°º").strip())
        except ValueError:
            temp = -1

        parts = [f"MMU_GATE_MAP GATE={gate}"]
        if self._selected_spool_id != -1:
            parts.append(f"SPOOLID={self._selected_spool_id}")
            parts.append("AVAILABLE=1")
        if name:
            parts.append(f'NAME="{name}"')
        if material:
            parts.append(f'MATERIAL="{material}"')
        if color:
            parts.append(f'COLOR="{color}"')
        if temp > 0:
            parts.append(f"TEMP={temp}")
        parts.append("QUIET=1")

        self.request_gate_map.emit(" ".join(parts))
        self.request_gate_map.emit("MMU_GATE_MAP REFRESH=1")
        self.popup.hide()
        self.handle_popup()

    @QtCore.pyqtSlot(dict, name="on-spools-received")
    def on_spools_received(self, result: dict) -> None:
        self._spool_load_widget.hide()
        self._spool_list_view.show()
        if result.get("error") is not None:
            return
        spools = result.get("response")
        if not isinstance(spools, list):
            return
        self._spool_id_map = {}
        self._spool_model.clear()
        self._spool_delegate.clear()
        self._spool_model.add_item(
            ListItem(
                text="+ Add Spool",
                _lfontsize=14,
                height=60,
            )
        )
        for spool in spools:
            spool_id = spool.get("id", "?")
            filament = spool.get("filament") or {}
            name = filament.get("name") or f"Spool #{spool_id}"
            material = filament.get("material") or ""
            self._spool_model.add_item(
                ListItem(
                    text=name,
                    right_text=material,
                    left_icon=self._make_color_pixmap(filament),
                    _lfontsize=14,
                    _rfontsize=12,
                    height=60,
                )
            )
            self._spool_id_map[name] = spool

    @QtCore.pyqtSlot(ListItem, name="on-spool-selected")
    def _on_spool_selected(self, item: ListItem) -> None:
        if not item:
            return
        if item.text == "+ Add Spool":
            self.request_open_add_spoolman.emit()
            return
        spool = self._spool_id_map.get(item.text)
        if not spool:
            return
        filament = spool.get("filament") or {}
        self._selected_spool_id = spool.get("id", -1)
        self._popup_name.setText(filament.get("name") or "")
        self._popup_color.setText(filament.get("color_hex") or "ffffff")
        self._popup_material.setText(filament.get("material") or "")
        temp = filament.get("settings_extruder_temp")
        self._popup_temp.setText(str(temp) if temp is not None else "")
        self._popup_stack.setCurrentIndex(0)

    def _on_spoolman_clicked(self):
        self._spool_list_view.hide()
        self._spool_load_widget.show()
        self._popup_stack.setCurrentIndex(1)
        self.request_spools.emit()

    @staticmethod
    def _make_color_pixmap(filament: dict) -> QtGui.QPixmap:
        size = 32
        pixmap = QtGui.QPixmap(size, size)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        multi_hexes = filament.get("multi_color_hexes")
        color_hex = filament.get("color_hex")
        if multi_hexes:
            hexes = [h.strip() for h in multi_hexes.split(",") if h.strip()]
            if hexes:
                clip = QtGui.QPainterPath()
                clip.addRoundedRect(QtCore.QRectF(0, 0, size, size), 6, 6)
                painter.setClipPath(clip)
                stripe_w = size / len(hexes)
                for i, h in enumerate(hexes):
                    painter.fillRect(
                        QtCore.QRectF(i * stripe_w, 0, stripe_w, size),
                        QtGui.QColor(f"#{h}"),
                    )
        elif color_hex:
            painter.setBrush(QtGui.QColor(f"#{color_hex}"))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QtCore.QRectF(0, 0, size, size), 6, 6)
        else:
            painter.setPen(QtGui.QColor(180, 180, 180))
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(QtCore.QRectF(1, 1, size - 2, size - 2), 6, 6)
        painter.end()
        return pixmap

    def addSpool(self, gate_info: GateInfo):
        self.carousel.addSpool(
            QtGui.QColor("#" + str(gate_info.color)[:6]),
            gate_info.index,
            gate_info.material,
            int(gate_info.temperature or 0),
            gate_info.status,
        )

    def _select_gate(self, idx: int):
        self.carousel.selectIndex(idx)
        self.amu_manager.select_gate(idx)

    def _on_selection(self, idx: int):
        if idx < 0 or idx >= len(self.carousel.buttons):
            return
        btn = self.carousel.buttons[idx]
        self.current_index = idx
        self.info_panel.update_for_slot(idx, btn)
        self.carousel.selectIndex(idx)
        self.info_panel.setFilamentStatus(self.status)

    @QtCore.pyqtSlot("PyQt_PyObject", str, str, str, int, name="request-keyboard")
    def _on_show_keyboard(
        self,
        field: QtWidgets.QLineEdit,
        prefix: str = "",
        suffix: str = "",
        pattern: str = "",
        max_char: int = 0,
    ) -> None:
        self._current_field = field
        self._qwerty.setPrefix(prefix)
        self._qwerty.setSuffix(suffix)
        self._qwerty.setPatern(pattern)
        self._qwerty.set_value(field.text().strip("#ºg"))
        self._qwerty.setMaxLength(max_char)
        self._qwerty.show()

    def _on_qwerty_go_back(self) -> None:
        self._qwerty.hide()

    def _on_qwerty_value_selected(self, value: str) -> None:
        self._qwerty.hide()
        if self._current_field:
            self._current_field.setText(value)
            self._current_field.editingFinished.emit()

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

    @QtCore.pyqtSlot(str, int, name="on-gate-temp-change")
    def _on_gate_temp_change(self, _name: str, value: int) -> None:
        self._numpad_popup.hide()
        self.info_panel._lbl_temp.setText(str(value))
        self.info_panel._lbl_temp.editingFinished.emit()

    @QtCore.pyqtSlot(str, int, name="on-gate-weight-change")
    def _on_gate_weight_change(self, _name: str, value: int) -> None:
        self._numpad_popup.hide()
        self.info_panel._lbl_weight.setText(str(value))
        self.info_panel._lbl_weight.editingFinished.emit()

    @QtCore.pyqtSlot(str, int, name="on-popup-temp-change")
    def _on_popup_temp_change(self, _name: str, value: int) -> None:
        self._numpad_popup.hide()
        self._popup_temp.setText(str(value))
        self._popup_temp.editingFinished.emit()

    def _build_ui(self):
        self.setMinimumSize(720, 420)
        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setMinimumSize(720, 420)
        self.setObjectName("temperature_page")
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        widget.setObjectName("filament_control_page")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.filament_page_header_layout = QtWidgets.QHBoxLayout()
        self.filament_page_header_layout.setObjectName("filament_page_header_layout")

        self.spacerItem1 = QtWidgets.QSpacerItem(
            60,
            0,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.filament_page_header_layout.addItem(self.spacerItem1)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.filament_page_header_title = QtWidgets.QLabel(parent=self)
        self.filament_page_header_title.setSizePolicy(sizePolicy)
        self.filament_page_header_title.setMinimumSize(QtCore.QSize(0, 60))
        self.filament_page_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.filament_page_header_title.setFont(font)
        self.filament_page_header_title.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.filament_page_header_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.filament_page_header_title.setObjectName("filament_page_header_title")
        self.filament_page_header_layout.addWidget(
            self.filament_page_header_title,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.main_back_button = IconButton(parent=self)
        self.main_back_button.setSizePolicy(sizePolicy)
        self.main_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.main_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.main_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.main_back_button.setObjectName("main_back_button")
        self.filament_page_header_layout.addWidget(self.main_back_button)

        self.verticalLayout.addLayout(self.filament_page_header_layout)

        amu_widget = QtWidgets.QWidget(parent=self)
        root = QtWidgets.QVBoxLayout()
        root.setContentsMargins(0, 0, 0, 0)

        carousel_frame = BlocksCustomFrame(self)
        cf_layout = QtWidgets.QVBoxLayout()

        self.carousel = SpoolCarousel(carousel_frame)
        QsizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.carousel.setSizePolicy(QsizePolicy)
        cf_layout.addWidget(self.carousel)

        self.info_panel = SpoolInfoPanel(parent=self, amu_manager=self.amu_manager)
        sizePolicy2 = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.info_panel.setSizePolicy(sizePolicy2)

        cf_layout.addWidget(self.info_panel)
        cf_layout.setContentsMargins(0, 0, 0, 0)
        cf_layout.setSpacing(0)
        carousel_frame.setLayout(cf_layout)

        root.addWidget(carousel_frame)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        amu_widget.setLayout(root)
        self.verticalLayout.addWidget(amu_widget)
        widget.setLayout(self.verticalLayout)
        self.addWidget(widget)

        self.filament_page_header_title.setText(
            QtCore.QCoreApplication.translate("widget", "Filament Control")
        )
