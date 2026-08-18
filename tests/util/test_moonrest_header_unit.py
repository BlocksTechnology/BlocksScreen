"""Unit tests for MoonRest.get_gcode_header (range fetch + connection release)."""

from types import SimpleNamespace
from unittest.mock import patch

from BlocksScreen.lib.moonrest import MoonRest


class _Resp:
    """Minimal streaming-response stub supporting the context-manager protocol."""

    def __init__(self, chunks, error=None):
        self._chunks = chunks
        self._error = error
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.closed = True

    def raise_for_status(self):
        if self._error:
            raise self._error

    def iter_content(self, chunk_size=65536):
        yield from self._chunks


def _stub():
    """A MoonRest-shaped object exposing just what get_gcode_header reads."""
    return SimpleNamespace(build_endpoint="http://h:7125", _api_key=None, timeout=5)


def test_returns_capped_bytes_and_closes():
    resp = _Resp([b"AB", b"CD", b"EF"])
    with patch("BlocksScreen.lib.moonrest.requests.get", return_value=resp):
        out = MoonRest.get_gcode_header(_stub(), "USB/c.gcode", max_bytes=4)
    assert out == b"ABCD"
    assert resp.closed  # connection released via the context manager


def test_returns_none_on_http_error():
    resp = _Resp([b"X"], error=RuntimeError("404"))
    with patch("BlocksScreen.lib.moonrest.requests.get", return_value=resp):
        assert MoonRest.get_gcode_header(_stub(), "c.gcode") is None
    assert resp.closed


def test_quotes_subdir_path():
    resp = _Resp([b"data"])
    with patch("BlocksScreen.lib.moonrest.requests.get", return_value=resp) as get:
        MoonRest.get_gcode_header(_stub(), "USB-X/my part.gcode", max_bytes=4)
    url = get.call_args.args[0]
    assert "USB-X/my%20part.gcode" in url  # spaces quoted, slash preserved
