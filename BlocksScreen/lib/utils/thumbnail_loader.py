"""Off-thread embedded-gcode thumbnail fallback (Range-request, base64-decoded, cached)."""

from __future__ import annotations

import base64
import binascii
import logging
import re
from collections import OrderedDict

from PyQt6 import QtCore, QtGui

logger = logging.getLogger(__name__)

# Matches PrusaSlicer/Cura "thumbnail begin" and the Creality "png begin" variant.
_THUMBNAIL_RE = re.compile(
    r"; (?:thumbnail|png) begin (\d+)[x*](\d+) \d+\s*\n(.*?); (?:thumbnail|png) end",
    re.DOTALL,
)


def parse_embedded_thumbnail(header: bytes) -> bytes | None:
    """Return PNG bytes of the largest thumbnail embedded in a gcode header."""
    text = header.decode("latin-1", errors="ignore")
    best_area = -1
    best_block = None
    for width, height, block in _THUMBNAIL_RE.findall(text):
        area = int(width) * int(height)
        if area > best_area:
            best_area, best_block = area, block
    if best_block is None:
        return None
    b64 = "".join(line.strip().lstrip(";").strip() for line in best_block.splitlines())
    try:
        return base64.b64decode(b64)
    except (ValueError, binascii.Error):
        return None


class _TaskSignals(QtCore.QObject):
    """Carries a worker result back to the UI thread (QRunnable can't hold signals)."""

    result = QtCore.pyqtSignal(str, object)  # (gcode_path, QImage | None)


class _EmbeddedThumbnailTask(QtCore.QRunnable):
    """Fetches + parses one gcode's embedded thumbnail off the UI thread."""

    def __init__(self, rest, gcode_path: str, signals: _TaskSignals) -> None:
        super().__init__()
        self._rest = rest
        self._gcode_path = gcode_path
        self._signals = signals

    @QtCore.pyqtSlot()
    def run(self) -> None:
        """Decode to QImage in the worker; the slot converts to pixmap on the UI thread."""
        image = None
        header = self._rest.get_gcode_header(self._gcode_path)
        if header:
            png = parse_embedded_thumbnail(header)
            if png:
                candidate = QtGui.QImage()
                if candidate.loadFromData(png, "PNG") and not candidate.isNull():
                    image = candidate
        self._signals.result.emit(self._gcode_path, image)


class ThumbnailLoader(QtCore.QObject):
    """Serves embedded gcode thumbnails via a capped thread pool + bounded LRU cache."""

    ready = QtCore.pyqtSignal(str, object)  # (gcode_path, QImage)

    _CACHE_MAX = 32

    def __init__(self, rest, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._rest = rest
        self._pool = QtCore.QThreadPool(self)
        self._pool.setMaxThreadCount(2)  # bound concurrent decodes on the 2GB Pi
        self._cache: OrderedDict[str, QtGui.QImage] = OrderedDict()
        self._inflight: set[str] = set()
        self._signals = _TaskSignals()
        self._signals.result.connect(self._on_result)

    def cached(self, gcode_path: str) -> QtGui.QImage | None:
        """Return an already-fetched thumbnail (promoted to MRU), or None."""
        image = self._cache.get(gcode_path)
        if image is not None:
            self._cache.move_to_end(gcode_path)
        return image

    def request_embedded(self, gcode_path: str) -> None:
        """Fetch a gcode's embedded thumbnail off-thread; emits ready() when available."""
        cached = self.cached(gcode_path)
        if cached is not None:
            self.ready.emit(gcode_path, cached)
            return
        if not gcode_path or self._rest is None or gcode_path in self._inflight:
            return
        self._inflight.add(gcode_path)
        self._pool.start(_EmbeddedThumbnailTask(self._rest, gcode_path, self._signals))

    def _on_result(self, gcode_path: str, image: object) -> None:
        """Cache the decoded image (LRU-bounded) and notify listeners."""
        self._inflight.discard(gcode_path)
        if image is None:
            return
        if len(self._cache) >= self._CACHE_MAX:
            self._cache.popitem(last=False)
        self._cache[gcode_path] = image
        self.ready.emit(gcode_path, image)


_loader: ThumbnailLoader | None = None


def configure(rest) -> ThumbnailLoader:
    """Create the shared loader from a MoonRest client (call once at startup)."""
    global _loader
    _loader = ThumbnailLoader(rest)
    return _loader


def get_loader() -> ThumbnailLoader | None:
    """Return the shared loader, or None if not configured yet."""
    return _loader


def cached_pixmap(gcode_path: str) -> QtGui.QPixmap | None:
    """Cached embedded thumbnail as a main-thread QPixmap; queues a fetch on miss."""
    loader = _loader
    gcode_path = gcode_path.removeprefix("/")
    if loader is None or not gcode_path:
        return None
    image = loader.cached(gcode_path)
    if image is None:
        loader.request_embedded(gcode_path)
        return None
    return QtGui.QPixmap.fromImage(image) if not image.isNull() else None
