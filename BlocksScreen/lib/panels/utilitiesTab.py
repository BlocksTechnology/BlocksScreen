import typing
from dataclasses import dataclass
from enum import Enum, auto
from functools import partial

from lib.moonrakerComm import MoonWebSocket
from lib.panels.widgets.troubleshootPage import TroubleshootPage
from lib.printer import Printer
from lib.ui.utilitiesStackedWidget_ui import Ui_utilitiesStackedWidget
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.toggleAnimatedButton import ToggleAnimatedButton
from PyQt6 import QtCore, QtGui, QtWidgets

from lib.panels.widgets.optionCardWidget import OptionCard
from lib.panels.widgets.inputshaperPage import InputShaperPage
from lib.panels.widgets.basePopup import BasePopup
from lib.panels.widgets.loadWidget import LoadingOverlayWidget

import re


@dataclass
class LedState:
    """Represents the state of an LED light."""

    led_type: str
    red: int = 0
    green: int = 0
    blue: int = 0
    white: int = 255
    state: str = "on"

    def get_gcode(self, name: str) -> str:
        """Generates the G-code command for the current state."""
        if self.state == "off":
            return f"SET_LED LED={name} RED=0 GREEN=0 BLUE=0 WHITE=0"
        if self.led_type == "white":
            return f"SET_LED LED={name} WHITE={self.white / 255:.2f}"
        # Default to RGB
        return (
            f"SET_LED LED={name} RED={self.red / 255:.2f} "
            f"GREEN={self.green / 255:.2f} BLUE={self.blue / 255:.2f} "
            f"WHITE={self.white / 255:.2f}"
        )


class Process(Enum):
    FAN = auto()
    AXIS = auto()
    BED_HEATER = auto()
    EXTRUDER = auto()
    AXIS_MAINTENANCE = auto()


class UtilitiesTab(QtWidgets.QStackedWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-back"
    )
    request_change_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, int, name="request-change-page"
    )
    request_available_objects_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="get-available-objects")
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    request_numpad_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int,
        str,
        str,
        "PyQt_PyObject",
        QtWidgets.QStackedWidget,
        name="request-numpad",
    )
    subscribe_config: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [list, "PyQt_PyObject"],
        [str, "PyQt_PyObject"],
        name="on-subscribe-config",
    )
    on_update_message: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="handle-update-message"
    )

    update_available: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="update-available"
    )

    show_update_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="show-update-page"
    )

    def __init__(
        self, parent: QtWidgets.QWidget, ws: MoonWebSocket, printer: Printer
    ) -> None:
        super().__init__(parent)

        self.panel = Ui_utilitiesStackedWidget()
        self.panel.setupUi(self)

        self.ws = ws
        self.printer: Printer = printer
        self.troubleshoot_page: TroubleshootPage = TroubleshootPage(self)

        # --- State Variables ---
        self.objects: dict = {
            "fans": {},
            "axis": {"x": "indf", "y": "indf", "z": "indf"},
            "bheat": {"Bed_Heater": "indf"},
            "extrude": {"extruder": "indf"},
            "leds": {},
        }
        self.x_inputshaper: dict = {}
        self.stepper_limits: dict = {}

        self.current_object: typing.Optional[str] = None
        self.current_process: typing.Optional[Process] = None
        self.axis_in: str = "x"
        self.amount: int = 1
        self.tb: bool = False
        self.cg = None
        self.aut: bool = False

        # --- UI Setup ---
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.loadPage = BasePopup(self)
        self.loadwidget = LoadingOverlayWidget(
            self, LoadingOverlayWidget.AnimationGIF.DEFAULT
        )
        self.loadPage.add_widget(self.loadwidget)

        self.panel.update_btn.clicked.connect(
            lambda: self.show_update_page[bool].emit(False)
        )

        self.is_page = InputShaperPage(self)
        self.addWidget(self.is_page)

        self.dialog_page = BasePopup(self, dialog=True, floating=True)
        self.addWidget(self.dialog_page)

        # --- Back Buttons ---
        for button in (
            self.panel.leds_back_btn,
            self.panel.info_back_btn,
            self.panel.leds_slider_back_btn,
            self.panel.input_shaper_back_btn,
            self.panel.routine_check_back_btn,
            self.is_page.update_back_btn,
        ):
            button.clicked.connect(self.back_button)

        # --- Page Navigation ---
        self._connect_page_change(self.panel.utilities_axes_btn, self.panel.axes_page)
        self._connect_page_change(
            self.panel.utilities_input_shaper_btn, self.panel.input_shaper_page
        )
        self._connect_page_change(self.panel.utilities_info_btn, self.panel.info_page)
        self._connect_page_change(
            self.panel.utilities_routine_check_btn, self.panel.routines_page
        )
        self._connect_page_change(self.panel.am_cancel, self.panel.utilities_page)

        self._connect_page_change(self.panel.axes_back_btn, self.panel.utilities_page)
        self._connect_page_change(
            self.troubleshoot_page.tb_back_btn, self.panel.utilities_page
        )

        # --- Routines ---
        self.panel.rc_fans.clicked.connect(partial(self.run_routine, Process.FAN))
        self.panel.rc_bheat.clicked.connect(
            partial(self.run_routine, Process.BED_HEATER)
        )
        self.panel.rc_ext.clicked.connect(partial(self.run_routine, Process.EXTRUDER))
        self.panel.rc_axis.clicked.connect(partial(self.run_routine, Process.AXIS))
        self.panel.rc_no.clicked.connect(self.on_routine_answer)
        self.panel.rc_yes.clicked.connect(self.on_routine_answer)

        # --- Axis Maintenance ---
        self.panel.axis_x_btn.clicked.connect(partial(self.axis_maintenance, "x"))
        self.panel.axis_y_btn.clicked.connect(partial(self.axis_maintenance, "y"))
        self.panel.axis_z_btn.clicked.connect(partial(self.axis_maintenance, "z"))

        self.panel.toggle_led_button.state = ToggleAnimatedButton.State.ON

        # --- LEDs ---
        # self.panel.leds_r_slider.sliderReleased.connect(self.update_led_values)
        # self.panel.leds_g_slider.sliderReleased.connect(self.update_led_values)
        # self.panel.leds_b_slider.sliderReleased.connect(self.update_led_values)
        self.panel.leds_w_slider.sliderReleased.connect(self.update_led_values)
        self.panel.toggle_led_button.clicked.connect(self.toggle_led_state)

        # --- Websocket/Printer Signals ---
        self.run_gcode_signal.connect(self.ws.api.run_gcode)
        self.is_page.run_gcode_signal.connect(self.ws.api.run_gcode)
        self.subscribe_config[str, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )
        self.subscribe_config[list, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )

        # --- Initialize Printer Communication ---
        self.printer.printer_config.connect(self.on_printer_config_received)
        self.printer.gcode_move_update.connect(self.on_gcode_move_update)

        self.panel.update_btn.setPixmap(
            QtGui.QPixmap(":/system/media/btn_icons/update-software-icon.svg")
        )

        self.automatic_is = OptionCard(
            self,
            "Automatic\nInput Shaper",
            "Automatic Input Shaper",
            QtGui.QPixmap(":/input_shaper/media/btn_icons/input_shaper_auto.svg"),
        )  # type: ignore
        self.automatic_is.setObjectName("Automatic_IS_Card")
        self.panel.is_content_layout.addWidget(
            self.automatic_is, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.automatic_is.continue_clicked.connect(
            lambda: self.handle_is("SHAPER_CALIBRATE")
        )

        self.manual_is = OptionCard(
            self,
            "Manual\nInput Shaper",
            "Manual Input Shaper",
            QtGui.QPixmap(":/input_shaper/media/btn_icons/input_shaper_manual.svg"),
        )  # type: ignore
        self.manual_is.setObjectName("Manual_IS_Card")
        self.panel.is_content_layout.addWidget(
            self.manual_is, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.manual_is.continue_clicked.connect(lambda: self.handle_is(""))

        self.is_types: dict = {}
        self.is_aut_types: dict = {}

        self.is_page.action_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.panel.input_shaper_page))
        )

    def handle_gcode_response(self, data: list[str]) -> None:
        """
        Parses a Klipper Input Shaper console message and updates self.is_types.
        """

        if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], str):
            print(
                f"WARNING: Invalid input format. Expected a list with one string. Received: {data}"
            )
            return

        message = data[0]

        pattern_fitted = re.compile(
            r"Fitted shaper '(?P<name>\w+)' frequency = (?P<freq>[\d\.]+) Hz \(vibrations = (?P<vib>[\d\.]+)%"
        )
        match_fitted = pattern_fitted.search(message)

        if match_fitted:
            name = match_fitted.group("name")
            freq = float(match_fitted.group("freq"))
            vib = float(match_fitted.group("vib"))
            current_data = self.is_types.get(name, {})
            current_data.update(
                {
                    "frequency": freq,
                    "vibration": vib,
                    "max_accel": current_data.get("max_accel", 0.0),
                }
            )
            self.is_types[name] = current_data

            return
        pattern_accel = re.compile(
            r"To avoid too much smoothing with '(?P<name>\w+)', suggested max_accel <= (?P<accel>[\d\.]+) mm/sec\^2"
        )
        match_accel = pattern_accel.search(message)

        if match_accel:
            name = match_accel.group("name")
            accel = float(match_accel.group("accel"))

            if name in self.is_types and isinstance(self.is_types[name], dict):
                self.is_types[name]["max_accel"] = accel
            else:
                self.is_types[name] = self.is_types.get(name, {})
                self.is_types[name]["max_accel"] = accel
            return

        pattern_recommended = re.compile(
            r"Recommended shaper_type_(?P<axis>[xy]) = (?P<type>\w+), shaper_freq_(?P=axis) = (?P<freq>[\d\.]+) Hz"
        )
        match_recommended = pattern_recommended.search(message)
        if match_recommended:
            axis = match_recommended.group("axis")
            recommended_type = match_recommended.group("type")
            self.is_types["Axis"] = axis
            if self.aut:
                self.is_aut_types[axis] = recommended_type
                if len(self.is_aut_types) == 2:
                    self.run_gcode_signal.emit("SAVE_CONFIG")
                    self.loadPage.hide()
                    self.aut = False
                    return
                return

            reordered = {recommended_type: self.is_types[recommended_type]}
            for key, value in self.is_types.items():
                if key not in ("suggested_type", recommended_type, "Axis"):
                    reordered[key] = value

            self.is_page.set_type_dictionary(self.is_types)
            first_key = next(iter(reordered.keys()), None)
            for key in reordered.keys():
                if key == first_key:
                    self.is_page.add_type_entry(key, "Recommended type")
                else:
                    self.is_page.add_type_entry(key)

            self.is_page.build_model_list()
            self.loadPage.hide()
            return

    def on_dialog_button_clicked(self, button_name: str) -> None:
        print(button_name)
        """Handle dialog button clicks"""
        if button_name == "Confirm":
            self.handle_is("SHAPER_CALIBRATE AXIS=Y")
        elif button_name == "Cancel":
            self.handle_is("SHAPER_CALIBRATE AXIS=X")

    def handle_is(self, gcode: str) -> None:
        if gcode == "SHAPER_CALIBRATE":
            self.run_gcode_signal.emit("G28\nM400")
            self.aut = True
            self.run_gcode_signal.emit(gcode)
        if gcode == "":
            print("manual Input Shaper Selected")
            self.dialog_page.confirm_background_color("#dfdfdf")
            self.dialog_page.cancel_background_color("#dfdfdf")
            self.dialog_page.cancel_font_color("#000000")
            self.dialog_page.confirm_font_color("#000000")
            self.dialog_page.cancel_button_text("X axis")
            self.dialog_page.confirm_button_text("Y axis")
            self.dialog_page.set_message(
                "Select the axis you want to execute the input shaper on:"
            )
            self.dialog_page.show()
            return
        else:
            self.run_gcode_signal.emit("G28\nM400")
            self.run_gcode_signal.emit(gcode)
            self.change_page(self.indexOf(self.is_page))

        self.loadwidget.set_status_message("Running Input Shaper...")
        self.loadPage.show()

    @QtCore.pyqtSlot(list, name="on_object_list")
    def on_object_list(self, object_list: list) -> None:
        """Handle receiving printer object list"""
        self.cg = object_list
        for obj in self.cg:
            base_name = obj.split()[0]

            # Only accept 'fan_generic' or 'fan'
            if base_name == "fan_generic" or base_name == "fan":
                self.objects["fans"][obj] = "indef"
        self._update_leds_from_config()

    @QtCore.pyqtSlot(dict, name="on_object_config")
    @QtCore.pyqtSlot(list, name="on_object_config")
    def on_object_config(self, config: typing.Union[dict, list]) -> None:
        """Handle receiving printer object configurations"""
        if not config:
            return
        config_items = [config] if isinstance(config, dict) else config
        for item in config_items:
            for key, value in item.items():
                if (
                    key.startswith("stepper_")
                    and isinstance(value, dict)
                    and key not in self.stepper_limits
                ):
                    pos_min = value.get("position_min")
                    pos_max = value.get("position_max")
                    if pos_min is not None or pos_max is not None:
                        self.stepper_limits[key] = {
                            "min": float(pos_min)
                            if pos_min is not None
                            else -float("inf"),
                            "max": float(pos_max)
                            if pos_max is not None
                            else float("inf"),
                        }

    def on_printer_config_received(self, config: dict) -> None:
        """Handle printer configuration"""
        for axis in ("x", "y", "z"):
            self.subscribe_config[str, "PyQt_PyObject"].emit(
                f"stepper_{axis}", self.on_object_config
            )

    @QtCore.pyqtSlot(str, list, name="on_gcode_move_update")
    def on_gcode_move_update(self, name: str, value: list) -> None:
        """Handle gcode move"""
        if not value:
            return
        if name == "gcode_position":
            ...

    def run_routine(self, process: Process):
        """Run check routine for available processes"""
        self.current_process = process
        routine_configs = {
            Process.FAN: ("fans", "fan is spinning"),
            Process.AXIS: ("axis", "axis is moving"),
            Process.BED_HEATER: ("bheat", "bed is heating"),
            Process.EXTRUDER: ("extrude", "extruder is being tested"),
        }
        if process not in routine_configs:
            return
        obj_key, message = routine_configs[process]
        obj_list = list(self.objects.get(obj_key, {}).keys())
        if not self._advance_routine_object(obj_list):
            if self.tb:
                self.troubleshoot_request()
                self.tb = False
            else:
                self.change_page(self.indexOf(self.panel.utilities_page))

            if process == Process.FAN:
                self.run_gcode_signal.emit("M107")
            return

        message = f"Please check if the {self.current_object} is functioning correctly."
        if process == Process.AXIS:
            message = f"Please ensure the {self.current_object} axis moves correctly."
        elif process in [Process.BED_HEATER, Process.EXTRUDER]:
            message = "Please check if the temperature reaches 60°C. \n you may need to wait a few moments."

        self.set_routine_check_page(
            f"Running routine for: {self.current_object}", message
        )
        self.show_waiting_page(
            self.indexOf(self.panel.rc_page),
            f"Please check if the {message}",
            10000 if process == Process.AXIS else 0,
        )
        self._send_routine_gcode()

    def _advance_routine_object(self, obj_list: list) -> bool:
        if not obj_list:
            is_first_run = self.current_object is None
            self.current_object = obj_list[0] if is_first_run and obj_list else "done"
            return is_first_run
        if self.current_object not in obj_list:
            if self.current_process == Process.AXIS:
                self.run_gcode_signal.emit("G28")
            self.current_object = obj_list[0]
            return True
        try:
            current_index = obj_list.index(self.current_object)
            if current_index + 1 < len(obj_list):
                self.current_object = obj_list[current_index + 1]
                return True
            else:
                self.current_object = None
                return False
        except ValueError:
            self.current_object = obj_list[0]
            return True

    def on_routine_answer(self) -> None:
        """Handle routine ongoing process"""
        if self.current_process is None or self.current_object is None:
            return
        if self.sender() == self.panel.rc_yes:
            answer = "yes"
        else:
            answer = "no"
            self.tb = True
        process_map = {
            Process.FAN: ("fans", self.current_object),
            Process.AXIS: ("axis", self.current_object),
            Process.BED_HEATER: ("bheat", "Bed_Heater"),
            Process.EXTRUDER: ("extrude", "extruder"),
        }
        if self.current_process in process_map:
            obj_key, item_key = process_map[self.current_process]
            self.objects[obj_key][item_key] = answer
            if self.current_process in [Process.BED_HEATER, Process.EXTRUDER]:
                self.run_gcode_signal.emit("TURN_OFF_HEATERS")
            self.run_routine(self.current_process)
        elif self.current_process == Process.AXIS_MAINTENANCE:
            if answer == "yes":
                self._run_axis_maintenance_gcode(self.current_object)
            else:
                self.change_page(self.indexOf(self.panel.axes_page))

    def _send_routine_gcode(self):
        """Send the correct G-code for the current process and object."""
        if self.current_process == Process.FAN:
            fan_name = self.current_object or next(iter(self.objects["fans"]), None)
            if fan_name:
                if fan_name == "fan":
                    self.run_gcode_signal.emit("M106 S255\nM400")
                else:
                    self.run_gcode_signal.emit(
                        f"SET_FAN_SPEED FAN={fan_name} SPEED=0.8\nM400"
                    )

            return

        gcode_map = {
            Process.BED_HEATER: "SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=60",
            Process.EXTRUDER: "SET_HEATER_TEMPERATURE HEATER=extruder TARGET=60",
            (Process.AXIS, "x"): "G91\nG1 X50 F700\nG1 X-50 F700",
            (Process.AXIS, "y"): "G91\nG1 Y50 F700\nG1 Y-50 F700",
            (Process.AXIS, "z"): "G91\nG1 Z50 F600\nG1 Z-50 F600",
        }

        key = (
            (self.current_process, self.current_object)
            if self.current_process == Process.AXIS
            else self.current_process
        )

        if gcode := gcode_map.get(key):
            self.run_gcode_signal.emit(f"{gcode}\nM400")

    def set_routine_check_page(self, title: str, label: str):
        """Set text on routine page"""
        self.panel.rc_tittle.setText(title)
        self.panel.rc_label.setText(label)

    def update_led_values(self) -> None:
        """Update led state and color values"""
        if self.current_object not in self.objects["leds"]:
            return
        led_state: LedState = self.objects["leds"][self.current_object]
        led_state.white = int(self.panel.leds_w_slider.value() * 255 / 100)
        self.save_led_state()

    def _update_leds_from_config(self):
        layout = self.panel.leds_content_layout

        while layout.count():
            if (child := layout.takeAt(0)) and child.widget():
                child.widget().deleteLater()  # type: ignore

        led_names = []
        if not self.cg:
            return

        # Collect LED names
        for obj in self.cg:
            if "led" in obj:
                try:
                    name = obj.split()[1]
                    led_names.append(name)
                    self.objects["leds"][name] = LedState(led_type="white")
                except IndexError:
                    pass

        max_columns = 3
        buttons = []  # store references to created buttons

        # Create LED buttons
        for i, name in enumerate(led_names):
            if self.panel.leds_widget:
                button = BlocksCustomButton()
                button.setFixedSize(200, 70)
                button.setText(name)
                button.setProperty("class", "menu_btn")
                button.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/LEDs.svg"))
                row, col = divmod(i, max_columns)
                layout.addWidget(button, row, col)
                button.clicked.connect(partial(self.handle_led_button, name))
                buttons.append(button)

        if len(buttons) == 1:
            self.panel.utilities_leds_btn.clicked.connect(
                partial(self.handle_led_button, led_names[0])
            )
        else:
            self._connect_page_change(
                self.panel.utilities_leds_btn, self.panel.leds_page
            )

    def toggle_led_state(self) -> None:
        """Toggle leds"""
        if self.current_object not in self.objects["leds"]:
            return
        led_state: LedState = self.objects["leds"][self.current_object]
        if led_state.state == "off":
            led_state.state = "on"
            self.panel.toggle_led_button.state = ToggleAnimatedButton.State.ON
        else:
            led_state.state = "off"
            self.panel.toggle_led_button.state = ToggleAnimatedButton.State.OFF
        self.save_led_state()

    def handle_led_button(self, name: str) -> None:
        """Handle led button clicked"""
        self.current_object = name
        led_state: LedState = self.objects["leds"].get(name)
        if not led_state:
            return
        is_rgb = led_state.led_type == "rgb"
        self.panel.leds_w_slider.setVisible(not is_rgb)
        self.panel.leds_w_slider.setValue(led_state.white)
        self.change_page(self.indexOf(self.panel.leds_slider_page))

    def save_led_state(self):
        """Save led state"""
        if self.current_object:
            if self.current_object in self.objects["leds"]:
                led_state: LedState = self.objects["leds"][self.current_object]
                self.run_gcode_signal.emit(led_state.get_gcode(self.current_object))

    def axis_maintenance(self, axis: str) -> None:
        """Routine, checks axis movement for printer debugging"""
        self.current_process = Process.AXIS_MAINTENANCE
        self.current_object = axis
        self.run_gcode_signal.emit(f"G28 {axis.upper()}\nM400")
        self.set_routine_check_page(
            "Axis Maintenance",
            f"Insert oil on the {axis.upper()} axis before confirming.",
        )
        self.show_waiting_page(
            self.indexOf(self.panel.rc_page),
            f"Homing {axis.upper()} axis...",
            5000,
        )

    def _run_axis_maintenance_gcode(self, axis: str):
        stepper_key = f"stepper_{axis}"
        if stepper_key in self.stepper_limits:
            max_pos = self.stepper_limits[stepper_key].get("max", 20)
            distance = int(max_pos) - 20
            self.run_gcode_signal.emit(
                f"G1 {axis.upper()}{distance} F3000\nM400\nG28 {axis.upper()}\nM400"
            )
            self.show_waiting_page(
                self.indexOf(self.panel.axes_page),
                f"Running maintenance cycle on {axis.upper()} axis...",
                5000,
            )
        else:
            self.change_page(self.indexOf(self.panel.axes_page))

    def troubleshoot_request(self) -> None:
        """Show troubleshoot page"""
        self.troubleshoot_page.show()

    def show_waiting_page(self, page_to_go_to: int, label: str, time_ms: int):
        """Show placeholder page"""
        self.loadwidget.set_status_message(label)
        self.loadPage.show()
        QtCore.QTimer.singleShot(time_ms, lambda: self.change_page(page_to_go_to))

    def _connect_page_change(self, button: QtWidgets.QWidget, page: QtWidgets.QWidget):
        if isinstance(button, QtWidgets.QAbstractButton):
            button.clicked.connect(lambda: self.change_page(self.indexOf(page)))

    def change_page(self, index: int):
        """Request change page by index"""
        self.loadPage.hide()
        self.troubleshoot_page.hide()
        if index < self.count():
            self.request_change_page.emit(3, index)

    @QtCore.pyqtSlot(name="request-back")
    def back_button(self) -> None:
        """Request back"""
        self.request_back.emit()
