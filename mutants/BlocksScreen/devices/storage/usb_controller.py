import logging
import os
import typing
from PyQt6 import QtCore

from .udisks2 import UDisksDBusAsync
from lib.panels.widgets.bannerPopup import BannerPopup

ResType: typing.TypeAlias = typing.Literal["always", "none"]
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


class USBManager(QtCore.QObject):
    usb_add: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, dict, name="usb-add"
    )
    usb_rem: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="usb-rem"
    )
    usb_hardware_detected: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="hardware-detected"
    )
    usb_hardware_removed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="hardware-removed"
    )
    usb_monitor_started: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="usb-monitor-started"
    )
    usb_monitor_finished: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="usb-monitor-finished"
    )
    usb_mounted: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="device-mounted"
    )

    usb_unmounted: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="device-unmounted"
    )

    def __init__(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        args = [parent, gcodes_dir]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUSBManagerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁUSBManagerǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁUSBManagerǁ__init____mutmut_orig(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_1(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(None)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_2(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = None
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_3(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir and os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_4(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser(None)
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_5(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("XX~/printer_data/gcodesXX")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_6(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/PRINTER_DATA/GCODES")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_7(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_8(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) or os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_9(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(None) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_10(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(None)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_11(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info(None)
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_12(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("XXProvided gcodes directory does not exist.XX")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_13(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_14(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("PROVIDED GCODES DIRECTORY DOES NOT EXIST.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_15(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = None
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_16(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=None, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_17(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=None
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_18(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_19(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_20(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = None
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_21(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = None
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_22(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "XXalwaysXX"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_23(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "ALWAYS"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_24(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(None)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_25(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(None)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_26(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(None)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_27(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(None)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_28(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(None)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_29(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(None)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_30(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(None)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_31(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(None)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_32(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(None)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_33(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(None)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_34(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(None)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_35(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(None)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_36(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(None)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_37(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(None)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_38(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(None)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_39(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = None
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_40(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = True
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_41(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(None)
        if self.restart_type == "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_42(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type != "always":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_43(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "XXalwaysXX":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_44(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "ALWAYS":
            self.udisks.finished.connect(self._handle_monitor_finished)

    def xǁUSBManagerǁ__init____mutmut_45(self, parent: QtCore.QObject, gcodes_dir: str | None) -> None:
        super().__init__(parent)
        self.gcodes_dir: str = gcodes_dir or os.path.expanduser("~/printer_data/gcodes")
        if not (os.path.isdir(self.gcodes_dir) and os.path.exists(self.gcodes_dir)):
            logging.info("Provided gcodes directory does not exist.")
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, gcodes_dir=self.gcodes_dir
        )
        # self.banner = BannerPopup(self)
        self.banner = BannerPopup()
        self._restart_type: ResType = "always"
        self.udisks.start(self.udisks.Priority.InheritPriority)
        self.udisks.hardware_detected.connect(self.handle_new_hardware)
        self.udisks.hardware_detected.connect(self.usb_hardware_detected)
        self.udisks.hardware_removed.connect(self.handle_rem_hardware)
        self.udisks.hardware_removed.connect(self.usb_hardware_removed)
        self.udisks.device_added.connect(self.handle_new_device)
        self.udisks.device_added.connect(self.usb_add)
        self.udisks.device_removed.connect(self.handle_rem_device)
        self.udisks.device_removed.connect(self.usb_rem)
        self.udisks.device_mounted.connect(self.handle_mounted_device)
        self.udisks.device_mounted.connect(self.usb_mounted)
        self.udisks.device_unmounted.connect(self.handle_unmounted_device)
        self.udisks.device_unmounted.connect(self.usb_unmounted)
        self.udisks.started.connect(self.usb_monitor_started)
        self.udisks.finished.connect(self.usb_monitor_finished)
        self.need_restart: bool = False
        self.udisks.finished.connect(self._handle_full_restart)
        if self.restart_type == "always":
            self.udisks.finished.connect(None)
    
    xǁUSBManagerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUSBManagerǁ__init____mutmut_1': xǁUSBManagerǁ__init____mutmut_1, 
        'xǁUSBManagerǁ__init____mutmut_2': xǁUSBManagerǁ__init____mutmut_2, 
        'xǁUSBManagerǁ__init____mutmut_3': xǁUSBManagerǁ__init____mutmut_3, 
        'xǁUSBManagerǁ__init____mutmut_4': xǁUSBManagerǁ__init____mutmut_4, 
        'xǁUSBManagerǁ__init____mutmut_5': xǁUSBManagerǁ__init____mutmut_5, 
        'xǁUSBManagerǁ__init____mutmut_6': xǁUSBManagerǁ__init____mutmut_6, 
        'xǁUSBManagerǁ__init____mutmut_7': xǁUSBManagerǁ__init____mutmut_7, 
        'xǁUSBManagerǁ__init____mutmut_8': xǁUSBManagerǁ__init____mutmut_8, 
        'xǁUSBManagerǁ__init____mutmut_9': xǁUSBManagerǁ__init____mutmut_9, 
        'xǁUSBManagerǁ__init____mutmut_10': xǁUSBManagerǁ__init____mutmut_10, 
        'xǁUSBManagerǁ__init____mutmut_11': xǁUSBManagerǁ__init____mutmut_11, 
        'xǁUSBManagerǁ__init____mutmut_12': xǁUSBManagerǁ__init____mutmut_12, 
        'xǁUSBManagerǁ__init____mutmut_13': xǁUSBManagerǁ__init____mutmut_13, 
        'xǁUSBManagerǁ__init____mutmut_14': xǁUSBManagerǁ__init____mutmut_14, 
        'xǁUSBManagerǁ__init____mutmut_15': xǁUSBManagerǁ__init____mutmut_15, 
        'xǁUSBManagerǁ__init____mutmut_16': xǁUSBManagerǁ__init____mutmut_16, 
        'xǁUSBManagerǁ__init____mutmut_17': xǁUSBManagerǁ__init____mutmut_17, 
        'xǁUSBManagerǁ__init____mutmut_18': xǁUSBManagerǁ__init____mutmut_18, 
        'xǁUSBManagerǁ__init____mutmut_19': xǁUSBManagerǁ__init____mutmut_19, 
        'xǁUSBManagerǁ__init____mutmut_20': xǁUSBManagerǁ__init____mutmut_20, 
        'xǁUSBManagerǁ__init____mutmut_21': xǁUSBManagerǁ__init____mutmut_21, 
        'xǁUSBManagerǁ__init____mutmut_22': xǁUSBManagerǁ__init____mutmut_22, 
        'xǁUSBManagerǁ__init____mutmut_23': xǁUSBManagerǁ__init____mutmut_23, 
        'xǁUSBManagerǁ__init____mutmut_24': xǁUSBManagerǁ__init____mutmut_24, 
        'xǁUSBManagerǁ__init____mutmut_25': xǁUSBManagerǁ__init____mutmut_25, 
        'xǁUSBManagerǁ__init____mutmut_26': xǁUSBManagerǁ__init____mutmut_26, 
        'xǁUSBManagerǁ__init____mutmut_27': xǁUSBManagerǁ__init____mutmut_27, 
        'xǁUSBManagerǁ__init____mutmut_28': xǁUSBManagerǁ__init____mutmut_28, 
        'xǁUSBManagerǁ__init____mutmut_29': xǁUSBManagerǁ__init____mutmut_29, 
        'xǁUSBManagerǁ__init____mutmut_30': xǁUSBManagerǁ__init____mutmut_30, 
        'xǁUSBManagerǁ__init____mutmut_31': xǁUSBManagerǁ__init____mutmut_31, 
        'xǁUSBManagerǁ__init____mutmut_32': xǁUSBManagerǁ__init____mutmut_32, 
        'xǁUSBManagerǁ__init____mutmut_33': xǁUSBManagerǁ__init____mutmut_33, 
        'xǁUSBManagerǁ__init____mutmut_34': xǁUSBManagerǁ__init____mutmut_34, 
        'xǁUSBManagerǁ__init____mutmut_35': xǁUSBManagerǁ__init____mutmut_35, 
        'xǁUSBManagerǁ__init____mutmut_36': xǁUSBManagerǁ__init____mutmut_36, 
        'xǁUSBManagerǁ__init____mutmut_37': xǁUSBManagerǁ__init____mutmut_37, 
        'xǁUSBManagerǁ__init____mutmut_38': xǁUSBManagerǁ__init____mutmut_38, 
        'xǁUSBManagerǁ__init____mutmut_39': xǁUSBManagerǁ__init____mutmut_39, 
        'xǁUSBManagerǁ__init____mutmut_40': xǁUSBManagerǁ__init____mutmut_40, 
        'xǁUSBManagerǁ__init____mutmut_41': xǁUSBManagerǁ__init____mutmut_41, 
        'xǁUSBManagerǁ__init____mutmut_42': xǁUSBManagerǁ__init____mutmut_42, 
        'xǁUSBManagerǁ__init____mutmut_43': xǁUSBManagerǁ__init____mutmut_43, 
        'xǁUSBManagerǁ__init____mutmut_44': xǁUSBManagerǁ__init____mutmut_44, 
        'xǁUSBManagerǁ__init____mutmut_45': xǁUSBManagerǁ__init____mutmut_45
    }
    xǁUSBManagerǁ__init____mutmut_orig.__name__ = 'xǁUSBManagerǁ__init__'

    def restart(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUSBManagerǁrestart__mutmut_orig'), object.__getattribute__(self, 'xǁUSBManagerǁrestart__mutmut_mutants'), args, kwargs, self)

    def xǁUSBManagerǁrestart__mutmut_orig(self) -> None:
        """Restart usb monitoring tool"""
        if not self.udisks.active:
            self.udisks.start(self.udisks.Priority.InheritPriority)
            return
        self.udisks.close()
        self.need_restart = True

    def xǁUSBManagerǁrestart__mutmut_1(self) -> None:
        """Restart usb monitoring tool"""
        if self.udisks.active:
            self.udisks.start(self.udisks.Priority.InheritPriority)
            return
        self.udisks.close()
        self.need_restart = True

    def xǁUSBManagerǁrestart__mutmut_2(self) -> None:
        """Restart usb monitoring tool"""
        if not self.udisks.active:
            self.udisks.start(None)
            return
        self.udisks.close()
        self.need_restart = True

    def xǁUSBManagerǁrestart__mutmut_3(self) -> None:
        """Restart usb monitoring tool"""
        if not self.udisks.active:
            self.udisks.start(self.udisks.Priority.InheritPriority)
            return
        self.udisks.close()
        self.need_restart = None

    def xǁUSBManagerǁrestart__mutmut_4(self) -> None:
        """Restart usb monitoring tool"""
        if not self.udisks.active:
            self.udisks.start(self.udisks.Priority.InheritPriority)
            return
        self.udisks.close()
        self.need_restart = False
    
    xǁUSBManagerǁrestart__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUSBManagerǁrestart__mutmut_1': xǁUSBManagerǁrestart__mutmut_1, 
        'xǁUSBManagerǁrestart__mutmut_2': xǁUSBManagerǁrestart__mutmut_2, 
        'xǁUSBManagerǁrestart__mutmut_3': xǁUSBManagerǁrestart__mutmut_3, 
        'xǁUSBManagerǁrestart__mutmut_4': xǁUSBManagerǁrestart__mutmut_4
    }
    xǁUSBManagerǁrestart__mutmut_orig.__name__ = 'xǁUSBManagerǁrestart'

    def close(self) -> None:
        """Close usb monitoring tool"""
        self.udisks.close()
        self.deleteLater()

    def _handle_full_restart(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUSBManagerǁ_handle_full_restart__mutmut_orig'), object.__getattribute__(self, 'xǁUSBManagerǁ_handle_full_restart__mutmut_mutants'), args, kwargs, self)

    def xǁUSBManagerǁ_handle_full_restart__mutmut_orig(self) -> None:
        if self.need_restart:
            self.udisks.start(self.udisks.Priority.InheritPriority)
            self.need_restart = False

    def xǁUSBManagerǁ_handle_full_restart__mutmut_1(self) -> None:
        if self.need_restart:
            self.udisks.start(None)
            self.need_restart = False

    def xǁUSBManagerǁ_handle_full_restart__mutmut_2(self) -> None:
        if self.need_restart:
            self.udisks.start(self.udisks.Priority.InheritPriority)
            self.need_restart = None

    def xǁUSBManagerǁ_handle_full_restart__mutmut_3(self) -> None:
        if self.need_restart:
            self.udisks.start(self.udisks.Priority.InheritPriority)
            self.need_restart = True
    
    xǁUSBManagerǁ_handle_full_restart__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUSBManagerǁ_handle_full_restart__mutmut_1': xǁUSBManagerǁ_handle_full_restart__mutmut_1, 
        'xǁUSBManagerǁ_handle_full_restart__mutmut_2': xǁUSBManagerǁ_handle_full_restart__mutmut_2, 
        'xǁUSBManagerǁ_handle_full_restart__mutmut_3': xǁUSBManagerǁ_handle_full_restart__mutmut_3
    }
    xǁUSBManagerǁ_handle_full_restart__mutmut_orig.__name__ = 'xǁUSBManagerǁ_handle_full_restart'

    @property
    def restart_type(self) -> ResType:
        return self._restart_type

    @restart_type.setter
    def restart_type(self, type: ResType) -> None:
        """Tool restart type, currently there are only two
        options available.

            - `always` - restarts the tool every time it stops
            - `none` - doesn't restart the tool at all
        """
        if type not in ("always", "none"):
            logging.info("Unknown restart type %s", (type,))
        if type == "always":
            if not self._restart_type == "always":
                self.udisks.finished.connect(self._handle_monitor_finished)
        else:
            try:
                self.udisks.finished.disconnect(self._handle_monitor_finished)
            except TypeError:
                pass
        self._restart_type = type

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
    def handle_new_hardware(self, path: str) -> None:
        """Handle new usb device hardware"""
        self.banner.new_message(self.banner.MessageType.CONNECT)

    @QtCore.pyqtSlot(str, name="hardware_removed")
    def handle_rem_hardware(self, path: str) -> None:
        """Handle usb device hardware removed"""
        self.banner.new_message(self.banner.MessageType.DISCONNECT)
