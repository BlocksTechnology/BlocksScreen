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

from lib.panels.controlTab import _ZTILT_TEXT, ControlTab  # noqa: E402
from lib.utils.moonraker_reply import (  # noqa: E402
    FIRST_HOME_TIMEOUT_MS,
    GcodeRun,
    HomedCalibration,
)

_PASS = "// Retries: 0/6 Probed points range: 0.012700 tolerance: 0.050000"
_LEGACY_OVERRIDE = "SET_KINEMATIC_POSITION Z=0\nG0 Z10\nM84 Z\nG28 Y\nG28 X"


def _make_tab(override: str = "", unsent: tuple[str, ...] = ()):
    loads: list[tuple[bool, str]] = []
    callbacks: dict[str, object] = {}

    def run_gcode(gcode, callback=None):
        if gcode in unsent:
            return False
        callbacks[gcode] = callback
        return True

    run = HomedCalibration(_ZTILT_TEXT, 180_000, runner=run_gcode)
    t = SimpleNamespace(
        _ztilt=run,
        hides=[],
        printer=SimpleNamespace(
            get_config=lambda _s: {"gcode": override} if override else {}
        ),
        ztilt_result_screen=MagicMock(),
        ztilt_result_screen_timer=MagicMock(),
    )

    def on_overlay(show, msg, force):
        loads.append((show, msg))
        t.hides.append((show, force))

    for name in (
        "_home_keeps_tilt",
        "_ztilt_report",
        "_on_ztilt_finished",
        "_handle_gcode_response",
    ):
        setattr(t, name, getattr(ControlTab, name).__get__(t))
    # PyQt cannot weakref a SimpleNamespace-bound method
    run.overlay.connect(on_overlay)
    run.finished.connect(lambda ok, msg: t._on_ztilt_finished(ok, msg))
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
    t._ztilt.timeout_ms = 50
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


def test_klippy_ready_forgets_replies_a_restart_lost(tab):
    t, _loads, callbacks = tab
    _home(callbacks)
    t._ztilt.stop()
    assert t._ztilt.busy
    t.printcores_page, t.disable_popups = MagicMock(), MagicMock()
    ControlTab.on_klippy_status(t, "ready")
    assert not t._ztilt.busy


def test_forgotten_reply_does_not_clear_a_newer_send(qtbot):
    sent: dict[str, object] = {}

    def runner(script, callback=None):
        sent[script] = callback
        return True

    run = GcodeRun(1000)
    run.runner = runner
    run.send("A", lambda _r: None)
    run.forget_replies()
    run.send("B", lambda _r: None)
    sent["A"]("ok")
    assert run.busy
    sent["B"]("ok")
    assert not run.busy


def test_finished_run_forces_the_overlay_closed(tab):
    t, _loads, callbacks = tab
    _home(callbacks)
    callbacks["Z_TILT_ADJUST"]("ok")
    callbacks["G28 Z"]("ok")
    assert t.hides[-1] == (False, True)


def test_failure_and_timeout_close_forced(tab, qtbot):
    t, _loads, callbacks = tab
    callbacks["G28\nM400"]({"error": {"code": 400, "message": "Endstop x still"}})
    assert t.hides[-1] == (False, True)
    ControlTab.handle_ztilt(t)
    callbacks["G28\nM400"]("ok")
    t._ztilt.timeout_ms = 50
    t._ztilt.feed()
    qtbot.waitUntil(lambda: t.hides[-1][0] is False, timeout=2000)
    assert t.hides[-1] == (False, True)


def test_disconnect_close_stays_unforced(tab):
    # Forcing it would also hide MainWindow's Klipper restart overlay
    t, _loads, callbacks = tab
    callbacks["G28\nM400"]({"error": {"code": 503, "message": "Klippy Disconnected"}})
    assert t.hides[-1] == (False, False)


def test_first_home_gets_the_long_timeout(tab):
    # The first G28 from the top runs BEACON_AUTO_CALIBRATE at 3 mm/s
    t, _loads, callbacks = tab
    assert t._ztilt._watchdog.interval() == FIRST_HOME_TIMEOUT_MS
    callbacks["G28\nM400"]("ok")
    assert t._ztilt._watchdog.interval() == 180_000


def test_unsent_final_home_waits_for_the_tilt(qtbot):
    t, loads, callbacks = _make_tab(unsent=("G28 Z",))
    callbacks["G28\nM400"]("ok")
    assert "Z_TILT_ADJUST" in callbacks and "G28 Z" not in callbacks
    assert loads[-1][0] is True  # The gantry is still probing
    callbacks["Z_TILT_ADJUST"]("ok")
    assert loads[-1][0] is False
    assert "not re-homed" in t.ztilt_result_screen.set_message.call_args.args[0]


def test_lost_link_blocks_retap_while_klipper_busy(tab):
    t, _loads, callbacks = tab
    klipper = {"busy": True}
    t._ztilt.klippy_busy = lambda: klipper["busy"]
    _home(callbacks)
    gone = {"error": {"code": -1, "message": "disconnected"}}
    callbacks["Z_TILT_ADJUST"](gone)
    callbacks["G28 Z"](gone)
    callbacks.clear()

    ControlTab.handle_ztilt(t)
    assert callbacks == {}
    assert "still running" in t.ztilt_result_screen.set_message.call_args.args[0]

    klipper["busy"] = False
    ControlTab.handle_ztilt(t)
    assert list(callbacks) == ["G28\nM400"]
