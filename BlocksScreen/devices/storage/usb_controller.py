import logging
import os
import typing
from PyQt6 import QtCore

from .udisks2 import UDisksDBusAsync


class USBManager(QtCore.QObject):
    usb_add: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="usb-add"
    )
    usb_rem: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="usb-rem"
    )

    def __init__(self, parent: QtCore.QObject, gcodes_dir: str, mnt_dir: str) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self._handle_new_hardware)
        self.udisks.hardware_removed.connect(self._handle_rem_hardware)

    def restart(self) -> None:
        self.udisks.start(self.udisks.Priority.InheritPriority)

    @QtCore.pyqtSlot(str, name="hardware_detected")
    def _handle_new_hardware(self, path: str):
        print("New hardware detected")

    @QtCore.pyqtSlot(str, name="hardware_removed")
    def _handle_rem_hardware(self, path: str):
        print("hardware  removed detected")
