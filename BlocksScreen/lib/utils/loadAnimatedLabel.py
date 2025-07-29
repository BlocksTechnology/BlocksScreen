from PyQt6 import QtGui, QtWidgets, QtCore

class LoadAnimatedLabel(QtWidgets.QLabel): 
    def __init__(self, parent) -> None:
        super().__init__(parent)
        