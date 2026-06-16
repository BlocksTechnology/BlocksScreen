import enum
import logging
from functools import partial

from PyQt6 import QtCore, QtWidgets, QtGui

from lib.filament import Filament
from lib.panels.widgets.popupDialogWidget import Popup
from lib.printer import Printer
from lib.ui.filamentStackedWidget_ui import Ui_filamentStackedWidget


logger = logging.getLogger(__name__)


class FilamentTypes(enum.Enum):
    PLA = Filament(name="PLA", temperature=220)
    PETG = Filament(name="PETG", temperature=240)
    ABS = Filament(name="ABS", temperature=250)
    HIPS = Filament(name="HIPS", temperature=250)
    NYLON = Filament(name="NYLON", temperature=270)
    TPU = Filament(name="TPU", temperature=230)
    UNKNOWN = Filament(name="UNKNOWN", temperature=250)


class BasicFilamentPanel(QtWidgets.QStackedWidget):
    run_gcode = QtCore.pyqtSignal(str, name="run_gcode")
    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")
    request_back = QtCore.pyqtSignal(name="request_back")
    request_change_tab = QtCore.pyqtSignal(int, name="request_change_tab")

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
        self._filament_state = self.FilamentStates.UNKNOWN
        self._setup_ui()
        self.set_filament_state()

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        """reset to main page every time the panel is shown"""
        self.change_page(0)
        return super().showEvent(a0)

    def _setup_ui(self) -> None:
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)

        self.popup = Popup(self)

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None

        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
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

    def on_save_variables_update(self, save_variables: dict):
        """receives save variables from the printer and updates the filament type accordingly

        Args:
            save_variables (dict): dictionary containing the save variables from the printer
        """
        filament_type = FilamentTypes.UNKNOWN
        for i in FilamentTypes:
            if i.value.name in save_variables["variables"]["filament_type"]:
                filament_type = i
                break
        self.panel.label_2.setText(filament_type.value.name)

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """slot to handle print stats updates changing back button behavior"""
        if "state" in field:
            self.state = value
            if value in ("printing", "paused"):
                try:
                    self.panel.main_back_button.disconnect()
                except TypeError:
                    pass

                self.panel.main_back_button.clicked.connect(
                    lambda: self.request_change_tab.emit(0)
                )

            else:
                try:
                    self.panel.main_back_button.disconnect()
                except TypeError:
                    pass
                self.panel.main_back_button.clicked.connect(
                    lambda: self.request_back.emit()
                )

    @QtCore.pyqtSlot(str, str, bool, name="on_filament_sensor_update")
    def on_filament_sensor_update(self, sensor_name: str, parameter: str, value: bool):
        """slot to handle filament sensor updates"""
        if parameter == "filament_detected":
            if not isinstance(value, bool):
                self.set_filament_state()
                self.handle_filament_state()
                return
            if sensor_name == self.filament_sensor:
                if value:
                    self.set_filament_state(True)
                else:
                    self.set_filament_state(False)

                return

    @QtCore.pyqtSlot(dict, name="on_load_filament")
    def on_load_filament(self, status: dict):
        """slot to handle load macro status updates"""
        if "state" in status.keys():
            if not status["state"]:
                self.target_temp = 0
                self.call_load_panel.emit(False, "")
                if self.state == "paused":
                    self.request_change_tab.emit(0)
                return
        self.call_load_panel.emit(
            True, f"Loading Filament\n{status['step'].capitalize()}"
        )

    @QtCore.pyqtSlot(dict, name="on_unload_filament")
    def on_unload_filament(self, status: dict):
        """slot to handle unload macro status updates"""
        if "state" in status.keys():
            if not status["state"]:
                self.target_temp = 0
                self.call_load_panel.emit(False, "")
                return
        self.call_load_panel.emit(
            True, f"Unloading Filament\n{status['step'].capitalize()}"
        )

    @QtCore.pyqtSlot(int, int, name="load_filament")
    def load_filament(
        self, toolhead: int = 0, filament: FilamentTypes = FilamentTypes.UNKNOWN
    ) -> None:
        """slot to handle load filament button click"""

        if not self.isVisible:
            return
        if self._filament_state == self.FilamentStates.UNKNOWN:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Unable to detect whether the filament is loaded or unloaded.",
            )
        if self._filament_state == self.FilamentStates.LOADED:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Filament is already loaded.",
            )
            return
        self.call_load_panel.emit(True, "Loading Filament")
        self.run_gcode.emit(
            f"""SAVE_VARIABLE VARIABLE=filament_type VALUE='"{filament.value.name}"'"""
        )
        self.run_gcode.emit("MMU_LOAD")

    @QtCore.pyqtSlot(str, int, name="unload_filament")
    def unload_filament(self, toolhead: int = 0, temp: int = 220) -> None:
        """slot to handle unload filament button click"""
        if not self.isVisible:
            return
        if self._filament_state == self.FilamentStates.UNKNOWN:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Unable to detect whether the filament is loaded or unloaded.",
            )
        if self._filament_state == self.FilamentStates.UNLOADED:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Filament is already unloaded.",
            )
            return
        self.find_routine_objects()
        self.call_load_panel.emit(True, "Unloading Filament")
        self.run_gcode.emit(
            f"""SAVE_VARIABLE VARIABLE=filament_type VALUE='"{FilamentTypes.UNKNOWN.value.name}"'"""
        )
        self.run_gcode.emit("MMU_UNLOAD")

    def on_mmu_state_changed(self, mmu_state):
        if mmu_state is None:
            return
        self.status = mmu_state.filament
        self.set_filament_state(True if self.status == "Loaded" else False)

    def set_filament_state(self, update: bool | None = None) -> None:
        """sets filament states and updates load/unload button accordingly if None then both buttons are enabled

        Args:
            update (bool | None): filament state to set, True for loaded, False for unloaded, None for unknown
        """
        if update is True:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
            self._filament_state = self.FilamentStates.LOADED
        elif update is False:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
            self._filament_state = self.FilamentStates.UNLOADED
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)
            self._filament_state = self.FilamentStates.UNKNOWN

    @property
    def filament_state(self):
        return self._filament_state

    def change_page(self, index: int) -> None:
        self.setCurrentIndex(index)

    def back_button(self) -> None:
        self.request_back.emit()

    def find_routine_objects(self):
        if not self.printer:
            return
        _available_objects = self.printer.available_objects.copy()
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
