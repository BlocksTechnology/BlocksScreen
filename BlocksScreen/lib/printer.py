from __future__ import annotations

import logging
import typing

import events
from lib.moonrakerComm import MoonWebSocket
from PyQt6 import QtCore, QtWidgets

_logger = logging.getLogger(name="logs/BlocksScreen.logs")


class Printer(QtCore.QObject):
    request_available_objects_signal = QtCore.pyqtSignal(
        name="get_available_objects"
    )
    request_object_subscription_signal = QtCore.pyqtSignal(
        dict, name="object_subscription"
    )
    toolhead_number_signal = QtCore.pyqtSignal(
        int, name="toolhead_number_received"
    )

    extruder_update = QtCore.pyqtSignal(
        str, str, float, name="extruder_update"
    )
    heater_bed_update = QtCore.pyqtSignal(
        str, str, float, name="heater_bed_update"
    )
    fan_update = QtCore.pyqtSignal(
        [str, str, float], [str, str, int], name="fan_update"
    )
    chamber_update = QtCore.pyqtSignal(name="chamber_update")

    idle_timeout_update = QtCore.pyqtSignal(
        [str, float], [str, str], name="idle_timeout_update"
    )

    gcode_move_update = QtCore.pyqtSignal(
        [str, list], [str, float], [str, bool], name="gcode_move_update"
    )
    toolhead_update = QtCore.pyqtSignal(
        [str, float], [str, list], [str, str], name="toolhead_update"
    )
    virtual_sdcard_update = QtCore.pyqtSignal(
        [str, float], [str, bool], name="virtual_sdcard_update"
    )
    print_stats_update = QtCore.pyqtSignal(
        [str, dict], [str, float], [str, str], name="print_stats_update"
    )
    display_update = QtCore.pyqtSignal(
        [str, str], [str, float], name="display_update"
    )
    temperature_sensor_update = QtCore.pyqtSignal(
        str, str, float, name="temperature_sensor_update"
    )
    temperature_fan_update = QtCore.pyqtSignal(
        str, str, float, name="temperature_fan_update"
    )
    filament_switch_sensor_update = QtCore.pyqtSignal(
        str, str, bool, name="filament_switch_sensor_update"
    )
    filament_motion_sensor_update = QtCore.pyqtSignal(
        str, str, bool, name="filament_motion_sensor_update"
    )
    output_pin_update = QtCore.pyqtSignal(
        str, str, float, name="output_pin_update"
    )
    bed_mesh_update = QtCore.pyqtSignal(
        str, list, list, list, list, name="bed_mesh_update"
    )
    gcode_macro_update = QtCore.pyqtSignal(
        str, dict, name="gcode_macro_update"
    )
    webhooks_update = QtCore.pyqtSignal(str, str, name="webhooks_update")
    query_printer_object = QtCore.pyqtSignal(dict, name="query_printer_object")
    save_config_pending: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="save_config_pending")
    )
    printer_config: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="printer_config"
    )

    configfile_update: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="configfile_update"
    )

    config_subscription: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(
            [dict],
            [list],
            name="config_subscription",
        )
    )
    manual_probe_update: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(dict, name="manual_probe_update")
    )
    available_gcode_cmds: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(dict, name="available_gcode_cmds")
    )
    gcode_response: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        list, name="gcode_response"
    )
    extruder_number: int = 0
    available_gcode_commands: dict = {}
    available_objects: dict = {}
    configfile: dict = {}
    printing: bool = False
    printing_state: str = ""
    print_file_loaded: bool = False
    printer_busy: bool = False
    current_loaded_file: str = ""
    current_loaded_file_metadata: str = ""

    def __init__(self, parent: QtCore.QObject, ws: MoonWebSocket, /) -> None:
        super(Printer, self).__init__(parent)

        self.ws = ws
        self.active_extruder_name: str = ""
        self.available_filament_sensors: dict = {}
        self.has_chamber: bool = False

        _heater_attributes: dict = {
            "current_temperature": 0.0,
            "target_temperature": 0.0,
            "can_extrude": False,
        }
        self.heaters_object: dict = {
            "extruder": _heater_attributes.copy(),
            "extruder1": _heater_attributes.copy(),
            "bed": _heater_attributes.copy(),
        }

        self.ws.klippy_state_signal.connect(self.on_klippy_status)
        self.request_available_objects_signal.connect(
            self.ws.api.get_available_objects
        )
        self.request_object_subscription_signal.connect(
            self.ws.api.object_subscription
        )
        self.query_printer_object.connect(self.ws.api.object_query)

    def clear_printer_objs(self) -> None:
        self.available_gcode_commands.clear()
        self.available_objects.clear()
        self.configfile.clear()
        self.printing = False
        self.printing_state = ""
        self.print_file_loaded = False
        self.printer_busy = False
        self.current_loaded_file = ""
        self.current_loaded_file_metadata = ""

    @QtCore.pyqtSlot(str, name="on_klippy_status")
    def on_klippy_status(self, state: str):
        # "startup", "error", "ready", "shutdown", "disconnected"
        if state.lower() == "ready":
            self.request_available_objects_signal.emit()  # request available objects
            _query_request: dict = {
                "idle_timeout": None,
                "print_stats": None,
                "virtual_sdcard": None,
            }
            self.query_printer_object.emit(_query_request)
        elif (
            state.lower() == "error"
            or state.lower() == "disconnected"
            or state.lower() == "shutdown"
        ):
            self.clear_printer_objs()

    @QtCore.pyqtSlot(list, name="on_object_list")
    def on_object_list(self, object_list: list):
        [self.available_objects.update({obj: None}) for obj in object_list]
        self.request_object_subscription_signal[dict].emit(
            self.available_objects
        )  # subscribe to all available printer objects

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

    @QtCore.pyqtSlot(str, "PyQt_PyObject", name="on_subscribe_config")
    @QtCore.pyqtSlot(list, "PyQt_PyObject", name="on_subscribe_config")
    def on_subscribe_config(self, section: str | list, callback) -> None:
        """Slot that manages object config subscriptions

        Args:
            section (str | list): Config section to subscribe to
            callback (function): Callback method that is executed signaled after

        Returns:
            _type_: _description_
        """
        logging.debug(
            f"NEW CONFIG SUBSCRIPTION : {self.on_subscribe_config} called from {callback.__class__.__name__}"
        )
        if not self.configfile.get("config"):
            return None
        if not section or not callable(callback):
            return

        if isinstance(section, str):
            self.config_subscription[dict].connect(callback)  # type:ignore
            self.config_subscription[dict].emit(
                {section: self.get_config(section)}
            )
        elif isinstance(section, list):
            self.config_subscription[list].connect(callback)  # type:ignore
            self.config_subscription[list].emit(
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
        if hasattr(self, f"_{_object_type}_object_updated"):
            _callback = getattr(self, f"_{_object_type}_object_updated")
            if callable(_callback):
                _callback(values, _object_name)
                return True
        return False

    @QtCore.pyqtSlot(list, name="on_object_report_received")
    def on_object_report_received(self, report: list) -> None:
        if not report or len(report) <= 1:
            return
        if isinstance(report[0], dict):
            _objects_updated_dict: dict = report[0]
        _objects_updated_names = list(report[0])
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

    ####################*# Callbacks #*#####################
    @QtCore.pyqtSlot(list, name="_gcode_response")
    def _gcode_response(self, report: list) -> None:
        self.gcode_response.emit(report)

    def _webhooks_object_updated(
        self, value: dict, name: str = "webhooks"
    ) -> None:
        """Sends an event type according to the received state
            from webhooks object

        Args:
            value (dict): _description_
            name (str, optional): _description_. Defaults to "".
        """
        if "state" in value.keys() and "state_message" in value.keys():
            self.webhooks_update.emit(
                value["state"], value["state_message"]
            )
            _logger.debug("Webhooks message received")
            _state: str = value["state"]
            _state_upper = _state[0].upper()
            _state_call = f"{_state_upper}{_state[1:]}"
            if hasattr(events, f"Klippy{_state_call}"):
                _logger.debug(f"Events has {_state_call} event")
                _event_callback = getattr(events, f"Klippy{_state_call}")
                if callable(_event_callback):
                    try:
                        event = _event_callback(
                            value["state"], value["state_message"]
                        )
                        instance = QtWidgets.QApplication.instance()
                        if instance is not None and isinstance(
                            event, QtCore.QEvent
                        ):
                            instance.sendEvent(self.parent(), event)
                        else:
                            raise Exception(
                                "QApplication.instance is None type."
                            )
                    except Exception as e:
                        _logger.debug(
                            f"Unable to send internal Klippy {_state_call} notification : {e}"
                        )

    def _gcode_move_object_updated(
        self, value: dict, name: str = "gcode_move"
    ) -> None:
        if "speed_factor" in value.keys():
            self.gcode_move_update[str, float].emit(
                "speed_factor", value["speed_factor"]
            )
        if "speed" in value.keys():
            self.gcode_move_update[str, float].emit("speed", value["speed"])
        if "extrude_factor" in value.keys():
            self.gcode_move_update[str, float].emit(
                "extruder_factor", value["extrude_factor"]
            )
        if "absolute_coordinates" in value.keys():
            self.gcode_move_update[str, bool].emit(
                "absolute_coordinates", value["absolute_coordinates"]
            )
        if "absolute_extrude" in value.keys():
            self.gcode_move_update[str, bool].emit(
                "absolute_extrude", value["absolute_extrude"]
            )
        if "homing_origin" in value.keys():
            self.gcode_move_update[str, list].emit(
                "homing_origin", value["homing_origin"]
            )
        if "position" in value.keys():
            self.gcode_move_update[str, list].emit(
                "position", value["position"]
            )
        if "gcode_position" in value.keys():
            self.gcode_move_update[str, list].emit(
                "gcode_position", value["gcode_position"]
            )

    def _toolhead_object_updated(
        self, values: dict, name: str = "toolhead"
    ) -> None:
        if "homed_axes" in values.keys():
            self.toolhead_update[str, str].emit(
                "homed_axes", values["homed_axes"]
            )
        if "print_time" in values.keys():
            self.toolhead_update[str, float].emit(
                "print_time", values["print_time"]
            )
        if "estimated_print_time" in values.keys():
            self.toolhead_update[str, float].emit(
                "estimated_print_time", values["estimated_print_time"]
            )
        if "extruder" in values.keys():
            self.toolhead_update[str, str].emit("extruder", values["extruder"])
            self.active_extruder_name = values["extruder"]
        if "position" in values.keys():
            self.toolhead_update[str, list].emit(
                "position", values["position"]
            )
        if "max_velocity" in values.keys():
            self.toolhead_update[str, float].emit(
                "max_velocity", values["max_velocity"]
            )
        if "max_accel" in values.keys():
            self.toolhead_update[str, float].emit(
                "max_accel", values["max_accel"]
            )
        if "max_accel_to_decel" in values.keys():
            self.toolhead_update[str, float].emit(
                "max_accel_to_decel", values["max_accel_to_decel"]
            )
        if "square_corner_velocity" in values.keys():
            self.toolhead_update[str, float].emit(
                "square_corner_velocity", values["square_corner_velocity"]
            )

    def _extruder_object_updated(
        self, value: dict, extruder_name: str = "extruder"
    ) -> None:
        if "temperature" in value.keys():
            self.extruder_update.emit(
                extruder_name, "temperature", value["temperature"]
            )
            self.heaters_object[f"{extruder_name}"]["actual_temperature"] = (
                value["temperature"]
            )
        if "target" in value.keys():
            self.extruder_update.emit(extruder_name, "target", value["target"])
            self.heaters_object[f"{extruder_name}"]["target_temperature"] = (
                value["target"]
            )
        if "can_extrude" in value.keys():
            self.heaters_object[f"{extruder_name}"]["can_extrude"] = value[
                "can_extrude"
            ]
        if "power" in value.keys():
            self.extruder_update.emit(extruder_name, "power", value["power"])
        if "pressure_advance" in value.keys():
            self.extruder_update.emit(
                extruder_name, "pressure_advance", value["pressure_advance"]
            )
        if "smooth_time" in value.keys():
            self.extruder_update.emit(
                extruder_name, "smooth_time", value["smooth_time"]
            )
        if "can_extrude" in value.keys():
            # TODO: Emit a signal that means that the extruder can extrude
            pass

    def _heater_bed_object_updated(
        self, value: dict, heater_name: str = "heater_bed"
    ) -> None:
        if "temperature" in value.keys():
            self.heater_bed_update.emit(
                heater_name, "temperature", value["temperature"]
            )
            self.heaters_object["bed"]["actual_temperature"] = value[
                "temperature"
            ]
        if "target" in value.keys():
            self.heater_bed_update.emit(heater_name, "target", value["target"])
            self.heaters_object["bed"]["target_temperature"] = value["target"]
        if "power" in value.keys():
            self.heater_bed_update.emit(heater_name, "power", value["power"])

    def _chamber_object_updated(
        self, value: dict, heater_name: str = "chamber"
    ):
        # TODO: Complete Chamber object, this object does not actually exist on klippy, i would need to create it
        self.has_chamber = True

    def _fan_object_updated(self, value: dict, fan_name: str = "fan") -> None:
        if "speed" in value.keys():
            self.fan_update[str, str, float].emit(
                "fan", "speed", value["speed"]
            )
        if "rpm" in value.keys():
            self.fan_update[str, str, int].emit("fan", "rpm", value["rpm"])

    def _fan_generic_object_updated(
        self, value: dict, fan_name: str = ""
    ) -> None:
        _names = ["fan_generic", fan_name]
        object_name = " ".join(_names)
        if "speed" in value.keys():
            self.fan_update[str, str, float].emit(
                object_name, "speed", value.get("speed")
            )
        if "rpm" in value.keys():
            self.fan_update[str, str, int].emit(
                object_name, "rpm", value.get("rpm")
            )

    def _controller_fan_object_updated(
        self, value: dict, fan_name: str = ""
    ) -> None:
        _names = ["controller_fan", fan_name]
        object_name = " ".join(_names)
        if "speed" in value.keys():
            self.fan_update[str, str, float].emit(
                object_name, "speed", value.get("speed")
            )
        elif "rpm" in value.keys():
            self.fan_update[str, str, int].emit(
                object_name, "rpm", value.get("rpm")
            )

    def _heater_fan_object_updated(
        self, value: dict, fan_name: str = ""
    ) -> None:
        # Associated with a heater, on when heater is active
        _names = ["heater_fan", fan_name]
        object_name = " ".join(_names)
        ...
        # _names = ["heater_fan", fan_name]
        # object_name = " ".join(_names)
        # if "speed" in value.keys():
        #     self.fan_update[str, str, float].emit(
        #         object_name, "speed", value.get("speed")
        #     )
        # elif "rpm" in value.keys():
        #     self.fan_update[str, str, int].emit(
        #         object_name, "rpm", value.get("rpm")
        #     )

    def _idle_timeout_object_updated(
        self, value: dict, name: str = "idle_timeout"
    ) -> None:
        if "state" in value.keys():
            self.idle_timeout_update[str, str].emit("state", value["state"])
            if "printing" in value["state"]:
                self.printer_busy = True
            elif (
                self.printing_state != "printing"
                and value["state"] != "printing"
            ):
                # It's also busy if the printer is printing or paused
                self.printer_busy = False
        if "printing_time" in value.keys():
            self.idle_timeout_update[str, float].emit(
                "printing_time", value["printing_time"]
            )

    def _virtual_sdcard_object_updated(
        self, values: dict, name: str = "virtual_sdcard"
    ) -> None:
        if "progress" in values.keys():
            self.virtual_sdcard_update[str, float].emit(
                "progress", values["progress"]
            )
        if "is_active" in values.keys():
            self.virtual_sdcard_update[str, bool].emit(
                "is_active", values["is_active"]
            )
        if "file_position" in values.keys():
            self.virtual_sdcard_update[str, float].emit(
                "file_position", float(values["file_position"])
            )

    def _print_stats_object_updated(
        self, values: dict, name: str = "print_stats"
    ) -> None:
        try:
            if "filename" in values.keys():
                self.print_stats_update[str, str].emit(
                    "filename", values["filename"]
                )
                self.print_file_loaded = True
            if "total_duration" in values.keys():
                self.print_stats_update[str, float].emit(
                    "total_duration", values["total_duration"]
                )
            if "print_duration" in values.keys():
                self.print_stats_update[str, float].emit(
                    "print_duration", values["print_duration"]
                )
            if "filament_used" in values.keys():
                self.print_stats_update[str, float].emit(
                    "filament_used", values["filament_used"]
                )
            if "state" in values.keys():
                self.print_stats_update[str, str].emit(
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
                self.print_stats_update[str, str].emit(
                    "message", values["message"]
                )
                # self.printing_error_message = values["message"]
            if "info" in values.keys():
                self.print_stats_update[str, dict].emit("info", values["info"])
            return
        except Exception as e:
            _logger.error(f"Error sending print stats update {e}")

    def _display_status_object_updated(
        self, values: dict, name: str = "display_status"
    ) -> None:
        if "message" in values.keys():
            self.display_update[str, str].emit("message", values["message"])
        if "progress" in values.keys():
            self.display_update[str, float].emit(
                "progress", values["progress"]
            )

    def _temperature_sensor_object_updated(
        self, values: dict, temperature_sensor_name: str
    ) -> None:
        if "temperature" in values.keys():
            self.temperature_sensor_update.emit(
                temperature_sensor_name, "temperature", values["temperature"]
            )
        if "measured_min_temp" in values.keys():
            self.temperature_sensor_update.emit(
                temperature_sensor_name,
                "measured_min_temp",
                values["measured_min_temp"],
            )
        if "measured_max_temp" in values.keys():
            self.temperature_sensor_update.emit(
                temperature_sensor_name,
                "measured_max_temp",
                values["measured_max_temp"],
            )

    def _temperature_fan_object_updated(
        self, values: dict, temperature_fan_name: str = ""
    ) -> None:
        _names = ["temperature_fan", temperature_fan_name]
        object_name = " ".join(_names)
        if "speed" in values.keys():
            self.temperature_fan_update.emit(
                object_name,
                "speed",
                values["speed"],
            )
        if "temperature" in values.keys():
            self.temperature_fan_update.emit(
                object_name,
                "temperature",
                values["temperature"],
            )
        if "target" in values.keys():
            self.temperature_fan_update.emit(
                object_name,
                "target",
                values["target"],
            )

    def _filament_switch_sensor_object_updated(
        self, values: dict, filament_switch_name: str
    ) -> None:
        if "filament_detected" in values.keys():
            self.filament_switch_sensor_update.emit(
                filament_switch_name,
                "filament_detected",
                values["filament_detected"],
            )
            self.available_filament_sensors.update(
                {f"{filament_switch_name}": values}
            )
        if "enabled" in values.keys():
            self.filament_switch_sensor_update.emit(
                filament_switch_name, "enabled", values["enabled"]
            )
            self.available_filament_sensors.update(
                {f"{filament_switch_name}": values}
            )

    def _filament_motion_sensor_object_updated(
        self, values: dict, filament_motion_name: str
    ) -> None:
        if "filament_detected" in values.keys():
            self.filament_motion_sensor_update.emit(
                filament_motion_name,
                "filament_detected",
                values["filament_detected"],
            )
            self.available_filament_sensors.update(
                {f"{filament_motion_name}": values}
            )

        if "enabled" in values.keys():
            self.filament_motion_sensor_update.emit(
                filament_motion_name, "enabled", values["enabled"]
            )
            self.available_filament_sensors.update(
                {f"{filament_motion_name}": values}
            )

    def _output_pin_object_updated(
        self, values: dict, output_pin_name: str
    ) -> None:
        if "value" in values.keys():
            self.output_pin_update.emit(
                output_pin_name, "value", values["value"]
            )

    def _bed_mesh_object_updated(
        self, values: dict, name: str = "bed_mesh"
    ) -> None:
        # TODO
        pass

    def _gcode_macro_object_updated(
        self, values: dict, gcode_macro_name: str
    ) -> None:
        # * values argument can come with many different types for this macro so handle them in another place

        self.gcode_macro_update.emit(gcode_macro_name, values)
        return

    def _configfile_object_updated(
        self, values: dict, name: str = "configfile"
    ) -> None:
        self.configfile.update(values)
        if "config" in values.keys():
            self.printer_config.emit(values["config"])
        if "settings" in values.keys():
            # TODO
            ...
        if "save_config_pending" in values.keys():
            self.save_config_pending.emit()
        if "save_config_pending_items" in values.keys():
            # TODO
            ...
        if "warnings" in values.keys():
            # TODO
            ...

        self.configfile_update.emit(values)  # Signal config update

        return

    def _gcode_object_updated(
        self, values: dict, name: str = "gcode_object"
    ) -> None:
        if not values.get("commands"):
            return
        self.available_gcode_commands.update(values.get("commands"))  # type: ignore
        self.available_gcode_cmds.emit(values.get("commands"))
        return

    def _manual_probe_object_updated(self, values: dict, name: str) -> None:
        self.manual_probe_update[dict].emit(values)
        return

    def _probe_object_updated(self, values: dict, name: str) -> None:
        # TODO
        ...

    def _bltouch_object_updated(self, values: dict, name: str) -> None:
        # TODO:
        ...

    def _probe_eddy_current_object_updated(
        self, values: dict, name: str
    ) -> None:
        # TODO
        pass

    def _axis_twist_compensation_object_updated(
        self, values: dict, name: str
    ) -> None:
        # TODO
        ...

    def _temperature_probe_object_updated(
        self, values: dict, name: str
    ) -> None:
        pass

    def _unload_filament_object_updated(
        self, values: dict, name: str
    ) -> None: ...  # TODO Add unload filament object verification
    def _load_filament_object_updated(
        self, values: dict, name: str
    ) -> None: ...  # TODO Add load filament object verification
