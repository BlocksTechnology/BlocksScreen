"""Shared fixtures: a fake device_discoveryd on a short-path Unix socket."""

import json
import os
import socket
import sys
import tempfile
import threading

import pytest

# App modules import top-level packages (`from tools...`, `from devices...`)
# with BlocksScreen/ on sys.path, as BlocksScreen.py sets it up. Appended,
# not prepended: first on the path, BlocksScreen/BlocksScreen.py (the entry
# script) would shadow the `BlocksScreen` package for every other test.
_BS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "BlocksScreen")
)
if _BS_DIR not in sys.path:
    sys.path.append(_BS_DIR)


@pytest.fixture
def sock_path():
    # Not tmp_path: AF_UNIX paths are limited to 108 bytes.
    d = tempfile.mkdtemp(prefix="dd-", dir="/tmp")
    path = os.path.join(d, "s.sock")
    yield path
    if os.path.exists(path):
        os.unlink(path)
    os.rmdir(d)


class FakeDaemon:
    """Accepts one client and sends it the given lines."""

    def __init__(self, path, messages):
        self._srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._srv.bind(path)
        self._srv.listen(1)
        self._payload = b"".join(
            (m if isinstance(m, bytes) else json.dumps(m).encode()) + b"\n"
            for m in messages
        )
        self._conn = None
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def _serve(self):
        self._conn, _ = self._srv.accept()
        # Split mid-line to exercise the client's line buffering.
        half = len(self._payload) // 2
        self._conn.sendall(self._payload[:half])
        self._conn.sendall(self._payload[half:])

    def close(self):
        if self._conn:
            self._conn.close()
        self._srv.close()
