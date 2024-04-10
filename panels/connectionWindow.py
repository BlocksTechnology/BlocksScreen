import typing
from PyQt6.QtWidgets import QFrame, QTabWidget, QWidget, QStackedWidget
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from qt_ui.connectionWindow_ui import *


class ConnectionWindow(QFrame):

    # @ Signals
    text_updated = pyqtSignal(int, name="connection_text_updated")
    retry_connection_clicked = pyqtSignal(name="retry_connection_clicked")
    wifi_clicked = pyqtSignal(name="wifi_clicked")
    reboot_clicked = pyqtSignal(name="reboot_clicked")
    restart_klipper_clicked = pyqtSignal(name="restart_klipper_clicked")

    def __init__(self, parent, *args, **kwargs):
        super(ConnectionWindow, self).__init__(parent, *args, **kwargs)
        self.main_window = parent
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

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

    def show_panel(self, reason: str | None = None):
        self.show()
        if reason is not None:
            self.text_update(reason)
            return True
        self.text_update()
        return False

    @pyqtSlot(int)
    @pyqtSlot(str)
    @pyqtSlot(name="text_update")
    def text_update(self, text: int | str | None = None):
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

    @pyqtSlot(name="websocket_connected_achieved")
    def websocket_connection_achieved(self):
        # * Close this window
        self.close()
