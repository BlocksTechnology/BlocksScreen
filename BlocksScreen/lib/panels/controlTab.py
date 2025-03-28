import logging
import typing
from functools import partial

from PyQt6.QtGui import QPaintEvent

from lib.bo.printer import Printer
from lib.moonrakerComm import MoonWebSocket
from lib.ui.controlStackedWidget_ui import Ui_controlStackedWidget
from PyQt6 import QtWidgets
from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
)


class ControlTab(QtWidgets.QStackedWidget):
    request_back_button_pressed = pyqtSignal(name="request_back_button_pressed")
    request_change_page = pyqtSignal(int, int, name="request_change_page")

    request_numpad_signal = pyqtSignal(
        int, str, str, "PyQt_PyObject", QtWidgets.QStackedWidget, name="request_numpad"
    )

    run_gcode_signal = pyqtSignal(str, name="run_gcode")

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget],
        ws: MoonWebSocket,
        printer: Printer,
    ) -> None:
        if parent is not None:
            super().__init__(parent)
        else:
            super().__init__()
        self.panel = Ui_controlStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.main_panel = parent
        self.ws = ws
        self.printer = printer

        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # Values to extrude in the extrude menu.
        self.extrude_length: int = 10
        self.extrude_feedrate: int = 2

        # Value to move axis
        self.move_length: float = 10.0
        self.move_feedrate: float = 25.0

        # Signal to update labels
        self.printer.toolhead_update_signal[str, list].connect(
            self.toolhead_position_change
        )
        self.printer.extruder_update_signal.connect(self.extruder_temperature_change)
        self.printer.heater_bed_update_signal.connect(
            self.heater_bed_temperature_change
        )

        # Connecting buttons in the panel routing tree
        # Control Screen
        self.panel.cp_motion_btn.clicked.connect(partial(self.change_page, 1))
        self.panel.cp_temperature_btn.clicked.connect(partial(self.change_page, 4))
        self.panel.cp_printer_settings_btn.clicked.connect(partial(self.change_page, 6))
        # Motion Screen
        self.panel.motion_extrude_btn.clicked.connect(partial(self.change_page, 2))
        self.panel.motion_move_axis_btn.clicked.connect(partial(self.change_page, 3))
        self.panel.mp_back_btn.clicked.connect(self.back_button)
        self.panel.motion_auto_home_btn.clicked.connect(
            partial(self.handle_gcode, ["G28"])
        )
        self.panel.motion_disable_steppers_btn.clicked.connect(
            partial(self.handle_gcode, ["M84"])
        )

        # Extrude
        self.panel.extrude_back_btn.clicked.connect(self.back_button)

        self.panel.extrude_select_length_10_btn.toggled.connect(
            partial(
                self.handle_toggle_extrude_length,
                caller=self.panel.extrude_select_length_10_btn,
                value=10,
            )
        )
        self.panel.extrude_select_length_50_btn.toggled.connect(
            partial(
                self.handle_toggle_extrude_length,
                caller=self.panel.extrude_select_length_50_btn,
                value=50,
            )
        )
        self.panel.extrude_select_length_100_btn.toggled.connect(
            partial(
                self.handle_toggle_extrude_length,
                caller=self.panel.extrude_select_length_100_btn,
                value=100,
            )
        )
        self.panel.extrude_select_feedrate_2_btn.toggled.connect(
            partial(
                self.handle_toggle_extrude_feedrate,
                caller=self.panel.extrude_select_feedrate_2_btn,
                value=2,
            )
        )
        self.panel.extrude_select_feedrate_5_btn.toggled.connect(
            partial(
                self.handle_toggle_extrude_feedrate,
                caller=self.panel.extrude_select_feedrate_5_btn,
                value=5,
            )
        )
        self.panel.extrude_select_feedrate_10_btn.toggled.connect(
            partial(
                self.handle_toggle_extrude_feedrate,
                caller=self.panel.extrude_select_feedrate_10_btn,
                value=10,
            )
        )
        self.panel.move_axis_select_length_1_btn.toggled.connect(
            partial(self.handle_select_move_length, value=1.0)
        )
        self.panel.move_axis_select_length_10_btn.toggled.connect(
            partial(self.handle_select_move_length, value = 10.)
        )
        self.panel.move_axis_select_length_100_btn.toggled.connect(
            partial(self.handle_select_move_length, 100)
        )
        self.panel.move_axis_select_feedrate_25_btn.toggled.connect(
            partial(self.handle_select_move_feedrate, 25)
        )
        self.panel.move_axis_select_feedrate_50_btn.toggled.connect(
            partial(self.handle_select_move_feedrate, 50)
        )
        self.panel.move_axis_select_feedrate_100_btn.toggled.connect(
            partial(self.handle_select_move_feedrate, 100)
        )
        self.panel.extrude_extrude_btn.clicked.connect(
            partial(self.handle_extrusion, True)
        )  # True for extrusion
        self.panel.extrude_retract_btn.clicked.connect(
            partial(self.handle_extrusion, False)
        )  # False for retraction

        # Move Axis
        self.panel.mva_back_btn.clicked.connect(self.back_button)
        # REVIEW: Aggregate these .connect(...)
        self.panel.move_axis_home_x_btn.clicked.connect(
            partial(self.handle_gcode, ["G28 X"])
        )
        self.panel.move_axis_home_y_btn.clicked.connect(
            partial(self.handle_gcode, ["G28 Y"])
        )
        self.panel.move_axis_home_z_btn.clicked.connect(
            partial(self.handle_gcode, ["G28 Z"])
        )
        self.panel.move_axis_home_all_btn.clicked.connect(
            partial(self.handle_gcode, ["G28"])
        )
        # REVIEW: Check if i can aggregate the same method, but with different values, instead of using different connects

        # Move Axis arrow buttons
        # REVIEW: Aggregate these .connect(...)
        self.panel.move_axis_up_btn.clicked.connect(partial(self.handle_move_axis, "Y"))
        self.panel.move_axis_down_btn.clicked.connect(
            partial(self.handle_move_axis, "Y-")
        )
        self.panel.move_axis_right_btn.clicked.connect(
            partial(self.handle_move_axis, "X")
        )
        self.panel.move_axis_left_btn.clicked.connect(
            partial(self.handle_move_axis, "X-")
        )
        self.panel.mva_z_up.clicked.connect(partial(self.handle_move_axis, "Z"))
        self.panel.mva_z_down.clicked.connect(partial(self.handle_move_axis, "Z-"))

        # Temperature
        self.panel.temp_back_button.clicked.connect(self.back_button)

        # Printer Settings Screen
        self.panel.printer_settings_back_btn.clicked.connect(self.back_button)

        self.run_gcode_signal.connect(self.ws.api.run_gcode)
        # @ object temperature change clicked

        self.panel.extruder_temp_display.clicked.connect(
            partial(
                self.request_numpad_signal.emit,
                2,
                "extruder",
                str(self.panel.extruder_temp_display.text()),
                self.handle_numpad_change,
                self,
            )
        )

        self.panel.bed_temp_display.clicked.connect(
            partial(
                self.request_numpad_signal.emit,
                2,
                "heater_bed",
                str(self.panel.bed_temp_display.text()),
                self.handle_numpad_change,
                self,
            )
        )

    def handle_gcode(self, gcode_list) -> None:
        for gcode in gcode_list:
            logging.debug(f"[ControlTabPanel] Emitting gcode signal: {gcode}")
            self.run_gcode_signal.emit(gcode)

    def change_page(self, index):
        self.request_change_page.emit(2, index)
        logging.debug(
            f"[ControlTabPanel] {self.change_page.__qualname__} called, emitting change page signal to {index}"
        )

    def back_button(self):
        self.request_back_button_pressed.emit()
        logging.debug("[ControlTabPanel] back button pressed")

    @pyqtSlot(str, int, name="numpad_new_value")
    @pyqtSlot(str, float, name="numpad_new_value")
    def handle_numpad_change(self, name: str, new_value: int | float) -> None:
        if name.startswith("fan") and isinstance(new_value, float):
            if 0.0 <= new_value <= 1.0:
                self.run_gcode_signal.emit(
                    f"SET_FAN_SPEED FAN={name} SPEED={new_value}"
                )

        elif isinstance(new_value, int):
            self.run_gcode_signal.emit(
                f"SET_HEATER_TEMPERATURE HEATER={name} TARGET={new_value}"
            )

    @pyqtSlot(bool, "PyQt_PyObject", int, name="select_extrude_feedrate")
    def handle_toggle_extrude_feedrate(self, checked, caller, value) -> None:
        if value == self.extrude_feedrate:
            return
        self.extrude_feedrate = value

    @pyqtSlot(bool, "PyQt_PyObject", int, name="select_extrude_length")
    def handle_toggle_extrude_length(self, checked: bool, caller, value: int) -> None:
        if self.extrude_length == value:
            return
        self.extrude_length = value

    @pyqtSlot(bool, float, name="handle_select_move_feedrate")
    def handle_select_move_feedrate(self, checked: bool, value: float) -> None:
        if self.move_feedrate == value:
            return
        self.move_feedrate = value

    @pyqtSlot(bool, float, name="handle_select_move_length")
    def handle_select_move_length(self, checked: bool, value: float) -> None:
        if self.move_length == value:
            return
        self.move_length = value

    def handle_extrusion(self, extrude) -> None:
        # TEST: Does the machine actually extrude or not
        can_extrude = self.printer.heaters_object["extruder"]["can_extrude"]

        if not can_extrude:
            self.panel.extrude_text_label.setText("Temperature too cold to extrude")
            return

        self.run_gcode_signal.emit("M83")
        if extrude:
            logging.debug(
                f"[ControlTabPanel] Emitting gcode signal:\nM83\nG1 E{self.extrude_length} F{self.extrude_feedrate * 60}"
            )
            self.run_gcode_signal.emit(
                f"G1 E{self.extrude_length} F{self.extrude_feedrate * 60}"
            )
            self.panel.extrude_text_label.setText(
                f"Extruding {self.extrude_length}mm at {self.extrude_feedrate}mm/s"
            )
        else:
            logging.debug(
                f"[ControlTabPanel] Emitting gcode signal:\nM83\nG1 E-{self.extrude_length} F{self.extrude_feedrate * 60}"
            )
            self.run_gcode_signal.emit(
                f"G1 E-{self.extrude_length} F{self.extrude_feedrate * 60}"
            )
            self.panel.extrude_text_label.setText(
                f"Retracting {self.extrude_length}mm at {self.extrude_feedrate}mm/s"
            )

    def handle_move_axis(self, axis) -> None:
        # REVIEW: Commands to move the axis
        logging.debug(
            f"[ControlTabPanel] Emitting gcode signal:\nG91\nG1 {axis}{self.move_length} F{self.move_feedrate * 60}\nG90"
        )
        self.run_gcode_signal.emit("G91")
        self.run_gcode_signal.emit(
            f"G1 {axis}{self.move_length} F{self.move_feedrate * 60}"
        )
        self.run_gcode_signal.emit("G90")

    def switch_extruder(self) -> None:
        # REVIEW: Naming conventions
        # TODO: Make this method available only when there is more than one extruder
        if self.printer.active_extruder_name == "extruder":
            self.handle_gcode(["T1"])
        else:
            self.handle_gcode(["T0"])

    @pyqtSlot(str, list, name="toolhead_update")
    def toolhead_position_change(self, field: str, values: list) -> None:
        # TEST: Does this actually work correctly?
        # TODO: What head is it moving? Adapt to show the number of the extruder/head
        if field == "position":
            logging.debug(f"[ControlTabPanel] Updating toolhead {field} to: {values}")
            self.panel.move_axis_x_value_label.setText(f"{values[0]}")
            self.panel.move_axis_y_value_label.setText(f"{values[1]}")
            self.panel.move_axis_z_value_label.setText(f"{values[2]}")

    @pyqtSlot(str, str, float, name="extruder_update")
    def extruder_temperature_change(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        # REVIEW: Naming convention when more than one extruder exists
        # TEST: Check if this is bulletproof
        if extruder_name == "extruder" and field == "temperature":
            self.panel.extruder_temp_display.setText(f"{new_value:.1f}")

        if extruder_name == "extruder" and field == "target":
            self.panel.extruder_temp_display.setSecondaryText(f"{new_value:.1f}")

        if extruder_name == "extruder1" and field == "temperature":
            ...

    @pyqtSlot(str, str, float, name="heater_bed_update")
    def heater_bed_temperature_change(
        self, name: str, field: str, new_value: float
    ) -> None:
        # TEST: Test if it works in all cases.
        if field == "temperature":
            self.panel.bed_temp_display.setText(f"{new_value:.1f}")

        if field == "target":
            self.panel.bed_temp_display.setSecondaryText(f"{new_value:.1f}")

    def paintEvent(self, a0: QPaintEvent) -> None:
        # Paint button bars
        return super().paintEvent(a0)
