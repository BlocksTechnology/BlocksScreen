from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from qt_ui.connectionWindow_ui import *


class ConnectionWindow(QFrame):
    
    text_updated = pyqtSignal(int,name="connection-text-updated")
    
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

        self.text_update()
        # @ Slot connections
        self.con_window.RetryConnectionButton.clicked.connect(
            self.retry_connection)
        
        # self.con_window.RebootSystemButton.clicked.connect(
        #     self.text_has_been_updated
        # )
        
        # TODO: self.con_window.RestartKlipperButton.clicked.connect()
        # TODO: self.con_window.WifiButton.clicked.connect()

    # def text_has_been_updated(self):
    #     print("HEllo")
        
    def show_panel(self, reason: str = None):
        self.show()
        if reason is not None:
            self.text_update(reason)
            return True
        self.text_update()
        return False

    @pyqtSlot(name="retry-websocket-connection")
    def retry_connection(self):
        self.main_window.ws.retry()

    @pyqtSlot(int)
    @pyqtSlot(str)
    @pyqtSlot(name="update-text")
    def text_update(self, text: int | str = None):
        if text is None:
            self.con_window.connectionTextBox.setText("""
                Connecting to Moonrakers Websocket.
                                                      """)
        if text == 0:
            self.con_window.connectionTextBox.setText("""
                Unable to Connect to moonraker websocket\n
                 Try again by reconnecting or \n
                 restarting klipper.
                                                      """)
            return True
        self.con_window.connectionTextBox.setText(
            f"Connecting to Moonraker and Klipper. \n \
                Connection Try number {text}.")
        
        return False

    @pyqtSlot(name="websocket-connected")
    def websocket_connection_achieved(self):
        # * Close this window
        self.close()
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
