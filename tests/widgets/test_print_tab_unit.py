"""Unit Tests for PrintTab"""

import sys
from unittest.mock import MagicMock

# Stub all bare lib.* imports that PrintTab.py needs at import time.
for _mod in [
    "configfile",
    "lib.files",
    "lib.moonrakerComm",
    "lib.panels.widgets.babystepPage",
    "lib.panels.widgets.basePopup",
    "lib.panels.widgets.confirmPage",
    "lib.panels.widgets.filesPage",
    "lib.panels.widgets.jobStatusPage",
    "lib.panels.widgets.numpadPage",
    "lib.panels.widgets.sensorsPanel",
    "lib.panels.widgets.slider_selector_page",
    "lib.panels.widgets.tunePage",
    "lib.printer",
    "lib.utils.blocks_button",
    "lib.utils.display_button",
    "devices.amu",
]:
    sys.modules[_mod] = MagicMock()

from BlocksScreen.lib.panels.printTab import PrintTab  # noqa: E402


def _make_stub(amu_manager=None, sensors=None):
    obj = MagicMock()
    obj._amu_manager = amu_manager
    obj.printer.available_filament_sensors = sensors if sensors is not None else {}
    return obj


class TestFilamentLoaded:
    def test_hh_loaded_returns_true(self):
        amu = MagicMock()
        amu.is_amu_active.return_value = True
        amu.get_state.return_value = MagicMock(filament="Loaded")
        assert PrintTab._filament_loaded((_make_stub(amu_manager=amu))) is True

    def test_hh_unloaded_returns_false(self):
        amu = MagicMock()
        amu.is_amu_active.return_value = True
        amu.get_state.return_value = MagicMock(filament="Unloaded")
        assert PrintTab._filament_loaded((_make_stub(amu_manager=amu))) is False

    def test_hh_unkown_returns_false(self):
        amu = MagicMock()
        amu.is_amu_active.return_value = True
        amu.get_state.return_value = MagicMock(filament="Unknown")
        assert PrintTab._filament_loaded((_make_stub(amu_manager=amu))) is False

    def test_hh_state_non_falls_through_to_sensors(self):
        amu = MagicMock()
        amu.is_amu_active.return_value = True
        amu.get_state.return_value = None
        sensors = {"switch": {"enabled": True, "filament_detected": True}}
        assert (
            PrintTab._filament_loaded((_make_stub(amu_manager=amu, sensors=sensors)))
            is True
        )

    def test_no_amu_falls_through_to_sensors(self):
        sensors = {"switch": {"enabled": True, "filament_detected": True}}
        assert PrintTab._filament_loaded((_make_stub(sensors=sensors))) is True

    def test_no_sensors_returns_true(self):
        assert PrintTab._filament_loaded((_make_stub())) is True

    def test_sensor_detected_returns_true(self):
        sensors = {"switch": {"enabled": True, "filament_detected": True}}
        assert PrintTab._filament_loaded(_make_stub(sensors=sensors)) is True

    def test_sensor_not_detected_returns_false(self):
        sensors = {"switch": {"enabled": True, "filament_detected": False}}
        assert PrintTab._filament_loaded(_make_stub(sensors=sensors)) is False

    def test_disabled_sensor_skipped_returns_false(self):
        sensors = {"switch": {"enabled": False, "filament_detected": True}}
        assert PrintTab._filament_loaded(_make_stub(sensors=sensors)) is False

    def test_non_dict_sensor_skipped_returns_false(self):
        sensors = {"motion": True}
        assert PrintTab._filament_loaded(_make_stub(sensors=sensors)) is False


class TestGuardStartPrint:
    def test_proceeds_when_filament_loaded(self):
        obj = _make_stub()
        obj._filament_loaded = MagicMock(return_value=True)
        PrintTab._guard_start_print(obj, "model.gcode")
        obj.jobStatusPage_widget.on_print_start.assert_called_once_with("model.gcode")
        obj._notify_no_filament.assert_not_called()

    def test_blocks_and_notifies_when_no_filament(self):
        obj = _make_stub()
        obj._filament_loaded = MagicMock(return_value=False)
        PrintTab._guard_start_print(obj, "model.gcode")
        obj._notify_no_filament.assert_called_once()
        obj.jobStatusPage_widget.on_print_start.assert_not_called()


class TestGuardResume:
    def test_proceeds_when_filament_loaded(self):
        obj = _make_stub()
        obj._filament_loaded = MagicMock(return_value=True)
        PrintTab._guard_resume(obj)
        obj.ws.api.resume_print.assert_called_once()
        obj._notify_no_filament.assert_not_called()

    def test_blocks_and_notifies_when_no_filament(self):
        obj = _make_stub()
        obj._filament_loaded = MagicMock(return_value=False)
        PrintTab._guard_resume(obj)
        obj._notify_no_filament.assert_called_once()
        obj.ws.api.resume_print.assert_not_called()
