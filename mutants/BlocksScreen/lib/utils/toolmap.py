from PyQt6 import QtWidgets, QtGui, QtCore
from enum import IntEnum
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


class FilamentPos(IntEnum):
    """State-machine position of the filament inside the MMU/extruder path."""

    UNKNOWN = -1
    UNLOADED = 0
    HOMED_GATE = 1
    START_BOWDEN = 2
    IN_BOWDEN = 3
    END_BOWDEN = 4
    HOMED_ENTRY = 5
    HOMED_EXTRUDER = 6
    EXTRUDER_ENTRY = 7
    HOMED_TS = 8
    IN_EXTRUDER = 9
    LOADED = 10


class FilamentPathWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentPathWidgetǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁFilamentPathWidgetǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁFilamentPathWidgetǁ__init____mutmut_orig(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_1(self, parent=None):
        super().__init__(None)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_2(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = None
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_3(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = None
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_4(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "XXT0XX"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_5(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "t0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_6(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = None
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_7(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 1.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_8(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = None
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_9(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 1.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_10(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = None
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_11(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(None, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_12(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, None)
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_13(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_14(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, )
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_15(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"XXanimationProgressXX")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_16(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationprogress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_17(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"ANIMATIONPROGRESS")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_18(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(None)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_19(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(801)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_20(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(None)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_21(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = None
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_22(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(None, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_23(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, None, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_24(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, None)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_25(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_26(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_27(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, )
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_28(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(101, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_29(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 201, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_30(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 256)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_31(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = None
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_32(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(None, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_33(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, None, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_34(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, None)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_35(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_36(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_37(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, )
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_38(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(181, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_39(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 181, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_40(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 181)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_41(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = None
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_42(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont(None, 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_43(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", None)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_44(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont(9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_45(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", )
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_46(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("XXSegoe UIXX", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_47(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("segoe ui", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_48(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("SEGOE UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_49(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 10)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_50(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(None)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_51(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(False)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_52(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(None, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_53(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, None)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_54(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_55(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, )
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_56(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(61, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_57(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 201)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_58(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            None,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_59(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            None
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_60(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding
        )
    def xǁFilamentPathWidgetǁ__init____mutmut_61(self, parent=None):
        super().__init__(parent)
        
        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"
        
        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)
        
        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)
        
        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)
        
        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            )
    
    xǁFilamentPathWidgetǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentPathWidgetǁ__init____mutmut_1': xǁFilamentPathWidgetǁ__init____mutmut_1, 
        'xǁFilamentPathWidgetǁ__init____mutmut_2': xǁFilamentPathWidgetǁ__init____mutmut_2, 
        'xǁFilamentPathWidgetǁ__init____mutmut_3': xǁFilamentPathWidgetǁ__init____mutmut_3, 
        'xǁFilamentPathWidgetǁ__init____mutmut_4': xǁFilamentPathWidgetǁ__init____mutmut_4, 
        'xǁFilamentPathWidgetǁ__init____mutmut_5': xǁFilamentPathWidgetǁ__init____mutmut_5, 
        'xǁFilamentPathWidgetǁ__init____mutmut_6': xǁFilamentPathWidgetǁ__init____mutmut_6, 
        'xǁFilamentPathWidgetǁ__init____mutmut_7': xǁFilamentPathWidgetǁ__init____mutmut_7, 
        'xǁFilamentPathWidgetǁ__init____mutmut_8': xǁFilamentPathWidgetǁ__init____mutmut_8, 
        'xǁFilamentPathWidgetǁ__init____mutmut_9': xǁFilamentPathWidgetǁ__init____mutmut_9, 
        'xǁFilamentPathWidgetǁ__init____mutmut_10': xǁFilamentPathWidgetǁ__init____mutmut_10, 
        'xǁFilamentPathWidgetǁ__init____mutmut_11': xǁFilamentPathWidgetǁ__init____mutmut_11, 
        'xǁFilamentPathWidgetǁ__init____mutmut_12': xǁFilamentPathWidgetǁ__init____mutmut_12, 
        'xǁFilamentPathWidgetǁ__init____mutmut_13': xǁFilamentPathWidgetǁ__init____mutmut_13, 
        'xǁFilamentPathWidgetǁ__init____mutmut_14': xǁFilamentPathWidgetǁ__init____mutmut_14, 
        'xǁFilamentPathWidgetǁ__init____mutmut_15': xǁFilamentPathWidgetǁ__init____mutmut_15, 
        'xǁFilamentPathWidgetǁ__init____mutmut_16': xǁFilamentPathWidgetǁ__init____mutmut_16, 
        'xǁFilamentPathWidgetǁ__init____mutmut_17': xǁFilamentPathWidgetǁ__init____mutmut_17, 
        'xǁFilamentPathWidgetǁ__init____mutmut_18': xǁFilamentPathWidgetǁ__init____mutmut_18, 
        'xǁFilamentPathWidgetǁ__init____mutmut_19': xǁFilamentPathWidgetǁ__init____mutmut_19, 
        'xǁFilamentPathWidgetǁ__init____mutmut_20': xǁFilamentPathWidgetǁ__init____mutmut_20, 
        'xǁFilamentPathWidgetǁ__init____mutmut_21': xǁFilamentPathWidgetǁ__init____mutmut_21, 
        'xǁFilamentPathWidgetǁ__init____mutmut_22': xǁFilamentPathWidgetǁ__init____mutmut_22, 
        'xǁFilamentPathWidgetǁ__init____mutmut_23': xǁFilamentPathWidgetǁ__init____mutmut_23, 
        'xǁFilamentPathWidgetǁ__init____mutmut_24': xǁFilamentPathWidgetǁ__init____mutmut_24, 
        'xǁFilamentPathWidgetǁ__init____mutmut_25': xǁFilamentPathWidgetǁ__init____mutmut_25, 
        'xǁFilamentPathWidgetǁ__init____mutmut_26': xǁFilamentPathWidgetǁ__init____mutmut_26, 
        'xǁFilamentPathWidgetǁ__init____mutmut_27': xǁFilamentPathWidgetǁ__init____mutmut_27, 
        'xǁFilamentPathWidgetǁ__init____mutmut_28': xǁFilamentPathWidgetǁ__init____mutmut_28, 
        'xǁFilamentPathWidgetǁ__init____mutmut_29': xǁFilamentPathWidgetǁ__init____mutmut_29, 
        'xǁFilamentPathWidgetǁ__init____mutmut_30': xǁFilamentPathWidgetǁ__init____mutmut_30, 
        'xǁFilamentPathWidgetǁ__init____mutmut_31': xǁFilamentPathWidgetǁ__init____mutmut_31, 
        'xǁFilamentPathWidgetǁ__init____mutmut_32': xǁFilamentPathWidgetǁ__init____mutmut_32, 
        'xǁFilamentPathWidgetǁ__init____mutmut_33': xǁFilamentPathWidgetǁ__init____mutmut_33, 
        'xǁFilamentPathWidgetǁ__init____mutmut_34': xǁFilamentPathWidgetǁ__init____mutmut_34, 
        'xǁFilamentPathWidgetǁ__init____mutmut_35': xǁFilamentPathWidgetǁ__init____mutmut_35, 
        'xǁFilamentPathWidgetǁ__init____mutmut_36': xǁFilamentPathWidgetǁ__init____mutmut_36, 
        'xǁFilamentPathWidgetǁ__init____mutmut_37': xǁFilamentPathWidgetǁ__init____mutmut_37, 
        'xǁFilamentPathWidgetǁ__init____mutmut_38': xǁFilamentPathWidgetǁ__init____mutmut_38, 
        'xǁFilamentPathWidgetǁ__init____mutmut_39': xǁFilamentPathWidgetǁ__init____mutmut_39, 
        'xǁFilamentPathWidgetǁ__init____mutmut_40': xǁFilamentPathWidgetǁ__init____mutmut_40, 
        'xǁFilamentPathWidgetǁ__init____mutmut_41': xǁFilamentPathWidgetǁ__init____mutmut_41, 
        'xǁFilamentPathWidgetǁ__init____mutmut_42': xǁFilamentPathWidgetǁ__init____mutmut_42, 
        'xǁFilamentPathWidgetǁ__init____mutmut_43': xǁFilamentPathWidgetǁ__init____mutmut_43, 
        'xǁFilamentPathWidgetǁ__init____mutmut_44': xǁFilamentPathWidgetǁ__init____mutmut_44, 
        'xǁFilamentPathWidgetǁ__init____mutmut_45': xǁFilamentPathWidgetǁ__init____mutmut_45, 
        'xǁFilamentPathWidgetǁ__init____mutmut_46': xǁFilamentPathWidgetǁ__init____mutmut_46, 
        'xǁFilamentPathWidgetǁ__init____mutmut_47': xǁFilamentPathWidgetǁ__init____mutmut_47, 
        'xǁFilamentPathWidgetǁ__init____mutmut_48': xǁFilamentPathWidgetǁ__init____mutmut_48, 
        'xǁFilamentPathWidgetǁ__init____mutmut_49': xǁFilamentPathWidgetǁ__init____mutmut_49, 
        'xǁFilamentPathWidgetǁ__init____mutmut_50': xǁFilamentPathWidgetǁ__init____mutmut_50, 
        'xǁFilamentPathWidgetǁ__init____mutmut_51': xǁFilamentPathWidgetǁ__init____mutmut_51, 
        'xǁFilamentPathWidgetǁ__init____mutmut_52': xǁFilamentPathWidgetǁ__init____mutmut_52, 
        'xǁFilamentPathWidgetǁ__init____mutmut_53': xǁFilamentPathWidgetǁ__init____mutmut_53, 
        'xǁFilamentPathWidgetǁ__init____mutmut_54': xǁFilamentPathWidgetǁ__init____mutmut_54, 
        'xǁFilamentPathWidgetǁ__init____mutmut_55': xǁFilamentPathWidgetǁ__init____mutmut_55, 
        'xǁFilamentPathWidgetǁ__init____mutmut_56': xǁFilamentPathWidgetǁ__init____mutmut_56, 
        'xǁFilamentPathWidgetǁ__init____mutmut_57': xǁFilamentPathWidgetǁ__init____mutmut_57, 
        'xǁFilamentPathWidgetǁ__init____mutmut_58': xǁFilamentPathWidgetǁ__init____mutmut_58, 
        'xǁFilamentPathWidgetǁ__init____mutmut_59': xǁFilamentPathWidgetǁ__init____mutmut_59, 
        'xǁFilamentPathWidgetǁ__init____mutmut_60': xǁFilamentPathWidgetǁ__init____mutmut_60, 
        'xǁFilamentPathWidgetǁ__init____mutmut_61': xǁFilamentPathWidgetǁ__init____mutmut_61
    }
    xǁFilamentPathWidgetǁ__init____mutmut_orig.__name__ = 'xǁFilamentPathWidgetǁ__init__'

    @QtCore.pyqtProperty(float)
    def animationProgress(self):
        """Property for QPropertyAnimation"""
        return self._animation_progress

    @animationProgress.setter
    def animationProgress(self, value):
        """Setter for animation progress - triggers repaint"""
        self._animation_progress = value
        self.update()

    def set_filament_position(self, position: FilamentPos) -> None:
        args = [position]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentPathWidgetǁset_filament_position__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentPathWidgetǁset_filament_position__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentPathWidgetǁset_filament_position__mutmut_orig(self, position: FilamentPos) -> None:
        """Set the current filament position with smooth animation"""
        self.filament_position = position
        
        # Get target percentage
        target = self._get_position_percentage(position)
        
        # Animate from current progress to target
        self._animation.stop()
        self._animation.setStartValue(self._animation_progress)
        self._animation.setEndValue(target)
        self._animation.start()

    def xǁFilamentPathWidgetǁset_filament_position__mutmut_1(self, position: FilamentPos) -> None:
        """Set the current filament position with smooth animation"""
        self.filament_position = None
        
        # Get target percentage
        target = self._get_position_percentage(position)
        
        # Animate from current progress to target
        self._animation.stop()
        self._animation.setStartValue(self._animation_progress)
        self._animation.setEndValue(target)
        self._animation.start()

    def xǁFilamentPathWidgetǁset_filament_position__mutmut_2(self, position: FilamentPos) -> None:
        """Set the current filament position with smooth animation"""
        self.filament_position = position
        
        # Get target percentage
        target = None
        
        # Animate from current progress to target
        self._animation.stop()
        self._animation.setStartValue(self._animation_progress)
        self._animation.setEndValue(target)
        self._animation.start()

    def xǁFilamentPathWidgetǁset_filament_position__mutmut_3(self, position: FilamentPos) -> None:
        """Set the current filament position with smooth animation"""
        self.filament_position = position
        
        # Get target percentage
        target = self._get_position_percentage(None)
        
        # Animate from current progress to target
        self._animation.stop()
        self._animation.setStartValue(self._animation_progress)
        self._animation.setEndValue(target)
        self._animation.start()

    def xǁFilamentPathWidgetǁset_filament_position__mutmut_4(self, position: FilamentPos) -> None:
        """Set the current filament position with smooth animation"""
        self.filament_position = position
        
        # Get target percentage
        target = self._get_position_percentage(position)
        
        # Animate from current progress to target
        self._animation.stop()
        self._animation.setStartValue(None)
        self._animation.setEndValue(target)
        self._animation.start()

    def xǁFilamentPathWidgetǁset_filament_position__mutmut_5(self, position: FilamentPos) -> None:
        """Set the current filament position with smooth animation"""
        self.filament_position = position
        
        # Get target percentage
        target = self._get_position_percentage(position)
        
        # Animate from current progress to target
        self._animation.stop()
        self._animation.setStartValue(self._animation_progress)
        self._animation.setEndValue(None)
        self._animation.start()
    
    xǁFilamentPathWidgetǁset_filament_position__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentPathWidgetǁset_filament_position__mutmut_1': xǁFilamentPathWidgetǁset_filament_position__mutmut_1, 
        'xǁFilamentPathWidgetǁset_filament_position__mutmut_2': xǁFilamentPathWidgetǁset_filament_position__mutmut_2, 
        'xǁFilamentPathWidgetǁset_filament_position__mutmut_3': xǁFilamentPathWidgetǁset_filament_position__mutmut_3, 
        'xǁFilamentPathWidgetǁset_filament_position__mutmut_4': xǁFilamentPathWidgetǁset_filament_position__mutmut_4, 
        'xǁFilamentPathWidgetǁset_filament_position__mutmut_5': xǁFilamentPathWidgetǁset_filament_position__mutmut_5
    }
    xǁFilamentPathWidgetǁset_filament_position__mutmut_orig.__name__ = 'xǁFilamentPathWidgetǁset_filament_position'

    def set_gate_name(self, name: str) -> None:
        args = [name]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentPathWidgetǁset_gate_name__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentPathWidgetǁset_gate_name__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentPathWidgetǁset_gate_name__mutmut_orig(self, name: str) -> None:
        """Set the gate/tool name"""
        self.gate_name = name
        self.update()

    def xǁFilamentPathWidgetǁset_gate_name__mutmut_1(self, name: str) -> None:
        """Set the gate/tool name"""
        self.gate_name = None
        self.update()
    
    xǁFilamentPathWidgetǁset_gate_name__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentPathWidgetǁset_gate_name__mutmut_1': xǁFilamentPathWidgetǁset_gate_name__mutmut_1
    }
    xǁFilamentPathWidgetǁset_gate_name__mutmut_orig.__name__ = 'xǁFilamentPathWidgetǁset_gate_name'

    def _get_position_percentage(self, position: FilamentPos) -> float:
        args = [position]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_orig(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_1(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = None
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_2(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 1.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_3(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 1.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_4(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 1.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_5(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 1.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_6(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 1.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_7(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 1.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_8(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 1.7,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_9(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 1.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_10(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 1.8,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_11(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 1.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_12(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 1.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_13(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 2.0,
        }
        return position_map.get(position, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_14(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(None, 0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_15(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, None)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_16(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(0.0)

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_17(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, )

    def xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_18(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        position_map = {
            FilamentPos.UNKNOWN: 0.0,
            FilamentPos.UNLOADED: 0.0,
            FilamentPos.HOMED_GATE: 0.15,
            FilamentPos.START_BOWDEN: 0.25,
            FilamentPos.IN_BOWDEN: 0.45,
            FilamentPos.END_BOWDEN: 0.65,
            FilamentPos.HOMED_ENTRY: 0.70,
            FilamentPos.HOMED_EXTRUDER: 0.75,
            FilamentPos.EXTRUDER_ENTRY: 0.80,
            FilamentPos.HOMED_TS: 0.85,
            FilamentPos.IN_EXTRUDER: 0.92,
            FilamentPos.LOADED: 1.0,
        }
        return position_map.get(position, 1.0)
    
    xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_1': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_1, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_2': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_2, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_3': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_3, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_4': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_4, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_5': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_5, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_6': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_6, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_7': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_7, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_8': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_8, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_9': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_9, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_10': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_10, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_11': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_11, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_12': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_12, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_13': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_13, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_14': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_14, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_15': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_15, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_16': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_16, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_17': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_17, 
        'xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_18': xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_18
    }
    xǁFilamentPathWidgetǁ_get_position_percentage__mutmut_orig.__name__ = 'xǁFilamentPathWidgetǁ_get_position_percentage'

    def _draw_vertical_path(self, painter: QtGui.QPainter) -> None:
        args = [painter]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_orig(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_1(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = None
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_2(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = None
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_3(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 31
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_4(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = None
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_5(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 31
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_6(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = None
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_7(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 31
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_8(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = None
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_9(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(None)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_10(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 + bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_11(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() * 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_12(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 3 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_13(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width * 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_14(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 3)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_15(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = None
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_16(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = None
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_17(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin + bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_18(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() + top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_19(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = None
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_20(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(None, 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_21(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), None)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_22(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_23(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), )
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_24(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(None, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_25(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, None, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_26(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, None), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_27(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_28(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_29(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, ), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_30(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(41, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_31(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 41, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_32(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 41), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_33(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 3)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_34(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(None)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_35(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(None)
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_36(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(None, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_37(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, None, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_38(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, None))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_39(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_40(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_41(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, ))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_42(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(26, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_43(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 26, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_44(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 26))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_45(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = None
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_46(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(None, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_47(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, None, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_48(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, None, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_49(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, None)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_50(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_51(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_52(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_53(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, )
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_54(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(None)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_55(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress >= 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_56(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 1.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_57(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = None
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_58(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress / bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_59(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(None)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_60(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(None)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_61(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = None
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_62(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                None, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_63(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                None, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_64(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                None, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_65(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                None
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_66(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_67(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_68(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_69(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_70(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(None)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_71(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = None
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_72(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x - bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_73(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width * 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_74(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 3
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_75(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = None
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_76(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(None)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_77(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(None, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_78(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, None))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_79(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_80(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, ))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_81(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 3))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_82(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(None)
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_83(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(None, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_84(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, None, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_85(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, None))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_86(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_87(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_88(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, ))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_89(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(26, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_90(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 26, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_91(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 26))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_92(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(None, 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_93(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), None, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_94(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, None)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_95(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_96(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_97(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, )
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_98(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(None, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_99(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, None), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_100(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_101(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, ), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_102(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 6, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_103(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 6)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_104(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = None
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_105(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y - bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_106(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height / 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_107(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 1.7
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_108(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = None
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_109(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 41
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_110(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = None
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_111(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y + box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_112(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height * 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_113(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 3
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_114(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = None
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_115(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(None, 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_116(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), None)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_117(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_118(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), )
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_119(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(None, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_120(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, None, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_121(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, None), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_122(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_123(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_124(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, ), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_125(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(1, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_126(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 151, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_127(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 151), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_128(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 3)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_129(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(None)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_130(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(None)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_131(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = None
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_132(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(None, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_133(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, None, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_134(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, None, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_135(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, None)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_136(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_137(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_138(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_139(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, )
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_140(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x + 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_141(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 4, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_142(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width - 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_143(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 7, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_144(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(None)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_145(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = None
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_146(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y - bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_147(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(None)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_148(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(None, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_149(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, None))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_150(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_151(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, ))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_152(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 3))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_153(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(None)
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_154(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(None, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_155(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, None, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_156(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, None))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_157(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_158(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_159(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, ))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_160(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(26, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_161(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 26, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_162(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 26))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_163(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(None, 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_164(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), None, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_165(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, None)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_166(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_167(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_168(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, )

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_169(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(None, hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_170(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, None), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_171(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(hub_y), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_172(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, ), 5, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_173(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 6, 5)

    def xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_174(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()
        
        top_margin = 30
        bottom_margin = 30
        
        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin
        
        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))
        
        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)
        
        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height
            
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)
            
            fill_rect = QtCore.QRectF(
                bar_x, 
                bar_y, 
                bar_width, 
                fill_height
            )
            painter.drawRect(fill_rect)
        
        # Draw position nodes
        center_x = bar_x + bar_width / 2
        
        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)
        
        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2
        
        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)
        
        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 6)
    
    xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_1': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_1, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_2': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_2, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_3': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_3, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_4': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_4, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_5': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_5, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_6': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_6, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_7': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_7, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_8': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_8, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_9': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_9, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_10': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_10, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_11': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_11, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_12': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_12, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_13': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_13, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_14': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_14, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_15': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_15, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_16': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_16, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_17': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_17, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_18': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_18, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_19': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_19, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_20': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_20, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_21': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_21, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_22': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_22, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_23': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_23, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_24': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_24, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_25': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_25, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_26': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_26, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_27': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_27, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_28': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_28, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_29': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_29, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_30': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_30, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_31': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_31, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_32': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_32, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_33': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_33, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_34': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_34, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_35': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_35, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_36': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_36, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_37': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_37, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_38': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_38, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_39': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_39, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_40': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_40, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_41': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_41, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_42': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_42, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_43': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_43, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_44': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_44, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_45': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_45, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_46': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_46, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_47': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_47, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_48': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_48, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_49': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_49, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_50': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_50, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_51': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_51, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_52': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_52, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_53': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_53, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_54': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_54, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_55': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_55, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_56': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_56, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_57': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_57, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_58': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_58, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_59': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_59, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_60': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_60, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_61': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_61, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_62': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_62, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_63': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_63, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_64': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_64, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_65': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_65, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_66': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_66, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_67': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_67, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_68': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_68, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_69': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_69, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_70': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_70, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_71': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_71, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_72': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_72, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_73': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_73, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_74': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_74, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_75': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_75, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_76': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_76, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_77': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_77, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_78': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_78, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_79': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_79, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_80': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_80, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_81': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_81, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_82': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_82, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_83': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_83, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_84': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_84, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_85': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_85, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_86': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_86, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_87': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_87, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_88': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_88, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_89': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_89, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_90': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_90, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_91': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_91, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_92': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_92, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_93': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_93, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_94': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_94, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_95': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_95, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_96': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_96, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_97': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_97, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_98': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_98, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_99': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_99, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_100': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_100, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_101': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_101, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_102': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_102, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_103': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_103, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_104': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_104, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_105': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_105, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_106': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_106, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_107': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_107, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_108': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_108, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_109': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_109, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_110': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_110, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_111': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_111, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_112': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_112, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_113': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_113, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_114': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_114, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_115': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_115, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_116': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_116, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_117': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_117, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_118': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_118, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_119': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_119, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_120': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_120, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_121': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_121, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_122': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_122, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_123': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_123, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_124': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_124, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_125': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_125, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_126': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_126, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_127': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_127, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_128': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_128, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_129': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_129, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_130': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_130, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_131': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_131, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_132': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_132, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_133': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_133, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_134': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_134, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_135': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_135, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_136': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_136, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_137': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_137, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_138': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_138, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_139': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_139, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_140': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_140, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_141': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_141, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_142': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_142, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_143': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_143, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_144': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_144, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_145': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_145, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_146': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_146, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_147': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_147, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_148': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_148, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_149': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_149, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_150': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_150, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_151': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_151, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_152': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_152, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_153': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_153, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_154': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_154, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_155': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_155, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_156': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_156, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_157': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_157, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_158': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_158, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_159': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_159, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_160': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_160, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_161': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_161, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_162': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_162, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_163': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_163, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_164': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_164, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_165': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_165, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_166': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_166, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_167': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_167, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_168': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_168, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_169': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_169, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_170': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_170, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_171': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_171, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_172': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_172, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_173': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_173, 
        'xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_174': xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_174
    }
    xǁFilamentPathWidgetǁ_draw_vertical_path__mutmut_orig.__name__ = 'xǁFilamentPathWidgetǁ_draw_vertical_path'

    def _draw_labels(self, painter: QtGui.QPainter) -> None:
        args = [painter]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentPathWidgetǁ_draw_labels__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentPathWidgetǁ_draw_labels__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_orig(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_1(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(None)
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_2(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(None, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_3(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, None, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_4(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, None))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_5(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_6(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_7(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, ))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_8(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(181, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_9(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 181, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_10(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 181))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_11(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(None)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_12(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = None
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_13(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(None, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_14(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, None, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_15(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, None, 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_16(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), None)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_17(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_18(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_19(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_20(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), )
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_21(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(1, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_22(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 6, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_23(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 21)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_24(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(None, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_25(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, None, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_26(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, None)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_27(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_28(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_29(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, )
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_30(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = None
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_31(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() + 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_32(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 26
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_33(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = None
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_34(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(None, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_35(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, None, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_36(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, None, 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_37(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), None)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_38(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_39(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_40(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_41(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), )
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_42(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(1, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_43(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 21)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_44(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(None, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_45(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, None, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_46(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, None)

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_47(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_48(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, "Toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_49(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, )

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_50(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "XXToolheadXX")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_51(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "toolhead")

    def xǁFilamentPathWidgetǁ_draw_labels__mutmut_52(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)
        
        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)
        
        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "TOOLHEAD")
    
    xǁFilamentPathWidgetǁ_draw_labels__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentPathWidgetǁ_draw_labels__mutmut_1': xǁFilamentPathWidgetǁ_draw_labels__mutmut_1, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_2': xǁFilamentPathWidgetǁ_draw_labels__mutmut_2, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_3': xǁFilamentPathWidgetǁ_draw_labels__mutmut_3, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_4': xǁFilamentPathWidgetǁ_draw_labels__mutmut_4, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_5': xǁFilamentPathWidgetǁ_draw_labels__mutmut_5, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_6': xǁFilamentPathWidgetǁ_draw_labels__mutmut_6, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_7': xǁFilamentPathWidgetǁ_draw_labels__mutmut_7, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_8': xǁFilamentPathWidgetǁ_draw_labels__mutmut_8, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_9': xǁFilamentPathWidgetǁ_draw_labels__mutmut_9, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_10': xǁFilamentPathWidgetǁ_draw_labels__mutmut_10, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_11': xǁFilamentPathWidgetǁ_draw_labels__mutmut_11, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_12': xǁFilamentPathWidgetǁ_draw_labels__mutmut_12, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_13': xǁFilamentPathWidgetǁ_draw_labels__mutmut_13, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_14': xǁFilamentPathWidgetǁ_draw_labels__mutmut_14, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_15': xǁFilamentPathWidgetǁ_draw_labels__mutmut_15, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_16': xǁFilamentPathWidgetǁ_draw_labels__mutmut_16, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_17': xǁFilamentPathWidgetǁ_draw_labels__mutmut_17, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_18': xǁFilamentPathWidgetǁ_draw_labels__mutmut_18, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_19': xǁFilamentPathWidgetǁ_draw_labels__mutmut_19, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_20': xǁFilamentPathWidgetǁ_draw_labels__mutmut_20, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_21': xǁFilamentPathWidgetǁ_draw_labels__mutmut_21, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_22': xǁFilamentPathWidgetǁ_draw_labels__mutmut_22, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_23': xǁFilamentPathWidgetǁ_draw_labels__mutmut_23, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_24': xǁFilamentPathWidgetǁ_draw_labels__mutmut_24, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_25': xǁFilamentPathWidgetǁ_draw_labels__mutmut_25, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_26': xǁFilamentPathWidgetǁ_draw_labels__mutmut_26, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_27': xǁFilamentPathWidgetǁ_draw_labels__mutmut_27, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_28': xǁFilamentPathWidgetǁ_draw_labels__mutmut_28, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_29': xǁFilamentPathWidgetǁ_draw_labels__mutmut_29, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_30': xǁFilamentPathWidgetǁ_draw_labels__mutmut_30, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_31': xǁFilamentPathWidgetǁ_draw_labels__mutmut_31, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_32': xǁFilamentPathWidgetǁ_draw_labels__mutmut_32, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_33': xǁFilamentPathWidgetǁ_draw_labels__mutmut_33, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_34': xǁFilamentPathWidgetǁ_draw_labels__mutmut_34, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_35': xǁFilamentPathWidgetǁ_draw_labels__mutmut_35, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_36': xǁFilamentPathWidgetǁ_draw_labels__mutmut_36, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_37': xǁFilamentPathWidgetǁ_draw_labels__mutmut_37, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_38': xǁFilamentPathWidgetǁ_draw_labels__mutmut_38, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_39': xǁFilamentPathWidgetǁ_draw_labels__mutmut_39, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_40': xǁFilamentPathWidgetǁ_draw_labels__mutmut_40, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_41': xǁFilamentPathWidgetǁ_draw_labels__mutmut_41, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_42': xǁFilamentPathWidgetǁ_draw_labels__mutmut_42, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_43': xǁFilamentPathWidgetǁ_draw_labels__mutmut_43, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_44': xǁFilamentPathWidgetǁ_draw_labels__mutmut_44, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_45': xǁFilamentPathWidgetǁ_draw_labels__mutmut_45, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_46': xǁFilamentPathWidgetǁ_draw_labels__mutmut_46, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_47': xǁFilamentPathWidgetǁ_draw_labels__mutmut_47, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_48': xǁFilamentPathWidgetǁ_draw_labels__mutmut_48, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_49': xǁFilamentPathWidgetǁ_draw_labels__mutmut_49, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_50': xǁFilamentPathWidgetǁ_draw_labels__mutmut_50, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_51': xǁFilamentPathWidgetǁ_draw_labels__mutmut_51, 
        'xǁFilamentPathWidgetǁ_draw_labels__mutmut_52': xǁFilamentPathWidgetǁ_draw_labels__mutmut_52
    }
    xǁFilamentPathWidgetǁ_draw_labels__mutmut_orig.__name__ = 'xǁFilamentPathWidgetǁ_draw_labels'

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        args = [event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentPathWidgetǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentPathWidgetǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentPathWidgetǁpaintEvent__mutmut_orig(self, event: QtGui.QPaintEvent) -> None:
        """Paint the widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        self._draw_vertical_path(painter)
        self._draw_labels(painter)
        
        painter.end()

    def xǁFilamentPathWidgetǁpaintEvent__mutmut_1(self, event: QtGui.QPaintEvent) -> None:
        """Paint the widget"""
        painter = None
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        self._draw_vertical_path(painter)
        self._draw_labels(painter)
        
        painter.end()

    def xǁFilamentPathWidgetǁpaintEvent__mutmut_2(self, event: QtGui.QPaintEvent) -> None:
        """Paint the widget"""
        painter = QtGui.QPainter(None)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        self._draw_vertical_path(painter)
        self._draw_labels(painter)
        
        painter.end()

    def xǁFilamentPathWidgetǁpaintEvent__mutmut_3(self, event: QtGui.QPaintEvent) -> None:
        """Paint the widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None)
        
        self._draw_vertical_path(painter)
        self._draw_labels(painter)
        
        painter.end()

    def xǁFilamentPathWidgetǁpaintEvent__mutmut_4(self, event: QtGui.QPaintEvent) -> None:
        """Paint the widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        self._draw_vertical_path(None)
        self._draw_labels(painter)
        
        painter.end()

    def xǁFilamentPathWidgetǁpaintEvent__mutmut_5(self, event: QtGui.QPaintEvent) -> None:
        """Paint the widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        self._draw_vertical_path(painter)
        self._draw_labels(None)
        
        painter.end()
    
    xǁFilamentPathWidgetǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentPathWidgetǁpaintEvent__mutmut_1': xǁFilamentPathWidgetǁpaintEvent__mutmut_1, 
        'xǁFilamentPathWidgetǁpaintEvent__mutmut_2': xǁFilamentPathWidgetǁpaintEvent__mutmut_2, 
        'xǁFilamentPathWidgetǁpaintEvent__mutmut_3': xǁFilamentPathWidgetǁpaintEvent__mutmut_3, 
        'xǁFilamentPathWidgetǁpaintEvent__mutmut_4': xǁFilamentPathWidgetǁpaintEvent__mutmut_4, 
        'xǁFilamentPathWidgetǁpaintEvent__mutmut_5': xǁFilamentPathWidgetǁpaintEvent__mutmut_5
    }
    xǁFilamentPathWidgetǁpaintEvent__mutmut_orig.__name__ = 'xǁFilamentPathWidgetǁpaintEvent'


# Example usage
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    
    window = QtWidgets.QWidget()
    window.setWindowTitle("Filament Path Widget Test")
    window.setStyleSheet("background-color: #2a2a2a;")
    
    layout = QtWidgets.QHBoxLayout(window)
    

    
    # Add slider for testing
    test_widget = FilamentPathWidget()
    test_widget.set_gate_name("T0")
    test_widget.setMaximumSize(30 , 200)
    layout.addWidget(test_widget)
    
    slider_layout = QtWidgets.QVBoxLayout()
    slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Vertical)
    slider.setMinimum(0)
    slider.setMaximum(10)
    slider.valueChanged.connect(lambda v: test_widget.set_filament_position(FilamentPos(v)))
    slider_layout.addWidget(QtWidgets.QLabel("Test"))
    slider_layout.addWidget(slider)
    layout.addLayout(slider_layout)
    
    window.resize(450, 350)
    window.show()
    
    sys.exit(app.exec())