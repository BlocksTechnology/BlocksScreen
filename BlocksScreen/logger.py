from __future__ import annotations

import atexit
import copy
import faulthandler
import logging
import logging.handlers
import os
import pathlib
import queue
import sys
import threading
import traceback
from datetime import datetime
from typing import ClassVar, TextIO

DEFAULT_FORMAT = (
    "[%(levelname)s] | %(asctime)s | %(name)s | "
    "%(relativeCreated)6d | %(threadName)s : %(message)s"
)

CRASH_LOG_PATH = "logs/blocksscreen_crash.log"
FAULT_LOG_PATH = "logs/blocksscreen_fault.log"


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


class CrashHandler:
    """
    Handles unhandled exceptions and C-level crashes.

    Writes detailed crash information to log files including:
    - Full traceback with line numbers
    - Local variables at each frame
    - Thread information
    - Timestamp
    """

    _instance: ClassVar[CrashHandler | None] = None
    _installed: ClassVar[bool] = False

    def __init__(
        self,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = True,
        exit_on_crash: bool = True,
    ) -> None:
        self._crash_log_path = pathlib.Path(crash_log_path)
        self._fault_log_path = pathlib.Path(fault_log_path)
        self._include_locals = include_locals
        self._exit_on_crash = exit_on_crash
        self._original_excepthook = sys.excepthook
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    @classmethod
    def install(
        cls,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = True,
        exit_on_crash: bool = True,
    ) -> CrashHandler:
        """
        Install the crash handler.

        Should be called as early as possible in the application startup.

        Args:
            crash_log_path: Path to write Python exception logs
            fault_log_path: Path to write C-level fault logs (segfaults)
            include_locals: Include local variables in traceback
            exit_on_crash: Force exit after logging (for systemd restart)

        Returns:
            The CrashHandler instance
        """
        if cls._installed and cls._instance:
            return cls._instance

        handler = cls(crash_log_path, fault_log_path, include_locals, exit_on_crash)
        handler._install()
        cls._instance = handler
        cls._installed = True

        return handler

    def _install(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "w")
            faulthandler.enable(file=self._fault_file, all_threads=True)

            # Also dump traceback on SIGUSR1 (useful for debugging hangs)
            try:
                import signal

                faulthandler.register(
                    signal.SIGUSR1,
                    file=self._fault_file,
                    all_threads=True,
                )
            except (AttributeError, OSError):
                pass  # Not available on all platforms

        except Exception as e:
            # Fall back to stderr
            faulthandler.enable()
            sys.stderr.write(f"Warning: Could not setup fault log file: {e}\n")

        # Install Python exception hook
        sys.excepthook = self._exception_hook

        # Install threading exception hook (Python 3.8+)
        if hasattr(threading, "excepthook"):
            threading.excepthook = self._threading_exception_hook

    def _format_exception_detailed(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: traceback,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("UNHANDLED EXCEPTION")
        lines.append("=" * 80)
        lines.append(f"Time: {datetime.now().isoformat()}")
        lines.append(f"Thread: {threading.current_thread().name}")
        lines.append(f"Exception Type: {exc_type.__module__}.{exc_type.__name__}")
        lines.append(f"Exception Value: {exc_value}")
        lines.append("")

        # Full traceback with context
        lines.append("-" * 80)
        lines.append("TRACEBACK (most recent call last):")
        lines.append("-" * 80)

        # Extract frames for detailed info
        tb_frames = traceback.extract_tb(exc_tb)

        for i, frame in enumerate(tb_frames):
            lines.append("")
            lines.append(f"  Frame {i + 1}: {frame.filename}")
            lines.append(f"    Line {frame.lineno} in {frame.name}()")
            lines.append(f"    Code: {frame.line}")

            # Try to get local variables if enabled
            if self._include_locals and exc_tb:
                try:
                    # Navigate to the correct frame
                    current_tb = exc_tb
                    for _ in range(i):
                        if current_tb.tb_next:
                            current_tb = current_tb.tb_next

                    frame_locals = current_tb.tb_frame.f_locals
                    if frame_locals:
                        lines.append("    Locals:")
                        for name, value in frame_locals.items():
                            # Skip private/dunder and limit value length
                            if name.startswith("__"):
                                continue
                            try:
                                value_str = repr(value)
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except Exception:
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except Exception:
                    pass

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" * 80)
        lines.append("ACTIVE THREADS:")
        lines.append("-" * 80)
        for thread in threading.enumerate():
            daemon_str = " (daemon)" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def _write_crash_log(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(".history.log")
            with open(history_path, "a") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def _exception_hook(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available
        try:
            logger = logging.getLogger("crash")
            logger.critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
            logger.critical(crash_info)
        except Exception:
            pass

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def _threading_exception_hook(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, args.exc_value, args.exc_traceback
        )

        # Add thread context
        thread_info = (
            f"\nThread that crashed: {args.thread.name if args.thread else 'Unknown'}\n"
        )
        crash_info = crash_info.replace(
            "UNHANDLED EXCEPTION", f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging
        try:
            logger = logging.getLogger("crash")
            logger.critical("Unhandled thread exception - see %s", self._crash_log_path)
        except Exception:
            pass

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Thread crashes might want different behavior
        if self._exit_on_crash:
            os._exit(1)

    def uninstall(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, "excepthook"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except Exception:
                pass

        CrashHandler._installed = False
        CrashHandler._instance = None


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
    _crash_handler: ClassVar[CrashHandler | None] = None

    @classmethod
    def _ensure_initialized(cls) -> None:
        """Register cleanup handler on first use."""
        if not cls._initialized:
            atexit.register(cls.shutdown)
            cls._initialized = True

    @classmethod
    def setup(
        cls,
        filename: str = "logs/BlocksScreen.log",
        level: int = logging.DEBUG,
        fmt: str = DEFAULT_FORMAT,
        capture_stdout: bool = False,
        capture_stderr: bool = True,
        console_output: bool = True,
        console_level: int | None = None,
        enable_crash_handler: bool = True,
        crash_log_path: str = CRASH_LOG_PATH,
        include_locals_in_crash: bool = True,
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
            enable_crash_handler: Enable crash handler for unhandled exceptions
            crash_log_path: Path to write crash logs
            include_locals_in_crash: Include local variables in crash logs
        """
        # Install crash handler FIRST (before anything else can fail)
        if enable_crash_handler:
            cls._crash_handler = CrashHandler.install(
                crash_log_path=crash_log_path,
                include_locals=include_locals_in_crash,
            )

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

        # Log startup
        logging.info("Logging initialized - crash logs: %s", crash_log_path)

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

        # Uninstall crash handler
        if cls._crash_handler:
            cls._crash_handler.uninstall()
            cls._crash_handler = None


def setup_logging(
    filename: str = "logs/app.log",
    level: int = logging.DEBUG,
    fmt: str = DEFAULT_FORMAT,
    capture_stdout: bool = False,
    capture_stderr: bool = True,
    console_output: bool = True,
    console_level: int | None = None,
    enable_crash_handler: bool = True,
    crash_log_path: str = CRASH_LOG_PATH,
    include_locals_in_crash: bool = True,
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
        enable_crash_handler: Enable crash handler for unhandled exceptions
        crash_log_path: Path to write crash logs
        include_locals_in_crash: Include local variables in crash logs
    """
    LogManager.setup(
        filename,
        level,
        fmt,
        capture_stdout,
        capture_stderr,
        console_output,
        console_level,
        enable_crash_handler,
        crash_log_path,
        include_locals_in_crash,
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


def install_crash_handler(
    crash_log_path: str = CRASH_LOG_PATH,
    fault_log_path: str = FAULT_LOG_PATH,
    include_locals: bool = True,
    exit_on_crash: bool = True,
) -> CrashHandler:
    """
    Install crash handler without full logging setup.

    Use this if you want crash handling before logging is configured.
    Call at the very beginning of your main.py.

    Args:
        crash_log_path: Path to write Python exception logs
        fault_log_path: Path to write C-level fault logs
        include_locals: Include local variables in traceback
        exit_on_crash: Force process exit after logging crash (for systemd restart)

    Returns:
        CrashHandler instance
    """
    return CrashHandler.install(
        crash_log_path, fault_log_path, include_locals, exit_on_crash
    )
