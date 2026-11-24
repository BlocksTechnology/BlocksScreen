"""Helpers for the callback replies of ``MoonAPI`` requests."""

import logging
from collections.abc import Callable
from dataclasses import dataclass

from PyQt6 import QtCore

_logger = logging.getLogger(__name__)

# -1: websocket closed; 503: Moonraker fails pending requests on a Klippy disconnect
_DISCONNECT_CODES = frozenset({-1, 503})

# RF50 first G28 from the top runs BEACON_AUTO_CALIBRATE at 3 mm/s: ~165 s from Z 486
FIRST_HOME_TIMEOUT_MS = 300_000

BUSY_MESSAGE = (
    "The printer is still running a command.\nWait for it to finish, then try again."
)


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

    def __init__(
        self,
        timeout_ms: int,
        parent: QtCore.QObject | None = None,
        *,
        runner: Callable[..., bool] | None = None,
        klippy_busy: Callable[[], bool] | None = None,
    ) -> None:
        super().__init__(parent)
        # MoonAPI.run_gcode(script, callback=...); False means the request was not sent
        self.runner = runner
        # Klipper's own busy state; a websocket drop answers -1 while it keeps running
        self.klippy_busy = klippy_busy
        # Silence limit restored on every progress sign
        self.timeout_ms = timeout_ms
        self._id = 0
        self._active = False
        # One token per sent script awaiting its reply
        self._pending: set[object] = set()
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
        """True while active, while a reply is owed, or while Klipper reports busy."""
        if self._active or self._pending:
            return True
        return self.klippy_busy is not None and self.klippy_busy()

    def start(self, timeout_ms: int | None = None) -> None:
        """Begin a run; ``timeout_ms`` overrides the limit until the first progress."""
        self._active = True
        self._watchdog.start(timeout_ms or self.timeout_ms)

    def stop(self) -> None:
        """End the run; replies still in flight no longer reach its handlers."""
        self._id += 1
        self._active = False
        self._watchdog.stop()

    def feed(self) -> None:
        """Restart the watchdog on progress, unless paused."""
        if self._watchdog.isActive():
            self._watchdog.start(self.timeout_ms)

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


@dataclass(frozen=True)
class CalibrationText:
    """User-facing texts of one homed calibration flow."""

    title: str  # Used mid-sentence, such as "Z-Tilt" or "input shaper"
    homing: str  # Overlay while the first G28 runs
    running: str  # Overlay once homed
    failed: str  # Result when the calibration command errors
    done: str = ""  # Result on success; empty shows none
    rehoming: str = "Homing the printer"


class HomedCalibration(GcodeRun):
    """Home, calibrate, re-home, report once; the overlay lives as long as the run."""

    # Like Mainsail's named loadings, dropped on reply (webSocketClient.ts removeWaitById)

    overlay = QtCore.pyqtSignal(bool, str, bool, name="overlay")
    finished = QtCore.pyqtSignal(bool, str, name="finished")

    def __init__(
        self,
        text: CalibrationText,
        timeout_ms: int,
        parent: QtCore.QObject | None = None,
        *,
        runner: Callable[..., bool] | None = None,
        klippy_busy: Callable[[], bool] | None = None,
    ) -> None:
        super().__init__(timeout_ms, parent, runner=runner, klippy_busy=klippy_busy)
        self.text = text
        self._lead = text.title[:1].upper() + text.title[1:]
        self._script = ""
        self._rehome = ""
        self._then: Callable[[], None] | None = None
        self._failed = False
        self._rehome_lost = False
        self.timed_out.connect(self._on_timed_out)

    def refused(self) -> bool:
        """True if Klipper or an earlier run is busy; reports it unless a run is up."""
        if not self.busy:
            return False
        # A lost link or timeout can leave Klipper busy; a new run would queue
        if not self.active:
            self.finished.emit(False, BUSY_MESSAGE)
        return True

    def run(
        self, script: str, rehome: str = "", then: Callable[[], None] | None = None
    ) -> None:
        """Home, run ``script``, then ``rehome``; ``then`` replaces the report on success."""
        self._script, self._rehome, self._then = script, rehome, then
        self._failed = self._rehome_lost = False
        self.start(FIRST_HOME_TIMEOUT_MS)
        self.show(self.text.homing)
        if not self.send("G28\nM400", self._on_first_home):
            self._unsent()

    def show(self, text: str) -> None:
        """Update the overlay text while the run lasts."""
        if self.active:
            self.overlay.emit(True, text, False)

    def end(self, ok: bool, message: str = "") -> None:
        """Finish the run, force the overlay closed and report ``message``."""
        self.stop()
        # Forced: MainWindow drops unforced hides while its restart guards are set
        self.overlay.emit(False, "", True)
        self.finished.emit(ok, message)

    def drop(self) -> None:
        """End a run whose link was lost; ConnectionPage or a restart overlay takes over."""
        self.stop()
        # Unforced, so a Klipper restart overlay already up stays
        self.overlay.emit(False, "", False)
        self.finished.emit(False, "")

    def _unsent(self) -> None:
        _logger.warning("%s: request not sent, Moonraker unreachable", self._lead)
        self.drop()

    def _on_first_home(self, reply: object) -> None:
        error = reply_error(reply)
        if is_disconnect_error(error):
            self.drop()
            return
        if error is not None:
            self.end(False, "Homing failed.\nCheck the printer and try again.")
            return
        self.show(self.text.running)
        # Separate scripts so the final home still runs after a failed calibration
        if not self.send(self._script, self._on_calibrated):
            self._unsent()
            return
        if self._rehome and not self.send(self._rehome, self._on_rehomed):
            # The calibration already moves the printer: keep the overlay until it replies
            _logger.warning("%s: final home not sent", self._lead)
            self._rehome_lost = True

    def _on_calibrated(self, reply: object) -> None:
        error = reply_error(reply)
        if is_disconnect_error(error):
            self.drop()
            return
        self._failed = error is not None
        if error is not None:
            _logger.warning("%s failed: %s", self._lead, error.get("message"))
        if self._rehome and not self._rehome_lost:
            status = "failed" if self._failed else "complete"
            self.show(f"{self._lead} calibration {status}\n{self.text.rehoming}")
        elif self._failed:
            self.end(False, self.text.failed)
        elif self._rehome_lost:
            self.end(
                False,
                f"{self._lead} calibration finished, but the printer was not re-homed."
                "\nHome the printer before printing.",
            )
        elif self._then is not None:
            self._then()
        else:
            self.end(True, self.text.done)

    def _on_rehomed(self, reply: object) -> None:
        error = reply_error(reply)
        if is_disconnect_error(error):
            self.drop()
        elif self._failed:
            self.end(False, self.text.failed)
        elif error is not None:
            self.end(
                False,
                f"Homing failed after {self.text.title} calibration.\n"
                "Home the printer before printing.",
            )
        else:
            self.end(True, self.text.done)

    def _on_timed_out(self) -> None:
        _logger.warning(
            "%s: no progress for %d s, closing the overlay",
            self._lead,
            self._watchdog.interval() // 1000,
        )
        self.overlay.emit(False, "", True)
        self.finished.emit(
            False,
            f"{self._lead} calibration timed out.\nCheck the printer and try again.",
        )
