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

    p = AxisMaintPage(None, run_gcode)
    qtbot.addWidget(p)
    p.am_x.setChecked(True)
    p.answerPage.show = MagicMock()
    p.calls = calls
    return p


def test_oil_prompt_waits_for_homing_reply(page):
    page.axis_maintenance()

    script, callback = page.calls[0]
    assert script.startswith("AXIS_MAINTENANCE_x")
    page.answerPage.show.assert_not_called()

    callback("ok")
    page.answerPage.show.assert_called_once()


def test_homing_error_skips_oil_prompt(page, qtbot):
    page.axis_maintenance()
    with qtbot.waitSignal(page.call_load_panel) as blocker:
        page.calls[0][1]({"error": {"code": 400, "message": "Endstop x"}})

    assert blocker.args == [False, "", False]
    page.answerPage.show.assert_not_called()


def test_offline_send_drops_loading_without_prompt(page, qtbot):
    page._run_gcode = lambda script, callback=None: False
    with qtbot.waitSignals([page.call_load_panel, page.call_load_panel]):
        page.axis_maintenance()

    page.answerPage.show.assert_not_called()
