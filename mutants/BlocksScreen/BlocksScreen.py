import logging
import sys
import typing

from logger import CrashHandler, LogManager, install_crash_handler, setup_logging

install_crash_handler()

from lib.panels.mainWindow import MainWindow  # noqa: E402
from PyQt6 import QtCore, QtGui, QtWidgets  # noqa: E402
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


class BlocksScreenApp(QtWidgets.QApplication):
    """QApplication subclass that routes unhandled slot exceptions to CrashHandler."""

    def notify(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:
        args = [a0, a1]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenAppǁnotify__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenAppǁnotify__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenAppǁnotify__mutmut_orig(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_1(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(None, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_2(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, None)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_3(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_4(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, )
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_5(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = None
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_6(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = None
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_7(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None or exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_8(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None or exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_9(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_10(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_11(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_12(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(None, exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_13(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, None, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_14(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, None)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_15(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_value, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_16(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_tb)
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_17(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, )
            return False

    def xǁBlocksScreenAppǁnotify__mutmut_18(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return True
    
    xǁBlocksScreenAppǁnotify__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenAppǁnotify__mutmut_1': xǁBlocksScreenAppǁnotify__mutmut_1, 
        'xǁBlocksScreenAppǁnotify__mutmut_2': xǁBlocksScreenAppǁnotify__mutmut_2, 
        'xǁBlocksScreenAppǁnotify__mutmut_3': xǁBlocksScreenAppǁnotify__mutmut_3, 
        'xǁBlocksScreenAppǁnotify__mutmut_4': xǁBlocksScreenAppǁnotify__mutmut_4, 
        'xǁBlocksScreenAppǁnotify__mutmut_5': xǁBlocksScreenAppǁnotify__mutmut_5, 
        'xǁBlocksScreenAppǁnotify__mutmut_6': xǁBlocksScreenAppǁnotify__mutmut_6, 
        'xǁBlocksScreenAppǁnotify__mutmut_7': xǁBlocksScreenAppǁnotify__mutmut_7, 
        'xǁBlocksScreenAppǁnotify__mutmut_8': xǁBlocksScreenAppǁnotify__mutmut_8, 
        'xǁBlocksScreenAppǁnotify__mutmut_9': xǁBlocksScreenAppǁnotify__mutmut_9, 
        'xǁBlocksScreenAppǁnotify__mutmut_10': xǁBlocksScreenAppǁnotify__mutmut_10, 
        'xǁBlocksScreenAppǁnotify__mutmut_11': xǁBlocksScreenAppǁnotify__mutmut_11, 
        'xǁBlocksScreenAppǁnotify__mutmut_12': xǁBlocksScreenAppǁnotify__mutmut_12, 
        'xǁBlocksScreenAppǁnotify__mutmut_13': xǁBlocksScreenAppǁnotify__mutmut_13, 
        'xǁBlocksScreenAppǁnotify__mutmut_14': xǁBlocksScreenAppǁnotify__mutmut_14, 
        'xǁBlocksScreenAppǁnotify__mutmut_15': xǁBlocksScreenAppǁnotify__mutmut_15, 
        'xǁBlocksScreenAppǁnotify__mutmut_16': xǁBlocksScreenAppǁnotify__mutmut_16, 
        'xǁBlocksScreenAppǁnotify__mutmut_17': xǁBlocksScreenAppǁnotify__mutmut_17, 
        'xǁBlocksScreenAppǁnotify__mutmut_18': xǁBlocksScreenAppǁnotify__mutmut_18
    }
    xǁBlocksScreenAppǁnotify__mutmut_orig.__name__ = 'xǁBlocksScreenAppǁnotify'


QtGui.QGuiApplication.setAttribute(
    QtCore.Qt.ApplicationAttribute.AA_SynthesizeMouseForUnhandledTouchEvents,
    True,
)
QtGui.QGuiApplication.setAttribute(
    QtCore.Qt.ApplicationAttribute.AA_SynthesizeTouchForUnhandledMouseEvents,
    True,
)

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def show_splash(window: typing.Optional[QtWidgets.QWidget] = None):
    args = [window]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_show_splash__mutmut_orig, x_show_splash__mutmut_mutants, args, kwargs, None)


def x_show_splash__mutmut_orig(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_1(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = None
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_2(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap(None)
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_3(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("XXBlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.pngXX")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_4(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("blocksscreen/blocksscreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_5(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BLOCKSSCREEN/BLOCKSSCREEN/LIB/UI/RESOURCES/LOGOBLOCKS.PNG")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_6(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = None
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_7(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=None)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_8(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(None)
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_9(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(None, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_10(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, None, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_11(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, None, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_12(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, None))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_13(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_14(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_15(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_16(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, ))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_17(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(1, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_18(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 1, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_19(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 401, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_20(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 201))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_21(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None or isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_22(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def x_show_splash__mutmut_23(window: typing.Optional[QtWidgets.QWidget] = None):
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(None)

x_show_splash__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_show_splash__mutmut_1': x_show_splash__mutmut_1, 
    'x_show_splash__mutmut_2': x_show_splash__mutmut_2, 
    'x_show_splash__mutmut_3': x_show_splash__mutmut_3, 
    'x_show_splash__mutmut_4': x_show_splash__mutmut_4, 
    'x_show_splash__mutmut_5': x_show_splash__mutmut_5, 
    'x_show_splash__mutmut_6': x_show_splash__mutmut_6, 
    'x_show_splash__mutmut_7': x_show_splash__mutmut_7, 
    'x_show_splash__mutmut_8': x_show_splash__mutmut_8, 
    'x_show_splash__mutmut_9': x_show_splash__mutmut_9, 
    'x_show_splash__mutmut_10': x_show_splash__mutmut_10, 
    'x_show_splash__mutmut_11': x_show_splash__mutmut_11, 
    'x_show_splash__mutmut_12': x_show_splash__mutmut_12, 
    'x_show_splash__mutmut_13': x_show_splash__mutmut_13, 
    'x_show_splash__mutmut_14': x_show_splash__mutmut_14, 
    'x_show_splash__mutmut_15': x_show_splash__mutmut_15, 
    'x_show_splash__mutmut_16': x_show_splash__mutmut_16, 
    'x_show_splash__mutmut_17': x_show_splash__mutmut_17, 
    'x_show_splash__mutmut_18': x_show_splash__mutmut_18, 
    'x_show_splash__mutmut_19': x_show_splash__mutmut_19, 
    'x_show_splash__mutmut_20': x_show_splash__mutmut_20, 
    'x_show_splash__mutmut_21': x_show_splash__mutmut_21, 
    'x_show_splash__mutmut_22': x_show_splash__mutmut_22, 
    'x_show_splash__mutmut_23': x_show_splash__mutmut_23
}
x_show_splash__mutmut_orig.__name__ = 'x_show_splash'


def on_quit() -> None:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_on_quit__mutmut_orig, x_on_quit__mutmut_mutants, args, kwargs, None)


def x_on_quit__mutmut_orig() -> None:
    logging.info("Final exit cleanup")
    LogManager.shutdown()


def x_on_quit__mutmut_1() -> None:
    logging.info(None)
    LogManager.shutdown()


def x_on_quit__mutmut_2() -> None:
    logging.info("XXFinal exit cleanupXX")
    LogManager.shutdown()


def x_on_quit__mutmut_3() -> None:
    logging.info("final exit cleanup")
    LogManager.shutdown()


def x_on_quit__mutmut_4() -> None:
    logging.info("FINAL EXIT CLEANUP")
    LogManager.shutdown()

x_on_quit__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_on_quit__mutmut_1': x_on_quit__mutmut_1, 
    'x_on_quit__mutmut_2': x_on_quit__mutmut_2, 
    'x_on_quit__mutmut_3': x_on_quit__mutmut_3, 
    'x_on_quit__mutmut_4': x_on_quit__mutmut_4
}
x_on_quit__mutmut_orig.__name__ = 'x_on_quit'


if __name__ == "__main__":
    setup_logging(
        filename="logs/BlocksScreen.log",
        level=logging.DEBUG,
        console_output=True,
        console_level=logging.DEBUG,
        capture_stderr=True,
        capture_stdout=False,
    )
    _logger = logging.getLogger(__name__)
    _logger.info("============ BlocksScreen Initializing ============")
    BlocksScreen = BlocksScreenApp([])
    BlocksScreen.setApplicationName("BlocksScreen")
    BlocksScreen.setApplicationDisplayName("BlocksScreen")
    BlocksScreen.setDesktopFileName("BlocksScreen")
    main_window = MainWindow()
    BlocksScreen.processEvents()
    BlocksScreen.aboutToQuit.connect(on_quit)
    main_window.show()
    sys.exit(BlocksScreen.exec())
