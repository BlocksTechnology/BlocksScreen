from collections import deque
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
        # Move Axis
        self.panel.move_axis_back_btn.clicked.connect(self.back_button)
        # Temperature
        self.panel.temperature_back_btn.clicked.connect(self.back_button)
        # Extrude
        self.panel.extrude_back_btn.clicked.connect(self.back_button)
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
                self.run_gcode_signal.emit(f"SET_FAN_SPEED FAN={name} SPEED{new_value}")

        elif isinstance(new_value, int):
            self.run_gcode_signal.emit(
                f"SET_HEATER_TEMPERATURE HEATER={name} TARGET={new_value}"
            )
