import asyncio
import enum
import hashlib
import logging
import threading
import typing
from uuid import uuid4

import sdbus
from PyQt6 import QtCore
from sdbus_async.networkmanager import (
    AccessPoint,
    AccessPointCapabilities,
    ActiveConnection,
    IPv4Config,
    NetworkConnectionSettings,
    NetworkDeviceGeneric,
    NetworkDeviceWired,
    NetworkDeviceWireless,
    NetworkManager,
    NetworkManagerConnectionProperties,
    NetworkManagerConnectivityState,
    NetworkManagerSettings,
    NetworkManagerState,
    WpaSecurityFlags,
    enums,
)
from sdbus_async.networkmanager.enums import (
    NetworkManagerConnectivityState,
    NetworkManagerState,
)
from sdbus_async.networkmanager.exceptions import (
    NmConnectionFailedError,
    NmConnectionInvalidPropertyError,
    NmConnectionPropertyNotFoundError,
)

logger = logging.getLogger("logs/BlocksScreen.log")


class NetworkManagerRescanError(Exception):
    """Exception raised when rescanning the network fails."""

    def __init__(self, error):
        super(NetworkManagerRescanError, self).__init__()
        self.error = error


class SdbusNetworkManagerAsync(QtCore.QObject):
    # class SdbusNetworkManagerAsync:
    class ConnectionPriority(enum.Enum):
        HIGH = 90
        MEDIUM = 50
        LOW = 0

    nm_state_change: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="nm-state-changed"
    )
    nm_properties_change: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(str, name="nm-properties-changed")
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
        # Network Manager dbus
        self.system_dbus = sdbus.sd_bus_open_system()
        if not self.system_dbus:
            logger.error("No dbus found, async network monitor exiting")
            self.close()
            return
        sdbus.set_default_bus(self.system_dbus)
        self.nm = NetworkManager()
        self.listener_thread.start()
        if self.listener_thread.is_alive():
            logger.info(
                f"Sdbus NetworkManager Monitor Thread {self.listener_thread.name} Running"
            )

        self.hotspot_ssid: str = "PrinterHotspot"
        self.hotspot_password: str = hashlib.sha256(
            "123456789".encode()
        ).hexdigest()

        self.check_connectivity()

        self.available_wired_interfaces = self.get_wired_interfaces()
        self.available_wireless_interfaces = self.get_wireless_interfaces()

        wireless_interfaces: typing.List[NetworkDeviceWireless] = (
            self.get_wireless_interfaces()
        )
        self.primary_wifi_interface: typing.Optional[NetworkDeviceWireless] = (
            wireless_interfaces[0] if wireless_interfaces else None
        )
        wired_interfaces: typing.List[NetworkDeviceWired] = (
            self.get_wired_interfaces()
        )
        self.primary_wired_interface: typing.Optional[NetworkDeviceWired] = (
            wired_interfaces[0] if wired_interfaces else None
        )

        if not self.is_known(self.hotspot_ssid):
            self.create_hotspot(self.hotspot_ssid, self.hotspot_password)

        if self.primary_wifi_interface:
            self.rescan_networks()

    def _listener_run_loop(self) -> None:
        try:
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(
                asyncio.gather(self.listener_monitor())
            )

        except Exception as e:
            logging.error(f"Exception on loop coroutine: {e}")

    async def _end_tasks(self) -> None:
        for task in self.listener_task_queue:
            task.cancel()
        await asyncio.gather(*self.listener_task_queue, return_exceptions=True)

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
        try:
            self._listeners_running = True

            self.listener_task_queue.append(
                self.loop.create_task(self._nm_state_listener())
            )
            self.listener_task_queue.append(
                self.loop.create_task(self._nm_properties_listener())
            )
            asyncio.gather(*self.listener_task_queue)
            await self.stop_listener_event.wait()
        except Exception as e:
            logging.error(
                f"Exception on listener monitor produced coroutine: {e}"
            )

    async def _nm_state_listener(self) -> None:
        while self._listeners_running:
            try:
                async for state in self.nm.state_changed:
                    enum_state = NetworkManagerState(state)
                    self.nm_state_change.emit(enum_state.name)
            except Exception as e:
                logging.error(
                    f"Exception on Network Manager state listener: {e}"
                )

    async def _nm_properties_listener(self) -> None:
        while self._listeners_running:
            try:
                logging.debug("Listening for Network Manager state change")
                async for properties in self.nm.properties_changed:
                    self.nm_properties_change.emit(properties)
                    ...
            except Exception as e:
                logging.error(
                    f"Exception on Network Manager state listener: {e}"
                )

    def check_nm_state(self) -> typing.Union[str, None]:
        if not self.nm:
            return
        future = asyncio.run_coroutine_threadsafe(
            self.nm.state.get_async(), self.loop
        )
        try:
            state_value = future.result(timeout=2)
            return str(NetworkManagerState(state_value).name)
        except Exception as e:
            logging.error(
                f"Exception while fetching Network Monitor State: {e}"
            )
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
            return NetworkManagerConnectivityState(connectivity).name
        except Exception as e:
            logging.error(
                f"Exception while fetching Network Monitor Connectivity State: {e}"
            )
            return ""

    def check_wifi_interface(self) -> bool:
        return bool(self.primary_wifi_interface)

    def get_available_interfaces(self) -> typing.List[str]:
        """Gets the names of all available interfaces

        Returns:
            typing.List[str]: List of strings with the available names of all interfaces
        """
        try:
            future = asyncio.run_coroutine_threadsafe(
                self.nm.get_devices(), self.loop
            )
            devices = future.result(timeout=2)
            interfaces = []
            for device in devices:
                interface_future = asyncio.run_coroutine_threadsafe(
                    NetworkDeviceGeneric(
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
                logger.error(
                    f"Exception Caught when toggling network : {result}"
                )
        return

    def disable_networking(self) -> None:
        if not (self.primary_wifi_interface and self.primary_wired_interface):
            return
        if (
            self.primary_wifi_interface == "/"
            and self.primary_wired_interface == "/"
        ):
            return
        asyncio.run_coroutine_threadsafe(
            self._toggle_networking(False), self.loop
        )

    def activate_networking(self) -> None:
        if not (self.primary_wifi_interface and self.primary_wired_interface):
            return
        if (
            self.primary_wifi_interface == "/"
            and self.primary_wired_interface == "/"
        ):
            return
        asyncio.run_coroutine_threadsafe(
            self._toggle_networking(True), self.loop
        )

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
                self.disconnect_network()
            if self.is_known(self.hotspot_ssid):
                self.connect_network(self.hotspot_ssid)
                asyncio.gather(self.nm.reload(0x0), return_exceptions=False)

                if self.nm.check_connectivity() == (
                    NetworkManagerConnectivityState.FULL
                    | NetworkManagerConnectivityState.LIMITED
                ):
                    logging.debug(f"Hotspot AP {self.hotspot_ssid} up!")

                return
            if old_ssid:
                self.connect_network(old_ssid)
                return
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")

    def hotspot_enabled(self) -> typing.Optional["bool"]:
        """Returns a boolean indicating whether the device hotspot is on or not .

        Returns:
            bool: True if Hotspot is activated, False otherwise.
        """
        # REFACTOR: untested for all cases
        return bool(self.hotspot_ssid == self.get_current_ssid())

    def get_wired_interfaces(self) -> typing.List[NetworkDeviceWired]:
        """get_wired_interfaces Get only the names for the available wired (Ethernet) interfaces.

        Returns:
            typing.List[str]: List containing the names of all wired(Ethernet) interfaces.
        """
        devs_future = asyncio.run_coroutine_threadsafe(
            self.nm.get_devices(), self.loop
        )
        devices = devs_future.result(timeout=2)

        return list(
            map(
                lambda path: NetworkDeviceWired(path),
                filter(
                    lambda path: path,
                    filter(
                        lambda device: asyncio.run_coroutine_threadsafe(
                            NetworkDeviceGeneric(
                                bus=self.system_dbus, device_path=device
                            ).device_type.get_async(),
                            self.loop,
                        ).result(timeout=2)
                        == enums.DeviceType.ETHERNET,
                        devices,
                    ),
                ),
            )
        )

    def get_wireless_interfaces(
        self,
    ) -> typing.List[NetworkDeviceWireless]:
        """get_wireless_interfaces Get only the names of wireless interfaces.

        Returns:
            typing.List[str]: A list containing the names of wireless interfaces.
        """
        # Each interface type has a device flag that is exposed in enums.DeviceType.<device such as Ethernet or Wifi>
        devs_future = asyncio.run_coroutine_threadsafe(
            self.nm.get_devices(), self.loop
        )
        devices = devs_future.result(timeout=2)
        return list(
            map(
                lambda path: NetworkDeviceWireless(
                    bus=self.system_dbus, device_path=path
                ),
                filter(
                    lambda path: path,
                    filter(
                        lambda device: asyncio.run_coroutine_threadsafe(
                            NetworkDeviceGeneric(
                                bus=self.system_dbus, device_path=device
                            ).device_type.get_async(),
                            self.loop,
                        ).result(timeout=3)
                        == enums.DeviceType.WIFI,
                        devices,
                    ),
                ),
            )
        )

    async def _gather_ssid(self) -> str:
        if not self.nm:
            return ""
        primary_con = await self.nm.primary_connection.get_async()
        if primary_con == "/":
            logger.debug("No primary connection")
            return ""
        active_connection = ActiveConnection(
            bus=self.system_dbus, connection_path=primary_con
        )
        if not active_connection:
            logger.debug("Active connection is none my man")
            return ""
        con = await active_connection.connection.get_async()
        con_settings = NetworkConnectionSettings(
            bus=self.system_dbus, settings_path=con
        )
        settings = await con_settings.get_settings()
        return str(settings["802-11-wireless"]["ssid"][1].decode())

    def get_current_ssid(self) -> str:
        try:
            future = asyncio.run_coroutine_threadsafe(
                self._gather_ssid(), self.loop
            )
            return future.result(timeout=5)
        except Exception as e:
            logging.info(f"Unexpected error occurred: {e}")
            return ""

    def get_current_ip_addr(self) -> str:
        """Get the current connection ip address.
        Returns:
            str: A string containing the current ip address
        """
        primary_con_fut = asyncio.run_coroutine_threadsafe(
            self.nm.primary_connection.get_async(), self.loop
        )
        primary_con = primary_con_fut.result(timeout=2)
        if primary_con == "/":
            logging.info("There is no NetworkManager active connection.")
            return ""

        _device_ip4_conf_path = ActiveConnection(
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
        ip4_conf = IPv4Config(
            bus=self.system_dbus, ip4_path=ip4_conf_future.result(timeout=2)
        )
        addr_data_fut = asyncio.run_coroutine_threadsafe(
            ip4_conf.address_data.get_async(), self.loop
        )
        addr_data = addr_data_fut.result(timeout=2)
        return [address_data["address"][1] for address_data in addr_data][0]

    async def _gather_primary_interface(
        self,
    ) -> typing.Union[
        NetworkDeviceWired, NetworkDeviceWireless, typing.Tuple, str
    ]:
        if not self.nm:
            return ""

        primary_connection = await self.nm.primary_connection.get_async()
        if not primary_connection:
            return ""
        if primary_connection == "/":
            if (
                self.primary_wifi_interface
                and self.primary_wifi_interface != "/"
            ):
                return self.primary_wifi_interface
            elif (
                self.primary_wired_interface
                and self.primary_wired_interface != "/"
            ):
                return self.primary_wired_interface
            else:
                "/"

        primary_conn_type = await self.nm.primary_connection_type.get_async()
        active_connection = ActiveConnection(
            bus=self.system_dbus, connection_path=primary_connection
        )
        gateway = await active_connection.devices.get_async()
        device_interface = await NetworkDeviceGeneric(
            bus=self.system_dbus, device_path=gateway[0]
        ).interface.get_async()
        return (device_interface, primary_connection, primary_conn_type)

    def get_primary_interface(
        self,
    ) -> typing.Union[
        NetworkDeviceWired, NetworkDeviceWireless, typing.Tuple, str
    ]:
        """Get the primary interface,
            If a there is a connection, returns the interface that is being currently used.

            If there is no connection and wifi is available return de wireless interface.

            If there is no wireless interface and no active connection return the first wired interface that is not (lo).


            ### `TODO: Completely blocking and should be refactored`
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
            task = self.loop.create_task(
                self.primary_wifi_interface.request_scan({})
            )
            results = await asyncio.gather(task, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    raise NetworkManagerRescanError(
                        f"Exception caught: {result}"
                    )
                return
        except Exception as e:
            logger.error(f"Exception caught, network scan failed: {e}")
            return

    def rescan_networks(self) -> None:
        """Scan for available networks."""
        future = asyncio.run_coroutine_threadsafe(self._rescan(), self.loop)
        return future.result(timeout=2)

    async def _get_network_info(self, ap: AccessPoint) -> typing.Tuple:
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
                "BSSID": bssid,
            },
        )

    async def _gather_networks(self, aps) -> typing.Dict:
        try:
            results = await asyncio.gather(
                *(
                    self.loop.create_task(self._get_network_info(ap))
                    for ap in aps
                ),
                return_exceptions=True,
            )
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Error retrieving network info : {result}")
            return dict(results)
        except Exception as e:
            logger.error(f"Exception while gathering AP information: {e}")
        logger.debug(
            "Successfully gathered available access point information"
        )
        return {}

    async def _get_available_networks(self) -> typing.Dict:
        if not self.primary_wifi_interface:
            return {"error": "No wifi interface found"}
        if self.primary_wifi_interface == "/":
            return {"error": "No wifi interface found"}
        await self._rescan()
        try:
            last_scan = await self.primary_wifi_interface.last_scan.get_async()
            if last_scan != -1:
                primary_wifi_dev_type = (
                    await self.primary_wifi_interface.device_type.get_async()
                )
                if primary_wifi_dev_type == enums.DeviceType.WIFI:
                    try:
                        aps = await self.primary_wifi_interface.get_all_access_points()
                        _aps: typing.List[AccessPoint] = list(
                            map(
                                lambda ap_path: AccessPoint(
                                    bus=self.system_dbus, point_path=ap_path
                                ),
                                aps,
                            )
                        )
                        task = self.loop.create_task(
                            self._gather_networks(_aps)
                        )
                        results = await asyncio.gather(
                            task, return_exceptions=True
                        )
                        for result in results:
                            if isinstance(result, Exception):
                                logger.error(
                                    f"There was an exception {result}"
                                )
                                return {}
                            else:
                                return dict(result)
                    except Exception as e:
                        logger.error(
                            f"Exception Caught on gathering available networks : {e}"
                        )
            return {}
        except Exception as e:
            logger.error(f"Exception while gathering access points: {e}")
        return {"error": "No available networks"}

    def get_available_networks(self) -> typing.Dict:
        future = asyncio.run_coroutine_threadsafe(
            self._get_available_networks(), self.loop
        )
        return future.result(timeout=1999)

    async def _get_security_type(self, ap: AccessPoint) -> typing.Tuple:
        """Get the security type from a network AccessPoint

        Args:
            ap (AccessPoint): The AccessPoint of the network.

        Returns:
            typing.Tuple: A Tuple containing all the flags about the WpaSecurityFlags ans AccessPointCapabilities
            - `(flags, wpa_flags, rsn_flags)`



        Check: For more information about the flags
            :py:class:`WpaSecurityFlags` and `ÀccessPointCapabilities` from :py:module:`python-sdbus-networkmanager.enums`
        """
        if not ap:
            return

        _rsn_flag_task = self.loop.create_task(ap.rsn_flags.get_async())
        _wpa_flag_task = self.loop.create_task(ap.wpa_flags.get_async())
        _sec_flags_task = self.loop.create_task(ap.flags.get_async())

        result = await asyncio.gather(
            _rsn_flag_task, _wpa_flag_task, _sec_flags_task
        )
        _rsn, _wpa, _sec = result
        if len(AccessPointCapabilities(_sec)) == 0:
            return ("Open", "")
        return (
            WpaSecurityFlags(_rsn),
            WpaSecurityFlags(_wpa),
            AccessPointCapabilities(_sec),
        )

    def get_saved_networks(self) -> typing.List[typing.Optional[typing.Dict]]:
        """get_saved_networks Gets a list with the names and ids of all saved networks on the device.

        Returns:
            typing.List[dict] | None: List that contains the names and ids of all saved networks on the device.



        I admit that this implementation is way to complicated, I don't even think it's great on memory and time, but i didn't use for loops so mission achieved.
        """
        if not self.nm:
            return [{"error": "No network manager"}]

        _connections: typing.List[str] = asyncio.run_coroutine_threadsafe(
            NetworkManagerSettings(bus=self.system_dbus).list_connections(),
            self.loop,
        ).result()

        asyncio.gather().result()
        # _network_settings: typing.List[NetworkManagerConnectionProperties] =

        saved_cons = list(
            map(
                lambda connection: NetworkConnectionSettings(
                    bus=self.system_dbus, settings_path=connection
                ),
                _connections,
            )
        )

        sv_cons_settings_future = asyncio.run_coroutine_threadsafe(
            self._get_settings(saved_cons),
            self.loop,
        )
        settings_list = sv_cons_settings_future.result(timeout=2)
        _known_networks_parameters: typing.List[
            typing.Optional[typing.Dict]
        ] = list(
            filter(
                lambda network_entry: network_entry is not None,
                list(
                    map(
                        lambda network_properties: (
                            {
                                "ssid": network_properties["802-11-wireless"][
                                    "ssid"
                                ][1].decode(),
                                "uuid": network_properties["connection"][
                                    "uuid"
                                ][1],
                                "signal": 0
                                + self.get_connection_signal_by_ssid(
                                    network_properties["802-11-wireless"][
                                        "ssid"
                                    ][1].decode()
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

    @staticmethod
    async def _get_settings(
        saved_connections: typing.List[NetworkConnectionSettings],
    ):
        tasks = [sc.get_settings() for sc in saved_connections]
        return await asyncio.gather(*tasks)

    def get_saved_networks_with_for(self) -> typing.List:
        """Get a list with the names and ids of all saved networks on the device.

        Returns:
            typing.List[dict]: List that contains the names and ids of all saved networks on the device.


        This implementation is equal to the klipper screen implementation, this one uses for loops and is simpler.
        https://github.com/KlipperScreen/KlipperScreen/blob/master/ks_includes/sdbus_nm.py Alfredo Monclues (alfrix) 2024
        """
        if not self.nm:
            return []
        saved_networks: list = []
        conn_future = asyncio.run_coroutine_threadsafe(
            NetworkManagerSettings(bus=self.system_dbus).list_connections(),
            self.loop,
        )
        connections = conn_future.result(timeout=2)
        saved_cons = [
            NetworkConnectionSettings(bus=self.system_dbus, settings_path=c)
            for c in connections
        ]

        sv_cons_settings_future = asyncio.run_coroutine_threadsafe(
            self._get_settings(saved_cons),
            self.loop,
        )

        settings_list = sv_cons_settings_future.result(timeout=2)

        for connection, conn in zip(connections, settings_list):
            if conn["connection"]["type"][1] == "802-11-wireless":
                saved_networks.append(
                    {
                        "SSID": conn["802-11-wireless"]["ssid"][1].decode(),
                        "UUID": conn["connection"]["uuid"][1],
                        "SECURITY_TYPE": conn[
                            str(conn["802-11-wireless"]["security"][1])
                        ]["key-mgmt"][1],
                        "CONNECTION_PATH": connection,
                        "MODE": conn["802-11-wireless"]["mode"],
                    }
                )
        return saved_networks

    def get_saved_ssid_names(self) -> typing.List[str]:
        """Get a list with the current saved network ssid names

        Returns:
            typing.List[str]: List that contains the names of the saved ssid network names
        """
        _saved_networks = self.get_saved_networks_with_for()
        if not _saved_networks:
            return []
        return list(
            map(
                lambda saved_network: (saved_network.get("SSID", None)),
                _saved_networks,
            )
        )

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
        return any(net.get("SSID", "") == ssid for net in saved_networks)

    async def _add_wifi_network(
        self,
        ssid: str,
        psk: str,
        priority: ConnectionPriority = ConnectionPriority.LOW,
    ) -> typing.Dict:
        """Add and save a new wifi network. `Asynchronous`

        Args:
            ssid (str): Network ssid
            psk (str): Network password
            priority (int, optional): Network connection priority. Defaults to ConnectionPriority.LOW.

        Raises:
            NotImplementedError:


        Returns:
            typing.Dict: Dictionary with a status key that reports whether or not the connection was saved and connected.

            On the returned dictionary a key value "error" can appear if an error occurred, the value will say what the error was.
            "exception"
        """
        if not self.primary_wifi_interface:
            return {"status": "error", "msg": "No available interface"}
        if self.primary_wifi_interface == "/":
            return {"status": "error", "msg": "No vailable interface"}

        psk = hashlib.sha256(psk.encode()).hexdigest()

        _available_networks = await self._get_available_networks()

        if "error" in _available_networks.keys():
            return {"status": "error", "msg": "No available networks"}

        if self.is_known(ssid):
            self.delete_network(ssid)

        if ssid in _available_networks.keys():
            target_network = _available_networks.get(ssid, {})
            if not target_network:
                return {"status": "error", "msg": "No available networks"}
            target_interface = (
                await self.primary_wifi_interface.interface.get_async()
            )
            _properties: NetworkManagerConnectionProperties = {
                "connection": {
                    "id": ("s", ssid),
                    "uuid": ("s", str(uuid4())),
                    "type": ("s", "802-11-wireless"),
                    "interface-name": (
                        "s",
                        target_interface,
                    ),
                    "autoconnect": ("b", bool(True)),
                    "autoconnect-priority": ("u", priority),
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
                    return {
                        "status": "error",
                        "msg": "No security type for network, stopping",
                    }
            if not _security_types[0]:
                return {"status": "error", "msg": "Unknown security type"}

            if not AccessPointCapabilities.NONE != _security_types[0]:
                _properties["802-11-wireless"]["security"] = (
                    "s",
                    "802-11-wireless-security",
                )
                if (
                    WpaSecurityFlags.P2P_WEP104
                    or WpaSecurityFlags.P2P_WEP40
                    or WpaSecurityFlags.BROADCAST_WEP104
                    or WpaSecurityFlags.BROADCAST_WEP40
                ) in (_security_types[1] or _security_types[2]):
                    _properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "none"),
                        "wep-key-type": ("u", 2),
                        "wep-key0": ("s", psk),
                        "auth-alg": ("s", "shared"),
                    }
                elif (
                    WpaSecurityFlags.P2P_TKIP
                    or WpaSecurityFlags.BROADCAST_TKIP
                ) in (_security_types[1] or _security_types[2]):
                    return {
                        "status": "error",
                        "msg": "Security type P2P_TKIP OR BRADCAST_TKIP not supported",
                    }
                elif (
                    WpaSecurityFlags.P2P_CCMP
                    or WpaSecurityFlags.BROADCAST_CCMP
                ) in (_security_types[1] or _security_types[2]):
                    # * AES/CCMP WPA2
                    _properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "wpa-psk"),
                        "psk": ("s", psk),
                        "pairwise": ("as", ["ccmp"]),
                    }

                elif (WpaSecurityFlags.AUTH_PSK) in (
                    _security_types[1] or _security_types[2]
                ):
                    # * AUTH_PSK -> WPA-PSK
                    _properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "wpa-psk"),
                        "psk": ("s", psk),
                    }
                elif WpaSecurityFlags.AUTH_802_1X in (
                    _security_types[1] or _security_types[2]
                ):
                    # * 802.1x IEEE standard
                    # Notes:
                    #   IEEE 802.1x standard used 8 to 64 passphrase hashed to derive
                    #   the actual key in the form of 64 hexadecimal character.
                    #
                    _properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "ieee802.1x"),
                        "wep-key-type": ("u", 2),
                        "wep-key0": ("s", psk),
                        "auth-alg": ("s", "shared"),
                    }
                elif (WpaSecurityFlags.AUTH_SAE) in (
                    _security_types[1] or _security_types[2]
                ):
                    # * SAE
                    # Notes:
                    #   The SAE is WPA3 so they use a passphrase of any length for authentication.
                    #
                    _properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "sae"),
                        "psk": ("s", psk),
                    }
                elif (WpaSecurityFlags.AUTH_OWE) in (
                    _security_types[1] or _security_types[2]
                ):
                    # * OWE
                    _properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "owe"),
                        "psk": ("s", psk),
                    }
                elif (WpaSecurityFlags.AUTH_OWE_TM) in (
                    _security_types[1] or _security_types[2]
                ):
                    # * OWE TM
                    raise NotImplementedError("AUTH_OWE_TM not supported")
                elif (WpaSecurityFlags.AUTH_EAP_SUITE_B) in (
                    _security_types[1] or _security_types[2]
                ):
                    # * EAP SUITE B
                    raise NotImplementedError("EAP SUITE B Auth not supported")

                try:
                    tasks = []
                    tasks.append(
                        self.loop.create_task(
                            NetworkManagerSettings(
                                bus=self.system_dbus
                            ).add_connection(_properties)
                        )
                    )
                    tasks.append(
                        self.loop.create_task(
                            NetworkManagerSettings(
                                bus=self.system_dbus
                            ).reload_connections()
                        )
                    )
                    results = await asyncio.gather(
                        *tasks, return_exceptions=True
                    )
                    for result in results:
                        if isinstance(result, Exception):
                            if isinstance(result, NmConnectionFailedError):
                                logger.error(
                                    f"Exception caught, could not connect to network: {result}"
                                )
                            if isinstance(
                                result, NmConnectionPropertyNotFoundError
                            ):
                                logger.error(
                                    f"Exception caught, network properties internal error: {result}"
                                )

                            return {
                                "status": "error",
                                "msg": f"Caught Exception Unable to add network connection {result}",
                            }
                        return {"status": "success"}
                except Exception as e:
                    logger.error(f"Unexpected error while adding network: {e}")
        return {"status": "failure", "msg": "Unable to add network connection"}

    def add_wifi_network(
        self,
        ssid: str,
        psk: str,
        priority: ConnectionPriority = ConnectionPriority.LOW,
    ) -> typing.Dict:
        """Add and Save a network to the device. `Synchronous`

        Args:
            ssid (str): Networks SSID
            psk (str): Networks password

        Raises:
            NotImplementedError: Some network security types are not yet available so there is no way to connect to them.

        Returns:
            typing.Dict: Dictionary with a status key that reports whether or not the connection was saved and connected.

            On the returned dictionary a key value "error" can appear if an error occurred, the value will say what the error was.
            "exception"
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

    def get_connection_path_by_ssid(
        self, ssid: str
    ) -> typing.Union[str, None]:
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
            return "There are no saved networks, must add a new network connection first."

        if len(_saved_networks) == 0:
            return "There are no saved networks, must add a new network connection first."
        for saved_network in _saved_networks:
            if saved_network["SSID"].lower() == ssid.lower():
                _connection_path = saved_network["CONNECTION_PATH"]

        return _connection_path

    def get_security_type_by_ssid(self, ssid: str) -> str:
        """Get the security type for a saved network by its ssid.

        Args:
            ssid (str): SSID of a saved network

        Returns:
            str | typing.Dict: _description_
        """
        if not self.nm:
            return ""
        if not self.is_known(ssid):
            return ""
        _security_type: str = ""
        _saved_networks = self.get_saved_networks_with_for()
        for network in _saved_networks:
            if network["SSID"].lower() == ssid.lower():
                _security_type = network["SECURITY_TYPE"]

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

        if dev_type.result(timeout=2) == enums.DeviceType.WIFI:
            # Get information on scanned networks:
            _aps: typing.List[AccessPoint] = list(
                map(
                    lambda ap_path: AccessPoint(
                        bus=self.system_dbus, point_path=ap_path
                    ),
                    asyncio.run_coroutine_threadsafe(
                        self.primary_wifi_interface.access_points.get_async(),
                        self.loop,
                    ).result(timeout=2),
                )
            )
            for ap in _aps:
                if (
                    asyncio.run_coroutine_threadsafe(
                        ap.ssid.get_async(), self.loop
                    )
                    .result(timeout=2)
                    .decode("utf-8")
                    .lower()
                    == ssid.lower()
                ):
                    return asyncio.run_coroutine_threadsafe(
                        ap.strength.get_async(), self.loop
                    ).result(timeout=2)

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
            return f"No saved connection path for the SSID: {ssid}"
        try:
            if self.nm.primary_connection == _connection_path:
                return f"Network connection already established with {ssid} "

            active_path = asyncio.run_coroutine_threadsafe(
                self.nm.activate_connection(str(_connection_path)), self.loop
            ).result(timeout=2)
            # active_path = self.nm.activate_connection(str(_connection_path))

        except Exception as e:
            raise Exception(
                f"Unknown error while trying to connect to {ssid} network: {e}"
            )
        return active_path

    async def _delete_network(self, settings_path) -> None:
        tasks = []
        tasks.append(
            self.loop.create_task(
                NetworkConnectionSettings(
                    bus=self.system_dbus, settings_path=str(settings_path)
                ).delete()
            )
        )

        tasks.append(
            self.loop.create_task(
                NetworkManagerSettings(
                    bus=self.system_dbus
                ).reload_connections()
            )
        )
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.error(
                    f"Caught Exception while deleting network: {result}"
                )
            return
        return

    def delete_network(self, ssid: str) -> typing.Union[typing.Dict, None]:
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
        _path = self.get_connection_path_by_ssid(ssid)
        try:
            task = self.loop.create_task(self._delete_network(_path))
            asyncio.gather(task, return_exceptions=False)
            return {"status": "success"}
        except Exception as e:
            logging.debug(f"Unexpected exception detected: {e}")
            return {"status": "error"}

    def get_hotspot_ssid(self) -> str:
        return self.hotspot_ssid

    def deactivate_connection(self, connection_path) -> None:
        if not self.nm:
            return
        if not self.primary_wifi_interface:
            return
        if self.primary_wifi_interface == "/":
            return
        asyncio.run_coroutine_threadsafe(
            self.nm.deactivate_connection(active_connection=connection_path),
            self.loop,
        )

    def deactivate_connection_by_ssid(self, ssid: str):
        if not self.nm:
            return
        if not self.primary_wifi_interface:
            return
        if self.primary_wifi_interface == "/":
            return
        _connection_path = self.get_connection_path_by_ssid(ssid)
        if not _connection_path:
            return f"No saved connection path for the SSID: {ssid}"
        try:
            self.deactivate_connection(_connection_path)
        except Exception as e:
            logger.error(
                f"Exception Caught while deactivating network {ssid}: {e}"
            )

    def create_hotspot(
        self, ssid: str = "PrinterHotspot", password: str = "123456789"
    ) -> typing.Dict:
        self.delete_network(ssid)
        psk = hashlib.sha256(password.encode()).hexdigest()
        properties: NetworkManagerConnectionProperties = {
            "connection": {
                "id": ("s", str(ssid)),
                "uuid": ("s", str(uuid4())),
                "type": ("s", "802-11-wireless"),  # 802-3-ethernet
                "autoconnect": ("b", bool(True)),
                "interface-name": ("s", "wlan0"),
            },
            "802-11-wireless": {
                "ssid": ("ay", ssid.encode("utf-8")),
                "mode": ("s", "ap"),
                "band": ("s", "bg"),
                "channel": ("u", 1),
                "security": ("s", "802-11-wireless-security"),
                "hidden": ("b", bool(False)),
            },
            "802-11-wireless-security": {
                "key-mgmt": ("s", "wpa-psk"),
                "psk": ("s", str(psk)),
                "pmf": ("u", 1),
                "pairwise": ("as", ["ccmp"]),
            },
            "ipv4": {
                "method": ("s", "shared"),
            },
            "ipv6": {"method": ("s", "ignore")},
        }

        try:
            tasks = []
            tasks.append(
                self.loop.create_task(
                    NetworkManagerSettings(
                        bus=self.system_dbus
                    ).add_connection(properties),
                )
            )
            tasks.append(
                self.loop.create_task(
                    NetworkManagerSettings(
                        bus=self.system_dbus
                    ).reload_connections()
                )
            )
            asyncio.gather(*tasks)
            return {"status": "success"}
        except Exception as e:
            logging.debug(
                f"Error occurred while adding hotspot connection: {e.args}"
            )
            return {"status": f"error, exception: {e}"}

    def set_network_priority(
        self, ssid: str, priority: ConnectionPriority = ConnectionPriority.LOW
    ) -> None:
        if not self.nm:
            return
        if not self.is_known(ssid):
            return
        self.update_connection_settings(ssid=ssid, priority=priority.value)

    def update_connection_settings(
        self,
        ssid: typing.Optional["str"] = None,
        password: typing.Optional["str"] = None,
        new_ssid: typing.Optional["str"] = None,
        priority: int = 0,
    ) -> typing.Dict:
        """Update the settings for a connection with a specified ssid and or a password

        Args:
            ssid (str | None): SSID of the network we want to update
            password
        Returns:
            typing.Dict: status dictionary with possible keys "error" and "status"
        """

        if not self.nm:
            return {"status": "error", "error": "No network manager"}

        _connection_path = self.get_connection_path_by_ssid(str(ssid))
        if not _connection_path:
            return {
                "status": "error",
                "error": "No saved connection with the specified ssid.",
            }
        try:
            con_settings = NetworkConnectionSettings(
                bus=self.system_dbus, settings_path=str(_connection_path)
            )
            properties = asyncio.run_coroutine_threadsafe(
                con_settings.get_settings(), self.loop
            ).result(timeout=2)
            if new_ssid:
                if ssid == self.hotspot_ssid:
                    self.hotspot_ssid = new_ssid
                properties["connection"]["id"] = ("s", str(new_ssid))
                properties["802-11-wireless"]["ssid"] = (
                    "ay",
                    new_ssid.encode("utf-8"),
                )
            if password:
                password = hashlib.sha256(password.encode()).hexdigest()
                if ssid == self.hotspot_ssid:
                    self.hotspot_password = password
                properties["802-11-wireless-security"]["psk"] = (
                    "s",
                    str(password),
                )

            if priority != 0:
                properties["connection"]["autoconnect-priority"] = (
                    "u",
                    priority,
                )
            task = self.loop.create_task(con_settings.update(properties))
            asyncio.gather(task)
            return {"status": "updated"}
        except Exception:
            return {"status": "error", "error": "Unexpected error"}
