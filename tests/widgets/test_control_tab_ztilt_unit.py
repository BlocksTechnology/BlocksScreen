"""ControlTab Z-Tilt overlay stays up until the final G28 reply."""

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
        _ztilt_run_id=0,
        ws=SimpleNamespace(api=SimpleNamespace(run_gcode=run_gcode)),
        call_load_panel=SimpleNamespace(emit=lambda s, m, _f: loads.append((s, m))),
        ztilt_result_screen=MagicMock(),
        ztilt_result_screen_timer=MagicMock(),
    )
    for name in (
        "_ztilt_stop",
        "_ztilt_send",
        "_ztilt_current",
        "_on_ztilt_first_home",
        "_on_ztilt_done",
        "_on_ztilt_homed",
        "_handle_gcode_response",
    ):
        setattr(t, name, getattr(ControlTab, name).__get__(t))
    ControlTab.handle_ztilt(t)
    assert list(callbacks) == ["G28\nM400"]
    return t, loads, callbacks


def _home(callbacks):
    callbacks["G28\nM400"]("ok")
    assert list(callbacks) == ["G28\nM400", "Z_TILT_ADJUST", "G28 Z"]


def test_overlay_stays_until_final_home(tab):
    t, loads, callbacks = tab
    _home(callbacks)
    t._handle_gcode_response([_PASS])
    assert loads[-1] == (
        True,
        "Calibrating Z-Tilt\nDeviation 0.013 mm, target 0.050 mm",
    )

    callbacks["Z_TILT_ADJUST"]("ok")
    assert loads[-1][0] is True
    t.ztilt_result_screen.show.assert_not_called()

    callbacks["G28 Z"]("ok")
    assert loads[-1][0] is False
    t.ztilt_result_screen.set_message.assert_called_once_with(
        "Z-Tilt calibration complete."
    )


def test_ztilt_error_reported_after_home(tab):
    t, loads, callbacks = tab
    _home(callbacks)
    callbacks["Z_TILT_ADJUST"]({"error": {"code": 400, "message": "Too many retries"}})
    assert loads[-1] == (
        True,
        "Z-Tilt calibration failed\nHoming the printer, please wait",
    )

    callbacks["G28 Z"]("ok")
    assert loads[-1][0] is False
    assert "failed" in t.ztilt_result_screen.set_message.call_args.args[0]
    t._handle_gcode_response([_PASS])
    assert loads[-1][0] is False


def test_second_tap_ignored_while_running(tab):
    t, _, callbacks = tab
    callbacks.clear()
    ControlTab.handle_ztilt(t)
    assert callbacks == {}
    assert t._ztilt_running


def test_first_home_failure_skips_ztilt(tab):
    t, loads, callbacks = tab
    callbacks["G28\nM400"]({"error": {"code": 400, "message": "Endstop x still"}})
    assert "Z_TILT_ADJUST" not in callbacks
    assert loads[-1][0] is False
    assert not t._ztilt_running
    t.ztilt_result_screen.set_message.assert_called_once_with(
        "Homing failed.\nCheck the printer and try again."
    )


def test_klippy_disconnect_closes_quietly(tab):
    t, loads, callbacks = tab
    _home(callbacks)
    gone = {"error": {"code": 503, "message": "Klippy Disconnected"}}
    callbacks["Z_TILT_ADJUST"](gone)
    assert loads[-1][0] is False
    assert not t._ztilt_running
    callbacks["G28 Z"](gone)
    t.ztilt_result_screen.show.assert_not_called()


def test_late_reply_from_ended_run_does_not_end_new_run(tab):
    # A 503 ends run 1 while its G28 Z reply is still in flight; a re-tap starts run 2.
    t, loads, callbacks = tab
    _home(callbacks)
    gone = {"error": {"code": 503, "message": "Klippy Disconnected"}}
    callbacks["Z_TILT_ADJUST"](gone)
    stale_home = callbacks["G28 Z"]
    callbacks.clear()
    ControlTab.handle_ztilt(t)
    stale_home(gone)
    assert t._ztilt_running
    assert loads[-1] == (True, "Calibrating Z-Tilt\nPlease wait")
