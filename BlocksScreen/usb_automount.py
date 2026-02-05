import asyncio
import logging
import os
import pathlib
import sys
import typing

import sdbus
from PyQt6 import QtCore, QtWidgets

# TODO: Add a way to verify the mnt_path and search_path, correlate those paths to the user, and infer where they may be located
# TODO: This is done so that we only need to use /media as the mnt path and printer_data/gcodes for the search_path, maybey also change the name of search_path because it is just very very wrong.
# TODO: Add more exception handling, missing timeouts and other sdbus issues that can appear
# TODO: Add restart UDisksDBusAsync thread, instantiate again or just create methods inside that class that make it restart itself


# NOTE: If the HINTSYSTEM == true then i should ignore because the partition may have OS sensitive partitions.NotImplementedError(
#
# )
class Device:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.partitions: dict[str, dict] = {}

    def update(self, data: dict) -> None:
        pass


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


class UDisksDBusAsync(QtCore.QThread):
    device_added: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, dict, name="device-added"
    )
    device_removed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="device-removed"
    )

    def __init__(self, parent: QtCore.QObject, mnt_dir: str, gcodes_dir: str) -> None:
        super().__init__(parent)
        self.task_stack = set()
        self.mnt_path: pathlib.Path = pathlib.Path(mnt_dir)
        self.gcodes_path: pathlib.Path = pathlib.Path(gcodes_dir)
        self.system_bus: sdbus.SdBus = sdbus.sd_bus_open_system()
        if not self.system_bus:
            self.close()
            return
        sdbus.set_default_bus(self.system_bus)
        self.obj_manager: UDisks2AsyncManager = UDisks2AsyncManager.new_proxy(
            service_name="org.freedesktop.UDisks2",
            object_path="/org/freedesktop/UDisks2",
            bus=self.system_bus,
        )
        self.loop: asyncio.AbstractEventLoop | None = None
        self.stop_event: asyncio.Event = asyncio.Event()
        self.listener_running: bool = False
        self.controlled_devs: dict[str, Device] = {}

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
            _ = self.wait()
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
        pchange_listener = asyncio.create_task(self._properties_changed_listener())
        self.task_stack.add(add_listener)
        self.task_stack.add(rem_listener)
        self.task_stack.add(pchange_listener)
        while self.stop_event:
            try:
                await asyncio.gather(add_listener, rem_listener, pchange_listener)
                add_listener.add_done_callback(
                    lambda _: self.task_stack.discard(add_listener)
                )
                rem_listener.add_done_callback(
                    lambda _: self.task_stack.discard(rem_listener)
                )
                pchange_listener.add_done_callback(
                    lambda _: self.task_stack.discard(pchange_listener)
                )
            except asyncio.CancelledError as e:
                _ = add_listener.cancel()
                _ = rem_listener.cancel()
                _ = pchange_listener.cancel()
                logging.error(
                    "Caught exception while starting UDisks2 interfaces listeners: %s",
                    e,
                )

    async def _add_interface_listener(self) -> None:
        async for path, interfaces in self.obj_manager.interfaces_added:
            if "org.freedesktop.Udisks2.Drive" in interfaces:
                dev = Device(path)
                self.controlled_devs.update({path: dev})
                continue
            if "org.freedesktop.UDisks2.Block" in interfaces:
                print("Reconizing block now ")
                bdev: UDisks2BlockAsyncInterface = UDisks2BlockAsyncInterface.new_proxy(
                    service_name="org.freedesktop.UDisks2",
                    object_path=path,
                    bus=self.system_bus,
                )
                drv_path = await bdev.drive
                print(drv_path)
                if drv_path in self.controlled_devs:
                    print("Driver in controlled devs")
                    dev: Device = self.controlled_devs[drv_path]
                    if "org.freedesktop.UDisks2.Filesystem" in interfaces:
                        devfs: UDisks2FileSystemAsyncInterface = (
                            UDisks2FileSystemAsyncInterface.new_proxy(
                                service_name="org.freedesktop.UDisks2",
                                object_path=path,
                                bus=self.system_bus,
                            )
                        )
                        devfs.properties_changed
                        continue
                    if "org.freedesktop.UDisks2.Partition" in interfaces:
                        print("Driver has partition ")
                        devpart: UDisks2PartitionAsyncInterface = (
                            UDisks2PartitionAsyncInterface.new_proxy(
                                service_name="org.freedesktop.UDisks2",
                                object_path=path,
                                bus=self.system_bus,
                            )
                        )
                        continue

    async def _properties_changed_listener(self) -> None:
        async for (
            path,
            changed_properties,
            invalid_properties,
        ) in self.obj_manager.properties_changed:
            print(path)
            print(changed_properties)
            print(invalid_properties)

    async def _rem_interface_listener(self) -> None:
        async for path, interfaces in self.obj_manager.interfaces_removed:
            if "org.freedesktop.UDisks2.Block" in interfaces:
                os.rmdir("/home/bugo/printer_data/gcodes/USB_PEN")

    def add_symlink(self, path: str, label: str | None) -> None:
        """Create symlink on `path`"""
        if not (os.path.exists(path) or os.path.islink(path)):
            dstb = pathlib.Path(path).joinpath(label if label else "USB DRIVE")
            os.symlink(src="/media/bugo/BLOCKS", dst=dstb)

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


class UDisks2PartitionAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name="org.freedesktop.UDisks2.Partition"
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_method_async(input_signature="s")
    async def set_type(self, type: str) -> None:
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="s")
    async def set_name(self, name: str) -> None:
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="a{sv}")
    async def delete(self, opts: dict) -> None:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="u")
    def number(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def type(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def flags(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def offset(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def size(self) -> int:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def name(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def uuid(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="o")
    def table(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def is_container(self) -> bytes:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def is_contained(self) -> bytes:
        raise NotImplementedError


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
            mnt_dir="/home/bugo/printer_data/gcodes/",
            gcodes_dir="/media/",
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    app.processEvents()
    sys.exit(app.exec())
