from PyQt6.QtWidgets import QStackedWidget, QWidget, QListView, QListWidget
from PyQt6.QtCore import pyqtSlot, pyqtSignal, pyqtBoundSignal
from PyQt6 import QtCore
import typing

from qt_ui.printStackedWidget_ui import Ui_printStackedWidget

class PrintTab(QStackedWidget):
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super(PrintTab, self).__init__(parent)

        self.panel = Ui_printStackedWidget()
        self.panel.setupUi(self)

        self.setCurrentIndex(0)
        self.show()
        
        # self.hide
        # @ Slot connections
        self.panel.print_btn.clicked.connect(self.showFilesPanel)
        self.panel.back_btn.clicked.connect(self.back)

        
    def showFilesPanel(self) -> None:
        self.setCurrentIndex(1)
    
    
    def back(self) -> None:
        _currentIndex = self.currentIndex()
        self.setCurrentIndex(_currentIndex -1 )

