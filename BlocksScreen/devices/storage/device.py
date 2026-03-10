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
        symlink_path: str,
    ) -> None:
        self.path: str = path
        self.symlink_path: str = symlink_path
        self.driver_interface: UDisks2DriveAsyncInterface = DriveInterface
        self.partitions: dict[str, UDisks2PartitionAsyncInterface] = {}
        self.raw_block: dict[str, UDisks2BlockAsyncInterface] = {}
        self.logical_blocks: dict[str, UDisks2BlockAsyncInterface] = {}
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = {}
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = {}
        self.symlinks: list[str] = []

    def get_logical_blocks(self) -> dict[str, UDisks2BlockAsyncInterface]:
        """The available logical blocks for the device"""
        return self.logical_blocks

    def get_driver(self) -> UDisks2DriveAsyncInterface | None:
        """Get current device driver"""
        if not self.driver_interface:
            return None
        return self.driver_interface

    def update_file_system(
        self, path: str, data: UDisks2FileSystemAsyncInterface
    ) -> None:
        """Add or update a filesystem for this device

        Args:
            path (str): filesystem path
            data (UDisks2FileSystemAsyncInterface): The interface
        """
        self.file_systems.update({path: data})

    def update_raw_block(self, path: str, block: UDisks2BlockAsyncInterface) -> None:
        """Add or update a raw block for this device

        Args:
            path (str): block path
            data (UDisks2BlockAsyncInterface): The blocks interface
        """
        self.raw_block.update({path: block})

    def update_logical_blocks(
        self, path: str, block: UDisks2BlockAsyncInterface
    ) -> None:
        """Add or update a logical block for this device

        Args:
            path (str): block path
            data (UDisks2BlockAsyncInterface): The block interface
        """
        self.logical_blocks.update({path: block})

    def update_part_table(
        self, path: str, part: UDisks2PartitionTableAsyncInterface
    ) -> None:
        """Add or update partition table for this device

        Args:
            path (str): Partition table path
            part (UDisks2PartitionTableAsyncInterface): The interface
        """
        self.partition_tables.update({path: part})

    def update_partitions(
        self, path: str, block: UDisks2PartitionAsyncInterface
    ) -> None:
        """Add or update partitions for the current device

        Args:
            path (str): the partition path
            data (UDisks2PartitionAsyncInterface): The partition interface
        """
        self.partitions.update({path: block})

    def kill(self) -> None:
        """Delete the device and removes any track of it

        Especially used when devices were removed unsafely
        """
        self.delete()

    def delete(self) -> None:
        """Cleanup and delete this device"""
        del self.driver_interface
        self.partitions.clear()
        self.raw_block.clear()
        self.file_systems.clear()
        self.partition_tables.clear()
        self.symlinks.clear()
