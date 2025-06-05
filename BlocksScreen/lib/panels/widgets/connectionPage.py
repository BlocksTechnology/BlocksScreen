import logging

from events import KlippyDisconnected, KlippyReady, KlippyShutdown
from lib.moonrakerComm import MoonWebSocket
from lib.ui.connectionWindow_ui import Ui_ConnectivityForm
from PyQt6 import QtWidgets
from PyQt6.QtCore import QEvent, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QFrame


class ConnectionPage(QFrame):
    # @ Signals
    text_updated = pyqtSignal(int, name="connection_text_updated")
    retry_connection_clicked = pyqtSignal(name="retry_connection_clicked")
    wifi_button_clicked = pyqtSignal(name="call_network_page")
    reboot_clicked = pyqtSignal(name="reboot_clicked")
    restart_klipper_clicked = pyqtSignal(name="restart_klipper_clicked")
    firmware_restart_clicked = pyqtSignal(name="firmware_restart_clicked")

    def __init__(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)
        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.installEventFilter(self.parent())

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
        self.ws.klippy_connected_signal.connect(self.on_klippy_connection)
        self.ws.klippy_state_signal.connect(self.on_klippy_state)

    def show_panel(self, reason: str | None = None):
        self.show()
        if reason is not None:
            self.text_update(reason)
            return True
        self.text_update()
        return False

    @pyqtSlot(bool, name="klippy_connection")
    def on_klippy_connection(self, state: bool):
        pass

    @pyqtSlot(str, name="on_klippy_state")
    def on_klippy_state(self, state: str):
        if state == "error":
            self.panel.connectionTextBox.setText("Klipper Connection Error")
            if not self.isVisible():
                self.show()
        elif state == "disconnected":
            self.panel.connectionTextBox.setText("Klipper Disconnected")

            if not self.isVisible():
                self.show()

        elif state == "shutdown":
            self.panel.connectionTextBox.setText("Klipper reports: SHUTDOWN")
            if not self.isVisible():
                self.show()
        elif state == "startup":
            self.panel.connectionTextBox.setText("Klipper Startup")
        elif state == "ready":
            self.panel.connectionTextBox.setText("Klipper Ready")
            self.hide()

    @pyqtSlot(int, name="on_websocket_connecting")
    @pyqtSlot(str, name="on_websocket_connecting")
    def on_websocket_connecting(self, attempt: int):
        self.text_update(attempt)

    @pyqtSlot(name="on_websocket_connection_achieved")
    def on_websocket_connection_achieved(self):
        self.panel.connectionTextBox.setText(
            "Moonraker Connected\n Klippy not ready"
        )
        self.hide()

    @pyqtSlot(name="on_websocket_connection_lost")
    def on_websocket_connection_lost(self):
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
        if event.type() == KlippyDisconnected.type():
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy shutdown")
                self.show()
                return True

        return super().eventFilter(object, event)
