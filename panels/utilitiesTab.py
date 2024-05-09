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

from qt_ui.utilitiesStackedWidget_ui import Ui_utilitiesStackedWidget

class UtilitiesTab(QStackedWidget):
    
    request_back_button_pressed = pyqtSignal(name = "request_back_button_pressed")
    request_change_page = pyqtSignal(int, int, name = "request_change_page")
    
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)

        self.panel = Ui_utilitiesStackedWidget()
        self.panel.setupUi(self)
        self.show()
        
        self.index_stack = []
        
        # Connecting the print_btn.clicked event to the change_page method
        #self.panel.main_print_btn.clicked.connect(self.change_page)
        #self.panel.files_back_folder_btn.clicked.connect(self.change_page)
        
    
    def change_page(self, index):
        self.request_change_page.emit(3, index)
        # self.index_stack.append(self.currentIndex())
        # self.setCurrentIndex(index)
 
    def back_button(self):
        self.request_back_button_pressed.emit()
        # self.back_button_signal.emit()
        # self.setCurrentIndex(self.index_stack[-1])  #Go to the last position of the stack.
        # self.index_stack.pop()                      #Remove the last position.
        
    