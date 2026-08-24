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
        super().__init__(parent)
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
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label: BlocksLabel | None = None
        self._text_label: BlocksLabel | None = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )

        # Constant paint state
        self._name_font = QtGui.QFont()
        self._name_font.setPointSize(20)
        self._value_font = QtGui.QFont()
        self._value_font.setPointSize(16)
        self._text_palette = QtGui.QPalette()
        self._text_palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtGui.QColorConstants.White
        )
        self._filament_text = ""
        self._enable_text = ""

        self._setupUI()
        self._refresh_state()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def _refresh_state(self) -> None:
        """Rebuild the drawn strings and the icon, both only change with the state"""
        filament_tabs = "\t" * 12
        enable_tabs = "\t" * 15
        self._filament_text = (
            f"Filament: {filament_tabs}{self.filament_state.name.capitalize()}"
        )
        self._enable_text = (
            f"Enable: {enable_tabs}{self.sensor_state.name.capitalize()}"
        )
        if self._icon_label is not None:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )

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
        """Invert the filament state in response to a Klipper update"""
        if not isinstance(state, SensorWidget.FilamentState):
            return
        self.filament_state = SensorWidget.FilamentState(not state.value)
        self._refresh_state()
        self.update()

    def toggle_button_state(self, state: ToggleAnimatedButton.State) -> None:
        """Called when the Klipper firmware reports an update to the filament sensor state"""
        self.toggle_button.setDisabled(False)
        if state.value != self.sensor_state.value:
            self.sensor_state = self.SensorState(state.value)
            self.toggle_button.state = ToggleAnimatedButton.State(
                self.sensor_state.value
            )
            self._refresh_state()
            self.update()

    @QtCore.pyqtSlot(ToggleAnimatedButton.State, name="state-change")
    def toggle_sensor_state(self, state: ToggleAnimatedButton.State) -> None:
        """Emit the appropriate G-Code command to change the filament sensor state."""
        if state.value != self.sensor_state.value:
            self.toggle_button.setDisabled(True)
            self.run_gcode_signal.emit(
                f"SET_FILAMENT_SENSOR SENSOR={self.text} ENABLE={int(state.value)}"
            )
            self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setFont(self._name_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state
        palette = self._text_palette

        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        style_painter.setFont(self._value_font)
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            self._filament_text,
            QtGui.QPalette.ColorRole.WindowText,
        )

        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            self._enable_text,
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def _setupUI(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName("sensorVerticalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        parent_width = self.parentWidget().width()
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(120, 100)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        font = QtGui.QFont()
        font.setPointSize(15)
        self._text_label_name_ = BlocksLabel(parent=self)
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._text_label_name_.setFont(font)
        self._text_label_name_.setStyleSheet("background: transparent; color: white;")
        self._text_label_name_.setText(str(self._text))

        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )

        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(parent_width, 20)

        self._text_label_detected.setPalette(palette)
        self._text_label_detected.setText(f"Filament: {self.filament_state}")

        self._text_label_state = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_state.sizePolicy().hasHeightForWidth()
        )
        self._text_label_state.setMinimumSize(parent_width, 20)

        self._text_label_state.setPalette(palette)
        self._text_label_state.setText(f"Enable: {self.sensor_state.name}")

        self._icon_label.setSizePolicy(size_policy)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumSize(100, 50)
        self.toggle_button.state = ToggleAnimatedButton.State.ON

        self.sensor_vertical_layout.addWidget(
            self._icon_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.sensor_vertical_layout.addWidget(
            self._text_label_name_, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.sensor_vertical_layout.addStretch()
        self.sensor_vertical_layout.addWidget(
            self._text_label_state, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.sensor_vertical_layout.addStretch()
        self.sensor_vertical_layout.addWidget(
            self._text_label_detected, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.sensor_vertical_layout.addStretch()
        self.sensor_vertical_layout.addWidget(
            self.toggle_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(self.sensor_vertical_layout)
