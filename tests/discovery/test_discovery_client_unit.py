"""DeviceDiscoveryClient against a fake device_discoveryd socket.

Signals are connected with DirectConnection so they fire on the client's
reader thread and land in a queue - no Qt event loop needed.
"""

import json
import logging
import queue
import time

import pytest
from PyQt6 import QtCore

from devices.discovery import client as dd_client
from devices.discovery.client import DeviceDiscoveryClient

from .conftest import FakeDaemon

DIRECT = QtCore.Qt.ConnectionType.DirectConnection
TIMEOUT = 5.0


def _collect(client):
    events = queue.Queue()
    client.snapshot_ready.connect(lambda v: events.put(("snapshot", v)), DIRECT)
    client.device_added.connect(lambda v: events.put(("added", v)), DIRECT)
    client.device_removed.connect(lambda v: events.put(("removed", v)), DIRECT)
    client.daemon_connected.connect(lambda: events.put(("connected", None)), DIRECT)
    return events


def _next(events):
    return events.get(timeout=TIMEOUT)


class TestDefaultSocketPath:
    def test_env_var_wins(self, monkeypatch):
        monkeypatch.setenv("DEVICE_DISCOVERY_SOCKET", "/x/y.sock")
        assert dd_client.default_socket_path() == "/x/y.sock"

    def test_systemd_path_when_present(self, monkeypatch):
        monkeypatch.delenv("DEVICE_DISCOVERY_SOCKET", raising=False)
        monkeypatch.setattr(
            dd_client.os.path, "exists", lambda p: p == dd_client.SYSTEMD_SOCKET_PATH
        )
        assert dd_client.default_socket_path() == dd_client.SYSTEMD_SOCKET_PATH

    def test_xdg_fallback(self, monkeypatch):
        monkeypatch.delenv("DEVICE_DISCOVERY_SOCKET", raising=False)
        monkeypatch.setenv("XDG_RUNTIME_DIR", "/run/user/1000")
        monkeypatch.setattr(dd_client.os.path, "exists", lambda p: False)
        assert (
            dd_client.default_socket_path()
            == "/run/user/1000/blockscreen/device_discovery.sock"
        )

    def test_no_tmp_fallback(self, monkeypatch):
        monkeypatch.delenv("DEVICE_DISCOVERY_SOCKET", raising=False)
        monkeypatch.delenv("XDG_RUNTIME_DIR", raising=False)
        monkeypatch.setattr(dd_client.os.path, "exists", lambda p: False)
        assert dd_client.default_socket_path() == dd_client.SYSTEMD_SOCKET_PATH


class TestProtocol:
    def test_snapshot_added_removed(self, sock_path):
        dev = {"name": "Klipper stm32h723xx", "connection": "Serial"}
        daemon = FakeDaemon(
            sock_path,
            [
                {"type": "hello", "proto": 1, "pid": 1},
                {"type": "snapshot", "devices": [dev]},
                {"type": "added", "device": dev},
                {"type": "removed", "device": dev},
            ],
        )
        client = DeviceDiscoveryClient(sock_path)
        events = _collect(client)
        client.start()
        try:
            assert _next(events) == ("connected", None)
            assert _next(events) == ("snapshot", [dev])
            assert _next(events) == ("added", dev)
            assert _next(events) == ("removed", dev)
        finally:
            client.stop()
            daemon.close()

    def test_malformed_and_unknown_lines_are_skipped(self, sock_path):
        daemon = FakeDaemon(
            sock_path,
            [
                b"not json",
                {"type": "future_message"},
                {"type": "snapshot", "devices": []},
            ],
        )
        client = DeviceDiscoveryClient(sock_path)
        events = _collect(client)
        client.start()
        try:
            assert _next(events) == ("connected", None)
            assert _next(events) == ("snapshot", [])
        finally:
            client.stop()
            daemon.close()

    def test_protocol_mismatch_warns(self, caplog):
        client = DeviceDiscoveryClient("/nonexistent")
        with caplog.at_level(logging.WARNING, logger=dd_client.__name__):
            client._dispatch(json.dumps({"type": "hello", "proto": 99}).encode())
        assert "protocol 99" in caplog.text

    def test_stop_without_daemon_returns(self, sock_path):
        client = DeviceDiscoveryClient(sock_path)  # nothing listening
        client.start()
        client.stop()
        assert not client._thread.is_alive()

    def test_stop_before_start(self):
        DeviceDiscoveryClient("/nonexistent").stop()


@pytest.fixture
def thread_exceptions(monkeypatch):
    """Exceptions that reached threading.excepthook (CrashHandler exits on these)."""
    import threading

    seen = []
    monkeypatch.setattr(threading, "excepthook", lambda args: seen.append(args))
    return seen


BAD_LINES = [
    b"not json",
    b"\xff\xfe bad utf-8",
    b"[" * 100000,  # deep nesting -> RecursionError in json
    b"42",
    b"[1, 2]",
    b'{"no": "type"}',
    b'{"type": 7}',
    b'{"type": "added"}',
    b'{"type": "added", "device": "x"}',
    b'{"type": "removed", "device": null}',
    b'{"type": "snapshot"}',
    b'{"type": "snapshot", "devices": {"a": 1}}',
    b'{"type": "hello", "proto": "banana"}',
]


class TestBrokenDaemon:
    def test_bad_messages_are_skipped_and_reading_continues(
        self, sock_path, thread_exceptions
    ):
        good = {"name": "ok", "connection": "Serial"}
        daemon = FakeDaemon(
            sock_path,
            BAD_LINES
            + [
                {"type": "snapshot", "devices": [1, "x", good]},
                {"type": "added", "device": good},
            ],
        )
        client = DeviceDiscoveryClient(sock_path)
        events = _collect(client)
        client.start()
        try:
            assert _next(events) == ("connected", None)
            assert _next(events) == ("snapshot", [good])  # non-dicts filtered
            assert _next(events) == ("added", good)
            assert client._thread.is_alive()
        finally:
            client.stop()
            daemon.close()
        assert thread_exceptions == []

    def test_oversized_line_drops_the_connection(self, sock_path, thread_exceptions):
        daemon = FakeDaemon(sock_path, [b"x" * (dd_client._MAX_LINE + 70000)])
        client = DeviceDiscoveryClient(sock_path)
        gone = queue.Queue()
        client.daemon_disconnected.connect(lambda: gone.put(True), DIRECT)
        client.start()
        try:
            assert gone.get(timeout=TIMEOUT)
            assert client._thread.is_alive()  # reconnecting, not dead
        finally:
            client.stop()
            daemon.close()
        assert thread_exceptions == []

    def test_unexpected_error_keeps_the_thread_alive(
        self, sock_path, monkeypatch, thread_exceptions
    ):
        calls = []

        def boom(self):
            calls.append(1)
            raise RuntimeError("bug")

        monkeypatch.setattr(DeviceDiscoveryClient, "_connect_and_read", boom)
        monkeypatch.setattr(dd_client, "_RECONNECT_DELAYS", (0.05,))
        client = DeviceDiscoveryClient(sock_path)
        client.start()
        try:
            deadline = time.monotonic() + TIMEOUT
            while len(calls) < 3 and time.monotonic() < deadline:
                time.sleep(0.02)
            assert len(calls) >= 3 and client._thread.is_alive()
        finally:
            client.stop()
        assert thread_exceptions == []

    @pytest.mark.parametrize("line", BAD_LINES)
    def test_fetch_snapshot_never_raises(self, sock_path, line):
        daemon = FakeDaemon(sock_path, [line])
        try:
            assert dd_client.fetch_snapshot(sock_path, timeout=0.5) is None
        finally:
            daemon.close()

    def test_fetch_snapshot_hung_daemon_is_bounded(self, sock_path):
        daemon = FakeDaemon(sock_path, [])  # accepts, never sends
        try:
            t0 = time.monotonic()
            assert dd_client.fetch_snapshot(sock_path, timeout=0.5) is None
            assert time.monotonic() - t0 < 1.5
        finally:
            daemon.close()
