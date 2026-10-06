import typing

from devices.amu import AMUManager, FilamentPos, MMUState
from lib.panels.widgets.FilamentTab.amuWidgets import SpoolCarousel, SpoolInfoPanel
from lib.panels.widgets.Common.basePopup import BasePopup
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class AMUpage(QtWidgets.QStackedWidget):
    _SELECT_DEBOUNCE_MS = 700

    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
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
        str, "PyQt_PyObject", name="request-color-wheel"
    )  # current hex, callback receiving the picked hex
    request_change_tab: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, name="request_change_tab"
    )

    def __init__(
        self, amu_manager, parent=None, *, load_popup: BasePopup | None = None
    ):
        super().__init__(parent)
        self.current_index = -1
        self.amu_manager: AMUManager = amu_manager
        self.load_popup = load_popup
        self.status = None
        self._pending_gate = -1
        self._select_timer = QtCore.QTimer(self)
        self._select_timer.setSingleShot(True)
        self._select_timer.setInterval(self._SELECT_DEBOUNCE_MS)
        self._select_timer.timeout.connect(self._send_select)
        self._build_ui()

        self.main_back_button.clicked.connect(self.request_back)

        self.amu_manager.mmu_state_changed.connect(self.on_mmu_state_changed)
        self.on_mmu_state_changed(self.amu_manager.get_state())
        self.info_panel.colorSelected.connect(self._on_color_selected)
        self.info_panel.colorSwatchClicked.connect(
            lambda hx: self.request_color_wheel.emit(
                hx, self.info_panel.set_selected_color
            )
        )
        self.info_panel._lbl_mat.editingFinished.connect(self._on_material_edited)
        self.info_panel._lbl_temp.editingFinished.connect(self._on_temp_edited)
        self.info_panel._lbl_temp.clicked.connect(self._open_temp_numpad)
        self.info_panel.request_keypad.connect(self.request_keyboard)
        self.info_panel.loadRequested.connect(self._on_load)
        self.info_panel.unloadRequested.connect(self._on_unload)
        self.info_panel.ejectRequested.connect(self.amu_manager.eject_gate)
        self.info_panel.checkRequested.connect(self.amu_manager.check_gate)

        self.carousel.selectionChanged.connect(self._select_gate)

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """Point the back button at request_back while printing, else at tab 0."""
        if isinstance(value, str) and "state" in field:
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
                self.main_back_button.clicked.connect(lambda: self.request_back.emit())

    def on_mmu_state_changed(self, mmu_state):
        """Sync the carousel and info panel to live MMU state."""
        prev = self.status
        self.status = mmu_state
        if mmu_state is None:
            self.current_index = -1
            self.info_panel.clear_slot(can_unload=False)
            return
        # apply_diff reuses the gates tuple when no gate_* key changed.
        if (
            prev is None
            or mmu_state.gates is not prev.gates
            or mmu_state.filament_pos != prev.filament_pos
        ):
            for gate_info in mmu_state.gates:
                self.carousel.addSpool(gate_info, mmu_state.filament_pos)
            self.update()
        self._on_selection(mmu_state)

    def _select_gate(self, idx: int):
        self.carousel.selectIndex(self.current_index)
        self._pending_gate = idx
        self._select_timer.start()

    def _send_select(self) -> None:
        self.amu_manager.select_gate(self._pending_gate)

    def _on_selection(self, mmu_state: MMUState) -> None:
        idx = mmu_state.gate
        if not 0 <= idx < len(self.carousel.buttons):
            self.current_index = -1
            self.info_panel.clear_slot(
                can_unload=mmu_state.filament_pos != FilamentPos.UNLOADED
            )
            return
        btn = self.carousel.buttons[idx]
        self.current_index = idx
        self.info_panel.update_for_slot(btn)
        self.carousel.selectIndex(idx)

    def _gate_temp(self) -> int | None:
        try:
            return round(float(self.info_panel._lbl_temp.text().strip("º")))
        except ValueError:
            return None

    def _on_gate_temp_change(self, _name: str, value: int) -> None:
        self.info_panel._lbl_temp.setText(str(value))
        self.info_panel._lbl_temp.editingFinished.emit()

    def _open_temp_numpad(self) -> None:
        self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
            "Temperature", self._gate_temp() or 0, self._on_gate_temp_change, 0, 500
        )

    def _on_temp_edited(self) -> None:
        temp = self._gate_temp()
        if temp is not None:
            self.amu_manager.set_gate_temp(self.current_index, temp)

    def _on_material_edited(self) -> None:
        material = self.info_panel._lbl_mat.text().strip()
        if material != "—":
            self.amu_manager.set_gate_material(self.current_index, material)

    def _on_color_selected(self, hex_str: str) -> None:
        self.amu_manager.set_gate_color(self.current_index, hex_str)

    def _on_load(self) -> None:
        if self.amu_manager.load_gate() and self.load_popup is not None:
            self.load_popup.show()

    def _on_unload(self) -> None:
        if self.amu_manager.unload() and self.load_popup is not None:
            self.load_popup.show()

    def _build_ui(self):
        self.setMinimumSize(700, 420)
        self.setObjectName("amu_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setMinimumSize(700, 420)
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
