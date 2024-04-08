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
        
        
        # self.panel.print_btn.clicked()

    
    