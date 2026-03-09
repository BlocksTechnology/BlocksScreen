import logging
import os
import typing
from PyQt6 import QtCore

from .udisks2 import UDisksDBusAsync

ResType: typing.TypeAlias = typing.Literal["always", "none"]


class USBManager(QtCore.QObject):
    usb_add: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="usb-add"
    )
    usb_rem: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="usb-rem"
    )
    usb_monitor_started: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="usb-monitor-started"
    )
    usb_monitor_finished: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="usb-monitor-finished"
    )

    def __init__(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def restart(self) -> None:
        """Restart usb monitoring tool"""
        if not self.udisks.active:
            self.udisks.start(self.udisks.Priority.InheritPriority)
            return
        self.udisks.close()
        self.need_restart = True

    def _handle_full_restart(self) -> None:
        if self.need_restart:
            self.udisks.start(self.udisks.Priority.InheritPriority)
            self.need_restart = False

    @property
    def restart_type(self) -> str:
        return self._restart_type

    @restart_type.setter
    def restart_type(self, type: ResType) -> None:
        if type not in ResType:
            logging.info("Unknown restart type %s", (type,))
        self._restart_type = type
        if type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    @QtCore.pyqtSlot(name="monitor-finished")
    def _handle_monitor_finished(self) -> None:
        # Just restart the monitor for now
        self.restart()

    @QtCore.pyqtSlot(str, str, name="device-mounted")
    def handle_mounted_device(self, path, symlink) -> None:
        """Handle new mounted device"""
        pass

    @QtCore.pyqtSlot(str, name="device-unmounted")
    def handle_unmounted_device(self, path) -> None:
        """Handle unmounted device"""
        pass

    @QtCore.pyqtSlot(str, dict, name="device-added")
    def handle_new_device(self, path, interface) -> None:
        """Handle new device"""
        pass

    @QtCore.pyqtSlot(str, name="device-removed")
    def handle_rem_device(self, path) -> None:
        """Handle device removed"""
        pass

    @QtCore.pyqtSlot(str, name="hardware_detected")
    def handle_new_hardware(self, path: str):
        """Handle new usb device hardware"""
        pass

    @QtCore.pyqtSlot(str, name="hardware_removed")
    def handle_rem_hardware(self, path: str):
        """Handle usb device hardware removed"""
        pass
