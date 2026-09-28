"""Qt client for the device_discoveryd daemon.

The daemon lives in its own repo (BlocksTechnology/DeviceDiscovery) and runs
as device-discoveryd.service; its docs/PROTOCOL.md is the contract this client
implements.

Owns a dedicated background thread that connects to the daemon's Unix
socket and blocks reading newline-delimited JSON messages. Results are
bridged back to Qt via pyqtSignals, mirroring the shape of
lib/updater_worker.py's D-Bus client - a background thread doing blocking
I/O, reconnecting with backoff, never touching Qt objects except through
signal emission (which is thread-safe: PyQt auto-queues the connection
when emitter and receiver live on different threads).

Unlike updater_worker.py this doesn't need asyncio: the protocol here is
one blocking recv() loop, so an event loop would add ceremony without
buying anything.
"""

from __future__ import annotations

import json
import logging
import os
import socket
import threading
import time
from typing import Any

from PyQt6 import QtCore

_log = logging.getLogger(__name__)

_RECONNECT_DELAYS = (2.0, 5.0, 10.0, 30.0)
_RECV_CHUNK = 65536
# A line longer than this is not a real message (the daemon caps what it
# queues per client at the same size): drop the connection instead of
# buffering without bound.
_MAX_LINE = 1 << 20

SUPPORTED_PROTOCOL = 1
"""Protocol version (the daemon's `hello.proto`) this client understands."""

SYSTEMD_SOCKET_PATH = "/run/device-discovery/device_discovery.sock"
"""Where device-discoveryd.service puts the socket (RuntimeDirectory=)."""


def default_socket_path() -> str:
    """Resolve the daemon socket path.

    `$DEVICE_DISCOVERY_SOCKET` wins, then the systemd service's path if it
    exists, then the daemon's fallback for runs outside systemd
    (`$XDG_RUNTIME_DIR`). The daemon's last-resort /tmp path is deliberately
    not followed: any local user could create it and feed the UI fake
    devices. With no match, the systemd path is returned and the client
    keeps retrying until the service comes up.
    """
    env_path = os.environ.get("DEVICE_DISCOVERY_SOCKET")
    if env_path:
        return env_path
    if os.path.exists(SYSTEMD_SOCKET_PATH):
        return SYSTEMD_SOCKET_PATH
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
    if runtime_dir:
        return os.path.join(runtime_dir, "blockscreen", "device_discovery.sock")
    return SYSTEMD_SOCKET_PATH


def _describe(device: dict[str, Any]) -> str:
    """One-line summary of a daemon device object for the log."""
    # vid_hex is only meaningful on USB entries (the daemon sends 0 for Serial).
    usb_id = (
        f"{device.get('vid_hex')}:{device.get('pid_hex')}"
        if device.get("connection") == "USB"
        else ""
    )
    return "{} [{}] {} {}".format(
        device.get("symlink_name") or device.get("name") or "?",
        device.get("connection", "?"),
        device.get("device_path") or "",
        usb_id,
    ).strip()


def _parse_message(line: bytes) -> dict[str, Any] | None:
    """Decode and validate one protocol line.

    Returns None for anything that isn't a well-formed message, so a broken
    or misbehaving daemon can never raise into the caller: unhandled
    exceptions (in any thread) make CrashHandler exit BlocksScreen.
    """
    try:
        msg = json.loads(line)
    except (ValueError, RecursionError):  # JSONDecodeError, bad UTF-8, deep nesting
        _log.warning("Malformed message from device_discoveryd: %r", line[:200])
        return None
    if not isinstance(msg, dict) or not isinstance(msg.get("type"), str):
        _log.warning("Invalid message from device_discoveryd: %r", line[:200])
        return None
    msg_type = msg["type"]
    if msg_type in ("added", "removed") and not isinstance(msg.get("device"), dict):
        _log.warning("device_discoveryd %s without a device object", msg_type)
        return None
    if msg_type == "snapshot":
        devices = msg.get("devices")
        if not isinstance(devices, list):
            _log.warning("device_discoveryd snapshot without a device list")
            return None
        msg["devices"] = [d for d in devices if isinstance(d, dict)]
    return msg


def fetch_snapshot(
    socket_path: str | None = None, timeout: float = 2.0
) -> list[dict[str, Any]] | None:
    """One-shot blocking query: connect, read hello + snapshot, disconnect.

    For code that needs the current device list synchronously and has no Qt
    event loop, such as the configuration manager at startup. Returns the
    snapshot's device dicts, or None when the daemon is unreachable, speaks
    an unsupported protocol, or sends no snapshot within `timeout` seconds -
    callers treat None as "fall back to another source".
    """
    path = socket_path or default_socket_path()
    deadline = time.monotonic() + timeout
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect(path)
            buf = b""
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    _log.debug("device_discoveryd: no snapshot within %.1fs", timeout)
                    return None
                sock.settimeout(remaining)
                chunk = sock.recv(_RECV_CHUNK)
                if not chunk:
                    return None
                buf += chunk
                if b"\n" not in buf and len(buf) > _MAX_LINE:
                    _log.warning("device_discoveryd sent an oversized line")
                    return None
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    msg = _parse_message(line) if line else None
                    if msg is None:
                        continue
                    msg_type = msg["type"]
                    if msg_type == "hello" and msg.get("proto") != SUPPORTED_PROTOCOL:
                        _log.warning(
                            "device_discoveryd speaks protocol %s, client supports %s",
                            msg.get("proto"),
                            SUPPORTED_PROTOCOL,
                        )
                        return None
                    if msg_type == "snapshot":
                        return msg["devices"]
    except OSError as exc:
        _log.debug("device_discoveryd snapshot unavailable at %s: %s", path, exc)
        return None


class DeviceDiscoveryClient(QtCore.QObject):
    """Background client for the device-discovery daemon's report socket.

    Connect to the signals first, then call start(): the daemon sends its
    snapshot immediately on connect, so starting earlier can drop it.
    """

    device_added = QtCore.pyqtSignal(dict, name="dd-device-added")
    device_removed = QtCore.pyqtSignal(dict, name="dd-device-removed")
    snapshot_ready = QtCore.pyqtSignal(list, name="dd-snapshot-ready")
    daemon_connected = QtCore.pyqtSignal(name="dd-daemon-conn")
    daemon_disconnected = QtCore.pyqtSignal(name="dd-daemon-disc")

    def __init__(self, socket_path: str | None = None) -> None:
        super().__init__()
        # None = resolve on every connection attempt: the systemd socket may
        # not exist yet when BlocksScreen starts (the daemon is Type=simple,
        # so it can still be binding), and a path fixed at construction
        # would then point at the fallback forever.
        self._explicit_path = socket_path
        self._stop_event = threading.Event()
        self._sock: socket.socket | None = None
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="DeviceDiscoveryClient"
        )

    def start(self) -> None:
        """Starts the reader thread. Call once, after connecting signals."""
        self._thread.start()

    def stop(self) -> None:
        """Stops the client and joins its thread. Safe to call once, from any thread."""
        self._stop_event.set()
        sock = self._sock
        if sock is not None:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        if self._thread.is_alive():
            self._thread.join(timeout=5.0)

    def _socket_path(self) -> str:
        return self._explicit_path or default_socket_path()

    def _run(self) -> None:
        attempt = 0
        while not self._stop_event.is_set():
            path = self._socket_path()
            try:
                self._connect_and_read(path)
                if not self._stop_event.is_set():
                    _log.info("device_discoveryd closed the connection, reconnecting")
                attempt = (
                    0  # clean disconnect after a working connection: reset backoff
                )
            except OSError as exc:
                # First failure at INFO so a missing/unreachable daemon shows
                # up in the journal; the retries after it stay at DEBUG.
                log = _log.info if attempt == 0 else _log.debug
                log("device_discoveryd not reachable at %s: %s", path, exc)
            except Exception:  # noqa: BLE001  # pylint: disable=broad-except
                # A bug here must not end the thread: CrashHandler would
                # exit the whole UI. Log it and reconnect with backoff.
                _log.exception("device_discoveryd client error, reconnecting")

            if self._stop_event.is_set():
                return

            self.daemon_disconnected.emit()
            delay = _RECONNECT_DELAYS[min(attempt, len(_RECONNECT_DELAYS) - 1)]
            attempt += 1
            self._stop_event.wait(delay)

    def _connect_and_read(self, path: str) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(2.0)  # periodic wake-up so stop_event is noticed promptly
        try:
            sock.connect(path)
        except OSError:
            sock.close()
            raise
        self._sock = sock
        self.daemon_connected.emit()
        _log.info("Connected to device_discoveryd at %s", path)

        buf = b""
        try:
            while not self._stop_event.is_set():
                try:
                    chunk = sock.recv(_RECV_CHUNK)
                except TimeoutError:
                    continue
                if not chunk:
                    return  # daemon closed the connection
                buf += chunk
                if b"\n" not in buf and len(buf) > _MAX_LINE:
                    _log.warning(
                        "device_discoveryd sent an oversized line, reconnecting"
                    )
                    return
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    if line:
                        self._dispatch(line)
        finally:
            self._sock = None
            sock.close()

    def _dispatch(self, line: bytes) -> None:
        msg = _parse_message(line)
        if msg is None:
            return
        msg_type = msg["type"]
        if msg_type == "snapshot":
            _log.info(
                "device_discoveryd snapshot: %d devices, serial: %s",
                len(msg["devices"]),
                [
                    d.get("symlink_name")
                    for d in msg["devices"]
                    if d.get("connection") == "Serial"
                ],
            )
            self.snapshot_ready.emit(msg["devices"])
        elif msg_type == "added":
            _log.info("device_discoveryd added: %s", _describe(msg["device"]))
            self.device_added.emit(msg["device"])
        elif msg_type == "removed":
            _log.info("device_discoveryd removed: %s", _describe(msg["device"]))
            self.device_removed.emit(msg["device"])
        elif msg_type == "hello":
            proto = msg.get("proto")
            if proto != SUPPORTED_PROTOCOL:
                _log.warning(
                    "device_discoveryd speaks protocol %s, client supports %s",
                    proto,
                    SUPPORTED_PROTOCOL,
                )
            _log.info("device_discoveryd hello: proto=%s pid=%s", proto, msg.get("pid"))
        else:
            _log.debug("Unknown message type from device_discoveryd: %s", msg_type)
