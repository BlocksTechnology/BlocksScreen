import logging
import sys
import typing

from logger import CrashHandler, LogManager, install_crash_handler, setup_logging

install_crash_handler()

from lib.panels.mainWindow import MainWindow  # noqa: E402
from PyQt6 import QtCore, QtGui, QtWidgets  # noqa: E402


class BlocksScreenApp(QtWidgets.QApplication):
    """QApplication subclass that routes unhandled slot exceptions to CrashHandler."""

    def notify(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False


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
    """Show splash screen on app initialization"""
    logo = QtGui.QPixmap("BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def on_quit() -> None:
    logging.info("Final exit cleanup")
    LogManager.shutdown()


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
