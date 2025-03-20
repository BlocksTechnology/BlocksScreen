import logging

from PyQt6.QtCore import QEvent, QObject, pyqtSignal, pyqtSlot
from PyQt6 import QtGui
from PyQt6.QtWidgets import QFrame

from events import KlippyDisconnected, KlippyReady, KlippyShutdown
from lib.moonrakerComm import MoonWebSocket

from lib.ui.connectionWindow_ui import Ui_ConnectivityForm


class ConnectionWindow(QFrame):
    # @ Signals
    text_updated = pyqtSignal(int, name="connection_text_updated")
    retry_connection_clicked = pyqtSignal(name="retry_connection_clicked")
    wifi_button_clicked = pyqtSignal(name="call_network_page")
    reboot_clicked = pyqtSignal(name="reboot_clicked")
    restart_klipper_clicked = pyqtSignal(name="restart_klipper_clicked")
    firmware_restart_clicked = pyqtSignal(name="firmware_restart_clicked")

    def __init__(self, parent, ws: MoonWebSocket, *args, **kwargs):
        super(ConnectionWindow, self).__init__(parent, *args, **kwargs)
        self.main_window = parent
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)
        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.installEventFilter(self.main_window)
        # self.text_update()

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.FirmwareRestartButton.clicked.connect(
            self.firmware_restart_clicked.emit
        )
        self.panel.RebootSystemButton.clicked.connect(self.reboot_clicked.emit)
        self.panel.RestartKlipperButton.clicked.connect(
            self.restart_klipper_clicked.emit
        )
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

    @pyqtSlot(bool, name="klippy_connection")
    def klippy_connection(self, state: bool):
        pass

    @pyqtSlot(str, name="klippy_state")
    def klippy_state(self, state: str):
        if state == "error":
            if not self.isVisible():
                self.show()
            self.panel.connectionTextBox.setText("Klipper Connection Error")

        elif state == "startup":
            self.panel.connectionTextBox.setText("Klipper Startup")
        elif state == "ready":
            self.panel.connectionTextBox.setText("Klipper Ready")
            self.hide()

    @pyqtSlot(int, name="websocket_connecting")
    @pyqtSlot(str, name="websocket_connecting")
    def websocket_connecting(self, attempt: int):
        self.text_update(attempt)

    @pyqtSlot(name="websocket_connection_achieved")
    def websocket_connection_achieved(self):
        self.panel.connectionTextBox.setText("Moonraker Connected\n Klippy not ready")
        self.hide()

    @pyqtSlot(name="websocket_connection_lost")
    def websocket_connection_lost(self):
        if not self.isVisible():
            self.show()
        self.text_update(text="Websocket lost")

    def text_update(self, text: int | str | None = None):
        logging.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "wb lost":
            self.panel.connectionTextBox.setText("Moonraker connection lost")
        if text is None:
            self.panel.connectionTextBox.setText(
                """
                Not connected to Moonraker Websocket
                """
            )
            return True
        if isinstance(text, str):
            self.panel.connectionTextBox.setText(
                f"\
                Connection to Moonraker unavailable\n \
                Try again by reconnecting or \n\
                restarting klipper\n\
                    {text}\
                "
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages
            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Unable to Connect to Moonraker. \n \
                   Try again"
                )
                return False
            self.panel.connectionTextBox.setText(
                f"Attempting to reconnect to Moonraker. \n \
                  Connection try number: {text}"
            )

        return False

    def eventFilter(self, object: QObject, event: QEvent) -> bool:
        if event is None:
            return super().eventFilter(object, event)

        if event.type() == KlippyDisconnected.type():
            if not self.isVisible():
                self.show()
                self.panel.connectionTextBox.setText("Klippy is disconnected")
        elif event.type() == KlippyReady.type():
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            if not self.isVisible():
                self.show()
                self.panel.connectionTextBox.setText("Klippy shutdown")
                return True

        return super().eventFilter(object, event)
