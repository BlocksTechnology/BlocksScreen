"""Unit tests for NetworkControlWindow (networkWindow.py).

Strategy
--------
All external dependencies (NetworkManager, Qt resource files,
custom widgets) are mocked in the ``win`` fixture defined in conftest.py.
Tests drive the window by calling public slot methods directly, then
assert on widget visibility and text state.

Coverage targets
----------------
* _handle_first_run — all 5 branches (ethernet / wifi-full / hotspot /
  wifi-on-no-conn / disconnected)
* _on_network_state_changed — normal display path + loading-state machine
* _display_connected_state — ethernet vs Wi-Fi vs hotspot
* _display_disconnected_state / _display_wifi_on_no_connection
* _sync_ethernet_panel — carrier visibility + toggle sync
* _set_loading_state / _clear_loading
* _handle_load_timeout — each pending-operation branch
* _on_reconnect_complete
* _on_operation_complete — success/failure branches
* _handle_wifi_toggle / _handle_hotspot_toggle / _handle_ethernet_toggle
* _emit_status_icon — ethernet / hotspot / wifi / disconnected
"""

from unittest.mock import MagicMock, patch

import pytest
from PyQt6 import QtCore, QtGui, QtWidgets

from BlocksScreen.lib.network.models import (ConnectionPriority,
                                             ConnectionResult,
                                             ConnectivityState, NetworkInfo,
                                             NetworkState, NetworkStatus,
                                             PendingOperation, SavedNetwork,
                                             SecurityType, WifiIconKey,
                                             signal_to_bars)
from BlocksScreen.lib.panels.networkWindow import NetworkControlWindow

# ─────────────────────────────────────────────────────────────────────────────
# Dead-code removal verification
# ─────────────────────────────────────────────────────────────────────────────


def test_new_ip_signal_removed():
    """Ensure dead new_ip_signal is not present on the class."""
    assert not hasattr(NetworkControlWindow, "new_ip_signal")


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _eth_state(**kw) -> NetworkState:
    """Minimal ethernet-connected state."""
    defaults = dict(
        connectivity=ConnectivityState.FULL,
        current_ssid="",
        current_ip="192.168.1.104",
        wifi_enabled=False,
        hotspot_enabled=False,
        ethernet_connected=True,
        ethernet_carrier=True,
    )
    defaults.update(kw)
    return NetworkState(**defaults)


def _wifi_state(**kw) -> NetworkState:
    """Minimal Wi-Fi connected state."""
    defaults = dict(
        connectivity=ConnectivityState.FULL,
        current_ssid="HomeNet",
        current_ip="192.168.1.50",
        wifi_enabled=True,
        hotspot_enabled=False,
        ethernet_connected=False,
        ethernet_carrier=False,
        signal_strength=75,
        security_type="wpa-psk",
    )
    defaults.update(kw)
    return NetworkState(**defaults)


def _hotspot_state(**kw) -> NetworkState:
    defaults = dict(
        connectivity=ConnectivityState.LIMITED,
        current_ssid="PrinterHotspot",
        current_ip="10.42.0.1",
        wifi_enabled=True,
        hotspot_enabled=True,
        ethernet_connected=False,
        ethernet_carrier=False,
        signal_strength=0,
    )
    defaults.update(kw)
    return NetworkState(**defaults)


def _disconnected_state(**kw) -> NetworkState:
    defaults = dict(
        connectivity=ConnectivityState.NONE,
        current_ssid="",
        current_ip="",
        wifi_enabled=False,
        hotspot_enabled=False,
        ethernet_connected=False,
        ethernet_carrier=False,
    )
    defaults.update(kw)
    return NetworkState(**defaults)


def _wifi_on_no_conn_state(**kw) -> NetworkState:
    defaults = dict(
        connectivity=ConnectivityState.NONE,
        current_ssid="",
        current_ip="",
        wifi_enabled=True,
        hotspot_enabled=False,
        ethernet_connected=False,
        ethernet_carrier=False,
    )
    defaults.update(kw)
    return NetworkState(**defaults)


# ─────────────────────────────────────────────────────────────────────────────
# Initialisation
# ─────────────────────────────────────────────────────────────────────────────


class TestInitialisation:
    def test_window_created(self, win):
        w, _nm = win
        assert w is not None

    def test_loading_widget_hidden_on_init(self, win):
        w, _nm = win
        assert not w.loadingwidget.isVisible()

    def test_info_box_visible_on_init(self, win):
        w, _nm = win
        assert w.mn_info_box.isVisible()

    def test_ethernet_button_hidden_on_init(self, win):
        """Ethernet button is invisible until a cable is detected."""
        w, _nm = win
        assert not w.ethernet_button.isVisible()

    def test_is_first_run_true_on_init(self, win):
        w, _nm = win
        assert w._is_first_run is True

    def test_pending_operation_none_on_init(self, win):
        w, _nm = win
        assert w._pending_operation == PendingOperation.NONE


# ─────────────────────────────────────────────────────────────────────────────
# _handle_first_run
# ─────────────────────────────────────────────────────────────────────────────


class TestHandleFirstRun:
    def test_ethernet_connected_shows_connected_state(self, win):
        w, nm = win
        state = _eth_state()
        w._handle_first_run(state)
        assert w.netlist_ssuid.isVisible()
        assert w.netlist_ssuid.text() == "Ethernet"

    def test_ethernet_disables_wifi_if_enabled(self, win):
        w, nm = win
        state = _eth_state(wifi_enabled=True)
        w._handle_first_run(state)
        nm.set_wifi_enabled.assert_called_once_with(False)

    def test_ethernet_does_not_disable_wifi_if_already_off(self, win):
        w, nm = win
        state = _eth_state(wifi_enabled=False)
        w._handle_first_run(state)
        nm.set_wifi_enabled.assert_not_called()

    def test_ethernet_shows_button_when_carrier(self, win):
        w, nm = win
        state = _eth_state()
        w._handle_first_run(state)
        assert w.ethernet_button.isVisible()

    def test_wifi_full_connectivity_shows_connected(self, win):
        w, nm = win
        state = _wifi_state()
        w._handle_first_run(state)
        assert w.netlist_ssuid.isVisible()
        assert w.netlist_ssuid.text() == "HomeNet"

    def test_hotspot_active_shows_connected(self, win):
        w, nm = win
        state = _hotspot_state()
        w._handle_first_run(state)
        assert w.netlist_ssuid.isVisible()

    def test_wifi_on_no_ssid_shows_no_connection(self, win):
        w, nm = win
        state = _wifi_on_no_conn_state()
        w._handle_first_run(state)
        assert w.netlist_ssuid.isVisible()
        assert "No network" in w.netlist_ssuid.text()

    def test_disconnected_shows_info_box(self, win):
        w, nm = win
        state = _disconnected_state()
        w._handle_first_run(state)
        assert w.mn_info_box.isVisible()

    def test_first_run_clears_loading(self, win):
        w, nm = win
        w.loadingwidget.setVisible(True)
        w._handle_first_run(_wifi_state())
        assert not w.loadingwidget.isVisible()

    def test_first_run_clears_is_connecting(self, win):
        w, nm = win
        w._is_connecting = True
        w._handle_first_run(_wifi_state())
        assert not w._is_connecting

    def test_buttons_enabled_after_first_run(self, win):
        w, nm = win
        w._handle_first_run(_disconnected_state())
        assert w.wifi_button.isEnabled()
        assert w.hotspot_button.isEnabled()
        assert w.ethernet_button.isEnabled()


# ─────────────────────────────────────────────────────────────────────────────
# _display_connected_state
# ─────────────────────────────────────────────────────────────────────────────


class TestDisplayConnectedState:
    def test_ethernet_shows_ethernet_label(self, win):
        w, _ = win
        w._display_connected_state(_eth_state())
        assert w.netlist_ssuid.text() == "Ethernet"

    def test_ethernet_shows_ip(self, win):
        w, _ = win
        w._display_connected_state(_eth_state())
        assert "192.168.1.104" in w.netlist_ip.text()

    def test_ethernet_hides_signal_strength(self, win):
        """Signal/security widgets are Wi-Fi-only and must stay hidden for ethernet."""
        w, _ = win
        w._display_connected_state(_eth_state())
        assert not w.netlist_strength.isVisible()
        assert not w.netlist_security.isVisible()

    def test_wifi_shows_ssid(self, win):
        w, _ = win
        w._display_connected_state(_wifi_state())
        assert w.netlist_ssuid.text() == "HomeNet"

    def test_wifi_shows_ip(self, win):
        w, _ = win
        w._display_connected_state(_wifi_state())
        assert "192.168.1.50" in w.netlist_ip.text()

    def test_wifi_shows_signal_and_security(self, win):
        w, _ = win
        w._active_signal = 75
        w._display_connected_state(_wifi_state())
        assert w.netlist_strength.isVisible()
        assert w.netlist_security.isVisible()

    def test_missing_ip_shows_placeholder(self, win):
        w, _ = win
        w._display_connected_state(_wifi_state(current_ip=""))
        assert "IP: --" in w.netlist_ip.text()

    def test_separator_visible_on_connect(self, win):
        w, _ = win
        w._display_connected_state(_wifi_state())
        assert w.mn_info_seperator.isVisible()

    def test_hotspot_hides_signal_and_security(self, win):
        w, _ = win
        w._display_connected_state(_hotspot_state())
        assert not w.netlist_strength.isVisible()
        assert not w.netlist_security.isVisible()

    def test_info_box_hidden_on_connect(self, win):
        w, _ = win
        w._display_connected_state(_wifi_state())
        assert not w.mn_info_box.isVisible()

    def test_ethernet_hides_vlan_combo_when_no_vlans(self, win):
        w, _ = win
        w._display_connected_state(_eth_state())
        assert not w.netlist_vlans_combo.isVisible()


# ─────────────────────────────────────────────────────────────────────────────
# _display_disconnected_state
# ─────────────────────────────────────────────────────────────────────────────


class TestDisplayDisconnectedState:
    def test_info_box_visible(self, win):
        w, _ = win
        w._display_disconnected_state()
        assert w.mn_info_box.isVisible()

    def test_ssid_hidden(self, win):
        w, _ = win
        w._display_disconnected_state()
        assert not w.netlist_ssuid.isVisible()

    def test_ip_hidden(self, win):
        w, _ = win
        w._display_disconnected_state()
        assert not w.netlist_ip.isVisible()

    def test_loading_hidden(self, win):
        w, _ = win
        w.loadingwidget.setVisible(True)
        w._display_disconnected_state()
        assert not w.loadingwidget.isVisible()

    def test_buttons_enabled(self, win):
        w, _ = win
        w._display_disconnected_state()
        assert w.wifi_button.isEnabled()
        assert w.hotspot_button.isEnabled()


# ─────────────────────────────────────────────────────────────────────────────
# _display_wifi_on_no_connection
# ─────────────────────────────────────────────────────────────────────────────


class TestDisplayWifiOnNoConnection:
    def test_ssid_label_shows_no_network(self, win):
        w, _ = win
        w._display_wifi_on_no_connection()
        assert "No network" in w.netlist_ssuid.text()

    def test_ip_shows_placeholder(self, win):
        w, _ = win
        w._display_wifi_on_no_connection()
        assert "IP: --" in w.netlist_ip.text()

    def test_signal_and_security_visible(self, win):
        w, _ = win
        w._display_wifi_on_no_connection()
        assert w.netlist_strength.isVisible()
        assert w.netlist_security.isVisible()

    def test_info_box_hidden(self, win):
        w, _ = win
        w._display_wifi_on_no_connection()
        assert not w.mn_info_box.isVisible()


# ─────────────────────────────────────────────────────────────────────────────
# _sync_ethernet_panel
# ─────────────────────────────────────────────────────────────────────────────


class TestSyncEthernetPanel:
    def test_visible_when_carrier(self, win):
        w, _ = win
        w._sync_ethernet_panel(_eth_state(ethernet_carrier=True))
        assert w.ethernet_button.isVisible()

    def test_hidden_when_no_carrier(self, win):
        w, _ = win
        w._sync_ethernet_panel(_eth_state(ethernet_carrier=False))
        assert not w.ethernet_button.isVisible()

    def test_toggle_on_when_connected(self, win):
        w, _ = win
        w._sync_ethernet_panel(_eth_state())
        eth_btn = w.ethernet_button.toggle_button
        assert eth_btn.state == eth_btn.State.ON

    def test_toggle_off_when_not_connected(self, win):
        w, _ = win
        state = NetworkState(
            ethernet_connected=False,
            ethernet_carrier=True,
            connectivity=ConnectivityState.NONE,
        )
        w._sync_ethernet_panel(state)
        eth_btn = w.ethernet_button.toggle_button
        assert eth_btn.state == eth_btn.State.OFF


# ─────────────────────────────────────────────────────────────────────────────
# _set_loading_state / _clear_loading
# ─────────────────────────────────────────────────────────────────────────────


class TestLoadingState:
    def test_loading_true_shows_widget(self, win):
        w, _ = win
        w._set_loading_state(True)
        assert w.loadingwidget.isVisible()

    def test_loading_true_disables_buttons(self, win):
        w, _ = win
        w._set_loading_state(True)
        assert not w.wifi_button.isEnabled()
        assert not w.hotspot_button.isEnabled()
        assert not w.ethernet_button.isEnabled()

    def test_loading_true_sets_is_connecting(self, win):
        w, _ = win
        w._set_loading_state(True)
        assert w._is_connecting is True

    def test_clear_loading_hides_widget(self, win):
        w, _ = win
        w._set_loading_state(True)
        w._clear_loading()
        assert not w.loadingwidget.isVisible()

    def test_clear_loading_re_enables_buttons(self, win):
        w, _ = win
        w._set_loading_state(True)
        w._clear_loading()
        assert w.wifi_button.isEnabled()
        assert w.hotspot_button.isEnabled()
        assert w.ethernet_button.isEnabled()

    def test_clear_loading_clears_is_connecting(self, win):
        w, _ = win
        w._set_loading_state(True)
        w._clear_loading()
        assert w._is_connecting is False

    def test_clear_loading_resets_pending_operation(self, win):
        w, _ = win
        w._pending_operation = PendingOperation.CONNECT
        w._clear_loading()
        assert w._pending_operation == PendingOperation.NONE

    def test_custom_timeout_ms_parameter(self, win):
        """_set_loading_state(timeout_ms=50000) starts the timer with 50 s."""
        w, _ = win
        w._set_loading_state(True, timeout_ms=50000)
        assert w.loadingwidget.isVisible()
        # Timer should be active with the custom interval
        assert w._load_timer.isActive()
        assert w._load_timer.interval() == 50000


# ─────────────────────────────────────────────────────────────────────────────
# _on_reconnect_complete
# ─────────────────────────────────────────────────────────────────────────────


class TestReconnectComplete:
    def test_navigates_to_main_page(self, win, qapp):
        w, _ = win
        # Navigate away first
        w.setCurrentIndex(w.indexOf(w.network_list_page))
        qapp.processEvents()
        w._on_reconnect_complete()
        qapp.processEvents()
        assert w.currentIndex() == w.indexOf(w.main_network_page)


# ─────────────────────────────────────────────────────────────────────────────
# _on_network_state_changed — normal (not connecting) path
# ─────────────────────────────────────────────────────────────────────────────


class TestOnNetworkStateChangedNormal:
    def _prime(self, w):
        """Mark first-run as done so the normal display path runs."""
        w._is_first_run = False
        w._is_connecting = False
        w._was_ethernet_connected = False

    def test_ethernet_shows_connected(self, win):
        w, _ = win
        self._prime(w)
        w._on_network_state_changed(_eth_state())
        assert w.netlist_ssuid.text() == "Ethernet"

    def test_wifi_connected_shows_ssid(self, win):
        w, _ = win
        self._prime(w)
        w._on_network_state_changed(_wifi_state())
        assert w.netlist_ssuid.text() == "HomeNet"

    def test_wifi_on_no_connection(self, win):
        w, _ = win
        self._prime(w)
        w._on_network_state_changed(_wifi_on_no_conn_state())
        assert "No network" in w.netlist_ssuid.text()

    def test_disconnected_shows_info_box(self, win):
        w, _ = win
        self._prime(w)
        w._on_network_state_changed(_disconnected_state())
        assert w.mn_info_box.isVisible()

    def test_first_run_flag_cleared_after_first_call(self, win):
        w, _ = win
        assert w._is_first_run is True
        w._on_network_state_changed(_disconnected_state())
        assert w._is_first_run is False

    def test_ethernet_plug_disables_wifi(self, win):
        """Ethernet cable plugged in during Wi-Fi session -> Wi-Fi disabled."""
        w, nm = win
        self._prime(w)
        w._was_ethernet_connected = False
        state = _eth_state(wifi_enabled=True)
        w._on_network_state_changed(state)
        nm.set_wifi_enabled.assert_called_with(False)


# ─────────────────────────────────────────────────────────────────────────────
# _on_network_state_changed — loading state machine
# ─────────────────────────────────────────────────────────────────────────────


class TestLoadingStateMachine:
    def _start_loading(self, w, op: PendingOperation):
        w._is_first_run = False
        w._pending_operation = op
        w._is_connecting = True
        w.loadingwidget.setVisible(True)

    def test_wifi_off_clears_on_radio_down(self, win):
        w, _ = win
        self._start_loading(w, PendingOperation.WIFI_OFF)
        state = NetworkState(
            wifi_enabled=False,
            hotspot_enabled=False,
            current_ssid="",
            connectivity=ConnectivityState.NONE,
        )
        w._on_network_state_changed(state)
        assert not w.loadingwidget.isVisible()
        assert not w._is_connecting

    def test_hotspot_on_clears_on_active(self, win):
        w, _ = win
        self._start_loading(w, PendingOperation.HOTSPOT_ON)
        w._on_network_state_changed(_hotspot_state())
        assert not w.loadingwidget.isVisible()

    def test_wifi_connect_clears_on_ssid_and_ip(self, win):
        w, _ = win
        self._start_loading(w, PendingOperation.CONNECT)
        w._target_ssid = "HomeNet"
        w._on_network_state_changed(_wifi_state())
        assert not w.loadingwidget.isVisible()

    def test_wifi_connect_keeps_loading_for_wrong_ssid(self, win):
        w, _ = win
        self._start_loading(w, PendingOperation.CONNECT)
        w._target_ssid = "OtherNet"
        w._on_network_state_changed(_wifi_state())
        # Should still be loading — SSID doesn't match target
        assert w._is_connecting

    def test_ethernet_on_clears_on_connected(self, win):
        w, _ = win
        self._start_loading(w, PendingOperation.ETHERNET_ON)
        w._on_network_state_changed(_eth_state())
        assert not w.loadingwidget.isVisible()

    def test_ethernet_off_clears_on_disconnected(self, win):
        w, _ = win
        self._start_loading(w, PendingOperation.ETHERNET_OFF)
        w._on_network_state_changed(_disconnected_state())
        assert not w.loadingwidget.isVisible()

    def test_static_ip_clears_on_expected_ip(self, win):
        w, _ = win
        self._start_loading(w, PendingOperation.WIFI_STATIC_IP)
        w._pending_expected_ip = "10.0.0.50"
        state = _wifi_state(current_ip="10.0.0.50")
        w._on_network_state_changed(state)
        assert not w.loadingwidget.isVisible()

    def test_static_ip_keeps_loading_for_old_ip(self, win):
        """Old IP still arriving -> stay in loading until expected IP appears."""
        w, _ = win
        self._start_loading(w, PendingOperation.WIFI_STATIC_IP)
        w._pending_expected_ip = "10.0.0.50"
        state = _wifi_state(current_ip="192.168.1.50")
        w._on_network_state_changed(state)
        assert w._is_connecting

    def test_vlan_dhcp_keeps_loading_even_with_ethernet(self, win):
        """VLAN DHCP must NOT clear loading when ethernet is already connected.

        This is the core fix — the old code used ETHERNET_ON which
        cleared immediately because ethernet was already up.
        """
        w, _ = win
        self._start_loading(w, PendingOperation.VLAN_DHCP)
        w._on_network_state_changed(_eth_state())
        # Loading MUST stay visible — VLAN DHCP is still in progress
        assert w._is_connecting
        assert w.loadingwidget.isVisible()

    def test_vlan_dhcp_syncs_ethernet_panel(self, win):
        """While VLAN DHCP loading is visible, the ethernet panel must update."""
        w, _ = win
        self._start_loading(w, PendingOperation.VLAN_DHCP)
        with patch.object(w, "_sync_ethernet_panel") as mock_sync:
            w._on_network_state_changed(_eth_state())
            mock_sync.assert_called()


# ─────────────────────────────────────────────────────────────────────────────
# _on_operation_complete
# ─────────────────────────────────────────────────────────────────────────────


class TestOnOperationComplete:
    def test_success_delete_navigates_to_main(self, win, qapp):
        w, nm = win
        w._is_first_run = False
        nm.current_state = NetworkState(wifi_enabled=True)
        result = ConnectionResult(success=True, message="Network deleted")
        w._on_operation_complete(result)
        qapp.processEvents()
        assert w.currentIndex() == w.indexOf(w.main_network_page)

    def test_success_delete_patches_cache_to_discovered(self, win, qapp):
        w, nm = win
        w._is_first_run = False
        nm.current_state = NetworkState(wifi_enabled=True)
        w._cached_scan_networks = [
            NetworkInfo(ssid="OldNet", network_status=NetworkStatus.SAVED)
        ]
        w._item_cache["OldNet"] = (4, "Saved", MagicMock())
        w._target_ssid = "OldNet"
        result = ConnectionResult(success=True, message="Network deleted")
        w._on_operation_complete(result)
        qapp.processEvents()
        patched = [n for n in w._cached_scan_networks if n.ssid == "OldNet"]
        assert patched[0].network_status == NetworkStatus.DISCOVERED
        # cache re-populated by rebuild with new status label
        if "OldNet" in w._item_cache:
            assert w._item_cache["OldNet"][1] == NetworkStatus.DISCOVERED.label

    def test_success_added_patches_cache_to_saved(self, win):
        w, _ = win
        w._is_first_run = False
        w._cached_scan_networks = [
            NetworkInfo(ssid="HomeNet", network_status=NetworkStatus.DISCOVERED)
        ]
        w._item_cache["HomeNet"] = (3, "Protected", MagicMock())
        w._target_ssid = "HomeNet"
        w._current_network_is_hidden = False
        result = ConnectionResult(success=True, message="HomeNet added and connecting")
        w._on_operation_complete(result)
        patched = [n for n in w._cached_scan_networks if n.ssid == "HomeNet"]
        assert patched[0].network_status == NetworkStatus.SAVED
        # cache re-populated by rebuild with new status label
        if "HomeNet" in w._item_cache:
            assert w._item_cache["HomeNet"][1] == NetworkStatus.SAVED.label

    def test_success_config_updated_shows_popup(self, win):
        w, _ = win
        w._is_first_run = False
        result = ConnectionResult(success=True, message="Config updated")
        with patch.object(w, "_show_info_popup") as mock_popup:
            w._on_operation_complete(result)
            mock_popup.assert_called_once()

    def test_failure_shows_error_popup(self, win):
        w, _ = win
        w._is_first_run = False
        w._is_connecting = True
        result = ConnectionResult(
            success=False, message="Auth failed", error_code="auth_failed"
        )
        with patch.object(w, "_show_error_popup") as mock_err:
            w._on_operation_complete(result)
            mock_err.assert_called_once()

    def test_failure_clears_loading(self, win):
        w, _ = win
        w._is_first_run = False
        w._is_connecting = True
        w.loadingwidget.setVisible(True)
        result = ConnectionResult(success=False, message="Failed", error_code="err")
        w._on_operation_complete(result)
        assert not w.loadingwidget.isVisible()

    def test_vlan_dhcp_timeout_shows_error(self, win):
        w, _ = win
        w._is_first_run = False
        result = ConnectionResult(
            success=False,
            message="No DHCP server",
            error_code="vlan_dhcp_timeout",
        )
        with patch.object(w, "_show_error_popup") as mock_err:
            w._on_operation_complete(result)
            mock_err.assert_called_once()

    def test_vlan_dhcp_timeout_clears_loading(self, win):
        """VLAN DHCP timeout must clear loading state."""
        w, _ = win
        w._is_first_run = False
        w._is_connecting = True
        w._pending_operation = PendingOperation.VLAN_DHCP
        w.loadingwidget.setVisible(True)
        result = ConnectionResult(
            success=False,
            message="No DHCP server",
            error_code="vlan_dhcp_timeout",
        )
        w._on_operation_complete(result)
        assert not w.loadingwidget.isVisible()
        assert not w._is_connecting

    def test_vlan_dhcp_success_clears_loading(self, win):
        """Successful VLAN DHCP must clear loading and update display."""
        w, nm = win
        w._is_first_run = False
        w._is_connecting = True
        w._pending_operation = PendingOperation.VLAN_DHCP
        w.loadingwidget.setVisible(True)
        nm.current_state = _eth_state()
        result = ConnectionResult(success=True, message="VLAN 100 connected")
        with patch.object(w, "_display_connected_state") as mock_disp:
            with patch.object(w, "_show_info_popup") as mock_info:
                w._on_operation_complete(result)
                mock_disp.assert_called_once()
                mock_info.assert_called_once_with("VLAN 100 connected")
        assert not w.loadingwidget.isVisible()
        assert not w._is_connecting

    def test_transient_mismatch_retries(self, win, qapp):
        """NM device-mismatch error during Wi-Fi connect -> retry scheduled."""
        w, nm = win
        w._is_first_run = False
        w._is_connecting = True
        w._pending_operation = PendingOperation.CONNECT
        w._target_ssid = "HomeNet"
        result = ConnectionResult(
            success=False,
            message="not compatible with device",
            error_code="nm_error",
        )
        with patch("BlocksScreen.lib.panels.networkWindow.QTimer") as mock_timer:
            w._on_operation_complete(result)
            mock_timer.singleShot.assert_called_once()
        # Loading should still be visible — retry is pending
        assert w._is_connecting


# ─────────────────────────────────────────────────────────────────────────────
# Toggle handlers
# ─────────────────────────────────────────────────────────────────────────────


class TestWifiToggle:
    def test_wifi_off_calls_set_wifi_enabled_false(self, win):
        w, nm = win
        w._handle_wifi_toggle(False)
        nm.set_wifi_enabled.assert_called_once_with(False)

    def test_wifi_off_sets_pending_operation(self, win):
        w, nm = win
        w._handle_wifi_toggle(False)
        assert w._pending_operation == PendingOperation.WIFI_OFF

    def test_wifi_off_shows_loading(self, win):
        w, nm = win
        w._handle_wifi_toggle(False)
        assert w.loadingwidget.isVisible()

    def test_wifi_on_no_saved_networks_shows_warning(self, win):
        w, nm = win
        nm.saved_networks = []
        with patch.object(w, "_show_warning_popup") as mock_warn:
            w._handle_wifi_toggle(True)
            mock_warn.assert_called_once()

    def test_wifi_on_with_saved_networks_starts_connect(self, win):
        w, nm = win
        saved = [
            SavedNetwork(
                ssid="HomeNet",
                uuid="abc",
                connection_path="/path/1",
                security_type="wpa-psk",
                mode="infrastructure",
            )
        ]
        nm.saved_networks = saved
        with patch("BlocksScreen.lib.panels.networkWindow.QTimer") as mock_timer:
            w._handle_wifi_toggle(True)
            mock_timer.singleShot.assert_called()
        assert w._pending_operation == PendingOperation.WIFI_ON

    def test_wifi_on_calls_set_wifi_enabled(self, win):
        w, nm = win
        nm.saved_networks = []
        w._handle_wifi_toggle(True)
        nm.set_wifi_enabled.assert_called_once_with(True)


class TestHotspotToggle:
    def test_hotspot_off_calls_toggle_hotspot_false(self, win):
        w, nm = win
        w._handle_hotspot_toggle(False)
        nm.toggle_hotspot.assert_called_once_with(False)

    def test_hotspot_off_shows_loading(self, win):
        w, nm = win
        w._handle_hotspot_toggle(False)
        assert w.loadingwidget.isVisible()

    def test_hotspot_on_creates_hotspot(self, win):
        w, nm = win
        w._handle_hotspot_toggle(True)
        nm.create_hotspot.assert_called_once()

    def test_hotspot_on_sets_pending_operation(self, win):
        w, nm = win
        w._handle_hotspot_toggle(True)
        assert w._pending_operation == PendingOperation.HOTSPOT_ON

    def test_hotspot_on_sets_loading(self, win):
        w, nm = win
        w._handle_hotspot_toggle(True)
        assert w.loadingwidget.isVisible()


class TestEthernetToggle:
    def test_ethernet_on_calls_connect_ethernet(self, win):
        w, nm = win
        w._handle_ethernet_toggle(True)
        nm.connect_ethernet.assert_called_once()

    def test_ethernet_on_sets_pending_ethernet_on(self, win):
        w, nm = win
        w._handle_ethernet_toggle(True)
        assert w._pending_operation == PendingOperation.ETHERNET_ON

    def test_ethernet_off_calls_disconnect_ethernet(self, win):
        w, nm = win
        w._handle_ethernet_toggle(False)
        nm.disconnect_ethernet.assert_called_once()

    def test_ethernet_off_sets_pending_ethernet_off(self, win):
        w, nm = win
        w._handle_ethernet_toggle(False)
        assert w._pending_operation == PendingOperation.ETHERNET_OFF


# ─────────────────────────────────────────────────────────────────────────────
# _emit_status_icon
# ─────────────────────────────────────────────────────────────────────────────


class TestEmitStatusIcon:
    def _capture_icon(self, w, state):
        emitted = []
        w.update_wifi_icon.connect(lambda v: emitted.append(v))
        w._emit_status_icon(state)
        return emitted[-1] if emitted else None

    def test_ethernet_emits_ethernet_key(self, win):
        w, _ = win
        key = self._capture_icon(w, _eth_state())
        assert key == WifiIconKey.ETHERNET

    def test_hotspot_emits_hotspot_key(self, win):
        w, _ = win
        key = self._capture_icon(w, _hotspot_state())
        assert key == WifiIconKey.HOTSPOT

    def test_wifi_connected_emits_signal_key(self, win):
        w, _ = win
        w._active_signal = 75
        key = self._capture_icon(w, _wifi_state())
        # Should be a WifiIconKey, not ethernet or hotspot sentinel
        assert key != WifiIconKey.ETHERNET
        assert key != WifiIconKey.HOTSPOT
        assert key >= 0

    def test_disconnected_emits_zero_bar_key(self, win):
        w, _ = win
        w._active_signal = 0
        key = self._capture_icon(w, _disconnected_state())
        assert key == WifiIconKey.from_bars(0, False)


# ─────────────────────────────────────────────────────────────────────────────
# _handle_load_timeout
# ─────────────────────────────────────────────────────────────────────────────


class TestHandleLoadTimeout:
    def _setup(self, w, nm, op: PendingOperation, state: NetworkState):
        w._is_first_run = False
        w._is_connecting = True
        w._pending_operation = op
        w.loadingwidget.setVisible(True)
        nm.current_state = state

    def test_hotspot_on_timeout_accepts_if_active(self, win):
        w, nm = win
        self._setup(w, nm, PendingOperation.HOTSPOT_ON, _hotspot_state())
        w._handle_load_timeout()
        assert not w.loadingwidget.isVisible()

    def test_wifi_connect_timeout_accepts_if_ssid_matches(self, win):
        w, nm = win
        self._setup(w, nm, PendingOperation.WIFI_ON, _wifi_state())
        w._target_ssid = "HomeNet"
        w._handle_load_timeout()
        assert not w.loadingwidget.isVisible()

    def test_ethernet_on_timeout_accepts_if_connected(self, win):
        w, nm = win
        self._setup(w, nm, PendingOperation.ETHERNET_ON, _eth_state())
        w._handle_load_timeout()
        assert not w.loadingwidget.isVisible()

    def test_static_ip_timeout_accepts_any_ip(self, win):
        w, nm = win
        self._setup(w, nm, PendingOperation.WIFI_STATIC_IP, _wifi_state())
        w._handle_load_timeout()
        assert not w.loadingwidget.isVisible()

    def test_generic_timeout_shows_error_popup(self, win):
        w, nm = win
        self._setup(w, nm, PendingOperation.NONE, _disconnected_state())
        with patch.object(w, "_show_error_popup") as mock_err:
            w._handle_load_timeout()
            mock_err.assert_called_once()
        assert not w.loadingwidget.isVisible()

    def test_vlan_dhcp_timeout_shows_specific_error(self, win):
        """50 s UI timer fires before worker's 45 s signal timeout."""
        w, nm = win
        self._setup(w, nm, PendingOperation.VLAN_DHCP, _eth_state())
        with patch.object(w, "_show_error_popup") as mock_err:
            w._handle_load_timeout()
            mock_err.assert_called_once()
            assert "VLAN DHCP" in mock_err.call_args[0][0]
        assert not w.loadingwidget.isVisible()


# ─────────────────────────────────────────────────────────────────────────────
# _on_network_error
# ─────────────────────────────────────────────────────────────────────────────


class TestOnVlanApply:
    """Verify _on_vlan_apply routes DHCP -> VLAN_DHCP and static -> ETHERNET_ON."""

    def test_dhcp_mode_sets_vlan_dhcp_pending(self, win):
        w, nm = win
        w._is_first_run = False
        w.vlan_id_spinbox.setValue(100)
        w.vlan_ip_field.setText("")  # empty IP -> DHCP
        w._on_vlan_apply()
        assert w._pending_operation == PendingOperation.VLAN_DHCP
        assert w._is_connecting
        nm.create_vlan_connection.assert_called_once_with(100, "", "", "", "", "")

    def test_static_ip_mode_sets_ethernet_on_pending(self, win):
        w, nm = win
        w._is_first_run = False
        w.vlan_ip_field.setText("10.0.0.1")
        w.vlan_mask_field.setText("255.255.255.0")
        # Mock validation to pass
        w.vlan_ip_field.is_valid = MagicMock(return_value=True)
        w.vlan_mask_field.is_valid_mask = MagicMock(return_value=True)
        w._on_vlan_apply()
        assert w._pending_operation == PendingOperation.ETHERNET_ON

    def test_dhcp_mode_uses_longer_timeout(self, win):
        """VLAN DHCP loading must use VLAN_DHCP_TIMEOUT_MS (50 s)."""
        w, nm = win
        w._is_first_run = False
        w.vlan_ip_field.setText("")  # DHCP
        w._on_vlan_apply()
        assert w._load_timer.interval() == 50000


class TestOnNetworkError:
    def test_shows_error_popup(self, win):
        w, _ = win
        with patch.object(w, "_show_error_popup") as mock_err:
            w._on_network_error("connect", "D-Bus timeout")
            mock_err.assert_called_once()

    def test_clears_loading(self, win):
        w, _ = win
        w._is_connecting = True
        w.loadingwidget.setVisible(True)
        w._on_network_error("scan", "bus error")
        assert not w.loadingwidget.isVisible()


# ─────────────────────────────────────────────────────────────────────────────
# _setupUI smoke test — covers ~1 200 statements in _setupUI + page helpers
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestSetupUIRunsWithoutError:
    """Calling _setupUI() must not raise — covers the entire UI construction path."""

    def test_setup_ui_completes(self, qapp):
        from unittest.mock import patch

        from PyQt6 import QtWidgets

        from BlocksScreen.lib.panels.networkWindow import NetworkControlWindow

        def _stub_init(self, *_a, **_kw):
            QtWidgets.QStackedWidget.__init__(self)

        with patch.object(NetworkControlWindow, "__init__", _stub_init):
            w = NetworkControlWindow()

        w._setupUI()
        assert w.main_network_page is not None
        assert w.network_list_page is not None
        assert w.add_network_page is not None
        assert w.saved_connection_page is not None
        assert w.wifi_static_ip_page is not None


# ─────────────────────────────────────────────────────────────────────────────
# Step 4a: Helper classes — PixmapCache, WifiIconProvider, IPAddressLineEdit
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestHelperClasses:
    def test_pixmap_cache_get_loads_and_caches(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import PixmapCache

        PixmapCache._cache.clear()
        px1 = PixmapCache.get(":/some/test/path.svg")
        px2 = PixmapCache.get(":/some/test/path.svg")
        assert px2 is px1  # same object from cache

    def test_pixmap_cache_preload_calls_get(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import PixmapCache

        PixmapCache._cache.clear()
        paths = [":/path/a.svg", ":/path/b.svg"]
        PixmapCache.preload(paths)
        assert ":/path/a.svg" in PixmapCache._cache
        assert ":/path/b.svg" in PixmapCache._cache

    def test_wifi_icon_provider_get_pixmap(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import WifiIconProvider

        px = WifiIconProvider.get_pixmap(75, is_protected=True)
        assert px is not None  # returns a QPixmap (even if null in offscreen)

    def test_ip_line_edit_is_valid_true(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import IPAddressLineEdit

        field = IPAddressLineEdit()
        field.setText("192.168.1.1")
        assert field.is_valid() is True

    def test_ip_line_edit_is_valid_false(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import IPAddressLineEdit

        field = IPAddressLineEdit()
        field.setText("999.999.999.999")
        assert field.is_valid() is False

    def test_ip_line_edit_is_valid_mask_prefix(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import IPAddressLineEdit

        field = IPAddressLineEdit()
        field.setText("24")
        assert field.is_valid_mask() is True

    def test_ip_line_edit_is_valid_mask_dotted(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import IPAddressLineEdit

        field = IPAddressLineEdit()
        field.setText("255.255.255.0")
        assert field.is_valid_mask() is True

    def test_ip_line_edit_is_valid_mask_out_of_range(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import IPAddressLineEdit

        field = IPAddressLineEdit()
        field.setText("33")
        assert field.is_valid_mask() is False

    def test_ip_line_edit_text_changed_empty(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import IPAddressLineEdit

        field = IPAddressLineEdit()
        field.setText("")
        # Empty text -> valid style (no error border)
        assert "red" not in field.styleSheet()

    def test_ip_line_edit_text_changed_valid(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import IPAddressLineEdit

        field = IPAddressLineEdit()
        field.setText("10.0.0.1")
        assert "red" not in field.styleSheet()

    def test_ip_line_edit_text_changed_invalid(self, qapp):
        from BlocksScreen.lib.panels.networkWindow import IPAddressLineEdit

        field = IPAddressLineEdit()
        field.setText("999.999.999.999")
        assert "red" in field.styleSheet()


# ─────────────────────────────────────────────────────────────────────────────
# Step 4b: _on_hotspot_config_save
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestOnHotspotConfigSave:
    def test_empty_name_shows_error(self, win):
        w, nm = win
        w.hotspot_name_input_field.setText("")
        w.hotspot_password_input_field.setText("password123")
        with patch.object(w, "_show_error_popup") as mock_err:
            w._on_hotspot_config_save()
            mock_err.assert_called_once()
        nm.update_hotspot_config.assert_not_called()

    def test_short_password_shows_error(self, win):
        w, nm = win
        w.hotspot_name_input_field.setText("MyHotspot")
        w.hotspot_password_input_field.setText("short")
        with patch.object(w, "_show_error_popup") as mock_err:
            w._on_hotspot_config_save()
            mock_err.assert_called_once()
        nm.update_hotspot_config.assert_not_called()

    def test_success_with_hotspot_inactive(self, win):
        w, nm = win
        w.hotspot_name_input_field.setText("MyHotspot")
        w.hotspot_password_input_field.setText("validpass")
        w.hotspot_button.toggle_button.state = w.hotspot_button.toggle_button.State.OFF
        w._on_hotspot_config_save()
        nm.update_hotspot_config.assert_called_once()
        # No loading overlay shown
        assert not w.loadingwidget.isVisible()

    def test_success_with_hotspot_active(self, win):
        w, nm = win
        w.hotspot_name_input_field.setText("MyHotspot")
        w.hotspot_password_input_field.setText("validpass")
        w.hotspot_button.toggle_button.state = w.hotspot_button.toggle_button.State.ON
        w._on_hotspot_config_save()
        nm.update_hotspot_config.assert_called_once()
        assert w.loadingwidget.isVisible()


# ─────────────────────────────────────────────────────────────────────────────
# Step 4c: _on_vlan_delete
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestOnVlanDelete:
    def test_calls_delete_and_shows_warning(self, win):
        w, nm = win
        w.vlan_id_spinbox.setValue(100)
        with patch.object(w, "_show_warning_popup") as mock_warn:
            w._on_vlan_delete()
            nm.delete_vlan_connection.assert_called_once_with(100)
            mock_warn.assert_called_once()
            assert "100" in mock_warn.call_args[0][0]


# ─────────────────────────────────────────────────────────────────────────────
# Step 4d: _on_interface_combo_changed
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestOnInterfaceComboChanged:
    def test_updates_ip_with_valid_ip(self, win):
        w, _ = win
        w.netlist_vlans_combo.addItem("eth0.100", "10.0.0.1")
        w._on_interface_combo_changed(0)
        assert "10.0.0.1" in w.netlist_ip.text()

    def test_shows_dashes_for_empty_ip(self, win):
        w, _ = win
        w.netlist_vlans_combo.addItem("eth0 (no IP)", "")
        w._on_interface_combo_changed(0)
        assert "IP: --" in w.netlist_ip.text()


# ─────────────────────────────────────────────────────────────────────────────
# Step 4e: _on_scan_complete
# ─────────────────────────────────────────────────────────────────────────────


def _make_network_info(**kw) -> NetworkInfo:
    defaults = dict(
        ssid="TestNet",
        signal_strength=75,
        network_status=NetworkStatus.DISCOVERED,
        bssid="AA:BB:CC:DD:EE:FF",
        frequency=2437,
        max_bitrate=54000,
        security_type=SecurityType.WPA2_PSK,
    )
    defaults.update(kw)
    return NetworkInfo(**defaults)


@pytest.mark.unit
class TestOnScanComplete:
    def test_filters_hotspot_ssid(self, win):
        w, nm = win
        nm.hotspot_ssid = "PrinterHotspot"
        nm.current_ssid = None
        nm.current_state = NetworkState()
        networks = [
            _make_network_info(ssid="PrinterHotspot"),
            _make_network_info(ssid="HomeNet"),
        ]
        w._on_scan_complete(networks)
        assert all(n.ssid != "PrinterHotspot" for n in w._cached_scan_networks)

    def test_updates_cached_networks(self, win):
        w, nm = win
        nm.hotspot_ssid = "Hotspot"
        nm.current_ssid = None
        nm.current_state = NetworkState()
        networks = [_make_network_info(ssid="Net1"), _make_network_info(ssid="Net2")]
        w._on_scan_complete(networks)
        ssids = {n.ssid for n in w._cached_scan_networks}
        assert "Net1" in ssids
        assert "Net2" in ssids

    def test_updates_signal_text_when_connected(self, win):
        w, nm = win
        nm.hotspot_ssid = "Hotspot"
        nm.current_ssid = "HomeNet"
        nm.current_state = NetworkState(current_ssid="HomeNet", wifi_enabled=True)
        networks = [
            _make_network_info(
                ssid="HomeNet", signal_strength=80, network_status=NetworkStatus.ACTIVE
            )
        ]
        w._on_scan_complete(networks)
        assert w._active_signal == 80
        assert "80" in w.netlist_strength.text()


# ─────────────────────────────────────────────────────────────────────────────
# Step 4f: _sync_active_network_list_icon
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestSyncActiveNetworkListIcon:
    def test_no_scan_networks_resets_bars(self, win):
        w, _ = win
        w._cached_scan_networks = []
        w._last_active_signal_bars = 3
        state = NetworkState(current_ssid="HomeNet")
        w._sync_active_network_list_icon(state)
        assert w._last_active_signal_bars == -1

    def test_same_bars_and_active_status_skips_rebuild(self, win):
        w, _ = win
        w._active_signal = 75
        w._last_active_signal_bars = signal_to_bars(75)
        w._cached_scan_networks = [
            _make_network_info(
                ssid="HomeNet",
                signal_strength=75,
                network_status=NetworkStatus.ACTIVE,
            )
        ]
        state = NetworkState(current_ssid="HomeNet")
        bars_before = w._last_active_signal_bars
        with patch.object(w, "_build_network_list_from_scan") as mock_build:
            w._sync_active_network_list_icon(state)
            mock_build.assert_not_called()
        assert w._last_active_signal_bars == bars_before

    def test_same_bars_but_stale_saved_status_triggers_rebuild(self, win):
        """Scan ran before connection established; status must update SAVED→ACTIVE."""
        w, _ = win
        w._active_signal = 75
        w._last_active_signal_bars = signal_to_bars(75)
        w._cached_scan_networks = [
            _make_network_info(
                ssid="HomeNet",
                signal_strength=75,
                network_status=NetworkStatus.SAVED,
            )
        ]
        state = NetworkState(current_ssid="HomeNet")
        with patch.object(w, "_build_network_list_from_scan") as mock_build:
            w._sync_active_network_list_icon(state)
            mock_build.assert_called_once()
        assert w._cached_scan_networks[0].network_status == NetworkStatus.ACTIVE

    def test_same_bars_but_discovered_status_triggers_rebuild(self, win):
        """Connected AP not yet saved should still show ACTIVE when connected."""
        w, _ = win
        w._active_signal = 75
        w._last_active_signal_bars = signal_to_bars(75)
        w._cached_scan_networks = [
            _make_network_info(
                ssid="HomeNet",
                signal_strength=75,
                network_status=NetworkStatus.DISCOVERED,
            )
        ]
        state = NetworkState(current_ssid="HomeNet")
        with patch.object(w, "_build_network_list_from_scan") as mock_build:
            w._sync_active_network_list_icon(state)
            mock_build.assert_called_once()
        assert w._cached_scan_networks[0].network_status == NetworkStatus.ACTIVE

    def test_bar_change_triggers_rebuild(self, win):
        w, _ = win
        w._active_signal = 95  # 4 bars
        w._last_active_signal_bars = 1  # different
        w._cached_scan_networks = [
            _make_network_info(ssid="HomeNet", signal_strength=30)
        ]
        state = NetworkState(current_ssid="HomeNet")
        with patch.object(w, "_build_network_list_from_scan") as mock_build:
            w._sync_active_network_list_icon(state)
            mock_build.assert_called_once()


# ─────────────────────────────────────────────────────────────────────────────
# Step 4g: _build_network_list_from_scan
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestBuildNetworkListFromScan:
    def test_empty_list_builds_only_hidden_entry(self, win):
        w, _ = win
        w._build_network_list_from_scan([])
        # model should have exactly 1 item: the hidden-network sentinel
        assert len(w._model.entries) == 1
        assert (
            "Hidden" in w._model.entries[0].text
            or "hidden" in w._model.entries[0].text.lower()
        )

    def test_saved_and_unsaved_adds_separator(self, win):
        w, nm = win
        saved_net = _make_network_info(
            ssid="SavedNet", network_status=NetworkStatus.SAVED
        )
        unsaved_net = _make_network_info(
            ssid="UnsavedNet", network_status=NetworkStatus.DISCOVERED
        )
        w._build_network_list_from_scan([saved_net, unsaved_net])
        # separator + hidden entry should be present
        texts = [item.text for item in w._model.entries]
        assert "" in texts  # separator has empty text

    def test_stale_cache_entries_evicted(self, win):
        w, _ = win
        # Pre-populate cache with a network that won't appear in scan
        from tests.network.conftest import _ListItemStub

        w._item_cache["OldNet"] = (2, "Saved", _ListItemStub(text="OldNet"))
        w._build_network_list_from_scan([_make_network_info(ssid="NewNet")])
        assert "OldNet" not in w._item_cache

    def test_hidden_ssid_skipped(self, win):
        w, _ = win
        # NetworkStatus.HIDDEN marks a placeholder for hidden networks
        net = _make_network_info(ssid="hidden_net", network_status=NetworkStatus.HIDDEN)
        w._build_network_list_from_scan([net])
        # Only the hidden-network sentinel should remain; the HIDDEN entry is skipped
        texts = [item.text for item in w._model.entries]
        assert "hidden_net" not in texts

    def test_returns_cached_item_if_unchanged(self, win):
        w, _ = win
        net = _make_network_info(ssid="StableNet", signal_strength=75)
        w._build_network_list_from_scan([net])
        first_item = w._item_cache.get("StableNet")
        w._build_network_list_from_scan([net])
        second_item = w._item_cache.get("StableNet")
        # Same (bars, status) → same ListItem object reused
        assert first_item is second_item


# ─────────────────────────────────────────────────────────────────────────────
# Step 4h: _on_ssid_item_clicked
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestOnSsidItemClicked:
    def _make_item(self, text: str):
        from tests.network.conftest import _ListItemStub

        return _ListItemStub(text=text)

    def test_hidden_network_navigates_to_hidden_page(self, win):
        w, _ = win
        hidden_idx = w.indexOf(w.hidden_network_page)
        with patch.object(type(w), "setCurrentIndex") as mock_set:
            w._on_ssid_item_clicked(self._make_item("Connect to Hidden Network..."))
            mock_set.assert_called_with(hidden_idx)

    def test_no_network_info_returns_early(self, win):
        w, nm = win
        nm.get_network_info.return_value = None
        with patch.object(w, "_show_saved_network_page") as mock_saved:
            w._on_ssid_item_clicked(self._make_item("SomeNet"))
            mock_saved.assert_not_called()

    def test_unsupported_security_shows_error(self, win):
        w, nm = win
        net = _make_network_info(ssid="WepNet", security_type=SecurityType.WEP)
        nm.get_network_info.return_value = net
        with patch.object(w, "_show_error_popup") as mock_err:
            w._on_ssid_item_clicked(self._make_item("WepNet"))
            mock_err.assert_called_once()

    def test_saved_network_shows_saved_page(self, win):
        w, nm = win
        net = _make_network_info(ssid="SavedNet", network_status=NetworkStatus.SAVED)
        nm.get_network_info.return_value = net
        nm.get_saved_network.return_value = None
        nm.current_ssid = None
        with patch.object(w, "_show_saved_network_page") as mock_saved:
            w._on_ssid_item_clicked(self._make_item("SavedNet"))
            mock_saved.assert_called_once_with(net)

    def test_unsaved_network_shows_add_page(self, win):
        w, nm = win
        net = _make_network_info(ssid="NewNet", network_status=NetworkStatus.DISCOVERED)
        nm.get_network_info.return_value = net
        with patch.object(w, "_show_add_network_page") as mock_add:
            w._on_ssid_item_clicked(self._make_item("NewNet"))
            mock_add.assert_called_once_with(net)


# ─────────────────────────────────────────────────────────────────────────────
# Step 4i: _show_saved_network_page
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestShowSavedNetworkPage:
    def test_populates_ssid_labels(self, win):
        w, nm = win
        nm.get_saved_network.return_value = None
        nm.current_ssid = None
        net = _make_network_info(ssid="HomeNet", signal_strength=60)
        with patch.object(type(w), "setCurrentIndex"):
            w._show_saved_network_page(net)
        assert w.saved_connection_network_name.text() == "HomeNet"
        assert w.snd_name.text() == "HomeNet"

    def test_sets_signal_from_active_signal(self, win):
        w, nm = win
        nm.get_saved_network.return_value = None
        nm.current_ssid = "HomeNet"
        w._active_signal = 85
        net = _make_network_info(ssid="HomeNet", signal_strength=60)
        with patch.object(type(w), "setCurrentIndex"):
            w._show_saved_network_page(net)
        assert w.saved_connection_signal_strength_info_frame.text() == "85%"

    def test_non_active_uses_network_signal(self, win):
        w, nm = win
        nm.get_saved_network.return_value = None
        nm.current_ssid = "OtherNet"
        w._active_signal = 85
        net = _make_network_info(ssid="HomeNet", signal_strength=60)
        with patch.object(type(w), "setCurrentIndex"):
            w._show_saved_network_page(net)
        assert w.saved_connection_signal_strength_info_frame.text() == "60%"

    def test_open_network_shows_open_label(self, win):
        w, nm = win
        nm.get_saved_network.return_value = None
        nm.current_ssid = None
        net = _make_network_info(ssid="OpenNet", security_type=SecurityType.OPEN)
        with patch.object(type(w), "setCurrentIndex"):
            w._show_saved_network_page(net)
        assert w.saved_connection_security_type_info_label.text() == "OPEN"

    def test_active_network_disables_activate_button(self, win):
        w, nm = win
        nm.get_saved_network.return_value = None
        nm.current_ssid = "ActiveNet"
        net = _make_network_info(ssid="ActiveNet", network_status=NetworkStatus.ACTIVE)
        with patch.object(type(w), "setCurrentIndex"):
            w._show_saved_network_page(net)
        assert not w.network_activate_btn.isEnabled()

    def test_no_saved_record_sets_medium_priority(self, win):
        w, nm = win
        nm.get_saved_network.return_value = None
        nm.current_ssid = None
        net = _make_network_info(ssid="AnyNet")
        with patch.object(type(w), "setCurrentIndex"):
            w._show_saved_network_page(net)
        assert w._initial_priority == ConnectionPriority.MEDIUM


# ─────────────────────────────────────────────────────────────────────────────
# Step 4j: _show_add_network_page
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestShowAddNetworkPage:
    def test_populates_ssid_label(self, win):
        w, _ = win
        net = _make_network_info(ssid="CafeNet")
        with patch.object(type(w), "setCurrentIndex"):
            w._show_add_network_page(net)
        assert w.add_network_network_label.text() == "CafeNet"

    def test_open_network_hides_password_frame(self, win):
        w, _ = win
        net = _make_network_info(ssid="OpenCafe", security_type=SecurityType.OPEN)
        with patch.object(type(w), "setCurrentIndex"):
            w._show_add_network_page(net)
        assert not w.frame_2.isVisible()

    def test_secured_network_shows_password_frame(self, win):
        w, _ = win
        net = _make_network_info(ssid="SecuredNet", security_type=SecurityType.WPA2_PSK)
        with patch.object(type(w), "setCurrentIndex"):
            w._show_add_network_page(net)
        assert w.frame_2.isVisible()

    def test_sets_connect_text_for_open_network(self, win):
        w, _ = win
        net = _make_network_info(ssid="OpenNet", security_type=SecurityType.OPEN)
        with patch.object(type(w), "setCurrentIndex"):
            w._show_add_network_page(net)
        assert w.add_network_validation_button.text() == "Connect"

    def test_sets_activate_text_for_secured_network(self, win):
        w, _ = win
        net = _make_network_info(ssid="SecNet", security_type=SecurityType.WPA2_PSK)
        with patch.object(type(w), "setCurrentIndex"):
            w._show_add_network_page(net)
        assert w.add_network_validation_button.text() == "Activate"


# ─────────────────────────────────────────────────────────────────────────────
# Step 4k: _add_network
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestAddNetwork:
    def test_empty_password_for_secured_shows_error(self, win):
        w, nm = win
        w._current_network_is_open = False
        w.add_network_network_label.setText("SecNet")
        w.add_network_password_field.setText("")
        with patch.object(w, "_show_error_popup") as mock_err:
            w._add_network()
            mock_err.assert_called_once()
        nm.add_network.assert_not_called()

    def test_success_dispatches_add_and_sets_loading(self, win):
        w, nm = win
        w._current_network_is_open = False
        w.add_network_network_label.setText("HomeNet")
        w.add_network_password_field.setText("secret123")
        with patch.object(type(w), "setCurrentIndex"):
            w._add_network()
        nm.add_network.assert_called_once_with("HomeNet", "secret123")
        assert w._pending_operation == PendingOperation.CONNECT

    def test_open_network_connects_without_password(self, win):
        w, nm = win
        w._current_network_is_open = True
        w.add_network_network_label.setText("OpenCafe")
        w.add_network_password_field.setText("")
        with patch.object(type(w), "setCurrentIndex"):
            w._add_network()
        nm.add_network.assert_called_once_with("OpenCafe", "")


# ─────────────────────────────────────────────────────────────────────────────
# Step 4l: _on_activate_network
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestOnActivateNetwork:
    def test_sets_pending_and_calls_connect(self, win):
        w, nm = win
        w.saved_connection_network_name.setText("HomeNet")
        with patch.object(type(w), "setCurrentIndex"):
            w._on_activate_network()
        assert w._target_ssid == "HomeNet"
        assert w._pending_operation == PendingOperation.CONNECT
        nm.connect_network.assert_called_once_with("HomeNet")


# ─────────────────────────────────────────────────────────────────────────────
# Step 4m: _on_delete_network
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestOnDeleteNetwork:
    def test_calls_delete_network(self, win):
        w, nm = win
        w.saved_connection_network_name.setText("OldNet")
        w._on_delete_network()
        nm.delete_network.assert_called_once_with("OldNet")


# ─────────────────────────────────────────────────────────────────────────────
# Step 4n: _on_save_network_details
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestOnSaveNetworkDetails:
    def test_no_changes_shows_info_popup(self, win):
        w, nm = win
        w.saved_connection_network_name.setText("HomeNet")
        w.saved_connection_change_password_field.setText("")
        w._initial_priority = ConnectionPriority.MEDIUM
        w.med_priority_btn.setChecked(True)
        with patch.object(w, "_show_info_popup") as mock_info:
            w._on_save_network_details()
            mock_info.assert_called_once()
        nm.update_network.assert_not_called()

    def test_password_change_calls_update(self, win):
        w, nm = win
        w.saved_connection_network_name.setText("HomeNet")
        w.saved_connection_change_password_field.setText("newpass")
        w._initial_priority = ConnectionPriority.MEDIUM
        w.med_priority_btn.setChecked(True)
        w._on_save_network_details()
        nm.update_network.assert_called_once_with(
            "HomeNet", password="newpass", priority=ConnectionPriority.MEDIUM.value
        )

    def test_priority_change_calls_update(self, win):
        w, nm = win
        w.saved_connection_network_name.setText("HomeNet")
        w.saved_connection_change_password_field.setText("")
        w._initial_priority = ConnectionPriority.MEDIUM
        w.high_priority_btn.setChecked(True)
        w._on_save_network_details()
        nm.update_network.assert_called_once()
        call_kwargs = nm.update_network.call_args.kwargs
        assert call_kwargs["priority"] == ConnectionPriority.HIGH.value


# ─────────────────────────────────────────────────────────────────────────────
# Step 4o: _on_hidden_network_connect
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestOnHiddenNetworkConnect:
    def test_empty_ssid_shows_error(self, win):
        w, nm = win
        w.hidden_network_ssid_field.setText("")
        with patch.object(w, "_show_error_popup") as mock_err:
            w._on_hidden_network_connect()
            mock_err.assert_called_once()
        nm.add_network.assert_not_called()

    def test_success_sets_loading_and_connects(self, win):
        w, nm = win
        w.hidden_network_ssid_field.setText("MyHiddenNet")
        w.hidden_network_password_field.setText("pass123")
        with patch.object(type(w), "setCurrentIndex"):
            w._on_hidden_network_connect()
        nm.add_network.assert_called_once_with("MyHiddenNet", "pass123")
        assert w._target_ssid == "MyHiddenNet"
        assert w._pending_operation == PendingOperation.CONNECT
        assert w._current_network_is_hidden is True

    def test_no_password_marks_open(self, win):
        w, nm = win
        w.hidden_network_ssid_field.setText("HiddenOpen")
        w.hidden_network_password_field.setText("")
        with patch.object(type(w), "setCurrentIndex"):
            w._on_hidden_network_connect()
        assert w._current_network_is_open is True


# ─────────────────────────────────────────────────────────────────────────────
# Step 4p: _on_ethernet_button_clicked
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestOnEthernetButtonClicked:
    def test_eth_off_shows_warning(self, win):
        w, _ = win
        w.ethernet_button.toggle_button.state = (
            w.ethernet_button.toggle_button.State.OFF
        )
        with patch.object(w, "_show_warning_popup") as mock_warn:
            w._on_ethernet_button_clicked()
            mock_warn.assert_called_once()

    def test_eth_on_navigates_to_vlan_page(self, win):
        w, _ = win
        w.ethernet_button.toggle_button.state = w.ethernet_button.toggle_button.State.ON
        vlan_idx = w.indexOf(w.vlan_page)
        with patch.object(type(w), "setCurrentIndex") as mock_set:
            w._on_ethernet_button_clicked()
            mock_set.assert_called_with(vlan_idx)


# ─────────────────────────────────────────────────────────────────────────────
# Step 4q: Wi-Fi static IP methods
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestWifiStaticIp:
    def _setup_fields(
        self, w, ip="192.168.1.10", mask="255.255.255.0", gateway="", dns1="", dns2=""
    ):
        w.wifi_sip_ip_field.setText(ip)
        w.wifi_sip_mask_field.setText(mask)
        w.wifi_sip_gateway_field.setText(gateway)
        w.wifi_sip_dns1_field.setText(dns1)
        w.wifi_sip_dns2_field.setText(dns2)

    def test_apply_invalid_ip_shows_error(self, win):
        w, nm = win
        w.wifi_sip_title.setText("HomeNet")
        self._setup_fields(w)
        w.wifi_sip_ip_field.is_valid = MagicMock(return_value=False)
        with patch.object(w, "_show_error_popup") as mock_err:
            w._on_wifi_static_ip_apply()
            mock_err.assert_called_once()
        nm.update_wifi_static_ip.assert_not_called()

    def test_apply_invalid_mask_shows_error(self, win):
        w, nm = win
        w.wifi_sip_title.setText("HomeNet")
        self._setup_fields(w)
        w.wifi_sip_ip_field.is_valid = MagicMock(return_value=True)
        w.wifi_sip_mask_field.is_valid_mask = MagicMock(return_value=False)
        with patch.object(w, "_show_error_popup") as mock_err:
            w._on_wifi_static_ip_apply()
            mock_err.assert_called_once()
        nm.update_wifi_static_ip.assert_not_called()

    def test_apply_valid_fields_dispatches(self, win):
        w, nm = win
        w.wifi_sip_title.setText("HomeNet")
        self._setup_fields(w, ip="10.0.0.5", mask="255.255.0.0")
        with patch.object(type(w), "setCurrentIndex"):
            w._on_wifi_static_ip_apply()
        nm.update_wifi_static_ip.assert_called_once_with(
            "HomeNet", "10.0.0.5", "255.255.0.0", "", "", ""
        )
        assert w._pending_operation == PendingOperation.WIFI_STATIC_IP

    def test_reset_dhcp_dispatches(self, win):
        w, nm = win
        w.wifi_sip_title.setText("HomeNet")
        with patch.object(type(w), "setCurrentIndex"):
            w._on_wifi_reset_dhcp()
        nm.reset_wifi_to_dhcp.assert_called_once_with("HomeNet")
        assert w._pending_operation == PendingOperation.WIFI_STATIC_IP

    def test_clicked_navigates_to_sip_page(self, win):
        w, nm = win
        w.snd_name.setText("HomeNet")
        saved = SavedNetwork(ssid="HomeNet", is_dhcp=False)
        nm.get_saved_network.return_value = saved
        sip_idx = w.indexOf(w.wifi_static_ip_page)
        with patch.object(type(w), "setCurrentIndex") as mock_set:
            w._on_wifi_static_ip_clicked()
            mock_set.assert_called_with(sip_idx)

    def test_clicked_dhcp_disables_reset_button(self, win):
        w, nm = win
        w.snd_name.setText("HomeNet")
        saved = SavedNetwork(ssid="HomeNet", is_dhcp=True)
        nm.get_saved_network.return_value = saved
        with patch.object(type(w), "setCurrentIndex"):
            w._on_wifi_static_ip_clicked()
        assert not w.wifi_sip_dhcp_button.isEnabled()


# ─────────────────────────────────────────────────────────────────────────────
# Step 4r: Window lifecycle
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestWindowLifecycle:
    def test_close_calls_nm_close(self, win):
        w, nm = win
        # Prevent the Qt widget from actually closing; exercise only our override
        with patch.object(QtWidgets.QStackedWidget, "close", return_value=True):
            w.close()
        nm.close.assert_called_once()

    def test_close_event_stops_timer(self, win):
        from PyQt6 import QtGui

        w, _ = win
        w._load_timer.start(5000)
        assert w._load_timer.isActive()
        w.closeEvent(QtGui.QCloseEvent())
        assert not w._load_timer.isActive()

    def test_show_event_calls_refresh(self, win):
        from PyQt6 import QtGui

        w, nm = win
        w.showEvent(QtGui.QShowEvent())
        nm.refresh_state.assert_called()


# ─────────────────────────────────────────────────────────────────────────────
# Hotspot config updated slot
# ─────────────────────────────────────────────────────────────────────────────


class TestHotspotConfigUpdated:
    def test_fields_updated_on_hotspot_config_updated(self, win):
        """_on_hotspot_config_updated sets hotspot input field texts."""
        w, _ = win
        w._on_hotspot_config_updated("MyAP", "mypassword", "wpa-psk")
        assert w.hotspot_name_input_field.text() == "MyAP"
        assert w.hotspot_password_input_field.text() == "mypassword"

    def test_security_param_ignored_in_fields(self, win):
        """Only SSID and password fields are updated; no crash on any security value."""
        w, _ = win
        w._on_hotspot_config_updated("AP2", "pass2", "wpa3-sae")
        assert w.hotspot_name_input_field.text() == "AP2"


# ─────────────────────────────────────────────────────────────────────────────
# Hardware error handling
# ─────────────────────────────────────────────────────────────────────────────


class TestHardwareErrorHandling:
    def test_wifi_unavailable_error_disables_wifi_button(self, win):
        w, _ = win
        w._on_network_error("wifi_unavailable", "No network device found")
        assert not w.wifi_button.isEnabled()

    def test_device_reconnected_reenables_wifi_button(self, win):
        w, nm = win
        w._on_network_error("wifi_unavailable", "No network device found")
        w._on_network_error("device_reconnected", "Network device reconnected")
        assert w.wifi_button.isEnabled()
        nm.refresh_state.assert_called()

    def test_unknown_error_shows_popup(self, win):
        """Non-hardware errors still call _show_error_popup."""
        w, _ = win
        w._on_network_error("connect", "connection failed")
        w._popup.new_message.assert_called()


# ─────────────────────────────────────────────────────────────────────────────
# QR Code on Hotspot Page
# ─────────────────────────────────────────────────────────────────────────────


class TestHotspotQRCode:
    def test_qr_img_always_visible(self, win):
        """qrcode_img is always present; no initial-hidden state."""
        w, _ = win
        assert w.qrcode_img is not None

    def test_qr_shown_after_hotspot_activated(self, win):
        """QR code should be displayed when hotspot activation succeeds."""
        w, nm = win
        w._is_first_run = False
        nm.hotspot_ssid = "TestAP"
        nm.hotspot_password = "testpass123"
        nm.hotspot_security = "wpa-psk"
        result = ConnectionResult(success=True, message="Hotspot 'TestAP' activated")
        with patch(
            "BlocksScreen.lib.panels.networkWindow.NetworkControlWindow._show_hotspot_qr"
        ) as mock_qr:
            w._on_operation_complete(result)
            mock_qr.assert_called_once_with("TestAP", "testpass123", "wpa-psk")

    def test_qr_cleared_after_hotspot_disabled(self, win):
        """qrcode_img should be cleared and show 'Hotspot not active' when disabled."""
        w, _ = win
        w._is_first_run = False
        result = ConnectionResult(success=True, message="Hotspot disabled")
        w._on_operation_complete(result)
        w.qrcode_img.clearPixmap.assert_called()
        w.qrcode_img.setText.assert_called_with("Hotspot not active")

    def test_show_hotspot_qr_sets_pixmap(self, win):
        """_show_hotspot_qr should clear text then set pixmap on success."""
        import sys
        import types

        w, _ = win
        mock_qrmod = types.ModuleType("lib.qrcode_gen")
        mock_qrmod.generate_wifi_qrcode = MagicMock(return_value=MagicMock())
        fake_pixmap = QtGui.QPixmap(10, 10)
        with (
            patch.dict(sys.modules, {"lib.qrcode_gen": mock_qrmod}),
            patch("PyQt6.QtGui.QPixmap.fromImage", return_value=fake_pixmap),
        ):
            w._show_hotspot_qr("TestAP", "testpass123", "wpa-psk")
        w.qrcode_img.setText.assert_called_with("")
        w.qrcode_img.setPixmap.assert_called()

    def test_show_hotspot_qr_clears_on_error(self, win):
        """_show_hotspot_qr should clear pixmap and set error text on failure."""
        import sys
        import types

        w, _ = win
        mock_qrmod = types.ModuleType("lib.qrcode_gen")
        mock_qrmod.generate_wifi_qrcode = MagicMock(
            side_effect=RuntimeError("QR gen failed")
        )
        with patch.dict(sys.modules, {"lib.qrcode_gen": mock_qrmod}):
            w._show_hotspot_qr("TestAP", "testpass123", "wpa-psk")
        w.qrcode_img.clearPixmap.assert_called()
        w.qrcode_img.setText.assert_called_with("QR error")
