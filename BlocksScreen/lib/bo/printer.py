from __future__ import annotations

import enum
import logging
from re import I
import typing

import events
import PyQt6
import PyQt6.QtCore
from lib.moonrakerComm import MoonWebSocket
from PyQt6.QtCore import QEvent, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication

_logger = logging.getLogger(name="logs/BlocksScreen.logs")


class PrinterState(enum.Enum):
    PRINTING = enum.auto()
    IDLE = enum.auto()
    ERROR = enum.auto()


class PrintStatsStates(enum.Enum):
    STANDBY = enum.auto()
    PRINTING = enum.auto()
    PAUSED = enum.auto()
    COMPLETE = enum.auto()
    ERROR = enum.auto()
    CANCELLED = enum.auto()


class IdleTimeoutStates(enum.StrEnum):
    """
    Idle timeout state field should not be used to determine if klipper is "printing" a file
    as the state will report printing when executing manual commands
    Args:
        enum (_type_): _description_
    """

    PRINTING = "Printing"
    READY = "Ready"
    IDLE = "Idle"


class Printer(QObject):
    # @ Signals
    extruder_number: int = 0
    request_available_objects_signal = pyqtSignal(name="get_available_objects")
    request_object_subscription_signal = pyqtSignal(
        dict, name="object_subscription"
    )
    on_toolhead_number_signal = pyqtSignal(
        int, name="toolhead_number_received"
    )

    on_available_objects = pyqtSignal(name="on_available_objects")

    on_extruder_update = pyqtSignal(str, str, float, name="on_extruder_update")
    on_heater_bed_update = pyqtSignal(
        str, str, float, name="on_heater_bed_update"
    )
    on_fan_update = pyqtSignal(
        [str, str, float], [str, str, int], name="on_fan_update"
    )
    on_chamber_update = pyqtSignal(name="on_chamber_update")

    on_idle_timeout_update = pyqtSignal(
        [str, float], [str, str], name="on_idle_timeout_update"
    )

    on_gcode_move_update = pyqtSignal(
        [str, list], [str, float], [str, bool], name="on_gcode_move_update"
    )
    on_toolhead_update = pyqtSignal(
        [str, float], [str, list], [str, str], name="on_toolhead_update"
    )
    on_virtual_sdcard_update = pyqtSignal(
        [str, float], [str, bool], name="on_virtual_sdcard_update"
    )
    on_print_stats_update = pyqtSignal(
        [str, dict], [str, float], [str, str], name="on_print_stats_update"
    )
    on_display_update = pyqtSignal(
        [str, str], [str, float], name="on_display_update"
    )
    on_temperature_sensor_update = pyqtSignal(
        str, str, float, name="on_temperature_sensor_update"
    )
    on_temperature_fan_update = pyqtSignal(
        str, str, float, name="on_temperature_fan_update"
    )
    on_filament_switch_sensor_update = pyqtSignal(
        str, str, bool, name="on_filament_switch_sensor_update"
    )
    on_filament_motion_sensor_update = pyqtSignal(
        str, str, bool, name="on_filament_motion_sensor_update"
    )
    on_output_pin_update = pyqtSignal(
        str, str, float, name="on_output_pin_update"
    )
    on_bed_mesh_update = pyqtSignal(
        str, list, list, list, list, name="on_bed_mesh_update"
    )
    on_gcode_macro_update = pyqtSignal(str, dict, name="on_gcode_macro_update")
    on_webhooks_update = pyqtSignal(str, str, name="on_webhooks_update")
    on_query_printer_object = pyqtSignal(dict, name="on_query_printer_object")
    on_save_config_pending: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = (
        pyqtSignal(name="save_config_pending")
    )
    on_printer_config: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = pyqtSignal(
        dict, name="on_printer_config"
    )

    on_configfile_update: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = (
        pyqtSignal(dict, name="on_configfile_update")
    )

    on_object_config: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = pyqtSignal(
        [list, list], [str, dict], name="on_object_config"
    )

    on_config_subscription: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = (
        pyqtSignal(
            [dict],
            [list],
            name="on_config_subscription",
        )
    )

    on_available_gcode_cmds: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = (
        pyqtSignal(dict, name="on_available_gcode_cmds")
    )
    on_gcode_response: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = pyqtSignal(
        list, name="on_gcode_response"
    )
    available_gcode_commands: dict = {}
    available_objects: dict = {}
    configfile: dict = {}
    printing: bool = False
    printing_state: str = ""
    print_file_loaded: bool = False
    printer_busy: bool = False
    current_loaded_file: str = ""
    current_loaded_file_metadata: str = ""

    def __init__(self, parent: QObject, ws: MoonWebSocket, /) -> None:
        super(Printer, self).__init__(parent)

        self.ws = ws
        self.active_extruder_name: str = ""
        self.printer_state_webhook: str = ""
        self.printer_message_webhook: str = ""
        self._last_eventTime: float = 0.0
        self.printer_objects: dict = {}

        self.printing_error_message: str | None = None

        self.available_filament_sensors: dict = {}
        heater_attributes: dict = {
            "current_temperature": 0.0,
            "target_temperature": 0.0,
            "can_extrude": False,
        }

        self.heaters_object: dict = {
            "extruder": heater_attributes.copy(),
            "extruder1": heater_attributes.copy(),
            "bed": heater_attributes.copy(),
        }

        self.has_chamber: bool = False

        # @ Signal/Slot Connections
        self.ws.klippy_state_signal.connect(self.on_klippy_ready)
        self.request_available_objects_signal.connect(
            self.ws.api.get_available_objects
        )
        self.request_object_subscription_signal.connect(
            self.ws.api.object_subscription
        )
        self.on_query_printer_object.connect(self.ws.api.object_query)

        # Distribute printer config objects
        # self.on_configfile_update.connect(self.on_unified_config_distribution)
        # self.on_configfile_update.connect(self.on_config_distribution)

    @pyqtSlot(str, name="on_klippy_ready")
    def on_klippy_ready(self, state: str):
        if state.lower() == "ready" or state == "printing":
            self.request_available_objects_signal.emit()  # request available objects
            _query_request: dict = {
                "idle_timeout": None,
                "print_stats": None,
                "virtual_sdcard": None,
            }
            self.on_query_printer_object.emit(_query_request)

    @pyqtSlot(list, name="on_object_list")
    def on_object_list(self, object_list: list):
        [self.available_objects.update({obj: None}) for obj in object_list]
        self.request_object_subscription_signal[dict].emit(
            self.available_objects
        )  # subscribe to all available printer objects

        # Find how many extruders exist
        # _extruder_regex = re.compile(r"^extruder{1}?\d?")
        # _find = list(filter(_extruder_regex.match, object_list))
        # self.extruder_number = len(_find)
        # self.on_toolhead_number_signal.emit(self.extruder_number)

    def has_config_keyword(self, section: str) -> bool:
        """Check if a section exists on the printers available object configurations
            Does not accept prefixes

        Args:
            section (str): Name of the section to check its existence

        Returns:
            bool: Whether or not a configuration exists for the specified section
        """
        if not section:
            return False
        _printer_config = self.configfile.get("config")
        if not _printer_config:
            return False
        return section in _printer_config

    def fetch_config_by_keyword(self, section: str) -> list:
        """Retrieve a section or sections from the printers configfile
        with prefix or with full section name

        Args:
            section (str): Name of the section
            name (str, optional): Name of the section object. Defaults to "".

        Returns:
            list: The entire section with the section as key or None if
                            nothing is found
        """
        if not self.configfile or not section:
            return []
        _printer_config = self.configfile.get("config")
        if not _printer_config:
            return []
        return [
            {key: _printer_config.get(key)}  # Used get to get the default None
            for key in _printer_config
            if key.startswith(str(section + " "))
            or key
            == section  # O(s) time per key, the space is for delimiting the prefix
        ]
        # Iterates over every key and checks if it starts
        # with the prefix -> Complexity O(n*s)
        # Simple but becomes costly for large n values
        # since the dictionary is not exactly big, it should be ok

    def get_config(self, section_name: str) -> dict:
        """Gets a printer config section, does not accept prefixes

        Args:
            section_name (str): Name of the printer object

        Returns:
            dict: The config dictionary of the printer object
        """
        if not section_name:
            return {}
        if not self.has_config_keyword(section_name):
            return {}
        _config = self.fetch_config_by_keyword(section_name)
        return _config[0].get(section_name)

    def search_config_list(
        self, search_list: list[str], _objects: list = []
    ) -> list:
        """
        Search a list of printer objects recursively

        Args:
                search_list (list): A list of objects to search for.
                _objects (list, optional): Internal list, should not be directly set or modified.
        ---

        Returns:
            list: A list containing the found objects with their configuration
        """
        if len(search_list) == 0:
            return _objects
        _objects.extend(self.fetch_config_by_keyword(search_list.pop()))
        return self.search_config_list(search_list, _objects)

    @pyqtSlot(str, "PyQt_PyObject", name="on_subscribe_config")
    @pyqtSlot(list, "PyQt_PyObject", name="on_subscribe_config")
    def on_subscribe_config(self, section: str | list, callback) -> None:
        logging.debug(
            f"NEW CONFIG SUBSCRIPTION : {self.on_subscribe_config} called from {callback.__class__.__name__}"
        )
        if not self.configfile.get("config"):
            return None
        if not section or not callable(callback):
            return

        if isinstance(section, str):
            self.on_config_subscription[dict].connect(callback)
            self.on_config_subscription[dict].emit(self.get_config(section))
        elif isinstance(section, list):
            self.on_config_subscription[list].connect(callback)
            self.on_config_subscription[list].emit(
                self.search_config_list(section)
            )
        return

    def _check_callback(self, name: str, values: dict) -> bool:
        _split: list = name.split(" ", 1)  # Only need the first " " separation

        _object_type, _object_name = tuple(
            _split + [""] * max(0, 2 - len(_split))
        )

        if name.startswith(
            "extruder"
        ):  # TODO fix this extruder and naming its just stupid code,
            # if this goes away the ui breaks :/ FOR NOW
            _object_name = name
        if hasattr(self, f"{_object_type}_object_updated"):
            _callback = getattr(self, f"{_object_type}_object_updated")
            if callable(_callback):
                _callback(values, _object_name)
                return True
        return False

    @pyqtSlot(list, name="on_object_report_received")
    def on_object_report_received(self, report: list) -> None:
        if not report or len(report) <= 1:
            return
        _report_length = len(report) - 1
        if isinstance(report[0], dict):
            _objects_updated_dict: dict = report[0]
        _objects_updated_names = list(report[0])
        self._last_eventTime = report[_report_length]
        self.printer_objects.update(dict(report[0]))
        # * Callbacks for each object updated object
        list(
            map(
                lambda n: self._check_callback(n, _objects_updated_dict[n]),
                _objects_updated_names,
            )
        )
        _logger.debug(
            f"""Object report received for {_objects_updated_names} 
            objects,going to callbacks"""
        )

    ####################*# Callbacks #*####################
    @pyqtSlot(list, name="on_gcode_response")
    def on_gcode_response_received(self, report: list) -> None:
        # TODO: Handle reports coming from subscribed websocket object
        # if not isinstance(report):
        _split_information = report[0].split("// ")
        
        self.on_gcode_response.emit(report)

    def webhooks_object_updated(self, value: dict, name: str = "") -> None:
        """webhooks_object_updated Sends an event type according to the state
            received from webhooks subscribed object

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
                _logger.error("Events does have the event")
                _event_callback = getattr(events, f"Klippy{_state_call}Event")
                if callable(_event_callback):
                    try:
                        event = _event_callback(
                            value["state"], value["state_message"]
                        )
                        instance = QApplication.instance()
                        if instance is not None and isinstance(event, QEvent):
                            instance.sendEvent(self.parent(), event)
                        else:
                            raise Exception(
                                "QApplication.instance is None type."
                            )
                    except Exception as e:
                        _logger.debug(
                            f"Unable to send internal Klippy {_state_call} notification : {e}"
                        )

    def gcode_move_object_updated(self, value: dict, name: str = "") -> None:
        if "speed_factor" in value.keys():
            self.on_gcode_move_update[str, float].emit(
                "speed_factor", value["speed_factor"]
            )
        if "speed" in value.keys():
            self.on_gcode_move_update[str, float].emit("speed", value["speed"])
        if "extrude_factor" in value.keys():
            self.on_gcode_move_update[str, float].emit(
                "extruder_factor", value["extrude_factor"]
            )
        if "absolute_coordinates" in value.keys():
            self.on_gcode_move_update[str, bool].emit(
                "absolute_coordinates", value["absolute_coordinates"]
            )
        if "absolute_extrude" in value.keys():
            self.on_gcode_move_update[str, bool].emit(
                "absolute_extrude", value["absolute_extrude"]
            )
        if "homing_origin" in value.keys():
            self.on_gcode_move_update[str, list].emit(
                "homing_origin", value["homing_origin"]
            )
        if "position" in value.keys():
            self.on_gcode_move_update[str, list].emit(
                "position", value["position"]
            )
        if "gcode_position" in value.keys():
            self.on_gcode_move_update[str, list].emit(
                "gcode_position", value["gcode_position"]
            )

    def toolhead_object_updated(self, values: dict, name: str = "") -> None:
        if "homed_axes" in values.keys():
            self.on_toolhead_update[str, str].emit(
                "homed_axes", values["homed_axes"]
            )
        if "print_time" in values.keys():
            self.on_toolhead_update[str, float].emit(
                "print_time", values["print_time"]
            )
        if "estimated_print_time" in values.keys():
            self.on_toolhead_update[str, float].emit(
                "estimated_print_time", values["estimated_print_time"]
            )
        if "extruder" in values.keys():
            self.on_toolhead_update[str, str].emit(
                "extruder", values["extruder"]
            )
            self.active_extruder_name = values["extruder"]
        if "position" in values.keys():
            self.on_toolhead_update[str, list].emit(
                "position", values["position"]
            )
        if "max_velocity" in values.keys():
            self.on_toolhead_update[str, float].emit(
                "max_velocity", values["max_velocity"]
            )
        if "max_accel" in values.keys():
            self.on_toolhead_update[str, float].emit(
                "max_accel", values["max_accel"]
            )
        if "max_accel_to_decel" in values.keys():
            self.on_toolhead_update[str, float].emit(
                "max_accel_to_decel", values["max_accel_to_decel"]
            )
        if "square_corner_velocity" in values.keys():
            self.on_toolhead_update[str, float].emit(
                "square_corner_velocity", values["square_corner_velocity"]
            )

    def extruder_object_updated(
        self, value: dict, extruder_name: str = "extruder"
    ) -> None:
        if "temperature" in value.keys():
            self.on_extruder_update.emit(
                extruder_name, "temperature", value["temperature"]
            )
            self.heaters_object[f"{extruder_name}"]["actual_temperature"] = (
                value["temperature"]
            )
        if "target" in value.keys():
            self.on_extruder_update.emit(
                extruder_name, "target", value["target"]
            )
            self.heaters_object[f"{extruder_name}"]["target_temperature"] = (
                value["target"]
            )
        if "can_extrude" in value.keys():
            self.heaters_object[f"{extruder_name}"]["can_extrude"] = value[
                "can_extrude"
            ]
        if "power" in value.keys():
            self.on_extruder_update.emit(
                extruder_name, "power", value["power"]
            )
        if "pressure_advance" in value.keys():
            self.on_extruder_update.emit(
                extruder_name, "pressure_advance", value["pressure_advance"]
            )
        if "smooth_time" in value.keys():
            self.on_extruder_update.emit(
                extruder_name, "smooth_time", value["smooth_time"]
            )
        if "can_extrude" in value.keys():
            # TODO: Emit a signal that means that the extruder can extrude
            pass

    def heater_bed_object_updated(
        self, value: dict, heater_name: str = "heater_bed"
    ) -> None:
        if "temperature" in value.keys():
            self.on_heater_bed_update.emit(
                heater_name, "temperature", value["temperature"]
            )
            self.heaters_object["bed"]["actual_temperature"] = value[
                "temperature"
            ]
        if "target" in value.keys():
            self.on_heater_bed_update.emit(
                heater_name, "target", value["target"]
            )
            self.heaters_object["bed"]["target_temperature"] = value["target"]
        if "power" in value.keys():
            self.on_heater_bed_update.emit(
                heater_name, "power", value["power"]
            )

    def chamber_object_updated(
        self, value: dict, heater_name: str = "chamber"
    ):
        # TODO: Complete the search for the chamber object, but there is no actual chamber heater. If i create a klippy module it can be done like this maybe
        self.has_chamber = True

    def fan_object_updated(self, value: dict, fan_name: str = "fan") -> None:
        if "speed" in value.keys():
            self.on_fan_update[str, str, float].emit(
                fan_name, "speed", value["speed"]
            )
        if "rpm" in value.keys():
            self.on_fan_update[str, str, int].emit(
                fan_name, "rpm", value["rpm"]
            )

    def idle_timeout_object_updated(self, value: dict, name: str = "") -> None:
        if "state" in value.keys():
            self.on_idle_timeout_update[str, str].emit("state", value["state"])
            if "printing" in value["state"]:
                self.printer_busy = True
            elif (
                self.printing_state != "printing"
                and value["state"] != "printing"
            ):
                # It's also busy if the printer is printing or paused
                self.printer_busy = False
        if "printing_time" in value.keys():
            self.on_idle_timeout_update[str, float].emit(
                "printing_time", value["printing_time"]
            )

    def virtual_sdcard_object_updated(
        self, values: dict, name: str = ""
    ) -> None:
        if "progress" in values.keys():
            self.on_virtual_sdcard_update[str, float].emit(
                "progress", values["progress"]
            )
        if "is_active" in values.keys():
            self.on_virtual_sdcard_update[str, bool].emit(
                "is_active", values["is_active"]
            )
        if "file_position" in values.keys():
            self.on_virtual_sdcard_update[str, float].emit(
                "file_position", float(values["file_position"])
            )

    def print_stats_object_updated(self, values: dict, name: str = "") -> None:
        try:
            if "filename" in values.keys():
                self.on_print_stats_update[str, str].emit(
                    "filename", values["filename"]
                )
                self.print_file_loaded = True
            if "total_duration" in values.keys():
                self.on_print_stats_update[str, float].emit(
                    "total_duration", values["total_duration"]
                )
            if "print_duration" in values.keys():
                self.on_print_stats_update[str, float].emit(
                    "print_duration", values["print_duration"]
                )
            if "filament_used" in values.keys():
                self.on_print_stats_update[str, float].emit(
                    "filament_used", values["filament_used"]
                )
            if "state" in values.keys():
                self.on_print_stats_update[str, str].emit(
                    "state", values["state"]
                )
                self.printing_state = values["state"]
                if values["state"] == "standby" or values["state"] == "error":
                    self.print_file_loaded = False
                    self.printing = False
                else:
                    self.print_file_loaded = True
                    if (
                        values["state"] == "printing"
                        or values["state"] == "pause"
                    ):
                        self.printing = True

            if "message" in values.keys():
                self.on_print_stats_update[str, str].emit(
                    "message", values["message"]
                )
                self.printing_error_message = values["message"]
            if "info" in values.keys():
                self.on_print_stats_update[str, dict].emit(
                    "info", values["info"]
                )
            return
        except Exception as e:
            _logger.error(f"Error sending print stats update {e}")

    def display_status_object_updated(
        self, values: dict, name: str = ""
    ) -> None:
        if "message" in values.keys():
            self.on_display_update[str, str].emit("message", values["message"])
        if "progress" in values.keys():
            self.on_display_update[str, float].emit(
                "progress", values["progress"]
            )

    def temperature_sensor_object_updated(
        self, values: dict, temperature_sensor_name: str
    ) -> None:
        if "temperature" in values.keys():
            self.on_temperature_sensor_update.emit(
                temperature_sensor_name, "temperature", values["temperature"]
            )
        if "measured_min_temp" in values.keys():
            self.on_temperature_sensor_update.emit(
                temperature_sensor_name,
                "measured_min_temp",
                values["measured_min_temp"],
            )
        if "measured_max_temp" in values.keys():
            self.on_temperature_sensor_update.emit(
                temperature_sensor_name,
                "measured_max_temp",
                values["measured_max_temp"],
            )

    def temperature_fan_object_updated(
        self, values: dict, temperature_fan_name: str
    ) -> None:
        if "speed" in values.keys():
            self.on_temperature_fan_update.emit(
                temperature_fan_name, "speed", values["speed"]
            )
        if "temperature" in values.keys():
            self.on_temperature_fan_update.emit(
                temperature_fan_name, "temperature", values["temperature"]
            )
        if "target" in values.keys():
            self.on_temperature_fan_update.emit(
                temperature_fan_name, "target", values["target"]
            )

    def filament_switch_sensor_object_updated(
        self, values: dict, filament_switch_name: str
    ) -> None:
        if "filament_detected" in values.keys():
            self.on_filament_switch_sensor_update.emit(
                filament_switch_name,
                "filament_detected",
                values["filament_detected"],
            )
            self.available_filament_sensors.update(
                {f"{filament_switch_name}": values}
            )
        if "enabled" in values.keys():
            self.on_filament_switch_sensor_update.emit(
                filament_switch_name, "enabled", values["enabled"]
            )
            self.available_filament_sensors.update(
                {f"{filament_switch_name}": values}
            )

    def filament_motion_sensor_object_updated(
        self, values: dict, filament_motion_name: str
    ) -> None:
        if "filament_detected" in values.keys():
            self.on_filament_motion_sensor_update.emit(
                filament_motion_name,
                "filament_detected",
                values["filament_detected"],
            )
            self.available_filament_sensors.update(
                {f"{filament_motion_name}": values}
            )

        if "enabled" in values.keys():
            self.on_filament_motion_sensor_update.emit(
                filament_motion_name, "enabled", values["enabled"]
            )
            self.available_filament_sensors.update(
                {f"{filament_motion_name}": values}
            )

    def output_pin_object_updated(
        self, values: dict, output_pin_name: str
    ) -> None:
        if "value" in values.keys():
            self.on_output_pin_update.emit(
                output_pin_name, "value", values["value"]
            )

    def bed_mesh_object_updated(self, values: dict, name: str) -> None:
        # TODO
        pass

    def gcode_macro_object_updated(
        self, values: dict, gcode_macro_name: str
    ) -> None:
        # * values argument can come with many different types for this macro so handle them in another place

        self.on_gcode_macro_update.emit(gcode_macro_name, values)
        return

    def configfile_object_updated(self, values: dict, name: str = "") -> None:
        self.configfile.update(values)
        if "config" in values.keys():
            self.on_printer_config.emit(values["config"])
        if "settings" in values.keys():
            # TODO
            ...
        if "save_config_pending" in values.keys():
            self.on_save_config_pending.emit()
        if "save_config_pending_items" in values.keys():
            # TODO
            ...
        if "warnings" in values.keys():
            # TODO
            ...
        # print(values)

        self.on_configfile_update.emit(values)  # Signal config update

        return

    def gcode_object_updated(self, values: dict, name: str = "") -> None:
        if not values.get("commands"):
            return
        self.available_gcode_commands.update(values.get("commands"))  # type: ignore
        self.on_available_gcode_cmds.emit(values.get("commands"))
        return

    def manual_probe_object_updated(self, values: dict, name: str) -> None:
        print(values)
        # TODO
        return

    def probe_object_updated(self, values: dict, name: str) -> None:
        # TODO
        print(values)
        ...

    def bltouch_object_updated(self, values: dict, name: str) -> None:
        print(values)
        # TODO:
        ...

    def probe_eddy_current_object_updated(
        self, values: dict, name: str
    ) -> None:
        # TODO
        pass

    def axis_twist_compensation_object_updated(
        self, values: dict, name: str
    ) -> None:
        # TODO
        ...

    def temperature_probe_object_updated(
        self, values: dict, name: str
    ) -> None:
        pass

    def unload_filament_object_updated(
        self, values: dict, name: str
    ) -> None: ...  # TODO Add unload filament object verification
    def load_filament_object_updated(
        self, values: dict, name: str
    ) -> None: ...  # TODO Add load filament object verification
