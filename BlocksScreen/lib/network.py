import asyncio
import enum
import logging
import threading
import typing
from uuid import uuid4

import sdbus
from PyQt6 import QtCore
from sdbus_async import networkmanager as dbusNm

logger = logging.getLogger(__name__)


class NetworkManagerRescanError(Exception):
    """Exception raised when rescanning the network fails."""

    def __init__(self, error):
        super(NetworkManagerRescanError, self).__init__()
        self.error = error


class SdbusNetworkManagerAsync(QtCore.QObject):
    class ConnectionPriority(enum.Enum):
        """Connection priorities"""

        HIGH = 90
        MEDIUM = 50
        LOW = 20

    nm_state_change: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="nm-state-changed"
    )
    nm_properties_change: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        tuple, name="nm-properties-changed"
    )

    def __init__(self) -> None:
        super().__init__()
        self._listeners_running: bool = False
        self.listener_thread: threading.Thread = threading.Thread(
            name="NMonitor.run_forever",
            target=self._listener_run_loop,
            daemon=False,
        )
        self.listener_task_queue: list = []
        self.loop = asyncio.new_event_loop()
        self.stop_listener_event = asyncio.Event()
        self.stop_listener_event.clear()
        self.system_dbus = sdbus.sd_bus_open_system()
        if not self.system_dbus:
            logger.error("No dbus found, async network monitor exiting")
            self.close()
            return
        sdbus.set_default_bus(self.system_dbus)
        self.nm = dbusNm.NetworkManager()
        self.listener_thread.start()
        if self.listener_thread.is_alive():
            logger.info(
                f"Sdbus NetworkManager Monitor Thread {self.listener_thread.name} Running"
            )
        self.hotspot_ssid: str = "PrinterHotspot"
        self.hotspot_password: str = "123456789"
        self.check_connectivity()
        self.available_wired_interfaces = self.get_wired_interfaces()
        self.available_wireless_interfaces = self.get_wireless_interfaces()
        self.old_ssid: str = ""
        wireless_interfaces: typing.List[dbusNm.NetworkDeviceWireless] = (
            self.get_wireless_interfaces()
        )
        self.primary_wifi_interface: typing.Optional[dbusNm.NetworkDeviceWireless] = (
            wireless_interfaces[0] if wireless_interfaces else None
        )
        wired_interfaces: typing.List[dbusNm.NetworkDeviceWired] = (
            self.get_wired_interfaces()
        )
        self.primary_wired_interface: typing.Optional[dbusNm.NetworkDeviceWired] = (
            wired_interfaces[0] if wired_interfaces else None
        )

        self.create_hotspot(self.hotspot_ssid, self.hotspot_password)
        if self.primary_wifi_interface:
            self.rescan_networks()

    def _listener_run_loop(self) -> None:
        try:
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(asyncio.gather(self.listener_monitor()))
        except Exception as e:
            logging.error(f"Exception on loop coroutine: {e}")

    async def _end_tasks(self) -> None:
        for task in self.listener_task_queue:
            task.cancel()
        results = await asyncio.gather(
            *self.listener_task_queue, return_exceptions=True
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Caught Exception while ending asyncio tasks: {result}")
            return

    def close(self) -> None:
        future = asyncio.run_coroutine_threadsafe(self._end_tasks(), self.loop)
        try:
            future.result(timeout=5)
        except Exception as e:
            logging.info(f"Exception while ending loop tasks: {e}")
        self.stop_listener_event.set()
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.listener_thread.join()
        self.loop.close()

    async def listener_monitor(self) -> None:
        """Monitor for NetworkManager properties"""
        try:
            self._listeners_running = True

            self.listener_task_queue.append(
                self.loop.create_task(self._nm_state_listener())
            )
            self.listener_task_queue.append(
                self.loop.create_task(self._nm_properties_listener())
            )
            results = asyncio.gather(*self.listener_task_queue, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    logger.error(
                        f"Caught Exception on network manager asyncio loop: {result}"
                    )
                    raise Exception(result)
                await self.stop_listener_event.wait()

        except Exception as e:
            logging.error(f"Exception on listener monitor produced coroutine: {e}")

    async def _nm_state_listener(self) -> None:
        while self._listeners_running:
            try:
                async for state in self.nm.state_changed:
                    enum_state = dbusNm.NetworkManagerState(state)
                    self.nm_state_change.emit(enum_state.name)
            except Exception as e:
                logging.error(f"Exception on Network Manager state listener: {e}")

    async def _nm_properties_listener(self) -> None:
        while self._listeners_running:
            try:
                logging.debug("Listening for Network Manager state change")
                async for properties in self.nm.properties_changed:
                    self.nm_properties_change.emit(properties)

            except Exception as e:
                logging.error(f"Exception on Network Manager state listener: {e}")

    def check_nm_state(self) -> typing.Union[str, None]:
        """Check NetworkManager state"""
        if not self.nm:
            return
        future = asyncio.run_coroutine_threadsafe(self.nm.state.get_async(), self.loop)
        try:
            state_value = future.result(timeout=2)
            return str(dbusNm.NetworkManagerState(state_value).name)
        except Exception as e:
            logging.error(f"Exception while fetching Network Monitor State: {e}")
            return None

    def check_connectivity(self) -> str:
        """Checks Network Manager Connectivity state

                UNKNOWN = 0 - Network connectivity is unknown, connectivity checks are disabled.

                NONE = 1    - Host is not connected to any network.

                PORTAL = 2  - Internet connection is hijacked by a captive portal gateway.

                LIMITED = 3 - The host is connected to a network, does not appear to be able to reach full internet.

                FULL = 4    - The host is connected to a network, appears to be able to reach fill internet.


        Returns:
            _type_: _description_
        """
        if not self.nm:
            return ""
        future = asyncio.run_coroutine_threadsafe(
            self.nm.check_connectivity(), self.loop
        )
        try:
            connectivity = future.result(timeout=2)
            return dbusNm.NetworkManagerConnectivityState(connectivity).name
        except Exception as e:
            logging.error(
                f"Exception while fetching Network Monitor Connectivity State: {e}"
            )
            return ""

    def check_wifi_interface(self) -> bool:
        """Check if wifi interface is set

        Returns:
            bool: true if it is. False otherwise
        """
        return bool(self.primary_wifi_interface)

    def get_available_interfaces(self) -> typing.Union[typing.List[str], None]:
        """Gets the names of all available interfaces

        Returns:
            typing.List[str]: List of strings with the available names of all interfaces
        """
        try:
            future = asyncio.run_coroutine_threadsafe(self.nm.get_devices(), self.loop)
            devices = future.result(timeout=2)
            interfaces = []
            for device in devices:
                interface_future = asyncio.run_coroutine_threadsafe(
                    dbusNm.NetworkDeviceGeneric(
                        bus=self.system_dbus, device_path=device
                    ).interface.get_async(),
                    self.loop,
                )
                interface_name = interface_future.result(timeout=2)
                interfaces.append(interface_name)
            return interfaces
        except Exception as e:
            logging.error(f"Exception on fetching available interfaces: {e}")

    def wifi_enabled(self) -> bool:
        """Returns a boolean if wireless is enabled on the device.

        Returns:
            bool: True if device is enabled | False if not
        """
        future = asyncio.run_coroutine_threadsafe(
            self.nm.wireless_enabled.get_async(), self.loop
        )
        return future.result(timeout=2)

    def toggle_wifi(self, toggle: bool):
        """toggle_wifi Enable/Disable wifi

        Args:
            toggle (bool):

            - True -> Enable wireless

            - False -> Disable wireless

        Raises:
            ValueError: Raised when the argument is not of type boolean.

        """
        if not isinstance(toggle, bool):
            raise TypeError("Toggle wifi expected boolean")
        if self.wifi_enabled() == toggle:
            return
        asyncio.run_coroutine_threadsafe(
            self.nm.wireless_enabled.set_async(toggle), self.loop
        )

    async def _toggle_networking(self, value: bool = True) -> None:
        if not self.primary_wifi_interface:
            return
        if self.primary_wifi_interface == "/":
            return
        results = asyncio.gather(
            self.loop.create_task(self.nm.enable(value)),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Exception Caught when toggling network : {result}")

    def disable_networking(self) -> None:
        """Disable networking"""
        if not (self.primary_wifi_interface and self.primary_wired_interface):
            return
        if self.primary_wifi_interface == "/" and self.primary_wired_interface == "/":
            return
        asyncio.run_coroutine_threadsafe(self._toggle_networking(False), self.loop)

    def activate_networking(self) -> None:
        """Activate networking"""
        if not (self.primary_wifi_interface and self.primary_wired_interface):
            return
        if self.primary_wifi_interface == "/" and self.primary_wired_interface == "/":
            return
        asyncio.run_coroutine_threadsafe(self._toggle_networking(True), self.loop)

    def toggle_hotspot(self, toggle: bool) -> None:
        """Activate/Deactivate device hotspot

        Args:
            toggle (bool): toggle option, True to activate Hotspot, False otherwise

        Raises:
            ValueError: If the toggle argument is not a Boolean.
        """
        if not isinstance(toggle, bool):
            raise TypeError("Correct type should be a boolean.")

        if not self.nm:
            return
        try:
            old_ssid: typing.Union[str, None] = self.get_current_ssid()
            if old_ssid:
                self.old_ssid = old_ssid
            if toggle:
                self.disconnect_network()
                self.connect_network(self.hotspot_ssid)
                results = asyncio.gather(
                    self.nm.reload(0x0), return_exceptions=True
                ).result()
                for result in results:
                    if isinstance(result, Exception):
                        raise Exception(result)

                if self.nm.check_connectivity() == (
                    dbusNm.NetworkManagerConnectivityState.FULL
                    | dbusNm.NetworkManagerConnectivityState.LIMITED
                ):
                    logging.debug(f"Hotspot AP {self.hotspot_ssid} up!")

                return
            else:
                if self.old_ssid:
                    self.connect_network(self.old_ssid)
                    return
        except Exception as e:
            logging.error(f"Caught Exception while toggling hotspot to {toggle}: {e}")

    def hotspot_enabled(self) -> typing.Optional["bool"]:
        """Returns a boolean indicating whether the device hotspot is on or not .

        Returns:
            bool: True if Hotspot is activated, False otherwise.
        """
        return bool(self.hotspot_ssid == self.get_current_ssid())

    def get_wired_interfaces(self) -> typing.List[dbusNm.NetworkDeviceWired]:
        """get_wired_interfaces Get only the names for the available wired (Ethernet) interfaces.

        Returns:
            typing.List[str]: List containing the names of all wired(Ethernet) interfaces.
        """
        devs_future = asyncio.run_coroutine_threadsafe(self.nm.get_devices(), self.loop)
        devices = devs_future.result(timeout=2)

        return list(
            map(
                lambda path: dbusNm.NetworkDeviceWired(path),
                filter(
                    lambda path: path,
                    filter(
                        lambda device: asyncio.run_coroutine_threadsafe(
                            dbusNm.NetworkDeviceGeneric(
                                bus=self.system_dbus, device_path=device
                            ).device_type.get_async(),
                            self.loop,
                        ).result(timeout=2)
                        == dbusNm.enums.DeviceType.ETHERNET,
                        devices,
                    ),
                ),
            )
        )

    def get_wireless_interfaces(
        self,
    ) -> typing.List[dbusNm.NetworkDeviceWireless]:
        """get_wireless_interfaces Get only the names of wireless interfaces.

        Returns:
            typing.List[str]: A list containing the names of wireless interfaces.
        """
        # Each interface type has a device flag that is exposed in enums.DeviceType.<device such as Ethernet or Wifi>
        devs_future = asyncio.run_coroutine_threadsafe(self.nm.get_devices(), self.loop)
        devices = devs_future.result(timeout=2)
        return list(
            map(
                lambda path: dbusNm.NetworkDeviceWireless(
                    bus=self.system_dbus, device_path=path
                ),
                filter(
                    lambda path: path,
                    filter(
                        lambda device: asyncio.run_coroutine_threadsafe(
                            dbusNm.NetworkDeviceGeneric(
                                bus=self.system_dbus, device_path=device
                            ).device_type.get_async(),
                            self.loop,
                        ).result(timeout=3)
                        == dbusNm.enums.DeviceType.WIFI,
                        devices,
                    ),
                ),
            )
        )

    async def _gather_ssid(self) -> str:
        try:
            if not self.nm:
                return ""
            primary_con = await self.nm.primary_connection.get_async()
            if primary_con == "/":
                logger.debug("No primary connection")
                return ""
            active_connection = dbusNm.ActiveConnection(
                bus=self.system_dbus, connection_path=primary_con
            )
            if not active_connection:
                logger.debug("Active connection is none my man")
                return ""
            con = await active_connection.connection.get_async()
            con_settings = dbusNm.NetworkConnectionSettings(
                bus=self.system_dbus, settings_path=con
            )
            settings = await con_settings.get_settings()
            return str(settings["802-11-wireless"]["ssid"][1].decode())
        except Exception as e:
            logger.error("Caught exception while gathering ssid %s", e)
        return ""

    def get_current_ssid(self) -> str:
        """Get current ssid

        Returns:
            str: ssid address
        """
        try:
            future = asyncio.run_coroutine_threadsafe(self._gather_ssid(), self.loop)
            return future.result(timeout=5)
        except Exception as e:
            logging.info(f"Unexpected error occurred: {e}")
        return ""

    def get_current_ip_addr(self) -> str:
        """Get the current connection ip address.
        Returns:
            str: A string containing the current ip address
        """
        try:
            primary_con_fut = asyncio.run_coroutine_threadsafe(
                self.nm.primary_connection.get_async(), self.loop
            )
            primary_con = primary_con_fut.result(timeout=2)
            if primary_con == "/":
                logging.info("There is no NetworkManager active connection.")
                return ""

            _device_ip4_conf_path = dbusNm.ActiveConnection(
                bus=self.system_dbus, connection_path=primary_con
            )
            ip4_conf_future = asyncio.run_coroutine_threadsafe(
                _device_ip4_conf_path.ip4_config.get_async(), self.loop
            )

            if _device_ip4_conf_path == "/":
                logging.info(
                    "NetworkManager reports no IP configuration for the interface"
                )
                return ""
            ip4_conf = dbusNm.IPv4Config(
                bus=self.system_dbus, ip4_path=ip4_conf_future.result(timeout=2)
            )
            addr_data_fut = asyncio.run_coroutine_threadsafe(
                ip4_conf.address_data.get_async(), self.loop
            )
            addr_data = addr_data_fut.result(timeout=2)
            return [address_data["address"][1] for address_data in addr_data][0]
        except IndexError as e:
            logger.error("List out of index %s", e)
        return ""

    async def _gather_primary_interface(
        self,
    ) -> typing.Union[
        dbusNm.NetworkDeviceWired,
        dbusNm.NetworkDeviceWireless,
        typing.Tuple,
        str,
    ]:
        if not self.nm:
            return ""

        primary_connection = await self.nm.primary_connection.get_async()
        if not primary_connection:
            return ""
        if primary_connection == "/":
            if self.primary_wifi_interface and self.primary_wifi_interface != "/":
                return self.primary_wifi_interface
            elif self.primary_wired_interface and self.primary_wired_interface != "/":
                return self.primary_wired_interface
            else:
                "/"

        primary_conn_type = await self.nm.primary_connection_type.get_async()
        active_connection = dbusNm.ActiveConnection(
            bus=self.system_dbus, connection_path=primary_connection
        )
        gateway = await active_connection.devices.get_async()
        device_interface = await dbusNm.NetworkDeviceGeneric(
            bus=self.system_dbus, device_path=gateway[0]
        ).interface.get_async()
        return (device_interface, primary_connection, primary_conn_type)

    def get_primary_interface(
        self,
    ) -> typing.Union[
        dbusNm.NetworkDeviceWired,
        dbusNm.NetworkDeviceWireless,
        typing.Tuple,
        str,
    ]:
        """Get the primary interface,
            If a there is a connection, returns the interface that is being currently used.

            If there is no connection and wifi is available return de wireless interface.

            If there is no wireless interface and no active connection return the first wired interface that is not (lo).


        Returns:
            typing.List:
        """
        future = asyncio.run_coroutine_threadsafe(
            self._gather_primary_interface(), self.loop
        )
        return future.result(timeout=2)

    async def _rescan(self) -> None:
        if not self.primary_wifi_interface:
            return
        if self.primary_wifi_interface == "/":
            return
        try:
            task = self.loop.create_task(self.primary_wifi_interface.request_scan({}))
            results = await asyncio.gather(task, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    raise NetworkManagerRescanError(f"Rescan error: {result}")
                return
        except Exception as e:
            logger.error(f"Caught Exception: {e.__class__.__name__}: {e}")
            return

    def rescan_networks(self) -> None:
        """Scan for available networks."""
        try:
            future = asyncio.run_coroutine_threadsafe(self._rescan(), self.loop)
            result = future.result(timeout=2)
            return result

        except Exception as e:
            logger.error(f"Caught Exception while rescanning networks: {e}")

    async def _get_network_info(self, ap: dbusNm.AccessPoint) -> typing.Tuple:
        ssid = await ap.ssid.get_async()
        sec = await self._get_security_type(ap)
        freq = await ap.frequency.get_async()
        channel = await ap.frequency.get_async()
        signal = await ap.strength.get_async()
        mbit = await ap.max_bitrate.get_async()
        bssid = await ap.hw_address.get_async()
        return (
            ssid.decode(),
            {
                "security": sec,
                "frequency": freq,
                "channel": channel,
                "signal_level": signal,
                "max_bitrate": mbit,
                "bssid": bssid,
            },
        )

    async def _gather_networks(
        self, aps: typing.List[dbusNm.AccessPoint]
    ) -> typing.Union[typing.List[typing.Tuple], None]:
        try:
            results = await asyncio.gather(
                *(self.loop.create_task(self._get_network_info(ap)) for ap in aps),
                return_exceptions=False,
            )
            return results
        except Exception as e:
            logger.error(
                f"Caught Exception while asynchronously gathering AP information: {e}"
            )

    async def _get_available_networks(self) -> typing.Union[typing.Dict, None]:
        if not self.primary_wifi_interface:
            return
        if self.primary_wifi_interface == "/":
            return
        await self._rescan()
        try:
            last_scan = await self.primary_wifi_interface.last_scan.get_async()
            if last_scan != -1:
                primary_wifi_dev_type = (
                    await self.primary_wifi_interface.device_type.get_async()
                )
                if primary_wifi_dev_type == dbusNm.enums.DeviceType.WIFI:
                    aps = await self.primary_wifi_interface.get_all_access_points()
                    _aps: typing.List[dbusNm.AccessPoint] = list(
                        map(
                            lambda ap_path: dbusNm.AccessPoint(
                                bus=self.system_dbus, point_path=ap_path
                            ),
                            aps,
                        )
                    )
                    task = self.loop.create_task(self._gather_networks(_aps))
                    result = await asyncio.gather(task, return_exceptions=False)
                    return dict(*result) if result else None  # type:ignore
        except Exception as e:
            logger.error(f"Caught Exception while gathering access points: {e}")
            return {}

    def get_available_networks(self) -> typing.Union[typing.Dict, None]:
        """Get available networks"""
        future = asyncio.run_coroutine_threadsafe(
            self._get_available_networks(), self.loop
        )
        return future.result(timeout=20)

    async def _get_security_type(self, ap: dbusNm.AccessPoint) -> typing.Tuple:
        """Get the security type from a network AccessPoint

        Args:
            ap (AccessPoint): The AccessPoint of the network.

        Returns:
            typing.Tuple: A Tuple containing all the flags about the WpaSecurityFlags ans AccessPointCapabilities
            - `(flags, wpa_flags, rsn_flags)`



        Check: For more information about the flags
            :py:class:`WpaSecurityFlags` and `AccessPointCapabilities` from :py:module:`python-sdbus-networkmanager.enums`
        """
        if not ap:
            return

        _rsn_flag_task = self.loop.create_task(ap.rsn_flags.get_async())
        _wpa_flag_task = self.loop.create_task(ap.wpa_flags.get_async())
        _sec_flags_task = self.loop.create_task(ap.flags.get_async())

        results = await asyncio.gather(
            _rsn_flag_task,
            _wpa_flag_task,
            _sec_flags_task,
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Exception caught getting security type: {result}")
                return ()
        _rsn, _wpa, _sec = results
        if len(dbusNm.AccessPointCapabilities(_sec)) == 0:
            return ("Open", "")
        return (
            dbusNm.WpaSecurityFlags(_rsn),
            dbusNm.WpaSecurityFlags(_wpa),
            dbusNm.AccessPointCapabilities(_sec),
        )

    def get_saved_networks(
        self,
    ) -> typing.List[typing.Dict] | None:
        """get_saved_networks Gets a list with the names and ids of all saved networks on the device.

        Returns:
            typing.List[dict] | None: List that contains the names and ids of all saved networks on the device.



        I admit that this implementation is way to complicated, I don't even think it's great on memory and time, but i didn't use for loops so mission achieved.
        """
        if not self.nm:
            return []

        try:
            _connections: typing.List[str] = asyncio.run_coroutine_threadsafe(
                dbusNm.NetworkManagerSettings(bus=self.system_dbus).list_connections(),
                self.loop,
            ).result(timeout=2)

            saved_cons = list(
                map(
                    lambda connection: dbusNm.NetworkConnectionSettings(
                        bus=self.system_dbus, settings_path=connection
                    ),
                    _connections,
                )
            )

            sv_cons_settings_future = asyncio.run_coroutine_threadsafe(
                self._get_settings(saved_cons),
                self.loop,
            )
            settings_list: typing.List[dbusNm.NetworkManagerConnectionProperties] = (
                sv_cons_settings_future.result(timeout=2)
            )
            _known_networks_parameters = list(
                filter(
                    lambda network_entry: network_entry is not None,
                    list(
                        map(
                            lambda network_properties: (
                                {
                                    "ssid": network_properties["802-11-wireless"][
                                        "ssid"
                                    ][1].decode(),
                                    "uuid": network_properties["connection"]["uuid"][1],
                                    "signal": 0
                                    + self.get_connection_signal_by_ssid(
                                        network_properties["802-11-wireless"]["ssid"][
                                            1
                                        ].decode()
                                    ),
                                    "security": network_properties[
                                        str(
                                            network_properties["802-11-wireless"][
                                                "security"
                                            ][1]
                                        )
                                    ]["key-mgmt"][1],
                                    "mode": network_properties["802-11-wireless"][
                                        "mode"
                                    ],
                                    "priority": network_properties["connection"].get(
                                        "autoconnect-priority", (None, None)
                                    )[1],
                                }
                                if network_properties["connection"]["type"][1]
                                == "802-11-wireless"
                                else None
                            ),
                            settings_list,
                        )
                    ),
                )
            )
            return _known_networks_parameters
        except Exception as e:
            logger.error(f"Caught exception while fetching saved networks: {e}")
        return []

    @staticmethod
    async def _get_settings(
        saved_connections: typing.List[dbusNm.NetworkConnectionSettings],
    ) -> typing.List[dbusNm.NetworkManagerConnectionProperties]:
        tasks = [sc.get_settings() for sc in saved_connections]
        return await asyncio.gather(*tasks, return_exceptions=False)

    def get_saved_networks_with_for(self) -> typing.List:
        """Get a list with the names and ids of all saved networks on the device.

        Returns:
            typing.List[dict]: List that contains the names and ids of all saved networks on the device.


        This implementation is equal to the klipper screen implementation, this one uses for loops and is simpler.
        https://github.com/KlipperScreen/KlipperScreen/blob/master/ks_includes/sdbus_nm.py Alfredo Monclues (alfrix) 2024
        """
        if not self.nm:
            return []
        try:
            saved_networks: list = []
            conn_future = asyncio.run_coroutine_threadsafe(
                dbusNm.NetworkManagerSettings(bus=self.system_dbus).list_connections(),
                self.loop,
            )

            connections = conn_future.result(timeout=2)

            # logger.debug(f"got connections from request {connections}")
            saved_cons = [
                dbusNm.NetworkConnectionSettings(bus=self.system_dbus, settings_path=c)
                for c in connections
            ]
            # logger.error(f"Getting saved networks with for: {conn_future}")

            sv_cons_settings_future = asyncio.run_coroutine_threadsafe(
                self._get_settings(saved_cons),
                self.loop,
            )

            settings_list = sv_cons_settings_future.result(timeout=2)

            for connection, conn in zip(connections, settings_list):
                if conn["connection"]["type"][1] == "802-11-wireless":
                    saved_networks.append(
                        {
                            "ssid": conn["802-11-wireless"]["ssid"][1].decode(),
                            "uuid": conn["connection"]["uuid"][1],
                            "security_type": conn[
                                str(conn["802-11-wireless"]["security"][1])
                            ]["key-mgmt"][1],
                            "connection_path": connection,
                            "mode": conn["802-11-wireless"]["mode"],
                        }
                    )
            return saved_networks
        except Exception as e:
            logger.error(f"Caught Exception while fetching saved networks: {e}")
        return []

    def get_saved_ssid_names(self) -> typing.List[str]:
        """Get a list with the current saved network ssid names

        Returns:
            typing.List[str]: List that contains the names of the saved ssid network names
        """
        try:
            _saved_networks = self.get_saved_networks_with_for()
            if not _saved_networks:
                return []
            return list(
                map(
                    lambda saved_network: (saved_network.get("ssid", None)),
                    _saved_networks,
                )
            )
        except BaseException as e:
            logger.error("Caught exception while getting saved SSID names %s", e)
        return []

    def is_known(self, ssid: str) -> bool:
        """Whether or not a network is known

        Args:
            ssid (str): The networks ssid

        Returns:
            bool: True if the network is known otherwise False
        """
        # saved_networks = asyncio.new_event_loop().run_until_complete(
        #     self.get_saved_networks_with_for()
        # )
        saved_networks = self.get_saved_networks_with_for()
        return any(net.get("ssid", "") == ssid for net in saved_networks)

    async def _add_wifi_network(
        self,
        ssid: str,
        psk: str,
        priority: ConnectionPriority = ConnectionPriority.LOW,
    ) -> dict:
        """Add new wifi connection

        Args:
            ssid (str): Network ssid.
            psk (str): Network password
            priority (ConnectionPriority, optional): Priority of the network connection. Defaults to ConnectionPriority.LOW.

        Raises:
            NotImplementedError: Network security type is not implemented

        Returns:
            dict: A dictionary containing the result of the operation
        """
        if not self.primary_wifi_interface:
            logger.debug("[add wifi network] no primary wifi interface ")
            return
        if self.primary_wifi_interface == "/":
            logger.debug("[add wifi network] no primary wifi interface ")
            return
        try:
            _available_networks = await self._get_available_networks()
            if not _available_networks:
                logger.debug("Networks not available cancelling adding network")
                return {"error": "No networks available"}
            if self.is_known(ssid):
                self.delete_network(ssid)
            if ssid in _available_networks.keys():
                target_network = _available_networks.get(ssid, {})
                if not target_network:
                    return {"error": "Network unavailable"}
                target_interface = (
                    await self.primary_wifi_interface.interface.get_async()
                )
                _properties: dbusNm.NetworkManagerConnectionProperties = {
                    "connection": {
                        "id": ("s", str(ssid)),
                        "uuid": ("s", str(uuid4())),
                        "type": ("s", "802-11-wireless"),
                        "interface-name": (
                            "s",
                            target_interface,
                        ),
                        "autoconnect": ("b", bool(True)),
                        "autoconnect-priority": (
                            "u",
                            priority.value,
                        ),  # We need an integer here
                    },
                    "802-11-wireless": {
                        "mode": ("s", "infrastructure"),
                        "ssid": ("ay", ssid.encode("utf-8")),
                    },
                    "ipv4": {"method": ("s", "auto")},
                    "ipv6": {"method": ("s", "auto")},
                }
                if "security" in target_network.keys():
                    _security_types = target_network.get("security")
                    if not _security_types:
                        return
                if not _security_types[0]:
                    return
                if (
                    dbusNm.AccessPointCapabilities.NONE != _security_types[-1]
                ):  # Normally on last index
                    _properties["802-11-wireless"]["security"] = (
                        "s",
                        "802-11-wireless-security",
                    )
                    if (
                        dbusNm.WpaSecurityFlags.P2P_WEP104
                        or dbusNm.WpaSecurityFlags.P2P_WEP40
                        or dbusNm.WpaSecurityFlags.BROADCAST_WEP104
                        or dbusNm.WpaSecurityFlags.BROADCAST_WEP40
                    ) in (_security_types[0] or _security_types[1]):
                        _properties["802-11-wireless-security"] = {
                            "key-mgmt": ("s", "none"),
                            "wep-key-type": ("u", 2),
                            "wep-key0": ("s", psk),
                            "auth-alg": ("s", "shared"),
                        }
                    elif (
                        dbusNm.WpaSecurityFlags.P2P_TKIP
                        or dbusNm.WpaSecurityFlags.BROADCAST_TKIP
                    ) in (_security_types[0] or _security_types[1]):
                        raise NotImplementedError(
                            "Security type P2P_TKIP OR BRADCAST_TKIP not supported"
                        )
                    elif (
                        dbusNm.WpaSecurityFlags.P2P_CCMP
                        or dbusNm.WpaSecurityFlags.BROADCAST_CCMP
                    ) in (_security_types[0] or _security_types[1]):
                        # * AES/CCMP WPA2
                        _properties["802-11-wireless-security"] = {
                            "key-mgmt": ("s", "wpa-psk"),
                            "auth-alg": ("s", "open"),
                            "psk": ("s", psk),
                            "pairwise": ("as", ["ccmp"]),
                        }
                    elif (dbusNm.WpaSecurityFlags.AUTH_PSK) in (
                        _security_types[0] or _security_types[1]
                    ):
                        # * AUTH_PSK -> WPA-PSK
                        _properties["802-11-wireless-security"] = {
                            "key-mgmt": ("s", "wpa-psk"),
                            "auth-alg": ("s", "open"),
                            "psk": ("s", psk),
                        }
                    elif dbusNm.WpaSecurityFlags.AUTH_802_1X in (
                        _security_types[0] or _security_types[1]
                    ):
                        # * 802.1x IEEE standard ieee802.1x
                        # Notes:
                        #   IEEE 802.1x standard used 8 to 64 passphrase hashed to derive
                        #   the actual key in the form of 64 hexadecimal character.
                        #
                        _properties["802-11-wireless-security"] = {
                            "key-mgmt": ("s", "wpa-eap"),
                            "wep-key-type": ("u", 2),
                            "wep-key0": ("s", psk),
                            "auth-alg": ("s", "shared"),
                        }
                    elif (dbusNm.WpaSecurityFlags.AUTH_SAE) in (
                        _security_types[0] or _security_types[1]
                    ):
                        # * SAE
                        # Notes:
                        #   The SAE is WPA3 so they use a passphrase of any length for authentication.
                        #
                        _properties["802-11-wireless-security"] = {
                            "key-mgmt": ("s", "sae"),
                            "auth-alg": ("s", "open"),
                            "psk": ("s", psk),
                        }
                    elif (dbusNm.WpaSecurityFlags.AUTH_OWE) in (
                        _security_types[0] or _security_types[1]
                    ):
                        # * OWE
                        _properties["802-11-wireless-security"] = {
                            "key-mgmt": ("s", "owe"),
                            "psk": ("s", psk),
                        }
                    elif (dbusNm.WpaSecurityFlags.AUTH_OWE_TM) in (
                        _security_types[0] or _security_types[1]
                    ):
                        # * OWE TM
                        raise NotImplementedError("AUTH_OWE_TM not supported")
                    elif (dbusNm.WpaSecurityFlags.AUTH_EAP_SUITE_B) in (
                        _security_types[0] or _security_types[1]
                    ):
                        # * EAP SUITE B
                        raise NotImplementedError("EAP SUITE B Auth not supported")
                    tasks = [
                        self.loop.create_task(
                            dbusNm.NetworkManagerSettings(
                                bus=self.system_dbus
                            ).add_connection(_properties)
                        ),
                        self.loop.create_task(self.nm.reload(0x0)),
                    ]
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    for result in results:
                        if isinstance(result, Exception):
                            if isinstance(
                                result,
                                dbusNm.exceptions.NmConnectionFailedError,
                            ):
                                logger.error(
                                    "Exception caught, could not connect to network: %s",
                                    str(result),
                                )
                                return {"error": f"Connection failed to {ssid}"}
                            if isinstance(
                                result,
                                dbusNm.exceptions.NmConnectionPropertyNotFoundError,
                            ):
                                logger.error(
                                    "Exception caught, network properties internal error: %s",
                                    str(result),
                                )
                                return {"error": "Network connection properties error"}
                            if isinstance(
                                result,
                                dbusNm.exceptions.NmConnectionInvalidPropertyError,
                            ):
                                logger.error(
                                    "Caught exception while adding new wifi connection: Invalid password: %s",
                                    str(result),
                                )
                                return {"error": "Invalid password"}
                            if isinstance(
                                result,
                                dbusNm.exceptions.NmSettingsPermissionDeniedError,
                            ):
                                logger.error(
                                    "Caught exception while adding new wifi connection: Permission Denied: %s",
                                    str(result),
                                )
                                return {"error": "Permission Denied"}
                        return {"state": "success"}
        except NotImplementedError:
            logger.error("Network security type not implemented")
            return {"error": "Network security type not implemented"}
        except Exception as e:
            logger.error(
                "Caught Exception Unable to add network connection : %s", str(e)
            )
            return {"error": "Unable to add network"}

    def add_wifi_network(
        self,
        ssid: str,
        psk: str,
        priority: ConnectionPriority = ConnectionPriority.MEDIUM,
    ) -> dict:
        """Add new wifi password `Synchronous`

        Args:
            ssid (str): Network ssid
            psk (str): Network password
            priority (ConnectionPriority, optional): Network priority. Defaults to ConnectionPriority.MEDIUM.

        Returns:
            dict: A dictionary containing the result of the operation
        """
        future = asyncio.run_coroutine_threadsafe(
            self._add_wifi_network(ssid, psk, priority), self.loop
        )
        return future.result(timeout=5)

    def disconnect_network(self) -> None:
        """Disconnect the active connection"""
        if not self.primary_wifi_interface:
            return
        if self.primary_wifi_interface == "/":
            return
        asyncio.run_coroutine_threadsafe(
            self.primary_wifi_interface.disconnect(), self.loop
        )

    def get_connection_path_by_ssid(self, ssid: str) -> typing.Union[str, None]:
        """Given a ssid, get the connection path, if it's saved

        Raises:
            ValueError: If the ssid was not of type string.

        Returns:
            str: connection path
        """
        if not isinstance(ssid, str):
            raise ValueError(
                f"SSID argument must be a string, inserted type is : {type(ssid)}"
            )
        _connection_path = None
        _saved_networks = self.get_saved_networks_with_for()
        if not _saved_networks:
            raise Exception(f"No network with ssid: {ssid}")
        if len(_saved_networks) == 0:
            raise Exception("There are no saved networks")
        for saved_network in _saved_networks:
            if saved_network["ssid"].lower() == ssid.lower():
                _connection_path = saved_network["connection_path"]
        return _connection_path

    def get_security_type_by_ssid(self, ssid: str) -> typing.Union[str, None]:
        """Get the security type for a saved network by its ssid.

        Args:
            ssid (str): SSID of a saved network

        Returns: None or str wit the security type
        """
        if not self.nm:
            return
        if not self.is_known(ssid):
            return
        _security_type: str = ""
        _saved_networks = self.get_saved_networks_with_for()
        for network in _saved_networks:
            if network["ssid"].lower() == ssid.lower():
                _security_type = network["security_type"]

        return _security_type

    def get_connection_signal_by_ssid(self, ssid: str) -> int:
        """Get the signal strength for a ssid

        Args:
            ssid (str): Ssid we wan't to scan

        Returns:
            int: the signal strength for that ssid
        """
        if not self.nm:
            return 0
        if not self.primary_wifi_interface:
            return 0
        if self.primary_wifi_interface == "/":
            return 0

        self.rescan_networks()

        dev_type = asyncio.run_coroutine_threadsafe(
            self.primary_wifi_interface.device_type.get_async(), self.loop
        )

        if dev_type.result(timeout=2) == dbusNm.enums.DeviceType.WIFI:
            # Get information on scanned networks:
            _aps: typing.List[dbusNm.AccessPoint] = list(
                map(
                    lambda ap_path: dbusNm.AccessPoint(
                        bus=self.system_dbus, point_path=ap_path
                    ),
                    asyncio.run_coroutine_threadsafe(
                        self.primary_wifi_interface.access_points.get_async(),
                        self.loop,
                    ).result(timeout=2),
                )
            )
            try:
                for ap in _aps:
                    if (
                        asyncio.run_coroutine_threadsafe(ap.ssid.get_async(), self.loop)
                        .result(timeout=2)
                        .decode("utf-8")
                        .lower()
                        == ssid.lower()
                    ):
                        return asyncio.run_coroutine_threadsafe(
                            ap.strength.get_async(), self.loop
                        ).result(timeout=2)
            except Exception:
                return 0
        return 0

    def connect_network(self, ssid: str) -> str:
        """Connect to a saved network given an ssid

        Raises:
            ValueError: Raised if the ssid argument is not of type string.
            Exception: Raised if there was an error while trying to connect.

        Returns:
            str: The active connection path, or a Message.
        """
        if not isinstance(ssid, str):
            raise ValueError(
                f"SSID argument must be a string, inserted type is : {type(ssid)}"
            )
        _connection_path = self.get_connection_path_by_ssid(ssid)
        if not _connection_path:
            raise Exception(f"No saved connection path for the SSID: {ssid}")
        try:
            if self.nm.primary_connection == _connection_path:
                raise Exception(f"Network connection already established with {ssid}")
            active_path = asyncio.run_coroutine_threadsafe(
                self.nm.activate_connection(str(_connection_path)), self.loop
            ).result(timeout=2)
            return active_path
        except Exception as e:
            raise Exception(
                f"Unknown error while trying to connect to {ssid} network: {e}"
            )

    async def _delete_network(self, settings_path) -> None:
        tasks = []
        tasks.append(
            self.loop.create_task(
                dbusNm.NetworkConnectionSettings(
                    bus=self.system_dbus, settings_path=str(settings_path)
                ).delete()
            )
        )

        tasks.append(
            self.loop.create_task(
                dbusNm.NetworkManagerSettings(bus=self.system_dbus).reload_connections()
            )
        )
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                raise Exception(f"Caught Exception while deleting network: {result}")

    def delete_network(self, ssid: str) -> None:
        """Deletes a saved network given a ssid

        Args:
            ssid (str): The networks ssid to be deleted

        ### `Should be refactored`
        Returns:
            typing.Dict: Status key with the outcome of the networks deletion.
        """
        if not isinstance(ssid, str):
            raise TypeError("SSID argument is of type string")
        if not self.is_known(ssid):
            logging.debug(f"No known network with SSID {ssid}")
            return
        try:
            self.deactivate_connection_by_ssid(ssid)
            _path = self.get_connection_path_by_ssid(ssid)
            task = self.loop.create_task(self._delete_network(_path))
            future = asyncio.gather(task, return_exceptions=True)
            results = future.result()
            for result in results:
                if isinstance(result, Exception):
                    raise Exception(result)
        except Exception as e:
            logging.debug(f"Caught Exception while deleting network {ssid}: {e}")

    def get_hotspot_ssid(self) -> str:
        """Get current hotspot ssid"""
        return self.hotspot_ssid

    def deactivate_connection(self, connection_path) -> None:
        """Deactivate a connection, by connection path"""
        if not self.nm:
            return
        if not self.primary_wifi_interface:
            return
        if self.primary_wifi_interface == "/":
            return
        try:
            future = asyncio.run_coroutine_threadsafe(
                self.nm.active_connections.get_async(), self.loop
            )
            active_connections = future.result(timeout=2)
            if connection_path in active_connections:
                task = self.loop.create_task(
                    self.nm.deactivate_connection(active_connection=connection_path)
                )
                future = asyncio.gather(task)
        except Exception as e:
            logger.error(
                f"Caught exception while deactivating network {connection_path}: {e}"
            )

    def deactivate_connection_by_ssid(self, ssid: str) -> None:
        """Deactivate connection by ssid"""
        if not self.nm:
            return
        if not self.primary_wifi_interface:
            return
        if self.primary_wifi_interface == "/":
            return

        try:
            _connection_path = self.get_connection_path_by_ssid(ssid)
            if not _connection_path:
                raise Exception(f"Network saved network with name {ssid}")
            self.deactivate_connection(_connection_path)
        except Exception as e:
            logger.error(f"Exception Caught while deactivating network {ssid}: {e}")

    def create_hotspot(
        self, ssid: str = "PrinterHotspot", password: str = "123456789"
    ) -> None:
        """Create hostpot

        Args:
            ssid (str, optional): Hotspot ssid. Defaults to "PrinterHotspot".
            password (str, optional): connection password. Defaults to "123456789".
        """
        if self.is_known(ssid):
            self.delete_network(ssid)
            logger.debug("old hotspot deleted")
        try:
            self.delete_network(ssid)
            # psk = hashlib.sha256(password.encode()).hexdigest()
            _properties: dbusNm.NetworkManagerConnectionProperties = {
                "connection": {
                    "id": ("s", str(ssid)),
                    "uuid": ("s", str(uuid4())),
                    "type": ("s", "802-11-wireless"),  # 802-3-ethernet
                    "interface-name": ("s", "wlan0"),
                },
                "802-11-wireless": {
                    "ssid": ("ay", ssid.encode("utf-8")),
                    "mode": ("s", "ap"),
                    "band": ("s", "bg"),
                    "channel": ("u", 6),
                    "security": ("s", "802-11-wireless-security"),
                },
                "802-11-wireless-security": {
                    "key-mgmt": ("s", "wpa-psk"),
                    "psk": ("s", password),
                    "pmf": ("u", 0),
                },
                "ipv4": {
                    "method": ("s", "shared"),
                },
                "ipv6": {"method": ("s", "ignore")},
            }

            tasks = [
                self.loop.create_task(
                    dbusNm.NetworkManagerSettings(bus=self.system_dbus).add_connection(
                        _properties
                    )
                ),
                self.loop.create_task(self.nm.reload(0x0)),
            ]

            self.loop.run_until_complete(
                asyncio.gather(*tasks, return_exceptions=False)
            )
            for task in tasks:
                self.loop.run_until_complete(task)

        except Exception as e:
            logging.error(f"Caught Exception while creating hotspot: {e}")

    def set_network_priority(
        self, ssid: str, priority: ConnectionPriority = ConnectionPriority.LOW
    ) -> None:
        """Set network priority

        Args:
            ssid (str): connection ssid
            priority (ConnectionPriority, optional): Priority. Defaults to ConnectionPriority.LOW.
        """
        if not self.nm:
            return
        if not self.is_known(ssid):
            return
        self.update_connection_settings(ssid=ssid, priority=priority.value)

    def update_connection_settings(
        self,
        ssid: str,
        password: typing.Optional["str"] = None,
        new_ssid: typing.Optional["str"] = None,
        priority: int = 20,
    ) -> None:
        """Update the settings for a connection with a specified ssid and or a password

        Args:
            ssid (str | None): SSID of the network we want to update
            password
        Returns:
            typing.Dict: status dictionary with possible keys "error" and "status"
        """

        if not self.nm:
            raise Exception("NetworkManager Missing")
        if not self.is_known(str(ssid)):
            raise Exception("%s network is not known, cannot update", ssid)

        _connection_path = self.get_connection_path_by_ssid(str(ssid))
        if not _connection_path:
            raise Exception("No saved connection with the specified ssid")
        try:
            con_settings = dbusNm.NetworkConnectionSettings(
                bus=self.system_dbus, settings_path=str(_connection_path)
            )
            properties = asyncio.run_coroutine_threadsafe(
                con_settings.get_settings(), self.loop
            ).result(timeout=2)
            if new_ssid:
                properties["connection"]["id"] = ("s", str(new_ssid))
                properties["802-11-wireless"]["ssid"] = (
                    "ay",
                    new_ssid.encode("utf-8"),
                )
            if password:
                # pwd = hashlib.sha256(password.encode()).hexdigest()
                properties["802-11-wireless-security"]["psk"] = (
                    "s",
                    str(password.encode("utf-8")),
                )

            if priority != 0:
                properties["connection"]["autoconnect-priority"] = (
                    "u",
                    priority,
                )

            tasks = [
                self.loop.create_task(con_settings.update(properties)),
                self.loop.create_task(self.nm.reload(0x0)),
            ]
            self.loop.run_until_complete(
                asyncio.gather(*tasks, return_exceptions=False)
            )

            if ssid == self.hotspot_ssid and new_ssid:
                self.hotspot_ssid = new_ssid
            if password != self.hotspot_password and password:
                self.hotspot_password = password
        except Exception as e:
            logger.error("Caught Exception while updating network: %s", e)
