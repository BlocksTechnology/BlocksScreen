"""ControlTab Z tilt overlay stays up until the final G28 reply."""

import sys
import types
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

# fresh stubs, not setdefault: patching an already-imported real configfile leaks
for _name in ("configfile", "lib.files", "lib.printer"):
    sys.modules[_name] = types.ModuleType(_name)
sys.modules["configfile"].BlocksScreenConfig = MagicMock
sys.modules["configfile"].get_configparser = MagicMock(return_value=MagicMock())
sys.modules["lib.files"].Files = MagicMock
sys.modules["lib.printer"].Printer = MagicMock

# tests/panels/conftest.py stubs these for the session; evict so the real module loads
sys.modules.pop("lib.panels.controlTab", None)
sys.modules.pop("lib.ui", None)
for _stubbed in [_m for _m in sys.modules if _m.startswith("lib.panels.widgets")]:
    sys.modules.pop(_stubbed, None)

from lib.panels.controlTab import ControlTab  # noqa: E402

_PASS = "// Retries: 0/6 Probed points range: 0.012700 tolerance: 0.050000"


@pytest.fixture
def tab():
    loads: list[tuple[bool, str]] = []
    callbacks: dict[str, object] = {}

    def run_gcode(gcode, callback=None):
        callbacks[gcode] = callback
        return True

    t = SimpleNamespace(
        _ztilt_running=False,
        _ztilt_failed=False,
        ws=SimpleNamespace(api=SimpleNamespace(run_gcode=run_gcode)),
        call_load_panel=SimpleNamespace(emit=lambda s, m, _f: loads.append((s, m))),
        ztilt_result_screen=MagicMock(),
        ztilt_result_screen_timer=MagicMock(),
    )
    for name in ("_on_ztilt_done", "_on_ztilt_homed", "_handle_gcode_response"):
        setattr(t, name, getattr(ControlTab, name).__get__(t))
    ControlTab.handle_ztilt(t)
    return t, loads, callbacks


def test_overlay_stays_until_final_home(tab):
    t, loads, callbacks = tab
    t._handle_gcode_response([_PASS])
    assert loads[-1] == (
        True,
        "Calibrating Z tilt\nDeviation 0.013 mm, target 0.050 mm",
    )

    callbacks["Z_TILT_ADJUST"]("ok")
    assert loads[-1][0] is True
    t.ztilt_result_screen.show.assert_not_called()

    callbacks["G28"]("ok")
    assert loads[-1][0] is False
    t.ztilt_result_screen.set_message.assert_called_once_with(
        "Z tilt calibration complete."
    )


def test_ztilt_error_reported_after_home(tab):
    t, loads, callbacks = tab
    callbacks["Z_TILT_ADJUST"]({"error": {"code": 400, "message": "Too many retries"}})
    assert loads[-1] == (
        True,
        "Z tilt calibration failed\nHoming the printer, please wait",
    )

    callbacks["G28"]("ok")
    assert loads[-1][0] is False
    assert "failed" in t.ztilt_result_screen.set_message.call_args.args[0]
    t._handle_gcode_response([_PASS])
    assert loads[-1][0] is False
