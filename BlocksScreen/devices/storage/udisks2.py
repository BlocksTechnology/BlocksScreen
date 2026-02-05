from PyQt6 import QtCore
import sdbus

from .udisks2_dbus_async import (
    UDisks2BlockAsyncInterface,
    UDisks2DriveAsyncInterface,
    UDisks2AsyncManager,
    UDisks2PartitionAsyncInterface,
    UDisks2FileSystemAsyncInterface,
    Interfaces,
)
import typing
import asyncio
import pathlib
import logging
import os

UDisks2_service: str = "org.freedesktop.UDisks2"
UDisks2_obj_path: str = "org/freedesktop/UDisks2"


class Device:
    def __init__(self, path: str, DriveInterface: UDisks2DriveAsyncInterface) -> None:
        self.path: str = path
        self.driver_interface: UDisks2DriveAsyncInterface = DriveInterface
        self.partitions: dict[str, UDisks2BlockAsyncInterface] = {}
        self.raw_block: dict[str, UDisks2BlockAsyncInterface] = {}
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = {}
        self.partition_tables: dict[str, UDisks2FileSystemAsyncInterface] = {}

    def update_raw_block(self, path: str, data: UDisks2BlockAsyncInterface) -> None:
        self.raw_block.update({path: data})

    def update_file_system(
        self, path: str, data: UDisks2FileSystemAsyncInterface
    ) -> None:
        self.file_systems.update({path: data})

    def update_paritions(self, path: str, data: UDisks2PartitionAsyncInterface) -> None:
        self.partitions.update({path: data})

    def get_logical_blocks(self) -> dict[str, UDisks2BlockAsyncInterface]:
        return self.partitions

    def get_driver(self) -> UDisks2DriveAsyncInterface | None:
        """Get current device driver"""
        if not self.driver_interface:
            return None
        return self.driver_interface

    def delete(self) -> None:
        del self.driver_interface
        for key in self.partitions.keys():
            block: UDisks2BlockAsyncInterface = self.partitions.pop(key)
            del block
        for key in self.raw_block.keys():
            raw_block: UDisks2BlockAsyncInterface = self.raw_block.pop(key)
            del raw_block
        for key in self.file_systems.keys():
            file_system: UDisks2FileSystemAsyncInterface = self.file_systems.pop(key)
            del file_system
        for key in self.partition_tables.keys():
            part_table: UDisks2PartitionAsyncInterface = self.partition_tables.pop(key)
            del part_table


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
            service_name=UDisks2_service,
            object_path=UDisks2_obj_path,
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
        try:
            if not self.loop:
                return
            if self.loop.is_running():
                self.stop_event.set()
                self.loop.call_soon_threadsafe(self.loop.stop)
            self.quit()
            _ = self.wait()
            self.deleteLater()
            for path in self.controlled_devs.keys():
                dev: Device = self.controlled_devs.pop(path)
                dev.delete()
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
        # self.task_stack.add(add_listener)
        # self.task_stack.add(rem_listener)
        # self.task_stack.add(pchange_listener)
        while self.stop_event:
            try:
                response = await asyncio.gather(
                    add_listener, rem_listener, pchange_listener
                )
                if response:
                    for result in response:
                        if isinstance(result, Exception):
                            logging.error("Caught exception on asyncio loop")
                # add_listener.add_done_callback(
                #     lambda _: self.task_stack.discard(add_listener)
                # )
                # rem_listener.add_done_callback(
                #     lambda _: self.task_stack.discard(rem_listener)
                # )
                # pchange_listener.add_done_callback(
                #     lambda _: self.task_stack.discard(pchange_listener)
                # )
            except asyncio.CancelledError as e:
                _ = add_listener.cancel()
                _ = rem_listener.cancel()
                _ = pchange_listener.cancel()
                logging.error(
                    "Caught exception while starting UDisks2 interfaces listeners: %s",
                    e,
                )

    async def _add_interface_listener(self) -> None:
        """Add interface signal handler

        Adds the new device to internal traking, can be retrieved with device path
        Creates symlink onto specified directory configured on the class

        """
        async for path, interfaces in self.obj_manager.interfaces_added:
            if Interfaces["Drive"] in interfaces:
                ddev: UDisks2DriveAsyncInterface = UDisks2DriveAsyncInterface.new_proxy(
                    service_name=UDisks2_service,
                    object_path=path,
                    bus=self.system_bus,
                )
                logging.info(
                    "New Hardware device recognized type: %s \n  path: %s",
                    await ddev.connection_bus,
                    path,
                )
                device: Device = Device(path, ddev)
                self.controlled_devs.update({path: device})
            if Interfaces["Block"] in interfaces:
                bdev: UDisks2BlockAsyncInterface = UDisks2BlockAsyncInterface.new_proxy(
                    service_name=UDisks2_service,
                    object_path=path,
                    bus=self.system_bus,
                )
                drv_path: str = await bdev.drive
                hint_sys, hint_ignore = await asyncio.gather(
                    bdev.hint_system, bdev.hint_ignore
                )
                if hint_sys or hint_ignore:
                    continue  # Always ignore if these flags are set to true
                if drv_path in self.controlled_devs:
                    logging.info("Recognized Block for device %s", path)
                    device: Device = self.controlled_devs[drv_path]
                    if "org.freedesktop.UDisks2.PartitionTable" in interfaces:
                        device.update_raw_block(path, bdev)
                        continue
                    if Interfaces["Filesystem"] in interfaces:
                        devfs: UDisks2FileSystemAsyncInterface = (
                            UDisks2FileSystemAsyncInterface.new_proxy(
                                service_name=UDisks2_service,
                                object_path=path,
                                bus=self.system_bus,
                            )
                        )
                        device.update_file_system(path, devfs)
                    if Interfaces["Partition"] in interfaces:
                        devpart: UDisks2PartitionAsyncInterface = (
                            UDisks2PartitionAsyncInterface.new_proxy(
                                service_name=UDisks2_service,
                                object_path=path,
                                bus=self.system_bus,
                            )
                        )
                        device.update_partitions(path, devpart)

    async def _properties_changed_listener(self) -> None:
        """Properties changed signal handling

        Updates tracked objects
        """
        async for (
            path,
            changed_properties,
            invalid_properties,
        ) in self.obj_manager.properties_changed:
            print("PROPERTIES CHANGED HERE ")
            print(path)
            print(changed_properties)
            print(invalid_properties)

    async def _rem_interface_listener(self) -> None:
        """Removed interfaces signal

        Removes tracked interface and cleansup any left behing data
        """
        async for path, interfaces in self.obj_manager.interfaces_removed:
            if INTERFACES["Block"] in interfaces:
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
