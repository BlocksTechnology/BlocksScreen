import logging
import sys
import PyQt6
from PyQt6 import uic
from PyQt6.QtCore import QEvent, QEventLoop, QObject, Qt, pyqtSignal, pyqtSlot, QCoreApplication
from PyQt6.QtWidgets import (QApplication, QDockWidget, QFrame, QMainWindow, QSplashScreen,
                             QWidget, QPushButton)
from PyQt6.QtGui import QColor, QPixmap
from qt_ui.Blocks_Screen_Lemos_ui import Ui_MainWindow
from qt_ui.connectionWindow_ui import Ui_ConnectivityForm
from scripts.moonrakerComm import (WebSocketMessageReceivedEvent, MoonAPI,
                                   MoonWebSocket, WebSocketConnectingEvent, WebSocketOpenEvent)
from scripts.moonrest import MoonRest
from resources import UI_Resources_rc
from qt_ui.ui_util import CustomQPushButton

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
        self.con_window = Ui_ConnectivityForm()
        self.con_window.setupUi(self)
        
        # self.con_window.RestartKlipperButton.clicked.connect(self.yo)
        # self.newButton.setIcon(self)
        self.setGeometry(self.frameRect())
        self.setEnabled(True)
        self.show()
    
    @pyqtSlot(name="App-start")
    def initialize(self):
        print("HLELL")
        self.main_window.ws.start()
        self.main_window.ws.try_connection()

    
    @pyqtSlot(int)
    @pyqtSlot(name="update-text")
    def text_update(self, reconnect_count):
        if reconnect_count == 0:
            self.con_window.connectionTextBox.setText("""
                Unable to Connect to moonraker websocket\n
                \t Try again by reconnecting or \n
                \t restarting klipper.
                                                      """)
            return True
        self.con_window.connectionTextBox.setText(
            f"Connecting to Moonraker and Klipper. \n \
                Connection Try number {reconnect_count}.")
        return False
    
    # def event(self, event):
    #     if event.type() == WebSocketConnectingEvent.wb_connecting_event_type:
    #         # print(event.kwargs)
    #         # self.close()
    #         # self.main_window.show()

    #         return True
    #         # return super().event(event)
    #         # return self.message_received_event(event)
    #     # elif event.type() == WebSoc
    #     return super().event(event)


class MainWindow(QMainWindow):
    app_initialize = pyqtSignal(name="App-start")

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
        
        # @ Slot connections
        self.app_initialize.connect(slot=self.start_window.initialize)

    # This slot is called when the button is pressed, it represents

    @pyqtSlot()
    def initialize(self):
        self.ws.start()
        self.ws.try_connection()

        # if self._ws.connected:

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
    pixmap = QPixmap("Blocks_Screen/media/logoblocks.png")
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
    main_window.app_initialize.emit()
    splash.finish(main_window)
    sys.exit(app.exec())
