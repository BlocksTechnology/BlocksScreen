import logging
import os
import sys
import typing
from PyQt6 import QtCore, QtWidgets

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
        if not (os.path.isdir(gcodes_dir) and os.path.exists(gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, mnt_dir=mnt_dir, gcodes_dir=gcodes_dir
        )
        self.udisks.start(self.udisks.Priority.InheritPriority)
        # TODO:: self.udisks.finished.connect(self.restart)
        # TODO:: self.udisks.started.connect( do somethign here)

    def restart(self) -> None:
        self.udisks.start(self.udisks.Priority.InheritPriority)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # udisks = UDisksDBus(self)
        # udisks.start(priority=udisks.Priority.InheritPriority)

        # print(udisks.currentThreadId())
        udisks = USBManager(
            parent=self,
            mnt_dir="/home/bugo/printer_data/gcodes/",
            gcodes_dir="/media/",
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    app.processEvents()
    sys.exit(app.exec())
