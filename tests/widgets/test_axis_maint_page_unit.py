"""Unit tests for AxisMaintPage: the oil prompt waits for the homing macro to finish."""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def page(qtbot):
    from BlocksScreen.lib.panels.widgets.UtilitiesTab.axisMaintPage import (
        AxisMaintPage,
    )

    calls: list = []

    def run_gcode(script, callback=None):
        calls.append((script, callback))
        return True

    p = AxisMaintPage(None, gcode_runner=run_gcode)
    qtbot.addWidget(p)
    p.show()
    p.am_x.setChecked(True)
    p.answerPage.show = MagicMock()
    p.error_popup.show = MagicMock()
    p.calls = calls
    return p


def test_oil_prompt_waits_for_homing_reply(page, qtbot):
    with qtbot.waitSignal(page.call_load_panel) as shown:
        page.axis_maintenance()
    assert shown.args == [True, "Homing X axis...", False]

    script, callback = page.calls[0]
    assert script.startswith("AXIS_MAINTENANCE_x")
    page.answerPage.show.assert_not_called()

    with qtbot.waitSignal(page.call_load_panel) as hidden:
        callback("ok")
    assert hidden.args == [False, "", False]
    page.answerPage.show.assert_called_once()


def test_cycle_shows_and_drops_its_overlay(page, qtbot):
    page.current_object = "x"
    with qtbot.waitSignal(page.call_load_panel) as shown:
        page._run_AXIS_MAINTENANCE_gcode()
    assert shown.args == [True, "Running maintenance cycle on X axis...", False]
    assert page.calls[0][0].startswith("AXIS_MAINTENANCE_FINISH_x")
    assert page._safety.interval() == 600_000

    with qtbot.waitSignal(page.call_load_panel) as hidden:
        page.calls[0][1]("ok")
    assert hidden.args == [False, "", False]


def test_homing_step_has_its_own_shorter_timeout(page):
    page.axis_maintenance()
    assert page._safety.interval() == 300_000


def test_homing_error_skips_oil_prompt(page, qtbot):
    page.axis_maintenance()
    with qtbot.waitSignal(page.call_load_panel) as blocker:
        page.calls[0][1]({"error": {"code": 400, "message": "Endstop x"}})

    assert blocker.args == [False, "", False]
    page.answerPage.show.assert_not_called()
    page.error_popup.show.assert_not_called()  # Klipper's "!!" popup covers it


def test_moonraker_level_error_gets_a_popup(page):
    page.axis_maintenance()
    page.calls[0][1]({"error": {"code": -32602, "message": "Invalid params"}})

    page.error_popup.show.assert_called_once()
    page.answerPage.show.assert_not_called()


def test_offline_send_drops_loading_without_prompt(page, qtbot):
    page.gcode_runner = lambda script, callback=None: False
    with qtbot.waitSignals([page.call_load_panel, page.call_load_panel]):
        page.axis_maintenance()

    page.answerPage.show.assert_not_called()


def test_no_runner_drops_loading_without_prompt(page, qtbot):
    page.gcode_runner = None
    with qtbot.waitSignals([page.call_load_panel, page.call_load_panel]):
        page.axis_maintenance()

    page.answerPage.show.assert_not_called()


def test_safety_timeout_frees_execute_and_ignores_late_reply(page, qtbot):
    page.axis_maintenance()
    page._safety.start(20)
    with qtbot.waitSignal(page.call_load_panel, timeout=2000) as blocker:
        pass
    assert blocker.args == [False, "", False]
    assert page.am_execute.isEnabled()

    # A late reply must not hide an overlay another flow may own by now.
    with qtbot.assertNotEmitted(page.call_load_panel, wait=50):
        page.calls[0][1]("ok")
    page.answerPage.show.assert_not_called()


def test_execute_disabled_until_reply(page):
    page.axis_maintenance()
    assert not page.am_execute.isEnabled()

    page.calls[0][1]("ok")
    assert page.am_execute.isEnabled()


def test_hidden_page_skips_oil_prompt_and_leaves_overlay(page, qtbot):
    page.axis_maintenance()
    page.hide()

    with qtbot.assertNotEmitted(page.call_load_panel, wait=50):
        page.calls[0][1]("ok")
    page.answerPage.show.assert_not_called()


def test_hidden_page_timeout_leaves_overlay(page, qtbot):
    page.axis_maintenance()
    page._safety.start(20)
    page.hide()
    with qtbot.assertNotEmitted(page.call_load_panel, wait=200):
        pass
