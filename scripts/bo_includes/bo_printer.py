from __future__ import annotations
import timeit
import sys
import re
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import typing

from scripts.moonrakerComm import MoonWebSocket


class Printer(QObject):
    # TODO: Handle subscriptions and information received by subscriptions
    # TODO: Handle configfile information -> Create a structure where i can save the config file internally
    # TODO: Create variables that store information about specific printer objects like extruder, temperature etc..
    # @ Signals
    extruder_number: int = 0
    request_available_objects_signal = pyqtSignal(name="get_available_objects")
    request_object_subscription_signal = pyqtSignal(dict, name="object_subscription")
    extruder_number_received_signal = pyqtSignal(int, name="extruder_number_received")
    # homed_axis_update = pyqtSignal(str, name="homed_axis_updated")
    extruder_temperature_update_signal = pyqtSignal(
        str, str, float, name="extruder_temperature_update"
    )
    heater_bed_temperature_update_signal = pyqtSignal(
        str, str, float, name="heater_bed_temperature_update"
    )
    
    def __init__(self, parent: typing.Optional["QObject"], ws: MoonWebSocket) -> None:
        super(Printer, self).__init__(parent)
        self.main_window = parent
        self.ws = ws
        self.available_objects: dict = {}

        self.printer_state: str = "none"
        self._last_eventTime: float = 0.0
        self.printer_objects: dict = {}

        # @ Signal/Slot Connections
        self.ws.klippy_state_signal.connect(self.klippy_ready_report)
        self.request_available_objects_signal.connect(self.ws.api.get_available_objects)
        self.request_object_subscription_signal.connect(self.ws.api.object_subscription)

       

    @pyqtSlot(str, name="klippy_ready_report")
    def klippy_ready_report(self, state: str):
        if state == "ready":
            self.request_available_objects_signal.emit()

    @pyqtSlot(list, name="object_list_received")
    def object_list_received(self, object_list: list):
        [self.available_objects.update({obj: None}) for obj in object_list]
        self.request_object_subscription_signal[dict].emit(self.available_objects)
        #* Find how many extruders the printer has  
        _extruder_regex = re.compile(r"^extruder{1}?\d?")
        # _object_list: list = list(self.printer_objects.keys())
        _find = list(filter(_extruder_regex.match, object_list))
        self.extruder_number = len(_find)
        
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

    ###*# Callback Related #*###
    
    def check_callback_method(self, name: str, values: dict):
        # * Checks if there is a callback with the object name, calls it, passes the updated fields
        if hasattr(self, f"{name}_object_updated"):
            _callback = getattr(self, f"{name}_object_updated")
            if callable(_callback):
                _callback(values)
                return True
        return False

    def extruder_object_updated(
        self, value: dict, extruder_name: str = "extruder"
    ) -> None:
        if "temperature" in value.keys():
            self.extruder_temperature_update_signal.emit(
                extruder_name, "temperature", value["temperature"]
            )
            # TODO: Send signal with the new temperature to update subscribers
        if "target" in value.keys():
            pass
        if "power" in value.keys():
            pass
        if "pressure_advance" in value.keys():
            pass
        if "smooth_time" in value.keys():
            pass

    def heater_bed_object_updated(
        self, value: dict, heater_name: str = "heater_bed"
    ) -> None:
        # print("The bed object was updated!!!!")
        if "temperature" in value.keys():
            self.heater_bed_temperature_update_signal.emit(
                heater_name, "temperature", value["temperature"]
            )
        pass
