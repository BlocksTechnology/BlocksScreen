import copy
import logging
import logging.config
import logging.handlers
import pathlib
import queue
import threading
from pathlib import Path


class QueueHandler(logging.Handler):
    """Handler that sends events to a queue"""

    def __init__(
        self,
        queue: queue.Queue,
        format: str = "[%(levelname)s] | %(asctime)s | %(name)s | %(relativeCreated)6d | %(threadName)s : %(message)s",
        level=logging.DEBUG,
    ):
        super(QueueHandler, self).__init__()
        self.log_queue = queue
        self.setFormatter(logging.Formatter(format, validate=True))
        self.setLevel(level)

    def emit(self, record):
        """Emit logging record"""
        try:
            msg = self.format(record)
            record = copy.copy(record)
            record.message = msg
            record.name = record.name
            record.msg = msg
            self.log_queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def setFormatter(self, fmt: logging.Formatter | None) -> None:
        """Set logging formatter"""
        return super().setFormatter(fmt)


class QueueListener(logging.handlers.TimedRotatingFileHandler):
    """Threaded listener watching for log records on the queue handler queue, passes them for processing"""

    def __init__(self, filename, encoding="utf-8"):
        log_path = pathlib.Path(filename)
        if log_path.parent != pathlib.Path("."):
            log_path.parent.mkdir(parents=True, exist_ok=True)
        super(QueueListener, self).__init__(
            filename=filename,
            when="MIDNIGHT",
            backupCount=10,
            encoding=encoding,
            delay=True,
        )
        self.queue = queue.Queue()
        self._thread = threading.Thread(
            name=f"log.{filename}", target=self._run, daemon=True
        )
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
        """Close logger listener"""
        if self._thread is None:
            return
        self.queue.put_nowait(None)
        self._thread.join()
        self._thread = None


def create_logger(
    name: str = "log",
    level=logging.INFO,
    format: str = "[%(levelname)s] | %(asctime)s | %(name)s | %(relativeCreated)6d | %(threadName)s : %(message)s",
):
    """Create amd return logger"""
    log_file_path = Path(name)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_file_path.exists():
        log_file_path.touch()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ql = QueueListener(filename=name)
    MainLoggingHandler = QueueHandler(ql.queue, format, level)
    logger.addHandler(MainLoggingHandler)
    return ql
