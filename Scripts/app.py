import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("Scripts/uiTemplate.ui", self)
        


if __name__=="__main__":
    
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

    # There is another way i can do this, by passing the .ui file to .py and then use that .py file in my app.
    # I can do this with the command pyuic6 -o <pythonfile>.py -x <uifile>.ui
        
    # Then i get a .py file from the .ui file