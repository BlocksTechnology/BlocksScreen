import pytest
from unittest.mock import MagicMock
from events import KlippyDisconnected, KlippyReady, KlippyShutdown
from BlocksScreen.lib.panels.widgets.connectionPage import (
    ConnectionState,
    ConnectionPage,
)


@pytest.fixture
def mock_ws():
    ws = MagicMock()
    ws.api = MagicMock()
    return ws


@pytest.fixture
def page(qtbot, mock_ws):
    widget = ConnectionPage(None, mock_ws)
    qtbot.addWidget(widget)
    widget.conn_toggle = False
    return widget


@pytest.fixture
def shown_page(qtbot, mock_ws):
    widget = ConnectionPage(None, mock_ws)
    qtbot.addWidget(widget)
    return widget


class TestSetState:
    def test_disconnected(self, page):
        page._set_state(ConnectionState.DISCONNECTED)
        assert page._state == ConnectionState.DISCONNECTED
        assert "offline" in page.status_label.text()

    def test_connecting(self, page):
        page._set_state(ConnectionState.CONNECTING, context="3")
        assert page._state == ConnectionState.CONNECTING
        assert "Attempt 3" in page.status_label.text()

    def test_websocket_lost(self, page):
        page._set_state(ConnectionState.WEBSOCKET_LOST)
        assert page._state == ConnectionState.WEBSOCKET_LOST
        assert "interrupted" in page.status_label.text()

    def test_moonraker_connected(self, page):
        page._set_state(ConnectionState.MOONRAKER_CONNECTED)
        assert page._state == ConnectionState.MOONRAKER_CONNECTED
        assert "Connection established" in page.status_label.text()

    def test_klipper_startup(self, page):
        page._set_state(ConnectionState.KLIPPER_STARTUP)
        assert page._state == ConnectionState.KLIPPER_STARTUP
        assert "starting up" in page.status_label.text()

    def test_klipper_ready(self, page):
        page._set_state(ConnectionState.KLIPPER_READY)
        assert page._state == ConnectionState.KLIPPER_READY
        assert "ready" in page.status_label.text()

    def test_klipper_disconnected(self, page):
        page._set_state(ConnectionState.KLIPPER_DISCONNECTED)
        assert page._state == ConnectionState.KLIPPER_DISCONNECTED
        assert "not responding" in page.status_label.text()

    def test_klipper_error(self, page):
        page._set_state(ConnectionState.KLIPPER_ERROR)
        assert page._state == ConnectionState.KLIPPER_ERROR
        assert "error" in page.status_label.text()

    def test_klipper_shutdown_context(self, page):
        page._set_state(ConnectionState.KLIPPER_SHUTDOWN, context="heater fault")
        assert page._state == ConnectionState.KLIPPER_SHUTDOWN
        assert "heater fault" in page.status_label.text()

    def test_real_shutdown_blocks_subsequent_fallback(self, page):
        page.webhook_update("shutdown", "heater fault")
        page.on_klippy_state("shutdown")  # no-context path — should be rejected
        assert "Heater fault" in page.status_label.text()

    def test_shutdown_confirmed_resets_on_state_change(self, page):
        page.webhook_update("shutdown", "heater fault")
        assert page._shutdown_confirmed is True
        page._set_state(ConnectionState.KLIPPER_READY)
        assert page._shutdown_confirmed is False

    def test_real_shutdown_reason_can_be_overwritten_by_another_real_reason(self, page):
        page.webhook_update("shutdown", "heater fault")
        page.webhook_update("shutdown", "thermistor short")
        assert "Thermistor short" in page.status_label.text()


class TestDotTimer:
    def test_connecting_starts_timer(self, page):
        page._set_state(ConnectionState.CONNECTING, context="1")
        assert page.dot_timer.isActive()

    def test_non_connecting_stops_timer(self, page):
        page._set_state(ConnectionState.CONNECTING, context="1")
        page._set_state(ConnectionState.MOONRAKER_CONNECTED)
        assert not page.dot_timer.isActive()

    def test_add_dot_cycles(self, page):
        page.base_text = "Connecting"
        page.dot_count = 0
        page._add_dot()
        assert page.status_label.text() == "Connecting."
        page._add_dot()
        assert page.status_label.text() == "Connecting.."
        page._add_dot()
        assert page.status_label.text() == "Connecting..."
        page._add_dot()
        assert page.status_label.text() == "Connecting"

    def test_dot_count_resets_on_connecting(self, page):
        page.dot_count = 2
        page._set_state(ConnectionState.CONNECTING, context="1")
        assert page.dot_count == 0


class TestVisibility:
    def test_auto_show_states_call_show(self, shown_page):
        for state in ConnectionPage._AUTO_SHOW_STATES:
            shown_page._state = ConnectionState.DISCONNECTED
            shown_page._firmware_restarting_pending = False
            shown_page.hide()
            shown_page._set_state(state)
            assert shown_page.isVisible(), f"{state} should auto-shown"

    def test_klipper_ready_hides(self, shown_page):
        shown_page.show()
        shown_page._set_state(ConnectionState.KLIPPER_READY)
        assert not shown_page.isVisible()

    def test_non_auto_show_does_not_show(self, shown_page):
        shown_page.hide()
        for state in (
            ConnectionState.CONNECTING,
            ConnectionState.MOONRAKER_CONNECTED,
            ConnectionState.KLIPPER_STARTUP,
        ):
            shown_page._set_state(state)
            assert not shown_page.isVisible(), f"{state} should not auto-shown"

    def test_conn_toggle_false_suppresses_show(self, shown_page):
        shown_page.conn_toggle = False
        shown_page.hide()
        shown_page._set_state(ConnectionState.DISCONNECTED)
        assert not shown_page.isVisible()


class TestRestartButton:
    def test_error_state_emits_firmware_restart(self, page, qtbot):
        page._set_state(ConnectionState.KLIPPER_ERROR)
        with qtbot.waitSignal(page.firmware_restart_clicked):
            page._on_restart_clicked()

    def test_shutdown_state_emits_firmware_restart(self, page, qtbot):
        page._set_state(ConnectionState.KLIPPER_SHUTDOWN)
        with qtbot.waitSignal(page.firmware_restart_clicked):
            page._on_restart_clicked()

    def test_other_state_emits_restart_klipper(self, page, qtbot):
        page._set_state(ConnectionState.KLIPPER_DISCONNECTED)
        with qtbot.waitSignal(page.restart_klipper_clicked):
            page._on_restart_clicked()

    def test_error_label_says_firmware_restart(self, page, qtbot):
        page._set_state(ConnectionState.KLIPPER_ERROR)
        assert page.restart_klipper_button.text() == "Firmware Restart"

    def test_normal_label_says_restart_klipper(self, page, qtbot):
        page._set_state(ConnectionState.KLIPPER_DISCONNECTED)
        assert page.restart_klipper_button.text() == "Restart Printer"


class TestSignalWiring:
    def test_reboot_button(self, page, qtbot):
        with qtbot.waitSignal(page.reboot_clicked):
            page.reboot_system_button.click()

    def test_wifi_button(self, page, qtbot):
        with qtbot.waitSignal(page.wifi_button_clicked):
            page.wifi_button.click()

    def test_notification_button(self, page, qtbot):
        with qtbot.waitSignal(page.notification_button_clicked):
            page.notification_button.click()

    def test_update_button(self, page, qtbot):
        with qtbot.waitSignal(page.update_button_clicked):
            page.update_page_button.click()

    def test_update_button_emits_true(self, page, qtbot):
        with qtbot.waitSignal(page.update_button_clicked) as blocker:
            page.update_page_button.click()
        assert blocker.args == [True]


class TestEventFilter:
    def test_klippy_disconnected_event(self, page):
        page.eventFilter(page, KlippyDisconnected(None))
        assert page._state == ConnectionState.KLIPPER_DISCONNECTED

    def test_klippy_ready_event(self, page):
        page.eventFilter(page, KlippyReady(None))
        assert page._state == ConnectionState.KLIPPER_READY

    def test_klippy_shutdown_event(self, page):
        page.eventFilter(page, KlippyShutdown(None))
        assert page._state == ConnectionState.KLIPPER_SHUTDOWN


class TestBugRegressions:
    def test_base_text_initialized(self, page):
        assert page.base_text == ""

    def test_signal_names_are_distinct(self, page):
        assert page.call_cancel_panel.signal != page.call_load_panel.signal

    def test_no_self_panel_attribute(self, page):
        assert not hasattr(page, "panel")

    def test_dot_count_resets_on_connecting(self, page):
        page.dot_count = 3
        page._set_state(ConnectionState.CONNECTING, context=1)
        assert page.dot_count == 0

    def test_websocket_lost_does_not_show_when_toggle_off(self, page):
        page.conn_toggle = False
        page._set_state(ConnectionState.WEBSOCKET_LOST)
        assert not page.isVisible()
