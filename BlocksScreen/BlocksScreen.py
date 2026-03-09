import logging
import sys
import typing

from lib.panels.mainWindow import MainWindow
from logger import setup_logging, LogManager
from PyQt6 import QtCore, QtGui, QtWidgets

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
    BlocksScreen = QtWidgets.QApplication([])
    BlocksScreen.setApplicationName("BlocksScreen")
    BlocksScreen.setApplicationDisplayName("BlocksScreen")
    BlocksScreen.setDesktopFileName("BlocksScreen")
    main_window = MainWindow()
    BlocksScreen.processEvents()
    BlocksScreen.aboutToQuit.connect(on_quit)
    main_window.show()
    sys.exit(BlocksScreen.exec())
