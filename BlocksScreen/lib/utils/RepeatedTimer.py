import logging
import threading
from collections.abc import Callable

logger = logging.getLogger(__name__)


class RepeatedTimer(threading.Thread):
    """Periodic callback driven by one long-lived thread per start/stop cycle."""

    def __init__(
        self,
        timeout: float,
        callback: Callable[..., object],
        name: str = "RepeatedTimer",
        *args,
        **kwargs,
    ):
        """Initialize a repeating timer that invokes callback every timeout seconds."""
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self._lock = threading.Lock()
        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer: threading.Thread | None = None
        self.startTimer()

    def _run(self) -> None:
        """Tick until stopped; wait() doubles as the sleep and the cancel signal."""
        # wait() returns True only when stopEvent is set, so a stop exits immediately
        # instead of burning the rest of the period.
        while not self.stopEvent.wait(self._timeout):
            if not callable(self._function):
                continue
            try:
                self._function(*self._args, **self._kwargs)
            except Exception:
                # One bad tick must not kill the thread and silently stop the timer.
                logger.exception("RepeatedTimer %s callback raised", self.name)
        with self._lock:
            self.running = False

    def startTimer(self) -> None:
        """Start timer"""
        with self._lock:
            if self.running:
                return
            self.stopEvent.clear()
            try:
                timer = threading.Thread(target=self._run, name=self.name, daemon=True)
                self._timer = timer
                self.running = True
            except Exception as e:
                self.running = False
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                ) from e
        # Start outside the lock to avoid holding it during thread creation
        timer.start()

    def stopTimer(self) -> None:
        """Stop timer"""
        with self._lock:
            if self._timer is None or not self.running:
                return
            timer = self._timer
            self._timer = None
            self.running = False
            # Set unconditionally so a stop during the callback still cancels the loop.
            self.stopEvent.set()
        # Bounded join: never stall the GUI thread waiting on a slow callback.
        if timer is not threading.current_thread():
            timer.join(timeout=0.1)
