import logging

from events import KlippyDisconnected, KlippyReady, KlippyShutdown
from lib.moonrakerComm import MoonWebSocket
from lib.ui.connectionWindow_ui import Ui_ConnectivityForm
from PyQt6 import QtCore, QtWidgets


class ConnectionPage(QtWidgets.QFrame):
    text_updated = QtCore.pyqtSignal(int, name="connection_text_updated")
    retry_connection_clicked = QtCore.pyqtSignal(name="retry_connection_clicked")
    wifi_button_clicked = QtCore.pyqtSignal(name="call_network_page")
    reboot_clicked = QtCore.pyqtSignal(name="reboot_clicked")
    restart_klipper_clicked = QtCore.pyqtSignal(name="restart_klipper_clicked")
    firmware_restart_clicked = QtCore.pyqtSignal(name="firmware_restart_clicked")

    def __init__(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)
        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

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
        self.ws.klippy_connected_signal.connect(self.on_klippy_connected)
        self.ws.klippy_state_signal.connect(self.on_klippy_state)

    def show_panel(self, reason: str | None = None):
        """Show widget"""
        self.show()
        if reason is not None:
            self.text_update(reason)
            return True
        self.text_update()
        return False

    @QtCore.pyqtSlot(bool, name="on_klippy_connected")
    def on_klippy_connection(self, connected: bool):
        """Handle klippy connection state"""
        self._klippy_connection = connected
        if not connected:
            self.panel.connectionTextBox.setText("Klipper Disconnected")
            if not self.isVisible():
                self.show()
        else:
            self.panel.connectionTextBox.setText("Klipper Connected")

    @QtCore.pyqtSlot(str, name="on_klippy_state")
    def on_klippy_state(self, state: str):
        """Handle klippy state changes"""
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

    @QtCore.pyqtSlot(int, name="on_websocket_connecting")
    @QtCore.pyqtSlot(str, name="on_websocket_connecting")
    def on_websocket_connecting(self, attempt: int):
        """Handle websocket connecting state"""
        self.text_update(attempt)

    @QtCore.pyqtSlot(name="on_websocket_connection_achieved")
    def on_websocket_connection_achieved(self):
        """Handle websocket connected state"""
        self.panel.connectionTextBox.setText("Moonraker Connected\n Klippy not ready")
        self.hide()

    @QtCore.pyqtSlot(name="on_websocket_connection_lost")
    def on_websocket_connection_lost(self):
        """Handle websocket connection lost state"""
        if not self.isVisible():
            self.show()
        self.text_update(text="Websocket lost")

    def text_update(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False

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
                f"""
                Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}
                """
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages
            if text == 0:
                self.dot_timer.stop()
                self.panel.connectionTextBox.setText(
                    "Unable to Connect to Moonraker.\n\nTry again"
                )
                return False

            if text == 1:
                if self.dot_timer.isActive():
                    self.dot_timer.stop()
                    return
                self.dot_timer.start()

            self.text2 = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

        return False

    def _add_dot(self):
        if self.state == "shutdown" and self.message is not None:
            self.dot_timer.stop()
            return False

        if self.dot_count > 2:
            self.dot_count = 1
        else:
            self.dot_count += 1
        dots = "." * self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.text2}{dots}")

    @QtCore.pyqtSlot(str, str, name="webhooks_update")
    def webhook_update(self, state: str, message: str):
        """Handle websocket webhook updates"""
        self.state = state
        self.message = message
        self.text_update()

    def eventFilter(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
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
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)
