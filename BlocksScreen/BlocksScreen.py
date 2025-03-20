import logging
import logging.handlers
import sys
import typing

import logger
import PyQt6
import PyQt6.Qt6
import PyQt6.Qt6.lib
import PyQt6.QtCore
import PyQt6.QtGui
import PyQt6.QtWidgets
from lib.panels.mainWindow import MainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QSplashScreen, QWidget

_logger = logging.getLogger(name="logs/BlocksScreen.log")


def setup_working_dir(): ...


def setup_app_loggers():
    ql = logger.create_logger(name="logs/BlocksScreen.log", level=logging.DEBUG)
    _logger = logging.getLogger(name="logs/BlocksScreen.log")
    _logger.info("============ BlocksScreen Initializing ============")


def show_splash(window: typing.Optional["QWidget"] = None):
    logo = QPixmap("Blocks_Screen/BlocksScreen/lib/ui/resources/logoblocks.png")
    splash = QSplashScreen(pixmap=logo)
    splash.setGeometry(PyQt6.QtCore.QRect(0, 0, 400, 200))
    # splash.showFullScreen()
    # splash.show()
    # sleep(2)

    # * Wait until the *window* is in view to close the splash screen
    if window is not None and isinstance(window, QWidget):
        splash.finish(window)


def run():
    setup_app_loggers()
    BlocksScreen = QApplication([])
    main_window = MainWindow()

    show_splash(main_window)

    BlocksScreen.setApplicationName("BlocksScreen")
    BlocksScreen.setApplicationDisplayName("BlocksScreen")
    BlocksScreen.setDesktopFileName("BlocksScreen")

    # ! Someone said that .processEvents sometimes crashes the system
    BlocksScreen.processEvents()

    # main_window.setScreen(BlocksScreen.screens()[2])

    # main_window.showFullScreen()
    main_window.showNormal()
    main_window.bo_startup.emit()
    sys.exit(BlocksScreen.exec())


if __name__ == "__main__":
    run()


# =============== VISUAL ASPECTS =============== #
# TODO: Add Bed heater icon
# TODO: Add Extruder heater icon


# =============== FUNCTIONALITY =============== #
# TODO: Add dynamically heater objects to the header
# TODO: Block the bar when the printer is doing stuff
# TODO: Create a callable window for errors, or warnings, that does not fade until the problem is corrected
# TODO: Add the wifi panel button with the icon


# TODO: When closing the application i need to guarantee that every single thread is also stopped.

# EXPLORE IMPLEMENTATION: Garbage collector (python gc package) !!

# TODO: Grey out the tab menu when the printer is actually printing
# BUG:  After printing, the tab bar remain disabled and cannot go to other menus


# TODO: Create a class that handles all the connections of signals and redirection


# QCoreApplication.postEvent -> post event is handled asynchronously

# QCoreApplication.sendEvent -> sendEvent is handled immediately
