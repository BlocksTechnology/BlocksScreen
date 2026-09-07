import enum
import logging
import re
import typing

from events import KlippyDisconnected, KlippyReady
from lib.moonrakerComm import MoonWebSocket
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)


class ConnectionState(enum.StrEnum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    WEBSOCKET_LOST = "websocket_lost"
    MOONRAKER_CONNECTED = "moonraker_connected"
    KLIPPER_STARTUP = "klipper_startup"
    KLIPPER_READY = "klipper_ready"
    KLIPPER_DISCONNECTED = "klipper_disconnected"
    KLIPPER_ERROR = "klipper_error"
    KLIPPER_SHUTDOWN = "klipper_shutdown"


class ConnectionPage(QtWidgets.QFrame):
    _SHUTDOWN_FALLBACK_CONTEXT: typing.Final[str] = (
        "Press 'Firmware Restart' to recover."
    )

    _MESSAGES: typing.ClassVar[dict[ConnectionState, str]] = {
        ConnectionState.DISCONNECTED: "The printer is offline.\nReconnecting automatically…",
        ConnectionState.CONNECTING: "Connecting to the printer\nAttempt {n}",
        ConnectionState.WEBSOCKET_LOST: "Connection interrupted.\nAttempting to reconnect…",
        ConnectionState.MOONRAKER_CONNECTED: "Connection established.\nWaiting for the printer to initialise…",
        ConnectionState.KLIPPER_STARTUP: "The printer is starting up.\nPlease wait…",
        ConnectionState.KLIPPER_READY: "The printer is ready.",
        ConnectionState.KLIPPER_DISCONNECTED: "The printer is not responding.\nPress 'Restart Printer' to reconnect.",
        ConnectionState.KLIPPER_ERROR: "A printer error has occurred.\nPress 'Firmware Restart' to recover.",
        ConnectionState.KLIPPER_SHUTDOWN: "The printer has shut down.\n{message}",
    }

    _AUTO_RECOVER_CONTEXTS: typing.ClassVar[frozenset[str]] = frozenset(
        {
            "m112 command",
            "printers emergency button pressed",
            "printer emergency button pressed",
        }
    )

    _SHUTDOWN_REASON_MAP: typing.ClassVar[dict[str, str]] = {
        "m112 command": "Emergency stop activated.\nRelease the emergency button, then\npress 'Firmware Restart' to recover.",
        "printers emergency button pressed": "Emergency stop activated.\nRelease the emergency button, then\npress 'Firmware Restart' to recover.",
        "printer emergency button pressed": "Emergency stop activated.\nRelease the emergency button, then\npress 'Firmware Restart' to recover.",
        "webhooks request": "Emergency stop activated.",
        "lost communication with mcu": "Lost communication with the MCU.",
        "timer too close": "MCU overload\nCommunication timing failure.\nPress 'Firmware Restart' to recover.",
        "adc out of range": "Temperature sensor fault.",
        "no next step": "Communication failure with the MCU.",
        "rescheduled timer in the past": "Motion rate exceeded\nReduce speed or acceleration.\nPress 'Firmware Restart' to recover.",
        "stepper too far in past": "Stepper timing failure\nReduce speed or acceleration.\nPress 'Firmware Restart' to recover.",
        "communication timeout during homing": "Communication timeout during homing.",
        "protocol error": "MCU communication protocol error.",
        "config error": "Configuration error\nCheck printer.cfg.\nPress 'Firmware Restart' to recover.",
        "mcu error during connect": "Failed to connect to the MCU.",
    }

    _FIRMWARE_RESTART_STATES: typing.ClassVar[frozenset[ConnectionState]] = frozenset(
        {
            ConnectionState.KLIPPER_ERROR,
            ConnectionState.KLIPPER_SHUTDOWN,
        }
    )

    _SHUTDOWN_NOISE: typing.ClassVar[frozenset[str]] = frozenset(
        {"forced shutdown command", "forced shutdown", "shutdown", "none", ""}
    )

    _RESTART_LABELS: typing.ClassVar[dict[ConnectionState, str]] = {
        ConnectionState.KLIPPER_ERROR: "Firmware Restart",
        ConnectionState.KLIPPER_SHUTDOWN: "Firmware Restart",
        ConnectionState.WEBSOCKET_LOST: "Retry Connection",
    }

    _KLIPPY_STATE_MAP: typing.ClassVar[dict[str, ConnectionState]] = {
        "error": ConnectionState.KLIPPER_ERROR,
        "disconnected": ConnectionState.KLIPPER_DISCONNECTED,
        "shutdown": ConnectionState.KLIPPER_SHUTDOWN,
        "startup": ConnectionState.KLIPPER_STARTUP,
        "ready": ConnectionState.KLIPPER_READY,
    }

    retry_connection_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="retry_connection_clicked"
    )
    wifi_button_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="call_network_page"
    )
    reboot_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="reboot_clicked"
    )
    restart_klipper_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="restart_klipper_clicked"
    )
    firmware_restart_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="firmware_restart_clicked"
    )
    update_button_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="show-update-page"
    )
    notification_button_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="notification_button_clicked"
    )
    call_load_panel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, str, bool, name="call-load-panel"
    )
    call_cancel_panel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="call-cancel-panel"
    )

    def __init__(self, parent: QtWidgets.QWidget, ws: MoonWebSocket, /) -> None:
        super().__init__(parent)
        self.ws = ws
        self._setup_ui()

        self._state: ConnectionState = ConnectionState.DISCONNECTED
        self.base_text: str = ""
        self.dot_count: int = 0
        self.conn_toggle: bool = True
        self._shutdown_confirmed: bool = (
            False  # prevents fallback from overwriting shutdown reason
        )
        self._last_shutdown_context: str = ""
        self._firmware_restarting_pending: bool = False
        self._last_restart_was_firmware: bool = False
        self._escalated_to_klipper_restart: bool = False

        self.dot_timer = QtCore.QTimer(self)
        self.dot_timer.setInterval(1000)
        self.dot_timer.timeout.connect(self._add_dot)

        self._restart_10s_timer = QtCore.QTimer(self)
        self._restart_10s_timer.setSingleShot(True)
        self._restart_10s_timer.setInterval(10_000)
        self._restart_10s_timer.timeout.connect(self._on_restart_10s_elapsed)

        self._restart_30s_timer = QtCore.QTimer(self)
        self._restart_30s_timer.setSingleShot(True)
        self._restart_30s_timer.setInterval(30_000)
        self._restart_30s_timer.timeout.connect(self._on_restart_30s_elapsed)

        self.restart_klipper_button.clicked.connect(self._on_restart_clicked)
        self.reboot_system_button.clicked.connect(self.reboot_clicked.emit)
        self.notification_button.clicked.connect(self.notification_button_clicked.emit)
        self.update_page_button.clicked.connect(self._on_update_page_clicked)
        self.wifi_button.clicked.connect(self.wifi_button_clicked.emit)

    @property
    def manual_restart_pending(self) -> bool:
        """True while a user-initiated restart (firmware or printer) is in flight."""
        return self._firmware_restarting_pending

    def _apply_shutdown_guard(self, state: ConnectionState, context: str) -> bool:
        if (
            self._state == ConnectionState.KLIPPER_SHUTDOWN
            and state != ConnectionState.KLIPPER_SHUTDOWN
        ):
            self._shutdown_confirmed = False
        elif state == ConnectionState.KLIPPER_SHUTDOWN:
            _is_real = context and context != ConnectionPage._SHUTDOWN_FALLBACK_CONTEXT
            if _is_real:
                self._shutdown_confirmed = True
                self._last_shutdown_context = context
            elif self._shutdown_confirmed or (
                self._state == ConnectionState.KLIPPER_SHUTDOWN and not context
            ):
                return False
        return True

    def _handle_pending_restart(self, state: ConnectionState) -> bool:
        if self._firmware_restarting_pending and state in (
            ConnectionState.KLIPPER_SHUTDOWN,
            ConnectionState.KLIPPER_ERROR,
            ConnectionState.WEBSOCKET_LOST,
        ):
            self._stop_restart_overlay()
        return state == ConnectionState.KLIPPER_DISCONNECTED and (
            self._firmware_restarting_pending
            or self._state == ConnectionState.KLIPPER_SHUTDOWN
        )

    def _set_state(self, state: ConnectionState, context: str = "") -> None:
        """Update connection state and refresh the UI accordingly."""
        if state == ConnectionState.KLIPPER_SHUTDOWN and not context:
            context = (
                self._last_shutdown_context or ConnectionPage._SHUTDOWN_FALLBACK_CONTEXT
            )
        if not self._apply_shutdown_guard(state, context):
            return
        if self._handle_pending_restart(state):
            return
        self.dot_timer.stop()
        self._state = state
        message = self._MESSAGES[state].format(n=context, message=context)
        self.status_label.setText(message)
        if state == ConnectionState.CONNECTING:
            self.base_text = message
            self.dot_count = 0
            self.dot_timer.start()
        elif state == ConnectionState.KLIPPER_READY:
            self._stop_restart_overlay()
            self._last_shutdown_context = ""
            self.hide()
            return
        if not self.isVisible() and self.conn_toggle:
            self.show()
        self._update_restart_label(state)

    def _stop_restart_overlay(self) -> None:
        self._firmware_restarting_pending = False
        self._restart_10s_timer.stop()
        self._restart_30s_timer.stop()
        self.call_load_panel.emit(False, "", False)

    def _add_dot(self) -> None:
        self.dot_count += 1
        if self.dot_count > 3:
            self.dot_count = 0
        dots = "." * self.dot_count
        self.status_label.setText(f"{self.base_text}{dots}")

    def _update_restart_label(self, state: ConnectionState) -> None:
        """Set restart_klipper_button label based on current state."""
        self.restart_klipper_button.setText(
            self._RESTART_LABELS.get(state, "Restart Printer")
        )

    @staticmethod
    def _strip_shutdown_prefix(raw: str) -> str:
        return re.sub(
            r"^(?:Shutdown due to |MCU '[^']*' shutdown[:.]\s*)",
            "",
            raw.split("\n")[0].strip(),
        )

    @staticmethod
    def _normalize_shutdown_lines(raw: str) -> str:
        line = ConnectionPage._strip_shutdown_prefix(raw)
        return line.lower().replace("'", "").replace("’", "")

    @staticmethod
    def _clean_shutdown_context(raw: str) -> str:
        line = ConnectionPage._strip_shutdown_prefix(raw)
        lower = ConnectionPage._normalize_shutdown_lines(line)
        if lower in ConnectionPage._SHUTDOWN_NOISE:
            return ""
        for key, display in ConnectionPage._SHUTDOWN_REASON_MAP.items():
            if lower.startswith(key):
                return display
        return line.capitalize()

    @staticmethod
    def _build_shutdown_context(raw: str) -> str:
        reason = ConnectionPage._clean_shutdown_context(raw)
        if not reason:
            return ConnectionPage._SHUTDOWN_FALLBACK_CONTEXT
        if "\n" in reason:
            return reason
        return f"{reason}\nPress 'Firmware Restart' to recover."

    @staticmethod
    def _is_auto_recovering_context(raw: str) -> bool:
        lower = ConnectionPage._normalize_shutdown_lines(raw)
        return any(
            lower.startswith(key) for key in ConnectionPage._AUTO_RECOVER_CONTEXTS
        )

    def _on_restart_clicked(self) -> None:
        if self._state == ConnectionState.WEBSOCKET_LOST:
            self.retry_connection_clicked.emit()
            return
        is_firmware = self._state in self._FIRMWARE_RESTART_STATES
        self._last_restart_was_firmware = is_firmware
        self._escalated_to_klipper_restart = False
        self._firmware_restarting_pending = True
        self.call_load_panel.emit(
            True,
            "Restarting firmware…" if is_firmware else "Restarting printer…",
            False,
        )
        self._restart_10s_timer.start()
        self._restart_30s_timer.start()
        if is_firmware:
            self.firmware_restart_clicked.emit()
        else:
            self.restart_klipper_clicked.emit()

    def _on_restart_10s_elapsed(self) -> None:
        self.call_load_panel.emit(True, "Still restarting, please wait…", False)

    def _on_restart_30s_elapsed(self) -> None:
        if self._last_restart_was_firmware and not self._escalated_to_klipper_restart:
            self._escalated_to_klipper_restart = True
            self.call_load_panel.emit(True, "Restarting printer...", False)
            self.restart_klipper_clicked.emit()
            self._restart_30s_timer.start()
            return
        self._stop_restart_overlay()

    def _on_update_page_clicked(self) -> None:
        self.update_button_clicked.emit(True)

    @QtCore.pyqtSlot(bool, name="toggle_connection_page")
    def set_toggle(self, toggle: bool) -> None:
        """Enable or disable auto-show behaviour."""
        self.conn_toggle = toggle

    @QtCore.pyqtSlot(str, name="on_klippy_state")
    def on_klippy_state(self, state: str) -> None:
        """Handle Klipper state string changes."""
        if (mapped := self._KLIPPY_STATE_MAP.get(state)) is not None:
            self._set_state(mapped)
        else:
            logger.warning("Unknown Klipper state: %s", state)

    @QtCore.pyqtSlot(int, name="on_websocket_connecting")
    def on_websocket_connecting(self, attempt: int) -> None:
        """Handle websocket reconnection attempts."""
        self._set_state(ConnectionState.CONNECTING, context=str(attempt))

    @QtCore.pyqtSlot(name="on_websocket_connection_achieved")
    def on_websocket_connection_achieved(self) -> None:
        """Handle websocket connection established."""
        self._set_state(ConnectionState.MOONRAKER_CONNECTED)

    @QtCore.pyqtSlot(name="on_websocket_connection_lost")
    def on_websocket_connection_lost(self) -> None:
        """Handle websocket connection lost."""
        self._set_state(ConnectionState.WEBSOCKET_LOST)

    @QtCore.pyqtSlot(str, str, name="webhooks_update")
    def webhook_update(self, state: str, message: str) -> None:
        """Handle Moonraker websocket state updates."""
        if state == "shutdown":
            should_auto_recover = (
                self._state != ConnectionState.KLIPPER_SHUTDOWN
                and not self._firmware_restarting_pending
                and self._is_auto_recovering_context(message)
            )
            self._set_state(
                ConnectionState.KLIPPER_SHUTDOWN,
                context=self._build_shutdown_context(message),
            )
            if should_auto_recover:
                self._last_restart_was_firmware = True
                self._escalated_to_klipper_restart = False
                self._firmware_restarting_pending = True
                self._restart_10s_timer.start()
                self._restart_30s_timer.start()

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:  # noqa: N802
        if self.conn_toggle:
            self.ws.api.refresh_update_status()
            self.call_load_panel.emit(False, "", False)
            self.call_cancel_panel.emit(False)
        super().showEvent(a0)

    def eventFilter(self, a0: QtCore.QObject | None, a1: QtCore.QEvent | None) -> bool:  # noqa: N802
        """Route Klipper custom events to _set_state"""
        if a1 is None:
            return super().eventFilter(a0, a1)
        if a1.type() == KlippyDisconnected.type():
            if not self._firmware_restarting_pending:
                self._set_state(ConnectionState.KLIPPER_DISCONNECTED)
        elif a1.type() == KlippyReady.type():
            self._set_state(ConnectionState.KLIPPER_READY)
        return super().eventFilter(a0, a1)

    def _setup_ui(self) -> None:
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.setMaximumSize(QtCore.QSize(800, 480))
        self.setObjectName("ConnectionPage")
        self.setStyleSheet(
            "#ConnectionPage{background-image: url(:/background/media/1st_background.png);}"
        )
        self.button_frame = BlocksCustomFrame(parent=self)
        self.button_frame.setGeometry(QtCore.QRect(10, 365, 780, 140))
        self.button_frame.setMinimumSize(QtCore.QSize(780, 140))
        self.button_frame.setMaximumSize(QtCore.QSize(780, 160))
        self.button_frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.button_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.button_frame.setLineWidth(0)
        self.button_frame.setObjectName("button_frame")

        self.button_layout = QtWidgets.QHBoxLayout(self.button_frame)
        self.button_layout.setContentsMargins(0, 5, 0, 0)
        self.button_layout.setSpacing(0)
        self.button_layout.setObjectName("button_layout")

        _btn_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )

        self.reboot_system_button = IconButton(parent=self.button_frame)
        self.reboot_system_button.setSizePolicy(_btn_policy)
        self.reboot_system_button.setMinimumSize(QtCore.QSize(115, 92))
        self.reboot_system_button.setMaximumSize(QtCore.QSize(115, 92))
        self.reboot_system_button.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor)
        )
        self.reboot_system_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.reboot_system_button.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.reboot_system_button.setFlat(True)
        self.reboot_system_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/system/media/btn_icons/reboot.svg")
        )
        self.reboot_system_button.setProperty("has_text", True)
        self.reboot_system_button.setProperty("text_formatting", "bottom")
        self.reboot_system_button.setText("Reboot")
        self.reboot_system_button.setObjectName("reboot_system_button")
        self.button_layout.addWidget(
            self.reboot_system_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        self.restart_klipper_button = IconButton(parent=self.button_frame)
        self.restart_klipper_button.setSizePolicy(_btn_policy)
        self.restart_klipper_button.setMinimumSize(QtCore.QSize(115, 92))
        self.restart_klipper_button.setMaximumSize(QtCore.QSize(115, 92))
        self.restart_klipper_button.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor)
        )
        self.restart_klipper_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.restart_klipper_button.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.restart_klipper_button.setFlat(True)
        self.restart_klipper_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/system/media/btn_icons/restart_klipper.svg")
        )
        self.restart_klipper_button.setProperty("has_text", True)
        self.restart_klipper_button.setProperty("text_formatting", "bottom")
        self.restart_klipper_button.setText("Restart Printer")
        self.restart_klipper_button.setObjectName("restart_klipper_button")
        self.button_layout.addWidget(
            self.restart_klipper_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        self.notification_button = IconButton(parent=self.button_frame)
        self.notification_button.setSizePolicy(_btn_policy)
        self.notification_button.setMinimumSize(QtCore.QSize(115, 92))
        self.notification_button.setMaximumSize(QtCore.QSize(115, 92))
        self.notification_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.notification_button.setFlat(True)
        self.notification_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/notification.svg")
        )
        self.notification_button.setProperty("has_text", True)
        self.notification_button.setProperty("text_formatting", "bottom")
        self.notification_button.setText("Notifications")
        self.notification_button.setObjectName("notification_button")
        self.button_layout.addWidget(
            self.notification_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        self.update_page_button = IconButton(parent=self.button_frame)
        self.update_page_button.setSizePolicy(_btn_policy)
        self.update_page_button.setMinimumSize(QtCore.QSize(115, 92))
        self.update_page_button.setMaximumSize(QtCore.QSize(115, 92))
        self.update_page_button.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor)
        )
        self.update_page_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.update_page_button.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.update_page_button.setFlat(True)
        self.update_page_button.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/system/media/btn_icons/update-software-icon.svg"),
        )
        self.update_page_button.setProperty("has_text", True)
        self.update_page_button.setProperty("text_formatting", "bottom")
        self.update_page_button.setText("Updates")
        self.update_page_button.setObjectName("update_page_button")
        self.button_layout.addWidget(
            self.update_page_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        self.wifi_button = IconButton(parent=self.button_frame)
        self.wifi_button.setSizePolicy(_btn_policy)
        self.wifi_button.setMinimumSize(QtCore.QSize(115, 92))
        self.wifi_button.setMaximumSize(QtCore.QSize(115, 92))
        self.wifi_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.wifi_button.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.wifi_button.setFlat(True)
        self.wifi_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/network/media/btn_icons/wifi_config.svg")
        )
        self.wifi_button.setProperty("has_text", True)
        self.wifi_button.setProperty("text_formatting", "bottom")
        self.wifi_button.setProperty("class", "system_control_btn")
        self.wifi_button.setText("Wi-Fi Settings")
        self.wifi_button.setObjectName("wifi_button")
        self.button_layout.addWidget(
            self.wifi_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        self.content_frame = QtWidgets.QFrame(parent=self)
        self.content_frame.setGeometry(QtCore.QRect(0, 0, 800, 365))
        self.content_frame.setMinimumSize(QtCore.QSize(800, 365))
        self.content_frame.setMaximumSize(QtCore.QSize(800, 365))
        self.content_frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.content_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.content_frame.setObjectName("content_frame")

        self.content_layout = QtWidgets.QVBoxLayout(self.content_frame)
        self.content_layout.setObjectName("content_layout")

        spacerItem = QtWidgets.QSpacerItem(
            775,
            70,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.content_layout.addItem(spacerItem)

        self.status_label = QtWidgets.QLabel(parent=self.content_frame)
        self.status_label.setMaximumSize(QtCore.QSize(800, 380))
        _font = QtGui.QFont()
        _font.setFamily("Momcake")
        _font.setPointSize(17)

        self.status_label.setFont(_font)
        self.status_label.setStyleSheet("color:white")
        self.status_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.NoTextInteraction
        )
        self.status_label.setObjectName("status_label")
        self.content_layout.addWidget(self.status_label)
