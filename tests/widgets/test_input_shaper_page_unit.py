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


def test_progress_lines_restart_the_watchdog(page, qtbot):
    p, loads, _ = page
    p._is_watchdog.setInterval(300)
    p.handle_is("SHAPER_CALIBRATE")
    for _ in range(5):
        qtbot.wait(100)
        p.handle_gcode_response(["// Testing frequency 20 Hz"])

    assert loads[-1][0] is True
    qtbot.waitUntil(lambda: loads[-1][0] is False, timeout=2000)
