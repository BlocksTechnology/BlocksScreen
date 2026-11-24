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


class TestPrinterBusy:
    def test_tracks_klipper_idle_timeout_state(self, printer) -> None:
        # Klipper sends "Printing" capitalised while any gcode runs
        printer._idle_timeout_object_updated({"state": "Printing"})
        assert printer.printer_busy
        printer._idle_timeout_object_updated({"state": "Ready"})
        assert not printer.printer_busy

    def test_not_stuck_busy_after_a_print(self, printer) -> None:
        # Ready can arrive before print_stats leaves "printing"; busy must not latch
        printer._print_stats_object_updated({"state": "printing"})
        printer._idle_timeout_object_updated({"state": "Ready"})
        assert printer.printer_busy
        printer._print_stats_object_updated({"state": "complete"})
        assert not printer.printer_busy

    def test_paused_print_counts_as_busy(self, printer) -> None:
        # Homing for a calibration during a pause would ruin the print
        printer._idle_timeout_object_updated({"state": "Ready"})
        printer._print_stats_object_updated({"state": "paused"})
        assert printer.printer_busy


class TestDisplayMessage:
    @staticmethod
    def _shown(printer) -> list:
        shown: list = []
        printer.display_update[str, str].connect(lambda _n, v: shown.append(v))
        return shown

    def test_subscribe_snapshot_is_not_shown(self, printer) -> None:
        # Klipper keeps the last M117 (RESUME's) until replaced; a restart re-reads it
        shown = self._shown(printer)
        printer._display_status_object_updated({"message": "Print Resumed"})
        assert shown == []

    def test_new_message_after_snapshot_is_shown(self, printer) -> None:
        shown = self._shown(printer)
        printer._display_status_object_updated({"message": None})
        printer._display_status_object_updated({"message": "Priming"})
        assert shown == ["Priming"]

    def test_same_snapshot_after_reconnect_is_not_shown(self, printer) -> None:
        shown = self._shown(printer)
        printer._display_status_object_updated({"message": "Print Resumed"})
        printer._display_status_object_updated({"message": "Print Resumed"})
        assert shown == []

    def test_klippy_restart_rearms_the_snapshot(self, printer) -> None:
        shown = self._shown(printer)
        printer._display_status_object_updated({"message": ""})
        printer.on_klippy_status("startup")
        printer._display_status_object_updated({"message": "Print Resumed"})
        assert shown == []
