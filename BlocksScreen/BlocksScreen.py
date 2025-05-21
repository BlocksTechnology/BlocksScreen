import logging
import os
import sys
import typing


import logger
import helper_methods as helper_methods
from screensaver import ScreenSaver
from lib.panels.mainWindow import MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1.0"
os.environ["QT_SCALE_FACTOR"] = "1.0"
os.environ["QT_DEVICE_PIXEL_RATIO"] = "1.0"
os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["QT_STYLE_OVERRIDE"] = "fusion"


_logger = logging.getLogger(name="logs/BlocksScreen.log")

QtGui.QGuiApplication.setHighDpiScaleFactorRoundingPolicy(  # type: ignore
    QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Ceil
)
QtGui.QGuiApplication.setLayoutDirection(  # type: ignore
    QtCore.Qt.LayoutDirection.LayoutDirectionAuto
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


def show_splash(window: typing.Optional["QtWidgets.QWidget"] = None):
    logo = QtGui.QPixmap(
        "Blocks_Screen/BlocksScreen/lib/ui/resources/logoblocks.png"
    )
    splash = QtWidgets.QSplashScreen(pixmap=logo)
    splash.setGeometry(QtCore.QRect(0, 0, 400, 200))
    # splash.showFullScreen()
    # splash.show()
    # sleep(2)

    # * Wait until the *window* is in view to close the splash screen
    if window is not None and isinstance(window, QtWidgets.QWidget):
        splash.finish(window)


def run():
    print(f"{RED} STARTING BLOCKS SCREEN {RESET}")
    setup_app_loggers()
    BlocksScreen = QtWidgets.QApplication([])
    main_window = MainWindow()

    show_splash(main_window)

    BlocksScreen.setApplicationName("BlocksScreen")
    BlocksScreen.setApplicationDisplayName("BlocksScreen")
    BlocksScreen.setDesktopFileName("BlocksScreen")
    BlocksScreen.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Round
    )

    screensaver = ScreenSaver()

    # ! Someone said that .processEvents sometimes crashes the system
    BlocksScreen.processEvents()
    # main_window.setScreen(BlocksScreen.screens()[2])
    # main_window.showFullScreen()
    main_window.showNormal()
    main_window.bo_ws_startup.emit()
    sys.exit(BlocksScreen.exec())


if __name__ == "__main__":
    run()
