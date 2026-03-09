"""Unit tests for BlocksScreen.lib.network.worker.NetworkManagerWorker.

All D-Bus modules are mocked via conftest.py — these tests run
without NetworkManager or a system bus.

Architecture: Tests target the sdbus_async worker API.
Async coroutines are tested directly via ``pytest-asyncio`` — NO daemon
thread, NO ``_run_sync``, NO ``run_coroutine_threadsafe``.

The ``_make_worker`` helper bypasses ``__init__`` so the asyncio daemon
thread is never started; each ``@pytest.mark.asyncio`` test drives the
coroutine on the test's own event loop.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest
from PyQt6.QtCore import QObject

from BlocksScreen.lib.network import worker as _worker_mod
from BlocksScreen.lib.network.models import (ConnectionPriority,
                                             ConnectionResult,
                                             ConnectivityState, HotspotConfig,
                                             NetworkInfo, NetworkState,
                                             NetworkStatus, SavedNetwork,
                                             SecurityType)
from BlocksScreen.lib.network.worker import NetworkManagerWorker
# Import conftest helpers
from tests.network.conftest import AsyncProxyMock, _ProxyFactory, _run


def _make_worker(qapp, *, running=True, with_wifi=True, with_wired=False):
    """Create a NetworkManagerWorker WITHOUT starting the asyncio thread.

    Bypasses ``__init__`` entirely so no ``threading.Thread`` is created
    and no D-Bus connection is opened.  Sets up a minimal internal state
    suitable for testing individual async methods with ``pytest-asyncio``.
    """
    with patch.object(
        NetworkManagerWorker, "__init__", lambda self: QObject.__init__(self)
    ):
        w = NetworkManagerWorker()

    # Core state — mirrors real __init__
    w._running = running
    w._system_bus = MagicMock(name="mock_system_bus")
    w._primary_wifi_path = (
        "/org/freedesktop/NetworkManager/Devices/2" if with_wifi else ""
    )
    w._primary_wifi_iface = "wlan0" if with_wifi else ""
    w._primary_wired_path = (
        "/org/freedesktop/NetworkManager/Devices/1" if with_wired else ""
    )
    w._primary_wired_iface = "eth0" if with_wired else ""
    w._iface_to_device_path = {}
    w._hotspot_config = HotspotConfig()
    w._saved_cache = []
    w._saved_cache_dirty = False
    w._is_hotspot_active = False
    w._consecutive_dbus_errors = 0
    w._background_tasks = set()


    # Signal-reactive architecture: persistent signal proxies
    w._signal_nm = None
    w._signal_wifi = None
    w._signal_wired = None
    w._signal_settings = None
    w._state_debounce_handle = None
    w._scan_debounce_handle = None
    w._listener_tasks = []

    # Stubs for thread-related attrs (never used in async tests)
    w._asyncio_loop = MagicMock()
    w._asyncio_thread = MagicMock()

    return w


def _bare_worker(qapp):
    """Minimal worker for signal / property tests — no mock state."""
    with patch.object(
        NetworkManagerWorker, "__init__", lambda self: QObject.__init__(self)
    ):
        w = NetworkManagerWorker()
    w._running = False
    w._system_bus = None
    w._primary_wifi_path = ""
    w._primary_wifi_iface = ""
    w._primary_wired_path = ""
    w._primary_wired_iface = ""
    w._iface_to_device_path = {}
    w._hotspot_config = HotspotConfig()
    w._saved_cache = []
    w._saved_cache_dirty = True
    w._is_hotspot_active = False
    w._consecutive_dbus_errors = 0
    w._background_tasks = set()

    w._signal_nm = None
    w._signal_wifi = None
    w._signal_wired = None
    w._signal_settings = None
    w._state_debounce_handle = None
    w._scan_debounce_handle = None
    w._listener_tasks = []
    w._asyncio_loop = MagicMock()
    w._asyncio_thread = MagicMock()
    return w


def _make(qapp, *, running=True, wifi=True, wired=True):
    with patch.object(
        NetworkManagerWorker, "__init__", lambda self: QObject.__init__(self)
    ):
        w = NetworkManagerWorker()
    w._running = running
    w._system_bus = MagicMock(name="mock_bus")
    w._primary_wifi_path = "/org/freedesktop/NetworkManager/Devices/2" if wifi else ""
    w._primary_wifi_iface = "wlan0" if wifi else ""
    w._primary_wired_path = "/org/freedesktop/NetworkManager/Devices/1" if wired else ""
    w._primary_wired_iface = "eth0" if wired else ""
    w._iface_to_device_path = {}
    w._hotspot_config = HotspotConfig()
    w._saved_cache = []
    w._saved_cache_dirty = False
    w._is_hotspot_active = False
    w._consecutive_dbus_errors = 0
    w._background_tasks = set()

    w._signal_nm = None
    w._signal_wifi = None
    w._signal_wired = None
    w._signal_settings = None
    w._state_debounce_handle = None
    w._scan_debounce_handle = None
    w._listener_tasks = []
    w._asyncio_loop = MagicMock()
    w._asyncio_thread = MagicMock()
    return w


def _wire(w, *, nm=None, wifi_proxy=None, wired_proxy=None, settings=None):
    """Wire mock D-Bus proxy factories onto worker."""
    if nm is not None:
        w._nm = _ProxyFactory(nm)
    if wifi_proxy is not None:
        w._wifi = _ProxyFactory(wifi_proxy)
    if wired_proxy is not None:
        w._wired = _ProxyFactory(wired_proxy)
        w._generic = MagicMock(return_value=wired_proxy)
    if settings is not None:
        w._nm_settings = _ProxyFactory(settings)
    return w



class TestWorkerCreation:
    def test_initial_state(self, qapp):
        w = _bare_worker(qapp)
        assert w._running is False
        assert w._system_bus is None
        assert w._primary_wifi_path == ""
        assert w._primary_wired_path == ""
        assert w._saved_cache == []
        assert w._saved_cache_dirty is True
        assert w._is_hotspot_active is False

    def test_all_signals_defined(self, qapp):
        w = _bare_worker(qapp)
        for name in (
            "state_changed",
            "networks_scanned",
            "saved_networks_loaded",
            "connection_result",
            "connectivity_changed",
            "error_occurred",
            "hotspot_info_ready",
            "reconnect_complete",
            "initialized",
        ):
            assert hasattr(w, name), f"Missing signal: {name}"

    def test_default_hotspot_config(self, qapp):
        w = _bare_worker(qapp)
        assert w._hotspot_config.ssid == "PrinterHotspot"
        assert w._hotspot_config.password == "123456789"
        assert w._hotspot_config.channel == 6
        assert w._hotspot_config.band == "bg"

    def test_proxy_factories_exist(self, qapp):
        w = _bare_worker(qapp)
        for name in (
            "_nm",
            "_wifi",
            "_wired",
            "_generic",
            "_active_conn",
            "_conn_settings",
            "_nm_settings",
            "_ap",
            "_ipv4",
        ):
            assert callable(getattr(w, name, None)), f"Missing factory: {name}"



class TestHotspotProperties:
    def test_hotspot_ssid(self, qapp):
        w = _bare_worker(qapp)
        assert w.hotspot_ssid == "PrinterHotspot"

    def test_hotspot_password(self, qapp):
        w = _bare_worker(qapp)
        assert w.hotspot_password == "123456789"



class TestAsyncInitialize:
    @pytest.mark.asyncio
    async def test_no_bus_emits_error(self, qapp):
        w = _bare_worker(qapp)
        w._system_bus = None
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append((op, msg)))
        await w._async_initialize()
        assert w._running is False
        assert len(errors) == 1
        assert errors[0][0] == "initialize"

    @pytest.mark.asyncio
    async def test_happy_path_sets_running(self, qapp):
        w = _make_worker(qapp, running=False)
        # Mock all async calls in initialize
        w._detect_interfaces = AsyncMock()
        w._enforce_boot_mutual_exclusion = AsyncMock()
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._activate_saved_vlans = AsyncMock()
        w._start_signal_listeners = AsyncMock()

        # Mock wifi proxy for request_scan call during init
        wifi_proxy = AsyncProxyMock(request_scan=AsyncMock())
        w._wifi = _ProxyFactory(wifi_proxy)

        hotspot_info = []
        w.hotspot_info_ready.connect(lambda s, p, sec: hotspot_info.append((s, p, sec)))
        initialized = []
        w.initialized.connect(lambda: initialized.append(True))

        await w._async_initialize()
        assert w._running is True
        assert len(hotspot_info) == 1
        assert hotspot_info[0] == ("PrinterHotspot", "123456789", "wpa-psk")
        assert len(initialized) == 1



class TestDetectInterfaces:
    @pytest.mark.asyncio
    async def test_exception_is_handled(self, qapp):
        w = _make_worker(qapp, with_wifi=False)
        nm_proxy = AsyncProxyMock(
            get_devices=AsyncMock(side_effect=Exception("D-Bus error"))
        )
        w._nm = _ProxyFactory(nm_proxy)
        await w._detect_interfaces()
        assert w._primary_wifi_path == ""

    @pytest.mark.asyncio
    async def test_detect_wifi_device(self, qapp):
        w = _make_worker(qapp, with_wifi=False)
        nm_proxy = AsyncProxyMock(get_devices=AsyncMock(return_value=["/dev/wifi0"]))
        w._nm = _ProxyFactory(nm_proxy)

        generic_proxy = AsyncProxyMock(
            device_type=2,
            interface="wlan0",
        )
        w._generic = lambda path: generic_proxy

        with patch.object(_worker_mod, "dbus_nm") as mock_dbus:
            mock_dbus.enums.DeviceType.WIFI = 2
            mock_dbus.enums.DeviceType.ETHERNET = 1
            await w._detect_interfaces()

        assert w._primary_wifi_path == "/dev/wifi0"
        assert w._iface_to_device_path["wlan0"] == "/dev/wifi0"

    @pytest.mark.asyncio
    async def test_detect_wired_device(self, qapp):
        w = _make_worker(qapp, with_wifi=False)
        nm_proxy = AsyncProxyMock(get_devices=AsyncMock(return_value=["/dev/eth0"]))
        w._nm = _ProxyFactory(nm_proxy)

        generic_proxy = AsyncProxyMock(
            device_type=1,
            interface="eth0",
        )
        w._generic = lambda path: generic_proxy

        with patch.object(_worker_mod, "dbus_nm") as mock_dbus:
            mock_dbus.enums.DeviceType.WIFI = 2
            mock_dbus.enums.DeviceType.ETHERNET = 1
            await w._detect_interfaces()

        assert w._primary_wired_path == "/dev/eth0"
        assert w._primary_wired_iface == "eth0"



class TestDecodeSSID:
    def test_bytes_input(self):
        assert NetworkManagerWorker._decode_ssid(b"TestNetwork") == "TestNetwork"

    def test_bytes_utf8_with_special_chars(self):
        assert NetworkManagerWorker._decode_ssid("Café".encode()) == "Café"

    def test_bytes_with_invalid_utf8(self):
        result = NetworkManagerWorker._decode_ssid(b"\xff\xfe")
        assert "�" in result or "\\x" in result

    def test_string_input(self):
        assert NetworkManagerWorker._decode_ssid("AlreadyStr") == "AlreadyStr"

    def test_none_input(self):
        assert NetworkManagerWorker._decode_ssid(None) == ""

    def test_empty_bytes(self):
        assert NetworkManagerWorker._decode_ssid(b"") == ""

    def test_empty_string(self):
        assert NetworkManagerWorker._decode_ssid("") == ""

    def test_integer_input(self):
        assert NetworkManagerWorker._decode_ssid(12345) == "12345"



class TestGetAllApProperties:
    @pytest.mark.asyncio
    async def test_success(self, qapp):
        w = _make_worker(qapp)
        ap_proxy = AsyncProxyMock(
            properties_get_all_dict=AsyncMock(
                return_value={"ssid": b"Test", "strength": 75}
            )
        )
        w._ap = lambda path: ap_proxy
        result = await w._get_all_ap_properties("/ap/1")
        assert result["ssid"] == b"Test"
        assert result["strength"] == 75

    @pytest.mark.asyncio
    async def test_exception_returns_empty_dict(self, qapp):
        w = _make_worker(qapp)
        ap_proxy = AsyncProxyMock(
            properties_get_all_dict=AsyncMock(side_effect=Exception("AP gone"))
        )
        w._ap = lambda path: ap_proxy
        result = await w._get_all_ap_properties("/ap/bad")
        assert result == {}



class TestIsEthernetConnected:
    @pytest.mark.asyncio
    async def test_no_wired_path_returns_false(self, qapp):
        w = _make_worker(qapp, with_wired=False)
        assert await w._is_ethernet_connected() is False

    @pytest.mark.asyncio
    async def test_state_activated_returns_true(self, qapp):
        w = _make_worker(qapp, with_wired=True)
        generic_proxy = AsyncProxyMock(state=100)
        w._generic = lambda path: generic_proxy
        assert await w._is_ethernet_connected() is True

    @pytest.mark.asyncio
    async def test_state_disconnected_returns_false(self, qapp):
        w = _make_worker(qapp, with_wired=True)
        generic_proxy = AsyncProxyMock(state=30)
        w._generic = lambda path: generic_proxy
        assert await w._is_ethernet_connected() is False

    @pytest.mark.asyncio
    async def test_exception_returns_false(self, qapp):
        w = _make_worker(qapp, with_wired=True)
        w._generic = MagicMock(side_effect=Exception("D-Bus error"))
        assert await w._is_ethernet_connected() is False



class TestHasEthernetCarrier:
    @pytest.mark.asyncio
    async def test_no_wired_path_returns_false(self, qapp):
        w = _make_worker(qapp, with_wired=False)
        assert await w._has_ethernet_carrier() is False

    @pytest.mark.asyncio
    async def test_state_30_returns_true(self, qapp):
        w = _make_worker(qapp, with_wired=True)
        generic_proxy = AsyncProxyMock(state=30)
        w._generic = lambda path: generic_proxy
        assert await w._has_ethernet_carrier() is True

    @pytest.mark.asyncio
    async def test_state_10_returns_false(self, qapp):
        w = _make_worker(qapp, with_wired=True)
        generic_proxy = AsyncProxyMock(state=10)
        w._generic = lambda path: generic_proxy
        assert await w._has_ethernet_carrier() is False



class TestConnectivityMapping:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (0, ConnectivityState.UNKNOWN),
            (1, ConnectivityState.NONE),
            (2, ConnectivityState.PORTAL),
            (3, ConnectivityState.LIMITED),
            (4, ConnectivityState.FULL),
            (99, ConnectivityState.UNKNOWN),
            (-1, ConnectivityState.UNKNOWN),
        ],
    )
    def test_map_connectivity(self, value, expected):
        assert NetworkManagerWorker._map_connectivity(value) == expected



class TestSecurityTypeDetection:
    def test_open_network(self):
        assert (
            NetworkManagerWorker._determine_security_type(0, 0, 0) == SecurityType.OPEN
        )

    def test_wpa2_psk_rsn_cipher_only(self):
        assert (
            NetworkManagerWorker._determine_security_type(1, 0, 0x08)
            == SecurityType.WPA2_PSK
        )

    def test_wpa2_psk_explicit(self):
        assert (
            NetworkManagerWorker._determine_security_type(1, 0, 0x108)
            == SecurityType.WPA2_PSK
        )

    def test_wpa3_sae(self):
        assert (
            NetworkManagerWorker._determine_security_type(1, 0, 0x400)
            == SecurityType.WPA3_SAE
        )

    def test_wpa_eap_via_rsn(self):
        assert (
            NetworkManagerWorker._determine_security_type(1, 0, 0x200)
            == SecurityType.WPA_EAP
        )

    def test_wpa_psk(self):
        assert (
            NetworkManagerWorker._determine_security_type(1, 0x08, 0)
            == SecurityType.WPA_PSK
        )

    def test_wpa_psk_explicit_keymgmt(self):
        assert (
            NetworkManagerWorker._determine_security_type(1, 0x100, 0)
            == SecurityType.WPA_PSK
        )

    def test_wpa_eap_via_wpa(self):
        assert (
            NetworkManagerWorker._determine_security_type(1, 0x200, 0)
            == SecurityType.WPA_EAP
        )

    def test_wep(self):
        assert (
            NetworkManagerWorker._determine_security_type(1, 0, 0) == SecurityType.WEP
        )

    def test_iphone_transition_mode(self):
        result = NetworkManagerWorker._determine_security_type(1, 0x08, 0x508)
        assert result == SecurityType.WPA3_SAE



class TestSignalEmission:
    def test_state_changed_signal(self, qapp):
        w = _bare_worker(qapp)
        received = []
        w.state_changed.connect(lambda s: received.append(s))
        state = NetworkState(connectivity=ConnectivityState.FULL, current_ssid="X")
        w.state_changed.emit(state)
        assert len(received) == 1
        assert received[0].current_ssid == "X"

    def test_networks_scanned_signal(self, qapp):
        w = _bare_worker(qapp)
        received = []
        w.networks_scanned.connect(lambda n: received.append(n))
        networks = [
            NetworkInfo(ssid="A", signal_strength=80),
            NetworkInfo(ssid="B", signal_strength=60),
        ]
        w.networks_scanned.emit(networks)
        assert len(received) == 1
        assert len(received[0]) == 2

    def test_connection_result_signal(self, qapp):
        w = _bare_worker(qapp)
        received = []
        w.connection_result.connect(lambda r: received.append(r))
        w.connection_result.emit(ConnectionResult(success=True, message="OK"))
        assert received[0].success is True

    def test_error_occurred_signal(self, qapp):
        w = _bare_worker(qapp)
        received = []
        w.error_occurred.connect(lambda op, msg: received.append((op, msg)))
        w.error_occurred.emit("test_op", "boom")
        assert received == [("test_op", "boom")]

    def test_connectivity_changed_signal(self, qapp):
        w = _bare_worker(qapp)
        received = []
        w.connectivity_changed.connect(lambda c: received.append(c))
        w.connectivity_changed.emit(ConnectivityState.FULL)
        assert received == [ConnectivityState.FULL]

    def test_hotspot_info_ready_signal_3_args(self, qapp):
        w = _bare_worker(qapp)
        received = []
        w.hotspot_info_ready.connect(lambda s, p, sec: received.append((s, p, sec)))
        w.hotspot_info_ready.emit("MyAP", "pass123", "wpa-psk")
        assert received == [("MyAP", "pass123", "wpa-psk")]

    def test_reconnect_complete_signal(self, qapp):
        w = _bare_worker(qapp)
        received = []
        w.reconnect_complete.connect(lambda: received.append(True))
        w.reconnect_complete.emit()
        assert received == [True]



class TestCheckConnectivity:
    @pytest.mark.asyncio
    async def test_emits_unknown_when_no_bus(self, qapp):
        w = _bare_worker(qapp)
        w._system_bus = None
        received = []
        w.connectivity_changed.connect(lambda c: received.append(c))
        await w._async_check_connectivity()
        assert received == [ConnectivityState.UNKNOWN]

    @pytest.mark.asyncio
    async def test_emits_correct_state(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(check_connectivity=AsyncMock(return_value=3))
        w._nm = _ProxyFactory(nm_proxy)
        received = []
        w.connectivity_changed.connect(lambda c: received.append(c))
        await w._async_check_connectivity()
        assert received == [ConnectivityState.LIMITED]

    @pytest.mark.asyncio
    async def test_emits_unknown_on_error(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(
            check_connectivity=AsyncMock(side_effect=Exception("D-Bus error"))
        )
        w._nm = _ProxyFactory(nm_proxy)
        received = []
        w.connectivity_changed.connect(lambda c: received.append(c))
        await w._async_check_connectivity()
        assert received == [ConnectivityState.UNKNOWN]



class TestGetCurrentSSID:
    @pytest.mark.asyncio
    async def test_primary_connection_returns_ssid(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(primary_connection="/active/1")
        w._nm = _ProxyFactory(nm_proxy)
        w._ssid_from_active_connection = AsyncMock(return_value="MyWiFi")
        assert await w._get_current_ssid() == "MyWiFi"

    @pytest.mark.asyncio
    async def test_primary_slash_falls_back(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(primary_connection="/")
        w._nm = _ProxyFactory(nm_proxy)
        w._get_ssid_from_any_active = AsyncMock(return_value="Fallback")
        assert await w._get_current_ssid() == "Fallback"

    @pytest.mark.asyncio
    async def test_exception_returns_empty(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(
            primary_connection=AsyncMock(side_effect=RuntimeError("crash"))
        )
        # Override primary_connection to raise on await
        w._nm = lambda: nm_proxy
        assert await w._get_current_ssid() == ""



class TestSSIDFromActiveConnection:
    @pytest.mark.asyncio
    async def test_returns_ssid_from_wireless_settings(self, qapp):
        w = _make_worker(qapp)
        active_proxy = AsyncProxyMock(connection="/settings/1")
        conn_proxy = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "802-11-wireless": {"ssid": ("ay", b"TestNet")},
                    "connection": {"type": ("s", "802-11-wireless")},
                }
            )
        )
        w._active_conn = lambda path: active_proxy
        w._conn_settings = lambda path: conn_proxy
        result = await w._ssid_from_active_connection("/active/1")
        assert result == "TestNet"

    @pytest.mark.asyncio
    async def test_non_wireless_returns_empty(self, qapp):
        w = _make_worker(qapp)
        active_proxy = AsyncProxyMock(connection="/settings/1")
        conn_proxy = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "connection": {"type": ("s", "802-3-ethernet")},
                }
            )
        )
        w._active_conn = lambda path: active_proxy
        w._conn_settings = lambda path: conn_proxy
        result = await w._ssid_from_active_connection("/active/1")
        assert result == ""

    @pytest.mark.asyncio
    async def test_exception_returns_empty(self, qapp):
        w = _make_worker(qapp)
        w._active_conn = MagicMock(side_effect=Exception("boom"))
        result = await w._ssid_from_active_connection("/active/bad")
        assert result == ""



class TestGetSSIDFromAnyActive:
    @pytest.mark.asyncio
    async def test_finds_wifi_in_active_connections(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(active_connections=["/a/1", "/a/2"])
        w._nm = _ProxyFactory(nm_proxy)
        call_count = [0]

        async def _mock_ssid(path):
            call_count[0] += 1
            return "" if call_count[0] == 1 else "HotspotSSID"

        w._ssid_from_active_connection = _mock_ssid
        assert await w._get_ssid_from_any_active() == "HotspotSSID"

    @pytest.mark.asyncio
    async def test_no_active_returns_empty(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(active_connections=[])
        w._nm = _ProxyFactory(nm_proxy)
        assert await w._get_ssid_from_any_active() == ""



class TestGetCurrentIp:
    @pytest.mark.asyncio
    async def test_primary_slash_returns_empty(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(primary_connection="/")
        w._nm = _ProxyFactory(nm_proxy)
        assert await w._get_current_ip() == ""

    @pytest.mark.asyncio
    async def test_happy_path_returns_ip(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(primary_connection="/active/1")
        w._nm = _ProxyFactory(nm_proxy)
        active_proxy = AsyncProxyMock(ip4_config="/ip4/1")
        w._active_conn = lambda path: active_proxy
        ipv4_proxy = AsyncProxyMock(address_data=[{"address": ("s", "192.168.1.50")}])
        w._ipv4 = lambda path: ipv4_proxy
        assert await w._get_current_ip() == "192.168.1.50"

    @pytest.mark.asyncio
    async def test_exception_returns_empty(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(
            primary_connection=AsyncMock(side_effect=Exception("fail"))
        )
        w._nm = lambda: nm_proxy
        assert await w._get_current_ip() == ""



class TestGetIpByInterface:
    @pytest.mark.asyncio
    async def test_cached_path_used(self, qapp):
        w = _make_worker(qapp)
        w._iface_to_device_path = {"wlan0": "/dev/wifi0"}
        generic_proxy = AsyncProxyMock(ip4_config="/ip4/1")
        w._generic = lambda path: generic_proxy
        ipv4_proxy = AsyncProxyMock(address_data=[{"address": ("s", "192.168.1.50")}])
        w._ipv4 = lambda path: ipv4_proxy
        assert await w._get_ip_by_interface("wlan0") == "192.168.1.50"

    @pytest.mark.asyncio
    async def test_no_matching_interface_returns_empty(self, qapp):
        w = _make_worker(qapp)
        w._iface_to_device_path = {}
        nm_proxy = AsyncProxyMock(get_devices=AsyncMock(return_value=["/dev/1"]))
        w._nm = _ProxyFactory(nm_proxy)
        generic_proxy = AsyncProxyMock(interface="eth0")
        w._generic = lambda path: generic_proxy
        assert await w._get_ip_by_interface("wlan0") == ""

    @pytest.mark.asyncio
    async def test_exception_returns_empty(self, qapp):
        w = _make_worker(qapp)
        w._iface_to_device_path = {}
        nm_proxy = AsyncProxyMock(get_devices=AsyncMock(side_effect=Exception("fail")))
        w._nm = _ProxyFactory(nm_proxy)
        assert await w._get_ip_by_interface("wlan0") == ""



class TestGetIpOsFallback:
    def test_empty_interface(self):
        assert NetworkManagerWorker._get_ip_os_fallback("") == ""



class TestGetCurrentState:
    @pytest.mark.asyncio
    async def test_not_running_emits_default_state(self, qapp):
        w = _make_worker(qapp, running=True)
        w._ensure_dbus_connection = AsyncMock(return_value=False)
        received = []
        w.state_changed.connect(lambda s: received.append(s))
        await w._async_get_current_state()
        assert len(received) == 1
        assert isinstance(received[0], NetworkState)

    @pytest.mark.asyncio
    async def test_exception_emits_error(self, qapp):
        w = _make_worker(qapp)
        w._ensure_dbus_connection = AsyncMock(side_effect=RuntimeError("crash"))
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append((op, msg)))
        await w._async_get_current_state()
        assert len(errors) == 1



class TestBuildCurrentState:
    @pytest.mark.asyncio
    async def test_returns_default_when_no_bus(self, qapp):
        w = _bare_worker(qapp)
        w._system_bus = None
        state = await w._build_current_state()
        assert state.connectivity == ConnectivityState.UNKNOWN
        assert state.wifi_enabled is False

    @pytest.mark.asyncio
    async def test_connected_state(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(
            check_connectivity=AsyncMock(return_value=4),
            wireless_enabled=True,
            primary_connection="/",
            active_connections=[],
        )
        w._nm = _ProxyFactory(nm_proxy)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._has_ethernet_carrier = AsyncMock(return_value=False)
        w._get_current_ssid = AsyncMock(return_value="")
        w._get_active_vlans = AsyncMock(return_value=[])
        state = await w._build_current_state()
        assert state.connectivity == ConnectivityState.FULL
        assert state.wifi_enabled is True
        assert state.current_ssid == ""

    @pytest.mark.asyncio
    async def test_connected_with_ssid_gets_signal_and_security(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(
            check_connectivity=AsyncMock(return_value=4),
            wireless_enabled=True,
        )
        w._nm = _ProxyFactory(nm_proxy)
        w._get_current_ssid = AsyncMock(return_value="HomeWiFi")
        w._get_ip_by_interface = AsyncMock(return_value="192.168.1.50")
        w._get_current_ip = AsyncMock(return_value="192.168.1.50")
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._has_ethernet_carrier = AsyncMock(return_value=False)
        w._build_signal_map = AsyncMock(return_value={"homewifi": 72})
        w._get_active_vlans = AsyncMock(return_value=[])

        sn = SavedNetwork(
            ssid="HomeWiFi",
            uuid="u",
            connection_path="/p",
            security_type="wpa-psk",
            mode="infrastructure",
        )
        w._saved_cache = [sn]
        w._saved_cache_dirty = False

        state = await w._build_current_state()
        assert state.signal_strength == 72
        assert state.security_type == "wpa-psk"
        assert state.current_ssid == "HomeWiFi"

    @pytest.mark.asyncio
    async def test_hotspot_state_has_correct_security(self, qapp):
        w = _make_worker(qapp)
        w._hotspot_config.ssid = "TestHotspot"
        nm_proxy = AsyncProxyMock(
            check_connectivity=AsyncMock(return_value=4),
            wireless_enabled=True,
        )
        w._nm = _ProxyFactory(nm_proxy)
        w._get_current_ssid = AsyncMock(return_value="TestHotspot")
        w._get_ip_by_interface = AsyncMock(return_value="10.42.0.1")
        w._get_current_ip = AsyncMock(return_value="10.42.0.1")
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._has_ethernet_carrier = AsyncMock(return_value=False)
        w._build_signal_map = AsyncMock(return_value={})
        w._get_active_vlans = AsyncMock(return_value=[])

        state = await w._build_current_state()
        assert state.hotspot_enabled is True
        assert state.security_type == "wpa-psk"

    @pytest.mark.asyncio
    async def test_hotspot_flag_fallback_when_dbus_ssid_empty(self, qapp):
        w = _make_worker(qapp)
        w._hotspot_config.ssid = "PrinterHotspot"
        w._is_hotspot_active = True
        nm_proxy = AsyncProxyMock(
            check_connectivity=AsyncMock(return_value=4),
            wireless_enabled=True,
        )
        w._nm = _ProxyFactory(nm_proxy)
        w._get_current_ssid = AsyncMock(return_value="")
        w._get_ip_by_interface = AsyncMock(return_value="10.42.0.1")
        w._get_current_ip = AsyncMock(return_value="")
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._has_ethernet_carrier = AsyncMock(return_value=False)
        w._build_signal_map = AsyncMock(return_value={})
        w._get_active_vlans = AsyncMock(return_value=[])

        state = await w._build_current_state()
        assert state.hotspot_enabled is True
        assert state.current_ssid == "PrinterHotspot"

    @pytest.mark.asyncio
    async def test_ethernet_connected_included_in_state(self, qapp):
        w = _make_worker(qapp, with_wired=True)
        nm_proxy = AsyncProxyMock(
            check_connectivity=AsyncMock(return_value=4),
            wireless_enabled=False,
        )
        w._nm = _ProxyFactory(nm_proxy)
        w._get_current_ssid = AsyncMock(return_value="")
        w._get_ip_by_interface = AsyncMock(return_value="192.168.0.10")
        w._is_ethernet_connected = AsyncMock(return_value=True)
        w._has_ethernet_carrier = AsyncMock(return_value=True)
        w._get_active_vlans = AsyncMock(return_value=[])

        state = await w._build_current_state()
        assert state.ethernet_connected is True
        assert state.ethernet_carrier is True

    @pytest.mark.asyncio
    async def test_exception_returns_default(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(
            check_connectivity=AsyncMock(side_effect=RuntimeError("bang"))
        )
        w._nm = _ProxyFactory(nm_proxy)
        state = await w._build_current_state()
        assert state.connectivity == ConnectivityState.UNKNOWN



class TestScanNetworks:
    @pytest.mark.asyncio
    async def test_scan_no_wifi_path_emits_empty(self, qapp):
        w = _make_worker(qapp, with_wifi=False)
        received = []
        w.networks_scanned.connect(lambda n: received.append(n))
        await w._async_scan_networks()
        assert received == [[]]

    @pytest.mark.asyncio
    async def test_scan_dbus_not_connected_emits_empty(self, qapp):
        w = _make_worker(qapp)
        w._ensure_dbus_connection = AsyncMock(return_value=False)
        received = []
        w.networks_scanned.connect(lambda n: received.append(n))
        await w._async_scan_networks()
        assert received == [[]]

    @pytest.mark.asyncio
    async def test_scan_last_scan_negative_emits_empty(self, qapp):
        w = _make_worker(qapp)
        w._ensure_dbus_connection = AsyncMock(return_value=True)
        wifi_proxy = AsyncProxyMock(
            request_scan=AsyncMock(),
            last_scan=-1,
        )
        w._wifi = _ProxyFactory(wifi_proxy)
        received = []
        w.networks_scanned.connect(lambda n: received.append(n))
        await w._async_scan_networks()
        assert received == [[]]

    @pytest.mark.asyncio
    async def test_scan_happy_path_emits_networks(self, qapp):
        w = _make_worker(qapp)
        w._ensure_dbus_connection = AsyncMock(return_value=True)
        nm_proxy = AsyncProxyMock(wireless_enabled=True)
        w._nm = _ProxyFactory(nm_proxy)
        wifi_proxy = AsyncProxyMock(
            request_scan=AsyncMock(),
            last_scan=100,
            get_all_access_points=AsyncMock(return_value=["/ap/1"]),
        )
        w._wifi = _ProxyFactory(wifi_proxy)
        w._get_current_ssid = AsyncMock(return_value="")
        w._get_saved_ssid_names_cached = AsyncMock(return_value=[])

        w._parse_ap = AsyncMock(
            return_value=NetworkInfo(
                ssid="TestNet",
                signal_strength=75,
                network_status=NetworkStatus.DISCOVERED,
                security_type=SecurityType.WPA2_PSK,
            )
        )
        received = []
        w.networks_scanned.connect(lambda n: received.append(n))
        await w._async_scan_networks()
        assert len(received) == 1
        assert len(received[0]) == 1
        assert received[0][0].ssid == "TestNet"

    @pytest.mark.asyncio
    async def test_scan_deduplicates_ssids(self, qapp):
        w = _make_worker(qapp)
        w._ensure_dbus_connection = AsyncMock(return_value=True)
        nm_proxy = AsyncProxyMock(wireless_enabled=True)
        w._nm = _ProxyFactory(nm_proxy)
        wifi_proxy = AsyncProxyMock(
            request_scan=AsyncMock(),
            last_scan=100,
            get_all_access_points=AsyncMock(return_value=["/ap/1", "/ap/2"]),
        )
        w._wifi = _ProxyFactory(wifi_proxy)
        w._get_current_ssid = AsyncMock(return_value="")
        w._get_saved_ssid_names_cached = AsyncMock(return_value=[])
        w._parse_ap = AsyncMock(
            return_value=NetworkInfo(
                ssid="DuplicateNet",
                signal_strength=80,
                network_status=NetworkStatus.DISCOVERED,
                security_type=SecurityType.WPA2_PSK,
            )
        )
        received = []
        w.networks_scanned.connect(lambda n: received.append(n))
        await w._async_scan_networks()
        assert len(received[0]) == 1

    @pytest.mark.asyncio
    async def test_scan_exception_emits_error_and_empty(self, qapp):
        w = _make_worker(qapp)
        w._ensure_dbus_connection = AsyncMock(return_value=True)
        wifi_proxy = AsyncProxyMock(
            request_scan=AsyncMock(),
            last_scan=100,
            get_all_access_points=AsyncMock(side_effect=RuntimeError("kaboom")),
        )
        w._wifi = _ProxyFactory(wifi_proxy)
        errors = []
        received = []
        w.error_occurred.connect(lambda op, msg: errors.append((op, msg)))
        w.networks_scanned.connect(lambda n: received.append(n))
        await w._async_scan_networks()
        assert len(errors) == 1
        assert received == [[]]



class TestParseAp:
    @pytest.mark.asyncio
    async def test_empty_props_returns_none(self, qapp):
        w = _make_worker(qapp)
        w._get_all_ap_properties = AsyncMock(return_value={})
        result = await w._parse_ap("/ap/x", "", set())
        assert result is None

    @pytest.mark.asyncio
    async def test_valid_ap_returns_network_info(self, qapp):
        w = _make_worker(qapp)
        w._get_all_ap_properties = AsyncMock(
            return_value={
                "ssid": b"MyNet",
                "strength": 70,
                "frequency": 2437,
                "hw_address": "AA:BB:CC:DD:EE:FF",
                "max_bitrate": 54000,
                "flags": 1,
                "wpa_flags": 0,
                "rsn_flags": 0x108,
            }
        )
        result = await w._parse_ap("/ap/1", "", set())
        assert result is not None
        assert result.ssid == "MyNet"
        assert result.security_type == SecurityType.WPA2_PSK

    @pytest.mark.asyncio
    async def test_active_network_marked(self, qapp):
        w = _make_worker(qapp)
        w._get_all_ap_properties = AsyncMock(
            return_value={
                "ssid": b"Active",
                "strength": 60,
                "frequency": 2437,
                "hw_address": "AA:BB",
                "max_bitrate": 54000,
                "flags": 1,
                "wpa_flags": 0,
                "rsn_flags": 0x108,
            }
        )
        result = await w._parse_ap("/ap/1", "Active", set())
        assert result.is_active is True

    @pytest.mark.asyncio
    async def test_saved_network_marked(self, qapp):
        w = _make_worker(qapp)
        w._get_all_ap_properties = AsyncMock(
            return_value={
                "ssid": b"Saved",
                "strength": 60,
                "frequency": 2437,
                "hw_address": "AA:BB",
                "max_bitrate": 54000,
                "flags": 1,
                "wpa_flags": 0,
                "rsn_flags": 0x108,
            }
        )
        result = await w._parse_ap("/ap/1", "", {"Saved"})
        assert result.is_saved is True

    @pytest.mark.asyncio
    async def test_hidden_ssid_returns_none(self, qapp):
        w = _make_worker(qapp)
        w._get_all_ap_properties = AsyncMock(
            return_value={
                "ssid": b"",
                "strength": 80,
                "frequency": 2437,
                "hw_address": "AA:BB",
                "max_bitrate": 54000,
                "flags": 1,
                "wpa_flags": 0,
                "rsn_flags": 0x08,
            }
        )
        result = await w._parse_ap("/ap/1", "", set())
        assert result is None



class TestBuildSignalMap:
    @pytest.mark.asyncio
    async def test_no_wifi_returns_empty(self, qapp):
        w = _make_worker(qapp, with_wifi=False)
        assert await w._build_signal_map() == {}

    @pytest.mark.asyncio
    async def test_keeps_strongest_for_duplicate_ssids(self, qapp):
        w = _make_worker(qapp)
        wifi_proxy = AsyncProxyMock(access_points=["/ap/1", "/ap/2"])
        w._wifi = _ProxyFactory(wifi_proxy)
        call_count = [0]

        async def mock_props(path):
            call_count[0] += 1
            strengths = {"/ap/1": 40, "/ap/2": 80}
            return {"ssid": b"SameNet", "strength": strengths[path]}

        w._get_all_ap_properties = mock_props
        result = await w._build_signal_map()
        assert result["samenet"] == 80



class TestSavedNetworkCache:
    def test_invalidate_marks_dirty(self, qapp):
        w = _bare_worker(qapp)
        w._saved_cache_dirty = False
        w._invalidate_saved_cache()
        assert w._saved_cache_dirty is True

    @pytest.mark.asyncio
    async def test_get_saved_ssid_names_uses_cache(self, qapp):
        w = _bare_worker(qapp)
        w._saved_cache = [
            SavedNetwork(
                ssid="A",
                uuid="u1",
                connection_path="/1",
                security_type="wpa-psk",
                mode="infrastructure",
            ),
            SavedNetwork(
                ssid="B",
                uuid="u2",
                connection_path="/2",
                security_type="open",
                mode="infrastructure",
            ),
        ]
        w._saved_cache_dirty = False
        assert await w._get_saved_ssid_names_cached() == ["A", "B"]

    @pytest.mark.asyncio
    async def test_get_saved_network_cached_found(self, qapp):
        w = _bare_worker(qapp)
        sn = SavedNetwork(
            ssid="Target",
            uuid="u",
            connection_path="/p",
            security_type="wpa-psk",
            mode="infrastructure",
        )
        w._saved_cache = [sn]
        w._saved_cache_dirty = False
        assert await w._get_saved_network_cached("target") == sn

    @pytest.mark.asyncio
    async def test_get_saved_network_cached_not_found(self, qapp):
        w = _bare_worker(qapp)
        w._saved_cache = []
        w._saved_cache_dirty = False
        assert await w._get_saved_network_cached("missing") is None

    @pytest.mark.asyncio
    async def test_is_known_true(self, qapp):
        w = _bare_worker(qapp)
        w._saved_cache = [
            SavedNetwork(
                ssid="Known",
                uuid="u",
                connection_path="/p",
                security_type="",
                mode="infrastructure",
            ),
        ]
        w._saved_cache_dirty = False
        assert await w._is_known("known") is True

    @pytest.mark.asyncio
    async def test_is_known_false(self, qapp):
        w = _bare_worker(qapp)
        w._saved_cache = []
        w._saved_cache_dirty = False
        assert await w._is_known("nope") is False

    @pytest.mark.asyncio
    async def test_get_connection_path_found(self, qapp):
        w = _bare_worker(qapp)
        sn = SavedNetwork(
            ssid="Net",
            uuid="u",
            connection_path="/conn/1",
            security_type="",
            mode="infrastructure",
        )
        w._saved_cache = [sn]
        w._saved_cache_dirty = False
        assert await w._get_connection_path("net") == "/conn/1"

    @pytest.mark.asyncio
    async def test_get_connection_path_not_found(self, qapp):
        w = _bare_worker(qapp)
        w._saved_cache = []
        w._saved_cache_dirty = False
        assert await w._get_connection_path("nope") is None



class TestLoadSavedNetworks:
    @pytest.mark.asyncio
    async def test_happy_path_emits_list(self, qapp):
        w = _make_worker(qapp)
        fake_saved = [
            SavedNetwork(
                ssid="Net1",
                uuid="u1",
                connection_path="/1",
                security_type="wpa-psk",
                mode="infrastructure",
            ),
        ]
        w._get_saved_networks_impl = AsyncMock(return_value=fake_saved)
        received = []
        w.saved_networks_loaded.connect(lambda n: received.append(n))
        await w._async_load_saved_networks()
        assert received == [fake_saved]
        assert w._saved_cache == fake_saved
        assert w._saved_cache_dirty is False

    @pytest.mark.asyncio
    async def test_exception_emits_error_and_empty(self, qapp):
        w = _make_worker(qapp)
        w._get_saved_networks_impl = AsyncMock(side_effect=RuntimeError("fail"))
        errors = []
        received = []
        w.error_occurred.connect(lambda op, msg: errors.append((op, msg)))
        w.saved_networks_loaded.connect(lambda n: received.append(n))
        await w._async_load_saved_networks()
        assert len(errors) == 1
        assert errors[0][0] == "load_saved_networks"
        assert received == [[]]



class TestGetSavedNetworksImpl:
    @pytest.mark.asyncio
    async def test_no_bus_returns_empty(self, qapp):
        w = _bare_worker(qapp)
        w._system_bus = None
        assert await w._get_saved_networks_impl() == []



class TestBuildConnectionProperties:
    def _call(self, qapp, flags=0, wpa_flags=0, rsn_flags=0, password="pass123"):
        w = _make_worker(qapp)
        props = {"flags": flags, "wpa_flags": wpa_flags, "rsn_flags": rsn_flags}
        return w._build_connection_properties("Net", password, "wlan0", 50, props)

    def test_open_network(self, qapp):
        result = self._call(qapp, flags=0)
        assert result is not None
        assert "802-11-wireless-security" not in result

    def test_wpa2_psk(self, qapp):
        result = self._call(qapp, flags=1, rsn_flags=0x108)
        assert result["802-11-wireless-security"]["key-mgmt"] == ("s", "wpa-psk")

    def test_sae_transition_uses_wpa_psk(self, qapp):
        result = self._call(qapp, flags=1, rsn_flags=0x508)
        assert result["802-11-wireless-security"]["key-mgmt"] == ("s", "wpa-psk")
        assert result["802-11-wireless-security"]["pmf"] == ("u", 2)  # OPTIONAL

    def test_pure_sae(self, qapp):
        result = self._call(qapp, flags=1, rsn_flags=0x400)
        assert result["802-11-wireless-security"]["key-mgmt"] == ("s", "sae")
        assert result["802-11-wireless-security"]["pmf"] == ("u", 3)  # REQUIRED

    def test_wpa_psk(self, qapp):
        result = self._call(qapp, flags=1, wpa_flags=0x108)
        assert result["802-11-wireless-security"]["key-mgmt"] == ("s", "wpa-psk")

    def test_wep_returns_none(self, qapp):
        """WEP is unsupported — returns None."""
        result = self._call(qapp, flags=1)  # privacy flag but no WPA/RSN
        assert result is None

    def test_wpa_eap_returns_none(self, qapp):
        result = self._call(qapp, flags=1, rsn_flags=0x200)
        assert result is None

    def test_connection_has_correct_base_structure(self, qapp):
        result = self._call(qapp, flags=1, rsn_flags=0x108)
        assert result["connection"]["type"] == ("s", "802-11-wireless")
        assert result["ipv4"]["method"] == ("s", "auto")
        assert result["802-11-wireless"]["mode"] == ("s", "infrastructure")



class TestConnectNetwork:
    @pytest.mark.asyncio
    async def test_connect_success_emits_result_and_state(self, qapp):
        w = _make_worker(qapp)
        w._connect_network_impl = AsyncMock(
            return_value=ConnectionResult(True, "Connected")
        )
        w._build_current_state = AsyncMock(
            return_value=NetworkState(current_ssid="Net")
        )
        results = []
        states = []
        w.connection_result.connect(lambda r: results.append(r))
        w.state_changed.connect(lambda s: states.append(s))
        await w._async_connect_network("Net")
        assert results[0].success is True
        assert len(states) >= 1
        assert w._is_hotspot_active is False

    @pytest.mark.asyncio
    async def test_connect_exception_emits_failure(self, qapp):
        w = _make_worker(qapp)
        w._connect_network_impl = AsyncMock(side_effect=RuntimeError("boom"))
        results = []
        w.connection_result.connect(lambda r: results.append(r))
        await w._async_connect_network("Net")
        assert results[0].success is False
        assert results[0].error_code == "connect_failed"



class TestConnectNetworkImpl:
    @pytest.mark.asyncio
    async def test_no_bus_returns_error(self, qapp):
        w = _make_worker(qapp)
        w._system_bus = None
        result = await w._connect_network_impl("Net")
        assert result.error_code == "no_nm"

    @pytest.mark.asyncio
    async def test_not_saved_returns_not_found(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(
            wireless_enabled=True,
            activate_connection=AsyncMock(),
        )
        w._nm = _ProxyFactory(nm_proxy)
        w._saved_cache = []
        w._saved_cache_dirty = False
        w._find_connection_path_direct = AsyncMock(return_value=None)
        result = await w._connect_network_impl("Ghost")
        assert result.error_code == "not_found"



class TestFindConnectionPathDirect:
    @pytest.mark.asyncio
    async def test_found(self, qapp):
        w = _make_worker(qapp)
        nm_settings_proxy = AsyncProxyMock(
            list_connections=AsyncMock(return_value=["/conn/1"])
        )
        w._nm_settings = _ProxyFactory(nm_settings_proxy)
        conn_proxy = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "connection": {"type": ("s", "802-11-wireless")},
                    "802-11-wireless": {"ssid": ("ay", b"TargetNet")},
                }
            )
        )
        w._conn_settings = lambda path: conn_proxy
        result = await w._find_connection_path_direct("targetnet")
        assert result == "/conn/1"
        assert w._saved_cache_dirty is True

    @pytest.mark.asyncio
    async def test_not_found(self, qapp):
        w = _make_worker(qapp)
        nm_settings_proxy = AsyncProxyMock(list_connections=AsyncMock(return_value=[]))
        w._nm_settings = _ProxyFactory(nm_settings_proxy)
        assert await w._find_connection_path_direct("ghost") is None

    @pytest.mark.asyncio
    async def test_skips_non_wireless(self, qapp):
        w = _make_worker(qapp)
        nm_settings_proxy = AsyncProxyMock(
            list_connections=AsyncMock(return_value=["/conn/eth"])
        )
        w._nm_settings = _ProxyFactory(nm_settings_proxy)
        conn_proxy = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "connection": {"type": ("s", "802-3-ethernet")},
                }
            )
        )
        w._conn_settings = lambda path: conn_proxy
        assert await w._find_connection_path_direct("net") is None

    @pytest.mark.asyncio
    async def test_exception_returns_none(self, qapp):
        w = _make_worker(qapp)
        nm_settings_proxy = AsyncProxyMock(
            list_connections=AsyncMock(side_effect=Exception("fail"))
        )
        w._nm_settings = _ProxyFactory(nm_settings_proxy)
        assert await w._find_connection_path_direct("net") is None



class TestDisconnect:
    @pytest.mark.asyncio
    async def test_disconnect_emits_success(self, qapp):
        w = _make_worker(qapp)
        wifi_proxy = AsyncProxyMock(disconnect=AsyncMock())
        w._wifi = _ProxyFactory(wifi_proxy)
        received = []
        w.connection_result.connect(lambda r: received.append(r))
        await w._async_disconnect()
        assert received[0].success is True

    @pytest.mark.asyncio
    async def test_disconnect_no_wifi_still_succeeds(self, qapp):
        w = _make_worker(qapp, with_wifi=False)
        received = []
        w.connection_result.connect(lambda r: received.append(r))
        await w._async_disconnect()
        assert received[0].success is True

    @pytest.mark.asyncio
    async def test_disconnect_emits_failure_on_error(self, qapp):
        w = _make_worker(qapp)
        wifi_proxy = AsyncProxyMock(
            disconnect=AsyncMock(side_effect=Exception("Not active"))
        )
        w._wifi = _ProxyFactory(wifi_proxy)
        received = []
        w.connection_result.connect(lambda r: received.append(r))
        await w._async_disconnect()
        assert received[0].success is False
        assert "Not active" in received[0].message



class TestDeleteNetwork:
    @pytest.mark.asyncio
    async def test_delete_success_emits_result_and_state(self, qapp):
        w = _make_worker(qapp)
        w._delete_network_impl = AsyncMock(
            return_value=ConnectionResult(True, "deleted")
        )
        w._build_current_state = AsyncMock(return_value=NetworkState())
        results = []
        states = []
        w.connection_result.connect(lambda r: results.append(r))
        w.state_changed.connect(lambda s: states.append(s))
        await w._async_delete_network("Net")
        assert results[0].success is True
        assert w._saved_cache_dirty is True
        assert len(states) >= 1

    @pytest.mark.asyncio
    async def test_delete_exception_emits_failure(self, qapp):
        w = _make_worker(qapp)
        w._delete_network_impl = AsyncMock(side_effect=RuntimeError("boom"))
        results = []
        w.connection_result.connect(lambda r: results.append(r))
        await w._async_delete_network("Net")
        assert results[0].error_code == "delete_failed"



class TestDeleteNetworkImpl:
    @pytest.mark.asyncio
    async def test_not_found(self, qapp):
        w = _make_worker(qapp)
        w._saved_cache = []
        w._saved_cache_dirty = False
        result = await w._delete_network_impl("ghost")
        assert result.error_code == "not_found"

    @pytest.mark.asyncio
    async def test_disconnects_if_active(self, qapp):
        w = _make_worker(qapp)
        sn = SavedNetwork(
            ssid="Active",
            uuid="u",
            connection_path="/conn/1",
            security_type="",
            mode="infrastructure",
        )
        w._saved_cache = [sn]
        w._saved_cache_dirty = False
        conn_proxy = AsyncProxyMock(delete=AsyncMock())
        w._conn_settings = lambda path: conn_proxy
        nm_settings_proxy = AsyncProxyMock(reload_connections=AsyncMock())
        w._nm_settings = _ProxyFactory(nm_settings_proxy)
        w._get_current_ssid = AsyncMock(return_value="Active")
        wifi_proxy = AsyncProxyMock(disconnect=AsyncMock())
        w._wifi = _ProxyFactory(wifi_proxy)
        result = await w._delete_network_impl("Active")
        assert result.success is True
        wifi_proxy.disconnect.assert_called_once()



class TestUpdateNetwork:
    @pytest.mark.asyncio
    async def test_update_emits_result(self, qapp):
        w = _make_worker(qapp)
        w._update_network_impl = AsyncMock(
            return_value=ConnectionResult(True, "updated")
        )
        results = []
        w.connection_result.connect(lambda r: results.append(r))
        await w._async_update_network("Net", "newpass", ConnectionPriority.HIGH.value)
        assert results[0].success is True
        assert w._saved_cache_dirty is True

    @pytest.mark.asyncio
    async def test_update_exception_emits_failure(self, qapp):
        w = _make_worker(qapp)
        w._update_network_impl = AsyncMock(side_effect=RuntimeError("boom"))
        results = []
        w.connection_result.connect(lambda r: results.append(r))
        await w._async_update_network("Net", "", 0)
        assert results[0].error_code == "update_failed"



class TestUpdateNetworkImpl:
    @pytest.mark.asyncio
    async def test_not_found(self, qapp):
        w = _make_worker(qapp)
        w._saved_cache = []
        w._saved_cache_dirty = False
        result = await w._update_network_impl("Ghost", None, None)
        assert result.error_code == "not_found"

    @pytest.mark.asyncio
    async def test_updates_password(self, qapp):
        w = _make_worker(qapp)
        sn = SavedNetwork(
            ssid="Net",
            uuid="u",
            connection_path="/conn/1",
            security_type="wpa-psk",
            mode="infrastructure",
        )
        w._saved_cache = [sn]
        w._saved_cache_dirty = False
        conn_proxy = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "connection": {"id": ("s", "Net")},
                    "802-11-wireless-security": {"key-mgmt": ("s", "wpa-psk")},
                }
            ),
            get_secrets=AsyncMock(
                return_value={
                    "802-11-wireless-security": {"psk": ("s", "oldpass")},
                }
            ),
            update=AsyncMock(),
        )
        w._conn_settings = lambda path: conn_proxy
        result = await w._update_network_impl("net", "newpass", None)
        assert result.success is True
        call_args = conn_proxy.update.call_args[0][0]
        assert call_args["802-11-wireless-security"]["psk"] == ("s", "newpass")

    @pytest.mark.asyncio
    async def test_updates_priority(self, qapp):
        w = _make_worker(qapp)
        sn = SavedNetwork(
            ssid="Net",
            uuid="u",
            connection_path="/conn/1",
            security_type="wpa-psk",
            mode="infrastructure",
        )
        w._saved_cache = [sn]
        w._saved_cache_dirty = False
        conn_proxy = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "connection": {"id": ("s", "Net")},
                }
            ),
            get_secrets=AsyncMock(side_effect=Exception("no secrets")),
            update=AsyncMock(),
        )
        w._conn_settings = lambda path: conn_proxy
        result = await w._update_network_impl("net", None, 90)
        assert result.success is True
        call_args = conn_proxy.update.call_args[0][0]
        assert call_args["connection"]["autoconnect-priority"] == ("i", 90)

    @pytest.mark.asyncio
    async def test_update_exception_returns_failure(self, qapp):
        w = _make_worker(qapp)
        sn = SavedNetwork(
            ssid="Net",
            uuid="u",
            connection_path="/conn/1",
            security_type="wpa-psk",
            mode="infrastructure",
        )
        w._saved_cache = [sn]
        w._saved_cache_dirty = False
        conn_proxy = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "connection": {"id": ("s", "Net")},
                }
            ),
            get_secrets=AsyncMock(side_effect=Exception("no secrets")),
            update=AsyncMock(side_effect=Exception("D-Bus error")),
        )
        w._conn_settings = lambda path: conn_proxy
        result = await w._update_network_impl("net", None, 90)
        assert result.success is False
        assert result.error_code == "update_failed"



class TestEnsureDbusConnection:
    @pytest.mark.asyncio
    async def test_not_running_returns_false(self, qapp):
        w = _make_worker(qapp, running=False)
        assert await w._ensure_dbus_connection() is False

    @pytest.mark.asyncio
    async def test_healthy_bus_returns_true(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(version="1.44.0")
        w._nm = _ProxyFactory(nm_proxy)
        assert await w._ensure_dbus_connection() is True
        assert w._consecutive_dbus_errors == 0

    @pytest.mark.asyncio
    async def test_error_increments_counter(self, qapp):
        w = _make_worker(qapp)
        nm_proxy = AsyncProxyMock(version=AsyncMock(side_effect=Exception("fail")))
        w._nm = lambda: nm_proxy
        result = await w._ensure_dbus_connection()
        assert result is False
        assert w._consecutive_dbus_errors == 1



class TestShutdown:
    @pytest.mark.asyncio
    async def test_shutdown_sets_not_running(self, qapp):
        w = _make_worker(qapp)
        await w._async_shutdown()
        assert w._running is False
        assert w._primary_wifi_path == ""
        assert w._primary_wired_path == ""



class TestDisconnectEthernet:
    @pytest.mark.asyncio
    async def test_no_wired_device_is_noop(self, qapp):
        w = _make_worker(qapp, with_wired=False)
        await w._async_disconnect_ethernet()  # should not raise

    @pytest.mark.asyncio
    async def test_calls_disconnect(self, qapp):
        w = _make_worker(qapp, with_wired=True)
        wired_proxy = AsyncProxyMock(disconnect=AsyncMock())
        w._wired = _ProxyFactory(wired_proxy)
        w._deactivate_all_vlans = AsyncMock()
        await w._async_disconnect_ethernet()
        wired_proxy.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_exception_logged_not_raised(self, qapp):
        w = _make_worker(qapp, with_wired=True)
        wired_proxy = AsyncProxyMock(
            disconnect=AsyncMock(side_effect=Exception("not connected"))
        )
        w._wired = _ProxyFactory(wired_proxy)
        w._deactivate_all_vlans = AsyncMock()
        await w._async_disconnect_ethernet()  # should not raise



class TestAddNetwork:
    @pytest.mark.asyncio
    async def test_add_emits_result_and_invalidates(self, qapp):
        w = _make_worker(qapp)
        w._add_network_impl = AsyncMock(return_value=ConnectionResult(True, "added"))
        received = []
        w.connection_result.connect(lambda r: results.append(r))
        results = received  # fix name
        await w._async_add_network("Net", "pass", ConnectionPriority.HIGH.value)
        assert received[0].success is True
        assert w._saved_cache_dirty is True

    @pytest.mark.asyncio
    async def test_add_exception_emits_failure(self, qapp):
        w = _make_worker(qapp)
        w._add_network_impl = AsyncMock(side_effect=RuntimeError("crash"))
        received = []
        w.connection_result.connect(lambda r: received.append(r))
        await w._async_add_network("Net", "pass", 0)
        assert received[0].success is False
        assert received[0].error_code == "add_failed"



class TestAddNetworkImpl:
    @pytest.mark.asyncio
    async def test_no_wifi_returns_no_interface(self, qapp):
        w = _make_worker(qapp, with_wifi=False)
        result = await w._add_network_impl("Net", "pass", 0)
        assert result.error_code == "no_interface"

    @pytest.mark.asyncio
    async def test_ap_not_found_returns_not_found(self, qapp):
        w = _make_worker(qapp)
        w._saved_cache = []
        w._saved_cache_dirty = False
        wifi_proxy = AsyncProxyMock(
            request_scan=AsyncMock(),
            get_all_access_points=AsyncMock(return_value=[]),
            interface="wlan0",
        )
        w._wifi = _ProxyFactory(wifi_proxy)
        result = await w._add_network_impl("Ghost", "pass", 0)
        assert result.error_code == "not_found"

    @pytest.mark.asyncio
    async def test_unsupported_security_returns_error(self, qapp):
        w = _make_worker(qapp)
        w._saved_cache = []
        w._saved_cache_dirty = False
        wifi_proxy = AsyncProxyMock(
            request_scan=AsyncMock(),
            get_all_access_points=AsyncMock(return_value=["/ap/1"]),
            interface="wlan0",
        )
        w._wifi = _ProxyFactory(wifi_proxy)
        w._get_all_ap_properties = AsyncMock(
            return_value={
                "ssid": b"EAPNet",
                "strength": 70,
                "frequency": 2437,
                "hw_address": "AA:BB",
                "max_bitrate": 54000,
                "flags": 1,
                "wpa_flags": 0,
                "rsn_flags": 0x200,
            }
        )
        result = await w._add_network_impl("EAPNet", "pass", 0)
        assert result.error_code == "unsupported_security"



class TestDeleteConnectionsById:
    @pytest.mark.asyncio
    async def test_deletes_matching(self, qapp):
        w = _make_worker(qapp)
        nm_settings_proxy = AsyncProxyMock(
            list_connections=AsyncMock(return_value=["/conn/1", "/conn/2"])
        )
        w._nm_settings = _ProxyFactory(nm_settings_proxy)

        conn1 = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "connection": {"id": ("s", "TestHotspot")},
                }
            ),
            delete=AsyncMock(),
        )
        conn2 = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "connection": {"id": ("s", "OtherNet")},
                }
            ),
            delete=AsyncMock(),
        )
        conns = {"/conn/1": conn1, "/conn/2": conn2}
        w._conn_settings = lambda path: conns[path]

        count = await w._delete_connections_by_id("TestHotspot")
        assert count == 1
        conn1.delete.assert_called_once()
        conn2.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_matches_returns_zero(self, qapp):
        w = _make_worker(qapp)
        nm_settings_proxy = AsyncProxyMock(list_connections=AsyncMock(return_value=[]))
        w._nm_settings = _ProxyFactory(nm_settings_proxy)
        count = await w._delete_connections_by_id("nothing")
        assert count == 0

    @pytest.mark.asyncio
    async def test_case_insensitive_match(self, qapp):
        w = _make_worker(qapp)
        nm_settings_proxy = AsyncProxyMock(
            list_connections=AsyncMock(return_value=["/conn/1"])
        )
        w._nm_settings = _ProxyFactory(nm_settings_proxy)
        conn = AsyncProxyMock(
            get_settings=AsyncMock(
                return_value={
                    "connection": {"id": ("s", "MyHotspot")},
                }
            ),
            delete=AsyncMock(),
        )
        w._conn_settings = lambda path: conn
        count = await w._delete_connections_by_id("myhotspot")
        assert count == 1



class TestEnterpriseNetworkHandling:
    def test_eap_detected_via_rsn_flags(self):
        result = NetworkManagerWorker._determine_security_type(
            flags=1, wpa_flags=0, rsn_flags=0x200
        )
        assert result == SecurityType.WPA_EAP

    def test_eap_detected_via_wpa_flags(self):
        result = NetworkManagerWorker._determine_security_type(
            flags=1, wpa_flags=0x200, rsn_flags=0
        )
        assert result == SecurityType.WPA_EAP

    @pytest.mark.asyncio
    async def test_eap_network_scanned_and_displayed(self, qapp):
        w = _make_worker(qapp)
        w._get_all_ap_properties = AsyncMock(
            return_value={
                "ssid": b"eduroam",
                "strength": 65,
                "frequency": 5180,
                "hw_address": "AA:BB:CC:DD:EE:01",
                "max_bitrate": 300000,
                "flags": 1,
                "wpa_flags": 0,
                "rsn_flags": 0x200,
            }
        )
        # WPA_EAP is unsupported -> _parse_ap returns None
        network = await w._parse_ap("/ap/1", "", set())
        assert network is None

    def test_eap_connection_profile_returns_none(self, qapp):
        w = _make_worker(qapp)
        ap_props = {"flags": 1, "wpa_flags": 0, "rsn_flags": 0x200}
        result = w._build_connection_properties(
            "eduroam", "unused", "wlan0", 50, ap_props
        )
        assert result is None

    def test_wep_connection_returns_none(self, qapp):
        """WEP is unsupported — _build_connection_properties returns None."""
        w = _make_worker(qapp)
        ap_props = {"flags": 1, "wpa_flags": 0, "rsn_flags": 0}
        result = w._build_connection_properties(
            "LegacyNet", "wepkey", "wlan0", 50, ap_props
        )
        assert result is None



class TestIpToNmUint32:
    def test_loopback(self):
        assert NetworkManagerWorker._ip_to_nm_uint32("127.0.0.1") > 0

    def test_round_trip(self):
        original = "192.168.1.100"
        uint = NetworkManagerWorker._ip_to_nm_uint32(original)
        back = NetworkManagerWorker._nm_uint32_to_ip(uint)
        assert back == original


class TestMaskToPrefix:
    def test_class_c_mask(self):
        assert NetworkManagerWorker._mask_to_prefix("255.255.255.0") == 24

    def test_cidr_string(self):
        assert NetworkManagerWorker._mask_to_prefix("24") == 24

    def test_class_b_mask(self):
        assert NetworkManagerWorker._mask_to_prefix("255.255.0.0") == 16

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            NetworkManagerWorker._mask_to_prefix("33")



class TestAsyncShutdown:
    def test_sets_not_running(self, qapp):
        w = _make(qapp)
        _run(w._async_shutdown())
        assert w._running is False

    def test_clears_listener_tasks(self, qapp):
        w = _make(qapp)
        mock_task = MagicMock()
        mock_task.done.return_value = False
        w._listener_tasks = [mock_task]
        _run(w._async_shutdown())
        mock_task.cancel.assert_called_once()
        assert w._listener_tasks == []

    def test_cancels_debounce_handles(self, qapp):
        w = _make(qapp)
        state_h = MagicMock()
        scan_h = MagicMock()
        w._state_debounce_handle = state_h
        w._scan_debounce_handle = scan_h
        _run(w._async_shutdown())
        state_h.cancel.assert_called_once()
        scan_h.cancel.assert_called_once()
        assert w._state_debounce_handle is None
        assert w._scan_debounce_handle is None

    def test_clears_signal_proxies(self, qapp):
        w = _make(qapp)
        w._signal_nm = MagicMock()
        w._signal_wifi = MagicMock()
        _run(w._async_shutdown())
        assert w._signal_nm is None
        assert w._signal_wifi is None

    def test_clears_paths_and_caches(self, qapp):
        w = _make(qapp)
        w._iface_to_device_path = {"wlan0": "/path"}
        w._saved_cache = [MagicMock()]
        _run(w._async_shutdown())
        assert w._primary_wifi_path == ""
        assert w._primary_wired_path == ""
        assert w._iface_to_device_path == {}
        assert w._saved_cache == []



class TestEnsureSignalProxies:
    def test_creates_nm_proxy_when_none(self, qapp):
        w = _make(qapp)
        assert w._signal_nm is None
        w._ensure_signal_proxies()
        assert w._signal_nm is not None

    def test_creates_wifi_proxy_when_wifi_path_set(self, qapp):
        w = _make(qapp)
        w._ensure_signal_proxies()
        assert w._signal_wifi is not None

    def test_no_wifi_proxy_without_wifi_path(self, qapp):
        w = _make(qapp, wifi=False)
        w._ensure_signal_proxies()
        assert w._signal_wifi is None

    def test_idempotent_when_already_set(self, qapp):
        w = _make(qapp)
        sentinel_nm = MagicMock()
        sentinel_wifi = MagicMock()
        sentinel_wired = MagicMock()
        sentinel_settings = MagicMock()
        w._signal_nm = sentinel_nm
        w._signal_wifi = sentinel_wifi
        w._signal_wired = sentinel_wired
        w._signal_settings = sentinel_settings
        w._ensure_signal_proxies()
        assert w._signal_nm is sentinel_nm
        assert w._signal_wifi is sentinel_wifi
        assert w._signal_wired is sentinel_wired
        assert w._signal_settings is sentinel_settings



class TestDebounceState:
    def test_schedule_creates_handle(self, qapp):
        w = _make(qapp)
        loop = MagicMock()
        handle = MagicMock()
        loop.call_later.return_value = handle
        w._asyncio_loop = loop
        w._schedule_debounced_state_rebuild()
        loop.call_later.assert_called_once()
        assert w._state_debounce_handle is handle

    def test_schedule_cancels_previous(self, qapp):
        w = _make(qapp)
        old = MagicMock()
        w._state_debounce_handle = old
        loop = MagicMock()
        loop.call_later.return_value = MagicMock()
        w._asyncio_loop = loop
        w._schedule_debounced_state_rebuild()
        old.cancel.assert_called_once()

    def test_fire_state_rebuild_when_running(self, qapp):
        w = _make(qapp)
        w._state_debounce_handle = MagicMock()
        loop = MagicMock()
        # Close coroutines handed to create_task so they are not GC'd unawaited.
        loop.create_task.side_effect = lambda coro, **kw: coro.close() or MagicMock()
        w._asyncio_loop = loop
        w._fire_state_rebuild()
        assert w._state_debounce_handle is None
        loop.create_task.assert_called_once()

    def test_fire_state_rebuild_skipped_when_stopped(self, qapp):
        w = _make(qapp, running=False)
        w._state_debounce_handle = MagicMock()
        loop = MagicMock()
        w._asyncio_loop = loop
        w._fire_state_rebuild()
        loop.create_task.assert_not_called()


class TestDebounceScan:
    def test_schedule_creates_handle(self, qapp):
        w = _make(qapp)
        loop = MagicMock()
        handle = MagicMock()
        loop.call_later.return_value = handle
        w._asyncio_loop = loop
        w._schedule_debounced_scan()
        assert w._scan_debounce_handle is handle

    def test_fire_scan_rebuild_when_running(self, qapp):
        w = _make(qapp)
        w._scan_debounce_handle = MagicMock()
        loop = MagicMock()
        # Close coroutines handed to create_task so they are not GC'd unawaited.
        loop.create_task.side_effect = lambda coro, **kw: coro.close() or MagicMock()
        w._asyncio_loop = loop
        w._fire_scan_rebuild()
        assert w._scan_debounce_handle is None
        loop.create_task.assert_called_once()



class TestFallbackPoll:
    def test_not_running_returns_immediately(self, qapp):
        w = _make(qapp, running=False)
        with patch.object(w, "_async_get_current_state", new_callable=AsyncMock) as m:
            _run(w._async_fallback_poll())
        m.assert_not_called()

    def test_calls_state_and_connectivity(self, qapp):
        w = _make(qapp)
        w._async_get_current_state = AsyncMock()
        w._async_check_connectivity = AsyncMock()
        w._async_load_saved_networks = AsyncMock()
        _run(w._async_fallback_poll())
        w._async_get_current_state.assert_awaited_once()
        w._async_check_connectivity.assert_awaited_once()
        w._async_load_saved_networks.assert_awaited_once()



class TestEnforceBootMutualExclusion:
    def test_no_ethernet_returns_early(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=True)
        _wire(w, nm=nm)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        _run(w._enforce_boot_mutual_exclusion())
        # wireless_enabled.set_async should NOT be called
        assert (
            not hasattr(nm.wireless_enabled, "set_async")
            or not nm.wireless_enabled.set_async.called
        )

    def test_ethernet_active_wifi_on_disables_wifi(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=True)
        _wire(w, nm=nm)
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock()
        _wire(w, wifi_proxy=wifi)
        w._is_ethernet_connected = AsyncMock(return_value=True)
        w._wait_for_wifi_radio = AsyncMock(return_value=True)
        _run(w._enforce_boot_mutual_exclusion())
        nm.wireless_enabled.set_async.assert_awaited_once_with(False)
        assert w._is_hotspot_active is False

    def test_ethernet_active_wifi_off_no_action(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=False)
        _wire(w, nm=nm)
        w._is_ethernet_connected = AsyncMock(return_value=True)
        _run(w._enforce_boot_mutual_exclusion())
        nm.wireless_enabled.set_async.assert_not_awaited()

    def test_exception_is_non_fatal(self, qapp):
        w = _make(qapp)
        w._is_ethernet_connected = AsyncMock(side_effect=RuntimeError("boom"))
        _run(w._enforce_boot_mutual_exclusion())  # must not raise



class TestWaitForWifiRadio:
    def test_returns_true_when_already_matching(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=True)
        _wire(w, nm=nm)
        result = _run(w._wait_for_wifi_radio(True, timeout=1.0))
        assert result is True

    def test_returns_false_on_timeout(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=False)
        _wire(w, nm=nm)
        result = _run(w._wait_for_wifi_radio(True, timeout=0.5))
        assert result is False



class TestSetWifiEnabled:
    def test_disable_wifi_happy_path(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=True)
        _wire(w, nm=nm)
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock()
        _wire(w, wifi_proxy=wifi)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._wait_for_wifi_radio = AsyncMock(return_value=True)
        w._build_current_state = AsyncMock(return_value=NetworkState())

        received = []
        w.connection_result.connect(received.append)
        _run(w._async_set_wifi_enabled(False))

        nm.wireless_enabled.set_async.assert_awaited_once_with(False)
        assert len(received) == 1
        assert received[0].success is True
        assert w._is_hotspot_active is False

    def test_enable_wifi_disconnects_ethernet(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=False)
        _wire(w, nm=nm)
        w._is_ethernet_connected = AsyncMock(return_value=True)
        w._async_disconnect_ethernet = AsyncMock()
        w._wait_for_wifi_radio = AsyncMock(return_value=True)
        w._build_current_state = AsyncMock(return_value=NetworkState())

        _run(w._async_set_wifi_enabled(True))
        w._async_disconnect_ethernet.assert_awaited_once()
        nm.wireless_enabled.set_async.assert_awaited_once_with(True)

    def test_already_matching_skips_toggle(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=True)
        _wire(w, nm=nm)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._build_current_state = AsyncMock(return_value=NetworkState())

        _run(w._async_set_wifi_enabled(True))
        nm.wireless_enabled.set_async.assert_not_awaited()

    def test_no_bus_returns_silently(self, qapp):
        w = _make(qapp)
        w._system_bus = None
        _run(w._async_set_wifi_enabled(True))  # must not raise

    def test_exception_emits_error(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(
            wireless_enabled=AsyncMock(side_effect=RuntimeError("fail"))
        )
        w._nm = _ProxyFactory(nm)
        w._is_ethernet_connected = AsyncMock(return_value=False)

        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append((op, msg)))
        _run(w._async_set_wifi_enabled(True))
        assert len(errors) == 1
        assert errors[0][0] == "set_wifi_enabled"



class TestDisconnectEthernetAsync:
    def test_no_wired_path_noop(self, qapp):
        w = _make(qapp, wired=False)
        _run(w._async_disconnect_ethernet())  # must not raise

    def test_calls_disconnect(self, qapp):
        w = _make(qapp)
        wired = AsyncProxyMock()
        wired.disconnect = AsyncMock()
        _wire(w, wired_proxy=wired)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._deactivate_all_vlans = AsyncMock()
        _run(w._async_disconnect_ethernet())
        wired.disconnect.assert_awaited_once()
        w._deactivate_all_vlans.assert_awaited_once()


class TestConnectEthernetAsync:
    def test_no_wired_path_emits_error(self, qapp):
        w = _make(qapp, wired=False)
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append(op))
        _run(w._async_connect_ethernet())
        assert errors == ["connect_ethernet"]

    def test_happy_path(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=True)
        nm.activate_connection = AsyncMock()
        _wire(w, nm=nm)
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock()
        _wire(w, wifi_proxy=wifi)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._wait_for_wifi_radio = AsyncMock(return_value=True)
        w._build_current_state = AsyncMock(return_value=NetworkState())
        w._activate_saved_vlans = AsyncMock()
        w._is_hotspot_active = False

        results = []
        w.connection_result.connect(results.append)
        _run(w._async_connect_ethernet())

        nm.wireless_enabled.set_async.assert_awaited_once_with(False)
        nm.activate_connection.assert_awaited_once()
        assert len(results) == 1
        assert results[0].success is True

    def test_exception_emits_error_and_state(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=AsyncMock(side_effect=RuntimeError("x")))
        w._nm = _ProxyFactory(nm)
        w._build_current_state = AsyncMock(return_value=NetworkState())

        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append(op))
        _run(w._async_connect_ethernet())
        assert "connect_ethernet" in errors



class TestToggleHotspotOff:
    def test_disable_cleans_up_profiles(self, qapp):
        w = _make(qapp)
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock()
        _wire(w, wifi_proxy=wifi)
        nm = AsyncProxyMock(wireless_enabled=True)
        _wire(w, nm=nm)
        w._is_hotspot_active = True
        w._delete_connections_by_id = AsyncMock(return_value=1)
        w._build_current_state = AsyncMock(return_value=NetworkState())

        results = []
        w.connection_result.connect(results.append)
        _run(w._async_toggle_hotspot(False))

        assert w._is_hotspot_active is False
        wifi.disconnect.assert_awaited_once()
        w._delete_connections_by_id.assert_awaited()
        nm.wireless_enabled.set_async.assert_awaited_once_with(False)
        assert results[0].success is True

    def test_disable_skips_radio_off_if_not_was_active(self, qapp):
        w = _make(qapp)
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock()
        _wire(w, wifi_proxy=wifi)
        nm = AsyncProxyMock(wireless_enabled=True)
        _wire(w, nm=nm)
        w._is_hotspot_active = False  # was NOT active
        w._delete_connections_by_id = AsyncMock(return_value=0)
        w._build_current_state = AsyncMock(return_value=NetworkState())

        _run(w._async_toggle_hotspot(False))
        nm.wireless_enabled.set_async.assert_not_awaited()

    def test_exception_emits_failure(self, qapp):
        w = _make(qapp)
        w._is_hotspot_active = True
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock(side_effect=RuntimeError("x"))
        _wire(w, wifi_proxy=wifi)
        w._delete_connections_by_id = AsyncMock(side_effect=RuntimeError("y"))

        results = []
        w.connection_result.connect(results.append)
        _run(w._async_toggle_hotspot(False))
        assert results[0].success is False


class TestToggleHotspotOn:
    def test_enable_delegates_to_create_and_activate(self, qapp):
        w = _make(qapp)
        w._async_create_and_activate_hotspot = AsyncMock()
        _run(w._async_toggle_hotspot(True))
        w._async_create_and_activate_hotspot.assert_awaited_once_with(
            w._hotspot_config.ssid,
            w._hotspot_config.password,
        )



class TestCreateAndActivateHotspot:
    def test_happy_path(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=True)
        nm.activate_connection = AsyncMock()
        _wire(w, nm=nm)
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock()
        _wire(w, wifi_proxy=wifi)
        settings = AsyncProxyMock()
        settings.add_connection = AsyncMock(return_value="/path/hotspot")
        _wire(w, settings=settings)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._delete_all_ap_mode_connections = AsyncMock(return_value=0)
        w._delete_connections_by_id = AsyncMock(return_value=0)
        w._build_current_state = AsyncMock(return_value=NetworkState())

        results = []
        w.connection_result.connect(results.append)
        hotspot_info = []
        w.hotspot_info_ready.connect(lambda s, p, sec: hotspot_info.append(s))

        _run(w._async_create_and_activate_hotspot("TestAP", "pass1234"))

        settings.add_connection.assert_awaited_once()
        conn_props = settings.add_connection.call_args[0][0]
        assert conn_props["connection"]["interface-name"][1] == "wlan0"
        assert conn_props["connection"]["autoconnect"] == ("b", False)
        nm.activate_connection.assert_awaited_once_with(
            "/path/hotspot",
            "/org/freedesktop/NetworkManager/Devices/2",
            "/",
        )
        assert w._is_hotspot_active is True
        assert len(results) == 1
        assert results[0].success is True
        assert len(hotspot_info) == 1

    def test_exception_emits_failure(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=AsyncMock(side_effect=RuntimeError("x")))
        w._nm = _ProxyFactory(nm)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._delete_all_ap_mode_connections = AsyncMock(return_value=0)
        w._delete_connections_by_id = AsyncMock()

        results = []
        w.connection_result.connect(results.append)
        _run(w._async_create_and_activate_hotspot("TestAP", "pass"))
        assert results[0].success is False
        assert w._is_hotspot_active is False



class TestHotspotActivation:
    def test_activate_connection_passes_wifi_device_path(self, qapp):
        """activate_connection must receive the wifi device path, not be called bare."""
        w = _make(qapp)
        w._primary_wifi_path = "/org/freedesktop/NetworkManager/Devices/4"
        w._primary_wifi_iface = "wlan0"
        nm = AsyncProxyMock(wireless_enabled=True)
        nm.activate_connection = AsyncMock(
            return_value="/org/freedesktop/NetworkManager/ActiveConnections/5"
        )
        _wire(w, nm=nm)
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock()
        _wire(w, wifi_proxy=wifi)
        settings = AsyncProxyMock()
        settings.add_connection = AsyncMock(return_value="/path/hotspot")
        _wire(w, settings=settings)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._delete_all_ap_mode_connections = AsyncMock(return_value=0)
        w._delete_connections_by_id = AsyncMock(return_value=0)
        w._build_current_state = AsyncMock(return_value=NetworkState())

        _run(w._async_create_and_activate_hotspot("TestSSID", "testpass", "wpa-psk"))

        args = nm.activate_connection.call_args[0]
        assert args[1] == "/org/freedesktop/NetworkManager/Devices/4"
        assert args[2] == "/"

    def test_interface_name_uses_detected_iface(self, qapp):
        """interface-name in connection profile uses _primary_wifi_iface, not hardcoded wlan0."""
        w = _make(qapp)
        w._primary_wifi_path = "/org/freedesktop/NetworkManager/Devices/4"
        w._primary_wifi_iface = "wlan1"
        nm = AsyncProxyMock(wireless_enabled=True)
        nm.activate_connection = AsyncMock(return_value="/path/ac")
        _wire(w, nm=nm)
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock()
        _wire(w, wifi_proxy=wifi)
        settings = AsyncProxyMock()
        settings.add_connection = AsyncMock(return_value="/path/hotspot")
        _wire(w, settings=settings)
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._delete_all_ap_mode_connections = AsyncMock(return_value=0)
        w._delete_connections_by_id = AsyncMock(return_value=0)
        w._build_current_state = AsyncMock(return_value=NetworkState())

        _run(w._async_create_and_activate_hotspot("TestSSID", "testpass", "wpa-psk"))

        conn_props = settings.add_connection.call_args[0][0]
        iface_name = conn_props["connection"]["interface-name"][1]
        assert iface_name == "wlan1"



class TestUpdateHotspotConfig:
    def test_inactive_updates_config_without_reactivating(self, qapp):
        w = _make(qapp)
        w._is_hotspot_active = False
        w._delete_all_ap_mode_connections = AsyncMock(return_value=0)
        w._delete_connections_by_id = AsyncMock(return_value=0)

        results = []
        w.connection_result.connect(results.append)
        hotspot_info = []
        w.hotspot_info_ready.connect(lambda s, p, sec: hotspot_info.append(s))

        _run(w._async_update_hotspot_config("OldSSID", "NewSSID", "newpwd", "wpa-psk"))

        assert w._hotspot_config.ssid == "NewSSID"
        assert w._hotspot_config.password == "newpwd"
        assert results[0].success is True
        assert hotspot_info == ["NewSSID"]

    def test_active_disconnects_and_reactivates(self, qapp):
        w = _make(qapp)
        w._is_hotspot_active = True
        wifi = AsyncProxyMock()
        wifi.disconnect = AsyncMock()
        _wire(w, wifi_proxy=wifi)
        w._delete_all_ap_mode_connections = AsyncMock(return_value=0)
        w._delete_connections_by_id = AsyncMock(return_value=1)
        w._async_create_and_activate_hotspot = AsyncMock()

        _run(w._async_update_hotspot_config("OldSSID", "NewSSID", "pwd", "wpa-psk"))
        wifi.disconnect.assert_awaited_once()
        w._async_create_and_activate_hotspot.assert_awaited_once()

    def test_different_ssid_deletes_new_ssid_profiles(self, qapp):
        w = _make(qapp)
        w._is_hotspot_active = False
        w._delete_all_ap_mode_connections = AsyncMock(return_value=0)
        w._delete_connections_by_id = AsyncMock(return_value=0)
        _run(w._async_update_hotspot_config("OldSSID", "NewSSID", "pwd", "wpa-psk"))
        # Should delete both old and new connection ids
        assert w._delete_connections_by_id.await_count == 2

    def test_same_ssid_only_deletes_once(self, qapp):
        w = _make(qapp)
        w._is_hotspot_active = False
        w._delete_all_ap_mode_connections = AsyncMock(return_value=0)
        w._delete_connections_by_id = AsyncMock(return_value=0)
        _run(w._async_update_hotspot_config("Same", "Same", "pwd", "wpa-psk"))
        assert w._delete_connections_by_id.await_count == 1

    def test_exception_emits_failure(self, qapp):
        w = _make(qapp)
        w._is_hotspot_active = False
        w._delete_all_ap_mode_connections = AsyncMock(return_value=0)
        w._delete_connections_by_id = AsyncMock(side_effect=RuntimeError("x"))
        results = []
        w.connection_result.connect(results.append)
        _run(w._async_update_hotspot_config("A", "B", "C", "wpa-psk"))
        assert results[0].success is False



class TestUpdateWifiStaticIp:
    def test_not_found_emits_error(self, qapp):
        w = _make(qapp)
        w._get_connection_path = AsyncMock(return_value=None)
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append(op))
        _run(
            w._async_update_wifi_static_ip(
                "NoNet", "10.0.0.1", "255.255.255.0", "10.0.0.1", "", ""
            )
        )
        assert errors == ["wifi_static_ip"]

    def test_happy_path(self, qapp):
        w = _make(qapp)
        w._get_connection_path = AsyncMock(return_value="/path/conn1")
        mock_cs = AsyncProxyMock()
        mock_cs.get_settings = AsyncMock(return_value={"ipv4": {}})
        mock_cs.update = AsyncMock()
        w._conn_settings = MagicMock(return_value=mock_cs)
        w._merge_wifi_secrets = AsyncMock()
        w._reconnect_wifi_profile = AsyncMock()
        w._build_current_state = AsyncMock(return_value=NetworkState())

        results = []
        w.connection_result.connect(results.append)
        reconnects = []
        w.reconnect_complete.connect(lambda: reconnects.append(True))

        _run(
            w._async_update_wifi_static_ip(
                "HomeNet", "10.0.0.50", "255.255.255.0", "10.0.0.1", "8.8.8.8", ""
            )
        )
        mock_cs.update.assert_awaited_once()
        w._reconnect_wifi_profile.assert_awaited_once_with("HomeNet")
        assert results[0].success is True
        assert len(reconnects) == 1

    def test_exception_emits_error(self, qapp):
        w = _make(qapp)
        w._get_connection_path = AsyncMock(return_value="/path/x")
        w._conn_settings = MagicMock(side_effect=RuntimeError("fail"))
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append(op))
        _run(
            w._async_update_wifi_static_ip("X", "10.0.0.1", "255.255.255.0", "", "", "")
        )
        assert "wifi_static_ip" in errors


class TestResetWifiToDhcp:
    def test_not_found_emits_error(self, qapp):
        w = _make(qapp)
        w._get_connection_path = AsyncMock(return_value=None)
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append(op))
        _run(w._async_reset_wifi_to_dhcp("NoNet"))
        assert errors == ["wifi_dhcp"]

    def test_happy_path(self, qapp):
        w = _make(qapp)
        w._get_connection_path = AsyncMock(return_value="/path/c")
        mock_cs = AsyncProxyMock()
        mock_cs.get_settings = AsyncMock(
            return_value={"ipv4": {"method": ("s", "manual")}}
        )
        mock_cs.update = AsyncMock()
        w._conn_settings = MagicMock(return_value=mock_cs)
        w._merge_wifi_secrets = AsyncMock()
        w._reconnect_wifi_profile = AsyncMock()
        w._build_current_state = AsyncMock(return_value=NetworkState())

        results = []
        w.connection_result.connect(results.append)
        _run(w._async_reset_wifi_to_dhcp("HomeNet"))
        mock_cs.update.assert_awaited_once()
        assert results[0].success is True



class TestCreateVlan:
    def test_no_wired_device_emits_error(self, qapp):
        w = _make(qapp, wired=False)
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append(op))
        _run(w._async_create_vlan(100, "10.0.0.1", "255.255.255.0", "10.0.0.1", "", ""))
        assert errors == ["create_vlan"]

    def test_static_ip_happy_path(self, qapp):
        w = _make(qapp)
        nm = AsyncProxyMock(wireless_enabled=False)
        nm.activate_connection = AsyncMock()
        _wire(w, nm=nm)
        settings = AsyncProxyMock()
        settings.add_connection = AsyncMock(return_value="/path/vlan")
        settings.list_connections = AsyncMock(return_value=[])
        _wire(w, settings=settings)
        w._is_ethernet_connected = AsyncMock(return_value=True)
        w._deactivate_connection_by_id = AsyncMock(return_value=False)
        w._delete_all_connections_by_id = AsyncMock()
        w._build_current_state = AsyncMock(return_value=NetworkState())

        results = []
        w.connection_result.connect(results.append)
        _run(w._async_create_vlan(100, "10.0.0.1", "255.255.255.0", "10.0.0.1", "", ""))
        nm.activate_connection.assert_awaited_once()
        assert any(r.success for r in results)


class TestDeleteVlan:
    def test_happy_path(self, qapp):
        w = _make(qapp)
        w._deactivate_connection_by_id = AsyncMock(return_value=True)
        w._delete_all_connections_by_id = AsyncMock()
        w._build_current_state = AsyncMock(return_value=NetworkState())

        results = []
        w.connection_result.connect(results.append)
        _run(w._async_delete_vlan(100))
        w._delete_all_connections_by_id.assert_awaited_once()
        assert results[0].success is True

    def test_exception_emits_error(self, qapp):
        w = _make(qapp)
        w._delete_all_connections_by_id = AsyncMock(side_effect=RuntimeError("x"))
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append(op))
        _run(w._async_delete_vlan(99))
        assert "delete_vlan" in errors



class TestStartSignalListeners:
    def test_creates_seven_listener_tasks(self, qapp):
        w = _make(qapp)
        loop = asyncio.new_event_loop()
        w._asyncio_loop = loop
        w._ensure_signal_proxies = MagicMock()

        async def _test():
            # Mock the listener coroutines to complete immediately
            w._listen_nm_state_changed = AsyncMock()
            w._listen_ap_added = AsyncMock()
            w._listen_ap_removed = AsyncMock()
            w._listen_wired_state_changed = AsyncMock()
            w._listen_wifi_state_changed = AsyncMock()
            w._listen_settings_new_connection = AsyncMock()
            w._listen_settings_connection_removed = AsyncMock()
            # _resilient_listener wraps them — mock it to just return
            w._resilient_listener = AsyncMock()
            w._track_task = MagicMock()
            await w._start_signal_listeners()

        loop.run_until_complete(_test())
        assert w._ensure_signal_proxies.called
        # 7 listeners -> 7 tasks
        assert len(w._listener_tasks) == 7
        loop.close()



class TestAsyncInitializeFull:
    def test_happy_path_full_init(self, qapp):
        w = _make(qapp, running=False)
        w._detect_interfaces = AsyncMock()
        w._enforce_boot_mutual_exclusion = AsyncMock()
        w._is_ethernet_connected = AsyncMock(return_value=False)
        w._activate_saved_vlans = AsyncMock()
        w._start_signal_listeners = AsyncMock()
        wifi = AsyncProxyMock()
        wifi.request_scan = AsyncMock()
        _wire(w, wifi_proxy=wifi)

        init_signals = []
        w.initialized.connect(lambda: init_signals.append(True))
        hotspot_info = []
        w.hotspot_info_ready.connect(lambda s, p, sec: hotspot_info.append(s))

        _run(w._async_initialize())

        assert w._running is True
        w._detect_interfaces.assert_awaited_once()
        w._enforce_boot_mutual_exclusion.assert_awaited_once()
        w._start_signal_listeners.assert_awaited_once()
        assert len(init_signals) == 1
        assert len(hotspot_info) == 1

    def test_no_bus_emits_error(self, qapp):
        w = _make(qapp, running=False)
        w._system_bus = None
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append(op))
        _run(w._async_initialize())
        assert errors == ["initialize"]

    def test_exception_emits_error_and_still_fires_initialized(self, qapp):
        w = _make(qapp, running=False)
        w._detect_interfaces = AsyncMock(side_effect=RuntimeError("boom"))
        errors = []
        w.error_occurred.connect(lambda op, msg: errors.append(op))
        inits = []
        w.initialized.connect(lambda: inits.append(True))
        _run(w._async_initialize())
        assert errors == ["initialize"]
        assert len(inits) == 1



class TestExceptionHandlerBranches:
    """Exercise exception and early-return branches in low-level scan helpers."""

    def test_get_current_ssid_exception_returns_empty(self, qapp):
        """_get_current_ssid() swallows exceptions and returns empty string."""
        w = _make_worker(qapp)
        nm = AsyncProxyMock()
        nm.active_connections = AsyncMock(side_effect=RuntimeError("dbus down"))
        _wire(w, nm=nm)
        result = _run(w._get_current_ssid())
        assert result == ""

    def test_get_current_ip_empty_primary_returns_empty(self, qapp):
        """_get_current_ip() returns empty when primary_connection is '/'."""
        w = _make_worker(qapp)
        nm = AsyncProxyMock(primary_connection="/")
        _wire(w, nm=nm)
        result = _run(w._get_current_ip())
        assert result == ""

    def test_get_ip_by_interface_device_not_found_returns_empty(self, qapp):
        """_get_ip_by_interface() returns '' when no device matches interface."""
        w = _make_worker(qapp)
        nm = AsyncProxyMock()
        nm.get_devices = AsyncMock(return_value=[])
        generic = AsyncProxyMock()
        generic.interface = AsyncMock(return_value="eth1")
        _wire(w, nm=nm)
        w._generic = lambda _path: generic
        result = _run(w._get_ip_by_interface("wlan99"))
        assert result == ""

    def test_get_ip_by_interface_no_ip4_config_returns_empty(self, qapp):
        """_get_ip_by_interface() returns '' when ip4_config is '/'."""
        w = _make_worker(qapp)
        nm = AsyncProxyMock()
        nm.get_devices = AsyncMock(return_value=["/dev/wlan0"])
        generic = AsyncProxyMock()
        generic.interface = AsyncMock(return_value="wlan0")
        generic.ip4_config = AsyncMock(return_value="/")
        _wire(w, nm=nm)
        w._generic = lambda _path: generic
        result = _run(w._get_ip_by_interface("wlan0"))
        assert result == ""

    def test_get_ip_by_interface_exception_returns_empty(self, qapp):
        """_get_ip_by_interface() swallows exceptions and returns empty string."""
        w = _make_worker(qapp)
        nm = AsyncProxyMock()
        nm.get_devices = AsyncMock(side_effect=RuntimeError("bus error"))
        _wire(w, nm=nm)
        result = _run(w._get_ip_by_interface("wlan0"))
        assert result == ""

    def test_scan_ap_exception_skips_ap(self, qapp):
        """_async_scan_networks() skips APs that raise during parse."""
        w = _make_worker(qapp)
        nm = AsyncProxyMock()
        nm.wireless_enabled = AsyncMock(return_value=True)
        wifi_proxy = AsyncProxyMock()
        wifi_proxy.request_scan = AsyncMock(return_value=None)
        wifi_proxy.last_scan = AsyncMock(return_value=1)
        wifi_proxy.get_all_access_points = AsyncMock(
            return_value=["/ap/bad", "/ap/good"]
        )
        _wire(w, nm=nm, wifi_proxy=wifi_proxy)
        w._get_current_ssid = AsyncMock(return_value="")
        w._get_saved_ssid_names_cached = AsyncMock(return_value=[])
        # First AP raises, second returns None (parsed as no-result)
        w._parse_ap = AsyncMock(side_effect=[RuntimeError("bad ap"), None])
        scanned = []
        w.networks_scanned.connect(lambda nets: scanned.extend(nets))
        _run(w._async_scan_networks())
        # No crash, empty result (second AP returned None)
        assert isinstance(scanned, list)
        assert scanned == []



class TestConnectNetworkImplException:
    """_connect_network_impl returns a failure result when activate_connection raises."""

    def test_activate_connection_exception_returns_failure(self, qapp):
        w = _make_worker(qapp)
        nm = AsyncProxyMock(wireless_enabled=True)
        nm.activate_connection = AsyncMock(side_effect=RuntimeError("D-Bus error"))
        _wire(w, nm=nm)
        w._get_connection_path = AsyncMock(return_value="/conn/1")
        w._find_connection_path_direct = AsyncMock(return_value=None)
        result = _run(w._connect_network_impl("HomeNet"))
        assert result.success is False
        assert result.error_code == "connect_failed"



class TestWaitForConnection:
    """_wait_for_connection covers timeout and consecutive-empty early-exit."""

    def test_wait_for_connection_consecutive_empty_stops_early(self, qapp):
        """Three consecutive empty SSID polls triggers early False return."""
        w = _make_worker(qapp)
        # Return empty SSID three times → consecutive_empty hits 3
        w._get_current_ssid = AsyncMock(return_value="")
        w._get_current_ip = AsyncMock(return_value="")
        result = _run(w._wait_for_connection("HomeNet", timeout=10.0))
        assert result is False

    def test_wait_for_connection_inner_exception_continues(self, qapp):
        """Exceptions inside the loop are silently swallowed (pass block)."""
        w = _make_worker(qapp)
        # Raise on first call, then return empty (hits consecutive_empty path)
        w._get_current_ssid = AsyncMock(
            side_effect=[RuntimeError("transient"), "", "", ""]
        )
        w._get_current_ip = AsyncMock(return_value="")
        result = _run(w._wait_for_connection("HomeNet", timeout=10.0))
        assert result is False



class TestGetSavedNetworksHandlesMalformedEntry:
    """_get_saved_networks_impl skips entries that raise during parse."""

    def test_malformed_entry_skipped_returns_valid_entries(self, qapp):
        """A connection that raises during parse is skipped; valid ones included."""
        w = _make_worker(qapp)

        good_settings = {
            "connection": {
                "type": (None, "802-11-wireless"),
                "uuid": (None, "uuid-1"),
                "autoconnect-priority": (None, 50),
                "timestamp": (None, 0),
            },
            "802-11-wireless": {
                "ssid": (None, b"GoodNet"),
                "mode": (None, "infrastructure"),
                "security": (None, ""),
            },
        }

        bad_settings_proxy = AsyncProxyMock()
        bad_settings_proxy.get_settings = AsyncMock(
            side_effect=RuntimeError("malformed")
        )
        good_settings_proxy = AsyncProxyMock()
        good_settings_proxy.get_settings = AsyncMock(return_value=good_settings)

        settings_manager = AsyncProxyMock()
        settings_manager.list_connections = AsyncMock(
            return_value=["/bad/conn", "/good/conn"]
        )
        _wire(w, settings=settings_manager)
        w._build_signal_map = AsyncMock(return_value={})

        call_map = {
            "/bad/conn": bad_settings_proxy,
            "/good/conn": good_settings_proxy,
        }
        w._conn_settings = lambda path: call_map[path]

        result = _run(w._get_saved_networks_impl())
        assert len(result) == 1
        assert result[0].ssid == "GoodNet"
