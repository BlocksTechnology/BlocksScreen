"""Unit tests for JobStatusWidget (JobStatusWidget.py)"""

import sys
import types
from unittest.mock import MagicMock

import pytest
from PyQt6 import QtGui, QtWidgets


# STUBS must be in sys.modules BEFORE jobStatusPage is imported so the widget
# uses lightweight stand-ins instead of the full custom classes.
def _make_stub(base):
    """Return a minimal subclass of *base* usable in place of a custom widget."""

    class Stub(base):
        secondary_text: str = ""

        def __init__(self, *args, **kwargs):
            kwargs.pop("floating", None)
            super().__init__(*args, **kwargs)

        def set_inner_pixmap(self, *a):
            pass

        def set_message(self, *a):
            pass

        def setPixmap(self, *a):
            pass

        def set_progress(self, *a):  # real CustomProgressBar takes a 0-1 float
            pass

    return Stub


_blocks_button = types.ModuleType("lib.utils.blocks_button")
_blocks_label = types.ModuleType("lib.utils.blocks_label")
_display_button = types.ModuleType("lib.utils.display_button")
_progress_bar = types.ModuleType("lib.utils.blocks_progressbar")
_base_popup = types.ModuleType("lib.panels.widgets.Common.basePopup")

_blocks_button.BlocksCustomButton = _make_stub(QtWidgets.QPushButton)
_blocks_label.BlocksLabel = _make_stub(QtWidgets.QLabel)
_display_button.DisplayButton = _make_stub(QtWidgets.QPushButton)
_progress_bar.CustomProgressBar = _make_stub(QtWidgets.QProgressBar)
_base_popup.BasePopup = _make_stub(QtWidgets.QDialog)

for _name, _mod in [
    ("lib.utils.blocks_button", _blocks_button),
    ("lib.utils.blocks_label", _blocks_label),
    ("lib.utils.display_button", _display_button),
    ("lib.utils.blocks_progressbar", _progress_bar),
    ("lib.panels.widgets.Common.basePopup", _base_popup),
]:
    sys.modules[_name] = _mod  # force-set so network conftest stubs don't win

import events  # noqa: F401, E402  # ensure events is importable before jobStatusPage loads
from lib.panels.widgets.PrintTab.jobStatusPage import JobStatusWidget  # noqa: E402


@pytest.fixture()
def widget(qtbot):
    """Create a JobStatusWidget with all state initialised."""
    w = JobStatusWidget(parent=None)
    # initialise state that slots depend on
    w._current_file_name = ""
    w._print_duration = 0.0
    w._internal_print_status = ""
    w.file_metadata = None
    w.total_layers = "?"
    qtbot.addWidget(w)
    return w


class TestOnPrintStart:
    """on_print_start sets state and emits signals"""

    def test_sets_current_file_name(self, widget):
        widget.on_print_start("test.gcode")
        assert widget._current_file_name == "test.gcode"

    def test_resets_print_duration(self, widget):
        widget._print_duration = 99.9
        widget.on_print_start("test.gcode")
        assert widget._print_duration == 0.0

    def test_emits_print_start_signal(self, widget, qtbot):
        with qtbot.waitSignal(widget.print_start, timeout=500) as sig:
            widget.on_print_start("my_file.gcode")
        assert sig.args == ["my_file.gcode"]


class TestHandlePrintState:
    """_handle_print_state drives the UI and signals correctly."""

    def test_printing_emits_show_request(self, widget, qtbot):
        with qtbot.waitSignal(widget.show_request, timeout=500):
            widget._handle_print_state("printing")

    # def test_paused_emits_show_request(self, widget, qtbot):
    #    with qtbot.waitSignal(widget.show_request, timeout=500):
    #        widget._handle_print_state("paused")

    def test_complete_emits_print_finish(self, widget, qtbot):
        with qtbot.waitSignal(widget.print_finish, timeout=500):
            widget._handle_print_state("complete")

    def test_complete_emits_hide_request(self, widget, qtbot):
        with qtbot.waitSignal(widget.hide_request, timeout=500):
            widget._handle_print_state("complete")

    def test_canceller_does_not_emit_print_finish(self, widget, qtbot):
        with qtbot.assertNotEmitted(widget.print_finish):
            widget._handle_print_state("cancelled")

    def test_invalid_state_clears_metadata(self, widget):
        widget.file_metadata = {"layer_height": 0.2}
        widget._handle_print_state("complete")
        assert widget.file_metadata is None

    def test_invalid_state_clears_filename(self, widget):
        widget._current_file_name = "print.gcode"
        widget._handle_print_state("error")
        assert widget._current_file_name == ""

    @pytest.mark.parametrize("state", ["error", "complete"])
    def test_finished_print_opens_cancel_page(self, widget, qtbot, state):
        widget._internal_print_status = "printing"
        with qtbot.waitSignal(widget.call_cancel_panel, timeout=500) as sig:
            widget._handle_print_state(state)
        assert sig.args == [True]

    def test_finish_screen_states_match_panels_stub(self):
        # tests/panels/conftest.py stubs this constant; keep both in step.
        assert JobStatusWidget.FINISH_SCREEN_STATES == {"complete", "error"}

    def test_cancelled_does_not_open_cancel_page(self, widget, qtbot):
        widget._internal_print_status = "printing"
        with qtbot.assertNotEmitted(widget.call_cancel_panel):
            widget._handle_print_state("cancelled")

    @pytest.mark.parametrize("state", ["error", "complete"])
    def test_stale_end_when_idle_does_not_open_cancel_page(self, widget, qtbot, state):
        widget._internal_print_status = ""
        with qtbot.assertNotEmitted(widget.call_cancel_panel):
            widget._handle_print_state(state)


class TestOnPrintStatsUpdate:
    """on_print_stats_update routes fields to the right state."""

    def test_state_field_triggers_handle_print_state(self, widget, qtbot):
        with qtbot.waitSignal(widget.show_request, timeout=500):
            widget.on_print_stats_update("state", "printing")

    def test_filename_field_updates_current_file(self, widget):
        widget.on_print_stats_update("filename", "cube.gcode")
        assert widget._current_file_name == "cube.gcode"

    def test_print_duration_stored_regardless_of_visibility(self, widget):
        widget.hide()
        widget.on_print_stats_update("print_duration", 42.5)
        assert widget._print_duration == 42.5

    def test_reported_current_layer_wins(self, widget):
        widget.on_print_stats_update("info", {"current_layer": 5})
        assert widget._reported_layer == 5
        assert widget.layer_display_button.text() == "5"

    def test_current_layer_none_keeps_estimate_active(self, widget):
        widget.on_print_stats_update("info", {"current_layer": None})
        assert widget._reported_layer is None

    def test_total_layer_value_stored(self, widget):
        widget.on_print_stats_update("info", {"total_layer": 120})
        assert widget.total_layers == 120


class TestOnGcodeMoveUpdate:
    """on_gcode_move_update computes layer from Z, gated on filament advancing."""

    def _ready_widget(self, widget):
        """Put widget in the state where gcode_move_update should fire."""
        widget.show()
        widget._internal_print_status = "printing"
        widget._print_duration = 10.0
        widget._first_layer_reached = True  # past the start purge
        widget.layer_display_button.setText("sentinel")
        widget.file_metadata = {
            "object_height": 10.0,
            "layer_height": 0.2,
            "first_layer_height": 0.2,
        }

    def _feed(self, widget, z, filament_used):
        """Report a Z move then filament progress, as the printer would."""
        widget.on_gcode_move_update("gcode_position", [0, 0, z, 0])
        widget.on_print_stats_update("filament_used", float(filament_used))

    def test_calculates_layer_from_z(self, widget):
        self._ready_widget(widget)
        self._feed(widget, 0.4, 1)  # z=0.4 -> layer 2
        assert widget.layer_display_button.text() == "2"

    def test_updates_when_hidden(self, widget):
        self._ready_widget(widget)
        widget.hide()
        self._feed(widget, 0.4, 1)
        assert widget.layer_display_button.text() == "2"

    def test_no_update_wrong_field(self, widget):
        self._ready_widget(widget)
        widget._filament_used = 1
        widget.on_gcode_move_update("position", [0, 0, 1.0, 0])
        assert widget.layer_display_button.text() == "sentinel"

    def test_no_update_when_not_printing(self, widget):
        self._ready_widget(widget)
        widget._internal_print_status = "paused"
        self._feed(widget, 1.0, 1)
        assert widget.layer_display_button.text() == "sentinel"

    def test_no_update_when_duration_zero(self, widget):
        self._ready_widget(widget)
        widget._print_duration = 0.0
        self._feed(widget, 1.0, 1)
        assert widget.layer_display_button.text() == "sentinel"

    def test_bedmesh_ignored(self, widget):
        """Bed mesh probing lifts Z but extrudes nothing (filament_used=0): stay at 0."""
        self._ready_widget(widget)
        widget.on_gcode_move_update("gcode_position", [0, 0, 15.0, 0])  # probe height
        widget.on_print_stats_update("filament_used", 0.0)
        assert widget.layer_display_button.text() == "sentinel"

    def test_park_zlift_ignored(self, widget):
        """Z-lift with no filament advance (Happy Hare pause park) must not bump the layer."""
        self._ready_widget(widget)
        self._feed(widget, 0.8, 1)  # layer 4
        assert widget.layer_display_button.text() == "4"
        widget.on_gcode_move_update(
            "gcode_position", [0, 0, 15.0, 0]
        )  # park, no extrusion
        assert widget.layer_display_button.text() == "4"

    def test_layer_tracks_extruding_z(self, widget):
        """Layer follows Z on extruding moves; may regress on a Z drop (Mainsail)."""
        self._ready_widget(widget)
        self._feed(widget, 0.8, 1)  # layer 4
        assert widget.layer_display_button.text() == "4"
        self._feed(widget, 0.4, 2)  # layer 2
        assert widget.layer_display_button.text() == "2"

    def test_reported_total_layer_not_overridden_by_estimate(self, widget):
        """Klipper-reported total_layer wins over the geometry estimate."""
        self._ready_widget(widget)
        widget.on_print_stats_update("info", {"total_layer": 999})
        assert widget.total_layer_reported is True
        self._feed(widget, 0.4, 1)
        assert widget.layer_display_button.secondary_text == "999"

    def test_reconnect_midprint_shows_current_and_total(self, widget):
        """Restart mid-print: filament already used + late metadata must fill both fields."""
        widget.show()
        widget._internal_print_status = "printing"
        widget.on_print_stats_update("print_duration", 500.0)
        widget.on_print_stats_update("filament_used", 1234.0)  # already printing
        widget.on_gcode_move_update(
            "gcode_position", [0, 0, 0.8, 0]
        )  # z=0.8 -> layer 4
        widget.on_fileinfo(
            {"object_height": 10.0, "layer_height": 0.2, "first_layer_height": 0.2}
        )
        # the start hold waits one file line, then the next extrusion paints the layer
        widget.virtual_sdcard_update("file_position", 2_000_000.0)
        widget.on_print_stats_update("filament_used", 1235.0)
        assert widget.layer_display_button.text() == "4"
        assert widget.layer_display_button.secondary_text != ""

    def test_estimate_runs_without_any_info_update(self, widget):
        """Klipper never resends an unchanged print_stats.info, so the estimate cannot wait to be armed."""
        widget.on_print_start("job.gcode")
        self._ready_widget(widget)
        self._feed(widget, 0.6, 1)  # z=0.6 -> layer 3
        assert widget.layer_display_button.text() == "3"


class TestFilamentPeakGate:
    """Only filament past its peak redraws the Z layer; pause retract at park Z must not."""

    def _printing_at_layer_4(self, widget):
        """Print running at Z 0.8 (layer 4) with 10 mm of filament used."""
        widget.show()
        widget.file_metadata = {
            "object_height": 10.0,
            "layer_height": 0.2,
            "first_layer_height": 0.2,
        }
        widget._handle_print_state("printing")
        widget._print_duration = 10.0
        widget._first_layer_reached = True  # PRINT_START already returned
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.2, 0])  # first layer
        widget.on_print_stats_update("filament_used", 5.0)
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.8, 0])
        widget.on_print_stats_update("filament_used", 10.0)
        assert widget.layer_display_button.text() == "4"

    def test_pause_retract_at_park_z_keeps_layer(self, widget):
        """RF50 PAUSE retracts and lifts before PAUSE_BASE, state still printing."""
        self._printing_at_layer_4(widget)
        widget.on_gcode_move_update("gcode_position", [0, 0, 15.8, 0])
        widget.on_print_stats_update("filament_used", 7.0)
        assert widget.layer_display_button.text() == "4"

    def test_unretract_at_park_z_keeps_layer(self, widget):
        self._printing_at_layer_4(widget)
        widget.on_gcode_move_update("gcode_position", [0, 0, 15.8, 0])
        widget.on_print_stats_update("filament_used", 7.0)
        widget.on_print_stats_update("filament_used", 10.0)
        assert widget.layer_display_button.text() == "4"

    def test_extrusion_past_peak_redraws(self, widget):
        self._printing_at_layer_4(widget)
        widget.on_print_stats_update("filament_used", 7.0)
        widget.on_gcode_move_update("gcode_position", [0, 0, 1.0, 0])
        widget.on_print_stats_update("filament_used", 10.5)
        assert widget.layer_display_button.text() == "5"

    def test_resume_keeps_peak(self, widget):
        """paused -> printing must not reset the peak, or the unretract at park Z redraws."""
        self._printing_at_layer_4(widget)
        widget.on_print_stats_update("filament_used", 7.0)
        widget._handle_print_state("paused")
        widget.on_gcode_move_update("gcode_position", [0, 0, 15.8, 0])
        widget._handle_print_state("printing")
        widget.on_print_stats_update("filament_used", 10.0)
        assert widget.layer_display_button.text() == "4"

    def test_reconnect_resets_peak(self, widget):
        """A stale peak from a missed print end must not hold the new print at 0."""
        widget._filament_peak = 500.0
        widget._internal_print_status = ""
        self._printing_at_layer_4(widget)

    def test_standby_resets_peak(self, widget):
        self._printing_at_layer_4(widget)
        widget._handle_print_state("standby")
        assert widget._filament_peak == 0.0


class TestVirtualSdcardUpdate:
    """virtual_sdcard_update sets progress bard, guarded by visibility."""

    def test_no_update_when_hidden(self, widget):
        from unittest.mock import patch

        widget.hide()
        with patch.object(widget.printing_progress_bar, "set_progress") as mock_test:
            widget.virtual_sdcard_update("progress", 0.5)
        mock_test.assert_not_called()

    def test_progress_field_sets_value(self, widget):
        from unittest.mock import patch

        widget.show()
        with patch.object(widget.printing_progress_bar, "set_progress") as mock_test:
            widget.virtual_sdcard_update("progress", 0.75)
        mock_test.assert_called_once_with(0.75)

    def test_non_progress_field_ignored(self, widget):
        from unittest.mock import patch

        widget.hide()
        with patch.object(widget.printing_progress_bar, "set_progress") as mock_test:
            widget.virtual_sdcard_update("is_active", True)
        mock_test.assert_not_called()


class TestOnFlowguardUpdate:
    """on_flowguard_update applies only the keys present in the payload."""

    def _mock_flowrate(self, widget):
        from unittest.mock import MagicMock

        widget.flowrate.setValue = MagicMock()
        widget.flowrate.set_max_clog = MagicMock()
        widget.flowrate.set_max_tangle = MagicMock()

    def test_partial_payload_does_not_raise(self, widget):
        self._mock_flowrate(widget)
        widget.on_flowguard_update("flowguard", {"level": 42})
        widget.flowrate.setValue.assert_called_once_with(42)
        widget.flowrate.set_max_clog.assert_not_called()
        widget.flowrate.set_max_tangle.assert_not_called()

    def test_full_payload_sets_all_fields(self, widget):
        self._mock_flowrate(widget)
        widget.on_flowguard_update(
            "flowguard", {"level": 10, "max_clog": 20, "max_tangle": 30}
        )
        widget.flowrate.setValue.assert_called_once_with(10)
        widget.flowrate.set_max_clog.assert_called_once_with(20)
        widget.flowrate.set_max_tangle.assert_called_once_with(30)


class TestStartPurgeHold:
    """The Z layer waits for PRINT_START to return: its MMU load and purge run off the bed."""

    _START_LINE = 1000.0

    def _start(self, widget):
        """Fresh print inside PRINT_START: duration grows from zero, file stays on its line."""
        widget.on_print_start("job.gcode")
        widget._internal_print_status = "printing"
        widget.file_metadata = {
            "object_height": 25.0,
            "layer_height": 0.2,
            "first_layer_height": 0.2,
        }
        widget.virtual_sdcard_update("file_position", self._START_LINE)
        widget.on_print_stats_update("print_duration", 0.5)

    def _start_macro_done(self, widget):
        widget.virtual_sdcard_update("file_position", self._START_LINE + 40)

    def _feed(self, widget, z, filament_used):
        """Report a Z move then filament progress, as the printer would."""
        widget.on_gcode_move_update("gcode_position", [0, 0, z, 0])
        widget.on_print_stats_update("filament_used", float(filament_used))

    def test_purge_above_first_layer_keeps_zero(self, widget):
        self._start(widget)
        self._feed(widget, 0.8, 35.5)  # KAMP LINE_PURGE height -> would be layer 4
        assert widget.layer_display_button.text() == "0"

    def test_first_layer_releases_the_estimate(self, widget):
        self._start(widget)
        self._feed(widget, 0.8, 35.5)
        self._start_macro_done(widget)
        self._feed(widget, 0.2, 36.5)
        assert widget.layer_display_button.text() == "1"
        self._feed(widget, 0.8, 80.0)  # layer 4 for real now
        assert widget.layer_display_button.text() == "4"

    def test_tool_change_at_start_holds_through_the_whole_macro(self, widget):
        """Loading T1 extrudes first: homing, contact probe, mesh and purge must all stay 0."""
        self._start(widget)
        shown = []
        # load at park Z, Beacon contact touch, mesh, then purge and Z-hop minutes later
        for duration, z, used in [
            (5.0, 5.0, 3.0),
            (90.0, 0.0, 3.5),
            (200.0, 2.0, 4.0),
            (400.0, 0.8, 40.0),
            (405.0, 1.6, 41.0),
        ]:
            widget.on_print_stats_update("print_duration", duration)
            self._feed(widget, z, used)
            shown.append(widget.layer_display_button.text())
        assert shown == ["0"] * 5
        self._start_macro_done(widget)
        self._feed(widget, 0.2, 42.0)
        assert widget.layer_display_button.text() == "1"

    def test_reconnect_midprint_shows_the_layer_on_the_next_line(self, widget):
        widget._internal_print_status = "printing"
        widget.file_metadata = {
            "object_height": 25.0,
            "layer_height": 0.2,
            "first_layer_height": 0.2,
        }
        widget.virtual_sdcard_update("file_position", 5_000_000.0)
        widget.on_print_stats_update("print_duration", 1800.0)
        self._feed(widget, 10.0, 5000.0)
        widget.virtual_sdcard_update("file_position", 5_000_060.0)
        self._feed(widget, 10.0, 5001.0)
        assert widget.layer_display_button.text() == "50"

    def test_new_job_rearms_the_hold(self, widget):
        self._start(widget)
        self._start_macro_done(widget)
        self._feed(widget, 0.2, 36.5)
        widget._handle_print_state("cancelled")
        self._start(widget)
        self._feed(widget, 0.8, 35.5)
        assert widget.layer_display_button.text() == "0"

    @pytest.mark.parametrize(
        ("first_layer_height", "z_offset", "expected"),
        [
            (0.2, 0.0, ["0", "0", "1", "2", "3", "10", "50"]),
            # Mainsail's formula is one layer high in these two, as before this PR
            (None, 0.0, ["0", "0", "2", "3", "4", "11", "51"]),
            (0.2, 0.01, ["0", "0", "2", "3", "4", "11", "51"]),
            (0.2, 0.6, ["0", "0", "4", "5", "6", "13", "53"]),
        ],
    )
    def test_whole_print_never_sticks_at_zero(
        self, widget, first_layer_height, z_offset, expected
    ):
        self._start(widget)
        if first_layer_height is None:
            del widget.file_metadata["first_layer_height"]
        shown = []
        # purge 0.8, Z-hop 1.6, PRINT_START returns, then the print from the first layer up
        for step, z in enumerate([0.8, 1.6, 0.2, 0.4, 0.6, 2.0, 10.0]):
            if step == 2:
                self._start_macro_done(widget)
            widget.on_print_stats_update("print_duration", 1.0 + step * 5)
            self._feed(widget, z + (z_offset if step >= 2 else 0.0), 35.0 + step * 10)
            shown.append(widget.layer_display_button.text())
        assert shown == expected


class TestPauseResumePrint:
    """pause_resume_print toggles state and emits the right signal."""

    def test_printing_emits_print_pause(self, widget, qtbot):
        widget._internal_print_status = "printing"
        with qtbot.waitSignal(widget.print_pause, timeout=500):
            widget.pause_resume_print()

    def test_paused_transitions_to_printing(self, widget, qtbot):
        widget._internal_print_status = "paused"
        with qtbot.waitSignal(widget.print_resume, timeout=500):
            widget.pause_resume_print()

    def test_disables_pause_button(self, widget):
        widget._internal_print_status = "printing"
        widget.pause_printing_btn.setEnabled(True)
        widget.pause_resume_print()
        assert not widget.pause_printing_btn.isEnabled()

    def test_unknown_state_emits_nothing(self, widget, qtbot):
        widget._internal_print_status = "idle"
        with qtbot.assertNotEmitted(widget.print_pause):
            with qtbot.assertNotEmitted(widget.print_resume):
                widget.pause_resume_print()


class TestHandleCancel:
    """handleCancel wires the cancel dialog exactly once."""

    def test_sets_cancel_message(self, widget):
        from unittest.mock import patch

        with patch.object(widget.cancel_print_dialog, "set_message") as m:
            widget.handleCancel()
        m.assert_called_once()
        assert "cancel" in m.call_args[0][0].lower()

    def test_opens_dialog(self, widget):
        from unittest.mock import patch

        with patch.object(widget.cancel_print_dialog, "open") as m:
            widget.handleCancel()
        m.assert_called_once()

    def test_accepted_triggers_print_cancel(self, widget, qtbot):
        widget.handleCancel()
        with qtbot.waitSignal(widget.print_cancel, timeout=500):
            widget.cancel_print_dialog.accepted.emit()

    def test_double_call_connects_only_once(self, widget):
        widget.handleCancel()
        widget.handleCancel()
        emissions: list[int] = []
        widget.print_cancel.connect(lambda: emissions.append(1))
        widget.cancel_print_dialog.accepted.emit()
        assert len(emissions) == 1


class TestOnFileInfo:
    """on_fileinfo loads the thumbnail and layer count regardless of visibility"""

    def _ready_widget(self, widget) -> dict:
        """Put widget in the state where gcode_move_update should fire."""
        widget.show()
        widget._internal_print_status = "printing"
        widget._print_duration = 10.0
        return {
            "layer_count": 20,
            "object_height": 10.0,
            "layer_height": 0.2,
            "first_layer_height": 0.2,
            "thumbnail_paths": [],
        }

    def test_load_correct_info(self, widget):
        _metadata = self._ready_widget(widget)
        widget.on_fileinfo(_metadata)
        assert widget.total_layers == "20"

    def test_handle_error_total_layers(self, widget):
        _metadata = self._ready_widget(widget)
        del _metadata["layer_count"]
        widget.on_fileinfo(_metadata)
        assert widget.total_layers == "---"

    def test_metadata_stored(self, widget):
        _metadata = self._ready_widget(widget)
        widget.on_fileinfo(_metadata)
        assert widget.file_metadata is _metadata

    def test_layer_display_not_reset_when_already_reporting(self, widget):
        """Re-showing after Tune redelivers cached metadata; must not reset the live layer."""
        widget.layer_display_button.setText("99")
        _metadata = self._ready_widget(widget)
        widget.on_fileinfo(_metadata)
        assert widget.layer_display_button.text() == "99"

    def test_secondary_text_set_to_total_layers(self, widget):
        _metadata = self._ready_widget(widget)
        widget.on_fileinfo(_metadata)
        assert widget.layer_display_button.secondary_text == "20"

    def test_browsed_file_metadata_ignored_midprint(self, widget):
        """fileinfo is global: a file browsed mid-print must not steal the job's totals."""
        _metadata = self._ready_widget(widget)
        _metadata["filename"] = "job.gcode"
        widget._current_file_name = "job.gcode"
        widget.on_fileinfo(_metadata)
        widget.on_fileinfo({"filename": "other.gcode", "layer_count": 999})
        assert widget.total_layers == "20"

    def test_browsed_metadata_ignored_without_job(self, widget):
        """With no job a browsed file must not fill the page; a leading / matches."""
        widget.on_fileinfo({"filename": "b.gcode", "layer_count": 5})
        assert widget.file_metadata is None
        widget._current_file_name = "a.gcode"
        widget.on_fileinfo({"filename": "/a.gcode", "layer_count": 5})
        assert widget.total_layers == "5"


class TestLoadThumbnails:
    """Only the largest readable thumbnail is decoded."""

    @pytest.fixture(autouse=True)
    def _no_view(self, widget, monkeypatch):
        """The progress bar is stubbed here; test the decode, not the scene."""
        monkeypatch.setattr(widget, "_ensure_thumbnail_widget", lambda: None)
        monkeypatch.setattr(widget, "thumbnail_view", MagicMock(), raising=False)
        monkeypatch.setattr(widget, "printing_progress_bar", MagicMock())

    @staticmethod
    def _png(path, side: int) -> str:
        """Write a side x side PNG and return its path."""
        img = QtGui.QImage(side, side, QtGui.QImage.Format.Format_ARGB32)
        img.fill(0)
        assert img.save(str(path))
        return str(path)

    def test_decodes_only_largest(self, widget, tmp_path):
        small = self._png(tmp_path / "s.png", 8)
        big = self._png(tmp_path / "b.png", 32)
        widget._load_thumbnails(small, big)
        assert [p.width() for p in widget.thumbnail_graphics] == [32]

    def test_unreadable_largest_falls_back_to_smaller(self, widget, tmp_path):
        small = self._png(tmp_path / "s.png", 8)
        widget._load_thumbnails(small, str(tmp_path / "missing.png"))
        assert [p.width() for p in widget.thumbnail_graphics] == [8]


class TestComputeProgress:
    """_compute_progress mirrors Mainsail file-relative progress."""

    def _bounds(self, widget):
        widget._gcode_start_byte = 100
        widget._gcode_end_byte = 1100

    def test_relative_midway(self, widget):
        self._bounds(widget)
        widget._file_position = 600
        assert widget._compute_progress() == pytest.approx(0.5)

    def test_before_start_is_zero(self, widget):
        """Start-macro bytes (mesh/plate cal) report 0%."""
        self._bounds(widget)
        widget._file_position = 50
        assert widget._compute_progress() == 0.0

    def test_after_end_is_one(self, widget):
        """Excluded end gcode reports 100%."""
        self._bounds(widget)
        widget._file_position = 5000
        assert widget._compute_progress() == 1.0

    def test_fallback_to_raw_without_bytes(self, widget):
        widget._gcode_start_byte = 0
        widget._gcode_end_byte = 0
        widget._raw_progress = 0.42
        assert widget._compute_progress() == 0.42


class TestResetOnNewFile:
    """A new filename clears stale layer/total; a repeat does not."""

    def test_new_filename_clears_stale_total(self, widget):
        widget._current_file_name = "old.gcode"
        widget.total_layers = "690"
        widget.layer_display_button.secondary_text = "690"
        widget.on_print_stats_update("filename", "new.gcode")
        assert widget.total_layers == "?"
        assert widget.layer_display_button.secondary_text == "?"

    def test_same_filename_does_not_reset(self, widget):
        widget._current_file_name = "same.gcode"
        widget.layer_display_button.secondary_text = "250"
        widget.on_print_stats_update("filename", "same.gcode")
        assert widget.layer_display_button.secondary_text == "250"


class TestPauseFreeze:
    """Layer is frozen across a pause so the park Z-lift never bumps it."""

    def test_pause_click_freezes(self, widget):
        widget._internal_print_status = "printing"
        widget.pause_resume_print()
        assert widget._layer_frozen is True

    def test_paused_state_freezes(self, widget):
        widget._handle_print_state("paused")
        assert widget._layer_frozen is True

    def test_printing_state_unfreezes(self, widget):
        widget._layer_frozen = True
        widget._handle_print_state("printing")
        assert widget._layer_frozen is False

    def test_frozen_ignores_reported_layer(self, widget):
        widget._layer_frozen = True
        widget.layer_display_button.setText("4")
        widget.on_print_stats_update("info", {"current_layer": 80})
        assert widget.layer_display_button.text() == "4"

    def test_frozen_blocks_z_recompute(self, widget):
        widget.show()
        widget._internal_print_status = "printing"
        widget._print_duration = 10.0
        widget.file_metadata = {
            "object_height": 10.0,
            "layer_height": 0.2,
            "first_layer_height": 0.2,
        }
        widget.layer_display_button.setText("4")
        widget._layer_frozen = True
        widget.on_gcode_move_update("gcode_position", [0, 0, 15.0, 0])
        widget.on_print_stats_update("filament_used", 5.0)
        assert widget.layer_display_button.text() == "4"


class TestResumeLayerHold:
    """Layer stays held through the resume reheat (park Z) until the file advances."""

    def _printing_at_layer_4(self, widget):
        """Print running at Z 0.8 (layer 4), file at byte 1000."""
        widget.show()
        widget.file_metadata = {
            "object_height": 10.0,
            "layer_height": 0.2,
            "first_layer_height": 0.2,
        }
        widget._handle_print_state("printing")
        widget._print_duration = 10.0
        widget._first_layer_reached = True  # PRINT_START already returned
        widget.virtual_sdcard_update("file_position", 1000.0)
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.2, 0])  # first layer
        widget.on_print_stats_update("filament_used", 0.5)
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.8, 0])
        widget.on_print_stats_update("filament_used", 1.0)
        assert widget.layer_display_button.text() == "4"

    def _pause_and_resume(self, widget):
        """Pause, park at Z 10, resume: state is printing but the nozzle is parked."""
        widget._handle_print_state("paused")
        widget.on_gcode_move_update("gcode_position", [0, 0, 10.0, 0])
        widget._handle_print_state("printing")

    def test_reheat_extrusion_at_park_z_keeps_layer(self, widget):
        self._printing_at_layer_4(widget)
        self._pause_and_resume(widget)
        widget.on_print_stats_update("filament_used", 1.5)  # purge during reheat
        assert widget.layer_display_button.text() == "4"

    def test_file_advance_releases_hold(self, widget):
        self._printing_at_layer_4(widget)
        self._pause_and_resume(widget)
        widget.virtual_sdcard_update("file_position", 1001.0)
        widget.on_gcode_move_update("gcode_position", [0, 0, 1.0, 0])
        widget.on_print_stats_update("filament_used", 2.0)
        assert widget.layer_display_button.text() == "5"

    def test_release_does_not_paint_stale_park_z(self, widget):
        self._printing_at_layer_4(widget)
        self._pause_and_resume(widget)
        widget.virtual_sdcard_update("file_position", 1001.0)  # Z still 10
        assert widget.layer_display_button.text() == "4"

    def test_fresh_start_not_held(self, widget):
        """standby -> printing must track Z at once, never hold at 0."""
        widget._handle_print_state("standby")
        self._printing_at_layer_4(widget)
        assert widget._layer_frozen is False

    def test_mid_print_restart_not_held(self, widget):
        """BlocksScreen restart mid-print sees printing first (no paused): no hold."""
        widget._internal_print_status = ""
        widget._handle_print_state("printing")
        assert widget._layer_frozen is False

    def test_cancel_during_reheat_clears_hold(self, widget):
        self._printing_at_layer_4(widget)
        self._pause_and_resume(widget)
        widget._handle_print_state("cancelled")
        assert widget._layer_frozen is False
        assert widget._awaiting_resume is False


class TestCompletionDisplay:
    """A completed print shows the final layer=total and is not blanked."""

    def _complete(self, widget):
        widget._internal_print_status = "printing"
        widget.total_layers = "250"
        widget.total_layer_reported = True
        widget._handle_print_state("complete")

    def test_shows_final_layer(self, widget):
        self._complete(widget)
        assert widget.layer_display_button.text() == "250"

    def test_total_not_blanked(self, widget):
        self._complete(widget)
        assert widget.total_layers == "250"


class TestResumeLock:
    """Pause stays locked until the file advances, and no reset strands it."""

    def _resume(self, widget, position: float = 100.0) -> None:
        widget._file_position = position
        widget._handle_print_state("paused")
        widget.pause_resume_print()
        widget._handle_print_state("printing")

    def test_resume_keeps_button_disabled(self, widget):
        self._resume(widget)
        assert widget._awaiting_resume is True
        assert not widget.pause_printing_btn.isEnabled()

    def test_position_at_baseline_keeps_lock(self, widget):
        self._resume(widget)
        widget.virtual_sdcard_update("file_position", 100.0)
        assert widget._awaiting_resume is True
        assert not widget.pause_printing_btn.isEnabled()

    def test_position_past_baseline_unlocks(self, widget):
        self._resume(widget)
        widget.virtual_sdcard_update("file_position", 101.0)
        assert widget._awaiting_resume is False
        assert widget.pause_printing_btn.isEnabled()

    def test_reset_while_awaiting_reenables_button(self, widget):
        self._resume(widget)
        widget._reset_job_display()
        assert widget._awaiting_resume is False
        assert widget.pause_printing_btn.isEnabled()

    def test_new_filename_while_awaiting_reenables_button(self, widget):
        widget._current_file_name = "old.gcode"
        self._resume(widget)
        widget.on_print_stats_update("filename", "new.gcode")
        assert widget.pause_printing_btn.isEnabled()

    def test_print_end_while_awaiting_reenables_button(self, widget):
        self._resume(widget)
        widget._handle_print_state("complete")
        assert widget._awaiting_resume is False
        assert widget.pause_printing_btn.isEnabled()
