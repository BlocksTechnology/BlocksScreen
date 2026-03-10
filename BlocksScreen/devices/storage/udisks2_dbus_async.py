# Sdbus Udisks2 Interface classes and manager
#
# Contains interface classes for async and blocking api of sdbus
#
#
# Hugo Costa hugo.santos.costa@gmail.com
import sdbus
import enum
import typing


class Interfaces(enum.Enum):
    Filesystem = "org.freedesktop.UDisks2.Filesystem"
    Drive = "org.freedesktop.UDisks2.Drive"
    Partition = "org.freedesktop.UDisks2.Partition"
    Block = "org.freedesktop.UDisks2.Block"
    PartitionTable = "org.freedesktop.UDisks2.PartitionTable"

    @classmethod
    def has_value(cls, value) -> bool:
        return value in (item.value for item in cls)


class UDisks2AsyncManager(sdbus.DbusObjectManagerInterfaceAsync):
    """Subclassed async dbus object manager"""

    def __init__(self) -> None:
        super().__init__()


class UDisks2PartitionTableAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name=Interfaces.PartitionTable.value
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_property_async(property_signature="ao")
    def partitions(self) -> list[str]:
        """Get list of object paths of the `org.freedesktop.Udisks2.Partitions`

        Returns:
            list[str]: list of object paths
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def type(self) -> str:
        """Get the type of partition table detected

        If blank the partition table was detected but it's unknown
        Returns:
            str: Known values ['dos', 'gpt', '']

        """
        raise NotImplementedError


class UDisks2PartitionAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name=Interfaces.Partition.value
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_method_async(input_signature="s")
    async def set_type(self, type: str) -> None:
        """Set new partition type

        Args:
            type (str): New partition type
        """
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="s")
    async def set_name(self, name: str) -> None:
        """Set partition name

        Args:
            name (str): new partition name
        """
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="a{sv}")
    async def delete(self, opts: dict[str, typing.Any]) -> None:
        """Deletes the partition

        Args:
            options (dict[str, any])
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="u")
    def number(self) -> int:
        """Number of the partition on the partition table

        Returns:
            number (int): partition number
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def type(self) -> str:
        """Partition type

        Returns:
            type (str): The partition type. For `dos` partition
            tables this string is a hexadecimal code (0x83, 0xfd).
            For `gpt` partition tables this is the UUID"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def flags(self) -> int:
        """Flags describing the partition.
        ---------------
        For `dos` partitions:
            - Bit 7 - The partition is marked as bootable
        ---------------
        For `gpt` partitions :
            - Bit 0 - System Partition
            - Bit 2 - Legacy BIOS bootable
            - Bit 60 - Read-only
            - Bit 62 - Hidden
            - Bit 63 - Do not automount


        Returns:
            flags (int): current flags
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def offset(self) -> int:
        """Offset of the partition in bytes

        Returns:
            Offset (int): partition offset
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def size(self) -> int:
        """Partition size, in bytes

        Returns:
            Size (int): partition size
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def name(self) -> str:
        """Partition name
        Returns:
            name (str): partition name
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def uuid(self) -> str:
        """Partition UUID
        Returns:
            uuid (str): partition uuid
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="o")
    def table(self) -> str:
        """Object path of the `org.freedesktop.Udisks2.PartitionTable` object that
        the partition belongs to.

        Returns:
            table (str): path
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def is_container(self) -> bool:
        """Set to True if the partition itself is acontainer for other partitions

        For example, for dos partition tables, this applies to socalled extended
        partition (partitions of type 0x05, 0x0f or 0x85) containing socalled logical partitions.


        Returns:
            is_container (bool): if it is a container
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def is_contained(self) -> bytes:
        """Set to True if the partition is contained in another partition
        Returns:
            is_contained (bool): if it's contained
        """
        raise NotImplementedError


class UDisks2FileSystemAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name=Interfaces.Filesystem.value
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
    def mount_points(self) -> list[bytes]:
        raise NotImplementedError


class UDisks2BlockAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name=Interfaces.Block.value
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_property_async(property_signature="s")
    def hint_name(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def hint_system(self) -> bool:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def hint_ignore(self) -> None:
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
    async def rescan(self, opts: dict[str, typing.Any]) -> None:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="o")
    def drive(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="a(sa{sv})")
    def configuration(self) -> list[typing.Any]:
        raise NotImplementedError


class UDisks2DriveAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name=Interfaces.Drive.value
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_property_async(property_signature="s")
    def revision(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def WWN(self) -> str:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="a{sv}")
    def configuration(self) -> dict[str, typing.Any]:
        raise NotImplementedError

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
    def removable(self) -> bool:
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
    async def eject(self, opts: dict[str, typing.Any]) -> None:
        raise NotImplementedError
