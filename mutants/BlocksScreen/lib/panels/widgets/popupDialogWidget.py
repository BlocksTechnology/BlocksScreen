import enum
from collections import deque
from typing import Deque

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


class Popup(QtWidgets.QDialog):
    class MessageType(enum.Enum):
        """Popup Message type (level)"""

        INFO = enum.auto()
        WARNING = enum.auto()
        ERROR = enum.auto()
        UNKNOWN = enum.auto()

    class ColorCode(enum.Enum):
        """Popup message-color code"""

        INFO = QtGui.QColor("#446CDB")
        WARNING = QtGui.QColor("#E7E147")
        ERROR = QtGui.QColor("#CA4949")

    def __init__(self, parent) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁ__init____mutmut_orig(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_1(self, parent) -> None:
        super().__init__(None)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_2(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = None
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_3(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(None)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_4(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(None)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_5(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(False)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_6(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = None
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_7(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = None
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_8(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = True
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_9(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = None
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_10(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = None
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_11(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = None
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_12(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(None, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_13(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, None, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_14(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, None)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_15(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_16(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_17(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, )
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_18(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(165, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_19(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 165, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_20(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 165)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_21(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = None
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_22(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(None)
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_23(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap("XX:ui/media/btn_icons/info.svgXX")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_24(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":UI/MEDIA/BTN_ICONS/INFO.SVG")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_25(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = None
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_26(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(None)
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_27(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap("XX:ui/media/btn_icons/warning.svgXX")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_28(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":UI/MEDIA/BTN_ICONS/WARNING.SVG")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_29(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = None
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_30(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(None)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_31(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap("XX:ui/media/btn_icons/error.svgXX")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_32(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":UI/MEDIA/BTN_ICONS/ERROR.SVG")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_33(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(None, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_34(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, None)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_35(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_36(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, )
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_37(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_38(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(None)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_39(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(False)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_40(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
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

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_41(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint & QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_42(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup & QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_43(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = None
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_44(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(None, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_45(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, None)
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_46(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_47(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, )
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_48(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"XXgeometryXX")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_49(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"GEOMETRY")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_50(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(None)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_51(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1001)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_52(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(None)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_53(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = None
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_54(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(None, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_55(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, None)
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_56(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_57(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, )
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_58(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"XXgeometryXX")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_59(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"GEOMETRY")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_60(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(None)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_61(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(201)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_62(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(None)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_63(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = None
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_64(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(None)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_65(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(None)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_66(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5001)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_67(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(None)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_68(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(False)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_69(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(None)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_70(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(None)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_71(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(None)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_72(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(None)
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_73(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: None)
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def xǁPopupǁ__init____mutmut_74(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(None)
    
    xǁPopupǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁ__init____mutmut_1': xǁPopupǁ__init____mutmut_1, 
        'xǁPopupǁ__init____mutmut_2': xǁPopupǁ__init____mutmut_2, 
        'xǁPopupǁ__init____mutmut_3': xǁPopupǁ__init____mutmut_3, 
        'xǁPopupǁ__init____mutmut_4': xǁPopupǁ__init____mutmut_4, 
        'xǁPopupǁ__init____mutmut_5': xǁPopupǁ__init____mutmut_5, 
        'xǁPopupǁ__init____mutmut_6': xǁPopupǁ__init____mutmut_6, 
        'xǁPopupǁ__init____mutmut_7': xǁPopupǁ__init____mutmut_7, 
        'xǁPopupǁ__init____mutmut_8': xǁPopupǁ__init____mutmut_8, 
        'xǁPopupǁ__init____mutmut_9': xǁPopupǁ__init____mutmut_9, 
        'xǁPopupǁ__init____mutmut_10': xǁPopupǁ__init____mutmut_10, 
        'xǁPopupǁ__init____mutmut_11': xǁPopupǁ__init____mutmut_11, 
        'xǁPopupǁ__init____mutmut_12': xǁPopupǁ__init____mutmut_12, 
        'xǁPopupǁ__init____mutmut_13': xǁPopupǁ__init____mutmut_13, 
        'xǁPopupǁ__init____mutmut_14': xǁPopupǁ__init____mutmut_14, 
        'xǁPopupǁ__init____mutmut_15': xǁPopupǁ__init____mutmut_15, 
        'xǁPopupǁ__init____mutmut_16': xǁPopupǁ__init____mutmut_16, 
        'xǁPopupǁ__init____mutmut_17': xǁPopupǁ__init____mutmut_17, 
        'xǁPopupǁ__init____mutmut_18': xǁPopupǁ__init____mutmut_18, 
        'xǁPopupǁ__init____mutmut_19': xǁPopupǁ__init____mutmut_19, 
        'xǁPopupǁ__init____mutmut_20': xǁPopupǁ__init____mutmut_20, 
        'xǁPopupǁ__init____mutmut_21': xǁPopupǁ__init____mutmut_21, 
        'xǁPopupǁ__init____mutmut_22': xǁPopupǁ__init____mutmut_22, 
        'xǁPopupǁ__init____mutmut_23': xǁPopupǁ__init____mutmut_23, 
        'xǁPopupǁ__init____mutmut_24': xǁPopupǁ__init____mutmut_24, 
        'xǁPopupǁ__init____mutmut_25': xǁPopupǁ__init____mutmut_25, 
        'xǁPopupǁ__init____mutmut_26': xǁPopupǁ__init____mutmut_26, 
        'xǁPopupǁ__init____mutmut_27': xǁPopupǁ__init____mutmut_27, 
        'xǁPopupǁ__init____mutmut_28': xǁPopupǁ__init____mutmut_28, 
        'xǁPopupǁ__init____mutmut_29': xǁPopupǁ__init____mutmut_29, 
        'xǁPopupǁ__init____mutmut_30': xǁPopupǁ__init____mutmut_30, 
        'xǁPopupǁ__init____mutmut_31': xǁPopupǁ__init____mutmut_31, 
        'xǁPopupǁ__init____mutmut_32': xǁPopupǁ__init____mutmut_32, 
        'xǁPopupǁ__init____mutmut_33': xǁPopupǁ__init____mutmut_33, 
        'xǁPopupǁ__init____mutmut_34': xǁPopupǁ__init____mutmut_34, 
        'xǁPopupǁ__init____mutmut_35': xǁPopupǁ__init____mutmut_35, 
        'xǁPopupǁ__init____mutmut_36': xǁPopupǁ__init____mutmut_36, 
        'xǁPopupǁ__init____mutmut_37': xǁPopupǁ__init____mutmut_37, 
        'xǁPopupǁ__init____mutmut_38': xǁPopupǁ__init____mutmut_38, 
        'xǁPopupǁ__init____mutmut_39': xǁPopupǁ__init____mutmut_39, 
        'xǁPopupǁ__init____mutmut_40': xǁPopupǁ__init____mutmut_40, 
        'xǁPopupǁ__init____mutmut_41': xǁPopupǁ__init____mutmut_41, 
        'xǁPopupǁ__init____mutmut_42': xǁPopupǁ__init____mutmut_42, 
        'xǁPopupǁ__init____mutmut_43': xǁPopupǁ__init____mutmut_43, 
        'xǁPopupǁ__init____mutmut_44': xǁPopupǁ__init____mutmut_44, 
        'xǁPopupǁ__init____mutmut_45': xǁPopupǁ__init____mutmut_45, 
        'xǁPopupǁ__init____mutmut_46': xǁPopupǁ__init____mutmut_46, 
        'xǁPopupǁ__init____mutmut_47': xǁPopupǁ__init____mutmut_47, 
        'xǁPopupǁ__init____mutmut_48': xǁPopupǁ__init____mutmut_48, 
        'xǁPopupǁ__init____mutmut_49': xǁPopupǁ__init____mutmut_49, 
        'xǁPopupǁ__init____mutmut_50': xǁPopupǁ__init____mutmut_50, 
        'xǁPopupǁ__init____mutmut_51': xǁPopupǁ__init____mutmut_51, 
        'xǁPopupǁ__init____mutmut_52': xǁPopupǁ__init____mutmut_52, 
        'xǁPopupǁ__init____mutmut_53': xǁPopupǁ__init____mutmut_53, 
        'xǁPopupǁ__init____mutmut_54': xǁPopupǁ__init____mutmut_54, 
        'xǁPopupǁ__init____mutmut_55': xǁPopupǁ__init____mutmut_55, 
        'xǁPopupǁ__init____mutmut_56': xǁPopupǁ__init____mutmut_56, 
        'xǁPopupǁ__init____mutmut_57': xǁPopupǁ__init____mutmut_57, 
        'xǁPopupǁ__init____mutmut_58': xǁPopupǁ__init____mutmut_58, 
        'xǁPopupǁ__init____mutmut_59': xǁPopupǁ__init____mutmut_59, 
        'xǁPopupǁ__init____mutmut_60': xǁPopupǁ__init____mutmut_60, 
        'xǁPopupǁ__init____mutmut_61': xǁPopupǁ__init____mutmut_61, 
        'xǁPopupǁ__init____mutmut_62': xǁPopupǁ__init____mutmut_62, 
        'xǁPopupǁ__init____mutmut_63': xǁPopupǁ__init____mutmut_63, 
        'xǁPopupǁ__init____mutmut_64': xǁPopupǁ__init____mutmut_64, 
        'xǁPopupǁ__init____mutmut_65': xǁPopupǁ__init____mutmut_65, 
        'xǁPopupǁ__init____mutmut_66': xǁPopupǁ__init____mutmut_66, 
        'xǁPopupǁ__init____mutmut_67': xǁPopupǁ__init____mutmut_67, 
        'xǁPopupǁ__init____mutmut_68': xǁPopupǁ__init____mutmut_68, 
        'xǁPopupǁ__init____mutmut_69': xǁPopupǁ__init____mutmut_69, 
        'xǁPopupǁ__init____mutmut_70': xǁPopupǁ__init____mutmut_70, 
        'xǁPopupǁ__init____mutmut_71': xǁPopupǁ__init____mutmut_71, 
        'xǁPopupǁ__init____mutmut_72': xǁPopupǁ__init____mutmut_72, 
        'xǁPopupǁ__init____mutmut_73': xǁPopupǁ__init____mutmut_73, 
        'xǁPopupǁ__init____mutmut_74': xǁPopupǁ__init____mutmut_74
    }
    xǁPopupǁ__init____mutmut_orig.__name__ = 'xǁPopupǁ__init__'

    def on_slide_in_finished(self):
        """Handle slide in animation finished"""
        if self.userInput:
            return
        self.timeout_timer.start()

    def on_slide_out_finished(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁon_slide_out_finished__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁon_slide_out_finished__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁon_slide_out_finished__mutmut_orig(self):
        """Handle slide out animation finished"""
        self.hide()
        self.isShown = False
        self.timeout_timer.stop()
        self._add_popup()

    def xǁPopupǁon_slide_out_finished__mutmut_1(self):
        """Handle slide out animation finished"""
        self.hide()
        self.isShown = None
        self.timeout_timer.stop()
        self._add_popup()

    def xǁPopupǁon_slide_out_finished__mutmut_2(self):
        """Handle slide out animation finished"""
        self.hide()
        self.isShown = True
        self.timeout_timer.stop()
        self._add_popup()
    
    xǁPopupǁon_slide_out_finished__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁon_slide_out_finished__mutmut_1': xǁPopupǁon_slide_out_finished__mutmut_1, 
        'xǁPopupǁon_slide_out_finished__mutmut_2': xǁPopupǁon_slide_out_finished__mutmut_2
    }
    xǁPopupǁon_slide_out_finished__mutmut_orig.__name__ = 'xǁPopupǁon_slide_out_finished'

    def _calculate_target_geometry(self) -> QtCore.QRect:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁ_calculate_target_geometry__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁ_calculate_target_geometry__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁ_calculate_target_geometry__mutmut_orig(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_1(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = None
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_2(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_3(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None or app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_4(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is not None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_5(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = None
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_6(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    return

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_7(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = None

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_8(self) -> QtCore.QRect:
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
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_9(self) -> QtCore.QRect:
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
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_10(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() / 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_11(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 1.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_12(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = None

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_13(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            ) - 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_14(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                None,
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_15(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                None,
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_16(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_17(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_18(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 11
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_19(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = None
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_20(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() - (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_21(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) / 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_22(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() + width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_23(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 3
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_24(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = None

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_25(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() - 20

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_26(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 21

        return QtCore.QRect(x, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_27(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(None, y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_28(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, None, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_29(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, None, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_30(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, None)

    def xǁPopupǁ_calculate_target_geometry__mutmut_31(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(y, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_32(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, width, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_33(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, height)

    def xǁPopupǁ_calculate_target_geometry__mutmut_34(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = (
            max(
                self.text_label.height(),
                self.icon_label.height(),
            )
            + 10
        )

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, )
    
    xǁPopupǁ_calculate_target_geometry__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁ_calculate_target_geometry__mutmut_1': xǁPopupǁ_calculate_target_geometry__mutmut_1, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_2': xǁPopupǁ_calculate_target_geometry__mutmut_2, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_3': xǁPopupǁ_calculate_target_geometry__mutmut_3, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_4': xǁPopupǁ_calculate_target_geometry__mutmut_4, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_5': xǁPopupǁ_calculate_target_geometry__mutmut_5, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_6': xǁPopupǁ_calculate_target_geometry__mutmut_6, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_7': xǁPopupǁ_calculate_target_geometry__mutmut_7, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_8': xǁPopupǁ_calculate_target_geometry__mutmut_8, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_9': xǁPopupǁ_calculate_target_geometry__mutmut_9, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_10': xǁPopupǁ_calculate_target_geometry__mutmut_10, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_11': xǁPopupǁ_calculate_target_geometry__mutmut_11, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_12': xǁPopupǁ_calculate_target_geometry__mutmut_12, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_13': xǁPopupǁ_calculate_target_geometry__mutmut_13, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_14': xǁPopupǁ_calculate_target_geometry__mutmut_14, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_15': xǁPopupǁ_calculate_target_geometry__mutmut_15, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_16': xǁPopupǁ_calculate_target_geometry__mutmut_16, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_17': xǁPopupǁ_calculate_target_geometry__mutmut_17, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_18': xǁPopupǁ_calculate_target_geometry__mutmut_18, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_19': xǁPopupǁ_calculate_target_geometry__mutmut_19, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_20': xǁPopupǁ_calculate_target_geometry__mutmut_20, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_21': xǁPopupǁ_calculate_target_geometry__mutmut_21, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_22': xǁPopupǁ_calculate_target_geometry__mutmut_22, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_23': xǁPopupǁ_calculate_target_geometry__mutmut_23, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_24': xǁPopupǁ_calculate_target_geometry__mutmut_24, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_25': xǁPopupǁ_calculate_target_geometry__mutmut_25, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_26': xǁPopupǁ_calculate_target_geometry__mutmut_26, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_27': xǁPopupǁ_calculate_target_geometry__mutmut_27, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_28': xǁPopupǁ_calculate_target_geometry__mutmut_28, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_29': xǁPopupǁ_calculate_target_geometry__mutmut_29, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_30': xǁPopupǁ_calculate_target_geometry__mutmut_30, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_31': xǁPopupǁ_calculate_target_geometry__mutmut_31, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_32': xǁPopupǁ_calculate_target_geometry__mutmut_32, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_33': xǁPopupǁ_calculate_target_geometry__mutmut_33, 
        'xǁPopupǁ_calculate_target_geometry__mutmut_34': xǁPopupǁ_calculate_target_geometry__mutmut_34
    }
    xǁPopupǁ_calculate_target_geometry__mutmut_orig.__name__ = 'xǁPopupǁ_calculate_target_geometry'

    def updateMask(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁupdateMask__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁupdateMask__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁupdateMask__mutmut_orig(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_1(self) -> None:
        """Update widget mask properties"""
        path = None
        path.addRoundedRect(self.rect().toRectF(), 10, 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_2(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(None, 10, 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_3(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), None, 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_4(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, None)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_5(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(10, 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_6(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_7(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, )
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_8(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 11, 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_9(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 11)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_10(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 10)
        region = None
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_11(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 10)
        region = QtGui.QRegion(None)
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_12(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 10)
        region = QtGui.QRegion(path.toFillPolygon(None).toPolygon())
        self.setMask(region)

    def xǁPopupǁupdateMask__mutmut_13(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(None)
    
    xǁPopupǁupdateMask__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁupdateMask__mutmut_1': xǁPopupǁupdateMask__mutmut_1, 
        'xǁPopupǁupdateMask__mutmut_2': xǁPopupǁupdateMask__mutmut_2, 
        'xǁPopupǁupdateMask__mutmut_3': xǁPopupǁupdateMask__mutmut_3, 
        'xǁPopupǁupdateMask__mutmut_4': xǁPopupǁupdateMask__mutmut_4, 
        'xǁPopupǁupdateMask__mutmut_5': xǁPopupǁupdateMask__mutmut_5, 
        'xǁPopupǁupdateMask__mutmut_6': xǁPopupǁupdateMask__mutmut_6, 
        'xǁPopupǁupdateMask__mutmut_7': xǁPopupǁupdateMask__mutmut_7, 
        'xǁPopupǁupdateMask__mutmut_8': xǁPopupǁupdateMask__mutmut_8, 
        'xǁPopupǁupdateMask__mutmut_9': xǁPopupǁupdateMask__mutmut_9, 
        'xǁPopupǁupdateMask__mutmut_10': xǁPopupǁupdateMask__mutmut_10, 
        'xǁPopupǁupdateMask__mutmut_11': xǁPopupǁupdateMask__mutmut_11, 
        'xǁPopupǁupdateMask__mutmut_12': xǁPopupǁupdateMask__mutmut_12, 
        'xǁPopupǁupdateMask__mutmut_13': xǁPopupǁupdateMask__mutmut_13
    }
    xǁPopupǁupdateMask__mutmut_orig.__name__ = 'xǁPopupǁupdateMask'

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁmousePressEvent__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁmousePressEvent__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁmousePressEvent__mutmut_orig(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.userInput:
            return
        self.timeout_timer.stop()
        self.slide_out_animation.setStartValue(self.slide_in_animation.currentValue())
        self.slide_in_animation.stop()
        self.slide_out_animation.start()

    def xǁPopupǁmousePressEvent__mutmut_1(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.userInput:
            return
        self.timeout_timer.stop()
        self.slide_out_animation.setStartValue(None)
        self.slide_in_animation.stop()
        self.slide_out_animation.start()
    
    xǁPopupǁmousePressEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁmousePressEvent__mutmut_1': xǁPopupǁmousePressEvent__mutmut_1
    }
    xǁPopupǁmousePressEvent__mutmut_orig.__name__ = 'xǁPopupǁmousePressEvent'

    def new_message(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        args = [message_type, message, timeout, userInput]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁnew_message__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁnew_message__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁnew_message__mutmut_orig(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_1(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "XXXX",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_2(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6001,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_3(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = True,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_4(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) != 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_5(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 5:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_6(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            None
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_7(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "XXmessageXX": message,
                "type": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_8(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "MESSAGE": message,
                "type": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_9(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "XXtypeXX": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_10(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "TYPE": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_11(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "XXtimeoutXX": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_12(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "TIMEOUT": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_13(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "XXuserInputXX": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_14(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "userinput": userInput,
            }
        )
        return self._add_popup()

    def xǁPopupǁnew_message__mutmut_15(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "USERINPUT": userInput,
            }
        )
        return self._add_popup()
    
    xǁPopupǁnew_message__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁnew_message__mutmut_1': xǁPopupǁnew_message__mutmut_1, 
        'xǁPopupǁnew_message__mutmut_2': xǁPopupǁnew_message__mutmut_2, 
        'xǁPopupǁnew_message__mutmut_3': xǁPopupǁnew_message__mutmut_3, 
        'xǁPopupǁnew_message__mutmut_4': xǁPopupǁnew_message__mutmut_4, 
        'xǁPopupǁnew_message__mutmut_5': xǁPopupǁnew_message__mutmut_5, 
        'xǁPopupǁnew_message__mutmut_6': xǁPopupǁnew_message__mutmut_6, 
        'xǁPopupǁnew_message__mutmut_7': xǁPopupǁnew_message__mutmut_7, 
        'xǁPopupǁnew_message__mutmut_8': xǁPopupǁnew_message__mutmut_8, 
        'xǁPopupǁnew_message__mutmut_9': xǁPopupǁnew_message__mutmut_9, 
        'xǁPopupǁnew_message__mutmut_10': xǁPopupǁnew_message__mutmut_10, 
        'xǁPopupǁnew_message__mutmut_11': xǁPopupǁnew_message__mutmut_11, 
        'xǁPopupǁnew_message__mutmut_12': xǁPopupǁnew_message__mutmut_12, 
        'xǁPopupǁnew_message__mutmut_13': xǁPopupǁnew_message__mutmut_13, 
        'xǁPopupǁnew_message__mutmut_14': xǁPopupǁnew_message__mutmut_14, 
        'xǁPopupǁnew_message__mutmut_15': xǁPopupǁnew_message__mutmut_15
    }
    xǁPopupǁnew_message__mutmut_orig.__name__ = 'xǁPopupǁnew_message'

    def _add_popup(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁ_add_popup__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁ_add_popup__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁ_add_popup__mutmut_orig(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_1(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped or self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_2(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages or self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_3(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state() != QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_4(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state() != QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_5(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = None
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_6(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = None
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_7(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get(None)
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_8(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("XXtypeXX")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_9(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("TYPE")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_10(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = None
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_11(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get(None)
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_12(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("XXmessageXX")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_13(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("MESSAGE")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_14(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = None
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_15(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get(None)
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_16(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("XXtimeoutXX")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_17(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("TIMEOUT")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_18(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(None)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_19(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message != self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_20(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = None
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_21(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    None
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_22(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get(None) != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_23(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("XXmessageXX") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_24(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("MESSAGE") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_25(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") == message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_26(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = None
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_27(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get(None)
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_28(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("XXuserInputXX")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_29(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userinput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_30(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("USERINPUT")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_31(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(None)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_32(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(61)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_33(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(None)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_34(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(501)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_35(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_36(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_37(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_38(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(None)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_39(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(None)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_40(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(None)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_41(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = None
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_42(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = None

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_43(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(None, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_44(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, None)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_45(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(-end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_46(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, )

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_47(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(1, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_48(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() / 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_49(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, +end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_50(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 3)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_51(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(None)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_52(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(None)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_53(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(None)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_54(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(None)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_55(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                None
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_56(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(None)
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_57(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap("XX:/arrow_icons/media/btn_icons/right_arrow.svgXX")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_58(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/ARROW_ICONS/MEDIA/BTN_ICONS/RIGHT_ARROW.SVG")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_59(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(None)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_60(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(None)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_61(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                None
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_62(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(None)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_63(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() / 1.2)
            )
            self.show()

    def xǁPopupǁ_add_popup__mutmut_64(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")
            self.text_label.setFixedHeight(60)
            self.text_label.setFixedWidth(500)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.actionbtn.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.text_label.setFixedHeight(
                int(self.text_label.sizeHint().height() * 2.2)
            )
            self.show()
    
    xǁPopupǁ_add_popup__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁ_add_popup__mutmut_1': xǁPopupǁ_add_popup__mutmut_1, 
        'xǁPopupǁ_add_popup__mutmut_2': xǁPopupǁ_add_popup__mutmut_2, 
        'xǁPopupǁ_add_popup__mutmut_3': xǁPopupǁ_add_popup__mutmut_3, 
        'xǁPopupǁ_add_popup__mutmut_4': xǁPopupǁ_add_popup__mutmut_4, 
        'xǁPopupǁ_add_popup__mutmut_5': xǁPopupǁ_add_popup__mutmut_5, 
        'xǁPopupǁ_add_popup__mutmut_6': xǁPopupǁ_add_popup__mutmut_6, 
        'xǁPopupǁ_add_popup__mutmut_7': xǁPopupǁ_add_popup__mutmut_7, 
        'xǁPopupǁ_add_popup__mutmut_8': xǁPopupǁ_add_popup__mutmut_8, 
        'xǁPopupǁ_add_popup__mutmut_9': xǁPopupǁ_add_popup__mutmut_9, 
        'xǁPopupǁ_add_popup__mutmut_10': xǁPopupǁ_add_popup__mutmut_10, 
        'xǁPopupǁ_add_popup__mutmut_11': xǁPopupǁ_add_popup__mutmut_11, 
        'xǁPopupǁ_add_popup__mutmut_12': xǁPopupǁ_add_popup__mutmut_12, 
        'xǁPopupǁ_add_popup__mutmut_13': xǁPopupǁ_add_popup__mutmut_13, 
        'xǁPopupǁ_add_popup__mutmut_14': xǁPopupǁ_add_popup__mutmut_14, 
        'xǁPopupǁ_add_popup__mutmut_15': xǁPopupǁ_add_popup__mutmut_15, 
        'xǁPopupǁ_add_popup__mutmut_16': xǁPopupǁ_add_popup__mutmut_16, 
        'xǁPopupǁ_add_popup__mutmut_17': xǁPopupǁ_add_popup__mutmut_17, 
        'xǁPopupǁ_add_popup__mutmut_18': xǁPopupǁ_add_popup__mutmut_18, 
        'xǁPopupǁ_add_popup__mutmut_19': xǁPopupǁ_add_popup__mutmut_19, 
        'xǁPopupǁ_add_popup__mutmut_20': xǁPopupǁ_add_popup__mutmut_20, 
        'xǁPopupǁ_add_popup__mutmut_21': xǁPopupǁ_add_popup__mutmut_21, 
        'xǁPopupǁ_add_popup__mutmut_22': xǁPopupǁ_add_popup__mutmut_22, 
        'xǁPopupǁ_add_popup__mutmut_23': xǁPopupǁ_add_popup__mutmut_23, 
        'xǁPopupǁ_add_popup__mutmut_24': xǁPopupǁ_add_popup__mutmut_24, 
        'xǁPopupǁ_add_popup__mutmut_25': xǁPopupǁ_add_popup__mutmut_25, 
        'xǁPopupǁ_add_popup__mutmut_26': xǁPopupǁ_add_popup__mutmut_26, 
        'xǁPopupǁ_add_popup__mutmut_27': xǁPopupǁ_add_popup__mutmut_27, 
        'xǁPopupǁ_add_popup__mutmut_28': xǁPopupǁ_add_popup__mutmut_28, 
        'xǁPopupǁ_add_popup__mutmut_29': xǁPopupǁ_add_popup__mutmut_29, 
        'xǁPopupǁ_add_popup__mutmut_30': xǁPopupǁ_add_popup__mutmut_30, 
        'xǁPopupǁ_add_popup__mutmut_31': xǁPopupǁ_add_popup__mutmut_31, 
        'xǁPopupǁ_add_popup__mutmut_32': xǁPopupǁ_add_popup__mutmut_32, 
        'xǁPopupǁ_add_popup__mutmut_33': xǁPopupǁ_add_popup__mutmut_33, 
        'xǁPopupǁ_add_popup__mutmut_34': xǁPopupǁ_add_popup__mutmut_34, 
        'xǁPopupǁ_add_popup__mutmut_35': xǁPopupǁ_add_popup__mutmut_35, 
        'xǁPopupǁ_add_popup__mutmut_36': xǁPopupǁ_add_popup__mutmut_36, 
        'xǁPopupǁ_add_popup__mutmut_37': xǁPopupǁ_add_popup__mutmut_37, 
        'xǁPopupǁ_add_popup__mutmut_38': xǁPopupǁ_add_popup__mutmut_38, 
        'xǁPopupǁ_add_popup__mutmut_39': xǁPopupǁ_add_popup__mutmut_39, 
        'xǁPopupǁ_add_popup__mutmut_40': xǁPopupǁ_add_popup__mutmut_40, 
        'xǁPopupǁ_add_popup__mutmut_41': xǁPopupǁ_add_popup__mutmut_41, 
        'xǁPopupǁ_add_popup__mutmut_42': xǁPopupǁ_add_popup__mutmut_42, 
        'xǁPopupǁ_add_popup__mutmut_43': xǁPopupǁ_add_popup__mutmut_43, 
        'xǁPopupǁ_add_popup__mutmut_44': xǁPopupǁ_add_popup__mutmut_44, 
        'xǁPopupǁ_add_popup__mutmut_45': xǁPopupǁ_add_popup__mutmut_45, 
        'xǁPopupǁ_add_popup__mutmut_46': xǁPopupǁ_add_popup__mutmut_46, 
        'xǁPopupǁ_add_popup__mutmut_47': xǁPopupǁ_add_popup__mutmut_47, 
        'xǁPopupǁ_add_popup__mutmut_48': xǁPopupǁ_add_popup__mutmut_48, 
        'xǁPopupǁ_add_popup__mutmut_49': xǁPopupǁ_add_popup__mutmut_49, 
        'xǁPopupǁ_add_popup__mutmut_50': xǁPopupǁ_add_popup__mutmut_50, 
        'xǁPopupǁ_add_popup__mutmut_51': xǁPopupǁ_add_popup__mutmut_51, 
        'xǁPopupǁ_add_popup__mutmut_52': xǁPopupǁ_add_popup__mutmut_52, 
        'xǁPopupǁ_add_popup__mutmut_53': xǁPopupǁ_add_popup__mutmut_53, 
        'xǁPopupǁ_add_popup__mutmut_54': xǁPopupǁ_add_popup__mutmut_54, 
        'xǁPopupǁ_add_popup__mutmut_55': xǁPopupǁ_add_popup__mutmut_55, 
        'xǁPopupǁ_add_popup__mutmut_56': xǁPopupǁ_add_popup__mutmut_56, 
        'xǁPopupǁ_add_popup__mutmut_57': xǁPopupǁ_add_popup__mutmut_57, 
        'xǁPopupǁ_add_popup__mutmut_58': xǁPopupǁ_add_popup__mutmut_58, 
        'xǁPopupǁ_add_popup__mutmut_59': xǁPopupǁ_add_popup__mutmut_59, 
        'xǁPopupǁ_add_popup__mutmut_60': xǁPopupǁ_add_popup__mutmut_60, 
        'xǁPopupǁ_add_popup__mutmut_61': xǁPopupǁ_add_popup__mutmut_61, 
        'xǁPopupǁ_add_popup__mutmut_62': xǁPopupǁ_add_popup__mutmut_62, 
        'xǁPopupǁ_add_popup__mutmut_63': xǁPopupǁ_add_popup__mutmut_63, 
        'xǁPopupǁ_add_popup__mutmut_64': xǁPopupǁ_add_popup__mutmut_64
    }
    xǁPopupǁ_add_popup__mutmut_orig.__name__ = 'xǁPopupǁ_add_popup'

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁshowEvent__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁshowEvent__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁshowEvent__mutmut_orig(self, a0: QtGui.QShowEvent) -> None:
        """Re-implementation, widget show"""
        self.slide_in_animation.start()
        self.isShown = True
        super().showEvent(a0)

    def xǁPopupǁshowEvent__mutmut_1(self, a0: QtGui.QShowEvent) -> None:
        """Re-implementation, widget show"""
        self.slide_in_animation.start()
        self.isShown = None
        super().showEvent(a0)

    def xǁPopupǁshowEvent__mutmut_2(self, a0: QtGui.QShowEvent) -> None:
        """Re-implementation, widget show"""
        self.slide_in_animation.start()
        self.isShown = False
        super().showEvent(a0)

    def xǁPopupǁshowEvent__mutmut_3(self, a0: QtGui.QShowEvent) -> None:
        """Re-implementation, widget show"""
        self.slide_in_animation.start()
        self.isShown = True
        super().showEvent(None)
    
    xǁPopupǁshowEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁshowEvent__mutmut_1': xǁPopupǁshowEvent__mutmut_1, 
        'xǁPopupǁshowEvent__mutmut_2': xǁPopupǁshowEvent__mutmut_2, 
        'xǁPopupǁshowEvent__mutmut_3': xǁPopupǁshowEvent__mutmut_3
    }
    xǁPopupǁshowEvent__mutmut_orig.__name__ = 'xǁPopupǁshowEvent'

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁresizeEvent__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁresizeEvent__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁresizeEvent__mutmut_orig(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implementation, handle resize event"""
        self.updateMask()
        super().resizeEvent(a0)

    def xǁPopupǁresizeEvent__mutmut_1(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implementation, handle resize event"""
        self.updateMask()
        super().resizeEvent(None)
    
    xǁPopupǁresizeEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁresizeEvent__mutmut_1': xǁPopupǁresizeEvent__mutmut_1
    }
    xǁPopupǁresizeEvent__mutmut_orig.__name__ = 'xǁPopupǁresizeEvent'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁpaintEvent__mutmut_orig(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_1(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = None
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_2(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(None)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_3(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_4(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, None)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_5(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_6(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, )

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_7(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, False)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_8(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = None
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_9(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type != Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_10(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = None
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_11(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type != Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_12(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = None
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_13(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type != Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_14(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = None

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_15(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = None
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_16(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(None)
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_17(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = None

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_18(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(None, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_19(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, None)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_20(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_21(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, )

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_22(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() * 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_23(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 3.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_24(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(None, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_25(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, None)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_26(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(_base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_27(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, )
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_28(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(1, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_29(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(None, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_30(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, None)

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_31(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(_base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_32(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, )

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_33(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(2.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_34(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(None))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_35(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(161))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_36(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(None)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_37(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(None)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def xǁPopupǁpaintEvent__mutmut_38(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(None, 10, 10)

    def xǁPopupǁpaintEvent__mutmut_39(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), None, 10)

    def xǁPopupǁpaintEvent__mutmut_40(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, None)

    def xǁPopupǁpaintEvent__mutmut_41(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(10, 10)

    def xǁPopupǁpaintEvent__mutmut_42(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10)

    def xǁPopupǁpaintEvent__mutmut_43(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, )

    def xǁPopupǁpaintEvent__mutmut_44(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 11, 10)

    def xǁPopupǁpaintEvent__mutmut_45(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 11)
    
    xǁPopupǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁpaintEvent__mutmut_1': xǁPopupǁpaintEvent__mutmut_1, 
        'xǁPopupǁpaintEvent__mutmut_2': xǁPopupǁpaintEvent__mutmut_2, 
        'xǁPopupǁpaintEvent__mutmut_3': xǁPopupǁpaintEvent__mutmut_3, 
        'xǁPopupǁpaintEvent__mutmut_4': xǁPopupǁpaintEvent__mutmut_4, 
        'xǁPopupǁpaintEvent__mutmut_5': xǁPopupǁpaintEvent__mutmut_5, 
        'xǁPopupǁpaintEvent__mutmut_6': xǁPopupǁpaintEvent__mutmut_6, 
        'xǁPopupǁpaintEvent__mutmut_7': xǁPopupǁpaintEvent__mutmut_7, 
        'xǁPopupǁpaintEvent__mutmut_8': xǁPopupǁpaintEvent__mutmut_8, 
        'xǁPopupǁpaintEvent__mutmut_9': xǁPopupǁpaintEvent__mutmut_9, 
        'xǁPopupǁpaintEvent__mutmut_10': xǁPopupǁpaintEvent__mutmut_10, 
        'xǁPopupǁpaintEvent__mutmut_11': xǁPopupǁpaintEvent__mutmut_11, 
        'xǁPopupǁpaintEvent__mutmut_12': xǁPopupǁpaintEvent__mutmut_12, 
        'xǁPopupǁpaintEvent__mutmut_13': xǁPopupǁpaintEvent__mutmut_13, 
        'xǁPopupǁpaintEvent__mutmut_14': xǁPopupǁpaintEvent__mutmut_14, 
        'xǁPopupǁpaintEvent__mutmut_15': xǁPopupǁpaintEvent__mutmut_15, 
        'xǁPopupǁpaintEvent__mutmut_16': xǁPopupǁpaintEvent__mutmut_16, 
        'xǁPopupǁpaintEvent__mutmut_17': xǁPopupǁpaintEvent__mutmut_17, 
        'xǁPopupǁpaintEvent__mutmut_18': xǁPopupǁpaintEvent__mutmut_18, 
        'xǁPopupǁpaintEvent__mutmut_19': xǁPopupǁpaintEvent__mutmut_19, 
        'xǁPopupǁpaintEvent__mutmut_20': xǁPopupǁpaintEvent__mutmut_20, 
        'xǁPopupǁpaintEvent__mutmut_21': xǁPopupǁpaintEvent__mutmut_21, 
        'xǁPopupǁpaintEvent__mutmut_22': xǁPopupǁpaintEvent__mutmut_22, 
        'xǁPopupǁpaintEvent__mutmut_23': xǁPopupǁpaintEvent__mutmut_23, 
        'xǁPopupǁpaintEvent__mutmut_24': xǁPopupǁpaintEvent__mutmut_24, 
        'xǁPopupǁpaintEvent__mutmut_25': xǁPopupǁpaintEvent__mutmut_25, 
        'xǁPopupǁpaintEvent__mutmut_26': xǁPopupǁpaintEvent__mutmut_26, 
        'xǁPopupǁpaintEvent__mutmut_27': xǁPopupǁpaintEvent__mutmut_27, 
        'xǁPopupǁpaintEvent__mutmut_28': xǁPopupǁpaintEvent__mutmut_28, 
        'xǁPopupǁpaintEvent__mutmut_29': xǁPopupǁpaintEvent__mutmut_29, 
        'xǁPopupǁpaintEvent__mutmut_30': xǁPopupǁpaintEvent__mutmut_30, 
        'xǁPopupǁpaintEvent__mutmut_31': xǁPopupǁpaintEvent__mutmut_31, 
        'xǁPopupǁpaintEvent__mutmut_32': xǁPopupǁpaintEvent__mutmut_32, 
        'xǁPopupǁpaintEvent__mutmut_33': xǁPopupǁpaintEvent__mutmut_33, 
        'xǁPopupǁpaintEvent__mutmut_34': xǁPopupǁpaintEvent__mutmut_34, 
        'xǁPopupǁpaintEvent__mutmut_35': xǁPopupǁpaintEvent__mutmut_35, 
        'xǁPopupǁpaintEvent__mutmut_36': xǁPopupǁpaintEvent__mutmut_36, 
        'xǁPopupǁpaintEvent__mutmut_37': xǁPopupǁpaintEvent__mutmut_37, 
        'xǁPopupǁpaintEvent__mutmut_38': xǁPopupǁpaintEvent__mutmut_38, 
        'xǁPopupǁpaintEvent__mutmut_39': xǁPopupǁpaintEvent__mutmut_39, 
        'xǁPopupǁpaintEvent__mutmut_40': xǁPopupǁpaintEvent__mutmut_40, 
        'xǁPopupǁpaintEvent__mutmut_41': xǁPopupǁpaintEvent__mutmut_41, 
        'xǁPopupǁpaintEvent__mutmut_42': xǁPopupǁpaintEvent__mutmut_42, 
        'xǁPopupǁpaintEvent__mutmut_43': xǁPopupǁpaintEvent__mutmut_43, 
        'xǁPopupǁpaintEvent__mutmut_44': xǁPopupǁpaintEvent__mutmut_44, 
        'xǁPopupǁpaintEvent__mutmut_45': xǁPopupǁpaintEvent__mutmut_45
    }
    xǁPopupǁpaintEvent__mutmut_orig.__name__ = 'xǁPopupǁpaintEvent'

    def _setupUI(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPopupǁ_setupUI__mutmut_orig'), object.__getattribute__(self, 'xǁPopupǁ_setupUI__mutmut_mutants'), args, kwargs, self)

    def xǁPopupǁ_setupUI__mutmut_orig(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_1(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_2(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_3(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_4(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_5(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_6(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_7(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_8(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_9(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_10(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_11(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_12(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_13(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_14(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_15(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_16(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_17(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_18(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_19(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_20(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_21(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_22(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_23(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_24(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_25(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_26(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_27(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_28(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_29(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_30(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_31(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_32(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_33(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_34(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_35(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_36(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_37(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_38(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_39(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_40(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_41(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_42(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_43(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_44(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_45(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_46(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_47(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_48(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_49(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_50(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_51(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_52(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_53(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_54(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_55(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_56(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_57(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_58(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_59(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_60(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_61(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_62(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_63(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_64(self) -> None:
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

    def xǁPopupǁ_setupUI__mutmut_65(self) -> None:
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
    
    xǁPopupǁ_setupUI__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPopupǁ_setupUI__mutmut_1': xǁPopupǁ_setupUI__mutmut_1, 
        'xǁPopupǁ_setupUI__mutmut_2': xǁPopupǁ_setupUI__mutmut_2, 
        'xǁPopupǁ_setupUI__mutmut_3': xǁPopupǁ_setupUI__mutmut_3, 
        'xǁPopupǁ_setupUI__mutmut_4': xǁPopupǁ_setupUI__mutmut_4, 
        'xǁPopupǁ_setupUI__mutmut_5': xǁPopupǁ_setupUI__mutmut_5, 
        'xǁPopupǁ_setupUI__mutmut_6': xǁPopupǁ_setupUI__mutmut_6, 
        'xǁPopupǁ_setupUI__mutmut_7': xǁPopupǁ_setupUI__mutmut_7, 
        'xǁPopupǁ_setupUI__mutmut_8': xǁPopupǁ_setupUI__mutmut_8, 
        'xǁPopupǁ_setupUI__mutmut_9': xǁPopupǁ_setupUI__mutmut_9, 
        'xǁPopupǁ_setupUI__mutmut_10': xǁPopupǁ_setupUI__mutmut_10, 
        'xǁPopupǁ_setupUI__mutmut_11': xǁPopupǁ_setupUI__mutmut_11, 
        'xǁPopupǁ_setupUI__mutmut_12': xǁPopupǁ_setupUI__mutmut_12, 
        'xǁPopupǁ_setupUI__mutmut_13': xǁPopupǁ_setupUI__mutmut_13, 
        'xǁPopupǁ_setupUI__mutmut_14': xǁPopupǁ_setupUI__mutmut_14, 
        'xǁPopupǁ_setupUI__mutmut_15': xǁPopupǁ_setupUI__mutmut_15, 
        'xǁPopupǁ_setupUI__mutmut_16': xǁPopupǁ_setupUI__mutmut_16, 
        'xǁPopupǁ_setupUI__mutmut_17': xǁPopupǁ_setupUI__mutmut_17, 
        'xǁPopupǁ_setupUI__mutmut_18': xǁPopupǁ_setupUI__mutmut_18, 
        'xǁPopupǁ_setupUI__mutmut_19': xǁPopupǁ_setupUI__mutmut_19, 
        'xǁPopupǁ_setupUI__mutmut_20': xǁPopupǁ_setupUI__mutmut_20, 
        'xǁPopupǁ_setupUI__mutmut_21': xǁPopupǁ_setupUI__mutmut_21, 
        'xǁPopupǁ_setupUI__mutmut_22': xǁPopupǁ_setupUI__mutmut_22, 
        'xǁPopupǁ_setupUI__mutmut_23': xǁPopupǁ_setupUI__mutmut_23, 
        'xǁPopupǁ_setupUI__mutmut_24': xǁPopupǁ_setupUI__mutmut_24, 
        'xǁPopupǁ_setupUI__mutmut_25': xǁPopupǁ_setupUI__mutmut_25, 
        'xǁPopupǁ_setupUI__mutmut_26': xǁPopupǁ_setupUI__mutmut_26, 
        'xǁPopupǁ_setupUI__mutmut_27': xǁPopupǁ_setupUI__mutmut_27, 
        'xǁPopupǁ_setupUI__mutmut_28': xǁPopupǁ_setupUI__mutmut_28, 
        'xǁPopupǁ_setupUI__mutmut_29': xǁPopupǁ_setupUI__mutmut_29, 
        'xǁPopupǁ_setupUI__mutmut_30': xǁPopupǁ_setupUI__mutmut_30, 
        'xǁPopupǁ_setupUI__mutmut_31': xǁPopupǁ_setupUI__mutmut_31, 
        'xǁPopupǁ_setupUI__mutmut_32': xǁPopupǁ_setupUI__mutmut_32, 
        'xǁPopupǁ_setupUI__mutmut_33': xǁPopupǁ_setupUI__mutmut_33, 
        'xǁPopupǁ_setupUI__mutmut_34': xǁPopupǁ_setupUI__mutmut_34, 
        'xǁPopupǁ_setupUI__mutmut_35': xǁPopupǁ_setupUI__mutmut_35, 
        'xǁPopupǁ_setupUI__mutmut_36': xǁPopupǁ_setupUI__mutmut_36, 
        'xǁPopupǁ_setupUI__mutmut_37': xǁPopupǁ_setupUI__mutmut_37, 
        'xǁPopupǁ_setupUI__mutmut_38': xǁPopupǁ_setupUI__mutmut_38, 
        'xǁPopupǁ_setupUI__mutmut_39': xǁPopupǁ_setupUI__mutmut_39, 
        'xǁPopupǁ_setupUI__mutmut_40': xǁPopupǁ_setupUI__mutmut_40, 
        'xǁPopupǁ_setupUI__mutmut_41': xǁPopupǁ_setupUI__mutmut_41, 
        'xǁPopupǁ_setupUI__mutmut_42': xǁPopupǁ_setupUI__mutmut_42, 
        'xǁPopupǁ_setupUI__mutmut_43': xǁPopupǁ_setupUI__mutmut_43, 
        'xǁPopupǁ_setupUI__mutmut_44': xǁPopupǁ_setupUI__mutmut_44, 
        'xǁPopupǁ_setupUI__mutmut_45': xǁPopupǁ_setupUI__mutmut_45, 
        'xǁPopupǁ_setupUI__mutmut_46': xǁPopupǁ_setupUI__mutmut_46, 
        'xǁPopupǁ_setupUI__mutmut_47': xǁPopupǁ_setupUI__mutmut_47, 
        'xǁPopupǁ_setupUI__mutmut_48': xǁPopupǁ_setupUI__mutmut_48, 
        'xǁPopupǁ_setupUI__mutmut_49': xǁPopupǁ_setupUI__mutmut_49, 
        'xǁPopupǁ_setupUI__mutmut_50': xǁPopupǁ_setupUI__mutmut_50, 
        'xǁPopupǁ_setupUI__mutmut_51': xǁPopupǁ_setupUI__mutmut_51, 
        'xǁPopupǁ_setupUI__mutmut_52': xǁPopupǁ_setupUI__mutmut_52, 
        'xǁPopupǁ_setupUI__mutmut_53': xǁPopupǁ_setupUI__mutmut_53, 
        'xǁPopupǁ_setupUI__mutmut_54': xǁPopupǁ_setupUI__mutmut_54, 
        'xǁPopupǁ_setupUI__mutmut_55': xǁPopupǁ_setupUI__mutmut_55, 
        'xǁPopupǁ_setupUI__mutmut_56': xǁPopupǁ_setupUI__mutmut_56, 
        'xǁPopupǁ_setupUI__mutmut_57': xǁPopupǁ_setupUI__mutmut_57, 
        'xǁPopupǁ_setupUI__mutmut_58': xǁPopupǁ_setupUI__mutmut_58, 
        'xǁPopupǁ_setupUI__mutmut_59': xǁPopupǁ_setupUI__mutmut_59, 
        'xǁPopupǁ_setupUI__mutmut_60': xǁPopupǁ_setupUI__mutmut_60, 
        'xǁPopupǁ_setupUI__mutmut_61': xǁPopupǁ_setupUI__mutmut_61, 
        'xǁPopupǁ_setupUI__mutmut_62': xǁPopupǁ_setupUI__mutmut_62, 
        'xǁPopupǁ_setupUI__mutmut_63': xǁPopupǁ_setupUI__mutmut_63, 
        'xǁPopupǁ_setupUI__mutmut_64': xǁPopupǁ_setupUI__mutmut_64, 
        'xǁPopupǁ_setupUI__mutmut_65': xǁPopupǁ_setupUI__mutmut_65
    }
    xǁPopupǁ_setupUI__mutmut_orig.__name__ = 'xǁPopupǁ_setupUI'
