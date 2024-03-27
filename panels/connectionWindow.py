from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import  pyqtSlot,pyqtSignal
from qt_ui.connectionWindow_ui import * 

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
