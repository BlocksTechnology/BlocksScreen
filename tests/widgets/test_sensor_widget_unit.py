"""Unit tests for SensorWidget (sensorWidget.py)"""

from PyQt6 import QtWidgets

from lib.panels.widgets.PrintTab.sensorWidget import SensorWidget


def test_missing_filament_paints_without_error(qapp):
    """The MISSING branch reads icon_pixmap_fnp in _setup_ui and paintEvent."""
    parent = QtWidgets.QWidget()
    widget = SensorWidget(parent, "filament_switch_sensor runout")
    widget.filament_state = SensorWidget.FilamentState.MISSING
    widget.grab()
    parent.deleteLater()
