import enum
from pickle import TRUE
from tarfile import GNU_MAGIC
import typing

import PyQt6.QtGui as QtGui
from lib.ui.filamentSensorsPage_ui import Ui_filament_sensors_page
from utils.ui import BlocksLabel
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget
import logging


class SensorWidget(QtWidgets.QWidget):
    class SensorType(enum.Enum):
        SWITCH = enum.auto()
        MOTION = enum.auto()

    class SensorFlags(enum.Flag):
        CLICKABLE = enum.auto()
        DISPLAY = enum.auto()

    class FilamentState(enum.Enum):
        MISSING = 0
        PRESENT = 1

    class SensorState(enum.IntEnum):
        OFF = 0
        ON = 1

    def __init__(self, parent, sensor_name: str):
        super(SensorWidget, self).__init__(parent)
        self.setObjectName(f"{str(sensor_name).split(' ')[1]}")
        self.setMinimumSize(640, 60)
        self.setMaximumSize(640, 60)
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.DISPLAY
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.MISSING
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.OFF
        self._button_icon_label = None
        self._icon_label = None
        self._text_label = None
        self._text: str = sensor_name.split(" ")[1]
        self._item_rect: QtCore.QRect | QtCore.QRect
        self.slider_select_on_pixmap: typing.Optional[QtGui.QPixmap] = QtGui.QPixmap(
            ":/button_borders/media/buttons/slide_select_yes.svg"
        )
        self._scaled_select_on_pixmap: typing.Optional[QtGui.QPixmap] = None
        self.slider_select_off_pixmap: typing.Optional[QtGui.QPixmap] = QtGui.QPixmap(
            ":/button_borders/media/buttons/slide_select_no.svg"
        )
        self._scaled_select_off_pixmap: typing.Optional[QtGui.QPixmap] = None

        self.icon_pixmap_filament_present: typing.Optional[QtGui.QPixmap] = (
            QtGui.QPixmap(  # TODO change icon according to the SensorType
                ":/filament/media/btn_icons/filament sensor.svg"
            )
        )
        self._scaled_icon_pixmap_fp: typing.Optional[QtGui.QPixmap] = None
        self.icon_pixmap_filament_not_present: typing.Optional[QtGui.QPixmap] = None
        self._scaled_icon_pixmap_fnp: typing.Optional[QtGui.QPixmap] = None

        self._construct_widget()

    @property
    def type(self) -> SensorType:
        return self._sensor_type

    @type.setter
    def type(self, type: SensorType):
        self._sensor_type = type

    @property
    def flags(self) -> SensorFlags:
        return self._flags

    @flags.setter
    def flags(self, flags: SensorFlags) -> None:
        self._flags = flags

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, new_text) -> None:
        if self._text_label is not None:
            self._text_label.setText(f"{new_text}")
            self._text = new_text

    @pyqtSlot(bool, name="change_fil_sensor_state")
    def change_fil_sensor_state(self, state: FilamentState):
        if isinstance(state, SensorWidget.FilamentState):
            self.filament_state = state

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        # TODO: Re-scale the icons and text content of the widget if the size of the entire widget changes
        return super().resizeEvent(a0)

    def _construct_widget(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QWidget(parent=self)
        self.sensor_horizontal_layout.setGeometry(QtCore.QRect(0, 0, 640, 60))
        self.sensor_horizontal_layout.setObjectName("horizontalLayoutWidget")
        self.sensor_layout = QtWidgets.QHBoxLayout(self.sensor_horizontal_layout)
        self.sensor_layout.setContentsMargins(0, 0, 0, 0)
        self.sensor_layout.setObjectName("sensor_item_layout")
        self.sensor_layout.addSpacing(5)
        # * Sensor icon label drawing
        if (
            self.icon_pixmap_filament_present is not None
            and self.icon_pixmap_filament_not_present is not None
        ):
            self._icon_label = BlocksLabel(parent=self.sensor_horizontal_layout)
            _policy = QtWidgets.QSizePolicy.Policy.Fixed
            size_policy = QtWidgets.QSizePolicy(_policy, _policy)
            size_policy.setHeightForWidth(
                self._icon_label.sizePolicy().hasHeightForWidth()
            )
            self._icon_label.setSizePolicy(size_policy)
            self._icon_label.setMinimumSize(60, 60)
            self._icon_label.setMaximumSize(60, 60)
            self._icon_label.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignHCenter
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            self._scaled_icon_pixmap_fp = self.icon_pixmap_filament_present.scaled(
                self._icon_label.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )

            self._scaled_icon_pixmap_fnp = self.icon_pixmap_filament_not_present.scaled(
                self._icon_label.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )

            self._icon_label.setPixmap(
                self._scaled_icon_pixmap_fp
                if self.filament_state == SensorWidget.FilamentState.PRESENT
                else self._scaled_icon_pixmap_fnp
            )
            self.sensor_layout.addWidget(self._icon_label)
            self._icon_label.update()

        # * Text label drawing
        self._text_label = QtWidgets.QLabel(parent=self.sensor_horizontal_layout)
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        self._text_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(20)
        _font.setItalic(False)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_layout.addWidget(self._text_label)
        self._text_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        # * Toggle icon drawing
        if (
            self.slider_select_on_pixmap is not None
            and self.slider_select_off_pixmap is not None
        ):
            self._button_icon_label = BlocksLabel(self.sensor_horizontal_layout)
            self._button_icon_label.setScaledContents(True)
            self._button_icon_label.setMinimumSize(60, 60)
            self._button_icon_label.setMaximumSize(60, 60)
            self._button_icon_label.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignHCenter
                & QtCore.Qt.AlignmentFlag.AlignVCenter
            )

            self._scaled_select_on_pixmap = self.slider_select_on_pixmap.scaled(
                self._button_icon_label.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )

            self._scaled_select_off_pixmap = self.slider_select_off_pixmap.scaled(
                self._button_icon_label.size(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            self._button_icon_label.setPixmap(
                self._scaled_select_on_pixmap
                if self.sensor_state == SensorWidget.SensorState.ON
                else self._scaled_select_off_pixmap
            )

            self.sensor_layout.addWidget(self._button_icon_label)
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self._button_icon_label is None:
            return
        if (
            self._scaled_select_on_pixmap is not None
            and self._scaled_select_off_pixmap is not None
        ):  # Update the toggle button pixmap which indicates the sensor state
            self._button_icon_label.setPixmap(
                self._scaled_select_on_pixmap
                if self.sensor_state == SensorWidget.SensorState.ON
                else self._scaled_select_off_pixmap
            )

        # * Paint the widget background red/green according to the presence of filament
        qp = QtWidgets.QStylePainter(self)
        qp.save()
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        if self.filament_state == SensorWidget.FilamentState.PRESENT:
            _color = QtGui.QColor(2, 204, 59, 100)
        else:
            _color = QtGui.QColor(204, 2, 2, 100)
        _brush = QtGui.QBrush()
        _brush.setColor(_color)
        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        qp.setBrush(_brush)
        qp.drawRoundedRect(
            self.rect().toRectF(), 15, 15, QtCore.Qt.SizeMode.AbsoluteSize
        )
        qp.restore()
        return super().paintEvent(a0)

    @property
    def toggle_sensor_gcode_command(self) -> str:
        self.sensor_state = (
            SensorWidget.SensorState.ON
            if self.sensor_state == SensorWidget.SensorState.OFF
            else SensorWidget.SensorState.OFF
        )
        return str(
            f"SET_FILAMENT_SENSOR SENSOR={self.text} ENABLE={not self.sensor_state.value}"
        )


# TODO: Add buttons that toggle on and of the available printer sensors
class SensorsWindow(QWidget):
    run_gcode_signal = pyqtSignal(str, name="run_gcode")

    toggle_sensor = pyqtSignal(str, name="toggle_fil_sensor")
    change_fil_sensor_state = pyqtSignal(
        SensorWidget.FilamentState, name="change_fil_sensor_state"
    )

    def __init__(self, parent, *args, **kwargs):
        super(SensorsWindow, self).__init__(parent, *args, **kwargs)

        self.parent_window = parent
        self.panel = Ui_filament_sensors_page()
        self.panel.setupUi(self)
        self.panel.fs_sensors_list.setLayoutDirection(
            Qt.LayoutDirection.LayoutDirectionAuto
        )
        self.panel.fs_sensors_list.itemClicked.connect(self.handle_sensor_clicked)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LayoutDirectionAuto)
        self.sensor_list: list[SensorWidget] = []

    @pyqtSlot(dict, name="handle_available_fil_sensors")
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
                        or str(printer_obj).startswith("filament_motion_sensor"),
                        sensors.keys(),
                    ),
                ),
            )
        )

    @pyqtSlot(str, str, bool, name="handle_fil_state_change")
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
                    self.change_fil_sensor_state.connect(_item.change_fil_sensor_state)
                    self.change_fil_sensor_state.emit(state)
                    self.change_fil_sensor_state.disconnect()
                    _item.update()
            elif parameter == "enabled":
                if _item is not None and isinstance(_item, SensorWidget):
                    self.toggle_sensor.emit(_item.toggle_sensor_gcode_command)

    @pyqtSlot(QtWidgets.QListWidgetItem, name="handle_sensor_clicked")
    def handle_sensor_clicked(self, sensor: QtWidgets.QListWidgetItem) -> None:
        _item = self.panel.fs_sensors_list.itemWidget(sensor)
        if _item is not None and isinstance(_item, SensorWidget):
            self.toggle_sensor.emit(_item.toggle_sensor_gcode_command)

    def create_sensor_widget(self, name: str) -> SensorWidget:
        """Creates a sensor row to be added to the QListWidget

        Args:
            name (str): The name of the filament sensor object
        """
        _item_widget = SensorWidget(parent=self.panel.fs_sensors_list, sensor_name=name)
        _list_item = QtWidgets.QListWidgetItem(parent=self.panel.fs_sensors_list)
        _list_item.setFlags(~Qt.ItemFlag.ItemIsEditable)
        _list_item.setSizeHint(QtCore.QSize(500, 60))
        self.panel.fs_sensors_list.setItemWidget(_list_item, _item_widget)

        return _item_widget
