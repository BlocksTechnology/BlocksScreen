import enum

from lib.utils.blocks_label import BlocksLabel
from lib.utils.toggleAnimatedButton import ToggleAnimatedButton
from PyQt6 import QtCore, QtGui, QtWidgets


class SensorWidget(QtWidgets.QWidget):
    class SensorType(enum.Enum):
        """Filament sensor type"""

        SWITCH = enum.auto()
        MOTION = enum.auto()

    class SensorFlags(enum.Flag):
        """Filament sensor flags"""

        CLICKABLE = enum.auto()
        DISPLAY = enum.auto()

    class FilamentState(enum.Enum):
        """Current filament state, sensor has or does not have filament"""

        MISSING = 0
        PRESENT = 1

    class SensorState(enum.IntEnum):
        """Current sensor filament state, if it's turned on or not"""

        OFF = False
        ON = True

    def __init__(self, parent, sensor_name: str):
        super(SensorWidget, self).__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(self.name)
        self.setMinimumSize(parent.contentsRect().width(), 60)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.MISSING
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.OFF
        self._icon_label = None
        self._text_label = None
        self._text: str = str(self.sensor_type.name) + " Sensor: " + str(self.name)
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()

    @property
    def type(self) -> SensorType:
        """Sensor type"""
        return self._sensor_type

    @type.setter
    def type(self, type: SensorType):
        self._sensor_type = type

    @property
    def flags(self) -> SensorFlags:
        """Current filament sensor flags"""
        return self._flags

    @flags.setter
    def flags(self, flags: SensorFlags) -> None:
        self._flags = flags

    @property
    def text(self) -> str:
        """Filament sensor text"""
        return self._text

    @text.setter
    def text(self, new_text) -> None:
        if self._text_label is not None:
            self._text_label.setText(f"{new_text}")
            self._text = new_text

    @QtCore.pyqtSlot(bool, name="change_fil_sensor_state")
    def change_fil_sensor_state(self, state: FilamentState):
        """Change filament sensor state"""
        if isinstance(state, SensorWidget.FilamentState):
            self.filament_state = state

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        # if (
        #     self._scaled_select_on_pixmap is not None
        #     and self._scaled_select_off_pixmap is not None
        # ):  # Update the toggle button pixmap which indicates the sensor state
        #     self._button_icon_label.setPixmap(
        #         self._scaled_select_on_pixmap
        #         if self.sensor_state == SensorWidget.SensorState.ON
        #         else self._scaled_select_off_pixmap
        #     )

        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )

        if self.filament_state == SensorWidget.FilamentState.PRESENT:
            _color = QtGui.QColor(2, 204, 59, 100)
        else:
            _color = QtGui.QColor(204, 50, 50, 100)
        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    @property
    def toggle_sensor_gcode_command(self) -> str:
        """Toggle filament sensor"""
        self.sensor_state = (
            SensorWidget.SensorState.ON
            if self.sensor_state == SensorWidget.SensorState.OFF
            else SensorWidget.SensorState.OFF
        )
        return str(
            f"SET_FILAMENT_SENSOR SENSOR={self.text} ENABLE={not self.sensor_state.value}"
        )

    def _setupUI(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(QtCore.QRect(0, 0, 640, 60))
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMaximumWidth(100)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)
