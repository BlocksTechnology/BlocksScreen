"""Unit tests for BlocksScreen.lib.network.models."""

import pytest

from BlocksScreen.lib.network.models import (SIGNAL_EXCELLENT_THRESHOLD,
                                             SIGNAL_FAIR_THRESHOLD,
                                             SIGNAL_GOOD_THRESHOLD,
                                             SIGNAL_MINIMUM_THRESHOLD,
                                             ConnectionPriority,
                                             ConnectionResult,
                                             ConnectivityState, HotspotConfig,
                                             HotspotSecurity, NetworkInfo,
                                             NetworkState, NetworkStatus,
                                             PendingOperation, SavedNetwork,
                                             SecurityType, VlanInfo,
                                             WifiIconKey,
                                             is_connectable_security,
                                             is_hidden_ssid, signal_to_bars)


class TestSecurityType:
    def test_all_members_exist(self):
        assert len(SecurityType) == 8

    def test_string_enum(self):
        assert SecurityType.OPEN == "open"
        assert isinstance(SecurityType.WPA2_PSK, str)

    def test_owe_value(self):
        assert SecurityType.OWE.value == "owe"

    def test_wpa_eap_value(self):
        assert SecurityType.WPA_EAP.value == "wpa-eap"

    def test_all_values_are_strings(self):
        for member in SecurityType:
            assert isinstance(member.value, str)

    def test_membership_check(self):
        """SecurityType supports 'in' checks against string values."""
        assert "open" in [m.value for m in SecurityType]
        assert "nonexistent" not in [m.value for m in SecurityType]

    def test_equality_with_string(self):
        """str(Enum) based — SecurityType.OPEN == 'open' because it's a str enum."""
        assert SecurityType.OPEN == "open"
        assert SecurityType.WPA2_PSK == "wpa2-psk"

    def test_enterprise_type_exists(self):
        """WPA-EAP (802.1x enterprise) is a valid security type."""
        assert SecurityType.WPA_EAP == "wpa-eap"
        assert SecurityType.WPA_EAP in SecurityType

    def test_all_expected_values(self):
        values = {m.value for m in SecurityType}
        assert values == {
            "open",
            "wep",
            "wpa-psk",
            "wpa2-psk",
            "sae",
            "wpa-eap",
            "owe",
            "unknown",
        }

    def test_is_connectable_security(self):
        assert is_connectable_security(SecurityType.WEP.value) == False

    def test_not_connectable_security(self):
        assert is_connectable_security("No security")



class TestConnectivityState:
    def test_all_states_exist(self):
        assert len(ConnectivityState) == 5
        assert ConnectivityState.FULL == 4

    def test_is_int_enum(self):
        assert ConnectivityState.FULL > ConnectivityState.NONE

    def test_portal_between_none_and_limited(self):
        assert (
            ConnectivityState.NONE
            < ConnectivityState.PORTAL
            < ConnectivityState.LIMITED
        )

    def test_int_conversion(self):
        """ConnectivityState members are usable as plain ints."""
        assert int(ConnectivityState.FULL) == 4
        assert ConnectivityState.UNKNOWN + 1 == 1



class TestConnectionPriority:
    def test_ordering(self):
        assert (
            ConnectionPriority.HIGH > ConnectionPriority.MEDIUM > ConnectionPriority.LOW
        )

    def test_highest_above_high(self):
        assert ConnectionPriority.HIGHEST > ConnectionPriority.HIGH

    def test_values_are_int(self):
        for member in ConnectionPriority:
            assert isinstance(member.value, int)

    def test_medium_is_default_for_saved_network(self):
        """ConnectionPriority.MEDIUM is the default for SavedNetwork.priority."""
        sn = SavedNetwork()
        assert sn.priority == ConnectionPriority.MEDIUM.value



class TestPendingOperation:
    def test_all_members_exist(self):
        assert len(PendingOperation) == 9

    def test_is_int_enum(self):
        """PendingOperation values are plain ints (memory-efficient)."""
        for member in PendingOperation:
            assert isinstance(member.value, int)

    def test_none_is_zero(self):
        assert PendingOperation.NONE == 0

    def test_values_are_unique(self):
        values = [m.value for m in PendingOperation]
        assert len(values) == len(set(values))

    def test_identity_comparison(self):
        op = PendingOperation.CONNECT
        assert op == PendingOperation.CONNECT
        assert op != PendingOperation.WIFI_ON

    def test_in_tuple_lookup(self):
        """Verify the pattern used by networkWindow loading guard."""
        op = PendingOperation.WIFI_OFF
        assert op in (PendingOperation.WIFI_OFF, PendingOperation.HOTSPOT_OFF)

        op2 = PendingOperation.CONNECT
        assert op2 not in (PendingOperation.WIFI_OFF, PendingOperation.HOTSPOT_OFF)

    def test_falsy_none(self):
        """PendingOperation.NONE == 0 is falsy — useful for bool checks."""
        assert not PendingOperation.NONE
        assert PendingOperation.CONNECT  # non-zero is truthy

    def test_all_expected_names(self):
        names = {m.name for m in PendingOperation}
        assert names == {
            "NONE",
            "WIFI_ON",
            "WIFI_OFF",
            "HOTSPOT_ON",
            "HOTSPOT_OFF",
            "CONNECT",
            "ETHERNET_ON",
            "ETHERNET_OFF",
            "WIFI_STATIC_IP",
        }

    def test_ethernet_on_value(self):
        assert PendingOperation.ETHERNET_ON == 6

    def test_ethernet_off_value(self):
        assert PendingOperation.ETHERNET_OFF == 7

    def test_ethernet_operations_are_truthy(self):
        """ETHERNET_ON/OFF are non-zero — truthy for loading guards."""
        assert PendingOperation.ETHERNET_ON
        assert PendingOperation.ETHERNET_OFF

    def test_ethernet_in_tuple_lookup(self):
        """Verify ethernet ops work in the same tuple-check pattern."""
        op = PendingOperation.ETHERNET_ON
        assert op in (PendingOperation.ETHERNET_ON, PendingOperation.ETHERNET_OFF)
        assert op not in (PendingOperation.WIFI_ON, PendingOperation.WIFI_OFF)



class TestSignalToBars:
    def test_zero_signal(self):
        assert signal_to_bars(0) == 0

    def test_below_minimum_threshold(self):
        assert signal_to_bars(SIGNAL_MINIMUM_THRESHOLD - 1) == 0

    def test_at_minimum_threshold(self):
        assert signal_to_bars(SIGNAL_MINIMUM_THRESHOLD) == 1

    def test_fair_signal(self):
        assert signal_to_bars(SIGNAL_FAIR_THRESHOLD + 1) == 2

    def test_good_signal(self):
        assert signal_to_bars(SIGNAL_GOOD_THRESHOLD) == 3

    def test_excellent_signal(self):
        assert signal_to_bars(SIGNAL_EXCELLENT_THRESHOLD) == 4

    def test_max_signal(self):
        assert signal_to_bars(100) == 4

    def test_boundary_25_returns_1(self):
        """At exactly 25% the signal is fair threshold — returns 1 (not 2)."""
        assert signal_to_bars(25) == 1

    def test_boundary_50_returns_3(self):
        assert signal_to_bars(50) == 3

    def test_boundary_75_returns_4(self):
        assert signal_to_bars(75) == 4

    def test_negative_signal(self):
        """Defensive: negative input should return 0."""
        assert signal_to_bars(-10) == 0

    def test_thresholds_are_ordered(self):
        assert (
            SIGNAL_MINIMUM_THRESHOLD
            < SIGNAL_FAIR_THRESHOLD
            < SIGNAL_GOOD_THRESHOLD
            < SIGNAL_EXCELLENT_THRESHOLD
        )



class TestWifiIconKey:
    def test_ethernet_value(self):
        assert WifiIconKey.ETHERNET == -1

    def test_hotspot_value(self):
        assert WifiIconKey.HOTSPOT == 10

    def test_all_wifi_members_exist(self):
        """0-4 bars x open/protected = 10 wifi members."""
        wifi_members = [
            m
            for m in WifiIconKey
            if m not in (WifiIconKey.ETHERNET, WifiIconKey.HOTSPOT)
        ]
        assert len(wifi_members) == 10

    def test_from_bars_open(self):
        key = WifiIconKey.from_bars(3, is_protected=False)
        assert key == WifiIconKey.WIFI_3_OPEN

    def test_from_bars_protected(self):
        key = WifiIconKey.from_bars(3, is_protected=True)
        assert key == WifiIconKey.WIFI_3_PROTECTED

    def test_from_bars_zero(self):
        key = WifiIconKey.from_bars(0, is_protected=False)
        assert key == WifiIconKey.WIFI_0_OPEN

    def test_from_bars_four_protected(self):
        key = WifiIconKey.from_bars(4, is_protected=True)
        assert key == WifiIconKey.WIFI_4_PROTECTED

    def test_from_bars_error(self):
        with pytest.raises(ValueError):
            WifiIconKey.from_bars(5, is_protected=False)

    def test_from_signal_excellent_protected(self):
        key = WifiIconKey.from_signal(80, is_protected=True)
        assert key == WifiIconKey.WIFI_4_PROTECTED

    def test_from_signal_good_open(self):
        key = WifiIconKey.from_signal(55, is_protected=False)
        assert key == WifiIconKey.WIFI_3_OPEN

    def test_from_signal_zero(self):
        key = WifiIconKey.from_signal(0, is_protected=False)
        assert key == WifiIconKey.WIFI_0_OPEN

    def test_bars_property(self):
        assert WifiIconKey.WIFI_2_OPEN.bars == 2
        assert WifiIconKey.WIFI_4_PROTECTED.bars == 4
        assert WifiIconKey.WIFI_0_OPEN.bars == 0

    def test_is_protected_property(self):
        assert WifiIconKey.WIFI_3_PROTECTED.is_protected is True
        assert WifiIconKey.WIFI_3_OPEN.is_protected is False

    def test_bars_raises_for_ethernet(self):
        with pytest.raises(ValueError):
            _ = WifiIconKey.ETHERNET.bars

    def test_bars_raises_for_hotspot(self):
        with pytest.raises(ValueError):
            _ = WifiIconKey.HOTSPOT.bars

    def test_is_protected_raises_for_ethernet(self):
        with pytest.raises(ValueError):
            _ = WifiIconKey.ETHERNET.is_protected

    def test_is_protected_raises_for_hotspot(self):
        with pytest.raises(ValueError):
            _ = WifiIconKey.HOTSPOT.is_protected

    def test_encoding_roundtrip(self):
        """from_bars -> bars/is_protected roundtrips correctly for all combos."""
        for bars in range(5):
            for protected in (True, False):
                key = WifiIconKey.from_bars(bars, protected)
                assert key.bars == bars
                assert key.is_protected is protected

    def test_is_int_enum(self):
        """WifiIconKey values are plain ints — cheap cross-thread signalling."""
        for member in WifiIconKey:
            assert isinstance(member.value, int)



class TestNetworkInfo:
    def test_defaults(self):
        info = NetworkInfo()
        assert info.ssid == ""
        assert info.security_type == SecurityType.UNKNOWN
        assert info.signal_strength == 0
        assert info.is_open is False
        assert info.bssid == ""

    def test_frozen(self, make_network_info):
        info = make_network_info()
        with pytest.raises(AttributeError):
            info.ssid = "Changed"

    def test_status_active(self):
        assert (
            NetworkInfo(ssid="X", network_status=NetworkStatus.ACTIVE).status
            == "Active"
        )

    def test_status_saved(self):
        assert (
            NetworkInfo(ssid="X", network_status=NetworkStatus.SAVED).status == "Saved"
        )

    def test_status_open(self):
        assert NetworkInfo(ssid="X", network_status=NetworkStatus.OPEN).status == "Open"

    def test_status_protected(self):
        assert (
            NetworkInfo(ssid="X", network_status=NetworkStatus.DISCOVERED).status
            == "Protected"
        )

    def test_is_active(self):
        assert NetworkInfo(ssid="x", network_status=NetworkStatus.ACTIVE).is_active

    def test_is_saved(self):
        assert NetworkInfo(ssid="x", network_status=NetworkStatus.SAVED).is_saved

    def test_is_hidden(self):
        assert NetworkInfo(ssid="x", network_status=NetworkStatus.HIDDEN).is_hidden

    def test_update_status_label_changes_label(self, preserve_labels):
        NetworkStatus.update_status_label(NetworkStatus.DISCOVERED, "Brand New")
        assert NetworkStatus.DISCOVERED.label == "Brand New"

    def test_status_priority(self):
        """Active status label returned regardless of other properties."""
        info = NetworkInfo(
            ssid="X",
            network_status=NetworkStatus.ACTIVE,
            security_type=SecurityType.OPEN,
        )
        assert info.status == "Active"

    def test_status_saved_over_open(self):
        """Saved status label takes priority — open is derived from security_type."""
        info = NetworkInfo(
            ssid="X",
            network_status=NetworkStatus.SAVED,
            security_type=SecurityType.OPEN,
        )
        assert info.status == "Saved"

    def test_security_type_accepts_string(self):
        """security_type field allows both SecurityType enum and raw str."""
        info = NetworkInfo(ssid="X", security_type="wpa-psk")
        assert info.security_type == "wpa-psk"

    def test_security_type_enterprise(self):
        """Enterprise security type can be set on NetworkInfo."""
        info = NetworkInfo(ssid="eduroam", security_type=SecurityType.WPA_EAP)
        assert info.security_type == SecurityType.WPA_EAP
        assert info.security_type == "wpa-eap"

    def test_equality(self, make_network_info):
        """Two NetworkInfo with identical fields compare equal (frozen dataclass)."""
        a = make_network_info(ssid="Same", signal_strength=50)
        b = make_network_info(ssid="Same", signal_strength=50)
        assert a == b

    def test_inequality_different_signal(self, make_network_info):
        a = make_network_info(ssid="Net", signal_strength=50)
        b = make_network_info(ssid="Net", signal_strength=90)
        assert a != b

    def test_hashable(self, make_network_info):
        """Frozen dataclass is hashable — can be used in sets."""
        info = make_network_info()
        s = {info}
        assert info in s



class TestSavedNetwork:
    def test_defaults(self):
        sn = SavedNetwork()
        assert sn.ssid == ""
        assert sn.mode == "infrastructure"
        assert sn.priority == ConnectionPriority.MEDIUM.value
        assert sn.timestamp == 0

    def test_frozen(self):
        sn = SavedNetwork(ssid="X")
        with pytest.raises(AttributeError):
            sn.ssid = "Changed"

    def test_custom_values(self, make_saved_network):
        sn = make_saved_network(priority=90, timestamp=1700000000)
        assert sn.priority == 90
        assert sn.timestamp == 1700000000

    def test_equality(self, make_saved_network):
        a = make_saved_network(ssid="Net", uuid="u1")
        b = make_saved_network(ssid="Net", uuid="u1")
        assert a == b



class TestConnectionResult:
    def test_success(self):
        r = ConnectionResult(success=True, message="OK")
        assert r.success is True
        assert r.data is None

    def test_failure_with_data(self):
        r = ConnectionResult(success=False, data={"attempts": 3})
        assert r.data == {"attempts": 3}

    def test_error_code_default(self):
        r = ConnectionResult()
        assert r.error_code == ""

    def test_frozen(self):
        r = ConnectionResult(success=True)
        with pytest.raises(AttributeError):
            r.success = False

    def test_all_fields_populated(self):
        r = ConnectionResult(
            success=False,
            message="Permission denied",
            error_code="permission_denied",
            data={"ssid": "Net"},
        )
        assert r.success is False
        assert r.message == "Permission denied"
        assert r.error_code == "permission_denied"
        assert r.data["ssid"] == "Net"



class TestNetworkState:
    def test_defaults(self):
        s = NetworkState()
        assert s.connectivity == ConnectivityState.UNKNOWN
        assert s.current_ssid is None
        assert s.current_ip == ""
        assert s.primary_interface == ""
        assert s.ethernet_connected is False
        assert s.ethernet_carrier is False

    def test_frozen(self):
        with pytest.raises(AttributeError):
            NetworkState().current_ssid = "x"

    def test_custom_values(self, make_network_state):
        s = make_network_state(hotspot_enabled=True, primary_interface="wlan0")
        assert s.hotspot_enabled is True
        assert s.primary_interface == "wlan0"

    def test_ethernet_connected_field(self):
        s = NetworkState(ethernet_connected=True)
        assert s.ethernet_connected is True

    def test_ethernet_connected_default_false(self):
        s = NetworkState()
        assert s.ethernet_connected is False

    def test_ethernet_carrier_field(self):
        """ethernet_carrier indicates physical cable presence."""
        s = NetworkState(ethernet_carrier=True)
        assert s.ethernet_carrier is True

    def test_ethernet_carrier_default_false(self):
        s = NetworkState()
        assert s.ethernet_carrier is False

    def test_carrier_without_connected(self):
        """Cable plugged in (carrier) but not activated (not connected)."""
        s = NetworkState(ethernet_carrier=True, ethernet_connected=False)
        assert s.ethernet_carrier is True
        assert s.ethernet_connected is False

    def test_full_state_snapshot(self):
        """All fields set — verifies the dataclass accepts all parameters."""
        s = NetworkState(
            connectivity=ConnectivityState.FULL,
            current_ssid="HomeWifi",
            current_ip="192.168.1.50",
            wifi_enabled=True,
            hotspot_enabled=False,
            primary_interface="wlan0",
            signal_strength=85,
            security_type="wpa-psk",
            ethernet_connected=False,
            ethernet_carrier=False,
        )
        assert s.connectivity == ConnectivityState.FULL
        assert s.signal_strength == 85



class TestHotspotConfig:
    def test_defaults(self):
        c = HotspotConfig()
        assert c.ssid == "PrinterHotspot"
        assert c.channel == 6
        assert c.band == "bg"
        assert c.password == "123456789"

    def test_mutable(self):
        c = HotspotConfig()
        c.ssid = "NewName"
        c.password = "newpass123"
        assert c.ssid == "NewName"
        assert c.password == "newpass123"

    def test_custom_init(self):
        c = HotspotConfig(ssid="Custom", password="secret", band="a", channel=36)
        assert c.ssid == "Custom"
        assert c.channel == 36
        assert c.band == "a"



class TestHotspotSecurity:
    def test_is_valid_returns_false_for_invalid_value(self):
        assert not HotspotSecurity.is_valid("invalid_value")



class TestIsHiddenSSID:
    @pytest.mark.parametrize(
        "ssid",
        [
            None,
            "",
            "   ",
            "\t",
            "\n",
            "\x00\x00\x00",
            "unknown",
            "UNKNOWN",
            "hidden",
            "<hidden>",
            "<HIDDEN>",
        ],
    )
    def test_hidden_values(self, ssid):
        assert is_hidden_ssid(ssid) is True

    @pytest.mark.parametrize(
        "ssid",
        [
            "MyNetwork",
            "Home WiFi",
            "Office_5GHz",
            "Guest",
            "NotHiddenNetwork",
            "MyHiddenSSID",
            "12345",
        ],
    )
    def test_normal_ssids(self, ssid):
        assert is_hidden_ssid(ssid) is False

    def test_single_null_byte(self):
        assert is_hidden_ssid("\x00") is True

    def test_mixed_content_not_hidden(self):
        assert is_hidden_ssid("net\x00work") is False

    def test_unicode_ssid_not_hidden(self):
        """Unicode SSIDs like CJK characters are valid, not hidden."""
        assert is_hidden_ssid("我的网络") is False

    def test_emoji_ssid_not_hidden(self):
        assert is_hidden_ssid("🏠WiFi") is False

    def test_leading_trailing_whitespace_hidden_indicator(self):
        """'  unknown  ' should still be detected (stripped then checked)."""
        assert is_hidden_ssid("  unknown  ") is True
        assert is_hidden_ssid("  <hidden>  ") is True

    def test_enterprise_ssid_not_hidden(self):
        """Common enterprise SSIDs are valid, not hidden."""
        assert is_hidden_ssid("eduroam") is False
        assert is_hidden_ssid("MEO-WiFi") is False
        assert is_hidden_ssid("CorporateWPA2") is False



class TestVlanInfo:
    def test_defaults(self):
        v = VlanInfo()
        assert v.vlan_id == 0
        assert v.ip_address == ""
        assert v.interface == ""
        assert v.gateway == ""
        assert v.dns_servers == ()
        assert v.is_dhcp is False

    def test_custom(self):
        v = VlanInfo(
            vlan_id=10,
            ip_address="10.0.0.5",
            interface="eth0.10",
            gateway="10.0.0.1",
            dns_servers=("8.8.8.8",),
            is_dhcp=True,
        )
        assert v.vlan_id == 10
        assert v.interface == "eth0.10"
        assert v.is_dhcp is True

    def test_frozen(self):
        v = VlanInfo()
        with pytest.raises(AttributeError):
            v.vlan_id = 99



class TestIsConnectableSecurity:
    @pytest.mark.parametrize(
        "sec",
        [
            SecurityType.WPA2_PSK,
            SecurityType.WPA3_SAE,
            SecurityType.WPA_PSK,
        ],
    )
    def test_supported(self, sec):
        assert is_connectable_security(sec) is True

    @pytest.mark.parametrize(
        "sec",
        [
            SecurityType.OWE,
            SecurityType.WPA_EAP,
            SecurityType.WEP,
            SecurityType.OPEN,
        ],
    )
    def test_unsupported(self, sec):
        assert is_connectable_security(sec) is False

    def test_unknown_string_is_connectable(self):
        """Unlisted security types are assumed connectable."""
        assert is_connectable_security("some-future-type") is True



class TestSignalToBarsThresholds:
    @pytest.mark.parametrize(
        "signal,expected_bars",
        [
            (4, 0),
            (5, 1),
            (24, 1),
            (26, 2),
            (49, 2),
            (50, 3),
            (74, 3),
            (75, 4),
            (0, 0),
            (100, 4),
        ],
    )
    def test_threshold_boundaries(self, signal, expected_bars):
        assert signal_to_bars(signal) == expected_bars



class TestWifiIconKeyEdgeCases:
    def test_from_bars_negative_raises(self):
        with pytest.raises(ValueError):
            WifiIconKey.from_bars(bars=-1, is_protected=False)
