"""Dev-only paint counter, replaces GammaRay which cannot attach to the PyQt6 wheel Qt"""

import logging
import os
import time
from collections import Counter

from PyQt6 import QtCore

logger = logging.getLogger(__name__)

_ENV_FLAG = "BS_PAINT_PROBE"
_ENV_INTERVAL = "BS_PAINT_PROBE_INTERVAL_MS"
_ENV_TOP = "BS_PAINT_PROBE_TOP"
_TRUTHY = frozenset({"1", "true", "True", "yes", "on"})


class PaintProbe(QtCore.QObject):
    """Counts paint events per widget, answers how often each widget repaints"""

    def __init__(
        self,
        app: QtCore.QCoreApplication,
        interval_ms: int = 5000,
        top: int = 20,
    ) -> None:
        super().__init__(app)
        self._counts: Counter[str] = Counter()
        self._top = top
        self._window_start = time.monotonic()
        app.installEventFilter(self)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._dump)
        self._timer.start(interval_ms)

    def eventFilter(self, a0: QtCore.QObject | None, a1: QtCore.QEvent | None) -> bool:
        """Re-implemented method, tally paints without consuming the event"""
        if a0 is not None and a1 is not None:
            if a1.type() == QtCore.QEvent.Type.Paint:
                # Key by name not id, ids get reused after a popup is destroyed
                self._counts[f"{type(a0).__name__}#{a0.objectName() or '-'}"] += 1
        return False

    def _dump(self) -> None:
        """Log the busiest painters for the elapsed window, then reset"""
        now = time.monotonic()
        elapsed = now - self._window_start
        self._window_start = now
        if not self._counts or elapsed <= 0:
            logger.info("paint probe: no paints in %.1fs", elapsed)
            return

        total = sum(self._counts.values())
        logger.info(
            "paint probe: %d paints in %.1fs (%.1f/s) across %d widgets",
            total,
            elapsed,
            total / elapsed,
            len(self._counts),
        )
        for name, count in self._counts.most_common(self._top):
            logger.info("  %7.1f/s  %6d  %s", count / elapsed, count, name)
        self._counts.clear()

    def stop(self) -> None:
        """Detach the filter, the probe adds a sip crossing per event while active"""
        self._timer.stop()
        app = self.parent()
        if app is not None:
            app.removeEventFilter(self)


def install(app: QtCore.QCoreApplication) -> PaintProbe | None:
    """Install the probe when BS_PAINT_PROBE is set, otherwise a no-op returning None"""
    if os.environ.get(_ENV_FLAG, "") not in _TRUTHY:
        return None
    interval_ms = int(os.environ.get(_ENV_INTERVAL, "5000"))
    top = int(os.environ.get(_ENV_TOP, "20"))
    logger.info("paint probe active, dumping top %d every %dms", top, interval_ms)
    return PaintProbe(app, interval_ms=interval_ms, top=top)
