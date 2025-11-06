import enum
from functools import partial


from lib.printer import Printer
from lib.filament import Filament
from lib.ui.filamentStackedWidget_ui import Ui_filamentStackedWidget

from lib.panels.widgets.loadPage import LoadScreen
from lib.panels.widgets.popupDialogWidget import Popup
from PyQt6 import QtCore, QtGui, QtWidgets


class FilamentTab(QtWidgets.QStackedWidget):
    request_filament_change_page = QtCore.pyqtSignal(name="filament_change_page")
    request_filament_load = QtCore.pyqtSignal(name="filament_load_t1")
    request_back = QtCore.pyqtSignal(name="request_back")
    request_change_page = QtCore.pyqtSignal(int, int, name="request_change_page")
    request_toolhead_count = QtCore.pyqtSignal(int, name="toolhead_number_received")
    run_gcode = QtCore.pyqtSignal(str, name="run_gcode")

    class FilamentTypes(enum.Enum):
        PLA = Filament(name="PLA", temperature=220)

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


        self.loadscreen = LoadScreen(self, LoadScreen.AnimationGIF.DEFAULT)
        self.addWidget(self.loadscreen)


        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self._sensor_states = {} 
        self.filament_type: Filament | None = None

        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(
            self.back_button
        )
        # REFACTOR self.panel.load_custom_btn.clicked.connect(partial(self.change_page, 2))
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)

        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=220)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=240)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=250)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=250)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=270)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=230)
        )

        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.run_gcode.connect(self.ws.api.run_gcode)

        self.printer.extruder_update.connect(self.on_extruder_update)

        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(self.on_filament_sensor_update)

    #IF nothings shows is bc of the connection between printer.py and this ,MAYbe the load and unload file itself with printer idk should work tho

    @QtCore.pyqtSlot(str, str, bool, name="on_filament_sensor_update")
    def on_filament_sensor_update(self, sensor_name: str, parameter: str, value: bool): 
        if parameter == "filament_detected":
            if not isinstance(value, bool):
                self._filament_state = self.FilamentStates.UNKNOWN
                self.handle_filamment_state()
                return
            self._sensor_states[sensor_name] = value
            if not self._sensor_states:
                new_state = self.FilamentStates.UNKNOWN
            elif all(self._sensor_states.values()):
                new_state = self.FilamentStates.LOADED
            else:
                new_state = self.FilamentStates.UNLOADED
            
            if self._filament_state != new_state:
                self._filament_state = new_state
                self.handle_filamment_state()


    @QtCore.pyqtSlot(str, str, float, name="on_extruder_update")
    def on_extruder_update(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        if not self.isVisible:
            return

        if self.target_temp != 0:
            if self.current_temp == self.target_temp:
                self.loadscreen.set_status_message("Extruder heated up \n please wait")
                return

            if field == "temperature":
                self.current_temp = round(new_value,0) #somehow this works 
                self.loadscreen.set_status_message(f"Heating up ({new_value}/{self.target_temp}) \n Please wait")
            


        if field == "target":
            self.target_temp = round(new_value,0) #somehow this works again
            self.loadscreen.set_status_message("Heating up \n Please wait")


    @QtCore.pyqtSlot(bool, name="on_load_filament")
    def on_load_filament(self,status:bool):
        if not self.isVisible:
            return


        if status:
            self.loadscreen.show()
        else:
            self.current_temp = 0
            self.loadscreen.hide()
            self._filament_state = self.FilamentStates.LOADED
        self.handle_filamment_state()

    @QtCore.pyqtSlot(bool, name="on_unload_filament")
    def on_unload_filament(self,status:bool):
        if not self.isVisible:
            return

        if status:
            self.loadscreen.show()
        else:
            self.loadscreen.hide()
            self.current_temp = 0
            self._filament_state = self.FilamentStates.UNLOADED
        self.handle_filamment_state()

        

    @QtCore.pyqtSlot(int, int, name="load_filament")
    def load_filament(self, toolhead: int = 0, temp: int = 220) -> None:
        if not self.isVisible:
            return

        if self._filament_state == self.FilamentStates.UNKNOWN:
            self.popup.new_message(message_type=Popup.MessageType.ERROR , message="Unable to detect whether the filament is loaded or unloaded.",)
        
        if self._filament_state == self.FilamentStates.LOADED:
            self.popup.new_message(message_type=Popup.MessageType.ERROR , message="Filament is already loaded.",)
            return  
        
        self.run_gcode.emit(
            f"LOAD_FILAMENT TOOLHEAD=load_toolhead TEMPERATURE={temp}"
        )

    @QtCore.pyqtSlot(str, int, name="unload_filament")
    def unload_filament(self, toolhead: int = 0, temp: int = 220) -> None:
        if not self.isVisible:
            return
            
        if self._filament_state == self.FilamentStates.UNKNOWN:
            self.popup.new_message(message_type=Popup.MessageType.ERROR , message="Unable to detect whether the filament is loaded or unloaded.",)

        if self._filament_state == self.FilamentStates.UNLOADED:
            self.popup.new_message(message_type=Popup.MessageType.ERROR , message="Filament is already unloaded.",)
            return  
        
        self.find_routine_objects()
        self.run_gcode.emit(f"UNLOAD_FILAMENT TEMPERATURE={temp}")
            
    def handle_filamment_state(self):
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_load_btn.setDisabled(True)
            self.panel.filament_page_load_btn.setDisabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setDisabled(True)
            self.panel.filament_page_unload_btn.setDisabled(False)
        else:
            self.panel.filament_page_load_btn.setDisabled(False)
            self.panel.filament_page_unload_btn.setDisabled(False)



    @property
    def filament_state(self):
        return self._filament_state

    def change_page(self, index):
        self.request_change_page.emit(1, index)

    def back_button(self):
        self.request_back.emit()

    def sizeHint(self) -> QtCore.QSize:
        return super().sizeHint()

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        if self.panel.load_page.isVisible() and self.toolhead_count == 1:
            self.panel.load_header_page_title.setText("Load Toolhead")
        if a0 is not None:
            return super().paintEvent(a0)

    def removeWidget(self, w: QtWidgets.QWidget | None) -> None:
        if w is not None:
            return super().removeWidget(w)

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        if a0 is not None:
            return super().resizeEvent(a0)

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
