from functools import partial
from PyQt6.QtWidgets import QStackedWidget, QWidget
from PyQt6 import QtCore
import typing

from PyQt6.QtCore import (
    pyqtSlot,
    pyqtSignal,
    pyqtBoundSignal,
    Qt,
    QAbstractListModel,
    QAbstractItemModel,
)

from lib.ui.utilitiesStackedWidget_ui import Ui_utilitiesStackedWidget


class UtilitiesTab(QStackedWidget):
    request_back = pyqtSignal(name="request_back")
    request_change_page = pyqtSignal(int, int, name="request_change_page")

    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)

        self.panel = Ui_utilitiesStackedWidget()
        self.panel.setupUi(self)

        # Connecting buttons in the panel routing tree
        # Utilities Screen
        self.panel.utilities_info_btn.clicked.connect(
            partial(self.change_page, 1)
        )
        self.panel.utilities_leds_btn.clicked.connect(
            partial(self.change_page, 2)
        )
        self.panel.utilities_lcd_settings_btn.clicked.connect(
            partial(self.change_page, 3)
        )

        # Info Screen
        self.panel.info_back_btn.clicked.connect(self.back_button)

        # LEDs Screen
        self.panel.leds_back_btn.clicked.connect(self.back_button)

        # LCD Settings Screen
        self.panel.lcd_settings_back_btn.clicked.connect(self.back_button)

    def change_page(self, index):
        # Emits with the request its tab index and its page index
        self.request_change_page.emit(3, index)

    def back_button(self):
        self.request_back.emit()
