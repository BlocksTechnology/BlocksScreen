"""Unit tests for SensorsWindow.reset_view_model (sensorsPanel.py)"""

from unittest.mock import MagicMock

from lib.panels.widgets.sensorsPanel import SensorsWindow


def test_reset_view_model_drops_stale_sensor_widgets():
    fake = MagicMock()
    widgets = {"a": MagicMock(), "b": MagicMock()}
    fake.sensor_tracking_widget = dict(widgets)
    SensorsWindow.reset_view_model(fake)
    for widget in widgets.values():
        fake.info_box_layout.removeWidget.assert_any_call(widget)
        widget.deleteLater.assert_called_once()
    assert fake.sensor_tracking_widget == {}
    assert fake.current_widget is None
    fake.model.clear.assert_called_once()
    fake.sensor_list.clear.assert_called_once()
