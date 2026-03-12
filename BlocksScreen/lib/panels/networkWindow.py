import fcntl
import ipaddress as _ipaddress
import logging
import socket as _socket
import struct
from dataclasses import replace
from functools import partial

from lib.network import (
    ConnectionPriority,
    ConnectionResult,
    ConnectivityState,
    NetworkInfo,
    NetworkManager,
    NetworkState,
    NetworkStatus,
    PendingOperation,
    SavedNetwork,
    WifiIconKey,
    is_connectable_security,
    is_hidden_ssid,
    signal_to_bars,
)
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from lib.panels.widgets.loadWidget import LoadingOverlayWidget
from lib.panels.widgets.popupDialogWidget import Popup
from lib.qrcode_gen import generate_wifi_qrcode
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_label import BlocksLabel
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.blocks_Scrollbar import CustomScrollBar
from lib.utils.blocks_togglebutton import NetworkWidgetbuttons
from lib.utils.check_button import BlocksCustomCheckButton
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer, pyqtSlot

logger = logging.getLogger(__name__)

LOAD_TIMEOUT_MS = 30_000
STATUS_CHECK_INTERVAL_MS = 2_000


class PixmapCache:
    """Process-wide cache for QPixmaps loaded from Qt resource paths.

    Every SVG is decoded exactly once. Qt's implicit sharing means the
    same QPixmap can be safely referenced by any number of widgets.
    Must only be called after QApplication is created.
    """

    _cache: dict[str, QtGui.QPixmap] = {}

    @classmethod
    def get(cls, path: str) -> QtGui.QPixmap:
        """Return the cached QPixmap for *path*, loading it on first access."""
        if path not in cls._cache:
            cls._cache[path] = QtGui.QPixmap(path)
        return cls._cache[path]

    @classmethod
    def preload(cls, paths: list[str]) -> None:
        """Batch-load a list of paths (called once during init)."""
        for path in paths:
            cls.get(path)


class WifiIconProvider:
    """Maps (signal_strength, is_protected) -> cached QPixmap via PixmapCache."""

    _PATHS: dict[tuple[int, bool], str] = {
        (
            b,
            p,
        ): f":/network/media/btn_icons/network/{b}bar_wifi{'_protected' if p else ''}.svg"
        for b in range(5)
        for p in (False, True)
    }

    @classmethod
    def get_pixmap(cls, signal: int, is_protected: bool = False) -> QtGui.QPixmap:
        """Get pixmap for given signal strength and protection status."""
        bars = signal_to_bars(signal)
        path = cls._PATHS.get((bars, is_protected), cls._PATHS[(0, False)])
        return PixmapCache.get(path)


class IPAddressLineEdit(BlocksCustomLinEdit):
    """Line-edit restricted to valid IPv4 addresses."""

    _VALID_STYLE = ""
    _INVALID_STYLE = "border: 2px solid red; border-radius: 8px;"

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        *,
        placeholder: str = "0.0.0.0",  # nosec B104 — UI placeholder text, not a socket bind
    ) -> None:
        """Initialise the IP-address input field with regex validation and optional placeholder."""
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        ip_re = QtCore.QRegularExpression(r"^[\d.]*$")
        self.setValidator(QtGui.QRegularExpressionValidator(ip_re, self))
        self.textChanged.connect(self._on_text_changed)

    def is_valid(self) -> bool:
        """Return ``True`` when the current text is a valid dotted-quad IPv4 address."""
        try:
            _ipaddress.IPv4Address(self.text().strip())
            return True
        except ValueError:
            return False

    def is_valid_mask(self) -> bool:
        """Return ``True`` when the current text is a valid subnet mask or CIDR prefix."""
        txt = self.text().strip()
        if txt.isdigit():
            n = int(txt)
            if 0 <= n <= 32:
                return True
            return False

        try:
            _ipaddress.IPv4Network(f"0.0.0.0/{txt}", strict=False)
            return True
        except ValueError:
            return False

    def _on_text_changed(self, text: str) -> None:
        """Update the field border colour in real-time as the user types."""
        if not text:
            self.setStyleSheet(self._VALID_STYLE)
            return
        try:
            _ipaddress.IPv4Address(text.strip())
            self.setStyleSheet(self._VALID_STYLE)
        except ValueError:
            self.setStyleSheet(self._INVALID_STYLE)
        self.update()


class NetworkControlWindow(QtWidgets.QStackedWidget):
    """Stacked-widget UI for all network control pages (Wi-Fi, Ethernet, VLAN, Hotspot).

    Owns a :class:`~BlocksScreen.lib.network.facade.NetworkManager` instance and
    mediates between the UI pages and the async D-Bus worker.
    """

    update_wifi_icon = QtCore.pyqtSignal(int, name="update-wifi-icon")

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        """Construct the stacked-widget UI, wire all signals/slots, and request initial state."""
        super().__init__(parent) if parent else super().__init__()

        self._init_instance_variables()
        self._setupUI()
        self._init_timers()
        self._init_model_view()
        self._init_network_manager()
        self._setup_navigation_signals()
        self._setup_action_signals()
        self._setup_toggle_signals()
        self._setup_password_visibility_signals()
        self._setup_icons()
        self._setup_input_fields()
        self._setup_keyboard()
        self._setup_scrollbar_signals()

        self._init_ui_state()
        self.hide()

    def _init_instance_variables(self) -> None:
        """Initialize instance variables."""
        self._is_first_run = True
        self._previous_panel: QtWidgets.QWidget | None = None
        self._current_field: QtWidgets.QLineEdit | None = None
        self._current_network_is_open = False
        self._current_network_is_hidden = False
        self._is_connecting = False
        self._target_ssid: str | None = None
        self._was_ethernet_connected: bool = False
        self._initial_priority: ConnectionPriority = ConnectionPriority.MEDIUM
        self._pending_operation: PendingOperation = PendingOperation.NONE
        self._pending_expected_ip: str = (
            ""  # IP to wait for before clearing WIFI_STATIC_IP loading
        )
        self._cached_scan_networks: list[NetworkInfo] = []
        self._last_active_signal_bars: int = -1
        self._active_signal: int = 0
        # Key = SSID, value = (signal_bars, status_label, ListItem).
        self._item_cache: dict[str, tuple[int, str, ListItem]] = {}
        # Singleton items reused across reconcile calls (zero allocation).
        self._separator_item: ListItem | None = None
        self._hidden_network_item: ListItem | None = None

    def _init_ui_state(self) -> None:
        """Initialize UI to clean disconnected state."""
        self.loadingwidget.setVisible(False)
        self._pending_operation = PendingOperation.NONE
        self._hide_all_info_elements()
        self._configure_info_box_centered()
        self.mn_info_box.setVisible(True)
        self.mn_info_box.setText(
            "There no active\ninternet connection.\nConnect via Ethernet, Wi-Fi,\nor enable a mobile hotspot\n for online features.\nPrinting functions will\nstill work offline."
        )

    def _init_network_manager(self) -> None:
        """Initialize network manager and connect signals."""
        self._nm = NetworkManager(self)

        self._nm.state_changed.connect(self._on_network_state_changed)

        self._nm.saved_networks_loaded.connect(self._on_saved_networks_loaded)

        self._nm.connection_result.connect(self._on_operation_complete)

        self._nm.error_occurred.connect(self._on_network_error)

        self.rescan_button.clicked.connect(self._nm.scan_networks)

        self.hotspot_name_input_field.setText(self._nm.hotspot_ssid)
        self.hotspot_password_input_field.setText(self._nm.hotspot_password)

        self._nm.networks_scanned.connect(self._on_scan_complete)

        self._nm.reconnect_complete.connect(self._on_reconnect_complete)

        self._nm.hotspot_config_updated.connect(self._on_hotspot_config_updated)

        self._prefill_ip_from_os()

    def _prefill_ip_from_os(self) -> None:
        """Read the current IP via SIOCGIFADDR ioctl and show it immediately.

        Bypasses NetworkManager D-Bus entirely — runs on the main thread,
        costs a single syscall, and completes in microseconds.  Called once
        during init so the user never sees "IP: --" if a connection was
        already active before the UI launched.
        """
        _SIOCGIFADDR = 0x8915
        for iface in ("eth0", "wlan0"):
            try:
                with _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM) as sock:
                    ifreq = struct.pack("256s", iface[:15].encode())
                    result = fcntl.ioctl(sock.fileno(), _SIOCGIFADDR, ifreq)
                ip = _socket.inet_ntoa(result[20:24])
                if ip and not ip.startswith("0."):
                    self.netlist_ip.setText(f"IP: {ip}")
                    self.netlist_ip.setVisible(True)
                    logger.debug("Startup IP prefill from OS (%s): %s", iface, ip)
                    return
            except OSError:
                continue

    @pyqtSlot()
    def _on_reconnect_complete(self) -> None:
        """Navigate back to the main panel after a static-IP or DHCP-reset operation."""
        logger.debug("reconnect_complete received — navigating to main_network_page")
        self.setCurrentIndex(self.indexOf(self.main_network_page))

    def _init_timers(self) -> None:
        """Initialize timers."""
        self._load_timer = QTimer(self)
        self._load_timer.setSingleShot(True)
        self._load_timer.timeout.connect(self._handle_load_timeout)

    def _init_model_view(self) -> None:
        """Initialize list model and view."""
        self._model = EntryListModel()
        self._model.setParent(self.listView)
        self._entry_delegate = EntryDelegate()
        self.listView.setModel(self._model)
        self.listView.setItemDelegate(self._entry_delegate)
        self._entry_delegate.item_selected.connect(self._on_ssid_item_clicked)
        self._configure_list_view_palette()

    @pyqtSlot(NetworkState)
    def _on_network_state_changed(self, state: NetworkState) -> None:
        """React to a NetworkState update: sync toggles, populate header and connection info."""
        logger.debug(
            "Network state: %s, SSID: %s, IP: %s, eth: %s",
            state.connectivity.name,
            state.current_ssid,
            state.current_ip,
            state.ethernet_connected,
        )

        if (
            state.current_ssid
            and state.signal_strength > 0
            and not state.hotspot_enabled
        ):
            self._active_signal = state.signal_strength
        elif not state.current_ssid or state.hotspot_enabled:
            self._active_signal = 0

        if self._is_first_run:
            self._handle_first_run(state)
            self._emit_status_icon(state)
            self._is_first_run = False
            self._was_ethernet_connected = state.ethernet_connected
            return

        # Cable just plugged in while Wi-Fi is active -> disable Wi-Fi
        if (
            state.ethernet_connected
            and not self._was_ethernet_connected
            and state.wifi_enabled
            and not self._is_connecting
        ):
            logger.info("Ethernet connected — turning off Wi-Fi")
            self._was_ethernet_connected = True
            wifi_btn = self.wifi_button.toggle_button
            hotspot_btn = self.hotspot_button.toggle_button
            with QtCore.QSignalBlocker(wifi_btn):
                wifi_btn.state = wifi_btn.State.OFF
            with QtCore.QSignalBlocker(hotspot_btn):
                hotspot_btn.state = hotspot_btn.State.OFF
            self._nm.set_wifi_enabled(False)
            self._sync_ethernet_panel(state)
            self._emit_status_icon(state)
            return

        self._was_ethernet_connected = state.ethernet_connected

        # Ethernet panel visibility is pure hardware state (carrier +
        # connection) and must update even while a loading operation is
        # in-flight.
        self._sync_ethernet_panel(state)

        # Sync toggle states (skipped when _is_connecting)
        self._sync_toggle_states(state)

        if self._is_connecting:
            # OFF operations: complete when radio off + no connection
            if self._pending_operation in (
                PendingOperation.WIFI_OFF,
                PendingOperation.HOTSPOT_OFF,
            ):
                if (
                    not state.wifi_enabled
                    and not state.hotspot_enabled
                    and not state.current_ssid
                ):
                    self._clear_loading()
                    self._display_disconnected_state()
                    self._emit_status_icon(state)
                    return
                # Also catch partial-off (wifi still disabling, no ssid)
                if not state.current_ssid and not state.hotspot_enabled:
                    self._clear_loading()
                    self._display_disconnected_state()
                    self._emit_status_icon(state)
                    return
                # Still transitioning — keep loading visible
                return

            # Hotspot ON: complete when hotspot_enabled + SSID + IP
            if self._pending_operation == PendingOperation.HOTSPOT_ON:
                if state.hotspot_enabled and state.current_ssid and state.current_ip:
                    self._clear_loading()
                    self._display_connected_state(state)
                    self._emit_status_icon(state)
                    return
                # Still waiting for hotspot to fully come up
                return

            if self._pending_operation in (
                PendingOperation.WIFI_ON,
                PendingOperation.CONNECT,
            ):
                if self._target_ssid and state.current_ssid == self._target_ssid:
                    if state.current_ip and state.connectivity in (
                        ConnectivityState.FULL,
                        ConnectivityState.LIMITED,
                    ):
                        self._clear_loading()
                        self._display_connected_state(state)
                        self._emit_status_icon(state)
                        return
                return

            if self._pending_operation == PendingOperation.ETHERNET_ON:
                if state.ethernet_connected:
                    self._clear_loading()
                    self._sync_ethernet_panel(state)
                    self._display_connected_state(state)
                    self._emit_status_icon(state)
                    return
                return

            if self._pending_operation == PendingOperation.ETHERNET_OFF:
                if not state.ethernet_connected:
                    self._clear_loading()
                    self._sync_ethernet_panel(state)
                    self._display_disconnected_state()
                    self._emit_status_icon(state)
                    return
                return

            # Wi-Fi static IP / DHCP reset: complete when we have the right IP.
            if self._pending_operation == PendingOperation.WIFI_STATIC_IP:
                ip = state.current_ip or ""
                expected = self._pending_expected_ip
                ip_matches = ip and (not expected or ip == expected)
                if ip_matches:
                    self._pending_expected_ip = ""
                    self._clear_loading()
                    self._display_connected_state(state)
                    self._emit_status_icon(state)
                    return
                # IP not yet correct — keep loading visible
                return

            return

        # Normal (not connecting) display updates.
        if state.ethernet_connected:
            self._display_connected_state(state)
        elif (
            state.current_ssid
            and state.current_ip
            and state.connectivity
            in (
                ConnectivityState.FULL,
                ConnectivityState.LIMITED,
            )
        ):
            self._display_connected_state(state)
        elif state.wifi_enabled or state.hotspot_enabled:
            self._display_wifi_on_no_connection()
        else:
            self._display_disconnected_state()

        self._emit_status_icon(state)
        self._sync_active_network_list_icon(state)

    @pyqtSlot(list)
    def _on_scan_complete(self, networks: list[NetworkInfo]) -> None:
        """Receive scan results, filter/sort them, and rebuild the SSID list view.

        Filters out the own hotspot SSID and networks with unsupported security
        types before populating the list view.
        """
        hotspot_ssid = self._nm.hotspot_ssid
        filtered = [
            n
            for n in networks
            if n.ssid != hotspot_ssid and is_connectable_security(n.security_type)
        ]

        current_ssid = self._nm.current_ssid
        if current_ssid:
            # Stamp the connected AP as ACTIVE so the list is correct on first
            # render even when the scan ran before the connection fully settled.
            filtered = [
                replace(net, network_status=NetworkStatus.ACTIVE)
                if net.ssid == current_ssid
                else net
                for net in filtered
            ]
            active = next((n for n in filtered if n.ssid == current_ssid), None)
            if active:
                self._active_signal = active.signal_strength
                self._last_active_signal_bars = signal_to_bars(self._active_signal)

        # Cache for signal-bar-change rebuilds
        self._cached_scan_networks = filtered

        self._build_network_list_from_scan(filtered)

        # Update panel text + header icon (both read _active_signal)
        if current_ssid:
            self.netlist_strength.setText(f"{self._active_signal}%")
            state = self._nm.current_state
            self._emit_status_icon(state)

    @pyqtSlot(list)
    def _on_saved_networks_loaded(self, networks: list[SavedNetwork]) -> None:
        """Receive saved-network data and update the priority spinbox for the active SSID."""
        logger.debug("Loaded %d saved networks", len(networks))

    @pyqtSlot(ConnectionResult)
    def _on_operation_complete(self, result: ConnectionResult) -> None:
        """Handle network operation completion."""
        logger.debug("Operation: success=%s, msg=%s", result.success, result.message)

        if result.success:
            msg_lower = result.message.lower()
            if "deleted" in msg_lower:
                ssid_deleted = (
                    self._target_ssid
                )  # capture before _clear_loading wipes it
                self._show_info_popup(result.message)
                self._clear_loading()
                self._display_wifi_on_no_connection()
                self.setCurrentIndex(self.indexOf(self.main_network_page))
                if ssid_deleted:
                    self._patch_cached_network_status(
                        ssid_deleted, NetworkStatus.DISCOVERED
                    )
            elif "hotspot" in msg_lower and "activated" in msg_lower:
                self._show_hotspot_qr(
                    self._nm.hotspot_ssid,
                    self._nm.hotspot_password,
                    self._nm.hotspot_security,
                )
            elif "hotspot disabled" in msg_lower:
                self.qrcode_img.clearPixmap()
                self.qrcode_img.setText("Hotspot not active")
            elif "wi-fi disabled" in msg_lower:
                pass
            elif "config updated" in msg_lower:
                self._show_info_popup(result.message)
            elif any(
                skip in msg_lower
                for skip in (
                    "added",
                    "connecting",
                    "disconnected",
                    "wi-fi enabled",
                )
            ):
                if (
                    ("added" in msg_lower or "connecting" in msg_lower)
                    and self._target_ssid
                    and not self._current_network_is_hidden
                ):
                    # Hidden networks are not in the scan cache; the next scan
                    # will surface them once NM reports them as saved/active.
                    self._patch_cached_network_status(
                        self._target_ssid, NetworkStatus.SAVED
                    )
            elif self._pending_operation == PendingOperation.WIFI_STATIC_IP:
                # Loading cleared by state machine (IP appears) or reconnect_complete.
                # No popup — the updated IP in the header is the confirmation.
                pass
            else:
                self._show_info_popup(result.message)
        else:
            msg_lower = result.message.lower()

            # Duplicate VLAN: clear loading and show the reason.
            if result.error_code == "duplicate_vlan":
                self._clear_loading()
                self._show_error_popup(result.message)
                return

            # When switching from ethernet to wifi, NM may report a
            # device-mismatch error because the wired profile hasn't
            # fully deactivated yet.  Retry the connection instead of
            # showing a confusing popup to the user.
            is_transient_mismatch = (
                "not compatible with device" in msg_lower
                or "mismatching interface" in msg_lower
                or "not available because profile" in msg_lower
            )
            if (
                is_transient_mismatch
                and self._pending_operation
                in (PendingOperation.WIFI_ON, PendingOperation.CONNECT)
                and self._target_ssid
            ):
                logger.debug(
                    "Transient NM device-mismatch during wifi activation "
                    "— retrying in 2 s: %s",
                    result.message,
                )
                ssid = self._target_ssid
                QTimer.singleShot(
                    2000, lambda _ssid=ssid: self._nm.connect_network(_ssid)
                )
                return  # Keep loading visible; state machine handles completion

            self._clear_loading()
            self._show_error_popup(result.message)

    @pyqtSlot(str, str)
    def _on_network_error(self, operation: str, message: str) -> None:
        """Log network errors and surface critical failures in the info box."""
        logger.error("Network error [%s]: %s", operation, message)

        if operation == "wifi_unavailable":
            self.wifi_button.setEnabled(False)
            self._show_error_popup(
                "Wi-Fi interface unavailable. Please check hardware."
            )
            return

        if operation == "device_reconnected":
            self.wifi_button.setEnabled(True)
            self._nm.refresh_state()
            return

        self._clear_loading()
        self._show_error_popup(f"Error: {message}")

    def _emit_status_icon(self, state: NetworkState) -> None:
        """Emit the correct header icon key based on current state.

        Ethernet -> ETHERNET, Hotspot -> HOTSPOT,
        Wi-Fi connected -> signal-strength key, otherwise -> 0-bar.

        Uses self._active_signal (the single source of truth) so the
        header icon always matches the list icon and panel percentage.
        """
        if state.ethernet_connected:
            self.update_wifi_icon.emit(WifiIconKey.ETHERNET)
        elif state.hotspot_enabled:
            self.update_wifi_icon.emit(WifiIconKey.HOTSPOT)
        elif state.current_ssid and state.connectivity in (
            ConnectivityState.FULL,
            ConnectivityState.LIMITED,
        ):
            self.update_wifi_icon.emit(
                WifiIconKey.from_signal(self._active_signal, False)
            )
        else:
            # Disconnected / no connection — 0-bar unprotected
            self.update_wifi_icon.emit(WifiIconKey.from_bars(0, False))

    def _sync_active_network_list_icon(self, state: NetworkState) -> None:
        """Rebuild the wifi list when the active network's signal bars or status changes.

        Between scans, state polling may report a different signal strength
        for the connected AP.  Also corrects the status label from SAVED to
        ACTIVE when the connection establishes after the last scan ran.
        Invalidates the item cache for that SSID so the next reconcile picks
        up the new icon/label, without touching other items.

        Uses self._active_signal as the single source of truth.
        """
        if not self._cached_scan_networks or not state.current_ssid:
            self._last_active_signal_bars = -1
            return

        new_bars = signal_to_bars(self._active_signal)

        # Also check whether the cached status already reflects ACTIVE.
        # If not, we must rebuild even when bars haven't changed (e.g. the
        # scan ran before the connection was fully established and marked the
        # network SAVED instead of ACTIVE).
        cached_active = next(
            (n for n in self._cached_scan_networks if n.ssid == state.current_ssid),
            None,
        )
        status_needs_update = cached_active is not None and not cached_active.is_active

        if new_bars == self._last_active_signal_bars and not status_needs_update:
            return  # No visual change — skip the rebuild

        # Invalidate cache for the active SSID so _get_or_create_item
        # creates a fresh ListItem with the updated signal icon and status.
        self._item_cache.pop(state.current_ssid, None)

        # Update the cached entry with the authoritative signal and status
        updated = [
            replace(
                net,
                signal_strength=self._active_signal,
                network_status=NetworkStatus.ACTIVE,
            )
            if net.ssid == state.current_ssid
            else net
            for net in self._cached_scan_networks
        ]

        self._cached_scan_networks = updated
        self._last_active_signal_bars = new_bars
        self._build_network_list_from_scan(updated)

    def _handle_first_run(self, state: NetworkState) -> None:
        """Run first-time UI setup once an initial state arrives (hide loading screen, etc.)."""
        self.loadingwidget.setVisible(False)
        self._is_connecting = False
        self._pending_operation = PendingOperation.NONE

        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button

        wifi_on = False
        hotspot_on = False

        if state.ethernet_connected:
            if state.wifi_enabled:
                self._nm.set_wifi_enabled(False)
            self._display_connected_state(state)
        elif state.connectivity == ConnectivityState.FULL and state.current_ssid:
            wifi_on = True
            self._display_connected_state(state)
        elif state.connectivity == ConnectivityState.LIMITED:
            hotspot_on = True
            self._display_connected_state(state)
            self._show_hotspot_qr(
                self._nm.hotspot_ssid,
                self._nm.hotspot_password,
                self._nm.hotspot_security,
            )
        elif state.wifi_enabled:
            wifi_on = True
            self._display_wifi_on_no_connection()
        else:
            self._display_disconnected_state()

        with QtCore.QSignalBlocker(wifi_btn):
            wifi_btn.state = wifi_btn.State.ON if wifi_on else wifi_btn.State.OFF
        with QtCore.QSignalBlocker(hotspot_btn):
            hotspot_btn.state = (
                hotspot_btn.State.ON if hotspot_on else hotspot_btn.State.OFF
            )

        self.wifi_button.setEnabled(True)
        self.hotspot_button.setEnabled(True)
        self.ethernet_button.setEnabled(True)
        self._sync_ethernet_panel(state)

    def _sync_toggle_states(self, state: NetworkState) -> None:
        """Synchronise Wi-Fi and hotspot toggle buttons to the current NetworkState
        without loops."""
        if self._is_connecting:
            return

        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button

        wifi_on = False
        hotspot_on = False

        if state.ethernet_connected:
            pass
        elif state.hotspot_enabled:
            hotspot_on = True
        elif state.wifi_enabled:
            wifi_on = True

        with QtCore.QSignalBlocker(wifi_btn):
            wifi_btn.state = wifi_btn.State.ON if wifi_on else wifi_btn.State.OFF
        with QtCore.QSignalBlocker(hotspot_btn):
            hotspot_btn.state = (
                hotspot_btn.State.ON if hotspot_on else hotspot_btn.State.OFF
            )

    def _sync_ethernet_panel(self, state: NetworkState) -> None:
        """Show/hide the ethernet panel and sync its toggle state.

        Visibility is driven by ``ethernet_carrier`` (cable physically
        plugged in), while the toggle position reflects the active
        connection state (``ethernet_connected``).
        """
        eth_btn = self.ethernet_button.toggle_button

        with QtCore.QSignalBlocker(eth_btn):
            eth_btn.state = (
                eth_btn.State.ON if state.ethernet_connected else eth_btn.State.OFF
            )

        # Panel visible as long as the cable is physically present
        self.ethernet_button.setVisible(state.ethernet_carrier)

    def _display_connected_state(self, state: NetworkState) -> None:
        """Display connected network information.

        Ethernet always takes display priority — if ``ethernet_connected``
        is True we show "Ethernet" even if a Wi-Fi SSID is still lingering
        (e.g. during the brief overlap before NM finishes disabling wifi).
        """
        self._hide_all_info_elements()

        is_ethernet = state.ethernet_connected

        self.netlist_ssuid.setText(
            "Ethernet" if is_ethernet else (state.current_ssid or "")
        )
        self.netlist_ssuid.setVisible(True)

        if state.current_ip:
            self.netlist_ip.setText(f"IP: {state.current_ip}")
        else:
            self.netlist_ip.setText("IP: --")
        self.netlist_ip.setVisible(True)

        # Show interface combo when ethernet is connected AND VLANs exist
        if is_ethernet and state.active_vlans:
            self.netlist_vlans_combo.blockSignals(True)
            self.netlist_vlans_combo.clear()
            self.netlist_vlans_combo.addItem(
                f"Ethernet — {state.current_ip or '--'}",
                state.current_ip or "",
            )
            for v in state.active_vlans:
                if v.is_dhcp:
                    ip_label = v.ip_address or "DHCP"
                else:
                    ip_label = v.ip_address or "--"
                self.netlist_vlans_combo.addItem(
                    f"VLAN {v.vlan_id} — {ip_label}",
                    v.ip_address or "",
                )
            self.netlist_vlans_combo.setCurrentIndex(0)
            self.netlist_vlans_combo.blockSignals(False)
            self.netlist_vlans_combo.setVisible(True)
        else:
            self.netlist_vlans_combo.setVisible(False)

        self.mn_info_seperator.setVisible(True)

        if not is_ethernet and not state.hotspot_enabled:
            signal_text = f"{self._active_signal}%" if self._active_signal > 0 else "--"
            self.netlist_strength.setText(signal_text)
            self.netlist_strength.setVisible(True)
            self.netlist_strength_label.setVisible(True)
            self.line_2.setVisible(True)

            sec_text = state.security_type.upper() if state.security_type else "OPEN"
            self.netlist_security.setText(sec_text)
            self.netlist_security.setVisible(True)
            self.netlist_security_label.setVisible(True)
            self.line_3.setVisible(True)

        self.wifi_button.setEnabled(True)
        self.hotspot_button.setEnabled(True)
        self.ethernet_button.setEnabled(True)

        self.update()

    def _display_disconnected_state(self) -> None:
        """Display disconnected state — both toggles OFF."""
        self._hide_all_info_elements()

        self.mn_info_box.setVisible(True)
        self.mn_info_box.setText(
            "There no active\ninternet connection.\nConnect via Ethernet, Wi-Fi,\nor enable a mobile hotspot\n for online features.\nPrinting functions will\nstill work offline."
        )

        self.wifi_button.setEnabled(True)
        self.hotspot_button.setEnabled(True)
        self.ethernet_button.setEnabled(True)

        self.update()

    def _display_wifi_on_no_connection(self) -> None:
        """Display info panel when Wi-Fi is on but not connected.

        Uses the same layout as the connected state but shows
        'No network connected' and empty fields.
        """
        self._hide_all_info_elements()

        self.netlist_ssuid.setText("No network connected")
        self.netlist_ssuid.setVisible(True)

        self.netlist_ip.setText("IP: --")
        self.netlist_ip.setVisible(True)

        self.mn_info_seperator.setVisible(True)

        self.netlist_strength.setText("--")
        self.netlist_strength.setVisible(True)
        self.netlist_strength_label.setVisible(True)
        self.line_2.setVisible(True)

        self.netlist_security.setText("--")
        self.netlist_security.setVisible(True)
        self.netlist_security_label.setVisible(True)
        self.line_3.setVisible(True)

        self.wifi_button.setEnabled(True)
        self.hotspot_button.setEnabled(True)
        self.ethernet_button.setEnabled(True)

        self.update()

    def _hide_all_info_elements(self) -> None:
        """Hide all info panel elements."""
        self.netlist_ip.setVisible(False)
        self.netlist_ssuid.setVisible(False)
        self.netlist_vlans_combo.setVisible(False)
        self.mn_info_seperator.setVisible(False)
        self.line_2.setVisible(False)
        self.netlist_strength.setVisible(False)
        self.netlist_strength_label.setVisible(False)
        self.line_3.setVisible(False)
        self.netlist_security.setVisible(False)
        self.netlist_security_label.setVisible(False)
        self.loadingwidget.setVisible(False)
        self.mn_info_box.setVisible(False)

    def _set_loading_state(
        self, loading: bool, timeout_ms: int = LOAD_TIMEOUT_MS
    ) -> None:
        """Set loading state with visible feedback text."""
        self.wifi_button.setEnabled(not loading)
        self.hotspot_button.setEnabled(not loading)
        self.ethernet_button.setEnabled(not loading)

        if loading:
            self._is_connecting = True
            self._hide_all_info_elements()
            self.loadingwidget.setVisible(True)

            if self._load_timer.isActive():
                self._load_timer.stop()
            self._load_timer.start(timeout_ms)
        else:
            self._is_connecting = False
            self._target_ssid = None
            self._pending_operation = PendingOperation.NONE
            self.loadingwidget.setVisible(False)

            if self._load_timer.isActive():
                self._load_timer.stop()
        self.update()

    def _clear_loading(self) -> None:
        """Hide the loading widget and re-enable the full UI."""
        self._set_loading_state(False)

    def _handle_load_timeout(self) -> None:
        """Hide the loading widget if it is still visible after the timeout fires."""
        if not self.loadingwidget.isVisible():
            return

        state = self._nm.current_state
        if (
            self._pending_operation == PendingOperation.HOTSPOT_ON
            and state.hotspot_enabled
            and state.current_ssid
        ):
            self._clear_loading()
            self._display_connected_state(state)
            return
        if (
            self._pending_operation
            in (PendingOperation.WIFI_ON, PendingOperation.CONNECT)
            and self._target_ssid
        ):
            if state.current_ssid == self._target_ssid and state.current_ip:
                self._clear_loading()
                self._display_connected_state(state)
                return
        if (
            self._pending_operation == PendingOperation.ETHERNET_ON
            and state.ethernet_connected
        ):
            self._clear_loading()
            self._sync_ethernet_panel(state)
            self._display_connected_state(state)
            return

        # Static IP / DHCP reset — if a state with an IP has arrived, accept it.
        if self._pending_operation == PendingOperation.WIFI_STATIC_IP:
            if state.current_ip:
                self._clear_loading()
                self._display_connected_state(state)
                return
            # No IP yet after timeout — clear loading and show whatever state we have.
            self._clear_loading()
            if state.current_ssid:
                self._display_connected_state(state)
            else:
                self._display_disconnected_state()
            return

        self._clear_loading()
        self._hide_all_info_elements()
        self._configure_info_box_centered()
        self.mn_info_box.setVisible(True)

        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button
        eth_btn = self.ethernet_button.toggle_button

        if self._pending_operation == PendingOperation.ETHERNET_ON:
            self.mn_info_box.setText(
                "Ethernet Connection Failed.\nCheck that the cable\nis plugged in."
            )
            with QtCore.QSignalBlocker(eth_btn):
                eth_btn.state = eth_btn.State.OFF
        elif wifi_btn.state == wifi_btn.State.ON:
            self.mn_info_box.setText(
                "Wi-Fi Connection Failed.\nThe connection attempt\ntimed out."
            )
        elif hotspot_btn.state == hotspot_btn.State.ON:
            self.mn_info_box.setText(
                "Hotspot Setup Failed.\nPlease restart the hotspot."
            )
        else:
            self.mn_info_box.setText(
                "Loading timed out.\nPlease check your connection\n and \ntry again."
            )

        self.wifi_button.setEnabled(True)
        self.hotspot_button.setEnabled(True)
        self.ethernet_button.setEnabled(True)
        self._show_error_popup("Connection timed out. Please try again.")

    def _configure_info_box_centered(self) -> None:
        """Centre-align the info box text and enable word-wrap."""
        self.mn_info_box.setWordWrap(True)
        self.mn_info_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    @QtCore.pyqtSlot(object, name="stateChange")
    def _on_toggle_state(self, new_state) -> None:
        """Route a toggle-button state change to the correct handler (Wi-Fi or hotspot)."""
        sender_button = self.sender()
        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button
        eth_btn = self.ethernet_button.toggle_button
        is_on = new_state == sender_button.State.ON

        if sender_button is wifi_btn:
            self._handle_wifi_toggle(is_on)
        elif sender_button is hotspot_btn:
            self._handle_hotspot_toggle(is_on)
        elif sender_button is eth_btn:
            self._handle_ethernet_toggle(is_on)

        # Both OFF state is now handled by _on_network_state_changed
        # when the worker emits the disconnected state.

    def _handle_wifi_toggle(self, is_on: bool) -> None:
        """Enable or disable Wi-Fi, enforcing the ethernet/hotspot mutual-exclusion rule."""
        if not is_on:
            self._target_ssid = None
            self._pending_operation = PendingOperation.WIFI_OFF
            self._set_loading_state(True)
            self._nm.set_wifi_enabled(False)
            return

        hotspot_btn = self.hotspot_button.toggle_button
        eth_btn = self.ethernet_button.toggle_button
        with QtCore.QSignalBlocker(hotspot_btn):
            hotspot_btn.state = hotspot_btn.State.OFF
        with QtCore.QSignalBlocker(eth_btn):
            eth_btn.state = eth_btn.State.OFF

        self._nm.set_wifi_enabled(True)

        # NOTE: set_wifi_enabled is dispatched to the worker — cached state
        # is STALE here (may still show ethernet).  Always proceed to the
        # saved-network connection path.

        saved = self._nm.saved_networks
        wifi_networks = [n for n in saved if "ap" not in n.mode]

        if not wifi_networks:
            self._show_warning_popup("No saved Wi-Fi networks. Please add one first.")
            self._display_wifi_on_no_connection()
            return

        # Sort by priority descending (highest priority first),
        # then by timestamp as tiebreaker — this gives "reconnect to
        # highest-priority saved network" behaviour.
        wifi_networks.sort(key=lambda n: (n.priority, n.timestamp), reverse=True)

        self._target_ssid = wifi_networks[0].ssid
        self._pending_operation = PendingOperation.WIFI_ON
        self._set_loading_state(True)

        # Non-blocking: disable hotspot then connect
        self._nm.toggle_hotspot(False)
        _ssid_to_connect = self._target_ssid
        QTimer.singleShot(500, lambda: self._nm.connect_network(_ssid_to_connect))

    def _handle_hotspot_toggle(self, is_on: bool) -> None:
        """Enable or disable the hotspot, enforcing the ethernet/Wi-Fi mutual-exclusion rule."""
        if not is_on:
            self._target_ssid = None
            self._pending_operation = PendingOperation.HOTSPOT_OFF
            self._set_loading_state(True)
            self._nm.toggle_hotspot(False)
            return

        wifi_btn = self.wifi_button.toggle_button
        eth_btn = self.ethernet_button.toggle_button
        with QtCore.QSignalBlocker(wifi_btn):
            wifi_btn.state = wifi_btn.State.OFF
        with QtCore.QSignalBlocker(eth_btn):
            eth_btn.state = eth_btn.State.OFF

        self._target_ssid = None
        self._pending_operation = PendingOperation.HOTSPOT_ON
        self._set_loading_state(True)

        hotspot_name = self.hotspot_name_input_field.text() or ""
        hotspot_pass = self.hotspot_password_input_field.text() or ""
        hotspot_sec = "wpa-psk"

        # Single atomic call: disconnect + delete stale + create + activate
        self._nm.create_hotspot(hotspot_name, hotspot_pass, hotspot_sec)

    def _handle_ethernet_toggle(self, is_on: bool) -> None:
        """Handle ethernet toggle with mutual exclusion."""
        if is_on:
            wifi_btn = self.wifi_button.toggle_button
            hotspot_btn = self.hotspot_button.toggle_button
            with QtCore.QSignalBlocker(wifi_btn):
                wifi_btn.state = wifi_btn.State.OFF
            with QtCore.QSignalBlocker(hotspot_btn):
                hotspot_btn.state = hotspot_btn.State.OFF

            self._target_ssid = None
            self._pending_operation = PendingOperation.ETHERNET_ON
            self._set_loading_state(True)
            self._nm.connect_ethernet()
            return

        self._target_ssid = None
        self._pending_operation = PendingOperation.ETHERNET_OFF
        self._set_loading_state(True)
        self._nm.disconnect_ethernet()

    @QtCore.pyqtSlot(str, str, str)
    def _on_hotspot_config_updated(
        self,
        ssid: str,
        password: str,
        security: str,  # pylint: disable=unused-argument
    ) -> None:
        """Refresh hotspot UI fields when worker reports updated config."""
        self.hotspot_name_input_field.setText(ssid)
        self.hotspot_password_input_field.setText(password)

    def _on_hotspot_config_save(self) -> None:
        """Save hotspot configuration changes.

        Reads new name/password from the UI fields, asks the worker to
        delete old profiles and create a new one.  If the hotspot was
        active, it will be re-activated with the new config (with a
        loading screen shown).
        """
        new_name = self.hotspot_name_input_field.text().strip()
        new_password = self.hotspot_password_input_field.text().strip()

        if not new_name:
            self._show_error_popup("Hotspot name cannot be empty.")
            return

        if len(new_password) < 8:
            self._show_error_popup("Hotspot password must be at least 8 characters.")
            return

        old_ssid = self._nm.hotspot_ssid

        self.setCurrentIndex(self.indexOf(self.main_network_page))

        # If hotspot is currently active, show loading for the reconnect
        hotspot_btn = self.hotspot_button.toggle_button
        if hotspot_btn.state == hotspot_btn.State.ON:
            self._target_ssid = None
            self._pending_operation = PendingOperation.HOTSPOT_ON
            self._set_loading_state(True)

        new_security = "wpa-psk"
        self._nm.update_hotspot_config(old_ssid, new_name, new_password, new_security)

    @QtCore.pyqtSlot()
    def _on_hotspot_activate(self) -> None:
        """Validate UI fields and immediately create + activate the hotspot."""
        new_name = self.hotspot_name_input_field.text().strip()
        new_password = self.hotspot_password_input_field.text().strip()

        if not new_name:
            self._show_error_popup("Hotspot name cannot be empty.")
            return

        if len(new_password) < 8:
            self._show_error_popup("Hotspot password must be at least 8 characters.")
            return

        # Mutual exclusion: turn off Wi-Fi and Ethernet
        wifi_btn = self.wifi_button.toggle_button
        eth_btn = self.ethernet_button.toggle_button
        with QtCore.QSignalBlocker(wifi_btn):
            wifi_btn.state = wifi_btn.State.OFF
        with QtCore.QSignalBlocker(eth_btn):
            eth_btn.state = eth_btn.State.OFF

        hotspot_btn = self.hotspot_button.toggle_button
        with QtCore.QSignalBlocker(hotspot_btn):
            hotspot_btn.state = hotspot_btn.State.ON

        self._target_ssid = None
        self._pending_operation = PendingOperation.HOTSPOT_ON
        self.setCurrentIndex(self.indexOf(self.main_network_page))
        self._set_loading_state(True)
        self._nm.create_hotspot(new_name, new_password, "wpa-psk")

    def _show_hotspot_qr(self, ssid: str, password: str, security: str) -> None:
        """Generate and display a WiFi QR code on the hotspot page."""
        try:
            img = generate_wifi_qrcode(ssid, password, security)
            pixmap = QtGui.QPixmap.fromImage(img)
            self.qrcode_img.setText("")
            self.qrcode_img.setPixmap(pixmap)
        except Exception as exc:  # pylint: disable=broad-except
            logger.debug("QR code generation failed: %s", exc)
            self.qrcode_img.clearPixmap()
            self.qrcode_img.setText("QR error")

    def _on_ethernet_button_clicked(self) -> None:
        """Navigate to the ethernet/VLAN settings page when the ethernet button is clicked."""
        if (
            self.ethernet_button.toggle_button.state
            == self.ethernet_button.toggle_button.State.OFF
        ):
            self._show_warning_popup("Turn on Ethernet first.")
            return
        self.setCurrentIndex(self.indexOf(self.vlan_page))

    def _on_vlan_apply(self) -> None:
        """Validate VLAN fields and call ``create_vlan_connection`` on the facade."""
        vlan_id = self.vlan_id_spinbox.value()
        ip_addr = self.vlan_ip_field.text().strip()
        mask = self.vlan_mask_field.text().strip()
        gateway = self.vlan_gateway_field.text().strip()
        dns1 = self.vlan_dns1_field.text().strip()
        dns2 = self.vlan_dns2_field.text().strip()

        if not ip_addr:
            self._show_error_popup("IP address is required.")
            return
        if not self.vlan_ip_field.is_valid():
            self._show_error_popup("Invalid IP address.")
            return
        if not self.vlan_mask_field.is_valid_mask():
            self._show_error_popup("Invalid subnet mask.")
            return
        if gateway and not self.vlan_gateway_field.is_valid():
            self._show_error_popup("Invalid gateway address.")
            return
        if dns1 and not self.vlan_dns1_field.is_valid():
            self._show_error_popup("Invalid primary DNS.")
            return
        if dns2 and not self.vlan_dns2_field.is_valid():
            self._show_error_popup("Invalid secondary DNS.")
            return

        self.setCurrentIndex(self.indexOf(self.main_network_page))
        self._pending_operation = PendingOperation.ETHERNET_ON
        self._set_loading_state(True)
        self._nm.create_vlan_connection(
            vlan_id,
            ip_addr,
            mask,
            gateway,
            dns1,
            dns2,
        )
        self._nm.request_state_soon(delay_ms=3000)

    def _on_vlan_delete(self) -> None:
        """Read the VLAN ID from the spinbox and request deletion via the facade."""
        vlan_id = self.vlan_id_spinbox.value()
        self._nm.delete_vlan_connection(vlan_id)
        self._show_warning_popup(f"VLAN {vlan_id} profile removed.")

    def _on_interface_combo_changed(self, index: int) -> None:
        """Swap the displayed IP when the user selects a different interface."""
        ip = self.netlist_vlans_combo.itemData(index)
        if ip is not None:
            self.netlist_ip.setText(f"IP: {ip}" if ip else "IP: --")

    def _on_wifi_static_ip_clicked(self) -> None:
        """Navigate from saved details page to WiFi static IP page."""
        ssid = self.snd_name.text()
        self.wifi_sip_title.setText(ssid)
        self.wifi_sip_ip_field.clear()
        self.wifi_sip_mask_field.clear()
        self.wifi_sip_gateway_field.clear()
        self.wifi_sip_dns1_field.clear()
        self.wifi_sip_dns2_field.clear()

        # Enable "Reset to DHCP" only when the profile is currently using a
        # static IP — if it is already DHCP there is nothing to reset.
        saved = self._nm.get_saved_network(ssid)
        is_dhcp = saved.is_dhcp if saved else True
        self.wifi_sip_dhcp_button.setEnabled(not is_dhcp)
        self.wifi_sip_dhcp_button.setToolTip(
            "Already using DHCP" if is_dhcp else "Reset this network to DHCP"
        )

        self.setCurrentIndex(self.indexOf(self.wifi_static_ip_page))

    def _on_wifi_static_ip_apply(self) -> None:
        """Validate static-IP fields and apply them to the current Wi-Fi connection.

        Mirrors the VLAN-creation UX: navigate to the main panel immediately,
        show the loading overlay, and clear it silently once ``reconnect_complete``
        fires (no popup — the updated IP appears in the panel header instead).
        """
        ssid = self.wifi_sip_title.text()
        ip_addr = self.wifi_sip_ip_field.text().strip()
        mask = self.wifi_sip_mask_field.text().strip()
        gateway = self.wifi_sip_gateway_field.text().strip()
        dns1 = self.wifi_sip_dns1_field.text().strip()
        dns2 = self.wifi_sip_dns2_field.text().strip()

        if not self.wifi_sip_ip_field.is_valid():
            self._show_error_popup("Invalid IP address.")
            return
        if not self.wifi_sip_mask_field.is_valid_mask():
            self._show_error_popup("Invalid subnet mask.")
            return
        if gateway and not self.wifi_sip_gateway_field.is_valid():
            self._show_error_popup("Invalid gateway address.")
            return
        if dns1 and not self.wifi_sip_dns1_field.is_valid():
            self._show_error_popup("Invalid primary DNS.")
            return
        if dns2 and not self.wifi_sip_dns2_field.is_valid():
            self._show_error_popup("Invalid secondary DNS.")
            return

        self.setCurrentIndex(self.indexOf(self.main_network_page))
        self._pending_operation = PendingOperation.WIFI_STATIC_IP
        self._pending_expected_ip: str = ip_addr  # hold loading until this IP appears
        self._active_signal = 0  # reset so signal shows "--" during reconnect
        self._set_loading_state(True)
        self._nm.update_wifi_static_ip(ssid, ip_addr, mask, gateway, dns1, dns2)
        self._nm.request_state_soon(delay_ms=3000)

    def _on_wifi_reset_dhcp(self) -> None:
        """Reset the current Wi-Fi connection back to DHCP via the facade.

        Same loading-screen pattern as static IP — no popup on success.
        """
        ssid = self.wifi_sip_title.text()
        self.setCurrentIndex(self.indexOf(self.main_network_page))
        self._pending_operation = PendingOperation.WIFI_STATIC_IP
        self._pending_expected_ip: str = ""  # any IP confirms DHCP success
        self._active_signal = 0  # reset so signal shows "--" during reconnect
        self._set_loading_state(True)
        self._nm.reset_wifi_to_dhcp(ssid)
        self._nm.request_state_soon(delay_ms=3000)

    def _build_network_list_from_scan(self, networks: list[NetworkInfo]) -> None:
        """Build/update network list from scan results.

        Uses the model's built-in reconcile() with an item cache so that
        ListItems are only allocated for networks whose visual state
        actually changed (different signal bars or status label).
        Unchanged items are reused from the cache — zero allocation.
        """
        self.listView.blockSignals(True)

        desired_items: list[ListItem] = []

        saved = [n for n in networks if n.is_saved]
        unsaved = [n for n in networks if not n.is_saved]

        for net in saved:
            item = self._get_or_create_item(net)
            if item is not None:
                desired_items.append(item)

        if saved and unsaved:
            desired_items.append(self._get_separator_item())

        for net in unsaved:
            item = self._get_or_create_item(net)
            if item is not None:
                desired_items.append(item)

        desired_items.append(self._get_hidden_network_item())

        self._model.reconcile(desired_items, self._item_key)
        self._entry_delegate.prev_index = 0
        self._sync_scrollbar()

        # Evict cache entries for SSIDs no longer in scan results
        live_ssids = {n.ssid for n in networks}
        stale = [k for k in self._item_cache if k not in live_ssids]
        for k in stale:
            del self._item_cache[k]

        self.listView.blockSignals(False)
        self.listView.update()

    def _patch_cached_network_status(self, ssid: str, status: NetworkStatus) -> None:
        """Optimistically update one entry in the scan cache and rebuild the list.

        Called immediately after add/delete so the list reflects the change
        without waiting for the next scan cycle.
        """
        self._cached_scan_networks = [
            replace(n, network_status=status) if n.ssid == ssid else n
            for n in self._cached_scan_networks
        ]
        self._item_cache.pop(ssid, None)
        self._build_network_list_from_scan(self._cached_scan_networks)

    def _get_or_create_item(self, network: NetworkInfo) -> ListItem | None:
        """Return a cached ListItem if the network's visual state is
        unchanged, otherwise create a new one and update the cache.

        Visual state = (signal_bars, status_label).  When both match
        the cached entry, the existing ListItem is returned as-is —
        no QPixmap lookup, no allocation.
        """
        if network.is_hidden or is_hidden_ssid(network.ssid):
            return None
        if not is_connectable_security(network.security_type):
            return None

        bars = signal_to_bars(network.signal_strength)
        status = network.status
        ssid = network.ssid

        cached = self._item_cache.get(ssid)
        if cached is not None:
            cached_bars, cached_status, cached_item = cached
            if cached_bars == bars and cached_status == status:
                return cached_item

        item = self._make_network_item(network)
        if item is not None:
            self._item_cache[ssid] = (bars, status, item)
        return item

    def _get_separator_item(self) -> ListItem:
        """Return the singleton separator item (created once, reused forever)."""
        if self._separator_item is None:
            self._separator_item = self._make_separator_item()
        return self._separator_item

    def _get_hidden_network_item(self) -> ListItem:
        """Return the singleton 'Connect to Hidden Network' item."""
        if self._hidden_network_item is None:
            self._hidden_network_item = self._make_hidden_network_item()
        return self._hidden_network_item

    @staticmethod
    def _item_key(item: ListItem) -> str:
        """Unique key for a list item (SSID, or sentinel for special rows)."""
        if item.not_clickable and not item.text:
            return "__separator__"
        return item.text

    def _make_network_item(self, network: NetworkInfo) -> ListItem | None:
        """Create a ListItem for a scanned network, or None if hidden/unsupported."""
        if network.is_hidden or is_hidden_ssid(network.ssid):
            return None
        if not is_connectable_security(network.security_type):
            return None

        wifi_pixmap = WifiIconProvider.get_pixmap(
            network.signal_strength, not network.is_open
        )

        return ListItem(
            text=network.ssid,
            left_icon=wifi_pixmap,
            right_text=network.status,
            right_icon=self._right_arrow_icon,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=80,
            not_clickable=False,
        )

    @staticmethod
    def _make_separator_item() -> ListItem:
        """Create a non-clickable separator item."""
        return ListItem(
            text="",
            left_icon=None,
            right_text="",
            right_icon=None,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=20,
            not_clickable=True,
        )

    def _make_hidden_network_item(self) -> ListItem:
        """Create the 'Connect to Hidden Network' entry."""
        return ListItem(
            text="Connect to Hidden Network...",
            left_icon=self._hiden_network_icon,
            right_text="",
            right_icon=self._right_arrow_icon,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=80,
            not_clickable=False,
        )

    @QtCore.pyqtSlot(ListItem, name="ssid-item-clicked")
    def _on_ssid_item_clicked(self, item: ListItem) -> None:
        """Handle a tap on an SSID list item: show the save or connect page as appropriate."""
        ssid = item.text

        if is_hidden_ssid(ssid) or ssid == "Connect to Hidden Network...":
            self.setCurrentIndex(self.indexOf(self.hidden_network_page))
            return

        network = self._nm.get_network_info(ssid)
        if not network:
            return

        # Reject unsupported security types (defence-in-depth)
        if not is_connectable_security(network.security_type):
            self._show_error_popup(
                f"'{ssid}' uses unsupported security "
                f"({network.security_type}).\n"
                "Only WPA/WPA2 networks are supported."
            )
            return

        if network.is_saved:
            self._show_saved_network_page(network)
        else:
            self._show_add_network_page(network)

    def _show_saved_network_page(self, network: NetworkInfo) -> None:
        """Populate and navigate to the saved-network detail page for *network*."""
        ssid = network.ssid

        self.saved_connection_network_name.setText(ssid)
        self.snd_name.setText(ssid)

        self.saved_connection_change_password_field.clear()
        self.saved_connection_change_password_field.setPlaceholderText(
            "Enter new password"
        )
        self.saved_connection_change_password_field.setHidden(True)
        if self.saved_connection_change_password_view.isChecked():
            self.saved_connection_change_password_view.setChecked(False)

        saved = self._nm.get_saved_network(ssid)

        if saved:
            self._set_priority_button(saved.priority)
            # Track initial values for change detection
            self._initial_priority = self._get_selected_priority()
        else:
            self._initial_priority = ConnectionPriority.MEDIUM

        # Signal strength — for the active network, use the unified
        # _active_signal so the details page matches the main panel
        # and header icon exactly.
        is_active = ssid == self._nm.current_ssid
        if is_active and self._active_signal > 0:
            signal_value = self._active_signal
        else:
            signal_value = network.signal_strength

        signal_text = f"{signal_value}%" if signal_value >= 0 else "--%"

        self.saved_connection_signal_strength_info_frame.setText(signal_text)

        if network.is_open:
            self.saved_connection_security_type_info_label.setText("OPEN")
        else:
            sec_type = saved.security_type if saved else "WPA"
            self.saved_connection_security_type_info_label.setText(sec_type.upper())

        self.network_activate_btn.setDisabled(is_active)
        self.sn_info.setText("Active Network" if is_active else "Saved Network")

        self.setCurrentIndex(self.indexOf(self.saved_connection_page))
        self.frame.update()

    def _show_add_network_page(self, network: NetworkInfo) -> None:
        """Populate and navigate to the add-network page for *network*."""
        self._current_network_is_open = network.is_open
        self._current_network_is_hidden = False

        self.add_network_network_label.setText(network.ssid)
        self.add_network_password_field.clear()

        self.frame_2.setVisible(not network.is_open)
        self.add_network_validation_button.setText(
            "Connect" if network.is_open else "Activate"
        )

        self.setCurrentIndex(self.indexOf(self.add_network_page))

    def _set_priority_button(self, priority: int | None) -> None:
        """Set priority button based on value."""
        if priority is not None and priority >= ConnectionPriority.HIGH.value:
            target = self.high_priority_btn
        elif priority is not None and priority <= ConnectionPriority.LOW.value:
            target = self.low_priority_btn
        else:
            target = self.med_priority_btn

        logger.debug(
            "Setting priority button: priority=%r -> %s", priority, target.text()
        )

        target.setChecked(True)

        self.high_priority_btn.update()
        self.med_priority_btn.update()
        self.low_priority_btn.update()

    def _get_selected_priority(self) -> ConnectionPriority:
        """Return the ``ConnectionPriority`` matching the currently selected radio button."""
        checked = self.priority_btn_group.checkedButton()
        logger.debug(
            "Priority selection: checked=%s, h=%s m=%s l=%s",
            checked.text() if checked else "None",
            self.high_priority_btn.isChecked(),
            self.med_priority_btn.isChecked(),
            self.low_priority_btn.isChecked(),
        )

        if checked is self.high_priority_btn:
            return ConnectionPriority.HIGH
        elif checked is self.low_priority_btn:
            return ConnectionPriority.LOW

        if self.high_priority_btn.isChecked():
            return ConnectionPriority.HIGH
        if self.low_priority_btn.isChecked():
            return ConnectionPriority.LOW
        return ConnectionPriority.MEDIUM

    @QtCore.pyqtSlot(name="add-network")
    def _add_network(self) -> None:
        """Add network - non-blocking."""
        self.add_network_validation_button.setEnabled(False)

        ssid = self.add_network_network_label.text()
        password = self.add_network_password_field.text()

        if not password and not self._current_network_is_open:
            self._show_error_popup("Password field cannot be empty.")
            self.add_network_validation_button.setEnabled(True)
            return

        self._target_ssid = ssid
        self._pending_operation = PendingOperation.CONNECT
        self._set_loading_state(True)

        self.add_network_password_field.clear()
        self.setCurrentIndex(self.indexOf(self.main_network_page))

        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button
        with QtCore.QSignalBlocker(wifi_btn):
            wifi_btn.state = wifi_btn.State.ON
        with QtCore.QSignalBlocker(hotspot_btn):
            hotspot_btn.state = hotspot_btn.State.OFF

        self._nm.add_network(ssid, password)

        self.add_network_validation_button.setEnabled(True)

    def _on_activate_network(self) -> None:
        """Activate the network shown on the saved-connection page."""
        ssid = self.saved_connection_network_name.text()

        self._target_ssid = ssid
        self._pending_operation = PendingOperation.CONNECT
        self._set_loading_state(True)

        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button
        with QtCore.QSignalBlocker(wifi_btn):
            wifi_btn.state = wifi_btn.State.ON
        with QtCore.QSignalBlocker(hotspot_btn):
            hotspot_btn.state = hotspot_btn.State.OFF

        self.setCurrentIndex(self.indexOf(self.main_network_page))
        self._nm.connect_network(ssid)

    def _on_delete_network(self) -> None:
        """Delete the profile shown on the saved-connection page and navigate back."""
        ssid = self.saved_connection_network_name.text()
        self._target_ssid = ssid
        self._nm.delete_network(ssid)

    def _on_save_network_details(self) -> None:
        """Save network settings changes (password / priority).

        Only performs an update if the user actually changed something.
        Shows a confirmation popup on success.
        """
        ssid = self.saved_connection_network_name.text()
        password = self.saved_connection_change_password_field.text()
        priority = self._get_selected_priority()

        password_changed = bool(password)
        priority_changed = priority != self._initial_priority

        if not password_changed and not priority_changed:
            self._show_info_popup("No changes to save.")
            return

        self._nm.update_network(
            ssid,
            password=password or "",
            priority=priority.value,
        )

        self._nm.load_saved_networks()

        # Update tracked baseline so a second press won't re-save
        self._initial_priority = priority

        self.saved_connection_change_password_field.clear()

    def _on_hidden_network_connect(self) -> None:
        """Connect to hidden network - non-blocking."""
        ssid = self.hidden_network_ssid_field.text().strip()
        password = self.hidden_network_password_field.text()

        if not ssid:
            self._show_error_popup("Please enter a network name.")
            return

        self._current_network_is_hidden = True
        self._current_network_is_open = not password
        self._target_ssid = ssid
        self._pending_operation = PendingOperation.CONNECT
        self._set_loading_state(True)

        self.hidden_network_ssid_field.clear()
        self.hidden_network_password_field.clear()

        self.setCurrentIndex(self.indexOf(self.main_network_page))

        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button
        with QtCore.QSignalBlocker(wifi_btn):
            wifi_btn.state = wifi_btn.State.ON
        with QtCore.QSignalBlocker(hotspot_btn):
            hotspot_btn.state = hotspot_btn.State.OFF

        self._nm.add_network(ssid, password)

    def _show_error_popup(self, message: str, timeout: int = 6000) -> None:
        """Display *message* in an error-styled info box with an auto-dismiss *timeout* ms."""
        self._popup.raise_()
        self._popup.new_message(
            message_type=Popup.MessageType.ERROR,
            message=message,
            timeout=timeout,
            userInput=False,
        )

    def _show_info_popup(self, message: str, timeout: int = 4000) -> None:
        """Display *message* in a neutral info box with an auto-dismiss *timeout* ms."""
        self._popup.raise_()
        self._popup.new_message(
            message_type=Popup.MessageType.INFO,
            message=message,
            timeout=timeout,
            userInput=False,
        )

    def _show_warning_popup(self, message: str, timeout: int = 5000) -> None:
        """Display *message* in a warning-styled info box with an auto-dismiss *timeout* ms."""
        self._popup.raise_()
        self._popup.new_message(
            message_type=Popup.MessageType.WARNING,
            message=message,
            timeout=timeout,
            userInput=False,
        )

    def close(self) -> bool:
        """Close and cleanup."""
        self._nm.close()
        return super().close()

    def closeEvent(self, event: QtGui.QCloseEvent | None) -> None:
        """Handle close event."""
        if self._load_timer.isActive():
            self._load_timer.stop()
        super().closeEvent(event)

    def showEvent(self, event: QtGui.QShowEvent | None) -> None:
        """Handle show event."""
        self._nm.refresh_state()
        super().showEvent(event)

    def _setupUI(self) -> None:
        """Build and lay out the entire stacked-widget UI tree."""
        self.setObjectName("wifi_stacked_page")
        self.resize(800, 480)

        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(0, 400))
        self.setMaximumSize(QtCore.QSize(16777215, 575))
        self.setStyleSheet(
            "#wifi_stacked_page{\n"
            "    background-image: url(:/background/media/1st_background.png);\n"
            "}\n"
        )

        self._popup = Popup(self)
        self._right_arrow_icon = PixmapCache.get(
            ":/arrow_icons/media/btn_icons/right_arrow.svg"
        )
        self._hiden_network_icon = PixmapCache.get(
            ":/network/media/btn_icons/network/0bar_wifi_protected.svg"
        )

        self._setup_main_network_page()
        self._setup_network_list_page()
        self._setup_add_network_page()
        self._setup_saved_connection_page()
        self._setup_saved_details_page()
        self._setup_hotspot_page()
        self._setup_hidden_network_page()
        self._setup_vlan_page()
        self._setup_wifi_static_ip_page()

        self.setCurrentIndex(0)

    def _create_white_palette(self) -> QtGui.QPalette:
        """Return a QPalette with all roles set to white (flat widget backgrounds)."""
        palette = QtGui.QPalette()
        white_brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        white_brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        grey_brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        grey_brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)

        for group in [
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorGroup.Inactive,
        ]:
            palette.setBrush(group, QtGui.QPalette.ColorRole.WindowText, white_brush)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Text, white_brush)

        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.WindowText,
            grey_brush,
        )
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Text,
            grey_brush,
        )

        return palette

    def _setup_main_network_page(self) -> None:
        """Setup the main network page."""
        self.main_network_page = QtWidgets.QWidget()
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.main_network_page.setSizePolicy(size_policy)

        main_layout = QtWidgets.QVBoxLayout(self.main_network_page)

        header_layout = QtWidgets.QHBoxLayout()

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                60,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.network_main_title = QtWidgets.QLabel(parent=self.main_network_page)
        title_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.network_main_title.setSizePolicy(title_policy)
        self.network_main_title.setMinimumSize(QtCore.QSize(300, 0))
        self.network_main_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.network_main_title.setFont(font)
        self.network_main_title.setStyleSheet("color:white")
        self.network_main_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.network_main_title.setText("Networks")

        header_layout.addWidget(self.network_main_title)

        self.network_backButton = IconButton(parent=self.main_network_page)
        self.network_backButton.setMinimumSize(QtCore.QSize(60, 60))
        self.network_backButton.setMaximumSize(QtCore.QSize(60, 60))
        self.network_backButton.setFlat(True)
        self.network_backButton.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/back.svg")
        )

        header_layout.addWidget(self.network_backButton)

        main_layout.addLayout(header_layout)

        content_layout = QtWidgets.QHBoxLayout()

        self.mn_information_layout = BlocksCustomFrame(parent=self.main_network_page)
        info_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.mn_information_layout.setSizePolicy(info_policy)
        self.mn_information_layout.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.mn_information_layout.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        info_layout = QtWidgets.QVBoxLayout(self.mn_information_layout)

        self.netlist_ssuid = QtWidgets.QLabel(parent=self.mn_information_layout)
        ssid_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.netlist_ssuid.setSizePolicy(ssid_policy)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.netlist_ssuid.setFont(font)
        self.netlist_ssuid.setStyleSheet("color: rgb(255, 255, 255);")
        self.netlist_ssuid.setText("")
        self.netlist_ssuid.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        info_layout.addWidget(self.netlist_ssuid)

        self.mn_info_seperator = QtWidgets.QFrame(parent=self.mn_information_layout)
        self.mn_info_seperator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.mn_info_seperator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        info_layout.addWidget(self.mn_info_seperator)

        self.netlist_ip = QtWidgets.QLabel(parent=self.mn_information_layout)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_ip.setFont(font)
        self.netlist_ip.setStyleSheet("color: rgb(255, 255, 255);")
        self.netlist_ip.setText("")
        self.netlist_ip.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        info_layout.addWidget(self.netlist_ip)

        self.netlist_vlans_combo = QtWidgets.QComboBox(
            parent=self.mn_information_layout
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.netlist_vlans_combo.setFont(font)
        self.netlist_vlans_combo.setMinimumSize(QtCore.QSize(240, 50))
        self.netlist_vlans_combo.setMaximumSize(QtCore.QSize(250, 50))
        self.netlist_vlans_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(26, 143, 191, 0.05);
                color: rgba(255, 255, 255, 200);
                border: 1px solid rgba(255, 255, 255, 80);
                border-radius: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: rgb(40, 40, 40);
                color: white;
                selection-background-color: rgba(26, 143, 191, 0.6);
            }
        """)

        self.netlist_vlans_combo.setVisible(False)
        self.netlist_vlans_combo.currentIndexChanged.connect(
            self._on_interface_combo_changed
        )

        info_layout.addWidget(
            self.netlist_vlans_combo, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        conn_info_layout = QtWidgets.QHBoxLayout()

        sg_info_layout = QtWidgets.QVBoxLayout()

        self.netlist_strength_label = QtWidgets.QLabel(
            parent=self.mn_information_layout
        )
        self.netlist_strength_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_strength_label.setFont(font)
        self.netlist_strength_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_strength_label.setText("Signal\nStrength")

        sg_info_layout.addWidget(self.netlist_strength_label)

        self.line_2 = QtWidgets.QFrame(parent=self.mn_information_layout)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        sg_info_layout.addWidget(self.line_2)

        self.netlist_strength = QtWidgets.QLabel(parent=self.mn_information_layout)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.netlist_strength.setFont(font)
        self.netlist_strength.setStyleSheet("color: rgb(255, 255, 255);")
        self.netlist_strength.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_strength.setText("")

        sg_info_layout.addWidget(self.netlist_strength)

        conn_info_layout.addLayout(sg_info_layout)

        sec_info_layout = QtWidgets.QVBoxLayout()

        self.netlist_security_label = QtWidgets.QLabel(
            parent=self.mn_information_layout
        )
        self.netlist_security_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_security_label.setFont(font)
        self.netlist_security_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_security_label.setText("Security\nType")

        sec_info_layout.addWidget(self.netlist_security_label)

        self.line_3 = QtWidgets.QFrame(parent=self.mn_information_layout)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        sec_info_layout.addWidget(self.line_3)

        self.netlist_security = QtWidgets.QLabel(parent=self.mn_information_layout)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.netlist_security.setFont(font)
        self.netlist_security.setStyleSheet("color: rgb(255, 255, 255);")
        self.netlist_security.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_security.setText("")

        sec_info_layout.addWidget(self.netlist_security)

        conn_info_layout.addLayout(sec_info_layout)
        info_layout.addLayout(conn_info_layout)

        self.mn_info_box = QtWidgets.QLabel(parent=self.mn_information_layout)
        self.mn_info_box.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.mn_info_box.setFont(font)
        self.mn_info_box.setStyleSheet("color: white")
        self.mn_info_box.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.mn_info_box.setText(
            "There no active\ninternet connection.\nConnect via Ethernet, Wi-Fi,\nor enable a mobile hotspot\n for online features.\nPrinting functions will\nstill work offline."
        )

        self.mn_info_box.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.mn_info_box.setWordWrap(True)
        info_layout.addWidget(self.mn_info_box)

        self.loadingwidget = LoadingOverlayWidget(parent=self.mn_information_layout)
        self.loadingwidget.setEnabled(True)
        loading_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.loadingwidget.setSizePolicy(loading_policy)
        self.loadingwidget.setText("")

        info_layout.addWidget(self.loadingwidget)

        content_layout.addWidget(self.mn_information_layout)

        option_layout = QtWidgets.QVBoxLayout()

        panel_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        font = QtGui.QFont()
        font.setPointSize(20)

        self.wifi_button = NetworkWidgetbuttons(parent=self.main_network_page)
        self.wifi_button.setSizePolicy(panel_policy)
        self.wifi_button.setMaximumSize(QtCore.QSize(400, 9999))
        self.wifi_button.setFont(font)
        self.wifi_button.setText("Wi-Fi")
        option_layout.addWidget(self.wifi_button)

        self.hotspot_button = NetworkWidgetbuttons(parent=self.main_network_page)
        self.hotspot_button.setSizePolicy(panel_policy)
        self.hotspot_button.setMaximumSize(QtCore.QSize(400, 9999))
        self.hotspot_button.setFont(font)
        self.hotspot_button.setText("Hotspot")
        option_layout.addWidget(self.hotspot_button)

        self.ethernet_button = NetworkWidgetbuttons(parent=self.main_network_page)
        self.ethernet_button.setSizePolicy(panel_policy)
        self.ethernet_button.setMaximumSize(QtCore.QSize(400, 9999))
        self.ethernet_button.setFont(font)
        self.ethernet_button.setText("Ethernet")
        self.ethernet_button.setVisible(False)
        option_layout.addWidget(self.ethernet_button)

        content_layout.addLayout(option_layout)
        main_layout.addLayout(content_layout)

        self.addWidget(self.main_network_page)

    def _setup_network_list_page(self) -> None:
        """Setup the network list page."""
        self.network_list_page = QtWidgets.QWidget()

        main_layout = QtWidgets.QVBoxLayout(self.network_list_page)

        header_layout = QtWidgets.QHBoxLayout()

        self.rescan_button = IconButton(parent=self.network_list_page)
        self.rescan_button.setMinimumSize(QtCore.QSize(60, 60))
        self.rescan_button.setMaximumSize(QtCore.QSize(60, 60))
        self.rescan_button.setText("Reload")
        self.rescan_button.setFlat(True)
        self.rescan_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/refresh.svg")
        )
        self.rescan_button.setProperty("button_type", "icon")

        header_layout.addWidget(self.rescan_button)

        self.network_list_title = QtWidgets.QLabel(parent=self.network_list_page)
        self.network_list_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.network_list_title.setPalette(self._create_white_palette())
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        self.network_list_title.setFont(title_font)
        self.network_list_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.network_list_title.setText("Wi-Fi List")

        header_layout.addWidget(self.network_list_title)

        self.nl_back_button = IconButton(parent=self.network_list_page)
        self.nl_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.nl_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.nl_back_button.setText("Back")
        self.nl_back_button.setFlat(True)
        self.nl_back_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/back.svg")
        )
        self.nl_back_button.setProperty("class", "back_btn")
        self.nl_back_button.setProperty("button_type", "icon")

        header_layout.addWidget(self.nl_back_button)

        main_layout.addLayout(header_layout)

        list_layout = QtWidgets.QHBoxLayout()

        self.listView = QtWidgets.QListView(self.network_list_page)
        list_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        list_policy.setHorizontalStretch(1)
        list_policy.setVerticalStretch(1)
        self.listView.setSizePolicy(list_policy)
        self.listView.setMinimumSize(QtCore.QSize(0, 0))
        self.listView.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.listView.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.listView.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.listView.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.listView.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.listView.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.listView.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.listView.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.listView.setUniformItemSizes(True)
        self.listView.setSpacing(5)

        QtWidgets.QScroller.grabGesture(
            self.listView,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            self.listView,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        scroller_instance = QtWidgets.QScroller.scroller(self.listView)
        scroller_props = scroller_instance.scrollerProperties()
        scroller_props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DragVelocitySmoothingFactor,
            0.05,
        )
        scroller_props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DecelerationFactor,
            0.4,
        )
        QtWidgets.QScroller.scroller(self.listView).setScrollerProperties(
            scroller_props
        )

        self.verticalScrollBar = CustomScrollBar(parent=self.network_list_page)
        scrollbar_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.verticalScrollBar.setSizePolicy(scrollbar_policy)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Orientation.Vertical)

        self.verticalScrollBar.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )

        self.listView.setVerticalScrollBar(self.verticalScrollBar)
        self.listView.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        list_layout.addWidget(self.listView)
        list_layout.addWidget(self.verticalScrollBar)

        main_layout.addLayout(list_layout)

        self.scroller = QtWidgets.QScroller.scroller(self.listView)

        self.addWidget(self.network_list_page)

    def _setup_add_network_page(self) -> None:
        """Setup the add network page."""
        self.add_network_page = QtWidgets.QWidget()

        main_layout = QtWidgets.QVBoxLayout(self.add_network_page)

        header_layout = QtWidgets.QHBoxLayout()

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                60,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.add_network_network_label = QtWidgets.QLabel(parent=self.add_network_page)
        label_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        self.add_network_network_label.setSizePolicy(label_policy)
        self.add_network_network_label.setMinimumSize(QtCore.QSize(0, 60))
        self.add_network_network_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.add_network_network_label.setFont(font)
        self.add_network_network_label.setStyleSheet("color:white")
        self.add_network_network_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.add_network_network_label.setText("TextLabel")

        header_layout.addWidget(self.add_network_network_label)

        self.add_network_page_backButton = IconButton(parent=self.add_network_page)
        self.add_network_page_backButton.setMinimumSize(QtCore.QSize(60, 60))
        self.add_network_page_backButton.setMaximumSize(QtCore.QSize(60, 60))
        self.add_network_page_backButton.setText("Back")
        self.add_network_page_backButton.setFlat(True)
        self.add_network_page_backButton.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/back.svg")
        )
        self.add_network_page_backButton.setProperty("class", "back_btn")
        self.add_network_page_backButton.setProperty("button_type", "icon")

        header_layout.addWidget(self.add_network_page_backButton)

        main_layout.addLayout(header_layout)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinimumSize
        )

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                50,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.frame_2 = BlocksCustomFrame(parent=self.add_network_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        frame_policy.setVerticalStretch(2)
        self.frame_2.setSizePolicy(frame_policy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 90))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        frame_layout_widget = QtWidgets.QWidget(parent=self.frame_2)
        frame_layout_widget.setGeometry(QtCore.QRect(10, 10, 761, 82))

        password_layout = QtWidgets.QHBoxLayout(frame_layout_widget)
        password_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMaximumSize
        )
        password_layout.setContentsMargins(0, 0, 0, 0)

        self.add_network_password_label = QtWidgets.QLabel(parent=frame_layout_widget)
        self.add_network_password_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_network_password_label.setFont(font)
        self.add_network_password_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.add_network_password_label.setText("Password")

        password_layout.addWidget(self.add_network_password_label)

        self.add_network_password_field = BlocksCustomLinEdit(
            parent=frame_layout_widget
        )
        self.add_network_password_field.setHidden(True)
        self.add_network_password_field.setMinimumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_network_password_field.setFont(font)

        password_layout.addWidget(self.add_network_password_field)

        self.add_network_password_view = IconButton(parent=frame_layout_widget)
        self.add_network_password_view.setMinimumSize(QtCore.QSize(60, 60))
        self.add_network_password_view.setMaximumSize(QtCore.QSize(60, 60))
        self.add_network_password_view.setText("View")
        self.add_network_password_view.setFlat(True)
        self.add_network_password_view.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/unsee.svg")
        )
        self.add_network_password_view.setProperty("class", "back_btn")
        self.add_network_password_view.setProperty("button_type", "icon")

        password_layout.addWidget(self.add_network_password_view)

        content_layout.addWidget(self.frame_2)

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                150,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)

        self.add_network_validation_button = BlocksCustomButton(
            parent=self.add_network_page
        )
        self.add_network_validation_button.setEnabled(True)
        btn_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        btn_policy.setHorizontalStretch(1)
        btn_policy.setVerticalStretch(1)
        self.add_network_validation_button.setSizePolicy(btn_policy)
        self.add_network_validation_button.setMinimumSize(QtCore.QSize(250, 80))
        self.add_network_validation_button.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(15)
        self.add_network_validation_button.setFont(font)
        self.add_network_validation_button.setIconSize(QtCore.QSize(16, 16))
        self.add_network_validation_button.setCheckable(False)
        self.add_network_validation_button.setChecked(False)
        self.add_network_validation_button.setFlat(True)
        self.add_network_validation_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/dialog/media/btn_icons/yes.svg")
        )
        self.add_network_validation_button.setText("Activate")
        self.add_network_validation_button.setObjectName(
            "add_network_validation_button"
        )
        button_layout.addWidget(
            self.add_network_validation_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        content_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)

        self.addWidget(self.add_network_page)

    def _setup_saved_connection_page(self) -> None:
        """Setup the saved connection page."""
        self.saved_connection_page = QtWidgets.QWidget()

        main_layout = QtWidgets.QVBoxLayout(self.saved_connection_page)

        header_layout = QtWidgets.QHBoxLayout()

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.saved_connection_network_name = QtWidgets.QLabel(
            parent=self.saved_connection_page
        )
        name_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.saved_connection_network_name.setSizePolicy(name_policy)
        self.saved_connection_network_name.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.saved_connection_network_name.setFont(font)
        self.saved_connection_network_name.setStyleSheet("color: rgb(255, 255, 255);")
        self.saved_connection_network_name.setText("")
        self.saved_connection_network_name.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.saved_connection_network_name.setObjectName(
            "saved_connection_network_name"
        )
        header_layout.addWidget(self.saved_connection_network_name)

        self.saved_connection_back_button = IconButton(
            parent=self.saved_connection_page
        )
        self.saved_connection_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.saved_connection_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.saved_connection_back_button.setFlat(True)
        self.saved_connection_back_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/back.svg")
        )
        self.saved_connection_back_button.setProperty("class", "back_btn")
        self.saved_connection_back_button.setProperty("button_type", "icon")

        header_layout.addWidget(
            self.saved_connection_back_button, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )

        main_layout.addLayout(header_layout)

        content_layout = QtWidgets.QVBoxLayout()

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        main_content_layout = QtWidgets.QHBoxLayout()

        info_layout = QtWidgets.QVBoxLayout()

        self.frame = BlocksCustomFrame(parent=self.saved_connection_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.frame.setSizePolicy(frame_policy)
        self.frame.setMaximumSize(QtCore.QSize(400, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        frame_inner_layout = QtWidgets.QVBoxLayout(self.frame)

        signal_layout = QtWidgets.QHBoxLayout()

        self.netlist_strength_label_2 = QtWidgets.QLabel(parent=self.frame)
        self.netlist_strength_label_2.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_strength_label_2.setFont(font)
        self.netlist_strength_label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_strength_label_2.setText("Signal\nStrength")

        signal_layout.addWidget(self.netlist_strength_label_2)

        self.saved_connection_signal_strength_info_frame = QtWidgets.QLabel(
            parent=self.frame
        )
        self.saved_connection_signal_strength_info_frame.setMinimumSize(
            QtCore.QSize(250, 0)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.saved_connection_signal_strength_info_frame.setFont(font)
        self.saved_connection_signal_strength_info_frame.setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.saved_connection_signal_strength_info_frame.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        signal_layout.addWidget(self.saved_connection_signal_strength_info_frame)

        frame_inner_layout.addLayout(signal_layout)

        self.line_4 = QtWidgets.QFrame(parent=self.frame)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        frame_inner_layout.addWidget(self.line_4)

        security_layout = QtWidgets.QHBoxLayout()

        self.netlist_security_label_2 = QtWidgets.QLabel(parent=self.frame)
        self.netlist_security_label_2.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_security_label_2.setFont(font)
        self.netlist_security_label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_security_label_2.setText("Security\nType")

        security_layout.addWidget(self.netlist_security_label_2)

        self.saved_connection_security_type_info_label = QtWidgets.QLabel(
            parent=self.frame
        )
        self.saved_connection_security_type_info_label.setMinimumSize(
            QtCore.QSize(250, 0)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.saved_connection_security_type_info_label.setFont(font)
        self.saved_connection_security_type_info_label.setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.saved_connection_security_type_info_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        security_layout.addWidget(self.saved_connection_security_type_info_label)

        frame_inner_layout.addLayout(security_layout)

        self.line_5 = QtWidgets.QFrame(parent=self.frame)
        self.line_5.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        frame_inner_layout.addWidget(self.line_5)

        status_layout = QtWidgets.QHBoxLayout()

        self.netlist_security_label_4 = QtWidgets.QLabel(parent=self.frame)
        self.netlist_security_label_4.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_security_label_4.setFont(font)
        self.netlist_security_label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_security_label_4.setText("Status")

        status_layout.addWidget(self.netlist_security_label_4)

        self.sn_info = QtWidgets.QLabel(parent=self.frame)
        self.sn_info.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sn_info.setFont(font)
        self.sn_info.setStyleSheet("color: rgb(255, 255, 255);")
        self.sn_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sn_info.setText("TextLabel")

        status_layout.addWidget(self.sn_info)

        frame_inner_layout.addLayout(status_layout)
        info_layout.addWidget(self.frame)
        main_content_layout.addLayout(info_layout)

        self.frame_8 = BlocksCustomFrame(parent=self.saved_connection_page)
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        buttons_layout = QtWidgets.QVBoxLayout(self.frame_8)

        self.network_activate_btn = BlocksCustomButton(parent=self.frame_8)
        self.network_activate_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.network_activate_btn.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.network_activate_btn.setFont(font)
        self.network_activate_btn.setFlat(True)
        self.network_activate_btn.setText("Connect")

        buttons_layout.addWidget(
            self.network_activate_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.network_details_btn = BlocksCustomButton(parent=self.frame_8)
        self.network_details_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.network_details_btn.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.network_details_btn.setFont(font)
        self.network_details_btn.setFlat(True)
        self.network_details_btn.setText("Details")

        buttons_layout.addWidget(
            self.network_details_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.network_delete_btn = BlocksCustomButton(parent=self.frame_8)
        self.network_delete_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.network_delete_btn.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.network_delete_btn.setFont(font)
        self.network_delete_btn.setFlat(True)
        self.network_delete_btn.setText("Forget")

        buttons_layout.addWidget(
            self.network_delete_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        main_content_layout.addWidget(self.frame_8)
        content_layout.addLayout(main_content_layout)
        main_layout.addLayout(content_layout)

        self.addWidget(self.saved_connection_page)

    def _setup_saved_details_page(self) -> None:
        """Setup the saved network details page."""
        self.saved_details_page = QtWidgets.QWidget()

        main_layout = QtWidgets.QVBoxLayout(self.saved_details_page)

        header_layout = QtWidgets.QHBoxLayout()

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                60,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.snd_name = QtWidgets.QLabel(parent=self.saved_details_page)
        name_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.snd_name.setSizePolicy(name_policy)
        self.snd_name.setMaximumSize(QtCore.QSize(16777215, 60))
        self.snd_name.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(20)
        self.snd_name.setFont(font)
        self.snd_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.snd_name.setText("SSID")

        header_layout.addWidget(self.snd_name)

        self.snd_back = IconButton(parent=self.saved_details_page)
        self.snd_back.setMinimumSize(QtCore.QSize(60, 60))
        self.snd_back.setMaximumSize(QtCore.QSize(60, 60))
        self.snd_back.setText("Back")
        self.snd_back.setFlat(True)
        self.snd_back.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/back.svg")
        )
        self.snd_back.setProperty("class", "back_btn")
        self.snd_back.setProperty("button_type", "icon")

        header_layout.addWidget(self.snd_back)

        main_layout.addLayout(header_layout)

        content_layout = QtWidgets.QVBoxLayout()

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.frame_9 = BlocksCustomFrame(parent=self.saved_details_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.frame_9.setSizePolicy(frame_policy)
        self.frame_9.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_9.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        frame_layout_widget = QtWidgets.QWidget(parent=self.frame_9)
        frame_layout_widget.setGeometry(QtCore.QRect(0, 0, 776, 62))

        password_layout = QtWidgets.QHBoxLayout(frame_layout_widget)
        password_layout.setContentsMargins(0, 0, 0, 0)

        self.saved_connection_change_password_label_3 = QtWidgets.QLabel(
            parent=frame_layout_widget
        )
        self.saved_connection_change_password_label_3.setPalette(
            self._create_white_palette()
        )
        font = QtGui.QFont()
        font.setPointSize(15)
        self.saved_connection_change_password_label_3.setFont(font)
        self.saved_connection_change_password_label_3.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.saved_connection_change_password_label_3.setText("Change\nPassword")
        self.saved_connection_change_password_label_3.setObjectName(
            "saved_connection_change_password_label_3"
        )
        password_layout.addWidget(
            self.saved_connection_change_password_label_3,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.saved_connection_change_password_field = BlocksCustomLinEdit(
            parent=frame_layout_widget
        )
        self.saved_connection_change_password_field.setHidden(True)
        self.saved_connection_change_password_field.setMinimumSize(
            QtCore.QSize(500, 60)
        )
        self.saved_connection_change_password_field.setMaximumSize(
            QtCore.QSize(500, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(12)
        self.saved_connection_change_password_field.setFont(font)
        self.saved_connection_change_password_field.setObjectName(
            "saved_connection_change_password_field"
        )
        password_layout.addWidget(
            self.saved_connection_change_password_field,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter,
        )

        self.saved_connection_change_password_view = IconButton(
            parent=frame_layout_widget
        )
        self.saved_connection_change_password_view.setMinimumSize(QtCore.QSize(60, 60))
        self.saved_connection_change_password_view.setMaximumSize(QtCore.QSize(60, 60))
        self.saved_connection_change_password_view.setText("View")
        self.saved_connection_change_password_view.setFlat(True)
        self.saved_connection_change_password_view.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/unsee.svg")
        )
        self.saved_connection_change_password_view.setProperty("class", "back_btn")
        self.saved_connection_change_password_view.setProperty("button_type", "icon")
        self.saved_connection_change_password_view.setObjectName(
            "saved_connection_change_password_view"
        )
        password_layout.addWidget(
            self.saved_connection_change_password_view,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        content_layout.addWidget(self.frame_9)

        priority_outer_layout = QtWidgets.QHBoxLayout()

        priority_inner_layout = QtWidgets.QVBoxLayout()

        self.frame_12 = BlocksCustomFrame(parent=self.saved_details_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.frame_12.setSizePolicy(frame_policy)
        self.frame_12.setMinimumSize(QtCore.QSize(400, 160))
        self.frame_12.setMaximumSize(QtCore.QSize(400, 99999))
        self.frame_12.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_12.setProperty("text", "Network priority")

        frame_inner_layout = QtWidgets.QVBoxLayout(self.frame_12)

        frame_inner_layout.addItem(
            QtWidgets.QSpacerItem(
                10,
                10,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        buttons_layout = QtWidgets.QHBoxLayout()

        self.priority_btn_group = QtWidgets.QButtonGroup(self)

        self.low_priority_btn = BlocksCustomCheckButton(parent=self.frame_12)
        self.low_priority_btn.setMinimumSize(QtCore.QSize(100, 100))
        self.low_priority_btn.setMaximumSize(QtCore.QSize(100, 100))
        self.low_priority_btn.setCheckable(True)
        self.low_priority_btn.setFlat(True)
        self.low_priority_btn.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/indf_svg.svg")
        )
        self.low_priority_btn.setText("Low")
        self.low_priority_btn.setProperty("class", "back_btn")
        self.low_priority_btn.setProperty("button_type", "icon")

        self.priority_btn_group.addButton(self.low_priority_btn)
        buttons_layout.addWidget(self.low_priority_btn)

        self.med_priority_btn = BlocksCustomCheckButton(parent=self.frame_12)
        self.med_priority_btn.setMinimumSize(QtCore.QSize(100, 100))
        self.med_priority_btn.setMaximumSize(QtCore.QSize(100, 100))
        self.med_priority_btn.setCheckable(True)
        self.med_priority_btn.setChecked(False)  # Don't set default checked
        self.med_priority_btn.setFlat(True)
        self.med_priority_btn.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/indf_svg.svg")
        )
        self.med_priority_btn.setText("Medium")
        self.med_priority_btn.setProperty("class", "back_btn")
        self.med_priority_btn.setProperty("button_type", "icon")

        self.priority_btn_group.addButton(self.med_priority_btn)
        buttons_layout.addWidget(self.med_priority_btn)

        self.high_priority_btn = BlocksCustomCheckButton(parent=self.frame_12)
        self.high_priority_btn.setMinimumSize(QtCore.QSize(100, 100))
        self.high_priority_btn.setMaximumSize(QtCore.QSize(100, 100))
        self.high_priority_btn.setCheckable(True)
        self.high_priority_btn.setChecked(False)
        self.high_priority_btn.setFlat(True)
        self.high_priority_btn.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/indf_svg.svg")
        )
        self.high_priority_btn.setText("High")
        self.high_priority_btn.setProperty("class", "back_btn")
        self.high_priority_btn.setProperty("button_type", "icon")

        self.priority_btn_group.addButton(self.high_priority_btn)
        buttons_layout.addWidget(self.high_priority_btn)

        frame_inner_layout.addLayout(buttons_layout)

        priority_inner_layout.addWidget(
            self.frame_12,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        priority_outer_layout.addLayout(priority_inner_layout)
        content_layout.addLayout(priority_outer_layout)

        bottom_btn_layout = QtWidgets.QHBoxLayout()
        bottom_btn_layout.setSpacing(20)

        self.saved_details_save_btn = BlocksCustomButton(parent=self.saved_details_page)
        self.saved_details_save_btn.setMinimumSize(QtCore.QSize(200, 80))
        self.saved_details_save_btn.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.saved_details_save_btn.setFont(font)
        self.saved_details_save_btn.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/save.svg")
        )
        self.saved_details_save_btn.setText("Save")
        bottom_btn_layout.addWidget(
            self.saved_details_save_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.wifi_static_ip_btn = BlocksCustomButton(parent=self.saved_details_page)
        self.wifi_static_ip_btn.setMinimumSize(QtCore.QSize(200, 80))
        self.wifi_static_ip_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.wifi_static_ip_btn.setFont(font)
        self.wifi_static_ip_btn.setFlat(True)
        self.wifi_static_ip_btn.setText("Static\nIP")
        self.wifi_static_ip_btn.setProperty(
            "icon_pixmap",
            PixmapCache.get(":/network/media/btn_icons/network/static_ip.svg"),
        )
        bottom_btn_layout.addWidget(
            self.wifi_static_ip_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        content_layout.addLayout(bottom_btn_layout)

        main_layout.addLayout(content_layout)

        self.addWidget(self.saved_details_page)

    def _setup_hotspot_page(self) -> None:
        """Setup the hotspot configuration page."""
        self.hotspot_page = QtWidgets.QWidget()

        main_layout = QtWidgets.QVBoxLayout(self.hotspot_page)

        header_layout = QtWidgets.QHBoxLayout()

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )
        title_font = QtGui.QFont()
        title_font.setPointSize(20)

        self.hotspot_header_title = QtWidgets.QLabel(parent=self.hotspot_page)
        self.hotspot_header_title.setPalette(self._create_white_palette())
        self.hotspot_header_title.setFont(title_font)
        self.hotspot_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hotspot_header_title.setText("Hotspot")

        header_layout.addWidget(self.hotspot_header_title)

        self.hotspot_back_button = IconButton(parent=self.hotspot_page)
        self.hotspot_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.hotspot_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.hotspot_back_button.setFlat(True)
        self.hotspot_back_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/back.svg")
        )
        self.hotspot_back_button.setProperty("class", "back_btn")
        self.hotspot_back_button.setProperty("button_type", "icon")

        header_layout.addWidget(self.hotspot_back_button)

        main_layout.addLayout(header_layout)

        self.hotspot_header_title.setMaximumSize(QtCore.QSize(16777215, 60))

        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setContentsMargins(-1, 5, -1, 5)

        # Left side: QR code frame
        self.frame_4 = QtWidgets.QFrame(parent=self.hotspot_page)
        frame_4_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.frame_4.setSizePolicy(frame_4_policy)
        qr_frame_font = QtGui.QFont()
        qr_frame_font.setPointSize(15)
        self.frame_4.setFont(qr_frame_font)
        self.frame_4.setStyleSheet("color: white;")

        frame_4_layout = QtWidgets.QHBoxLayout(self.frame_4)

        self.qrcode_img = BlocksLabel(parent=self.frame_4)
        self.qrcode_img.setMinimumSize(QtCore.QSize(325, 325))
        self.qrcode_img.setMaximumSize(QtCore.QSize(325, 325))
        qrcode_font = QtGui.QFont()
        qrcode_font.setPointSize(15)
        self.qrcode_img.setFont(qrcode_font)
        self.qrcode_img.setText("Hotspot not active")

        frame_4_layout.addWidget(self.qrcode_img)

        content_layout.addWidget(self.frame_4)

        # Right side: form fields frame
        self.frame_3 = QtWidgets.QFrame(parent=self.hotspot_page)
        self.frame_3.setMaximumWidth(350)

        frame_3_layout = QtWidgets.QVBoxLayout(self.frame_3)

        label_font = QtGui.QFont()
        label_font.setPointSize(15)
        label_font.setFamily("Momcake")
        field_font = QtGui.QFont()
        field_font.setPointSize(12)

        self.hotspot_info_name_label = QtWidgets.QLabel(parent=self.frame_3)
        name_label_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Maximum,
        )
        self.hotspot_info_name_label.setSizePolicy(name_label_policy)
        self.hotspot_info_name_label.setMinimumSize(QtCore.QSize(173, 0))
        self.hotspot_info_name_label.setPalette(self._create_white_palette())
        self.hotspot_info_name_label.setFont(label_font)
        self.hotspot_info_name_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignBottom
        )
        self.hotspot_info_name_label.setText("Hotspot Name")

        frame_3_layout.addWidget(self.hotspot_info_name_label)

        self.hotspot_name_input_field = BlocksCustomLinEdit(parent=self.frame_3)
        self.hotspot_name_input_field.setMinimumSize(QtCore.QSize(300, 40))
        self.hotspot_name_input_field.setMaximumSize(QtCore.QSize(300, 60))
        self.hotspot_name_input_field.setFont(field_font)
        self.hotspot_name_input_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)

        frame_3_layout.addWidget(
            self.hotspot_name_input_field, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.hotspot_info_password_label = QtWidgets.QLabel(parent=self.frame_3)
        self.hotspot_info_password_label.setSizePolicy(name_label_policy)
        self.hotspot_info_password_label.setMinimumSize(QtCore.QSize(173, 0))
        self.hotspot_info_password_label.setPalette(self._create_white_palette())
        self.hotspot_info_password_label.setFont(label_font)
        self.hotspot_info_password_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignBottom
        )
        self.hotspot_info_password_label.setText("Hotspot Password")

        frame_3_layout.addWidget(self.hotspot_info_password_label)

        self.hotspot_password_input_field = BlocksCustomLinEdit(parent=self.frame_3)
        self.hotspot_password_input_field.setMinimumSize(QtCore.QSize(300, 40))
        self.hotspot_password_input_field.setMaximumSize(QtCore.QSize(300, 60))
        self.hotspot_password_input_field.setFont(field_font)
        self.hotspot_password_input_field.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Password
        )

        frame_3_layout.addWidget(
            self.hotspot_password_input_field, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        frame_3_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                40,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.hotspot_change_confirm = BlocksCustomButton(parent=self.frame_3)
        self.hotspot_change_confirm.setMinimumSize(QtCore.QSize(250, 80))
        self.hotspot_change_confirm.setMaximumSize(QtCore.QSize(250, 80))
        confirm_font = QtGui.QFont()
        confirm_font.setPointSize(18)
        confirm_font.setBold(True)
        confirm_font.setWeight(75)
        self.hotspot_change_confirm.setFont(confirm_font)
        self.hotspot_change_confirm.setProperty(
            "icon_pixmap", PixmapCache.get(":/dialog/media/btn_icons/yes.svg")
        )
        self.hotspot_change_confirm.setText("Activate")

        frame_3_layout.addWidget(
            self.hotspot_change_confirm, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        content_layout.addWidget(self.frame_3)

        main_layout.addLayout(content_layout)

        self.addWidget(self.hotspot_page)

    def _setup_hidden_network_page(self) -> None:
        """Setup the hidden network page for connecting to networks with hidden SSID."""
        self.hidden_network_page = QtWidgets.QWidget()

        main_layout = QtWidgets.QVBoxLayout(self.hidden_network_page)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                60,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.hidden_network_title = QtWidgets.QLabel(parent=self.hidden_network_page)
        self.hidden_network_title.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(20)
        self.hidden_network_title.setFont(font)
        self.hidden_network_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hidden_network_title.setText("Hidden Network")
        header_layout.addWidget(self.hidden_network_title)

        self.hidden_network_back_button = IconButton(parent=self.hidden_network_page)
        self.hidden_network_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.hidden_network_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.hidden_network_back_button.setFlat(True)
        self.hidden_network_back_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/back.svg")
        )
        self.hidden_network_back_button.setProperty("button_type", "icon")
        header_layout.addWidget(self.hidden_network_back_button)

        main_layout.addLayout(header_layout)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                30,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        ssid_frame = BlocksCustomFrame(parent=self.hidden_network_page)
        ssid_frame.setMinimumSize(QtCore.QSize(0, 80))
        ssid_frame.setMaximumSize(QtCore.QSize(16777215, 90))
        ssid_frame_layout = QtWidgets.QHBoxLayout(ssid_frame)

        ssid_label = QtWidgets.QLabel("Network\nName", parent=ssid_frame)
        ssid_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        ssid_label.setFont(font)
        ssid_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        ssid_frame_layout.addWidget(ssid_label)

        self.hidden_network_ssid_field = BlocksCustomLinEdit(parent=ssid_frame)
        self.hidden_network_ssid_field.setMinimumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.hidden_network_ssid_field.setFont(font)
        self.hidden_network_ssid_field.setPlaceholderText("Enter network name")
        ssid_frame_layout.addWidget(self.hidden_network_ssid_field)

        content_layout.addWidget(ssid_frame)

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        password_frame = BlocksCustomFrame(parent=self.hidden_network_page)
        password_frame.setMinimumSize(QtCore.QSize(0, 80))
        password_frame.setMaximumSize(QtCore.QSize(16777215, 90))
        password_frame_layout = QtWidgets.QHBoxLayout(password_frame)

        password_label = QtWidgets.QLabel("Password", parent=password_frame)
        password_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        password_label.setFont(font)
        password_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        password_frame_layout.addWidget(password_label)

        self.hidden_network_password_field = BlocksCustomLinEdit(parent=password_frame)
        self.hidden_network_password_field.setHidden(True)
        self.hidden_network_password_field.setMinimumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.hidden_network_password_field.setFont(font)
        self.hidden_network_password_field.setPlaceholderText(
            "Enter password (leave empty for open networks)"
        )
        self.hidden_network_password_field.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Password
        )
        password_frame_layout.addWidget(self.hidden_network_password_field)

        self.hidden_network_password_view = IconButton(parent=password_frame)
        self.hidden_network_password_view.setMinimumSize(QtCore.QSize(60, 60))
        self.hidden_network_password_view.setMaximumSize(QtCore.QSize(60, 60))
        self.hidden_network_password_view.setFlat(True)
        self.hidden_network_password_view.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/unsee.svg")
        )
        self.hidden_network_password_view.setProperty("button_type", "icon")
        password_frame_layout.addWidget(self.hidden_network_password_view)

        content_layout.addWidget(password_frame)

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                50,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.hidden_network_connect_button = BlocksCustomButton(
            parent=self.hidden_network_page
        )
        self.hidden_network_connect_button.setMinimumSize(QtCore.QSize(250, 80))
        self.hidden_network_connect_button.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.hidden_network_connect_button.setFont(font)
        self.hidden_network_connect_button.setFlat(True)
        self.hidden_network_connect_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/dialog/media/btn_icons/yes.svg")
        )
        self.hidden_network_connect_button.setText("Connect")
        content_layout.addWidget(
            self.hidden_network_connect_button, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        main_layout.addLayout(content_layout)
        self.addWidget(self.hidden_network_page)

        self.hidden_network_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.network_list_page))
        )
        self.hidden_network_connect_button.clicked.connect(
            self._on_hidden_network_connect
        )
        self.hidden_network_ssid_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.hidden_network_page, self.hidden_network_ssid_field
            )
        )
        self.hidden_network_password_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.hidden_network_page, self.hidden_network_password_field
            )
        )
        self._setup_password_visibility_toggle(
            self.hidden_network_password_view, self.hidden_network_password_field
        )

    def _setup_vlan_page(self) -> None:
        """Construct the VLAN settings page widgets and add it to the stacked widget."""
        self.vlan_page = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(self.vlan_page)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )
        vlan_title = QtWidgets.QLabel("VLAN Configuration", parent=self.vlan_page)
        vlan_title.setPalette(self._create_white_palette())
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        vlan_title.setFont(title_font)
        vlan_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(vlan_title)

        self.vlan_back_button = IconButton(parent=self.vlan_page)
        self.vlan_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.vlan_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.vlan_back_button.setFlat(True)
        self.vlan_back_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/back.svg")
        )
        self.vlan_back_button.setProperty("button_type", "icon")
        header_layout.addWidget(self.vlan_back_button)
        main_layout.addLayout(header_layout)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setContentsMargins(-1, 5, -1, 5)

        label_font = QtGui.QFont()
        label_font.setPointSize(13)
        label_font.setBold(True)
        field_font = QtGui.QFont()
        field_font.setPointSize(12)
        field_min = QtCore.QSize(360, 45)
        field_max = QtCore.QSize(500, 55)

        def _make_row(label_text, field):
            """Build a labelled row widget containing *field* for the VLAN settings form."""
            frame = BlocksCustomFrame(parent=self.vlan_page)
            frame.setMinimumSize(QtCore.QSize(0, 50))
            frame.setMaximumSize(QtCore.QSize(16777215, 50))
            row = QtWidgets.QHBoxLayout(frame)
            row.setContentsMargins(10, 2, 10, 2)
            label = QtWidgets.QLabel(label_text, parent=frame)
            label.setPalette(self._create_white_palette())
            label.setFont(label_font)
            label.setMinimumWidth(120)
            label.setMaximumWidth(160)
            label.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            row.addWidget(label)
            field.setFont(field_font)
            field.setMinimumSize(field_min)
            field.setMaximumSize(field_max)
            row.addWidget(field)
            return frame

        self.vlan_id_spinbox = QtWidgets.QSpinBox(parent=self.vlan_page)
        self.vlan_id_spinbox.setRange(1, 4094)
        self.vlan_id_spinbox.setValue(1)
        self.vlan_id_spinbox.lineEdit().setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.vlan_id_spinbox.lineEdit().setReadOnly(True)
        # Prevent text selection when stepping — deselect after each value change
        self.vlan_id_spinbox.valueChanged.connect(
            lambda: self.vlan_id_spinbox.lineEdit().deselect()
        )
        self.vlan_id_spinbox.setStyleSheet("""
            QSpinBox {
                color: white;
                background: rgba(13,99,128,54);
                border: 1px solid rgba(255,255,255,60);
                border-radius: 8px;
                padding: 4px 8px;
                nohighlights;
            }
            QSpinBox::up-button {
                width: 55px;
                height: 22px;
            }
            QSpinBox::down-button {
                width: 55px;
                height: 22px;
            }
        """)
        content_layout.addWidget(_make_row("VLAN ID", self.vlan_id_spinbox))

        self.vlan_ip_field = IPAddressLineEdit(
            parent=self.vlan_page, placeholder="192.168.1.100"
        )
        content_layout.addWidget(_make_row("IP Address", self.vlan_ip_field))

        self.vlan_mask_field = IPAddressLineEdit(
            parent=self.vlan_page, placeholder="255.255.255.0 or 24"
        )
        content_layout.addWidget(_make_row("Subnet Mask", self.vlan_mask_field))

        self.vlan_gateway_field = IPAddressLineEdit(
            parent=self.vlan_page, placeholder="192.168.1.1"
        )
        content_layout.addWidget(_make_row("Gateway", self.vlan_gateway_field))

        self.vlan_dns1_field = IPAddressLineEdit(
            parent=self.vlan_page, placeholder="8.8.8.8"
        )
        content_layout.addWidget(_make_row("DNS 1", self.vlan_dns1_field))

        self.vlan_dns2_field = IPAddressLineEdit(
            parent=self.vlan_page, placeholder="8.8.4.4 (optional)"
        )
        content_layout.addWidget(_make_row("DNS 2", self.vlan_dns2_field))

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )
        btn_font = QtGui.QFont()
        btn_font.setPointSize(16)
        btn_font.setBold(True)

        self.vlan_apply_button = BlocksCustomButton(parent=self.vlan_page)
        self.vlan_apply_button.setMinimumSize(QtCore.QSize(180, 60))
        self.vlan_apply_button.setMaximumSize(QtCore.QSize(220, 60))
        self.vlan_apply_button.setFont(btn_font)
        self.vlan_apply_button.setText("Apply")
        self.vlan_apply_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/save.svg")
        )
        btn_layout.addWidget(
            self.vlan_apply_button, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.vlan_delete_button = BlocksCustomButton(parent=self.vlan_page)
        self.vlan_delete_button.setMinimumSize(QtCore.QSize(180, 60))
        self.vlan_delete_button.setMaximumSize(QtCore.QSize(220, 60))
        self.vlan_delete_button.setFont(btn_font)
        self.vlan_delete_button.setText("Delete")
        self.vlan_delete_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/garbage-icon.svg")
        )
        btn_layout.addWidget(
            self.vlan_delete_button, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        content_layout.addLayout(btn_layout)
        main_layout.addLayout(content_layout)
        self.addWidget(self.vlan_page)

    def _setup_wifi_static_ip_page(self) -> None:
        """Construct the Wi-Fi static-IP settings page widgets and add it to the stacked widget."""
        self.wifi_static_ip_page = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(self.wifi_static_ip_page)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )
        self.wifi_sip_title = QtWidgets.QLabel(
            "Static IP", parent=self.wifi_static_ip_page
        )
        self.wifi_sip_title.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(20)
        self.wifi_sip_title.setFont(font)
        self.wifi_sip_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.wifi_sip_title)

        self.wifi_sip_back_button = IconButton(parent=self.wifi_static_ip_page)
        self.wifi_sip_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.wifi_sip_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.wifi_sip_back_button.setFlat(True)
        self.wifi_sip_back_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/back.svg")
        )
        self.wifi_sip_back_button.setProperty("button_type", "icon")
        header_layout.addWidget(self.wifi_sip_back_button)
        main_layout.addLayout(header_layout)

        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setContentsMargins(-1, 5, -1, 5)

        label_font = QtGui.QFont()
        label_font.setPointSize(13)
        label_font.setBold(True)
        field_font = QtGui.QFont()
        field_font.setPointSize(12)
        field_min = QtCore.QSize(360, 45)
        field_max = QtCore.QSize(500, 55)

        def _make_row(label_text, field):
            """Build a labelled row widget containing *field* for the static-IP settings form."""
            frame = BlocksCustomFrame(parent=self.wifi_static_ip_page)
            frame.setMinimumSize(QtCore.QSize(0, 50))
            frame.setMaximumSize(QtCore.QSize(16777215, 50))
            row = QtWidgets.QHBoxLayout(frame)
            row.setContentsMargins(10, 2, 10, 2)
            label = QtWidgets.QLabel(label_text, parent=frame)
            label.setPalette(self._create_white_palette())
            label.setFont(label_font)
            label.setMinimumWidth(120)
            label.setMaximumWidth(160)
            label.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            row.addWidget(label)
            field.setFont(field_font)
            field.setMinimumSize(field_min)
            field.setMaximumSize(field_max)
            row.addWidget(field)
            return frame

        self.wifi_sip_ip_field = IPAddressLineEdit(
            parent=self.wifi_static_ip_page, placeholder="192.168.1.100"
        )
        content_layout.addWidget(_make_row("IP Address", self.wifi_sip_ip_field))

        self.wifi_sip_mask_field = IPAddressLineEdit(
            parent=self.wifi_static_ip_page, placeholder="255.255.255.0 or 24"
        )
        content_layout.addWidget(_make_row("Subnet Mask", self.wifi_sip_mask_field))

        self.wifi_sip_gateway_field = IPAddressLineEdit(
            parent=self.wifi_static_ip_page, placeholder="192.168.1.1"
        )
        content_layout.addWidget(_make_row("Gateway", self.wifi_sip_gateway_field))

        self.wifi_sip_dns1_field = IPAddressLineEdit(
            parent=self.wifi_static_ip_page, placeholder="8.8.8.8"
        )
        content_layout.addWidget(_make_row("DNS 1", self.wifi_sip_dns1_field))

        self.wifi_sip_dns2_field = IPAddressLineEdit(
            parent=self.wifi_static_ip_page, placeholder="8.8.4.4 (optional)"
        )
        content_layout.addWidget(_make_row("DNS 2", self.wifi_sip_dns2_field))

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_font = QtGui.QFont()
        btn_font.setPointSize(16)
        btn_font.setBold(True)

        self.wifi_sip_apply_button = BlocksCustomButton(parent=self.wifi_static_ip_page)
        self.wifi_sip_apply_button.setMinimumSize(QtCore.QSize(180, 80))
        self.wifi_sip_apply_button.setMaximumSize(QtCore.QSize(220, 80))
        self.wifi_sip_apply_button.setFont(btn_font)
        self.wifi_sip_apply_button.setText("Apply")
        self.wifi_sip_apply_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/save.svg")
        )
        btn_layout.addWidget(
            self.wifi_sip_apply_button, 0, QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        self.wifi_sip_dhcp_button = BlocksCustomButton(parent=self.wifi_static_ip_page)
        self.wifi_sip_dhcp_button.setMinimumSize(QtCore.QSize(180, 80))
        self.wifi_sip_dhcp_button.setMaximumSize(QtCore.QSize(220, 80))
        self.wifi_sip_dhcp_button.setFont(btn_font)
        self.wifi_sip_dhcp_button.setText("Reset\nDHCP")
        self.wifi_sip_dhcp_button.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/garbage-icon.svg")
        )
        btn_layout.addWidget(
            self.wifi_sip_dhcp_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        content_layout.addLayout(btn_layout)
        main_layout.addLayout(content_layout)
        self.addWidget(self.wifi_static_ip_page)

    def _setup_navigation_signals(self) -> None:
        """Connect all navigation-button clicked signals to their target page indexes."""
        self.wifi_button.clicked.connect(self._on_wifi_button_clicked)
        self.hotspot_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.hotspot_page))
        )
        self.ethernet_button.clicked.connect(self._on_ethernet_button_clicked)
        self.nl_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.main_network_page))
        )
        self.network_backButton.clicked.connect(self.hide)

        self.add_network_page_backButton.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.network_list_page))
        )
        self.saved_connection_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.network_list_page))
        )
        self.network_details_btn.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.saved_details_page))
        )
        self.hotspot_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.main_network_page))
        )
        self.hotspot_change_confirm.clicked.connect(self._on_hotspot_activate)

        self.vlan_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.main_network_page))
        )
        self.vlan_apply_button.clicked.connect(self._on_vlan_apply)
        self.vlan_delete_button.clicked.connect(self._on_vlan_delete)

        self.wifi_static_ip_btn.clicked.connect(self._on_wifi_static_ip_clicked)
        self.wifi_sip_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.saved_details_page))
        )
        self.wifi_sip_apply_button.clicked.connect(self._on_wifi_static_ip_apply)
        self.wifi_sip_dhcp_button.clicked.connect(self._on_wifi_reset_dhcp)

    def _on_wifi_button_clicked(self) -> None:
        """Navigate to the Wi-Fi scan page, starting or stopping scan polling as needed."""
        if (
            self.wifi_button.toggle_button.state
            == self.wifi_button.toggle_button.State.OFF
        ):
            self._show_warning_popup("Turn on Wi-Fi first.")
            return
        self.setCurrentIndex(self.indexOf(self.network_list_page))

    def _setup_action_signals(self) -> None:
        """Setup action signals."""
        self.add_network_validation_button.clicked.connect(self._add_network)
        self.snd_back.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.saved_connection_page))
        )
        self.saved_details_save_btn.clicked.connect(self._on_save_network_details)
        self.network_activate_btn.clicked.connect(self._on_activate_network)
        self.network_delete_btn.clicked.connect(self._on_delete_network)

    def _setup_toggle_signals(self) -> None:
        """Setup toggle button signals."""
        self.wifi_button.toggle_button.stateChange.connect(self._on_toggle_state)
        self.hotspot_button.toggle_button.stateChange.connect(self._on_toggle_state)
        self.ethernet_button.toggle_button.stateChange.connect(self._on_toggle_state)

    def _setup_password_visibility_signals(self) -> None:
        """Setup password visibility toggle signals."""
        self._setup_password_visibility_toggle(
            self.add_network_password_view,
            self.add_network_password_field,
        )
        self._setup_password_visibility_toggle(
            self.saved_connection_change_password_view,
            self.saved_connection_change_password_field,
        )

    def _setup_password_visibility_toggle(
        self, view_button: QtWidgets.QWidget, password_field: QtWidgets.QLineEdit
    ) -> None:
        """Setup password visibility toggle for a button/field pair."""
        view_button.setCheckable(True)

        see_icon = PixmapCache.get(":/ui/media/btn_icons/see.svg")
        unsee_icon = PixmapCache.get(":/ui/media/btn_icons/unsee.svg")

        view_button.toggled.connect(
            lambda checked: password_field.setHidden(not checked)
        )

        view_button.toggled.connect(
            lambda checked: view_button.setPixmap(
                unsee_icon if not checked else see_icon
            )
        )

    def _setup_icons(self) -> None:
        """Setup button icons."""
        self.hotspot_button.setPixmap(
            PixmapCache.get(":/network/media/btn_icons/hotspot.svg")
        )
        self.wifi_button.setPixmap(
            PixmapCache.get(":/network/media/btn_icons/wifi_config.svg")
        )
        self.ethernet_button.setPixmap(
            PixmapCache.get(":/network/media/btn_icons/network/ethernet_connected.svg"),
        )
        self.network_delete_btn.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/garbage-icon.svg")
        )
        self.network_activate_btn.setProperty(
            "icon_pixmap", PixmapCache.get(":/dialog/media/btn_icons/yes.svg")
        )
        self.network_details_btn.setProperty(
            "icon_pixmap", PixmapCache.get(":/ui/media/btn_icons/printer_settings.svg")
        )

    def _setup_input_fields(self) -> None:
        """Setup input field properties."""
        self.add_network_password_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)
        self.hotspot_name_input_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)
        self.hotspot_password_input_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)

        self.hotspot_password_input_field.setPlaceholderText("Defaults to: 123456789")
        self.hotspot_name_input_field.setText(str(self._nm.hotspot_ssid))

        self.hotspot_password_input_field.setText(str(self._nm.hotspot_password))

    def _setup_keyboard(self) -> None:
        """Setup the on-screen keyboard."""
        self._qwerty = CustomQwertyKeyboard(self)
        self.addWidget(self._qwerty)
        self._qwerty.value_selected.connect(self._on_qwerty_value_selected)
        self._qwerty.request_back.connect(self._on_qwerty_go_back)

        self.add_network_password_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.add_network_page, self.add_network_password_field
            )
        )
        self.hotspot_password_input_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.hotspot_page, self.hotspot_password_input_field
            )
        )
        self.hotspot_name_input_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.hotspot_page, self.hotspot_name_input_field
            )
        )
        self.saved_connection_change_password_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.saved_details_page,
                self.saved_connection_change_password_field,
            )
        )

        for field, page in [
            (self.vlan_ip_field, self.vlan_page),
            (self.vlan_mask_field, self.vlan_page),
            (self.vlan_gateway_field, self.vlan_page),
            (self.vlan_dns1_field, self.vlan_page),
            (self.vlan_dns2_field, self.vlan_page),
            (self.wifi_sip_ip_field, self.wifi_static_ip_page),
            (self.wifi_sip_mask_field, self.wifi_static_ip_page),
            (self.wifi_sip_gateway_field, self.wifi_static_ip_page),
            (self.wifi_sip_dns1_field, self.wifi_static_ip_page),
            (self.wifi_sip_dns2_field, self.wifi_static_ip_page),
        ]:
            field.clicked.connect(
                lambda _=False, f=field, p=page: self._on_show_keyboard(p, f)
            )

    def _setup_scrollbar_signals(self) -> None:
        """Setup scrollbar synchronization signals."""
        self.listView.verticalScrollBar().valueChanged.connect(
            self._handle_scrollbar_change
        )
        self.verticalScrollBar.valueChanged.connect(self._handle_scrollbar_change)
        self.verticalScrollBar.valueChanged.connect(
            lambda value: self.listView.verticalScrollBar().setValue(value)
        )
        self.verticalScrollBar.show()

    def _configure_list_view_palette(self) -> None:
        """Configure the list view palette for transparency."""
        palette = QtGui.QPalette()

        for group in [
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorGroup.Disabled,
        ]:
            transparent = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
            transparent.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Button, transparent)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Window, transparent)

            no_brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            no_brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Base, no_brush)

            highlight = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
            highlight.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Highlight, highlight)

            link = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
            link.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Link, link)

        self.listView.setPalette(palette)

    def _on_show_keyboard(
        self, panel: QtWidgets.QWidget, field: QtWidgets.QLineEdit
    ) -> None:
        """Show the QWERTY keyboard panel, saving the originating panel and input field."""
        self._previous_panel = panel
        self._current_field = field
        self._qwerty.set_value(field.text())
        self.setCurrentIndex(self.indexOf(self._qwerty))

    def _on_qwerty_go_back(self) -> None:
        """Hide the keyboard and return to the previously active panel."""
        if self._previous_panel:
            self.setCurrentIndex(self.indexOf(self._previous_panel))

    def _on_qwerty_value_selected(self, value: str) -> None:
        """Apply the keyboard-selected *value* to the previously focused input field."""
        if self._previous_panel:
            self.setCurrentIndex(self.indexOf(self._previous_panel))
        if self._current_field:
            self._current_field.setText(value)

    def _handle_scrollbar_change(self, value: int) -> None:
        """Synchronise the custom scrollbar thumb to the list-view scroll position."""
        self.verticalScrollBar.blockSignals(True)
        self.verticalScrollBar.setValue(value)
        self.verticalScrollBar.blockSignals(False)

    def _sync_scrollbar(self) -> None:
        """Push the current list-view scroll position into the custom scrollbar."""
        list_scrollbar = self.listView.verticalScrollBar()
        self.verticalScrollBar.setMinimum(list_scrollbar.minimum())
        self.verticalScrollBar.setMaximum(list_scrollbar.maximum())
        self.verticalScrollBar.setPageStep(list_scrollbar.pageStep())

    def setCurrentIndex(self, index: int) -> None:
        """Set the current page index."""
        if not self.isVisible():
            return

        if index == self.indexOf(self.add_network_page):
            self._setup_add_network_page_state()
        elif index == self.indexOf(self.saved_connection_page):
            self._setup_saved_connection_page_state()

        self.update()
        super().setCurrentIndex(index)

    def _setup_add_network_page_state(self) -> None:
        """Setup add network page state."""
        self.add_network_password_field.clear()

        if self._current_network_is_open:
            self.frame_2.setVisible(False)
            self.add_network_validation_button.setText("Connect")
        else:
            self.frame_2.setVisible(True)
            self.add_network_password_field.setPlaceholderText(
                "Insert password here, press enter when finished."
            )
            self.add_network_validation_button.setText("Activate")

    def _setup_saved_connection_page_state(self) -> None:
        """Setup saved connection page state."""
        self.saved_connection_change_password_field.clear()
        self.saved_connection_change_password_field.setPlaceholderText(
            "Change network password"
        )

    def setProperty(self, name: str, value: object) -> bool:
        """Set a property value."""
        if name == "wifi_button_pixmap":
            self._background = value
        return super().setProperty(name, value)

    @QtCore.pyqtSlot(name="call-network-panel")
    def show_network_panel(self) -> None:
        """Show the network panel."""
        if not self.parent():
            return

        self.setCurrentIndex(self.indexOf(self.network_list_page))
        parent_size = self.parent().size()
        self.setGeometry(0, 0, parent_size.width(), parent_size.height())
        self.updateGeometry()
        self.repaint()
        self.show()
        self._nm.scan_networks()

