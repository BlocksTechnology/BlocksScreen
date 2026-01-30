from ast import Not
import logging
import asyncio
import sys
import sdbus
from PyQt6 import QtCore, QtWidgets, QtDBus
import typing


class UsbManager(QtCore.QObject):
    usb_add: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="usb-add"
    )
    usb_rem: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="usb-rem"
    )

    def __init__(self, parent: QtCore.QObject) -> None:
        super().__init__(parent)


class UDisksDBusAsync(QtCore.QThread):
    def __init__(self, parent: QtCore.QObject) -> None:
        super().__init__(parent)
        self.system_bus: sdbus.SdBus = sdbus.sd_bus_open_system()
        if not self.system_bus:
            self.close()
            return
        sdbus.set_default_bus(self.system_bus)
        self.obj_manager: UDisks2AsyncManager = UDisks2AsyncManager.new_proxy(
            "org.freedesktop.UDisks2", "/org/freedesktop/UDisks2", self.system_bus
        )

    def _get_managed_objects(self):
        return asyncio.run(self.obj_manager.get_managed_objects())

    def _setup_asyncio_loop(self) -> None:
        asyncio.new_event_loop()
        pass

    def run(self) -> None:
        try:
            loop = self._setup_asyncio_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(asyncio.gather(self.async_listener_monitor()))
        except:
            logging.error("Caught exception on usb run loop")
        pass

    def close(self) -> None:
        pass

    async def async_listener_monitor(self) -> None:
        pass


class UDisksDBus(QtCore.QThread):
    usb_add: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(str, name="usb-add")
    usb_rem: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(str, name="usb-rem")

    def __init__(self, parent: QtCore.QObject) -> None:
        super().__init__(parent)
        self.system_bus: sdbus.SdBus = sdbus.sd_bus_open_system()
        if not self.system_bus:
            self.close()
            return
        sdbus.set_default_bus(self.system_bus)
        self.obj_manager: UDisks2Manager = UDisks2Manager(
            "org.freedesktop.UDisks2", "/org/freedesktop/UDisks2", self.system_bus
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start())
        udisks = UDisks2DBusAsync(loop)
        loop.run_forever()

    def run(self) -> None:
        # self.obj_manager.InterfacesAdded(obj path, dict entyry)
        # self.obj_manager.InterfacesRemoved(obj path, dict entyr)
        # self.obj_manager.interfaces_added.connect(self._on_interface_added)
        print(self.obj_manager.get_managed_objects())
        # self.obj_manager.interfaces_removed.connect(self._on_interface_removed)

    def _on_interface_added(self, path, interfaces) -> None:
        pass

    def _on_interface_removed(self, path, interfaces) -> None:
        pass

    def close(self) -> None:
        logging.info("Closing usb udisks2 dbus connection")
        self.system_bus.close()
        self.quit()

    def safe_remove(self, bus, drive_path) -> None:
        pass

    def create_symlink(self, bus, drive_path, directory) -> None:
        pass

    def power_off(self, bus, drive_path) -> None:
        pass

    def check_eject_support(sefl, bus, drive_path) -> None:
        pass

    def force_refresh(self, bus, drive_path) -> None:
        pass

    def get_clean_symlinks(self, bus, drive_path) -> None:
        pass


class UDisks2AsyncManager(sdbus.DbusObjectManagerInterfaceAsync):
    """Subclassed async dbus object manager"""

    def __init__(self) -> None:
        super().__init__()


class UDisks2Manager(sdbus.DbusObjectManagerInterface):
    """subclassed Dbus object manager"""

    def __init__(
        self,
        service_name: str,
        object_path: str,
        bus: sdbus.SdBus | None = None,
    ):
        super().__init__(service_name, object_path, bus)


class UDisks2FileSystemAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name="org.freedesktop.UDisks2.Filesystem"
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_method_async(input_signature="a{sv}", result_signature="s")
    async def mount(self, opts) -> str:
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="a{sv}")
    async def unmount(self, opts) -> None:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def size(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="ayy")
    def mount_points(self) -> list[str]:
        raise NotImplementedError


class UDisks2FileSystemInterface(
    sdbus.DbusInterfaceCommon, interface_name="org.freedesktop.UDisks2.Filesystem"
):
    @sdbus.dbus_method(input_signature="a{sv}", result_signature="s")
    def mount(self, opts) -> str:
        raise NotImplementedError

    @sdbus.dbus_method(input_signature="a{sv}")
    def unmount(self, opts) -> None:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="t")
    def size(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="ayy")
    def mount_points(self) -> list[str]:
        raise NotImplementedError


class UDisks2BlockAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name="org.freedesktop.UDisks2.Block"
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_property_async(property_signature="s")
    def hint_name(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="ay")
    def device(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def device_number(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id_label(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id_UUID(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id_usage(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id_type(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="ayy")
    def symlinks(self) -> list[bytes]:
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="a{sv}")
    async def rescan(self, opts: dict) -> None:
        raise NotImplementedError


class UDisks2BlockInterface(
    sdbus.DbusInterfaceCommon, interface_name="org.freedesktop.UDisks2.Block"
):
    @sdbus.dbus_property(property_signature="s")
    def hint_name(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="ay")
    def device(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="t")
    def device_number(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def id(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def id_label(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def id_UUID(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def id_usage(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="ayy")
    def symlinks(self) -> list[bytes]:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def id_type(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_method(input_signature="a{sv}")
    def rescan(self, opts: dict) -> None:
        raise NotImplementedError


class UDisks2DriveAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name="org.freedesktop.UDisks2.Drive"
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_property_async(property_signature="b")
    def can_power_off(self) -> bool:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def model(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def serial(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def ejectable(self) -> bool:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def removable(self) -> bool:  # FIXME : MAYBE THIS IS BYTES INSTEAD OF BOOL
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def time_detected(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def media_available(self) -> bytes:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def media_changed_detected(self) -> bytes:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def media(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="a{sv}")
    async def eject(self, opts: dict) -> None:
        raise NotImplementedError


class UDisks2DriveInterface(
    sdbus.DbusInterfaceCommon, interface_name="org.freedesktop.UDisks2.Drive"
):
    @sdbus.dbus_property(property_signature="b")
    def can_power_off(self) -> bool:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def model(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def serial(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="b")
    def ejectable(self) -> bool:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="b")
    def removable(self) -> bytes:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="t")
    def time_detected(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="b")
    def media_available(self) -> bytes:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="b")
    def media_changed_detected(self) -> bytes:
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def media(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_method(input_signature="a{sv}")
    def eject(self, opts: dict) -> None:
        raise NotImplementedError


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # udisks = UDisksDBus(self)
        # udisks.start(priority=udisks.Priority.InheritPriority)

        # print(udisks.currentThreadId())
        udisks = UDisksDBusAsync(self)
        udisks.start(priority=udisks.Priority.InheritPriority)


# async def start() -> None:
# bus = sdbus.sd_bus_open_system()
# fs = UDisks2BlockAsyncInterface().new_proxy(
#     "org.freedesktop.UDisks2", "/org/freedesktop/UDisks2/block_devices/sdd", bus
# )
#
# id = await fs.device_number
# device = await fs.device
# print(id)
# print(device)
# manager = UDisks2DBusAsync()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    app.processEvents()
    sys.exit(app.exec())
