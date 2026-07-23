"""Unit tests for embedded-thumbnail parsing + off-thread ThumbnailLoader."""

from BlocksScreen.lib.utils.thumbnail_loader import (
    ThumbnailLoader,
    parse_embedded_thumbnail,
)

_PNG_1x1 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4"
    "z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
)


def _header(*blocks) -> bytes:
    """Build a fake gcode header carrying the given (keyword, w, h) thumbnails."""
    parts = []
    for keyword, width, height in blocks:
        sep = "x" if keyword == "thumbnail" else "*"
        parts.append(
            f"; {keyword} begin {width}{sep}{height} 100\n"
            f"; {_PNG_1x1}\n"
            f"; {keyword} end\n"
        )
    return "".join(parts).encode("latin-1")


class TestParse:
    def test_picks_largest_by_area(self):
        png = parse_embedded_thumbnail(
            _header(("thumbnail", 48, 48), ("thumbnail", 300, 300))
        )
        assert png is not None and png[:4] == b"\x89PNG"

    def test_handles_creality_png_variant(self):
        png = parse_embedded_thumbnail(_header(("png", 96, 96)))
        assert png is not None and png[:4] == b"\x89PNG"

    def test_none_when_absent(self):
        assert parse_embedded_thumbnail(b"; not a thumbnail\nG1 X0 Y0\n") is None


class _FakeRest:
    def __init__(self, header):
        self._header = header

    def get_gcode_header(self, rel_path, max_bytes=131072):
        return self._header


class TestLoader:
    def test_emits_ready_with_decoded_image(self, qtbot):
        loader = ThumbnailLoader(_FakeRest(_header(("thumbnail", 300, 300))))
        with qtbot.waitSignal(loader.ready, timeout=2000) as sig:
            loader.request_embedded("USB-X/cube.gcode")
        path, image = sig.args
        assert path == "USB-X/cube.gcode"
        assert image is not None and not image.isNull()
        assert loader.cached("USB-X/cube.gcode") is not None

    def test_no_thumbnail_does_not_emit(self, qtbot):
        loader = ThumbnailLoader(_FakeRest(b"G1 X0 Y0\n"))
        with qtbot.assertNotEmitted(loader.ready, wait=300):
            loader.request_embedded("x.gcode")
