import logging
from collections import deque
from typing import Deque

from devices.amu import AMUManager
from devices.amu.models import GateStatus
from lib.panels.widgets.addFilamentPage import AddFilamentPage
from lib.panels.widgets.addSpoolPage import AddSpoolPage
from lib.panels.widgets.amuPage import AMUpage
from lib.panels.widgets.basePopup import BasePopup
from lib.panels.widgets.basicFilamentPanel import BasicFilamentPanel
from lib.panels.widgets.colorWheelWidget import ColorWheelWidget
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from lib.panels.widgets.loadWidget import LoadingOverlayWidget
from lib.panels.widgets.numpadPage import CustomNumpad
from lib.panels.widgets.spoolmanPage import SpoolmanPage
from lib.printer import Printer
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from lib.utils.toolmap import MmuToolmapWidget
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)


class FilamentTab(QtWidgets.QStackedWidget):
    request_filament_change_page = QtCore.pyqtSignal(name="filament_change_page")
    request_filament_load = QtCore.pyqtSignal(name="filament_load_t1")
    request_back = QtCore.pyqtSignal(name="request_back")
    request_change_page = QtCore.pyqtSignal(int, int, name="request_change_page")
    request_change_tab = QtCore.pyqtSignal(int, name="request_change_tab")
    request_toolhead_count = QtCore.pyqtSignal(int, name="toolhead_number_received")
    run_gcode = QtCore.pyqtSignal(str, name="run_gcode")
    call_load_panel = QtCore.pyqtSignal(bool, str, bool, name="call-load-panel")

    def __init__(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False
        self._popup_callback = None
        self.ui = self.setupUi()
        self.change_page(self.indexOf(self.ui))

        self._previous_gate_states: dict[int, bool] = {}
        self.pre_gate_idx = {}
        self.popup_gates: Deque = deque()
        self._spool_id_map: dict[str, dict] = {}
        self._current_field: QtWidgets.QLineEdit | None = None
        self._color_target_field = None
        self.moonraker_run = True

        self._setup_pre_gate_popup()
        self._setup_load_popup()
        self.amu_manager.mmu_state_changed.connect(self.on_mmu_state_changed)

        self._extruder_current_temp = 0.0
        self._extruder_target_temp = 0.0
        self.printer.extruder_update.connect(self.on_extruder_update)

        self.spoolmanPanel = SpoolmanPage(self)
        self.addWidget(self.spoolmanPanel)
        self.fp_button_2.clicked.connect(
            lambda: self.change_page(self.indexOf(self.spoolmanPanel))
        )
        self.spoolmanPanel.request_back.connect(self.request_back)

        self.spoolmanPanel.request_spools.connect(
            lambda: self.ws.api.spoolman_proxy(
                "GET", "/v1/spool", callback=self.spoolmanPanel.on_spools_received
            )
        )
        self.spoolmanPanel.request_get_spool_id.connect(
            lambda: self.ws.api.get_spool_id()
        )
        self.spoolmanPanel.request_delete_spool.connect(
            lambda spool_id: self.ws.api.delete_spool(
                spool_id, callback=self.spoolmanPanel.on_delete_spool_result
            )
        )
        self.spoolmanPanel.request_filaments.connect(
            lambda: self.ws.api.get_filaments(
                callback=self.spoolmanPanel.on_filaments_received
            )
        )
        self.spoolmanPanel.request_add_spool.connect(
            lambda filament_id, body: self.ws.api.add_spool(
                filament_id, body, callback=self.spoolmanPanel.on_add_spool_result
            )
        )
        self.spoolmanPanel.request_add_filament.connect(
            lambda body: self.ws.api.add_filament(
                body, callback=self.spoolmanPanel.on_add_filament_result
            )
        )

        self._basic_panel = BasicFilamentPanel(
            self.printer, self.cfg, parent=self, load_popup=self.load_popup
        )
        self._basic_panel.run_gcode.connect(self.run_gcode)
        self._basic_panel.call_load_panel.connect(self.call_load_panel)
        self._basic_panel.request_back.connect(self.request_back)
        self._basic_panel.request_change_tab.connect(self.request_change_tab)
        self._basic_panel.filament_selected.connect(self.open_pregate_popup)
        self.amu_manager.mmu_state_changed.connect(
            self._basic_panel.on_mmu_state_changed
        )
        self.addWidget(self._basic_panel)
        self.fp_button_1.clicked.connect(
            lambda: self.change_page(self.indexOf(self._basic_panel))
        )

        self.ws.connected_signal.connect(self.handle_moonraker_components)

        self.run_gcode.connect(self.ws.api.run_gcode)

    def handle_moonraker_components(self):
        if self.moonraker_run:
            components = self.ws._moonRest.get_server_info()
            if "spoolman" not in components["result"].get("components", []):
                self.fp_button_2.hide()
                self._popup_stack.addWidget(self._build_form_page())
                self._popup_stack.addWidget(self._build_spool_page())
            else:
                self.fp_button_2.show()
                self._popup_stack.addWidget(self._build_spool_page())
                self._popup_stack.addWidget(self._build_form_page())
                self.request_filament_change_page.emit()
            self.moonraker_run = False

    def change_page(self, index: int) -> None:
        """Requests a page change page to the global manager

        Args:
            index (int): page index
        """
        self.request_change_page.emit(1, index)

    def _setup_load_popup(self) -> None:
        self.load_popup = BasePopup(self, floating=False, dialog=False)
        load_container = QtWidgets.QWidget(self.load_popup)
        load_layout = QtWidgets.QVBoxLayout(load_container)

        self.load_status_label = QtWidgets.QLabel(load_container)
        self.load_status_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label_font = QtGui.QFont()
        label_font.setPointSize(20)
        self.load_status_label.setFont(label_font)
        self.load_status_label.setStyleSheet("color: #ffffff; background: transparent;")
        self.load_status_label.setMaximumHeight(100)
        load_layout.addWidget(self.load_status_label)

        self.load_status_widget = MmuToolmapWidget(load_container)
        load_layout.addWidget(self.load_status_widget)

        self.load_popup.add_widget(load_container)

    @QtCore.pyqtSlot(str, str, float, name="on-extruder-update")
    def on_extruder_update(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        if extruder_name != "extruder":
            return
        if field == "temperature":
            self._extruder_current_temp = new_value
        elif field == "target":
            self._extruder_target_temp = new_value
        else:
            return
        self.load_status_widget.set_temps(
            self._extruder_current_temp, self._extruder_target_temp
        )

    def _setup_pre_gate_popup(self) -> None:
        self._numpad = CustomNumpad(self)
        self._numpad.hide()
        self._numpad_popup = BasePopup(self, False, False)
        self._numpad_popup.add_widget(self._numpad)
        self._numpad.numpad_back_btn.clicked.connect(self._numpad_popup.hide)

        self._qwerty = CustomQwertyKeyboard(self)
        self._qwerty.hide()
        self._qwerty.numpad_back_btn.clicked.connect(self._on_qwerty_go_back)
        self._qwerty.value_selected.connect(self._on_qwerty_value_selected)

        self._color_wheel = ColorWheelWidget(self)
        self._color_wheel.hide()
        self._color_wheel_popup = BasePopup(self, True, False)
        self._color_wheel_popup.x_offset = 0.95
        self._color_wheel_popup.y_offset = 0.95
        self._color_wheel_popup.add_widget(self._color_wheel)
        self._color_wheel.request_back.connect(self._color_wheel_popup.hide)
        self._color_wheel.color_selected.connect(self._on_color_selected)

        self._popup_stack = QtWidgets.QStackedWidget()

        self.popup = BasePopup(self, False, False)
        self.popup.add_widget(self._popup_stack)

    def _build_form_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        root = QtWidgets.QVBoxLayout(page)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(8)

        hdr = QtWidgets.QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.setSpacing(0)
        back_btn = IconButton(page)
        back_btn.setFixedSize(QtCore.QSize(60, 60))
        back_btn.setFlat(True)
        back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        back_btn.clicked.connect(lambda: self.popup.hide())
        hdr.addWidget(back_btn)

        self._popup_title_lbl = QtWidgets.QLabel("Filament Detected", page)
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        self._popup_title_lbl.setFont(title_font)
        self._popup_title_lbl.setStyleSheet("color: white; background: transparent;")
        self._popup_title_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._popup_title_lbl.setFixedHeight(50)
        hdr.addWidget(self._popup_title_lbl, 1)

        blank = QtWidgets.QWidget(self)

        blank.setFixedSize(60, 60)
        hdr.addWidget(blank)

        root.addLayout(hdr)

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
        self._popup_temp.setText("250")

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
            lambda: self._open_numpad(
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

        skip_btn = BlocksCustomButton(page)
        skip_btn.setFixedSize(230, 80)
        skip_btn.setText("Skip")
        skip_btn.setFont(font)
        skip_btn.clicked.connect(self.handle_skip_button)
        skip_btn.setPixmap(
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
        )
        btn_row.addWidget(skip_btn)

        accept_btn = BlocksCustomButton(page)
        accept_btn.setFixedSize(230, 80)
        accept_btn.setText("Accept")
        accept_btn.setFont(font)
        accept_btn.clicked.connect(self.on_popup_accept)
        accept_btn.setPixmap(QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg"))
        btn_row.addWidget(accept_btn)

        root.addLayout(btn_row)
        return page

    def _build_spool_page(self) -> QtWidgets.QWidget:
        page = QtWidgets.QWidget()
        root = QtWidgets.QVBoxLayout(page)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        hdr = QtWidgets.QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.setSpacing(0)

        blank = QtWidgets.QWidget(self)
        blank.setFixedSize(60, 60)
        hdr.addWidget(blank)

        title_font = QtGui.QFont()
        title_font.setPointSize(18)
        self._spoolman_title_lbl = QtWidgets.QLabel("Select Spool", page)
        self._spoolman_title_lbl.setFont(title_font)
        self._spoolman_title_lbl.setFixedHeight(60)
        self._spoolman_title_lbl.setStyleSheet("color: white; background: transparent;")
        self._spoolman_title_lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(self._spoolman_title_lbl, 1)
        back_btn = IconButton(page)
        back_btn.setFixedSize(QtCore.QSize(60, 60))
        back_btn.setFlat(True)
        back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        back_btn.clicked.connect(lambda: self.popup.hide())
        hdr.addWidget(back_btn)

        root.addLayout(hdr)

        vertical_layout = QtWidgets.QHBoxLayout()

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

        self._add_spool_page = AddSpoolPage(self)
        self._add_filament_page = AddFilamentPage(self)

        self._add_stack = QtWidgets.QStackedWidget()
        self._add_stack.addWidget(self._add_spool_page)  # index 0
        self._add_stack.addWidget(self._add_filament_page)  # index 1

        self._add_filament_page.accepted.connect(self._add_spool_page.reset)

        self._add_popup = BasePopup(self, False, False)
        self._add_popup.add_widget(self._add_stack)

        self._add_spool_page.request_filaments.connect(
            lambda: self.ws.api.get_filaments(
                callback=self._add_spool_page.on_filaments_received
            )
        )
        self._add_spool_page.cancelled.connect(self._add_popup.hide)

        self._add_spool_page.request_add_spool.connect(
            lambda filament_id, body: self.ws.api.add_spool(
                filament_id,
                body,
                callback=self._add_spool_page.on_add_spool_result,
            )
        )
        self._add_spool_page.accepted.connect(
            lambda: {
                self.ws.api.spoolman_proxy(
                    "GET", "/v1/spool", callback=self.on_spools_received
                ),
                self._add_popup.hide(),
            }
        )

        self._add_spool_page.open_add_filament.connect(
            lambda: self._add_stack.setCurrentIndex(1)
        )

        self._add_filament_page.request_add_filament.connect(
            lambda body: self.ws.api.add_filament(
                body,
                callback=self._add_filament_page.on_add_filament_result,
            )
        )
        self._add_filament_page.request_add_manufacturer.connect(
            lambda body: self.ws.api.add_manufacturer(
                body,
                callback=self._add_filament_page.on_add_manufacturer_result,
            )
        )

        self._add_filament_page.accepted.connect(
            lambda: self._add_stack.setCurrentIndex(0)
        )
        self._add_filament_page.cancelled.connect(
            lambda: self._add_stack.setCurrentIndex(0)
        )

        vertical_layout.addWidget(frame)

        frame_2 = BlocksCustomFrame(page)
        frame_2_lay = QtWidgets.QVBoxLayout(frame_2)
        frame_2_lay.setContentsMargins(4, 4, 4, 4)
        key_font = QtGui.QFont()
        key_font.setPointSize(12)

        val_font = QtGui.QFont()
        val_font.setPointSize(14)

        def _add_row(title_text: str) -> QtWidgets.QLabel:
            row = QtWidgets.QHBoxLayout()
            row.setSpacing(4)
            title = QtWidgets.QLabel(title_text, self)
            title.setFont(key_font)
            title.setStyleSheet("color: rgb(180,180,180); background: transparent;")
            title.setFixedHeight(32)
            title.setMinimumWidth(80)
            title.setMaximumWidth(110)
            value = QtWidgets.QLabel("—", self)
            value.setFont(val_font)
            value.setStyleSheet("color: white; background: transparent;")
            value.setFixedHeight(32)
            value.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            row.addWidget(title, 0)
            row.addWidget(value, 1)
            frame_2_lay.addLayout(row)
            return value

        self.filament_name_label = _add_row("Name:")
        self.vendor_label = _add_row("Vendor:")
        self.material_label = _add_row("Material:")
        self.weight_label = _add_row("Remaining:")

        font = QtGui.QFont()
        font.setPointSize(17)

        self.skip_btn = BlocksCustomButton(frame_2)
        self.skip_btn.setText("Skip")
        self.skip_btn.setFixedSize(QtCore.QSize(230, 80))
        self.skip_btn.setFont(font)
        self.skip_btn.setPixmap(
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
        )
        self.skip_btn.clicked.connect(self.handle_skip_button)

        self.accept_btn = BlocksCustomButton(frame_2)
        self.accept_btn.setText("Accept")
        self.accept_btn.setFixedSize(QtCore.QSize(230, 80))
        self.accept_btn.setPixmap(QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg"))
        self.accept_btn.setFont(font)
        self.accept_btn.clicked.connect(lambda: self._on_spool_selected())

        frame_2_lay.addWidget(
            self.skip_btn, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        frame_2_lay.addWidget(
            self.accept_btn, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        vertical_layout.addWidget(frame_2)
        root.addLayout(vertical_layout, 1)

        return page

    def handle_skip_button(self):
        gate = self.pre_gate_idx.get("gate", 0)
        self.popup.hide()
        self._reset_popup()
        self.run_gcode.emit(
            f"MMU_GATE_MAP GATE={gate} MATERIAL=N/A NAME=N/A COLOR=FFFFFF SPOOLID=-1 TEMP=250 QUIET=1"
        )
        if self._popup_callback is not None:
            try:
                self._popup_callback()
            except Exception as e:
                logger.error(f"Error executing pre-gate accept callback: {e}")
            finally:
                self._popup_callback = None

    def handle_popup(self, force=False):
        """Handles showing the popup for pre-gate filament detection.
        If multiple gates trigger, they will be queued and shown one at a time.

        Args:
            force (bool): If True, forces the popup to open even if no gates are queued.
        """
        if self.popup.isVisible():
            return
        self.ws.api.spoolman_proxy("GET", "/v1/spool", callback=self.on_spools_received)
        if not self.popup_gates:
            if force:
                self.pre_gate_idx = {"gate": 0}
                msg = (
                    f"{self._material_filter} Filament Info"
                    if self._material_filter
                    else "Load filament information"
                )
                self._popup_title_lbl.setText(msg)
                self._spoolman_title_lbl.setText(msg)
            else:
                return
        else:
            self.pre_gate_idx = self.popup_gates.popleft()
            gate = self.pre_gate_idx.get("gate", -1)
            self._popup_title_lbl.setText(f"Filament Detected — Gate {gate}")
            self._spoolman_title_lbl.setText(f"Filament Detected — Gate {gate}")

        self.popup.show()

    @QtCore.pyqtSlot(int, str, str, "PyQt_PyObject", name="open-pregate-popup")
    def open_pregate_popup(self, temp, material, name, callback=None):
        self._popup_name.setText(name)
        self._popup_material.setText(material)
        self._popup_temp.setText(str(temp))
        self._popup_callback = callback
        self._material_filter = material

        self._add_spool_page.setFilter(material)
        self._add_filament_page.setData(material, temp)
        self.handle_popup(True)

    def on_popup_accept(self):
        """Handles the accept action from the pre-gate popup to send the appropriate G-code to map the gate to the spool."""
        gate = self.pre_gate_idx.get("gate", 0)
        name = self._popup_name.text().strip() or "N/A"
        color = self._popup_color.text().strip("#").strip()
        material = self._popup_material.text().strip()
        try:
            temp = int(self._popup_temp.text().strip("°º").strip())
        except ValueError:
            temp = -1

        parts = [f"MMU_GATE_MAP GATE={gate} SPOOLID=-1"]
        if name:
            parts.append(f'NAME="{name}"')
        if material:
            parts.append(f'MATERIAL="{material}"')
        if color:
            parts.append(f'COLOR="{color}"')
        if temp > 0:
            parts.append(f"TEMP={temp}")
        parts.append("QUIET=1")

        self.run_gcode.emit(" ".join(parts))
        self.run_gcode.emit("MMU_GATE_MAP REFRESH=1")

        if self._popup_callback is not None:
            try:
                self._popup_callback()
            except Exception as e:
                logger.error(f"Error executing pre-gate accept callback: {e}")
            finally:
                self._popup_callback = None

        self._reset_popup()
        self.popup.hide()
        self._add_spool_page.setFilter(None)
        self._add_filament_page.setData("---", 0)
        self.handle_popup()

    def _reset_popup(self):
        self._popup_name.setText("")
        self._popup_color.setText("ffffff")
        self._popup_material.setText("")
        self._popup_temp.setText("250")

    @QtCore.pyqtSlot(dict, name="on-spools-received")
    def on_spools_received(self, result: dict) -> None:
        """Handles the result from the API call to get spools for the spoolman page."""
        self._spool_load_widget.hide()
        self._spool_list_view.show()

        self.reset_spool_info()

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
            if (
                self._material_filter
                and self._material_filter.lower() not in material.lower()
            ):
                continue

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
        self.update()

    def _on_spool_selected(self) -> None:
        item = self._spool_model.get_selected_item()
        if item is None:
            return
        spool = self._spool_id_map.get(item.text)

        if self.sender() != self.accept_btn:
            if item.text == "+ Add Spool":
                self._add_popup.show()
                return
            if spool is None:
                return
            self.accept_btn.setEnabled(True)
            filament = spool.get("filament") or {}
            self.filament_name_label.setText(item.text)
            self.material_label.setText(filament.get("material", "N/A"))
            self.weight_label.setText(
                f"{spool.get('remaining_weight')} g"
                if spool.get("remaining_weight") is not None
                else "N/A"
            )
            self.vendor_label.setText(
                filament.get("vendor", "N/A").get("name", "N/A")
                if filament.get("vendor")
                else "N/A"
            )

            return
        if not spool:
            return
        filament = spool.get("filament") or {}
        f_id = spool.get("id", -1)
        f_name = filament.get("name", "N/A")
        f_color = filament.get("color_hex", "ffffff")
        f_material = filament.get("material", "")
        f_temp = filament.get("settings_extruder_temp", -1)
        gate = self.pre_gate_idx.get("gate", 0)

        self.accept_btn.setEnabled(False)
        self.popup.hide()
        self._add_spool_page.setFilter(None)
        self._add_filament_page.setData("---", 0)
        self.run_gcode.emit(
            f"MMU_GATE_MAP GATE={gate} SPOOLID={f_id} NAME='{f_name}' MATERIAL='{f_material}' COLOR='{f_color}' TEMP={f_temp} QUIET=1"
        )
        if self._popup_callback is not None:
            try:
                self._popup_callback()
            except Exception as e:
                logger.error(f"Error executing pre-gate accept callback: {e}")
            finally:
                self._popup_callback = None

    def reset_spool_info(self):
        self.filament_name_label.setText("N/A")
        self.material_label.setText("N/A")
        self.weight_label.setText("N/A")
        self.vendor_label.setText("N/A")
        self.accept_btn.setEnabled(False)

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

    def _open_numpad(
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

        def _on_value(n, v):
            self._numpad_popup.hide()
            callback(n, v)

        self._numpad.value_selected.connect(_on_value)
        self._numpad.set_name(name)
        self._numpad.set_value(current_value)
        self._numpad.set_min_value(min_value)
        self._numpad.set_max_value(max_value)
        self._numpad_popup.show()

    @QtCore.pyqtSlot(str, int, name="on-popup-temp-change")
    def _on_popup_temp_change(self, _name: str, value: int) -> None:
        self._popup_temp.setText(str(value))

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
        self._qwerty.setPattern(pattern)
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

    def _open_color_wheel(self, field) -> None:
        self._color_target_field = field
        self._color_wheel.set_color_hex(field.text().strip("#") or "ffffff")
        self._color_wheel_popup.show()
        self._color_wheel_popup.raise_()

    @QtCore.pyqtSlot(str, name="on-color-selected")
    def _on_color_selected(self, hex_str: str) -> None:
        if self._color_target_field is not None:
            self._color_target_field.setText(hex_str)
            self._color_target_field.editingFinished.emit()
            self._color_target_field = None

    def on_mmu_state_changed(self, mmu_state):
        """Handles changes in the MMU state from the AMU manager to update the UI and show the load panel when loading/unloading."""
        for gate_info in mmu_state.gates:
            previous_state = self._previous_gate_states.get(gate_info.index)
            self._previous_gate_states[gate_info.index] = gate_info.status in [
                GateStatus.AVAILABLE,
                GateStatus.AVAILABLE_FROM_BUFFER,
            ]
            if (
                previous_state is False
                and self._previous_gate_states[gate_info.index] is True
            ):
                self.popup_gates.append({"gate": gate_info.index})
                if len(mmu_state.gates) > 1:
                    self.handle_popup()

        if not self.amu_configured:
            if len(mmu_state.gates) > 1:
                self.amupage = AMUpage(
                    self.amu_manager, parent=self, load_popup=self.load_popup
                )
                self.addWidget(self.amupage)
                try:
                    self.removeWidget(self._basic_panel)
                    self._basic_panel.deleteLater()
                    self.fp_button_1.disconnect()
                except TypeError:
                    pass
                self.fp_button_1.clicked.connect(
                    lambda: self.change_page(self.indexOf(self.amupage))
                )
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_change_tab.connect(self.request_change_tab)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_numpad[
                    str, int, "PyQt_PyObject", int, int
                ].connect(self._open_numpad)
                self.printer.print_stats_update[str, str].connect(
                    self.amupage.on_print_stats_update
                )
                self.printer.print_stats_update[str, dict].connect(
                    self.amupage.on_print_stats_update
                )
                self.printer.print_stats_update[str, float].connect(
                    self.amupage.on_print_stats_update
                )
                self.amupage.request_keyboard.connect(self._on_show_keyboard)
                self.amupage.request_color_wheel.connect(self._open_color_wheel)

            self.amu_configured = True

        self.load_status_widget.set_filament_pos(
            mmu_state.filament_pos, mmu_state.bowden_progress
        )
        for sensor_name in ("mmu_pre_gate", "mmu_gate", "toolhead"):
            self.load_status_widget.set_sensor(
                sensor_name, bool(mmu_state.sensors.get(sensor_name))
            )
        self.load_status_widget.set_action(mmu_state.action)

        gate_info = mmu_state.current_gate_info
        raw_color = (
            str(gate_info.color).lstrip("#")[:6]
            if gate_info and gate_info.color
            else ""
        )
        parsed_color = QtGui.QColor("#" + raw_color) if raw_color else QtGui.QColor()
        if parsed_color.isValid():
            self.load_status_widget.set_gate_color(parsed_color)

        self.load_status_label.setText(mmu_state.action)

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.load_popup.hide()
                if not len(mmu_state.gates) > 1:
                    self._basic_panel.change_page(0)
        elif mmu_state.action in ("Loading", "Unloading"):
            self.load_state = True
            self.load_popup.show()

    def setupUi(self):
        self.resize(710, 410)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        widget = QtWidgets.QWidget()
        widget.setMinimumSize(QtCore.QSize(710, 410))
        widget.setMaximumSize(QtCore.QSize(710, 410))
        self.setObjectName("filament_page")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.fp_header_layout = QtWidgets.QHBoxLayout()
        self.fp_header_layout.setObjectName("fp_header_layout")

        self.fp_header_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                60,
                QtWidgets.QSizePolicy.Policy.Fixed,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )
        self.fp_header_title = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fp_header_title.sizePolicy().hasHeightForWidth()
        )
        self.fp_header_title.setSizePolicy(sizePolicy)
        self.fp_header_title.setMinimumSize(QtCore.QSize(300, 60))
        self.fp_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.fp_header_title.setFont(font)
        self.fp_header_title.setStyleSheet("background: transparent; color: white;")
        self.fp_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fp_header_title.setObjectName("fp_header_title")
        self.fp_header_layout.addWidget(self.fp_header_title)

        self.fp_header_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                60,
                QtWidgets.QSizePolicy.Policy.Fixed,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.verticalLayout.addLayout(self.fp_header_layout)
        self.fp_content_layout = QtWidgets.QGridLayout()
        self.fp_content_layout.setObjectName("fp_content_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        self.fp_button_1 = BlocksCustomButton(parent=self)
        self.fp_button_1.setSizePolicy(sizePolicy)
        self.fp_button_1.setMinimumSize(QtCore.QSize(250, 80))
        self.fp_button_1.setMaximumSize(QtCore.QSize(250, 80))
        self.fp_button_1.setFont(font)
        self.fp_button_1.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.fp_button_1.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.fp_button_1.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/filament_related/media/btn_icons/load_filament.svg"),
        )
        self.fp_button_1.setObjectName("fp_button_1")

        self.fp_content_layout.addWidget(self.fp_button_1, 1, 0, 1, 1)

        self.fp_button_2 = BlocksCustomButton(parent=self)
        self.fp_button_2.setSizePolicy(sizePolicy)
        self.fp_button_2.setMinimumSize(QtCore.QSize(10, 80))
        self.fp_button_2.setMaximumSize(QtCore.QSize(250, 80))
        self.fp_button_2.setFont(font)
        self.fp_button_2.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.fp_button_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.fp_button_2.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/filament_related/media/btn_icons/base dados spool 1.svg"),
        )
        self.fp_button_2.setObjectName("fp_button_2")

        self.fp_content_layout.addWidget(self.fp_button_2, 1, 1, 1, 1)

        self.verticalLayout.addLayout(self.fp_content_layout)
        widget.setLayout(self.verticalLayout)

        self.fp_content_layout.setRowMinimumHeight(
            0, int(87.5)
        )  # 87.5 to compensate for not having margin on the rest of the buttons
        self.fp_content_layout.setRowMinimumHeight(
            2, int(87.5)
        )  # dont ask how i got this value , it was try and repeat

        self.addWidget(widget)
        self.fp_header_title.setText("Filament")
        self.fp_button_1.setText("Filament\nControl")
        self.fp_button_2.setText("Spoolman")
