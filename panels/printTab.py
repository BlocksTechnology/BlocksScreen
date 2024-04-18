from PyQt6.QtWidgets import QStackedWidget, QWidget
from PyQt6 import QtCore
import typing

from qt_ui.printStackedWidget_ui import Ui_printStackedWidget

class PrintTab(QStackedWidget):
    
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)

        self.panel = Ui_printStackedWidget()
        self.panel.setupUi(self)
        self.show()
        
        self.index_stack = []
        
        # Connecting the print_btn.clicked event to the change_page method
        self.panel.main_print_btn.clicked.connect(self.change_page)
        self.panel.files_back_folder_btn.clicked.connect(self.change_page)
        
    
    def change_page(self, int):
        self.setCurrentIndex(1)
        self.index_stack.append(self.currentIndex())
        
    