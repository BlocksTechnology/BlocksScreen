from PyQt6.QtWidgets import QStackedWidget, QWidget
from PyQt6 import QtCore
import typing

from qt_ui.filamentStackedWidget_ui import Ui_filamentStacketWidget

class FilamentTab(QStackedWidget):
    
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)

        self.panel = Ui_filamentStacketWidget()
        self.panel.setupUi(self)
        self.show()
        
        self.index_stack = []
        
        # Connecting the filament_btn.clicked event to the change_page method
        #self.panel.main_filament_btn.clicked.connect(self.change_page)
        #self.panel.files_back_folder_btn.clicked.connect(self.change_page)
        
    
    def change_page(self, int):
        self.setCurrentIndex(int)
        self.index_stack.append(self.currentIndex())
        
    