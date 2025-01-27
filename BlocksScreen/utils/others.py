#!/usr/bin/python
import logging
import queue
import threading
import typing
from functools import partial

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QPushButton, QStackedWidget, QStyle, QWidget

# from qt_ui.customNumpad_ui import Ui_customNumpad

_logger = logging.getLogger(__name__)




# PYTHON 'is' checks if the object points to the same object, which is different than ==






# TODO: Create a method that checks if the application requirements
# TODO: Create a method that validates the working directory of the GUI


def validate_requirements(): ...
def validate_working_dir(): ...
def scan_dir(dir: str) -> typing.Dict: ...
def scan_file(filename: str, dir: str) -> bool: ...


def validate_directory() -> bool: ...


def scan_directory(dir: str, ext: str = None):
    ...
    # """Scan a directory for files and nested directories"""
    # if not isinstance(dir, str):
    #     raise ValueError("dir expected str type")

    # if os.access(dir, os.X_OK and os.W_OK and os.R_OK):
    #     for root, dirs, files in os.walk(dir):

    #         for
