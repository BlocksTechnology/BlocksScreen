"""InputShaperPage overlay and watchdog tests."""

import pytest

_RECOMMENDED = "// Recommended shaper_type_{a} = mzv, shaper_freq_{a} = 41.0 Hz"


@pytest.fixture
def page(qtbot):
    from BlocksScreen.lib.panels.widgets.UtilitiesTab.inputshaperPage import (
        InputShaperPage,
    )

    p = InputShaperPage(logic=True)
    qtbot.addWidget(p)
    loads: list[tuple[bool, str]] = []
    gcodes: list[str] = []
    p.call_load_panel.connect(lambda show, msg, _force: loads.append((show, msg)))
    p.run_gcode_signal.connect(gcodes.append)
    return p, loads, gcodes


def test_auto_run_keeps_overlay_until_klipper_restarts(page):
    p, loads, gcodes = page
    p.handle_is("SHAPER_CALIBRATE")
    for axis in "xy":
        p.handle_gcode_response([_RECOMMENDED.format(a=axis)])

    assert gcodes[-1] == "SAVE_CONFIG"
    assert loads[-1][0] is True
    assert p._is_watchdog.isActive()

    p.handle_gcode_response(["// Klipper state: Disconnect"])
    assert not p._is_watchdog.isActive()
    assert loads[-1][0] is True
    assert not p.aut


def test_failed_save_closes_overlay(page):
    p, loads, _ = page
    p.handle_is("SHAPER_CALIBRATE")
    p.handle_gcode_response(["!! Probing within a faulty area"])
    assert loads[-1][0] is True
    for axis in "xy":
        p.handle_gcode_response([_RECOMMENDED.format(a=axis)])

    p.handle_gcode_response(
        ["!! SAVE_CONFIG section 'heater_bed' option 'control' conflicts"]
    )
    assert loads[-1][0] is False
    assert not p._is_watchdog.isActive()


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
    p, loads, _ = page
    p.handle_is("SHAPER_CALIBRATE")
    p.handle_gcode_response(["// Testing axis x"])
    p.handle_gcode_response(["// Testing frequency 62 Hz"])
    assert loads[-1] == (True, "Measuring resonances\nX axis: 62 Hz")
    p.handle_gcode_response(
        ["// Calculating the best input shaper parameters for y axis"]
    )
    assert loads[-1][1] == "Calculating the best input shaper\nY axis"

    # Single-axis runs print no "Testing axis" line, so the axis comes from AXIS=
    p.handle_is("SHAPER_CALIBRATE AXIS=Y")
    p.handle_gcode_response(["// Testing frequency 40 Hz"])
    assert loads[-1][1] == "Measuring resonances\nY axis: 40 Hz"


def test_failed_sweep_closes_overlay_after_final_home(page):
    p, loads, _ = page
    sent: list[tuple[str, object]] = []
    p.run_gcode_callback.connect(lambda gcode, cb: sent.append((gcode, cb)))
    p.handle_is("SHAPER_CALIBRATE")
    assert [g for g, _ in sent] == ["SHAPER_CALIBRATE", "G28"]

    sent[0][1]({"error": {"code": 400, "message": "Invalid adxl345 id"}})
    assert not p._is_watchdog.isActive()
    assert loads[-1] == (
        True,
        "Input shaper calibration failed\nHoming the printer, please wait",
    )
    sent[1][1]({"result": "ok"})
    assert loads[-1][0] is False

    # A successful sweep leaves the overlay to the SAVE_CONFIG restart
    sent.clear()
    p.handle_is("SHAPER_CALIBRATE")
    sent[0][1]({"result": "ok"})
    sent[1][1]({"result": "ok"})
    assert loads[-1][0] is True
