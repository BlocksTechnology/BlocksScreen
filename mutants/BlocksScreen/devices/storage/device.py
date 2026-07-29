from .udisks2_dbus_async import (
    UDisks2BlockAsyncInterface,
    UDisks2DriveAsyncInterface,
    UDisks2PartitionAsyncInterface,
    UDisks2FileSystemAsyncInterface,
    UDisks2PartitionTableAsyncInterface,
)
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


class Device:
    def __init__(
        self,
        path: str,
        DriveInterface: UDisks2DriveAsyncInterface,
        symlink_path: str,
    ) -> None:
        args = [path, DriveInterface, symlink_path]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁDeviceǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁDeviceǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁDeviceǁ__init____mutmut_orig(
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
    def xǁDeviceǁ__init____mutmut_1(
        self,
        path: str,
        DriveInterface: UDisks2DriveAsyncInterface,
        symlink_path: str,
    ) -> None:
        self.path: str = None
        self.symlink_path: str = symlink_path
        self.driver_interface: UDisks2DriveAsyncInterface = DriveInterface
        self.partitions: dict[str, UDisks2PartitionAsyncInterface] = {}
        self.raw_block: dict[str, UDisks2BlockAsyncInterface] = {}
        self.logical_blocks: dict[str, UDisks2BlockAsyncInterface] = {}
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = {}
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = {}
        self.symlinks: list[str] = []
    def xǁDeviceǁ__init____mutmut_2(
        self,
        path: str,
        DriveInterface: UDisks2DriveAsyncInterface,
        symlink_path: str,
    ) -> None:
        self.path: str = path
        self.symlink_path: str = None
        self.driver_interface: UDisks2DriveAsyncInterface = DriveInterface
        self.partitions: dict[str, UDisks2PartitionAsyncInterface] = {}
        self.raw_block: dict[str, UDisks2BlockAsyncInterface] = {}
        self.logical_blocks: dict[str, UDisks2BlockAsyncInterface] = {}
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = {}
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = {}
        self.symlinks: list[str] = []
    def xǁDeviceǁ__init____mutmut_3(
        self,
        path: str,
        DriveInterface: UDisks2DriveAsyncInterface,
        symlink_path: str,
    ) -> None:
        self.path: str = path
        self.symlink_path: str = symlink_path
        self.driver_interface: UDisks2DriveAsyncInterface = None
        self.partitions: dict[str, UDisks2PartitionAsyncInterface] = {}
        self.raw_block: dict[str, UDisks2BlockAsyncInterface] = {}
        self.logical_blocks: dict[str, UDisks2BlockAsyncInterface] = {}
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = {}
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = {}
        self.symlinks: list[str] = []
    def xǁDeviceǁ__init____mutmut_4(
        self,
        path: str,
        DriveInterface: UDisks2DriveAsyncInterface,
        symlink_path: str,
    ) -> None:
        self.path: str = path
        self.symlink_path: str = symlink_path
        self.driver_interface: UDisks2DriveAsyncInterface = DriveInterface
        self.partitions: dict[str, UDisks2PartitionAsyncInterface] = None
        self.raw_block: dict[str, UDisks2BlockAsyncInterface] = {}
        self.logical_blocks: dict[str, UDisks2BlockAsyncInterface] = {}
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = {}
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = {}
        self.symlinks: list[str] = []
    def xǁDeviceǁ__init____mutmut_5(
        self,
        path: str,
        DriveInterface: UDisks2DriveAsyncInterface,
        symlink_path: str,
    ) -> None:
        self.path: str = path
        self.symlink_path: str = symlink_path
        self.driver_interface: UDisks2DriveAsyncInterface = DriveInterface
        self.partitions: dict[str, UDisks2PartitionAsyncInterface] = {}
        self.raw_block: dict[str, UDisks2BlockAsyncInterface] = None
        self.logical_blocks: dict[str, UDisks2BlockAsyncInterface] = {}
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = {}
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = {}
        self.symlinks: list[str] = []
    def xǁDeviceǁ__init____mutmut_6(
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
        self.logical_blocks: dict[str, UDisks2BlockAsyncInterface] = None
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = {}
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = {}
        self.symlinks: list[str] = []
    def xǁDeviceǁ__init____mutmut_7(
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
        self.file_systems: dict[str, UDisks2FileSystemAsyncInterface] = None
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = {}
        self.symlinks: list[str] = []
    def xǁDeviceǁ__init____mutmut_8(
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
        self.partition_tables: dict[str, UDisks2PartitionTableAsyncInterface] = None
        self.symlinks: list[str] = []
    def xǁDeviceǁ__init____mutmut_9(
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
        self.symlinks: list[str] = None
    
    xǁDeviceǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁDeviceǁ__init____mutmut_1': xǁDeviceǁ__init____mutmut_1, 
        'xǁDeviceǁ__init____mutmut_2': xǁDeviceǁ__init____mutmut_2, 
        'xǁDeviceǁ__init____mutmut_3': xǁDeviceǁ__init____mutmut_3, 
        'xǁDeviceǁ__init____mutmut_4': xǁDeviceǁ__init____mutmut_4, 
        'xǁDeviceǁ__init____mutmut_5': xǁDeviceǁ__init____mutmut_5, 
        'xǁDeviceǁ__init____mutmut_6': xǁDeviceǁ__init____mutmut_6, 
        'xǁDeviceǁ__init____mutmut_7': xǁDeviceǁ__init____mutmut_7, 
        'xǁDeviceǁ__init____mutmut_8': xǁDeviceǁ__init____mutmut_8, 
        'xǁDeviceǁ__init____mutmut_9': xǁDeviceǁ__init____mutmut_9
    }
    xǁDeviceǁ__init____mutmut_orig.__name__ = 'xǁDeviceǁ__init__'

    def get_logical_blocks(self) -> dict[str, UDisks2BlockAsyncInterface]:
        """The available logical blocks for the device"""
        return self.logical_blocks

    def get_driver(self) -> UDisks2DriveAsyncInterface | None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁDeviceǁget_driver__mutmut_orig'), object.__getattribute__(self, 'xǁDeviceǁget_driver__mutmut_mutants'), args, kwargs, self)

    def xǁDeviceǁget_driver__mutmut_orig(self) -> UDisks2DriveAsyncInterface | None:
        """Get current device driver"""
        if not self.driver_interface:
            return None
        return self.driver_interface

    def xǁDeviceǁget_driver__mutmut_1(self) -> UDisks2DriveAsyncInterface | None:
        """Get current device driver"""
        if self.driver_interface:
            return None
        return self.driver_interface
    
    xǁDeviceǁget_driver__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁDeviceǁget_driver__mutmut_1': xǁDeviceǁget_driver__mutmut_1
    }
    xǁDeviceǁget_driver__mutmut_orig.__name__ = 'xǁDeviceǁget_driver'

    def update_file_system(
        self, path: str, data: UDisks2FileSystemAsyncInterface
    ) -> None:
        args = [path, data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁDeviceǁupdate_file_system__mutmut_orig'), object.__getattribute__(self, 'xǁDeviceǁupdate_file_system__mutmut_mutants'), args, kwargs, self)

    def xǁDeviceǁupdate_file_system__mutmut_orig(
        self, path: str, data: UDisks2FileSystemAsyncInterface
    ) -> None:
        """Add or update a filesystem for this device

        Args:
            path (str): filesystem path
            data (UDisks2FileSystemAsyncInterface): The interface
        """
        self.file_systems.update({path: data})

    def xǁDeviceǁupdate_file_system__mutmut_1(
        self, path: str, data: UDisks2FileSystemAsyncInterface
    ) -> None:
        """Add or update a filesystem for this device

        Args:
            path (str): filesystem path
            data (UDisks2FileSystemAsyncInterface): The interface
        """
        self.file_systems.update(None)
    
    xǁDeviceǁupdate_file_system__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁDeviceǁupdate_file_system__mutmut_1': xǁDeviceǁupdate_file_system__mutmut_1
    }
    xǁDeviceǁupdate_file_system__mutmut_orig.__name__ = 'xǁDeviceǁupdate_file_system'

    def update_raw_block(self, path: str, block: UDisks2BlockAsyncInterface) -> None:
        args = [path, block]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁDeviceǁupdate_raw_block__mutmut_orig'), object.__getattribute__(self, 'xǁDeviceǁupdate_raw_block__mutmut_mutants'), args, kwargs, self)

    def xǁDeviceǁupdate_raw_block__mutmut_orig(self, path: str, block: UDisks2BlockAsyncInterface) -> None:
        """Add or update a raw block for this device

        Args:
            path (str): block path
            data (UDisks2BlockAsyncInterface): The blocks interface
        """
        self.raw_block.update({path: block})

    def xǁDeviceǁupdate_raw_block__mutmut_1(self, path: str, block: UDisks2BlockAsyncInterface) -> None:
        """Add or update a raw block for this device

        Args:
            path (str): block path
            data (UDisks2BlockAsyncInterface): The blocks interface
        """
        self.raw_block.update(None)
    
    xǁDeviceǁupdate_raw_block__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁDeviceǁupdate_raw_block__mutmut_1': xǁDeviceǁupdate_raw_block__mutmut_1
    }
    xǁDeviceǁupdate_raw_block__mutmut_orig.__name__ = 'xǁDeviceǁupdate_raw_block'

    def update_logical_blocks(
        self, path: str, block: UDisks2BlockAsyncInterface
    ) -> None:
        args = [path, block]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁDeviceǁupdate_logical_blocks__mutmut_orig'), object.__getattribute__(self, 'xǁDeviceǁupdate_logical_blocks__mutmut_mutants'), args, kwargs, self)

    def xǁDeviceǁupdate_logical_blocks__mutmut_orig(
        self, path: str, block: UDisks2BlockAsyncInterface
    ) -> None:
        """Add or update a logical block for this device

        Args:
            path (str): block path
            data (UDisks2BlockAsyncInterface): The block interface
        """
        self.logical_blocks.update({path: block})

    def xǁDeviceǁupdate_logical_blocks__mutmut_1(
        self, path: str, block: UDisks2BlockAsyncInterface
    ) -> None:
        """Add or update a logical block for this device

        Args:
            path (str): block path
            data (UDisks2BlockAsyncInterface): The block interface
        """
        self.logical_blocks.update(None)
    
    xǁDeviceǁupdate_logical_blocks__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁDeviceǁupdate_logical_blocks__mutmut_1': xǁDeviceǁupdate_logical_blocks__mutmut_1
    }
    xǁDeviceǁupdate_logical_blocks__mutmut_orig.__name__ = 'xǁDeviceǁupdate_logical_blocks'

    def update_part_table(
        self, path: str, part: UDisks2PartitionTableAsyncInterface
    ) -> None:
        args = [path, part]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁDeviceǁupdate_part_table__mutmut_orig'), object.__getattribute__(self, 'xǁDeviceǁupdate_part_table__mutmut_mutants'), args, kwargs, self)

    def xǁDeviceǁupdate_part_table__mutmut_orig(
        self, path: str, part: UDisks2PartitionTableAsyncInterface
    ) -> None:
        """Add or update partition table for this device

        Args:
            path (str): Partition table path
            part (UDisks2PartitionTableAsyncInterface): The interface
        """
        self.partition_tables.update({path: part})

    def xǁDeviceǁupdate_part_table__mutmut_1(
        self, path: str, part: UDisks2PartitionTableAsyncInterface
    ) -> None:
        """Add or update partition table for this device

        Args:
            path (str): Partition table path
            part (UDisks2PartitionTableAsyncInterface): The interface
        """
        self.partition_tables.update(None)
    
    xǁDeviceǁupdate_part_table__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁDeviceǁupdate_part_table__mutmut_1': xǁDeviceǁupdate_part_table__mutmut_1
    }
    xǁDeviceǁupdate_part_table__mutmut_orig.__name__ = 'xǁDeviceǁupdate_part_table'

    def update_partitions(
        self, path: str, block: UDisks2PartitionAsyncInterface
    ) -> None:
        args = [path, block]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁDeviceǁupdate_partitions__mutmut_orig'), object.__getattribute__(self, 'xǁDeviceǁupdate_partitions__mutmut_mutants'), args, kwargs, self)

    def xǁDeviceǁupdate_partitions__mutmut_orig(
        self, path: str, block: UDisks2PartitionAsyncInterface
    ) -> None:
        """Add or update partitions for the current device

        Args:
            path (str): the partition path
            data (UDisks2PartitionAsyncInterface): The partition interface
        """
        self.partitions.update({path: block})

    def xǁDeviceǁupdate_partitions__mutmut_1(
        self, path: str, block: UDisks2PartitionAsyncInterface
    ) -> None:
        """Add or update partitions for the current device

        Args:
            path (str): the partition path
            data (UDisks2PartitionAsyncInterface): The partition interface
        """
        self.partitions.update(None)
    
    xǁDeviceǁupdate_partitions__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁDeviceǁupdate_partitions__mutmut_1': xǁDeviceǁupdate_partitions__mutmut_1
    }
    xǁDeviceǁupdate_partitions__mutmut_orig.__name__ = 'xǁDeviceǁupdate_partitions'

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
