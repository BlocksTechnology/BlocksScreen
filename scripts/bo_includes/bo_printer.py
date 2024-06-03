from __future__ import annotations
import timeit
import sys
import re
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication
import typing

from scripts.moonrakerComm import MoonWebSocket
from scripts.events import *
from scripts import events
import logging

_logger = logging.getLogger(__name__)


class Printer(QObject):
    # TODO: Handle subscriptions and information received by subscriptions
    # TODO: Handle configfile information -> Create a structure where i can save the config file internally
    # TODO: Create variables that store information about specific printer objects like extruder, temperature etc..
    # @ Signals
    extruder_number: int = 0
    request_available_objects_signal = pyqtSignal(name="get_available_objects")
    request_object_subscription_signal = pyqtSignal(dict, name="object_subscription")
    extruder_number_received_signal = pyqtSignal(int, name="extruder_number_received")

    extruder_update_signal = pyqtSignal(str, str, float, name="extruder_update")
    heater_bed_update_signal = pyqtSignal(str, str, float, name="heater_bed_update")
    fan_update_signal = pyqtSignal(
        [str, str, float], [str, str, int], name="fan_update"
    )
    chamber_update_signal = pyqtSignal()

    # idle_timeout_update_signal = pyqtSignal(str,[float], [str], name="idle_timeout_update")
    idle_timeout_update_signal = pyqtSignal(
        [str, float], [str, str], name="idle_timeout_update"
    )

    gcode_move_update_signal = pyqtSignal(
        [str, list], [str, float], [str, bool], name="gcode_move_update"
    )
    toolhead_update_signal = pyqtSignal(
        [str, float], [str, list], [str, str], name="toolhead_update"
    )
    virtual_sdcard_update_signal = pyqtSignal(
        [str, float], [str, bool], name="virtual_sdcard_update"
    )
    print_stats_update_signal = pyqtSignal(
        [str, dict], [str, float], [str, str], name="print_stats_update"
    )
    display_update_signal = pyqtSignal([str, str], [str, float], name="display_update")
    temperature_sensor_update_signal = pyqtSignal(
        str, str, float, name="temperature_sensor_update"
    )
    temperature_fan_update_signal = pyqtSignal(
        str, str, float, name="temperature_fan_update"
    )
    filament_switch_sensor_update_signal = pyqtSignal(
        str, str, bool, name="filament_switch_sensor_update"
    )
    output_pin_update_signal = pyqtSignal(str, str, float, name="output_pin_update")
    bed_mesh_update_signal = pyqtSignal(
        str, list, list, list, list, name="bed_mesh_updated"
    )
    gcode_macro_update_signal = pyqtSignal(str, dict, name="gcode_macro_update")

    printer_webhooks_updated_signal = pyqtSignal(str, str, name="webhooks_update")

    
    query_printer_object = pyqtSignal(dict, name="query_object")

    def __init__(self, parent: typing.Optional["QObject"], ws: MoonWebSocket) -> None:
        super(Printer, self).__init__(parent)
        self.main_window = parent
        self.ws = ws

        self.available_objects: dict = {}
        self.active_extruder_name: str = ""
        self.printer_state_webhook: str = ""
        self.printer_message_webhook: str = ""
        self._last_eventTime: float = 0.0
        self.printer_objects: dict = {}

        self.printing: bool = False
        self.print_file_loaded: bool = False
        self.printing_state: str = ""
        self.printing_error_message: str | None = None
        self.printer_busy: bool = False
        self.current_loaded_file: str = ""
        self.current_loaded_file_metadata: str = ""

        self.has_chamber : bool = False
        
        # @ Signal/Slot Connections
        self.ws.klippy_state_signal.connect(self.klippy_ready_report)
        
        self.request_available_objects_signal.connect(self.ws.api.get_available_objects)
        self.request_object_subscription_signal.connect(self.ws.api.object_subscription)
        self.query_printer_object.connect(self.ws.api.object_query)    

    @pyqtSlot(str, name="klippy_ready_report")
    def klippy_ready_report(self, state: str):
        if state == "ready":
            self.request_available_objects_signal.emit()
            
            # * Query some objects to determine the printer state 
            _query_request: dict = {
                "idle_timeout": None, 
                "print_stats": None,
                "virtual_sdcard": None
            }    
            self.query_printer_object.emit(_query_request)

    @pyqtSlot(list, name="object_list_received")
    def object_list_received(self, object_list: list):
        [self.available_objects.update({obj: None}) for obj in object_list]
        self.request_object_subscription_signal[dict].emit(self.available_objects)
        # * Find how many extruders the printer has
        _extruder_regex = re.compile(r"^extruder{1}?\d?")
        # _object_list: list = list(self.printer_objects.keys())
        _find = list(filter(_extruder_regex.match, object_list))
        self.extruder_number = len(_find)
        # print(object_list)

    @pyqtSlot(list, name="object_report_received")
    def report_received(self, report: list) -> None:
        if report is None or len(report) <= 1:
            return None
        _report_length = len(report) - 1
        if isinstance(report[0], dict):
            _objects_updated_dict: dict = report[0]
        _objects_updated_names = list(report[0])
        self._last_eventTime = report[_report_length]
        self.printer_objects.update(dict(report[0]))
        # * Calls callbacks for each object that was updated
        list(
            map(
                lambda n: self.check_callback_method(n, _objects_updated_dict[n]),
                _objects_updated_names,
            )
        )

    @pyqtSlot(list, name="gcode_reponse_report_received")
    def gcode_response_report(self, report: list) -> None:
        # TODO: Handle reports coming from subscribed websocket object
        # if not isinstance(report):
        _split_information = report[0].split("// ")

        # print(_split_information)
    
    ###*# Callback Related #*###
    # TODO : Names for the objects must be passed, ex:. "extruder", "extruder1"
    # TODO: Extruder name, right now is different, but i want to use the same method for all extruders.
    def check_callback_method(self, name: str, values: dict):
        # * Split the name argument if the string is "<object type> <object name>"
        # ! This can be better implemented
        _split: list = name.split(" ")
        if len(_split) > 1:
            object_type = _split[0]
            object_name = _split[1]
        else:
            object_type = name
            object_name = ""
        if name.startswith("extruder"):
            object_type = "extruder"
            object_name = name

        # * Checks if there is a callback with the object name, calls it, passes the updated fields
        if hasattr(self, f"{object_type}_object_updated"):
            _callback = getattr(self, f"{object_type}_object_updated")
            if callable(_callback):
                _callback(values, object_name)
                return True
        return False

    #####*## Callbacks for the objects ##*#####
    def webhooks_object_updated(self, value: dict, name: str = "") -> None:
        """webhooks_object_updated Sends an event type according to the state received from
                webhooks subscribed object

        Args:
            value (dict): _description_
            name (str, optional): _description_. Defaults to "".
        """
        if "state" in value.keys() and "state_message" in value.keys():
            _logger.debug("Webhooks message received")
            _state: str = value["state"]
            _state_upper = _state[0].upper()
            _state_call = f"{_state_upper}{_state[1:]}"
            if hasattr(events, f"Klippy{_state_call}Event"):
                _event_callback = getattr(events, f"Klippy{_state_call}Event")
                if callable(_event_callback):
                    try:
                        event = _event_callback(value["state"], value["state_message"])
                        instance = QApplication.instance()
                        if instance is not None:
                            instance.sendEvent(self.main_window, event)
                        else:
                            raise Exception("QApplication.instance is None type.")
                    except Exception as e:
                        _logger.debug(
                            f"Unable to send internal Klippy {_state_call} notification : {e}"
                        )

    def gcode_move_object_updated(self, value: dict, name: str = "") -> None:
        if "speed_factor" in value.keys():
            self.gcode_move_update_signal[str, float].emit(
                "speed_factor", value["speed_factor"]
            )
        if "speed" in value.keys():
            self.gcode_move_update_signal[str, float].emit("speed", value["speed"])
        if "extrude_factor" in value.keys():
            self.gcode_move_update_signal[str, float].emit(
                "extruder_factor", value["extrude_factor"]
            )
        if "absolute_coordinates" in value.keys():
            self.gcode_move_update_signal[str, bool].emit(
                "absolute_coordinates", value["absolute_coordinates"]
            )
        if "absolute_extrude" in value.keys():
            self.gcode_move_update_signal[str, bool].emit(
                "absolute_extrude", value["absolute_extrude"]
            )
        if "homing_origin" in value.keys():
            self.gcode_move_update_signal[str, list].emit(
                "homing_origin", value["homing_origin"]
            )
        if "position" in value.keys():
            self.gcode_move_update_signal[str, list].emit("position", value["position"])
        if "gcode_position" in value.keys():
            self.gcode_move_update_signal[str, list].emit(
                "gcode_position", value["gcode_position"]
            )

    def toolhead_object_updated(self, values: dict, name: str = "") -> None:
        if "homed_axes" in values.keys():
            self.toolhead_update_signal[str, str].emit(
                "homed_axes", values["homed_axes"]
            )
        if "print_time" in values.keys():
            self.toolhead_update_signal[str, float].emit(
                "print_time", values["print_time"]
            )
        if "estimated_print_time" in values.keys():
            self.toolhead_update_signal[str, float].emit(
                "estimated_print_time", values["estimated_print_time"]
            )
        if "extruder" in values.keys():
            self.toolhead_update_signal[str, str].emit("extruder", values["extruder"])
            self.active_extruder_name = values["extruder"]
        if "position" in values.keys():
            self.toolhead_update_signal[str, list].emit("position", values["position"])
        if "max_velocity" in values.keys():
            self.toolhead_update_signal[str, float].emit(
                "max_velocity", values["max_velocity"]
            )
        if "max_accel" in values.keys():
            self.toolhead_update_signal[str, float].emit(
                "max_accel", values["max_accel"]
            )
        if "max_accel_to_decel" in values.keys():
            self.toolhead_update_signal[str, float].emit(
                "max_accel_to_decel", values["max_accel_to_decel"]
            )
        if "square_corner_velocity" in values.keys():
            self.toolhead_update_signal[str, float].emit(
                "square_corner_velocity", values["square_corner_velocity"]
            )

    def extruder_object_updated(
        self, value: dict, extruder_name: str = "extruder"
    ) -> None:
        if "temperature" in value.keys():
            self.extruder_update_signal.emit(
                extruder_name, "temperature", value["temperature"]
            )
        if "target" in value.keys():
            self.extruder_update_signal.emit(extruder_name, "target", value["target"])
        if "power" in value.keys():
            self.extruder_update_signal.emit(extruder_name, "power", value["power"])
        if "pressure_advance" in value.keys():
            self.extruder_update_signal.emit(
                extruder_name, "pressure_advance", value["pressure_advance"]
            )
        if "smooth_time" in value.keys():
            self.extruder_update_signal.emit(
                extruder_name, "smooth_time", value["smooth_time"]
            )
        if "can_extrude" in value.keys():
            # TODO: Emit a signal that means that the extruder can extrude
            pass

    def heater_bed_object_updated(
        self, value: dict, heater_name: str = "heater_bed"
    ) -> None:
        if "temperature" in value.keys():
            self.heater_bed_update_signal.emit(
                heater_name, "temperature", value["temperature"]
            )
        if "target" in value.keys():
            self.heater_bed_update_signal.emit(heater_name, "target", value["target"])
        if "power" in value.keys():
            self.heater_bed_update_signal.emit(heater_name, "power", value["power"])

    def chamber_object_updated(self, value:dict, heater_name:str = "chamber"):
        # TODO: this needs to be completed 
        self.has_chamber = True
        
    def fan_object_updated(self, value: dict, fan_name: str = "fan") -> None:
        if "speed" in value.keys():
            self.fan_update_signal[str, str, float].emit(
                fan_name, "speed", value["speed"]
            )
        if "rpm" in value.keys():
            self.fan_update_signal[str, str, int].emit(fan_name, "rpm", value["rpm"])

    def idle_timeout_object_updated(self, value: dict, name: str = "") -> None:
        if "state" in value.keys():
            self.idle_timeout_update_signal[str, str].emit("state", value["state"])
            if "printing" in value["state"]:

                self.printer_busy = True
            elif self.printing_state != "printing" and value["state"] != "printing": 
                # It's also busy if the printer is printing or paused 
                self.printer_busy = False
        if "printing_time" in value.keys():
            self.idle_timeout_update_signal[str, float].emit(
                "printing_time", value["printing_time"]
            )

    def virtual_sdcard_object_updated(self, values: dict, name: str = "") -> None:
        if "progress" in values.keys():
            self.virtual_sdcard_update_signal[str, float].emit(
                "progress", values["progress"]
            )
        if "is_active" in values.keys():
            self.virtual_sdcard_update_signal[str, bool].emit(
                "is_active", values["is_active"]
            )
        if "file_position" in values.keys():
            self.virtual_sdcard_update_signal[str, float].emit(
                "file_position", float(values["file_position"])
            )

    def print_stats_object_updated(self, values: dict, name: str = "") -> None:
        try:
            if "filename" in values.keys():
                self.print_stats_update_signal[str, str].emit(
                    "filename", values["filename"]
                )
                self.print_file_loaded = True
            if "total_duration" in values.keys():
                self.print_stats_update_signal[str, float].emit(
                    "total_duration", values["total_duration"]
                )
            if "print_duration" in values.keys():
                self.print_stats_update_signal[str, float].emit(
                    "print_duration", values["print_duration"]
                )
            if "filament_used" in values.keys():
                self.print_stats_update_signal[str, float].emit(
                    "filament_used", values["filament_used"]
                )
            if "state" in values.keys():
                self.print_stats_update_signal[str, str].emit("state", values["state"])
                self.printing_state = values["state"]
                if values["state"] == "standby" or values["state"] == "error":
                    self.print_file_loaded = False
                    self.printing = False
                else: 
                    self.print_file_loaded = True 
                    if values['state'] == "printing" or values['state'] == 'pause': 
                        self.printing = True

            if "message" in values.keys():
                self.print_stats_update_signal[str, str].emit("message", values["message"])
                self.printing_error_message = values["message"]
            if "info" in values.keys():
                self.print_stats_update_signal[str, dict].emit("info", values["info"])
            return
        except Exception as e: 
            _logger.debug(f"Error sending print stats update {e}")

    def display_status_object_updated(self, values: dict, name: str = "") -> None:
        if "message" in values.keys():
            self.display_update_signal[str, str].emit("message", values["message"])
        if "progress" in values.keys():
            self.display_update_signal[str, float].emit("progress", values["progress"])

    def temperature_sensor_object_updated(
        self, values: dict, temperature_sensor_name: str
    ) -> None:
        if "temperature" in values.keys():
            self.temperature_sensor_update_signal.emit(
                temperature_sensor_name, "temperature", values["temperature"]
            )
        if "measured_min_temp" in values.keys():
            self.temperature_sensor_update_signal.emit(
                temperature_sensor_name,
                "measured_min_temp",
                values["measured_min_temp"],
            )
        if "measured_max_temp" in values.keys():
            self.temperature_sensor_update_signal.emit(
                temperature_sensor_name,
                "measured_max_temp",
                values["measured_max_temp"],
            )

    def temperature_fan_object_updated(
        self, values: dict, temperature_fan_name: str
    ) -> None:
        if "speed" in values.keys():
            self.temperature_fan_update_signal.emit(
                temperature_fan_name, "speed", values["speed"]
            )
        if "temperature" in values.keys():
            self.temperature_fan_update_signal.emit(
                temperature_fan_name, "temperature", values["temperature"]
            )
        if "target" in values.keys():
            self.temperature_fan_update_signal.emit(
                temperature_fan_name, "target", values["target"]
            )

    def filament_switch_sensor_object_updated(
        self, values: dict, filament_switch_name: str
    ) -> None:
        if "filament_detected" in values.keys():
            self.filament_switch_sensor_update_signal.emit(
                filament_switch_name, "filament_detected", values["filament_detected"]
            )
        if "enabled" in values.keys():
            self.filament_switch_sensor_update_signal.emit(
                filament_switch_name, "enabled", values["enabled"]
            )

    def output_pin_object_updated(self, values: dict, output_pin_name: str) -> None:
        if "value" in values.keys():
            self.output_pin_update_signal.emit(
                output_pin_name, "value", values["value"]
            )

    def bed_mesh_object_updated(self, values: dict, name: str) -> None:
        # * Handle the bed mesh received from the printer here
        pass
        # bed_mesh_names = [
        #     "profile_name",
        #     "mesh_min",
        #     "mesh_max",
        #     "probed_matrix",
        #     "mesh_matrix",
        # ]
        # if bed_mesh_names in values.keys():
        #     self.bed_mesh_update_signal.emit(
        #         values["profile_name"],
        #         values["mesh_min"],
        #         values["mesh_max"],
        #         values["probed_matrix"],
        #         values["mesh_matrix"],
        #     )

    def gcode_macro_object_updated(self, values: dict, gcode_macro_name: str) -> None:
        # * values argument can come with many different types for this macro so handle them in another place
        self.gcode_macro_update_signal.emit(gcode_macro_name, values)
        pass

    def configfile_object_updated(self, values: dict, name: str) -> None:
        # * Handle the printer config file here
        pass
