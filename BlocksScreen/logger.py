from __future__ import annotations

import atexit
import copy
import logging
import logging.handlers
import pathlib
import queue
import sys
import threading
from typing import ClassVar, TextIO

DEFAULT_FORMAT = (
    "[%(levelname)s] | %(asctime)s | %(name)s | "
    "%(relativeCreated)6d | %(threadName)s : %(message)s"
)


class StreamToLogger(TextIO):
    """
    Redirects a stream (stdout/stderr) to a logger.

    Useful for capturing output from subprocesses, X11, or print statements.
    """

    def __init__(
        self,
        logger: logging.Logger,
        level: int = logging.INFO,
        original_stream: TextIO | None = None,
    ) -> None:
        self._logger = logger
        self._level = level
        self._original = original_stream
        self._buffer = ""

    def write(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except Exception:
                    pass

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def flush(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(self._level, self._buffer.rstrip())
            self._buffer = ""

        if self._original:
            try:
                self._original.flush()
            except Exception:
                pass

    def fileno(self) -> int:
        """Return file descriptor for compatibility."""
        if self._original:
            return self._original.fileno()
        raise OSError("No file descriptor available")

    def isatty(self) -> bool:
        """Check if stream is a TTY."""
        if self._original:
            return self._original.isatty()
        return False

    # Required for TextIO interface
    def read(self, n: int = -1) -> str:
        return ""

    def readline(self, limit: int = -1) -> str:
        return ""

    def readlines(self, hint: int = -1) -> list[str]:
        return []

    def seek(self, offset: int, whence: int = 0) -> int:
        return 0

    def tell(self) -> int:
        return 0

    def truncate(self, size: int | None = None) -> int:
        return 0

    def writable(self) -> bool:
        return True

    def readable(self) -> bool:
        return False

    def seekable(self) -> bool:
        return False

    def close(self) -> None:
        self.flush()

    @property
    def closed(self) -> bool:
        return False

    def __enter__(self) -> "StreamToLogger":
        return self

    def __exit__(self, *args) -> None:
        self.close()


class QueueHandler(logging.Handler):
    """
    Logging handler that sends records to a queue.

    Records are formatted before being placed on the queue,
    then consumed by a QueueListener in a background thread.
    """

    def __init__(
        self,
        log_queue: queue.Queue,
        fmt: str = DEFAULT_FORMAT,
        level: int = logging.DEBUG,
    ) -> None:
        super().__init__(level)
        self._queue = log_queue
        self.setFormatter(logging.Formatter(fmt))

    def emit(self, record: logging.LogRecord) -> None:
        """Format and queue the log record."""
        try:
            # Format the message
            msg = self.format(record)

            # Copy record and update message
            record = copy.copy(record)
            record.msg = msg
            record.args = None  # Already formatted
            record.message = msg

            self._queue.put_nowait(record)
        except Exception:
            self.handleError(record)


class AsyncFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Async file handler using a background thread.

    Wraps TimedRotatingFileHandler with a queue and worker thread
    for non-blocking log writes. Automatically recreates log file
    if deleted during runtime.
    """

    def __init__(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def _ensure_file_exists(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None and not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except Exception:
                    pass
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except Exception:
            pass

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record with file existence check."""
        with self._lock:
            self._ensure_file_exists()
            super().emit(record)

    def _worker(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.5)
                if record is None:
                    break
                self.handle(record)
            except queue.Empty:
                continue
            except Exception:
                # Don't crash the worker thread
                pass

    @property
    def queue(self) -> queue.Queue:
        """Get the log queue for QueueHandler."""
        return self._queue

    def close(self) -> None:
        """Stop worker thread and close file handler."""
        if self._thread is None or not self._thread.is_alive():
            super().close()
            return

        # Signal worker to stop
        self._stop_event.set()
        self._queue.put_nowait(None)

        # Wait for worker to finish
        self._thread.join(timeout=2.0)
        self._thread = None

        # Close the file handler
        super().close()


class _ExcludeStreamLoggers(logging.Filter):
    """Filter to exclude stdout/stderr loggers from console output."""

    def filter(self, record: logging.LogRecord) -> bool:
        # Exclude to avoid double printing (already goes to console via StreamToLogger)
        return record.name not in ("stdout", "stderr")


class LogManager:
    """
    Manages application logging.

    Creates async file loggers with queue-based handlers.
    Ensures proper cleanup on application exit.
    """

    _handlers: ClassVar[dict[str, AsyncFileHandler]] = {}
    _initialized: ClassVar[bool] = False
    _original_stdout: ClassVar[TextIO | None] = None
    _original_stderr: ClassVar[TextIO | None] = None

    @classmethod
    def _ensure_initialized(cls) -> None:
        """Register cleanup handler on first use."""
        if not cls._initialized:
            atexit.register(cls.shutdown)
            cls._initialized = True

    @classmethod
    def setup(
        cls,
        filename: str = "logs/app.log",
        level: int = logging.DEBUG,
        fmt: str = DEFAULT_FORMAT,
        capture_stdout: bool = False,
        capture_stderr: bool = True,
        console_output: bool = True,
        console_level: int | None = None,
    ) -> None:
        """
        Setup root logger for entire application.

        Call once at startup. After this, all modules can use:
            logger = logging.getLogger(__name__)

        Args:
            filename: Log file path
            level: Logging level for all loggers
            fmt: Log format string
            capture_stdout: Redirect stdout to logger
            capture_stderr: Redirect stderr to logger
            console_output: Also print logs to console
            console_level: Console log level (defaults to same as level)
        """
        cls._ensure_initialized()

        # Store original streams before any redirection
        if cls._original_stdout is None:
            cls._original_stdout = sys.stdout
        if cls._original_stderr is None:
            cls._original_stderr = sys.stderr

        # Get root logger
        root = logging.getLogger()

        # Don't add duplicate handlers
        if root.handlers:
            return

        root.setLevel(level)

        # Create async file handler
        file_handler = AsyncFileHandler(filename)
        cls._handlers["root"] = file_handler

        # Create queue handler that feeds the file handler
        queue_handler = QueueHandler(file_handler.queue, fmt, level)
        root.addHandler(queue_handler)

        # Add console handler
        if console_output:
            cls._add_console_handler(root, console_level or level, fmt)

        # Capture stdout/stderr (after console handler is set up)
        if capture_stdout:
            cls.redirect_stdout()
        if capture_stderr:
            cls.redirect_stderr()

    @classmethod
    def _add_console_handler(cls, logger: logging.Logger, level: int, fmt: str) -> None:
        """Add a console handler that prints to original stdout."""
        # Use original stdout to avoid recursion if stdout is redirected
        stream = cls._original_stdout or sys.stdout

        console_handler = logging.StreamHandler(stream)
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(fmt))

        # Filter out stderr logger to avoid double printing
        console_handler.addFilter(_ExcludeStreamLoggers())

        logger.addHandler(console_handler)

    @classmethod
    def get_logger(
        cls,
        name: str,
        filename: str | None = None,
        level: int = logging.INFO,
        fmt: str = DEFAULT_FORMAT,
    ) -> logging.Logger:
        """
        Get or create a named logger with its own file output.

        Args:
            name: Logger name
            filename: Log file path (defaults to "logs/{name}.log")
            level: Logging level
            fmt: Log format string

        Returns:
            Configured Logger instance
        """
        cls._ensure_initialized()

        logger = logging.getLogger(name)

        # Don't add duplicate handlers
        if logger.handlers:
            return logger

        logger.setLevel(level)

        # Create async file handler
        if filename is None:
            filename = f"logs/{name}.log"

        file_handler = AsyncFileHandler(filename)
        cls._handlers[name] = file_handler

        # Create queue handler that feeds the file handler
        queue_handler = QueueHandler(file_handler.queue, fmt, level)
        logger.addHandler(queue_handler)

        # Don't propagate to root (has its own file)
        logger.propagate = False

        return logger

    @classmethod
    def redirect_stdout(cls, logger_name: str = "stdout") -> None:
        """
        Redirect stdout to logger.

        Captures print() statements and subprocess output.
        """
        logger = logging.getLogger(logger_name)
        sys.stdout = StreamToLogger(logger, logging.INFO, cls._original_stdout)

    @classmethod
    def redirect_stderr(cls, logger_name: str = "stderr") -> None:
        """
        Redirect stderr to logger.

        Captures X11 errors, warnings, and subprocess errors.
        """
        logger = logging.getLogger(logger_name)
        sys.stderr = StreamToLogger(logger, logging.WARNING, cls._original_stderr)

    @classmethod
    def restore_streams(cls) -> None:
        """Restore original stdout/stderr."""
        if cls._original_stdout:
            sys.stdout = cls._original_stdout
        if cls._original_stderr:
            sys.stderr = cls._original_stderr

    @classmethod
    def shutdown(cls) -> None:
        """Close all handlers. Called automatically on exit."""
        # Restore original streams
        cls.restore_streams()

        # Close handlers
        for handler in cls._handlers.values():
            handler.close()
        cls._handlers.clear()


def setup_logging(
    filename: str = "logs/app.log",
    level: int = logging.DEBUG,
    fmt: str = DEFAULT_FORMAT,
    capture_stdout: bool = False,
    capture_stderr: bool = True,
    console_output: bool = True,
    console_level: int | None = None,
) -> None:
    """
    Setup logging for entire application.

    Call once at startup. After this, all modules can use:
        import logging
        logger = logging.getLogger(__name__)

    Args:
        filename: Log file path
        level: Logging level
        fmt: Log format string
        capture_stdout: Redirect stdout (print statements) to logger
        capture_stderr: Redirect stderr (X11 errors, warnings) to logger
        console_output: Also print logs to console/terminal
        console_level: Console log level (defaults to same as level)
    """
    LogManager.setup(
        filename,
        level,
        fmt,
        capture_stdout,
        capture_stderr,
        console_output,
        console_level,
    )

def get_logger(
    name: str,
    filename: str | None = None,
    level: int = logging.INFO,
    fmt: str = DEFAULT_FORMAT,
) -> logging.Logger:
    """
    Get or create a logger with its own file output.

    Args:
        name: Logger name
        filename: Log file path (defaults to "logs/{name}.log")
        level: Logging level
        fmt: Log format string

    Returns:
        Configured Logger instance
    """
    return LogManager.get_logger(name, filename, level, fmt)
