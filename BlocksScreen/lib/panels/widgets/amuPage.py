from PyQt6 import QtCore, QtGui, QtWidgets
import typing
from lib.utils.icon_button import IconButton
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_linedit import BlocksCustomLinEdit

from devices.amu.models import GateInfo, GateStatus


from lib.panels.widgets.basePopup import BasePopup

from devices.amu import AMUManager
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard

from collections import deque
from typing import Deque

from lib.panels.widgets.amuWidgets import SpoolCarousel , SpoolInfoPanel


class AMUpage(QtWidgets.QStackedWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )

    def __init__(self, amu_manager, parent=None):
        super().__init__(parent)
        self._previous_gate_states: dict[int, bool] = {}
        self.current_index = -1
        self.pre_gate_idx = -1
        self.amu_manager: AMUManager = amu_manager
        self.popup_gates: Deque = deque()

        self._build_ui()

        self.amu_manager.mmu_state_changed.connect(self.on_mmu_state_changed)
        self.on_mmu_state_changed(self.amu_manager.get_state())
        self.info_panel._lbl_color.editingFinished.connect(
            lambda: self.amu_manager.set_gate_color(
                self.current_index,
                self.info_panel._lbl_color.text().strip("#") + "FF",
            )
        )
        self.info_panel._lbl_mat.editingFinished.connect(
            lambda: self.amu_manager.set_gate_material(
                self.current_index, self.info_panel._lbl_mat.text().strip("º")
            )
        )
        self.info_panel._lbl_temp.editingFinished.connect(
            lambda: self.amu_manager.set_gate_temp(
                self.current_index, self.info_panel._lbl_temp.text().strip("º")
            )
        )

        # self.info_panel._lbl_weight.editingFinished.connect(lambda:self.amu_manager.set_gate_weight(self.current_index, int(self.info_panel._lbl_weight.text())))

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

    def _setup_popup(self):
        self.popup = BasePopup(self, False, False)
        self.popup_wiget = self._popup_widget_ui()
        self.popup.add_widget(self.popup_wiget)

    def on_mmu_state_changed(self, mmu_state):
        self.status = mmu_state
        if not self._previous_gate_states:
            for gate_info in mmu_state.gates:
                self._previous_gate_states[gate_info.index] = gate_info.status in [
                    GateStatus.AVAILABLE,
                    GateStatus.AVAILABLE_FROM_BUFFER,
                ]

        for i in range(len(mmu_state.gates)):
            gate_info = mmu_state.gates[i]
            self.addSpool(gate_info)
            self.update()
        self._on_selection(mmu_state.gate)

    def on_pre_gate(self, gate_index: int, detected: bool):
        """Only show popup when gate transitions from False to True."""
        previous_state = self._previous_gate_states.get(gate_index)
        self._previous_gate_states[gate_index] = detected
        if previous_state is False and detected is True:
            self.popup_gates.append({"gate":gate_index})
            self.handle_popup()
    
    def handle_popup(self):
        if self.popup.isVisible():
            return
        if not self.popup_gates:
            return
        self.pre_gate_idx = self.popup_gates.popleft()
        self.popup.ui.label.setText(f'Filament Detected on gate {self.pre_gate_idx["gate"]}')
        self.popup.show()


    def addSpool(
        self,
        gate_info: GateInfo,
    ):
        self.carousel.addSpool(
            QtGui.QColor("#" + str(gate_info.color)[:-2]),
            gate_info.index,
            gate_info.material,
            gate_info.temperature,
            gate_info.status,
        )

    def _select_gate(self, idx: int):
        self.carousel.selectIndex(self.current_index)
        self.amu_manager.select_tool(idx)

    def _on_selection(self, idx: int):
        btn = self.carousel.buttons[idx]
        self.current_index = idx
        self.info_panel.update_for_slot(idx, btn)
        self.carousel.selectIndex(idx)
        self.info_panel.setFilamentStatus(self.status)

    @QtCore.pyqtSlot("PyQt_PyObject",str , str , str , int,name="request-keyboard")
    def _on_show_keyboard(self, field: QtWidgets.QLineEdit , prefix:str = "" ,suffix: str = ""  ,pattern:str = "",max_char:int = 0) -> None:
        """Show the QWERTY keyboard panel, saving the originating panel and input field."""
        self._current_field = field
        self._qwerty.setPrefix(prefix)
        self._qwerty.setSuffix(suffix)
        self._qwerty.setPatern(pattern)
        self._qwerty.set_value(field.text().strip("#ºg"))
        self._qwerty.setMaxLength(max_char)
        self._qwerty.show()

    def _on_qwerty_go_back(self) -> None:
        """Hide the keyboard and return to the previously active panel."""
        self._qwerty.hide()

    def _on_qwerty_value_selected(self, value: str) -> None:
        """Apply the keyboard-selected *value* to the previously focused input field."""
        self._qwerty.hide()
        if self._current_field:
            self._current_field.setText(value)
            self._current_field.editingFinished.emit()

    def on_popup_accept(self):
        """Validate popup fields and save data if all are filled."""
        # Get the popup widget
        popup_widget = self.popup.ui
        
        # Get values from the line edits
        color = popup_widget._lbl_color.text().strip("#")+"ff"
        material = popup_widget._lbl_mat.text().strip()
        weight = popup_widget._lbl_weight.text().strip("g")
        temp = popup_widget._lbl_temp.text().strip(" º")
        

        
        self.amu_manager.set_gate_info(gate= self.pre_gate_idx["gate"] , material=material , color=color , spool_id=-1 , temperature=temp)
        self.popup.hide()
        self.handle_popup()
    


    def _popup_widget_ui(self):
        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(widget)

        font = QtGui.QFont()
        font.setPointSize(20)

        widget.label = QtWidgets.QLabel("Filament Detected")
        widget.label.setFont(font)
        widget.label.setStyleSheet("color:white")
        widget.label.setMinimumSize(0, 60)
        layout.addWidget(widget.label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        grid_widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(grid_widget)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(2)

        font = QtGui.QFont()
        font.setPointSize(14)

        def make_key(text):
            l = QtWidgets.QLabel(text)
            l.setStyleSheet("color: rgb(255,255,255);")
            l.setFont(font)
            return l

        def make_val(edit: bool = True, type: str = "keypad"):
            """Make either an editable line edit or a static label, depending on the *edit* flag. The *type* arg determines the signal emitted on edit (numpad vs qwerty).

            Args:
                text (str, optional): _description_. Defaults to "—".
                edit (bool, optional): _description_. Defaults to True.
                type (str, optional): type of the input field gets ignored if edit is False. Defaults to "keypad".

            Returns:
                _type_: retuns label or line edit widget depending on the edit flag.
            """


            l = BlocksCustomLinEdit(self)
            l.setFont(font)
            l.setMinimumSize(0, 60)

            return l

        widget._lbl_color = make_val()
        widget._lbl_mat = make_val()
        widget._lbl_weight = make_val()
        widget._lbl_temp = make_val()

        rows = [
            ("Color", widget._lbl_color, "keypad"),
            ("Material", widget._lbl_mat, "keypad"),
            ("Weight", widget._lbl_weight, "numpad"),
            ("Temperature" , widget._lbl_temp, "numpad")
        ]
        self._swatch = QtWidgets.QLabel()
        self._swatch.setFixedSize(52, 52)
        self._swatch.setStyleSheet("border-radius: 2px; background: #222;")
        grid.addWidget(self._swatch , 0 , 3)
        for i, (key, val, _) in enumerate(rows):
            grid.addWidget(make_key(key), i, 0 , QtCore.Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(val, i, 1)

        layout.addWidget(grid_widget, 1)

        def _update_swatch(self):
            color = QtGui.QColor(str(widget._lbl_color.text())+"ff")
            self._swatch.setStyleSheet(
                f"border-radius: 12px;"
                f"background: rgb({color.red()},{color.green()},{color.blue()});"
                f"border: 2px solid white;"
            )

        widget._lbl_color.textChanged.connect(lambda: _update_swatch(self))

        widget._lbl_color.setText("#ffffff")
        widget._lbl_mat.setText("PLA")
        widget._lbl_weight.setText("1000g")
        widget._lbl_temp.setText("220")

        widget._lbl_color.clicked.connect(lambda: self._on_show_keyboard(widget._lbl_color,prefix="#" , max_char=6))
        widget._lbl_mat.clicked.connect(lambda: self._on_show_keyboard(widget._lbl_mat))
        widget._lbl_weight.clicked.connect(
            lambda: self._on_show_keyboard(widget._lbl_weight , suffix="g")
        )
        widget._lbl_temp.clicked.connect(lambda:self._on_show_keyboard(widget._lbl_temp,suffix="º" , pattern="int", max_char=3))

        

        horizntal_layout = QtWidgets.QHBoxLayout(self)

        self.button_1 = BlocksCustomButton(self)
        self.button_1.setMaximumSize(200, 80)
        self.button_1.setMinimumSize(200, 80)
        self.button_1.setText("Spoolman")

        self.button_2 = BlocksCustomButton(self)
        self.button_2.setMaximumSize(200, 80)
        self.button_2.setMinimumSize(200, 80)
        self.button_2.setText("Accept")
        self.button_2.clicked.connect(self.on_popup_accept)

        horizntal_layout.addWidget(self.button_1)
        horizntal_layout.addWidget(self.button_2)
        layout.addLayout(horizntal_layout)

        widget.setLayout(layout)
        return widget

    def _build_ui(self):
        self.setMinimumSize(720, 420)
        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setMinimumSize(720, 420)
        self.setObjectName("temperature_page")
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        widget.setObjectName("filament_control_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
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
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # Carousel inside its own BlocksCustomFrame
        carousel_frame = BlocksCustomFrame(self)

        cf_layout = QtWidgets.QVBoxLayout(self)

        self.carousel = SpoolCarousel(carousel_frame)
        QsizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.carousel.setSizePolicy(QsizePolicy)
        cf_layout.addWidget(self.carousel)

        # Info / operation panel
        self.info_panel = SpoolInfoPanel(parent=self, amu_manager=self.amu_manager)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.info_panel.setSizePolicy(sizePolicy)

        # self.info_panel.request_numpad[str, int, "PyQt_PyObject", int, int].connect(
        #     self.on_numpad_request
        # )

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

        _translate = QtCore.QCoreApplication.translate

        self.filament_page_header_title.setText(
            _translate("widget", "Filament Control")
        )
