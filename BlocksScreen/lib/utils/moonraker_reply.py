"""Helpers for the callback replies of ``MoonAPI`` requests."""

from collections.abc import Callable

from PyQt6 import QtCore

# -1: websocket closed; 503: Moonraker fails pending requests on a Klippy disconnect
_DISCONNECT_CODES = frozenset({-1, 503})


def reply_error(reply: object) -> dict | None:
    """Return the error of a ``send_request`` callback reply, or None on success."""
    if not isinstance(reply, dict) or reply.get("error") is None:
        return None
    error = reply["error"]
    return error if isinstance(error, dict) else {"message": str(error)}


def is_disconnect_error(error: dict | None) -> bool:
    """True if a reply error means the link to Klipper was lost, not a failed command."""
    return error is not None and error.get("code") in _DISCONNECT_CODES


class GcodeRun(QtCore.QObject):
    """A gcode sequence driven by its replies, with an inactivity watchdog."""

    timed_out = QtCore.pyqtSignal(name="timed-out")

    def __init__(self, timeout_ms: int, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        # MoonAPI.run_gcode(script, callback=...); False means the request was not sent
        self.runner: Callable[..., bool] | None = None
        self._id = 0
        self._active = False
        self._pending: set[object] = (
            set()
        )  # one token per sent script awaiting its reply
        self._watchdog = QtCore.QTimer(self)
        self._watchdog.setSingleShot(True)
        self._watchdog.setInterval(timeout_ms)
        self._watchdog.timeout.connect(self._on_timeout)

    @property
    def active(self) -> bool:
        """True from ``start`` until ``stop`` or a timeout."""
        return self._active

    @property
    def busy(self) -> bool:
        """True while active or while Klipper still owes a reply to a sent script."""
        return self._active or bool(self._pending)

    def start(self) -> None:
        """Begin a run and arm the watchdog."""
        self._active = True
        self._watchdog.start()

    def stop(self) -> None:
        """End the run; replies still in flight no longer reach its handlers."""
        self._id += 1
        self._active = False
        self._watchdog.stop()

    def feed(self) -> None:
        """Restart the watchdog on progress, unless paused."""
        if self._watchdog.isActive():
            self._watchdog.start()

    def forget_replies(self) -> None:
        """Drop pending replies on a Klippy (re)start: a new Klippy owes none."""
        self._pending.clear()

    def pause(self) -> None:
        """Disarm the watchdog for a step that always replies, such as SAVE_CONFIG."""
        self._watchdog.stop()

    def send(self, script: str, handler: Callable[[object], None]) -> bool:
        """Run ``script``; ``handler`` gets the reply while this run lasts."""
        run_id, token = self._id, object()

        def on_reply(reply: object) -> None:
            self._pending.discard(token)
            if run_id == self._id:
                self.feed()
                handler(reply)

        # Counted first, so a runner that replies synchronously stays balanced
        self._pending.add(token)
        if self.runner is not None and self.runner(script, callback=on_reply):
            return True
        self._pending.discard(token)
        return False

    def _on_timeout(self) -> None:
        self.stop()
        self.timed_out.emit()
