import logging
import threading
from collections.abc import Callable

logger = logging.getLogger(__name__)


class RepeatedTimer:
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
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self._lock = threading.Lock()
        self.running = False
        self.stopEvent = threading.Event()
        self._timer: threading.Thread | None = None
        self.startTimer()

    def _run(self, stopEvent: threading.Event) -> None:
        """Tick until stopEvent is set; wait() is both the sleep and the cancel."""
        while not stopEvent.wait(self._timeout):
            if not callable(self._function):
                continue
            try:
                self._function(*self._args, **self._kwargs)
            except Exception:
                # One bad tick must not kill the thread and silently stop the timer.
                logger.exception("RepeatedTimer %s callback raised", self.name)

    def startTimer(self) -> None:
        """Start timer"""
        with self._lock:
            if self.running:
                return
            # New event per generation so a thread still in a slow callback cannot resume
            self.stopEvent = threading.Event()
            try:
                timer = threading.Thread(
                    target=self._run,
                    args=(self.stopEvent,),
                    name=self.name,
                    daemon=True,
                )
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
            # Unconditional: a stop during the callback must still cancel the loop
            self.stopEvent.set()
        # Bounded join: never stall the caller on a slow callback
        if timer is not threading.current_thread():
            timer.join(timeout=0.1)
