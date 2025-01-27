import copy
import logging
import logging.handlers
import queue
import threading


class QueueHandler(logging.Handler):
    """Handler that sends events to a queue"""

    def __init__(
        self,
        queue: queue.Queue,
        format: str = "'[%(levelname)s] | %(asctime)s | %(name)s | %(relativeCreated)6d | %(threadName)s : %(message)s",
        level=logging.DEBUG,
    ):
        super(QueueHandler, self).__init__()
        self.log_queue = queue
        self.setFormatter(logging.Formatter(format, validate=True))
        self.setLevel(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            record = copy.copy(record)
            record.message = msg
            record.name = record.name
            record.msg = msg
            self.log_queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def flush(self): ...

    # TODO: Implement this

    def setFormatter(self, fmt: logging.Formatter | None) -> None:
        return super().setFormatter(fmt)


class QueueListener(logging.handlers.TimedRotatingFileHandler):
    """Threaded listener watching for log records on the queue handler queue, passes them for processing"""

    def __init__(self, filename, encoding="utf-8"):
        super(QueueListener, self).__init__(
            filename=filename, when="MIDNIGHT", backupCount=10, encoding=encoding, delay=True
        )
        self.queue = queue.Queue()
        self._thread = threading.Thread(name=f"log.{filename}",target=self._run, daemon=True)
        self._thread.start()
        

    def _run(self):
        while True:
            try:
                record = self.queue.get(True)
                if record is None:
                    break
                self.handle(record)
            except queue.Empty:
                break

    def close(self):
        if self._thread is None:
            return
        self.queue.put_nowait(None)
        self._thread.join()
        self._thread = None

    def doRollover(self) -> None: ...

    # TODO: Implement this

    def getFilesToDelete(self) -> list[str]: ...

    # TODO: Delete files that one month old

global MainLoggingHandler
def create_logger(
    name: str = "log",
    level=logging.INFO,
    format: str = "'[%(levelname)s] | %(asctime)s | %(name)s | %(relativeCreated)6d | %(threadName)s : %(message)s",
):
    global MainLoggingHandler
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ql = QueueListener(filename=name)
    MainLoggingHandler = QueueHandler(ql.queue, format, level)
    logger.addHandler(MainLoggingHandler)
    
    print(logger.handlers)

    return ql


def destroy_logger(name): ...  # TODO: Implement this 




# [ ] SLOW: Currently the logging is slow, which slows down the initialization of the screen