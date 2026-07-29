import enum
import typing
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


class ToggleAnimatedButton(QtWidgets.QAbstractButton):
    class State(enum.Enum):
        ON = True
        OFF = False

    stateChange: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        State, name="state-change"
    )

    def __init__(self, parent) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁToggleAnimatedButtonǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁToggleAnimatedButtonǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁToggleAnimatedButtonǁ__init____mutmut_orig(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_1(self, parent) -> None:
        super().__init__(None)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_2(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(None)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_3(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(None, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_4(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, None))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_5(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_6(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, ))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_7(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(81, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_8(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 41))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_9(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(None, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_10(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, None)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_11(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_12(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_13(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, False)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_14(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(None, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_15(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, None)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_16(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_17(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, )

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_18(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, False)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_19(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(None)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_20(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(81)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_21(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(None)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_22(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(False)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_23(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = None
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_24(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) / 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_25(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() / 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_26(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 1.8
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_27(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 3
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_28(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = None
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_29(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) / 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_30(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() / 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_31(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 1.2
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_32(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 3
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_33(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = None

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_34(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition + self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_35(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width() + self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_36(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius / 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_37(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 3
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_38(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = None
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_39(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = None
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_40(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(None, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_41(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, None, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_42(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, None)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_43(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_44(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_45(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, )
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_46(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(224, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_47(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 224, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_48(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 224)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_49(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = None

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_50(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(None, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_51(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, None, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_52(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, None)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_53(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_54(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_55(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, )

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_56(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(256, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_57(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 101, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_58(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 11)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_59(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = None
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_60(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(None, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_61(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, None, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_62(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, None)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_63(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_64(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_65(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, )
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_66(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(1, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_67(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 201, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_68(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 1)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_69(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = None

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_70(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(None, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_71(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, None, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_72(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, None)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_73(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_74(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_75(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, )

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_76(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(201, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_77(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 1, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_78(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 1)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_79(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = None
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_80(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor(None)
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_81(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("XX#A9A9A9XX")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_82(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#a9a9a9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_83(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = None
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_84(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor(None)
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_85(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("XX#666666XX")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_86(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = None
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_87(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = None

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_88(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 251

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_89(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = None

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_90(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state != ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_91(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = None

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_92(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(None, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_93(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, None)

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_94(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_95(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, )

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_96(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"XXhandle_positionXX")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_97(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"HANDLE_POSITION")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_98(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(None)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_99(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(None)
        self.pressed.connect(self.setup_animation)

    def xǁToggleAnimatedButtonǁ__init____mutmut_100(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(None)
    
    xǁToggleAnimatedButtonǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁToggleAnimatedButtonǁ__init____mutmut_1': xǁToggleAnimatedButtonǁ__init____mutmut_1, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_2': xǁToggleAnimatedButtonǁ__init____mutmut_2, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_3': xǁToggleAnimatedButtonǁ__init____mutmut_3, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_4': xǁToggleAnimatedButtonǁ__init____mutmut_4, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_5': xǁToggleAnimatedButtonǁ__init____mutmut_5, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_6': xǁToggleAnimatedButtonǁ__init____mutmut_6, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_7': xǁToggleAnimatedButtonǁ__init____mutmut_7, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_8': xǁToggleAnimatedButtonǁ__init____mutmut_8, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_9': xǁToggleAnimatedButtonǁ__init____mutmut_9, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_10': xǁToggleAnimatedButtonǁ__init____mutmut_10, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_11': xǁToggleAnimatedButtonǁ__init____mutmut_11, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_12': xǁToggleAnimatedButtonǁ__init____mutmut_12, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_13': xǁToggleAnimatedButtonǁ__init____mutmut_13, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_14': xǁToggleAnimatedButtonǁ__init____mutmut_14, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_15': xǁToggleAnimatedButtonǁ__init____mutmut_15, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_16': xǁToggleAnimatedButtonǁ__init____mutmut_16, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_17': xǁToggleAnimatedButtonǁ__init____mutmut_17, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_18': xǁToggleAnimatedButtonǁ__init____mutmut_18, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_19': xǁToggleAnimatedButtonǁ__init____mutmut_19, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_20': xǁToggleAnimatedButtonǁ__init____mutmut_20, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_21': xǁToggleAnimatedButtonǁ__init____mutmut_21, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_22': xǁToggleAnimatedButtonǁ__init____mutmut_22, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_23': xǁToggleAnimatedButtonǁ__init____mutmut_23, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_24': xǁToggleAnimatedButtonǁ__init____mutmut_24, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_25': xǁToggleAnimatedButtonǁ__init____mutmut_25, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_26': xǁToggleAnimatedButtonǁ__init____mutmut_26, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_27': xǁToggleAnimatedButtonǁ__init____mutmut_27, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_28': xǁToggleAnimatedButtonǁ__init____mutmut_28, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_29': xǁToggleAnimatedButtonǁ__init____mutmut_29, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_30': xǁToggleAnimatedButtonǁ__init____mutmut_30, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_31': xǁToggleAnimatedButtonǁ__init____mutmut_31, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_32': xǁToggleAnimatedButtonǁ__init____mutmut_32, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_33': xǁToggleAnimatedButtonǁ__init____mutmut_33, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_34': xǁToggleAnimatedButtonǁ__init____mutmut_34, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_35': xǁToggleAnimatedButtonǁ__init____mutmut_35, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_36': xǁToggleAnimatedButtonǁ__init____mutmut_36, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_37': xǁToggleAnimatedButtonǁ__init____mutmut_37, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_38': xǁToggleAnimatedButtonǁ__init____mutmut_38, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_39': xǁToggleAnimatedButtonǁ__init____mutmut_39, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_40': xǁToggleAnimatedButtonǁ__init____mutmut_40, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_41': xǁToggleAnimatedButtonǁ__init____mutmut_41, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_42': xǁToggleAnimatedButtonǁ__init____mutmut_42, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_43': xǁToggleAnimatedButtonǁ__init____mutmut_43, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_44': xǁToggleAnimatedButtonǁ__init____mutmut_44, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_45': xǁToggleAnimatedButtonǁ__init____mutmut_45, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_46': xǁToggleAnimatedButtonǁ__init____mutmut_46, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_47': xǁToggleAnimatedButtonǁ__init____mutmut_47, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_48': xǁToggleAnimatedButtonǁ__init____mutmut_48, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_49': xǁToggleAnimatedButtonǁ__init____mutmut_49, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_50': xǁToggleAnimatedButtonǁ__init____mutmut_50, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_51': xǁToggleAnimatedButtonǁ__init____mutmut_51, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_52': xǁToggleAnimatedButtonǁ__init____mutmut_52, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_53': xǁToggleAnimatedButtonǁ__init____mutmut_53, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_54': xǁToggleAnimatedButtonǁ__init____mutmut_54, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_55': xǁToggleAnimatedButtonǁ__init____mutmut_55, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_56': xǁToggleAnimatedButtonǁ__init____mutmut_56, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_57': xǁToggleAnimatedButtonǁ__init____mutmut_57, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_58': xǁToggleAnimatedButtonǁ__init____mutmut_58, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_59': xǁToggleAnimatedButtonǁ__init____mutmut_59, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_60': xǁToggleAnimatedButtonǁ__init____mutmut_60, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_61': xǁToggleAnimatedButtonǁ__init____mutmut_61, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_62': xǁToggleAnimatedButtonǁ__init____mutmut_62, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_63': xǁToggleAnimatedButtonǁ__init____mutmut_63, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_64': xǁToggleAnimatedButtonǁ__init____mutmut_64, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_65': xǁToggleAnimatedButtonǁ__init____mutmut_65, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_66': xǁToggleAnimatedButtonǁ__init____mutmut_66, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_67': xǁToggleAnimatedButtonǁ__init____mutmut_67, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_68': xǁToggleAnimatedButtonǁ__init____mutmut_68, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_69': xǁToggleAnimatedButtonǁ__init____mutmut_69, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_70': xǁToggleAnimatedButtonǁ__init____mutmut_70, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_71': xǁToggleAnimatedButtonǁ__init____mutmut_71, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_72': xǁToggleAnimatedButtonǁ__init____mutmut_72, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_73': xǁToggleAnimatedButtonǁ__init____mutmut_73, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_74': xǁToggleAnimatedButtonǁ__init____mutmut_74, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_75': xǁToggleAnimatedButtonǁ__init____mutmut_75, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_76': xǁToggleAnimatedButtonǁ__init____mutmut_76, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_77': xǁToggleAnimatedButtonǁ__init____mutmut_77, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_78': xǁToggleAnimatedButtonǁ__init____mutmut_78, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_79': xǁToggleAnimatedButtonǁ__init____mutmut_79, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_80': xǁToggleAnimatedButtonǁ__init____mutmut_80, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_81': xǁToggleAnimatedButtonǁ__init____mutmut_81, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_82': xǁToggleAnimatedButtonǁ__init____mutmut_82, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_83': xǁToggleAnimatedButtonǁ__init____mutmut_83, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_84': xǁToggleAnimatedButtonǁ__init____mutmut_84, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_85': xǁToggleAnimatedButtonǁ__init____mutmut_85, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_86': xǁToggleAnimatedButtonǁ__init____mutmut_86, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_87': xǁToggleAnimatedButtonǁ__init____mutmut_87, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_88': xǁToggleAnimatedButtonǁ__init____mutmut_88, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_89': xǁToggleAnimatedButtonǁ__init____mutmut_89, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_90': xǁToggleAnimatedButtonǁ__init____mutmut_90, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_91': xǁToggleAnimatedButtonǁ__init____mutmut_91, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_92': xǁToggleAnimatedButtonǁ__init____mutmut_92, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_93': xǁToggleAnimatedButtonǁ__init____mutmut_93, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_94': xǁToggleAnimatedButtonǁ__init____mutmut_94, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_95': xǁToggleAnimatedButtonǁ__init____mutmut_95, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_96': xǁToggleAnimatedButtonǁ__init____mutmut_96, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_97': xǁToggleAnimatedButtonǁ__init____mutmut_97, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_98': xǁToggleAnimatedButtonǁ__init____mutmut_98, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_99': xǁToggleAnimatedButtonǁ__init____mutmut_99, 
        'xǁToggleAnimatedButtonǁ__init____mutmut_100': xǁToggleAnimatedButtonǁ__init____mutmut_100
    }
    xǁToggleAnimatedButtonǁ__init____mutmut_orig.__name__ = 'xǁToggleAnimatedButtonǁ__init__'

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁToggleAnimatedButtonǁresizeEvent__mutmut_orig'), object.__getattribute__(self, 'xǁToggleAnimatedButtonǁresizeEvent__mutmut_mutants'), args, kwargs, self)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_orig(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_1(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = None
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_2(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) / 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_3(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() / 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_4(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 1.8
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_5(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 3
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_6(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = None
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_7(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) / 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_8(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() / 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_9(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 1.2
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_10(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 3
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_11(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = None
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_12(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition + self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_13(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width() + self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_14(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius / 2
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_15(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 3
        )
        return super().resizeEvent(a0)

    def xǁToggleAnimatedButtonǁresizeEvent__mutmut_16(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        return super().resizeEvent(None)
    
    xǁToggleAnimatedButtonǁresizeEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁToggleAnimatedButtonǁresizeEvent__mutmut_1': xǁToggleAnimatedButtonǁresizeEvent__mutmut_1, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_2': xǁToggleAnimatedButtonǁresizeEvent__mutmut_2, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_3': xǁToggleAnimatedButtonǁresizeEvent__mutmut_3, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_4': xǁToggleAnimatedButtonǁresizeEvent__mutmut_4, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_5': xǁToggleAnimatedButtonǁresizeEvent__mutmut_5, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_6': xǁToggleAnimatedButtonǁresizeEvent__mutmut_6, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_7': xǁToggleAnimatedButtonǁresizeEvent__mutmut_7, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_8': xǁToggleAnimatedButtonǁresizeEvent__mutmut_8, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_9': xǁToggleAnimatedButtonǁresizeEvent__mutmut_9, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_10': xǁToggleAnimatedButtonǁresizeEvent__mutmut_10, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_11': xǁToggleAnimatedButtonǁresizeEvent__mutmut_11, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_12': xǁToggleAnimatedButtonǁresizeEvent__mutmut_12, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_13': xǁToggleAnimatedButtonǁresizeEvent__mutmut_13, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_14': xǁToggleAnimatedButtonǁresizeEvent__mutmut_14, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_15': xǁToggleAnimatedButtonǁresizeEvent__mutmut_15, 
        'xǁToggleAnimatedButtonǁresizeEvent__mutmut_16': xǁToggleAnimatedButtonǁresizeEvent__mutmut_16
    }
    xǁToggleAnimatedButtonǁresizeEvent__mutmut_orig.__name__ = 'xǁToggleAnimatedButtonǁresizeEvent'

    def sizeHint(self) -> QtCore.QSize:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁToggleAnimatedButtonǁsizeHint__mutmut_orig'), object.__getattribute__(self, 'xǁToggleAnimatedButtonǁsizeHint__mutmut_mutants'), args, kwargs, self)

    def xǁToggleAnimatedButtonǁsizeHint__mutmut_orig(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        return QtCore.QSize(80, 40)

    def xǁToggleAnimatedButtonǁsizeHint__mutmut_1(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        return QtCore.QSize(None, 40)

    def xǁToggleAnimatedButtonǁsizeHint__mutmut_2(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        return QtCore.QSize(80, None)

    def xǁToggleAnimatedButtonǁsizeHint__mutmut_3(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        return QtCore.QSize(40)

    def xǁToggleAnimatedButtonǁsizeHint__mutmut_4(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        return QtCore.QSize(80, )

    def xǁToggleAnimatedButtonǁsizeHint__mutmut_5(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        return QtCore.QSize(81, 40)

    def xǁToggleAnimatedButtonǁsizeHint__mutmut_6(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        return QtCore.QSize(80, 41)
    
    xǁToggleAnimatedButtonǁsizeHint__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁToggleAnimatedButtonǁsizeHint__mutmut_1': xǁToggleAnimatedButtonǁsizeHint__mutmut_1, 
        'xǁToggleAnimatedButtonǁsizeHint__mutmut_2': xǁToggleAnimatedButtonǁsizeHint__mutmut_2, 
        'xǁToggleAnimatedButtonǁsizeHint__mutmut_3': xǁToggleAnimatedButtonǁsizeHint__mutmut_3, 
        'xǁToggleAnimatedButtonǁsizeHint__mutmut_4': xǁToggleAnimatedButtonǁsizeHint__mutmut_4, 
        'xǁToggleAnimatedButtonǁsizeHint__mutmut_5': xǁToggleAnimatedButtonǁsizeHint__mutmut_5, 
        'xǁToggleAnimatedButtonǁsizeHint__mutmut_6': xǁToggleAnimatedButtonǁsizeHint__mutmut_6
    }
    xǁToggleAnimatedButtonǁsizeHint__mutmut_orig.__name__ = 'xǁToggleAnimatedButtonǁsizeHint'

    @QtCore.pyqtProperty(int)
    def animation_speed(self) -> int:
        """Widget property animation speed"""
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, new_speed: int) -> None:
        self.slide_animation.setDuration(new_speed)
        self._animation_speed = new_speed

    @property
    def state(self) -> State:
        """Widget property, toggle state"""
        return self._state

    @state.setter
    def state(self, new_state: State) -> None:
        if self._state == new_state:
            return
        self._state = new_state
        if self.isVisible():
            self.stateChange.emit(self._state)
            self.setup_animation()
        self.update()

    @QtCore.pyqtProperty(float)
    def handle_position(self) -> float:
        """Widget property handle position"""
        return self._handle_position

    @handle_position.setter
    def handle_position(self, new_pos: float) -> None:
        self._handle_position = new_pos
        self.update()

    @QtCore.pyqtProperty(QtGui.QColor)
    def backgroundColor(self) -> QtGui.QColor:
        """Widget property background color"""
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, new_color: QtGui.QColor) -> None:
        self._backgroundColor = new_color
        self.update()

    @QtCore.pyqtProperty(QtGui.QColor)
    def handleColor(self) -> QtGui.QColor:
        """Widget property handle color"""
        return self._handleColor

    @handleColor.setter
    def handleColor(self, new_color: QtGui.QColor) -> None:
        self._handleColor = new_color
        self.update()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁToggleAnimatedButtonǁshowEvent__mutmut_orig'), object.__getattribute__(self, 'xǁToggleAnimatedButtonǁshowEvent__mutmut_mutants'), args, kwargs, self)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_orig(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_1(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = None
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_2(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = None
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_3(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = None
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_4(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = None
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_5(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() / 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_6(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 3.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_7(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = None
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_8(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() / 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_9(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 3.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_10(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            None,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_11(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            None,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_12(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            None,
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_13(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            None,
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_14(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            None,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_15(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            None,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_16(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            None,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_17(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_18(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_19(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_20(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_21(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_22(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_23(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_24(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            1,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_25(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            1,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_26(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = None
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_27(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state != ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_28(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = None
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_29(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            None,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_30(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            None,
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_31(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            None,
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_32(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            None,
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_33(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_34(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_35(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_36(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_37(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) / 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_38(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() / 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_39(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 1.2) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_40(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 3),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_41(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() / 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_42(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 1.8),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_43(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() / 0.80),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_44(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 1.8),
        )
        return super().showEvent(a0)

    def xǁToggleAnimatedButtonǁshowEvent__mutmut_45(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(None)
    
    xǁToggleAnimatedButtonǁshowEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁToggleAnimatedButtonǁshowEvent__mutmut_1': xǁToggleAnimatedButtonǁshowEvent__mutmut_1, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_2': xǁToggleAnimatedButtonǁshowEvent__mutmut_2, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_3': xǁToggleAnimatedButtonǁshowEvent__mutmut_3, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_4': xǁToggleAnimatedButtonǁshowEvent__mutmut_4, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_5': xǁToggleAnimatedButtonǁshowEvent__mutmut_5, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_6': xǁToggleAnimatedButtonǁshowEvent__mutmut_6, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_7': xǁToggleAnimatedButtonǁshowEvent__mutmut_7, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_8': xǁToggleAnimatedButtonǁshowEvent__mutmut_8, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_9': xǁToggleAnimatedButtonǁshowEvent__mutmut_9, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_10': xǁToggleAnimatedButtonǁshowEvent__mutmut_10, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_11': xǁToggleAnimatedButtonǁshowEvent__mutmut_11, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_12': xǁToggleAnimatedButtonǁshowEvent__mutmut_12, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_13': xǁToggleAnimatedButtonǁshowEvent__mutmut_13, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_14': xǁToggleAnimatedButtonǁshowEvent__mutmut_14, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_15': xǁToggleAnimatedButtonǁshowEvent__mutmut_15, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_16': xǁToggleAnimatedButtonǁshowEvent__mutmut_16, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_17': xǁToggleAnimatedButtonǁshowEvent__mutmut_17, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_18': xǁToggleAnimatedButtonǁshowEvent__mutmut_18, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_19': xǁToggleAnimatedButtonǁshowEvent__mutmut_19, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_20': xǁToggleAnimatedButtonǁshowEvent__mutmut_20, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_21': xǁToggleAnimatedButtonǁshowEvent__mutmut_21, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_22': xǁToggleAnimatedButtonǁshowEvent__mutmut_22, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_23': xǁToggleAnimatedButtonǁshowEvent__mutmut_23, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_24': xǁToggleAnimatedButtonǁshowEvent__mutmut_24, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_25': xǁToggleAnimatedButtonǁshowEvent__mutmut_25, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_26': xǁToggleAnimatedButtonǁshowEvent__mutmut_26, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_27': xǁToggleAnimatedButtonǁshowEvent__mutmut_27, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_28': xǁToggleAnimatedButtonǁshowEvent__mutmut_28, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_29': xǁToggleAnimatedButtonǁshowEvent__mutmut_29, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_30': xǁToggleAnimatedButtonǁshowEvent__mutmut_30, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_31': xǁToggleAnimatedButtonǁshowEvent__mutmut_31, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_32': xǁToggleAnimatedButtonǁshowEvent__mutmut_32, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_33': xǁToggleAnimatedButtonǁshowEvent__mutmut_33, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_34': xǁToggleAnimatedButtonǁshowEvent__mutmut_34, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_35': xǁToggleAnimatedButtonǁshowEvent__mutmut_35, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_36': xǁToggleAnimatedButtonǁshowEvent__mutmut_36, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_37': xǁToggleAnimatedButtonǁshowEvent__mutmut_37, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_38': xǁToggleAnimatedButtonǁshowEvent__mutmut_38, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_39': xǁToggleAnimatedButtonǁshowEvent__mutmut_39, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_40': xǁToggleAnimatedButtonǁshowEvent__mutmut_40, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_41': xǁToggleAnimatedButtonǁshowEvent__mutmut_41, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_42': xǁToggleAnimatedButtonǁshowEvent__mutmut_42, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_43': xǁToggleAnimatedButtonǁshowEvent__mutmut_43, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_44': xǁToggleAnimatedButtonǁshowEvent__mutmut_44, 
        'xǁToggleAnimatedButtonǁshowEvent__mutmut_45': xǁToggleAnimatedButtonǁshowEvent__mutmut_45
    }
    xǁToggleAnimatedButtonǁshowEvent__mutmut_orig.__name__ = 'xǁToggleAnimatedButtonǁshowEvent'

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        args = [pixmap]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁToggleAnimatedButtonǁsetPixmap__mutmut_orig'), object.__getattribute__(self, 'xǁToggleAnimatedButtonǁsetPixmap__mutmut_mutants'), args, kwargs, self)

    def xǁToggleAnimatedButtonǁsetPixmap__mutmut_orig(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = pixmap
        # self.repaint()
        self.update()

    def xǁToggleAnimatedButtonǁsetPixmap__mutmut_1(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = None
        # self.repaint()
        self.update()
    
    xǁToggleAnimatedButtonǁsetPixmap__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁToggleAnimatedButtonǁsetPixmap__mutmut_1': xǁToggleAnimatedButtonǁsetPixmap__mutmut_1
    }
    xǁToggleAnimatedButtonǁsetPixmap__mutmut_orig.__name__ = 'xǁToggleAnimatedButtonǁsetPixmap'

    @QtCore.pyqtSlot(name="clicked")
    def setup_animation(self) -> None:
        """Setup widget animation"""
        if not self.slide_animation.state == self.slide_animation.State.Running:
            self.slide_animation.setEndValue(
                self._handle_ONPosition
                if self.state == ToggleAnimatedButton.State.OFF
                else self._handle_OFFPosition
            )
            self.slide_animation.start()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        args = [e]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_orig'), object.__getattribute__(self, 'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_mutants'), args, kwargs, self)

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_orig(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) and self.underMouse():
                if not self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(not self._state.value)
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(e)
        e.ignore()

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_1(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) or self.underMouse():
                if not self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(not self._state.value)
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(e)
        e.ignore()

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_2(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(None) and self.underMouse():
                if not self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(not self._state.value)
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(e)
        e.ignore()

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_3(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) and self.underMouse():
                if self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(not self._state.value)
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(e)
        e.ignore()

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_4(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) and self.underMouse():
                if not self.slide_animation.state != self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(not self._state.value)
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(e)
        e.ignore()

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_5(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) and self.underMouse():
                if not self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = None
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(e)
        e.ignore()

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_6(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) and self.underMouse():
                if not self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(None)
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(e)
        e.ignore()

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_7(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) and self.underMouse():
                if not self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(self._state.value)
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(e)
        e.ignore()

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_8(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) and self.underMouse():
                if not self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(not self._state.value)
                    self.stateChange.emit(None)
                    super().mousePressEvent(e)
        e.ignore()

    def xǁToggleAnimatedButtonǁmousePressEvent__mutmut_9(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) and self.underMouse():
                if not self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(not self._state.value)
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(None)
        e.ignore()
    
    xǁToggleAnimatedButtonǁmousePressEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_1': xǁToggleAnimatedButtonǁmousePressEvent__mutmut_1, 
        'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_2': xǁToggleAnimatedButtonǁmousePressEvent__mutmut_2, 
        'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_3': xǁToggleAnimatedButtonǁmousePressEvent__mutmut_3, 
        'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_4': xǁToggleAnimatedButtonǁmousePressEvent__mutmut_4, 
        'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_5': xǁToggleAnimatedButtonǁmousePressEvent__mutmut_5, 
        'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_6': xǁToggleAnimatedButtonǁmousePressEvent__mutmut_6, 
        'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_7': xǁToggleAnimatedButtonǁmousePressEvent__mutmut_7, 
        'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_8': xǁToggleAnimatedButtonǁmousePressEvent__mutmut_8, 
        'xǁToggleAnimatedButtonǁmousePressEvent__mutmut_9': xǁToggleAnimatedButtonǁmousePressEvent__mutmut_9
    }
    xǁToggleAnimatedButtonǁmousePressEvent__mutmut_orig.__name__ = 'xǁToggleAnimatedButtonǁmousePressEvent'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁToggleAnimatedButtonǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁToggleAnimatedButtonǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_orig(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_1(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = None
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_2(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(None)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_3(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state = QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_4(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state &= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_5(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state = QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_6(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state &= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_7(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state = QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_8(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state &= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_9(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = None
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_10(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = None
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_11(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = None
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_12(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = None
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_13(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            None,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_14(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            None,
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_15(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            None,
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_16(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            None,
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_17(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_18(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_19(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_20(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_21(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) / 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_22(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() / 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_23(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 1.2) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_24(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 3),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_25(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() / 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_26(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 1.8),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_27(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() / 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_28(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 1.8),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_29(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(None)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_30(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = None
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_31(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(None)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_32(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_33(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(None)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_34(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(None)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_35(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(None)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_36(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = None
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_37(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = None
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_38(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = None
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_39(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() + rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_40(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() - rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_41(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() / 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_42(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 1.8
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_43(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = None
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_44(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) * (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_45(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position + min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_46(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x + min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_47(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = None

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_48(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(None, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_49(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, None)

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_50(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_51(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, )

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_52(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(1.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_53(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(None, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_54(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, None))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_55(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_56(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, ))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_57(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(2.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_58(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = None
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_59(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red() - (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_60(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) / progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_61(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() + self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_62(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = None
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_63(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green() - (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_64(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) / progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_65(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() + self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_66(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = None
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_67(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue() - (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_68(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) / progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_69(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() + self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_70(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = None

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_71(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha() - (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_72(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) / progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_73(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() + self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_74(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = None

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_75(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(None, int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_76(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), None, int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_77(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), None, int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_78(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), None)

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_79(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_80(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_81(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_82(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), )

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_83(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(None), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_84(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(None), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_85(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(None), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_86(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(None))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_87(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            None,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_88(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            None,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_89(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_90(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_91(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            None,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_92(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            None,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_93(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_94(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_95(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_96(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(None)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_97(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = None
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_98(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                None,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_99(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                None,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_100(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                None,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_101(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                None,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_102(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_103(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_104(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_105(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_106(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() / 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_107(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 3.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_108(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() / 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_109(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 3.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_110(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() / 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_111(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 1.9,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_112(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() / 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_113(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 1.9,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_114(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = None
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_115(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                None,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_116(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                None,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_117(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                None,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_118(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_119(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_120(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_121(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = None
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_122(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = None
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_123(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = None
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_124(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_125(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() + scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_126(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 3.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_127(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = None
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_128(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_129(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() + scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_130(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 3.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_131(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = None
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_132(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                None,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_133(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                None,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_134(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                None,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_135(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                None,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_136(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_137(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_138(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_139(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_140(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() - adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_141(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() - adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_142(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                None,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_143(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                None,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_144(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                None,  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_145(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_146(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()

    def xǁToggleAnimatedButtonǁpaintEvent__mutmut_147(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off
        option.state |= QtWidgets.QStyle.StateFlag.State_On
        option.state |= QtWidgets.QStyle.StateFlag.State_Active

        _rect = self.contentsRect()
        bg_color = self.backgroundColor
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        rect_norm = _rect.toRectF().normalized()
        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        # Inline color interpolation (no separate functions)
        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        self.handleColor = QtGui.QColor(int(r), int(g), int(b), int(a))

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            self.handleColor if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                )
        painter.end()
    
    xǁToggleAnimatedButtonǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁToggleAnimatedButtonǁpaintEvent__mutmut_1': xǁToggleAnimatedButtonǁpaintEvent__mutmut_1, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_2': xǁToggleAnimatedButtonǁpaintEvent__mutmut_2, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_3': xǁToggleAnimatedButtonǁpaintEvent__mutmut_3, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_4': xǁToggleAnimatedButtonǁpaintEvent__mutmut_4, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_5': xǁToggleAnimatedButtonǁpaintEvent__mutmut_5, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_6': xǁToggleAnimatedButtonǁpaintEvent__mutmut_6, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_7': xǁToggleAnimatedButtonǁpaintEvent__mutmut_7, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_8': xǁToggleAnimatedButtonǁpaintEvent__mutmut_8, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_9': xǁToggleAnimatedButtonǁpaintEvent__mutmut_9, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_10': xǁToggleAnimatedButtonǁpaintEvent__mutmut_10, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_11': xǁToggleAnimatedButtonǁpaintEvent__mutmut_11, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_12': xǁToggleAnimatedButtonǁpaintEvent__mutmut_12, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_13': xǁToggleAnimatedButtonǁpaintEvent__mutmut_13, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_14': xǁToggleAnimatedButtonǁpaintEvent__mutmut_14, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_15': xǁToggleAnimatedButtonǁpaintEvent__mutmut_15, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_16': xǁToggleAnimatedButtonǁpaintEvent__mutmut_16, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_17': xǁToggleAnimatedButtonǁpaintEvent__mutmut_17, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_18': xǁToggleAnimatedButtonǁpaintEvent__mutmut_18, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_19': xǁToggleAnimatedButtonǁpaintEvent__mutmut_19, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_20': xǁToggleAnimatedButtonǁpaintEvent__mutmut_20, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_21': xǁToggleAnimatedButtonǁpaintEvent__mutmut_21, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_22': xǁToggleAnimatedButtonǁpaintEvent__mutmut_22, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_23': xǁToggleAnimatedButtonǁpaintEvent__mutmut_23, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_24': xǁToggleAnimatedButtonǁpaintEvent__mutmut_24, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_25': xǁToggleAnimatedButtonǁpaintEvent__mutmut_25, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_26': xǁToggleAnimatedButtonǁpaintEvent__mutmut_26, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_27': xǁToggleAnimatedButtonǁpaintEvent__mutmut_27, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_28': xǁToggleAnimatedButtonǁpaintEvent__mutmut_28, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_29': xǁToggleAnimatedButtonǁpaintEvent__mutmut_29, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_30': xǁToggleAnimatedButtonǁpaintEvent__mutmut_30, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_31': xǁToggleAnimatedButtonǁpaintEvent__mutmut_31, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_32': xǁToggleAnimatedButtonǁpaintEvent__mutmut_32, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_33': xǁToggleAnimatedButtonǁpaintEvent__mutmut_33, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_34': xǁToggleAnimatedButtonǁpaintEvent__mutmut_34, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_35': xǁToggleAnimatedButtonǁpaintEvent__mutmut_35, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_36': xǁToggleAnimatedButtonǁpaintEvent__mutmut_36, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_37': xǁToggleAnimatedButtonǁpaintEvent__mutmut_37, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_38': xǁToggleAnimatedButtonǁpaintEvent__mutmut_38, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_39': xǁToggleAnimatedButtonǁpaintEvent__mutmut_39, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_40': xǁToggleAnimatedButtonǁpaintEvent__mutmut_40, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_41': xǁToggleAnimatedButtonǁpaintEvent__mutmut_41, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_42': xǁToggleAnimatedButtonǁpaintEvent__mutmut_42, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_43': xǁToggleAnimatedButtonǁpaintEvent__mutmut_43, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_44': xǁToggleAnimatedButtonǁpaintEvent__mutmut_44, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_45': xǁToggleAnimatedButtonǁpaintEvent__mutmut_45, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_46': xǁToggleAnimatedButtonǁpaintEvent__mutmut_46, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_47': xǁToggleAnimatedButtonǁpaintEvent__mutmut_47, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_48': xǁToggleAnimatedButtonǁpaintEvent__mutmut_48, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_49': xǁToggleAnimatedButtonǁpaintEvent__mutmut_49, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_50': xǁToggleAnimatedButtonǁpaintEvent__mutmut_50, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_51': xǁToggleAnimatedButtonǁpaintEvent__mutmut_51, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_52': xǁToggleAnimatedButtonǁpaintEvent__mutmut_52, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_53': xǁToggleAnimatedButtonǁpaintEvent__mutmut_53, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_54': xǁToggleAnimatedButtonǁpaintEvent__mutmut_54, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_55': xǁToggleAnimatedButtonǁpaintEvent__mutmut_55, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_56': xǁToggleAnimatedButtonǁpaintEvent__mutmut_56, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_57': xǁToggleAnimatedButtonǁpaintEvent__mutmut_57, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_58': xǁToggleAnimatedButtonǁpaintEvent__mutmut_58, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_59': xǁToggleAnimatedButtonǁpaintEvent__mutmut_59, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_60': xǁToggleAnimatedButtonǁpaintEvent__mutmut_60, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_61': xǁToggleAnimatedButtonǁpaintEvent__mutmut_61, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_62': xǁToggleAnimatedButtonǁpaintEvent__mutmut_62, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_63': xǁToggleAnimatedButtonǁpaintEvent__mutmut_63, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_64': xǁToggleAnimatedButtonǁpaintEvent__mutmut_64, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_65': xǁToggleAnimatedButtonǁpaintEvent__mutmut_65, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_66': xǁToggleAnimatedButtonǁpaintEvent__mutmut_66, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_67': xǁToggleAnimatedButtonǁpaintEvent__mutmut_67, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_68': xǁToggleAnimatedButtonǁpaintEvent__mutmut_68, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_69': xǁToggleAnimatedButtonǁpaintEvent__mutmut_69, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_70': xǁToggleAnimatedButtonǁpaintEvent__mutmut_70, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_71': xǁToggleAnimatedButtonǁpaintEvent__mutmut_71, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_72': xǁToggleAnimatedButtonǁpaintEvent__mutmut_72, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_73': xǁToggleAnimatedButtonǁpaintEvent__mutmut_73, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_74': xǁToggleAnimatedButtonǁpaintEvent__mutmut_74, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_75': xǁToggleAnimatedButtonǁpaintEvent__mutmut_75, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_76': xǁToggleAnimatedButtonǁpaintEvent__mutmut_76, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_77': xǁToggleAnimatedButtonǁpaintEvent__mutmut_77, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_78': xǁToggleAnimatedButtonǁpaintEvent__mutmut_78, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_79': xǁToggleAnimatedButtonǁpaintEvent__mutmut_79, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_80': xǁToggleAnimatedButtonǁpaintEvent__mutmut_80, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_81': xǁToggleAnimatedButtonǁpaintEvent__mutmut_81, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_82': xǁToggleAnimatedButtonǁpaintEvent__mutmut_82, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_83': xǁToggleAnimatedButtonǁpaintEvent__mutmut_83, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_84': xǁToggleAnimatedButtonǁpaintEvent__mutmut_84, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_85': xǁToggleAnimatedButtonǁpaintEvent__mutmut_85, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_86': xǁToggleAnimatedButtonǁpaintEvent__mutmut_86, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_87': xǁToggleAnimatedButtonǁpaintEvent__mutmut_87, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_88': xǁToggleAnimatedButtonǁpaintEvent__mutmut_88, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_89': xǁToggleAnimatedButtonǁpaintEvent__mutmut_89, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_90': xǁToggleAnimatedButtonǁpaintEvent__mutmut_90, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_91': xǁToggleAnimatedButtonǁpaintEvent__mutmut_91, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_92': xǁToggleAnimatedButtonǁpaintEvent__mutmut_92, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_93': xǁToggleAnimatedButtonǁpaintEvent__mutmut_93, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_94': xǁToggleAnimatedButtonǁpaintEvent__mutmut_94, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_95': xǁToggleAnimatedButtonǁpaintEvent__mutmut_95, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_96': xǁToggleAnimatedButtonǁpaintEvent__mutmut_96, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_97': xǁToggleAnimatedButtonǁpaintEvent__mutmut_97, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_98': xǁToggleAnimatedButtonǁpaintEvent__mutmut_98, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_99': xǁToggleAnimatedButtonǁpaintEvent__mutmut_99, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_100': xǁToggleAnimatedButtonǁpaintEvent__mutmut_100, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_101': xǁToggleAnimatedButtonǁpaintEvent__mutmut_101, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_102': xǁToggleAnimatedButtonǁpaintEvent__mutmut_102, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_103': xǁToggleAnimatedButtonǁpaintEvent__mutmut_103, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_104': xǁToggleAnimatedButtonǁpaintEvent__mutmut_104, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_105': xǁToggleAnimatedButtonǁpaintEvent__mutmut_105, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_106': xǁToggleAnimatedButtonǁpaintEvent__mutmut_106, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_107': xǁToggleAnimatedButtonǁpaintEvent__mutmut_107, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_108': xǁToggleAnimatedButtonǁpaintEvent__mutmut_108, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_109': xǁToggleAnimatedButtonǁpaintEvent__mutmut_109, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_110': xǁToggleAnimatedButtonǁpaintEvent__mutmut_110, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_111': xǁToggleAnimatedButtonǁpaintEvent__mutmut_111, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_112': xǁToggleAnimatedButtonǁpaintEvent__mutmut_112, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_113': xǁToggleAnimatedButtonǁpaintEvent__mutmut_113, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_114': xǁToggleAnimatedButtonǁpaintEvent__mutmut_114, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_115': xǁToggleAnimatedButtonǁpaintEvent__mutmut_115, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_116': xǁToggleAnimatedButtonǁpaintEvent__mutmut_116, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_117': xǁToggleAnimatedButtonǁpaintEvent__mutmut_117, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_118': xǁToggleAnimatedButtonǁpaintEvent__mutmut_118, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_119': xǁToggleAnimatedButtonǁpaintEvent__mutmut_119, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_120': xǁToggleAnimatedButtonǁpaintEvent__mutmut_120, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_121': xǁToggleAnimatedButtonǁpaintEvent__mutmut_121, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_122': xǁToggleAnimatedButtonǁpaintEvent__mutmut_122, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_123': xǁToggleAnimatedButtonǁpaintEvent__mutmut_123, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_124': xǁToggleAnimatedButtonǁpaintEvent__mutmut_124, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_125': xǁToggleAnimatedButtonǁpaintEvent__mutmut_125, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_126': xǁToggleAnimatedButtonǁpaintEvent__mutmut_126, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_127': xǁToggleAnimatedButtonǁpaintEvent__mutmut_127, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_128': xǁToggleAnimatedButtonǁpaintEvent__mutmut_128, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_129': xǁToggleAnimatedButtonǁpaintEvent__mutmut_129, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_130': xǁToggleAnimatedButtonǁpaintEvent__mutmut_130, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_131': xǁToggleAnimatedButtonǁpaintEvent__mutmut_131, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_132': xǁToggleAnimatedButtonǁpaintEvent__mutmut_132, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_133': xǁToggleAnimatedButtonǁpaintEvent__mutmut_133, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_134': xǁToggleAnimatedButtonǁpaintEvent__mutmut_134, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_135': xǁToggleAnimatedButtonǁpaintEvent__mutmut_135, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_136': xǁToggleAnimatedButtonǁpaintEvent__mutmut_136, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_137': xǁToggleAnimatedButtonǁpaintEvent__mutmut_137, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_138': xǁToggleAnimatedButtonǁpaintEvent__mutmut_138, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_139': xǁToggleAnimatedButtonǁpaintEvent__mutmut_139, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_140': xǁToggleAnimatedButtonǁpaintEvent__mutmut_140, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_141': xǁToggleAnimatedButtonǁpaintEvent__mutmut_141, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_142': xǁToggleAnimatedButtonǁpaintEvent__mutmut_142, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_143': xǁToggleAnimatedButtonǁpaintEvent__mutmut_143, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_144': xǁToggleAnimatedButtonǁpaintEvent__mutmut_144, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_145': xǁToggleAnimatedButtonǁpaintEvent__mutmut_145, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_146': xǁToggleAnimatedButtonǁpaintEvent__mutmut_146, 
        'xǁToggleAnimatedButtonǁpaintEvent__mutmut_147': xǁToggleAnimatedButtonǁpaintEvent__mutmut_147
    }
    xǁToggleAnimatedButtonǁpaintEvent__mutmut_orig.__name__ = 'xǁToggleAnimatedButtonǁpaintEvent'
