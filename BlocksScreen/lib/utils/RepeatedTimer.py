import threading


class RepeatedTimer(threading.Thread):
    def __init__(
        self,
        timeout,
        callback,
        name="RepeatedTimer",
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
        self._timer = None
        self.startTimer()

    def _run(self):
        """Invoke the callback and restart the timer loop, unless stopped."""
        with self._lock:
            self.running = False
            if self.stopEvent.is_set():
                return
        if callable(self._function):
            self._function(*self._args, **self._kwargs)
        self.startTimer()

    def startTimer(self):
        """Start timer"""
        with self._lock:
            if self.running:
                return
            self.stopEvent.clear()
            try:
                timer = threading.Timer(self._timeout, self._run)
                timer.daemon = True
                self._timer = timer
                self.running = True
            except Exception as e:
                self.running = False
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                ) from e
        # Start outside the lock to avoid holding it during thread creation
        timer.start()

    def stopTimer(self):
        """Stop timer"""
        with self._lock:
            if self._timer is None or not self.running:
                return
            timer = self._timer
            self._timer = None
            self.running = False
            self.stopEvent.set()
        timer.cancel()
        timer.join()
