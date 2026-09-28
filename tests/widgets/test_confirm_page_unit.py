"""Unit tests for ConfirmWidget metadata handling (confirmPage.py)"""

from unittest.mock import MagicMock

import pytest
from lib.panels.widgets.confirmPage import ConfirmWidget


def _labels(metadata: dict) -> tuple[str, str]:
    fake = MagicMock()
    ConfirmWidget._update_metadata_labels(fake, metadata)
    return (
        fake.cf_info_tf.setText.call_args.args[0],
        fake.cf_info_tr.setText.call_args.args[0],
    )


@pytest.mark.parametrize(
    "metadata",
    [
        {},
        {"filament_weight_total": None, "estimated_time": None},
        {"filament_weight_total": "12", "estimated_time": "60"},
        {"filament_weight_total": -1.0, "estimated_time": -5},
    ],
)
def test_missing_or_invalid_metadata_shows_unknown(metadata):
    assert _labels(metadata) == ("Total Filament: Unknown", "Slicer time: Unknown")


def test_valid_metadata_formats_grams_and_time():
    assert _labels({"filament_weight_total": 12.345, "estimated_time": 3725.6}) == (
        "Total Filament: 12.35g",
        "Slicer time: 1h 2m",
    )


def test_heavy_print_uses_kilograms():
    tf, _ = _labels({"filament_weight_total": 1500.0, "estimated_time": 30})
    assert tf == "Total Filament: 1.50kg"


def test_show_widget_with_empty_metadata_still_updates_filename():
    fake = MagicMock()
    ConfirmWidget.on_show_widget(fake, "gcodes/sub/part.gcode", {})
    assert (fake.directory, fake.filename) == ("gcodes/sub", "part.gcode")
    fake.cf_file_name.setText.assert_called_once_with("part.gcode")
    fake._update_metadata_labels.assert_called_once_with({})
