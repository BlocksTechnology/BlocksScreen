from __future__ import annotations
import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
import contextvars
from queue import SimpleQueue
from typing import Optional, Dict, Any

_correlation_id = contextvars.ContextVar("correlation_id", default=None)

def set_correlation_id(corr_id: Optional[str]) -> None:
    _correlation_id.set(corr_id)

def get_correlation_id() -> Optional[str]:
    return _correlation_id.get()

class JsonFormatter(logging.Formatter):
    def __init__(self, static_fields: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.static_fields = static_fields or {}

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "level": record.levelname.lower(),
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.thread,
        }
        if self.static_fields:
            payload.update(self.static_fields)
        corr = getattr(record, "correlation_id", None)
        if corr:
            payload["correlation_id"] = corr
        for k, v in record.__dict__.items():
            if k in payload or k.startswith("_"):
                continue
            if k in ("args","msg","exc_info","exc_text","stack_info","msecs",
                     "relativeCreated","levelno","pathname","filename",
                     "threadName","processName","created","name","lineno",
                     "funcName","module"):
                continue
            if isinstance(v, (str, int, float, bool)) or v is None:
                payload[k] = v
            else:
                try:
                    json.dumps(v); payload[k] = v
                except Exception:
                    payload[k] = repr(v)
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack_info"] = self.formatStack(record.stack_info)
        return json.dumps(payload, ensure_ascii=False)

class HumanFormatter(logging.Formatter):
    def __init__(self, show_logger=True):
        fmt = "%(levelname)s - "
        fmt += "%(name)s - " if show_logger else ""
        fmt += "%(message)s"
        super().__init__(fmt)

class CorrelationAdapter(logging.LoggerAdapter):
    def __init__(self, logger: logging.Logger, static_fields: Optional[Dict[str, Any]] = None):
        super().__init__(logger, extra=static_fields or {})

    def process(self, msg, kwargs):
        extra = dict(kwargs.get("extra", {}))
        if "correlation_id" not in extra:
            corr = get_correlation_id()
            if corr:
                extra["correlation_id"] = corr
        for k, v in self.extra.items():
            extra.setdefault(k, v)
        kwargs["extra"] = extra
        return msg, kwargs

def get_logger(
    name: str = "BlocksLogger",
    *,
    env: str = "dev",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    rotate_max_bytes: int = 2_000_000,
    rotate_backups: int = 3,
    json_console: bool = False,
    service: Optional[str] = None,
) -> logging.LoggerAdapter:

    eff_level = level.upper() if level else ("DEBUG" if env == "dev" else "INFO")
    lvl = getattr(logging, eff_level, logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(lvl)
    logger.propagate = False
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formatters
    human_fmt = HumanFormatter(show_logger=True)
    json_fmt = JsonFormatter(static_fields={"service": service or name, "env": env})

    # Handlers reais
    handlers = []

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(lvl)
    console_handler.setFormatter(json_fmt if json_console else human_fmt)
    handlers.append(console_handler)

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=rotate_max_bytes, backupCount=rotate_backups, encoding="utf-8"
        )
        file_handler.setLevel(lvl)
        file_handler.setFormatter(json_fmt)
        handlers.append(file_handler)



    log_queue = SimpleQueue()
    queue_handler = QueueHandler(log_queue)
    queue_handler.setLevel(lvl)
    logger.addHandler(queue_handler)

    listener = QueueListener(log_queue, *handlers, respect_handler_level=True)
    listener.start()

    return CorrelationAdapter(logger, static_fields={"service": service or name, "env": env})

__all__ = [
    "get_logger", "set_correlation_id", "get_correlation_id",
    "JsonFormatter", "HumanFormatter", "CorrelationAdapter",