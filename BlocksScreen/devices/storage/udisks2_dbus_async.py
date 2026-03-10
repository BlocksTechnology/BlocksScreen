# Sdbus Udisks2 Interface classes and manager
#
# Contains interface classes for async and blocking api of sdbus
#
#
# Hugo Costa hugo.santos.costa@gmail.com
import enum
import typing

import sdbus


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
        """Set to True if the partition itself is a container for other partitions

        For example, for dos partition tables, this applies to so-called extended
        partition (partitions of type 0x05, 0x0f or 0x85) containing so-called logical partitions.


        Returns:
            is_container (bool): if it is a container
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def is_contained(self) -> bool:
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
        """Mounts the filesystem

        Args:
            options dict[str, tuple[str, any]]: Options to mount the filesystem

        Returns:
            path (str): mount path
        """
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="a{sv}")
    async def unmount(self, opts) -> None:
        """Unmount a mounted device

        Args:
            options dict[str, any]: Known options (in addition to the standart options) include `force` (of type `b`)
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def size(self) -> int:
        """Size of the filesystem. This is the amount
        of bytes used on the block device representing an outer
        filesystem boundary

        Returns:
            size (int): Size of the filesystem
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="ayy")
    def mount_points(self) -> list[bytes]:
        """An array of filesystem paths for where the
        file system on the device is mounted. If the
        device is not mounted, this array will be empty

        Returns
            mount_points (list[bytes]): Array of filesystem paths
        """
        raise NotImplementedError


class UDisks2BlockAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name=Interfaces.Block.value
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_property_async(property_signature="s")
    def hint_name(self) -> str:
        """Hint name, if not blank, the name to
        that presents the device

        Returns:
            name (str): name of the device"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def hint_system(self) -> bool:
        """If the device is considered a system device
        True if it is. System devices are devices that
        require additional permissions to access

        Returns
            hint system (bool): If device is `system device`"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def hint_ignore(self) -> bool:
        """If the device should be hidden from users
        Returns
            ignore (bool): True if the system should be ignored"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="ay")
    def device(self) -> list[int] | bytes:
        """Special device file for the block device

        Returns:
            file path (list[int] | bytes): The file path"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def device_number(self) -> int:
        """Device `dev_t` of the block device"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id(self) -> str:
        """Unique persistend identifier for the device
        blank if no such identifier is available

        Returns:
            id (str): unique identifier"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id_label(self) -> str:
        """Label for the filesystem or other structured
        data on the block device.
        If the property is blank there is no label or
        it is unknown

        Returns:
            label (str): filesystem label for the block"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id_UUID(self) -> str:
        """UUID of the filesystem or other structured
        data on the block device. Do not make any
        assumptions about the UUID as its format
        depends on what kind of data is on the device

        Returns:
            uuid (str): uuid"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id_usage(self) -> str:
        """Result of probing for signatures on the block device
        Known values include
            - filesystem -> Used for mountable filesystems
            - crypto -> Used for e.g. LUKS devices
            - raid -> Used for e.g. RAID members
            - other -> Something else was detected

        -----
        If blank no known signature was detected. It doesn't
        necessarily mean the device contains no structured data;
        it only means that probing failed

        Returns:
            usage (str): usage signature"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id_type(self) -> str:
        """Property that contains more information about
        the probing result of the blocks device. It depends
        on the IdUsage property
            - filesystem -> The mountable file system that was detected (e.g. vfat).
            - crypto -> Encrypted data. Known values include crypto_LUKS.
            - raid -> RAID or similar. Known values include LVM2_member (for LVM2 components), linux_raid_member (for MD-RAID components.)
            - other -> Something else. Known values include swap (for swap space), suspend (data used when resuming from suspend-to-disk).
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="ayy")
    def symlinks(self) -> list[bytes]:
        """Known symlinks in `/dev` that point to the device
        in the file **Device** property.

        Returns:
            symlinks (list[bytes]): available symlinks
        """
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="a{sv}")
    async def rescan(self, opts: dict[str, typing.Any]) -> None:
        """Request that the kernel and core OS rescans the
        contents of the device and update their state to reflect
        this

        Args:
            options: unused
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="o")
    def drive(self) -> str:
        """The org.freedesktop.UDisks2.Drive object that the
        block device belongs to, or '/' if no such object
        exits

        Returns:
            drive (str): path
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="a(sa{sv})")
    def configuration(self) -> list[typing.Any]:
        """The configuration for the device
        This is an array of pairs (type, details), where `type` is
        a string identifying the configuration source and the
        `details` has the actual configuration data.
        For entries of type `fstab` known configurations are:
            - fsname (type 'ay') - The special device
            - dir (type 'ay') - The mount point
            - type (type 'ay') - The filesystem type
            - opts (type 'ay') - Options
            - freq (type 'i') - Dump frequency in days
            - passno (type 'i') - Pass number of parallel fsck
        For entries of type `crypttab` known configurations are:
            - name (type 'ay') - The name to set the device up as
            - device (type 'ay') - The special device
            - passphrase-path (type 'ay') - Either empty to specify
                that no password is set, otherwise a path to a file
                containing the ecnryption password. This may also point
                to a special devicde file in /dev such as /dev/random
            - options (type 'ay') - Options
        """
        raise NotImplementedError


class UDisks2DriveAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name=Interfaces.Drive.value
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_property_async(property_signature="s")
    def revision(self) -> str:
        """Firmware revision or blank if unknown
        Returns:
            revision (str): revision or blank
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def WWN(self) -> str:
        """The World Wide Name of the drive or blank if unknown
        Returns:
            wwn (str) : wwn or none
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="a{sv}")
    def configuration(self) -> dict[str, typing.Any]:
        """Configuration directives applied to the drive when
        its connected.

        Returns:
            configurations (dict): applied configurations
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def can_power_off(self) -> bool:
        """Whether the drive can be safely removed/powered off

        Returns:
            can_power_off (bool): whether it can be removed or powered off"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def model(self) -> str:
        """Name for the model of the drive

        Returns:
            model (str): name of the model, blank if unknown"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def connection_bus(self) -> str:
        """Physical connection bus for the drive, as seen
        by the user

        Returns:
            connection bus (str): physical connection bus ['usb', 'sdio', 'ieee1394']
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def serial(self) -> str:
        """Serial number

        Returns:
            serial (str): serial number blank if unknown
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def ejectable(self) -> bool:
        """Whether the media can be ejected from the drive of the
        drive accepts the `eject` command to switch its state
        so that the it displays 'Safe To Remove'

        *This is only a guess*
        Returns:
            ejectable (bool): can be ejected
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def removable(self) -> bool:
        """Hint whether the drive and/or its media is considered
        removable by the user.

        *This is only a guess*

        Returns:
            removable (bool): whether the drive is considered removable
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="t")
    def time_detected(self) -> int:
        """The time the drive was first detected

        Returns:
            time (int): time it was first detected
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def media_available(self) -> bool:
        """This is always True if `MediaChangeDetected` is False
        Returns:
            media available (bool): True if media change detected is false
        """
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def media_changed_detected(self) -> bool:
        """Set to true only if media changes are detected

        Returns:
            media change detected (bool): True if media changes are detected"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def media(self) -> str:
        """The kind of media

        Returns:
            media (str): The kind of media, blank if unknown"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="b")
    def media_removable(self) -> bool:
        """Whether the media can be removed from the drive

        Returns:
            media_removable (bool): Whether it can be removed"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def id(self) -> str:
        """Unique persistent identifier for the device or
        blank if not available

        Returns:
            id (str): Identifier e.g “ST32000542AS-6XW00W51”"""
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def vendor(self) -> str:
        """Name for the vendor of the dirve or blank if
        unknown

        Returns:
            vendor (str): Name of the vendor or blank"""
        raise NotImplementedError

    @sdbus.dbus_method_async(input_signature="a{sv}")
    async def eject(self, opts: dict[str, typing.Any]) -> None:
        """Ejects the media from the drive

        Args:
            options (dict): currently unused
        """

        raise NotImplementedError
