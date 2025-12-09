from ctypes import alignment
import enum
import typing

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

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )

    def __init__(self, parent, sensor_name: str):
        super(SensorWidget, self).__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(self.name)
        self.setMinimumSize(250, 250)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = (
            SensorWidget.SensorState.ON
        )
        self._icon_label = None
        self._text_label = None
        self._text: str = (
            f"{self.name}"
        )
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self.setupUI()
        #self.toggle_button.stateChange.connect(self.toggle_button_state)
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)
        

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
            
    @QtCore.pyqtSlot(FilamentState, name="change_fil_sensor_state")
    def change_fil_sensor_state(self, state: FilamentState):
        """Change filament sensor state"""
        if isinstance(state, SensorWidget.FilamentState):
            if state == SensorWidget.FilamentState.PRESENT:
                self.filament_state = SensorWidget.FilamentState.MISSING
            else:
                self.filament_state = SensorWidget.FilamentState.PRESENT
            self.update()
    
    
    def toggle_button_state(self, state: ToggleAnimatedButton.State) -> None:
        if state.value != self.sensor_state.value:
            self.sensor_state = self.SensorState(state.value)
            self.toggle_button.state = ToggleAnimatedButton.State(self.sensor_state.value)
            self.repaint()
            
    @QtCore.pyqtSlot(ToggleAnimatedButton.State, name="state-change")       
    def toggle_sensor_state(self, state: ToggleAnimatedButton.State) -> None:
        if state.value != self.sensor_state.value:
            self.sensor_state = self.SensorState(state.value)
            self.run_gcode_signal.emit(f"SET_FILAMENT_SENSOR SENSOR={self.text} ENABLE={int(self.sensor_state.value)}")
            self.repaint()
        
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        return super().resizeEvent(a0)

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
            _color = QtGui.QColor(2, 204, 59, 200)
        else:
            _color = QtGui.QColor(204, 50, 50, 200)
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
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(20)
        style_painter.setFont(_font)
        
        if self.sensor_state == SensorWidget.SensorState.ON:
            _color = QtGui.QColor(2, 204, 59, 200)
        else:
            _color = QtGui.QColor(204, 50, 50, 200)
        
        style_painter.setPen(_color)

        label_name = self._text_label_name_ 
        label_detected = self._text_label_detected 
        label_state = self._text_label_state 

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText,_color)
        
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
        )
        
        palette_as_needed = label_detected.palette()
        palette_as_needed.setColor(
            palette_as_needed.ColorRole.WindowText, QtGui.QColorConstants.White
        )
        style_painter.setPen(QtGui.QColor("white"))

        _font.setPointSize(15)
        style_painter.setFont(_font)
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette_as_needed,
            True,
            f"Filament: {self.filament_state.name}",
        )
        
        style_painter.setFont(_font)
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette_as_needed,
            True,
             f"Enable: {self.sensor_state.name}"
        )
        style_painter.end()

    def _setupUI(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        #self.sensor_vertical_layout.setGeometry(QtCore.QRect(0, 0, 640, 100))
        self.sensor_vertical_layout.setObjectName("sensorVerticalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(80, 80)
        self._icon_label.setMaximumSize(80, 80)
        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 60)
        self._text_label_name_.setMaximumSize(self.rect().width(), 60)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)
        #LABEL 2 
        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(self.rect().width(), 60)
        self._text_label_detected.setMaximumSize(self.rect().width(), 60)

        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(12)
        palette_as_needed = self._text_label_detected.palette()
        palette_as_needed.setColor(
            palette_as_needed.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        filament_state = not self.filament_state
        self._text_label_detected.setPalette(palette_as_needed)
        self._text_label_detected.setFont(_font)
        self._text_label_detected.setText(f"Filament: {self.filament_state}")
        
        #LABEL 3
        self._text_label_state = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_state.sizePolicy().hasHeightForWidth()
        )
        self._text_label_state.setMinimumSize(self.rect().width(), 60)
        self._text_label_state.setMaximumSize(self.rect().width(), 60)

        self._text_label_state.setPalette(palette_as_needed)
        self._text_label_state.setFont(_font)
        self._text_label_state.setText(f"Enable: {self.sensor_state.name}")
        
        
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._text_label_state.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._text_label_detected.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


        
        self._icon_label.setSizePolicy(size_policy)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMaximumWidth(100)
        self.toggle_button.state = ToggleAnimatedButton.State.ON

        self._text_label_detected.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sensor_vertical_layout.addWidget(self._icon_label,alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sensor_vertical_layout.addWidget(self._text_label_name_, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sensor_vertical_layout.addWidget(self._text_label_state,alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sensor_vertical_layout.addWidget(self._text_label_detected,alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sensor_vertical_layout.addWidget(self.toggle_button)
        
        self.setLayout(self.sensor_vertical_layout)
