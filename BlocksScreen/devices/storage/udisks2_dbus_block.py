# Sdbus Udisks2 Interface classes and manager
#
# Contains interface classes for async and blocking api of sdbus
#
#
# Hugo Costa hugo.santos.costa@gmail.com
import typing

import sdbus


class UDisks2Manager(sdbus.DbusObjectManagerInterface):
    """subclassed Dbus object manager"""

    def __init__(
        self,
        service_name: str,
        object_path: str,
        bus: sdbus.SdBus | None = None,
    ):
        super().__init__(service_name, object_path, bus)


class UDisks2FileSystemInterface(
    sdbus.DbusInterfaceCommon, interface_name="org.freedesktop.UDisks2.Filesystem"
):
    @sdbus.dbus_method(input_signature="a{sv}", result_signature="s")
    def mount(self, opts) -> str:
        """Mounts the filesystem

        Args:
            options dict[str, tuple[str, any]]: Options to mount the filesystem

        Returns:
            path (str): mount path
        """
        raise NotImplementedError

    @sdbus.dbus_method(input_signature="a{sv}")
    def unmount(self, opts) -> None:
        """Unmount a mounted device

        Args:
            options dict[str, any]: Known options (in addition to the standart options) include `force` (of type `b`)
        """
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="t")
    def size(self) -> int:
        """Size of the filesystem. This is the amount
        of bytes used on the block device representing an outer
        fileysstem boundary

        Returns:
            size (int): Size of the filesystem
        """
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="ayy")
    def mount_points(self) -> list[str]:
        """An array of filesystem paths for where the
        file system on the device is mounted. If the
        device is not mounted, this array will be empty

        Returns
            mount_points (list[bytes]): Array of filesystem paths
        """

        raise NotImplementedError


class UDisks2BlockInterface(
    sdbus.DbusInterfaceCommon, interface_name="org.freedesktop.UDisks2.Block"
):
    @sdbus.dbus_property(property_signature="s")
    def hint_name(self) -> str:
        """Hint name, if not blank, the name to
        that presents the device

        Returns:
            name (str): name of the device"""

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="ay")
    def device(self) -> str:
        """Special device file for the block device

        Returns:
            file path (list[int] | bytes): The file path"""

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="t")
    def device_number(self) -> int:
        """Device `dev_t` of the block device"""
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def id(self) -> str:
        """Unique persistend identifier for the device
        blank if no such identifier is available

        Returns:
            id (str): unique identifier
        """

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def id_label(self) -> str:
        """Label for the filesystem or other structured
        data on the block device.
        If the property is blank there is no label or
        it is unknown

        Returns:
            label (str): filesystem label for the block
        """

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def id_UUID(self) -> str:
        """UUID of the filesystem or other structured
        data on the block device. Do not make any
        assumptions about the UUID as its format
        depends on what kind of data is on the device

        Returns:
            uuid (str): uuid"""

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
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
            usage (str): usage signature
        """
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="ayy")
    def symlinks(self) -> list[bytes]:
        """Known symlinks in `/dev` that point to the device
        in the file **Device** property.

        Returns:
            symlinks (list[bytes]): available symlinks
        """

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
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

    @sdbus.dbus_method(input_signature="a{sv}")
    def rescan(self, opts: dict[str, typing.Any]) -> None:
        """Request that the kernel and core OS rescans the
        contents of the device and update their state to reflect
        this

        Args:
            options: unused
        """

        raise NotImplementedError


class UDisks2DriveInterface(
    sdbus.DbusInterfaceCommon, interface_name="org.freedesktop.UDisks2.Drive"
):
    @sdbus.dbus_property(property_signature="b")
    def can_power_off(self) -> bool:
        """Whether the drive can be safely removed/powered off

        Returns:
            can_power_off (bool): whether it can be removed or powered off"""

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def model(self) -> str:
        """Name for the model of the drive

        Returns:
            model (str): name of the model, blank if unknown"""
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def serial(self) -> str:
        """Serial number

        Returns:
            serial (str): serial number blank if unknown
        """
        raise NotImplementedError

    @sdbus.dbus_property(property_signature="b")
    def ejectable(self) -> bool:
        """Whether the media can be ejected from the drive of the
        drive accepts the `eject` command to switch its state
        so that the it displays 'Safe To Remove'

        *This is only a guess*
        Returns:
            ejectable (bool): can be ejected
        """

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="b")
    def removable(self) -> bytes:
        """Hint whether the drive and/or its media is considered
        removable by the user.

        *This is only a guess*

        Returns:
            removable (bool): whether the drive is considered removable
        """

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="t")
    def time_detected(self) -> int:
        """The time the drive was first detected

        Returns:
            time (int): time it was first detected
        """

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="b")
    def media_available(self) -> bytes:
        """This is always True if `MediaChangeDetected` is False
        Returns:
            media available (bytes): True if media change detected is false
        """

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="b")
    def media_changed_detected(self) -> bytes:
        """Set to true only if media changes are detected

        Returns:
            media change detected (bytes): True if media changes are detected"""

        raise NotImplementedError

    @sdbus.dbus_property(property_signature="s")
    def media(self) -> str:
        """The kind of media

        Returns:
            media (str): The kind of media, blank if unknown"""

        raise NotImplementedError

    @sdbus.dbus_method(input_signature="a{sv}")
    def eject(self, opts: dict[str, typing.Any]) -> None:
        """Ejects the media from the drive

        Args:
            options (dict): currently unused
        """

        raise NotImplementedError
