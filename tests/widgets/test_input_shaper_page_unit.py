"""InputShaperPage overlay, watchdog and reply-driven run flow tests."""

import pytest

_RECOMMENDED = "// Recommended shaper_type_{a} = mzv, shaper_freq_{a} = 41.0 Hz"
_FAIL = {"error": {"code": 400, "message": "Invalid adxl345 id"}}
_GONE = {"error": {"code": 503, "message": "Klippy Disconnected"}}
_HOME = "G28\nM400"


@pytest.fixture
def page(qtbot):
    from BlocksScreen.lib.panels.widgets.UtilitiesTab.inputshaperPage import (
        InputShaperPage,
    )

    loads: list[tuple[bool, str]] = []
    fails: list[str] = []
    sent: dict[str, object] = {}

    def runner(gcode, callback=None):
        sent[gcode] = callback
        return True

    p = InputShaperPage(logic=True, gcode_runner=runner)
    qtbot.addWidget(p)
    p.call_load_panel.connect(lambda show, msg, _force: loads.append((show, msg)))
    p.run_finished.connect(fails.append)
    return p, loads, sent, fails


def _start(p, sent, gcode="SHAPER_CALIBRATE"):
    p.handle_is(gcode)
    assert list(sent) == [_HOME]
    sent[_HOME]("ok")
    # Auto runs end in SAVE_CONFIG, whose restart unhomes anyway: no final home.
    final = [] if gcode == "SHAPER_CALIBRATE" else ["G28"]
    assert list(sent) == [_HOME, gcode, *final]


def _sweep_both_axes(p):
    for axis in "xy":
        p.handle_gcode_response([_RECOMMENDED.format(a=axis)])


def test_auto_run_saves_after_sweep(page):
    p, loads, sent, fails = page
    _start(p, sent)
    _sweep_both_axes(p)
    assert "SAVE_CONFIG" not in sent

    sent["SHAPER_CALIBRATE"]("ok")
    assert "G28" not in sent
    assert loads[-1][1].startswith("Saving input shaper settings")
    sent["SAVE_CONFIG"]("ok")
    assert loads[-1][0] is True  # Klipper restarts: the overlay waits for it
    assert not p._run.busy and not p._saving
    assert not p._run._watchdog.isActive()
    assert fails == []

    p.on_klippy_state("startup")
    assert loads[-1][0] is True
    p.on_klippy_state("ready")
    assert loads[-1][0] is False
    count = len(loads)
    p.on_klippy_state("ready")
    assert len(loads) == count  # Only the restart after its own save closes it


def test_failed_first_home_skips_sweep(page):
    p, loads, sent, fails = page
    p.handle_is("SHAPER_CALIBRATE")
    sent[_HOME]({"error": {"code": 400, "message": "Endstop x still triggered"}})
    assert list(sent) == [_HOME]
    assert loads[-1][0] is False
    assert fails == ["Homing failed.\nCheck the printer and try again."]
    assert not p._run.busy


def test_failed_save_reports_and_closes_overlay(page):
    p, loads, sent, fails = page
    _start(p, sent)
    _sweep_both_axes(p)
    sent["SHAPER_CALIBRATE"]("ok")
    # The save must not be timed out while Klipper restarts
    assert p._saving and not p._run._watchdog.isActive()
    sent["SAVE_CONFIG"]({"error": {"code": 400, "message": "conflicts"}})
    assert loads[-1][0] is False
    assert not p._run.busy
    assert fails == [
        "Saving the input shaper result failed.\nCheck the printer config."
    ]


def test_failed_auto_sweep_reported_at_once(page):
    p, loads, sent, fails = page
    _start(p, sent)
    sent["SHAPER_CALIBRATE"](_FAIL)
    assert loads[-1][0] is False
    assert fails == [
        "Input shaper calibration failed.\nCheck the accelerometer and try again."
    ]
    assert "SAVE_CONFIG" not in sent


def test_sweep_without_both_results_does_not_save(page):
    p, loads, sent, fails = page
    _start(p, sent)
    p.handle_gcode_response([_RECOMMENDED.format(a="x")])
    sent["SHAPER_CALIBRATE"]("ok")
    assert loads[-1][0] is False
    assert len(fails) == 1
    assert "SAVE_CONFIG" not in sent


def test_klippy_disconnect_closes_quietly(page):
    p, loads, sent, fails = page
    _start(p, sent)
    _sweep_both_axes(p)
    sent["SHAPER_CALIBRATE"](_GONE)
    assert loads[-1][0] is False
    assert not p._run.busy
    assert "SAVE_CONFIG" not in sent
    assert fails == []


def test_second_start_ignored_while_running(page):
    p, _, sent, _ = page
    p.handle_is("SHAPER_CALIBRATE")
    sent.clear()
    p.handle_is("SHAPER_CALIBRATE AXIS=X")
    p.handle_is("")  # The axis dialog is not opened mid-run either
    assert sent == {}
    assert p.aut


def test_unsent_request_closes_overlay(page):
    p, loads, _, _ = page
    p._run.runner = lambda _gcode, callback=None: False
    p.handle_is("SHAPER_CALIBRATE")
    assert loads[-1][0] is False
    assert not p._run.busy and not p._run._watchdog.isActive()


def test_timeout_blocks_new_run_until_klipper_answers(page, qtbot):
    p, loads, sent, fails = page
    p._run.timeout_ms = 50
    _start(p, sent)
    old = dict(sent)
    qtbot.waitUntil(lambda: loads[-1][0] is False, timeout=2000)
    assert not p._run.active and not p.aut
    assert fails == [
        "Input shaper calibration timed out.\nCheck the printer and try again."
    ]

    # Klipper still runs the old sweep: a re-tap must not queue a second one
    p._run.timeout_ms = 120_000
    sent.clear()
    p.handle_is("SHAPER_CALIBRATE")
    assert sent == {}
    assert "still running" in fails[-1]

    # Its late reply neither saves nor reopens the overlay, and frees the page
    _sweep_both_axes(p)
    old["SHAPER_CALIBRATE"]("ok")
    assert "SAVE_CONFIG" not in sent
    assert loads[-1][0] is False
    _start(p, sent)
    assert p._run.active


def test_single_axis_closes_on_final_home(page):
    p, loads, sent, fails = page
    _start(p, sent, "SHAPER_CALIBRATE AXIS=X")
    sent["SHAPER_CALIBRATE AXIS=X"]("ok")
    assert loads[-1][0] is True
    sent["G28"]("ok")
    assert loads[-1][0] is False
    assert "SAVE_CONFIG" not in sent
    assert fails == []


def test_single_axis_failed_sweep_reported_after_final_home(page):
    p, loads, sent, fails = page
    _start(p, sent, "SHAPER_CALIBRATE AXIS=X")
    sent["SHAPER_CALIBRATE AXIS=X"](_FAIL)
    assert loads[-1] == (
        True,
        "Input shaper calibration failed\nHoming the printer",
    )
    # A "!!" from the final home does not end the run early
    p.handle_gcode_response(["!! Probe triggered prior to movement"])
    assert loads[-1][0] is True and fails == []
    sent["G28"]("ok")
    assert loads[-1][0] is False
    assert fails == [
        "Input shaper calibration failed.\nCheck the accelerometer and try again."
    ]


def test_single_axis_final_home_failure_is_reported(page):
    p, loads, sent, fails = page
    _start(p, sent, "SHAPER_CALIBRATE AXIS=X")
    sent["SHAPER_CALIBRATE AXIS=X"]("ok")
    sent["G28"]({"error": {"code": 400, "message": "Endstop x still triggered"}})
    assert loads[-1][0] is False
    assert fails == [
        "Homing failed after input shaper calibration.\n"
        "Home the printer before printing."
    ]


def test_progress_lines_restart_the_watchdog(page, qtbot):
    p, loads, sent, _ = page
    p._run.timeout_ms = 300
    _start(p, sent)
    for _ in range(5):
        qtbot.wait(100)
        p.handle_gcode_response(["// Testing frequency 20 Hz"])

    assert loads[-1][0] is True
    qtbot.waitUntil(lambda: loads[-1][0] is False, timeout=2000)


def test_unrelated_output_does_not_feed_the_watchdog(page, qtbot):
    p, loads, sent, _ = page
    p._run.timeout_ms = 300
    _start(p, sent)
    for _ in range(5):
        qtbot.wait(100)
        p.handle_gcode_response(["// MMU: gate 0 idle"])
    assert loads[-1][0] is False
    assert not p._run.active


def test_sweep_progress_reaches_overlay(page):
    p, loads, sent, _ = page
    _start(p, sent)
    p.handle_gcode_response(["// Testing axis x"])
    p.handle_gcode_response(["// Testing frequency 62 Hz"])
    assert loads[-1] == (True, "Measuring Resonances\nX axis: 62 Hz")
    p.handle_gcode_response(
        ["// Calculating the best input shaper parameters for y axis"]
    )
    assert loads[-1][1] == "Calculating the best input shaper\nY axis"
    sent["SHAPER_CALIBRATE"](_FAIL)

    # Single-axis runs print no "Testing axis" line, so the axis comes from AXIS=
    sent.clear()
    _start(p, sent, "SHAPER_CALIBRATE AXIS=Y")
    p.handle_gcode_response(["// Testing frequency 40 Hz"])
    assert loads[-1][1] == "Measuring Resonances\nY axis: 40 Hz"


def test_klipper_busy_blocks_new_run(page):
    # After a websocket drop the replies are gone but Klipper may still sweep
    p, _loads, sent, fails = page
    p._run.klippy_busy = lambda: True
    p.handle_is("SHAPER_CALIBRATE")
    assert sent == {}
    assert "still running" in fails[-1]
    p._run.klippy_busy = lambda: False
    _start(p, sent)


def _saved(p, sent, reply="ok"):
    _start(p, sent)
    _sweep_both_axes(p)
    sent["SHAPER_CALIBRATE"]("ok")
    sent["SAVE_CONFIG"](reply)


@pytest.mark.parametrize(
    ("reply", "state", "expected"),
    [
        ("ok", "ready", "Input shaper settings saved."),
        (_GONE, "ready", "Input shaper settings saved."),
        ({"error": {"code": -1, "message": "closed"}}, "ready", "connection dropped"),
        ("ok", "error", "did not restart cleanly"),
        ("ok", "shutdown", "did not restart cleanly"),
    ],
)
def test_save_restart_reports_once_klipper_is_back(page, reply, state, expected):
    # Moonraker fails SAVE_CONFIG with 503 when the restart drops Klippy: that is success
    p, loads, sent, fails = page
    _saved(p, sent, reply)
    assert loads[-1][0] is True and fails == []
    p.on_klippy_state("startup")
    assert fails == []
    p.on_klippy_state(state)
    assert loads[-1] == (False, "")
    assert len(fails) == 1 and expected in fails[0]
    p.on_klippy_state("ready")
    assert len(fails) == 1


def test_new_run_clears_previous_results(page):
    p, _loads, sent, _ = page
    _start(p, sent)
    _sweep_both_axes(p)
    assert p.is_types
    sent["SHAPER_CALIBRATE"](_FAIL)
    sent.clear()
    _start(p, sent)
    assert p.is_types == {} and p.type_dict == {}


def test_manual_apply_goes_through_the_runner(page, monkeypatch):
    # The list page needs the real icon widgets, which the test stubs replace
    p, loads, sent, _ = page
    monkeypatch.setattr(p, "logic", False)
    monkeypatch.setattr(p, "reset_view_model", lambda: None)
    monkeypatch.setattr(p, "setCurrentIndex", lambda _i: None)
    monkeypatch.setattr(p, "is_page", None, raising=False)
    p.type_dict = {"Axis": "x", "mzv": {"frequency": 41.0}}
    p.currentItem = type("Item", (), {"text": "mzv"})()
    p.handle_ism_confirm()
    script = "SET_INPUT_SHAPER SHAPER_TYPE_X=mzv SHAPER_FREQ_X=41.0"
    assert list(sent) == [script]
    assert loads[-1] == (True, "Applying input shaper")
    sent[script]("ok")
    assert "SAVE_CONFIG" in sent
