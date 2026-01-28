import logging
import sdbus
from PyQt6 import QtCore


# class UDisksDBus(QtCore.QThread):
class UDisksDBus:
    # usb_add: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(str, name="usb-add")
    # usb_rem: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(str, name="usb-rem")
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
    def mount(self, opts):
        return self.call_dbus_method("Mount", opts)

    @sdbus.dbus_method(input_signature="a{sv}", result_signature="s")
    def unmount(self, opts) -> str:
        return self.call_dbus_method("Unmount", opts)

    @sdbus.dbus_property(property_signature="t")
    def size(self) -> int:
        return self.get_dbus_property("Size")


class UDisks2BlockInterface(
    sdbus.DbusInterfaceCommon, interface_name="org.freedesktop.UDisks2.Block"
):
    @sdbus.dbus_property(property_signature="ay")
    def dev(self):
        return self.get_dbus_property("Device")

    @sdbus.dbus_property(property_signature="s")
    def id_label(self):
        return self.get_dbus_property("IdLabel")

    @sdbus.dbus_property(property_signature="s")
    def id_type(self):
        return self.get_dbus_property("IdType")

    @sdbus.dbus_method(input_signature="a{sv}", result_signature="")
    def rescan(self, opts):
        return self.call_dbus_method("Rescan", opts)


class UDisks2DriveInterface(
    sdbus.DbusInterfaceCommon, interface_name="org.freedesktop.UDisks2.Filesystem"
):
    @sdbus.dbus_property(property_signature="b")
    def can_poweroff(self) -> bytes:
        return self.get_dbus_property("CanPowerOff")

    @sdbus.dbus_property(property_signature="b")
    def removable(self) -> bytes:
        return self.get_dbus_property("Removable")

    @sdbus.dbus_property(property_signature="b")
    def ejectable(self) -> bytes:
        return self.get_dbus_property("Ejectable")

    @sdbus.dbus_property(property_signature="t")
    def time_detected(self) -> any:
        return self.get_dbus_property("TimeDetected")

    @sdbus.dbus_property(property_signature="b")
    def media_available(self) -> bytes:
        return self.get_dbus_property("MediaAvailable")

    @sdbus.dbus_property(property_signature="b")
    def media_changed_detected(self) -> bytes:
        return self.get_dbus_property("MediaChangedDetected")

    @sdbus.dbus_property(property_signature="s")
    def media(self) -> str:
        return self.get_dbus_property("Media")

    @sdbus.dbus_method(input_signature="a{sv}", result_signature="s")
    def eject(self, options) -> str:
        return self.call_dbus_method("Eject", options)


if __name__ == "__main__":
    bus = sdbus.sd_bus_open_system()
    manager = UDisks2Manager("org.freedesktop.UDisks2", "/org/freedesktop/UDisks2", bus)
    objects = manager.get_managed_objects()
    for path in objects.keys():
        print(f" -> {path}")

    # s = UDisks2BlockInterface(
    #     service_name="org.freedesktop.UDisks2",
    #     object_path="/org/freedesktop/UDisks2/block_devices/sda",
    #     bus=sdbus.sd_bus_open_system(),
    # )
    # print(s.id_label)
