"""Unit tests for moonrakerComm."""

import base64
import hashlib
import importlib
import json
import socket
import sys
import threading
import time
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from PyQt6 import QtCore

from BlocksScreen.lib import moonrakerComm
from BlocksScreen.lib.moonrakerComm import MoonAPI, OneShotTokenError


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


class TestRequestCallbacks:
    def _reply(self, sock, callback, payload: dict) -> None:
        sock.request_table[9] = ["server.spoolman.proxy", {}, callback]
        sock.on_message(None, json.dumps({"jsonrpc": "2.0", "id": 9, **payload}))

    def test_result_reaches_callback(self, ws):
        got = []
        self._reply(ws, got.append, {"result": {"response": [1], "error": None}})
        assert got == [{"response": [1], "error": None}]

    def test_jsonrpc_error_reaches_callback(self, ws):
        got = []
        err = {"code": 503, "message": "Spoolman server not available"}
        self._reply(ws, got.append, {"error": err})
        assert got == [{"error": err}]

    def test_raising_callback_is_logged_not_raised(self, ws, caplog):
        def boom(_result):
            raise RuntimeError("boom")

        self._reply(ws, boom, {"result": {}})
        assert "callback" in caplog.text

    def test_callback_runs_on_gui_thread(self, ws, qtbot):
        threads = []

        def record(_result):
            threads.append(threading.current_thread())

        worker = threading.Thread(target=self._reply, args=(ws, record, {"result": {}}))
        worker.start()
        worker.join()
        qtbot.waitUntil(lambda: bool(threads))
        assert threads == [threading.main_thread()]


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

    def test_close_fails_pending_requests(self, ws, qtbot):
        ws.ws = MagicMock()
        got = []
        ws.request_table[3] = ["server.info", {}, None]
        ws.request_table[4] = ["server.spoolman.proxy", {}, got.append]
        ws.on_close(None, 1006, "gone")
        assert ws.request_table == {}
        qtbot.waitUntil(lambda: bool(got))
        assert got == [{"error": {"code": -1, "message": "disconnected"}}]

    def test_failed_send_returns_false_and_forgets_request(self, ws, monkeypatch):
        # conftest stubs websocket; an except clause needs a real class
        monkeypatch.setattr(moonrakerComm.websocket, "WebSocketException", OSError)
        ws.connected = True
        ws.ws = MagicMock()
        ws.ws.send.side_effect = OSError("broken pipe")
        assert ws.send_request("server.info", callback=MagicMock()) is False
        assert ws.request_table == {}

    def test_send_racing_close_answers_the_callback_once(self, ws, qtbot, monkeypatch):
        """on_close already failed the callback, so True keeps the caller from a 2nd."""
        monkeypatch.setattr(moonrakerComm.websocket, "WebSocketException", OSError)
        ws.connected = True
        ws.ws = MagicMock()

        def close_then_fail(_packet):
            ws.on_close(None, 1006, "gone")
            raise OSError("broken pipe")

        ws.ws.send.side_effect = close_then_fail
        got = []
        assert ws.send_request("server.info", callback=got.append) is True
        qtbot.waitUntil(lambda: bool(got))
        qtbot.wait(20)
        assert got == [{"error": {"code": -1, "message": "disconnected"}}]

    def test_callback_error_keeps_socket_usable(self, ws):
        """A raising callback reaches on_error but the socket stays open."""
        ws.connected = True
        ws.ws = MagicMock()
        ws.on_error(ws.ws, AttributeError("'FilamentTab' has no '_material_filter'"))
        assert ws.send_request("server.info") is True
        ws.ws.close.assert_not_called()

    def test_send_while_disconnected_never_calls_back(self, ws, qtbot):
        callback = MagicMock()
        assert ws.send_request("server.info", callback=callback) is False
        assert ws.request_table == {}
        qtbot.wait(20)
        callback.assert_not_called()


class TestShutdown:
    def test_disconnect_wakes_dispatcher_and_stops_poll(self, ws):
        ws.ws = MagicMock()
        ws._wst = MagicMock(is_alive=MagicMock(return_value=False))
        ws.wb_disconnect()
        ws.ws.sock.sock.shutdown.assert_called_once_with(socket.SHUT_RD)
        ws.ws.close.assert_not_called()  # teardown on the ws thread sends the close frame
        assert ws.ws.keep_running is False
        ws.query_klippy_status_timer.stopTimer.assert_called_once()

    def test_disconnect_falls_back_to_close(self, ws):
        ws.ws = MagicMock()
        ws.ws.sock.sock.shutdown.side_effect = OSError("not connected")
        ws._wst = MagicMock(is_alive=MagicMock(return_value=False))
        ws.wb_disconnect()
        ws.ws.close.assert_called_once()

    def test_callbacks_silent_after_disconnect(self, ws, monkeypatch, qtbot):
        ws.wb_disconnect()
        connect = MagicMock()
        monkeypatch.setattr(ws, "connect", connect)
        emitted = []
        ws.connected_signal.connect(lambda: emitted.append("open"))
        ws.connection_lost[str].connect(emitted.append)
        ws.server_components_signal.connect(emitted.append)
        ws.ws = MagicMock()
        ws.request_table[1] = ("server.info", {}, None)
        ws.on_open(None)
        ws.on_message(None, json.dumps({"id": 1, "result": {"components": []}}))
        ws.on_close(None, 1000, "bye")
        assert ws.reconnect() is False
        qtbot.wait(20)
        assert emitted == []
        assert ws.connected is False
        connect.assert_not_called()

    def test_real_socket_thread_exits_within_join(self, ws, qtbot, monkeypatch):
        # Unfixed, ~40% of closes left run_forever in epoll for ping_timeout (10 s).
        monkeypatch.delitem(sys.modules, "websocket", raising=False)  # conftest stub
        monkeypatch.setattr(
            moonrakerComm, "websocket", importlib.import_module("websocket")
        )
        port = _serve_ws()
        ws._host, ws._port = "127.0.0.1", port
        ws.moonRest.get_oneshot_token.return_value = "t"
        for _ in range(8):
            ws._closing = False
            assert ws.connect() is True
            qtbot.waitUntil(lambda: ws.connected, timeout=3000)
            start = time.monotonic()
            ws.wb_disconnect()
            assert not ws._wst.is_alive()
            assert time.monotonic() - start < 2
            ws.connected = False


def _serve_ws() -> int:
    """Minimal RFC 6455 server: handshake, then answer a close frame like Moonraker."""
    srv = socket.create_server(("127.0.0.1", 0))

    def _client(conn: socket.socket) -> None:
        with conn:
            req = b""
            while b"\r\n\r\n" not in req:
                req += conn.recv(4096)
            key = next(
                line.split(b":", 1)[1].strip()
                for line in req.split(b"\r\n")
                if line.lower().startswith(b"sec-websocket-key")
            )
            accept = base64.b64encode(hashlib.sha1(key + _WS_GUID).digest())  # nosec B324
            conn.sendall(
                b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n"
                b"Connection: Upgrade\r\nSec-WebSocket-Accept: " + accept + b"\r\n\r\n"
            )
            while (hdr := conn.recv(2)) and len(hdr) == 2:
                length = hdr[1] & 0x7F
                conn.recv(4 + length)
                if hdr[0] & 0x0F == 8:
                    conn.sendall(b"\x88\x02\x03\xe8")
                    return

    def _accept() -> None:
        while True:
            threading.Thread(
                target=_client, args=(srv.accept()[0],), daemon=True
            ).start()

    threading.Thread(target=_accept, daemon=True).start()
    return srv.getsockname()[1]


_WS_GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


@pytest.fixture
def api():
    """MoonAPI over a stub socket; it parents itself to ws, so ws must be a QObject."""
    sock = QtCore.QObject()
    sock.send_request = MagicMock(return_value=True)
    return MoonAPI(sock)


class TestGetSpool:
    def test_goes_through_the_proxy(self, api) -> None:
        api.get_spool(42, None)
        params = api._ws.send_request.call_args.kwargs
        assert params["method"] == "server.spoolman.proxy"
        assert params["params"] == {
            "use_v2_response": False,
            "request_method": "GET",
            "path": "/v1/spool/42",
        }

    def test_passes_the_callback_through(self, api) -> None:
        def cb(_result):
            return None

        api.get_spool(1, cb)
        assert api._ws.send_request.call_args.kwargs["callback"] is cb
