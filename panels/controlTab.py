from PyQt6.QtWidgets import QStackedWidget, QWidget
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, pyqtSlot
import typing


from functools import partial

from qt_ui.controlStackedWidget_ui import Ui_controlStackedWidget

class ControlTab(QStackedWidget):
    
    page_index_signal = pyqtSignal(int, name="change_page")
    
    def __init__(self, parent: typing.Optional[QWidget]) -> None:
        super().__init__(parent)

        self.panel = Ui_controlStackedWidget()
        self.panel.setupUi(self)
        self.show()
        
        self.index_stack = []
        
        # Connecting the print_btn.clicked event to the change_page method
        #self.panel.main_print_btn.clicked.connect(self.change_page)
        #self.panel.files_back_folder_btn.clicked.connect(self.change_page)
        
        self.panel.control_motion_btn.clicked.connect(partial(self.change_page, 1))
        # self.panel.control_motion_btn.clicked.connect()
        
        # self.panel.control_bed_leveling_btn.clicked.connect(self.)
        
        
    # @pyqtSlot(name="change_page")
    def change_page(self, int):
        self.setCurrentIndex(int)
        _button = self.sender()
        print(_button.text())
        self.index_stack.append(self.currentIndex())
        
    
    @pyqtSlot(name="change_page")
    def page_index(self):
        _current_index = self.currentIndex()
        