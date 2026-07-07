"""Unit tests for JobStatusWidget (JobStatusWidget.py)"""

import sys
import types
import pytest
from PyQt6 import QtWidgets


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

    return Stub


_blocks_button = types.ModuleType("lib.utils.blocks_button")
_blocks_label = types.ModuleType("lib.utils.blocks_label")
_display_button = types.ModuleType("lib.utils.display_button")
_progress_bar = types.ModuleType("lib.utils.blocks_progressbar")
_base_popup = types.ModuleType("lib.panels.widgets.basePopup")

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
    ("lib.panels.widgets.basePopup", _base_popup),
]:
    sys.modules[_name] = _mod  # force-set so network conftest stubs don't win

import events  # noqa: F401, E402  # ensure events is importable before jobStatusPage loads
from lib.panels.widgets.jobStatusPage import JobStatusWidget  # noqa: E402


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

    def test_sets_status_to_printing(self, widget):
        widget.on_print_start("test.gcode")
        assert widget._internal_print_status == "printing"

    def test_emits_print_start_signal(self, widget, qtbot):
        with qtbot.waitSignal(widget.print_start, timeout=500) as sig:
            widget.on_print_start("my_file.gcode")
        assert sig.args == ["my_file.gcode"]


class TestHandlePrintState:
    """_handle_print_state drives the UI and signals correctly."""

    def test_printing_emits_show_request(self, widget, qtbot):
        with qtbot.waitSignal(widget.show_request, timeout=500):
            widget._handle_print_state("printing")

    def test_paused_emits_show_request(self, widget, qtbot):
        with qtbot.waitSignal(widget.show_request, timeout=500):
            widget._handle_print_state("paused")

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

    def test_current_layer_not_none_disables_fallback(self, widget):
        widget.on_print_stats_update("info", {"current_layer": 5})
        assert widget.layer_fallback is False

    def test_current_layer_none_enables_fallback(self, widget):
        widget.on_print_stats_update("info", {"current_layer": None})
        assert widget.layer_fallback is True

    def test_total_layer_value_stored(self, widget):
        widget.on_print_stats_update("info", {"total_layer": 120})
        assert widget.total_layers == 120


class TestOnGcodeMoveUpdate:
    """on_gcode_move_update computes layer from Z position."""

    def _ready_widget(self, widget):
        """Put widget in the state where gcode_move_update should fire."""
        widget.show()
        widget._internal_print_status = "printing"
        widget.layer_fallback = True
        widget._print_duration = 10.0
        widget.layer_display_button.setText("sentinel")
        widget.file_metadata = {
            "object_height": 10.0,
            "layer_height": 0.2,
            "first_layer_height": 0.2,
        }

    def test_updates_when_hidden(self, widget):
        """Layer must keep syncing while the page is hidden (e.g. behind Tune),
        mirroring Mainsail so the value is correct the moment it's shown again."""
        self._ready_widget(widget)
        widget.hide()
        # z=0.4 -> layer 2; E must advance past the high-water mark to count.
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.4, 1])
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.4, 2])
        assert widget.layer_display_button.text() == "2"

    def test_no_update_wrong_field(self, widget):
        self._ready_widget(widget)
        widget.on_gcode_move_update("position", [0, 0, 1.0, 0])
        assert widget.layer_display_button.text() == "sentinel"

    def test_no_update_when_not_printing(self, widget):
        self._ready_widget(widget)
        widget._internal_print_status = "paused"
        widget.on_gcode_move_update("gcode_position", [0, 0, 1.0, 0])
        assert widget.layer_display_button.text() == "sentinel"

    def test_no_update_when_duration_zero(self, widget):
        self._ready_widget(widget)
        widget._print_duration = 0.0
        widget.on_gcode_move_update("gcode_position", [0, 0, 1.0, 0])
        assert widget.layer_display_button.text() == "sentinel"

    def test_calculates_layer_from_z(self, widget):
        self._ready_widget(widget)
        widget.on_gcode_move_update(
            "gcode_position", [0, 0, 0.4, 0]
        )  # z=0.4 -> layer 2
        assert widget.layer_display_button.text() == "2"

    def test_z_hop_self_corrects(self, widget):
        """Stateless Z recompute (Mainsail): a transient hop settles back on return."""
        self._ready_widget(widget)
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.4, 0])
        assert widget.layer_display_button.text() == "2"
        widget.on_gcode_move_update("gcode_position", [0, 0, 1.0, 0])  # hop -> layer 5
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.4, 0])  # back -> layer 2
        assert widget.layer_display_button.text() == "2"

    def test_layer_tracks_z(self, widget):
        """Layer follows current Z and may regress on a Z drop (Mainsail)."""
        self._ready_widget(widget)
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.8, 0])  # layer 4
        assert widget.layer_display_button.text() == "4"
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.4, 0])  # layer 2
        assert widget.layer_display_button.text() == "2"

    def test_reported_total_layer_not_overridden_by_estimate(self, widget):
        """Klipper-reported total_layer wins over the geometry estimate."""
        self._ready_widget(widget)
        widget.on_print_stats_update("info", {"total_layer": 999})
        assert widget.total_layer_reported is True
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.4, 1])
        widget.on_gcode_move_update("gcode_position", [0, 0, 0.4, 2])
        assert widget.layer_display_button.secondary_text == "999"


class TestVirtualSdcardUpdate:
    """virtual_sdcard_update sets progress bard, guarded by visibility."""

    def test_no_update_when_hidden(self, widget):
        from unittest.mock import patch

        widget.hide()
        with patch.object(widget.printing_progress_bar, "setValue") as mock_test:
            widget.virtual_sdcard_update("progress", 50)
        mock_test.assert_not_called()

    def test_progress_field_sets_value(self, widget):
        from unittest.mock import patch

        widget.show()
        with patch.object(widget.printing_progress_bar, "setValue") as mock_test:
            widget.virtual_sdcard_update("progress", 75)
        mock_test.assert_called_once_with(75)

    def test_non_progress_field_ignored(self, widget):
        from unittest.mock import patch

        widget.hide()
        with patch.object(widget.printing_progress_bar, "setValue") as mock_test:
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
        widget.layer_fallback = True
        widget._print_duration = 10.0
        return {
            "layer_count": 20,
            "object_height": 10.0,
            "layer_height": 0.2,
            "first_layer_height": 0.2,
            "thumbnail_images": [],
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
