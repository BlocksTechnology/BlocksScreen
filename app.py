import logging
import sys

from PyQt6 import uic
from PyQt6.QtCore import QEvent, QEventLoop, QObject, Qt, pyqtSignal, pyqtSlot, QCoreApplication
from PyQt6.QtWidgets import (QApplication, QDockWidget, QFrame, QMainWindow, QSplashScreen,
                             QWidget)
from PyQt6.QtGui import QColor, QPixmap
from Qt_UI.Blocks_Screen_Lemos_ui import Ui_MainWindow
from Qt_UI.connectionWindow_ui import Ui_Form
from Scripts.moonrakerComm import (WebSocketMessageReceivedEvent, MoonAPI,
                                   MoonWebSocket, WebSocketConnectEvent)
from Scripts.moonrest import MoonRest

"""
    QSplashScreen
    Functions ->
        finish()
        message()
        pixmap()
        setPixmap()
        
    Virtual Functions ->
        drawContents()
        
    Slots ->
        clearMessage()
        showMessage()
        
    More Info on ->
        https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QSplashScreen.html#qsplashscreen
    
"""
    
class ConnectionWindow(QFrame):
    def __init__(self, main_window, *args, **kwargs):
        super(ConnectionWindow, self).__init__(
            parent=main_window, *args, **kwargs)
        self.main_window = main_window
        self.con_window = Ui_Form()
        self.con_window.setupUi(self)
        self.con_window.RetryConnection.clicked.connect(self.initialize)
       
        self.setStyleSheet("background-color: white;")
        self.setGeometry(self.frameRect())
        self.setEnabled(True)
        # self.setHi
        self.show()

    @pyqtSlot()
    def initialize(self):
        self.main_window.ws.start()
        self.main_window.ws.try_connection()
        self.con_window.TextFrame.setWindowIconText(
            "Connecting to Moonraker and Klipper")

    def event(self, event):
        if event.type() == WebSocketConnectEvent.wb_connect_event_type:
            # print(event.kwargs)
            self.close()
            self.main_window.show()

            return True
            # return super().event(event)
            # return self.message_received_event(event)
        return super().event(event)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        
        # self.con_window.setupUi(self)
        self.ui.setupUi(self)
        # uic.loadUi("Scripts/uiTemplate.ui", self)        In Case i want to use the .ui file

        self.start_window = ConnectionWindow(main_window=self)

        self._moonRest = MoonRest()
        self.ws = MoonWebSocket(self)

        # self.ui.pushButton_2.clicked.connect(self.initialize)
        # self.con_window..Re.clicked.connect(self.initialize)
        # self.ws.message_signal.connect(self.message)

    # This slot is called when the button is pressed, it represents
    @pyqtSlot()
    def initialize(self):
        self.ws.start()
        self.ws.try_connection()

        # if self._ws.connected:

    @pyqtSlot(name="message_received")
    def message(self):
        self.ui.pushButton_2.setText("BITCH")

    # def message_received(self, event, *args):
    #     print("Hello")

    def message_received_event(self, event):
        print("event")

    def event(self, event):
        # print(event)
        if event.type() == WebSocketMessageReceivedEvent.message_event_type:
            # print(event.kwargs)
            return True
            # return super().event(event)
            # return self.message_received_event(event)
        return super().event(event)


if __name__ == "__main__":
    
    
    app = QApplication([])
    pixmap = QPixmap("/home/bugo/github/Blocks_Screen/MEDIA/logoblocks.png")
    splash = QSplashScreen(pixmap)
    # splash.setGeometry(main_window)
    splash.showNormal()
    splash.showMessage("Loading")
    app.processEvents()
    
    # There is another way i can do this, by passing the .ui file to .py and then use that .py file in my app.
    # I can do this with the command pyuic6 -o <pythonfile>.py -x <uifile>.ui
    # Then i get a .py file from the .ui file
    main_window = MainWindow()
    main_window.show()
    splash.finish(main_window)
    sys.exit(app.exec())
