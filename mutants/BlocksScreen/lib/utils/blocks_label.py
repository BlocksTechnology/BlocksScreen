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


class BlocksLabel(QtWidgets.QLabel):
    """Custom QLabel with marquee scrolling, glow animation, and icon overlay support."""

    def __init__(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        args = [parent, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁ__init____mutmut_orig(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_1(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(None, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_2(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_3(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_4(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, )

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_5(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(None, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_6(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, None)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_7(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_8(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, )
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_9(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, False)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_10(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = ""
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_11(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = None
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_12(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = "XXXX"
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_13(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = ""
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_14(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = ""
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_15(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = None
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_16(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = True
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_17(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_18(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_19(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = None
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_20(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(None)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_21(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = None
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_22(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 1.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_23(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = None
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_24(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 41
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_25(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = None
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_26(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 41
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_27(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = None
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_28(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 31
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_29(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = None
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_30(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 3
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_31(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = None
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_32(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 1
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_33(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = None
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_34(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = True
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_35(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(None)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_36(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(False)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_37(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(None)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_38(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(False)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_39(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            None,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_40(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            None,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_41(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_42(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_43(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = None
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_44(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor(None)
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_45(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("XX#E95757XX")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_46(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#e95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_47(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = None
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_48(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 301
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_49(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = None
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_50(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(None, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_51(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, None)
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_52(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_53(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, )
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_54(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"XXglow_colorXX")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_55(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"GLOW_COLOR")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_56(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(None)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_57(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(None)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_58(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(None)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_59(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(None)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_60(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = None
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_61(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 1.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_62(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = None
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_63(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 1.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_64(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = None
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_65(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 1.0
        self.icon_margin: int = 5
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_66(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = None
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_67(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 6
        self.first_run = True

    def xǁBlocksLabelǁ__init____mutmut_68(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = None

    def xǁBlocksLabelǁ__init____mutmut_69(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = False
    
    xǁBlocksLabelǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁ__init____mutmut_1': xǁBlocksLabelǁ__init____mutmut_1, 
        'xǁBlocksLabelǁ__init____mutmut_2': xǁBlocksLabelǁ__init____mutmut_2, 
        'xǁBlocksLabelǁ__init____mutmut_3': xǁBlocksLabelǁ__init____mutmut_3, 
        'xǁBlocksLabelǁ__init____mutmut_4': xǁBlocksLabelǁ__init____mutmut_4, 
        'xǁBlocksLabelǁ__init____mutmut_5': xǁBlocksLabelǁ__init____mutmut_5, 
        'xǁBlocksLabelǁ__init____mutmut_6': xǁBlocksLabelǁ__init____mutmut_6, 
        'xǁBlocksLabelǁ__init____mutmut_7': xǁBlocksLabelǁ__init____mutmut_7, 
        'xǁBlocksLabelǁ__init____mutmut_8': xǁBlocksLabelǁ__init____mutmut_8, 
        'xǁBlocksLabelǁ__init____mutmut_9': xǁBlocksLabelǁ__init____mutmut_9, 
        'xǁBlocksLabelǁ__init____mutmut_10': xǁBlocksLabelǁ__init____mutmut_10, 
        'xǁBlocksLabelǁ__init____mutmut_11': xǁBlocksLabelǁ__init____mutmut_11, 
        'xǁBlocksLabelǁ__init____mutmut_12': xǁBlocksLabelǁ__init____mutmut_12, 
        'xǁBlocksLabelǁ__init____mutmut_13': xǁBlocksLabelǁ__init____mutmut_13, 
        'xǁBlocksLabelǁ__init____mutmut_14': xǁBlocksLabelǁ__init____mutmut_14, 
        'xǁBlocksLabelǁ__init____mutmut_15': xǁBlocksLabelǁ__init____mutmut_15, 
        'xǁBlocksLabelǁ__init____mutmut_16': xǁBlocksLabelǁ__init____mutmut_16, 
        'xǁBlocksLabelǁ__init____mutmut_17': xǁBlocksLabelǁ__init____mutmut_17, 
        'xǁBlocksLabelǁ__init____mutmut_18': xǁBlocksLabelǁ__init____mutmut_18, 
        'xǁBlocksLabelǁ__init____mutmut_19': xǁBlocksLabelǁ__init____mutmut_19, 
        'xǁBlocksLabelǁ__init____mutmut_20': xǁBlocksLabelǁ__init____mutmut_20, 
        'xǁBlocksLabelǁ__init____mutmut_21': xǁBlocksLabelǁ__init____mutmut_21, 
        'xǁBlocksLabelǁ__init____mutmut_22': xǁBlocksLabelǁ__init____mutmut_22, 
        'xǁBlocksLabelǁ__init____mutmut_23': xǁBlocksLabelǁ__init____mutmut_23, 
        'xǁBlocksLabelǁ__init____mutmut_24': xǁBlocksLabelǁ__init____mutmut_24, 
        'xǁBlocksLabelǁ__init____mutmut_25': xǁBlocksLabelǁ__init____mutmut_25, 
        'xǁBlocksLabelǁ__init____mutmut_26': xǁBlocksLabelǁ__init____mutmut_26, 
        'xǁBlocksLabelǁ__init____mutmut_27': xǁBlocksLabelǁ__init____mutmut_27, 
        'xǁBlocksLabelǁ__init____mutmut_28': xǁBlocksLabelǁ__init____mutmut_28, 
        'xǁBlocksLabelǁ__init____mutmut_29': xǁBlocksLabelǁ__init____mutmut_29, 
        'xǁBlocksLabelǁ__init____mutmut_30': xǁBlocksLabelǁ__init____mutmut_30, 
        'xǁBlocksLabelǁ__init____mutmut_31': xǁBlocksLabelǁ__init____mutmut_31, 
        'xǁBlocksLabelǁ__init____mutmut_32': xǁBlocksLabelǁ__init____mutmut_32, 
        'xǁBlocksLabelǁ__init____mutmut_33': xǁBlocksLabelǁ__init____mutmut_33, 
        'xǁBlocksLabelǁ__init____mutmut_34': xǁBlocksLabelǁ__init____mutmut_34, 
        'xǁBlocksLabelǁ__init____mutmut_35': xǁBlocksLabelǁ__init____mutmut_35, 
        'xǁBlocksLabelǁ__init____mutmut_36': xǁBlocksLabelǁ__init____mutmut_36, 
        'xǁBlocksLabelǁ__init____mutmut_37': xǁBlocksLabelǁ__init____mutmut_37, 
        'xǁBlocksLabelǁ__init____mutmut_38': xǁBlocksLabelǁ__init____mutmut_38, 
        'xǁBlocksLabelǁ__init____mutmut_39': xǁBlocksLabelǁ__init____mutmut_39, 
        'xǁBlocksLabelǁ__init____mutmut_40': xǁBlocksLabelǁ__init____mutmut_40, 
        'xǁBlocksLabelǁ__init____mutmut_41': xǁBlocksLabelǁ__init____mutmut_41, 
        'xǁBlocksLabelǁ__init____mutmut_42': xǁBlocksLabelǁ__init____mutmut_42, 
        'xǁBlocksLabelǁ__init____mutmut_43': xǁBlocksLabelǁ__init____mutmut_43, 
        'xǁBlocksLabelǁ__init____mutmut_44': xǁBlocksLabelǁ__init____mutmut_44, 
        'xǁBlocksLabelǁ__init____mutmut_45': xǁBlocksLabelǁ__init____mutmut_45, 
        'xǁBlocksLabelǁ__init____mutmut_46': xǁBlocksLabelǁ__init____mutmut_46, 
        'xǁBlocksLabelǁ__init____mutmut_47': xǁBlocksLabelǁ__init____mutmut_47, 
        'xǁBlocksLabelǁ__init____mutmut_48': xǁBlocksLabelǁ__init____mutmut_48, 
        'xǁBlocksLabelǁ__init____mutmut_49': xǁBlocksLabelǁ__init____mutmut_49, 
        'xǁBlocksLabelǁ__init____mutmut_50': xǁBlocksLabelǁ__init____mutmut_50, 
        'xǁBlocksLabelǁ__init____mutmut_51': xǁBlocksLabelǁ__init____mutmut_51, 
        'xǁBlocksLabelǁ__init____mutmut_52': xǁBlocksLabelǁ__init____mutmut_52, 
        'xǁBlocksLabelǁ__init____mutmut_53': xǁBlocksLabelǁ__init____mutmut_53, 
        'xǁBlocksLabelǁ__init____mutmut_54': xǁBlocksLabelǁ__init____mutmut_54, 
        'xǁBlocksLabelǁ__init____mutmut_55': xǁBlocksLabelǁ__init____mutmut_55, 
        'xǁBlocksLabelǁ__init____mutmut_56': xǁBlocksLabelǁ__init____mutmut_56, 
        'xǁBlocksLabelǁ__init____mutmut_57': xǁBlocksLabelǁ__init____mutmut_57, 
        'xǁBlocksLabelǁ__init____mutmut_58': xǁBlocksLabelǁ__init____mutmut_58, 
        'xǁBlocksLabelǁ__init____mutmut_59': xǁBlocksLabelǁ__init____mutmut_59, 
        'xǁBlocksLabelǁ__init____mutmut_60': xǁBlocksLabelǁ__init____mutmut_60, 
        'xǁBlocksLabelǁ__init____mutmut_61': xǁBlocksLabelǁ__init____mutmut_61, 
        'xǁBlocksLabelǁ__init____mutmut_62': xǁBlocksLabelǁ__init____mutmut_62, 
        'xǁBlocksLabelǁ__init____mutmut_63': xǁBlocksLabelǁ__init____mutmut_63, 
        'xǁBlocksLabelǁ__init____mutmut_64': xǁBlocksLabelǁ__init____mutmut_64, 
        'xǁBlocksLabelǁ__init____mutmut_65': xǁBlocksLabelǁ__init____mutmut_65, 
        'xǁBlocksLabelǁ__init____mutmut_66': xǁBlocksLabelǁ__init____mutmut_66, 
        'xǁBlocksLabelǁ__init____mutmut_67': xǁBlocksLabelǁ__init____mutmut_67, 
        'xǁBlocksLabelǁ__init____mutmut_68': xǁBlocksLabelǁ__init____mutmut_68, 
        'xǁBlocksLabelǁ__init____mutmut_69': xǁBlocksLabelǁ__init____mutmut_69
    }
    xǁBlocksLabelǁ__init____mutmut_orig.__name__ = 'xǁBlocksLabelǁ__init__'

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁresizeEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁresizeEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁresizeEvent__mutmut_orig(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.update_text_metrics()
        return super().resizeEvent(a0)

    def xǁBlocksLabelǁresizeEvent__mutmut_1(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.update_text_metrics()
        return super().resizeEvent(None)
    
    xǁBlocksLabelǁresizeEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁresizeEvent__mutmut_1': xǁBlocksLabelǁresizeEvent__mutmut_1
    }
    xǁBlocksLabelǁresizeEvent__mutmut_orig.__name__ = 'xǁBlocksLabelǁresizeEvent'

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        args = [ev]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁmousePressEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁmousePressEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁmousePressEvent__mutmut_orig(self, ev: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press event"""
        if (
            ev.button() == QtCore.Qt.MouseButton.LeftButton
            and not self.timer.isActive()
            and self._marquee
        ):
            self.start_scroll()

    def xǁBlocksLabelǁmousePressEvent__mutmut_1(self, ev: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press event"""
        if (
            ev.button() == QtCore.Qt.MouseButton.LeftButton
            and not self.timer.isActive() or self._marquee
        ):
            self.start_scroll()

    def xǁBlocksLabelǁmousePressEvent__mutmut_2(self, ev: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press event"""
        if (
            ev.button() == QtCore.Qt.MouseButton.LeftButton or not self.timer.isActive()
            and self._marquee
        ):
            self.start_scroll()

    def xǁBlocksLabelǁmousePressEvent__mutmut_3(self, ev: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press event"""
        if (
            ev.button() != QtCore.Qt.MouseButton.LeftButton
            and not self.timer.isActive()
            and self._marquee
        ):
            self.start_scroll()

    def xǁBlocksLabelǁmousePressEvent__mutmut_4(self, ev: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press event"""
        if (
            ev.button() == QtCore.Qt.MouseButton.LeftButton
            and self.timer.isActive()
            and self._marquee
        ):
            self.start_scroll()
    
    xǁBlocksLabelǁmousePressEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁmousePressEvent__mutmut_1': xǁBlocksLabelǁmousePressEvent__mutmut_1, 
        'xǁBlocksLabelǁmousePressEvent__mutmut_2': xǁBlocksLabelǁmousePressEvent__mutmut_2, 
        'xǁBlocksLabelǁmousePressEvent__mutmut_3': xǁBlocksLabelǁmousePressEvent__mutmut_3, 
        'xǁBlocksLabelǁmousePressEvent__mutmut_4': xǁBlocksLabelǁmousePressEvent__mutmut_4
    }
    xǁBlocksLabelǁmousePressEvent__mutmut_orig.__name__ = 'xǁBlocksLabelǁmousePressEvent'

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁsetPixmap__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁsetPixmap__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁsetPixmap__mutmut_orig(self, a0: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = a0
        self.update()

    def xǁBlocksLabelǁsetPixmap__mutmut_1(self, a0: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = None
        self.update()
    
    xǁBlocksLabelǁsetPixmap__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁsetPixmap__mutmut_1': xǁBlocksLabelǁsetPixmap__mutmut_1
    }
    xǁBlocksLabelǁsetPixmap__mutmut_orig.__name__ = 'xǁBlocksLabelǁsetPixmap'

    def clearPixmap(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁclearPixmap__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁclearPixmap__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁclearPixmap__mutmut_orig(self) -> None:
        """Clear the current pixmap."""
        self.icon_pixmap = None
        self.update()

    def xǁBlocksLabelǁclearPixmap__mutmut_1(self) -> None:
        """Clear the current pixmap."""
        self.icon_pixmap = ""
        self.update()
    
    xǁBlocksLabelǁclearPixmap__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁclearPixmap__mutmut_1': xǁBlocksLabelǁclearPixmap__mutmut_1
    }
    xǁBlocksLabelǁclearPixmap__mutmut_orig.__name__ = 'xǁBlocksLabelǁclearPixmap'

    def setText(self, text: str) -> None:
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁsetText__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁsetText__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁsetText__mutmut_orig(self, text: str) -> None:
        """Set widget text"""
        self._text = text
        self.scroll_pos = 0.0
        self.update_text_metrics()

    def xǁBlocksLabelǁsetText__mutmut_1(self, text: str) -> None:
        """Set widget text"""
        self._text = None
        self.scroll_pos = 0.0
        self.update_text_metrics()

    def xǁBlocksLabelǁsetText__mutmut_2(self, text: str) -> None:
        """Set widget text"""
        self._text = text
        self.scroll_pos = None
        self.update_text_metrics()

    def xǁBlocksLabelǁsetText__mutmut_3(self, text: str) -> None:
        """Set widget text"""
        self._text = text
        self.scroll_pos = 1.0
        self.update_text_metrics()
    
    xǁBlocksLabelǁsetText__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁsetText__mutmut_1': xǁBlocksLabelǁsetText__mutmut_1, 
        'xǁBlocksLabelǁsetText__mutmut_2': xǁBlocksLabelǁsetText__mutmut_2, 
        'xǁBlocksLabelǁsetText__mutmut_3': xǁBlocksLabelǁsetText__mutmut_3
    }
    xǁBlocksLabelǁsetText__mutmut_orig.__name__ = 'xǁBlocksLabelǁsetText'

    @property
    def background_color(self) -> typing.Optional[QtGui.QColor]:
        """Widget background color"""
        return self._background_color

    @background_color.setter
    def background_color(self, color: QtGui.QColor) -> None:
        self._background_color = color

    @property
    def border_color(self) -> typing.Optional[QtGui.QColor]:
        """Widget border color"""
        return self._border_color

    @border_color.setter
    def border_color(self, color: QtGui.QColor) -> None:
        self._border_color = color

    @property
    def rounded(self) -> bool:
        """Widget rounded property"""
        return self._rounded

    @rounded.setter
    def rounded(self, on: bool) -> None:
        self._rounded = on

    @property
    def marquee(self) -> bool:
        """Widget enable marquee effect"""
        return self._marquee

    @marquee.setter
    def marquee(self, activate: bool) -> None:
        self._marquee = activate
        self.update_text_metrics()

    @QtCore.pyqtProperty(int)
    def animation_speed(self) -> int:
        """Widget animation speed property"""
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, new_speed: int) -> None:
        self._animation_speed = new_speed

    @QtCore.pyqtProperty(QtGui.QColor)
    def glow_color(self) -> QtGui.QColor:
        """Widget glow color property"""
        return self._glow_color

    @glow_color.setter
    def glow_color(self, color: QtGui.QColor) -> None:
        self._glow_color = color
        self.repaint()

    @QtCore.pyqtSlot(name="start_glow_animation")
    def start_glow_animation(self) -> None:
        """Start glow animation"""
        self.glow_animation.setDuration(self.animation_speed)
        start_color = QtGui.QColor("#00000000")
        end_color = QtGui.QColor("#E95757")
        self.glow_animation.setStartValue(start_color)
        self.glow_animation.setEndValue(end_color)
        self.glow_animation.setDirection(QtCore.QPropertyAnimation.Direction.Forward)
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.start()

    @QtCore.pyqtSlot(name="change_glow_direction")
    def change_glow_direction(self) -> None:
        """Handle Change glow direction"""
        current_direction = self.glow_animation.direction()
        if current_direction == self.glow_animation.Direction.Forward:
            self.glow_animation.setDirection(self.glow_animation.Direction.Backward)
        else:
            self.glow_animation.setDirection(self.glow_animation.Direction.Forward)

    def update_text_metrics(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁupdate_text_metrics__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁupdate_text_metrics__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_orig(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_1(self) -> None:
        """Handle widget text metrics"""
        font_metrics = None
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_2(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = None
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_3(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(None)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_4(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = None
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_5(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = None

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_6(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(None)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_7(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width - self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_8(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee or self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_9(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width >= self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_10(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = None
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_11(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 1.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_12(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(None, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_13(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, None)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_14(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_15(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, )
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_16(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2001, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_17(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = None
        self.update()

    def xǁBlocksLabelǁupdate_text_metrics__mutmut_18(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 1.0
        self.update()
    
    xǁBlocksLabelǁupdate_text_metrics__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁupdate_text_metrics__mutmut_1': xǁBlocksLabelǁupdate_text_metrics__mutmut_1, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_2': xǁBlocksLabelǁupdate_text_metrics__mutmut_2, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_3': xǁBlocksLabelǁupdate_text_metrics__mutmut_3, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_4': xǁBlocksLabelǁupdate_text_metrics__mutmut_4, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_5': xǁBlocksLabelǁupdate_text_metrics__mutmut_5, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_6': xǁBlocksLabelǁupdate_text_metrics__mutmut_6, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_7': xǁBlocksLabelǁupdate_text_metrics__mutmut_7, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_8': xǁBlocksLabelǁupdate_text_metrics__mutmut_8, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_9': xǁBlocksLabelǁupdate_text_metrics__mutmut_9, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_10': xǁBlocksLabelǁupdate_text_metrics__mutmut_10, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_11': xǁBlocksLabelǁupdate_text_metrics__mutmut_11, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_12': xǁBlocksLabelǁupdate_text_metrics__mutmut_12, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_13': xǁBlocksLabelǁupdate_text_metrics__mutmut_13, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_14': xǁBlocksLabelǁupdate_text_metrics__mutmut_14, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_15': xǁBlocksLabelǁupdate_text_metrics__mutmut_15, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_16': xǁBlocksLabelǁupdate_text_metrics__mutmut_16, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_17': xǁBlocksLabelǁupdate_text_metrics__mutmut_17, 
        'xǁBlocksLabelǁupdate_text_metrics__mutmut_18': xǁBlocksLabelǁupdate_text_metrics__mutmut_18
    }
    xǁBlocksLabelǁupdate_text_metrics__mutmut_orig.__name__ = 'xǁBlocksLabelǁupdate_text_metrics'

    def start_scroll(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁstart_scroll__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁstart_scroll__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁstart_scroll__mutmut_orig(self) -> None:
        """Start or restart the scrolling."""
        if not self.timer.isActive():
            self.scroll_pos = 0
            self.loop_count = 0
            self.timer.start(self.scroll_animation_speed)

    def xǁBlocksLabelǁstart_scroll__mutmut_1(self) -> None:
        """Start or restart the scrolling."""
        if self.timer.isActive():
            self.scroll_pos = 0
            self.loop_count = 0
            self.timer.start(self.scroll_animation_speed)

    def xǁBlocksLabelǁstart_scroll__mutmut_2(self) -> None:
        """Start or restart the scrolling."""
        if not self.timer.isActive():
            self.scroll_pos = None
            self.loop_count = 0
            self.timer.start(self.scroll_animation_speed)

    def xǁBlocksLabelǁstart_scroll__mutmut_3(self) -> None:
        """Start or restart the scrolling."""
        if not self.timer.isActive():
            self.scroll_pos = 1
            self.loop_count = 0
            self.timer.start(self.scroll_animation_speed)

    def xǁBlocksLabelǁstart_scroll__mutmut_4(self) -> None:
        """Start or restart the scrolling."""
        if not self.timer.isActive():
            self.scroll_pos = 0
            self.loop_count = None
            self.timer.start(self.scroll_animation_speed)

    def xǁBlocksLabelǁstart_scroll__mutmut_5(self) -> None:
        """Start or restart the scrolling."""
        if not self.timer.isActive():
            self.scroll_pos = 0
            self.loop_count = 1
            self.timer.start(self.scroll_animation_speed)

    def xǁBlocksLabelǁstart_scroll__mutmut_6(self) -> None:
        """Start or restart the scrolling."""
        if not self.timer.isActive():
            self.scroll_pos = 0
            self.loop_count = 0
            self.timer.start(None)
    
    xǁBlocksLabelǁstart_scroll__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁstart_scroll__mutmut_1': xǁBlocksLabelǁstart_scroll__mutmut_1, 
        'xǁBlocksLabelǁstart_scroll__mutmut_2': xǁBlocksLabelǁstart_scroll__mutmut_2, 
        'xǁBlocksLabelǁstart_scroll__mutmut_3': xǁBlocksLabelǁstart_scroll__mutmut_3, 
        'xǁBlocksLabelǁstart_scroll__mutmut_4': xǁBlocksLabelǁstart_scroll__mutmut_4, 
        'xǁBlocksLabelǁstart_scroll__mutmut_5': xǁBlocksLabelǁstart_scroll__mutmut_5, 
        'xǁBlocksLabelǁstart_scroll__mutmut_6': xǁBlocksLabelǁstart_scroll__mutmut_6
    }
    xǁBlocksLabelǁstart_scroll__mutmut_orig.__name__ = 'xǁBlocksLabelǁstart_scroll'

    def stop_scroll(self) -> None:
        """Stop marquee text scroll effect"""
        self.timer.stop()
        self.repaint()

    def _scroll_text(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁ_scroll_text__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁ_scroll_text__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁ_scroll_text__mutmut_orig(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_1(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee and self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_2(self) -> None:
        """Smoothly scroll the text leftwards."""
        if self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_3(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = None
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_4(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed / (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_5(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed * 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_6(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1001.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_7(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos = p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_8(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos += p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_9(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos < -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_10(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= +self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_11(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count = 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_12(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count -= 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_13(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 2
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_14(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count > self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_15(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = None
        self.update()

    def xǁBlocksLabelǁ_scroll_text__mutmut_16(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 1.0
        self.update()
    
    xǁBlocksLabelǁ_scroll_text__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁ_scroll_text__mutmut_1': xǁBlocksLabelǁ_scroll_text__mutmut_1, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_2': xǁBlocksLabelǁ_scroll_text__mutmut_2, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_3': xǁBlocksLabelǁ_scroll_text__mutmut_3, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_4': xǁBlocksLabelǁ_scroll_text__mutmut_4, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_5': xǁBlocksLabelǁ_scroll_text__mutmut_5, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_6': xǁBlocksLabelǁ_scroll_text__mutmut_6, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_7': xǁBlocksLabelǁ_scroll_text__mutmut_7, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_8': xǁBlocksLabelǁ_scroll_text__mutmut_8, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_9': xǁBlocksLabelǁ_scroll_text__mutmut_9, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_10': xǁBlocksLabelǁ_scroll_text__mutmut_10, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_11': xǁBlocksLabelǁ_scroll_text__mutmut_11, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_12': xǁBlocksLabelǁ_scroll_text__mutmut_12, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_13': xǁBlocksLabelǁ_scroll_text__mutmut_13, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_14': xǁBlocksLabelǁ_scroll_text__mutmut_14, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_15': xǁBlocksLabelǁ_scroll_text__mutmut_15, 
        'xǁBlocksLabelǁ_scroll_text__mutmut_16': xǁBlocksLabelǁ_scroll_text__mutmut_16
    }
    xǁBlocksLabelǁ_scroll_text__mutmut_orig.__name__ = 'xǁBlocksLabelǁ_scroll_text'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁpaintEvent__mutmut_orig(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_1(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = None
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_2(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(None)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_3(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(None, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_4(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, None)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_5(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_6(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, )
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_7(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, False)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_8(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(None, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_9(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, None)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_10(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_11(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, )
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_12(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, False)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_13(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(None, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_14(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, None)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_15(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_16(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, )
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_17(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, False)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_18(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = None
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_19(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(None)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_20(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(None)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_21(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = None
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_22(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(None, 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_23(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), None, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_24(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, None)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_25(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_26(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_27(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, )
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_28(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(None), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_29(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 11, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_30(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 11)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_31(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(None, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_32(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, None)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_33(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_34(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, )
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_35(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(None, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_36(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, None)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_37(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_38(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, )

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_39(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = None
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_40(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                None,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_41(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                None,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_42(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                None,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_43(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                None,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_44(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_45(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_46(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_47(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_48(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 - self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_49(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                1.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_50(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 - self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_51(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                1.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_52(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() + self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_53(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() + self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_54(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = None
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_55(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                None,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_56(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                None,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_57(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                None,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_58(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_59(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_60(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_61(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = None
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_62(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = None
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_63(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = None
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_64(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_65(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() + scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_66(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 3.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_67(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = None
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_68(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) / 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_69(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() + scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_70(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 3.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_71(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = None
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_72(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                None,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_73(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                None,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_74(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                None,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_75(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                None,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_76(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_77(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_78(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_79(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_80(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() - adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_81(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() - adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_82(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(None, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_83(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, None, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_84(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, None)
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_85(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(_icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_86(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_87(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, )
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_88(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() != self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_89(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = None
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_90(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = None
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_91(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(None, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_92(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, None, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_93(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, None, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_94(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, None)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_95(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_96(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_97(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_98(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, )
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_99(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 11.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_100(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 11.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_101(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = None
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_102(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                None,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_103(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                None,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_104(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                None,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_105(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                None,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_106(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_107(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_108(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_109(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_110(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) * 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_111(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() + rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_112(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() / 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_113(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 1.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_114(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 3,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_115(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) * 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_116(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() + rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_117(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() / 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_118(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 1.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_119(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 3,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_120(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() / 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_121(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 1.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_122(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() / 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_123(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 1.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_124(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = None
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_125(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                None, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_126(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, None, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_127(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, None, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_128(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, None
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_129(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_130(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_131(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_132(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_133(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 11.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_134(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 11.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_135(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = None
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_136(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(None)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_137(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(None)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_138(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(None)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_139(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(None, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_140(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, None)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_141(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_142(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, )
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_143(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = None
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_144(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(None)
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_145(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(None)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_146(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(None)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_147(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = None

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_148(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y() - (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_149(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                ) * 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_150(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent() + self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_151(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height() - self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_152(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 3
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_153(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width >= self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_154(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    None, self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_155(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), None
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_156(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_157(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_158(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(None, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_159(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, None), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_160(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_161(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, ), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_162(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() - self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_163(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    None,
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_164(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    None,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_165(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_166(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_167(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        None, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_168(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, None
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_169(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_170(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_171(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos - self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_172(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() - self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_173(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = None

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_174(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() - (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_175(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) * 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_176(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() + self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_177(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 3

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_178(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(None, self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_179(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), None)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_180(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_181(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), )
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_182(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(None, baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_183(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, None), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_184(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(baseline_y), self._text)
            qp.restore()

        qp.end()

    def xǁBlocksLabelǁpaintEvent__mutmut_185(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(
                0.0 + self.icon_margin,
                0.0 + self.icon_margin,
                self.width() - self.icon_margin,
                self.height() - self.icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            adjusted_icon = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(adjusted_icon, _icon_scaled, _icon_scaled.rect().toRectF())
        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (
                    rect.height()
                    + self.fontMetrics().ascent()
                    - self.fontMetrics().descent()
                )
                / 2
            )

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, ), self._text)
            qp.restore()

        qp.end()
    
    xǁBlocksLabelǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁpaintEvent__mutmut_1': xǁBlocksLabelǁpaintEvent__mutmut_1, 
        'xǁBlocksLabelǁpaintEvent__mutmut_2': xǁBlocksLabelǁpaintEvent__mutmut_2, 
        'xǁBlocksLabelǁpaintEvent__mutmut_3': xǁBlocksLabelǁpaintEvent__mutmut_3, 
        'xǁBlocksLabelǁpaintEvent__mutmut_4': xǁBlocksLabelǁpaintEvent__mutmut_4, 
        'xǁBlocksLabelǁpaintEvent__mutmut_5': xǁBlocksLabelǁpaintEvent__mutmut_5, 
        'xǁBlocksLabelǁpaintEvent__mutmut_6': xǁBlocksLabelǁpaintEvent__mutmut_6, 
        'xǁBlocksLabelǁpaintEvent__mutmut_7': xǁBlocksLabelǁpaintEvent__mutmut_7, 
        'xǁBlocksLabelǁpaintEvent__mutmut_8': xǁBlocksLabelǁpaintEvent__mutmut_8, 
        'xǁBlocksLabelǁpaintEvent__mutmut_9': xǁBlocksLabelǁpaintEvent__mutmut_9, 
        'xǁBlocksLabelǁpaintEvent__mutmut_10': xǁBlocksLabelǁpaintEvent__mutmut_10, 
        'xǁBlocksLabelǁpaintEvent__mutmut_11': xǁBlocksLabelǁpaintEvent__mutmut_11, 
        'xǁBlocksLabelǁpaintEvent__mutmut_12': xǁBlocksLabelǁpaintEvent__mutmut_12, 
        'xǁBlocksLabelǁpaintEvent__mutmut_13': xǁBlocksLabelǁpaintEvent__mutmut_13, 
        'xǁBlocksLabelǁpaintEvent__mutmut_14': xǁBlocksLabelǁpaintEvent__mutmut_14, 
        'xǁBlocksLabelǁpaintEvent__mutmut_15': xǁBlocksLabelǁpaintEvent__mutmut_15, 
        'xǁBlocksLabelǁpaintEvent__mutmut_16': xǁBlocksLabelǁpaintEvent__mutmut_16, 
        'xǁBlocksLabelǁpaintEvent__mutmut_17': xǁBlocksLabelǁpaintEvent__mutmut_17, 
        'xǁBlocksLabelǁpaintEvent__mutmut_18': xǁBlocksLabelǁpaintEvent__mutmut_18, 
        'xǁBlocksLabelǁpaintEvent__mutmut_19': xǁBlocksLabelǁpaintEvent__mutmut_19, 
        'xǁBlocksLabelǁpaintEvent__mutmut_20': xǁBlocksLabelǁpaintEvent__mutmut_20, 
        'xǁBlocksLabelǁpaintEvent__mutmut_21': xǁBlocksLabelǁpaintEvent__mutmut_21, 
        'xǁBlocksLabelǁpaintEvent__mutmut_22': xǁBlocksLabelǁpaintEvent__mutmut_22, 
        'xǁBlocksLabelǁpaintEvent__mutmut_23': xǁBlocksLabelǁpaintEvent__mutmut_23, 
        'xǁBlocksLabelǁpaintEvent__mutmut_24': xǁBlocksLabelǁpaintEvent__mutmut_24, 
        'xǁBlocksLabelǁpaintEvent__mutmut_25': xǁBlocksLabelǁpaintEvent__mutmut_25, 
        'xǁBlocksLabelǁpaintEvent__mutmut_26': xǁBlocksLabelǁpaintEvent__mutmut_26, 
        'xǁBlocksLabelǁpaintEvent__mutmut_27': xǁBlocksLabelǁpaintEvent__mutmut_27, 
        'xǁBlocksLabelǁpaintEvent__mutmut_28': xǁBlocksLabelǁpaintEvent__mutmut_28, 
        'xǁBlocksLabelǁpaintEvent__mutmut_29': xǁBlocksLabelǁpaintEvent__mutmut_29, 
        'xǁBlocksLabelǁpaintEvent__mutmut_30': xǁBlocksLabelǁpaintEvent__mutmut_30, 
        'xǁBlocksLabelǁpaintEvent__mutmut_31': xǁBlocksLabelǁpaintEvent__mutmut_31, 
        'xǁBlocksLabelǁpaintEvent__mutmut_32': xǁBlocksLabelǁpaintEvent__mutmut_32, 
        'xǁBlocksLabelǁpaintEvent__mutmut_33': xǁBlocksLabelǁpaintEvent__mutmut_33, 
        'xǁBlocksLabelǁpaintEvent__mutmut_34': xǁBlocksLabelǁpaintEvent__mutmut_34, 
        'xǁBlocksLabelǁpaintEvent__mutmut_35': xǁBlocksLabelǁpaintEvent__mutmut_35, 
        'xǁBlocksLabelǁpaintEvent__mutmut_36': xǁBlocksLabelǁpaintEvent__mutmut_36, 
        'xǁBlocksLabelǁpaintEvent__mutmut_37': xǁBlocksLabelǁpaintEvent__mutmut_37, 
        'xǁBlocksLabelǁpaintEvent__mutmut_38': xǁBlocksLabelǁpaintEvent__mutmut_38, 
        'xǁBlocksLabelǁpaintEvent__mutmut_39': xǁBlocksLabelǁpaintEvent__mutmut_39, 
        'xǁBlocksLabelǁpaintEvent__mutmut_40': xǁBlocksLabelǁpaintEvent__mutmut_40, 
        'xǁBlocksLabelǁpaintEvent__mutmut_41': xǁBlocksLabelǁpaintEvent__mutmut_41, 
        'xǁBlocksLabelǁpaintEvent__mutmut_42': xǁBlocksLabelǁpaintEvent__mutmut_42, 
        'xǁBlocksLabelǁpaintEvent__mutmut_43': xǁBlocksLabelǁpaintEvent__mutmut_43, 
        'xǁBlocksLabelǁpaintEvent__mutmut_44': xǁBlocksLabelǁpaintEvent__mutmut_44, 
        'xǁBlocksLabelǁpaintEvent__mutmut_45': xǁBlocksLabelǁpaintEvent__mutmut_45, 
        'xǁBlocksLabelǁpaintEvent__mutmut_46': xǁBlocksLabelǁpaintEvent__mutmut_46, 
        'xǁBlocksLabelǁpaintEvent__mutmut_47': xǁBlocksLabelǁpaintEvent__mutmut_47, 
        'xǁBlocksLabelǁpaintEvent__mutmut_48': xǁBlocksLabelǁpaintEvent__mutmut_48, 
        'xǁBlocksLabelǁpaintEvent__mutmut_49': xǁBlocksLabelǁpaintEvent__mutmut_49, 
        'xǁBlocksLabelǁpaintEvent__mutmut_50': xǁBlocksLabelǁpaintEvent__mutmut_50, 
        'xǁBlocksLabelǁpaintEvent__mutmut_51': xǁBlocksLabelǁpaintEvent__mutmut_51, 
        'xǁBlocksLabelǁpaintEvent__mutmut_52': xǁBlocksLabelǁpaintEvent__mutmut_52, 
        'xǁBlocksLabelǁpaintEvent__mutmut_53': xǁBlocksLabelǁpaintEvent__mutmut_53, 
        'xǁBlocksLabelǁpaintEvent__mutmut_54': xǁBlocksLabelǁpaintEvent__mutmut_54, 
        'xǁBlocksLabelǁpaintEvent__mutmut_55': xǁBlocksLabelǁpaintEvent__mutmut_55, 
        'xǁBlocksLabelǁpaintEvent__mutmut_56': xǁBlocksLabelǁpaintEvent__mutmut_56, 
        'xǁBlocksLabelǁpaintEvent__mutmut_57': xǁBlocksLabelǁpaintEvent__mutmut_57, 
        'xǁBlocksLabelǁpaintEvent__mutmut_58': xǁBlocksLabelǁpaintEvent__mutmut_58, 
        'xǁBlocksLabelǁpaintEvent__mutmut_59': xǁBlocksLabelǁpaintEvent__mutmut_59, 
        'xǁBlocksLabelǁpaintEvent__mutmut_60': xǁBlocksLabelǁpaintEvent__mutmut_60, 
        'xǁBlocksLabelǁpaintEvent__mutmut_61': xǁBlocksLabelǁpaintEvent__mutmut_61, 
        'xǁBlocksLabelǁpaintEvent__mutmut_62': xǁBlocksLabelǁpaintEvent__mutmut_62, 
        'xǁBlocksLabelǁpaintEvent__mutmut_63': xǁBlocksLabelǁpaintEvent__mutmut_63, 
        'xǁBlocksLabelǁpaintEvent__mutmut_64': xǁBlocksLabelǁpaintEvent__mutmut_64, 
        'xǁBlocksLabelǁpaintEvent__mutmut_65': xǁBlocksLabelǁpaintEvent__mutmut_65, 
        'xǁBlocksLabelǁpaintEvent__mutmut_66': xǁBlocksLabelǁpaintEvent__mutmut_66, 
        'xǁBlocksLabelǁpaintEvent__mutmut_67': xǁBlocksLabelǁpaintEvent__mutmut_67, 
        'xǁBlocksLabelǁpaintEvent__mutmut_68': xǁBlocksLabelǁpaintEvent__mutmut_68, 
        'xǁBlocksLabelǁpaintEvent__mutmut_69': xǁBlocksLabelǁpaintEvent__mutmut_69, 
        'xǁBlocksLabelǁpaintEvent__mutmut_70': xǁBlocksLabelǁpaintEvent__mutmut_70, 
        'xǁBlocksLabelǁpaintEvent__mutmut_71': xǁBlocksLabelǁpaintEvent__mutmut_71, 
        'xǁBlocksLabelǁpaintEvent__mutmut_72': xǁBlocksLabelǁpaintEvent__mutmut_72, 
        'xǁBlocksLabelǁpaintEvent__mutmut_73': xǁBlocksLabelǁpaintEvent__mutmut_73, 
        'xǁBlocksLabelǁpaintEvent__mutmut_74': xǁBlocksLabelǁpaintEvent__mutmut_74, 
        'xǁBlocksLabelǁpaintEvent__mutmut_75': xǁBlocksLabelǁpaintEvent__mutmut_75, 
        'xǁBlocksLabelǁpaintEvent__mutmut_76': xǁBlocksLabelǁpaintEvent__mutmut_76, 
        'xǁBlocksLabelǁpaintEvent__mutmut_77': xǁBlocksLabelǁpaintEvent__mutmut_77, 
        'xǁBlocksLabelǁpaintEvent__mutmut_78': xǁBlocksLabelǁpaintEvent__mutmut_78, 
        'xǁBlocksLabelǁpaintEvent__mutmut_79': xǁBlocksLabelǁpaintEvent__mutmut_79, 
        'xǁBlocksLabelǁpaintEvent__mutmut_80': xǁBlocksLabelǁpaintEvent__mutmut_80, 
        'xǁBlocksLabelǁpaintEvent__mutmut_81': xǁBlocksLabelǁpaintEvent__mutmut_81, 
        'xǁBlocksLabelǁpaintEvent__mutmut_82': xǁBlocksLabelǁpaintEvent__mutmut_82, 
        'xǁBlocksLabelǁpaintEvent__mutmut_83': xǁBlocksLabelǁpaintEvent__mutmut_83, 
        'xǁBlocksLabelǁpaintEvent__mutmut_84': xǁBlocksLabelǁpaintEvent__mutmut_84, 
        'xǁBlocksLabelǁpaintEvent__mutmut_85': xǁBlocksLabelǁpaintEvent__mutmut_85, 
        'xǁBlocksLabelǁpaintEvent__mutmut_86': xǁBlocksLabelǁpaintEvent__mutmut_86, 
        'xǁBlocksLabelǁpaintEvent__mutmut_87': xǁBlocksLabelǁpaintEvent__mutmut_87, 
        'xǁBlocksLabelǁpaintEvent__mutmut_88': xǁBlocksLabelǁpaintEvent__mutmut_88, 
        'xǁBlocksLabelǁpaintEvent__mutmut_89': xǁBlocksLabelǁpaintEvent__mutmut_89, 
        'xǁBlocksLabelǁpaintEvent__mutmut_90': xǁBlocksLabelǁpaintEvent__mutmut_90, 
        'xǁBlocksLabelǁpaintEvent__mutmut_91': xǁBlocksLabelǁpaintEvent__mutmut_91, 
        'xǁBlocksLabelǁpaintEvent__mutmut_92': xǁBlocksLabelǁpaintEvent__mutmut_92, 
        'xǁBlocksLabelǁpaintEvent__mutmut_93': xǁBlocksLabelǁpaintEvent__mutmut_93, 
        'xǁBlocksLabelǁpaintEvent__mutmut_94': xǁBlocksLabelǁpaintEvent__mutmut_94, 
        'xǁBlocksLabelǁpaintEvent__mutmut_95': xǁBlocksLabelǁpaintEvent__mutmut_95, 
        'xǁBlocksLabelǁpaintEvent__mutmut_96': xǁBlocksLabelǁpaintEvent__mutmut_96, 
        'xǁBlocksLabelǁpaintEvent__mutmut_97': xǁBlocksLabelǁpaintEvent__mutmut_97, 
        'xǁBlocksLabelǁpaintEvent__mutmut_98': xǁBlocksLabelǁpaintEvent__mutmut_98, 
        'xǁBlocksLabelǁpaintEvent__mutmut_99': xǁBlocksLabelǁpaintEvent__mutmut_99, 
        'xǁBlocksLabelǁpaintEvent__mutmut_100': xǁBlocksLabelǁpaintEvent__mutmut_100, 
        'xǁBlocksLabelǁpaintEvent__mutmut_101': xǁBlocksLabelǁpaintEvent__mutmut_101, 
        'xǁBlocksLabelǁpaintEvent__mutmut_102': xǁBlocksLabelǁpaintEvent__mutmut_102, 
        'xǁBlocksLabelǁpaintEvent__mutmut_103': xǁBlocksLabelǁpaintEvent__mutmut_103, 
        'xǁBlocksLabelǁpaintEvent__mutmut_104': xǁBlocksLabelǁpaintEvent__mutmut_104, 
        'xǁBlocksLabelǁpaintEvent__mutmut_105': xǁBlocksLabelǁpaintEvent__mutmut_105, 
        'xǁBlocksLabelǁpaintEvent__mutmut_106': xǁBlocksLabelǁpaintEvent__mutmut_106, 
        'xǁBlocksLabelǁpaintEvent__mutmut_107': xǁBlocksLabelǁpaintEvent__mutmut_107, 
        'xǁBlocksLabelǁpaintEvent__mutmut_108': xǁBlocksLabelǁpaintEvent__mutmut_108, 
        'xǁBlocksLabelǁpaintEvent__mutmut_109': xǁBlocksLabelǁpaintEvent__mutmut_109, 
        'xǁBlocksLabelǁpaintEvent__mutmut_110': xǁBlocksLabelǁpaintEvent__mutmut_110, 
        'xǁBlocksLabelǁpaintEvent__mutmut_111': xǁBlocksLabelǁpaintEvent__mutmut_111, 
        'xǁBlocksLabelǁpaintEvent__mutmut_112': xǁBlocksLabelǁpaintEvent__mutmut_112, 
        'xǁBlocksLabelǁpaintEvent__mutmut_113': xǁBlocksLabelǁpaintEvent__mutmut_113, 
        'xǁBlocksLabelǁpaintEvent__mutmut_114': xǁBlocksLabelǁpaintEvent__mutmut_114, 
        'xǁBlocksLabelǁpaintEvent__mutmut_115': xǁBlocksLabelǁpaintEvent__mutmut_115, 
        'xǁBlocksLabelǁpaintEvent__mutmut_116': xǁBlocksLabelǁpaintEvent__mutmut_116, 
        'xǁBlocksLabelǁpaintEvent__mutmut_117': xǁBlocksLabelǁpaintEvent__mutmut_117, 
        'xǁBlocksLabelǁpaintEvent__mutmut_118': xǁBlocksLabelǁpaintEvent__mutmut_118, 
        'xǁBlocksLabelǁpaintEvent__mutmut_119': xǁBlocksLabelǁpaintEvent__mutmut_119, 
        'xǁBlocksLabelǁpaintEvent__mutmut_120': xǁBlocksLabelǁpaintEvent__mutmut_120, 
        'xǁBlocksLabelǁpaintEvent__mutmut_121': xǁBlocksLabelǁpaintEvent__mutmut_121, 
        'xǁBlocksLabelǁpaintEvent__mutmut_122': xǁBlocksLabelǁpaintEvent__mutmut_122, 
        'xǁBlocksLabelǁpaintEvent__mutmut_123': xǁBlocksLabelǁpaintEvent__mutmut_123, 
        'xǁBlocksLabelǁpaintEvent__mutmut_124': xǁBlocksLabelǁpaintEvent__mutmut_124, 
        'xǁBlocksLabelǁpaintEvent__mutmut_125': xǁBlocksLabelǁpaintEvent__mutmut_125, 
        'xǁBlocksLabelǁpaintEvent__mutmut_126': xǁBlocksLabelǁpaintEvent__mutmut_126, 
        'xǁBlocksLabelǁpaintEvent__mutmut_127': xǁBlocksLabelǁpaintEvent__mutmut_127, 
        'xǁBlocksLabelǁpaintEvent__mutmut_128': xǁBlocksLabelǁpaintEvent__mutmut_128, 
        'xǁBlocksLabelǁpaintEvent__mutmut_129': xǁBlocksLabelǁpaintEvent__mutmut_129, 
        'xǁBlocksLabelǁpaintEvent__mutmut_130': xǁBlocksLabelǁpaintEvent__mutmut_130, 
        'xǁBlocksLabelǁpaintEvent__mutmut_131': xǁBlocksLabelǁpaintEvent__mutmut_131, 
        'xǁBlocksLabelǁpaintEvent__mutmut_132': xǁBlocksLabelǁpaintEvent__mutmut_132, 
        'xǁBlocksLabelǁpaintEvent__mutmut_133': xǁBlocksLabelǁpaintEvent__mutmut_133, 
        'xǁBlocksLabelǁpaintEvent__mutmut_134': xǁBlocksLabelǁpaintEvent__mutmut_134, 
        'xǁBlocksLabelǁpaintEvent__mutmut_135': xǁBlocksLabelǁpaintEvent__mutmut_135, 
        'xǁBlocksLabelǁpaintEvent__mutmut_136': xǁBlocksLabelǁpaintEvent__mutmut_136, 
        'xǁBlocksLabelǁpaintEvent__mutmut_137': xǁBlocksLabelǁpaintEvent__mutmut_137, 
        'xǁBlocksLabelǁpaintEvent__mutmut_138': xǁBlocksLabelǁpaintEvent__mutmut_138, 
        'xǁBlocksLabelǁpaintEvent__mutmut_139': xǁBlocksLabelǁpaintEvent__mutmut_139, 
        'xǁBlocksLabelǁpaintEvent__mutmut_140': xǁBlocksLabelǁpaintEvent__mutmut_140, 
        'xǁBlocksLabelǁpaintEvent__mutmut_141': xǁBlocksLabelǁpaintEvent__mutmut_141, 
        'xǁBlocksLabelǁpaintEvent__mutmut_142': xǁBlocksLabelǁpaintEvent__mutmut_142, 
        'xǁBlocksLabelǁpaintEvent__mutmut_143': xǁBlocksLabelǁpaintEvent__mutmut_143, 
        'xǁBlocksLabelǁpaintEvent__mutmut_144': xǁBlocksLabelǁpaintEvent__mutmut_144, 
        'xǁBlocksLabelǁpaintEvent__mutmut_145': xǁBlocksLabelǁpaintEvent__mutmut_145, 
        'xǁBlocksLabelǁpaintEvent__mutmut_146': xǁBlocksLabelǁpaintEvent__mutmut_146, 
        'xǁBlocksLabelǁpaintEvent__mutmut_147': xǁBlocksLabelǁpaintEvent__mutmut_147, 
        'xǁBlocksLabelǁpaintEvent__mutmut_148': xǁBlocksLabelǁpaintEvent__mutmut_148, 
        'xǁBlocksLabelǁpaintEvent__mutmut_149': xǁBlocksLabelǁpaintEvent__mutmut_149, 
        'xǁBlocksLabelǁpaintEvent__mutmut_150': xǁBlocksLabelǁpaintEvent__mutmut_150, 
        'xǁBlocksLabelǁpaintEvent__mutmut_151': xǁBlocksLabelǁpaintEvent__mutmut_151, 
        'xǁBlocksLabelǁpaintEvent__mutmut_152': xǁBlocksLabelǁpaintEvent__mutmut_152, 
        'xǁBlocksLabelǁpaintEvent__mutmut_153': xǁBlocksLabelǁpaintEvent__mutmut_153, 
        'xǁBlocksLabelǁpaintEvent__mutmut_154': xǁBlocksLabelǁpaintEvent__mutmut_154, 
        'xǁBlocksLabelǁpaintEvent__mutmut_155': xǁBlocksLabelǁpaintEvent__mutmut_155, 
        'xǁBlocksLabelǁpaintEvent__mutmut_156': xǁBlocksLabelǁpaintEvent__mutmut_156, 
        'xǁBlocksLabelǁpaintEvent__mutmut_157': xǁBlocksLabelǁpaintEvent__mutmut_157, 
        'xǁBlocksLabelǁpaintEvent__mutmut_158': xǁBlocksLabelǁpaintEvent__mutmut_158, 
        'xǁBlocksLabelǁpaintEvent__mutmut_159': xǁBlocksLabelǁpaintEvent__mutmut_159, 
        'xǁBlocksLabelǁpaintEvent__mutmut_160': xǁBlocksLabelǁpaintEvent__mutmut_160, 
        'xǁBlocksLabelǁpaintEvent__mutmut_161': xǁBlocksLabelǁpaintEvent__mutmut_161, 
        'xǁBlocksLabelǁpaintEvent__mutmut_162': xǁBlocksLabelǁpaintEvent__mutmut_162, 
        'xǁBlocksLabelǁpaintEvent__mutmut_163': xǁBlocksLabelǁpaintEvent__mutmut_163, 
        'xǁBlocksLabelǁpaintEvent__mutmut_164': xǁBlocksLabelǁpaintEvent__mutmut_164, 
        'xǁBlocksLabelǁpaintEvent__mutmut_165': xǁBlocksLabelǁpaintEvent__mutmut_165, 
        'xǁBlocksLabelǁpaintEvent__mutmut_166': xǁBlocksLabelǁpaintEvent__mutmut_166, 
        'xǁBlocksLabelǁpaintEvent__mutmut_167': xǁBlocksLabelǁpaintEvent__mutmut_167, 
        'xǁBlocksLabelǁpaintEvent__mutmut_168': xǁBlocksLabelǁpaintEvent__mutmut_168, 
        'xǁBlocksLabelǁpaintEvent__mutmut_169': xǁBlocksLabelǁpaintEvent__mutmut_169, 
        'xǁBlocksLabelǁpaintEvent__mutmut_170': xǁBlocksLabelǁpaintEvent__mutmut_170, 
        'xǁBlocksLabelǁpaintEvent__mutmut_171': xǁBlocksLabelǁpaintEvent__mutmut_171, 
        'xǁBlocksLabelǁpaintEvent__mutmut_172': xǁBlocksLabelǁpaintEvent__mutmut_172, 
        'xǁBlocksLabelǁpaintEvent__mutmut_173': xǁBlocksLabelǁpaintEvent__mutmut_173, 
        'xǁBlocksLabelǁpaintEvent__mutmut_174': xǁBlocksLabelǁpaintEvent__mutmut_174, 
        'xǁBlocksLabelǁpaintEvent__mutmut_175': xǁBlocksLabelǁpaintEvent__mutmut_175, 
        'xǁBlocksLabelǁpaintEvent__mutmut_176': xǁBlocksLabelǁpaintEvent__mutmut_176, 
        'xǁBlocksLabelǁpaintEvent__mutmut_177': xǁBlocksLabelǁpaintEvent__mutmut_177, 
        'xǁBlocksLabelǁpaintEvent__mutmut_178': xǁBlocksLabelǁpaintEvent__mutmut_178, 
        'xǁBlocksLabelǁpaintEvent__mutmut_179': xǁBlocksLabelǁpaintEvent__mutmut_179, 
        'xǁBlocksLabelǁpaintEvent__mutmut_180': xǁBlocksLabelǁpaintEvent__mutmut_180, 
        'xǁBlocksLabelǁpaintEvent__mutmut_181': xǁBlocksLabelǁpaintEvent__mutmut_181, 
        'xǁBlocksLabelǁpaintEvent__mutmut_182': xǁBlocksLabelǁpaintEvent__mutmut_182, 
        'xǁBlocksLabelǁpaintEvent__mutmut_183': xǁBlocksLabelǁpaintEvent__mutmut_183, 
        'xǁBlocksLabelǁpaintEvent__mutmut_184': xǁBlocksLabelǁpaintEvent__mutmut_184, 
        'xǁBlocksLabelǁpaintEvent__mutmut_185': xǁBlocksLabelǁpaintEvent__mutmut_185
    }
    xǁBlocksLabelǁpaintEvent__mutmut_orig.__name__ = 'xǁBlocksLabelǁpaintEvent'

    def setProperty(self, name: str, value: typing.Any) -> bool:
        args = [name, value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksLabelǁsetProperty__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksLabelǁsetProperty__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksLabelǁsetProperty__mutmut_orig(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.setPixmap(value)
        return super().setProperty(name, value)

    def xǁBlocksLabelǁsetProperty__mutmut_1(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name != "icon_pixmap":
            self.setPixmap(value)
        return super().setProperty(name, value)

    def xǁBlocksLabelǁsetProperty__mutmut_2(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "XXicon_pixmapXX":
            self.setPixmap(value)
        return super().setProperty(name, value)

    def xǁBlocksLabelǁsetProperty__mutmut_3(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "ICON_PIXMAP":
            self.setPixmap(value)
        return super().setProperty(name, value)

    def xǁBlocksLabelǁsetProperty__mutmut_4(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.setPixmap(None)
        return super().setProperty(name, value)

    def xǁBlocksLabelǁsetProperty__mutmut_5(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.setPixmap(value)
        return super().setProperty(None, value)

    def xǁBlocksLabelǁsetProperty__mutmut_6(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.setPixmap(value)
        return super().setProperty(name, None)

    def xǁBlocksLabelǁsetProperty__mutmut_7(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.setPixmap(value)
        return super().setProperty(value)

    def xǁBlocksLabelǁsetProperty__mutmut_8(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.setPixmap(value)
        return super().setProperty(name, )
    
    xǁBlocksLabelǁsetProperty__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksLabelǁsetProperty__mutmut_1': xǁBlocksLabelǁsetProperty__mutmut_1, 
        'xǁBlocksLabelǁsetProperty__mutmut_2': xǁBlocksLabelǁsetProperty__mutmut_2, 
        'xǁBlocksLabelǁsetProperty__mutmut_3': xǁBlocksLabelǁsetProperty__mutmut_3, 
        'xǁBlocksLabelǁsetProperty__mutmut_4': xǁBlocksLabelǁsetProperty__mutmut_4, 
        'xǁBlocksLabelǁsetProperty__mutmut_5': xǁBlocksLabelǁsetProperty__mutmut_5, 
        'xǁBlocksLabelǁsetProperty__mutmut_6': xǁBlocksLabelǁsetProperty__mutmut_6, 
        'xǁBlocksLabelǁsetProperty__mutmut_7': xǁBlocksLabelǁsetProperty__mutmut_7, 
        'xǁBlocksLabelǁsetProperty__mutmut_8': xǁBlocksLabelǁsetProperty__mutmut_8
    }
    xǁBlocksLabelǁsetProperty__mutmut_orig.__name__ = 'xǁBlocksLabelǁsetProperty'
