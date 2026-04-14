import enum
from functools import partial

import logging
from lib.printer import Printer
from lib.filament import Filament
from lib.ui.filamentStackedWidget_ui import Ui_filamentStackedWidget
from configfile import get_configparser
from lib.panels.widgets.popupDialogWidget import Popup
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)


class FilamentTypes(enum.Enum):
    PLA = Filament(name="PLA", temperature=220)
    PETG = Filament(name="PETG", temperature=240)
    ABS = Filament(name="ABS", temperature=250)
    HIPS = Filament(name="HIPS", temperature=250)
    NYLON = Filament(name="NYLON", temperature=270)
    TPU = Filament(name="TPU", temperature=230)
    UNKNOWN = Filament(name="UNKNOWN", temperature=250)


class FilamentTab(QtWidgets.QStackedWidget):
    request_filament_change_page = QtCore.pyqtSignal(name="filament_change_page")
    request_filament_load = QtCore.pyqtSignal(name="filament_load_t1")
    request_back = QtCore.pyqtSignal(name="request_back")
    request_change_page = QtCore.pyqtSignal(int, int, name="request_change_page")
    request_change_tab = QtCore.pyqtSignal(int, name="request_change_tab")
    request_toolhead_count = QtCore.pyqtSignal(int, name="toolhead_number_received")
    run_gcode = QtCore.pyqtSignal(str, name="run_gcode")
    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")

    class FilamentStates(enum.Enum):
        LOADED = enum.auto()
        UNLOADED = enum.auto()
        UNKNOWN = -1

        def __repr__(self) -> str:
            return "<%s.%s>" % (self.__class__.__name__, self._name_)

    def __init__(self, parent: QtWidgets.QWidget, printer: Printer, ws, /) -> None:
        super().__init__(parent)
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.ws = ws
        self.printer = printer
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        cfg = get_configparser()
        if cfg.has_section("filament_presence"):
            i = cfg.get_section("filament_presence", None)
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
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.run_gcode.connect(self.ws.api.run_gcode)
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)


        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def on_save_variables_update(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["variables"]["filament_type"]:
                self.filament_type = i
                break
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(self.filament_type.value.name)

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """Handle print stats object update"""
        if isinstance(value, str):
            if "state" in field:
                self.state = value
                if value in ("printing", "pausing", "paused", "resuming"):
                    self.panel.main_back_button.show()
                    self.panel.spacerItem1.changeSize(
                        60,
                        0,
                        QtWidgets.QSizePolicy.Policy.Minimum,
                        QtWidgets.QSizePolicy.Policy.Minimum,
                    )
                if value in ("standby"):
                    self.panel.main_back_button.hide()
                    self.panel.spacerItem1.changeSize(
                        0,
                        0,
                        QtWidgets.QSizePolicy.Policy.Minimum,
                        QtWidgets.QSizePolicy.Policy.Minimum,
                    )

    @QtCore.pyqtSlot(str, str, bool, name="on_filament_sensor_update")
    def on_filament_sensor_update(self, sensor_name: str, parameter: str, value: bool):
        """Handle filament sensor object update"""
        if parameter == "filament_detected":
            if not isinstance(value, bool):
                self._filament_state = self.FilamentStates.UNKNOWN
                self.handle_filament_state()
                return
            if sensor_name == self.filament_sensor:
                if value:
                    self._filament_state = self.FilamentStates.LOADED
                else:
                    self._filament_state = self.FilamentStates.UNLOADED
                return
        self.handle_filament_state()


    @QtCore.pyqtSlot(dict, name="on_load_filament")
    def on_load_filament(self, status: dict):
        """Handle load filament object updated"""
        if "state" in status.keys():
            if not status["state"]:
                self.target_temp = 0
                self.call_load_panel.emit(False, "")
                if self.state == "printing":
                    self.request_change_tab.emit(0)
                return
        self.call_load_panel.emit(True, f"Loading Filament\n{status['step'].capitalize()}")
        self.handle_filament_state()

    @QtCore.pyqtSlot(dict, name="on_unload_filament")
    def on_unload_filament(self, status: dict):
        """Handle unload filament object updated"""
        if "state" in status.keys():
            if not status["state"]:
                self.target_temp = 0
                self.call_load_panel.emit(False, "")
                return
        self.call_load_panel.emit(True, f"Unloading Filament\n{status['step'].capitalize()}")
        self.handle_filament_state()

    @QtCore.pyqtSlot(int, int, name="load_filament")
    def load_filament(
        self, toolhead: int = 0, filament: FilamentTypes = FilamentTypes.UNKNOWN
    ) -> None:
        """Handle load filament buttons clicked"""
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
        self.run_gcode.emit(
            f"LOAD_FILAMENT TOOLHEAD=load_toolhead TEMPERATURE={filament.value.temperature}"
        )

    @QtCore.pyqtSlot(str, int, name="unload_filament")
    def unload_filament(self, toolhead: int = 0, temp: int = 220) -> None:
        """Handle unload filament button clicked"""
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
        self.run_gcode.emit(f"UNLOAD_FILAMENT TEMPERATURE={temp}")

    def handle_filament_state(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    @property
    def filament_state(self):
        return self._filament_state

    def change_page(self, index):
        """Issue a page change"""
        self.request_change_page.emit(1, index)

    def back_button(self):
        """Go back a page"""
        self.request_back.emit()

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        """Widget painting"""
        if self.panel.load_page.isVisible() and self.toolhead_count == 1:
            self.panel.load_header_page_title.setText("Load Toolhead")
        if a0 is not None:
            return super().paintEvent(a0)

    def find_routine_objects(self):
        """Check if printer has load/unload printer objects"""
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
