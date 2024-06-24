from collections import deque
import logging
from PyQt6.QtWidgets import QStackedWidget, QWidget
from functools import partial
from PyQt6.QtCore import pyqtSignal, pyqtSlot
import typing

from PyQt6.QtCore import (
    pyqtSlot,
    pyqtSignal,
    Qt,
)
from functools import partial

from scripts.moonrakerComm import MoonWebSocket
from scripts.bo_includes.bo_printer import Printer
from qt_ui.controlStackedWidget_ui import Ui_controlStackedWidget

_logger = logging.getLogger(__name__)

class ControlTab(QStackedWidget):
    request_back_button_pressed = pyqtSignal(name="request_back_button_pressed")
    request_change_page = pyqtSignal(int, int, name="request_change_page")

    request_numpad_signal = pyqtSignal(
        int, str, str, "PyQt_PyObject", QStackedWidget, name="request_numpad"
    )  # enviar o nome da funcao que depois quero receber os dados
    # subscribe_numpad_value_signal = pyqtSignal(str, str, name="subscribe_numpad_value")

    run_gcode_signal = pyqtSignal(str, name="run_gcode")

    def __init__(
        self, parent: typing.Optional[QWidget], ws: MoonWebSocket, printer: Printer
    ) -> None:
        super().__init__(parent)

        self.panel = Ui_controlStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.main_panel = parent
        self.ws = ws
        self.printer = printer

        self.index_stack = deque(maxlen=4)
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        
        # Values to extrude in the extrude menu.
        self.extrude_length = 10
        self.extrude_feedrate = 2

        # Value to move axis
        self.move_length = 10
        self.move_feedrate = 25

        # Signal to update labels
        self.printer.toolhead_update_signal[str, list].connect(self.toolhead_position_change)
        self.printer.toolhead_update_signal[str, str].connect(self.toolhead_extruder_active)
        self.printer.extruder_update_signal.connect(self.extruder_temperature_change)
        self.printer.heater_bed_update_signal.connect(
            self.heater_bed_temperature_change
        )

        # Connecting buttons in the panel routing tree
        # Control Screen
        self.panel.control_motion_btn.clicked.connect(partial(self.change_page, 1))
        self.panel.control_temperature_btn.clicked.connect(partial(self.change_page, 4))
        self.panel.control_printer_settings_btn.clicked.connect(
            partial(self.change_page, 6)
        )
        # Motion Screen
        self.panel.motion_extrude_btn.clicked.connect(partial(self.change_page, 2))
        self.panel.motion_move_axis_btn.clicked.connect(partial(self.change_page, 3))
        self.panel.motion_back_btn.clicked.connect(self.back_button)
        self.panel.motion_auto_home_btn.clicked.connect(partial(self.handle_gcode, ["G28"]))
        self.panel.motion_disable_steppers_btn.clicked.connect(partial(self.handle_gcode, ["M84"]))
        
        # Extrude
        self.panel.extrude_back_btn.clicked.connect(self.back_button)
        self.panel.extrude_select_length_10_btn.clicked.connect(partial(self.select_extrude_length, 10))
        self.panel.extrude_select_length_50_btn.clicked.connect(partial(self.select_extrude_length, 50))
        self.panel.extrude_select_length_100_btn.clicked.connect(partial(self.select_extrude_length, 100))
        self.panel.extrude_select_feedrate_2_btn.clicked.connect(partial(self.select_extrude_feedrate, 2))
        self.panel.extrude_select_feedrate_5_btn.clicked.connect(partial(self.select_extrude_feedrate, 5))
        self.panel.extrude_select_feedrate_10_btn.clicked.connect(partial(self.select_extrude_feedrate, 10))
        self.panel.extrude_extrude_btn.clicked.connect(partial(self.handle_extrusion, True)) #True for extrusion
        self.panel.extrude_retract_btn.clicked.connect(partial(self.handle_extrusion, False)) #False for retraction
        self.panel.extrude_active_tool_switch_btn.clicked.connect(self.switch_extruder)
        
        # Move Axis
        self.panel.move_axis_back_btn.clicked.connect(self.back_button)
        self.panel.move_axis_home_x_btn.clicked.connect(partial(self.handle_gcode, ["G28 X"]))
        self.panel.move_axis_home_y_btn.clicked.connect(partial(self.handle_gcode, ["G28 Y"]))
        self.panel.move_axis_home_z_btn.clicked.connect(partial(self.handle_gcode, ["G28 Z"]))
        self.panel.move_axis_home_all_btn.clicked.connect(partial(self.handle_gcode, ["G28"]))
        self.panel.move_axis_select_length_1_btn.clicked.connect(partial(self.select_move_length, 1))
        self.panel.move_axis_select_length_10_btn.clicked.connect(partial(self.select_move_length, 10))
        self.panel.move_axis_select_length_100_btn.clicked.connect(partial(self.select_move_length, 100))
        self.panel.move_axis_select_feedrate_25_btn.clicked.connect(partial(self.select_move_feedrate, 25))
        self.panel.move_axis_select_feedrate_50_btn.clicked.connect(partial(self.select_move_feedrate, 50))
        self.panel.move_axis_select_feedrate_100_btn.clicked.connect(partial(self.select_move_feedrate, 100))
        self.panel.move_axis_tool_switch_btn.clicked.connect(self.switch_extruder)
        # Move Axis arrow buttons
        self.panel.move_axis_up_btn.clicked.connect(partial(self.handle_move_axis, "Y"))
        self.panel.move_axis_down_btn.clicked.connect(partial(self.handle_move_axis, "Y-"))
        self.panel.move_axis_right_btn.clicked.connect(partial(self.handle_move_axis, "X"))
        self.panel.move_axis_left_btn.clicked.connect(partial(self.handle_move_axis, "X-"))
        self.panel.move_bed_up_btn.clicked.connect(partial(self.handle_move_axis, "Z"))
        self.panel.move_bed_down_btn.clicked.connect(partial(self.handle_move_axis, "Z-"))
        
        
        # Temperature
        self.panel.temperature_back_btn.clicked.connect(self.back_button)

        # Printer Settings Screen
        self.panel.printer_settings_back_btn.clicked.connect(self.back_button)

        self.run_gcode_signal.connect(self.ws.api.run_gcode)
        # @ object temperature change clicked
        
        self.panel.hotend_temp_btn.clicked.connect(
            partial(
                self.request_numpad_signal.emit,
                2,
                "extruder",
                self.panel.temperature_hotend_1_value_label.text(),
                self.handle_numpad_change,
                self,
            )
        )
        self.panel.hotend_1_temp_btn.clicked.connect(
            partial(
                self.request_numpad_signal.emit,
                2,
                "extruder1",
                self.panel.temperature_hotend_2_value_label.text(),
                self.handle_numpad_change,
                self,
            )
        )
        self.panel.chamber_temp_btn.clicked.connect(
            partial(
                self.request_numpad_signal.emit,
                2,
                "chamber",
                self.panel.temperature_chamber_value_label_5.text(),
                self.handle_numpad_change,
                self,
            )
        )
        # self.panel.chamber_1_temp_btn.clicked.connect(
        #     partial(
        #         self.request_numpad_signal.emit,
        #         "chamber1",
        #         self.panel.tempere
        #     )
        # )
        self.panel.fan_power_btn.clicked.connect(
            partial(
                self.request_numpad_signal.emit,
                2,
                "fan",
                self.panel.temperature_fan_1_value_label.text(),
                self.handle_numpad_change,
                self,
            )
        )

        self.panel.fan_1_power_btn.clicked.connect(
            partial(
                self.request_numpad_signal.emit,
                2,
                "fan1",
                self.panel.temperature_fan_2_value_label.text(),
                self.handle_numpad_change,
                self,
            )
        )
        self.show()

    def handle_gcode(self, gcode_list) -> None:
        for gcode in gcode_list:
            print(f"Emiting gcode signal: {gcode}.")
            self.run_gcode_signal.emit(gcode)

    def change_page(self, index):
        self.request_change_page.emit(2, index)
        # self.index_stack.append(self.currentIndex())
        # self.setCurrentIndex(index)

    def back_button(self):
        self.request_back_button_pressed.emit()
        # self.back_button_signal.emit()
        # self.setCurrentIndex(self.index_stack[-1])  #Go to the last position of the stack.
        # self.index_stack.pop()                      #Remove the last position.

    @pyqtSlot(str, int, name="numpad_new_value")
    @pyqtSlot(str, float, name="numpad_new_value")
    def handle_numpad_change(self, name: str, new_value: int | float) -> None:

        if name.startswith("fan") and isinstance(new_value, float):
            if 0.0 <= new_value <= 1.0:
                self.run_gcode_signal.emit(f"SET_FAN_SPEED FAN={name} SPEED={new_value}")

        elif isinstance(new_value, int):
            self.run_gcode_signal.emit(
                f"SET_HEATER_TEMPERATURE HEATER={name} TARGET={new_value}"
            )
            
    def select_extrude_feedrate(self, extrude_feedrate) -> None:
        _logger.debug(f"Setting extrude feedrate to {extrude_feedrate}")
        self.extrude_feedrate = extrude_feedrate
        self.panel.extrude_text_label.setText(f"Extrude length: {self.extrude_length}mm Extrude Feedrate: {self.extrude_feedrate}mm/s")

    def select_extrude_length(self, extrude_length) -> None:
        _logger.debug(f"Setting extrude length to {extrude_length}")
        self.extrude_length = extrude_length
        self.panel.extrude_text_label.setText(f"Extrude length: {self.extrude_length}mm Extrude Feedrate: {self.extrude_feedrate}mm/s")

    def select_move_feedrate(self, move_feedrate) -> None:
        self.move_feedrate = move_feedrate

    def select_move_length(self, move_length) -> None:
        self.move_length = move_length

    def handle_extrusion(self, extrude) -> None:
        
        can_extrude = self.printer.heaters_object["extruder"]["can_extrude"]
        
        if not can_extrude:
            self.panel.extrude_text_label.setText(f"Temperature too cold to extrude")
            return
        
        self.run_gcode_signal.emit("M83")
        if extrude:
            _logger.debug(f"Emiting gcode signal:\nM83\nG1 E{self.extrude_length} F{self.extrude_feedrate * 60}")
            self.run_gcode_signal.emit(f"G1 E{self.extrude_length} F{self.extrude_feedrate * 60}")
            self.panel.extrude_text_label.setText(f"Extruding {self.extrude_length}mm at {self.extrude_feedrate}mm/s")
        else:
            _logger.debug(f"Emiting gcode signal:\nM83\nG1 E-{self.extrude_length} F{self.extrude_feedrate * 60}")
            self.run_gcode_signal.emit(f"G1 E-{self.extrude_length} F{self.extrude_feedrate * 60}")
            self.panel.extrude_text_label.setText(f"Retracting {self.extrude_length}mm at {self.extrude_feedrate}mm/s")
            
    def handle_move_axis(self, axis) -> None:
        _logger.debug(f"Emiting gcode signal:\nG91\nG1 {axis}{self.move_length} F{self.move_feedrate * 60}\nG90")
        self.run_gcode_signal.emit("G91")
        self.run_gcode_signal.emit(f"G1 {axis}{self.move_length} F{self.move_feedrate * 60}")
        self.run_gcode_signal.emit("G90")
        
    def switch_extruder(self) -> None:
        if self.printer.active_extruder_name == "extruder":
            self.handle_gcode(["T1"])
        else:
            self.handle_gcode(["T0"])
        
    @pyqtSlot(str, str, name="toolhead_update")
    def toolhead_extruder_active(self, field: str, extruder: str) -> None:
        
        if field == "extruder":
            _logger.debug(f"active {field} is: {extruder}")
            self.panel.extrude_active_tool_switch_btn.setText(f"{extruder}")
            self.panel.move_axis_tool_switch_btn.setText(f"{extruder}")
            
    @pyqtSlot(str, list, name="toolhead_update")
    def toolhead_position_change(self, field: str, values: list) -> None:
        
        if field == "position":
            _logger.debug(f"Updating toolhead {field} to: {values}")
            self.panel.move_axis_x_value_label.setText(f"{values[0]}")
            self.panel.move_axis_y_value_label.setText(f"{values[1]}")
            self.panel.move_axis_z_value_label.setText(f"{values[2]}")

    @pyqtSlot(str, str, float, name="extruder_update")
    def extruder_temperature_change(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        if extruder_name == "extruder" and field == "temperature":
            self.panel.temperature_hotend_1_value_label.setText(f"{new_value:.1f}")
        
        if extruder_name == "extruder1" and field == "temperature":
            self.panel.temperature_hotend_2_value_label.setText(f"{new_value:.1f}")


    @pyqtSlot(str, str, float, name="heater_bed_update")
    def heater_bed_temperature_change(
        self, name: str, field: str, new_value: float
    ) -> None:
        if field == "temperature":
            self.panel.temperature_bed_value_label.setText(f"{new_value:.1f}")