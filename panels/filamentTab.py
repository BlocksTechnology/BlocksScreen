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

from qt_ui.filamentStackedWidget_ui import Ui_filamentStacketWidget

class FilamentTab(QStackedWidget):
    
    request_filament_change_page = pyqtSignal(name="filament_change_page")
    request_filament_load_t1 = pyqtSignal(name = "filament_load_t1")
    request_filament_load_t2 = pyqtSignal(name = "filament_load_t2")
    request_back_button_pressed = pyqtSignal(name = "request_back_button_pressed")
    request_change_page = pyqtSignal(int, int, name = "request_change_page")
    
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)

        self.panel = Ui_filamentStacketWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.show()
        
        self.index_stack = []
        
        # Connecting buttons in the panel routing tree
        # Filament Screen
        self.panel.filament_load_btn.clicked.connect(partial(self.change_page, 1))
        self.panel.filament_unload_btn.clicked.connect(partial(self.change_page, 5))
        self.panel.filament_dryers_btn.clicked.connect(partial(self.change_page, 6))
        
        # Load Screen
        self.panel.load_tool_1_icon_btn.clicked.connect(partial(self.change_page, 2))
        self.panel.load_tool_2_icon_btn.clicked.connect(partial(self.change_page, 3))     
        self.panel.load_tool_back_btn.clicked.connect(self.back_button) 
        
        # Load Tool Head 1
        self.panel.load_t1_custom_btn.clicked.connect(partial(self.change_page, 4))
        self.panel.load_t1_back_btn.clicked.connect(self.back_button) 
        self.panel.load_t1_pla_btn.clicked.connect(partial(self.load_filament_t1, 1))
        self.panel.load_t1_petg_btn.clicked.connect(partial(self.load_filament_t1, 2))
        self.panel.load_t1_abs_btn.clicked.connect(partial(self.load_filament_t1, 3))
        self.panel.load_t1_hips_btn.clicked.connect(partial(self.load_filament_t1, 4))
        self.panel.load_t1_nylon_btn.clicked.connect(partial(self.load_filament_t1, 5))
        self.panel.load_t1_tpu_btn.clicked.connect(partial(self.load_filament_t1, 6))
        
        # Load Tool Head 2
        self.panel.load_t2_custom_btn.clicked.connect(partial(self.change_page, 4))
        self.panel.load_t2_back_btn.clicked.connect(self.back_button) 
        self.panel.load_t2_pla_btn.clicked.connect(partial(self.load_filament_t1, 1))
        self.panel.load_t2_petg_btn.clicked.connect(partial(self.load_filament_t1, 2))
        self.panel.load_t2_abs_btn.clicked.connect(partial(self.load_filament_t1, 3))
        self.panel.load_t2_hips_btn.clicked.connect(partial(self.load_filament_t1, 4))
        self.panel.load_t2_nylon_btn.clicked.connect(partial(self.load_filament_t1, 5))
        self.panel.load_t2_tpu_btn.clicked.connect(partial(self.load_filament_t1, 6))
        
        # Custom Filament Screen
        self.panel.custom_fil_back_btn.clicked.connect(self.back_button) 
        
        # Unload Screen
        self.panel.unload_back_btn.clicked.connect(self.back_button) 
        
        # Dryers Screen
        self.panel.dryers_back_btn.clicked.connect(self.back_button) 
    
    def change_page(self, index):
        # Emits with the request its tab index and its page index
        self.request_change_page.emit(1, index)
 
    def back_button(self):
        self.request_back_button_pressed.emit()
        
    def load_filament_t1(self, filament):
        self.request_filament_load_t1.emit
    