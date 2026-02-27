# pylint: disable=protected-access

import asyncio
import logging

from PyQt6.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot

from .models import (
    ConnectionPriority,
    ConnectionResult,
    ConnectivityState,
    NetworkInfo,
    NetworkState,
    SavedNetwork,
)
from .worker import NetworkManagerWorker

logger = logging.getLogger(__name__)

_KEEPALIVE_POLL_MS: int = 300_000  # 5 minutes — safety net for missed signals


class NetworkManager(QObject):
    """Main-thread manager/interface to the NetworkManager D-Bus worker.

    The UI layer should only interact with this class.  Internally it owns
    a ``NetworkManagerWorker`` that runs all D-Bus coroutines on its
    dedicated asyncio thread.

    Coroutines are submitted to ``worker._asyncio_loop`` — the same loop
    on which the D-Bus file-descriptor was registered — so signal delivery
    and async I/O always occur on the correct selector.

    """

    state_changed = pyqtSignal(NetworkState)
    networks_scanned = pyqtSignal(list)
    saved_networks_loaded = pyqtSignal(list)
    connection_result = pyqtSignal(ConnectionResult)
    connectivity_changed = pyqtSignal(ConnectivityState)
    error_occurred = pyqtSignal(str, str)
    reconnect_complete = pyqtSignal()
    hotspot_config_updated = pyqtSignal(str, str, str)

    def __init__(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def _schedule(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    @pyqtSlot()
    def _on_worker_initialized(self) -> None:
        """Called once when the worker finishes
            D-Bus init and interface detection.

        Starts the keepalive timer *after* _primary_wifi_path and
        _primary_wired_path are populated, eliminating the old 2-second
        guess-timer that raced with init on slow boots.
        """
        if self._shutting_down:
            return
        self._worker_ready = True
        logger.info(
            "Worker initialised — starting keepalive (every %d ms)",
            _KEEPALIVE_POLL_MS,
        )
        self._keepalive_timer.start()
        self._schedule(self._worker._async_get_current_state())
        self._schedule(self._worker._async_scan_networks())
        self._schedule(self._worker._async_load_saved_networks())

    def shutdown(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def close(self) -> None:
        """Alias for ``shutdown``"""
        self.shutdown()

    @pyqtSlot(NetworkState)
    def _on_state_changed(self, state: NetworkState) -> None:
        """Cache the new state and re-emit to UI consumers."""
        if self._shutting_down:
            return
        self._cached_state = state
        self.state_changed.emit(state)

    @pyqtSlot(list)
    def _on_networks_scanned(self, networks: list) -> None:
        """Cache scan results, rebuild SSID lookup map, and re-emit."""
        if self._shutting_down:
            return
        self._cached_networks = networks
        self._network_info_map = {n.ssid: n for n in networks}
        self.networks_scanned.emit(networks)

    @pyqtSlot(list)
    def _on_saved_networks_loaded(self, networks: list) -> None:
        """Cache saved profiles, rebuild lowercase lookup map, and re-emit."""
        if self._shutting_down:
            return
        self._cached_saved = networks
        self._saved_network_map = {n.ssid.lower(): n for n in networks}
        self.saved_networks_loaded.emit(networks)

    @pyqtSlot(str, str, str)
    def _on_hotspot_info_ready(self, ssid: str, password: str, security: str) -> None:
        """Update the main-thread hotspot cache and notify UI via ``hotspot_config_updated``."""
        self._cached_hotspot_ssid = ssid
        self._cached_hotspot_password = password
        self._cached_hotspot_security = security
        self.hotspot_config_updated.emit(ssid, password, security)

    @pyqtSlot()
    def _on_keepalive_tick(self) -> None:
        """Safety-net refresh — runs every 5 min to catch any missed signals."""
        if self._shutting_down:
            return
        self._schedule(self._worker._async_get_current_state())
        self._schedule(self._worker._async_check_connectivity())
        self._schedule(self._worker._async_load_saved_networks())

    def request_state_soon(self, delay_ms: int = 500) -> None:
        """Request a state refresh after a short delay."""
        QTimer.singleShot(
            delay_ms,
            lambda: self._schedule(self._worker._async_get_current_state()),
        )

    def get_current_state(self) -> None:
        """Request an immediate state refresh from the worker."""
        self._schedule(self._worker._async_get_current_state())

    def refresh_state(self) -> None:
        """Request a state refresh and a saved-network reload from the worker."""
        self._schedule(self._worker._async_get_current_state())
        self._schedule(self._worker._async_load_saved_networks())

    def scan_networks(self) -> None:
        """Request an immediate Wi-Fi scan from the worker."""
        self._schedule(self._worker._async_scan_networks())

    def load_saved_networks(self) -> None:
        """Request a reload of saved connection profiles from the worker."""
        self._schedule(self._worker._async_load_saved_networks())

    def check_connectivity(self) -> None:
        """Request an NM connectivity check from the worker."""
        self._schedule(self._worker._async_check_connectivity())

    def add_network(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(self._worker._async_add_network(ssid, password, priority))

    def connect_network(self, ssid: str) -> None:
        """Connect to an already-saved network by *ssid*."""
        self._schedule(self._worker._async_connect_network(ssid))

    def disconnect(self) -> None:
        """Disconnect the currently active Wi-Fi connection."""
        self._schedule(self._worker._async_disconnect())

    def delete_network(self, ssid: str) -> None:
        """Delete the saved profile for *ssid*."""
        self._schedule(self._worker._async_delete_network(ssid))

    def update_network(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(ssid, password, priority))

    def set_wifi_enabled(self, enabled: bool) -> None:
        """Enable or disable the Wi-Fi radio."""
        self._schedule(self._worker._async_set_wifi_enabled(enabled))

    def create_hotspot(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, password, security)
        )

    def toggle_hotspot(self, enable: bool) -> None:
        """Deactivate the hotspot (enable=False) or create+activate (enable=True)."""
        self._schedule(self._worker._async_toggle_hotspot(enable))

    def update_hotspot_config(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, new_ssid, new_password, security
            )
        )

    def disconnect_ethernet(self) -> None:
        """Deactivate the primary wired interface."""
        self._schedule(self._worker._async_disconnect_ethernet())

    def connect_ethernet(self) -> None:
        """Activate the primary wired interface."""
        self._schedule(self._worker._async_connect_ethernet())

    def create_vlan_connection(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def delete_vlan_connection(self, vlan_id: int) -> None:
        """Delete all NM profiles for *vlan_id*."""
        self._schedule(self._worker._async_delete_vlan(vlan_id))

    def update_wifi_static_ip(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def reset_wifi_to_dhcp(self, ssid: str) -> None:
        """Reset a saved Wi-Fi profile back to DHCP."""
        self._schedule(self._worker._async_reset_wifi_to_dhcp(ssid))

    @property
    def current_state(self) -> NetworkState:
        """Most recently cached ``NetworkState`` snapshot."""
        return self._cached_state

    @property
    def current_ssid(self) -> str | None:
        """SSID of the currently active Wi-Fi connection, or ``None``."""
        return self._cached_state.current_ssid

    @property
    def saved_networks(self) -> list[SavedNetwork]:
        """Most recently cached list of saved ``SavedNetwork`` profiles."""
        return self._cached_saved

    @property
    def hotspot_ssid(self) -> str:
        """Hotspot SSID — read from main-thread cache (thread-safe)."""
        return self._cached_hotspot_ssid

    @property
    def hotspot_password(self) -> str:
        """Hotspot password — read from main-thread cache (thread-safe)."""
        return self._cached_hotspot_password

    @property
    def hotspot_security(self) -> str:
        """Hotspot security type — always 'wpa-psk' (WPA2-PSK, thread-safe)."""
        return self._cached_hotspot_security

    def get_network_info(self, ssid: str) -> NetworkInfo | None:
        """Return the scanned ``NetworkInfo`` for *ssid*, or ``None``."""
        return self._network_info_map.get(ssid)

    def get_saved_network(self, ssid: str) -> SavedNetwork | None:
        """Return the saved ``SavedNetwork`` for *ssid* (case-insensitive)."""
        return self._saved_network_map.get(ssid.lower())
