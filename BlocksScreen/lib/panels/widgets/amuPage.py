import typing

from devices.amu import AMUManager
from devices.amu.models import GateInfo
from lib.panels.widgets.amuWidgets import SpoolCarousel, SpoolInfoPanel
from lib.panels.widgets.basePopup import BasePopup
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class AMUpage(QtWidgets.QStackedWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    request_gate_map: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request-gate-map"
    )
    request_numpad: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str, int, "PyQt_PyObject"],
        [str, int, "PyQt_PyObject", int, int],
        name="request-numpad",
    )
    request_keyboard: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        "PyQt_PyObject", str, str, str, int, name="request-keyboard"
    )
    request_color_wheel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        "PyQt_PyObject", name="request-color-wheel"
    )
    request_change_tab: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, name="request_change_tab"
    )

    def __init__(self, amu_manager, parent=None, load_popup: BasePopup | None = None):
        super().__init__(parent)
        self.current_index = -1
        self.amu_manager: AMUManager = amu_manager
        self._build_ui()
        self.load_popup = load_popup

        self.main_back_button.clicked.connect(self.request_back)

        self.amu_manager.mmu_state_changed.connect(self.on_mmu_state_changed)
        self.on_mmu_state_changed(self.amu_manager.get_state())
        self.info_panel._lbl_color.editingFinished.connect(
            lambda: self.amu_manager.set_gate_color(
                self.current_index,
                self.info_panel._lbl_color.text().strip("#"),
            )
        )
        self.info_panel._lbl_color.clicked.connect(
            lambda: self.request_color_wheel.emit(self.info_panel._lbl_color)
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

        self.info_panel.request_keypad.connect(self.request_keyboard)
        self.info_panel.loadRequested.connect(
            lambda: {
                self.amu_manager.load_gate(),
                self.load_popup.show(),
            }
        )
        self.info_panel.unloadRequested.connect(
            lambda: {
                self.amu_manager.unload(),
                self.load_popup.show(),
            }
        )
        self.info_panel.ejectRequested.connect(self.amu_manager.eject_gate)
        self.info_panel.checkRequested.connect(self.amu_manager.check_gate)

        self.carousel.selectionChanged.connect(self._select_gate)

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """Rewire the back button between "request_back" and "change to tab 0" based on print state."""
        if isinstance(value, str):
            if "state" in field:
                self.state = value
                if value in ("printing", "pausing", "paused", "resuming"):
                    try:
                        self.main_back_button.clicked.disconnect()
                    except TypeError:
                        pass

                    self.main_back_button.clicked.connect(
                        lambda: self.request_change_tab.emit(0)
                    )

                else:
                    try:
                        self.main_back_button.clicked.disconnect()
                    except TypeError:
                        pass
                    self.main_back_button.clicked.connect(
                        lambda: self.request_back.emit()
                    )

    def on_mmu_state_changed(self, mmu_state):
        """Refresh the carousel and the info panel's selected gate from live MMU state."""
        if mmu_state is None:
            return
        self.status = mmu_state
        for i in range(len(mmu_state.gates)):
            self.addSpool(mmu_state.gates[i])
        self.update()
        self._on_selection(mmu_state.gate)

    def addSpool(self, gate_info: GateInfo):
        """Add or refresh a gate's carousel button from its GateInfo."""
        self.carousel.addSpool(
            QtGui.QColor("#" + str(gate_info.color)[:6]),
            gate_info.index,
            gate_info.material,
            int(gate_info.temperature or 0),
            gate_info.status,
        )

    def _select_gate(self, idx: int):
        self.carousel.selectIndex(self.current_index)
        self.amu_manager.select_gate(idx)

    def _on_selection(self, idx: int):
        if idx < 0 or idx >= len(self.carousel.buttons):
            return
        btn = self.carousel.buttons[idx]
        self.current_index = idx
        self.info_panel.update_for_slot(idx, btn)
        self.carousel.selectIndex(idx)
        self.info_panel.setFilamentStatus(self.status)

    def _on_gate_temp_change(self, _name: str, value: int) -> None:
        self.info_panel._lbl_temp.setText(str(value))
        self.info_panel._lbl_temp.editingFinished.emit()

    def _on_gate_weight_change(self, _name: str, value: int) -> None:
        self.info_panel._lbl_weight.setText(str(value))
        self.info_panel._lbl_weight.editingFinished.emit()

    def _build_ui(self):
        self.setMinimumSize(700, 420)
        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setMinimumSize(700, 420)
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
