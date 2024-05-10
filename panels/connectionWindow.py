import typing
from PyQt6.QtWidgets import QFrame, QTabWidget, QWidget, QStackedWidget
from PyQt6.QtCore import QEvent, QObject, pyqtSlot, pyqtSignal
from qt_ui.connectionWindow_ui import *
from scripts.events import *
from scripts.moonrakerComm import MoonWebSocket


class ConnectionWindow(QFrame):

    # @ Signals
    text_updated = pyqtSignal(int, name="connection_text_updated")
    retry_connection_clicked = pyqtSignal(name="retry_connection_clicked")
    wifi_clicked = pyqtSignal(name="wifi_clicked")
    reboot_clicked = pyqtSignal(name="reboot_clicked")
    restart_klipper_clicked = pyqtSignal(name="restart_klipper_clicked")

    def __init__(self, parent, ws: MoonWebSocket, *args, **kwargs):
        super(ConnectionWindow, self).__init__(parent, *args, **kwargs)
        self.main_window = parent
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)
        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False

        self.setGeometry(self.frameRect())
        self.setEnabled(True)
        self.show_panel()
        self.text_update()

        # @ Slot connections
        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.WifiButton.clicked.connect(self.wifi_clicked.emit)
        self.panel.RebootSystemButton.clicked.connect(self.reboot_clicked.emit)
        self.panel.RestartKlipperButton.clicked.connect(
            self.restart_klipper_clicked.emit
        )

        # TODO: Don't know if i should use these signals here or not, maybe they should be outside
        self.ws.connection_lost.connect(slot=self.show)
        self.ws.klippy_connected_signal.connect(self.klippy_connection)
        self.ws.klippy_state_signal.connect(self.klippy_state)

    def show_panel(self, reason: str | None = None):
        self.show()
        if reason is not None:
            self.text_update(reason)
            return True
        self.text_update()
        return False

    @pyqtSlot(bool)
    @pyqtSlot(name="klippy_connection")
    def klippy_connection(self, state: bool):
        pass

    @pyqtSlot(str)
    @pyqtSlot(name="klippy_state")
    def klippy_state(self, state: str):
        if state == "error":
            if not self.isVisible():
                self.show()
            self.panel.connectionTextBox.setText("Klipper Connection error")

        elif state == "startup":
            self.panel.connectionTextBox.setText("Kippy startup")
        elif state == "ready":
            self.close()

    @pyqtSlot(int)
    @pyqtSlot(str)
    @pyqtSlot(name="websocket_connecting")
    def websocket_connecting(self, attempt: int):
        print(attempt)
        self.text_update(attempt)

    @pyqtSlot(name="websocket_connection_achieved")
    def websocket_connection_achieved(self):
        self.panel.connectionTextBox.setText("Moonraker Connected\n klippy not ready")
        # # * Close this window
        # self.close()

    @pyqtSlot(name="websocket_connection_lost")
    def websocket_connection_lost(self):
        if not self.isVisible():
            self.show()
        self.text_update(text="wb lost")

    def text_update(self, text: int | str | None = None):
        if text == "wb lost":
            self.panel.connectionTextBox.setText("Moonraker connection lost.")
        if text is None:
            self.panel.connectionTextBox.setText(
                """
                Not connected to Moonrakers Websocket. 
                """
            )
            return True
        if isinstance(text, str):
            self.panel.connectionTextBox.setText(
                f"\
                Connection to Moonraker unavailable\n \
                Try again by reconnecting or \n\
                restarting klipper.\n\
                    {text}\
                "
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages
            if text == 0:
                self.panel.connectionTextBox.setText(
                    f"Unable to Connect to Moonraker. \n \
                   Try again."
                )
                return False
            self.panel.connectionTextBox.setText(
                f"Attempting to reconnect to Moonraker. \n \
                  Connection try number: {text}."
            )

        return False

    # def customEvent(self, a0: QEvent ) -> None:
    #     # * In here i know i receive custom events such as the wbesocketOpenEvent
    #     # But i'm not sending it as a custom event but as a normal one.. .
    #     # Why is that??? shouldn't i send it with customEvent method?
    #     # why is that method here if it doesn't do shit ?
    #     if a0.type() >= 65500:
    #         print(f"a custom event was received in connectionWindow:\n\t {a0.__class__} ")
    #         # print(a0.__class__)
    #         if a0.type() == KlippyDisconnectedEvent.type():
    #             print("REceived custom event klippy ready ")
    #             return False

    #     return super().customEvent(a0)

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        # print(f"Event method in connectionWindow ->\n\t Event class : {e.__class__}")
        if a1.type() == KlippyDisconnectedEvent.type():
            if not self.isVisible():
                self.show()
                self.panel.connectionTextBox.setText("Klippy is disconnected")
        elif a1.type() == KlippyReadyEvent.type():
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False
        elif a1.type() == KlippyShudownEvent.type():
            if not self.isVisible():
                self.show()
                self.panel.connectionTextBox.setText("Klippy shutdown")
                return False
        return super().eventFilter(a0, a1)
