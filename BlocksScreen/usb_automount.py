import os
import logging
import asyncio
import sys
import sdbus
from PyQt6 import QtCore, QtWidgets, QtDBus
import typing


class USBManager(QtCore.QObject):
    usb_add: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="usb-add"
    )
    usb_rem: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="usb-rem"
    )

    def __init__(self, parent: QtCore.QObject, mnt_path: str, search_path: str) -> None:
        super().__init__(parent)
        self.udisks: UDisksDBusAsync = UDisksDBusAsync(
            parent=self, mnt_path=mnt_path, search_path=search_path
        )
        # self.udisks.finished.connect(self.restart)  # TODO: Implement thread restart
        self.udisks.start(self.udisks.Priority.InheritPriority)

    def close(self) -> None:
        pass

    def restart(self) -> None:
        self.udisks.start(self.udisks.Priority.InheritPriority)


class UDisksDBusAsync(QtCore.QThread):
    device_added: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, dict, name="device-added"
    )
    device_removed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="device-removed"
    )

    def __init__(self, parent: QtCore.QObject, mnt_path: str, search_path: str) -> None:
        super().__init__(parent)
        self.task_stack = set()
        self.mnt_path: str = mnt_path
        self.search_path: str = search_path
        self.system_bus: sdbus.SdBus = sdbus.sd_bus_open_system()
        if not self.system_bus:
            self.close()
            return
        sdbus.set_default_bus(self.system_bus)
        self.obj_manager: UDisks2AsyncManager = UDisks2AsyncManager.new_proxy(
            "org.freedesktop.UDisks2", "/org/freedesktop/UDisks2", self.system_bus
        )
        self.loop: asyncio.AbstractEventLoop | None = None
        self.stop_event: asyncio.Event = asyncio.Event()
        self.listener_running: bool = False
        self.controlled_devs = {}

    def run(self) -> None:
        """Start UDisks2 USB monitoring"""
        self.stop_event.clear()
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.monitor_dbus())
        except asyncio.CancelledError as err:
            logging.error("Caught exception on udisks2 monitor, %s", err)
            self.close()
            return

    def close(self) -> None:
        if not self.loop:
            return  # TODO: Raise an exception or do something when the loop does not exist
        try:
            if self.loop.is_running():
                self.stop_event.set()
                self.loop.call_soon_threadsafe(self.loop.stop)
            self.quit()
            self.wait()
            self.deleteLater()
        except asyncio.CancelledError as e:
            logging.error(
                "Caught exception while trying to close Udisks2 monitor: %s", e
            )

    async def monitor_dbus(self) -> None:
        """Schedule coroutines for UDisks2 signals `interfaces_added` and `interfaces_removed`
        Creates symlink upon device insertion and cleans up symlink on removal.

        """
        add_listener = asyncio.create_task(self._add_interface_listener())
        rem_listener = asyncio.create_task(self._rem_interface_listener())
        self.task_stack.add(add_listener)
        self.task_stack.add(rem_listener)
        while self.stop_event:
            try:
                await asyncio.gather(add_listener, rem_listener)
                add_listener.add_done_callback(self.task_stack.discard(add_listener))
                rem_listener.add_done_callback(self.task_stack.discard(rem_listener))
            except asyncio.CancelledError:
                add_listener.cancel()
                rem_listener.cancel()
                # TODO: Add logging here

    async def _add_interface_listener(self) -> None:
        async for path, interfaces in self.obj_manager.interfaces_added:
            if "org.freedesktop.UDisks2.Block" in interfaces:
                self.device_added.emit(path, interfaces)
                bdev = UDisks2BlockAsyncInterface.new_proxy(
                    "org.freedesktop.UDisks2", path, self.system_bus
                )
                drive_path = await bdev.drive
                if not drive_path:
                    continue
                ddev = UDisks2DriveAsyncInterface.new_proxy(
                    "org.freedesktop.UDisks2", drive_path, self.system_bus
                )
                vendor_name = await ddev.vendor
                con_bus, removable, media_removable = await asyncio.gather(
                    ddev.connection_bus,
                    ddev.removable,
                    ddev.media_removable,
                )
                if con_bus.lower() == "usb":
                    if removable and media_removable:
                        self.add_symlink("/home/bugo/printer_data/gcodes/USB_PEN")
                        print(
                            f"MEDIA ADDED, {vendor_name}, {con_bus}, {removable}, {media_removable}"
                        )

    async def _rem_interface_listener(self) -> None:
        async for path, interfaces in self.obj_manager.interfaces_removed:
            if "org.freedesktop.UDisks2.Block" in interfaces:
                os.rmdir("/home/bugo/printer_data/gcodes/USB_PEN")

    def add_symlink(self, path: str) -> None:
        """Create symlink on `path`"""
        if not (os.path.exists(path) or os.path.islink(path)):
            os.symlink(
                src="/media/bugo/BLOCKS",
                dst="/home/bugo/printer_data/gcodes/USB_PEN",
            )

    def rem_symlink(self, path: str) -> None:
        """Remove symlink located in `path`"""
        if os.path.islink(path) or os.path.exists(path):
            try:
                os.remove(path)
                logging.info("Symlink cleaning done, removed %s", path)
            except OSError as e:
                logging.error(
                    "Caught exception while trying to remove USB symlink: %s", e
                )


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

    @sdbus.dbus_property_async(property_signature="o")
    def drive(self) -> str:
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
    def connection_bus(self) -> str:
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

    @sdbus.dbus_property_async(property_signature="b")
    def media_removable(self) -> bool:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def vendor(self) -> str:
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
        udisks = USBManager(
            parent=self,
            mnt_path="/home/bugo/printer_data/gcodes/",
            search_path="/media/",
        )


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
