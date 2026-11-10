"""MoonRest gcode Range fetches."""

from unittest.mock import patch

import requests

from BlocksScreen.lib.moonrest import MoonRest


class _Resp:
    """Streaming response stub usable as a context manager."""

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
    """A real MoonRest; construction opens no connection."""
    return MoonRest(host="h", port=7125)


def test_returns_capped_bytes_and_closes():
    resp = _Resp([b"AB", b"CD", b"EF"])
    with patch("BlocksScreen.lib.moonrest.requests.get", return_value=resp):
        out = MoonRest.get_gcode_header(_stub(), "USB/c.gcode", max_bytes=4)
    assert out == b"ABCD"
    assert resp.closed


def test_oversized_chunk_is_trimmed_to_cap():
    """A server ignoring Range still yields at most max_bytes."""
    resp = _Resp([b"ABCDEF"])
    with patch("BlocksScreen.lib.moonrest.requests.get", return_value=resp):
        assert MoonRest.get_gcode_header(_stub(), "c.gcode", max_bytes=4) == b"ABCD"


def test_returns_none_on_http_error():
    resp = _Resp([b"X"], error=requests.HTTPError("404"))
    with patch("BlocksScreen.lib.moonrest.requests.get", return_value=resp):
        assert MoonRest.get_gcode_header(_stub(), "c.gcode") is None
    assert resp.closed


def test_quotes_subdir_path():
    resp = _Resp([b"data"])
    with patch("BlocksScreen.lib.moonrest.requests.get", return_value=resp) as get:
        MoonRest.get_gcode_header(_stub(), "USB-X/my part.gcode", max_bytes=4)
    url = get.call_args.args[0]
    assert "USB-X/my%20part.gcode" in url  # spaces quoted, slash preserved


def test_tail_returns_small_whole_file():
    """Moonraker 200s the whole file when it fits the range."""
    resp = _Resp([b"AB", b"CD"])
    with patch("BlocksScreen.lib.moonrest.requests.get", return_value=resp) as get:
        out = MoonRest.get_gcode_tail(_stub(), "c.gcode", max_bytes=4)
    assert out == b"ABCD"
    assert get.call_args.kwargs["headers"]["Range"] == "bytes=-4"
    assert resp.closed


def test_tail_gives_up_when_range_ignored():
    """Past max_bytes means Range was ignored; stop reading."""
    chunks = iter([b"AB", b"CD", b"EF", b"GH"])
    resp = _Resp(chunks)
    with patch("BlocksScreen.lib.moonrest.requests.get", return_value=resp):
        assert MoonRest.get_gcode_tail(_stub(), "c.gcode", max_bytes=4) is None
    assert next(chunks) == b"GH"  # the rest of the body was never pulled
    assert resp.closed
