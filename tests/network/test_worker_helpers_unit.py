"""Unit tests for the NetworkManagerWorker helpers extracted to cut C901 complexity."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from PyQt6.QtCore import QObject

from BlocksScreen.lib.network import worker as _worker_mod
from BlocksScreen.lib.network.models import ConnectivityState
from BlocksScreen.lib.network.worker import NetworkManagerWorker
from tests.network.conftest import AsyncProxyMock, _ProxyFactory

_ONLINE = ConnectivityState.FULL


def _worker(qapp) -> NetworkManagerWorker:
    """Build a worker without its asyncio thread or D-Bus connection."""
    with patch.object(
        NetworkManagerWorker, "__init__", lambda self: QObject.__init__(self)
    ):
        w = NetworkManagerWorker()
    w._system_bus = MagicMock(name="mock_bus")
    w._primary_wifi_iface = "wlan0"
    w._primary_wired_iface = "eth0"
    w._iface_to_device_path = {}
    w._saved_cache_dirty = False
    w._get_ip_by_interface = AsyncMock(return_value="")
    w._get_current_ip = AsyncMock(return_value="")
    w._get_ip_os_fallback = MagicMock(return_value="")
    return w


class TestResolveCurrentIp:
    @pytest.mark.asyncio
    async def test_wired_uses_nm_address(self, qapp):
        w = _worker(qapp)
        w._get_ip_by_interface.return_value = "192.168.0.10"
        assert await w._resolve_current_ip("wlan0", "", True, _ONLINE) == (
            "192.168.0.10",
            True,
        )
        w._get_ip_by_interface.assert_awaited_once_with("eth0")

    @pytest.mark.asyncio
    async def test_wired_falls_back_to_os_address(self, qapp):
        w = _worker(qapp)
        w._get_ip_os_fallback.return_value = "192.168.0.11"
        assert await w._resolve_current_ip("wlan0", "", True, _ONLINE) == (
            "192.168.0.11",
            True,
        )
        w._get_ip_os_fallback.assert_called_once_with("eth0")

    @pytest.mark.asyncio
    async def test_wifi_falls_back_to_primary_connection_ip(self, qapp):
        w = _worker(qapp)
        w._get_current_ip.return_value = "10.0.0.5"
        assert await w._resolve_current_ip("wlan0", "Home", False, _ONLINE) == (
            "10.0.0.5",
            False,
        )
        w._get_ip_by_interface.assert_awaited_once_with("wlan0")

    @pytest.mark.asyncio
    async def test_os_fallback_on_wired_marks_ethernet(self, qapp):
        w = _worker(qapp)
        w._get_ip_os_fallback.side_effect = lambda i: (
            "192.168.0.12" if i == "eth0" else ""
        )
        assert await w._resolve_current_ip("wlan0", "", False, _ONLINE) == (
            "192.168.0.12",
            True,
        )

    @pytest.mark.asyncio
    async def test_os_fallback_on_wifi_keeps_ethernet_flag(self, qapp):
        w = _worker(qapp)
        w._get_ip_os_fallback.side_effect = lambda i: "10.0.0.6" if i == "wlan0" else ""
        assert await w._resolve_current_ip("wlan0", "", False, _ONLINE) == (
            "10.0.0.6",
            False,
        )

    @pytest.mark.asyncio
    async def test_offline_skips_os_fallback(self, qapp):
        w = _worker(qapp)
        result = await w._resolve_current_ip("wlan0", "", False, ConnectivityState.NONE)
        assert result == ("", False)
        w._get_ip_os_fallback.assert_not_called()


class TestWifiSignalAndSecurity:
    @pytest.mark.asyncio
    async def test_no_ssid_skips_dbus(self, qapp):
        w = _worker(qapp)
        w._build_signal_map = AsyncMock()
        assert await w._wifi_signal_and_security("") == (0, "")
        w._build_signal_map.assert_not_awaited()


class TestBuildVlanProperties:
    def test_full_static_profile(self, qapp):
        w = _worker(qapp)
        props = w._build_vlan_properties(
            "VLAN 10",
            10,
            "eth0",
            ("192.168.10.2", "255.255.255.0", "192.168.10.1"),
            ("1.1.1.1", "8.8.8.8"),
        )
        to_uint = NetworkManagerWorker._ip_to_nm_uint32
        assert props["connection"]["id"] == ("s", "VLAN 10")
        assert props["connection"]["type"] == ("s", "vlan")
        assert props["connection"]["autoconnect"] == ("b", False)
        assert props["vlan"] == {"id": ("u", 10), "parent": ("s", "eth0")}
        assert props["ipv4"]["addresses"] == (
            "aau",
            [[to_uint("192.168.10.2"), 24, to_uint("192.168.10.1")]],
        )
        assert props["ipv4"]["gateway"] == ("s", "192.168.10.1")
        assert props["ipv4"]["dns"] == ("au", [to_uint("1.1.1.1"), to_uint("8.8.8.8")])
        assert props["ipv6"] == {"method": ("s", "ignore")}

    def test_optional_gateway_and_dns_omitted(self, qapp):
        w = _worker(qapp)
        props = w._build_vlan_properties(
            "VLAN 20", 20, "eth0", ("10.20.0.2", "16", ""), ("", "9.9.9.9")
        )
        assert props["ipv4"]["addresses"][1][0][1:] == [16, 0]
        assert props["ipv4"]["gateway"] == ("s", "")
        assert props["ipv4"]["dns"] == (
            "au",
            [NetworkManagerWorker._ip_to_nm_uint32("9.9.9.9")],
        )

    def test_invalid_address_raises(self, qapp):
        w = _worker(qapp)
        with pytest.raises(ValueError):
            w._build_vlan_properties(
                "VLAN 30", 30, "eth0", ("999.1.1.1", "24", ""), ("", "")
            )


@patch.object(_worker_mod.asyncio, "sleep", new=AsyncMock())
class TestWaitForProfileIp:
    @pytest.mark.asyncio
    async def test_returns_ip_once_ssid_matches(self, qapp):
        w = _worker(qapp)
        w._get_current_ssid = AsyncMock(side_effect=["Other", "home"])
        w._get_current_ip.return_value = "10.0.0.7"
        assert await w._wait_for_profile_ip("Home", timeout=5.0) == "10.0.0.7"
        assert w._get_current_ssid.await_count == 2

    @pytest.mark.asyncio
    async def test_os_fallback_when_nm_has_no_ip(self, qapp):
        w = _worker(qapp)
        w._get_current_ssid = AsyncMock(return_value="Home")
        w._get_ip_os_fallback.return_value = "10.0.0.8"
        assert await w._wait_for_profile_ip("Home", timeout=5.0) == "10.0.0.8"

    @pytest.mark.asyncio
    async def test_lookup_error_is_retried(self, qapp):
        w = _worker(qapp)
        w._get_current_ssid = AsyncMock(side_effect=[RuntimeError("dbus"), "Home"])
        w._get_current_ip.return_value = "10.0.0.9"
        assert await w._wait_for_profile_ip("Home", timeout=5.0) == "10.0.0.9"

    @pytest.mark.asyncio
    async def test_timeout_returns_empty(self, qapp):
        w = _worker(qapp)
        w._get_current_ssid = AsyncMock(return_value="Other")
        assert await w._wait_for_profile_ip("Home", timeout=0.01) == ""


class TestDeleteAllApModeConnections:
    @pytest.mark.asyncio
    async def test_deletes_only_ap_profiles_and_invalidates_cache(self, qapp):
        w = _worker(qapp)
        profiles = {
            "/c/ap": {
                "connection": {"type": ("s", "802-11-wireless")},
                "802-11-wireless": {"mode": ("s", "ap")},
            },
            "/c/sta": {
                "connection": {"type": ("s", "802-11-wireless")},
                "802-11-wireless": {"mode": ("s", "infrastructure")},
            },
            "/c/eth": {"connection": {"type": ("s", "802-3-ethernet")}},
        }
        conns = {
            path: AsyncProxyMock(
                get_settings=AsyncMock(return_value=s), delete=AsyncMock()
            )
            for path, s in profiles.items()
        }
        w._nm_settings = _ProxyFactory(
            AsyncProxyMock(list_connections=AsyncMock(return_value=list(conns)))
        )
        w._conn_settings = lambda path: conns[path]

        assert await w._delete_all_ap_mode_connections() == 1
        conns["/c/ap"].delete.assert_awaited_once()
        conns["/c/sta"].delete.assert_not_awaited()
        conns["/c/eth"].delete.assert_not_awaited()
        assert w._saved_cache_dirty is True

    @pytest.mark.asyncio
    async def test_nothing_deleted_keeps_cache(self, qapp):
        w = _worker(qapp)
        w._nm_settings = _ProxyFactory(
            AsyncProxyMock(list_connections=AsyncMock(return_value=[]))
        )
        assert await w._delete_all_ap_mode_connections() == 0
        assert w._saved_cache_dirty is False
