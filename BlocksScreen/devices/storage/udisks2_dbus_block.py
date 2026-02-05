# Sdbus Udisks2 Interface classes and manager
#
# Contains interface classes for async and blocking api of sdbus
#
#
# Hugo Costa hugo.santos.costa@gmail.com
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
