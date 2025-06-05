
from lib.ui.filamentSensorsPage_ui import Ui_filament_sensors_page
from PyQt6 import QtCore, QtWidgets
from lib.panels.widgets.sensorWidget import SensorWidget


# TODO: Add buttons that toggle on and of the available printer sensors
class SensorsWindow(QtWidgets.QWidget):
    run_gcode_signal = QtCore.pyqtSignal(str, name="run_gcode")
    change_fil_sensor_state = QtCore.pyqtSignal(
        SensorWidget.FilamentState, name="change_fil_sensor_state"
    )

    def __init__(self, parent, *args, **kwargs):
        super(SensorsWindow, self).__init__(parent, *args, **kwargs)

        self.parent_window = parent
        self.panel = Ui_filament_sensors_page()
        self.panel.setupUi(self)

        self.panel.fs_sensors_list.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LayoutDirectionAuto
        )
        self.panel.fs_sensors_list.itemClicked.connect(
            self.handle_sensor_clicked
        )
        self.sensor_list: list[SensorWidget] = []

    @QtCore.pyqtSlot(dict, name="handle_available_fil_sensors")
    def handle_available_fil_sensors(self, sensors: dict) -> None:
        if not isinstance(sensors, dict):
            return

        self.sensor_list = list(
            map(
                lambda sensor: self.create_sensor_widget(name=sensor),
                list(
                    filter(
                        lambda printer_obj: str(printer_obj).startswith(
                            "filament_switch_sensor"
                        )
                        or str(printer_obj).startswith(
                            "filament_motion_sensor"
                        ),
                        sensors.keys(),
                    ),
                ),
            )
        )

    @QtCore.pyqtSlot(str, str, bool, name="handle_fil_state_change")
    def handle_fil_state_change(
        self, sensor_name: str, parameter: str, value: bool
    ) -> None:
        if sensor_name in self.sensor_list:
            state = SensorWidget.FilamentState(value)
            _split = sensor_name.split(" ")
            _item = self.panel.fs_sensors_list.findChild(
                SensorWidget,
                name=_split[1],
                options=QtCore.Qt.FindChildOption.FindChildrenRecursively,
            )
            if parameter == "filament_detected":
                if isinstance(_item, SensorWidget) and hasattr(
                    _item, "change_fil_sensor_state"
                ):
                    self.change_fil_sensor_state.connect(
                        _item.change_fil_sensor_state
                    )
                    self.change_fil_sensor_state.emit(state)
                    self.change_fil_sensor_state.disconnect()
                    _item.repaint()

            elif parameter == "enabled":
                if _item and isinstance(_item, SensorWidget):
                    self.run_gcode_signal.emit(
                        _item.toggle_sensor_gcode_command
                    )

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem, name="handle_sensor_clicked")
    def handle_sensor_clicked(self, sensor: QtWidgets.QListWidgetItem) -> None:
        _item = self.panel.fs_sensors_list.itemWidget(sensor)
        if _item and isinstance(_item, SensorWidget):
            self.run_gcode_signal.emit(_item.toggle_sensor_gcode_command)

    def create_sensor_widget(self, name: str) -> SensorWidget:
        """Creates a sensor row to be added to the QListWidget

        Args:
            name (str): The name of the filament sensor object
        """

        _item_widget = SensorWidget(
            parent=self.panel.fs_sensors_list, sensor_name=name
        )
        _list_item = QtWidgets.QListWidgetItem(
            parent=self.panel.fs_sensors_list
        )
        _list_item.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        _list_item.setSizeHint(QtCore.QSize(500, 60))
        self.panel.fs_sensors_list.setItemWidget(_list_item, _item_widget)

        return _item_widget
