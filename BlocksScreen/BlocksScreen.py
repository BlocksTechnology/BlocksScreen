
import logging
import sys
import typing

import helper_methods as helper_methods
import logger
from lib.panels.mainWindow import MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets

_logger = logging.getLogger(name="logs/BlocksScreen.log")
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


def setup_working_dir(): ...


def setup_app_loggers():
    ql = logger.create_logger(
        name="logs/BlocksScreen.log", level=logging.DEBUG
    )
    _logger = logging.getLogger(name="logs/BlocksScreen.log")
    _logger.info("============ BlocksScreen Initializing ============")


def show_splash(window: typing.Optional[QtWidgets.QWidget] = None):
    logo = QtGui.QPixmap(
        "BlocksScreen/BlocksScreen/lib/ui/resources/logoblocks.png"
    )
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def run():
    setup_app_loggers()
    BlocksScreen = QtWidgets.QApplication([])
    BlocksScreen.setApplicationName("BlocksScreen")
    BlocksScreen.setApplicationDisplayName("BlocksScreen")
    BlocksScreen.setDesktopFileName("BlocksScreen")
    
    main_window = MainWindow()

    BlocksScreen.processEvents()
    main_window.show()
    sys.exit(BlocksScreen.exec())


if __name__ == "__main__":
    run()
