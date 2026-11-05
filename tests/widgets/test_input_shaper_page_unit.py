"""InputShaperPage overlay, watchdog and reply-driven run flow tests."""

import pytest

_RECOMMENDED = "// Recommended shaper_type_{a} = mzv, shaper_freq_{a} = 41.0 Hz"
_FAIL = {"error": {"code": 400, "message": "Invalid adxl345 id"}}
_GONE = {"error": {"code": 503, "message": "Klippy Disconnected"}}


@pytest.fixture
def page(qtbot):
    from BlocksScreen.lib.panels.widgets.UtilitiesTab.inputshaperPage import (
        InputShaperPage,
    )

    p = InputShaperPage(logic=True)
    qtbot.addWidget(p)
    loads: list[tuple[bool, str]] = []
    sent: dict[str, object] = {}

    def runner(gcode, callback=None):
        sent[gcode] = callback
        return True

    p.gcode_runner = runner
    p.call_load_panel.connect(lambda show, msg, _force: loads.append((show, msg)))
    return p, loads, sent


def _sweep_both_axes(p):
    for axis in "xy":
        p.handle_gcode_response([_RECOMMENDED.format(a=axis)])


def test_auto_run_saves_after_final_home(page):
    p, loads, sent = page
    p.handle_is("SHAPER_CALIBRATE")
    assert list(sent) == ["G28\nM400", "SHAPER_CALIBRATE", "G28"]
    _sweep_both_axes(p)
    assert "SAVE_CONFIG" not in sent

    sent["SHAPER_CALIBRATE"]("ok")
    assert loads[-1] == (True, "Resonances measured\nHoming the printer, please wait")
    # A "!!" from the final home is not a failed save
    p.handle_gcode_response(["!! Probe triggered prior to movement"])
    assert loads[-1][0] is True

    sent["G28"]("ok")
    assert loads[-1][1].startswith("Saving input shaper settings")
    sent["SAVE_CONFIG"]("ok")
    assert loads[-1][0] is True  # Klipper restarts; ConnectionPage takes over
    assert not p._running and not p._saving
    assert not p._is_watchdog.isActive()


def test_failed_save_closes_overlay(page):
    p, loads, sent = page
    p.handle_is("SHAPER_CALIBRATE")
    _sweep_both_axes(p)
    sent["SHAPER_CALIBRATE"]("ok")
    sent["G28"]("ok")
    sent["SAVE_CONFIG"]({"error": {"code": 400, "message": "conflicts"}})
    assert loads[-1][0] is False
    assert not p._running


def test_failed_sweep_closes_overlay_after_final_home(page):
    p, loads, sent = page
    p.handle_is("SHAPER_CALIBRATE")
    sent["SHAPER_CALIBRATE"](_FAIL)
    assert loads[-1] == (
        True,
        "Input shaper calibration failed\nHoming the printer, please wait",
    )
    sent["G28"]("ok")
    assert loads[-1][0] is False
    assert "SAVE_CONFIG" not in sent


def test_sweep_without_both_results_does_not_save(page):
    p, loads, sent = page
    p.handle_is("SHAPER_CALIBRATE")
    p.handle_gcode_response([_RECOMMENDED.format(a="x")])
    sent["SHAPER_CALIBRATE"]("ok")
    sent["G28"]("ok")
    assert loads[-1][0] is False
    assert "SAVE_CONFIG" not in sent


def test_klippy_disconnect_closes_quietly(page):
    p, loads, sent = page
    p.handle_is("SHAPER_CALIBRATE")
    _sweep_both_axes(p)
    sent["SHAPER_CALIBRATE"](_GONE)
    assert loads[-1][0] is False
    assert not p._running
    # The final home's late reply belongs to a finished run
    sent["G28"](_GONE)
    assert "SAVE_CONFIG" not in sent


def test_second_start_ignored_while_running(page):
    p, _, sent = page
    p.handle_is("SHAPER_CALIBRATE")
    first = sent["SHAPER_CALIBRATE"]
    sent.clear()
    p.handle_is("SHAPER_CALIBRATE AXIS=X")
    assert sent == {}
    assert p.aut
    first("ok")


def test_unsent_request_closes_overlay(page):
    p, loads, _ = page
    p.gcode_runner = lambda _gcode, _callback=None: False
    p.handle_is("SHAPER_CALIBRATE")
    assert loads[-1][0] is False
    assert not p._running and not p._is_watchdog.isActive()


def test_watchdog_timeout_drops_late_replies(page, qtbot):
    p, loads, sent = page
    p._is_watchdog.setInterval(50)
    p.handle_is("SHAPER_CALIBRATE")
    qtbot.waitUntil(lambda: loads[-1][0] is False, timeout=2000)
    assert not p._running and not p.aut

    _sweep_both_axes(p)
    sent["SHAPER_CALIBRATE"]("ok")
    sent["G28"]("ok")
    assert loads[-1][0] is False
    assert "SAVE_CONFIG" not in sent


def test_single_axis_closes_on_final_home(page):
    p, loads, sent = page
    p.handle_is("SHAPER_CALIBRATE AXIS=X")
    sent["SHAPER_CALIBRATE AXIS=X"]("ok")
    assert loads[-1][0] is True
    sent["G28"]("ok")
    assert loads[-1][0] is False
    assert "SAVE_CONFIG" not in sent


def test_progress_lines_restart_the_watchdog(page, qtbot):
    p, loads, _ = page
    p._is_watchdog.setInterval(300)
    p.handle_is("SHAPER_CALIBRATE")
    for _ in range(5):
        qtbot.wait(100)
        p.handle_gcode_response(["// Testing frequency 20 Hz"])

    assert loads[-1][0] is True
    qtbot.waitUntil(lambda: loads[-1][0] is False, timeout=2000)


def test_sweep_progress_reaches_overlay(page):
    p, loads, sent = page
    p.handle_is("SHAPER_CALIBRATE")
    p.handle_gcode_response(["// Testing axis x"])
    p.handle_gcode_response(["// Testing frequency 62 Hz"])
    assert loads[-1] == (True, "Measuring resonances\nX axis: 62 Hz")
    p.handle_gcode_response(
        ["// Calculating the best input shaper parameters for y axis"]
    )
    assert loads[-1][1] == "Calculating the best input shaper\nY axis"
    sent["SHAPER_CALIBRATE"](_FAIL)
    sent["G28"]("ok")

    # Single-axis runs print no "Testing axis" line, so the axis comes from AXIS=
    p.handle_is("SHAPER_CALIBRATE AXIS=Y")
    p.handle_gcode_response(["// Testing frequency 40 Hz"])
    assert loads[-1][1] == "Measuring resonances\nY axis: 40 Hz"
