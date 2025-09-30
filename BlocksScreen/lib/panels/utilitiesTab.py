import csv
import typing
from dataclasses import dataclass
from enum import Enum, auto
from functools import partial

from lib.moonrakerComm import MoonWebSocket
from lib.panels.widgets.loadPage import LoadScreen
from lib.panels.widgets.troubleshootPage import TroubleshootPage
from lib.printer import Printer
from lib.panels.widgets.updatePage import UpdatePage


from lib.ui.utilitiesStackedWidget_ui import Ui_utilitiesStackedWidget

from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.toggleAnimatedButton import ToggleAnimatedButton
from PyQt6 import QtCore, QtGui, QtWidgets


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
        self.ammount: int = 1
        self.tb: bool = False

        # --- UI Setup ---
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.loadPage = LoadScreen(self)
        self.addWidget(self.loadPage)

        self.update_page = UpdatePage(self)
        self.addWidget(self.update_page)

        # --- Back Buttons ---
        for button in (
            self.panel.is_back_btn,
            self.panel.leds_back_btn,
            self.panel.info_back_btn,
            self.panel.leds_slider_back_btn,
            self.panel.input_shaper_back_btn,
            self.panel.routine_check_back_btn,
            self.update_page.update_back_btn,
        ):
            button.clicked.connect(self.back_button)

        # --- Page Navigation ---
        self._connect_page_change(self.panel.utilities_axes_btn, self.panel.axes_page)
        self._connect_page_change(self.panel.update_btn, self.update_page)
        self._connect_page_change(
            self.panel.utilities_input_shaper_btn, self.panel.input_shaper_page
        )
        self._connect_page_change(self.panel.utilities_info_btn, self.panel.info_page)
        self._connect_page_change(self.panel.utilities_leds_btn, self.panel.leds_page)
        self._connect_page_change(
            self.panel.utilities_routine_check_btn, self.panel.routines_page
        )
        self._connect_page_change(self.panel.is_confirm_btn, self.panel.utilities_page)
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

        # --- Input Shaper ---
        self.panel.is_X_startis_btn.clicked.connect(
            partial(self.run_resonance_test, "x")
        )
        self.panel.is_Y_startis_btn.clicked.connect(
            partial(self.run_resonance_test, "y")
        )
        self.panel.am_confirm.clicked.connect(self.apply_input_shaper_selection)
        self.panel.isc_btn_group.buttonClicked.connect(
            lambda btn: setattr(self, "ammount", int(btn.text()))
        )
        self._connect_numpad_request(self.panel.isui_fq, "frequency", "Frequency")
        self._connect_numpad_request(self.panel.isui_sm, "smoothing", "Smoothing")

        self.panel.toggle_led_button.state = ToggleAnimatedButton.State.ON

        # --- LEDs ---
        self.panel.leds_r_slider.sliderReleased.connect(self.update_led_values)
        self.panel.leds_g_slider.sliderReleased.connect(self.update_led_values)
        self.panel.leds_b_slider.sliderReleased.connect(self.update_led_values)
        self.panel.leds_w_slider.sliderReleased.connect(self.update_led_values)
        self.panel.toggle_led_button.clicked.connect(self.toggle_led_state)

        # --- Websocket/Printer Signals ---
        self.run_gcode_signal.connect(self.ws.api.run_gcode)
        self.subscribe_config[str, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )
        self.subscribe_config[list, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )

        # --- Initialize Printer Communication ---
        self.printer.printer_config.connect(self.on_printer_config_received)
        self.printer.gcode_move_update.connect(self.on_gcode_move_update)

        # ---- Websocket connections ----
        self.update_page.request_full_update.connect(self.ws.api.full_update)
        self.update_page.request_recover_repo.connect(self.ws.api.recover_corrupt_repo)
        self.update_page.request_refresh_update.connect(
            self.ws.api.refresh_update_status
        )
        self.update_page.request_rollback_update.connect(self.ws.api.rollback_update)
        self.update_page.request_update_client.connect(self.ws.api.update_client)
        self.update_page.request_update_klipper.connect(self.ws.api.update_klipper)
        self.update_page.request_update_moonraker.connect(self.ws.api.update_moonraker)
        self.update_page.request_update_status.connect(self.ws.api.update_status)
        self.update_page.request_update_system.connect(self.ws.api.update_system)

    @QtCore.pyqtSlot(list, name="on_object_list")
    def on_object_list(self, object_list: list) -> None:
        self.cg = object_list
        for obj in self.cg:
            if "fan" in obj and "pin" not in obj and "controller" not in obj:
                self.objects["fans"][obj] = "indf"
        self._update_leds_from_config()

    @QtCore.pyqtSlot(dict, name="on_object_config")
    @QtCore.pyqtSlot(list, name="on_object_config")
    def on_object_config(self, config: typing.Union[dict, list]) -> None:
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
        for axis in ("x", "y", "z"):
            self.subscribe_config[str, "PyQt_PyObject"].emit(
                f"stepper_{axis}", self.on_object_config
            )

    @QtCore.pyqtSlot(str, list, name="on_gcode_move_update")
    def on_gcode_move_update(self, name: str, value: list) -> None:
        if not value:
            return
        if name == "gcode_position":
            self.position = value

    def _connect_numpad_request(self, button: QtWidgets.QWidget, name: str, title: str):
        if isinstance(button, QtWidgets.QPushButton):
            button.clicked.connect(
                lambda: self.request_numpad_signal.emit(
                    3, name, title, self.handle_numpad_change, self
                )
            )

    def handle_numpad_change(self, name: str, new_value: typing.Union[int, float]):
        if name == "frequency":
            self.panel.isui_fq.setText(f"Frequency: {new_value} Hz")
        elif name == "smoothing":
            self.panel.isui_sm.setText(f"Smoothing: {new_value}")

    def run_routine(self, process: Process):
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
        self.set_routine_check_page(f"Running routine for: {self.current_object}", "")
        self.show_waiting_page(
            self.indexOf(self.panel.rc_page),
            f"Please check if the {message}",
            5 if process in [Process.FAN, Process.AXIS] else 5,
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
        gcode_map = {
            Process.FAN: "M106 S80",
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
            # self.run_gcode_signal.emit(f"{gcode}\nM400")
            return

    def set_routine_check_page(self, title: str, label: str):
        self.panel.rc_tittle.setText(title)
        self.panel.rc_label.setText(label)

    def update_led_values(self) -> None:
        if self.current_object not in self.objects["leds"]:
            return
        led_state: LedState = self.objects["leds"][self.current_object]
        led_state.red = self.panel.leds_r_slider.value()
        led_state.green = self.panel.leds_g_slider.value()
        led_state.blue = self.panel.leds_b_slider.value()
        led_state.white = self.panel.leds_w_slider.value()
        self.save_led_state()

    def _update_leds_from_config(self):
        layout = self.panel.leds_content_layout
        while layout.count():
            if (child := layout.takeAt(0)) and child.widget():
                child.widget().deleteLater()
        led_names = []
        for obj in self.cg:
            if "led" in obj:
                try:
                    name = obj.split()[1]
                    led_names.append(name)
                    self.objects["leds"][name] = LedState(led_type="white")
                except IndexError:
                    ...
        max_columns = 3
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

    def toggle_led_state(self) -> None:
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
        self.current_object = name
        led_state: LedState = self.objects["leds"].get(name)
        if not led_state:
            return
        is_rgb = led_state.led_type == "rgb"
        self.panel.leds_r_slider.setVisible(is_rgb)
        self.panel.leds_g_slider.setVisible(is_rgb)
        self.panel.leds_b_slider.setVisible(is_rgb)
        self.panel.leds_w_slider.setVisible(not is_rgb)
        self.panel.leds_slider_title_label.setText(name)
        self.panel.leds_r_slider.setValue(led_state.red)
        self.panel.leds_g_slider.setValue(led_state.green)
        self.panel.leds_b_slider.setValue(led_state.blue)
        self.panel.leds_w_slider.setValue(led_state.white)
        self.change_page(self.indexOf(self.panel.leds_slider_page))

    def save_led_state(self):
        if self.current_object:
            if self.current_object in self.objects["leds"]:
                led_state: LedState = self.objects["leds"][self.current_object]
                self.run_gcode_signal.emit(led_state.get_gcode(self.current_object))

    # input shapper
    def run_resonance_test(self, axis: str) -> None:
        self.axis_in = axis
        path_map = {
            "x": "/tmp/resonances_x_axis_data.csv",
            "y": "/tmp/resonances_y_axis_data.csv",
        }
        if not (csv_path := path_map.get(axis)):
            return
        self.run_gcode_signal.emit(f"SHAPER_CALIBRATE AXIS={axis.upper()}")
        self.data = self._parse_shaper_csv(csv_path)
        for entry in self.data:
            shaper = entry["shaper"]
            panel_attr = f"am_{shaper}"
            if hasattr(self.panel, panel_attr):
                text = (
                    f"Shaper: {shaper}, Freq: {entry['frequency']}Hz, Vibrations: {entry['vibrations']}%\n"
                    f"Smoothing: {entry['smoothing']}, Max Accel: {entry['max_accel']}mm/sec"
                )
                getattr(self.panel, panel_attr).setText(text)
                self.x_inputshaper[panel_attr] = entry
        self.change_page(self.indexOf(self.panel.is_page))

    def _parse_shaper_csv(self, file_path: str) -> list:
        results = []
        try:
            with open(file_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row.get("shaper") and row.get("freq"):
                        results.append(
                            {
                                k: row.get(v, "N/A")
                                for k, v in {
                                    "shaper": "shaper",
                                    "frequency": "freq",
                                    "vibrations": "vibrations",
                                    "smoothing": "smoothing",
                                    "max_accel": "max_accel",
                                }.items()
                            }
                        )
        except FileNotFoundError:
            ...
        except csv.Error as e:
            ...
        return results

    def apply_input_shaper_selection(self) -> None:
        if not (checked_button := self.panel.is_btn_group.checkedButton()):
            return
        selected_name = checked_button.objectName()
        if selected_name == "am_user_input":
            self.change_page(
                self.indexOf(self.panel.input_shaper_page)
            )  # TEST: CHANGED THIS FROM input_shaper_user_input
            return
        if not (shaper_data := self.x_inputshaper.get(selected_name)):
            return
        gcode = (
            f"SET_INPUT_SHAPER SHAPER_TYPE={shaper_data['shaper']} "
            f"SHAPER_FREQ_{self.axis_in.upper()}={shaper_data['frequency']} "
            f"SHAPER_DAMPING_{self.axis_in.upper()}={shaper_data['smoothing']}"
        )
        self.run_gcode_signal.emit(gcode)
        self.change_page(self.indexOf(self.panel.utilities_page))

    def axis_maintenance(self, axis: str) -> None:
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
        self.troubleshoot_page.geometry_calc()
        self.troubleshoot_page.show()

    def show_waiting_page(self, page_to_go_to: int, label: str, time_ms: int):
        self.loadPage.label.setText(label)
        self.loadPage.show()
        QtCore.QTimer.singleShot(time_ms, lambda: self.change_page(page_to_go_to))

    def _connect_page_change(self, button: QtWidgets.QWidget, page: QtWidgets.QWidget):
        if isinstance(button, QtWidgets.QPushButton):
            button.clicked.connect(lambda: self.change_page(self.indexOf(page)))

    def change_page(self, index: int):
        self.loadPage.hide()
        self.troubleshoot_page.hide()
        if index < self.count():
            self.request_change_page.emit(3, index)

    @QtCore.pyqtSlot(name="request-back")
    def back_button(self) -> None:
        self.request_back.emit()
