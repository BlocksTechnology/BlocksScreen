import asyncio
import logging
import threading
import typing

import sdbus
from PyQt6 import QtCore
from sdbus_async import networkmanager


class SdbusNMMonitor(QtCore.QObject):
    state_change: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="nm-state-changed"
    )
    prop_changed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="nm-properties-changed"
    )
    added_conn: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="nm-conn-added"
    )
    rem_con: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="nm-conn-added"
    )

    def __init__(self) -> None:
        super().__init__()

        self._running: bool = False  # control
        # Run on separate thread
        self.thread: threading.Thread = threading.Thread(
            name="asyncio.NMonitor.run_forever",
            target=self._run_loop,
        )
        self.thread.daemon = False  # Do not exit the thread

        # Create a new asyncio loop
        self.loop = asyncio.new_event_loop()

        # Asyncio Event
        self.stop_event = asyncio.Event()
        self.stop_event.clear()
        # open asd set system sdbus
        self.system_dbus = sdbus.sd_bus_open_system()
        if not self.system_dbus:
            logging.info("No dbus found, async network monitor exiting")
            del self
            return
        sdbus.set_default_bus(self.system_dbus)

        # Instantiate NetworkManager
        self.nm = networkmanager.NetworkManager()

        # Start thread
        self.thread.start()

        if self.thread.is_alive():
            logging.info(
                f"Sdbus NetworkManager Monitor Thread {self.thread.name} Running"
            )

    def close(self) -> None:
        self._running = False
        if hasattr(self, "state_listener_task"):
            self.state_listener_task.cancel()
        if hasattr(self, "added_ap_listener_task"):
            self.added_ap_listener_task.cancel()
        if hasattr(self, "rem_ap_listener_task"):
            self.rem_ap_listener_task.cancel()
        if hasattr(self, "prop_changed_listener_task"):
            self.prop_changed_listener_task.cancel()
        try:
            self.loop.run_until_complete(self.state_listener_task)
            self.loop.run_until_complete(self.added_ap_listener_task)
            self.loop.run_until_complete(self.rem_ap_listener_task)
        except asyncio.CancelledError as e:
            logging.error(f"Exception while cancelling {e}")
        self.stop_event.set()
        self.loop.call_soon_threadsafe(self.stop_event.set)
        self.loop.close()
        self.thread.join()

    def _run_loop(self) -> None:
        try:
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(asyncio.gather(self.monitor()))
        except Exception as e:
            logging.error(f"Exception on loop coroutine: {e}")

    async def monitor(self) -> None:
        try:
            self._running = True
            self.state_listener_task = self.loop.create_task(
                self._state_change_listener()
            )
            self.added_ap_listener_task = self.loop.create_task(
                self._access_added_listener()
            )
            self.rem_ap_listener_task = self.loop.create_task(
                self._access_rem_listener()
            )
            self.prop_changed_listener_task = self.loop.create_task(
                self._properties_changed_listener()
            )
            await (
                self.stop_event.wait()
            )  # Wait until .set() is done on self.stop_event
        except Exception as e:
            logging.error(f"Exception on monitor coroutine: {e}")

    async def _state_change_listener(self) -> None:
        while self._running:
            try:
                logging.debug(
                    "Listening coroutine for NetworkManager state signal..."
                )
                async for state in self.nm.state_changed:
                    enum_state = networkmanager.NetworkManagerState(state)
                    logging.debug(
                        f"NM State Changed: {enum_state.name} ({state})"
                    )
                    self.state_change.emit(state)
            except Exception as e:
                logging.error(f"Exception on NM state listener: {e}")

    async def _properties_changed_listener(self) -> None:
        while self._running:
            try:
                logging.debug(
                    "Listening coroutine for NetworkManager state signal..."
                )
                async for state in self.nm.properties_changed:
                    enum_state = networkmanager.NetworkManagerState(state)
                    logging.debug(
                        f"NM State Changed: {enum_state.name} ({state})"
                    )
                    self.state_change.emit(state)
            except Exception as e:
                logging.error(f"Exception on NM state listener: {e}")

    async def _access_added_listener(self) -> None:
        while self._running:
            try:
                logging.debug("Listening coroutine for added access points")
                async for ac in self.nm.device_added:
                    logging.debug(f"Signal for device added received {ac}")
                    self.added_conn.emit(ac)
            except Exception as e:
                logging.error(f"Error for added access points listener: {e}")

    async def _access_rem_listener(self) -> None:
        while self._running:
            try:
                logging.debug("Listening coroutine for removed access points")
                async for ac in self.nm.device_removed:
                    self.rem_con.emit(ac)
            except Exception as e:
                logging.error(f"Error for removed access points listener: {e}")
