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
        super().__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = callback
        self._args = args
        self._kwargs = kwargs

        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()

    def _run(self):
        self.running = False
        self.startTimer()
        self.stopEvent.wait()
        if callable(self._function):
            self._function(*self._args, **self._kwargs)

    def startTimer(self):
        """Start timer"""
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if not self.stopEvent.is_set():
                    self.stopEvent.set()
            except Exception as e:
                raise Exception(
                    f"RepeatedTimer {self.name} error while starting timer, error: {e}"
                )
            finally:
                self.running = False
            self.running = True

    def stopTimer(self):
        """Stop timer"""
        if self._timer is None:
            return
        if self.running:
            self._timer.cancel()
            self._timer.join()
            self._timer = None
            self.stopEvent.clear()
            self.running = False
