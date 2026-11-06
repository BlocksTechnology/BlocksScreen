from unittest.mock import MagicMock

import pytest
from BlocksScreen.lib.klippy_status import KlippyStatus


@pytest.fixture
def ws():
    mock = MagicMock()
    mock.send_request.return_value = True
    return mock


@pytest.fixture
def status(qtbot, ws):
    obj = KlippyStatus(ws)
    obj.on_connected()
    return obj


def _server_info(status, state, klippy_connected=True):
    status.on_klippy_state(state)
    status.on_server_info_tick(klippy_connected)


def _last_callback(ws):
    assert ws.send_request.call_args.args[0] == "printer.info"
    return ws.send_request.call_args.kwargs["callback"]


class TestEmitOnChange:
    def test_repeat_is_silent(self, status, qtbot):
        status.on_webhooks("shutdown", "Timer too close")
        with qtbot.assertNotEmitted(status.changed):
            status.on_webhooks("shutdown", "Timer too close")
            status.on_klippy_state("shutdown")
            status.on_klippy_notify("shutdown")

    def test_change_emits_triple(self, status, qtbot):
        with qtbot.waitSignal(status.changed) as blocker:
            status.on_webhooks("error", "boom")
        assert blocker.args == ["connected", "error", "boom"]

    def test_state_change_clears_message(self, status):
        status.on_webhooks("shutdown", "Timer too close")
        status.on_klippy_state("startup")
        assert (status.state, status.message) == ("startup", "")

    def test_same_state_keeps_message(self, status):
        status.on_webhooks("error", "boom")
        status.on_klippy_state("error")
        assert status.message == "boom"

    def test_ready_message_from_webhooks_is_silent(self, status, qtbot):
        status.on_klippy_state("ready")
        with qtbot.assertNotEmitted(status.changed):
            status.on_webhooks("ready", "Printer is ready")
        assert status.message == ""

    def test_push_before_connected_is_ignored(self, qtbot, ws):
        obj = KlippyStatus(ws)
        obj.on_klippy_state("shutdown")
        assert obj.state == ""


class TestPrinterInfo:
    def test_reply_sets_reason(self, status, ws):
        _server_info(status, "error")
        _last_callback(ws)({"state": "error", "state_message": "boom"})
        assert (status.state, status.message) == ("error", "boom")

    def test_stale_reply_dropped_after_push(self, status, ws):
        _server_info(status, "shutdown")
        stale = _last_callback(ws)
        status.on_klippy_notify("disconnected")
        stale({"state": "shutdown", "state_message": "old"})
        assert (status.state, status.message) == ("disconnected", "")

    def test_reply_dropped_after_link_loss(self, status, ws):
        _server_info(status, "error")
        stale = _last_callback(ws)
        status.on_connection_lost("gone")
        status.on_connected()
        stale({"state": "error", "state_message": "old"})
        assert (status.link, status.state, status.message) == ("connected", "", "")

    def test_error_reply_ignored(self, status, ws):
        _server_info(status, "shutdown")
        _last_callback(ws)({"error": {"code": 503, "message": "Klippy Disconnected"}})
        assert (status.state, status.message) == ("shutdown", "")

    def test_transition_polls_once(self, status, ws):
        _server_info(status, "shutdown")
        assert ws.send_request.call_count == 1

    def test_transition_without_klippy_skips_poll(self, status, ws):
        _server_info(status, "disconnected", klippy_connected=False)
        ws.send_request.assert_not_called()

    def test_tick_polls_while_not_ready(self, status, ws):
        status.on_klippy_state("error")
        ws.send_request.reset_mock()
        status.on_server_info_tick(True)
        ws.send_request.assert_called_once()

    @pytest.mark.parametrize(
        ("state", "klippy_connected"), [("ready", True), ("error", False)]
    )
    def test_tick_skips_poll(self, status, ws, state, klippy_connected):
        status.on_klippy_state(state)
        ws.send_request.reset_mock()
        status.on_server_info_tick(klippy_connected)
        ws.send_request.assert_not_called()


class TestLink:
    def test_link_loss_resets_state(self, status):
        status.on_webhooks("shutdown", "Timer too close")
        status.on_connection_lost("gone")
        assert (status.link, status.state, status.message) == ("lost", "", "")

    def test_connecting_repeats_are_silent(self, status, qtbot):
        status.on_connecting(1)
        with qtbot.assertNotEmitted(status.changed):
            status.on_connecting(2)
