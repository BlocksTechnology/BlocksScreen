from collections import deque
from PyQt6.QtWidgets import QStackedWidget, QWidget
from functools import partial
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, pyqtSlot
import typing

from PyQt6.QtCore import (
    pyqtSlot,
    pyqtSignal,
    pyqtBoundSignal,
    Qt,
    QAbstractListModel,
    QAbstractItemModel,
)
from scripts.moonrakerComm import MoonWebSocket
from scripts.bo_includes.bo_printer import Printer
from functools import partial

from qt_ui.controlStackedWidget_ui import Ui_controlStackedWidget

class ControlTab(QStackedWidget):
    request_back_button_pressed = pyqtSignal(name = "request_back_button_pressed")
    request_change_page = pyqtSignal(int, int, name = "request_change_page")
    def __init__(self, parent: typing.Optional[QWidget], ws: MoonWebSocket, printer: Printer) -> None:
        super().__init__(parent)

        self.panel = Ui_controlStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.main_panel = parent
        self.ws = ws
        self.printer = printer
        
        self.show()
    
        self.index_stack = deque(maxlen=4)
        
        # Connecting buttons in the panel routing tree
        # Control Screen
        self.panel.control_motion_btn.clicked.connect(partial(self.change_page, 1))
        self.panel.control_temperature_btn.clicked.connect(partial(self.change_page, 4))
        self.panel.control_printer_settings_btn.clicked.connect(partial(self.change_page, 6))
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
    
    def change_page(self, index):
        self.request_change_page.emit(2, index)
        # self.index_stack.append(self.currentIndex())
        # self.setCurrentIndex(index)
 
    def back_button(self):
        self.request_back_button_pressed.emit()
        # self.back_button_signal.emit()
        # self.setCurrentIndex(self.index_stack[-1])  #Go to the last position of the stack.
        # self.index_stack.pop()                      #Remove the last position.
    