"""Unit tests for SensorsWindow routing Klipper filament sensor updates."""

from types import SimpleNamespace

import pytest
from lib.panels.widgets.sensorsPanel import SensorsWindow
from lib.panels.widgets.sensorWidget import SensorWidget
from PyQt6 import QtWidgets


@pytest.fixture()
def parent(qtbot):
    """Parent widget; SensorWidget sizes itself from it."""
    w = QtWidgets.QWidget()
    qtbot.addWidget(w)
    return w


@pytest.fixture()
def sensor(parent):
    """SensorWidget for a Klipper filament_switch_sensor."""
    return SensorWidget(parent, "filament_switch_sensor runout")


def _route(sensor, name, parameter, value):
    # unbound call skips SensorsWindow._setupUi, which needs compiled qrc fonts
    panel = SimpleNamespace(sensor_tracking_widget={sensor.name: sensor})
    SensorsWindow.handle_fil_state_change(panel, name, parameter, value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("detected", "expected"),
    [
        (True, SensorWidget.FilamentState.PRESENT),
        (False, SensorWidget.FilamentState.MISSING),
    ],
)
def test_filament_detected_sets_state(sensor, detected, expected):
    _route(sensor, "runout", "filament_detected", detected)
    assert sensor.filament_state is expected


def test_unknown_sensor_ignored(sensor):
    before = sensor.filament_state
    _route(sensor, "other", "filament_detected", not before.value)
    assert sensor.filament_state is before


@pytest.mark.parametrize(
    ("klipper_name", "short_name"),
    [("filament_motion_sensor encoder", "encoder"), ("cutter_sensor", "cutter_sensor")],
)
def test_sensor_name(parent, klipper_name, short_name):
    assert SensorWidget(parent, klipper_name).name == short_name
