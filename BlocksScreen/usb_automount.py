from PyQt6 import QtCore
import typing
import sdbus


class SdbusUSBWatcher(QtCore.QThread):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.mutex.condition: QtCore.QWaitCondition()
        self.mutex: QtCore.QMutex = QtCore.QMutex()
        self.running: bool = False

    def run(self) -> None: ...

    def try_mount(self) -> None: ...

    def try_cleanup(self) -> None: ...


class UDisksDBus(QtCore.QThread):
    usb_add: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="usb-add")
    usb_rem: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="usb-rem")

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.system_bus: sdbus.SdBus = sdbus.sd_bus_open_system()
        if not self.system_bus:
            self.close()
            return
        sdbus.set_default_bus(self.system_bus)


class UDisks2FileSystemInterface(
    sdbus.DbusInterfaceCommon, interface_name="org.freedesktop.UDisks2.Filesystem"
):
    @sdbus.dbus_method(input_signature='a{sv}', result_signature='s')
    def mount(self, options):
        return self.call_dbus_method('Mount', options)


class UDisks2BlockInterface(sdbus.DbusInterfaceCommon, interface_name="org.freedestop.UDisks2.Block"):

  @sdbus.dbus_property(property_signature="ay")
   def dev(self):
        return self.get_dbus_property("Device")

    @sdbus.dbus_property(property_signature="s")
    def id_label(self):
        return self.get_dbus_property("IdLabel")

    @sdbus.dbus_method(input_signature='a{sv}', result_signature=)
    def rescan(self, options):
        return self.call_dbus_method('Rescan', options)

class UDisks2Manager(sdbus.sdbus.DbusObjectManagerInterface): 
    pass


if "__main__" == __name__:
    s = UDisksDBus()
