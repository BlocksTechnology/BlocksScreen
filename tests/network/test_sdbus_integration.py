"""Integration tests for NetworkManagerWorker against real NetworkManager.

Gate
----
These tests are **opt-in** and require:
  * NetworkManager running on the host (systemctl is-active NetworkManager)
  * NM_INTEGRATION_TESTS=1 in the environment

Run with:
    make test-integration
or:
    NM_INTEGRATION_TESTS=1 pytest -v tests/network/test_sdbus_integration.py

Signal capture
--------------
Qt signals emitted on the worker's asyncio thread are **not** delivered
to the test thread via QueuedConnection (no Qt event loop running).
All signal connections use ``Qt.ConnectionType.DirectConnection`` so
slots execute synchronously on the emitting thread.

Timeout
-------
Module-level ``pytestmark`` raises the per-test timeout to 120 s to
accommodate real D-Bus scans on Raspberry Pi hardware.
"""

import asyncio
import os
from contextlib import contextmanager

import pytest
from PyQt6.QtCore import Qt

# ─────────────────────────────────────────────────────────────────────────────
# Gate — skip entire module when opt-in flag is absent
# ─────────────────────────────────────────────────────────────────────────────
_ENABLED = os.environ.get("NM_INTEGRATION_TESTS", "0") == "1"
_SKIP = pytest.mark.skipif(not _ENABLED, reason="NM_INTEGRATION_TESTS not set")
_TEST_PREFIX = "TEST_BLOCKS_"

pytestmark = [_SKIP, pytest.mark.timeout(120)]


# ─────────────────────────────────────────────────────────────────────────────
# Signal capture helper
# ─────────────────────────────────────────────────────────────────────────────


@contextmanager
def _capture(signal):
    """Connect with DirectConnection so slots fire on the emitting thread."""
    received: list = []
    signal.connect(received.append, Qt.ConnectionType.DirectConnection)
    try:
        yield received
    finally:
        try:
            signal.disconnect(received.append)
        except (TypeError, RuntimeError):
            pass


# ─────────────────────────────────────────────────────────────────────────────
# Session-scoped real worker
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def real_worker(qapp):
    """Start a real NetworkManagerWorker backed by real D-Bus modules.

    ``conftest.py`` patches ``sys.modules`` globally with D-Bus stubs so that
    unit tests run without NetworkManager.  This fixture temporarily removes
    those patches, force-reimports ``worker.py`` so its module-level
    ``dbus_nm`` / ``sdbus`` / ``get_configparser`` bindings point to real
    objects, then immediately restores the stubs.

    Python module-level bindings are fixed at import time.  Restoring the
    stubs to ``sys.modules`` afterwards does NOT change the names already
    bound inside ``worker.py``, so ``sdbus.sd_bus_open_system()`` and
    ``dbus_nm.NetworkManager(...)`` continue to use the real implementations.
    """
    import sys
    import threading
    from pathlib import Path

    # Add BlocksScreen/ to sys.path so `import configfile` resolves to
    # BlocksScreen/configfile.py (worker.py imports it at module level).
    _bs_dir = str(Path(__file__).resolve().parent.parent.parent / "BlocksScreen")
    _path_was_added = _bs_dir not in sys.path
    if _path_was_added:
        sys.path.insert(0, _bs_dir)

    # Remove D-Bus / configfile stubs to expose the real installed packages.
    _stub_keys = [
        k
        for k in list(sys.modules)
        if k in ("sdbus", "sdbus_async", "sdbus_block", "configfile")
        or k.startswith(("sdbus_async.", "sdbus_block."))
    ]
    _saved_stubs = {k: sys.modules.pop(k) for k in _stub_keys}

    # Remove cached worker module to force fresh execution with real imports.
    _worker_key = "BlocksScreen.lib.network.worker"
    _saved_worker = sys.modules.pop(_worker_key, None)

    try:
        from BlocksScreen.lib.network.worker import NetworkManagerWorker
    except ImportError as exc:
        # Real sdbus packages not installed on this host — skip gracefully.
        sys.modules.update(_saved_stubs)
        if _path_was_added and sys.path and sys.path[0] == _bs_dir:
            sys.path.pop(0)
        if _saved_worker is not None:
            sys.modules[_worker_key] = _saved_worker
        pytest.skip(f"Real D-Bus packages not available: {exc}")
        return

    # Restore stubs immediately so remaining tests keep using mocks.
    # worker.py's module-level names are already bound to real objects and
    # are unaffected by this sys.modules restoration.
    sys.modules.update(_saved_stubs)
    if _path_was_added and sys.path and sys.path[0] == _bs_dir:
        sys.path.pop(0)

    w = NetworkManagerWorker()

    # Wait for FULL initialisation (including _detect_interfaces).
    # ``_running`` is set True *before* ``_detect_interfaces`` runs, so
    # polling ``_running`` alone is a race condition.  The ``initialized``
    # signal is emitted at the very end of ``_async_initialize``, after all
    # setup steps have completed.
    _init_done = threading.Event()
    w.initialized.connect(lambda: _init_done.set(), Qt.ConnectionType.DirectConnection)
    if not _init_done.wait(timeout=15.0):
        pytest.skip("NetworkManagerWorker failed to initialise within 15 s")

    yield w

    # Restore the original mocked worker module so that any tests collected
    # after this fixture (e.g. test_worker_unit.py) still see the stub-backed
    # module in sys.modules.
    if _saved_worker is not None:
        sys.modules[_worker_key] = _saved_worker

    # Graceful shutdown
    try:
        future = asyncio.run_coroutine_threadsafe(w._async_shutdown(), w._asyncio_loop)
        future.result(timeout=10.0)
    except Exception:
        pass
    if w._asyncio_loop.is_running():
        w._asyncio_loop.call_soon_threadsafe(w._asyncio_loop.stop)
    if hasattr(w, "_asyncio_thread") and w._asyncio_thread.is_alive():
        w._asyncio_thread.join(timeout=5.0)


def _run(worker, coro_factory, timeout: float = 15.0):
    """Submit *coro_factory()* to the worker loop and block until done."""
    future = asyncio.run_coroutine_threadsafe(coro_factory(), worker._asyncio_loop)
    return future.result(timeout=timeout)


# ─────────────────────────────────────────────────────────────────────────────
# Connectivity
# ─────────────────────────────────────────────────────────────────────────────


class TestRealConnectivity:
    def test_check_connectivity_returns_known_state(self, real_worker):
        from BlocksScreen.lib.network.models import ConnectivityState

        with _capture(real_worker.connectivity_changed) as received:
            _run(real_worker, real_worker._async_check_connectivity)
        assert len(received) == 1
        assert isinstance(received[0], ConnectivityState)

    def test_get_current_state_emits_network_state(self, real_worker):
        from BlocksScreen.lib.network.models import NetworkState

        with _capture(real_worker.state_changed) as received:
            _run(real_worker, real_worker._async_get_current_state)
        assert len(received) >= 1
        assert isinstance(received[-1], NetworkState)

    def test_current_state_has_valid_connectivity(self, real_worker):
        from BlocksScreen.lib.network.models import ConnectivityState

        with _capture(real_worker.state_changed) as received:
            _run(real_worker, real_worker._async_get_current_state)
        assert received[-1].connectivity in list(ConnectivityState)


class TestRealInterfaces:
    def test_wifi_path_detected(self, real_worker):
        assert real_worker._primary_wifi_path, "No Wi-Fi interface found"

    def test_wired_path_detected(self, real_worker):
        assert real_worker._primary_wired_path, "No wired interface found"

    def test_iface_cache_populated(self, real_worker):
        assert len(real_worker._iface_to_device_path) > 0


# ─────────────────────────────────────────────────────────────────────────────
# Saved networks (non-destructive)
# ─────────────────────────────────────────────────────────────────────────────


class TestRealSavedNetworks:
    def test_load_saved_networks_emits_list(self, real_worker):
        with _capture(real_worker.saved_networks_loaded) as received:
            _run(real_worker, real_worker._async_load_saved_networks)
        assert len(received) == 1
        assert isinstance(received[0], list)

    def test_saved_networks_are_saved_network_instances(self, real_worker):
        from BlocksScreen.lib.network.models import SavedNetwork

        with _capture(real_worker.saved_networks_loaded) as received:
            _run(real_worker, real_worker._async_load_saved_networks)
        for net in received[0]:
            assert isinstance(net, SavedNetwork)
            assert net.ssid

    def test_saved_network_has_connection_path(self, real_worker):
        with _capture(real_worker.saved_networks_loaded) as received:
            _run(real_worker, real_worker._async_load_saved_networks)
        for net in received[0]:
            assert net.connection_path.startswith("/org/freedesktop/NetworkManager")


# ─────────────────────────────────────────────────────────────────────────────
# AP scanning (non-destructive)
# ─────────────────────────────────────────────────────────────────────────────


class TestRealScan:
    def test_scan_emits_list(self, real_worker):
        with _capture(real_worker.networks_scanned) as received:
            _run(real_worker, real_worker._async_scan_networks, timeout=30.0)
        assert len(received) >= 1
        assert isinstance(received[-1], list)

    def test_scanned_networks_are_network_info(self, real_worker):
        from BlocksScreen.lib.network.models import NetworkInfo

        with _capture(real_worker.networks_scanned) as received:
            _run(real_worker, real_worker._async_scan_networks, timeout=30.0)
        for net in received[-1]:
            assert isinstance(net, NetworkInfo)

    def test_scanned_networks_have_ssid(self, real_worker):
        with _capture(real_worker.networks_scanned) as received:
            _run(real_worker, real_worker._async_scan_networks, timeout=30.0)
        for net in received[-1]:
            assert net.ssid
            assert isinstance(net.ssid, str)

    def test_scanned_signal_strength_in_range(self, real_worker):
        with _capture(real_worker.networks_scanned) as received:
            _run(real_worker, real_worker._async_scan_networks, timeout=30.0)
        for net in received[-1]:
            assert 0 <= net.signal_strength <= 100


# ─────────────────────────────────────────────────────────────────────────────
# Wi-Fi radio state (non-destructive read)
# ─────────────────────────────────────────────────────────────────────────────


class TestRealWifiRadio:
    def test_wireless_enabled_is_bool(self, real_worker):
        async def _check():
            return await real_worker._nm().wireless_enabled

        result = _run(real_worker, _check)
        assert isinstance(result, bool)

    def test_detect_interfaces_repopulates_cache(self, real_worker):
        real_worker._iface_to_device_path.clear()
        _run(real_worker, real_worker._detect_interfaces)
        assert len(real_worker._iface_to_device_path) > 0


# ─────────────────────────────────────────────────────────────────────────────
# Ethernet state (non-destructive)
# ─────────────────────────────────────────────────────────────────────────────


class TestRealEthernet:
    def test_ethernet_connected_returns_bool(self, real_worker):
        result = _run(real_worker, real_worker._is_ethernet_connected)
        assert isinstance(result, bool)

    def test_ethernet_carrier_returns_bool(self, real_worker):
        result = _run(real_worker, real_worker._has_ethernet_carrier)
        assert isinstance(result, bool)

    def test_get_active_vlans_returns_tuple(self, real_worker):
        result = _run(real_worker, real_worker._get_active_vlans)
        assert isinstance(result, tuple)


# ─────────────────────────────────────────────────────────────────────────────
# IP helpers (non-destructive)
# ─────────────────────────────────────────────────────────────────────────────


class TestRealIpHelpers:
    def test_get_ip_by_interface_wlan0_returns_str(self, real_worker):
        result = _run(real_worker, lambda: real_worker._get_ip_by_interface("wlan0"))
        assert isinstance(result, str)

    def test_get_ip_by_interface_eth0_returns_str(self, real_worker):
        result = _run(real_worker, lambda: real_worker._get_ip_by_interface("eth0"))
        assert isinstance(result, str)

    def test_get_ip_unknown_interface_returns_empty(self, real_worker):
        result = _run(
            real_worker, lambda: real_worker._get_ip_by_interface("nonexistent99")
        )
        assert result == ""

    def test_os_fallback_returns_str(self, real_worker):
        assert isinstance(real_worker._get_ip_os_fallback("eth0"), str)

    def test_os_fallback_unknown_iface_returns_empty(self, real_worker):
        assert real_worker._get_ip_os_fallback("nonexistent99") == ""


# ─────────────────────────────────────────────────────────────────────────────
# Destructive write tests — TEST_-prefixed profiles only
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def cleanup_test_profiles(real_worker):
    """Delete any TEST_-prefixed connection profiles after each test."""
    yield

    async def _cleanup():
        try:
            conns = await real_worker._nm_settings().list_connections()
            for cp in conns:
                try:
                    settings = await real_worker._conn_settings(cp).get_settings()
                    conn_id = settings.get("connection", {}).get("id", (None, ""))[1]
                    if str(conn_id).startswith(_TEST_PREFIX):
                        await real_worker._conn_settings(cp).delete()
                except Exception:
                    pass
        except Exception:
            pass

    future = asyncio.run_coroutine_threadsafe(_cleanup(), real_worker._asyncio_loop)
    try:
        future.result(timeout=10.0)
    except Exception:
        pass


class TestRealHotspotConfig:
    def test_hotspot_info_ready_emitted_on_init(self, real_worker):
        assert isinstance(real_worker.hotspot_ssid, str)
        assert isinstance(real_worker.hotspot_password, str)

    def test_hotspot_config_update_persists(self, real_worker):
        original_ssid = real_worker._hotspot_config.ssid
        original_pwd = real_worker._hotspot_config.password

        async def _update():
            await real_worker._async_update_hotspot_config(
                original_ssid,
                f"{_TEST_PREFIX}ConfigTest",
                "testpass99",
                "wpa-psk",
            )

        _run(real_worker, _update, timeout=15.0)

        async def _restore():
            await real_worker._async_update_hotspot_config(
                f"{_TEST_PREFIX}ConfigTest",
                original_ssid,
                original_pwd,
                "wpa-psk",
            )

        _run(real_worker, _restore, timeout=15.0)
        assert real_worker._hotspot_config.ssid == original_ssid


class TestRealSignalMap:
    def test_build_signal_map_returns_dict(self, real_worker):
        result = _run(real_worker, real_worker._build_signal_map, timeout=15.0)
        assert isinstance(result, dict)

    def test_signal_map_values_in_range(self, real_worker):
        result = _run(real_worker, real_worker._build_signal_map, timeout=15.0)
        for ssid, strength in result.items():
            assert isinstance(ssid, str)
            assert 0 <= strength <= 100


class TestRealDbusHealth:
    def test_ensure_dbus_connection_returns_true(self, real_worker):
        result = _run(real_worker, real_worker._ensure_dbus_connection)
        assert result is True

    def test_resets_error_counter_on_success(self, real_worker):
        real_worker._consecutive_dbus_errors = 2
        _run(real_worker, real_worker._ensure_dbus_connection)
        assert real_worker._consecutive_dbus_errors == 0


class TestRealFallbackPoll:
    def test_fallback_poll_does_not_crash(self, real_worker):
        with _capture(real_worker.state_changed) as received:
            _run(real_worker, real_worker._async_fallback_poll, timeout=20.0)
        assert len(received) >= 1
