import enum
import typing

from lib.utils.blocks_label import BlocksLabel
from lib.utils.toggleAnimatedButton import ToggleAnimatedButton
from PyQt6 import QtCore, QtGui, QtWidgets
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


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
        args = [parent, sensor_name]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSensorWidgetǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁSensorWidgetǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁSensorWidgetǁ__init____mutmut_orig(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_1(self, parent, sensor_name: str):
        super().__init__(None)
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_2(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = None
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_3(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(None)[1]
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_4(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(None).split(" ")[1]
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_5(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split("XX XX")[1]
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_6(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[2]
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_7(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = None

        self.setObjectName(self.name)
        self.setMinimumSize(250, 250)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_8(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "XXswitchXX" in str(sensor_name).split(" ")[0].lower()
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_9(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "SWITCH" in str(sensor_name).split(" ")[0].lower()
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_10(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" not in str(sensor_name).split(" ")[0].lower()
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_11(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].upper()
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_12(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(None)[0].lower()
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_13(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(None).split(" ")[0].lower()
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_14(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split("XX XX")[0].lower()
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_15(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[1].lower()
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_16(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(None)
        self.setMinimumSize(250, 250)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_17(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(self.name)
        self.setMinimumSize(None, 250)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_18(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(self.name)
        self.setMinimumSize(250, None)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_19(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(self.name)
        self.setMinimumSize(250)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_20(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(self.name)
        self.setMinimumSize(250, )
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_21(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(self.name)
        self.setMinimumSize(251, 250)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_22(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(self.name)
        self.setMinimumSize(250, 251)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_23(self, parent, sensor_name: str):
        super().__init__(parent)
        self.name = str(sensor_name).split(" ")[1]
        self.sensor_type: SensorWidget.SensorType = (
            self.SensorType.SWITCH
            if "switch" in str(sensor_name).split(" ")[0].lower()
            else self.SensorType.MOTION
        )

        self.setObjectName(self.name)
        self.setMinimumSize(250, 250)
        self.setLayoutDirection(None)

        self._sensor_type: SensorWidget.SensorType = self.SensorType.SWITCH
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_24(self, parent, sensor_name: str):
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

        self._sensor_type: SensorWidget.SensorType = None
        self._flags: SensorWidget.SensorFlags = self.SensorFlags.CLICKABLE
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_25(self, parent, sensor_name: str):
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
        self._flags: SensorWidget.SensorFlags = None
        self.filament_state: SensorWidget.FilamentState = (
            SensorWidget.FilamentState.PRESENT
        )
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_26(self, parent, sensor_name: str):
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
        self.filament_state: SensorWidget.FilamentState = None
        self.sensor_state: SensorWidget.SensorState = SensorWidget.SensorState.ON
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_27(self, parent, sensor_name: str):
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
        self.sensor_state: SensorWidget.SensorState = None
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_28(self, parent, sensor_name: str):
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
        self._icon_label = ""
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_29(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = ""
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_30(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = None
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_31(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = None
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_32(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = None
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_33(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            None
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_34(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            "XX:/filament_related/media/btn_icons/filament_sensor_turn_on.svgXX"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_35(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/FILAMENT_RELATED/MEDIA/BTN_ICONS/FILAMENT_SENSOR_TURN_ON.SVG"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_36(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = None
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_37(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            None
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_38(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            "XX:/filament_related/media/btn_icons/filament_sensor_off.svgXX"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_39(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/FILAMENT_RELATED/MEDIA/BTN_ICONS/FILAMENT_SENSOR_OFF.SVG"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(self.toggle_sensor_state)

    def xǁSensorWidgetǁ__init____mutmut_40(self, parent, sensor_name: str):
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
        self._icon_label = None
        self._text_label = None
        self._text = self.name
        self._item_rect: QtCore.QRect = QtCore.QRect()
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        self.icon_pixmap_fnp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_off.svg"
        )
        self._setupUI()
        self.toggle_button.stateChange.connect(None)
    
    xǁSensorWidgetǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSensorWidgetǁ__init____mutmut_1': xǁSensorWidgetǁ__init____mutmut_1, 
        'xǁSensorWidgetǁ__init____mutmut_2': xǁSensorWidgetǁ__init____mutmut_2, 
        'xǁSensorWidgetǁ__init____mutmut_3': xǁSensorWidgetǁ__init____mutmut_3, 
        'xǁSensorWidgetǁ__init____mutmut_4': xǁSensorWidgetǁ__init____mutmut_4, 
        'xǁSensorWidgetǁ__init____mutmut_5': xǁSensorWidgetǁ__init____mutmut_5, 
        'xǁSensorWidgetǁ__init____mutmut_6': xǁSensorWidgetǁ__init____mutmut_6, 
        'xǁSensorWidgetǁ__init____mutmut_7': xǁSensorWidgetǁ__init____mutmut_7, 
        'xǁSensorWidgetǁ__init____mutmut_8': xǁSensorWidgetǁ__init____mutmut_8, 
        'xǁSensorWidgetǁ__init____mutmut_9': xǁSensorWidgetǁ__init____mutmut_9, 
        'xǁSensorWidgetǁ__init____mutmut_10': xǁSensorWidgetǁ__init____mutmut_10, 
        'xǁSensorWidgetǁ__init____mutmut_11': xǁSensorWidgetǁ__init____mutmut_11, 
        'xǁSensorWidgetǁ__init____mutmut_12': xǁSensorWidgetǁ__init____mutmut_12, 
        'xǁSensorWidgetǁ__init____mutmut_13': xǁSensorWidgetǁ__init____mutmut_13, 
        'xǁSensorWidgetǁ__init____mutmut_14': xǁSensorWidgetǁ__init____mutmut_14, 
        'xǁSensorWidgetǁ__init____mutmut_15': xǁSensorWidgetǁ__init____mutmut_15, 
        'xǁSensorWidgetǁ__init____mutmut_16': xǁSensorWidgetǁ__init____mutmut_16, 
        'xǁSensorWidgetǁ__init____mutmut_17': xǁSensorWidgetǁ__init____mutmut_17, 
        'xǁSensorWidgetǁ__init____mutmut_18': xǁSensorWidgetǁ__init____mutmut_18, 
        'xǁSensorWidgetǁ__init____mutmut_19': xǁSensorWidgetǁ__init____mutmut_19, 
        'xǁSensorWidgetǁ__init____mutmut_20': xǁSensorWidgetǁ__init____mutmut_20, 
        'xǁSensorWidgetǁ__init____mutmut_21': xǁSensorWidgetǁ__init____mutmut_21, 
        'xǁSensorWidgetǁ__init____mutmut_22': xǁSensorWidgetǁ__init____mutmut_22, 
        'xǁSensorWidgetǁ__init____mutmut_23': xǁSensorWidgetǁ__init____mutmut_23, 
        'xǁSensorWidgetǁ__init____mutmut_24': xǁSensorWidgetǁ__init____mutmut_24, 
        'xǁSensorWidgetǁ__init____mutmut_25': xǁSensorWidgetǁ__init____mutmut_25, 
        'xǁSensorWidgetǁ__init____mutmut_26': xǁSensorWidgetǁ__init____mutmut_26, 
        'xǁSensorWidgetǁ__init____mutmut_27': xǁSensorWidgetǁ__init____mutmut_27, 
        'xǁSensorWidgetǁ__init____mutmut_28': xǁSensorWidgetǁ__init____mutmut_28, 
        'xǁSensorWidgetǁ__init____mutmut_29': xǁSensorWidgetǁ__init____mutmut_29, 
        'xǁSensorWidgetǁ__init____mutmut_30': xǁSensorWidgetǁ__init____mutmut_30, 
        'xǁSensorWidgetǁ__init____mutmut_31': xǁSensorWidgetǁ__init____mutmut_31, 
        'xǁSensorWidgetǁ__init____mutmut_32': xǁSensorWidgetǁ__init____mutmut_32, 
        'xǁSensorWidgetǁ__init____mutmut_33': xǁSensorWidgetǁ__init____mutmut_33, 
        'xǁSensorWidgetǁ__init____mutmut_34': xǁSensorWidgetǁ__init____mutmut_34, 
        'xǁSensorWidgetǁ__init____mutmut_35': xǁSensorWidgetǁ__init____mutmut_35, 
        'xǁSensorWidgetǁ__init____mutmut_36': xǁSensorWidgetǁ__init____mutmut_36, 
        'xǁSensorWidgetǁ__init____mutmut_37': xǁSensorWidgetǁ__init____mutmut_37, 
        'xǁSensorWidgetǁ__init____mutmut_38': xǁSensorWidgetǁ__init____mutmut_38, 
        'xǁSensorWidgetǁ__init____mutmut_39': xǁSensorWidgetǁ__init____mutmut_39, 
        'xǁSensorWidgetǁ__init____mutmut_40': xǁSensorWidgetǁ__init____mutmut_40
    }
    xǁSensorWidgetǁ__init____mutmut_orig.__name__ = 'xǁSensorWidgetǁ__init__'

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
        self.update()

    def toggle_button_state(self, state: ToggleAnimatedButton.State) -> None:
        args = [state]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSensorWidgetǁtoggle_button_state__mutmut_orig'), object.__getattribute__(self, 'xǁSensorWidgetǁtoggle_button_state__mutmut_mutants'), args, kwargs, self)

    def xǁSensorWidgetǁtoggle_button_state__mutmut_orig(self, state: ToggleAnimatedButton.State) -> None:
        """Called when the Klipper firmware reports an update to the filament sensor state"""
        self.toggle_button.setDisabled(False)
        if state.value != self.sensor_state.value:
            self.sensor_state = self.SensorState(state.value)
            self.toggle_button.state = ToggleAnimatedButton.State(
                self.sensor_state.value
            )
            self.update()

    def xǁSensorWidgetǁtoggle_button_state__mutmut_1(self, state: ToggleAnimatedButton.State) -> None:
        """Called when the Klipper firmware reports an update to the filament sensor state"""
        self.toggle_button.setDisabled(None)
        if state.value != self.sensor_state.value:
            self.sensor_state = self.SensorState(state.value)
            self.toggle_button.state = ToggleAnimatedButton.State(
                self.sensor_state.value
            )
            self.update()

    def xǁSensorWidgetǁtoggle_button_state__mutmut_2(self, state: ToggleAnimatedButton.State) -> None:
        """Called when the Klipper firmware reports an update to the filament sensor state"""
        self.toggle_button.setDisabled(True)
        if state.value != self.sensor_state.value:
            self.sensor_state = self.SensorState(state.value)
            self.toggle_button.state = ToggleAnimatedButton.State(
                self.sensor_state.value
            )
            self.update()

    def xǁSensorWidgetǁtoggle_button_state__mutmut_3(self, state: ToggleAnimatedButton.State) -> None:
        """Called when the Klipper firmware reports an update to the filament sensor state"""
        self.toggle_button.setDisabled(False)
        if state.value == self.sensor_state.value:
            self.sensor_state = self.SensorState(state.value)
            self.toggle_button.state = ToggleAnimatedButton.State(
                self.sensor_state.value
            )
            self.update()

    def xǁSensorWidgetǁtoggle_button_state__mutmut_4(self, state: ToggleAnimatedButton.State) -> None:
        """Called when the Klipper firmware reports an update to the filament sensor state"""
        self.toggle_button.setDisabled(False)
        if state.value != self.sensor_state.value:
            self.sensor_state = None
            self.toggle_button.state = ToggleAnimatedButton.State(
                self.sensor_state.value
            )
            self.update()

    def xǁSensorWidgetǁtoggle_button_state__mutmut_5(self, state: ToggleAnimatedButton.State) -> None:
        """Called when the Klipper firmware reports an update to the filament sensor state"""
        self.toggle_button.setDisabled(False)
        if state.value != self.sensor_state.value:
            self.sensor_state = self.SensorState(None)
            self.toggle_button.state = ToggleAnimatedButton.State(
                self.sensor_state.value
            )
            self.update()

    def xǁSensorWidgetǁtoggle_button_state__mutmut_6(self, state: ToggleAnimatedButton.State) -> None:
        """Called when the Klipper firmware reports an update to the filament sensor state"""
        self.toggle_button.setDisabled(False)
        if state.value != self.sensor_state.value:
            self.sensor_state = self.SensorState(state.value)
            self.toggle_button.state = None
            self.update()

    def xǁSensorWidgetǁtoggle_button_state__mutmut_7(self, state: ToggleAnimatedButton.State) -> None:
        """Called when the Klipper firmware reports an update to the filament sensor state"""
        self.toggle_button.setDisabled(False)
        if state.value != self.sensor_state.value:
            self.sensor_state = self.SensorState(state.value)
            self.toggle_button.state = ToggleAnimatedButton.State(
                None
            )
            self.update()
    
    xǁSensorWidgetǁtoggle_button_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSensorWidgetǁtoggle_button_state__mutmut_1': xǁSensorWidgetǁtoggle_button_state__mutmut_1, 
        'xǁSensorWidgetǁtoggle_button_state__mutmut_2': xǁSensorWidgetǁtoggle_button_state__mutmut_2, 
        'xǁSensorWidgetǁtoggle_button_state__mutmut_3': xǁSensorWidgetǁtoggle_button_state__mutmut_3, 
        'xǁSensorWidgetǁtoggle_button_state__mutmut_4': xǁSensorWidgetǁtoggle_button_state__mutmut_4, 
        'xǁSensorWidgetǁtoggle_button_state__mutmut_5': xǁSensorWidgetǁtoggle_button_state__mutmut_5, 
        'xǁSensorWidgetǁtoggle_button_state__mutmut_6': xǁSensorWidgetǁtoggle_button_state__mutmut_6, 
        'xǁSensorWidgetǁtoggle_button_state__mutmut_7': xǁSensorWidgetǁtoggle_button_state__mutmut_7
    }
    xǁSensorWidgetǁtoggle_button_state__mutmut_orig.__name__ = 'xǁSensorWidgetǁtoggle_button_state'

    @QtCore.pyqtSlot(ToggleAnimatedButton.State, name="state-change")
    def toggle_sensor_state(self, state: ToggleAnimatedButton.State) -> None:
        """Emit the appropriate G-Code command to change the filament sensor state."""
        if state.value != self.sensor_state.value:
            self.toggle_button.setDisabled(True)
            self.run_gcode_signal.emit(
                f"SET_FILAMENT_SENSOR SENSOR={self.text} ENABLE={int(state.value)}"
            )
            self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSensorWidgetǁresizeEvent__mutmut_orig'), object.__getattribute__(self, 'xǁSensorWidgetǁresizeEvent__mutmut_mutants'), args, kwargs, self)

    def xǁSensorWidgetǁresizeEvent__mutmut_orig(self, a0: QtGui.QResizeEvent) -> None:
        """Handle widget resize events."""
        return super().resizeEvent(a0)

    def xǁSensorWidgetǁresizeEvent__mutmut_1(self, a0: QtGui.QResizeEvent) -> None:
        """Handle widget resize events."""
        return super().resizeEvent(None)
    
    xǁSensorWidgetǁresizeEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSensorWidgetǁresizeEvent__mutmut_1': xǁSensorWidgetǁresizeEvent__mutmut_1
    }
    xǁSensorWidgetǁresizeEvent__mutmut_orig.__name__ = 'xǁSensorWidgetǁresizeEvent'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSensorWidgetǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁSensorWidgetǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁSensorWidgetǁpaintEvent__mutmut_orig(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_1(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = None
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_2(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(None)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_3(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(None, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_4(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, None)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_5(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_6(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, )
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_7(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, False)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_8(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            None, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_9(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, None
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_10(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_11(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_12(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, False
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_13(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            None, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_14(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, None
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_15(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_16(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_17(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, False
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_18(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                None
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_19(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state != self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_20(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = None
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_21(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(None)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_22(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(21)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_23(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(None)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_24(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = None
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_25(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = None
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_26(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = None

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_27(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = None
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_28(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(None, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_29(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, None)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_30(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_31(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, )
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_32(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            None,
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_33(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            None,
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_34(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            None,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_35(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            None,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_36(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            None,
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_37(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            None,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_38(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_39(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_40(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_41(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_42(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_43(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_44(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            False,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_45(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(None)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_46(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(17)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_47(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(None)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_48(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = None
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_49(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = None
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_50(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 / "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_51(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 13 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_52(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "XX\tXX"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_53(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            None,
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_54(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            None,
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_55(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            None,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_56(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            None,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_57(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            None,
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_58(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            None,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_59(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_60(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_61(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_62(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_63(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_64(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_65(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            False,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_66(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = None
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_67(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer = 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_68(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer -= 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_69(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 / "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_70(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 4 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_71(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "XX\tXX"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_72(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            None,
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_73(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            None,
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_74(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            None,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_75(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            None,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_76(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            None,
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_77(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            None,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_78(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_79(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_80(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_81(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_82(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_83(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            True,
            f"Enable: {tab_spacer}{sensor_state_text}",
            )
        style_painter.end()

    def xǁSensorWidgetǁpaintEvent__mutmut_84(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self._icon_label:
            self._icon_label.setPixmap(
                self.icon_pixmap_fp
                if self.filament_state == self.FilamentState.PRESENT
                else self.icon_pixmap_fnp
            )
        _font = QtGui.QFont()
        _font.setPointSize(20)
        style_painter.setFont(_font)

        label_name = self._text_label_name_
        label_detected = self._text_label_detected
        label_state = self._text_label_state

        palette = label_name.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        style_painter.drawItemText(
            label_name.geometry(),
            label_name.alignment(),
            palette,
            True,
            label_name.text(),
            QtGui.QPalette.ColorRole.WindowText,
        )

        _font.setPointSize(16)
        style_painter.setFont(_font)
        filament_text = self.filament_state.name.capitalize()
        tab_spacer = 12 * "\t"
        style_painter.drawItemText(
            label_state.geometry(),
            label_state.alignment(),
            palette,
            True,
            f"Filament: {tab_spacer}{filament_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )

        sensor_state_text = self.sensor_state.name.capitalize()
        tab_spacer += 3 * "\t"
        style_painter.drawItemText(
            label_detected.geometry(),
            label_detected.alignment(),
            palette,
            False,
            f"Enable: {tab_spacer}{sensor_state_text}",
            QtGui.QPalette.ColorRole.WindowText,
        )
        style_painter.end()
    
    xǁSensorWidgetǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSensorWidgetǁpaintEvent__mutmut_1': xǁSensorWidgetǁpaintEvent__mutmut_1, 
        'xǁSensorWidgetǁpaintEvent__mutmut_2': xǁSensorWidgetǁpaintEvent__mutmut_2, 
        'xǁSensorWidgetǁpaintEvent__mutmut_3': xǁSensorWidgetǁpaintEvent__mutmut_3, 
        'xǁSensorWidgetǁpaintEvent__mutmut_4': xǁSensorWidgetǁpaintEvent__mutmut_4, 
        'xǁSensorWidgetǁpaintEvent__mutmut_5': xǁSensorWidgetǁpaintEvent__mutmut_5, 
        'xǁSensorWidgetǁpaintEvent__mutmut_6': xǁSensorWidgetǁpaintEvent__mutmut_6, 
        'xǁSensorWidgetǁpaintEvent__mutmut_7': xǁSensorWidgetǁpaintEvent__mutmut_7, 
        'xǁSensorWidgetǁpaintEvent__mutmut_8': xǁSensorWidgetǁpaintEvent__mutmut_8, 
        'xǁSensorWidgetǁpaintEvent__mutmut_9': xǁSensorWidgetǁpaintEvent__mutmut_9, 
        'xǁSensorWidgetǁpaintEvent__mutmut_10': xǁSensorWidgetǁpaintEvent__mutmut_10, 
        'xǁSensorWidgetǁpaintEvent__mutmut_11': xǁSensorWidgetǁpaintEvent__mutmut_11, 
        'xǁSensorWidgetǁpaintEvent__mutmut_12': xǁSensorWidgetǁpaintEvent__mutmut_12, 
        'xǁSensorWidgetǁpaintEvent__mutmut_13': xǁSensorWidgetǁpaintEvent__mutmut_13, 
        'xǁSensorWidgetǁpaintEvent__mutmut_14': xǁSensorWidgetǁpaintEvent__mutmut_14, 
        'xǁSensorWidgetǁpaintEvent__mutmut_15': xǁSensorWidgetǁpaintEvent__mutmut_15, 
        'xǁSensorWidgetǁpaintEvent__mutmut_16': xǁSensorWidgetǁpaintEvent__mutmut_16, 
        'xǁSensorWidgetǁpaintEvent__mutmut_17': xǁSensorWidgetǁpaintEvent__mutmut_17, 
        'xǁSensorWidgetǁpaintEvent__mutmut_18': xǁSensorWidgetǁpaintEvent__mutmut_18, 
        'xǁSensorWidgetǁpaintEvent__mutmut_19': xǁSensorWidgetǁpaintEvent__mutmut_19, 
        'xǁSensorWidgetǁpaintEvent__mutmut_20': xǁSensorWidgetǁpaintEvent__mutmut_20, 
        'xǁSensorWidgetǁpaintEvent__mutmut_21': xǁSensorWidgetǁpaintEvent__mutmut_21, 
        'xǁSensorWidgetǁpaintEvent__mutmut_22': xǁSensorWidgetǁpaintEvent__mutmut_22, 
        'xǁSensorWidgetǁpaintEvent__mutmut_23': xǁSensorWidgetǁpaintEvent__mutmut_23, 
        'xǁSensorWidgetǁpaintEvent__mutmut_24': xǁSensorWidgetǁpaintEvent__mutmut_24, 
        'xǁSensorWidgetǁpaintEvent__mutmut_25': xǁSensorWidgetǁpaintEvent__mutmut_25, 
        'xǁSensorWidgetǁpaintEvent__mutmut_26': xǁSensorWidgetǁpaintEvent__mutmut_26, 
        'xǁSensorWidgetǁpaintEvent__mutmut_27': xǁSensorWidgetǁpaintEvent__mutmut_27, 
        'xǁSensorWidgetǁpaintEvent__mutmut_28': xǁSensorWidgetǁpaintEvent__mutmut_28, 
        'xǁSensorWidgetǁpaintEvent__mutmut_29': xǁSensorWidgetǁpaintEvent__mutmut_29, 
        'xǁSensorWidgetǁpaintEvent__mutmut_30': xǁSensorWidgetǁpaintEvent__mutmut_30, 
        'xǁSensorWidgetǁpaintEvent__mutmut_31': xǁSensorWidgetǁpaintEvent__mutmut_31, 
        'xǁSensorWidgetǁpaintEvent__mutmut_32': xǁSensorWidgetǁpaintEvent__mutmut_32, 
        'xǁSensorWidgetǁpaintEvent__mutmut_33': xǁSensorWidgetǁpaintEvent__mutmut_33, 
        'xǁSensorWidgetǁpaintEvent__mutmut_34': xǁSensorWidgetǁpaintEvent__mutmut_34, 
        'xǁSensorWidgetǁpaintEvent__mutmut_35': xǁSensorWidgetǁpaintEvent__mutmut_35, 
        'xǁSensorWidgetǁpaintEvent__mutmut_36': xǁSensorWidgetǁpaintEvent__mutmut_36, 
        'xǁSensorWidgetǁpaintEvent__mutmut_37': xǁSensorWidgetǁpaintEvent__mutmut_37, 
        'xǁSensorWidgetǁpaintEvent__mutmut_38': xǁSensorWidgetǁpaintEvent__mutmut_38, 
        'xǁSensorWidgetǁpaintEvent__mutmut_39': xǁSensorWidgetǁpaintEvent__mutmut_39, 
        'xǁSensorWidgetǁpaintEvent__mutmut_40': xǁSensorWidgetǁpaintEvent__mutmut_40, 
        'xǁSensorWidgetǁpaintEvent__mutmut_41': xǁSensorWidgetǁpaintEvent__mutmut_41, 
        'xǁSensorWidgetǁpaintEvent__mutmut_42': xǁSensorWidgetǁpaintEvent__mutmut_42, 
        'xǁSensorWidgetǁpaintEvent__mutmut_43': xǁSensorWidgetǁpaintEvent__mutmut_43, 
        'xǁSensorWidgetǁpaintEvent__mutmut_44': xǁSensorWidgetǁpaintEvent__mutmut_44, 
        'xǁSensorWidgetǁpaintEvent__mutmut_45': xǁSensorWidgetǁpaintEvent__mutmut_45, 
        'xǁSensorWidgetǁpaintEvent__mutmut_46': xǁSensorWidgetǁpaintEvent__mutmut_46, 
        'xǁSensorWidgetǁpaintEvent__mutmut_47': xǁSensorWidgetǁpaintEvent__mutmut_47, 
        'xǁSensorWidgetǁpaintEvent__mutmut_48': xǁSensorWidgetǁpaintEvent__mutmut_48, 
        'xǁSensorWidgetǁpaintEvent__mutmut_49': xǁSensorWidgetǁpaintEvent__mutmut_49, 
        'xǁSensorWidgetǁpaintEvent__mutmut_50': xǁSensorWidgetǁpaintEvent__mutmut_50, 
        'xǁSensorWidgetǁpaintEvent__mutmut_51': xǁSensorWidgetǁpaintEvent__mutmut_51, 
        'xǁSensorWidgetǁpaintEvent__mutmut_52': xǁSensorWidgetǁpaintEvent__mutmut_52, 
        'xǁSensorWidgetǁpaintEvent__mutmut_53': xǁSensorWidgetǁpaintEvent__mutmut_53, 
        'xǁSensorWidgetǁpaintEvent__mutmut_54': xǁSensorWidgetǁpaintEvent__mutmut_54, 
        'xǁSensorWidgetǁpaintEvent__mutmut_55': xǁSensorWidgetǁpaintEvent__mutmut_55, 
        'xǁSensorWidgetǁpaintEvent__mutmut_56': xǁSensorWidgetǁpaintEvent__mutmut_56, 
        'xǁSensorWidgetǁpaintEvent__mutmut_57': xǁSensorWidgetǁpaintEvent__mutmut_57, 
        'xǁSensorWidgetǁpaintEvent__mutmut_58': xǁSensorWidgetǁpaintEvent__mutmut_58, 
        'xǁSensorWidgetǁpaintEvent__mutmut_59': xǁSensorWidgetǁpaintEvent__mutmut_59, 
        'xǁSensorWidgetǁpaintEvent__mutmut_60': xǁSensorWidgetǁpaintEvent__mutmut_60, 
        'xǁSensorWidgetǁpaintEvent__mutmut_61': xǁSensorWidgetǁpaintEvent__mutmut_61, 
        'xǁSensorWidgetǁpaintEvent__mutmut_62': xǁSensorWidgetǁpaintEvent__mutmut_62, 
        'xǁSensorWidgetǁpaintEvent__mutmut_63': xǁSensorWidgetǁpaintEvent__mutmut_63, 
        'xǁSensorWidgetǁpaintEvent__mutmut_64': xǁSensorWidgetǁpaintEvent__mutmut_64, 
        'xǁSensorWidgetǁpaintEvent__mutmut_65': xǁSensorWidgetǁpaintEvent__mutmut_65, 
        'xǁSensorWidgetǁpaintEvent__mutmut_66': xǁSensorWidgetǁpaintEvent__mutmut_66, 
        'xǁSensorWidgetǁpaintEvent__mutmut_67': xǁSensorWidgetǁpaintEvent__mutmut_67, 
        'xǁSensorWidgetǁpaintEvent__mutmut_68': xǁSensorWidgetǁpaintEvent__mutmut_68, 
        'xǁSensorWidgetǁpaintEvent__mutmut_69': xǁSensorWidgetǁpaintEvent__mutmut_69, 
        'xǁSensorWidgetǁpaintEvent__mutmut_70': xǁSensorWidgetǁpaintEvent__mutmut_70, 
        'xǁSensorWidgetǁpaintEvent__mutmut_71': xǁSensorWidgetǁpaintEvent__mutmut_71, 
        'xǁSensorWidgetǁpaintEvent__mutmut_72': xǁSensorWidgetǁpaintEvent__mutmut_72, 
        'xǁSensorWidgetǁpaintEvent__mutmut_73': xǁSensorWidgetǁpaintEvent__mutmut_73, 
        'xǁSensorWidgetǁpaintEvent__mutmut_74': xǁSensorWidgetǁpaintEvent__mutmut_74, 
        'xǁSensorWidgetǁpaintEvent__mutmut_75': xǁSensorWidgetǁpaintEvent__mutmut_75, 
        'xǁSensorWidgetǁpaintEvent__mutmut_76': xǁSensorWidgetǁpaintEvent__mutmut_76, 
        'xǁSensorWidgetǁpaintEvent__mutmut_77': xǁSensorWidgetǁpaintEvent__mutmut_77, 
        'xǁSensorWidgetǁpaintEvent__mutmut_78': xǁSensorWidgetǁpaintEvent__mutmut_78, 
        'xǁSensorWidgetǁpaintEvent__mutmut_79': xǁSensorWidgetǁpaintEvent__mutmut_79, 
        'xǁSensorWidgetǁpaintEvent__mutmut_80': xǁSensorWidgetǁpaintEvent__mutmut_80, 
        'xǁSensorWidgetǁpaintEvent__mutmut_81': xǁSensorWidgetǁpaintEvent__mutmut_81, 
        'xǁSensorWidgetǁpaintEvent__mutmut_82': xǁSensorWidgetǁpaintEvent__mutmut_82, 
        'xǁSensorWidgetǁpaintEvent__mutmut_83': xǁSensorWidgetǁpaintEvent__mutmut_83, 
        'xǁSensorWidgetǁpaintEvent__mutmut_84': xǁSensorWidgetǁpaintEvent__mutmut_84
    }
    xǁSensorWidgetǁpaintEvent__mutmut_orig.__name__ = 'xǁSensorWidgetǁpaintEvent'

    def _setupUI(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSensorWidgetǁ_setupUI__mutmut_orig'), object.__getattribute__(self, 'xǁSensorWidgetǁ_setupUI__mutmut_mutants'), args, kwargs, self)

    def xǁSensorWidgetǁ_setupUI__mutmut_orig(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_1(self):
        _policy = None
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_2(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = None
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_3(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(None, _policy)
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_4(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, None)
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_5(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy)
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_6(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, )
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_7(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(None)
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_8(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(None)
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_9(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = None
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_10(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName(None)
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_11(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName("XXsensorVerticalLayoutXX")
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_12(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName("sensorverticallayout")
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_13(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName("SENSORVERTICALLAYOUT")
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_14(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName("sensorVerticalLayout")
        self._icon_label = None
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        parent_width = self.parentWidget().width()
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(120, 100)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_15(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName("sensorVerticalLayout")
        self._icon_label = BlocksLabel(None)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        parent_width = self.parentWidget().width()
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(120, 100)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_16(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName("sensorVerticalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(None)
        parent_width = self.parentWidget().width()
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(120, 100)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_17(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName("sensorVerticalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        parent_width = None
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(120, 100)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_18(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_vertical_layout = QtWidgets.QVBoxLayout()
        self.sensor_vertical_layout.setObjectName("sensorVerticalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        parent_width = self.parentWidget().width()
        self._icon_label.setSizePolicy(None)
        self._icon_label.setMinimumSize(120, 100)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_19(self):
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
        self._icon_label.setMinimumSize(None, 100)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_20(self):
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
        self._icon_label.setMinimumSize(120, None)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_21(self):
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
        self._icon_label.setMinimumSize(100)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_22(self):
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
        self._icon_label.setMinimumSize(120, )

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_23(self):
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
        self._icon_label.setMinimumSize(121, 100)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_24(self):
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
        self._icon_label.setMinimumSize(120, 101)

        self._icon_label.setPixmap(
            self.icon_pixmap_fp
            if self.filament_state == self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_25(self):
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
            None
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_26(self):
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
            if self.filament_state != self.FilamentState.PRESENT
            else self.icon_pixmap_fnp
        )
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_27(self):
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
        self._text_label_name_ = None
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_28(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=None)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_29(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            None
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_30(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(None, 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_31(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), None)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_32(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_33(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), )
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_34(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 41)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_35(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(None)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_36(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = None
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_37(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            None, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_38(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, None
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_39(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_40(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_41(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(None)
        self._text_label_name_.setText(str(self._text))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_42(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(None)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_43(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(None))
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

    def xǁSensorWidgetǁ_setupUI__mutmut_44(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(None)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_45(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = None
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

    def xǁSensorWidgetǁ_setupUI__mutmut_46(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=None)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_47(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            None
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

    def xǁSensorWidgetǁ_setupUI__mutmut_48(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(None, 20)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_49(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(parent_width, None)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_50(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(20)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_51(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(parent_width, )

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

    def xǁSensorWidgetǁ_setupUI__mutmut_52(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(parent_width, 21)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_53(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(parent_width, 20)

        self._text_label_detected.setPalette(None)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_54(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(parent_width, 20)

        self._text_label_detected.setPalette(palette)
        self._text_label_detected.setText(None)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_55(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(parent_width, 20)

        self._text_label_detected.setPalette(palette)
        self._text_label_detected.setText(f"Filament: {self.filament_state}")

        self._text_label_state = None
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

    def xǁSensorWidgetǁ_setupUI__mutmut_56(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
        self._icon_label.setSizePolicy(size_policy)

        self._text_label_detected = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_detected.sizePolicy().hasHeightForWidth()
        )
        self._text_label_detected.setMinimumSize(parent_width, 20)

        self._text_label_detected.setPalette(palette)
        self._text_label_detected.setText(f"Filament: {self.filament_state}")

        self._text_label_state = QtWidgets.QLabel(parent=None)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_57(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            None
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

    def xǁSensorWidgetǁ_setupUI__mutmut_58(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self._text_label_state.setMinimumSize(None, 20)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_59(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self._text_label_state.setMinimumSize(parent_width, None)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_60(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self._text_label_state.setMinimumSize(20)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_61(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self._text_label_state.setMinimumSize(parent_width, )

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

    def xǁSensorWidgetǁ_setupUI__mutmut_62(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self._text_label_state.setMinimumSize(parent_width, 21)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_63(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

        self._text_label_state.setPalette(None)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_64(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self._text_label_state.setText(None)

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

    def xǁSensorWidgetǁ_setupUI__mutmut_65(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

        self._icon_label.setSizePolicy(None)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_66(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self.toggle_button = None
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

    def xǁSensorWidgetǁ_setupUI__mutmut_67(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self.toggle_button = ToggleAnimatedButton(None)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_68(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self.toggle_button.setMinimumSize(None, 50)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_69(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self.toggle_button.setMinimumSize(100, None)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_70(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self.toggle_button.setMinimumSize(50)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_71(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self.toggle_button.setMinimumSize(100, )
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

    def xǁSensorWidgetǁ_setupUI__mutmut_72(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self.toggle_button.setMinimumSize(101, 50)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_73(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self.toggle_button.setMinimumSize(100, 51)
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

    def xǁSensorWidgetǁ_setupUI__mutmut_74(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
        self.toggle_button.state = None

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

    def xǁSensorWidgetǁ_setupUI__mutmut_75(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            None, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
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

    def xǁSensorWidgetǁ_setupUI__mutmut_76(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self._icon_label, alignment=None
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

    def xǁSensorWidgetǁ_setupUI__mutmut_77(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
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

    def xǁSensorWidgetǁ_setupUI__mutmut_78(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self._icon_label, )
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

    def xǁSensorWidgetǁ_setupUI__mutmut_79(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            None, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
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

    def xǁSensorWidgetǁ_setupUI__mutmut_80(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self._text_label_name_, alignment=None
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

    def xǁSensorWidgetǁ_setupUI__mutmut_81(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
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

    def xǁSensorWidgetǁ_setupUI__mutmut_82(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self._text_label_name_, )
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

    def xǁSensorWidgetǁ_setupUI__mutmut_83(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            None, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
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

    def xǁSensorWidgetǁ_setupUI__mutmut_84(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self._text_label_state, alignment=None
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

    def xǁSensorWidgetǁ_setupUI__mutmut_85(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft
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

    def xǁSensorWidgetǁ_setupUI__mutmut_86(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self._text_label_state, )
        self.sensor_vertical_layout.addStretch()
        self.sensor_vertical_layout.addWidget(
            self._text_label_detected, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.sensor_vertical_layout.addStretch()
        self.sensor_vertical_layout.addWidget(
            self.toggle_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(self.sensor_vertical_layout)

    def xǁSensorWidgetǁ_setupUI__mutmut_87(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            None, alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.sensor_vertical_layout.addStretch()
        self.sensor_vertical_layout.addWidget(
            self.toggle_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(self.sensor_vertical_layout)

    def xǁSensorWidgetǁ_setupUI__mutmut_88(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self._text_label_detected, alignment=None
        )
        self.sensor_vertical_layout.addStretch()
        self.sensor_vertical_layout.addWidget(
            self.toggle_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(self.sensor_vertical_layout)

    def xǁSensorWidgetǁ_setupUI__mutmut_89(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            alignment=QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.sensor_vertical_layout.addStretch()
        self.sensor_vertical_layout.addWidget(
            self.toggle_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(self.sensor_vertical_layout)

    def xǁSensorWidgetǁ_setupUI__mutmut_90(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self._text_label_detected, )
        self.sensor_vertical_layout.addStretch()
        self.sensor_vertical_layout.addWidget(
            self.toggle_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(self.sensor_vertical_layout)

    def xǁSensorWidgetǁ_setupUI__mutmut_91(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            None, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(self.sensor_vertical_layout)

    def xǁSensorWidgetǁ_setupUI__mutmut_92(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self.toggle_button, alignment=None
        )

        self.setLayout(self.sensor_vertical_layout)

    def xǁSensorWidgetǁ_setupUI__mutmut_93(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.setLayout(self.sensor_vertical_layout)

    def xǁSensorWidgetǁ_setupUI__mutmut_94(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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
            self.toggle_button, )

        self.setLayout(self.sensor_vertical_layout)

    def xǁSensorWidgetǁ_setupUI__mutmut_95(self):
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
        self._text_label_name_ = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label_name_.sizePolicy().hasHeightForWidth()
        )
        self._text_label_name_.setMinimumSize(self.rect().width(), 40)
        self._text_label_name_.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = self._text_label_name_.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.Transparent
        )
        self._text_label_name_.setPalette(palette)
        self._text_label_name_.setText(str(self._text))
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

        self.setLayout(None)
    
    xǁSensorWidgetǁ_setupUI__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSensorWidgetǁ_setupUI__mutmut_1': xǁSensorWidgetǁ_setupUI__mutmut_1, 
        'xǁSensorWidgetǁ_setupUI__mutmut_2': xǁSensorWidgetǁ_setupUI__mutmut_2, 
        'xǁSensorWidgetǁ_setupUI__mutmut_3': xǁSensorWidgetǁ_setupUI__mutmut_3, 
        'xǁSensorWidgetǁ_setupUI__mutmut_4': xǁSensorWidgetǁ_setupUI__mutmut_4, 
        'xǁSensorWidgetǁ_setupUI__mutmut_5': xǁSensorWidgetǁ_setupUI__mutmut_5, 
        'xǁSensorWidgetǁ_setupUI__mutmut_6': xǁSensorWidgetǁ_setupUI__mutmut_6, 
        'xǁSensorWidgetǁ_setupUI__mutmut_7': xǁSensorWidgetǁ_setupUI__mutmut_7, 
        'xǁSensorWidgetǁ_setupUI__mutmut_8': xǁSensorWidgetǁ_setupUI__mutmut_8, 
        'xǁSensorWidgetǁ_setupUI__mutmut_9': xǁSensorWidgetǁ_setupUI__mutmut_9, 
        'xǁSensorWidgetǁ_setupUI__mutmut_10': xǁSensorWidgetǁ_setupUI__mutmut_10, 
        'xǁSensorWidgetǁ_setupUI__mutmut_11': xǁSensorWidgetǁ_setupUI__mutmut_11, 
        'xǁSensorWidgetǁ_setupUI__mutmut_12': xǁSensorWidgetǁ_setupUI__mutmut_12, 
        'xǁSensorWidgetǁ_setupUI__mutmut_13': xǁSensorWidgetǁ_setupUI__mutmut_13, 
        'xǁSensorWidgetǁ_setupUI__mutmut_14': xǁSensorWidgetǁ_setupUI__mutmut_14, 
        'xǁSensorWidgetǁ_setupUI__mutmut_15': xǁSensorWidgetǁ_setupUI__mutmut_15, 
        'xǁSensorWidgetǁ_setupUI__mutmut_16': xǁSensorWidgetǁ_setupUI__mutmut_16, 
        'xǁSensorWidgetǁ_setupUI__mutmut_17': xǁSensorWidgetǁ_setupUI__mutmut_17, 
        'xǁSensorWidgetǁ_setupUI__mutmut_18': xǁSensorWidgetǁ_setupUI__mutmut_18, 
        'xǁSensorWidgetǁ_setupUI__mutmut_19': xǁSensorWidgetǁ_setupUI__mutmut_19, 
        'xǁSensorWidgetǁ_setupUI__mutmut_20': xǁSensorWidgetǁ_setupUI__mutmut_20, 
        'xǁSensorWidgetǁ_setupUI__mutmut_21': xǁSensorWidgetǁ_setupUI__mutmut_21, 
        'xǁSensorWidgetǁ_setupUI__mutmut_22': xǁSensorWidgetǁ_setupUI__mutmut_22, 
        'xǁSensorWidgetǁ_setupUI__mutmut_23': xǁSensorWidgetǁ_setupUI__mutmut_23, 
        'xǁSensorWidgetǁ_setupUI__mutmut_24': xǁSensorWidgetǁ_setupUI__mutmut_24, 
        'xǁSensorWidgetǁ_setupUI__mutmut_25': xǁSensorWidgetǁ_setupUI__mutmut_25, 
        'xǁSensorWidgetǁ_setupUI__mutmut_26': xǁSensorWidgetǁ_setupUI__mutmut_26, 
        'xǁSensorWidgetǁ_setupUI__mutmut_27': xǁSensorWidgetǁ_setupUI__mutmut_27, 
        'xǁSensorWidgetǁ_setupUI__mutmut_28': xǁSensorWidgetǁ_setupUI__mutmut_28, 
        'xǁSensorWidgetǁ_setupUI__mutmut_29': xǁSensorWidgetǁ_setupUI__mutmut_29, 
        'xǁSensorWidgetǁ_setupUI__mutmut_30': xǁSensorWidgetǁ_setupUI__mutmut_30, 
        'xǁSensorWidgetǁ_setupUI__mutmut_31': xǁSensorWidgetǁ_setupUI__mutmut_31, 
        'xǁSensorWidgetǁ_setupUI__mutmut_32': xǁSensorWidgetǁ_setupUI__mutmut_32, 
        'xǁSensorWidgetǁ_setupUI__mutmut_33': xǁSensorWidgetǁ_setupUI__mutmut_33, 
        'xǁSensorWidgetǁ_setupUI__mutmut_34': xǁSensorWidgetǁ_setupUI__mutmut_34, 
        'xǁSensorWidgetǁ_setupUI__mutmut_35': xǁSensorWidgetǁ_setupUI__mutmut_35, 
        'xǁSensorWidgetǁ_setupUI__mutmut_36': xǁSensorWidgetǁ_setupUI__mutmut_36, 
        'xǁSensorWidgetǁ_setupUI__mutmut_37': xǁSensorWidgetǁ_setupUI__mutmut_37, 
        'xǁSensorWidgetǁ_setupUI__mutmut_38': xǁSensorWidgetǁ_setupUI__mutmut_38, 
        'xǁSensorWidgetǁ_setupUI__mutmut_39': xǁSensorWidgetǁ_setupUI__mutmut_39, 
        'xǁSensorWidgetǁ_setupUI__mutmut_40': xǁSensorWidgetǁ_setupUI__mutmut_40, 
        'xǁSensorWidgetǁ_setupUI__mutmut_41': xǁSensorWidgetǁ_setupUI__mutmut_41, 
        'xǁSensorWidgetǁ_setupUI__mutmut_42': xǁSensorWidgetǁ_setupUI__mutmut_42, 
        'xǁSensorWidgetǁ_setupUI__mutmut_43': xǁSensorWidgetǁ_setupUI__mutmut_43, 
        'xǁSensorWidgetǁ_setupUI__mutmut_44': xǁSensorWidgetǁ_setupUI__mutmut_44, 
        'xǁSensorWidgetǁ_setupUI__mutmut_45': xǁSensorWidgetǁ_setupUI__mutmut_45, 
        'xǁSensorWidgetǁ_setupUI__mutmut_46': xǁSensorWidgetǁ_setupUI__mutmut_46, 
        'xǁSensorWidgetǁ_setupUI__mutmut_47': xǁSensorWidgetǁ_setupUI__mutmut_47, 
        'xǁSensorWidgetǁ_setupUI__mutmut_48': xǁSensorWidgetǁ_setupUI__mutmut_48, 
        'xǁSensorWidgetǁ_setupUI__mutmut_49': xǁSensorWidgetǁ_setupUI__mutmut_49, 
        'xǁSensorWidgetǁ_setupUI__mutmut_50': xǁSensorWidgetǁ_setupUI__mutmut_50, 
        'xǁSensorWidgetǁ_setupUI__mutmut_51': xǁSensorWidgetǁ_setupUI__mutmut_51, 
        'xǁSensorWidgetǁ_setupUI__mutmut_52': xǁSensorWidgetǁ_setupUI__mutmut_52, 
        'xǁSensorWidgetǁ_setupUI__mutmut_53': xǁSensorWidgetǁ_setupUI__mutmut_53, 
        'xǁSensorWidgetǁ_setupUI__mutmut_54': xǁSensorWidgetǁ_setupUI__mutmut_54, 
        'xǁSensorWidgetǁ_setupUI__mutmut_55': xǁSensorWidgetǁ_setupUI__mutmut_55, 
        'xǁSensorWidgetǁ_setupUI__mutmut_56': xǁSensorWidgetǁ_setupUI__mutmut_56, 
        'xǁSensorWidgetǁ_setupUI__mutmut_57': xǁSensorWidgetǁ_setupUI__mutmut_57, 
        'xǁSensorWidgetǁ_setupUI__mutmut_58': xǁSensorWidgetǁ_setupUI__mutmut_58, 
        'xǁSensorWidgetǁ_setupUI__mutmut_59': xǁSensorWidgetǁ_setupUI__mutmut_59, 
        'xǁSensorWidgetǁ_setupUI__mutmut_60': xǁSensorWidgetǁ_setupUI__mutmut_60, 
        'xǁSensorWidgetǁ_setupUI__mutmut_61': xǁSensorWidgetǁ_setupUI__mutmut_61, 
        'xǁSensorWidgetǁ_setupUI__mutmut_62': xǁSensorWidgetǁ_setupUI__mutmut_62, 
        'xǁSensorWidgetǁ_setupUI__mutmut_63': xǁSensorWidgetǁ_setupUI__mutmut_63, 
        'xǁSensorWidgetǁ_setupUI__mutmut_64': xǁSensorWidgetǁ_setupUI__mutmut_64, 
        'xǁSensorWidgetǁ_setupUI__mutmut_65': xǁSensorWidgetǁ_setupUI__mutmut_65, 
        'xǁSensorWidgetǁ_setupUI__mutmut_66': xǁSensorWidgetǁ_setupUI__mutmut_66, 
        'xǁSensorWidgetǁ_setupUI__mutmut_67': xǁSensorWidgetǁ_setupUI__mutmut_67, 
        'xǁSensorWidgetǁ_setupUI__mutmut_68': xǁSensorWidgetǁ_setupUI__mutmut_68, 
        'xǁSensorWidgetǁ_setupUI__mutmut_69': xǁSensorWidgetǁ_setupUI__mutmut_69, 
        'xǁSensorWidgetǁ_setupUI__mutmut_70': xǁSensorWidgetǁ_setupUI__mutmut_70, 
        'xǁSensorWidgetǁ_setupUI__mutmut_71': xǁSensorWidgetǁ_setupUI__mutmut_71, 
        'xǁSensorWidgetǁ_setupUI__mutmut_72': xǁSensorWidgetǁ_setupUI__mutmut_72, 
        'xǁSensorWidgetǁ_setupUI__mutmut_73': xǁSensorWidgetǁ_setupUI__mutmut_73, 
        'xǁSensorWidgetǁ_setupUI__mutmut_74': xǁSensorWidgetǁ_setupUI__mutmut_74, 
        'xǁSensorWidgetǁ_setupUI__mutmut_75': xǁSensorWidgetǁ_setupUI__mutmut_75, 
        'xǁSensorWidgetǁ_setupUI__mutmut_76': xǁSensorWidgetǁ_setupUI__mutmut_76, 
        'xǁSensorWidgetǁ_setupUI__mutmut_77': xǁSensorWidgetǁ_setupUI__mutmut_77, 
        'xǁSensorWidgetǁ_setupUI__mutmut_78': xǁSensorWidgetǁ_setupUI__mutmut_78, 
        'xǁSensorWidgetǁ_setupUI__mutmut_79': xǁSensorWidgetǁ_setupUI__mutmut_79, 
        'xǁSensorWidgetǁ_setupUI__mutmut_80': xǁSensorWidgetǁ_setupUI__mutmut_80, 
        'xǁSensorWidgetǁ_setupUI__mutmut_81': xǁSensorWidgetǁ_setupUI__mutmut_81, 
        'xǁSensorWidgetǁ_setupUI__mutmut_82': xǁSensorWidgetǁ_setupUI__mutmut_82, 
        'xǁSensorWidgetǁ_setupUI__mutmut_83': xǁSensorWidgetǁ_setupUI__mutmut_83, 
        'xǁSensorWidgetǁ_setupUI__mutmut_84': xǁSensorWidgetǁ_setupUI__mutmut_84, 
        'xǁSensorWidgetǁ_setupUI__mutmut_85': xǁSensorWidgetǁ_setupUI__mutmut_85, 
        'xǁSensorWidgetǁ_setupUI__mutmut_86': xǁSensorWidgetǁ_setupUI__mutmut_86, 
        'xǁSensorWidgetǁ_setupUI__mutmut_87': xǁSensorWidgetǁ_setupUI__mutmut_87, 
        'xǁSensorWidgetǁ_setupUI__mutmut_88': xǁSensorWidgetǁ_setupUI__mutmut_88, 
        'xǁSensorWidgetǁ_setupUI__mutmut_89': xǁSensorWidgetǁ_setupUI__mutmut_89, 
        'xǁSensorWidgetǁ_setupUI__mutmut_90': xǁSensorWidgetǁ_setupUI__mutmut_90, 
        'xǁSensorWidgetǁ_setupUI__mutmut_91': xǁSensorWidgetǁ_setupUI__mutmut_91, 
        'xǁSensorWidgetǁ_setupUI__mutmut_92': xǁSensorWidgetǁ_setupUI__mutmut_92, 
        'xǁSensorWidgetǁ_setupUI__mutmut_93': xǁSensorWidgetǁ_setupUI__mutmut_93, 
        'xǁSensorWidgetǁ_setupUI__mutmut_94': xǁSensorWidgetǁ_setupUI__mutmut_94, 
        'xǁSensorWidgetǁ_setupUI__mutmut_95': xǁSensorWidgetǁ_setupUI__mutmut_95
    }
    xǁSensorWidgetǁ_setupUI__mutmut_orig.__name__ = 'xǁSensorWidgetǁ_setupUI'
