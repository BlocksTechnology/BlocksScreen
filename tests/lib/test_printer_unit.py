"""Unit test for Printer typed signals"""

from unittest.mock import MagicMock

import pytest

from BlocksScreen.lib.printer import Printer


@pytest.fixture
def printer(qapp):
    ws = MagicMock()
    return Printer(None, ws)


class TestObjectUpdatedSignal:
    def test_emitted_on_mmu_update(self, printer, qtbot) -> None:
        with qtbot.waitSignal(printer.object_updated) as blocker:
            printer._check_callback("mmu", {"enabled": True})
        assert blocker.args == ["mmu", "", {"enabled": True}]

    def test_emitted_on_pre_gate_update(self, printer, qtbot) -> None:
        with qtbot.waitSignal(printer.object_updated) as blocker:
            printer._check_callback(
                "filament_switch_sensor Mmu Pre Gate 0", {"filament_detected": True}
            )
        assert blocker.args == [
            "filament_switch_sensor",
            "Mmu Pre Gate 0",
            {"filament_detected": True},
        ]

    def test_emitted_for_any_object(self, printer, qtbot) -> None:
        with qtbot.waitSignal(printer.object_updated) as blocker:
            printer._check_callback("extruder", {"temperature": 200.0})
        assert blocker.args[0] == "extruder"


class TestKlippyStateChangedSignal:
    def test_emitted_on_ready(self, printer, qtbot) -> None:
        with qtbot.waitSignal(printer.klippy_state_changed) as blocker:
            printer.on_klippy_status("ready")
        assert blocker.args[0] == "ready"

    def test_emitted_on_disconnect(self, printer, qtbot) -> None:
        with qtbot.waitSignal(printer.klippy_state_changed) as blocker:
            printer.on_klippy_status("disconnect")
        assert blocker.args[0] == "disconnect"

    def test_emitted_on_error(self, printer, qtbot) -> None:
        with qtbot.waitSignal(printer.klippy_state_changed) as blocker:
            printer.on_klippy_status("error")
        assert blocker.args[0] == "error"
