from __future__ import annotations
import logging
import typing
from functools import partial

# from lib.bo.printer import Printer
# from lib.moonrakerComm import MoonWebSocket
from lib.panels.probeHelperPage import ProbeHelper
from lib.ui.controlStackedWidget_ui import Ui_controlStackedWidget
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import (
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtGui import QPaintEvent


class ControlTab(QtWidgets.QStackedWidget):
    request_back_button = pyqtSignal(name="request_back_button")
    request_change_page = pyqtSignal(int, int, name="request_change_page")

    request_numpad_signal = pyqtSignal(
        int,
        str,
        str,
        "PyQt_PyObject",
        QtWidgets.QStackedWidget,
        name="request_numpad",
    )

    run_gcode_signal = pyqtSignal(str, name="run_gcode")

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        ws: typing.Type["MoonWebSocket"],
        printer: typing.Type["Printer"],
        /,
    ) -> None:
        super().__init__(parent)
        self.panel = Ui_controlStackedWidget()
        self.panel.setupUi(self)

        self.ws = ws
        self.printer = printer
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.timers = []
        self.extruder_info: dict = {}
        self.bed_info: dict = {}
        self.toolhead_info: dict = {}
        self.extrude_length: int = 10
        self.extrude_feedrate: int = 2
        self.extrude_page_message: str = ""
        self.move_length: float = 1.0
        self.move_speed: float = 25.0

        self.probe_helper_page = ProbeHelper(self)
        self.addWidget(self.probe_helper_page)
        self.probe_helper_page.request_page_view.connect(
            partial(self.change_page, self.indexOf(self.probe_helper_page))
        )
        self.probe_helper_page.query_printer_object.connect(
            self.ws.api.object_query
        )
        self.probe_helper_page.run_gcode_signal.connect(self.ws.api.run_gcode)
        self.probe_helper_page.request_back.connect(self.back_button)
        self.printer.available_gcode_cmds.connect(
            self.probe_helper_page.on_available_gcode_cmds
        )
        self.probe_helper_page.subscribe_config[str, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )

        self.probe_helper_page.subscribe_config[list, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )
        self.printer.gcode_move_update.connect(
            self.probe_helper_page.on_gcode_move_update
        )
        self.printer.manual_probe_update.connect(
            self.probe_helper_page.on_manual_probe_update
        )
        self.printer.printer_config.connect(
            self.probe_helper_page.on_printer_config
        )
        self.printer.gcode_response.connect(
            self.probe_helper_page.handle_gcode_response
        )

        self.printer.toolhead_update[str, list].connect(
            self.on_toolhead_update
        )
        self.printer.extruder_update.connect(self.on_extruder_update)
        self.printer.heater_bed_update.connect(self.on_heater_bed_update)

        self.panel.cp_motion_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.motion_page))
        )
        self.panel.cp_temperature_btn.clicked.connect(
            partial(
                self.change_page, self.indexOf(self.panel.temperature_page)
            )
        )
        self.panel.cp_printer_settings_btn.clicked.connect(
            partial(
                self.change_page,
                self.indexOf(self.panel.printer_settings_page),
            )
        )
        # self.panel.cp_nozzles_calibration_btn.clicked.connect(
        #     partial(self.change_page, self.indexOf(self.panel.z_adjustment_page))
        # )
        self.panel.cp_nozzles_calibration_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.probe_helper_page))
        )

        self.panel.motion_extrude_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.extrude_page))
        )
        self.panel.motion_move_axis_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.move_axis_page))
        )
        self.panel.mp_back_btn.clicked.connect(self.back_button)
        self.panel.motion_auto_home_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "G28\nM400")
        )
        self.panel.motion_disable_steppers_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "M84\nM400")
        )

        self.panel.exp_back_btn.clicked.connect(self.back_button)

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
            partial(self.handle_select_move_length, value=10.0)
        )
        self.panel.move_axis_select_length_100_btn.toggled.connect(
            partial(self.handle_select_move_length, value=100.0)
        )
        self.panel.move_axis_select_speed_25_btn.toggled.connect(
            partial(self.handle_select_move_speed, value=25.0)
        )
        self.panel.move_axis_select_speed_50_btn.toggled.connect(
            partial(self.handle_select_move_speed, value=50.0)
        )
        self.panel.move_axis_select_speed_100_btn.toggled.connect(
            partial(self.handle_select_move_speed, value=100.0)
        )
        self.panel.exp_extrude_btn.clicked.connect(
            partial(self.handle_extrusion, True)
        )  # True for extrusion
        self.panel.exp_unextrude_btn.clicked.connect(
            partial(self.handle_extrusion, False)
        )  # False for retraction

        # Move Axis
        self.panel.mva_back_btn.clicked.connect(self.back_button)

        self.panel.move_axis_home_x_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "G28 X\nM400")
        )
        self.panel.move_axis_home_y_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "G28 Y\nM400")
        )
        self.panel.move_axis_home_z_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "G28 Z\nM400")
        )
        self.panel.move_axis_home_all_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "G28\nM400")
        )
        self.panel.move_axis_up_btn.clicked.connect(
            partial(self.handle_move_axis, "Y")
        )
        self.panel.move_axis_down_btn.clicked.connect(
            partial(self.handle_move_axis, "Y-")
        )
        self.panel.move_axis_right_btn.clicked.connect(
            partial(self.handle_move_axis, "X")
        )
        self.panel.move_axis_left_btn.clicked.connect(
            partial(self.handle_move_axis, "X-")
        )
        self.panel.mva_z_up.clicked.connect(
            partial(self.handle_move_axis, "Z")
        )
        self.panel.mva_z_down.clicked.connect(
            partial(self.handle_move_axis, "Z-")
        )

        self.panel.temp_back_button.clicked.connect(self.back_button)

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
        self.panel.cooldown_btn.clicked.connect(
            lambda: self.run_gcode_signal.emit(
                "SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=0\n\
                SET_HEATER_TEMPERATURE HEATER=extruder TARGET=0"
            )
        )

    def change_page(self, index):
        self.request_change_page.emit(2, index)
        logging.debug(
            f"[ControlTabPanel] {self.change_page.__qualname__} called, emitting change page signal to {index}"
        )

    def back_button(self):
        self.request_back_button.emit()
        logging.debug("[ControlTabPanel] back button pressed")

    def register_timed_callback(self, time, callback) -> None:
        _timer = QtCore.QTimer()
        _timer.setSingleShot(True)
        _timer.timeout.connect(callback)
        _timer.start(int(time))
        self.timers.append(_timer)

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
    def handle_toggle_extrude_feedrate(
        self, checked: bool, caller, value: int
    ) -> None:
        """Slot to change the extruder feedrate, mainly used for toggle buttons

        Args:
            checked (bool): Button checked state
            caller (PyQtObject): The button that called this slot
            value (int): New value for the extruder feedrate
        """
        if value == self.extrude_feedrate:
            return
        self.extrude_feedrate = value

    @pyqtSlot(bool, "PyQt_PyObject", int, name="select_extrude_length")
    def handle_toggle_extrude_length(
        self, checked: bool, caller, value: int
    ) -> None:
        """Slot that changes the extrude length, mainly used for toggle buttons

        Args:
            checked (bool): Button checked state
            caller (PyQtObject): The button that called this slot
            value (int): New value for the extrude length
        """
        if self.extrude_length == value:
            return
        self.extrude_length = value

    @pyqtSlot(bool, float, name="handle_select_move_speed")
    def handle_select_move_speed(self, checked: bool, value: float) -> None:
        """Slot that changes the move speed of manual move commands, mainly used
        for toggle buttons

        Args:
            checked (bool): Button checked state
            value (float): New move speed value
        """
        if self.move_speed == value:
            return
        self.move_speed = value

    @pyqtSlot(bool, float, name="handle_select_move_length")
    def handle_select_move_length(self, checked: bool, value: float) -> None:
        """Slot that changes the move length of manual move commands,
        mainly used for toggle buttons


        Args:
            checked (bool): Button checked state
            value (float): New length value
        """
        if self.move_length == value:
            return
        self.move_length = value

    @pyqtSlot(str, name="handle_extrusion")
    def handle_extrusion(self, extrude: bool) -> None:
        """Slot that requests an extrusion/unextrusion move

        Args:
            extrude (bool): If True extrudes otherwise unextrudes.
        """
        can_extrude = bool(
            self.printer.heaters_object["extruder"]["can_extrude"]
        )

        if not can_extrude:
            self.extrude_page_message = "Temperature too cold to extrude"
            self.panel.exp_info_label.setText(self.extrude_page_message)
            return

        if extrude:
            self.run_gcode_signal.emit(
                f"M83\nG1 E{self.extrude_length} F{self.extrude_feedrate * 60}\nM82\nM400"
            )
            self.extrude_page_message = "Extruding"
            self.panel.exp_info_label.setText(self.extrude_page_message)
        else:
            self.run_gcode_signal.emit(
                f"M83\nG1 E-{self.extrude_length} F{self.extrude_feedrate * 60}\nM82\nM400"
            )
            self.extrude_page_message = "Retracting"
            self.panel.exp_info_label.setText(self.extrude_page_message)

        # This block of code schedules a method to be called in x amount of milliseconds
        _sch_time_s = float(
            self.extrude_length / self.extrude_feedrate
        )  # calculate the amount of time it'll take for the operation
        self.extrude_page_message = "Ready"
        self.register_timed_callback(
            int(_sch_time_s + 2.0) * 1000,  # In milliseconds
            lambda: self.panel.exp_info_label.setText(
                self.extrude_page_message
            ),
        )

    @pyqtSlot(str, name="handle_move_axis")
    def handle_move_axis(self, axis: str) -> None:
        """Slot that requests manual move command



        Args:
            axis (str): String that contains one of the following axis `
                ['X',
                'X-'
                ,'Y'
                ,'Y-'
                ,'Z'
                ,'Z-']`. [^1]

        ---


        [^1]: The **-** symbol indicates the negative direction for that axis

        """
        if axis not in ["X", "X-", "Y", "Y-", "Z", "Z-"]:
            return

        self.run_gcode_signal.emit(
            f"G91\nG0 {axis}{float(self.move_length)} F{float(self.move_speed * 60)}\nG90\nM400"
        )

    @pyqtSlot(str, name="switch_extruder")
    def switch_extruder(self) -> None:
        """Requests extruder change

        TODO : Only available when more than one extruder exists

        **Currently not used!**
        """
        if self.printer.active_extruder_name == "extruder":
            self.run_gcode_signal.emit("T1\nM400")
        else:
            self.run_gcode_signal.emit("T0\nM400")

    @pyqtSlot(str, list, name="on_toolhead_update")
    def on_toolhead_update(self, field: str, values: list) -> None:
        if field == "position":
            logging.debug(
                f"[ControlTabPanel] Updating toolhead {field} to: {values}"
            )
            self.panel.move_axis_x_value_label.setText(f"{values[0]}")
            self.panel.move_axis_y_value_label.setText(f"{values[1]}")
            self.panel.move_axis_z_value_label.setText(f"{values[2]}")

        self.toolhead_info.update({f"{field}": values})

    @pyqtSlot(str, str, float, name="on_extruder_update")
    def on_extruder_update(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        if extruder_name == "extruder" and field == "temperature":
            self.panel.extruder_temp_display.setText(f"{new_value:.1f}")
        if extruder_name == "extruder" and field == "target":
            self.panel.extruder_temp_display.set_secondary_text(
                f"{new_value:.1f}"
            )

        self.extruder_info.update(
            {f"{extruder_name}": {f"{field}": new_value}}
        )

    @pyqtSlot(str, str, float, name="on_heater_bed_update")
    def on_heater_bed_update(
        self, name: str, field: str, new_value: float
    ) -> None:
        if field == "temperature":
            self.panel.bed_temp_display.setText(f"{new_value:.1f}")
        if field == "target":
            self.panel.bed_temp_display.set_secondary_text(f"{new_value:.1f}")
        self.bed_info.update({f"{name}": {f"{field}": new_value}})

    def paintEvent(self, a0: QPaintEvent) -> None:
        if self.panel.extrude_page.isVisible():
            self.panel.exp_info_label.setText(self.extrude_page_message)
        return super().paintEvent(a0)
