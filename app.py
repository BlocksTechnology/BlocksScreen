import sys
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSplashScreen)
from PyQt6.QtGui import QPixmap

from scripts.moonrakerComm import (WebSocketMessageReceivedEvent, MoonWebSocket)
from scripts.moonrest import MoonRest



# * Panels
from panels.connectionWindow import ConnectionWindow
from panels.printTab import PrintTab

from panels.controlTab import ControlTab
from panels.filamentTab import FilamentTab
from panels.utilitiesTab import UtilitiesTab


from resources.background_resources_rc import *
from resources.button_resources_rc import *
from resources.main_menu_resources_rc import *
from resources.system_resources_rc import *

from qt_ui.Blocks_Screen_Lemos_ui import Ui_MainWindow
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


class MainWindow(QMainWindow):
    app_initialize = pyqtSignal(name="app-start-websocket-connection")

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

        # @ Panels 
        self.printPanel = PrintTab(self.ui.printTab)
        self.filamentPanel = FilamentTab(self.ui.filamentTab)
        self.controlPanel = ControlTab(self.ui.controlTab)
        self.utilitiesPanel = UtilitiesTab(self.ui.utilitiesTab)
        
        # @ Slot connections
        self.app_initialize.connect(slot=self.initialize_websocket_connection)
        self.ws.connected_signal.connect(slot= self.start_window.websocket_connection_achieved)
        
        # self.start_window.text_updated.connect(self.text_has_been_updated)
        # self.ws.connection_lost.connect(slot= self.start_window.show_panel)
    # This slot is called when the button is pressed, it represents

    

    @pyqtSlot(name="app-start-websocket-connection")
    def initialize_websocket_connection(self):
        self.ws.start()
        self.ws.try_connection()

    @pyqtSlot(str)
    @pyqtSlot(name="websocket-connection-lost")
    def websocket_connection_lost(self, reason:str):
        self.start_window.show_panel(reason)


    # @pyqtSlot(name
    def event(self, event):
        if event.type() == WebSocketMessageReceivedEvent.message_event_type:  # TODO: This will go to another place
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
    
    # @ Someone said that .processEvents sometimes crashes the system
    app.processEvents()

    # There is another way i can do this, by passing the .ui file to .py and then use that .py file in my app.
    # I can do this with the command pyuic6 -o <pythonfile>.py -x <uifile>.ui
    # Then i get a .py file from the .ui file
    main_window = MainWindow()
    main_window.show()
    main_window.app_initialize.emit()
    splash.finish(main_window)
    sys.exit(app.exec())





""" 
    MECANISMO NR 1
    
        Eventos -> ser rapidos ou ter um queue 

            rapidos -> sendEvent(local, event)
            queue -> postEvent()


        Podem ser vistos em qualquer parte do programa ou podem ser explicitamente transmitidos
        para uma classe.
        
        
        Qualquer classe que seja um "child" de uma outra do QT
        
            def event(self, event):         Sempre chamada quando existe um event 
                <qualquer coisa>
        
    MECANISMO NR 2 
    
        SINALS & SLOTS 
    
        
"""
