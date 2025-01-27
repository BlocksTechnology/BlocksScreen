import threading 

class RepeatedTimer(threading.Thread):
    def __init__(self, timeout, function, name="RepeatedTimer", *args, **kwargs):
        super(RepeatedTimer, self).__init__(daemon=True)
        self.name = name
        self._timeout = timeout
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()

    def startTimer(self):
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon = True
                self._timer.start()
                if self.stopEvent.is_set() is False:
                    self.stopEvent.set()
            except Exception as e : 
                raise Exception(f"RepeatedTimer {self.name} error while starting timer, error: {e}")
            finally: 
                self.running = False 
            self.running = True

    def _run(self):
        self.running = False
        self.startTimer()
        self.stopEvent.wait()
        if callable(self._function):  # and self.stopEvent.is_set() is False:
            self._function(*self._args, **self._kwargs)

    def stopTimer(self):
        # self._timer.cancel()
        if self._timer is None:
            return
        if self.running:
            self._timer.cancel()
            self.stopEvent.clear()
            self.running = False

    @staticmethod
    def pauseTimer(self):
        # TODO never tested
        self.stopEvent.clear()
        self.running = False

    @staticmethod
    def resumeTimer(self):
        # TODO: never tested
        self.stopEvent.set()
        self.running = True