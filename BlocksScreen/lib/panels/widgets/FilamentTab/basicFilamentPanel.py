import enum
import logging
from functools import partial

from devices.amu.models import FilamentPos, GateStatus
from lib.filament import Filament
from lib.panels.widgets.Common.basePopup import BasePopup
from lib.panels.widgets.Common.popupDialogWidget import Popup
from lib.printer import Printer
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_field import BlocksField
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
            return f"<{self.__class__.__name__}.{self._name_}>"

    def __init__(
        self,
        printer: Printer,
        cfg,
        parent=None,
        *,
        amu_manager,
        load_popup: BasePopup | None = None,
    ) -> None:
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
        self.load_popup = load_popup
        self.amu_manager = amu_manager
        self._mmu_state = None
        self._setup_ui()
        self.filament_state = self.FilamentStates.UNKNOWN

        self.setCurrentIndex(0)

        self.confirm_pos_popup = BasePopup(self, False, True)
        self.confirm_pos_popup.set_message(
            "Change the filament position?\n\n"
            "This overrides the printer's filament state.\n"
            "Only confirm if it matches where the filament\n"
            "actually is in the printer."
        )
        self._pos_pending = ""
        self.confirm_pos_popup.accepted.connect(
            lambda: self._accept_pos_change(self._pos_pending)
        )
        self.confirm_pos_popup.rejected.connect(self._reject_pos_change)

        self.popup = Popup(self)

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None

        self.Basic_fp_load_btn.clicked.connect(self._on_load_clicked)
        self.Basic_fp_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.fcp_back_button.clicked.connect(self.back_button)

        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )
        self.Basic_fp_check_btn.clicked.connect(
            lambda: self.run_gcode.emit("MMU_CHECK_GATE")
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
        self._lbl_mat.set_right_text(filament_type.value.name)

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """slot to handle print stats updates changing back button behavior"""
        if "state" in field:
            self.state = value
            self._refresh_check_btn()
            self._refresh_pos_editable()
            if value in ("printing", "paused"):
                try:
                    self.main_back_button.disconnect()
                except TypeError:
                    pass

                self.main_back_button.clicked.connect(
                    lambda: self.request_change_tab.emit(0)
                )

            else:
                try:
                    self.main_back_button.disconnect()
                except TypeError:
                    pass
                self.main_back_button.clicked.connect(lambda: self.request_back.emit())

    @QtCore.pyqtSlot(str, str, bool, name="on_filament_sensor_update")
    def on_filament_sensor_update(self, sensor_name: str, parameter: str, value: bool):
        """slot to handle filament sensor updates"""
        if self.mmu_configured:
            return
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
        if "state" in status and not status["state"]:
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
        if "state" in status and not status["state"]:
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
        if not self._in_print:
            self.run_gcode.emit(
                f"""SAVE_VARIABLE VARIABLE=filament_type VALUE='"{filament.value.name}"'"""
            )
        if not self.mmu_configured:
            self.call_load_panel.emit(True, "Loading", True)
            self.run_gcode.emit("LOAD_FILAMENT")
            return
        if self.amu_manager.load_gate() and self.load_popup is not None:
            self.load_popup.show()

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
        if not self._in_print:
            self.run_gcode.emit(
                f"""SAVE_VARIABLE VARIABLE=filament_type VALUE='"{FilamentTypes.UNKNOWN.value.name}"'"""
            )

        if not self.mmu_configured:
            self.call_load_panel.emit(True, "Unloading", True)
            self.run_gcode.emit("UNLOAD_FILAMENT")
            return
        if self.amu_manager.unload() and self.load_popup is not None:
            self.load_popup.show()

    def _on_load_clicked(self) -> None:
        if self._in_print:
            self.load_filament(0, FilamentTypes.UNKNOWN)
            return
        self.change_page(self.indexOf(self.fcp))

    def open_pre_gate_popup(self, filament_type: FilamentTypes):
        """Emit filament_selected so the pre-gate popup can confirm the gate before loading."""
        callback_action = partial(self.load_filament, 0, filament_type)

        self.filament_selected.emit(
            filament_type.value.temperature,
            filament_type.value.name,
            filament_type.value.name,
            callback_action,
        )

    def on_mmu_state_changed(self, mmu_state):
        """Wire load buttons to the pre-gate flow on first MMU state, and track filament state."""
        if mmu_state is None:
            return

        if not self.mmu_configured:
            for btn, _filament_type in self.filament_buttons_list:
                try:
                    btn.clicked.disconnect()
                except TypeError:
                    pass

                btn.clicked.connect(partial(self.open_pre_gate_popup, _filament_type))
            self.Basic_fp_check_btn.show()
            self._lbl_clr.show()
            self.mmu_configured = True
            self.Vlayout.setSpacing(10)

        self._mmu_state = mmu_state
        if mmu_state.filament_pos == FilamentPos.LOADED:
            self.filament_state = self.FilamentStates.LOADED
        elif mmu_state.filament_pos == FilamentPos.UNLOADED:
            self.filament_state = self.FilamentStates.UNLOADED
        else:
            self.filament_state = self.FilamentStates.UNKNOWN
        self._refresh_pos_editable()
        gate_info = mmu_state.current_gate_info
        self._apply_color_swatch(gate_info.color if gate_info else "")

    def _apply_color_swatch(self, color_str: str) -> None:
        text = (color_str or "").strip()
        hex_text = text.lstrip("#")
        if len(hex_text) == 8:
            hex_text = hex_text[:6]
        color = QtGui.QColor(f"#{hex_text}")
        if not color.isValid() and text:
            color = QtGui.QColor(text)
        if color.isValid():
            self._lbl_clr.set_right_text("")
            self._lbl_clr.set_right_stylesheet(
                "min-width: 146px; min-height: 46px;"
                "border-radius: 8px;"
                f"background: rgb({color.red()},{color.green()},{color.blue()});"
                "border: 2px solid rgba(255,255,255,80);"
            )
        else:
            self._lbl_clr.set_right_text("✕")
            self._lbl_clr.set_right_stylesheet(
                "min-width: 146px; min-height: 46px;"
                "border-radius: 8px;"
                "background: rgb(40,40,40);"
                "border: 2px dashed rgba(255,255,255,80);"
                "color: #e8445a;"
                "font-size: 28px; font-weight: bold;"
            )

    @property
    def _gate_has_filament(self) -> bool:
        _gate = self._mmu_state.current_gate_info if self._mmu_state else None
        return _gate is None or _gate.status != GateStatus.EMPTY

    @property
    def _mmu_busy(self) -> bool:
        return self._mmu_state is not None and self._mmu_state.action not in (
            "",
            "Idle",
        )

    @property
    def _in_print(self) -> bool:
        return self.state in ("printing", "paused")

    @property
    def filament_state(self):
        return self._filament_state

    @filament_state.setter
    def filament_state(self, update: FilamentStates) -> None:
        self._filament_state = update
        self.Basic_fp_load_btn.setEnabled(update is not self.FilamentStates.LOADED)
        self.Basic_fp_unload_btn.setEnabled(update is not self.FilamentStates.UNLOADED)
        if self._lbl_pos.select_option(update.name.capitalize()):
            self._pos_committed = self._lbl_pos.text()

    def change_page(self, index: int) -> None:
        """Switch this stacked widget to the page at *index*."""
        self.setCurrentIndex(index)

    def back_button(self) -> None:
        """Emit request_back to signal the parent tab to navigate away."""
        self.request_back.emit()

    def find_routine_objects(self):
        """Return whether load/unload gcode macros are available on the printer."""
        if not self.printer:
            return
        _available_objects = self.printer.available_objects
        if "load_filament" in _available_objects:
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects:
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects:
            return True
        return "gcode_macro UNLOAD_FILAMENT" in _available_objects

    def on_pos_change(self) -> None:
        """Ask to confirm a user-picked position, reverting it if declined."""
        new_pos = self._lbl_pos.text()
        if new_pos == self._pos_committed:
            return
        self._pos_pending = new_pos
        self.confirm_pos_popup.open()

    def _accept_pos_change(self, new_pos: str) -> None:
        self._pos_committed = new_pos
        self.amu_manager.recover_single_gate(new_pos == "Loaded")

    def _reject_pos_change(self) -> None:
        self._lbl_pos.select_option(self._pos_committed)

    def _refresh_check_btn(self) -> None:
        self.Basic_fp_check_btn.setEnabled(not self._in_print)

    def _refresh_pos_editable(self) -> None:
        self._lbl_pos.set_editable(
            self.mmu_configured and self.state != "printing" and not self._mmu_busy
        )

    def _setupInfoBox(self):
        root = BlocksCustomFrame(parent=self.filament_control_page)
        root.setMinimumSize(QtCore.QSize(350, 300))
        root.setObjectName("root")

        font = QtGui.QFont()
        font.setPointSize(15)

        hozlay = QtWidgets.QVBoxLayout(root)

        self._lbl_mat = BlocksField(self, "Material:", "bottom")

        self._lbl_pos = BlocksField(self, "Position:", None, "DropDownMenu")
        self._lbl_pos.set_placeholder("Unknown")
        self._lbl_pos.set_options(["Loaded", "Unloaded"])
        self._lbl_pos.select_option("Unknown")
        self._pos_committed = self._lbl_pos.text()
        self._lbl_pos.on_edit.connect(self.on_pos_change)
        self._lbl_pos.set_editable(False)

        self._lbl_clr = BlocksField(self, "Color:", "upper")
        self._apply_color_swatch("")
        self._lbl_clr.hide()

        hozlay.addWidget(self._lbl_mat)
        hozlay.addWidget(self._lbl_pos)
        hozlay.addWidget(self._lbl_clr)
        return root

    def _setup_ui(self) -> None:
        """Build the basic filament panel: load/unload controls and status labels."""
        self.setObjectName("basic_filament_panel")

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
        self.filament_control_page.setFixedSize(QtCore.QSize(710, 400))
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

        self.Basic_fp_header_layout = QtWidgets.QHBoxLayout()
        self.Basic_fp_header_layout.addItem(spacerItem1)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.Basic_fp_header_title = QtWidgets.QLabel(parent=self.filament_control_page)
        self.Basic_fp_header_title.setSizePolicy(sizePolicy)
        self.Basic_fp_header_title.setMinimumSize(QtCore.QSize(0, 60))
        self.Basic_fp_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.Basic_fp_header_title.setFont(font)
        self.Basic_fp_header_title.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.Basic_fp_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.Basic_fp_header_layout.addWidget(
            self.Basic_fp_header_title,
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
        self.Basic_fp_header_layout.addWidget(self.main_back_button)

        self.verticalLayout.addLayout(self.Basic_fp_header_layout)

        self.HLayout = QtWidgets.QHBoxLayout()
        self.HLayout.setObjectName("HLayout")

        self.HLayout.addWidget(
            self._setupInfoBox(), 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

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

        self.buttons_frame = BlocksCustomFrame(parent=self.filament_control_page)
        self.buttons_frame.setFixedSize(QtCore.QSize(290, 300))
        self.buttons_frame.setObjectName("buttons_frame")

        self.Vlayout = QtWidgets.QVBoxLayout(self.buttons_frame)
        self.Vlayout.setObjectName("Vlayout")
        self.Vlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.Basic_fp_load_btn = BlocksCustomButton(parent=self.filament_control_page)
        self.Basic_fp_load_btn.setSizePolicy(sizePolicy)
        self.Basic_fp_load_btn.setFixedSize(QtCore.QSize(250, 80))
        self.Basic_fp_load_btn.setFont(font)
        self.Basic_fp_load_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/filament_related/media/btn_icons/load_filament.svg"),
        )
        self.Basic_fp_load_btn.setObjectName("Basic_fp_load_btn")
        self.Vlayout.addWidget(self.Basic_fp_load_btn)

        self.Basic_fp_unload_btn = BlocksCustomButton(parent=self.filament_control_page)
        self.Basic_fp_unload_btn.setSizePolicy(sizePolicy)
        self.Basic_fp_unload_btn.setFixedSize(QtCore.QSize(250, 80))
        self.Basic_fp_unload_btn.setFont(font)
        self.Basic_fp_unload_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/filament_related/media/btn_icons/unload_filament.svg"),
        )
        self.Basic_fp_unload_btn.setObjectName("Basic_fp_unload_btn")
        self.Vlayout.addWidget(self.Basic_fp_unload_btn)

        self.Basic_fp_check_btn = BlocksCustomButton(parent=self.filament_control_page)
        self.Basic_fp_check_btn.setSizePolicy(sizePolicy)
        self.Basic_fp_check_btn.setFixedSize(QtCore.QSize(250, 80))
        self.Basic_fp_check_btn.setFont(font)
        self.Basic_fp_check_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/filament_related/media/btn_icons/check gate 1.svg"),
        )
        self.Basic_fp_check_btn.setObjectName("Basic_fp_check_btn")
        self.Vlayout.addWidget(self.Basic_fp_check_btn)
        self.Basic_fp_check_btn.hide()
        self.Vlayout.setSpacing(40)

        self.HLayout.addWidget(
            self.buttons_frame, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.verticalLayout.addLayout(self.HLayout)

        self.addWidget(self.filament_control_page)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)

        # fcp = filament choose Page
        self.fcp = QtWidgets.QWidget()
        self.fcp.setSizePolicy(sizePolicy)
        self.fcp.setMinimumSize(QtCore.QSize(710, 400))
        self.fcp.setMaximumSize(QtCore.QSize(720, 420))
        self.fcp.setSizeIncrement(QtCore.QSize(1, 1))
        self.fcp.setObjectName("fcp")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fcp)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addItem(
            QtWidgets.QSpacerItem(
                20,
                24,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.fcp_header_layout = QtWidgets.QHBoxLayout()
        self.fcp_header_layout.setObjectName("fcp_header_layout")

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.fcp_header_title = QtWidgets.QLabel(parent=self.fcp)
        self.fcp_header_title.setMinimumSize(QtCore.QSize(0, 60))
        self.fcp_header_title.setFont(font)
        self.fcp_header_title.setStyleSheet("background: transparent; color: white;")
        self.fcp_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fcp_header_title.setObjectName("fcp_header_title")

        self.fcp_header_layout.addWidget(self.fcp_header_title)

        self.fcp_back_button = IconButton(parent=self.fcp)
        self.fcp_back_button.setSizePolicy(sizePolicy)
        self.fcp_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.fcp_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.fcp_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.fcp_back_button.setObjectName("fcp_back_button")
        self.fcp_header_layout.addWidget(self.fcp_back_button)

        self.verticalLayout_2.addLayout(self.fcp_header_layout)
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

        self.fcp_content_layout = QtWidgets.QGridLayout()
        self.fcp_content_layout.setContentsMargins(5, 5, 5, 5)
        self.fcp_content_layout.setHorizontalSpacing(6)
        self.fcp_content_layout.setObjectName("fcp_content_layout")

        filament_buttons = [
            (
                "load_pla_btn",
                "PLA",
                ":/top_bar_icons/media/topbar/pla_filament_topbar.svg",
                0,
                0,
                FilamentTypes.PLA,
            ),
            (
                "load_petg_btn",
                "PETG",
                ":/top_bar_icons/media/topbar/petg_filament_topbar.svg",
                0,
                1,
                FilamentTypes.PETG,
            ),
            (
                "load_abs_btn",
                "ABS",
                ":/top_bar_icons/media/topbar/abs_filament_topbar.svg",
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
            btn = BlocksCustomButton(parent=self.fcp)
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
            self.fcp_content_layout.addWidget(btn, row, col, 1, 1)
            self.filament_buttons_list.append((btn, _filament_type))

        self.verticalLayout_2.addLayout(self.fcp_content_layout)

        spacerItem20 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout_2.addItem(spacerItem20)
        self.addWidget(self.fcp)

        self.setCurrentIndex(0)

        self.Basic_fp_header_title.setText("Filament Control")
        self.Basic_fp_load_btn.setText("Load")
        self.Basic_fp_unload_btn.setText("Unload")
        self.Basic_fp_check_btn.setText("Check gate")
        self.fcp_header_title.setText("Load Filament")
        self.fcp_back_button.setText("Back")
