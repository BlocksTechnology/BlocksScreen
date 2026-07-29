import enum
from collections import deque

from lib.utils.icon_button import IconButton
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


class BannerPopup(QtWidgets.QWidget):
    class MessageType(enum.Enum):
        """Popup Message type (level)"""

        CONNECT = enum.auto()
        DISCONNECT = enum.auto()
        CORRUPTED = enum.auto()
        UNKNOWN = enum.auto()

    def __init__(self, parent=None) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁ__init____mutmut_orig(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_1(self, parent=None) -> None:
        if parent:
            super().__init__(None)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_2(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = None
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_3(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(None)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_4(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(None)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_5(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(False)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_6(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = None
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_7(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = None
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_8(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = True
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_9(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = None
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_10(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(None, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_11(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, None, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_12(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, None)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_13(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_14(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_15(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_16(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(165, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_17(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 165, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_18(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 165)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_19(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(None, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_20(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, None)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_21(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_22(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, )
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_23(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_24(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(None)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_25(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(False)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_26(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            None
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_27(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool & QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_28(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint & QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_29(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = None
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_30(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(None, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_31(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, None)
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_32(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_33(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, )
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_34(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"XXgeometryXX")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_35(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"GEOMETRY")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_36(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(None)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_37(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1001)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_38(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(None)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_39(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = None
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_40(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(None, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_41(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, None)
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_42(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_43(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, )
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_44(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"XXgeometryXX")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_45(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"GEOMETRY")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_46(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(None)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_47(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(201)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_48(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(None)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_49(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = None
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_50(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(None)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_51(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(None)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_52(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5001)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_53(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(None)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_54(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(False)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_55(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(None)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_56(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(None)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_57(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4001)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_58(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(None)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_59(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(None)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_60(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(None)
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_61(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: None)
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁBannerPopupǁ__init____mutmut_62(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self.oneshot = QtCore.QTimer(self)
        self.oneshot.setInterval(5000)
        self.oneshot.setSingleShot(True)
        self.oneshot.timeout.connect(self._add_popup)
        self.timeout_timer.setInterval(4000)
        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(None)
    
    xǁBannerPopupǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁ__init____mutmut_1': xǁBannerPopupǁ__init____mutmut_1, 
        'xǁBannerPopupǁ__init____mutmut_2': xǁBannerPopupǁ__init____mutmut_2, 
        'xǁBannerPopupǁ__init____mutmut_3': xǁBannerPopupǁ__init____mutmut_3, 
        'xǁBannerPopupǁ__init____mutmut_4': xǁBannerPopupǁ__init____mutmut_4, 
        'xǁBannerPopupǁ__init____mutmut_5': xǁBannerPopupǁ__init____mutmut_5, 
        'xǁBannerPopupǁ__init____mutmut_6': xǁBannerPopupǁ__init____mutmut_6, 
        'xǁBannerPopupǁ__init____mutmut_7': xǁBannerPopupǁ__init____mutmut_7, 
        'xǁBannerPopupǁ__init____mutmut_8': xǁBannerPopupǁ__init____mutmut_8, 
        'xǁBannerPopupǁ__init____mutmut_9': xǁBannerPopupǁ__init____mutmut_9, 
        'xǁBannerPopupǁ__init____mutmut_10': xǁBannerPopupǁ__init____mutmut_10, 
        'xǁBannerPopupǁ__init____mutmut_11': xǁBannerPopupǁ__init____mutmut_11, 
        'xǁBannerPopupǁ__init____mutmut_12': xǁBannerPopupǁ__init____mutmut_12, 
        'xǁBannerPopupǁ__init____mutmut_13': xǁBannerPopupǁ__init____mutmut_13, 
        'xǁBannerPopupǁ__init____mutmut_14': xǁBannerPopupǁ__init____mutmut_14, 
        'xǁBannerPopupǁ__init____mutmut_15': xǁBannerPopupǁ__init____mutmut_15, 
        'xǁBannerPopupǁ__init____mutmut_16': xǁBannerPopupǁ__init____mutmut_16, 
        'xǁBannerPopupǁ__init____mutmut_17': xǁBannerPopupǁ__init____mutmut_17, 
        'xǁBannerPopupǁ__init____mutmut_18': xǁBannerPopupǁ__init____mutmut_18, 
        'xǁBannerPopupǁ__init____mutmut_19': xǁBannerPopupǁ__init____mutmut_19, 
        'xǁBannerPopupǁ__init____mutmut_20': xǁBannerPopupǁ__init____mutmut_20, 
        'xǁBannerPopupǁ__init____mutmut_21': xǁBannerPopupǁ__init____mutmut_21, 
        'xǁBannerPopupǁ__init____mutmut_22': xǁBannerPopupǁ__init____mutmut_22, 
        'xǁBannerPopupǁ__init____mutmut_23': xǁBannerPopupǁ__init____mutmut_23, 
        'xǁBannerPopupǁ__init____mutmut_24': xǁBannerPopupǁ__init____mutmut_24, 
        'xǁBannerPopupǁ__init____mutmut_25': xǁBannerPopupǁ__init____mutmut_25, 
        'xǁBannerPopupǁ__init____mutmut_26': xǁBannerPopupǁ__init____mutmut_26, 
        'xǁBannerPopupǁ__init____mutmut_27': xǁBannerPopupǁ__init____mutmut_27, 
        'xǁBannerPopupǁ__init____mutmut_28': xǁBannerPopupǁ__init____mutmut_28, 
        'xǁBannerPopupǁ__init____mutmut_29': xǁBannerPopupǁ__init____mutmut_29, 
        'xǁBannerPopupǁ__init____mutmut_30': xǁBannerPopupǁ__init____mutmut_30, 
        'xǁBannerPopupǁ__init____mutmut_31': xǁBannerPopupǁ__init____mutmut_31, 
        'xǁBannerPopupǁ__init____mutmut_32': xǁBannerPopupǁ__init____mutmut_32, 
        'xǁBannerPopupǁ__init____mutmut_33': xǁBannerPopupǁ__init____mutmut_33, 
        'xǁBannerPopupǁ__init____mutmut_34': xǁBannerPopupǁ__init____mutmut_34, 
        'xǁBannerPopupǁ__init____mutmut_35': xǁBannerPopupǁ__init____mutmut_35, 
        'xǁBannerPopupǁ__init____mutmut_36': xǁBannerPopupǁ__init____mutmut_36, 
        'xǁBannerPopupǁ__init____mutmut_37': xǁBannerPopupǁ__init____mutmut_37, 
        'xǁBannerPopupǁ__init____mutmut_38': xǁBannerPopupǁ__init____mutmut_38, 
        'xǁBannerPopupǁ__init____mutmut_39': xǁBannerPopupǁ__init____mutmut_39, 
        'xǁBannerPopupǁ__init____mutmut_40': xǁBannerPopupǁ__init____mutmut_40, 
        'xǁBannerPopupǁ__init____mutmut_41': xǁBannerPopupǁ__init____mutmut_41, 
        'xǁBannerPopupǁ__init____mutmut_42': xǁBannerPopupǁ__init____mutmut_42, 
        'xǁBannerPopupǁ__init____mutmut_43': xǁBannerPopupǁ__init____mutmut_43, 
        'xǁBannerPopupǁ__init____mutmut_44': xǁBannerPopupǁ__init____mutmut_44, 
        'xǁBannerPopupǁ__init____mutmut_45': xǁBannerPopupǁ__init____mutmut_45, 
        'xǁBannerPopupǁ__init____mutmut_46': xǁBannerPopupǁ__init____mutmut_46, 
        'xǁBannerPopupǁ__init____mutmut_47': xǁBannerPopupǁ__init____mutmut_47, 
        'xǁBannerPopupǁ__init____mutmut_48': xǁBannerPopupǁ__init____mutmut_48, 
        'xǁBannerPopupǁ__init____mutmut_49': xǁBannerPopupǁ__init____mutmut_49, 
        'xǁBannerPopupǁ__init____mutmut_50': xǁBannerPopupǁ__init____mutmut_50, 
        'xǁBannerPopupǁ__init____mutmut_51': xǁBannerPopupǁ__init____mutmut_51, 
        'xǁBannerPopupǁ__init____mutmut_52': xǁBannerPopupǁ__init____mutmut_52, 
        'xǁBannerPopupǁ__init____mutmut_53': xǁBannerPopupǁ__init____mutmut_53, 
        'xǁBannerPopupǁ__init____mutmut_54': xǁBannerPopupǁ__init____mutmut_54, 
        'xǁBannerPopupǁ__init____mutmut_55': xǁBannerPopupǁ__init____mutmut_55, 
        'xǁBannerPopupǁ__init____mutmut_56': xǁBannerPopupǁ__init____mutmut_56, 
        'xǁBannerPopupǁ__init____mutmut_57': xǁBannerPopupǁ__init____mutmut_57, 
        'xǁBannerPopupǁ__init____mutmut_58': xǁBannerPopupǁ__init____mutmut_58, 
        'xǁBannerPopupǁ__init____mutmut_59': xǁBannerPopupǁ__init____mutmut_59, 
        'xǁBannerPopupǁ__init____mutmut_60': xǁBannerPopupǁ__init____mutmut_60, 
        'xǁBannerPopupǁ__init____mutmut_61': xǁBannerPopupǁ__init____mutmut_61, 
        'xǁBannerPopupǁ__init____mutmut_62': xǁBannerPopupǁ__init____mutmut_62
    }
    xǁBannerPopupǁ__init____mutmut_orig.__name__ = 'xǁBannerPopupǁ__init__'

    def event(self, a0):
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁevent__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁevent__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁevent__mutmut_orig(self, a0):
        if a0.type() in (QtCore.QEvent.Type.MouseButtonPress,):
            if self.rect().contains(a0.position().toPoint()):
                self.timeout_timer.stop()
                self.slide_out_animation.setStartValue(
                    self.slide_in_animation.currentValue()
                )
                self.slide_in_animation.stop()
                self.slide_out_animation.start()

        return super().event(a0)

    def xǁBannerPopupǁevent__mutmut_1(self, a0):
        if a0.type() not in (QtCore.QEvent.Type.MouseButtonPress,):
            if self.rect().contains(a0.position().toPoint()):
                self.timeout_timer.stop()
                self.slide_out_animation.setStartValue(
                    self.slide_in_animation.currentValue()
                )
                self.slide_in_animation.stop()
                self.slide_out_animation.start()

        return super().event(a0)

    def xǁBannerPopupǁevent__mutmut_2(self, a0):
        if a0.type() in (QtCore.QEvent.Type.MouseButtonPress,):
            if self.rect().contains(None):
                self.timeout_timer.stop()
                self.slide_out_animation.setStartValue(
                    self.slide_in_animation.currentValue()
                )
                self.slide_in_animation.stop()
                self.slide_out_animation.start()

        return super().event(a0)

    def xǁBannerPopupǁevent__mutmut_3(self, a0):
        if a0.type() in (QtCore.QEvent.Type.MouseButtonPress,):
            if self.rect().contains(a0.position().toPoint()):
                self.timeout_timer.stop()
                self.slide_out_animation.setStartValue(
                    None
                )
                self.slide_in_animation.stop()
                self.slide_out_animation.start()

        return super().event(a0)

    def xǁBannerPopupǁevent__mutmut_4(self, a0):
        if a0.type() in (QtCore.QEvent.Type.MouseButtonPress,):
            if self.rect().contains(a0.position().toPoint()):
                self.timeout_timer.stop()
                self.slide_out_animation.setStartValue(
                    self.slide_in_animation.currentValue()
                )
                self.slide_in_animation.stop()
                self.slide_out_animation.start()

        return super().event(None)
    
    xǁBannerPopupǁevent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁevent__mutmut_1': xǁBannerPopupǁevent__mutmut_1, 
        'xǁBannerPopupǁevent__mutmut_2': xǁBannerPopupǁevent__mutmut_2, 
        'xǁBannerPopupǁevent__mutmut_3': xǁBannerPopupǁevent__mutmut_3, 
        'xǁBannerPopupǁevent__mutmut_4': xǁBannerPopupǁevent__mutmut_4
    }
    xǁBannerPopupǁevent__mutmut_orig.__name__ = 'xǁBannerPopupǁevent'

    def on_slide_in_finished(self):
        """Handle slide in animation finished"""
        self.timeout_timer.start()

    def on_slide_out_finished(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁon_slide_out_finished__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁon_slide_out_finished__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁon_slide_out_finished__mutmut_orig(self):
        """Handle slide out animation finished"""
        self.hide()
        self.isShown = False
        self.timeout_timer.stop()
        self._add_popup()

    def xǁBannerPopupǁon_slide_out_finished__mutmut_1(self):
        """Handle slide out animation finished"""
        self.hide()
        self.isShown = None
        self.timeout_timer.stop()
        self._add_popup()

    def xǁBannerPopupǁon_slide_out_finished__mutmut_2(self):
        """Handle slide out animation finished"""
        self.hide()
        self.isShown = True
        self.timeout_timer.stop()
        self._add_popup()
    
    xǁBannerPopupǁon_slide_out_finished__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁon_slide_out_finished__mutmut_1': xǁBannerPopupǁon_slide_out_finished__mutmut_1, 
        'xǁBannerPopupǁon_slide_out_finished__mutmut_2': xǁBannerPopupǁon_slide_out_finished__mutmut_2
    }
    xǁBannerPopupǁon_slide_out_finished__mutmut_orig.__name__ = 'xǁBannerPopupǁon_slide_out_finished'

    def _calculate_target_geometry(self) -> QtCore.QRect:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁ_calculate_target_geometry__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁ_calculate_target_geometry__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_orig(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_1(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = None
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_2(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_3(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None or app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_4(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is not None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_5(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = None
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_6(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    return
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_7(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = None
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_8(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = None
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_9(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(None)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_10(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() / 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_11(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 1.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_12(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = None
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_13(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 81
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_14(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = None
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_15(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width - 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_16(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() + width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_17(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() - parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_18(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 51
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_19(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = None
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_20(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() - 30
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_21(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 31
        return QtCore.QRect(x, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_22(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(None, y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_23(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, None, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_24(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, None, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_25(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, None)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_26(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(y, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_27(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, width, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_28(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, height)

    def xǁBannerPopupǁ_calculate_target_geometry__mutmut_29(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        parent_rect = main_window.geometry()
        width = int(parent_rect.width() * 0.35)
        height = 80
        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30
        return QtCore.QRect(x, y, width, )
    
    xǁBannerPopupǁ_calculate_target_geometry__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁ_calculate_target_geometry__mutmut_1': xǁBannerPopupǁ_calculate_target_geometry__mutmut_1, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_2': xǁBannerPopupǁ_calculate_target_geometry__mutmut_2, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_3': xǁBannerPopupǁ_calculate_target_geometry__mutmut_3, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_4': xǁBannerPopupǁ_calculate_target_geometry__mutmut_4, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_5': xǁBannerPopupǁ_calculate_target_geometry__mutmut_5, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_6': xǁBannerPopupǁ_calculate_target_geometry__mutmut_6, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_7': xǁBannerPopupǁ_calculate_target_geometry__mutmut_7, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_8': xǁBannerPopupǁ_calculate_target_geometry__mutmut_8, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_9': xǁBannerPopupǁ_calculate_target_geometry__mutmut_9, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_10': xǁBannerPopupǁ_calculate_target_geometry__mutmut_10, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_11': xǁBannerPopupǁ_calculate_target_geometry__mutmut_11, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_12': xǁBannerPopupǁ_calculate_target_geometry__mutmut_12, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_13': xǁBannerPopupǁ_calculate_target_geometry__mutmut_13, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_14': xǁBannerPopupǁ_calculate_target_geometry__mutmut_14, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_15': xǁBannerPopupǁ_calculate_target_geometry__mutmut_15, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_16': xǁBannerPopupǁ_calculate_target_geometry__mutmut_16, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_17': xǁBannerPopupǁ_calculate_target_geometry__mutmut_17, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_18': xǁBannerPopupǁ_calculate_target_geometry__mutmut_18, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_19': xǁBannerPopupǁ_calculate_target_geometry__mutmut_19, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_20': xǁBannerPopupǁ_calculate_target_geometry__mutmut_20, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_21': xǁBannerPopupǁ_calculate_target_geometry__mutmut_21, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_22': xǁBannerPopupǁ_calculate_target_geometry__mutmut_22, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_23': xǁBannerPopupǁ_calculate_target_geometry__mutmut_23, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_24': xǁBannerPopupǁ_calculate_target_geometry__mutmut_24, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_25': xǁBannerPopupǁ_calculate_target_geometry__mutmut_25, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_26': xǁBannerPopupǁ_calculate_target_geometry__mutmut_26, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_27': xǁBannerPopupǁ_calculate_target_geometry__mutmut_27, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_28': xǁBannerPopupǁ_calculate_target_geometry__mutmut_28, 
        'xǁBannerPopupǁ_calculate_target_geometry__mutmut_29': xǁBannerPopupǁ_calculate_target_geometry__mutmut_29
    }
    xǁBannerPopupǁ_calculate_target_geometry__mutmut_orig.__name__ = 'xǁBannerPopupǁ_calculate_target_geometry'

    def updateMask(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁupdateMask__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁupdateMask__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁupdateMask__mutmut_orig(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 50, 70)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_1(self) -> None:
        """Update widget mask properties"""
        path = None
        path.addRoundedRect(self.rect().toRectF(), 50, 70)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_2(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(None, 50, 70)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_3(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), None, 70)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_4(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 50, None)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_5(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(50, 70)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_6(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 70)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_7(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 50, )
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_8(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 51, 70)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_9(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 50, 71)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_10(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 50, 70)
        region = None
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_11(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 50, 70)
        region = QtGui.QRegion(None)
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_12(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 50, 70)
        region = QtGui.QRegion(path.toFillPolygon(None).toPolygon())
        self.setMask(region)

    def xǁBannerPopupǁupdateMask__mutmut_13(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 50, 70)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(None)
    
    xǁBannerPopupǁupdateMask__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁupdateMask__mutmut_1': xǁBannerPopupǁupdateMask__mutmut_1, 
        'xǁBannerPopupǁupdateMask__mutmut_2': xǁBannerPopupǁupdateMask__mutmut_2, 
        'xǁBannerPopupǁupdateMask__mutmut_3': xǁBannerPopupǁupdateMask__mutmut_3, 
        'xǁBannerPopupǁupdateMask__mutmut_4': xǁBannerPopupǁupdateMask__mutmut_4, 
        'xǁBannerPopupǁupdateMask__mutmut_5': xǁBannerPopupǁupdateMask__mutmut_5, 
        'xǁBannerPopupǁupdateMask__mutmut_6': xǁBannerPopupǁupdateMask__mutmut_6, 
        'xǁBannerPopupǁupdateMask__mutmut_7': xǁBannerPopupǁupdateMask__mutmut_7, 
        'xǁBannerPopupǁupdateMask__mutmut_8': xǁBannerPopupǁupdateMask__mutmut_8, 
        'xǁBannerPopupǁupdateMask__mutmut_9': xǁBannerPopupǁupdateMask__mutmut_9, 
        'xǁBannerPopupǁupdateMask__mutmut_10': xǁBannerPopupǁupdateMask__mutmut_10, 
        'xǁBannerPopupǁupdateMask__mutmut_11': xǁBannerPopupǁupdateMask__mutmut_11, 
        'xǁBannerPopupǁupdateMask__mutmut_12': xǁBannerPopupǁupdateMask__mutmut_12, 
        'xǁBannerPopupǁupdateMask__mutmut_13': xǁBannerPopupǁupdateMask__mutmut_13
    }
    xǁBannerPopupǁupdateMask__mutmut_orig.__name__ = 'xǁBannerPopupǁupdateMask'

    def mousePressEvent(self, a0: QtGui.QMouseEvent | None) -> None:
        """Re-implemented method, handle mouse press events"""
        return

    def new_message(
        self,
        message_type: MessageType = MessageType.CONNECT,
    ):
        args = [message_type]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁnew_message__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁnew_message__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁnew_message__mutmut_orig(
        self,
        message_type: MessageType = MessageType.CONNECT,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.CONNECT .
        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "type": message_type,
            }
        )
        return self._add_popup()

    def xǁBannerPopupǁnew_message__mutmut_1(
        self,
        message_type: MessageType = MessageType.CONNECT,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.CONNECT .
        Returns:
            _type_: _description_
        """
        if len(self.messages) != 4:
            return

        self.messages.append(
            {
                "type": message_type,
            }
        )
        return self._add_popup()

    def xǁBannerPopupǁnew_message__mutmut_2(
        self,
        message_type: MessageType = MessageType.CONNECT,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.CONNECT .
        Returns:
            _type_: _description_
        """
        if len(self.messages) == 5:
            return

        self.messages.append(
            {
                "type": message_type,
            }
        )
        return self._add_popup()

    def xǁBannerPopupǁnew_message__mutmut_3(
        self,
        message_type: MessageType = MessageType.CONNECT,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.CONNECT .
        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            None
        )
        return self._add_popup()

    def xǁBannerPopupǁnew_message__mutmut_4(
        self,
        message_type: MessageType = MessageType.CONNECT,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.CONNECT .
        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "XXtypeXX": message_type,
            }
        )
        return self._add_popup()

    def xǁBannerPopupǁnew_message__mutmut_5(
        self,
        message_type: MessageType = MessageType.CONNECT,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.CONNECT .
        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "TYPE": message_type,
            }
        )
        return self._add_popup()
    
    xǁBannerPopupǁnew_message__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁnew_message__mutmut_1': xǁBannerPopupǁnew_message__mutmut_1, 
        'xǁBannerPopupǁnew_message__mutmut_2': xǁBannerPopupǁnew_message__mutmut_2, 
        'xǁBannerPopupǁnew_message__mutmut_3': xǁBannerPopupǁnew_message__mutmut_3, 
        'xǁBannerPopupǁnew_message__mutmut_4': xǁBannerPopupǁnew_message__mutmut_4, 
        'xǁBannerPopupǁnew_message__mutmut_5': xǁBannerPopupǁnew_message__mutmut_5
    }
    xǁBannerPopupǁnew_message__mutmut_orig.__name__ = 'xǁBannerPopupǁnew_message'

    def _add_popup(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁ_add_popup__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁ_add_popup__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁ_add_popup__mutmut_orig(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_1(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped or self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_2(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages or self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_3(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state() != QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_4(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state() != QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_5(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = None
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_6(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = None

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_7(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get(None)

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_8(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("XXtypeXX")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_9(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("TYPE")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_10(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = None
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_11(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "XXUnknown EventXX"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_12(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "unknown event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_13(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "UNKNOWN EVENT"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_14(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = None

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_15(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = "XX:ui/media/btn_icons/info.svgXX"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_16(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":UI/MEDIA/BTN_ICONS/INFO.SVG"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_17(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_18(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_19(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_20(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = None
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_21(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "XXUsb ConnectedXX"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_22(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "usb connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_23(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "USB CONNECTED"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_24(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = None
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_25(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "XXUsb DisconnectedXX"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_26(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "usb disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_27(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "USB DISCONNECTED"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_28(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = None
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_29(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "XXUsb CorruptedXX"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_30(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "usb corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_31(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "USB CORRUPTED"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_32(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = None
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_33(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = "XX:/ui/media/btn_icons/troubleshoot.svgXX"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_34(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/UI/MEDIA/BTN_ICONS/TROUBLESHOOT.SVG"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_35(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = None
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_36(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = None

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_37(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(None, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_38(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, None)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_39(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_40(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, )

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_41(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() / 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_42(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 3, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_43(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 1)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_44(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(None)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_45(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(None))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_46(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(None)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_47(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(None)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_48(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(None)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_49(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(None)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_50(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(None)
            self.text_label.setText(message)
            self.show()

    def xǁBannerPopupǁ_add_popup__mutmut_51(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.oneshot.isActive():
                return
            self.oneshot.start()
            return
        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            message_type = message_entry.get("type")

            message = "Unknown Event"
            icon = ":ui/media/btn_icons/info.svg"

            # TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                    message = "Usb Connected"
                    # icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                    message = "Usb Disconnected"
                    # icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                    message = "Usb Corrupted"
                    icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2, 0)

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(None)
            self.show()
    
    xǁBannerPopupǁ_add_popup__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁ_add_popup__mutmut_1': xǁBannerPopupǁ_add_popup__mutmut_1, 
        'xǁBannerPopupǁ_add_popup__mutmut_2': xǁBannerPopupǁ_add_popup__mutmut_2, 
        'xǁBannerPopupǁ_add_popup__mutmut_3': xǁBannerPopupǁ_add_popup__mutmut_3, 
        'xǁBannerPopupǁ_add_popup__mutmut_4': xǁBannerPopupǁ_add_popup__mutmut_4, 
        'xǁBannerPopupǁ_add_popup__mutmut_5': xǁBannerPopupǁ_add_popup__mutmut_5, 
        'xǁBannerPopupǁ_add_popup__mutmut_6': xǁBannerPopupǁ_add_popup__mutmut_6, 
        'xǁBannerPopupǁ_add_popup__mutmut_7': xǁBannerPopupǁ_add_popup__mutmut_7, 
        'xǁBannerPopupǁ_add_popup__mutmut_8': xǁBannerPopupǁ_add_popup__mutmut_8, 
        'xǁBannerPopupǁ_add_popup__mutmut_9': xǁBannerPopupǁ_add_popup__mutmut_9, 
        'xǁBannerPopupǁ_add_popup__mutmut_10': xǁBannerPopupǁ_add_popup__mutmut_10, 
        'xǁBannerPopupǁ_add_popup__mutmut_11': xǁBannerPopupǁ_add_popup__mutmut_11, 
        'xǁBannerPopupǁ_add_popup__mutmut_12': xǁBannerPopupǁ_add_popup__mutmut_12, 
        'xǁBannerPopupǁ_add_popup__mutmut_13': xǁBannerPopupǁ_add_popup__mutmut_13, 
        'xǁBannerPopupǁ_add_popup__mutmut_14': xǁBannerPopupǁ_add_popup__mutmut_14, 
        'xǁBannerPopupǁ_add_popup__mutmut_15': xǁBannerPopupǁ_add_popup__mutmut_15, 
        'xǁBannerPopupǁ_add_popup__mutmut_16': xǁBannerPopupǁ_add_popup__mutmut_16, 
        'xǁBannerPopupǁ_add_popup__mutmut_17': xǁBannerPopupǁ_add_popup__mutmut_17, 
        'xǁBannerPopupǁ_add_popup__mutmut_18': xǁBannerPopupǁ_add_popup__mutmut_18, 
        'xǁBannerPopupǁ_add_popup__mutmut_19': xǁBannerPopupǁ_add_popup__mutmut_19, 
        'xǁBannerPopupǁ_add_popup__mutmut_20': xǁBannerPopupǁ_add_popup__mutmut_20, 
        'xǁBannerPopupǁ_add_popup__mutmut_21': xǁBannerPopupǁ_add_popup__mutmut_21, 
        'xǁBannerPopupǁ_add_popup__mutmut_22': xǁBannerPopupǁ_add_popup__mutmut_22, 
        'xǁBannerPopupǁ_add_popup__mutmut_23': xǁBannerPopupǁ_add_popup__mutmut_23, 
        'xǁBannerPopupǁ_add_popup__mutmut_24': xǁBannerPopupǁ_add_popup__mutmut_24, 
        'xǁBannerPopupǁ_add_popup__mutmut_25': xǁBannerPopupǁ_add_popup__mutmut_25, 
        'xǁBannerPopupǁ_add_popup__mutmut_26': xǁBannerPopupǁ_add_popup__mutmut_26, 
        'xǁBannerPopupǁ_add_popup__mutmut_27': xǁBannerPopupǁ_add_popup__mutmut_27, 
        'xǁBannerPopupǁ_add_popup__mutmut_28': xǁBannerPopupǁ_add_popup__mutmut_28, 
        'xǁBannerPopupǁ_add_popup__mutmut_29': xǁBannerPopupǁ_add_popup__mutmut_29, 
        'xǁBannerPopupǁ_add_popup__mutmut_30': xǁBannerPopupǁ_add_popup__mutmut_30, 
        'xǁBannerPopupǁ_add_popup__mutmut_31': xǁBannerPopupǁ_add_popup__mutmut_31, 
        'xǁBannerPopupǁ_add_popup__mutmut_32': xǁBannerPopupǁ_add_popup__mutmut_32, 
        'xǁBannerPopupǁ_add_popup__mutmut_33': xǁBannerPopupǁ_add_popup__mutmut_33, 
        'xǁBannerPopupǁ_add_popup__mutmut_34': xǁBannerPopupǁ_add_popup__mutmut_34, 
        'xǁBannerPopupǁ_add_popup__mutmut_35': xǁBannerPopupǁ_add_popup__mutmut_35, 
        'xǁBannerPopupǁ_add_popup__mutmut_36': xǁBannerPopupǁ_add_popup__mutmut_36, 
        'xǁBannerPopupǁ_add_popup__mutmut_37': xǁBannerPopupǁ_add_popup__mutmut_37, 
        'xǁBannerPopupǁ_add_popup__mutmut_38': xǁBannerPopupǁ_add_popup__mutmut_38, 
        'xǁBannerPopupǁ_add_popup__mutmut_39': xǁBannerPopupǁ_add_popup__mutmut_39, 
        'xǁBannerPopupǁ_add_popup__mutmut_40': xǁBannerPopupǁ_add_popup__mutmut_40, 
        'xǁBannerPopupǁ_add_popup__mutmut_41': xǁBannerPopupǁ_add_popup__mutmut_41, 
        'xǁBannerPopupǁ_add_popup__mutmut_42': xǁBannerPopupǁ_add_popup__mutmut_42, 
        'xǁBannerPopupǁ_add_popup__mutmut_43': xǁBannerPopupǁ_add_popup__mutmut_43, 
        'xǁBannerPopupǁ_add_popup__mutmut_44': xǁBannerPopupǁ_add_popup__mutmut_44, 
        'xǁBannerPopupǁ_add_popup__mutmut_45': xǁBannerPopupǁ_add_popup__mutmut_45, 
        'xǁBannerPopupǁ_add_popup__mutmut_46': xǁBannerPopupǁ_add_popup__mutmut_46, 
        'xǁBannerPopupǁ_add_popup__mutmut_47': xǁBannerPopupǁ_add_popup__mutmut_47, 
        'xǁBannerPopupǁ_add_popup__mutmut_48': xǁBannerPopupǁ_add_popup__mutmut_48, 
        'xǁBannerPopupǁ_add_popup__mutmut_49': xǁBannerPopupǁ_add_popup__mutmut_49, 
        'xǁBannerPopupǁ_add_popup__mutmut_50': xǁBannerPopupǁ_add_popup__mutmut_50, 
        'xǁBannerPopupǁ_add_popup__mutmut_51': xǁBannerPopupǁ_add_popup__mutmut_51
    }
    xǁBannerPopupǁ_add_popup__mutmut_orig.__name__ = 'xǁBannerPopupǁ_add_popup'

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁshowEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁshowEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁshowEvent__mutmut_orig(self, a0: QtGui.QShowEvent | None) -> None:
        """Re-implementation, widget show"""
        self.slide_in_animation.start()
        self.isShown = True
        super().showEvent(a0)

    def xǁBannerPopupǁshowEvent__mutmut_1(self, a0: QtGui.QShowEvent | None) -> None:
        """Re-implementation, widget show"""
        self.slide_in_animation.start()
        self.isShown = None
        super().showEvent(a0)

    def xǁBannerPopupǁshowEvent__mutmut_2(self, a0: QtGui.QShowEvent | None) -> None:
        """Re-implementation, widget show"""
        self.slide_in_animation.start()
        self.isShown = False
        super().showEvent(a0)

    def xǁBannerPopupǁshowEvent__mutmut_3(self, a0: QtGui.QShowEvent | None) -> None:
        """Re-implementation, widget show"""
        self.slide_in_animation.start()
        self.isShown = True
        super().showEvent(None)
    
    xǁBannerPopupǁshowEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁshowEvent__mutmut_1': xǁBannerPopupǁshowEvent__mutmut_1, 
        'xǁBannerPopupǁshowEvent__mutmut_2': xǁBannerPopupǁshowEvent__mutmut_2, 
        'xǁBannerPopupǁshowEvent__mutmut_3': xǁBannerPopupǁshowEvent__mutmut_3
    }
    xǁBannerPopupǁshowEvent__mutmut_orig.__name__ = 'xǁBannerPopupǁshowEvent'

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁresizeEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁresizeEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁresizeEvent__mutmut_orig(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implementation, handle resize event"""
        self.updateMask()
        super().resizeEvent(a0)

    def xǁBannerPopupǁresizeEvent__mutmut_1(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implementation, handle resize event"""
        self.updateMask()
        super().resizeEvent(None)
    
    xǁBannerPopupǁresizeEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁresizeEvent__mutmut_1': xǁBannerPopupǁresizeEvent__mutmut_1
    }
    xǁBannerPopupǁresizeEvent__mutmut_orig.__name__ = 'xǁBannerPopupǁresizeEvent'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁpaintEvent__mutmut_orig(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_1(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = None
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_2(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(None)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_3(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_4(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, None)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_5(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_6(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, )

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_7(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, False)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_8(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = None

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_9(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = None
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_10(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(None)
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_11(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = None

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_12(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(None, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_13(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, None)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_14(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_15(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, )

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_16(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() * 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_17(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 3.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_18(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(None, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_19(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, None)
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_20(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(_base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_21(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, )
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_22(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(1, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_23(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(None))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_24(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(161))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_25(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(None, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_26(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, None)

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_27(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(_base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_28(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, )

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_29(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(2.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_30(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(None))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_31(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(201))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_32(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(None)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_33(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(None)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_34(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(None, 50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_35(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), None, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_36(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, None)

    def xǁBannerPopupǁpaintEvent__mutmut_37(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(50, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_38(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 70)

    def xǁBannerPopupǁpaintEvent__mutmut_39(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, )

    def xǁBannerPopupǁpaintEvent__mutmut_40(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 51, 70)

    def xǁBannerPopupǁpaintEvent__mutmut_41(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 71)
    
    xǁBannerPopupǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁpaintEvent__mutmut_1': xǁBannerPopupǁpaintEvent__mutmut_1, 
        'xǁBannerPopupǁpaintEvent__mutmut_2': xǁBannerPopupǁpaintEvent__mutmut_2, 
        'xǁBannerPopupǁpaintEvent__mutmut_3': xǁBannerPopupǁpaintEvent__mutmut_3, 
        'xǁBannerPopupǁpaintEvent__mutmut_4': xǁBannerPopupǁpaintEvent__mutmut_4, 
        'xǁBannerPopupǁpaintEvent__mutmut_5': xǁBannerPopupǁpaintEvent__mutmut_5, 
        'xǁBannerPopupǁpaintEvent__mutmut_6': xǁBannerPopupǁpaintEvent__mutmut_6, 
        'xǁBannerPopupǁpaintEvent__mutmut_7': xǁBannerPopupǁpaintEvent__mutmut_7, 
        'xǁBannerPopupǁpaintEvent__mutmut_8': xǁBannerPopupǁpaintEvent__mutmut_8, 
        'xǁBannerPopupǁpaintEvent__mutmut_9': xǁBannerPopupǁpaintEvent__mutmut_9, 
        'xǁBannerPopupǁpaintEvent__mutmut_10': xǁBannerPopupǁpaintEvent__mutmut_10, 
        'xǁBannerPopupǁpaintEvent__mutmut_11': xǁBannerPopupǁpaintEvent__mutmut_11, 
        'xǁBannerPopupǁpaintEvent__mutmut_12': xǁBannerPopupǁpaintEvent__mutmut_12, 
        'xǁBannerPopupǁpaintEvent__mutmut_13': xǁBannerPopupǁpaintEvent__mutmut_13, 
        'xǁBannerPopupǁpaintEvent__mutmut_14': xǁBannerPopupǁpaintEvent__mutmut_14, 
        'xǁBannerPopupǁpaintEvent__mutmut_15': xǁBannerPopupǁpaintEvent__mutmut_15, 
        'xǁBannerPopupǁpaintEvent__mutmut_16': xǁBannerPopupǁpaintEvent__mutmut_16, 
        'xǁBannerPopupǁpaintEvent__mutmut_17': xǁBannerPopupǁpaintEvent__mutmut_17, 
        'xǁBannerPopupǁpaintEvent__mutmut_18': xǁBannerPopupǁpaintEvent__mutmut_18, 
        'xǁBannerPopupǁpaintEvent__mutmut_19': xǁBannerPopupǁpaintEvent__mutmut_19, 
        'xǁBannerPopupǁpaintEvent__mutmut_20': xǁBannerPopupǁpaintEvent__mutmut_20, 
        'xǁBannerPopupǁpaintEvent__mutmut_21': xǁBannerPopupǁpaintEvent__mutmut_21, 
        'xǁBannerPopupǁpaintEvent__mutmut_22': xǁBannerPopupǁpaintEvent__mutmut_22, 
        'xǁBannerPopupǁpaintEvent__mutmut_23': xǁBannerPopupǁpaintEvent__mutmut_23, 
        'xǁBannerPopupǁpaintEvent__mutmut_24': xǁBannerPopupǁpaintEvent__mutmut_24, 
        'xǁBannerPopupǁpaintEvent__mutmut_25': xǁBannerPopupǁpaintEvent__mutmut_25, 
        'xǁBannerPopupǁpaintEvent__mutmut_26': xǁBannerPopupǁpaintEvent__mutmut_26, 
        'xǁBannerPopupǁpaintEvent__mutmut_27': xǁBannerPopupǁpaintEvent__mutmut_27, 
        'xǁBannerPopupǁpaintEvent__mutmut_28': xǁBannerPopupǁpaintEvent__mutmut_28, 
        'xǁBannerPopupǁpaintEvent__mutmut_29': xǁBannerPopupǁpaintEvent__mutmut_29, 
        'xǁBannerPopupǁpaintEvent__mutmut_30': xǁBannerPopupǁpaintEvent__mutmut_30, 
        'xǁBannerPopupǁpaintEvent__mutmut_31': xǁBannerPopupǁpaintEvent__mutmut_31, 
        'xǁBannerPopupǁpaintEvent__mutmut_32': xǁBannerPopupǁpaintEvent__mutmut_32, 
        'xǁBannerPopupǁpaintEvent__mutmut_33': xǁBannerPopupǁpaintEvent__mutmut_33, 
        'xǁBannerPopupǁpaintEvent__mutmut_34': xǁBannerPopupǁpaintEvent__mutmut_34, 
        'xǁBannerPopupǁpaintEvent__mutmut_35': xǁBannerPopupǁpaintEvent__mutmut_35, 
        'xǁBannerPopupǁpaintEvent__mutmut_36': xǁBannerPopupǁpaintEvent__mutmut_36, 
        'xǁBannerPopupǁpaintEvent__mutmut_37': xǁBannerPopupǁpaintEvent__mutmut_37, 
        'xǁBannerPopupǁpaintEvent__mutmut_38': xǁBannerPopupǁpaintEvent__mutmut_38, 
        'xǁBannerPopupǁpaintEvent__mutmut_39': xǁBannerPopupǁpaintEvent__mutmut_39, 
        'xǁBannerPopupǁpaintEvent__mutmut_40': xǁBannerPopupǁpaintEvent__mutmut_40, 
        'xǁBannerPopupǁpaintEvent__mutmut_41': xǁBannerPopupǁpaintEvent__mutmut_41
    }
    xǁBannerPopupǁpaintEvent__mutmut_orig.__name__ = 'xǁBannerPopupǁpaintEvent'

    def _setupUI(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBannerPopupǁ_setupUI__mutmut_orig'), object.__getattribute__(self, 'xǁBannerPopupǁ_setupUI__mutmut_mutants'), args, kwargs, self)

    def xǁBannerPopupǁ_setupUI__mutmut_orig(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_1(self) -> None:
        self.horizontal_layout = None
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_2(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(None)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_3(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(None, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_4(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, None, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_5(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, None, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_6(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, None)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_7(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_8(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_9(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_10(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, )

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_11(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(6, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_12(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 6, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_13(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 6, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_14(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 6)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_15(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = None
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_16(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(None)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_17(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(None)
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_18(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(None, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_19(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, None))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_20(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_21(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, ))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_22(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(61, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_23(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 61))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_24(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(None)
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_25(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(None, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_26(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, None))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_27(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_28(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, ))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_29(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(61, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_30(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 61))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_31(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(None)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_32(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(False)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_33(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = None
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_34(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(None)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_35(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet(None)
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_36(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("XXbackground: transparent; color:whiteXX")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_37(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("BACKGROUND: TRANSPARENT; COLOR:WHITE")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_38(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(None)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_39(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(None)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_40(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(False)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_41(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = None
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_42(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(None)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_43(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(19)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_44(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily(None)
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_45(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("XXsans-serifXX")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_46(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("SANS-SERIF")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_47(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = None
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_48(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            None, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_49(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, None
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_50(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_51(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_52(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(None)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_53(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(None)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_54(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = None
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_55(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(None)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_56(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(None)

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_57(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(None, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_58(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, None))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_59(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_60(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, ))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_61(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(61, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_62(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 61))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_63(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(None)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_64(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(None)
        self.horizontal_layout.addWidget(self.actionbtn)

    def xǁBannerPopupǁ_setupUI__mutmut_65(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(None)
    
    xǁBannerPopupǁ_setupUI__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBannerPopupǁ_setupUI__mutmut_1': xǁBannerPopupǁ_setupUI__mutmut_1, 
        'xǁBannerPopupǁ_setupUI__mutmut_2': xǁBannerPopupǁ_setupUI__mutmut_2, 
        'xǁBannerPopupǁ_setupUI__mutmut_3': xǁBannerPopupǁ_setupUI__mutmut_3, 
        'xǁBannerPopupǁ_setupUI__mutmut_4': xǁBannerPopupǁ_setupUI__mutmut_4, 
        'xǁBannerPopupǁ_setupUI__mutmut_5': xǁBannerPopupǁ_setupUI__mutmut_5, 
        'xǁBannerPopupǁ_setupUI__mutmut_6': xǁBannerPopupǁ_setupUI__mutmut_6, 
        'xǁBannerPopupǁ_setupUI__mutmut_7': xǁBannerPopupǁ_setupUI__mutmut_7, 
        'xǁBannerPopupǁ_setupUI__mutmut_8': xǁBannerPopupǁ_setupUI__mutmut_8, 
        'xǁBannerPopupǁ_setupUI__mutmut_9': xǁBannerPopupǁ_setupUI__mutmut_9, 
        'xǁBannerPopupǁ_setupUI__mutmut_10': xǁBannerPopupǁ_setupUI__mutmut_10, 
        'xǁBannerPopupǁ_setupUI__mutmut_11': xǁBannerPopupǁ_setupUI__mutmut_11, 
        'xǁBannerPopupǁ_setupUI__mutmut_12': xǁBannerPopupǁ_setupUI__mutmut_12, 
        'xǁBannerPopupǁ_setupUI__mutmut_13': xǁBannerPopupǁ_setupUI__mutmut_13, 
        'xǁBannerPopupǁ_setupUI__mutmut_14': xǁBannerPopupǁ_setupUI__mutmut_14, 
        'xǁBannerPopupǁ_setupUI__mutmut_15': xǁBannerPopupǁ_setupUI__mutmut_15, 
        'xǁBannerPopupǁ_setupUI__mutmut_16': xǁBannerPopupǁ_setupUI__mutmut_16, 
        'xǁBannerPopupǁ_setupUI__mutmut_17': xǁBannerPopupǁ_setupUI__mutmut_17, 
        'xǁBannerPopupǁ_setupUI__mutmut_18': xǁBannerPopupǁ_setupUI__mutmut_18, 
        'xǁBannerPopupǁ_setupUI__mutmut_19': xǁBannerPopupǁ_setupUI__mutmut_19, 
        'xǁBannerPopupǁ_setupUI__mutmut_20': xǁBannerPopupǁ_setupUI__mutmut_20, 
        'xǁBannerPopupǁ_setupUI__mutmut_21': xǁBannerPopupǁ_setupUI__mutmut_21, 
        'xǁBannerPopupǁ_setupUI__mutmut_22': xǁBannerPopupǁ_setupUI__mutmut_22, 
        'xǁBannerPopupǁ_setupUI__mutmut_23': xǁBannerPopupǁ_setupUI__mutmut_23, 
        'xǁBannerPopupǁ_setupUI__mutmut_24': xǁBannerPopupǁ_setupUI__mutmut_24, 
        'xǁBannerPopupǁ_setupUI__mutmut_25': xǁBannerPopupǁ_setupUI__mutmut_25, 
        'xǁBannerPopupǁ_setupUI__mutmut_26': xǁBannerPopupǁ_setupUI__mutmut_26, 
        'xǁBannerPopupǁ_setupUI__mutmut_27': xǁBannerPopupǁ_setupUI__mutmut_27, 
        'xǁBannerPopupǁ_setupUI__mutmut_28': xǁBannerPopupǁ_setupUI__mutmut_28, 
        'xǁBannerPopupǁ_setupUI__mutmut_29': xǁBannerPopupǁ_setupUI__mutmut_29, 
        'xǁBannerPopupǁ_setupUI__mutmut_30': xǁBannerPopupǁ_setupUI__mutmut_30, 
        'xǁBannerPopupǁ_setupUI__mutmut_31': xǁBannerPopupǁ_setupUI__mutmut_31, 
        'xǁBannerPopupǁ_setupUI__mutmut_32': xǁBannerPopupǁ_setupUI__mutmut_32, 
        'xǁBannerPopupǁ_setupUI__mutmut_33': xǁBannerPopupǁ_setupUI__mutmut_33, 
        'xǁBannerPopupǁ_setupUI__mutmut_34': xǁBannerPopupǁ_setupUI__mutmut_34, 
        'xǁBannerPopupǁ_setupUI__mutmut_35': xǁBannerPopupǁ_setupUI__mutmut_35, 
        'xǁBannerPopupǁ_setupUI__mutmut_36': xǁBannerPopupǁ_setupUI__mutmut_36, 
        'xǁBannerPopupǁ_setupUI__mutmut_37': xǁBannerPopupǁ_setupUI__mutmut_37, 
        'xǁBannerPopupǁ_setupUI__mutmut_38': xǁBannerPopupǁ_setupUI__mutmut_38, 
        'xǁBannerPopupǁ_setupUI__mutmut_39': xǁBannerPopupǁ_setupUI__mutmut_39, 
        'xǁBannerPopupǁ_setupUI__mutmut_40': xǁBannerPopupǁ_setupUI__mutmut_40, 
        'xǁBannerPopupǁ_setupUI__mutmut_41': xǁBannerPopupǁ_setupUI__mutmut_41, 
        'xǁBannerPopupǁ_setupUI__mutmut_42': xǁBannerPopupǁ_setupUI__mutmut_42, 
        'xǁBannerPopupǁ_setupUI__mutmut_43': xǁBannerPopupǁ_setupUI__mutmut_43, 
        'xǁBannerPopupǁ_setupUI__mutmut_44': xǁBannerPopupǁ_setupUI__mutmut_44, 
        'xǁBannerPopupǁ_setupUI__mutmut_45': xǁBannerPopupǁ_setupUI__mutmut_45, 
        'xǁBannerPopupǁ_setupUI__mutmut_46': xǁBannerPopupǁ_setupUI__mutmut_46, 
        'xǁBannerPopupǁ_setupUI__mutmut_47': xǁBannerPopupǁ_setupUI__mutmut_47, 
        'xǁBannerPopupǁ_setupUI__mutmut_48': xǁBannerPopupǁ_setupUI__mutmut_48, 
        'xǁBannerPopupǁ_setupUI__mutmut_49': xǁBannerPopupǁ_setupUI__mutmut_49, 
        'xǁBannerPopupǁ_setupUI__mutmut_50': xǁBannerPopupǁ_setupUI__mutmut_50, 
        'xǁBannerPopupǁ_setupUI__mutmut_51': xǁBannerPopupǁ_setupUI__mutmut_51, 
        'xǁBannerPopupǁ_setupUI__mutmut_52': xǁBannerPopupǁ_setupUI__mutmut_52, 
        'xǁBannerPopupǁ_setupUI__mutmut_53': xǁBannerPopupǁ_setupUI__mutmut_53, 
        'xǁBannerPopupǁ_setupUI__mutmut_54': xǁBannerPopupǁ_setupUI__mutmut_54, 
        'xǁBannerPopupǁ_setupUI__mutmut_55': xǁBannerPopupǁ_setupUI__mutmut_55, 
        'xǁBannerPopupǁ_setupUI__mutmut_56': xǁBannerPopupǁ_setupUI__mutmut_56, 
        'xǁBannerPopupǁ_setupUI__mutmut_57': xǁBannerPopupǁ_setupUI__mutmut_57, 
        'xǁBannerPopupǁ_setupUI__mutmut_58': xǁBannerPopupǁ_setupUI__mutmut_58, 
        'xǁBannerPopupǁ_setupUI__mutmut_59': xǁBannerPopupǁ_setupUI__mutmut_59, 
        'xǁBannerPopupǁ_setupUI__mutmut_60': xǁBannerPopupǁ_setupUI__mutmut_60, 
        'xǁBannerPopupǁ_setupUI__mutmut_61': xǁBannerPopupǁ_setupUI__mutmut_61, 
        'xǁBannerPopupǁ_setupUI__mutmut_62': xǁBannerPopupǁ_setupUI__mutmut_62, 
        'xǁBannerPopupǁ_setupUI__mutmut_63': xǁBannerPopupǁ_setupUI__mutmut_63, 
        'xǁBannerPopupǁ_setupUI__mutmut_64': xǁBannerPopupǁ_setupUI__mutmut_64, 
        'xǁBannerPopupǁ_setupUI__mutmut_65': xǁBannerPopupǁ_setupUI__mutmut_65
    }
    xǁBannerPopupǁ_setupUI__mutmut_orig.__name__ = 'xǁBannerPopupǁ_setupUI'
