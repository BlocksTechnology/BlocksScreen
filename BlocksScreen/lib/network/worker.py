import asyncio
import fcntl
import ipaddress
import logging
import os
import socket as _socket
import struct
import threading
from uuid import uuid4

import sdbus
from configfile import get_configparser
from PyQt6.QtCore import QObject, pyqtSignal
from sdbus_async import networkmanager as dbus_nm

from .models import (
    ConnectionPriority,
    ConnectionResult,
    ConnectivityState,
    HotspotConfig,
    HotspotSecurity,
    NetworkInfo,
    NetworkState,
    NetworkStatus,
    SavedNetwork,
    SecurityType,
    VlanInfo,
    is_connectable_security,
    is_hidden_ssid,
)

logger = logging.getLogger(__name__)

_CAN_RELOAD_CONNECTIONS: bool = os.getuid() == 0

# Debounce window for coalescing rapid D-Bus signal bursts (seconds).
_DEBOUNCE_DELAY: float = 0.8
# Delay before restarting a failed signal listener (seconds).
_LISTENER_RESTART_DELAY: float = 3.0
# Timeout for _wait_for_connection: must cover 802.11 handshake + DHCP.
_WIFI_CONNECT_TIMEOUT: float = 20.0


class NetworkManagerWorker(QObject):
    """Async NetworkManager worker (signal-reactive).

    Owns an asyncio event loop running on a dedicated daemon thread.
    All D-Bus operations execute as coroutines on that loop.

    Primary state updates are driven by D-Bus signals, not polling.
    """

    state_changed = pyqtSignal(NetworkState, name="stateChanged")
    networks_scanned = pyqtSignal(list, name="networksScanned")
    saved_networks_loaded = pyqtSignal(list, name="savedNetworksLoaded")
    connection_result = pyqtSignal(ConnectionResult, name="connectionResult")
    connectivity_changed = pyqtSignal(ConnectivityState, name="connectivityChanged")
    error_occurred = pyqtSignal(str, str, name="errorOccurred")
    hotspot_info_ready = pyqtSignal(str, str, str, name="hotspotInfoReady")
    reconnect_complete = pyqtSignal(name="reconnectComplete")

    _MAX_DBUS_ERRORS_BEFORE_RECONNECT: int = 3

    initialized = pyqtSignal(name="workerInitialized")

    def __init__(self) -> None:
        """Initialise the worker, creating the asyncio loop and daemon thread.

        Sets up all instance state (interface paths, hotspot config, signal
        proxies, debounce handles) and immediately starts the asyncio daemon
        thread that opens the system D-Bus and drives all NetworkManager
        coroutines.
        """
        super().__init__()
        self._running: bool = False
        self._system_bus: sdbus.SdBus | None = None

        # Path strings only — read-proxies are always created fresh.
        self._primary_wifi_path: str = ""
        self._primary_wifi_iface: str = ""
        self._primary_wired_path: str = ""
        self._primary_wired_iface: str = ""

        self._iface_to_device_path: dict[str, str] = {}

        self._hotspot_config = HotspotConfig()
        self._load_hotspot_config()
        self._saved_cache: list[SavedNetwork] = []
        self._saved_cache_dirty: bool = True
        self._is_hotspot_active: bool = False
        self._consecutive_dbus_errors: int = 0

        self._background_tasks: set[asyncio.Task] = set()

        self._signal_nm: dbus_nm.NetworkManager | None = None
        self._signal_wifi: dbus_nm.NetworkDeviceWireless | None = None
        self._signal_wired: dbus_nm.NetworkDeviceGeneric | None = None
        self._signal_settings: dbus_nm.NetworkManagerSettings | None = None

        self._state_debounce_handle: asyncio.TimerHandle | None = None
        self._scan_debounce_handle: asyncio.TimerHandle | None = None

        # Tracked for cancellation during shutdown.
        self._listener_tasks: list[asyncio.Task] = []

        # Asyncio loop — created here, driven on the daemon thread.
        self.stop_event = asyncio.Event()
        self.stop_event.clear()
        self._asyncio_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self._asyncio_thread = threading.Thread(
            target=self._run_asyncio_loop,
            daemon=True,
            name="NetworkManagerAsyncLoop",
        )
        self._asyncio_thread.start()

    def _run_asyncio_loop(self) -> None:
        """Open the system D-Bus and run the asyncio event loop on this thread."""
        asyncio.set_event_loop(self._asyncio_loop)
        try:
            self._system_bus = sdbus.sd_bus_open_system()
            sdbus.set_default_bus(self._system_bus)
            self._track_task(
                self._asyncio_loop.create_task(self._async_initialize(), name="nm_init")
            )
            logger.debug(
                "D-Bus opened on asyncio thread '%s'",
                threading.current_thread().name,
            )
        except Exception as exc:
            logger.error("Failed to open system D-Bus: %s", exc)
        self._asyncio_loop.run_forever()

    def _track_task(self, task: asyncio.Task) -> None:
        """Register a background task so it is cancelled on shutdown."""
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    async def _async_shutdown(self) -> None:
        """Tear down all async state and stop the event loop."""
        self._running = False

        for task in self._listener_tasks:
            if not task.done():
                task.cancel()
        self._listener_tasks.clear()

        if self._state_debounce_handle:
            self._state_debounce_handle.cancel()
            self._state_debounce_handle = None
        if self._scan_debounce_handle:
            self._scan_debounce_handle.cancel()
            self._scan_debounce_handle = None

        self._signal_nm = None
        self._signal_wifi = None
        self._signal_wired = None
        self._signal_settings = None

        self._primary_wifi_path = ""
        self._primary_wifi_iface = ""
        self._primary_wired_path = ""
        self._primary_wired_iface = ""
        self._iface_to_device_path.clear()
        self._saved_cache.clear()


        for task in list(self._background_tasks):
            if not task.done():
                task.cancel()
        self._background_tasks.clear()
        self._system_bus = None
        logger.info("NetworkManagerWorker async shutdown complete")
        self._asyncio_loop.call_soon_threadsafe(self._asyncio_loop.stop)

    def _nm(self) -> dbus_nm.NetworkManager:
        """Return a fresh NetworkManager root D-Bus proxy."""
        return dbus_nm.NetworkManager(bus=self._system_bus)

    def _generic(self, path: str) -> dbus_nm.NetworkDeviceGeneric:
        """Return a fresh generic network device D-Bus proxy for the given path."""
        return dbus_nm.NetworkDeviceGeneric(bus=self._system_bus, device_path=path)

    def _wifi(self, path: str | None = None) -> dbus_nm.NetworkDeviceWireless:
        """Return a fresh wireless device D-Bus proxy (defaults to primary Wi-Fi path)."""
        return dbus_nm.NetworkDeviceWireless(
            bus=self._system_bus,
            device_path=path or self._primary_wifi_path,
        )

    def _wired(self, path: str | None = None) -> dbus_nm.NetworkDeviceWired:
        """Return a fresh wired device D-Bus proxy (defaults to primary wired path)."""
        return dbus_nm.NetworkDeviceWired(
            bus=self._system_bus,
            device_path=path or self._primary_wired_path,
        )

    def _get_wifi_iface_name(self) -> str:
        """Return the detected Wi-Fi interface name.

        ``_primary_wifi_iface`` is set atomically with ``_primary_wifi_path``
        in ``_detect_interfaces()``.  The dict-lookup and ``"wlan0"`` branches
        are defensive fallbacks in case the two somehow diverge.
        """
        if self._primary_wifi_iface:
            return self._primary_wifi_iface
        for iface, path in self._iface_to_device_path.items():
            if path == self._primary_wifi_path:
                return iface
        return "wlan0"  # safe fallback

    def _active_conn(self, path: str) -> dbus_nm.ActiveConnection:
        """Return a fresh ActiveConnection D-Bus proxy for the given path."""
        return dbus_nm.ActiveConnection(bus=self._system_bus, connection_path=path)

    def _conn_settings(self, path: str) -> dbus_nm.NetworkConnectionSettings:
        """Return a fresh NetworkConnectionSettings D-Bus proxy for the given path."""
        return dbus_nm.NetworkConnectionSettings(
            bus=self._system_bus, settings_path=path
        )

    def _nm_settings(self) -> dbus_nm.NetworkManagerSettings:
        """Return a fresh NetworkManagerSettings D-Bus proxy."""
        return dbus_nm.NetworkManagerSettings(bus=self._system_bus)

    def _ap(self, path: str) -> dbus_nm.AccessPoint:
        """Return a fresh AccessPoint D-Bus proxy for the given path."""
        return dbus_nm.AccessPoint(bus=self._system_bus, point_path=path)

    def _ipv4(self, path: str) -> dbus_nm.IPv4Config:
        """Return a fresh IPv4Config D-Bus proxy for the given path."""
        return dbus_nm.IPv4Config(bus=self._system_bus, ip4_path=path)

    def _ensure_signal_proxies(self) -> None:
        """Create or recreate persistent proxies for D-Bus signal listening.

        These proxies are NOT used for property reads (to avoid the
        sdbus_async caching bug).  They exist solely so the ``async for``
        signal iterators stay alive.  Must be called on the asyncio thread.
        """
        if self._signal_nm is None:
            self._signal_nm = dbus_nm.NetworkManager(bus=self._system_bus)

        if self._signal_wifi is None and self._primary_wifi_path:
            self._signal_wifi = dbus_nm.NetworkDeviceWireless(
                bus=self._system_bus,
                device_path=self._primary_wifi_path,
            )

        if self._signal_wired is None and self._primary_wired_path:
            self._signal_wired = dbus_nm.NetworkDeviceGeneric(
                bus=self._system_bus,
                device_path=self._primary_wired_path,
            )

        if self._signal_settings is None:
            self._signal_settings = dbus_nm.NetworkManagerSettings(
                bus=self._system_bus,
            )

    def get_ip_by_interface(self, interface: str = "wlan0") -> str:
        """Return the current IPv4 address for *interface*, blocking up to 5 s."""
        future = asyncio.run_coroutine_threadsafe(
            self._get_ip_by_interface(interface), self._asyncio_loop
        )
        try:
            return future.result(timeout=5.0)
        except Exception:
            # Timeout or cancellation from the async loop; caller treats "" as unknown.
            return ""

    @property
    def hotspot_ssid(self) -> str:
        """The SSID configured for the hotspot."""
        return self._hotspot_config.ssid

    @property
    def hotspot_password(self) -> str:
        """The password configured for the hotspot."""
        return self._hotspot_config.password

    async def _async_initialize(self) -> None:
        """Bootstrap the worker on the asyncio thread.

        Detects network interfaces, enforces the boot-time ethernet/Wi-Fi
        mutual exclusion, activates any saved VLANs if ethernet is present,
        triggers an initial Wi-Fi scan, and starts all D-Bus signal listeners.
        Emits ``initialized`` when done (even on failure, so the manager can
        unblock its caller).
        """
        try:
            if not self._system_bus:
                self.error_occurred.emit("initialize", "No D-Bus connection")
                return

            self._running = True
            await self._detect_interfaces()
            await self._enforce_boot_mutual_exclusion()

            if await self._is_ethernet_connected():
                await self._activate_saved_vlans()

            self.hotspot_info_ready.emit(
                self._hotspot_config.ssid,
                self._hotspot_config.password,
                self._hotspot_config.security,
            )

            if self._primary_wifi_path:
                try:
                    await self._wifi().request_scan({})
                except Exception as exc:
                    logger.debug("Initial Wi-Fi scan request ignored: %s", exc)

            await self._start_signal_listeners()

            logger.info(
                "NetworkManagerWorker initialised on thread '%s' "
                "(sdbus_async, signal-reactive)",
                threading.current_thread().name,
            )
            self.initialized.emit()
        except Exception as exc:
            logger.exception("Failed to initialise NetworkManagerWorker")
            self.error_occurred.emit("initialize", str(exc))
            self.initialized.emit()

    async def _detect_interfaces(self) -> None:
        """Enumerate NM devices and record the primary Wi-Fi and Ethernet paths.

        Iterates all NetworkManager devices, maps interface names to D-Bus
        object paths, and stores the first WIFI and ETHERNET device found as
        the primary interfaces used for all subsequent operations.  Emits
        ``error_occurred`` if no interfaces at all are found.
        """
        try:
            devices = await self._nm().get_devices()
            for device_path in devices:
                device = self._generic(device_path)
                device_type = await device.device_type
                iface_name = await self._generic(device_path).interface
                if iface_name:
                    self._iface_to_device_path[iface_name] = device_path

                if (
                    device_type == dbus_nm.enums.DeviceType.WIFI
                    and not self._primary_wifi_path
                ):
                    self._primary_wifi_path = device_path
                    self._primary_wifi_iface = iface_name
                elif (
                    device_type == dbus_nm.enums.DeviceType.ETHERNET
                    and not self._primary_wired_path
                ):
                    self._primary_wired_path = device_path
                    self._primary_wired_iface = iface_name
        except Exception as exc:
            logger.error("Failed to detect interfaces: %s", exc)

        if not self._primary_wifi_path and not self._primary_wired_path:
            # Both absent — likely D-Bus not ready yet or no hardware present.
            logger.warning("No network interfaces detected after scan")
            self.error_occurred.emit("wifi_unavailable", "No network device found")
        elif not self._primary_wifi_path:
            # Ethernet-only or Wi-Fi driver still loading — log but don't alarm.
            logger.warning("No Wi-Fi interface detected; ethernet-only mode")

    async def _enforce_boot_mutual_exclusion(self) -> None:
        """Disable Wi-Fi at boot if ethernet is already connected.

        Prevents the device from simultaneously using both interfaces at
        startup.  If ethernet is active and the Wi-Fi radio is on, the Wi-Fi
        device is disconnected and the radio is disabled, then we wait up to
        8 s for the radio to confirm it is off.  Failures are logged but not
        propagated — a non-fatal best-effort action at boot.
        """
        try:
            if not await self._is_ethernet_connected():
                return
            if not await self._nm().wireless_enabled:
                return
            logger.info("Boot: ethernet active + Wi-Fi enabled — disabling Wi-Fi")
            if self._primary_wifi_path:
                try:
                    await self._wifi().disconnect()
                except Exception as exc:
                    logger.debug("Pre-radio-disable disconnect ignored: %s", exc)
            await self._nm().wireless_enabled.set_async(False)
            await self._wait_for_wifi_radio(False, timeout=8.0)
            self._is_hotspot_active = False
        except Exception as exc:
            logger.warning("Boot mutual exclusion failed (non-fatal): %s", exc)

    async def _start_signal_listeners(self) -> None:
        """Create persistent proxies and spawn all D-Bus signal listeners.

        Each listener runs in its own Task and automatically restarts
        after transient errors (with a back-off delay).
        """
        self._ensure_signal_proxies()

        listeners = [
            ("nm_state", self._listen_nm_state_changed),
            ("wifi_ap_added", self._listen_ap_added),
            ("wifi_ap_removed", self._listen_ap_removed),
            ("wired_state", self._listen_wired_state_changed),
            ("wifi_state", self._listen_wifi_state_changed),
            ("settings_conn_added", self._listen_settings_new_connection),
            ("settings_conn_removed", self._listen_settings_connection_removed),
        ]

        for name, coro_fn in listeners:
            task = self._asyncio_loop.create_task(
                self._resilient_listener(name, coro_fn),
                name=f"listener_{name}",
            )
            self._listener_tasks.append(task)
            self._track_task(task)

        logger.info("Started %d D-Bus signal listeners", len(self._listener_tasks))

    async def _resilient_listener(
        self, name: str, listener_fn: "asyncio.coroutines"
    ) -> None:
        """Wrapper that restarts *listener_fn* on failure with back-off."""
        while self._running:
            try:
                await listener_fn()
            except asyncio.CancelledError:
                logger.debug("Listener '%s' cancelled", name)
                return
            except Exception as exc:
                if not self._running:
                    return
                logger.warning(
                    "Listener '%s' failed: %s — restarting in %.1f s",
                    name,
                    exc,
                    _LISTENER_RESTART_DELAY,
                )
                # Rebuild signal proxies in case the bus was reset
                self._signal_nm = None
                self._signal_wifi = None
                self._signal_wired = None
                self._signal_settings = None
                await asyncio.sleep(_LISTENER_RESTART_DELAY)
                if self._running:
                    self._ensure_signal_proxies()

    async def _listen_nm_state_changed(self) -> None:
        """React to NetworkManager global state transitions."""
        if not self._signal_nm:
            return
        logger.debug("NM StateChanged listener started")
        async for state_value in self._signal_nm.state_changed:
            if not self._running:
                return
            try:
                nm_state = dbus_nm.NetworkManagerState(state_value)
                logger.debug(
                    "NM StateChanged: %s (%d)",
                    nm_state.name,
                    state_value,
                )
            except ValueError:
                logger.debug("NM StateChanged: unknown (%d)", state_value)

            self._schedule_debounced_state_rebuild()
            self._schedule_debounced_scan()

    async def _listen_ap_added(self) -> None:
        """React to new access points appearing in scan results.

        Triggers a debounced scan rebuild (not a full rescan — NM has
        already updated its internal AP list).
        """
        if not self._signal_wifi:
            return
        logger.debug("AP Added listener started on %s", self._primary_wifi_path)
        async for ap_path in self._signal_wifi.access_point_added:
            if not self._running:
                return
            logger.debug("AP added: %s", ap_path)
            self._schedule_debounced_scan()

    async def _listen_ap_removed(self) -> None:
        """React to access points disappearing from scan results."""
        if not self._signal_wifi:
            return
        logger.debug("AP Removed listener started on %s", self._primary_wifi_path)
        async for ap_path in self._signal_wifi.access_point_removed:
            if not self._running:
                return
            logger.debug("AP removed: %s", ap_path)
            self._schedule_debounced_scan()

    async def _listen_wired_state_changed(self) -> None:
        """React to wired device state transitions (cable plug/unplug).

        The ``state_changed`` signal on the Device interface emits
        ``(new_state, old_state, reason)`` with signature ``'uuu'``.
        """
        if not self._signal_wired:
            return
        logger.debug("Wired state listener started on %s", self._primary_wired_path)
        async for new_state, old_state, reason in self._signal_wired.state_changed:
            if not self._running:
                return
            logger.debug(
                "Wired state: %d -> %d (reason %d)",
                old_state,
                new_state,
                reason,
            )
            self._schedule_debounced_state_rebuild()

    async def _listen_wifi_state_changed(self) -> None:
        """React to Wi-Fi device state transitions.

        Detects enabled/disabled, connecting, disconnected transitions
        instantly — complements the NM global ``state_changed`` signal
        which may not fire for all device-level transitions.
        """
        if not self._signal_wifi:
            return
        logger.debug("Wi-Fi state listener started on %s", self._primary_wifi_path)
        async for new_state, old_state, reason in self._signal_wifi.state_changed:
            if not self._running:
                return
            logger.debug(
                "Wi-Fi state: %d -> %d (reason %d)",
                old_state,
                new_state,
                reason,
            )
            self._schedule_debounced_state_rebuild()

    async def _listen_settings_new_connection(self) -> None:
        """React to new saved connection profiles being added."""
        if not self._signal_settings:
            return
        logger.debug("Settings NewConnection listener started")
        async for conn_path in self._signal_settings.new_connection:
            if not self._running:
                return
            logger.debug("Settings: new connection %s", conn_path)
            self._saved_cache_dirty = True
            self._track_task(
                self._asyncio_loop.create_task(
                    self._async_load_saved_networks(),
                    name="saved_on_new_connection",
                )
            )

    async def _listen_settings_connection_removed(self) -> None:
        """React to saved connection profiles being deleted."""
        if not self._signal_settings:
            return
        logger.debug("Settings ConnectionRemoved listener started")
        async for conn_path in self._signal_settings.connection_removed:
            if not self._running:
                return
            logger.debug("Settings: connection removed %s", conn_path)
            self._saved_cache_dirty = True
            self._track_task(
                self._asyncio_loop.create_task(
                    self._async_load_saved_networks(),
                    name="saved_on_connection_removed",
                )
            )

    def _schedule_debounced_state_rebuild(self) -> None:
        """Schedule a state rebuild after a short debounce window.

        Multiple rapid D-Bus signals (e.g. during a roam or reconnect)
        coalesce into a single ``_build_current_state`` call, saving
        ~12-15 D-Bus round-trips per coalesced burst.
        """
        if self._state_debounce_handle:
            self._state_debounce_handle.cancel()
        self._state_debounce_handle = self._asyncio_loop.call_later(
            _DEBOUNCE_DELAY, self._fire_state_rebuild
        )

    def _fire_state_rebuild(self) -> None:
        """Debounce callback — spawns the actual async state rebuild."""
        self._state_debounce_handle = None
        if self._running:
            self._track_task(
                self._asyncio_loop.create_task(
                    self._async_get_current_state(),
                    name="debounced_state_rebuild",
                )
            )

    def _schedule_debounced_scan(self) -> None:
        """Schedule a scan-results rebuild after a debounce window.

        AP Added/Removed signals can fire in rapid bursts when
        entering/leaving a dense area.  Coalescing prevents NxN AP
        property reads.
        """
        if self._scan_debounce_handle:
            self._scan_debounce_handle.cancel()
        self._scan_debounce_handle = self._asyncio_loop.call_later(
            _DEBOUNCE_DELAY, self._fire_scan_rebuild
        )

    def _fire_scan_rebuild(self) -> None:
        """Debounce callback — spawns the async scan rebuild."""
        self._scan_debounce_handle = None
        if self._running:
            self._track_task(
                self._asyncio_loop.create_task(
                    self._async_scan_networks(),
                    name="debounced_scan_rebuild",
                )
            )

    async def _async_fallback_poll(self) -> None:
        """Lightweight fallback for missed signals.

        Called at a long interval (default 60 s) by the manager.
        Rebuilds state, connectivity, and saved networks.
        """
        if not self._running:
            return
        await self._async_get_current_state()
        await self._async_check_connectivity()
        await self._async_load_saved_networks()

    async def _ensure_dbus_connection(self) -> bool:
        """Verify the D-Bus connection is healthy, reconnecting if needed.

        Performs a lightweight ``version`` property read as a health check.
        Consecutive failures increment ``_consecutive_dbus_errors``; once the
        threshold is reached, opens a new system bus, re-detects interfaces,
        rebuilds signal proxies, and restarts all listener tasks.  Returns
        ``True`` if the bus is usable (either always-healthy or successfully
        reconnected), ``False`` otherwise.
        """
        if not self._running:
            return False
        try:
            _ = await self._nm().version
            self._consecutive_dbus_errors = 0
            return True
        except Exception as exc:
            self._consecutive_dbus_errors += 1
            logger.warning(
                "D-Bus health check failed (%d/%d): %s",
                self._consecutive_dbus_errors,
                self._MAX_DBUS_ERRORS_BEFORE_RECONNECT,
                exc,
            )
            if self._consecutive_dbus_errors < self._MAX_DBUS_ERRORS_BEFORE_RECONNECT:
                return False
            logger.warning("Attempting D-Bus reconnection...")
            try:
                self._system_bus = sdbus.sd_bus_open_system()
                sdbus.set_default_bus(self._system_bus)
                self._primary_wifi_path = ""
                self._primary_wifi_iface = ""
                self._primary_wired_path = ""
                self._primary_wired_iface = ""
                self._iface_to_device_path.clear()
                await self._detect_interfaces()
                # Rebuild signal proxies on new bus
                self._signal_nm = None
                self._signal_wifi = None
                self._signal_wired = None
                self._signal_settings = None
                self._ensure_signal_proxies()
                # Cancel stale listener tasks bound to old proxies
                # and restart them on the new bus connection.
                for task in self._listener_tasks:
                    if not task.done():
                        task.cancel()
                self._listener_tasks.clear()
                await self._start_signal_listeners()
                self._consecutive_dbus_errors = 0
                logger.info("D-Bus reconnection succeeded")
                if self._primary_wifi_path or self._primary_wired_path:
                    self.error_occurred.emit(
                        "device_reconnected", "Network device reconnected"
                    )
                return True
            except Exception as re_err:
                logger.error("D-Bus reconnection failed: %s", re_err)
                return False

    async def _is_ethernet_connected(self) -> bool:
        """Return True if the primary wired device is fully activated (state 100)."""
        if not self._primary_wired_path:
            return False
        try:
            return await self._generic(self._primary_wired_path).state == 100
        except Exception as exc:
            logger.debug("Error checking ethernet state: %s", exc)
            return False

    async def _has_ethernet_carrier(self) -> bool:
        """Return True if the primary wired device has a physical link (state >= 30).

        State 30 is DISCONNECTED in NM's device state enum, which still implies
        a cable is present.  This is a weaker check than ``_is_ethernet_connected``
        and is used to populate ``NetworkState.ethernet_carrier`` for UI feedback.
        """
        if not self._primary_wired_path:
            return False
        try:
            return await self._generic(self._primary_wired_path).state >= 30
        except Exception:
            # D-Bus read failed; carrier state unknown — treat as no carrier.
            return False

    async def _wait_for_wifi_radio(self, desired: bool, timeout: float = 3.0) -> bool:
        """Poll NM wireless_enabled until it matches *desired* or *timeout* expires."""
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        _logged = False
        while loop.time() < deadline:
            try:
                if await self._nm().wireless_enabled == desired:
                    return True
            except Exception as exc:
                if not _logged:
                    logger.debug("Polling wireless_enabled failed: %s", exc)
                    _logged = True
            await asyncio.sleep(0.25)
        return False

    async def _wait_for_wifi_device_ready(self, timeout: float = 8.0) -> bool:
        """Poll wlan0 device state until it reaches DISCONNECTED (30) or above."""
        if not self._primary_wifi_path:
            return False
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        _logged = False
        while loop.time() < deadline:
            try:
                if await self._generic(self._primary_wifi_path).state >= 30:
                    return True
            except Exception as exc:
                if not _logged:
                    logger.debug("Polling Wi-Fi device state failed: %s", exc)
                    _logged = True
            await asyncio.sleep(0.25)
        return False

    async def _async_get_current_state(self) -> None:
        """Rebuild and emit the full NetworkState, enforcing runtime mutual exclusion."""
        try:
            if not await self._ensure_dbus_connection():
                self.state_changed.emit(NetworkState())
                return
            state = await self._build_current_state()
            if (
                state.ethernet_connected
                and state.wifi_enabled
                and not state.hotspot_enabled
                and not self._is_hotspot_active
            ):
                logger.info(
                    "Runtime mutual exclusion: ethernet active + "
                    "Wi-Fi — disabling Wi-Fi"
                )
                if self._primary_wifi_path:
                    try:
                        await self._wifi().disconnect()
                    except Exception as exc:
                        logger.debug("Disconnect before Wi-Fi disable ignored: %s", exc)
                await self._nm().wireless_enabled.set_async(False)
                await asyncio.sleep(0.5)
                state = await self._build_current_state()
            self.state_changed.emit(state)
        except Exception as exc:
            logger.error("Failed to get current state: %s", exc)
            self.error_occurred.emit("get_current_state", str(exc))

    @staticmethod
    def _get_ip_os_fallback(iface: str) -> str:
        """Return the IPv4 address for *iface* via a raw ioctl SIOCGIFADDR call.

        Used as a fallback when the NM D-Bus IPv4Config path returns nothing —
        common immediately after DHCP on slower hardware.
        """
        if not iface:
            return ""
        _SIOCGIFADDR = 0x8915
        try:
            with _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM) as sock:
                ifreq = struct.pack("256s", iface[:15].encode())
                result = fcntl.ioctl(sock.fileno(), _SIOCGIFADDR, ifreq)
                return _socket.inet_ntoa(result[20:24])
        except Exception:
            # ioctl fails when the interface has no address; caller treats "" as unknown.
            return ""

    async def _build_current_state(self) -> NetworkState:
        """Read all relevant NM properties and assemble a NetworkState snapshot."""
        if not self._system_bus:
            return NetworkState()
        try:
            connectivity_value = await self._nm().check_connectivity()
            connectivity = self._map_connectivity(connectivity_value)
            wifi_enabled = bool(await self._nm().wireless_enabled)
            current_ssid = await self._get_current_ssid()

            eth_connected = await self._is_ethernet_connected()
            if eth_connected:
                current_ip = await self._get_ip_by_interface(
                    self._primary_wired_iface or "eth0"
                )
                if not current_ip:
                    current_ip = self._get_ip_os_fallback(
                        self._primary_wired_iface or "eth0"
                    )
                current_ssid = ""
            elif current_ssid:
                current_ip = await self._get_ip_by_interface("wlan0")
                if not current_ip:
                    current_ip = await self._get_current_ip()
            else:
                current_ip = ""

            if not current_ip and connectivity in (
                ConnectivityState.FULL,
                ConnectivityState.LIMITED,
            ):
                for _iface in (
                    self._primary_wired_iface or "eth0",
                    "wlan0",
                ):
                    _fallback = self._get_ip_os_fallback(_iface)
                    if _fallback:
                        current_ip = _fallback
                        if _iface != "wlan0":
                            eth_connected = True
                        logger.debug("OS fallback IP for '%s': %s", _iface, _fallback)
                        break

            signal = 0
            sec_type = ""
            if current_ssid:
                signal_map = await self._build_signal_map()
                signal = signal_map.get(current_ssid.lower(), 0)
                saved = await self._get_saved_network_cached(current_ssid)
                sec_type = saved.security_type if saved else ""

            hotspot_enabled = current_ssid == self._hotspot_config.ssid

            if not hotspot_enabled and self._is_hotspot_active and not current_ssid:
                hotspot_enabled = True
                current_ssid = self._hotspot_config.ssid
                logger.debug(
                    "Hotspot SSID not found via D-Bus, using config: '%s'",
                    current_ssid,
                )

            if hotspot_enabled:
                sec_type = self._hotspot_config.security
                if not current_ip:
                    current_ip = await self._get_ip_by_interface("wlan0")

            return NetworkState(
                connectivity=connectivity,
                current_ssid=current_ssid,
                current_ip=current_ip,
                wifi_enabled=wifi_enabled,
                hotspot_enabled=hotspot_enabled,
                signal_strength=signal,
                security_type=sec_type,
                ethernet_connected=eth_connected,
                ethernet_carrier=await self._has_ethernet_carrier(),
                active_vlans=await self._get_active_vlans(),
            )
        except Exception as exc:
            logger.error("Error building current state: %s", exc)
            return NetworkState()

    @staticmethod
    def _map_connectivity(value: int) -> ConnectivityState:
        """Map a raw NM connectivity integer to a ConnectivityState enum member."""
        try:
            return ConnectivityState(value)
        except ValueError:
            return ConnectivityState.UNKNOWN

    async def _async_check_connectivity(self) -> None:
        """Query NM connectivity and emit connectivity_changed."""
        try:
            if not self._system_bus:
                self.connectivity_changed.emit(ConnectivityState.UNKNOWN)
                return
            self.connectivity_changed.emit(
                self._map_connectivity(await self._nm().check_connectivity())
            )
        except Exception as exc:
            logger.error("Failed to check connectivity: %s", exc)
            self.connectivity_changed.emit(ConnectivityState.UNKNOWN)

    async def _get_current_ssid(self) -> str:
        """Return the SSID of the currently active Wi-Fi connection, or empty string."""
        try:
            primary_con = await self._nm().primary_connection
            if primary_con and primary_con != "/":
                ssid = await self._ssid_from_active_connection(primary_con)
                if ssid:
                    return ssid
            return await self._get_ssid_from_any_active()
        except Exception as exc:
            logger.debug("Error getting current SSID: %s", exc)
            return ""

    async def _ssid_from_active_connection(self, active_path: str) -> str:
        """Extract the Wi-Fi SSID from an active connection object path, or return ''."""
        try:
            conn_path = await self._active_conn(active_path).connection
            if not conn_path or conn_path == "/":
                return ""
            settings = await self._conn_settings(conn_path).get_settings()
            if "802-11-wireless" in settings:
                ssid = settings["802-11-wireless"]["ssid"][1].decode()
                return ssid
        except Exception as exc:
            logger.debug(
                "Error reading active connection %s: %s",
                active_path,
                exc,
            )
        return ""

    async def _get_ssid_from_any_active(self) -> str:
        """Scan all active NM connections and return the first Wi-Fi SSID found."""
        try:
            active_paths = await self._nm().active_connections
            for active_path in active_paths:
                ssid = await self._ssid_from_active_connection(active_path)
                if ssid:
                    return ssid
        except Exception as exc:
            logger.debug("Error scanning active connections: %s", exc)
        return ""

    async def _get_current_ip(self) -> str:
        """Return the IPv4 address from the primary NM connection's IP4Config."""
        try:
            primary_con = await self._nm().primary_connection
            if primary_con == "/":
                return ""
            ip4_path = await self._active_conn(primary_con).ip4_config
            if ip4_path == "/":
                return ""
            addr_data = await self._ipv4(ip4_path).address_data
            if addr_data:
                return addr_data[0]["address"][1]
            return ""
        except Exception as exc:
            logger.debug("Error getting current IP: %s", exc)
            return ""

    async def _get_ip_by_interface(self, interface: str = "wlan0") -> str:
        """Return the IPv4 address assigned to *interface* via NM's IP4Config D-Bus object."""
        try:
            device_path = self._iface_to_device_path.get(interface)
            if not device_path:
                devices = await self._nm().get_devices()
                for dp in devices:
                    if await self._generic(dp).interface == interface:
                        device_path = dp
                        self._iface_to_device_path[interface] = dp
                        break
            if not device_path:
                return ""
            ip4_path = await self._generic(device_path).ip4_config
            if not ip4_path or ip4_path == "/":
                return ""
            addr_data = await self._ipv4(ip4_path).address_data
            if addr_data:
                return addr_data[0]["address"][1]
            return ""
        except Exception as exc:
            logger.error("Failed to get IP for %s: %s", interface, exc)
            return ""

    async def _async_scan_networks(self) -> None:
        """Request an NM rescan, parse visible APs, and emit networks_scanned."""
        try:
            if not self._primary_wifi_path:
                self.networks_scanned.emit([])
                return
            if not await self._ensure_dbus_connection():
                self.networks_scanned.emit([])
                return

            if not await self._nm().wireless_enabled:
                self.networks_scanned.emit([])
                return

            try:
                await self._wifi().request_scan({})
            except Exception as exc:
                logger.debug(
                    "Scan request ignored (already scanning or radio off): %s", exc
                )

            if await self._wifi().last_scan == -1:
                self.networks_scanned.emit([])
                return

            ap_paths = await self._wifi().get_all_access_points()
            current_ssid = await self._get_current_ssid()
            saved_ssids = set(await self._get_saved_ssid_names_cached())

            networks: list[NetworkInfo] = []
            seen_ssids: set[str] = set()

            for ap_path in ap_paths:
                try:
                    info = await self._parse_ap(ap_path, current_ssid, saved_ssids)
                    if (
                        info
                        and info.ssid not in seen_ssids
                        and not is_hidden_ssid(info.ssid)
                        and (info.signal_strength > 0 or info.is_active)
                    ):
                        networks.append(info)
                        seen_ssids.add(info.ssid)
                except Exception as exc:
                    logger.debug("Failed to parse AP %s: %s", ap_path, exc)

            networks.sort(key=lambda n: (-n.network_status, -n.signal_strength))
            self.networks_scanned.emit(networks)

        except Exception as exc:
            logger.error("Failed to scan networks: %s", exc)
            self.error_occurred.emit("scan_networks", str(exc))
            self.networks_scanned.emit([])

    async def _get_all_ap_properties(self, ap_path: str) -> dict[str, object]:
        """Fetch all D-Bus properties for an AccessPoint in one round-trip."""
        try:
            return await self._ap(ap_path).properties_get_all_dict(
                on_unknown_member="ignore"
            )
        except Exception as exc:
            logger.debug("GetAll failed for AP %s: %s", ap_path, exc)
            return {}

    async def _build_signal_map(self) -> dict[str, int]:
        """Return a mapping of lowercase SSID to best-seen signal strength (0-100)."""
        signal_map: dict[str, int] = {}
        if not self._primary_wifi_path:
            return signal_map
        try:
            ap_paths = await self._wifi().access_points
            for ap_path in ap_paths:
                try:
                    props = await self._get_all_ap_properties(ap_path)
                    ssid = self._decode_ssid(props.get("ssid", b""))
                    if ssid:
                        strength = int(props.get("strength", 0))
                        key = ssid.lower()
                        if strength > signal_map.get(key, 0):
                            signal_map[key] = strength
                except Exception as exc:
                    logger.debug("Skipping AP in signal map: %s", exc)
                    continue
        except Exception as exc:
            logger.debug("Error building signal map: %s", exc)
        return signal_map

    async def _parse_ap(
        self, ap_path: str, current_ssid: str, saved_ssids: set
    ) -> NetworkInfo | None:
        """Parse an AccessPoint D-Bus object into a NetworkInfo, or None if unusable."""
        props = await self._get_all_ap_properties(ap_path)
        if not props:
            return None

        ssid = self._decode_ssid(props.get("ssid", b""))
        if not ssid or is_hidden_ssid(ssid):
            return None

        flags = int(props.get("flags", 0))
        wpa_flags = int(props.get("wpa_flags", 0))
        rsn_flags = int(props.get("rsn_flags", 0))
        is_open = (flags & 1) == 0

        security = self._determine_security_type(flags, wpa_flags, rsn_flags)
        if not is_connectable_security(security):
            return None

        is_active = ssid == current_ssid
        is_saved = ssid in saved_ssids
        if is_active:
            net_status = NetworkStatus.ACTIVE
        elif is_saved:
            net_status = NetworkStatus.SAVED
        elif is_open:
            net_status = NetworkStatus.OPEN
        else:
            net_status = NetworkStatus.DISCOVERED

        return NetworkInfo(
            ssid=ssid,
            signal_strength=int(props.get("strength", 0)),
            network_status=net_status,
            bssid=str(props.get("hw_address", "")),
            frequency=int(props.get("frequency", 0)),
            max_bitrate=int(props.get("max_bitrate", 0)),
            security_type=security,
        )

    @staticmethod
    def _decode_ssid(raw: object) -> str:
        """Decode a raw SSID byte string to a UTF-8 str, replacing invalid bytes."""
        if isinstance(raw, bytes):
            return raw.decode("utf-8", errors="replace")
        return str(raw) if raw else ""

    @staticmethod
    def _determine_security_type(
        flags: int, wpa_flags: int, rsn_flags: int
    ) -> SecurityType:
        """Determine the Wi-Fi SecurityType from AP capability flags."""
        if (flags & 1) == 0:
            return SecurityType.OPEN
        if rsn_flags:
            if rsn_flags & 0x400:
                return SecurityType.WPA3_SAE
            if rsn_flags & 0x200:
                return SecurityType.WPA_EAP
            return SecurityType.WPA2_PSK
        if wpa_flags:
            if wpa_flags & 0x200:
                return SecurityType.WPA_EAP
            return SecurityType.WPA_PSK
        return SecurityType.WEP

    def _invalidate_saved_cache(self) -> None:
        """Mark the saved-networks cache as dirty so it is rebuilt on next access."""
        self._saved_cache_dirty = True

    async def _get_saved_ssid_names_cached(self) -> list[str]:
        """Return SSID names for all saved Wi-Fi profiles, refreshing cache if dirty."""
        if self._saved_cache_dirty:
            self._saved_cache = await self._get_saved_networks_impl()
            self._saved_cache_dirty = False
        return [n.ssid for n in self._saved_cache]

    async def _get_saved_network_cached(self, ssid: str) -> SavedNetwork | None:
        """Return the SavedNetwork for *ssid* from cache (case-insensitive), or None."""
        if self._saved_cache_dirty:
            self._saved_cache = await self._get_saved_networks_impl()
            self._saved_cache_dirty = False
        ssid_lower = ssid.lower()
        for n in self._saved_cache:
            if n.ssid.lower() == ssid_lower:
                return n
        return None

    async def _async_load_saved_networks(self) -> None:
        """Reload all saved Wi-Fi profiles and emit saved_networks_loaded."""
        try:
            networks = await self._get_saved_networks_impl()
            self._saved_cache = networks
            self._saved_cache_dirty = False
            self.saved_networks_loaded.emit(networks)
        except Exception as exc:
            logger.error("Failed to load saved networks: %s", exc)
            self.error_occurred.emit("load_saved_networks", str(exc))
            self.saved_networks_loaded.emit([])

    async def _get_saved_networks_impl(self) -> list[SavedNetwork]:
        """Enumerate NM connection profiles and return infrastructure Wi-Fi ones."""
        if not self._system_bus:
            return []
        try:
            connections = await self._nm_settings().list_connections()
            signal_map = await self._build_signal_map()
            saved: list[SavedNetwork] = []

            for conn_path in connections:
                try:
                    settings = await self._conn_settings(conn_path).get_settings()
                    if settings["connection"]["type"][1] != "802-11-wireless":
                        continue

                    wireless = settings["802-11-wireless"]
                    ssid = wireless["ssid"][1].decode()
                    uuid = settings["connection"]["uuid"][1]
                    mode = str(wireless.get("mode", (None, "infrastructure"))[1])

                    security_key = str(wireless.get("security", (None, ""))[1])
                    sec_type = ""
                    if security_key and security_key in settings:
                        sec_type = settings[security_key].get("key-mgmt", (None, ""))[1]

                    priority = settings["connection"].get(
                        "autoconnect-priority",
                        (None, ConnectionPriority.MEDIUM.value),
                    )[1]
                    timestamp = settings["connection"].get("timestamp", (None, 0))[1]
                    signal = signal_map.get(ssid.lower(), 0)
                    ipv4_method = settings.get("ipv4", {}).get(
                        "method", (None, "auto")
                    )[1]
                    is_dhcp = ipv4_method != "manual"

                    saved.append(
                        SavedNetwork(
                            ssid=ssid,
                            uuid=uuid,
                            connection_path=conn_path,
                            security_type=sec_type,
                            mode=mode,
                            priority=priority or ConnectionPriority.MEDIUM.value,
                            signal_strength=signal,
                            timestamp=int(timestamp or 0),
                            is_dhcp=is_dhcp,
                        )
                    )
                except Exception as exc:
                    logger.debug("Failed to parse connection: %s", exc)

            return saved
        except Exception as exc:
            logger.error("Error getting saved networks: %s", exc)
            return []

    async def _is_known(self, ssid: str) -> bool:
        """Return True if a saved profile for *ssid* exists in the cache."""
        return await self._get_saved_network_cached(ssid) is not None

    async def _get_connection_path(self, ssid: str) -> str | None:
        """Return the D-Bus connection path for a saved *ssid* profile, or None."""
        saved = await self._get_saved_network_cached(ssid)
        return saved.connection_path if saved else None

    async def _async_add_network(self, ssid: str, password: str, priority: int) -> None:
        """Add and activate a new Wi-Fi profile, emitting connection_result when done."""
        try:
            result = await self._add_network_impl(ssid, password, priority)
            self._invalidate_saved_cache()
            self.connection_result.emit(result)
        except Exception as exc:
            logger.error("Failed to add network: %s", exc)
            self.connection_result.emit(
                ConnectionResult(
                    success=False,
                    message=str(exc),
                    error_code="add_failed",
                )
            )

    async def _add_network_impl(
        self, ssid: str, password: str, priority: int
    ) -> ConnectionResult:
        """Scan for the SSID, build a connection profile, add it to NM, and activate it.

        Deletes any pre-existing profile for the same SSID before adding.
        Returns a failed ConnectionResult if the SSID is not visible, the
        security type is unsupported, or the 20-second activation wait times out.
        """
        if not self._primary_wifi_path or not self._system_bus:
            return ConnectionResult(False, "No Wi-Fi interface", "no_interface")

        if await self._is_known(ssid):
            await self._delete_network_impl(ssid)
            self._invalidate_saved_cache()

        try:
            await self._wifi().request_scan({})
        except Exception as exc:
            logger.debug("Pre-connect scan request ignored: %s", exc)

        ap_paths = await self._wifi().get_all_access_points()
        target_ap_path: str | None = None
        target_ap_props: dict[str, object] = {}
        for ap_path in ap_paths:
            props = await self._get_all_ap_properties(ap_path)
            if self._decode_ssid(props.get("ssid", b"")) == ssid:
                target_ap_path = ap_path
                target_ap_props = props
                break

        if not target_ap_path:
            return ConnectionResult(False, f"Network '{ssid}' not found", "not_found")

        interface = await self._wifi().interface
        conn_props = self._build_connection_properties(
            ssid, password, interface, priority, target_ap_props
        )
        if not conn_props:
            return ConnectionResult(
                False,
                "Unsupported security type",
                "unsupported_security",
            )

        try:
            nm_settings = self._nm_settings()
            conn_path = await nm_settings.add_connection(conn_props)
        except Exception as exc:
            err_str = str(exc).lower()
            if "psk" in err_str and ("invalid" in err_str or "property" in err_str):
                return ConnectionResult(
                    False,
                    "Wrong password, try again.",
                    "invalid_password",
                )
            return ConnectionResult(False, str(exc), "add_failed")

        if _CAN_RELOAD_CONNECTIONS:
            try:
                await self._nm_settings().reload_connections()
            except Exception as reload_err:
                logger.debug("reload_connections non-fatal: %s", reload_err)

        try:
            await self._nm().activate_connection(conn_path)
            if not await self._wait_for_connection(ssid, timeout=_WIFI_CONNECT_TIMEOUT):
                await self._delete_network_impl(ssid)
                self._invalidate_saved_cache()
                return ConnectionResult(
                    False,
                    f"Authentication failed for '{ssid}'.\n"
                    "The saved profile has been removed.\n"
                    "Please check the password and try again.",
                    "auth_failed",
                )
            return ConnectionResult(True, f"Network '{ssid}' added and connecting")
        except Exception as act_err:
            logger.warning("Activate after add failed: %s", act_err)
            return ConnectionResult(True, f"Network '{ssid}' added (activate manually)")

    def _build_connection_properties(
        self,
        ssid: str,
        password: str,
        interface: str,
        priority: int,
        ap_props: dict[str, object],
    ) -> dict[str, object] | None:
        """Build NM connection property dict for *ssid* from its AP capability flags.

        Returns None if the security type is unsupported (e.g. WPA-EAP).
        Handles OPEN, WPA-PSK, WPA2-PSK, and WPA3-SAE (including SAE-transition).
        """
        flags = int(ap_props.get("flags", 0))
        wpa_flags = int(ap_props.get("wpa_flags", 0))
        rsn_flags = int(ap_props.get("rsn_flags", 0))

        props: dict[str, object] = {
            "connection": {
                "id": ("s", ssid),
                "uuid": ("s", str(uuid4())),
                "type": ("s", "802-11-wireless"),
                "interface-name": ("s", interface),
                "autoconnect": ("b", True),
                "autoconnect-priority": ("i", priority),
            },
            "802-11-wireless": {
                "mode": ("s", "infrastructure"),
                "ssid": ("ay", ssid.encode("utf-8")),
            },
            "ipv4": {
                "method": ("s", "auto"),
                "route-metric": ("i", 200),
            },
            "ipv6": {"method": ("s", "auto")},
        }

        if (flags & 1) == 0:
            return props

        props["802-11-wireless"]["security"] = (
            "s",
            "802-11-wireless-security",
        )
        security = self._determine_security_type(flags, wpa_flags, rsn_flags)

        if not is_connectable_security(security):
            logger.warning(
                "Rejecting connection to '%s': unsupported security %s",
                ssid,
                security.value,
            )
            return None

        if security == SecurityType.WPA3_SAE:
            has_psk = bool((rsn_flags & 0x100) or wpa_flags)
            if has_psk:
                logger.debug(
                    "SAE transition for '%s' — using wpa-psk + PMF optional",
                    ssid,
                )
                props["802-11-wireless-security"] = {
                    "key-mgmt": ("s", "wpa-psk"),
                    "auth-alg": ("s", "open"),
                    "psk": ("s", password),
                    "pmf": ("u", 2),  # OPTIONAL — required for SAE-transition APs
                }
            else:
                logger.debug("Pure SAE detected for '%s'", ssid)
                props["802-11-wireless-security"] = {
                    "key-mgmt": ("s", "sae"),
                    "auth-alg": ("s", "open"),
                    "psk": ("s", password),
                    "pmf": ("u", 3),  # REQUIRED — mandatory for pure WPA3-SAE
                }
        elif security in (
            SecurityType.WPA2_PSK,
            SecurityType.WPA_PSK,
        ):
            props["802-11-wireless-security"] = {
                "key-mgmt": ("s", "wpa-psk"),
                "auth-alg": ("s", "open"),
                "psk": ("s", password),
            }
        else:
            logger.warning(
                "Unsupported security type '%s' for '%s'",
                security.value,
                ssid,
            )
            return None

        return props

    async def _async_connect_network(self, ssid: str) -> None:
        """Activate an existing saved Wi-Fi profile and emit connection_result."""
        try:
            self._is_hotspot_active = False
            result = await self._connect_network_impl(ssid)
            self.connection_result.emit(result)
            self.state_changed.emit(await self._build_current_state())
        except Exception as exc:
            logger.error("Failed to connect: %s", exc)
            self.connection_result.emit(
                ConnectionResult(
                    success=False,
                    message=str(exc),
                    error_code="connect_failed",
                )
            )

    async def _wait_for_connection(
        self, ssid: str, timeout: float = _WIFI_CONNECT_TIMEOUT
    ) -> bool:
        """Poll until *ssid* is active and has an IP, or until *timeout* expires.

        Starts with a 1.5 s initial delay to let NM begin the association.
        Returns False early if the SSID disappears for 3 consecutive polls.
        """
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        await asyncio.sleep(1.5)
        consecutive_empty = 0
        while loop.time() < deadline:
            try:
                current = await self._get_current_ssid()
                if current and current.lower() == ssid.lower():
                    ip = await self._get_current_ip()
                    if ip:
                        return True
                    consecutive_empty = 0
                else:
                    consecutive_empty += 1
                    if consecutive_empty >= 3:
                        return False
            except Exception as exc:
                logger.debug("Connection wait poll failed: %s", exc)
            await asyncio.sleep(0.5)
        return False

    async def _connect_network_impl(self, ssid: str) -> ConnectionResult:
        """Enable Wi-Fi if needed, locate the saved profile, and activate it."""
        if not self._system_bus:
            return ConnectionResult(False, "NetworkManager unavailable", "no_nm")

        if not await self._nm().wireless_enabled:
            await self._nm().wireless_enabled.set_async(True)
            if not await self._wait_for_wifi_radio(True, timeout=8.0):
                return ConnectionResult(
                    False,
                    "Wi-Fi radio failed to turn on.\nPlease try again.",
                    "radio_failed",
                )
            await self._wait_for_wifi_device_ready(timeout=8.0)

        conn_path = await self._get_connection_path(ssid)
        if not conn_path:
            conn_path = await self._find_connection_path_direct(ssid)
        if not conn_path:
            return ConnectionResult(False, f"Network '{ssid}' not saved", "not_found")

        try:
            await self._nm().activate_connection(conn_path)
            if not await self._wait_for_connection(ssid, timeout=_WIFI_CONNECT_TIMEOUT):
                return ConnectionResult(
                    False,
                    f"Could not connect to '{ssid}'.\n"
                    "Please check signal strength and try again.",
                    "connect_timeout",
                )
            return ConnectionResult(True, f"Connected to '{ssid}'")
        except Exception as exc:
            return ConnectionResult(False, str(exc), "connect_failed")

    async def _find_connection_path_direct(self, ssid: str) -> str | None:
        """Search NM settings for an infrastructure profile matching *ssid* directly."""
        try:
            connections = await self._nm_settings().list_connections()
            for conn_path in connections:
                try:
                    settings = await self._conn_settings(conn_path).get_settings()
                    if settings["connection"]["type"][1] != "802-11-wireless":
                        continue
                    conn_ssid = settings["802-11-wireless"]["ssid"][1].decode()
                    if conn_ssid.lower() == ssid.lower():
                        self._invalidate_saved_cache()
                        return conn_path
                except Exception as exc:
                    logger.debug("Skipping connection in path lookup: %s", exc)
                    continue
        except Exception as exc:
            logger.debug("Direct connection path lookup failed: %s", exc)
        return None

    async def _async_disconnect(self) -> None:
        """Disconnect the primary Wi-Fi device and emit connection_result."""
        try:
            if self._primary_wifi_path:
                await self._wifi().disconnect()
            self.connection_result.emit(ConnectionResult(True, "Disconnected"))
        except Exception as exc:
            logger.error("Disconnect failed: %s", exc)
            self.connection_result.emit(
                ConnectionResult(
                    success=False,
                    message=str(exc),
                    error_code="disconnect_failed",
                )
            )

    async def _async_delete_network(self, ssid: str) -> None:
        """Delete the saved profile for *ssid* and emit connection_result."""
        try:
            result = await self._delete_network_impl(ssid)
            self._invalidate_saved_cache()
            self.connection_result.emit(result)
            if result.success:
                self.state_changed.emit(await self._build_current_state())
        except Exception as exc:
            logger.error("Delete failed: %s", exc)
            self.connection_result.emit(
                ConnectionResult(
                    success=False,
                    message=str(exc),
                    error_code="delete_failed",
                )
            )

    async def _delete_network_impl(self, ssid: str) -> ConnectionResult:
        """Delete the NM connection profile for *ssid* and disconnect if it is active."""
        conn_path = await self._get_connection_path(ssid)
        if not conn_path:
            return ConnectionResult(False, f"Network '{ssid}' not found", "not_found")
        try:
            await self._conn_settings(conn_path).delete()

            if _CAN_RELOAD_CONNECTIONS:
                try:
                    await self._nm_settings().reload_connections()
                except Exception as reload_err:
                    logger.debug("reload_connections non-fatal: %s", reload_err)

            current_ssid = await self._get_current_ssid()
            if current_ssid and current_ssid.lower() == ssid.lower():
                if self._primary_wifi_path:
                    try:
                        await self._wifi().disconnect()
                    except Exception as exc:
                        logger.debug("Disconnect after network delete ignored: %s", exc)

            return ConnectionResult(True, f"Network '{ssid}' deleted")
        except Exception as exc:
            return ConnectionResult(False, str(exc), "delete_failed")

    async def _async_update_network(
        self,
        ssid: str,
        password: str = "",
        priority: int = 0,
    ) -> None:
        """Update password and/or priority for a saved profile and emit connection_result."""
        try:
            result = await self._update_network_impl(
                ssid,
                password or None,
                priority if priority != 0 else None,
            )
            self._invalidate_saved_cache()
            self.connection_result.emit(result)
        except Exception as exc:
            logger.error("Update failed: %s", exc)
            self.connection_result.emit(
                ConnectionResult(
                    success=False,
                    message=str(exc),
                    error_code="update_failed",
                )
            )

    async def _update_network_impl(
        self,
        ssid: str,
        password: str | None,
        priority: int | None,
    ) -> ConnectionResult:
        """Merge updated password/priority into the existing NM connection settings."""
        conn_path = await self._get_connection_path(ssid)
        if not conn_path:
            return ConnectionResult(False, f"Network '{ssid}' not found", "not_found")
        try:
            cs = self._conn_settings(conn_path)
            props = await cs.get_settings()
            await self._merge_wifi_secrets(cs, props)

            if password and "802-11-wireless-security" in props:
                props["802-11-wireless-security"]["psk"] = (
                    "s",
                    password,
                )

            if priority is not None:
                props["connection"]["autoconnect-priority"] = (
                    "i",
                    priority,
                )
                logger.debug("Setting priority for '%s' to %d", ssid, priority)

            await cs.update(props)
            logger.debug("Network '%s' update() succeeded", ssid)
            return ConnectionResult(True, f"Network '{ssid}' updated")
        except Exception as exc:
            logger.error("Update failed for '%s': %s", ssid, exc)
            err_str = str(exc).lower()
            if "psk" in err_str and ("invalid" in err_str or "property" in err_str):
                return ConnectionResult(
                    False,
                    "Wrong password, try again.",
                    "invalid_password",
                )
            return ConnectionResult(False, str(exc), "update_failed")

    async def _async_set_wifi_enabled(self, enabled: bool) -> None:
        """Enable or disable the Wi-Fi radio, handling ethernet mutual exclusion."""
        try:
            if not self._system_bus:
                return
            if not enabled:
                self._is_hotspot_active = False

            if enabled and await self._is_ethernet_connected():
                await self._async_disconnect_ethernet()

            current = await self._nm().wireless_enabled
            if current != enabled:
                if not enabled:
                    if self._primary_wifi_path:
                        try:
                            await self._wifi().disconnect()
                        except Exception as exc:
                            logger.debug(
                                "Disconnect before Wi-Fi toggle ignored: %s", exc
                            )
                        await asyncio.sleep(0.5)

                await self._nm().wireless_enabled.set_async(enabled)

                if not await self._wait_for_wifi_radio(enabled, timeout=8.0):
                    logger.warning(
                        "Wi-Fi radio did not reach %s within 8 s",
                        "enabled" if enabled else "disabled",
                    )

            self.connection_result.emit(
                ConnectionResult(
                    True,
                    f"Wi-Fi {'enabled' if enabled else 'disabled'}",
                )
            )
            self.state_changed.emit(await self._build_current_state())
        except Exception as exc:
            logger.error("Failed to toggle Wi-Fi: %s", exc)
            self.error_occurred.emit("set_wifi_enabled", str(exc))

    async def _async_disconnect_ethernet(self) -> None:
        """Deactivate all VLANs, disconnect ethernet, and wait up to 4 s for teardown."""
        if not self._primary_wired_path:
            return
        try:
            await self._deactivate_all_vlans()
            await self._wired().disconnect()
            loop = asyncio.get_running_loop()
            deadline = loop.time() + 4.0
            while loop.time() < deadline:
                await asyncio.sleep(0.5)
                if not await self._is_ethernet_connected():
                    break
            logger.info("Ethernet disconnected")
        except Exception as exc:
            logger.error("Failed to disconnect ethernet: %s", exc)

    async def _async_connect_ethernet(self) -> None:
        """Disable Wi-Fi/hotspot, activate the wired device, and restore saved VLANs."""
        if not self._primary_wired_path:
            self.error_occurred.emit("connect_ethernet", "No wired device found")
            return
        try:
            if self._is_hotspot_active:
                await self._async_toggle_hotspot(False)

            if self._primary_wifi_path:
                try:
                    await self._wifi().disconnect()
                except Exception as exc:
                    logger.debug("Pre-VLAN disconnect ignored: %s", exc)
                await asyncio.sleep(0.5)

            if await self._nm().wireless_enabled:
                await self._nm().wireless_enabled.set_async(False)
                await self._wait_for_wifi_radio(False, timeout=8.0)

            await self._nm().activate_connection("/", self._primary_wired_path, "/")
            await asyncio.sleep(1.5)

            await self._activate_saved_vlans()
            logger.info("Ethernet connection activated")
            self.connection_result.emit(ConnectionResult(True, "Ethernet connected"))
            self.state_changed.emit(await self._build_current_state())
        except Exception as exc:
            logger.error("Failed to connect ethernet: %s", exc)
            self.error_occurred.emit("connect_ethernet", str(exc))
            self.state_changed.emit(await self._build_current_state())

    async def _async_create_vlan(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str,
        dns2: str,
    ) -> None:
        """Create and activate a VLAN connection with a static IP on the primary wired interface.

        Emits connection_result and state_changed when done.
        """
        if not self._primary_wired_path:
            self.error_occurred.emit("create_vlan", "No wired device")
            return
        try:
            if self._is_hotspot_active:
                await self._async_toggle_hotspot(False)

            if self._primary_wifi_path:
                try:
                    await self._wifi().disconnect()
                except Exception as exc:
                    logger.debug("Pre-VLAN disconnect ignored: %s", exc)
                await asyncio.sleep(0.5)

            if await self._nm().wireless_enabled:
                await self._nm().wireless_enabled.set_async(False)
                await self._wait_for_wifi_radio(False, timeout=8.0)

            if not await self._is_ethernet_connected():
                await self._nm().activate_connection("/", self._primary_wired_path, "/")
                await asyncio.sleep(1.5)

            iface = self._primary_wired_iface or "eth0"

            try:
                existing_conns = await self._nm_settings().list_connections()
                for existing_path in existing_conns:
                    try:
                        s = await self._conn_settings(existing_path).get_settings()
                        if (
                            s.get("connection", {}).get("type", (None, ""))[1] == "vlan"
                            and s.get("vlan", {}).get("id", (None, -1))[1] == vlan_id
                            and s.get("vlan", {}).get("parent", (None, ""))[1] == iface
                        ):
                            self.connection_result.emit(
                                ConnectionResult(
                                    False,
                                    f"VLAN {vlan_id} already exists on "
                                    f"{iface}.\nRemove it first before "
                                    "creating a new one.",
                                    "duplicate_vlan",
                                )
                            )
                            return
                    except Exception as exc:
                        logger.debug(
                            "Skipping connection in duplicate VLAN check: %s", exc
                        )
                        continue
            except Exception as dup_err:
                logger.debug(
                    "Duplicate VLAN check failed (non-fatal): %s",
                    dup_err,
                )

            vlan_conn_id = f"VLAN {vlan_id}"

            if await self._deactivate_connection_by_id(vlan_conn_id):
                await asyncio.sleep(1.0)

            await self._delete_all_connections_by_id(vlan_conn_id)
            await asyncio.sleep(0.5)

            prefix = self._mask_to_prefix(subnet_mask)
            ip_uint = self._ip_to_nm_uint32(ip_address)
            gw_uint = self._ip_to_nm_uint32(gateway) if gateway else 0
            dns_list: list[int] = []
            if dns1:
                dns_list.append(self._ip_to_nm_uint32(dns1))
            if dns2:
                dns_list.append(self._ip_to_nm_uint32(dns2))

            conn_props: dict[str, object] = {
                "connection": {
                    "id": ("s", vlan_conn_id),
                    "uuid": ("s", str(uuid4())),
                    "type": ("s", "vlan"),
                    "autoconnect": ("b", False),
                },
                "vlan": {
                    "id": ("u", vlan_id),
                    "parent": ("s", iface),
                },
                "ipv4": {
                    "method": ("s", "manual"),
                    "addresses": (
                        "aau",
                        [[ip_uint, prefix, gw_uint]],
                    ),
                    "gateway": ("s", gateway or ""),
                    "dns": ("au", dns_list),
                    "route-metric": ("i", 500),
                },
                "ipv6": {"method": ("s", "ignore")},
            }

            conn_path = await self._nm_settings().add_connection(conn_props)
            await self._nm().activate_connection(conn_path, "/", "/")
            self.state_changed.emit(await self._build_current_state())
            await asyncio.sleep(1.5)

            self.connection_result.emit(
                ConnectionResult(True, f"VLAN {vlan_id} connected")
            )
            self.state_changed.emit(await self._build_current_state())
        except Exception as exc:
            logger.error("Failed to create VLAN %d: %s", vlan_id, exc)
            self.error_occurred.emit("create_vlan", str(exc))
            self.state_changed.emit(await self._build_current_state())

    async def _async_delete_vlan(self, vlan_id: int) -> None:
        """Delete all NM connection profiles for *vlan_id* and emit connection_result."""
        try:
            deleted = await self._delete_all_connections_by_id(f"VLAN {vlan_id}")
            logger.info(
                "Deleted %d VLAN profile(s) for VLAN %d",
                deleted,
                vlan_id,
            )
            self.connection_result.emit(
                ConnectionResult(True, f"VLAN {vlan_id} removed")
            )
            self.state_changed.emit(await self._build_current_state())
        except Exception as exc:
            logger.error("Failed to delete VLAN %d: %s", vlan_id, exc)
            self.error_occurred.emit("delete_vlan", str(exc))

    async def _get_active_vlans(self) -> tuple[VlanInfo, ...]:
        """Return a tuple of VlanInfo for all currently active VLAN connections."""
        vlans: list[VlanInfo] = []
        try:
            active_paths = await self._nm().active_connections
            for active_path in active_paths:
                try:
                    ac = self._active_conn(active_path)
                    conn_path = await ac.connection
                    settings = await self._conn_settings(conn_path).get_settings()
                    conn_type = settings.get("connection", {}).get("type", (None, ""))[
                        1
                    ]
                    if conn_type != "vlan":
                        continue

                    vlan_id = settings.get("vlan", {}).get("id", (None, 0))[1]
                    iface = settings.get("connection", {}).get(
                        "interface-name", (None, "")
                    )[1]
                    if not iface:
                        parent = settings.get("vlan", {}).get("parent", (None, "eth0"))[
                            1
                        ]
                        iface = f"{parent}.{vlan_id}"

                    ipv4_method = settings.get("ipv4", {}).get(
                        "method", (None, "auto")
                    )[1]
                    is_dhcp = ipv4_method != "manual"

                    dns_data = settings.get("ipv4", {}).get("dns-data", (None, []))[1]
                    dns_servers: tuple[str, ...] = ()
                    if dns_data:
                        dns_servers = tuple(str(d) for d in dns_data)
                    else:
                        dns_raw = settings.get("ipv4", {}).get("dns", (None, []))[1]
                        if dns_raw:
                            dns_servers = tuple(
                                self._nm_uint32_to_ip(d) for d in dns_raw
                            )

                    ip_addr = ""
                    gateway = ""
                    try:
                        ip4_path = await self._active_conn(active_path).ip4_config
                        if ip4_path and ip4_path != "/":
                            ip4_cfg = self._ipv4(ip4_path)
                            addr_data = await ip4_cfg.address_data
                            if addr_data:
                                ip_addr = str(addr_data[0]["address"][1])
                            gw = await ip4_cfg.gateway
                            if gw:
                                gateway = str(gw)
                    except Exception as exc:
                        logger.debug(
                            "D-Bus IP read for VLAN failed, falling back to OS: %s", exc
                        )
                        if iface:
                            ip_addr = await self._get_ip_by_interface(iface)

                    if not ip_addr and iface:
                        ip_addr = self._get_ip_os_fallback(iface)

                    vlans.append(
                        VlanInfo(
                            vlan_id=int(vlan_id),
                            ip_address=ip_addr,
                            interface=iface,
                            gateway=gateway,
                            dns_servers=dns_servers,
                            is_dhcp=is_dhcp,
                        )
                    )
                except Exception as exc:
                    logger.debug("Skipping connection in active VLAN list: %s", exc)
                    continue
        except Exception as exc:
            logger.debug("Error getting active VLANs: %s", exc)
        return tuple(vlans)

    async def _deactivate_all_vlans(self) -> None:
        """Deactivate all active VLAN connections via the NM D-Bus interface."""
        try:
            active_paths = list(await self._nm().active_connections)
            for active_path in active_paths:
                try:
                    conn_path = await self._active_conn(active_path).connection
                    settings = await self._conn_settings(conn_path).get_settings()
                    conn_type = settings.get("connection", {}).get("type", (None, ""))[
                        1
                    ]
                    if conn_type != "vlan":
                        continue
                    conn_id = settings.get("connection", {}).get("id", (None, ""))[1]
                    await self._nm().deactivate_connection(active_path)
                    logger.debug("Deactivated VLAN '%s'", conn_id)
                except Exception as exc:
                    logger.debug("Skipping VLAN during deactivation: %s", exc)
                    continue
            await asyncio.sleep(0.5)
        except Exception as exc:
            logger.debug("Error deactivating VLANs: %s", exc)

    async def _activate_saved_vlans(self) -> None:
        """Activate all saved VLAN connection profiles found in NM settings."""
        try:
            nm_settings = self._nm_settings()
            connections = await nm_settings.connections
            for conn_path in connections:
                try:
                    settings = await self._conn_settings(conn_path).get_settings()
                    conn_type = settings.get("connection", {}).get("type", (None, ""))[
                        1
                    ]
                    if conn_type != "vlan":
                        continue
                    conn_id = settings.get("connection", {}).get("id", (None, ""))[1]
                    await self._nm().activate_connection(conn_path, "/", "/")
                    logger.debug("Activated saved VLAN '%s'", conn_id)
                    await asyncio.sleep(1.0)
                except Exception as exc:
                    logger.debug("Failed to activate VLAN: %s", exc)
        except Exception as exc:
            logger.debug("Error activating saved VLANs: %s", exc)

    async def _reconnect_wifi_profile(self, ssid: str) -> None:
        """Disconnect, then re-activate the saved Wi-Fi profile for *ssid*.

        Waits up to 10 s for an IP address before returning.  Used after
        updating a connection's static IP or DHCP settings so the new
        configuration is applied immediately.
        """
        logger.debug(
            "Reconnecting Wi-Fi profile '%s' to apply new settings",
            ssid,
        )
        if self._primary_wifi_path:
            try:
                await self._wifi().disconnect()
            except Exception as disc_err:
                logger.debug("Disconnect before reconnect: %s", disc_err)
            await asyncio.sleep(1.5)

        fresh_path = await self._get_connection_path(ssid)
        if not fresh_path:
            fresh_path = await self._find_connection_path_direct(ssid)
        if not fresh_path:
            logger.warning(
                "Reconnect skipped: could not find saved profile for '%s'",
                ssid,
            )
            return

        try:
            await self._nm().activate_connection(fresh_path)
        except Exception as act_err:
            logger.warning(
                "Reconnect activate failed for '%s': %s",
                ssid,
                act_err,
            )
            return

        loop = asyncio.get_running_loop()
        deadline = loop.time() + 10.0
        while loop.time() < deadline:
            await asyncio.sleep(1.0)
            found_ip: str = ""
            try:
                current = await self._get_current_ssid()
                if current and current.lower() == ssid.lower():
                    found_ip = await self._get_current_ip() or ""
                    if not found_ip:
                        found_ip = self._get_ip_os_fallback("wlan0") or ""
            except Exception as exc:
                logger.debug(
                    "IP address lookup during connection wait ignored: %s", exc
                )

            if found_ip:
                logger.info(
                    "Reconnect complete for '%s': IP=%s",
                    ssid,
                    found_ip,
                )
                try:
                    self._invalidate_saved_cache()
                    self.saved_networks_loaded.emit(
                        await self._get_saved_networks_impl()
                    )
                except Exception as cache_err:
                    logger.debug(
                        "Cache refresh after reconnect failed: %s",
                        cache_err,
                    )
                return

        logger.warning("Reconnect for '%s': IP not assigned within 10 s", ssid)

    async def _async_update_wifi_static_ip(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str,
        dns2: str,
    ) -> None:
        """Apply a static IPv4 configuration to a saved Wi-Fi profile and reconnect."""
        conn_path = await self._get_connection_path(ssid)
        if not conn_path:
            self.error_occurred.emit("wifi_static_ip", f"'{ssid}' not found")
            return
        try:
            cs = self._conn_settings(conn_path)
            props = await cs.get_settings()
            await self._merge_wifi_secrets(cs, props)

            prefix = self._mask_to_prefix(subnet_mask)
            ip_uint = self._ip_to_nm_uint32(ip_address)
            gw_uint = self._ip_to_nm_uint32(gateway) if gateway else 0
            dns_list: list[int] = []
            if dns1:
                dns_list.append(self._ip_to_nm_uint32(dns1))
            if dns2:
                dns_list.append(self._ip_to_nm_uint32(dns2))

            props["ipv4"] = {
                "method": ("s", "manual"),
                "addresses": (
                    "aau",
                    [[ip_uint, prefix, gw_uint]],
                ),
                "gateway": ("s", gateway or ""),
                "dns": ("au", dns_list),
            }
            props["ipv6"] = {"method": ("s", "disabled")}
            await cs.update(props)
            self._invalidate_saved_cache()
            logger.info(
                "Static IP set for '%s': %s/%d gw %s (IPv6 disabled)",
                ssid,
                ip_address,
                prefix,
                gateway,
            )

            await self._reconnect_wifi_profile(ssid)

            self.connection_result.emit(
                ConnectionResult(True, f"Static IP set for '{ssid}'")
            )
            self.state_changed.emit(await self._build_current_state())
            self.reconnect_complete.emit()
        except Exception as exc:
            logger.error("Failed to set static IP for '%s': %s", ssid, exc)
            self.error_occurred.emit("wifi_static_ip", str(exc))

    async def _async_reset_wifi_to_dhcp(self, ssid: str) -> None:
        """Reset a saved Wi-Fi profile's IPv4 settings to DHCP and reconnect."""
        conn_path = await self._get_connection_path(ssid)
        if not conn_path:
            self.error_occurred.emit("wifi_dhcp", f"'{ssid}' not found")
            return
        try:
            cs = self._conn_settings(conn_path)
            props = await cs.get_settings()
            await self._merge_wifi_secrets(cs, props)
            props["ipv4"] = {"method": ("s", "auto")}
            await cs.update(props)
            self._invalidate_saved_cache()
            logger.info("Reset '%s' to DHCP", ssid)

            await self._reconnect_wifi_profile(ssid)

            self.connection_result.emit(ConnectionResult(True, f"'{ssid}' set to DHCP"))
            self.state_changed.emit(await self._build_current_state())
            self.reconnect_complete.emit()
        except Exception as exc:
            logger.error("Failed to reset '%s' to DHCP: %s", ssid, exc)
            self.error_occurred.emit("wifi_dhcp", str(exc))

    def _load_hotspot_config(self) -> None:
        """Populate _hotspot_config from the config file.

        Writes defaults if missing.
        """
        try:
            cfg = get_configparser()
            if not cfg.has_section("hotspot"):
                cfg.add_section("hotspot")

            hotspot = cfg.get_section("hotspot")

            if hotspot.has_option("ssid"):
                self._hotspot_config.ssid = hotspot.get("ssid", str, "PrinterHotspot")
            else:
                cfg.add_option("hotspot", "ssid", "PrinterHotspot")

            if hotspot.has_option("password"):
                self._hotspot_config.password = hotspot.get(
                    "password", str, "123456789"
                )
            else:
                cfg.add_option("hotspot", "password", "123456789")

            cfg.save_configuration()
        except Exception as exc:
            logger.warning("Could not load hotspot config, using defaults: %s", exc)

    def _save_hotspot_config(self) -> None:
        """Persist current _hotspot_config ssid/password to the config file."""
        try:
            cfg = get_configparser()
            cfg.update_option("hotspot", "ssid", self._hotspot_config.ssid)
            cfg.update_option("hotspot", "password", self._hotspot_config.password)
            cfg.save_configuration()
        except Exception as exc:
            logger.warning("Could not save hotspot config: %s", exc)

    async def _async_create_and_activate_hotspot(
        self,
        ssid: str,
        password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Create a new WPA2-PSK AP-mode profile and activate it as a hotspot.

        Removes all stale AP-mode and same-name profiles before adding the new
        one.  Disconnects ethernet if active so the Wi-Fi radio is available.
        """
        try:
            config_ssid = ssid or "PrinterHotspot"
            config_pwd = password or "123456789"
            config_sec = (
                security
                if HotspotSecurity.is_valid(security)
                else HotspotSecurity.WPA2_PSK.value
            )
            self._hotspot_config.ssid = config_ssid
            self._hotspot_config.password = config_pwd
            self._hotspot_config.security = config_sec
            self._save_hotspot_config()

            if not await self._nm().wireless_enabled:
                await self._nm().wireless_enabled.set_async(True)
                await self._wait_for_wifi_radio(True, timeout=8.0)

            if not await self._wait_for_wifi_device_ready(timeout=8.0):
                logger.warning(
                    "wlan0 did not reach DISCONNECTED within 8 s; "
                    "proceeding with hotspot activation anyway"
                )

            ethernet_was_active = await self._is_ethernet_connected()
            if ethernet_was_active:
                try:
                    await self._async_disconnect_ethernet()
                except Exception as exc:
                    logger.debug("Pre-hotspot ethernet disconnect ignored: %s", exc)
                # Brief pause to let eth0 finish deactivating before NM
                # processes the hotspot activation request.
                await asyncio.sleep(1.0)
            if self._primary_wifi_path:
                try:
                    await self._wifi().disconnect()
                except Exception as exc:
                    logger.debug("Pre-hotspot Wi-Fi disconnect ignored: %s", exc)

            await self._delete_all_ap_mode_connections()
            # Also delete by connection id in case a non-AP profile shares the
            # hotspot name (e.g. a leftover infrastructure profile named the
            # same as the SSID). _delete_all_ap_mode_connections already caught
            # all AP-mode profiles, so this second list_connections call is a
            # narrow safety net.
            await self._delete_connections_by_id(config_ssid)

            conn_props: dict[str, object] = {
                "connection": {
                    "id": ("s", config_ssid),
                    "uuid": ("s", str(uuid4())),
                    "type": ("s", "802-11-wireless"),
                    "interface-name": ("s", self._get_wifi_iface_name()),
                    "autoconnect": ("b", False),
                },
                "802-11-wireless": {
                    "ssid": ("ay", config_ssid.encode("utf-8")),
                    "mode": ("s", "ap"),
                    "band": ("s", self._hotspot_config.band),
                    "channel": (
                        "u",
                        self._hotspot_config.channel,
                    ),
                    "security": (
                        "s",
                        "802-11-wireless-security",
                    ),
                },
                "ipv4": {"method": ("s", "shared")},
                "ipv6": {"method": ("s", "ignore")},
            }

            conn_props["802-11-wireless-security"] = {
                "key-mgmt": ("s", "wpa-psk"),
                "psk": ("s", config_pwd),
                "pmf": ("u", 0),
            }
            # AP mode is always WPA2-PSK; WPA3-SAE in AP mode requires driver
            # support not guaranteed on the target hardware.
            config_sec = HotspotSecurity.WPA2_PSK.value
            self._hotspot_config.security = config_sec

            conn_path = await self._nm_settings().add_connection(conn_props)
            logger.debug(
                "Hotspot profile created at %s (security=%s)",
                conn_path,
                config_sec,
            )

            await self._nm().activate_connection(
                conn_path, self._primary_wifi_path, "/"
            )
            self._is_hotspot_active = True
            self._invalidate_saved_cache()

            self.hotspot_info_ready.emit(config_ssid, config_pwd, config_sec)
            self.connection_result.emit(
                ConnectionResult(True, f"Hotspot '{config_ssid}' activated")
            )

            await asyncio.sleep(1.5)
            self.state_changed.emit(await self._build_current_state())

        except Exception as exc:
            logger.error("Hotspot create+activate failed: %s", exc)
            self._is_hotspot_active = False
            self.connection_result.emit(
                ConnectionResult(False, str(exc), "hotspot_failed")
            )

    async def _async_update_hotspot_config(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Update hotspot SSID/password and re-activate if the hotspot was running."""
        try:
            was_active = self._is_hotspot_active

            if was_active and self._primary_wifi_path:
                try:
                    await self._wifi().disconnect()
                except Exception as exc:
                    logger.debug("Pre-hotspot-update disconnect ignored: %s", exc)
                self._is_hotspot_active = False

            await self._delete_all_ap_mode_connections()
            deleted_old = await self._delete_connections_by_id(old_ssid)
            logger.debug(
                "Cleaned up %d old hotspot profiles for '%s'",
                deleted_old,
                old_ssid,
            )

            if new_ssid.lower() != old_ssid.lower():
                await self._delete_connections_by_id(new_ssid)

            validated_sec = (
                security
                if HotspotSecurity.is_valid(security)
                else HotspotSecurity.WPA2_PSK.value
            )
            self._hotspot_config.ssid = new_ssid
            self._hotspot_config.password = new_password
            self._hotspot_config.security = validated_sec
            self._save_hotspot_config()

            self.hotspot_info_ready.emit(
                new_ssid,
                new_password,
                self._hotspot_config.security,
            )

            if was_active:
                await self._async_create_and_activate_hotspot(
                    new_ssid,
                    new_password,
                    self._hotspot_config.security,
                )
            else:
                self.connection_result.emit(
                    ConnectionResult(
                        True,
                        f"Hotspot config updated to '{new_ssid}'",
                    )
                )
        except Exception as exc:
            logger.error("Hotspot config update failed: %s", exc)
            self.connection_result.emit(
                ConnectionResult(False, str(exc), "hotspot_config_failed")
            )

    async def _async_toggle_hotspot(self, enable: bool) -> None:
        """Enable or disable the hotspot, cleaning up profiles and Wi-Fi radio state."""
        try:
            if enable:
                await self._async_create_and_activate_hotspot(
                    self._hotspot_config.ssid,
                    self._hotspot_config.password,
                )
                return

            was_hotspot_active = self._is_hotspot_active
            self._is_hotspot_active = False
            if self._primary_wifi_path:
                try:
                    await self._wifi().disconnect()
                except Exception as exc:
                    logger.debug("Hotspot-off disconnect ignored: %s", exc)

            deleted = await self._delete_connections_by_id(self._hotspot_config.ssid)
            logger.debug("Hotspot OFF: cleaned up %d profile(s)", deleted)

            if was_hotspot_active and await self._nm().wireless_enabled:
                await self._nm().wireless_enabled.set_async(False)

            self.connection_result.emit(ConnectionResult(True, "Hotspot disabled"))
            self.state_changed.emit(await self._build_current_state())
        except Exception as exc:
            logger.error("Failed to toggle hotspot: %s", exc)
            self._is_hotspot_active = False
            self.connection_result.emit(
                ConnectionResult(
                    success=False,
                    message=str(exc),
                    error_code="hotspot_toggle_failed",
                )
            )

    async def _merge_wifi_secrets(
        self,
        conn_settings: dbus_nm.NetworkConnectionSettings,
        props: dict,
    ) -> None:
        """Fetch Wi-Fi secrets from NM and merge them into *props* in place.

        Required before calling update() so that the PSK is re-included;
        NM redacts secrets from get_settings() responses.
        """
        try:
            secrets = await conn_settings.get_secrets("802-11-wireless-security")
            sec_key = "802-11-wireless-security"
            if sec_key in secrets:
                props.setdefault(sec_key, {}).update(secrets[sec_key])
        except Exception as exc:
            logger.debug("Could not fetch Wi-Fi secrets (NM may redact): %s", exc)

    async def _deactivate_connection_by_id(self, conn_id: str) -> bool:
        """Deactivate the first active connection whose profile id matches *conn_id*."""
        try:
            active_paths = await self._nm().active_connections
            for active_path in active_paths:
                try:
                    conn_path = await self._active_conn(active_path).connection
                    settings = await self._conn_settings(conn_path).get_settings()
                    cid = settings.get("connection", {}).get("id", (None, ""))[1]
                    if cid == conn_id:
                        await self._nm().deactivate_connection(active_path)
                        logger.debug(
                            "Deactivated active connection '%s'",
                            conn_id,
                        )
                        return True
                except Exception as exc:
                    logger.debug(
                        "Skipping connection during deactivation lookup: %s", exc
                    )
        except Exception as exc:
            logger.debug("Error deactivating '%s': %s", conn_id, exc)
        return False

    async def _delete_all_connections_by_id(self, conn_id: str) -> int:
        """Delete every NM connection profile whose id exactly matches *conn_id*."""
        deleted = 0
        try:
            connections = await self._nm_settings().list_connections()
            for conn_path in connections:
                try:
                    cs = self._conn_settings(conn_path)
                    settings = await cs.get_settings()
                    cid = settings.get("connection", {}).get("id", (None, ""))[1]
                    if cid == conn_id:
                        await cs.delete()
                        deleted += 1
                except Exception as exc:
                    logger.debug(
                        "Skipping connection in cleanup for '%s': %s", conn_id, exc
                    )
        except Exception as exc:
            logger.error("Cleanup for '%s' failed: %s", conn_id, exc)
        return deleted

    async def _delete_all_ap_mode_connections(self) -> int:
        """Delete all saved Wi-Fi connections in AP mode.

        Called before creating a new hotspot to remove stale profiles from
        previous hotspot sessions, regardless of their SSID.  Without this,
        old AP-mode profiles accumulate in NetworkManager and NM may
        auto-activate them on the next boot.
        """
        deleted = 0
        try:
            connections = await self._nm_settings().list_connections()
            for conn_path in connections:
                try:
                    cs = self._conn_settings(conn_path)
                    settings = await cs.get_settings()
                    conn_type = settings.get("connection", {}).get("type", (None, ""))[
                        1
                    ]
                    if conn_type != "802-11-wireless":
                        continue
                    mode = settings.get("802-11-wireless", {}).get("mode", (None, ""))[
                        1
                    ]
                    if mode == "ap":
                        conn_id = settings.get("connection", {}).get("id", (None, ""))[
                            1
                        ]
                        await cs.delete()
                        deleted += 1
                        logger.debug(
                            "Removed stale AP profile '%s' at %s", conn_id, conn_path
                        )
                except Exception as exc:
                    logger.debug("Skipping connection in AP profile cleanup: %s", exc)
        except Exception as exc:
            logger.error("Failed to remove stale AP profiles: %s", exc)
        if deleted:
            self._invalidate_saved_cache()
        return deleted

    async def _delete_connections_by_id(self, ssid: str) -> int:
        """Delete every NM connection profile whose id matches *ssid* (case-insensitive)."""
        deleted = 0
        try:
            connections = await self._nm_settings().list_connections()
            for conn_path in connections:
                try:
                    cs = self._conn_settings(conn_path)
                    settings = await cs.get_settings()
                    conn_id = settings.get("connection", {}).get("id", (None, ""))[1]
                    if conn_id.lower() == ssid.lower():
                        await cs.delete()
                        deleted += 1
                        logger.debug(
                            "Deleted stale profile '%s' at %s",
                            conn_id,
                            conn_path,
                        )
                except Exception as exc:
                    logger.debug(
                        "Skip connection %s during cleanup: %s",
                        conn_path,
                        exc,
                    )
        except Exception as exc:
            logger.error(
                "Failed to enumerate connections for cleanup: %s",
                exc,
            )
        if deleted:
            self._invalidate_saved_cache()
        return deleted

    @staticmethod
    def _ip_to_nm_uint32(ip_str: str) -> int:
        """Convert a dotted-decimal IPv4 string to a native-endian uint32 for NM."""
        return struct.unpack("=I", ipaddress.IPv4Address(ip_str).packed)[0]

    @staticmethod
    def _nm_uint32_to_ip(uint_ip: int) -> str:
        """Convert a native-endian uint32 from NM back to a dotted-decimal IPv4 string."""
        return str(ipaddress.IPv4Address(struct.pack("=I", uint_ip)))

    @staticmethod
    def _mask_to_prefix(mask_str: str) -> int:
        """Convert a subnet mask or CIDR prefix string to an integer prefix length."""
        stripped = mask_str.strip()
        if stripped.isdigit():
            prefix = int(stripped)
            if 0 <= prefix <= 32:
                return prefix
            raise ValueError(f"CIDR prefix out of range: {prefix}")
        return bin(int(ipaddress.IPv4Address(stripped))).count("1")
