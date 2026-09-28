"""Unit tests for moonrakerComm."""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from PyQt6 import QtCore

from BlocksScreen.lib import moonrakerComm
from BlocksScreen.lib.moonrakerComm import OneShotTokenError


class TestOneShotTokenError:
    def test_str_carries_message(self):
        # A super(OneShotTokenError).__init__ regression left str(exc) empty.
        exc = OneShotTokenError("token fetch failed")
        assert str(exc) == "token fetch failed"
        assert exc.message == "token fetch failed"

    def test_default_message(self):
        exc = OneShotTokenError()
        assert str(exc) == "Unable to get oneshot token"

    def test_errors_attribute_kept(self):
        exc = OneShotTokenError("boom", errors={"code": 401})
        assert exc.errors == {"code": 401}


class _Parent(QtCore.QObject):
    config = SimpleNamespace(get=lambda _key, parser=None, default=None: default)


@pytest.fixture
def ws(qtbot, monkeypatch):
    monkeypatch.setattr(moonrakerComm, "RepeatedTimer", MagicMock())
    monkeypatch.setattr(moonrakerComm, "MoonRest", MagicMock())
    parent = _Parent()
    sock = moonrakerComm.MoonWebSocket(parent)
    yield sock
    del parent


def _notify(sock, method: str) -> None:
    sock.on_message(None, json.dumps({"jsonrpc": "2.0", "method": method}))


class TestKlippyNotifications:
    def test_ready_does_not_requery(self, ws):
        # Moonraker sets READY before notifying, so the poll already saw it
        ws.query_klippy_status_timer.running = False
        queries = []
        ws.query_server_info_signal.connect(lambda: queries.append(1))
        _notify(ws, "notify_klippy_ready")
        assert queries == []

    @pytest.mark.parametrize(
        "method", ["notify_klippy_disconnected", "notify_klippy_shutdown"]
    )
    def test_leaving_ready_restarts_poll_without_synthetic_state(self, ws, method):
        states = []
        ws.klippy_state_signal.connect(states.append)
        _notify(ws, method)
        ws.query_klippy_status_timer.startTimer.assert_called_once()
        assert states == []  # server.info reply reports the real state


class TestServerInfoComponents:
    def _reply(self, sock, payload: dict) -> None:
        sock.request_table[7] = ["server.info", {}, None]
        sock.on_message(None, json.dumps({"jsonrpc": "2.0", "id": 7, **payload}))

    def test_emits_components_even_without_klippy_state(self, ws):
        seen = []
        ws.server_components_signal.connect(seen.append)
        self._reply(ws, {"result": {"components": ["spoolman", "history"]}})
        assert seen == [["spoolman", "history"]]

    def test_error_reply_emits_nothing(self, ws):
        seen = []
        ws.server_components_signal.connect(seen.append)
        self._reply(ws, {"error": {"code": 500, "message": "boom"}})
        assert seen == []

    @pytest.mark.parametrize("state", ["startup", "disconnected", "shutdown", "error"])
    def test_poll_never_gives_up_before_ready(self, ws, state):
        # Klippy may sit in startup for 90s waiting on the MCU (serialhdl.py)
        for _ in range(100):
            self._reply(ws, {"result": {"klippy_state": state}})
        ws.query_klippy_status_timer.stopTimer.assert_not_called()
        self._reply(ws, {"result": {"klippy_state": "ready"}})
        ws.query_klippy_status_timer.stopTimer.assert_called_once()

    def test_state_emitted_on_change_only(self, ws, monkeypatch):
        # A repeated shutdown would cancel the restart overlay mid-restart
        update = MagicMock()
        monkeypatch.setattr(ws.api, "update_status", update)
        states = []
        ws.klippy_state_signal.connect(states.append)
        for state in ["shutdown"] * 3 + ["startup"] * 3 + ["ready"] * 2:
            self._reply(ws, {"result": {"klippy_state": state}})
        assert states == ["shutdown", "startup", "ready"]
        update.assert_called_once()

    def test_klippy_restart_reemits_unchanged_state(self, ws):
        # A failed FIRMWARE_RESTART goes shutdown to shutdown faster than the poll
        states = []
        ws.klippy_state_signal.connect(states.append)
        self._reply(ws, {"result": {"klippy_state": "shutdown"}})
        _notify(ws, "notify_klippy_disconnected")
        self._reply(ws, {"result": {"klippy_state": "shutdown"}})
        assert states == ["shutdown", "shutdown"]

    def test_reconnect_reemits_unchanged_state(self, ws):
        states = []
        ws.klippy_state_signal.connect(states.append)
        self._reply(ws, {"result": {"klippy_state": "ready"}})
        ws.on_open(None)
        self._reply(ws, {"result": {"klippy_state": "ready"}})
        assert states == ["ready", "ready"]


class TestReconnectCycle:
    def test_retries_forever_until_connected(self, ws, monkeypatch):
        connect = MagicMock(return_value=False)
        monkeypatch.setattr(ws, "connect", connect)
        ws._retry_timer = MagicMock()
        ws._reconnect_count = 100
        for _ in range(10):
            ws.reconnect()
        assert connect.call_count == 10
        ws._retry_timer.stopTimer.assert_not_called()

    def test_reconnect_noop_once_connected(self, ws, monkeypatch):
        connect = MagicMock()
        monkeypatch.setattr(ws, "connect", connect)
        ws.connected = True
        assert ws.reconnect() is True
        connect.assert_not_called()

    def test_reconnect_waits_for_attempt_in_flight(self, ws, monkeypatch):
        connect = MagicMock()
        monkeypatch.setattr(ws, "connect", connect)
        ws._wst = MagicMock(is_alive=MagicMock(return_value=True))
        assert ws.reconnect() is False
        connect.assert_not_called()

    def test_reconnect_skips_while_another_attempt_starts(self, ws, monkeypatch):
        connect = MagicMock()
        monkeypatch.setattr(ws, "connect", connect)
        with ws._connect_lock:
            assert ws.reconnect() is False
        connect.assert_not_called()

    def test_connect_pings_to_detect_dead_socket(self, ws, monkeypatch):
        app = MagicMock()
        monkeypatch.setattr(moonrakerComm.websocket, "WebSocketApp", app)
        assert ws.connect() is True
        ws._wst.join(1)
        app.return_value.run_forever.assert_called_once_with(
            ping_interval=ws.PING_INTERVAL, ping_timeout=ws.PING_TIMEOUT
        )
        assert ws.PING_INTERVAL > ws.PING_TIMEOUT  # else run_forever raises

    def test_disconnect_stops_retry_timer(self, ws):
        ws._retry_timer = MagicMock()
        ws.wb_disconnect()
        ws._retry_timer.stopTimer.assert_called_once()

    def test_try_connection_arms_one_watchdog(self, ws, monkeypatch):
        timers = MagicMock()
        monkeypatch.setattr(moonrakerComm, "RepeatedTimer", timers)
        connect = MagicMock(return_value=True)
        monkeypatch.setattr(ws, "connect", connect)
        ws.try_connection()
        ws.try_connection()
        timers.assert_called_once_with(ws.timeout, ws.reconnect)
        timers.return_value.startTimer.assert_called_once()
        assert connect.call_count == 2

    def test_open_resets_count_and_keeps_watchdog(self, ws):
        ws._retry_timer = MagicMock()
        ws._reconnect_count = 5
        ws.on_open(None)
        assert ws._reconnect_count == 0
        ws._retry_timer.stopTimer.assert_not_called()

    def test_close_leaves_reconnect_to_watchdog(self, ws, monkeypatch, qtbot):
        connect = MagicMock()
        monkeypatch.setattr(ws, "connect", connect)
        ws.ws = MagicMock()
        ws.on_close(None, 1006, "gone")
        qtbot.wait(50)
        connect.assert_not_called()
