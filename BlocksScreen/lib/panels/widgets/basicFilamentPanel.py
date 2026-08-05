import enum
import logging
from functools import partial

from devices.amu.models import FilamentPos, GateStatus
from lib.filament import Filament
from lib.panels.widgets.popupDialogWidget import Popup
from lib.printer import Printer
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)


class FilamentTypes(enum.Enum):
    PLA = Filament(name="PLA", temperature=220)
    PETG = Filament(name="PETG", temperature=240)
    ABS = Filament(name="ABS", temperature=250)
    PP = Filament(name="PP", temperature=250)
    NYLON = Filament(name="NYLON", temperature=270)
    PC = Filament(name="PC", temperature=230)
    UNKNOWN = Filament(name="UNKNOWN", temperature=250)


class BasicFilamentPanel(QtWidgets.QStackedWidget):
    run_gcode = QtCore.pyqtSignal(str, name="run_gcode")
    call_load_panel = QtCore.pyqtSignal(bool, str, bool, name="call-load-panel")
    request_back = QtCore.pyqtSignal(name="request_back")
    request_change_tab = QtCore.pyqtSignal(int, name="request_change_tab")
    filament_selected = QtCore.pyqtSignal(
        int, str, str, "PyQt_PyObject", name="filament_selected"
    )

    class FilamentStates(enum.Enum):
        UNKNOWN = -1
        LOADED = enum.auto()
        UNLOADED = enum.auto()

        def __repr__(self) -> str:
            return "<%s.%s>" % (self.__class__.__name__, self._name_)

    def __init__(self, printer: Printer, cfg, parent=None) -> None:
        super().__init__(parent)
        self.printer = printer
        self.cfg = cfg
        self.state = "standby"
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.has_load_unload_objects = None
        self.filament_buttons_list = []
        self.mmu_configured = False
        self._setupUi()
        self.filament_state = self.FilamentStates.UNKNOWN

        self.setCurrentIndex(0)

        self.popup = Popup(self)

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None

        self.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.load_page))
        )
        self.load_header_back_button.clicked.connect(self.back_button)
        self.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )

        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )
        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)
        self.printer.save_variables_update.connect(self.on_save_variables_update)

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        """reset to main page every time the panel is shown"""
        self.change_page(0)
        return super().showEvent(a0)

    def on_save_variables_update(self, save_variables: dict):
        """receives save variables from the printer and updates the filament type accordingly

        Args:
            save_variables (dict): dictionary containing the save variables from the printer
        """
        filament_type = FilamentTypes.UNKNOWN
        variables = save_variables.get("variables", {})
        filament_type = variables.get("filament_type", "")
        for i in FilamentTypes:
            if filament_type and i.value.name in filament_type:
                filament_type = i
                break
        self._lbl_mat.setText(filament_type.value.name)

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """slot to handle print stats updates changing back button behavior"""
        if "state" in field:
            self.state = value
            if value in ("printing", "paused"):
                try:
                    self.main_back_button.disconnect()
                    self.filament_page_load_btn.disconnect()
                except TypeError:
                    pass

                self.main_back_button.clicked.connect(
                    lambda: self.request_change_tab.emit(0)
                )
                self.filament_page_load_btn.clicked.connect(
                    lambda: self.load_filament(0, FilamentTypes.UNKNOWN)
                )

            else:
                try:
                    self.main_back_button.disconnect()
                    self.filament_page_load_btn.disconnect()
                except TypeError:
                    pass
                self.main_back_button.clicked.connect(lambda: self.request_back.emit())
                self.filament_page_load_btn.clicked.connect(
                    partial(self.change_page, self.indexOf(self.load_page))
                )

    @QtCore.pyqtSlot(str, str, bool, name="on_filament_sensor_update")
    def on_filament_sensor_update(self, sensor_name: str, parameter: str, value: bool):
        """slot to handle filament sensor updates"""
        if parameter == "filament_detected":
            if not isinstance(value, bool):
                self.filament_state = self.FilamentStates.UNKNOWN
                return
            if sensor_name == self.filament_sensor:
                self.filament_state = (
                    self.FilamentStates.LOADED
                    if value
                    else self.FilamentStates.UNLOADED
                )
                return

    @QtCore.pyqtSlot(dict, name="on_load_filament")
    def on_load_filament(self, status: dict):
        """slot to handle load macro status updates"""
        if "state" in status.keys():
            if not status["state"]:
                self.target_temp = 0
                self.call_load_panel.emit(False, "", False)
                self.change_page(0)
                if self.state == "paused":
                    self.request_change_tab.emit(0)
                return
        self.call_load_panel.emit(
            True, f"Loading Filament\n{status['step'].capitalize()}", False
        )

    @QtCore.pyqtSlot(dict, name="on_unload_filament")
    def on_unload_filament(self, status: dict):
        """slot to handle unload macro status updates"""
        if "state" in status.keys():
            if not status["state"]:
                self.target_temp = 0
                self.call_load_panel.emit(False, "", False)
                self.change_page(0)
                return
        self.call_load_panel.emit(
            True, f"Unloading Filament\n{status['step'].capitalize()}", False
        )

    @QtCore.pyqtSlot(int, int, name="load_filament")
    def load_filament(
        self, toolhead: int = 0, filament: FilamentTypes = FilamentTypes.UNKNOWN
    ) -> None:
        """slot to handle load filament button click"""

        if not self.isVisible():
            return
        if self.filament_state == self.FilamentStates.UNKNOWN:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Unable to detect whether the filament is loaded or unloaded.",
            )
        if self.filament_state == self.FilamentStates.LOADED:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Filament is already loaded.",
            )
            return
        self.run_gcode.emit(
            f"""SAVE_VARIABLE VARIABLE=filament_type VALUE='"{filament.value.name}"'"""
        )
        self.call_load_panel.emit(True, "Loading", True)
        if not self.mmu_configured:
            self.run_gcode.emit("LOAD_FILAMENT")
            return
        self.run_gcode.emit("MMU_LOAD")

    @QtCore.pyqtSlot(str, int, name="unload_filament")
    def unload_filament(self, toolhead: int = 0, temp: int = 220) -> None:
        """slot to handle unload filament button click"""
        if not self.isVisible():
            return
        if self.filament_state == self.FilamentStates.UNKNOWN:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Unable to detect whether the filament is loaded or unloaded.",
            )
        if self.filament_state == self.FilamentStates.UNLOADED:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Filament is already unloaded.",
            )
            return
        self.find_routine_objects()
        self.run_gcode.emit(
            f"""SAVE_VARIABLE VARIABLE=filament_type VALUE='"{FilamentTypes.UNKNOWN.value.name}"'"""
        )

        self.call_load_panel.emit(True, "Unloading", True)
        if not self.mmu_configured:
            self.run_gcode.emit("UNLOAD_FILAMENT")
            return
        self.run_gcode.emit("MMU_EJECT")

    def open_pre_gate_popup(self, filament_type: FilamentTypes):
        callback_action = partial(self.load_filament, 0, filament_type)

        self.filament_selected.emit(
            filament_type.value.temperature,
            filament_type.value.name,
            filament_type.value.name,
            callback_action,
        )

    def on_mmu_state_changed(self, mmu_state):
        if mmu_state is None:
            return

        if not self.mmu_configured:
            for btn, _filament_type in self.filament_buttons_list:
                try:
                    btn.clicked.disconnect()
                except TypeError:
                    pass

                btn.clicked.connect(partial(self.open_pre_gate_popup, _filament_type))
            self.mmu_configured = True

        if mmu_state.filament_pos == FilamentPos.UNLOADED:
            self.filament_state = self.FilamentStates.UNLOADED
            gate_info = mmu_state.current_gate_info
            status = gate_info.status if gate_info is not None else GateStatus.UNKNOWN
            self.filament_page_load_btn.setEnabled(status != GateStatus.EMPTY)
        else:
            self.filament_state = self.FilamentStates.LOADED

    @property
    def filament_state(self):
        return self._filament_state

    @filament_state.setter
    def filament_state(self, update: FilamentStates) -> None:
        self._filament_state = update
        if update is self.FilamentStates.LOADED:
            self.filament_page_unload_btn.setEnabled(True)
            self.filament_page_load_btn.setEnabled(False)
        elif update is self.FilamentStates.UNLOADED:
            self.filament_page_unload_btn.setEnabled(False)
            self.filament_page_load_btn.setEnabled(True)
        else:
            self.filament_page_load_btn.setEnabled(True)
            self.filament_page_unload_btn.setEnabled(True)

    def change_page(self, index: int) -> None:
        self.setCurrentIndex(index)

    def back_button(self) -> None:
        self.request_back.emit()

    def find_routine_objects(self):
        if not self.printer:
            return
        _available_objects = self.printer.available_objects
        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True
        return False

    def _setupInfoBox(self):
        root = BlocksCustomFrame(parent=self.filament_control_page)
        root.setMinimumSize(QtCore.QSize(600, 80))
        root.setMaximumSize(QtCore.QSize(600, 80))
        root.setObjectName("root")

        font = QtGui.QFont()
        font.setPointSize(15)

        hozlay = QtWidgets.QHBoxLayout(root)

        self.filament_page_info_title_6 = QtWidgets.QLabel(self)
        self.filament_page_info_title_6.setMinimumSize(QtCore.QSize(0, 0))
        self.filament_page_info_title_6.setMaximumSize(QtCore.QSize(170, 60))
        self.filament_page_info_title_6.setFont(font)
        self.filament_page_info_title_6.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.filament_page_info_title_6.setObjectName("filament_page_info_title_6")

        font = QtGui.QFont()
        font.setPointSize(13)

        self._lbl_mat = QtWidgets.QLabel(self)
        self._lbl_mat.setMinimumSize(QtCore.QSize(0, 60))
        self._lbl_mat.setMaximumSize(QtCore.QSize(16777215, 60))
        self._lbl_mat.setFont(font)
        self._lbl_mat.setStyleSheet("color:white")
        self._lbl_mat.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._lbl_mat.setObjectName("_lbl_mat")

        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setStyleSheet("color:white")
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")

        self.filament_page_info_title_6.setText("Filament Type: ")
        self._lbl_mat.setText("...")

        hozlay.addWidget(self.filament_page_info_title_6)
        hozlay.addWidget(self.line_2)
        hozlay.addWidget(self._lbl_mat)

        return root

    def _setupUi(self):
        self.setObjectName("self")
        self.resize(710, 411)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 410))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self.filament_control_page = QtWidgets.QWidget()

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filament_control_page.sizePolicy().hasHeightForWidth()
        )

        self.filament_control_page.setSizePolicy(sizePolicy)
        self.filament_control_page.setMinimumSize(QtCore.QSize(710, 400))
        self.filament_control_page.setMaximumSize(QtCore.QSize(720, 420))
        self.filament_control_page.setObjectName("filament_control_page")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.filament_control_page)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        spacerItem1 = QtWidgets.QSpacerItem(
            60,
            0,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        self.verticalLayout.addItem(spacerItem)

        self.filament_page_header_layout = QtWidgets.QHBoxLayout()
        self.filament_page_header_layout.addItem(spacerItem1)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.filament_page_header_title = QtWidgets.QLabel(
            parent=self.filament_control_page
        )
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

        self.filament_page_header_layout.addWidget(
            self.filament_page_header_title,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(20)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        self.main_back_button = IconButton(parent=self.filament_control_page)
        self.main_back_button.setSizePolicy(sizePolicy)
        self.main_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.main_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.main_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.main_back_button.setObjectName("main_back_button")
        self.filament_page_header_layout.addWidget(self.main_back_button)

        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        spacerItem3 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        spacerItem4 = QtWidgets.QSpacerItem(
            20,
            26,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        spacerItem5 = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Maximum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        spacerItem6 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        spacerItem7 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout.addLayout(self.filament_page_header_layout)
        self.verticalLayout.addItem(spacerItem2)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.addItem(spacerItem6)

        self.verticalLayout_3.addWidget(
            self._setupInfoBox(), 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.verticalLayout_3.addItem(spacerItem3)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.filament_page_load_btn = BlocksCustomButton(
            parent=self.filament_control_page
        )
        self.filament_page_load_btn.setSizePolicy(sizePolicy)
        self.filament_page_load_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.filament_page_load_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.filament_page_load_btn.setFont(font)
        self.filament_page_load_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/filament_related/media/btn_icons/load_filament.svg"),
        )
        self.filament_page_load_btn.setObjectName("filament_page_load_btn")
        self.horizontalLayout.addWidget(self.filament_page_load_btn)

        self.filament_page_unload_btn = BlocksCustomButton(
            parent=self.filament_control_page
        )

        self.filament_page_unload_btn.setSizePolicy(sizePolicy)
        self.filament_page_unload_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.filament_page_unload_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.filament_page_unload_btn.setFont(font)
        self.filament_page_unload_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/filament_related/media/btn_icons/unload_filament.svg"),
        )
        self.filament_page_unload_btn.setObjectName("filament_page_unload_btn")

        self.horizontalLayout.addWidget(self.filament_page_unload_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout.addItem(spacerItem4)
        self.verticalLayout.addItem(spacerItem7)
        self.addWidget(self.filament_control_page)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)

        self.load_page = QtWidgets.QWidget()
        self.load_page.setSizePolicy(sizePolicy)
        self.load_page.setMinimumSize(QtCore.QSize(710, 400))
        self.load_page.setMaximumSize(QtCore.QSize(720, 420))
        self.load_page.setSizeIncrement(QtCore.QSize(1, 1))
        self.load_page.setObjectName("load_page")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.load_page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addItem(
            QtWidgets.QSpacerItem(
                20,
                24,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.load_page_header_layout = QtWidgets.QHBoxLayout()
        self.load_page_header_layout.setObjectName("load_page_header_layout")
        self.load_page_header_layout.addItem(spacerItem5)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.load_header_page_title = QtWidgets.QLabel(parent=self.load_page)
        self.load_header_page_title.setMinimumSize(QtCore.QSize(0, 60))
        self.load_header_page_title.setFont(font)
        self.load_header_page_title.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.load_header_page_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.load_header_page_title.setObjectName("load_header_page_title")

        self.load_page_header_layout.addWidget(self.load_header_page_title)

        self.load_header_back_button = IconButton(parent=self.load_page)
        self.load_header_back_button.setSizePolicy(sizePolicy)
        self.load_header_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.load_header_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.load_header_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.load_header_back_button.setObjectName("load_header_back_button")
        self.load_page_header_layout.addWidget(self.load_header_back_button)

        self.verticalLayout_2.addLayout(self.load_page_header_layout)
        spacerItem9 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout_2.addItem(spacerItem9)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.load_page_content_layout = QtWidgets.QGridLayout()
        self.load_page_content_layout.setContentsMargins(5, 5, 5, 5)
        self.load_page_content_layout.setHorizontalSpacing(6)
        self.load_page_content_layout.setObjectName("load_page_content_layout")

        filament_buttons = [
            (
                "load_pla_btn",
                "PLA",
                ":/filament_related/media/topbar/pla_filament_topbar.svg",
                0,
                0,
                FilamentTypes.PLA,
            ),
            (
                "load_petg_btn",
                "PETG",
                ":/filament_related/media/topbar/petg_filament_topbar.svg",
                0,
                1,
                FilamentTypes.PETG,
            ),
            (
                "load_abs_btn",
                "ABS",
                ":/filament_related/media/topbar/abs_filament_topbar.svg",
                1,
                0,
                FilamentTypes.ABS,
            ),
            (
                "load_PP_btn",
                "PP",
                ":/top_bar_icons/media/topbar/pp_filament_topbar.svg",
                1,
                1,
                FilamentTypes.PP,
            ),
            (
                "load_nylon_btn",
                "NYLON",
                ":/top_bar_icons/media/topbar/nylon_filament_topbar.svg",
                2,
                0,
                FilamentTypes.NYLON,
            ),
            (
                "load_PC_btn",
                "PC",
                ":/top_bar_icons/media/topbar/pc_filament_topbar.svg",
                2,
                1,
                FilamentTypes.PC,
            ),
        ]

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        for obj_name, text, pixmap_path, row, col, _filament_type in filament_buttons:
            btn = BlocksCustomButton(parent=self.load_page)
            btn.setMinimumSize(QtCore.QSize(200, 80))
            btn.setMaximumSize(QtCore.QSize(200, 80))
            btn.setFont(font)
            btn.setText(text)
            btn.clicked.connect(partial(self.load_filament, 0, _filament_type))
            btn.clicked.connect(
                partial(self.change_page, self.indexOf(self.filament_control_page))
            )
            btn.setProperty("icon_pixmap", QtGui.QPixmap(pixmap_path))
            btn.setObjectName(obj_name)
            self.load_page_content_layout.addWidget(btn, row, col, 1, 1)
            self.filament_buttons_list.append((btn, _filament_type))

        self.verticalLayout_2.addLayout(self.load_page_content_layout)

        spacerItem20 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout_2.addItem(spacerItem20)
        self.addWidget(self.load_page)

        self.setCurrentIndex(0)

        self.filament_page_header_title.setText("Filament Control")
        self.filament_page_load_btn.setText("Load")
        self.filament_page_unload_btn.setText("Unload")
        self.load_header_page_title.setText("Load Filament")
        self.load_header_back_button.setText("Back")
