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
from lib.utils.moonraker_reply import GcodeRun  # noqa: E402

_PASS = "// Retries: 0/6 Probed points range: 0.012700 tolerance: 0.050000"
_LEGACY_OVERRIDE = "SET_KINEMATIC_POSITION Z=0\nG0 Z10\nM84 Z\nG28 Y\nG28 X"


def _make_tab(override: str = ""):
    loads: list[tuple[bool, str]] = []
    callbacks: dict[str, object] = {}

    def run_gcode(gcode, callback=None):
        callbacks[gcode] = callback
        return True

    run = GcodeRun(180_000)
    run.runner = run_gcode
    t = SimpleNamespace(
        _ztilt=run,
        _ztilt_failed=False,
        _ztilt_rehome=True,
        printer=SimpleNamespace(
            get_config=lambda _s: {"gcode": override} if override else {}
        ),
        call_load_panel=SimpleNamespace(emit=lambda s, m, _f: loads.append((s, m))),
        ztilt_result_screen=MagicMock(),
        ztilt_result_screen_timer=MagicMock(),
    )
    for name in (
        "_home_keeps_tilt",
        "_ztilt_report",
        "_ztilt_stop",
        "_ztilt_finish",
        "_on_ztilt_timeout",
        "_on_ztilt_first_home",
        "_on_ztilt_done",
        "_on_ztilt_homed",
        "_handle_gcode_response",
    ):
        setattr(t, name, getattr(ControlTab, name).__get__(t))
    # PyQt cannot weakref a SimpleNamespace-bound method
    run.timed_out.connect(lambda: t._on_ztilt_timeout())
    ControlTab.handle_ztilt(t)
    assert list(callbacks) == ["G28\nM400"]
    return t, loads, callbacks


@pytest.fixture
def tab(qtbot):
    return _make_tab()


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
    assert loads[-1] == (True, "Z-Tilt calibration failed\nHoming Z axis")

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
    assert t._ztilt.active
    t.ztilt_result_screen.show.assert_not_called()


def test_first_home_failure_skips_ztilt(tab):
    t, loads, callbacks = tab
    callbacks["G28\nM400"]({"error": {"code": 400, "message": "Endstop x still"}})
    assert "Z_TILT_ADJUST" not in callbacks
    assert loads[-1][0] is False
    assert not t._ztilt.busy
    t.ztilt_result_screen.set_message.assert_called_once_with(
        "Homing failed.\nCheck the printer and try again."
    )


def test_klippy_disconnect_closes_quietly(tab):
    t, loads, callbacks = tab
    _home(callbacks)
    gone = {"error": {"code": 503, "message": "Klippy Disconnected"}}
    callbacks["Z_TILT_ADJUST"](gone)
    assert loads[-1][0] is False
    assert not t._ztilt.active
    callbacks["G28 Z"](gone)
    assert not t._ztilt.busy
    t.ztilt_result_screen.show.assert_not_called()


def test_stale_reply_does_not_reach_new_run(tab):
    # Moonraker fails every pending request on a disconnect; only then may run 2 start
    t, loads, callbacks = tab
    _home(callbacks)
    gone = {"error": {"code": 503, "message": "Klippy Disconnected"}}
    callbacks["Z_TILT_ADJUST"](gone)
    stale_home = callbacks["G28 Z"]
    callbacks.clear()
    ControlTab.handle_ztilt(t)
    assert callbacks == {}
    stale_home(gone)
    t.ztilt_result_screen.show.assert_called_once()  # Only the still-running notice
    ControlTab.handle_ztilt(t)
    assert t._ztilt.active
    assert loads[-1] == (True, "Calibrating Z-Tilt\nHoming the printer")


def test_timeout_blocks_new_run_until_klipper_answers(tab, qtbot):
    t, loads, callbacks = tab
    _home(callbacks)
    t._ztilt._watchdog.setInterval(50)
    t._handle_gcode_response([_PASS])
    qtbot.waitUntil(lambda: loads[-1][0] is False, timeout=2000)
    t.ztilt_result_screen.set_message.assert_called_once_with(
        "Z-Tilt calibration timed out.\nCheck the printer and try again."
    )

    # Klipper still runs the old tilt: a re-tap must not queue a second one
    pending = dict(callbacks)
    callbacks.clear()
    ControlTab.handle_ztilt(t)
    assert callbacks == {}
    assert "still running" in t.ztilt_result_screen.set_message.call_args.args[0]

    pending["Z_TILT_ADJUST"]("ok")
    pending["G28 Z"]("ok")
    assert loads[-1][0] is False  # Late replies do not reopen the overlay
    ControlTab.handle_ztilt(t)
    assert list(callbacks) == ["G28\nM400"]


def test_legacy_override_skips_final_home(qtbot):
    # Its M84 would disable the Z motors and undo the tilt
    t, loads, callbacks = _make_tab(_LEGACY_OVERRIDE)
    callbacks["G28\nM400"]("ok")
    assert list(callbacks) == ["G28\nM400", "Z_TILT_ADJUST"]
    callbacks["Z_TILT_ADJUST"]("ok")
    assert loads[-1][0] is False
    assert not t._ztilt.busy
    t.ztilt_result_screen.set_message.assert_called_once_with(
        "Z-Tilt calibration complete."
    )
