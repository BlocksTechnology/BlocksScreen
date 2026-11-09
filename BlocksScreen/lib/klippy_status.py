"""Klipper state store for ConnectionPage (KlipperScreen printer.py, Mainsail checkKlippyState).

MainWindow, Printer and the panels still act on ``MoonWebSocket.klippy_state_signal``.
"""

from lib.moonrakerComm import MoonWebSocket
from PyQt6 import QtCore


class KlippyStatus(QtCore.QObject):
    """Merge ws link, server.info, webhooks, notify_klippy_* and printer.info."""

    # link: ""|connecting|connected|lost
    # state: ""|startup|ready|error|shutdown|disconnected
    changed = QtCore.pyqtSignal(str, str, str, name="klippy-status-changed")

    _NOTIFY_STATES: frozenset[str] = frozenset({"ready", "shutdown", "disconnected"})

    def __init__(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._ws = ws
        self.link: str = ""
        self.state: str = ""
        self.message: str = ""
        self._gen: int = 0
        # printer.info answered this generation; later reasons come via webhooks
        self._settled: bool = False
        ws.connecting_signal.connect(self.on_connecting)
        ws.connected_signal.connect(self.on_connected)
        ws.connection_lost.connect(self.on_connection_lost)
        ws.klippy_state_signal.connect(self.on_klippy_state)
        ws.klippy_connected_signal.connect(self.on_server_info_tick)

    def _apply(self, link: str, state: str, message: str) -> None:
        if state == "ready":
            message = ""  # Never displayed; sources disagree
        if (link, state, message) == (self.link, self.state, self.message):
            return
        self.link, self.state, self.message = link, state, message
        self.changed.emit(link, state, message)

    def _invalidate(self) -> None:
        """Drop in-flight printer.info and poll again on the next tick."""
        self._gen += 1
        self._settled = False

    def _push_state(self, state: str, message: str | None) -> None:
        self._invalidate()
        if self.link != "connected":
            return  # Resent by server.info on reconnect
        if message is None:
            message = self.message if state == self.state else ""
        self._apply(self.link, state, message)

    def _poll(self) -> None:
        gen = self._gen

        def _on_reply(reply: dict | None) -> None:
            self._on_printer_info(gen, reply)

        self._ws.send_request("printer.info", callback=_on_reply)

    def _on_printer_info(self, gen: int, reply: dict | None) -> None:
        if gen != self._gen or self.link != "connected":
            return
        if not isinstance(reply, dict) or "error" in reply:
            return  # 503 while Klippy is disconnected
        state = reply.get("state")
        if not state:
            return
        self._settled = True
        self._apply(self.link, state, reply.get("state_message") or "")

    @QtCore.pyqtSlot(name="on-connecting")
    def on_connecting(self, *_: object) -> None:
        """Mark the websocket as reconnecting."""
        self._invalidate()
        self._apply("connecting", "", "")

    @QtCore.pyqtSlot(name="on-connected")
    def on_connected(self) -> None:
        """Mark the websocket open; Klipper state arrives with the next server.info."""
        self._invalidate()
        self._apply("connected", "", "")

    @QtCore.pyqtSlot(str, name="on-connection-lost")
    def on_connection_lost(self, *_: object) -> None:
        """Forget Klipper state and drop any in-flight printer.info."""
        self._invalidate()
        self._apply("lost", "", "")

    @QtCore.pyqtSlot(str, name="on-klippy-state")
    def on_klippy_state(self, state: str) -> None:
        """Take a server.info transition; the tick that follows fetches its reason."""
        self._push_state(state, None)

    @QtCore.pyqtSlot(bool, name="on-server-info-tick")
    def on_server_info_tick(self, klippy_connected: bool) -> None:
        """Poll printer.info on server.info ticks until it answers for the current state."""
        # Also recovers a reconnect whose state transition never reached the store
        if (
            klippy_connected
            and self.link == "connected"
            and self.state != "ready"
            and not self._settled
        ):
            self._poll()

    @QtCore.pyqtSlot(str, str, name="on-webhooks")
    def on_webhooks(self, state: str, message: str) -> None:
        """Take state and reason from the webhooks subscription."""
        if state:
            self._push_state(state, message)

    @QtCore.pyqtSlot(str, name="on-klippy-notify")
    def on_klippy_notify(self, state: str) -> None:
        """Take a notify_klippy_ready/shutdown/disconnected state."""
        if state in self._NOTIFY_STATES:
            self._push_state(state, None)
