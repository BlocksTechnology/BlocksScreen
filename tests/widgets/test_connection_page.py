import pytest
from unittest.mock import MagicMock
from BlocksScreen.lib.klippy_status import KlippyStatus
from BlocksScreen.lib.panels.widgets.MainWindow.connectionPage import (
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


class _Feed:
    """Drives ConnectionPage through KlippyStatus, the way mainWindow wires it."""

    def __init__(self, page: ConnectionPage) -> None:
        self.page = page
        self.ws = MagicMock()
        self.ws.send_request.return_value = True
        self.status = KlippyStatus(self.ws)
        self.status.changed.connect(page.render)
        self.status.on_connected()

    def webhooks(self, state: str, message: str) -> None:
        self.status.on_webhooks(state, message)

    def server_info(self, state: str) -> None:
        self.status.on_klippy_state(state)
        self.status.on_server_info_tick(state != "disconnected")

    def notify(self, state: str) -> None:
        self.status.on_klippy_notify(state)

    def printer_info(self, state: str, message: str) -> None:
        self.status._poll()
        callback = self.ws.send_request.call_args.kwargs["callback"]
        callback({"state": state, "state_message": message})


@pytest.fixture
def feed(page):
    return _Feed(page)


class TestSetState:
    def test_disconnected(self, page):
        page._set_state(ConnectionState.DISCONNECTED)
        assert page._state == ConnectionState.DISCONNECTED
        assert "offline" in page.status_label.text()

    def test_connecting(self, page):
        page.render("connecting", "", "")
        assert page._state == ConnectionState.CONNECTING
        assert page.status_label.text().endswith("Attempting to reconnect.")

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

    def test_real_shutdown_survives_bare_server_info(self, feed):
        feed.webhooks("shutdown", "heater fault")
        feed.server_info("shutdown")
        assert "Heater fault" in feed.page.status_label.text()

    def test_reason_cleared_after_recovery(self, feed):
        feed.webhooks("shutdown", "heater fault")
        feed.server_info("ready")
        feed.server_info("shutdown")
        assert "Heater fault" not in feed.page.status_label.text()
        assert feed.page._FALLBACK_REASON in feed.page.status_label.text()

    def test_real_shutdown_reason_can_be_overwritten_by_another_real_reason(self, feed):
        feed.webhooks("shutdown", "heater fault")
        feed.webhooks("shutdown", "thermistor short")
        assert "Thermistor short" in feed.page.status_label.text()


class TestDotTimer:
    def test_connecting_starts_timer(self, page):
        page._set_state(ConnectionState.CONNECTING)
        assert page.dot_timer.isActive()

    def test_non_connecting_stops_timer(self, page):
        page._set_state(ConnectionState.CONNECTING)
        page._set_state(ConnectionState.MOONRAKER_CONNECTED)
        assert not page.dot_timer.isActive()

    def test_add_dot_cycles(self, page):
        page.base_text = "Connecting"
        page.dot_count = 0
        for dots in [".", "..", "...", "."]:
            page._add_dot()
            assert page.status_label.text() == f"Connecting{dots}"

    def test_dot_count_resets_on_connecting(self, page):
        page.dot_count = 2
        page._set_state(ConnectionState.CONNECTING)
        assert page.dot_count == 1

    def test_repeat_attempts_keep_dot_beat(self, page):
        # Attempts come every 3s from the retry thread, off the 1s dot beat
        page.render("connecting", "", "")
        page._add_dot()
        page.render("connecting", "", "")
        assert page.status_label.text().endswith("reconnect..")
        assert page.dot_count == 2


class TestVisibility:
    def test_all_non_ready_states_auto_show(self, shown_page):
        for state in ConnectionState:
            if state == ConnectionState.KLIPPER_READY:
                continue
            shown_page._firmware_restarting_pending = False
            shown_page._state = ConnectionState.DISCONNECTED
            shown_page.hide()
            shown_page._set_state(state)
            assert shown_page.isVisible(), f"{state} should auto-show"

    def test_klipper_ready_hides(self, shown_page):
        shown_page.show()
        shown_page._set_state(ConnectionState.KLIPPER_READY)
        assert not shown_page.isVisible()

    def test_conn_toggle_false_suppresses_show(self, shown_page):
        shown_page.conn_toggle = False
        shown_page.hide()
        shown_page._set_state(ConnectionState.DISCONNECTED)
        assert not shown_page.isVisible()

    def test_show_emits_page_shown(self, shown_page, qtbot):
        shown_page.hide()
        with qtbot.waitSignal(shown_page.page_shown):
            shown_page._set_state(ConnectionState.WEBSOCKET_LOST)

    def test_show_sends_no_update_request(self, shown_page, mock_ws):
        # machine.update.refresh 503s while printing and raised an ERROR popup on start
        shown_page.hide()
        shown_page.show()
        mock_ws.api.refresh_update_status.assert_not_called()
        mock_ws.api.update_status.assert_not_called()

    def test_manual_show_emits_page_shown_with_toggle_off(self, page, qtbot):
        # Top-level popups cover this frame whether or not it auto-showed.
        page.hide()
        with qtbot.waitSignal(page.page_shown):
            page.show()


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

    def test_websocket_lost_offers_restart_not_retry(self, page, qtbot):
        # Reconnect is automatic, so the button only restarts Klipper
        page._set_state(ConnectionState.WEBSOCKET_LOST)
        assert page.restart_klipper_button.text() == "Restart Printer"
        with qtbot.waitSignal(page.restart_klipper_clicked):
            page._on_restart_clicked()


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


class TestKlippyNotify:
    def test_klippy_disconnected_notify(self, feed):
        feed.notify("disconnected")
        assert feed.page._state == ConnectionState.KLIPPER_DISCONNECTED

    def test_klippy_ready_notify(self, feed):
        feed.notify("ready")
        assert feed.page._state == ConnectionState.KLIPPER_READY

    def test_disconnected_after_shutdown_keeps_reason(self, feed):
        # Regression test for #220
        feed.webhooks("shutdown", "heater fault")
        feed.notify("disconnected")
        assert feed.page._state == ConnectionState.KLIPPER_SHUTDOWN
        assert "Heater fault" in feed.page.status_label.text()

    def test_save_config_restart_shows_page_then_hides(self, shown_page, qtbot):
        # SAVE_CONFIG from ready: the page replaces the caller's overlay until ready
        feed = _Feed(shown_page)
        feed.server_info("ready")
        assert not shown_page.isVisible()
        with qtbot.waitSignal(shown_page.call_load_panel) as blocker:
            feed.notify("disconnected")
        assert blocker.args == [False, "", False]
        assert shown_page._state == ConnectionState.KLIPPER_DISCONNECTED
        assert shown_page.isVisible()
        feed.server_info("startup")
        feed.server_info("ready")
        assert not shown_page.isVisible()


class TestBugRegressions:
    def test_base_text_initialized(self, page):
        assert page.base_text == ""

    def test_signal_names_are_distinct(self, page):
        assert page.call_cancel_panel.signal != page.call_load_panel.signal

    def test_no_self_panel_attribute(self, page):
        assert not hasattr(page, "panel")

    def test_dot_count_resets_on_connecting(self, page):
        page.dot_count = 3
        page._set_state(ConnectionState.CONNECTING)
        assert page.dot_count == 1

    def test_websocket_lost_does_not_show_when_toggle_off(self, page):
        page.conn_toggle = False
        page._set_state(ConnectionState.WEBSOCKET_LOST)
        assert not page.isVisible()

    @pytest.mark.parametrize(
        "raw",
        [
            "Shutdown due to M112 command",
            "Printers Emergency Button Pressed.",
            "Printer Emergency Button Pressed.",
        ],
    )
    def test_estop_reasons_share_one_text(self, page, raw):
        assert ConnectionPage._build_reason(raw) == ConnectionPage._ESTOP_TEXT

    def test_unmapped_shutdown_reason_strips_prefix(self, page):
        result = ConnectionPage._clean_shutdown_context(
            "Shutdown due to some obscure fault"
        )
        assert result == "Some obscure fault"


class TestErrorMessages:
    # Verbatim Klipper state_message after an E-stop + host reboot (mcu.py + error_mcu.py)
    MCU_STILL_SHUTDOWN = (
        "Can not update MCU 'mcu' config as it is shutdown\n"
        "Once the underlying issue is corrected, use the\n"
        '"FIRMWARE_RESTART" command to reset the firmware, reload the\n'
        "config, and restart the host software.\n"
        "Error configuring printer\n"
    )

    def test_mcu_still_shutdown_after_reboot(self, feed):
        feed.webhooks("error", self.MCU_STILL_SHUTDOWN)
        text = feed.page.status_label.text()
        assert feed.page._state == ConnectionState.KLIPPER_ERROR
        assert "emergency button" in text
        assert "Error configuring printer" not in text

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("mcu 'mcu': Unable to connect", "Cannot reach the controller board"),
            ("Failed automated reset of MCU 'mcu'", "did not reset"),
            ("MCU Protocol error\n\nThis is frequently caused", "out of date"),
        ],
    )
    def test_known_error_reasons(self, feed, raw, expected):
        feed.webhooks("error", raw)
        assert expected in feed.page.status_label.text()

    def test_previous_mcu_shutdown_after_reboot(self, feed):
        # Real order: server.info's bare "shutdown", then the printer.info reply; no subscription
        feed.server_info("shutdown")
        feed.printer_info(
            "shutdown",
            "Previous MCU 'mcu' shutdown: Command request\n"
            "Once the underlying issue is corrected, use the\n"
            '"FIRMWARE_RESTART" command to reset the firmware',
        )
        assert feed.page._state == ConnectionState.KLIPPER_SHUTDOWN
        assert "emergency button" in feed.page.status_label.text()
        assert feed.page._firmware_restarting_pending is False

    def test_error_during_config_after_reboot(self, feed):
        # mcu.py _send_get_config: the other message an E-stop + reboot can produce
        feed.webhooks("error", "MCU 'mcu' error during config: Command request")
        assert "emergency button" in feed.page.status_label.text()

    def test_live_command_request_is_not_previous_stop(self, feed):
        feed.webhooks("shutdown", "MCU 'mcu' shutdown: Command request")
        text = feed.page.status_label.text()
        assert "Emergency stop activated." in text
        assert "previous stop" not in text

    def test_unknown_error_keeps_name_case(self, feed):
        feed.webhooks("error", "pin PA1 used multiple times in config")
        assert "Pin PA1 used multiple times in config" in feed.page.status_label.text()

    def test_unknown_error_shows_klipper_line(self, feed):
        feed.webhooks(
            "error", "Option 'step_pin' in section 'stepper_x' must be specified"
        )
        text = feed.page.status_label.text()
        assert "step_pin" in text
        assert "Firmware Restart" in text

    def test_empty_error_keeps_generic_text(self, feed):
        feed.webhooks("error", "")
        assert feed.page.status_label.text() == (
            "A printer error has occurred.\nPress 'Firmware Restart' to recover."
        )

    def test_ready_after_error_hides_page(self, feed):
        # Last write wins
        feed.webhooks("error", "boom")
        feed.webhooks("ready", "Printer is ready")
        assert feed.page._state == ConnectionState.KLIPPER_READY

    def test_printer_info_error_shows_reason(self, feed):
        feed.server_info("error")
        feed.printer_info("error", self.MCU_STILL_SHUTDOWN)
        assert "emergency button" in feed.page.status_label.text()

    def test_printer_info_new_error_reason_replaces_old(self, feed):
        # Failed FIRMWARE_RESTART: same state, new message
        feed.webhooks("error", "mcu 'mcu': Unable to connect")
        feed.printer_info("error", "Failed automated reset of MCU 'mcu'")
        assert "did not reset" in feed.page.status_label.text()

    def test_printer_info_startup_is_applied(self, feed):
        feed.server_info("disconnected")
        feed.printer_info("startup", "Printer is starting")
        assert feed.page._state == ConnectionState.KLIPPER_STARTUP


class TestRestartOverlay:
    def _start_restart(self, feed):
        feed.webhooks("shutdown", "Timer too close")
        feed.page._on_restart_clicked()
        assert feed.page.manual_restart_pending

    def test_closes_on_ready(self, feed):
        self._start_restart(feed)
        feed.notify("disconnected")
        feed.server_info("startup")
        assert feed.page.manual_restart_pending
        feed.server_info("ready")
        assert not feed.page.manual_restart_pending

    def test_closes_on_link_loss(self, feed):
        self._start_restart(feed)
        feed.status.on_connection_lost("gone")
        assert not feed.page.manual_restart_pending

    def test_closes_on_new_failure(self, feed):
        self._start_restart(feed)
        feed.notify("disconnected")
        assert feed.page.manual_restart_pending
        feed.server_info("error")
        assert not feed.page.manual_restart_pending

    def test_reason_update_keeps_overlay(self, feed):
        self._start_restart(feed)
        feed.printer_info("shutdown", "Lost communication with MCU 'mcu'")
        assert feed.page.manual_restart_pending


class TestKlippyStateRegressions:
    TIMER_TOO_CLOSE = "MCU 'mcu' shutdown: Timer too close"
    ESTOP = "Shutdown due to Printers Emergency Button Pressed."

    @pytest.mark.parametrize("state", ["shutdown", "error"])
    def test_r1_bare_server_info_keeps_reason(self, feed, state):
        feed.webhooks(state, self.TIMER_TOO_CLOSE)
        feed.server_info(state)
        assert "MCU overload" in feed.page.status_label.text()

    def test_r2_repeated_shutdown_keeps_restart_overlay(self, feed, qtbot):
        feed.webhooks("shutdown", self.TIMER_TOO_CLOSE)
        feed.page._on_restart_clicked()
        with qtbot.assertNotEmitted(feed.page.call_load_panel):
            feed.webhooks("shutdown", self.TIMER_TOO_CLOSE)
            feed.printer_info("shutdown", self.TIMER_TOO_CLOSE)
        assert feed.page.manual_restart_pending
        assert feed.page._restart_30s_timer.isActive()

    def test_r3_estop_arms_nothing(self, feed):
        feed.webhooks("shutdown", self.ESTOP)
        page = feed.page
        assert not page.manual_restart_pending
        assert not page._restart_10s_timer.isActive()
        assert not page._restart_30s_timer.isActive()
        assert "Release the emergency button" in page.status_label.text()
        assert page.restart_klipper_button.text() == "Firmware Restart"
