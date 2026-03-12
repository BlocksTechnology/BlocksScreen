"""Unit tests for BlocksScreen.lib.network.manager.NetworkManager.

The worker and its asyncio thread are mocked — these tests verify the
manager's caching, signal forwarding, lifecycle, scan/poll deferred-init,
and public API without any D-Bus interaction.

Architecture (current):
  The manager owns a ``NetworkManagerWorker`` which runs all D-Bus
  coroutines on a dedicated asyncio thread.  Public methods call
  ``_schedule(coro)`` which dispatches via ``run_coroutine_threadsafe``.
  The worker emits pyqtSignals that the manager forwards to the UI.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import BlocksScreen.lib.network.manager as manager_mod
from BlocksScreen.lib.network.models import (ConnectionPriority,
                                             ConnectionResult,
                                             ConnectivityState, HotspotConfig,
                                             NetworkInfo, NetworkState,
                                             NetworkStatus, SavedNetwork,
                                             SecurityType)


def _make_mock_timer():
    timer = MagicMock()
    timer._active = False
    timer._interval = 0
    timer.isActive.side_effect = lambda: timer._active
    timer.start.side_effect = lambda: setattr(timer, "_active", True)
    timer.stop.side_effect = lambda: setattr(timer, "_active", False)
    timer.setInterval.side_effect = lambda ms: setattr(timer, "_interval", ms)
    timer.interval.side_effect = lambda: timer._interval
    return timer


async def _noop_coro():
    pass


@pytest.fixture
def nm(qapp):
    with (
        patch("BlocksScreen.lib.network.manager.NetworkManagerWorker") as MockWorker,
        patch("BlocksScreen.lib.network.manager.QTimer") as MockQTimer,
    ):
        mock_worker = MagicMock()
        for sig in (
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
            setattr(mock_worker, sig, MagicMock())

        for method in (
            "_async_get_current_state",
            "_async_scan_networks",
            "_async_load_saved_networks",
            "_async_check_connectivity",
            "_async_add_network",
            "_async_connect_network",
            "_async_disconnect",
            "_async_delete_network",
            "_async_update_network",
            "_async_set_wifi_enabled",
            "_async_create_and_activate_hotspot",
            "_async_update_hotspot_config",
            "_async_toggle_hotspot",
            "_async_disconnect_ethernet",
            "_async_connect_ethernet",
            "_async_create_vlan",
            "_async_delete_vlan",
            "_async_update_wifi_static_ip",
            "_async_reset_wifi_to_dhcp",
            "_async_shutdown",
        ):
            setattr(mock_worker, method, MagicMock(return_value=_noop_coro()))

        # Set a real HotspotConfig so seeding from worker._hotspot_config works.
        mock_worker._hotspot_config = HotspotConfig()
        mock_loop = MagicMock()
        mock_loop.is_running.return_value = True
        mock_worker._asyncio_loop = mock_loop
        mock_worker._asyncio_thread = MagicMock()
        MockWorker.return_value = mock_worker

        mock_keepalive_timer = _make_mock_timer()
        MockQTimer.side_effect = [mock_keepalive_timer]

        from BlocksScreen.lib.network.manager import NetworkManager

        with patch("BlocksScreen.lib.network.manager.asyncio") as mock_aio:
            mock_future = MagicMock()
            mock_future.add_done_callback = MagicMock()
            mock_aio.run_coroutine_threadsafe.return_value = mock_future
            mock_aio.Future = asyncio.Future

            nm_inst = NetworkManager()
            nm_inst._mock_worker = mock_worker
            nm_inst._mock_asyncio = mock_aio
            yield nm_inst



def test_manager_hotspot_cache_seeded_from_worker_config(qapp):
    """Manager must read saved config from worker synchronously, not use defaults."""
    with (
        patch("BlocksScreen.lib.network.manager.NetworkManagerWorker") as MockWorker,
        patch("BlocksScreen.lib.network.manager.QTimer"),
    ):
        mock_worker = MagicMock()
        mock_worker._hotspot_config = HotspotConfig(
            ssid="SavedSSID", password="SavedPass", security="wpa-psk"
        )
        for sig in (
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
            setattr(mock_worker, sig, MagicMock())
        mock_worker._asyncio_loop = MagicMock()
        mock_worker._asyncio_loop.is_running.return_value = True
        mock_worker._asyncio_thread = MagicMock()
        MockWorker.return_value = mock_worker

        from BlocksScreen.lib.network.manager import NetworkManager

        nm_inst = NetworkManager()
        assert nm_inst.hotspot_ssid == "SavedSSID"
        assert nm_inst.hotspot_password == "SavedPass"



class TestFacadeCreation:
    def test_initial_cached_state(self, nm):
        assert isinstance(nm._cached_state, NetworkState)
        assert nm._cached_networks == []
        assert nm._cached_saved == []

    def test_initial_hotspot_cache(self, nm):
        assert nm._cached_hotspot_ssid == "PrinterHotspot"
        assert nm._cached_hotspot_password == "123456789"

    def test_not_shutting_down(self, nm):
        assert nm._shutting_down is False

    def test_worker_not_yet_ready(self, nm):
        assert nm._worker_ready is False

    def test_signals_defined(self, nm):
        for sig in (
            "state_changed",
            "networks_scanned",
            "saved_networks_loaded",
            "connection_result",
            "connectivity_changed",
            "error_occurred",
        ):
            assert hasattr(nm, sig)

    def test_network_info_map_initially_empty(self, nm):
        assert nm._network_info_map == {}

    def test_saved_network_map_initially_empty(self, nm):
        assert nm._saved_network_map == {}

    def test_pending_futures_initially_empty(self, nm):
        assert nm._pending_futures == set()

    def test_schedule_with_not_started_loop(self, nm):

        # replace worker.loop with a real loop but *not running*
        nm._worker._asyncio_loop = asyncio.new_event_loop()
        nm._pending_futures = set()

        async def coro():
            pass

        test = coro()

        nm._schedule(test)

        assert nm._pending_futures == set()

        # coroutine should be closed
        with pytest.raises(RuntimeError):
            test.send(None)



class TestCacheSlots:
    def test_on_state_changed(self, nm):
        state = NetworkState(
            connectivity=ConnectivityState.FULL, current_ssid="CachedNet"
        )
        received = []
        nm.state_changed.connect(lambda s: received.append(s))
        nm._on_state_changed(state)
        assert nm._cached_state == state
        assert len(received) == 1

    def test_on_state_changed_skipped_during_shutdown(self, nm):
        nm._shutting_down = True
        old_state = nm._cached_state
        nm._on_state_changed(NetworkState(current_ssid="Ignored"))
        assert nm._cached_state is old_state

    def test_on_networks_scanned(self, nm):
        networks = [
            NetworkInfo(ssid="Net1", signal_strength=80),
            NetworkInfo(ssid="Net2", signal_strength=60),
        ]
        received = []
        nm.networks_scanned.connect(lambda n: received.append(n))
        nm._on_networks_scanned(networks)
        assert nm._cached_networks == networks
        assert "Net1" in nm._network_info_map
        assert "Net2" in nm._network_info_map

    def test_on_networks_scanned_overwrites_map(self, nm):
        nm._network_info_map = {"OldNet": MagicMock()}
        nm._on_networks_scanned([NetworkInfo(ssid="New", signal_strength=50)])
        assert "OldNet" not in nm._network_info_map
        assert "New" in nm._network_info_map

    def test_on_networks_scanned_skipped_during_shutdown(self, nm):
        nm._shutting_down = True
        nm._cached_networks = []
        nm._on_networks_scanned([NetworkInfo(ssid="Late")])
        assert nm._cached_networks == []
        assert nm._network_info_map == {}

    def test_on_saved_networks_loaded(self, nm):
        saved = [
            SavedNetwork(
                ssid="S1",
                uuid="u1",
                connection_path="/1",
                security_type="wpa-psk",
                mode="infrastructure",
            ),
        ]
        nm._on_saved_networks_loaded(saved)
        assert "s1" in nm._saved_network_map
        assert nm._cached_saved == saved

    def test_on_saved_networks_loaded_case_insensitive(self, nm):
        saved = [
            SavedNetwork(
                ssid="MixedCase",
                uuid="u",
                connection_path="/1",
                security_type="",
                mode="infrastructure",
            ),
        ]
        nm._on_saved_networks_loaded(saved)
        assert nm.get_saved_network("MIXEDCASE") is saved[0]
        assert nm.get_saved_network("mixedcase") is saved[0]

    def test_on_saved_networks_loaded_skipped_during_shutdown(self, nm):
        nm._shutting_down = True
        nm._cached_saved = []
        nm._on_saved_networks_loaded(
            [
                SavedNetwork(
                    ssid="Late",
                    uuid="u",
                    connection_path="/1",
                    security_type="",
                    mode="infrastructure",
                ),
            ]
        )
        assert nm._cached_saved == []
        assert nm._saved_network_map == {}

    def test_on_hotspot_info_ready(self, nm):
        nm._on_hotspot_info_ready("TestAP", "secret123", "wpa-psk")
        assert nm._cached_hotspot_ssid == "TestAP"
        assert nm._cached_hotspot_password == "secret123"
        assert nm._cached_hotspot_security == "wpa-psk"

    def test_on_networks_scanned_duplicate_ssid_last_wins(self, nm):
        networks = [
            NetworkInfo(ssid="Same", signal_strength=40),
            NetworkInfo(ssid="Same", signal_strength=90),
        ]
        nm._on_networks_scanned(networks)
        assert nm._network_info_map["Same"].signal_strength == 90



class TestConvenienceProperties:
    def test_current_ssid(self, nm):
        nm._cached_state = NetworkState(current_ssid="MySSID")
        assert nm.current_ssid == "MySSID"

    def test_current_ssid_none(self, nm):
        nm._cached_state = NetworkState()
        assert nm.current_ssid is None

    def test_current_state_property(self, nm):
        state = NetworkState(connectivity=ConnectivityState.FULL)
        nm._cached_state = state
        assert nm.current_state is state

    def test_saved_networks_property(self, nm):
        saved = [SavedNetwork(ssid="A")]
        nm._cached_saved = saved
        assert nm.saved_networks is saved

    def test_hotspot_ssid_property(self, nm):
        nm._cached_hotspot_ssid = "CustomAP"
        assert nm.hotspot_ssid == "CustomAP"

    def test_hotspot_password_property(self, nm):
        nm._cached_hotspot_password = "secret"
        assert nm.hotspot_password == "secret"

    def test_hotspot_security_property(self, nm):
        nm._cached_hotspot_security = "wpa-psk"
        assert nm.hotspot_security == "wpa-psk"

    def test_get_network_info_found(self, nm):
        info = NetworkInfo(ssid="TargetNet", signal_strength=75)
        nm._network_info_map = {"TargetNet": info}
        assert nm.get_network_info("TargetNet") is info

    def test_get_network_info_not_found(self, nm):
        nm._network_info_map = {}
        assert nm.get_network_info("Ghost") is None

    def test_get_saved_network_case_insensitive(self, nm):
        sn = SavedNetwork(
            ssid="Saved",
            uuid="u",
            connection_path="/p",
            security_type="wpa-psk",
            mode="infrastructure",
            priority=90,
        )
        nm._saved_network_map = {"saved": sn}
        assert nm.get_saved_network("SAVED") is sn

    def test_get_saved_network_not_found(self, nm):
        nm._saved_network_map = {}
        assert nm.get_saved_network("Ghost") is None



class TestPublicAPI:
    def _count(self, nm):
        return nm._mock_asyncio.run_coroutine_threadsafe.call_count

    def test_get_current_state(self, nm):
        b = self._count(nm)
        nm.get_current_state()
        assert self._count(nm) > b

    def test_refresh_state(self, nm):
        b = self._count(nm)
        nm.refresh_state()
        assert self._count(nm) >= b + 2

    def test_scan_networks(self, nm):
        b = self._count(nm)
        nm.scan_networks()
        assert self._count(nm) > b

    def test_load_saved_networks(self, nm):
        b = self._count(nm)
        nm.load_saved_networks()
        assert self._count(nm) > b

    def test_check_connectivity(self, nm):
        b = self._count(nm)
        nm.check_connectivity()
        assert self._count(nm) > b

    def test_add_network(self, nm):
        b = self._count(nm)
        nm.add_network("Net", "pass", ConnectionPriority.HIGH.value)
        assert self._count(nm) > b

    def test_connect_network(self, nm):
        b = self._count(nm)
        nm.connect_network("MyNet")
        assert self._count(nm) > b

    def test_disconnect(self, nm):
        b = self._count(nm)
        nm.disconnect()
        assert self._count(nm) > b

    def test_delete_network(self, nm):
        b = self._count(nm)
        nm.delete_network("OldNet")
        assert self._count(nm) > b

    def test_update_network(self, nm):
        b = self._count(nm)
        nm.update_network("Net", "p", 90)
        assert self._count(nm) > b

    def test_set_wifi_enabled(self, nm):
        b = self._count(nm)
        nm.set_wifi_enabled(False)
        assert self._count(nm) > b

    def test_create_hotspot(self, nm):
        b = self._count(nm)
        nm.create_hotspot("AP", "pass", "wpa-psk")
        assert self._count(nm) > b

    def test_toggle_hotspot(self, nm):
        b = self._count(nm)
        nm.toggle_hotspot(True)
        assert self._count(nm) > b

    def test_update_hotspot_config(self, nm):
        b = self._count(nm)
        nm.update_hotspot_config("Old", "New", "pass")
        assert self._count(nm) > b

    def test_disconnect_ethernet(self, nm):
        b = self._count(nm)
        nm.disconnect_ethernet()
        assert self._count(nm) > b

    def test_connect_ethernet(self, nm):
        b = self._count(nm)
        nm.connect_ethernet()
        assert self._count(nm) > b

    def test_create_vlan(self, nm):
        b = self._count(nm)
        nm.create_vlan_connection(100, "10.0.0.5", "255.255.255.0", "10.0.0.1")
        assert self._count(nm) > b

    def test_delete_vlan(self, nm):
        b = self._count(nm)
        nm.delete_vlan_connection(100)
        assert self._count(nm) > b

    def test_update_wifi_static_ip(self, nm):
        b = self._count(nm)
        nm.update_wifi_static_ip("Net", "10.0.0.5", "255.255.255.0", "10.0.0.1")
        assert self._count(nm) > b

    def test_reset_wifi_to_dhcp(self, nm):
        b = self._count(nm)
        nm.reset_wifi_to_dhcp("Net")
        assert self._count(nm) > b

    def test_schedule_drops_when_shutting_down(self, nm):
        nm._shutting_down = True
        b = self._count(nm)
        nm.get_current_state()
        assert self._count(nm) == b



class TestKeepalive:
    def test_keepalive_tick_dispatches(self, nm):
        b = nm._mock_asyncio.run_coroutine_threadsafe.call_count
        nm._on_keepalive_tick()
        assert nm._mock_asyncio.run_coroutine_threadsafe.call_count > b

    def test_keepalive_tick_does_not_crash(self, nm):
        for _ in range(4):
            nm._on_keepalive_tick()

    def test_keepalive_tick_skipped_during_shutdown(self, nm):
        nm._shutting_down = True
        b = nm._mock_asyncio.run_coroutine_threadsafe.call_count
        nm._on_keepalive_tick()
        assert nm._mock_asyncio.run_coroutine_threadsafe.call_count == b

    def test_keepalive_tick_refreshes_state_connectivity_saved(self, nm):
        b = nm._mock_asyncio.run_coroutine_threadsafe.call_count
        nm._on_keepalive_tick()
        # Should dispatch 3 coroutines: state + connectivity + saved
        assert nm._mock_asyncio.run_coroutine_threadsafe.call_count == b + 3



class TestWorkerInitialized:
    def test_sets_worker_ready(self, nm):
        nm._on_worker_initialized()
        assert nm._worker_ready is True

    def test_starts_keepalive_timer(self, nm):
        nm._on_worker_initialized()
        assert nm._keepalive_timer.isActive()

    def test_skipped_during_shutdown(self, nm):
        nm._shutting_down = True
        nm._on_worker_initialized()
        assert nm._worker_ready is False

    def test_dispatches_initial_refresh(self, nm):
        b = nm._mock_asyncio.run_coroutine_threadsafe.call_count
        nm._on_worker_initialized()
        assert nm._mock_asyncio.run_coroutine_threadsafe.call_count >= b + 3

    def test_request_state_soon_fires_callback(self, nm, monkeypatch):
        called = {}

        def fake_schedule(coro):
            called["scheduled"] = True

        monkeypatch.setattr(nm, "_schedule", fake_schedule)

        # QTimer is mocked in nm fixture; make singleShot invoke callback synchronously
        fired_with_ms = []
        monkeypatch.setattr(
            manager_mod.QTimer,
            "singleShot",
            lambda ms, cb: (fired_with_ms.append(ms), cb()),
        )

        nm.request_state_soon(delay_ms=123)

        assert called.get("scheduled") is True
        assert fired_with_ms == [123]



class TestFacadeShutdown:
    def test_shutdown_sets_flag(self, nm):
        nm.shutdown()
        assert nm._shutting_down is True

    def test_shutdown_stops_keepalive_timer(self, nm):
        nm._on_worker_initialized()
        nm.shutdown()
        assert not nm._keepalive_timer.isActive()

    def test_close_is_alias(self, nm):
        nm.close()
        assert nm._shutting_down is True

    def test_shutdown_idempotent(self, nm):
        nm.shutdown()
        nm.shutdown()
        assert nm._shutting_down is True

    def test_shutdown_swallows_future_exception(self, nm, caplog):
        import logging

        assert nm._worker._asyncio_loop.is_running()
        nm._mock_asyncio.run_coroutine_threadsafe.return_value.result.side_effect = (
            RuntimeError("async shutdown failed")
        )
        with caplog.at_level(logging.WARNING, logger="BlocksScreen.lib.network.manager"):
            nm.shutdown()
        assert nm._shutting_down is True
        assert "async shutdown failed" in caplog.text

    def test_shutdown_skips_coroutine_when_loop_not_running(self, nm):
        nm._worker._asyncio_loop.is_running.return_value = False
        nm.shutdown()
        nm._mock_asyncio.run_coroutine_threadsafe.assert_not_called()
        assert nm._shutting_down is True



class TestSignalForwarding:
    def test_error_occurred_signal_exists(self, nm):
        """Facade exposes error_occurred as a real pyqtSignal."""
        assert hasattr(nm, "error_occurred")
        # Connect and emit on the manager's own signal (not worker-forwarded)
        received = []
        nm.error_occurred.connect(lambda op, msg: received.append((op, msg)))
        nm.error_occurred.emit("test_op", "test_msg")
        assert received == [("test_op", "test_msg")]

    def test_reconnect_complete_signal_exists(self, nm):
        """Facade exposes reconnect_complete as a real pyqtSignal."""
        received = []
        nm.reconnect_complete.connect(lambda: received.append(True))
        nm.reconnect_complete.emit()
        assert len(received) == 1

    def test_worker_error_signal_wired_on_init(self, nm):
        """Worker's error_occurred.connect was called during init."""
        nm._worker.error_occurred.connect.assert_called()

    def test_worker_reconnect_signal_wired_on_init(self, nm):
        """Worker's reconnect_complete.connect was called during init."""
        nm._worker.reconnect_complete.connect.assert_called()

    def test_hotspot_config_updated_emits_on_ready(self, nm, qtbot):
        received = []
        nm.hotspot_config_updated.connect(
            lambda s, p, sec: received.append((s, p, sec))
        )
        nm._on_hotspot_info_ready("NewSSID", "NewPass", "wpa-psk")
        assert received == [("NewSSID", "NewPass", "wpa-psk")]

    def test_hotspot_info_ready_updates_cache(self, nm):
        nm._on_hotspot_info_ready("Updated", "NewPW", "wpa-psk")
        assert nm.hotspot_ssid == "Updated"
        assert nm.hotspot_password == "NewPW"
        assert nm.hotspot_security == "wpa-psk"
