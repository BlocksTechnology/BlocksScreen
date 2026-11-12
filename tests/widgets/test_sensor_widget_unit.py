"""Unit tests for SensorWidget (sensorWidget.py)"""

from unittest.mock import MagicMock

import pytest
from PyQt6 import QtWidgets

from lib.panels.widgets.PrintTab.sensorWidget import SensorWidget


@pytest.mark.parametrize(
    ("state", "attr"),
    [
        (SensorWidget.FilamentState.MISSING, "icon_pixmap_fnp"),
        (SensorWidget.FilamentState.PRESENT, "icon_pixmap_fp"),
    ],
)
def test_paint_shows_the_pixmap_for_the_filament_state(qapp, state, attr):
    """paintEvent hands the label the pixmap matching the state, the MISSING one included."""
    parent = QtWidgets.QWidget()
    widget = SensorWidget(parent, "filament_switch_sensor runout")
    widget.filament_state = state
    widget._icon_label.setPixmap = MagicMock()
    widget.grab()
    widget._icon_label.setPixmap.assert_called_with(getattr(widget, attr))
    parent.deleteLater()
