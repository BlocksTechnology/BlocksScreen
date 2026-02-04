import pyudev
import sys
import logging
import asyncio
from PyQt6 import QtCore, QtWidgets


class UDevListener(QtCore.QThread):
    def __init__(self, parent: QtCore.QObject) -> None:
        super().__init__(parent)
        self.stop_event: asyncio.Event = asyncio.Event()
        self.loop: asyncio.AbstractEventLoop | None = None
        self.task_stack = set()
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by("block")

        self.observer = pyudev.MonitorObserver(self.monitor, self.log_event)

        for dev in self.context.list_devices(subsystem="block", DEVTYPE="partition"):
            print(dev)

    def run(self) -> None:
        self.observer.start()

    # try:
    #         self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    #         asyncio.set_event_loop(self.loop)
    #         self.loop.run_until_complete(self.udev_monitor())
    #     except asyncio.CancelledError as e:
    #         logging.error("Caught exception while trying to close Udev monitor: %s", e)
    #
    # async def udev_monitor(self) -> None:
    #     listener = asyncio.create_task(self.listener())
    #     self.task_stack.add(listener)
    #     while self.stop_event:
    #         try:
    #             await asyncio.gather(self.listener())
    #             listener.add_done_callback(self.task_stack.discard(listener))
    #         except asyncio.CancelledError:
    #             listener.cancel()
    #     pass
    #
    # async def listener(self) -> None:
    #     self.observer.start()

    def log_event(self, action, device) -> None:
        print(action)
        print(device)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        udev_listener = UDevListener(self)
        udev_listener.start(udev_listener.Priority.InheritPriority)


if __name__ == "__main__":
    print(pyudev.udev_version())
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    app.processEvents()
    sys.exit(app.exec())
