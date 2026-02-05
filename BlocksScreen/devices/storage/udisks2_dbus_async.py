# Sdbus Udisks2 Interface classes and manager
#
# Contains interface classes for async and blocking api of sdbus
#
#
# Hugo Costa hugo.santos.costa@gmail.com
import sdbus

Interfaces: dict[str, str] = {
    "Filesystem": "org.freedesktop.Filesystem",
    "Drive": "org.freedesktop.Drive",
    "Partition": "org.freedesktop.Partition",
    "Block": "org.freedesktop.Block",
    "PartitionTable": "org.freedesktop.PartitionTable",
}


class UDisks2AsyncManager(sdbus.DbusObjectManagerInterfaceAsync):
    """Subclassed async dbus object manager"""

    def __init__(self) -> None:
        super().__init__()


class UDisks2PartitionTableAsyncInterface(
    sdbus.DbusInterfaceCommonAsync,
    interface_name="org.freedesktop.UDisks2.PartitionTable",
):
    def __init__(self) -> None:
        super().__init__()

    @sdbus.dbus_property_async(property_signature="ao")
    def partitions(self) -> list[str]:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="s")
    def type(self) -> str:
        raise NotImplementedError


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


class UDisks2BlockAsyncInterface(
    sdbus.DbusInterfaceCommonAsync, interface_name="org.freedesktop.UDisks2.Block"
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
    async def rescan(self, opts: dict) -> None:
        raise NotImplementedError

    @sdbus.dbus_property_async(property_signature="o")
    def drive(self) -> str:
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
