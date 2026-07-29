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
import types
from datetime import datetime
from typing import ClassVar, TextIO

DEFAULT_FORMAT = (
    "[%(levelname)s] | %(asctime)s | %(name)s | "
    "%(relativeCreated)6d | %(threadName)s : %(message)s"
)

CRASH_LOG_PATH = "logs/blocksscreen_crash.log"
FAULT_LOG_PATH = "logs/blocksscreen_fault.log"
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


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
        args = [logger, level, original_stream]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁ__init____mutmut_orig(
        self,
        logger: logging.Logger,
        level: int = logging.INFO,
        original_stream: TextIO | None = None,
    ) -> None:
        self._logger = logger
        self._level = level
        self._original = original_stream
        self._buffer = ""

    def xǁStreamToLoggerǁ__init____mutmut_1(
        self,
        logger: logging.Logger,
        level: int = logging.INFO,
        original_stream: TextIO | None = None,
    ) -> None:
        self._logger = None
        self._level = level
        self._original = original_stream
        self._buffer = ""

    def xǁStreamToLoggerǁ__init____mutmut_2(
        self,
        logger: logging.Logger,
        level: int = logging.INFO,
        original_stream: TextIO | None = None,
    ) -> None:
        self._logger = logger
        self._level = None
        self._original = original_stream
        self._buffer = ""

    def xǁStreamToLoggerǁ__init____mutmut_3(
        self,
        logger: logging.Logger,
        level: int = logging.INFO,
        original_stream: TextIO | None = None,
    ) -> None:
        self._logger = logger
        self._level = level
        self._original = None
        self._buffer = ""

    def xǁStreamToLoggerǁ__init____mutmut_4(
        self,
        logger: logging.Logger,
        level: int = logging.INFO,
        original_stream: TextIO | None = None,
    ) -> None:
        self._logger = logger
        self._level = level
        self._original = original_stream
        self._buffer = None

    def xǁStreamToLoggerǁ__init____mutmut_5(
        self,
        logger: logging.Logger,
        level: int = logging.INFO,
        original_stream: TextIO | None = None,
    ) -> None:
        self._logger = logger
        self._level = level
        self._original = original_stream
        self._buffer = "XXXX"
    
    xǁStreamToLoggerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁ__init____mutmut_1': xǁStreamToLoggerǁ__init____mutmut_1, 
        'xǁStreamToLoggerǁ__init____mutmut_2': xǁStreamToLoggerǁ__init____mutmut_2, 
        'xǁStreamToLoggerǁ__init____mutmut_3': xǁStreamToLoggerǁ__init____mutmut_3, 
        'xǁStreamToLoggerǁ__init____mutmut_4': xǁStreamToLoggerǁ__init____mutmut_4, 
        'xǁStreamToLoggerǁ__init____mutmut_5': xǁStreamToLoggerǁ__init____mutmut_5
    }
    xǁStreamToLoggerǁ__init____mutmut_orig.__name__ = 'xǁStreamToLoggerǁ__init__'

    def write(self, message: str) -> int:
        args = [message]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁwrite__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁwrite__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁwrite__mutmut_orig(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_1(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(None)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_2(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = ""

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_3(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer = message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_4(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer -= message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_5(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "XX\nXX" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_6(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" not in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_7(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = None
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_8(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split(None, 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_9(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", None)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_10(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split(1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_11(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", )
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_12(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.rsplit("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_13(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("XX\nXX", 1)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_14(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 2)
                if line.strip():
                    self._logger.log(self._level, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_15(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(None, line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_16(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, None)

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_17(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(line.rstrip())

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_18(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, )

        return len(message)

    def xǁStreamToLoggerǁwrite__mutmut_19(self, message: str) -> int:
        """Write message to logger."""
        if message:
            if self._original:
                try:
                    self._original.write(message)
                    self._original.flush()
                except OSError:
                    # Original stream closed or broken pipe — continue logging
                    self._original = None

            self._buffer += message

            while "\n" in self._buffer:
                line, self._buffer = self._buffer.split("\n", 1)
                if line.strip():
                    self._logger.log(self._level, line.lstrip())

        return len(message)
    
    xǁStreamToLoggerǁwrite__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁwrite__mutmut_1': xǁStreamToLoggerǁwrite__mutmut_1, 
        'xǁStreamToLoggerǁwrite__mutmut_2': xǁStreamToLoggerǁwrite__mutmut_2, 
        'xǁStreamToLoggerǁwrite__mutmut_3': xǁStreamToLoggerǁwrite__mutmut_3, 
        'xǁStreamToLoggerǁwrite__mutmut_4': xǁStreamToLoggerǁwrite__mutmut_4, 
        'xǁStreamToLoggerǁwrite__mutmut_5': xǁStreamToLoggerǁwrite__mutmut_5, 
        'xǁStreamToLoggerǁwrite__mutmut_6': xǁStreamToLoggerǁwrite__mutmut_6, 
        'xǁStreamToLoggerǁwrite__mutmut_7': xǁStreamToLoggerǁwrite__mutmut_7, 
        'xǁStreamToLoggerǁwrite__mutmut_8': xǁStreamToLoggerǁwrite__mutmut_8, 
        'xǁStreamToLoggerǁwrite__mutmut_9': xǁStreamToLoggerǁwrite__mutmut_9, 
        'xǁStreamToLoggerǁwrite__mutmut_10': xǁStreamToLoggerǁwrite__mutmut_10, 
        'xǁStreamToLoggerǁwrite__mutmut_11': xǁStreamToLoggerǁwrite__mutmut_11, 
        'xǁStreamToLoggerǁwrite__mutmut_12': xǁStreamToLoggerǁwrite__mutmut_12, 
        'xǁStreamToLoggerǁwrite__mutmut_13': xǁStreamToLoggerǁwrite__mutmut_13, 
        'xǁStreamToLoggerǁwrite__mutmut_14': xǁStreamToLoggerǁwrite__mutmut_14, 
        'xǁStreamToLoggerǁwrite__mutmut_15': xǁStreamToLoggerǁwrite__mutmut_15, 
        'xǁStreamToLoggerǁwrite__mutmut_16': xǁStreamToLoggerǁwrite__mutmut_16, 
        'xǁStreamToLoggerǁwrite__mutmut_17': xǁStreamToLoggerǁwrite__mutmut_17, 
        'xǁStreamToLoggerǁwrite__mutmut_18': xǁStreamToLoggerǁwrite__mutmut_18, 
        'xǁStreamToLoggerǁwrite__mutmut_19': xǁStreamToLoggerǁwrite__mutmut_19
    }
    xǁStreamToLoggerǁwrite__mutmut_orig.__name__ = 'xǁStreamToLoggerǁwrite'

    def flush(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁflush__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁflush__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁflush__mutmut_orig(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(self._level, self._buffer.rstrip())
            self._buffer = ""

        if self._original:
            try:
                self._original.flush()
            except OSError:
                # Original stream closed or broken pipe
                self._original = None

    def xǁStreamToLoggerǁflush__mutmut_1(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(None, self._buffer.rstrip())
            self._buffer = ""

        if self._original:
            try:
                self._original.flush()
            except OSError:
                # Original stream closed or broken pipe
                self._original = None

    def xǁStreamToLoggerǁflush__mutmut_2(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(self._level, None)
            self._buffer = ""

        if self._original:
            try:
                self._original.flush()
            except OSError:
                # Original stream closed or broken pipe
                self._original = None

    def xǁStreamToLoggerǁflush__mutmut_3(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(self._buffer.rstrip())
            self._buffer = ""

        if self._original:
            try:
                self._original.flush()
            except OSError:
                # Original stream closed or broken pipe
                self._original = None

    def xǁStreamToLoggerǁflush__mutmut_4(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(self._level, )
            self._buffer = ""

        if self._original:
            try:
                self._original.flush()
            except OSError:
                # Original stream closed or broken pipe
                self._original = None

    def xǁStreamToLoggerǁflush__mutmut_5(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(self._level, self._buffer.lstrip())
            self._buffer = ""

        if self._original:
            try:
                self._original.flush()
            except OSError:
                # Original stream closed or broken pipe
                self._original = None

    def xǁStreamToLoggerǁflush__mutmut_6(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(self._level, self._buffer.rstrip())
            self._buffer = None

        if self._original:
            try:
                self._original.flush()
            except OSError:
                # Original stream closed or broken pipe
                self._original = None

    def xǁStreamToLoggerǁflush__mutmut_7(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(self._level, self._buffer.rstrip())
            self._buffer = "XXXX"

        if self._original:
            try:
                self._original.flush()
            except OSError:
                # Original stream closed or broken pipe
                self._original = None

    def xǁStreamToLoggerǁflush__mutmut_8(self) -> None:
        """Flush remaining buffer."""
        if self._buffer.strip():
            self._logger.log(self._level, self._buffer.rstrip())
            self._buffer = ""

        if self._original:
            try:
                self._original.flush()
            except OSError:
                # Original stream closed or broken pipe
                self._original = ""
    
    xǁStreamToLoggerǁflush__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁflush__mutmut_1': xǁStreamToLoggerǁflush__mutmut_1, 
        'xǁStreamToLoggerǁflush__mutmut_2': xǁStreamToLoggerǁflush__mutmut_2, 
        'xǁStreamToLoggerǁflush__mutmut_3': xǁStreamToLoggerǁflush__mutmut_3, 
        'xǁStreamToLoggerǁflush__mutmut_4': xǁStreamToLoggerǁflush__mutmut_4, 
        'xǁStreamToLoggerǁflush__mutmut_5': xǁStreamToLoggerǁflush__mutmut_5, 
        'xǁStreamToLoggerǁflush__mutmut_6': xǁStreamToLoggerǁflush__mutmut_6, 
        'xǁStreamToLoggerǁflush__mutmut_7': xǁStreamToLoggerǁflush__mutmut_7, 
        'xǁStreamToLoggerǁflush__mutmut_8': xǁStreamToLoggerǁflush__mutmut_8
    }
    xǁStreamToLoggerǁflush__mutmut_orig.__name__ = 'xǁStreamToLoggerǁflush'

    def fileno(self) -> int:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁfileno__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁfileno__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁfileno__mutmut_orig(self) -> int:
        """Return file descriptor for compatibility."""
        if self._original:
            return self._original.fileno()
        raise OSError("No file descriptor available")

    def xǁStreamToLoggerǁfileno__mutmut_1(self) -> int:
        """Return file descriptor for compatibility."""
        if self._original:
            return self._original.fileno()
        raise OSError(None)

    def xǁStreamToLoggerǁfileno__mutmut_2(self) -> int:
        """Return file descriptor for compatibility."""
        if self._original:
            return self._original.fileno()
        raise OSError("XXNo file descriptor availableXX")

    def xǁStreamToLoggerǁfileno__mutmut_3(self) -> int:
        """Return file descriptor for compatibility."""
        if self._original:
            return self._original.fileno()
        raise OSError("no file descriptor available")

    def xǁStreamToLoggerǁfileno__mutmut_4(self) -> int:
        """Return file descriptor for compatibility."""
        if self._original:
            return self._original.fileno()
        raise OSError("NO FILE DESCRIPTOR AVAILABLE")
    
    xǁStreamToLoggerǁfileno__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁfileno__mutmut_1': xǁStreamToLoggerǁfileno__mutmut_1, 
        'xǁStreamToLoggerǁfileno__mutmut_2': xǁStreamToLoggerǁfileno__mutmut_2, 
        'xǁStreamToLoggerǁfileno__mutmut_3': xǁStreamToLoggerǁfileno__mutmut_3, 
        'xǁStreamToLoggerǁfileno__mutmut_4': xǁStreamToLoggerǁfileno__mutmut_4
    }
    xǁStreamToLoggerǁfileno__mutmut_orig.__name__ = 'xǁStreamToLoggerǁfileno'

    def isatty(self) -> bool:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁisatty__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁisatty__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁisatty__mutmut_orig(self) -> bool:
        """Check if stream is a TTY."""
        if self._original:
            return self._original.isatty()
        return False

    def xǁStreamToLoggerǁisatty__mutmut_1(self) -> bool:
        """Check if stream is a TTY."""
        if self._original:
            return self._original.isatty()
        return True
    
    xǁStreamToLoggerǁisatty__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁisatty__mutmut_1': xǁStreamToLoggerǁisatty__mutmut_1
    }
    xǁStreamToLoggerǁisatty__mutmut_orig.__name__ = 'xǁStreamToLoggerǁisatty'

    # Required for TextIO interface
    def read(self, n: int = -1) -> str:
        args = [n]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁread__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁread__mutmut_mutants'), args, kwargs, self)

    # Required for TextIO interface
    def xǁStreamToLoggerǁread__mutmut_orig(self, n: int = -1) -> str:
        return ""

    # Required for TextIO interface
    def xǁStreamToLoggerǁread__mutmut_1(self, n: int = -1) -> str:
        return "XXXX"
    
    xǁStreamToLoggerǁread__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁread__mutmut_1': xǁStreamToLoggerǁread__mutmut_1
    }
    xǁStreamToLoggerǁread__mutmut_orig.__name__ = 'xǁStreamToLoggerǁread'

    def readline(self, limit: int = -1) -> str:
        args = [limit]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁreadline__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁreadline__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁreadline__mutmut_orig(self, limit: int = -1) -> str:
        return ""

    def xǁStreamToLoggerǁreadline__mutmut_1(self, limit: int = -1) -> str:
        return "XXXX"
    
    xǁStreamToLoggerǁreadline__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁreadline__mutmut_1': xǁStreamToLoggerǁreadline__mutmut_1
    }
    xǁStreamToLoggerǁreadline__mutmut_orig.__name__ = 'xǁStreamToLoggerǁreadline'

    def readlines(self, hint: int = -1) -> list[str]:
        return []

    def seek(self, offset: int, whence: int = 0) -> int:
        args = [offset, whence]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁseek__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁseek__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁseek__mutmut_orig(self, offset: int, whence: int = 0) -> int:
        return 0

    def xǁStreamToLoggerǁseek__mutmut_1(self, offset: int, whence: int = 1) -> int:
        return 0

    def xǁStreamToLoggerǁseek__mutmut_2(self, offset: int, whence: int = 0) -> int:
        return 1
    
    xǁStreamToLoggerǁseek__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁseek__mutmut_1': xǁStreamToLoggerǁseek__mutmut_1, 
        'xǁStreamToLoggerǁseek__mutmut_2': xǁStreamToLoggerǁseek__mutmut_2
    }
    xǁStreamToLoggerǁseek__mutmut_orig.__name__ = 'xǁStreamToLoggerǁseek'

    def tell(self) -> int:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁtell__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁtell__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁtell__mutmut_orig(self) -> int:
        return 0

    def xǁStreamToLoggerǁtell__mutmut_1(self) -> int:
        return 1
    
    xǁStreamToLoggerǁtell__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁtell__mutmut_1': xǁStreamToLoggerǁtell__mutmut_1
    }
    xǁStreamToLoggerǁtell__mutmut_orig.__name__ = 'xǁStreamToLoggerǁtell'

    def truncate(self, size: int | None = None) -> int:
        args = [size]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁtruncate__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁtruncate__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁtruncate__mutmut_orig(self, size: int | None = None) -> int:
        return 0

    def xǁStreamToLoggerǁtruncate__mutmut_1(self, size: int | None = None) -> int:
        return 1
    
    xǁStreamToLoggerǁtruncate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁtruncate__mutmut_1': xǁStreamToLoggerǁtruncate__mutmut_1
    }
    xǁStreamToLoggerǁtruncate__mutmut_orig.__name__ = 'xǁStreamToLoggerǁtruncate'

    def writable(self) -> bool:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁwritable__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁwritable__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁwritable__mutmut_orig(self) -> bool:
        return True

    def xǁStreamToLoggerǁwritable__mutmut_1(self) -> bool:
        return False
    
    xǁStreamToLoggerǁwritable__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁwritable__mutmut_1': xǁStreamToLoggerǁwritable__mutmut_1
    }
    xǁStreamToLoggerǁwritable__mutmut_orig.__name__ = 'xǁStreamToLoggerǁwritable'

    def readable(self) -> bool:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁreadable__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁreadable__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁreadable__mutmut_orig(self) -> bool:
        return False

    def xǁStreamToLoggerǁreadable__mutmut_1(self) -> bool:
        return True
    
    xǁStreamToLoggerǁreadable__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁreadable__mutmut_1': xǁStreamToLoggerǁreadable__mutmut_1
    }
    xǁStreamToLoggerǁreadable__mutmut_orig.__name__ = 'xǁStreamToLoggerǁreadable'

    def seekable(self) -> bool:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁStreamToLoggerǁseekable__mutmut_orig'), object.__getattribute__(self, 'xǁStreamToLoggerǁseekable__mutmut_mutants'), args, kwargs, self)

    def xǁStreamToLoggerǁseekable__mutmut_orig(self) -> bool:
        return False

    def xǁStreamToLoggerǁseekable__mutmut_1(self) -> bool:
        return True
    
    xǁStreamToLoggerǁseekable__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁStreamToLoggerǁseekable__mutmut_1': xǁStreamToLoggerǁseekable__mutmut_1
    }
    xǁStreamToLoggerǁseekable__mutmut_orig.__name__ = 'xǁStreamToLoggerǁseekable'

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
    then consumed by a ThreadedFileHandler worker in a background thread.
    """

    def __init__(
        self,
        log_queue: queue.Queue,
        level: int = logging.DEBUG,
    ) -> None:
        args = [log_queue, level]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁQueueHandlerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁQueueHandlerǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁQueueHandlerǁ__init____mutmut_orig(
        self,
        log_queue: queue.Queue,
        level: int = logging.DEBUG,
    ) -> None:
        super().__init__(level)
        self._queue = log_queue

    def xǁQueueHandlerǁ__init____mutmut_1(
        self,
        log_queue: queue.Queue,
        level: int = logging.DEBUG,
    ) -> None:
        super().__init__(None)
        self._queue = log_queue

    def xǁQueueHandlerǁ__init____mutmut_2(
        self,
        log_queue: queue.Queue,
        level: int = logging.DEBUG,
    ) -> None:
        super().__init__(level)
        self._queue = None
    
    xǁQueueHandlerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁQueueHandlerǁ__init____mutmut_1': xǁQueueHandlerǁ__init____mutmut_1, 
        'xǁQueueHandlerǁ__init____mutmut_2': xǁQueueHandlerǁ__init____mutmut_2
    }
    xǁQueueHandlerǁ__init____mutmut_orig.__name__ = 'xǁQueueHandlerǁ__init__'

    def emit(self, record: logging.LogRecord) -> None:
        args = [record]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁQueueHandlerǁemit__mutmut_orig'), object.__getattribute__(self, 'xǁQueueHandlerǁemit__mutmut_mutants'), args, kwargs, self)

    def xǁQueueHandlerǁemit__mutmut_orig(self, record: logging.LogRecord) -> None:
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

    def xǁQueueHandlerǁemit__mutmut_1(self, record: logging.LogRecord) -> None:
        """Format and queue the log record."""
        try:
            # Format the message
            msg = None

            # Copy record and update message
            record = copy.copy(record)
            record.msg = msg
            record.args = None  # Already formatted
            record.message = msg

            self._queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def xǁQueueHandlerǁemit__mutmut_2(self, record: logging.LogRecord) -> None:
        """Format and queue the log record."""
        try:
            # Format the message
            msg = self.format(None)

            # Copy record and update message
            record = copy.copy(record)
            record.msg = msg
            record.args = None  # Already formatted
            record.message = msg

            self._queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def xǁQueueHandlerǁemit__mutmut_3(self, record: logging.LogRecord) -> None:
        """Format and queue the log record."""
        try:
            # Format the message
            msg = self.format(record)

            # Copy record and update message
            record = None
            record.msg = msg
            record.args = None  # Already formatted
            record.message = msg

            self._queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def xǁQueueHandlerǁemit__mutmut_4(self, record: logging.LogRecord) -> None:
        """Format and queue the log record."""
        try:
            # Format the message
            msg = self.format(record)

            # Copy record and update message
            record = copy.copy(None)
            record.msg = msg
            record.args = None  # Already formatted
            record.message = msg

            self._queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def xǁQueueHandlerǁemit__mutmut_5(self, record: logging.LogRecord) -> None:
        """Format and queue the log record."""
        try:
            # Format the message
            msg = self.format(record)

            # Copy record and update message
            record = copy.copy(record)
            record.msg = None
            record.args = None  # Already formatted
            record.message = msg

            self._queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def xǁQueueHandlerǁemit__mutmut_6(self, record: logging.LogRecord) -> None:
        """Format and queue the log record."""
        try:
            # Format the message
            msg = self.format(record)

            # Copy record and update message
            record = copy.copy(record)
            record.msg = msg
            record.args = ""  # Already formatted
            record.message = msg

            self._queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def xǁQueueHandlerǁemit__mutmut_7(self, record: logging.LogRecord) -> None:
        """Format and queue the log record."""
        try:
            # Format the message
            msg = self.format(record)

            # Copy record and update message
            record = copy.copy(record)
            record.msg = msg
            record.args = None  # Already formatted
            record.message = None

            self._queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def xǁQueueHandlerǁemit__mutmut_8(self, record: logging.LogRecord) -> None:
        """Format and queue the log record."""
        try:
            # Format the message
            msg = self.format(record)

            # Copy record and update message
            record = copy.copy(record)
            record.msg = msg
            record.args = None  # Already formatted
            record.message = msg

            self._queue.put_nowait(None)
        except Exception:
            self.handleError(record)

    def xǁQueueHandlerǁemit__mutmut_9(self, record: logging.LogRecord) -> None:
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
            self.handleError(None)
    
    xǁQueueHandlerǁemit__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁQueueHandlerǁemit__mutmut_1': xǁQueueHandlerǁemit__mutmut_1, 
        'xǁQueueHandlerǁemit__mutmut_2': xǁQueueHandlerǁemit__mutmut_2, 
        'xǁQueueHandlerǁemit__mutmut_3': xǁQueueHandlerǁemit__mutmut_3, 
        'xǁQueueHandlerǁemit__mutmut_4': xǁQueueHandlerǁemit__mutmut_4, 
        'xǁQueueHandlerǁemit__mutmut_5': xǁQueueHandlerǁemit__mutmut_5, 
        'xǁQueueHandlerǁemit__mutmut_6': xǁQueueHandlerǁemit__mutmut_6, 
        'xǁQueueHandlerǁemit__mutmut_7': xǁQueueHandlerǁemit__mutmut_7, 
        'xǁQueueHandlerǁemit__mutmut_8': xǁQueueHandlerǁemit__mutmut_8, 
        'xǁQueueHandlerǁemit__mutmut_9': xǁQueueHandlerǁemit__mutmut_9
    }
    xǁQueueHandlerǁemit__mutmut_orig.__name__ = 'xǁQueueHandlerǁemit'


class ThreadedFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    File handler that writes on a background thread.

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
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        args = [filename, when, backup_count, encoding, fmt]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁThreadedFileHandlerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁThreadedFileHandlerǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁThreadedFileHandlerǁ__init____mutmut_orig(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_1(
        self,
        filename: str,
        when: str = "XXmidnightXX",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_2(
        self,
        filename: str,
        when: str = "MIDNIGHT",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_3(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 11,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_4(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "XXutf-8XX",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_5(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "UTF-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_6(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = None

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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_7(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(None)

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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_8(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent == pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_9(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path(None):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_10(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("XX.XX"):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_11(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=None, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_12(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=None)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_13(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_14(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, )

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_15(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=False, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_16(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=False)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_17(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=None,
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_18(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            when=None,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_19(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=None,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_20(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            encoding=None,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_21(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
            delay=None,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_22(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            when=when,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_23(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            backupCount=backup_count,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_24(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            encoding=encoding,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_25(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
    ) -> None:
        self._log_path = pathlib.Path(filename)

        # Create log directory if needed
        if self._log_path.parent != pathlib.Path("."):
            self._log_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(
            filename=filename,
            when=when,
            backupCount=backup_count,
            delay=True,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_26(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
            )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_27(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
            delay=False,
        )
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_28(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(None)

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_29(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(None))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_30(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = None
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_31(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = None
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_32(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = None
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_33(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=None,
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_34(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=None,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_35(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=None,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_36(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            target=self._worker,
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_37(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            daemon=True,
        )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_38(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            )
        self._thread.start()

    def xǁThreadedFileHandlerǁ__init____mutmut_39(
        self,
        filename: str,
        when: str = "midnight",
        backup_count: int = 10,
        encoding: str = "utf-8",
        fmt: str = DEFAULT_FORMAT,
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
        self.setFormatter(logging.Formatter(fmt))

        self._queue: queue.Queue[logging.LogRecord | None] = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            name=f"logger-{self._log_path.stem}",
            target=self._worker,
            daemon=False,
        )
        self._thread.start()
    
    xǁThreadedFileHandlerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁThreadedFileHandlerǁ__init____mutmut_1': xǁThreadedFileHandlerǁ__init____mutmut_1, 
        'xǁThreadedFileHandlerǁ__init____mutmut_2': xǁThreadedFileHandlerǁ__init____mutmut_2, 
        'xǁThreadedFileHandlerǁ__init____mutmut_3': xǁThreadedFileHandlerǁ__init____mutmut_3, 
        'xǁThreadedFileHandlerǁ__init____mutmut_4': xǁThreadedFileHandlerǁ__init____mutmut_4, 
        'xǁThreadedFileHandlerǁ__init____mutmut_5': xǁThreadedFileHandlerǁ__init____mutmut_5, 
        'xǁThreadedFileHandlerǁ__init____mutmut_6': xǁThreadedFileHandlerǁ__init____mutmut_6, 
        'xǁThreadedFileHandlerǁ__init____mutmut_7': xǁThreadedFileHandlerǁ__init____mutmut_7, 
        'xǁThreadedFileHandlerǁ__init____mutmut_8': xǁThreadedFileHandlerǁ__init____mutmut_8, 
        'xǁThreadedFileHandlerǁ__init____mutmut_9': xǁThreadedFileHandlerǁ__init____mutmut_9, 
        'xǁThreadedFileHandlerǁ__init____mutmut_10': xǁThreadedFileHandlerǁ__init____mutmut_10, 
        'xǁThreadedFileHandlerǁ__init____mutmut_11': xǁThreadedFileHandlerǁ__init____mutmut_11, 
        'xǁThreadedFileHandlerǁ__init____mutmut_12': xǁThreadedFileHandlerǁ__init____mutmut_12, 
        'xǁThreadedFileHandlerǁ__init____mutmut_13': xǁThreadedFileHandlerǁ__init____mutmut_13, 
        'xǁThreadedFileHandlerǁ__init____mutmut_14': xǁThreadedFileHandlerǁ__init____mutmut_14, 
        'xǁThreadedFileHandlerǁ__init____mutmut_15': xǁThreadedFileHandlerǁ__init____mutmut_15, 
        'xǁThreadedFileHandlerǁ__init____mutmut_16': xǁThreadedFileHandlerǁ__init____mutmut_16, 
        'xǁThreadedFileHandlerǁ__init____mutmut_17': xǁThreadedFileHandlerǁ__init____mutmut_17, 
        'xǁThreadedFileHandlerǁ__init____mutmut_18': xǁThreadedFileHandlerǁ__init____mutmut_18, 
        'xǁThreadedFileHandlerǁ__init____mutmut_19': xǁThreadedFileHandlerǁ__init____mutmut_19, 
        'xǁThreadedFileHandlerǁ__init____mutmut_20': xǁThreadedFileHandlerǁ__init____mutmut_20, 
        'xǁThreadedFileHandlerǁ__init____mutmut_21': xǁThreadedFileHandlerǁ__init____mutmut_21, 
        'xǁThreadedFileHandlerǁ__init____mutmut_22': xǁThreadedFileHandlerǁ__init____mutmut_22, 
        'xǁThreadedFileHandlerǁ__init____mutmut_23': xǁThreadedFileHandlerǁ__init____mutmut_23, 
        'xǁThreadedFileHandlerǁ__init____mutmut_24': xǁThreadedFileHandlerǁ__init____mutmut_24, 
        'xǁThreadedFileHandlerǁ__init____mutmut_25': xǁThreadedFileHandlerǁ__init____mutmut_25, 
        'xǁThreadedFileHandlerǁ__init____mutmut_26': xǁThreadedFileHandlerǁ__init____mutmut_26, 
        'xǁThreadedFileHandlerǁ__init____mutmut_27': xǁThreadedFileHandlerǁ__init____mutmut_27, 
        'xǁThreadedFileHandlerǁ__init____mutmut_28': xǁThreadedFileHandlerǁ__init____mutmut_28, 
        'xǁThreadedFileHandlerǁ__init____mutmut_29': xǁThreadedFileHandlerǁ__init____mutmut_29, 
        'xǁThreadedFileHandlerǁ__init____mutmut_30': xǁThreadedFileHandlerǁ__init____mutmut_30, 
        'xǁThreadedFileHandlerǁ__init____mutmut_31': xǁThreadedFileHandlerǁ__init____mutmut_31, 
        'xǁThreadedFileHandlerǁ__init____mutmut_32': xǁThreadedFileHandlerǁ__init____mutmut_32, 
        'xǁThreadedFileHandlerǁ__init____mutmut_33': xǁThreadedFileHandlerǁ__init____mutmut_33, 
        'xǁThreadedFileHandlerǁ__init____mutmut_34': xǁThreadedFileHandlerǁ__init____mutmut_34, 
        'xǁThreadedFileHandlerǁ__init____mutmut_35': xǁThreadedFileHandlerǁ__init____mutmut_35, 
        'xǁThreadedFileHandlerǁ__init____mutmut_36': xǁThreadedFileHandlerǁ__init____mutmut_36, 
        'xǁThreadedFileHandlerǁ__init____mutmut_37': xǁThreadedFileHandlerǁ__init____mutmut_37, 
        'xǁThreadedFileHandlerǁ__init____mutmut_38': xǁThreadedFileHandlerǁ__init____mutmut_38, 
        'xǁThreadedFileHandlerǁ__init____mutmut_39': xǁThreadedFileHandlerǁ__init____mutmut_39
    }
    xǁThreadedFileHandlerǁ__init____mutmut_orig.__name__ = 'xǁThreadedFileHandlerǁ__init__'

    def _ensure_file_exists(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_orig'), object.__getattribute__(self, 'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_mutants'), args, kwargs, self)

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_orig(self) -> None:
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
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_1(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None and not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_2(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=None, exist_ok=True)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None and not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_3(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=True, exist_ok=None)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None and not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_4(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(exist_ok=True)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None and not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_5(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=True, )

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None and not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_6(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=False, exist_ok=True)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None and not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_7(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=True, exist_ok=False)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None and not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_8(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None or not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_9(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is None and not self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_10(self) -> None:
        """Ensure log file and directory exist, recreate if deleted."""
        try:
            # Check if directory exists
            if not self._log_path.parent.exists():
                self._log_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file was deleted (stream is open but file gone)
            if self.stream is not None and self._log_path.exists():
                # Close old stream
                try:
                    self.stream.close()
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_11(self) -> None:
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
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = ""

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_12(self) -> None:
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
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is not None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_13(self) -> None:
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
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = None

        except OSError as exc:
            sys.__stderr__.write(
                f"[logger] Failed to recreate log file {self._log_path}: {exc}\n"
            )

    def xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_14(self) -> None:
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
                except OSError:
                    pass  # Stream already closed; safe to discard
                self.stream = None

            # Reopen stream if needed
            if self.stream is None:
                self.stream = self._open()

        except OSError as exc:
            sys.__stderr__.write(
                None
            )
    
    xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_1': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_1, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_2': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_2, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_3': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_3, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_4': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_4, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_5': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_5, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_6': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_6, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_7': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_7, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_8': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_8, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_9': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_9, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_10': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_10, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_11': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_11, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_12': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_12, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_13': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_13, 
        'xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_14': xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_14
    }
    xǁThreadedFileHandlerǁ_ensure_file_exists__mutmut_orig.__name__ = 'xǁThreadedFileHandlerǁ_ensure_file_exists'

    def emit(self, record: logging.LogRecord) -> None:
        args = [record]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁThreadedFileHandlerǁemit__mutmut_orig'), object.__getattribute__(self, 'xǁThreadedFileHandlerǁemit__mutmut_mutants'), args, kwargs, self)

    def xǁThreadedFileHandlerǁemit__mutmut_orig(self, record: logging.LogRecord) -> None:
        """Emit a record, recovering if the log file was deleted."""
        try:
            super().emit(record)
        except (OSError, ValueError):
            self._ensure_file_exists()
            try:
                super().emit(record)
            except OSError as exc:
                sys.__stderr__.write(f"[logger] Failed to write log record: {exc}\n")

    def xǁThreadedFileHandlerǁemit__mutmut_1(self, record: logging.LogRecord) -> None:
        """Emit a record, recovering if the log file was deleted."""
        try:
            super().emit(None)
        except (OSError, ValueError):
            self._ensure_file_exists()
            try:
                super().emit(record)
            except OSError as exc:
                sys.__stderr__.write(f"[logger] Failed to write log record: {exc}\n")

    def xǁThreadedFileHandlerǁemit__mutmut_2(self, record: logging.LogRecord) -> None:
        """Emit a record, recovering if the log file was deleted."""
        try:
            super().emit(record)
        except (OSError, ValueError):
            self._ensure_file_exists()
            try:
                super().emit(None)
            except OSError as exc:
                sys.__stderr__.write(f"[logger] Failed to write log record: {exc}\n")

    def xǁThreadedFileHandlerǁemit__mutmut_3(self, record: logging.LogRecord) -> None:
        """Emit a record, recovering if the log file was deleted."""
        try:
            super().emit(record)
        except (OSError, ValueError):
            self._ensure_file_exists()
            try:
                super().emit(record)
            except OSError as exc:
                sys.__stderr__.write(None)
    
    xǁThreadedFileHandlerǁemit__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁThreadedFileHandlerǁemit__mutmut_1': xǁThreadedFileHandlerǁemit__mutmut_1, 
        'xǁThreadedFileHandlerǁemit__mutmut_2': xǁThreadedFileHandlerǁemit__mutmut_2, 
        'xǁThreadedFileHandlerǁemit__mutmut_3': xǁThreadedFileHandlerǁemit__mutmut_3
    }
    xǁThreadedFileHandlerǁemit__mutmut_orig.__name__ = 'xǁThreadedFileHandlerǁemit'

    def _worker(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁThreadedFileHandlerǁ_worker__mutmut_orig'), object.__getattribute__(self, 'xǁThreadedFileHandlerǁ_worker__mutmut_mutants'), args, kwargs, self)

    def xǁThreadedFileHandlerǁ_worker__mutmut_orig(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.5)
                if record is None:
                    break
                self.emit(record)
            except queue.Empty:
                continue
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(f"[logger] Worker thread error: {exc}\n")

    def xǁThreadedFileHandlerǁ_worker__mutmut_1(self) -> None:
        """Background worker that processes queued log records."""
        while self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.5)
                if record is None:
                    break
                self.emit(record)
            except queue.Empty:
                continue
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(f"[logger] Worker thread error: {exc}\n")

    def xǁThreadedFileHandlerǁ_worker__mutmut_2(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = None
                if record is None:
                    break
                self.emit(record)
            except queue.Empty:
                continue
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(f"[logger] Worker thread error: {exc}\n")

    def xǁThreadedFileHandlerǁ_worker__mutmut_3(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=None)
                if record is None:
                    break
                self.emit(record)
            except queue.Empty:
                continue
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(f"[logger] Worker thread error: {exc}\n")

    def xǁThreadedFileHandlerǁ_worker__mutmut_4(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=1.5)
                if record is None:
                    break
                self.emit(record)
            except queue.Empty:
                continue
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(f"[logger] Worker thread error: {exc}\n")

    def xǁThreadedFileHandlerǁ_worker__mutmut_5(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.5)
                if record is not None:
                    break
                self.emit(record)
            except queue.Empty:
                continue
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(f"[logger] Worker thread error: {exc}\n")

    def xǁThreadedFileHandlerǁ_worker__mutmut_6(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.5)
                if record is None:
                    return
                self.emit(record)
            except queue.Empty:
                continue
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(f"[logger] Worker thread error: {exc}\n")

    def xǁThreadedFileHandlerǁ_worker__mutmut_7(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.5)
                if record is None:
                    break
                self.emit(None)
            except queue.Empty:
                continue
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(f"[logger] Worker thread error: {exc}\n")

    def xǁThreadedFileHandlerǁ_worker__mutmut_8(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.5)
                if record is None:
                    break
                self.emit(record)
            except queue.Empty:
                break
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(f"[logger] Worker thread error: {exc}\n")

    def xǁThreadedFileHandlerǁ_worker__mutmut_9(self) -> None:
        """Background worker that processes queued log records."""
        while not self._stop_event.is_set():
            try:
                record = self._queue.get(timeout=0.5)
                if record is None:
                    break
                self.emit(record)
            except queue.Empty:
                continue
            except Exception as exc:
                # Last resort: surface unexpected worker errors without crashing the thread
                sys.__stderr__.write(None)
    
    xǁThreadedFileHandlerǁ_worker__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁThreadedFileHandlerǁ_worker__mutmut_1': xǁThreadedFileHandlerǁ_worker__mutmut_1, 
        'xǁThreadedFileHandlerǁ_worker__mutmut_2': xǁThreadedFileHandlerǁ_worker__mutmut_2, 
        'xǁThreadedFileHandlerǁ_worker__mutmut_3': xǁThreadedFileHandlerǁ_worker__mutmut_3, 
        'xǁThreadedFileHandlerǁ_worker__mutmut_4': xǁThreadedFileHandlerǁ_worker__mutmut_4, 
        'xǁThreadedFileHandlerǁ_worker__mutmut_5': xǁThreadedFileHandlerǁ_worker__mutmut_5, 
        'xǁThreadedFileHandlerǁ_worker__mutmut_6': xǁThreadedFileHandlerǁ_worker__mutmut_6, 
        'xǁThreadedFileHandlerǁ_worker__mutmut_7': xǁThreadedFileHandlerǁ_worker__mutmut_7, 
        'xǁThreadedFileHandlerǁ_worker__mutmut_8': xǁThreadedFileHandlerǁ_worker__mutmut_8, 
        'xǁThreadedFileHandlerǁ_worker__mutmut_9': xǁThreadedFileHandlerǁ_worker__mutmut_9
    }
    xǁThreadedFileHandlerǁ_worker__mutmut_orig.__name__ = 'xǁThreadedFileHandlerǁ_worker'

    @property
    def queue(self) -> queue.Queue:
        """Get the log queue for QueueHandler."""
        return self._queue

    def close(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁThreadedFileHandlerǁclose__mutmut_orig'), object.__getattribute__(self, 'xǁThreadedFileHandlerǁclose__mutmut_mutants'), args, kwargs, self)

    def xǁThreadedFileHandlerǁclose__mutmut_orig(self) -> None:
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

    def xǁThreadedFileHandlerǁclose__mutmut_1(self) -> None:
        """Stop worker thread and close file handler."""
        if self._thread is None and not self._thread.is_alive():
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

    def xǁThreadedFileHandlerǁclose__mutmut_2(self) -> None:
        """Stop worker thread and close file handler."""
        if self._thread is not None or not self._thread.is_alive():
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

    def xǁThreadedFileHandlerǁclose__mutmut_3(self) -> None:
        """Stop worker thread and close file handler."""
        if self._thread is None or self._thread.is_alive():
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

    def xǁThreadedFileHandlerǁclose__mutmut_4(self) -> None:
        """Stop worker thread and close file handler."""
        if self._thread is None or not self._thread.is_alive():
            super().close()
            return

        # Signal worker to stop
        self._stop_event.set()
        self._queue.put_nowait(None)

        # Wait for worker to finish
        self._thread.join(timeout=None)
        self._thread = None

        # Close the file handler
        super().close()

    def xǁThreadedFileHandlerǁclose__mutmut_5(self) -> None:
        """Stop worker thread and close file handler."""
        if self._thread is None or not self._thread.is_alive():
            super().close()
            return

        # Signal worker to stop
        self._stop_event.set()
        self._queue.put_nowait(None)

        # Wait for worker to finish
        self._thread.join(timeout=3.0)
        self._thread = None

        # Close the file handler
        super().close()

    def xǁThreadedFileHandlerǁclose__mutmut_6(self) -> None:
        """Stop worker thread and close file handler."""
        if self._thread is None or not self._thread.is_alive():
            super().close()
            return

        # Signal worker to stop
        self._stop_event.set()
        self._queue.put_nowait(None)

        # Wait for worker to finish
        self._thread.join(timeout=2.0)
        self._thread = ""

        # Close the file handler
        super().close()
    
    xǁThreadedFileHandlerǁclose__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁThreadedFileHandlerǁclose__mutmut_1': xǁThreadedFileHandlerǁclose__mutmut_1, 
        'xǁThreadedFileHandlerǁclose__mutmut_2': xǁThreadedFileHandlerǁclose__mutmut_2, 
        'xǁThreadedFileHandlerǁclose__mutmut_3': xǁThreadedFileHandlerǁclose__mutmut_3, 
        'xǁThreadedFileHandlerǁclose__mutmut_4': xǁThreadedFileHandlerǁclose__mutmut_4, 
        'xǁThreadedFileHandlerǁclose__mutmut_5': xǁThreadedFileHandlerǁclose__mutmut_5, 
        'xǁThreadedFileHandlerǁclose__mutmut_6': xǁThreadedFileHandlerǁclose__mutmut_6
    }
    xǁThreadedFileHandlerǁclose__mutmut_orig.__name__ = 'xǁThreadedFileHandlerǁclose'


class _ExcludeStreamLoggers(logging.Filter):
    """Filter to exclude stdout/stderr loggers from console output."""

    def filter(self, record: logging.LogRecord) -> bool:
        args = [record]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁ_ExcludeStreamLoggersǁfilter__mutmut_orig'), object.__getattribute__(self, 'xǁ_ExcludeStreamLoggersǁfilter__mutmut_mutants'), args, kwargs, self)

    def xǁ_ExcludeStreamLoggersǁfilter__mutmut_orig(self, record: logging.LogRecord) -> bool:
        # Exclude to avoid double printing (already goes to console via StreamToLogger)
        return record.name not in ("stdout", "stderr")

    def xǁ_ExcludeStreamLoggersǁfilter__mutmut_1(self, record: logging.LogRecord) -> bool:
        # Exclude to avoid double printing (already goes to console via StreamToLogger)
        return record.name in ("stdout", "stderr")

    def xǁ_ExcludeStreamLoggersǁfilter__mutmut_2(self, record: logging.LogRecord) -> bool:
        # Exclude to avoid double printing (already goes to console via StreamToLogger)
        return record.name not in ("XXstdoutXX", "stderr")

    def xǁ_ExcludeStreamLoggersǁfilter__mutmut_3(self, record: logging.LogRecord) -> bool:
        # Exclude to avoid double printing (already goes to console via StreamToLogger)
        return record.name not in ("STDOUT", "stderr")

    def xǁ_ExcludeStreamLoggersǁfilter__mutmut_4(self, record: logging.LogRecord) -> bool:
        # Exclude to avoid double printing (already goes to console via StreamToLogger)
        return record.name not in ("stdout", "XXstderrXX")

    def xǁ_ExcludeStreamLoggersǁfilter__mutmut_5(self, record: logging.LogRecord) -> bool:
        # Exclude to avoid double printing (already goes to console via StreamToLogger)
        return record.name not in ("stdout", "STDERR")
    
    xǁ_ExcludeStreamLoggersǁfilter__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁ_ExcludeStreamLoggersǁfilter__mutmut_1': xǁ_ExcludeStreamLoggersǁfilter__mutmut_1, 
        'xǁ_ExcludeStreamLoggersǁfilter__mutmut_2': xǁ_ExcludeStreamLoggersǁfilter__mutmut_2, 
        'xǁ_ExcludeStreamLoggersǁfilter__mutmut_3': xǁ_ExcludeStreamLoggersǁfilter__mutmut_3, 
        'xǁ_ExcludeStreamLoggersǁfilter__mutmut_4': xǁ_ExcludeStreamLoggersǁfilter__mutmut_4, 
        'xǁ_ExcludeStreamLoggersǁfilter__mutmut_5': xǁ_ExcludeStreamLoggersǁfilter__mutmut_5
    }
    xǁ_ExcludeStreamLoggersǁfilter__mutmut_orig.__name__ = 'xǁ_ExcludeStreamLoggersǁfilter'


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
        args = [crash_log_path, fault_log_path, include_locals, exit_on_crash]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCrashHandlerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁCrashHandlerǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁCrashHandlerǁ__init____mutmut_orig(
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

    def xǁCrashHandlerǁ__init____mutmut_1(
        self,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = False,
        exit_on_crash: bool = True,
    ) -> None:
        self._crash_log_path = pathlib.Path(crash_log_path)
        self._fault_log_path = pathlib.Path(fault_log_path)
        self._include_locals = include_locals
        self._exit_on_crash = exit_on_crash
        self._original_excepthook = sys.excepthook
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_2(
        self,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = True,
        exit_on_crash: bool = False,
    ) -> None:
        self._crash_log_path = pathlib.Path(crash_log_path)
        self._fault_log_path = pathlib.Path(fault_log_path)
        self._include_locals = include_locals
        self._exit_on_crash = exit_on_crash
        self._original_excepthook = sys.excepthook
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_3(
        self,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = True,
        exit_on_crash: bool = True,
    ) -> None:
        self._crash_log_path = None
        self._fault_log_path = pathlib.Path(fault_log_path)
        self._include_locals = include_locals
        self._exit_on_crash = exit_on_crash
        self._original_excepthook = sys.excepthook
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_4(
        self,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = True,
        exit_on_crash: bool = True,
    ) -> None:
        self._crash_log_path = pathlib.Path(None)
        self._fault_log_path = pathlib.Path(fault_log_path)
        self._include_locals = include_locals
        self._exit_on_crash = exit_on_crash
        self._original_excepthook = sys.excepthook
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_5(
        self,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = True,
        exit_on_crash: bool = True,
    ) -> None:
        self._crash_log_path = pathlib.Path(crash_log_path)
        self._fault_log_path = None
        self._include_locals = include_locals
        self._exit_on_crash = exit_on_crash
        self._original_excepthook = sys.excepthook
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_6(
        self,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = True,
        exit_on_crash: bool = True,
    ) -> None:
        self._crash_log_path = pathlib.Path(crash_log_path)
        self._fault_log_path = pathlib.Path(None)
        self._include_locals = include_locals
        self._exit_on_crash = exit_on_crash
        self._original_excepthook = sys.excepthook
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_7(
        self,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = True,
        exit_on_crash: bool = True,
    ) -> None:
        self._crash_log_path = pathlib.Path(crash_log_path)
        self._fault_log_path = pathlib.Path(fault_log_path)
        self._include_locals = None
        self._exit_on_crash = exit_on_crash
        self._original_excepthook = sys.excepthook
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_8(
        self,
        crash_log_path: str = CRASH_LOG_PATH,
        fault_log_path: str = FAULT_LOG_PATH,
        include_locals: bool = True,
        exit_on_crash: bool = True,
    ) -> None:
        self._crash_log_path = pathlib.Path(crash_log_path)
        self._fault_log_path = pathlib.Path(fault_log_path)
        self._include_locals = include_locals
        self._exit_on_crash = None
        self._original_excepthook = sys.excepthook
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_9(
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
        self._original_excepthook = None
        self._original_threading_excepthook = getattr(threading, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_10(
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
        self._original_threading_excepthook = None
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_11(
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
        self._original_threading_excepthook = getattr(None, "excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_12(
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
        self._original_threading_excepthook = getattr(threading, None, None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_13(
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
        self._original_threading_excepthook = getattr("excepthook", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_14(
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
        self._original_threading_excepthook = getattr(threading, None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_15(
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
        self._original_threading_excepthook = getattr(threading, "excepthook", )
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_16(
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
        self._original_threading_excepthook = getattr(threading, "XXexcepthookXX", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_17(
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
        self._original_threading_excepthook = getattr(threading, "EXCEPTHOOK", None)
        self._fault_file: TextIO | None = None

    def xǁCrashHandlerǁ__init____mutmut_18(
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
        self._fault_file: TextIO | None = ""
    
    xǁCrashHandlerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCrashHandlerǁ__init____mutmut_1': xǁCrashHandlerǁ__init____mutmut_1, 
        'xǁCrashHandlerǁ__init____mutmut_2': xǁCrashHandlerǁ__init____mutmut_2, 
        'xǁCrashHandlerǁ__init____mutmut_3': xǁCrashHandlerǁ__init____mutmut_3, 
        'xǁCrashHandlerǁ__init____mutmut_4': xǁCrashHandlerǁ__init____mutmut_4, 
        'xǁCrashHandlerǁ__init____mutmut_5': xǁCrashHandlerǁ__init____mutmut_5, 
        'xǁCrashHandlerǁ__init____mutmut_6': xǁCrashHandlerǁ__init____mutmut_6, 
        'xǁCrashHandlerǁ__init____mutmut_7': xǁCrashHandlerǁ__init____mutmut_7, 
        'xǁCrashHandlerǁ__init____mutmut_8': xǁCrashHandlerǁ__init____mutmut_8, 
        'xǁCrashHandlerǁ__init____mutmut_9': xǁCrashHandlerǁ__init____mutmut_9, 
        'xǁCrashHandlerǁ__init____mutmut_10': xǁCrashHandlerǁ__init____mutmut_10, 
        'xǁCrashHandlerǁ__init____mutmut_11': xǁCrashHandlerǁ__init____mutmut_11, 
        'xǁCrashHandlerǁ__init____mutmut_12': xǁCrashHandlerǁ__init____mutmut_12, 
        'xǁCrashHandlerǁ__init____mutmut_13': xǁCrashHandlerǁ__init____mutmut_13, 
        'xǁCrashHandlerǁ__init____mutmut_14': xǁCrashHandlerǁ__init____mutmut_14, 
        'xǁCrashHandlerǁ__init____mutmut_15': xǁCrashHandlerǁ__init____mutmut_15, 
        'xǁCrashHandlerǁ__init____mutmut_16': xǁCrashHandlerǁ__init____mutmut_16, 
        'xǁCrashHandlerǁ__init____mutmut_17': xǁCrashHandlerǁ__init____mutmut_17, 
        'xǁCrashHandlerǁ__init____mutmut_18': xǁCrashHandlerǁ__init____mutmut_18
    }
    xǁCrashHandlerǁ__init____mutmut_orig.__name__ = 'xǁCrashHandlerǁ__init__'

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
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCrashHandlerǁ_install__mutmut_orig'), object.__getattribute__(self, 'xǁCrashHandlerǁ_install__mutmut_mutants'), args, kwargs, self)

    def xǁCrashHandlerǁ_install__mutmut_orig(self) -> None:
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

    def xǁCrashHandlerǁ_install__mutmut_1(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = None
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

    def xǁCrashHandlerǁ_install__mutmut_2(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(None, "w")
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

    def xǁCrashHandlerǁ_install__mutmut_3(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, None)
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

    def xǁCrashHandlerǁ_install__mutmut_4(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open("w")
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

    def xǁCrashHandlerǁ_install__mutmut_5(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, )
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

    def xǁCrashHandlerǁ_install__mutmut_6(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "XXwXX")
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

    def xǁCrashHandlerǁ_install__mutmut_7(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "W")
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

    def xǁCrashHandlerǁ_install__mutmut_8(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "w")
            faulthandler.enable(file=None, all_threads=True)

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

    def xǁCrashHandlerǁ_install__mutmut_9(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "w")
            faulthandler.enable(file=self._fault_file, all_threads=None)

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

    def xǁCrashHandlerǁ_install__mutmut_10(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "w")
            faulthandler.enable(all_threads=True)

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

    def xǁCrashHandlerǁ_install__mutmut_11(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "w")
            faulthandler.enable(file=self._fault_file, )

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

    def xǁCrashHandlerǁ_install__mutmut_12(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "w")
            faulthandler.enable(file=self._fault_file, all_threads=False)

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

    def xǁCrashHandlerǁ_install__mutmut_13(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "w")
            faulthandler.enable(file=self._fault_file, all_threads=True)

            # Also dump traceback on SIGUSR1 (useful for debugging hangs)
            try:
                import signal

                faulthandler.register(
                    None,
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

    def xǁCrashHandlerǁ_install__mutmut_14(self) -> None:
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
                    file=None,
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

    def xǁCrashHandlerǁ_install__mutmut_15(self) -> None:
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
                    all_threads=None,
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

    def xǁCrashHandlerǁ_install__mutmut_16(self) -> None:
        """Install exception hooks."""
        # Setup faulthandler for C-level crashes (segfaults, etc.)
        try:
            self._fault_file = open(self._fault_log_path, "w")
            faulthandler.enable(file=self._fault_file, all_threads=True)

            # Also dump traceback on SIGUSR1 (useful for debugging hangs)
            try:
                import signal

                faulthandler.register(
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

    def xǁCrashHandlerǁ_install__mutmut_17(self) -> None:
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

    def xǁCrashHandlerǁ_install__mutmut_18(self) -> None:
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

    def xǁCrashHandlerǁ_install__mutmut_19(self) -> None:
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
                    all_threads=False,
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

    def xǁCrashHandlerǁ_install__mutmut_20(self) -> None:
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
            sys.stderr.write(None)

        # Install Python exception hook
        sys.excepthook = self._exception_hook

        # Install threading exception hook (Python 3.8+)
        if hasattr(threading, "excepthook"):
            threading.excepthook = self._threading_exception_hook

    def xǁCrashHandlerǁ_install__mutmut_21(self) -> None:
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
        sys.excepthook = None

        # Install threading exception hook (Python 3.8+)
        if hasattr(threading, "excepthook"):
            threading.excepthook = self._threading_exception_hook

    def xǁCrashHandlerǁ_install__mutmut_22(self) -> None:
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
        if hasattr(None, "excepthook"):
            threading.excepthook = self._threading_exception_hook

    def xǁCrashHandlerǁ_install__mutmut_23(self) -> None:
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
        if hasattr(threading, None):
            threading.excepthook = self._threading_exception_hook

    def xǁCrashHandlerǁ_install__mutmut_24(self) -> None:
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
        if hasattr("excepthook"):
            threading.excepthook = self._threading_exception_hook

    def xǁCrashHandlerǁ_install__mutmut_25(self) -> None:
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
        if hasattr(threading, ):
            threading.excepthook = self._threading_exception_hook

    def xǁCrashHandlerǁ_install__mutmut_26(self) -> None:
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
        if hasattr(threading, "XXexcepthookXX"):
            threading.excepthook = self._threading_exception_hook

    def xǁCrashHandlerǁ_install__mutmut_27(self) -> None:
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
        if hasattr(threading, "EXCEPTHOOK"):
            threading.excepthook = self._threading_exception_hook

    def xǁCrashHandlerǁ_install__mutmut_28(self) -> None:
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
            threading.excepthook = None
    
    xǁCrashHandlerǁ_install__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCrashHandlerǁ_install__mutmut_1': xǁCrashHandlerǁ_install__mutmut_1, 
        'xǁCrashHandlerǁ_install__mutmut_2': xǁCrashHandlerǁ_install__mutmut_2, 
        'xǁCrashHandlerǁ_install__mutmut_3': xǁCrashHandlerǁ_install__mutmut_3, 
        'xǁCrashHandlerǁ_install__mutmut_4': xǁCrashHandlerǁ_install__mutmut_4, 
        'xǁCrashHandlerǁ_install__mutmut_5': xǁCrashHandlerǁ_install__mutmut_5, 
        'xǁCrashHandlerǁ_install__mutmut_6': xǁCrashHandlerǁ_install__mutmut_6, 
        'xǁCrashHandlerǁ_install__mutmut_7': xǁCrashHandlerǁ_install__mutmut_7, 
        'xǁCrashHandlerǁ_install__mutmut_8': xǁCrashHandlerǁ_install__mutmut_8, 
        'xǁCrashHandlerǁ_install__mutmut_9': xǁCrashHandlerǁ_install__mutmut_9, 
        'xǁCrashHandlerǁ_install__mutmut_10': xǁCrashHandlerǁ_install__mutmut_10, 
        'xǁCrashHandlerǁ_install__mutmut_11': xǁCrashHandlerǁ_install__mutmut_11, 
        'xǁCrashHandlerǁ_install__mutmut_12': xǁCrashHandlerǁ_install__mutmut_12, 
        'xǁCrashHandlerǁ_install__mutmut_13': xǁCrashHandlerǁ_install__mutmut_13, 
        'xǁCrashHandlerǁ_install__mutmut_14': xǁCrashHandlerǁ_install__mutmut_14, 
        'xǁCrashHandlerǁ_install__mutmut_15': xǁCrashHandlerǁ_install__mutmut_15, 
        'xǁCrashHandlerǁ_install__mutmut_16': xǁCrashHandlerǁ_install__mutmut_16, 
        'xǁCrashHandlerǁ_install__mutmut_17': xǁCrashHandlerǁ_install__mutmut_17, 
        'xǁCrashHandlerǁ_install__mutmut_18': xǁCrashHandlerǁ_install__mutmut_18, 
        'xǁCrashHandlerǁ_install__mutmut_19': xǁCrashHandlerǁ_install__mutmut_19, 
        'xǁCrashHandlerǁ_install__mutmut_20': xǁCrashHandlerǁ_install__mutmut_20, 
        'xǁCrashHandlerǁ_install__mutmut_21': xǁCrashHandlerǁ_install__mutmut_21, 
        'xǁCrashHandlerǁ_install__mutmut_22': xǁCrashHandlerǁ_install__mutmut_22, 
        'xǁCrashHandlerǁ_install__mutmut_23': xǁCrashHandlerǁ_install__mutmut_23, 
        'xǁCrashHandlerǁ_install__mutmut_24': xǁCrashHandlerǁ_install__mutmut_24, 
        'xǁCrashHandlerǁ_install__mutmut_25': xǁCrashHandlerǁ_install__mutmut_25, 
        'xǁCrashHandlerǁ_install__mutmut_26': xǁCrashHandlerǁ_install__mutmut_26, 
        'xǁCrashHandlerǁ_install__mutmut_27': xǁCrashHandlerǁ_install__mutmut_27, 
        'xǁCrashHandlerǁ_install__mutmut_28': xǁCrashHandlerǁ_install__mutmut_28
    }
    xǁCrashHandlerǁ_install__mutmut_orig.__name__ = 'xǁCrashHandlerǁ_install'

    def _format_exception_detailed(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        args = [exc_type, exc_value, exc_tb]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCrashHandlerǁ_format_exception_detailed__mutmut_orig'), object.__getattribute__(self, 'xǁCrashHandlerǁ_format_exception_detailed__mutmut_mutants'), args, kwargs, self)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_orig(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_1(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = None

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_2(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_3(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" / 80)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_4(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("XX=XX" * 80)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_5(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 81)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_6(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_7(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("XXUNHANDLED EXCEPTIONXX")
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_8(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("unhandled exception")
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_9(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("UNHANDLED EXCEPTION")
        lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_10(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("UNHANDLED EXCEPTION")
        lines.append("=" / 80)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_11(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("UNHANDLED EXCEPTION")
        lines.append("XX=XX" * 80)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_12(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("UNHANDLED EXCEPTION")
        lines.append("=" * 81)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_13(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("UNHANDLED EXCEPTION")
        lines.append("=" * 80)
        lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_14(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("UNHANDLED EXCEPTION")
        lines.append("=" * 80)
        lines.append(f"Time: {datetime.now().isoformat()}")
        lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_15(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> str:
        """Format exception with detailed information."""
        lines: list[str] = []

        # Header
        lines.append("=" * 80)
        lines.append("UNHANDLED EXCEPTION")
        lines.append("=" * 80)
        lines.append(f"Time: {datetime.now().isoformat()}")
        lines.append(f"Thread: {threading.current_thread().name}")
        lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_16(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_17(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append(None)

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_18(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("XXXX")

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_19(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_20(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("-" / 80)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_21(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("XX-XX" * 80)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_22(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("-" * 81)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_23(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_24(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("XXTRACEBACK (most recent call last):XX")
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_25(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("traceback (most recent call last):")
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_26(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("TRACEBACK (MOST RECENT CALL LAST):")
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_27(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append(None)

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_28(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("-" / 80)

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_29(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("XX-XX" * 80)

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_30(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        lines.append("-" * 81)

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_31(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        tb_frames = None

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_32(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
        tb_frames = traceback.extract_tb(None)

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_33(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        for i, frame in enumerate(None):
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_34(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
            lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_35(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
            lines.append("XXXX")
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_36(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
            lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_37(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
            lines.append(f"  Frame {i - 1}: {frame.filename}")
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_38(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
            lines.append(f"  Frame {i + 2}: {frame.filename}")
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_39(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
            lines.append(None)
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_40(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
            lines.append(None)

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_41(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
            if self._include_locals or exc_tb:
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_42(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                    current_tb = None
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_43(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                    for _ in range(None):
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_44(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            current_tb = None

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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_45(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

                    frame_locals = None
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_46(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                        lines.append(None)
                        for name, value in frame_locals.items():
                            # Skip private/dunder and limit value length
                            if name.startswith("__"):
                                continue
                            try:
                                value_str = repr(value)
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_47(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                        lines.append("XX    Locals:XX")
                        for name, value in frame_locals.items():
                            # Skip private/dunder and limit value length
                            if name.startswith("__"):
                                continue
                            try:
                                value_str = repr(value)
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_48(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                        lines.append("    locals:")
                        for name, value in frame_locals.items():
                            # Skip private/dunder and limit value length
                            if name.startswith("__"):
                                continue
                            try:
                                value_str = repr(value)
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_49(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                        lines.append("    LOCALS:")
                        for name, value in frame_locals.items():
                            # Skip private/dunder and limit value length
                            if name.startswith("__"):
                                continue
                            try:
                                value_str = repr(value)
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_50(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            if name.startswith(None):
                                continue
                            try:
                                value_str = repr(value)
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_51(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            if name.startswith("XX__XX"):
                                continue
                            try:
                                value_str = repr(value)
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_52(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                                break
                            try:
                                value_str = repr(value)
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_53(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                                value_str = None
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_54(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                                value_str = repr(None)
                                if len(value_str) > 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_55(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                                if len(value_str) >= 200:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_56(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                                if len(value_str) > 201:
                                    value_str = value_str[:200] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_57(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                                    value_str = None
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_58(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                                    value_str = value_str[:200] - "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_59(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                                    value_str = value_str[:201] + "..."
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_60(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                                    value_str = value_str[:200] + "XX...XX"
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_61(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = None
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_62(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "XX<repr failed>XX"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_63(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<REPR FAILED>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_64(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(None)
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_65(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append(None)

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_66(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("XX    Locals: <unavailable>XX")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_67(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    locals: <unavailable>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_68(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    LOCALS: <UNAVAILABLE>")

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_69(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append(None)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_70(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("XXXX")
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_71(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append(None)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_72(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" / 80)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_73(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("XX-XX" * 80)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_74(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 81)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_75(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append(None)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_76(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("XXSTANDARD TRACEBACK:XX")
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_77(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("standard traceback:")
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_78(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append(None)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_79(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" / 80)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_80(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("XX-XX" * 80)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_81(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 81)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_82(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append(None)

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_83(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(None))

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_84(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("XXXX".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_85(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(None, exc_value, exc_tb)))

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_86(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, None, exc_tb)))

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_87(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, None)))

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_88(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_value, exc_tb)))

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_89(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_tb)))

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_90(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, )))

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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_91(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append(None)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_92(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" / 80)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_93(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("XX-XX" * 80)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_94(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" * 81)
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

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_95(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" * 80)
        lines.append(None)
        lines.append("-" * 80)
        for thread in threading.enumerate():
            daemon_str = " (daemon)" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_96(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" * 80)
        lines.append("XXACTIVE THREADS:XX")
        lines.append("-" * 80)
        for thread in threading.enumerate():
            daemon_str = " (daemon)" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_97(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" * 80)
        lines.append("active threads:")
        lines.append("-" * 80)
        for thread in threading.enumerate():
            daemon_str = " (daemon)" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_98(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" * 80)
        lines.append("ACTIVE THREADS:")
        lines.append(None)
        for thread in threading.enumerate():
            daemon_str = " (daemon)" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_99(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" * 80)
        lines.append("ACTIVE THREADS:")
        lines.append("-" / 80)
        for thread in threading.enumerate():
            daemon_str = " (daemon)" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_100(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" * 80)
        lines.append("ACTIVE THREADS:")
        lines.append("XX-XX" * 80)
        for thread in threading.enumerate():
            daemon_str = " (daemon)" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_101(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

        # Standard traceback
        lines.append("")
        lines.append("-" * 80)
        lines.append("STANDARD TRACEBACK:")
        lines.append("-" * 80)
        lines.append("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))

        # Thread info
        lines.append("-" * 80)
        lines.append("ACTIVE THREADS:")
        lines.append("-" * 81)
        for thread in threading.enumerate():
            daemon_str = " (daemon)" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_102(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
            daemon_str = None
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_103(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
            daemon_str = "XX (daemon)XX" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_104(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
            daemon_str = " (DAEMON)" if thread.daemon else ""
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_105(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
            daemon_str = " (daemon)" if thread.daemon else "XXXX"
            lines.append(
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_106(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
                None
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_107(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
                f"  - {thread.name}{daemon_str}: {'XXaliveXX' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_108(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
                f"  - {thread.name}{daemon_str}: {'ALIVE' if thread.is_alive() else 'dead'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_109(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'XXdeadXX'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_110(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
                f"  - {thread.name}{daemon_str}: {'alive' if thread.is_alive() else 'DEAD'}"
            )

        lines.append("")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_111(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

        lines.append(None)
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_112(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

        lines.append("XXXX")
        lines.append("=" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_113(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
        lines.append(None)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_114(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
        lines.append("=" / 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_115(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
        lines.append("XX=XX" * 80)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_116(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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
        lines.append("=" * 81)

        return "\n".join(lines)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_117(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

        return "\n".join(None)

    def xǁCrashHandlerǁ_format_exception_detailed__mutmut_118(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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
                            except (
                                Exception
                            ):  # repr() may raise arbitrary errors on broken objects
                                value_str = "<repr failed>"
                            lines.append(f"      {name} = {value_str}")
                except (AttributeError, TypeError):
                    lines.append("    Locals: <unavailable>")

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

        return "XX\nXX".join(lines)
    
    xǁCrashHandlerǁ_format_exception_detailed__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCrashHandlerǁ_format_exception_detailed__mutmut_1': xǁCrashHandlerǁ_format_exception_detailed__mutmut_1, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_2': xǁCrashHandlerǁ_format_exception_detailed__mutmut_2, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_3': xǁCrashHandlerǁ_format_exception_detailed__mutmut_3, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_4': xǁCrashHandlerǁ_format_exception_detailed__mutmut_4, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_5': xǁCrashHandlerǁ_format_exception_detailed__mutmut_5, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_6': xǁCrashHandlerǁ_format_exception_detailed__mutmut_6, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_7': xǁCrashHandlerǁ_format_exception_detailed__mutmut_7, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_8': xǁCrashHandlerǁ_format_exception_detailed__mutmut_8, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_9': xǁCrashHandlerǁ_format_exception_detailed__mutmut_9, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_10': xǁCrashHandlerǁ_format_exception_detailed__mutmut_10, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_11': xǁCrashHandlerǁ_format_exception_detailed__mutmut_11, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_12': xǁCrashHandlerǁ_format_exception_detailed__mutmut_12, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_13': xǁCrashHandlerǁ_format_exception_detailed__mutmut_13, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_14': xǁCrashHandlerǁ_format_exception_detailed__mutmut_14, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_15': xǁCrashHandlerǁ_format_exception_detailed__mutmut_15, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_16': xǁCrashHandlerǁ_format_exception_detailed__mutmut_16, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_17': xǁCrashHandlerǁ_format_exception_detailed__mutmut_17, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_18': xǁCrashHandlerǁ_format_exception_detailed__mutmut_18, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_19': xǁCrashHandlerǁ_format_exception_detailed__mutmut_19, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_20': xǁCrashHandlerǁ_format_exception_detailed__mutmut_20, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_21': xǁCrashHandlerǁ_format_exception_detailed__mutmut_21, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_22': xǁCrashHandlerǁ_format_exception_detailed__mutmut_22, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_23': xǁCrashHandlerǁ_format_exception_detailed__mutmut_23, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_24': xǁCrashHandlerǁ_format_exception_detailed__mutmut_24, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_25': xǁCrashHandlerǁ_format_exception_detailed__mutmut_25, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_26': xǁCrashHandlerǁ_format_exception_detailed__mutmut_26, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_27': xǁCrashHandlerǁ_format_exception_detailed__mutmut_27, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_28': xǁCrashHandlerǁ_format_exception_detailed__mutmut_28, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_29': xǁCrashHandlerǁ_format_exception_detailed__mutmut_29, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_30': xǁCrashHandlerǁ_format_exception_detailed__mutmut_30, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_31': xǁCrashHandlerǁ_format_exception_detailed__mutmut_31, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_32': xǁCrashHandlerǁ_format_exception_detailed__mutmut_32, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_33': xǁCrashHandlerǁ_format_exception_detailed__mutmut_33, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_34': xǁCrashHandlerǁ_format_exception_detailed__mutmut_34, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_35': xǁCrashHandlerǁ_format_exception_detailed__mutmut_35, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_36': xǁCrashHandlerǁ_format_exception_detailed__mutmut_36, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_37': xǁCrashHandlerǁ_format_exception_detailed__mutmut_37, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_38': xǁCrashHandlerǁ_format_exception_detailed__mutmut_38, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_39': xǁCrashHandlerǁ_format_exception_detailed__mutmut_39, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_40': xǁCrashHandlerǁ_format_exception_detailed__mutmut_40, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_41': xǁCrashHandlerǁ_format_exception_detailed__mutmut_41, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_42': xǁCrashHandlerǁ_format_exception_detailed__mutmut_42, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_43': xǁCrashHandlerǁ_format_exception_detailed__mutmut_43, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_44': xǁCrashHandlerǁ_format_exception_detailed__mutmut_44, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_45': xǁCrashHandlerǁ_format_exception_detailed__mutmut_45, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_46': xǁCrashHandlerǁ_format_exception_detailed__mutmut_46, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_47': xǁCrashHandlerǁ_format_exception_detailed__mutmut_47, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_48': xǁCrashHandlerǁ_format_exception_detailed__mutmut_48, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_49': xǁCrashHandlerǁ_format_exception_detailed__mutmut_49, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_50': xǁCrashHandlerǁ_format_exception_detailed__mutmut_50, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_51': xǁCrashHandlerǁ_format_exception_detailed__mutmut_51, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_52': xǁCrashHandlerǁ_format_exception_detailed__mutmut_52, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_53': xǁCrashHandlerǁ_format_exception_detailed__mutmut_53, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_54': xǁCrashHandlerǁ_format_exception_detailed__mutmut_54, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_55': xǁCrashHandlerǁ_format_exception_detailed__mutmut_55, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_56': xǁCrashHandlerǁ_format_exception_detailed__mutmut_56, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_57': xǁCrashHandlerǁ_format_exception_detailed__mutmut_57, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_58': xǁCrashHandlerǁ_format_exception_detailed__mutmut_58, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_59': xǁCrashHandlerǁ_format_exception_detailed__mutmut_59, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_60': xǁCrashHandlerǁ_format_exception_detailed__mutmut_60, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_61': xǁCrashHandlerǁ_format_exception_detailed__mutmut_61, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_62': xǁCrashHandlerǁ_format_exception_detailed__mutmut_62, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_63': xǁCrashHandlerǁ_format_exception_detailed__mutmut_63, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_64': xǁCrashHandlerǁ_format_exception_detailed__mutmut_64, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_65': xǁCrashHandlerǁ_format_exception_detailed__mutmut_65, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_66': xǁCrashHandlerǁ_format_exception_detailed__mutmut_66, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_67': xǁCrashHandlerǁ_format_exception_detailed__mutmut_67, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_68': xǁCrashHandlerǁ_format_exception_detailed__mutmut_68, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_69': xǁCrashHandlerǁ_format_exception_detailed__mutmut_69, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_70': xǁCrashHandlerǁ_format_exception_detailed__mutmut_70, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_71': xǁCrashHandlerǁ_format_exception_detailed__mutmut_71, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_72': xǁCrashHandlerǁ_format_exception_detailed__mutmut_72, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_73': xǁCrashHandlerǁ_format_exception_detailed__mutmut_73, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_74': xǁCrashHandlerǁ_format_exception_detailed__mutmut_74, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_75': xǁCrashHandlerǁ_format_exception_detailed__mutmut_75, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_76': xǁCrashHandlerǁ_format_exception_detailed__mutmut_76, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_77': xǁCrashHandlerǁ_format_exception_detailed__mutmut_77, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_78': xǁCrashHandlerǁ_format_exception_detailed__mutmut_78, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_79': xǁCrashHandlerǁ_format_exception_detailed__mutmut_79, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_80': xǁCrashHandlerǁ_format_exception_detailed__mutmut_80, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_81': xǁCrashHandlerǁ_format_exception_detailed__mutmut_81, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_82': xǁCrashHandlerǁ_format_exception_detailed__mutmut_82, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_83': xǁCrashHandlerǁ_format_exception_detailed__mutmut_83, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_84': xǁCrashHandlerǁ_format_exception_detailed__mutmut_84, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_85': xǁCrashHandlerǁ_format_exception_detailed__mutmut_85, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_86': xǁCrashHandlerǁ_format_exception_detailed__mutmut_86, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_87': xǁCrashHandlerǁ_format_exception_detailed__mutmut_87, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_88': xǁCrashHandlerǁ_format_exception_detailed__mutmut_88, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_89': xǁCrashHandlerǁ_format_exception_detailed__mutmut_89, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_90': xǁCrashHandlerǁ_format_exception_detailed__mutmut_90, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_91': xǁCrashHandlerǁ_format_exception_detailed__mutmut_91, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_92': xǁCrashHandlerǁ_format_exception_detailed__mutmut_92, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_93': xǁCrashHandlerǁ_format_exception_detailed__mutmut_93, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_94': xǁCrashHandlerǁ_format_exception_detailed__mutmut_94, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_95': xǁCrashHandlerǁ_format_exception_detailed__mutmut_95, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_96': xǁCrashHandlerǁ_format_exception_detailed__mutmut_96, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_97': xǁCrashHandlerǁ_format_exception_detailed__mutmut_97, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_98': xǁCrashHandlerǁ_format_exception_detailed__mutmut_98, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_99': xǁCrashHandlerǁ_format_exception_detailed__mutmut_99, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_100': xǁCrashHandlerǁ_format_exception_detailed__mutmut_100, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_101': xǁCrashHandlerǁ_format_exception_detailed__mutmut_101, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_102': xǁCrashHandlerǁ_format_exception_detailed__mutmut_102, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_103': xǁCrashHandlerǁ_format_exception_detailed__mutmut_103, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_104': xǁCrashHandlerǁ_format_exception_detailed__mutmut_104, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_105': xǁCrashHandlerǁ_format_exception_detailed__mutmut_105, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_106': xǁCrashHandlerǁ_format_exception_detailed__mutmut_106, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_107': xǁCrashHandlerǁ_format_exception_detailed__mutmut_107, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_108': xǁCrashHandlerǁ_format_exception_detailed__mutmut_108, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_109': xǁCrashHandlerǁ_format_exception_detailed__mutmut_109, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_110': xǁCrashHandlerǁ_format_exception_detailed__mutmut_110, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_111': xǁCrashHandlerǁ_format_exception_detailed__mutmut_111, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_112': xǁCrashHandlerǁ_format_exception_detailed__mutmut_112, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_113': xǁCrashHandlerǁ_format_exception_detailed__mutmut_113, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_114': xǁCrashHandlerǁ_format_exception_detailed__mutmut_114, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_115': xǁCrashHandlerǁ_format_exception_detailed__mutmut_115, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_116': xǁCrashHandlerǁ_format_exception_detailed__mutmut_116, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_117': xǁCrashHandlerǁ_format_exception_detailed__mutmut_117, 
        'xǁCrashHandlerǁ_format_exception_detailed__mutmut_118': xǁCrashHandlerǁ_format_exception_detailed__mutmut_118
    }
    xǁCrashHandlerǁ_format_exception_detailed__mutmut_orig.__name__ = 'xǁCrashHandlerǁ_format_exception_detailed'

    def _write_crash_log(self, content: str) -> None:
        args = [content]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCrashHandlerǁ_write_crash_log__mutmut_orig'), object.__getattribute__(self, 'xǁCrashHandlerǁ_write_crash_log__mutmut_mutants'), args, kwargs, self)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_orig(self, content: str) -> None:
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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_1(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=None, exist_ok=True)

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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_2(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=None)

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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_3(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(exist_ok=True)

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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_4(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, )

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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_5(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=False, exist_ok=True)

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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_6(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=False)

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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_7(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(None, "w") as f:
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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_8(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, None) as f:
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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_9(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open("w") as f:
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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_10(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, ) as f:
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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_11(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "XXwXX") as f:
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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_12(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "W") as f:
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

    def xǁCrashHandlerǁ_write_crash_log__mutmut_13(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(None)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(".history.log")
            with open(history_path, "a") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_14(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = None
            with open(history_path, "a") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_15(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(None)
            with open(history_path, "a") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_16(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix("XX.history.logXX")
            with open(history_path, "a") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_17(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(".HISTORY.LOG")
            with open(history_path, "a") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_18(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(".history.log")
            with open(None, "a") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_19(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(".history.log")
            with open(history_path, None) as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_20(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(".history.log")
            with open("a") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_21(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(".history.log")
            with open(history_path, ) as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_22(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(".history.log")
            with open(history_path, "XXaXX") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_23(self, content: str) -> None:
        """Write crash information to log file."""
        try:
            # Ensure directory exists
            self._crash_log_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to crash log
            with open(self._crash_log_path, "w") as f:
                f.write(content)

            # Also append to a history file
            history_path = self._crash_log_path.with_suffix(".history.log")
            with open(history_path, "A") as f:
                f.write(content)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_24(self, content: str) -> None:
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
                f.write(None)
                f.write("\n\n")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_25(self, content: str) -> None:
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
                f.write(None)

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_26(self, content: str) -> None:
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
                f.write("XX\n\nXX")

        except Exception as e:
            # Last resort: write to stderr
            sys.stderr.write(f"Failed to write crash log: {e}\n")
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_27(self, content: str) -> None:
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
            sys.stderr.write(None)
            sys.stderr.write(content)

    def xǁCrashHandlerǁ_write_crash_log__mutmut_28(self, content: str) -> None:
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
            sys.stderr.write(None)
    
    xǁCrashHandlerǁ_write_crash_log__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCrashHandlerǁ_write_crash_log__mutmut_1': xǁCrashHandlerǁ_write_crash_log__mutmut_1, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_2': xǁCrashHandlerǁ_write_crash_log__mutmut_2, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_3': xǁCrashHandlerǁ_write_crash_log__mutmut_3, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_4': xǁCrashHandlerǁ_write_crash_log__mutmut_4, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_5': xǁCrashHandlerǁ_write_crash_log__mutmut_5, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_6': xǁCrashHandlerǁ_write_crash_log__mutmut_6, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_7': xǁCrashHandlerǁ_write_crash_log__mutmut_7, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_8': xǁCrashHandlerǁ_write_crash_log__mutmut_8, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_9': xǁCrashHandlerǁ_write_crash_log__mutmut_9, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_10': xǁCrashHandlerǁ_write_crash_log__mutmut_10, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_11': xǁCrashHandlerǁ_write_crash_log__mutmut_11, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_12': xǁCrashHandlerǁ_write_crash_log__mutmut_12, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_13': xǁCrashHandlerǁ_write_crash_log__mutmut_13, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_14': xǁCrashHandlerǁ_write_crash_log__mutmut_14, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_15': xǁCrashHandlerǁ_write_crash_log__mutmut_15, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_16': xǁCrashHandlerǁ_write_crash_log__mutmut_16, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_17': xǁCrashHandlerǁ_write_crash_log__mutmut_17, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_18': xǁCrashHandlerǁ_write_crash_log__mutmut_18, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_19': xǁCrashHandlerǁ_write_crash_log__mutmut_19, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_20': xǁCrashHandlerǁ_write_crash_log__mutmut_20, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_21': xǁCrashHandlerǁ_write_crash_log__mutmut_21, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_22': xǁCrashHandlerǁ_write_crash_log__mutmut_22, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_23': xǁCrashHandlerǁ_write_crash_log__mutmut_23, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_24': xǁCrashHandlerǁ_write_crash_log__mutmut_24, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_25': xǁCrashHandlerǁ_write_crash_log__mutmut_25, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_26': xǁCrashHandlerǁ_write_crash_log__mutmut_26, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_27': xǁCrashHandlerǁ_write_crash_log__mutmut_27, 
        'xǁCrashHandlerǁ_write_crash_log__mutmut_28': xǁCrashHandlerǁ_write_crash_log__mutmut_28
    }
    xǁCrashHandlerǁ_write_crash_log__mutmut_orig.__name__ = 'xǁCrashHandlerǁ_write_crash_log'

    def _exception_hook(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        args = [exc_type, exc_value, exc_tb]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCrashHandlerǁ_exception_hook__mutmut_orig'), object.__getattribute__(self, 'xǁCrashHandlerǁ_exception_hook__mutmut_mutants'), args, kwargs, self)

    def xǁCrashHandlerǁ_exception_hook__mutmut_orig(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_1(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(None, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_2(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, None):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_3(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_4(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, ):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_5(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(None, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_6(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, None, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_7(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, None)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_8(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_9(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_10(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, )
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_11(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = None

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_12(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(None, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_13(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, None, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_14(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, None)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_15(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_16(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_tb)

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_17(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_18(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions."""
        # Don't handle keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            self._original_excepthook(exc_type, exc_value, exc_tb)
            return

        # Format detailed crash info
        crash_info = self._format_exception_detailed(exc_type, exc_value, exc_tb)

        # Write to crash log
        self._write_crash_log(None)

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_19(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                None, self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_20(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", None
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_21(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_22(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_23(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger(None).critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_24(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("XXcrashXX").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_25(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("CRASH").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_26(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "XXUnhandled exception - see %s for detailsXX", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_27(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_28(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "UNHANDLED EXCEPTION - SEE %S FOR DETAILS", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_29(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(None)

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_30(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(None, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_31(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, None, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_32(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, None)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_33(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_34(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_35(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, )

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(1)

    def xǁCrashHandlerǁ_exception_hook__mutmut_36(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(None)

    def xǁCrashHandlerǁ_exception_hook__mutmut_37(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_tb: types.TracebackType | None,
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

        # Also log via logging if available (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled exception - see %s for details", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook (prints traceback)
        self._original_excepthook(exc_type, exc_value, exc_tb)

        # Force exit if configured (for systemd restart)
        if self._exit_on_crash:
            os._exit(2)
    
    xǁCrashHandlerǁ_exception_hook__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCrashHandlerǁ_exception_hook__mutmut_1': xǁCrashHandlerǁ_exception_hook__mutmut_1, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_2': xǁCrashHandlerǁ_exception_hook__mutmut_2, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_3': xǁCrashHandlerǁ_exception_hook__mutmut_3, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_4': xǁCrashHandlerǁ_exception_hook__mutmut_4, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_5': xǁCrashHandlerǁ_exception_hook__mutmut_5, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_6': xǁCrashHandlerǁ_exception_hook__mutmut_6, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_7': xǁCrashHandlerǁ_exception_hook__mutmut_7, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_8': xǁCrashHandlerǁ_exception_hook__mutmut_8, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_9': xǁCrashHandlerǁ_exception_hook__mutmut_9, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_10': xǁCrashHandlerǁ_exception_hook__mutmut_10, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_11': xǁCrashHandlerǁ_exception_hook__mutmut_11, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_12': xǁCrashHandlerǁ_exception_hook__mutmut_12, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_13': xǁCrashHandlerǁ_exception_hook__mutmut_13, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_14': xǁCrashHandlerǁ_exception_hook__mutmut_14, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_15': xǁCrashHandlerǁ_exception_hook__mutmut_15, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_16': xǁCrashHandlerǁ_exception_hook__mutmut_16, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_17': xǁCrashHandlerǁ_exception_hook__mutmut_17, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_18': xǁCrashHandlerǁ_exception_hook__mutmut_18, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_19': xǁCrashHandlerǁ_exception_hook__mutmut_19, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_20': xǁCrashHandlerǁ_exception_hook__mutmut_20, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_21': xǁCrashHandlerǁ_exception_hook__mutmut_21, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_22': xǁCrashHandlerǁ_exception_hook__mutmut_22, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_23': xǁCrashHandlerǁ_exception_hook__mutmut_23, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_24': xǁCrashHandlerǁ_exception_hook__mutmut_24, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_25': xǁCrashHandlerǁ_exception_hook__mutmut_25, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_26': xǁCrashHandlerǁ_exception_hook__mutmut_26, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_27': xǁCrashHandlerǁ_exception_hook__mutmut_27, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_28': xǁCrashHandlerǁ_exception_hook__mutmut_28, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_29': xǁCrashHandlerǁ_exception_hook__mutmut_29, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_30': xǁCrashHandlerǁ_exception_hook__mutmut_30, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_31': xǁCrashHandlerǁ_exception_hook__mutmut_31, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_32': xǁCrashHandlerǁ_exception_hook__mutmut_32, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_33': xǁCrashHandlerǁ_exception_hook__mutmut_33, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_34': xǁCrashHandlerǁ_exception_hook__mutmut_34, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_35': xǁCrashHandlerǁ_exception_hook__mutmut_35, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_36': xǁCrashHandlerǁ_exception_hook__mutmut_36, 
        'xǁCrashHandlerǁ_exception_hook__mutmut_37': xǁCrashHandlerǁ_exception_hook__mutmut_37
    }
    xǁCrashHandlerǁ_exception_hook__mutmut_orig.__name__ = 'xǁCrashHandlerǁ_exception_hook'

    def _threading_exception_hook(self, args: threading.ExceptHookArgs) -> None:
        args = [args]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCrashHandlerǁ_threading_exception_hook__mutmut_orig'), object.__getattribute__(self, 'xǁCrashHandlerǁ_threading_exception_hook__mutmut_mutants'), args, kwargs, self)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_orig(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_1(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = None

        # Add thread context
        thread_info = (
            f"\nThread that crashed: {args.thread.name if args.thread else 'Unknown'}\n"
        )
        crash_info = crash_info.replace(
            "UNHANDLED EXCEPTION", f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_2(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            None, args.exc_value, args.exc_traceback
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_3(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, None, args.exc_traceback
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_4(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, args.exc_value, None
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_5(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_value, args.exc_traceback
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_6(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, args.exc_traceback
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_7(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, args.exc_value, )

        # Add thread context
        thread_info = (
            f"\nThread that crashed: {args.thread.name if args.thread else 'Unknown'}\n"
        )
        crash_info = crash_info.replace(
            "UNHANDLED EXCEPTION", f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_8(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, args.exc_value, args.exc_traceback
        )

        # Add thread context
        thread_info = None
        crash_info = crash_info.replace(
            "UNHANDLED EXCEPTION", f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_9(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, args.exc_value, args.exc_traceback
        )

        # Add thread context
        thread_info = (
            f"\nThread that crashed: {args.thread.name if args.thread else 'XXUnknownXX'}\n"
        )
        crash_info = crash_info.replace(
            "UNHANDLED EXCEPTION", f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_10(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, args.exc_value, args.exc_traceback
        )

        # Add thread context
        thread_info = (
            f"\nThread that crashed: {args.thread.name if args.thread else 'unknown'}\n"
        )
        crash_info = crash_info.replace(
            "UNHANDLED EXCEPTION", f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_11(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, args.exc_value, args.exc_traceback
        )

        # Add thread context
        thread_info = (
            f"\nThread that crashed: {args.thread.name if args.thread else 'UNKNOWN'}\n"
        )
        crash_info = crash_info.replace(
            "UNHANDLED EXCEPTION", f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_12(self, args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in threads."""
        # Format detailed crash info
        crash_info = self._format_exception_detailed(
            args.exc_type, args.exc_value, args.exc_traceback
        )

        # Add thread context
        thread_info = (
            f"\nThread that crashed: {args.thread.name if args.thread else 'Unknown'}\n"
        )
        crash_info = None

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_13(self, args: threading.ExceptHookArgs) -> None:
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
            None, f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_14(self, args: threading.ExceptHookArgs) -> None:
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
            "UNHANDLED EXCEPTION", None
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_15(self, args: threading.ExceptHookArgs) -> None:
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
            f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_16(self, args: threading.ExceptHookArgs) -> None:
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
            "UNHANDLED EXCEPTION", )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_17(self, args: threading.ExceptHookArgs) -> None:
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
            "XXUNHANDLED EXCEPTIONXX", f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_18(self, args: threading.ExceptHookArgs) -> None:
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
            "unhandled exception", f"UNHANDLED THREAD EXCEPTION{thread_info}"
        )

        # Write to crash log
        self._write_crash_log(crash_info)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_19(self, args: threading.ExceptHookArgs) -> None:
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
        self._write_crash_log(None)

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_20(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                None, self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_21(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", None
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_22(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_23(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_24(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger(None).critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_25(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("XXcrashXX").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_26(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("CRASH").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_27(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "XXUnhandled thread exception - see %sXX", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_28(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_29(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "UNHANDLED THREAD EXCEPTION - SEE %S", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_30(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(None)

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_31(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(None)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_32(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = None
            if thread is None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_33(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None and not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_34(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is not None or not thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_35(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or thread.daemon:
                os._exit(1)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_36(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(None)

    def xǁCrashHandlerǁ_threading_exception_hook__mutmut_37(self, args: threading.ExceptHookArgs) -> None:
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

        # Log via logging (may fail if logging is not configured)
        try:
            logging.getLogger("crash").critical(
                "Unhandled thread exception - see %s", self._crash_log_path
            )
        except Exception as exc:
            sys.__stderr__.write(f"[logger] Could not emit crash log record: {exc}\n")

        # Call original hook if available
        if self._original_threading_excepthook:
            self._original_threading_excepthook(args)

        # Force exit if configured (for systemd restart)
        # Skip for daemon threads — transient errors in background workers
        # (network, D-Bus) should not kill the whole process.
        if self._exit_on_crash:
            thread = args.thread
            if thread is None or not thread.daemon:
                os._exit(2)
    
    xǁCrashHandlerǁ_threading_exception_hook__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCrashHandlerǁ_threading_exception_hook__mutmut_1': xǁCrashHandlerǁ_threading_exception_hook__mutmut_1, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_2': xǁCrashHandlerǁ_threading_exception_hook__mutmut_2, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_3': xǁCrashHandlerǁ_threading_exception_hook__mutmut_3, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_4': xǁCrashHandlerǁ_threading_exception_hook__mutmut_4, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_5': xǁCrashHandlerǁ_threading_exception_hook__mutmut_5, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_6': xǁCrashHandlerǁ_threading_exception_hook__mutmut_6, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_7': xǁCrashHandlerǁ_threading_exception_hook__mutmut_7, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_8': xǁCrashHandlerǁ_threading_exception_hook__mutmut_8, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_9': xǁCrashHandlerǁ_threading_exception_hook__mutmut_9, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_10': xǁCrashHandlerǁ_threading_exception_hook__mutmut_10, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_11': xǁCrashHandlerǁ_threading_exception_hook__mutmut_11, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_12': xǁCrashHandlerǁ_threading_exception_hook__mutmut_12, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_13': xǁCrashHandlerǁ_threading_exception_hook__mutmut_13, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_14': xǁCrashHandlerǁ_threading_exception_hook__mutmut_14, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_15': xǁCrashHandlerǁ_threading_exception_hook__mutmut_15, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_16': xǁCrashHandlerǁ_threading_exception_hook__mutmut_16, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_17': xǁCrashHandlerǁ_threading_exception_hook__mutmut_17, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_18': xǁCrashHandlerǁ_threading_exception_hook__mutmut_18, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_19': xǁCrashHandlerǁ_threading_exception_hook__mutmut_19, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_20': xǁCrashHandlerǁ_threading_exception_hook__mutmut_20, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_21': xǁCrashHandlerǁ_threading_exception_hook__mutmut_21, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_22': xǁCrashHandlerǁ_threading_exception_hook__mutmut_22, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_23': xǁCrashHandlerǁ_threading_exception_hook__mutmut_23, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_24': xǁCrashHandlerǁ_threading_exception_hook__mutmut_24, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_25': xǁCrashHandlerǁ_threading_exception_hook__mutmut_25, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_26': xǁCrashHandlerǁ_threading_exception_hook__mutmut_26, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_27': xǁCrashHandlerǁ_threading_exception_hook__mutmut_27, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_28': xǁCrashHandlerǁ_threading_exception_hook__mutmut_28, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_29': xǁCrashHandlerǁ_threading_exception_hook__mutmut_29, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_30': xǁCrashHandlerǁ_threading_exception_hook__mutmut_30, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_31': xǁCrashHandlerǁ_threading_exception_hook__mutmut_31, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_32': xǁCrashHandlerǁ_threading_exception_hook__mutmut_32, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_33': xǁCrashHandlerǁ_threading_exception_hook__mutmut_33, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_34': xǁCrashHandlerǁ_threading_exception_hook__mutmut_34, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_35': xǁCrashHandlerǁ_threading_exception_hook__mutmut_35, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_36': xǁCrashHandlerǁ_threading_exception_hook__mutmut_36, 
        'xǁCrashHandlerǁ_threading_exception_hook__mutmut_37': xǁCrashHandlerǁ_threading_exception_hook__mutmut_37
    }
    xǁCrashHandlerǁ_threading_exception_hook__mutmut_orig.__name__ = 'xǁCrashHandlerǁ_threading_exception_hook'

    def uninstall(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCrashHandlerǁuninstall__mutmut_orig'), object.__getattribute__(self, 'xǁCrashHandlerǁuninstall__mutmut_mutants'), args, kwargs, self)

    def xǁCrashHandlerǁuninstall__mutmut_orig(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, "excepthook"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_1(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = None

        if self._original_threading_excepthook and hasattr(threading, "excepthook"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_2(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook or hasattr(threading, "excepthook"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_3(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(None, "excepthook"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_4(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, None):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_5(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr("excepthook"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_6(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, ):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_7(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, "XXexcepthookXX"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_8(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, "EXCEPTHOOK"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_9(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, "excepthook"):
            threading.excepthook = None

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_10(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, "excepthook"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = None
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_11(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, "excepthook"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = True
        CrashHandler._instance = None

    def xǁCrashHandlerǁuninstall__mutmut_12(self) -> None:
        """Restore original exception hooks."""
        sys.excepthook = self._original_excepthook

        if self._original_threading_excepthook and hasattr(threading, "excepthook"):
            threading.excepthook = self._original_threading_excepthook

        if self._fault_file:
            try:
                self._fault_file.close()
            except OSError:
                pass  # File already closed; nothing to recover

        CrashHandler._installed = False
        CrashHandler._instance = ""
    
    xǁCrashHandlerǁuninstall__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCrashHandlerǁuninstall__mutmut_1': xǁCrashHandlerǁuninstall__mutmut_1, 
        'xǁCrashHandlerǁuninstall__mutmut_2': xǁCrashHandlerǁuninstall__mutmut_2, 
        'xǁCrashHandlerǁuninstall__mutmut_3': xǁCrashHandlerǁuninstall__mutmut_3, 
        'xǁCrashHandlerǁuninstall__mutmut_4': xǁCrashHandlerǁuninstall__mutmut_4, 
        'xǁCrashHandlerǁuninstall__mutmut_5': xǁCrashHandlerǁuninstall__mutmut_5, 
        'xǁCrashHandlerǁuninstall__mutmut_6': xǁCrashHandlerǁuninstall__mutmut_6, 
        'xǁCrashHandlerǁuninstall__mutmut_7': xǁCrashHandlerǁuninstall__mutmut_7, 
        'xǁCrashHandlerǁuninstall__mutmut_8': xǁCrashHandlerǁuninstall__mutmut_8, 
        'xǁCrashHandlerǁuninstall__mutmut_9': xǁCrashHandlerǁuninstall__mutmut_9, 
        'xǁCrashHandlerǁuninstall__mutmut_10': xǁCrashHandlerǁuninstall__mutmut_10, 
        'xǁCrashHandlerǁuninstall__mutmut_11': xǁCrashHandlerǁuninstall__mutmut_11, 
        'xǁCrashHandlerǁuninstall__mutmut_12': xǁCrashHandlerǁuninstall__mutmut_12
    }
    xǁCrashHandlerǁuninstall__mutmut_orig.__name__ = 'xǁCrashHandlerǁuninstall'


class LogManager:
    """
    Manages application logging.

    Creates async file loggers with queue-based handlers.
    Ensures proper cleanup on application exit.
    """

    _handlers: ClassVar[dict[str, ThreadedFileHandler]] = {}
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
            logging.getLogger(__name__).warning(
                "Root logger already has handlers; skipping LogManager.setup()"
            )
            return

        root.setLevel(level)

        # Create async file handler
        file_handler = ThreadedFileHandler(filename, fmt=fmt)
        cls._handlers["root"] = file_handler

        # Create queue handler that feeds the file handler
        queue_handler = QueueHandler(file_handler.queue, level)
        root.addHandler(queue_handler)

        # Add console handler
        if console_output:
            cls._add_console_handler(root, console_level or level, fmt)

        # Suppress verbose third-party library debug logs
        for noisy in ("urllib3", "websocket", "PIL"):
            logging.getLogger(noisy).setLevel(logging.WARNING)

        # Capture stdout/stderr (after console handler is set up)
        if capture_stdout:
            cls.redirect_stdout()
        if capture_stderr:
            cls.redirect_stderr()

        # Log startup
        logging.getLogger(__name__).info(
            "Logging initialized - crash logs: %s", crash_log_path
        )

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

        file_handler = ThreadedFileHandler(filename, fmt=fmt)
        cls._handlers[name] = file_handler

        # Create queue handler that feeds the file handler
        queue_handler = QueueHandler(file_handler.queue, level)
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
    args = [filename, level, fmt, capture_stdout, capture_stderr, console_output, console_level, enable_crash_handler, crash_log_path, include_locals_in_crash]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_setup_logging__mutmut_orig, x_setup_logging__mutmut_mutants, args, kwargs, None)


def x_setup_logging__mutmut_orig(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_1(
    filename: str = "XXlogs/app.logXX",
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_2(
    filename: str = "LOGS/APP.LOG",
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_3(
    filename: str = "logs/app.log",
    level: int = logging.DEBUG,
    fmt: str = DEFAULT_FORMAT,
    capture_stdout: bool = True,
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_4(
    filename: str = "logs/app.log",
    level: int = logging.DEBUG,
    fmt: str = DEFAULT_FORMAT,
    capture_stdout: bool = False,
    capture_stderr: bool = False,
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_5(
    filename: str = "logs/app.log",
    level: int = logging.DEBUG,
    fmt: str = DEFAULT_FORMAT,
    capture_stdout: bool = False,
    capture_stderr: bool = True,
    console_output: bool = False,
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_6(
    filename: str = "logs/app.log",
    level: int = logging.DEBUG,
    fmt: str = DEFAULT_FORMAT,
    capture_stdout: bool = False,
    capture_stderr: bool = True,
    console_output: bool = True,
    console_level: int | None = None,
    enable_crash_handler: bool = False,
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_7(
    filename: str = "logs/app.log",
    level: int = logging.DEBUG,
    fmt: str = DEFAULT_FORMAT,
    capture_stdout: bool = False,
    capture_stderr: bool = True,
    console_output: bool = True,
    console_level: int | None = None,
    enable_crash_handler: bool = True,
    crash_log_path: str = CRASH_LOG_PATH,
    include_locals_in_crash: bool = False,
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_8(
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
        filename=None,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_9(
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
        filename=filename,
        level=None,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_10(
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
        filename=filename,
        level=level,
        fmt=None,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_11(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=None,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_12(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=None,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_13(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=None,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_14(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=None,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_15(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=None,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_16(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=None,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_17(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=None,
    )


def x_setup_logging__mutmut_18(
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
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_19(
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
        filename=filename,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_20(
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
        filename=filename,
        level=level,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_21(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_22(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_23(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_24(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_25(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        crash_log_path=crash_log_path,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_26(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        include_locals_in_crash=include_locals_in_crash,
    )


def x_setup_logging__mutmut_27(
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
        filename=filename,
        level=level,
        fmt=fmt,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        console_output=console_output,
        console_level=console_level,
        enable_crash_handler=enable_crash_handler,
        crash_log_path=crash_log_path,
        )

x_setup_logging__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_setup_logging__mutmut_1': x_setup_logging__mutmut_1, 
    'x_setup_logging__mutmut_2': x_setup_logging__mutmut_2, 
    'x_setup_logging__mutmut_3': x_setup_logging__mutmut_3, 
    'x_setup_logging__mutmut_4': x_setup_logging__mutmut_4, 
    'x_setup_logging__mutmut_5': x_setup_logging__mutmut_5, 
    'x_setup_logging__mutmut_6': x_setup_logging__mutmut_6, 
    'x_setup_logging__mutmut_7': x_setup_logging__mutmut_7, 
    'x_setup_logging__mutmut_8': x_setup_logging__mutmut_8, 
    'x_setup_logging__mutmut_9': x_setup_logging__mutmut_9, 
    'x_setup_logging__mutmut_10': x_setup_logging__mutmut_10, 
    'x_setup_logging__mutmut_11': x_setup_logging__mutmut_11, 
    'x_setup_logging__mutmut_12': x_setup_logging__mutmut_12, 
    'x_setup_logging__mutmut_13': x_setup_logging__mutmut_13, 
    'x_setup_logging__mutmut_14': x_setup_logging__mutmut_14, 
    'x_setup_logging__mutmut_15': x_setup_logging__mutmut_15, 
    'x_setup_logging__mutmut_16': x_setup_logging__mutmut_16, 
    'x_setup_logging__mutmut_17': x_setup_logging__mutmut_17, 
    'x_setup_logging__mutmut_18': x_setup_logging__mutmut_18, 
    'x_setup_logging__mutmut_19': x_setup_logging__mutmut_19, 
    'x_setup_logging__mutmut_20': x_setup_logging__mutmut_20, 
    'x_setup_logging__mutmut_21': x_setup_logging__mutmut_21, 
    'x_setup_logging__mutmut_22': x_setup_logging__mutmut_22, 
    'x_setup_logging__mutmut_23': x_setup_logging__mutmut_23, 
    'x_setup_logging__mutmut_24': x_setup_logging__mutmut_24, 
    'x_setup_logging__mutmut_25': x_setup_logging__mutmut_25, 
    'x_setup_logging__mutmut_26': x_setup_logging__mutmut_26, 
    'x_setup_logging__mutmut_27': x_setup_logging__mutmut_27
}
x_setup_logging__mutmut_orig.__name__ = 'x_setup_logging'


def get_logger(
    name: str,
    filename: str | None = None,
    level: int = logging.INFO,
    fmt: str = DEFAULT_FORMAT,
) -> logging.Logger:
    args = [name, filename, level, fmt]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_logger__mutmut_orig, x_get_logger__mutmut_mutants, args, kwargs, None)


def x_get_logger__mutmut_orig(
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


def x_get_logger__mutmut_1(
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
    return LogManager.get_logger(None, filename, level, fmt)


def x_get_logger__mutmut_2(
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
    return LogManager.get_logger(name, None, level, fmt)


def x_get_logger__mutmut_3(
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
    return LogManager.get_logger(name, filename, None, fmt)


def x_get_logger__mutmut_4(
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
    return LogManager.get_logger(name, filename, level, None)


def x_get_logger__mutmut_5(
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
    return LogManager.get_logger(filename, level, fmt)


def x_get_logger__mutmut_6(
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
    return LogManager.get_logger(name, level, fmt)


def x_get_logger__mutmut_7(
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
    return LogManager.get_logger(name, filename, fmt)


def x_get_logger__mutmut_8(
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
    return LogManager.get_logger(name, filename, level, )

x_get_logger__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_logger__mutmut_1': x_get_logger__mutmut_1, 
    'x_get_logger__mutmut_2': x_get_logger__mutmut_2, 
    'x_get_logger__mutmut_3': x_get_logger__mutmut_3, 
    'x_get_logger__mutmut_4': x_get_logger__mutmut_4, 
    'x_get_logger__mutmut_5': x_get_logger__mutmut_5, 
    'x_get_logger__mutmut_6': x_get_logger__mutmut_6, 
    'x_get_logger__mutmut_7': x_get_logger__mutmut_7, 
    'x_get_logger__mutmut_8': x_get_logger__mutmut_8
}
x_get_logger__mutmut_orig.__name__ = 'x_get_logger'


def install_crash_handler(
    crash_log_path: str = CRASH_LOG_PATH,
    fault_log_path: str = FAULT_LOG_PATH,
    include_locals: bool = True,
    exit_on_crash: bool = True,
) -> CrashHandler:
    args = [crash_log_path, fault_log_path, include_locals, exit_on_crash]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_install_crash_handler__mutmut_orig, x_install_crash_handler__mutmut_mutants, args, kwargs, None)


def x_install_crash_handler__mutmut_orig(
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


def x_install_crash_handler__mutmut_1(
    crash_log_path: str = CRASH_LOG_PATH,
    fault_log_path: str = FAULT_LOG_PATH,
    include_locals: bool = False,
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


def x_install_crash_handler__mutmut_2(
    crash_log_path: str = CRASH_LOG_PATH,
    fault_log_path: str = FAULT_LOG_PATH,
    include_locals: bool = True,
    exit_on_crash: bool = False,
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


def x_install_crash_handler__mutmut_3(
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
        None, fault_log_path, include_locals, exit_on_crash
    )


def x_install_crash_handler__mutmut_4(
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
        crash_log_path, None, include_locals, exit_on_crash
    )


def x_install_crash_handler__mutmut_5(
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
        crash_log_path, fault_log_path, None, exit_on_crash
    )


def x_install_crash_handler__mutmut_6(
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
        crash_log_path, fault_log_path, include_locals, None
    )


def x_install_crash_handler__mutmut_7(
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
        fault_log_path, include_locals, exit_on_crash
    )


def x_install_crash_handler__mutmut_8(
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
        crash_log_path, include_locals, exit_on_crash
    )


def x_install_crash_handler__mutmut_9(
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
        crash_log_path, fault_log_path, exit_on_crash
    )


def x_install_crash_handler__mutmut_10(
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
        crash_log_path, fault_log_path, include_locals, )

x_install_crash_handler__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_install_crash_handler__mutmut_1': x_install_crash_handler__mutmut_1, 
    'x_install_crash_handler__mutmut_2': x_install_crash_handler__mutmut_2, 
    'x_install_crash_handler__mutmut_3': x_install_crash_handler__mutmut_3, 
    'x_install_crash_handler__mutmut_4': x_install_crash_handler__mutmut_4, 
    'x_install_crash_handler__mutmut_5': x_install_crash_handler__mutmut_5, 
    'x_install_crash_handler__mutmut_6': x_install_crash_handler__mutmut_6, 
    'x_install_crash_handler__mutmut_7': x_install_crash_handler__mutmut_7, 
    'x_install_crash_handler__mutmut_8': x_install_crash_handler__mutmut_8, 
    'x_install_crash_handler__mutmut_9': x_install_crash_handler__mutmut_9, 
    'x_install_crash_handler__mutmut_10': x_install_crash_handler__mutmut_10
}
x_install_crash_handler__mutmut_orig.__name__ = 'x_install_crash_handler'
