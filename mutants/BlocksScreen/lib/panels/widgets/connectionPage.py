import logging

from events import KlippyDisconnected, KlippyReady, KlippyShutdown
from lib.moonrakerComm import MoonWebSocket
from lib.ui.connectionWindow_ui import Ui_ConnectivityForm
from PyQt6 import QtCore, QtWidgets

logger = logging.getLogger(__name__)
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class ConnectionPage(QtWidgets.QFrame):
    text_updated = QtCore.pyqtSignal(int, name="connection_text_updated")
    retry_connection_clicked = QtCore.pyqtSignal(name="retry_connection_clicked")
    wifi_button_clicked = QtCore.pyqtSignal(name="call_network_page")
    reboot_clicked = QtCore.pyqtSignal(name="reboot_clicked")
    restart_klipper_clicked = QtCore.pyqtSignal(name="restart_klipper_clicked")
    firmware_restart_clicked = QtCore.pyqtSignal(name="firmware_restart_clicked")
    update_button_clicked = QtCore.pyqtSignal(bool, name="show-update-page")
    notification_btn_clicked = QtCore.pyqtSignal(name="notification_btn_clicked")
    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")
    call_cancel_panel = QtCore.pyqtSignal(bool, name="call-load-panel")

    def __init__(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        args = [parent, ws]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConnectionPageǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁConnectionPageǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁConnectionPageǁ__init____mutmut_orig(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_1(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(None)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_2(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(None)
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_3(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(None, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_4(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, None))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_5(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_6(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, ))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_7(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(801, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_8(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 481))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_9(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = None
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_10(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(None)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_11(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            None
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_12(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: None
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_13(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(None)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_14(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(False)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_15(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = None
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_16(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = None
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_17(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "XXdisconnectedXX"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_18(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "DISCONNECTED"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_19(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = None
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_20(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "XXclosedXX"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_21(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "CLOSED"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_22(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = None
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_23(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = True
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_24(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = None
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_25(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "XXshutdownXX"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_26(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "SHUTDOWN"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_27(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = None
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_28(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 1
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_29(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = ""
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_30(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = None
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_31(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = False
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_32(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = None
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_33(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(None)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_34(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(None)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_35(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1001)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_36(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(None)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_37(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(None)

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_38(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            None
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_39(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(None)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
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

    def xǁConnectionPageǁ__init____mutmut_40(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(None)
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

    def xǁConnectionPageǁ__init____mutmut_41(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
        self.panel.FirmwareRestartButton.clicked.connect(
            None
        )
        self.panel.RebootSystemButton.clicked.connect(self.reboot_clicked.emit)
        self.panel.RestartKlipperButton.clicked.connect(
            self.restart_klipper_clicked.emit
        )
        self.ws.connection_lost.connect(slot=self.show)
        self.ws.klippy_connected_signal.connect(self.on_klippy_connected)
        self.ws.klippy_state_signal.connect(self.on_klippy_state)

    def xǁConnectionPageǁ__init____mutmut_42(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
        self.panel.FirmwareRestartButton.clicked.connect(
            self.firmware_restart_clicked.emit
        )
        self.panel.RebootSystemButton.clicked.connect(None)
        self.panel.RestartKlipperButton.clicked.connect(
            self.restart_klipper_clicked.emit
        )
        self.ws.connection_lost.connect(slot=self.show)
        self.ws.klippy_connected_signal.connect(self.on_klippy_connected)
        self.ws.klippy_state_signal.connect(self.on_klippy_state)

    def xǁConnectionPageǁ__init____mutmut_43(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
        self.panel.FirmwareRestartButton.clicked.connect(
            self.firmware_restart_clicked.emit
        )
        self.panel.RebootSystemButton.clicked.connect(self.reboot_clicked.emit)
        self.panel.RestartKlipperButton.clicked.connect(
            None
        )
        self.ws.connection_lost.connect(slot=self.show)
        self.ws.klippy_connected_signal.connect(self.on_klippy_connected)
        self.ws.klippy_state_signal.connect(self.on_klippy_state)

    def xǁConnectionPageǁ__init____mutmut_44(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
        self.panel.FirmwareRestartButton.clicked.connect(
            self.firmware_restart_clicked.emit
        )
        self.panel.RebootSystemButton.clicked.connect(self.reboot_clicked.emit)
        self.panel.RestartKlipperButton.clicked.connect(
            self.restart_klipper_clicked.emit
        )
        self.ws.connection_lost.connect(slot=None)
        self.ws.klippy_connected_signal.connect(self.on_klippy_connected)
        self.ws.klippy_state_signal.connect(self.on_klippy_state)

    def xǁConnectionPageǁ__init____mutmut_45(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
        self.panel.FirmwareRestartButton.clicked.connect(
            self.firmware_restart_clicked.emit
        )
        self.panel.RebootSystemButton.clicked.connect(self.reboot_clicked.emit)
        self.panel.RestartKlipperButton.clicked.connect(
            self.restart_klipper_clicked.emit
        )
        self.ws.connection_lost.connect(slot=self.show)
        self.ws.klippy_connected_signal.connect(None)
        self.ws.klippy_state_signal.connect(self.on_klippy_state)

    def xǁConnectionPageǁ__init____mutmut_46(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.panel = Ui_ConnectivityForm()
        self.panel.setupUi(self)

        self.panel.updatepageButton.clicked.connect(
            lambda: self.update_button_clicked[bool].emit(True)
        )

        self.ws = ws
        self._moonraker_status: str = "disconnected"
        self._klippy_state: str = "closed"
        self._klippy_connection: bool = False
        self.state = "shutdown"
        self.dot_count = 0
        self.message = None
        self.conn_toggle: bool = True
        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self.installEventFilter(self.parent())

        self.panel.RetryConnectionButton.clicked.connect(
            self.retry_connection_clicked.emit
        )
        self.panel.wifi_button.clicked.connect(self.wifi_button_clicked.emit)
        self.panel.notification_btn.clicked.connect(self.notification_btn_clicked.emit)
        self.panel.FirmwareRestartButton.clicked.connect(
            self.firmware_restart_clicked.emit
        )
        self.panel.RebootSystemButton.clicked.connect(self.reboot_clicked.emit)
        self.panel.RestartKlipperButton.clicked.connect(
            self.restart_klipper_clicked.emit
        )
        self.ws.connection_lost.connect(slot=self.show)
        self.ws.klippy_connected_signal.connect(self.on_klippy_connected)
        self.ws.klippy_state_signal.connect(None)
    
    xǁConnectionPageǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConnectionPageǁ__init____mutmut_1': xǁConnectionPageǁ__init____mutmut_1, 
        'xǁConnectionPageǁ__init____mutmut_2': xǁConnectionPageǁ__init____mutmut_2, 
        'xǁConnectionPageǁ__init____mutmut_3': xǁConnectionPageǁ__init____mutmut_3, 
        'xǁConnectionPageǁ__init____mutmut_4': xǁConnectionPageǁ__init____mutmut_4, 
        'xǁConnectionPageǁ__init____mutmut_5': xǁConnectionPageǁ__init____mutmut_5, 
        'xǁConnectionPageǁ__init____mutmut_6': xǁConnectionPageǁ__init____mutmut_6, 
        'xǁConnectionPageǁ__init____mutmut_7': xǁConnectionPageǁ__init____mutmut_7, 
        'xǁConnectionPageǁ__init____mutmut_8': xǁConnectionPageǁ__init____mutmut_8, 
        'xǁConnectionPageǁ__init____mutmut_9': xǁConnectionPageǁ__init____mutmut_9, 
        'xǁConnectionPageǁ__init____mutmut_10': xǁConnectionPageǁ__init____mutmut_10, 
        'xǁConnectionPageǁ__init____mutmut_11': xǁConnectionPageǁ__init____mutmut_11, 
        'xǁConnectionPageǁ__init____mutmut_12': xǁConnectionPageǁ__init____mutmut_12, 
        'xǁConnectionPageǁ__init____mutmut_13': xǁConnectionPageǁ__init____mutmut_13, 
        'xǁConnectionPageǁ__init____mutmut_14': xǁConnectionPageǁ__init____mutmut_14, 
        'xǁConnectionPageǁ__init____mutmut_15': xǁConnectionPageǁ__init____mutmut_15, 
        'xǁConnectionPageǁ__init____mutmut_16': xǁConnectionPageǁ__init____mutmut_16, 
        'xǁConnectionPageǁ__init____mutmut_17': xǁConnectionPageǁ__init____mutmut_17, 
        'xǁConnectionPageǁ__init____mutmut_18': xǁConnectionPageǁ__init____mutmut_18, 
        'xǁConnectionPageǁ__init____mutmut_19': xǁConnectionPageǁ__init____mutmut_19, 
        'xǁConnectionPageǁ__init____mutmut_20': xǁConnectionPageǁ__init____mutmut_20, 
        'xǁConnectionPageǁ__init____mutmut_21': xǁConnectionPageǁ__init____mutmut_21, 
        'xǁConnectionPageǁ__init____mutmut_22': xǁConnectionPageǁ__init____mutmut_22, 
        'xǁConnectionPageǁ__init____mutmut_23': xǁConnectionPageǁ__init____mutmut_23, 
        'xǁConnectionPageǁ__init____mutmut_24': xǁConnectionPageǁ__init____mutmut_24, 
        'xǁConnectionPageǁ__init____mutmut_25': xǁConnectionPageǁ__init____mutmut_25, 
        'xǁConnectionPageǁ__init____mutmut_26': xǁConnectionPageǁ__init____mutmut_26, 
        'xǁConnectionPageǁ__init____mutmut_27': xǁConnectionPageǁ__init____mutmut_27, 
        'xǁConnectionPageǁ__init____mutmut_28': xǁConnectionPageǁ__init____mutmut_28, 
        'xǁConnectionPageǁ__init____mutmut_29': xǁConnectionPageǁ__init____mutmut_29, 
        'xǁConnectionPageǁ__init____mutmut_30': xǁConnectionPageǁ__init____mutmut_30, 
        'xǁConnectionPageǁ__init____mutmut_31': xǁConnectionPageǁ__init____mutmut_31, 
        'xǁConnectionPageǁ__init____mutmut_32': xǁConnectionPageǁ__init____mutmut_32, 
        'xǁConnectionPageǁ__init____mutmut_33': xǁConnectionPageǁ__init____mutmut_33, 
        'xǁConnectionPageǁ__init____mutmut_34': xǁConnectionPageǁ__init____mutmut_34, 
        'xǁConnectionPageǁ__init____mutmut_35': xǁConnectionPageǁ__init____mutmut_35, 
        'xǁConnectionPageǁ__init____mutmut_36': xǁConnectionPageǁ__init____mutmut_36, 
        'xǁConnectionPageǁ__init____mutmut_37': xǁConnectionPageǁ__init____mutmut_37, 
        'xǁConnectionPageǁ__init____mutmut_38': xǁConnectionPageǁ__init____mutmut_38, 
        'xǁConnectionPageǁ__init____mutmut_39': xǁConnectionPageǁ__init____mutmut_39, 
        'xǁConnectionPageǁ__init____mutmut_40': xǁConnectionPageǁ__init____mutmut_40, 
        'xǁConnectionPageǁ__init____mutmut_41': xǁConnectionPageǁ__init____mutmut_41, 
        'xǁConnectionPageǁ__init____mutmut_42': xǁConnectionPageǁ__init____mutmut_42, 
        'xǁConnectionPageǁ__init____mutmut_43': xǁConnectionPageǁ__init____mutmut_43, 
        'xǁConnectionPageǁ__init____mutmut_44': xǁConnectionPageǁ__init____mutmut_44, 
        'xǁConnectionPageǁ__init____mutmut_45': xǁConnectionPageǁ__init____mutmut_45, 
        'xǁConnectionPageǁ__init____mutmut_46': xǁConnectionPageǁ__init____mutmut_46
    }
    xǁConnectionPageǁ__init____mutmut_orig.__name__ = 'xǁConnectionPageǁ__init__'

    @QtCore.pyqtSlot(bool, name="toggle_connection_page")
    def set_toggle(self, toggle: bool):
        """Toggle connection page showing or not"""
        self.conn_toggle = toggle

    def show_panel(self, reason: str | None = None):
        args = [reason]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConnectionPageǁshow_panel__mutmut_orig'), object.__getattribute__(self, 'xǁConnectionPageǁshow_panel__mutmut_mutants'), args, kwargs, self)

    def xǁConnectionPageǁshow_panel__mutmut_orig(self, reason: str | None = None):
        """Show widget"""
        self.show()
        if reason is not None:
            self.text_update(reason)
            return True
        self.text_update()
        return False

    def xǁConnectionPageǁshow_panel__mutmut_1(self, reason: str | None = None):
        """Show widget"""
        self.show()
        if reason is None:
            self.text_update(reason)
            return True
        self.text_update()
        return False

    def xǁConnectionPageǁshow_panel__mutmut_2(self, reason: str | None = None):
        """Show widget"""
        self.show()
        if reason is not None:
            self.text_update(None)
            return True
        self.text_update()
        return False

    def xǁConnectionPageǁshow_panel__mutmut_3(self, reason: str | None = None):
        """Show widget"""
        self.show()
        if reason is not None:
            self.text_update(reason)
            return False
        self.text_update()
        return False

    def xǁConnectionPageǁshow_panel__mutmut_4(self, reason: str | None = None):
        """Show widget"""
        self.show()
        if reason is not None:
            self.text_update(reason)
            return True
        self.text_update()
        return True
    
    xǁConnectionPageǁshow_panel__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConnectionPageǁshow_panel__mutmut_1': xǁConnectionPageǁshow_panel__mutmut_1, 
        'xǁConnectionPageǁshow_panel__mutmut_2': xǁConnectionPageǁshow_panel__mutmut_2, 
        'xǁConnectionPageǁshow_panel__mutmut_3': xǁConnectionPageǁshow_panel__mutmut_3, 
        'xǁConnectionPageǁshow_panel__mutmut_4': xǁConnectionPageǁshow_panel__mutmut_4
    }
    xǁConnectionPageǁshow_panel__mutmut_orig.__name__ = 'xǁConnectionPageǁshow_panel'

    def showEvent(self, a0: QtCore.QEvent | None):
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConnectionPageǁshowEvent__mutmut_orig'), object.__getattribute__(self, 'xǁConnectionPageǁshowEvent__mutmut_mutants'), args, kwargs, self)

    def xǁConnectionPageǁshowEvent__mutmut_orig(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(False, "")
            self.call_cancel_panel.emit(False)
            return super().showEvent(a0)

    def xǁConnectionPageǁshowEvent__mutmut_1(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(None, "")
            self.call_cancel_panel.emit(False)
            return super().showEvent(a0)

    def xǁConnectionPageǁshowEvent__mutmut_2(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(False, None)
            self.call_cancel_panel.emit(False)
            return super().showEvent(a0)

    def xǁConnectionPageǁshowEvent__mutmut_3(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit("")
            self.call_cancel_panel.emit(False)
            return super().showEvent(a0)

    def xǁConnectionPageǁshowEvent__mutmut_4(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(False, )
            self.call_cancel_panel.emit(False)
            return super().showEvent(a0)

    def xǁConnectionPageǁshowEvent__mutmut_5(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(True, "")
            self.call_cancel_panel.emit(False)
            return super().showEvent(a0)

    def xǁConnectionPageǁshowEvent__mutmut_6(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(False, "XXXX")
            self.call_cancel_panel.emit(False)
            return super().showEvent(a0)

    def xǁConnectionPageǁshowEvent__mutmut_7(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(False, "")
            self.call_cancel_panel.emit(None)
            return super().showEvent(a0)

    def xǁConnectionPageǁshowEvent__mutmut_8(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(False, "")
            self.call_cancel_panel.emit(True)
            return super().showEvent(a0)

    def xǁConnectionPageǁshowEvent__mutmut_9(self, a0: QtCore.QEvent | None):
        """Handle show event"""
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(False, "")
            self.call_cancel_panel.emit(False)
            return super().showEvent(None)
    
    xǁConnectionPageǁshowEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConnectionPageǁshowEvent__mutmut_1': xǁConnectionPageǁshowEvent__mutmut_1, 
        'xǁConnectionPageǁshowEvent__mutmut_2': xǁConnectionPageǁshowEvent__mutmut_2, 
        'xǁConnectionPageǁshowEvent__mutmut_3': xǁConnectionPageǁshowEvent__mutmut_3, 
        'xǁConnectionPageǁshowEvent__mutmut_4': xǁConnectionPageǁshowEvent__mutmut_4, 
        'xǁConnectionPageǁshowEvent__mutmut_5': xǁConnectionPageǁshowEvent__mutmut_5, 
        'xǁConnectionPageǁshowEvent__mutmut_6': xǁConnectionPageǁshowEvent__mutmut_6, 
        'xǁConnectionPageǁshowEvent__mutmut_7': xǁConnectionPageǁshowEvent__mutmut_7, 
        'xǁConnectionPageǁshowEvent__mutmut_8': xǁConnectionPageǁshowEvent__mutmut_8, 
        'xǁConnectionPageǁshowEvent__mutmut_9': xǁConnectionPageǁshowEvent__mutmut_9
    }
    xǁConnectionPageǁshowEvent__mutmut_orig.__name__ = 'xǁConnectionPageǁshowEvent'

    @QtCore.pyqtSlot(bool, name="on_klippy_connected")
    def on_klippy_connection(self, connected: bool):
        """Handle klippy connection state"""
        self.dot_timer.stop()

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
        self.dot_timer.stop()
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

    @QtCore.pyqtSlot(int, name="on_websocket_connecting")
    @QtCore.pyqtSlot(str, name="on_websocket_connecting")
    def on_websocket_connecting(self, attempt: int):
        """Handle websocket connecting state"""
        self.text_update(attempt)

    @QtCore.pyqtSlot(name="on_websocket_connection_achieved")
    def on_websocket_connection_achieved(self):
        """Handle websocket connected state"""
        self.dot_timer.stop()
        self.panel.connectionTextBox.setText("Moonraker Connected\n Klippy not ready")

    @QtCore.pyqtSlot(name="on_websocket_connection_lzost")
    def on_websocket_connection_lost(self):
        """Handle websocket connection lost state"""
        if not self.isVisible():
            self.show()
        self.dot_timer.stop()
        self.text_update(text="Websocket lost")

    def text_update(self, text: int | str | None = None):
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConnectionPageǁtext_update__mutmut_orig'), object.__getattribute__(self, 'xǁConnectionPageǁtext_update__mutmut_mutants'), args, kwargs, self)

    def xǁConnectionPageǁtext_update__mutmut_orig(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_1(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" or self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_2(self, text: int | str | None = None):
        """Update widget text"""
        if self.state != "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_3(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "XXshutdownXX" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_4(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "SHUTDOWN" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_5(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_6(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return True
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_7(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(None)
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_8(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text != "wb lost":
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_9(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "XXwb lostXX":
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_10(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "WB LOST":
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_11(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "wb lost":
            self.panel.connectionTextBox.setText(None)
        if text is None:
            self.panel.connectionTextBox.setText(
                """
                Not connected to Moonraker Websocket
                """
            )
            return True
        if isinstance(text, str):
            self.panel.connectionTextBox.setText(
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_12(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "wb lost":
            self.panel.connectionTextBox.setText("XXMoonraker connection lostXX")
        if text is None:
            self.panel.connectionTextBox.setText(
                """
                Not connected to Moonraker Websocket
                """
            )
            return True
        if isinstance(text, str):
            self.panel.connectionTextBox.setText(
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_13(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "wb lost":
            self.panel.connectionTextBox.setText("moonraker connection lost")
        if text is None:
            self.panel.connectionTextBox.setText(
                """
                Not connected to Moonraker Websocket
                """
            )
            return True
        if isinstance(text, str):
            self.panel.connectionTextBox.setText(
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_14(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "wb lost":
            self.panel.connectionTextBox.setText("MOONRAKER CONNECTION LOST")
        if text is None:
            self.panel.connectionTextBox.setText(
                """
                Not connected to Moonraker Websocket
                """
            )
            return True
        if isinstance(text, str):
            self.panel.connectionTextBox.setText(
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_15(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "wb lost":
            self.panel.connectionTextBox.setText("Moonraker connection lost")
        if text is not None:
            self.panel.connectionTextBox.setText(
                """
                Not connected to Moonraker Websocket
                """
            )
            return True
        if isinstance(text, str):
            self.panel.connectionTextBox.setText(
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_16(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "wb lost":
            self.panel.connectionTextBox.setText("Moonraker connection lost")
        if text is None:
            self.panel.connectionTextBox.setText(
                None
            )
            return True
        if isinstance(text, str):
            self.panel.connectionTextBox.setText(
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_17(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
        if text == "wb lost":
            self.panel.connectionTextBox.setText("Moonraker connection lost")
        if text is None:
            self.panel.connectionTextBox.setText(
                """
                Not connected to Moonraker Websocket
                """
            )
            return False
        if isinstance(text, str):
            self.panel.connectionTextBox.setText(
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_18(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                None
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_19(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return False
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_20(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = None

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_21(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text != 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_22(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 1:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_23(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    None
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_24(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "XXConnection to Moonraker timeout \n \n please retryXX"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_25(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "connection to moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_26(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "CONNECTION TO MOONRAKER TIMEOUT \n \n PLEASE RETRY"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_27(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = None

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_28(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 1

            self.dot_timer.start()
            self._add_dot()

        return False

    def xǁConnectionPageǁtext_update__mutmut_29(self, text: int | str | None = None):
        """Update widget text"""
        if self.state == "shutdown" and self.message is not None:
            return False
        self.dot_timer.stop()
        logger.debug(f"[ConnectionWindowPanel] text_update: {text}")
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
                f"""Connection to Moonraker unavailable\nTry again by reconnecting or \nrestarting klipper\n{text}"""
            )
            return True
        if isinstance(text, int):
            # * Websocket connection messages

            self.base_text = f"Attempting to reconnect to Moonraker.\n\nConnection try number: {text}"

            if text == 0:
                self.panel.connectionTextBox.setText(
                    "Connection to Moonraker timeout \n \n please retry"
                )
                return
            self.dot_count = 0

            self.dot_timer.start()
            self._add_dot()

        return True
    
    xǁConnectionPageǁtext_update__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConnectionPageǁtext_update__mutmut_1': xǁConnectionPageǁtext_update__mutmut_1, 
        'xǁConnectionPageǁtext_update__mutmut_2': xǁConnectionPageǁtext_update__mutmut_2, 
        'xǁConnectionPageǁtext_update__mutmut_3': xǁConnectionPageǁtext_update__mutmut_3, 
        'xǁConnectionPageǁtext_update__mutmut_4': xǁConnectionPageǁtext_update__mutmut_4, 
        'xǁConnectionPageǁtext_update__mutmut_5': xǁConnectionPageǁtext_update__mutmut_5, 
        'xǁConnectionPageǁtext_update__mutmut_6': xǁConnectionPageǁtext_update__mutmut_6, 
        'xǁConnectionPageǁtext_update__mutmut_7': xǁConnectionPageǁtext_update__mutmut_7, 
        'xǁConnectionPageǁtext_update__mutmut_8': xǁConnectionPageǁtext_update__mutmut_8, 
        'xǁConnectionPageǁtext_update__mutmut_9': xǁConnectionPageǁtext_update__mutmut_9, 
        'xǁConnectionPageǁtext_update__mutmut_10': xǁConnectionPageǁtext_update__mutmut_10, 
        'xǁConnectionPageǁtext_update__mutmut_11': xǁConnectionPageǁtext_update__mutmut_11, 
        'xǁConnectionPageǁtext_update__mutmut_12': xǁConnectionPageǁtext_update__mutmut_12, 
        'xǁConnectionPageǁtext_update__mutmut_13': xǁConnectionPageǁtext_update__mutmut_13, 
        'xǁConnectionPageǁtext_update__mutmut_14': xǁConnectionPageǁtext_update__mutmut_14, 
        'xǁConnectionPageǁtext_update__mutmut_15': xǁConnectionPageǁtext_update__mutmut_15, 
        'xǁConnectionPageǁtext_update__mutmut_16': xǁConnectionPageǁtext_update__mutmut_16, 
        'xǁConnectionPageǁtext_update__mutmut_17': xǁConnectionPageǁtext_update__mutmut_17, 
        'xǁConnectionPageǁtext_update__mutmut_18': xǁConnectionPageǁtext_update__mutmut_18, 
        'xǁConnectionPageǁtext_update__mutmut_19': xǁConnectionPageǁtext_update__mutmut_19, 
        'xǁConnectionPageǁtext_update__mutmut_20': xǁConnectionPageǁtext_update__mutmut_20, 
        'xǁConnectionPageǁtext_update__mutmut_21': xǁConnectionPageǁtext_update__mutmut_21, 
        'xǁConnectionPageǁtext_update__mutmut_22': xǁConnectionPageǁtext_update__mutmut_22, 
        'xǁConnectionPageǁtext_update__mutmut_23': xǁConnectionPageǁtext_update__mutmut_23, 
        'xǁConnectionPageǁtext_update__mutmut_24': xǁConnectionPageǁtext_update__mutmut_24, 
        'xǁConnectionPageǁtext_update__mutmut_25': xǁConnectionPageǁtext_update__mutmut_25, 
        'xǁConnectionPageǁtext_update__mutmut_26': xǁConnectionPageǁtext_update__mutmut_26, 
        'xǁConnectionPageǁtext_update__mutmut_27': xǁConnectionPageǁtext_update__mutmut_27, 
        'xǁConnectionPageǁtext_update__mutmut_28': xǁConnectionPageǁtext_update__mutmut_28, 
        'xǁConnectionPageǁtext_update__mutmut_29': xǁConnectionPageǁtext_update__mutmut_29
    }
    xǁConnectionPageǁtext_update__mutmut_orig.__name__ = 'xǁConnectionPageǁtext_update'

    def _add_dot(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConnectionPageǁ_add_dot__mutmut_orig'), object.__getattribute__(self, 'xǁConnectionPageǁ_add_dot__mutmut_mutants'), args, kwargs, self)

    def xǁConnectionPageǁ_add_dot__mutmut_orig(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_1(self):
        """Add one dot per second (max 3)."""
        self.dot_count = 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_2(self):
        """Add one dot per second (max 3)."""
        self.dot_count -= 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_3(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 2
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_4(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count >= 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_5(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 4:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_6(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = None
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_7(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count - " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_8(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." / self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_9(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "XX.XX" * self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_10(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " / (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_11(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + "XX XX" * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_12(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " * (3 + self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_13(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " * (4 - self.dot_count)
        self.panel.connectionTextBox.setText(f"{self.base_text}{dots}")

    def xǁConnectionPageǁ_add_dot__mutmut_14(self):
        """Add one dot per second (max 3)."""
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_timer.stop()
            return
        dots = "." * self.dot_count + " " * (3 - self.dot_count)
        self.panel.connectionTextBox.setText(None)
    
    xǁConnectionPageǁ_add_dot__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConnectionPageǁ_add_dot__mutmut_1': xǁConnectionPageǁ_add_dot__mutmut_1, 
        'xǁConnectionPageǁ_add_dot__mutmut_2': xǁConnectionPageǁ_add_dot__mutmut_2, 
        'xǁConnectionPageǁ_add_dot__mutmut_3': xǁConnectionPageǁ_add_dot__mutmut_3, 
        'xǁConnectionPageǁ_add_dot__mutmut_4': xǁConnectionPageǁ_add_dot__mutmut_4, 
        'xǁConnectionPageǁ_add_dot__mutmut_5': xǁConnectionPageǁ_add_dot__mutmut_5, 
        'xǁConnectionPageǁ_add_dot__mutmut_6': xǁConnectionPageǁ_add_dot__mutmut_6, 
        'xǁConnectionPageǁ_add_dot__mutmut_7': xǁConnectionPageǁ_add_dot__mutmut_7, 
        'xǁConnectionPageǁ_add_dot__mutmut_8': xǁConnectionPageǁ_add_dot__mutmut_8, 
        'xǁConnectionPageǁ_add_dot__mutmut_9': xǁConnectionPageǁ_add_dot__mutmut_9, 
        'xǁConnectionPageǁ_add_dot__mutmut_10': xǁConnectionPageǁ_add_dot__mutmut_10, 
        'xǁConnectionPageǁ_add_dot__mutmut_11': xǁConnectionPageǁ_add_dot__mutmut_11, 
        'xǁConnectionPageǁ_add_dot__mutmut_12': xǁConnectionPageǁ_add_dot__mutmut_12, 
        'xǁConnectionPageǁ_add_dot__mutmut_13': xǁConnectionPageǁ_add_dot__mutmut_13, 
        'xǁConnectionPageǁ_add_dot__mutmut_14': xǁConnectionPageǁ_add_dot__mutmut_14
    }
    xǁConnectionPageǁ_add_dot__mutmut_orig.__name__ = 'xǁConnectionPageǁ_add_dot'

    @QtCore.pyqtSlot(str, str, name="webhooks_update")
    def webhook_update(self, state: str, message: str):
        """Handle websocket webhook updates"""
        self.state = state
        self.message = message
        self.text_update()

    def eventFilter(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        args = [object, event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConnectionPageǁeventFilter__mutmut_orig'), object.__getattribute__(self, 'xǁConnectionPageǁeventFilter__mutmut_mutants'), args, kwargs, self)

    def xǁConnectionPageǁeventFilter__mutmut_orig(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_1(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() != KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_2(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_3(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(None)
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_4(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("XXKlippy DisconnectedXX")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_5(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("klippy disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_6(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("KLIPPY DISCONNECTED")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_7(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() != KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_8(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText(None)
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_9(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("XXKlippy ReadyXX")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_10(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("klippy ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_11(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("KLIPPY READY")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_12(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return True

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_13(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() != KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_14(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_15(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(None)
                self.show()
                return True

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_16(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return False

        return super().eventFilter(object, event)

    def xǁConnectionPageǁeventFilter__mutmut_17(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(None, event)

    def xǁConnectionPageǁeventFilter__mutmut_18(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, None)

    def xǁConnectionPageǁeventFilter__mutmut_19(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(event)

    def xǁConnectionPageǁeventFilter__mutmut_20(self, object: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if event.type() == KlippyDisconnected.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText("Klippy Disconnected")
                self.show()

        elif event.type() == KlippyReady.type():
            self.dot_timer.stop()
            self.panel.connectionTextBox.setText("Klippy Ready")
            self.hide()
            return False

        elif event.type() == KlippyShutdown.type():
            self.dot_timer.stop()
            if not self.isVisible():
                self.panel.connectionTextBox.setText(f"{self.message}")
                self.show()
                return True

        return super().eventFilter(object, )
    
    xǁConnectionPageǁeventFilter__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConnectionPageǁeventFilter__mutmut_1': xǁConnectionPageǁeventFilter__mutmut_1, 
        'xǁConnectionPageǁeventFilter__mutmut_2': xǁConnectionPageǁeventFilter__mutmut_2, 
        'xǁConnectionPageǁeventFilter__mutmut_3': xǁConnectionPageǁeventFilter__mutmut_3, 
        'xǁConnectionPageǁeventFilter__mutmut_4': xǁConnectionPageǁeventFilter__mutmut_4, 
        'xǁConnectionPageǁeventFilter__mutmut_5': xǁConnectionPageǁeventFilter__mutmut_5, 
        'xǁConnectionPageǁeventFilter__mutmut_6': xǁConnectionPageǁeventFilter__mutmut_6, 
        'xǁConnectionPageǁeventFilter__mutmut_7': xǁConnectionPageǁeventFilter__mutmut_7, 
        'xǁConnectionPageǁeventFilter__mutmut_8': xǁConnectionPageǁeventFilter__mutmut_8, 
        'xǁConnectionPageǁeventFilter__mutmut_9': xǁConnectionPageǁeventFilter__mutmut_9, 
        'xǁConnectionPageǁeventFilter__mutmut_10': xǁConnectionPageǁeventFilter__mutmut_10, 
        'xǁConnectionPageǁeventFilter__mutmut_11': xǁConnectionPageǁeventFilter__mutmut_11, 
        'xǁConnectionPageǁeventFilter__mutmut_12': xǁConnectionPageǁeventFilter__mutmut_12, 
        'xǁConnectionPageǁeventFilter__mutmut_13': xǁConnectionPageǁeventFilter__mutmut_13, 
        'xǁConnectionPageǁeventFilter__mutmut_14': xǁConnectionPageǁeventFilter__mutmut_14, 
        'xǁConnectionPageǁeventFilter__mutmut_15': xǁConnectionPageǁeventFilter__mutmut_15, 
        'xǁConnectionPageǁeventFilter__mutmut_16': xǁConnectionPageǁeventFilter__mutmut_16, 
        'xǁConnectionPageǁeventFilter__mutmut_17': xǁConnectionPageǁeventFilter__mutmut_17, 
        'xǁConnectionPageǁeventFilter__mutmut_18': xǁConnectionPageǁeventFilter__mutmut_18, 
        'xǁConnectionPageǁeventFilter__mutmut_19': xǁConnectionPageǁeventFilter__mutmut_19, 
        'xǁConnectionPageǁeventFilter__mutmut_20': xǁConnectionPageǁeventFilter__mutmut_20
    }
    xǁConnectionPageǁeventFilter__mutmut_orig.__name__ = 'xǁConnectionPageǁeventFilter'
