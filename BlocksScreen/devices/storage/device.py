from .udisks2_dbus_async import (
    UDisks2BlockAsyncInterface,
    UDisks2DriveAsyncInterface,
    UDisks2PartitionAsyncInterface,
    UDisks2FileSystemAsyncInterface,
    UDisks2PartitionTableAsyncInterface,
)
import typing
import pathlib

_T = typing.TypeVar(name="_T")


class Device:
    def __init__(
        self,
        path: str,
        DriveInterface: UDisks2DriveAsyncInterface,
        symlink_path: str | pathlib.Path,
    ) -> None:
        self.path: str = path
        self.symlink_path: str = path
        self.driver_interface: UDisks2DriveAsyncInterface = DriveInterface
        self.partitions: dict[str, UDisks2PartitionAsyncInterface] = {}
        self.raw_block: dict[str, UDisks2BlockAsyncInterface] = {}
        self.logical_blocks: dict[str, UDisks2BlockAsyncInterface] = {}
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = {}
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = {}
        self.symlinks: list[str] = []

    def get_logical_blocks(self) -> dict[str, UDisks2BlockAsyncInterface]:
        return self.logical_blocks

    def get_driver(self) -> UDisks2DriveAsyncInterface | None:
        """Get current device driver"""
        if not self.driver_interface:
            return None
        return self.driver_interface

    def update_file_system(
        self, path: str, data: UDisks2FileSystemAsyncInterface
    ) -> None:
        self.file_systems.update({path: data})

    def update_raw_block(self, path: str, block: UDisks2BlockAsyncInterface) -> None:
        self.raw_block.update({path: block})

    def update_logical_blocks(
        self, path: str, block: UDisks2BlockAsyncInterface
    ) -> None:
        self.logical_blocks.update({path: block})

    def update_part_table(
        self, path: str, part: UDisks2PartitionTableAsyncInterface
    ) -> None:
        self.partition_tables.update({path: part})

    def update_partitions(
        self, path: str, block: UDisks2PartitionAsyncInterface
    ) -> None:
        self.partitions.update({path: block})

    def kill(self) -> None:
        """Delete the device and removes any track of it

        Specialy used when devices were removed unsafely
        """
        self.delete()

    def delete(self) -> None:
        del self.driver_interface
        self.partitions.clear()
        self.raw_block.clear()
        self.file_systems.clear()
        self.partition_tables.clear()
