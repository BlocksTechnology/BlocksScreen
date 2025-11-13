from __future__ import annotations

import typing
from functools import partial
import re
from lib.moonrakerComm import MoonWebSocket
from lib.panels.widgets.loadPage import LoadScreen
from lib.panels.widgets.numpadPage import CustomNumpad
from lib.panels.widgets.printcorePage import SwapPrintcorePage
from lib.panels.widgets.probeHelperPage import ProbeHelper
from lib.printer import Printer
from lib.ui.controlStackedWidget_ui import Ui_controlStackedWidget  
from PyQt6 import QtCore, QtGui, QtWidgets

from lib.panels.widgets.popupDialogWidget import Popup
from lib.utils.display_button import DisplayButton
from lib.panels.widgets.slider_selector_page import SliderPage

from lib.panels.widgets.optionCardWidget import OptionCard
from helper_methods import normalize

class ControlTab(QtWidgets.QStackedWidget):
    """Printer Control Stacked Widget"""

    request_back_button = QtCore.pyqtSignal(name="request-back-button")
    request_change_page = QtCore.pyqtSignal(int, int, name="request-change-page")
    request_numpad_signal = QtCore.pyqtSignal(
        int,
        str,
        str,
        "PyQt_PyObject",
        QtWidgets.QStackedWidget,
        name="request-numpad",
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    disable_popups: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="disable-popups"
    )
    request_numpad: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str, int, "PyQt_PyObject"],
        [str, int, "PyQt_PyObject", int, int],
        name="request-numpad",
    )
    request_file_info: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request-file-info"
    )
    tune_display_buttons: dict = {}
    card_options: dict = {}

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        ws: MoonWebSocket,
        printer: Printer,
        /,
    ) -> None:
        super().__init__(parent)
        self.panel = Ui_controlStackedWidget()
        self.panel.setupUi(self)

        self.popup = Popup(self)

        self.ws: MoonWebSocket = ws
        self.printer: Printer = printer
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
        self.printcores_page = SwapPrintcorePage(self)
        self.addWidget(self.printcores_page)
        self.loadpage = LoadScreen(self, LoadScreen.AnimationGIF.DEFAULT)
        self.addWidget(self.loadpage)

        self.sliderPage = SliderPage(self)
        self.addWidget(self.sliderPage)
        self.sliderPage.request_back.connect(self.back_button)
        
        self.probe_helper_page.request_page_view.connect(
            partial(self.change_page, self.indexOf(self.probe_helper_page))
        )
        self.probe_helper_page.query_printer_object.connect(self.ws.api.object_query)
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
        self.printer.printer_config.connect(self.probe_helper_page.on_printer_config)
        self.printer.gcode_response.connect(
            self.probe_helper_page.handle_gcode_response
        )
        self.printer.toolhead_update[str, list].connect(self.on_toolhead_update)
        self.printer.extruder_update.connect(self.on_extruder_update)
        self.printer.heater_bed_update.connect(self.on_heater_bed_update)
        self.panel.cp_motion_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.motion_page))
        )
        self.panel.cp_temperature_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.temperature_page))
        )
        self.panel.cp_fans_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.fans_page))
        )
        self.panel.fans_back_btn.clicked.connect(self.back_button)
        self.panel.cp_switch_print_core_btn.clicked.connect(self.show_swapcore)
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
        self.panel.mva_select_length_1_btn.toggled.connect(
            partial(self.handle_select_move_length, value=1.0)
        )
        self.panel.mva_select_length_10_btn.toggled.connect(
            partial(self.handle_select_move_length, value=10.0)
        )
        self.panel.mva_select_length_100_btn.toggled.connect(
            partial(self.handle_select_move_length, value=100.0)
        )
        self.panel.mva_select_speed_25_btn.toggled.connect(
            partial(self.handle_select_move_speed, value=25.0)
        )
        self.panel.mva_select_speed_50_btn.toggled.connect(
            partial(self.handle_select_move_speed, value=50.0)
        )
        self.panel.mva_select_speed_100_btn.toggled.connect(
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
        self.panel.mva_home_x_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "G28 X\nM400")
        )
        self.panel.mva_home_y_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "G28 Y\nM400")
        )
        self.panel.mva_home_z_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "G28 Z\nM400")
        )
        self.panel.mva_home_all_btn.clicked.connect(
            partial(self.run_gcode_signal.emit, "G28\nM400")
        )
        self.panel.mva_up_btn.clicked.connect(partial(self.handle_move_axis, "Y"))
        self.panel.mva_down_btn.clicked.connect(partial(self.handle_move_axis, "Y-"))
        self.panel.mva_right_btn.clicked.connect(partial(self.handle_move_axis, "X"))
        self.panel.mva_left_btn.clicked.connect(partial(self.handle_move_axis, "X-"))
        self.panel.mva_z_up.clicked.connect(
            partial(self.handle_move_axis, "Z-")  # Move nozzle closer to bed
        )
        self.panel.mva_z_down.clicked.connect(
            partial(self.handle_move_axis, "Z")  # Move nozzle away from bed
        )
        self.panel.temp_back_button.clicked.connect(self.back_button)
        self.panel.printer_settings_back_btn.clicked.connect(self.back_button)
        self.run_gcode_signal.connect(self.ws.api.run_gcode)
        # @ object temperature change clicked
        self.numpadPage = CustomNumpad(self)
        self.numpadPage.request_back.connect(self.request_back_button)
        self.addWidget(self.numpadPage)

        self.panel.extruder_temp_display.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Extruder Temperature",
                int(round(float(self.panel.extruder_temp_display.secondary_text))),
                self.on_numpad_change,
                0,
                300,  # TODO: Get this value from printer objects
            )
        )
        self.panel.bed_temp_display.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Bed Temperature",
                int(round(float(self.panel.bed_temp_display.secondary_text))),
                self.on_numpad_change,
                0,
                120,  # TODO: Get this value from printer objects
            )
        )
        self.request_numpad[str, int, "PyQt_PyObject", int, int].connect(
            self.on_numpad_request
        )

        self.panel.cooldown_btn.clicked.connect(
            lambda: self.run_gcode_signal.emit(
                "SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=0\n\
                SET_HEATER_TEMPERATURE HEATER=extruder TARGET=0"
            )
        )

        self.panel.cp_z_tilt_btn.clicked.connect(lambda: self.handle_ztilt())

        self.printcores_page.pc_accept.clicked.connect(self.handle_swapcore)

        self.ws.klippy_state_signal.connect(self.on_klippy_status)
        self.ws.klippy_state_signal.connect(self.probe_helper_page.on_klippy_status)
        self.printer.on_printcore_update.connect(self.handle_printcoreupdate)
        self.printer.gcode_response.connect(self._handle_gcode_response)

        # self.panel.cp_printer_settings_btn.hide()
        self.panel.temperature_cooldown_btn.hide()
        self.panel.cooldown_btn.hide()
        self.panel.cp_switch_print_core_btn.hide()

        self.printer.fan_update[str, str, float].connect(
            self.on_fan_object_update
        )
        self.printer.fan_update[str, str, int].connect(
            self.on_fan_object_update
        )

    @QtCore.pyqtSlot(str, str, float, name="on_fan_update")
    @QtCore.pyqtSlot(str, str, int, name="on_fan_update")
    def on_fan_object_update(
        self, name: str, field: str, new_value: int | float
    ) -> None:
        """Slot Method that receives information from fan objects

        Args:
            name (str): fan object name
            field (str): field name
            new_value (int | float): New value for field name
        """
        if "speed" in field:
            if not self.tune_display_buttons.get(name, None):
                if name in ("fan", "fan_generic"):       
                    if  "blower" in name.lower():
                        _icon = QtGui.QPixmap(
                            ":/temperature_related/media/btn_icons/blower.svg"
                        )
                    else:
                        _icon = QtGui.QPixmap(":/temperature_related/media/btn_icons/fan.svg")

                    _card = OptionCard(self, name, str(name), _icon)  # type: ignore
                    _card.setObjectName(str(name))
                    self.card_options.update({str(name): _card})
                    self.panel.fans_content_layout.addWidget(_card)

                    if not hasattr(self.card_options.get(name), "continue_clicked"):
                        del _card
                        self.card_options.pop(name)
                        return
                    
                    self.card_options.get(name).setMode(True)
                    self.card_options.get(name).secondtext.setText(f"{new_value}%")
                    self.card_options.get(name).continue_clicked.connect(
                        lambda: self.on_slidePage_request(
                            str(name),
                            self.card_options.get(name).secondtext.text().replace("%", ""),
                            self.on_slider_change,
                            0,
                            100,
                        )
                    )
                    self.tune_display_buttons[name] = self.card_options.get(name) #{self.card_options.get(name),True,self.card_options.get(name).secondtext.text().replace("%", "")}


                    self.card_options.get(name)
                    self.update()
            _display_button = self.tune_display_buttons.get(name)
            if not _display_button:
                return
            _display_button.secondtext.setText(
                f"{new_value * 100:.0f}%"
            )

    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", name="on_slidePage_request")
    @QtCore.pyqtSlot(
        str, int, "PyQt_PyObject", int, int, name="on_slidePage_request"
    )
    def on_slidePage_request(
        self,
        name: str,
        current_value: int,
        callback,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        self.sliderPage.value_selected.connect(callback)
        self.sliderPage.set_name(name)
        self.sliderPage.set_slider_position(int(current_value))
        self.sliderPage.set_slider_minimum(min_value)
        self.sliderPage.set_slider_maximum(max_value)
        self.change_page(self.indexOf(self.sliderPage))


    @QtCore.pyqtSlot(str, int, name="on_slider_change")
    def on_slider_change(self, name: str, new_value: int) -> None:
        if "speed" in name.lower():
            self.speed_factor_override = new_value / 100
            self.run_gcode_signal.emit(f"M220 S{new_value}")

        if "fan" in name.lower():
            if name.lower() == "fan":
                self.run_gcode_signal.emit(
                    f"M106 S{int(round((normalize(float(new_value / 100), 0.0, 1.0, 0, 255))))}"
                )  # [0, 255] Range
            else:
                self.run_gcode_signal.emit(
                    f"SET_FAN_SPEED FAN={name} SPEED={float(new_value / 100.00)}"
                )  # [0.0, 1.0] Range

    def create_display_button(self, name: str) -> DisplayButton:
        """Create and return a DisplayButton

        Args:
            name (str): Name for the display button

        Returns:
            DisplayButton: The created DisplayButton object
        """
        display_button = DisplayButton()
        display_button.setObjectName(str(name + "_display"))
        display_button.setMinimumSize(QtCore.QSize(150, 50))
        display_button.setMaximumSize(QtCore.QSize(150, 80))
        font = QtGui.QFont()
        font.setPointSize(16)
        display_button.setFont(font)
        return display_button
    
    def handle_printcoreupdate(self, value:dict):

        if value["swapping"] == "idle":
            return

        if value["swapping"] == "in_pos":
            self.loadpage.hide()
            self.printcores_page.show()
            self.disable_popups.emit(True)
            self.printcores_page.setText(
                "Please Insert Print Core \n \n Afterwards click continue"
            )
        if value["swapping"] == "unloading":
            self.loadpage.set_status_message("Unloading print core")

        if value["swapping"] == "cleaning":
            self.loadpage.set_status_message("Cleaning print core")

    def _handle_gcode_response(self, messages: list):
        """Handle gcode response for Z-tilt adjustment"""
        pattern = r"Retries:\s*(\d+)/(\d+).*?range:\s*([\d.]+)\s*tolerance:\s*([\d.]+)"

        for msg_list in messages:
            if not msg_list:
                continue

            if (
                "Retries:" in msg_list
                and "range:" in msg_list
                and "tolerance:" in msg_list
            ):
                print("Match candidate:", msg_list)
                match = re.search(pattern, msg_list)
                print("Regex match:", match)

                if match:
                    retries_done = int(match.group(1))
                    retries_total = int(match.group(2))
                    probed_range = float(match.group(3))
                    tolerance = float(match.group(4))
                    if retries_done == retries_total:
                        self.loadpage.hide()
                        return

                    if probed_range < tolerance:
                        self.loadpage.hide()
                        return

                    self.loadpage.set_status_message(
                        f"Retries: {retries_done}/{retries_total} | Range: {probed_range:.6f} | Tolerance: {tolerance:.6f}"
                    )

    def handle_ztilt(self):
        """Handle Z-Tilt Adjustment"""
        self.loadpage.show()
        self.loadpage.set_status_message("Please wait, performing Z-axis calibration.")
        self.run_gcode_signal.emit("G28\nM400\nZ_TILT_ADJUST")

    @QtCore.pyqtSlot(str, name="on-klippy-status")
    def on_klippy_status(self, state: str):
        """Handles incoming klippy status changes"""
        if state.lower() == "ready":
            self.printcores_page.hide()
            self.disable_popups.emit(False)
            return
        if state.lower() == "startup":
            self.printcores_page.setText("Almost done \n be patient")
            return

    def show_swapcore(self):
        """Show swap printcore"""
        self.run_gcode_signal.emit("CHANGE_PRINTCORES")
        self.loadpage.show()
        self.loadpage.set_status_message("Preparing to swap print core")

    def handle_swapcore(self):
        """Handle swap printcore routine finish"""
        self.printcores_page.setText("Executing \n Firmware Restart")
        self.run_gcode_signal.emit("FIRMWARE_RESTART")

    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", name="on-numpad-request")
    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", int, int, name="on-numpad-request")
    def on_numpad_request(
        self,
        name: str,
        current_value: int,
        callback,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        """Handles numpad widget request"""
        self.numpadPage.value_selected.connect(callback)
        self.numpadPage.set_name(name)
        self.numpadPage.set_value(current_value)
        self.numpadPage.set_min_value(min_value)
        self.numpadPage.set_max_value(max_value)
        self.change_page(self.indexOf(self.numpadPage))

    @QtCore.pyqtSlot(str, int, name="on-numpad-change")
    def on_numpad_change(self, name: str, new_value: int) -> None:
        """Handles inputted numpad values"""
        if "bed" in name.lower():
            name = "heater_bed"
        elif "extruder" in name.lower():
            name = "extruder"
        self.run_gcode_signal.emit(
            f"SET_HEATER_TEMPERATURE HEATER={name} TARGET={new_value}"
        )

    def change_page(self, index):
        """Handles changing page"""
        self.request_change_page.emit(2, index)

    def back_button(self):
        """Handle back button click"""
        self.request_back_button.emit()

    def register_timed_callback(self, time: int, callback: callable) -> None:
        """Registers timed callback and starts the timeout"""
        _timer = QtCore.QTimer()
        _timer.setSingleShot(True)
        _timer.timeout.connect(callback)
        _timer.start(int(time))
        self.timers.append(_timer)

    @QtCore.pyqtSlot(bool, "PyQt_PyObject", int, name="select-extrude-feedrate")
    def handle_toggle_extrude_feedrate(self, checked: bool, caller, value: int) -> None:
        """Slot to change the extruder feedrate, mainly used for toggle buttons

        Args:
            checked (bool): Button checked state
            caller (PyQtObject): The button that called this slot
            value (int): New value for the extruder feedrate
        """
        if value == self.extrude_feedrate:
            return
        self.extrude_feedrate = value

    @QtCore.pyqtSlot(bool, "PyQt_PyObject", int, name="select-extrude-length")
    def handle_toggle_extrude_length(self, checked: bool, caller, value: int) -> None:
        """Slot that changes the extrude length, mainly used for toggle buttons

        Args:
            checked (bool): Button checked state
            caller (PyQtObject): The button that called this slot
            value (int): New value for the extrude length
        """
        if self.extrude_length == value:
            return
        self.extrude_length = value

    @QtCore.pyqtSlot(bool, float, name="handle-select-move-speed")
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

    @QtCore.pyqtSlot(bool, float, name="handle-select-move-length")
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

    @QtCore.pyqtSlot(str, name="handle-extrusion")
    def handle_extrusion(self, extrude: bool) -> None:
        """Slot that requests an extrusion/unextrusion move

        Args:
            extrude (bool): If True extrudes otherwise unextrudes.
        """
        can_extrude = bool(self.printer.heaters_object["extruder"]["can_extrude"])
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
            lambda: self.panel.exp_info_label.setText(self.extrude_page_message),
        )

    @QtCore.pyqtSlot(str, name="handle-move-axis")
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

    @QtCore.pyqtSlot(str, list, name="on-toolhead-update")
    def on_toolhead_update(self, field: str, values: list) -> None:
        """Handles updated from toolhead printer object"""
        if field == "position":
            self.panel.mva_x_value_label.setText(f"{values[0]:.2f}")
            self.panel.mva_y_value_label.setText(f"{values[1]:.2f}")
            self.panel.mva_z_value_label.setText(f"{values[2]:.3f}")

            if values[0] == "252,50" and values[1] == "250" and values[2] == "50":
                self.loadpage.hide
        self.toolhead_info.update({f"{field}": values})

    @QtCore.pyqtSlot(str, str, float, name="on-extruder-update")
    def on_extruder_update(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        """Handles updates from extruder printer object"""
        if extruder_name == "extruder" and field == "temperature":
            self.panel.extruder_temp_display.setText(f"{new_value:.1f}")
        if extruder_name == "extruder" and field == "target":
            self.panel.extruder_temp_display.secondary_text = f"{new_value:.1f}"
        self.extruder_info.update({f"{extruder_name}": {f"{field}": new_value}})

    @QtCore.pyqtSlot(str, str, float, name="on-heater-bed-update")
    def on_heater_bed_update(self, name: str, field: str, new_value: float) -> None:
        """Handles updated from heater_bed printer object"""
        if field == "temperature":
            self.panel.bed_temp_display.setText(f"{new_value:.1f}")
        if field == "target":
            self.panel.bed_temp_display.secondary_text = f"{new_value:.1f}"
        self.bed_info.update({f"{name}": {f"{field}": new_value}})

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Handles ControlTab Widget painting"""
        if self.panel.extrude_page.isVisible():
            self.panel.exp_info_label.setText(self.extrude_page_message)
        return super().paintEvent(a0)
