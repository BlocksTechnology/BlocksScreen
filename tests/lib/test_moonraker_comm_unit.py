"""Unit tests for moonrakerComm."""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from BlocksScreen.lib import moonrakerComm
from BlocksScreen.lib.moonrakerComm import OneShotTokenError
from PyQt6 import QtCore


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
    def test_ready_requeries_after_poll_cap(self, ws):
        ws.query_klippy_status_timer.running = False
        queries = []
        ws.query_server_info_signal.connect(lambda: queries.append(1))
        _notify(ws, "notify_klippy_ready")
        assert queries == [1]

    def test_ready_skipped_while_polling(self, ws):
        ws.query_klippy_status_timer.running = True
        queries = []
        ws.query_server_info_signal.connect(lambda: queries.append(1))
        _notify(ws, "notify_klippy_ready")
        assert queries == []

    @pytest.mark.parametrize(
        "method", ["notify_klippy_disconnected", "notify_klippy_shutdown"]
    )
    def test_leaving_ready_restarts_poll_without_synthetic_state(self, ws, method):
        ws._klippy_retry_count = 30
        states = []
        ws.klippy_state_signal.connect(states.append)
        _notify(ws, method)
        assert ws._klippy_retry_count == 0
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


class TestReconnectCycle:
    def test_gives_up_without_another_attempt(self, ws, monkeypatch):
        connect = MagicMock()
        monkeypatch.setattr(ws, "connect", connect)
        ws._retry_timer = MagicMock()
        ws.connecting = True
        ws._reconnect_count = ws.max_retries
        assert ws.reconnect() is False
        connect.assert_not_called()
        assert ws.connecting is False
        ws._retry_timer.stopTimer.assert_called_once()

    def test_try_connection_starts_fresh_cycle(self, ws, monkeypatch):
        monkeypatch.setattr(ws, "connect", MagicMock(return_value=True))
        ws._reconnect_count = ws.max_retries + 4
        ws.try_connection()
        assert ws._reconnect_count == 0
        moonrakerComm.RepeatedTimer.assert_called_with(ws.timeout, ws.reconnect)
