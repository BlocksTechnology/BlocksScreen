"""Unit tests for the screensaver timeout floor and fallback."""

import importlib
import pathlib
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

_BLOCKSSCREEN = pathlib.Path(__file__).parent.parent.parent / "BlocksScreen"
if str(_BLOCKSSCREEN) not in sys.path:
    sys.path.append(str(_BLOCKSSCREEN))

# drop tests/network's configfile mock
sys.modules.pop("configfile", None)

from configfile import BlocksScreenConfig  # noqa: E402


@pytest.fixture
def make_saver(qapp, tmp_path, monkeypatch):
    # tests/panels stubs "screensaver"; import the real one for this test only
    monkeypatch.delitem(sys.modules, "screensaver", raising=False)
    screensaver = importlib.import_module("screensaver")
    monkeypatch.setattr(screensaver.ScreenSaver, "_dpms_available", False)
    # keep the shared class-level QTimer from being started
    monkeypatch.setattr(screensaver.ScreenSaver, "timer", MagicMock())

    def make(timeout):
        path = tmp_path / "BlocksScreen.cfg"
        path.write_text(
            f"[server]\nhost: localhost\n\n[screensaver]\ntimeout: {timeout}\n"
        )
        cfg = BlocksScreenConfig(path, "server")
        cfg.load_config()
        saver = screensaver.ScreenSaver(SimpleNamespace(config=cfg))
        qapp.removeEventFilter(saver)
        return saver

    return make


@pytest.mark.parametrize(
    ("timeout", "expected"),
    [("0", 60_000), ("5000", 60_000), ("300000", 300_000), ("abc", 500_000)],
)
def test_blank_timeout(make_saver, timeout, expected):
    assert make_saver(timeout).blank_timeout == expected
