"""Regression test for the SIGTERM restart-splash shutdown path.

Field crash (BLOCKS-RF50, dev @ dc1a67d4): after a successful self-update the
SIGTERM handler ran show_splash() + processEvents() directly on Python's signal
trampoline, re-entering Qt's paint engine mid-paint. This produced
`QBackingStore::endPaint() called with active painter` / recursive-repaint
warnings and then a fatal SEGV, crash-looping the only field-update path.

The fix defers the splash/quit work to the Qt event loop via
QTimer.singleShot(0, ...), so it never runs inline on the signal trampoline.
This test locks in that structural invariant (deterministic, headless).
"""

import importlib.util
import signal
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PyQt6 import QtWidgets

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENTRY = _PROJECT_ROOT / "BlocksScreen" / "BlocksScreen.py"


def _load_entry_module():
    """Load BlocksScreen.py with its heavy UI/deps stubbed out."""
    stubs: dict[str, types.ModuleType] = {}

    def _stub(name: str, **attrs: object) -> types.ModuleType:
        mod = types.ModuleType(name)
        for key, val in attrs.items():
            setattr(mod, key, val)
        stubs[name] = mod
        return mod

    _stub("configfile", get_configparser=MagicMock())

    lib = _stub("lib")
    lib.__path__ = []  # type: ignore[attr-defined]
    panels = _stub("lib.panels")
    panels.__path__ = []  # type: ignore[attr-defined]
    _stub("lib.panels.mainWindow", MainWindow=MagicMock())

    class _CrashHandler:
        _instance = None

        @staticmethod
        def _exception_hook(*_a: object, **_k: object) -> None:
            pass

    _stub(
        "logger",
        CrashHandler=_CrashHandler,
        LogManager=MagicMock(),
        install_crash_handler=lambda *a, **k: None,
        setup_logging=lambda *a, **k: None,
    )

    tools = _stub("tools")
    tools.__path__ = []  # type: ignore[attr-defined]
    _stub("tools.configuration_manager", ConfigManager=MagicMock())

    saved = {k: sys.modules.get(k) for k in stubs}
    sys.modules.update(stubs)
    try:
        spec = importlib.util.spec_from_file_location("_bs_entry_under_test", _ENTRY)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v


@pytest.fixture(scope="module")
def entry_mod():
    return _load_entry_module()


@pytest.fixture
def qapp():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    yield app


def test_sigterm_defers_shutdown_off_signal_trampoline(entry_mod, qapp, monkeypatch):
    show_splash = MagicMock()
    write_fb0 = MagicMock()
    monkeypatch.setattr(entry_mod, "show_splash", show_splash)
    monkeypatch.setattr(entry_mod, "_write_splash_to_fb0", write_fb0)
    monkeypatch.setattr(qapp, "quit", MagicMock())

    original = signal.getsignal(signal.SIGTERM)
    try:
        entry_mod._setup_sigterm(qapp)
        handler = signal.getsignal(signal.SIGTERM)
        assert callable(handler)

        # Simulate SIGTERM delivery on the trampoline.
        handler(signal.SIGTERM, None)

        # Nothing paint-related may run inline: that is what corrupts the
        # backing store mid-paint and SEGVs.
        show_splash.assert_not_called()
        write_fb0.assert_not_called()
        qapp.quit.assert_not_called()

        # Draining the event loop runs the deferred work cleanly.
        QtWidgets.QApplication.processEvents()
        show_splash.assert_called_once()
        write_fb0.assert_called_once()
        qapp.quit.assert_called_once()
    finally:
        signal.signal(signal.SIGTERM, original)
