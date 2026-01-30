import logging
import sdbus
from PyQt6 import QtCore
import typing


class UDisksDBus(QtCore.QThread):
    usb_add: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(str, name="usb-add")
    usb_rem: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(str, name="usb-rem")

    def __init__(self, parent: QtCore.QObject) -> None:
        # super().__init__(parent)
        self.system_bus: sdbus.SdBus = sdbus.sd_bus_open_system()
        self.obj_manager: UDisks2Manager = UDisks2Manager(
            "org.freedesktop.UDisks2", "/org/freedesktop/UDisks2", self.system_bus
        )
        if not self.system_bus:
            self.close()
            return
        sdbus.set_default_bus(self.system_bus)

    def close(self) -> None:
        logging.info("Closing usb udisks2 dbus connection")
        self.system_bus.close()


class UDisks2Manager(sdbus.DbusObjectManagerInterface):
    """subclassed Dbus object manager"""

    pass


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


if __name__ == "__main__":
    bus = sdbus.sd_bus_open_system()
    manager = UDisks2Manager("org.freedesktop.UDisks2", "/org/freedesktop/UDisks2", bus)
    objects = manager.get_managed_objects()
    for path, item in objects.items():
        print(f" -> {path}")
        # print(f"    ->{item.keys()}")
    s = UDisks2BlockInterface(
        service_name="org.freedesktop.UDisks2",
        object_path="/org/freedesktop/UDisks2/block_devices/sdd1",
        bus=bus,
    )
    f = UDisks2FileSystemInterface(
        service_name="org.freedesktop.UDisks2",
        object_path="/org/freedesktop/UDisks2/block_devices/sdd1",
        bus=bus,
    )
    d = UDisks2DriveInterface(
        service_name="org.freedesktop.UDisks2",
        # object_path="/org/freedesktop/UDisks2/block_devices/sd",
        object_path="/org/freedesktop/UDisks2/drives/ASolid_USB_25072833720072",
        bus=bus,
    )
    print(f"File system size -> {f.size}")
    print(f"file system mount points -> {f.mount_points}")
    print(f"Block hint name -> {s.hint_name}")
    print(f"Block device -> {s.device}")
    print(f"Block id -> {s.id}")
    print(f"Block id label -> {s.id_label}")
    print(f"Block id uuid -> {s.id_UUID}")
    print(f"Block id usage -> {s.id_usage}")
    print(f"Block symlinks -> {s.symlinks}")
    print(f"Block id type -> {s.id_type}")
    print(f"Block device number -> {s.device_number}")
    print(f"Drive can power off -> {d.can_power_off}")
    print(f"Drive model -> {d.model}")
    print(f"Drive serial -> {d.serial}")
    print(f"Drive ejectable -> {d.ejectable}")
    print(f"Drive time detected -> {d.time_detected}")
    print(f"Drive removable -> {d.removable}")
