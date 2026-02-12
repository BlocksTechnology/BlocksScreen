import asyncio
import logging
import os
import pathlib
import typing
from collections.abc import Coroutine
import unicodedata

import sdbus
from PyQt6 import QtCore

from .device import Device
from .udisks2_dbus_async import (
    Interfaces,
    UDisks2AsyncManager,
    UDisks2BlockAsyncInterface,
    UDisks2DriveAsyncInterface,
    UDisks2FileSystemAsyncInterface,
    UDisks2PartitionAsyncInterface,
    UDisks2PartitionTableAsyncInterface,
)

UDisks2_service: str = "org.freedesktop.UDisks2"
UDisks2_obj_path: str = "org/freedesktop/UDisks2"
USER_HOME_DIR: str = os.path.expanduser("~")

AlreadyMountedException = "org.freedesktop.UDisks2.Error.AlreadyMounted"

_T = typing.TypeVar(name="_T")


def validate_label(label: str, strict: bool = True, max_length: int = 100) -> str:
    """
    Comprehensive validation for filesystem labels with security protection.

    Args:
        label: Raw input label to validate
        strict: If True, returns empty string for any invalid input
        max_length: Maximum allowed length in bytes
        allow_unicode: If False, converts to ASCII only

    Returns:
        Sanitized and validated label safe for filesystem use
    """
    if not label:
        return ""
    if not label.strip():
        return ""
    if len(label.encode("utf-8")) > max_length:
        return "" if strict else label[:max_length]
    normalized_label = unicodedata.normalize("NFC", label)
    if any(ord(char) < 32 for char in normalized_label):
        if strict:
            return ""
        normalized_label = "".join(char for char in normalized_label if ord(char) >= 32)

    dangerous_chars = {
        "\0",
        "/",
        "\\",
        ";",
        "|",
        "&",
        "$",
        "`",
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        "<",
        ">",
        '"',
        "'",
        "*",
        "?",
        "!",
    }
    clean_label = "".join(c for c in normalized_label if c not in dangerous_chars)
    if (
        ".." in clean_label
        or clean_label.startswith("/")
        or clean_label.startswith("\\")
    ):
        return (
            ""
            if strict
            else clean_label.replace("..", "").replace("/", "_").replace("\\", "_")
        )

    final_label = clean_label.strip(" .")[:max_length]
    return final_label if final_label else ""


def fire_n_forget(
    coro: Coroutine[typing.Any, typing.Any, typing.Any],
    name: str,
    task_stack: set[asyncio.Task[typing.Any]],
) -> asyncio.Task[typing.Any]:
    task: asyncio.Task[typing.Any] = asyncio.create_task(coro, name=name)
    task_stack.add(task)

    def cleanup(task: asyncio.Task[_T]) -> None:
        task_stack.discard(task)
        try:
            task.result()
        except asyncio.CancelledError:
            task.cancel()
            logging.error("Task %s was cancelled", task.get_name())
        except Exception as e:
            logging.error(
                "Caught exception in %s : %s", task.get_name(), e, exc_info=True
            )

    task.add_done_callback(cleanup)
    return task


class UDisksDBusAsync(QtCore.QThread):
    hardware_detected: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="hardware-detected"
    )
    device_added: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, dict, name="device-added"
    )
    device_removed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="device-removed"
    )  # device path
    hardware_removed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="hardware-removed"
    )  # device path
    device_mounted: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="device-mounted"
    )  # device path, new symlink path

    def __init__(self, parent: QtCore.QObject, gcodes_dir: str) -> None:
        super().__init__(parent)
        self.task_stack: set[asyncio.Task[typing.Any]] = set()
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
        self._cleanup_broken_symlinks()

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
        """Schedule coroutines for UDisks2 signals `interfaces_added`, `interfaces_removed`
        and `properties_changed`. Creates symlink upon device insertion and cleans up symlink on removal.

        """
        tasks: dict[str, Coroutine[typing.Any, typing.Any, typing.Any]] = {
            "add": self._add_interface_listener(),
            "rem": self._rem_interface_listener(),
            "prop": self._properties_changed_listener(),
        }
        _ = fire_n_forget(
            coro=self.restore_tracked(),
            name="Main-Restore-Discovery",
            task_stack=self.task_stack,
        )
        managed_tasks: list[asyncio.Task[typing.Any]] = []
        for name, coro in tasks.items():
            t = asyncio.create_task(coro, name=name)
            self.task_stack.add(t)
            t.add_done_callback(lambda _: self.task_stack.discard(t))
            managed_tasks.append(t)
        try:
            await asyncio.gather(*managed_tasks)
        except asyncio.CancelledError as e:
            for task in self.task_stack:
                _ = task.cancel()
            logging.info("UDisks2 Monitor stopped: %s", e)
        except Exception as e:
            logging.error("Caught exception UDisks2 listeners failed: %s", e)

    async def restore_tracked(self) -> None:
        """Get and restore controlled mass storage devices"""
        info = await self.obj_manager.get_managed_objects()
        for path, interfaces in info.items():
            fire_n_forget(
                coro=self._handle_new_device(path, interfaces),
                name=f"Restore-Discovery-{path}",
                task_stack=self.task_stack,
            )

    async def _add_interface_listener(self) -> None:
        """Handle add interface signal from UDisks2 DBus connection

        Adds the new device to internal traking, can be retrieved with device path
        Creates symlink onto specified directory configured on the class
        """
        async for path, interfaces in self.obj_manager.interfaces_added:
            fire_n_forget(
                self._handle_new_device(path, interfaces),
                name=f"UDisks-Discovery-{path}",
                task_stack=self.task_stack,
            )

    async def _handle_new_device(self, path: str, interfaces) -> None:
        """Handle new devices, can be used on `interfaces_added` signal and
        when recovering states from `get_managed_objects`

        """
        try:
            if Interfaces.Drive.value in interfaces:
                ddev: UDisks2DriveAsyncInterface = UDisks2DriveAsyncInterface.new_proxy(
                    service_name=UDisks2_service,
                    object_path=path,
                    bus=self.system_bus,
                )
                hwbus: str = await ddev.connection_bus
                logging.info(
                    "New Hardware device recognized type: %s \n  path: %s",
                    hwbus,
                    path,
                )
                media_removable, ejectable, con_bus = await asyncio.gather(
                    ddev.media_removable, ddev.ejectable, ddev.connection_bus
                )
                if not (media_removable and ejectable and con_bus == "usb"):
                    # Only handle usb devices and remoble storage media
                    return
                device: Device = Device(
                    path, DriveInterface=ddev, symlink_path=self.gcodes_path
                )
                self.controlled_devs.update({path: device})
                self.hardware_detected[str].emit(path)
            if Interfaces.Block.value in interfaces:
                # NOTE: Here lies the Phase II and PhaseIII,
                # Phase II -> dict[Block, PartitionTable] -> This tells me the size of the drive
                # PhaseIII -> dict[Block, Partition, Filesystem] -> This i can mount and see the files
                # We can see that the Block interface alwasy comes in these phases, so junst instantiate once
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
                    # Always ignore if these flags are set
                    return
                if (
                    drv_path in self.controlled_devs
                ):  # Only continue if there is a drive on that block which is managed by us
                    dev: Device = self.controlled_devs[drv_path]
                    if all(
                        phase in interfaces
                        for phase in (
                            Interfaces.PartitionTable.value,
                            Interfaces.Block.value,
                        )
                    ):
                        # NOTE: This is specifically Phase II, parent  physical drive
                        devpt: UDisks2PartitionTableAsyncInterface = (
                            UDisks2PartitionTableAsyncInterface.new_proxy(
                                service_name=UDisks2_service,
                                object_path=path,
                                bus=self.system_bus,
                            )
                        )
                        dev.update_raw_block(path, bdev)
                        dev.update_part_table(path, devpt)
                    if Interfaces.Filesystem.value in interfaces:
                        # This is a child, try and mount.
                        devfs: UDisks2FileSystemAsyncInterface = (
                            UDisks2FileSystemAsyncInterface.new_proxy(
                                service_name=UDisks2_service,
                                object_path=path,
                                bus=self.system_bus,
                            )
                        )
                        dev.update_file_system(path, devfs)
                        self.device_added.emit(path, interfaces)
                        # dev.mount()
                        self.mount(dev)
                    if Interfaces.Partition.value in interfaces:
                        # NOTE: This is specifically PhaseIII
                        devpart: UDisks2PartitionAsyncInterface = (
                            UDisks2PartitionAsyncInterface.new_proxy(
                                service_name=UDisks2_service,
                                object_path=path,
                                bus=self.system_bus,
                            )
                        )
                        dev.update_partitions(path, devpart)
                    dev.update_logical_blocks(path, bdev)
        except sdbus.dbus_exceptions.DbusUnknownMethodError as e:
            logging.error(
                "Caught exception on device inserted unknown method: %s",
                e,
                exc_info=True,
            )
        except sdbus.dbus_exceptions.DbusUnknownInterfaceError as e:
            logging.error(
                "Caught exception on device inserted unknown interface: %s",
                e,
                exc_info=True,
            )
        except Exception as e:
            logging.error(
                "Caught fatal exception during discovery process %s: %s",
                path,
                e,
                exc_info=True,
            )

    async def _properties_changed_listener(self) -> None:
        """Handle properties_changed signal from UDisks2 Dbus connection

        Updates tracked objects
        """
        print("Some properties changed in here")
        async for (
            path,
            changed_properties,
            invalid_properties,
        ) in self.obj_manager.properties_changed:
            pass

    async def _rem_interface_listener(self) -> None:
        """Handle device removal signals from UDisks2 Dbus connection

        Removes tracked interface and cleansup any left behing data
        """
        async for path, interfaces in self.obj_manager.interfaces_removed:
            try:
                if Interfaces.Drive.value in interfaces:
                    if path in self.controlled_devs:
                        print("hardware_removed")
                        device: Device = self.controlled_devs.pop(path)
                        device.kill()
                        # self._cleanup_symlinks()
                        del device
                        self.hardware_removed[str].emit(path)
            except sdbus.dbus_exceptions.DbusUnknownMethodError as e:
                logging.error(
                    "Caught exception on device removed unknown method: %s",
                    e,
                    exc_info=True,
                )
            except sdbus.dbus_exceptions.DbusUnknownInterfaceError as e:
                logging.error(
                    "Caught exception on device removed unknown interface %s",
                    e,
                    exc_info=True,
                )
            except Exception as e:
                logging.error(
                    "Caught fatal exception on removed device: %s, %s",
                    path,
                    e,
                    exc_info=True,
                )

    def mount(self, device: Device):
        """Mounts the devices mountpoints"""
        # fileqt: int = device.get_mountable()
        # filesys: list[UDisks2FileSystemAsyncInterface] = device.get_filesystems()
        for path, filesystem in device.file_systems.items():
            clean_path = str(path).strip("\x00")
            task = fire_n_forget(
                coro=self._mount_filesystem(filesystem),
                name=f"Mount-filesystem-{clean_path}",
                task_stack=self.task_stack,
            )

    def _finish_mount(self, task) -> None:
        self.task_stack.discard(task)
        task.result()

    async def _mount_filesystem(
        self, filesystem: UDisks2FileSystemAsyncInterface, label: str = ""
    ) -> str:
        validated_label = validate_label(label)
        try:
            opts: dict[str, tuple[str, typing.Any]] = {
                "auto.no_user_interactions": ("b", True),
                "fstype": ("s", "auto"),
                "as-user": ("s", os.environ.get("USER")),
                "options": ("s", "rw,relatime,sync"),
            }
            mnt_path: str = await filesystem.mount(opts)
            symres: str = self.add_symlink(
                path=mnt_path,
                label=validated_label,
                dst_path=self.gcodes_path.as_posix(),
            )
            return symres if mnt_path and symres else ""
        except sdbus.SdBusUnmappedMessageError as e:
            if AlreadyMountedException in e.args[0]:
                logging.info(
                    "Device filesystem already mounted on %s, verifying gcodes symlink",
                    str(e.args[1]),
                )
                print("Device already mounted !!!!!")
                mount_points: list[bytes] = await filesystem.mount_points
                if not mount_points:
                    return ""
                print(mount_points[0].decode("utf-8"))
                return self.add_symlink(
                    path=str(mount_points[0].decode("utf-8")),
                    dst_path=self.gcodes_path.as_posix(),
                    label=validated_label,
                )
        except Exception as e:
            logging.error(
                "Caught exception while mounting file system %s : %s",
                filesystem,
                e,
                exc_info=True,
            )
        return ""

    def add_symlink(
        self,
        path: str,
        dst_path: str,
        label: str = "",
        _index: int = 0,
        _validated: bool = False,
    ) -> str:
        """Create symlink on `dst_path`

        If there is a symlink created on `dst_path` with the same label,
        which points to the same `path` then it will return the `dst_path`
        as validation. If `dst_path` does not resolve to the same `path`
        then it will cleanup that symlink and create a replacement.

        In case there is no `label` then the created `symlink` on `dst_path`
        will default to **USB DRIVE**. If *USB DRIVE* symlink already exists
        then it will create a variant of that fallback **USB DRIVE [1-254]**
        """
        print("ON ADD SYMLINK")
        if not _validated and label:
            label = validate_label(label, strict=True)
        fallback: str = "USB DRIVE" if _index == 0 else str(f"USB DRIVE {_index}")
        dstb = pathlib.Path(dst_path).joinpath(label if label else fallback)
        try:
            # NOTE: Check if there is any symlink pointing to the same directory i want

            self.gcodes_path.rglob("*")
            thereis = any(
                filter(
                    lambda _: dstb.resolve().as_posix() == path,
                    self.gcodes_path.rglob("*"),
                )
            )
            for dir in self.gcodes_path.rglob("*"):
                print(dir)
            if not (os.path.exists(dstb) or os.path.islink(dstb)):
                os.symlink(src=path, dst=dstb.resolve())
                return dstb.as_posix() if os.path.exists(dstb) else ""
            if os.path.exists(dstb) and os.path.islink(dstb):
                if dstb.resolve().as_posix() == pathlib.Path(path).as_posix():
                    return dstb.as_posix()
                if not label:
                    _index += 1
                    if _index == 255:
                        return ""
                    return self.add_symlink(
                        path, dst_path, label, _index, _validated=True
                    )
                if self.rem_symlink(path=dstb.as_posix()):
                    return self.add_symlink(path, dst_path, label, _validated=True)
        except PermissionError:
            logging.error(
                "Caught fatal exception no permissions, unable to create symlink on specified path"
            )
        except OSError as e:
            logging.error("Caught fatal exception %s", e)
        return ""

    def rem_symlink(self, path: str | pathlib.Path) -> bool:
        """Remove `ONLY` symlinks located in `path` if it is allowed"""
        print("ON REMOVE SYMLINK")
        resolved_path = pathlib.Path(path).resolve()
        print(resolved_path)
        resolved_gcodes_path = pathlib.Path(self.gcodes_path).as_posix()
        print(resolved_gcodes_path)
        try:
            _ = resolved_path.relative_to(resolved_gcodes_path)
        except ValueError:
            logging.error("Path transversal attempt in rem_symlink: %s", path)
            return False

        if not os.path.islink(resolved_path):
            logging.error("Provided path %s is NOT a symlink, refusing to delete", path)
            return False
        try:
            os.remove(resolved_path)
            return True
        except (PermissionError, OSError):
            logging.error("Caught fatal exception failed to remove symlink %s", path)
        return False

    def _cleanup_symlinks(self) -> None:
        """Cleanup all symlinks on gcodes directory

        This method is private, if used outside of it's intended purpose
        devices will lose track of what symlinks are assiciated with them

        USE WITH CARE
        """
        for dir in self.gcodes_path.rglob("*"):
            if os.path.islink(dir):
                _ = self.rem_symlink(dir.as_posix())

    def _cleanup_broken_symlinks(self) -> None:
        for dir in self.gcodes_path.rglob("*"):
            if os.path.islink(dir) and not os.path.exists(dir):
                _ = self.rem_symlink(dir)
