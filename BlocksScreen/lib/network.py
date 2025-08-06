import logging
import typing
from uuid import uuid4

import sdbus
import sdbus.dbus_common_elements
from PyQt6.QtCore import QObject, pyqtSlot
from sdbus_block.networkmanager import (
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
    NetworkManagerSettings,
    WpaSecurityFlags,
    enums,
)
from sdbus_block.networkmanager.exceptions import (
    NmConnectionFailedError,
    NmConnectionInvalidPropertyError,
    NmConnectionPropertyNotFoundError,
)

# TODO: Add Logging, separate logger in this case so i can structure it better
# TODO: Remove the statically attributed variables


class NetworkManagerRescanError(Exception):
    """Exception raised when rescanning the network fails."""

    def __init__(self, error):
        super(NetworkManagerRescanError, self).__init__()
        self.error = error


class SdbusNetworkManager(QObject):
    """Class that controls the linux NetworkManager tool using the sdbus library.

    - Check and get available interfaces..
    - Scans for available networks using the wireless interface.
    - Connect to an available network using wireless interface.
    - Methods to Create, Activate and deactivate a Hotspot.
    - Get the current ip address of the machine.
    - Prefer wired connection over wireless if available.
    """

    def __init__(self, parent: typing.Optional["QObject"]):
        super(SdbusNetworkManager, self).__init__()

        self.system_dbus = sdbus.sd_bus_open_system()

        if self.system_dbus is None:
            return

        self.known_networks = []

        self.saved_networks_ssids: typing.List
        self.hotspot_ssid: str = "PrinterHotspot"
        self.hotspot_password: str = "123456789"
        # * Test the networkmanager
        sdbus.set_default_bus(self.system_dbus)

        try:
            self.nm = NetworkManager()
        except Exception as e:
            logging.debug(
                f"Exception occurred when getting NetworkManager, exception message: {e}"
            )

        self.available_wired_interfaces = self.get_wired_interfaces()
        self.available_wireless_interfaces = self.get_wireless_interfaces()

        self.primary_wifi_interface: NetworkDeviceWireless | None = (
            self.get_wireless_interfaces()[0]
            if len(self.get_wireless_interfaces()) > 0
            else None
        )
        self.primary_wired_interface: NetworkDeviceWired | None = (
            self.get_wired_interfaces()[0]
            if len(self.get_wired_interfaces()) > 0
            else None
        )

        self.rescan_networks()

    # def send_event(e0: QEvent):
    #     if self.parent is None:
    #         return None
    #     try:
    #         event = events.NetworkScan("Scanning networks")
    #         instance = QApplication.instance()
    #         if instance is not None:
    #             instance.sendEvent(self.parent, event)
    #         else:
    #             raise TypeError("QApplication.instance expected a non-None value")
    #     except Exception as e :
    #         _logger.info(f"Unexpected error sending event {event}")

    def get_available_interfaces(self) -> typing.List[str]:
        """get_available_interfaces Gets the names of all available interfaces

        Returns:
            typing.List[str]: List of strings with the available names of all interfaces
        """

        return [
            NetworkDeviceGeneric(device).interface
            for device in self.nm.get_devices()
        ]

    def wifi_enabled(self) -> bool:
        """wifi_enabled Returns a boolean if wireless is enabled on the device.

        Returns:
            bool: True if device is enabled | False if not
        """
        return self.nm.wireless_enabled

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
            raise TypeError("Correct type should be a boolean")
        self.nm.wireless_enabled = toggle

    def toggle_hotspot(self, toggle: bool):
        """Activate/Deactivate device hotspot

        Args:
            toggle (bool): toggle option, True to activate Hotspot, False otherwise

        Raises:
            ValueError: If the toggle argument is not a Boolean.
        """
        # TODO: toggle Hotspot, function to activate or deactivate the device hotspot
        if not isinstance(toggle, bool):
            raise TypeError("Correct type should be a boolean.")
            # TODO: Toggle Hotspot
        pass

    def hotspot_enabled(self) -> typing.Optional["bool"]:
        """Returns a boolean indicating whether the device hotspot is on or not .

        Returns:
            bool: True if Hotspot is activated, False otherwise.
        """
        # TODO: Hotspot enbaled or not
        pass

    def get_wired_interfaces(self) -> typing.List[NetworkDeviceWired]:
        """get_wired_interfaces Get only the names for the available wired (Ethernet) interfaces.

        Returns:
            typing.List[str]: List containing the names of all wired(Ethernet) interfaces.
        """
        return list(
            map(
                lambda path: NetworkDeviceWired(path),
                filter(
                    lambda path: path,
                    filter(
                        lambda device: NetworkDeviceGeneric(device).device_type
                        == enums.DeviceType.ETHERNET,
                        self.nm.get_devices(),
                    ),
                ),
            )
        )

    def get_wireless_interfaces(self) -> typing.List[NetworkDeviceWireless]:
        """get_wireless_interfaces Get only the names of wireless interfaces.

        Returns:
            typing.List[str]: A list containing the names of wireless interfaces.
        """
        # Each interface type has a device flag that is exposed in enums.DeviceType.<device such as Ethernet or Wifi>
        return list(
            map(
                lambda path: NetworkDeviceWireless(path),
                filter(
                    lambda path: path,
                    filter(
                        lambda device: NetworkDeviceGeneric(device).device_type
                        == enums.DeviceType.WIFI,
                        self.nm.get_devices(),
                    ),
                ),
            )
        )

    def get_current_ip_addr(self) -> typing.List[str] | None:
        """get_current_ip_addr Gets the current connection ip address.

        Returns:
            str: A string containing the current ip address
        """

        if self.nm.primary_connection == "/":
            # TODO: Logging
            print("There is no NetworkManager connection. No IP Address")
            return None
        _device_ip4_conf_path = ActiveConnection(
            self.nm.primary_connection
        ).ip4_config
        if _device_ip4_conf_path == "/":
            # NetworkManager reports that there is no ipv4 config for the interface, probably there is no connection at this time.
            logging.info(
                "NetworkManager reports no IP configuration for the interface"
            )
            # TODO: Logging
            return None

        ip4_conf = IPv4Config(_device_ip4_conf_path)
        _addrs = [
            address_data["address"][1]
            for address_data in ip4_conf.address_data
        ]
        return _addrs

    def get_primary_interface(
        self,
    ) -> NetworkDeviceWired | NetworkDeviceWireless | typing.Tuple | str:
        """get_primary_interface Return the primary interface,
            If a there is a connection, returns the interface that is being currently used.

            If there is no connection and wifi is available return de wireless interface.

            If there is no wireless interface and no active connection return the first wired interface that is not (lo).

        Returns:
            typing.List:
        """
        if self.nm.primary_connection == "/":
            if self.primary_wifi_interface is not None:
                return self.primary_wifi_interface
            elif self.primary_wired_interface is not None:
                return self.primary_wired_interface
            # TODO: Add the case where it is on Access point mode.
            else:
                return "/"
        gateway = ActiveConnection(self.nm.primary_connection).devices[0]
        return (
            NetworkDeviceGeneric(gateway).interface,
            self.nm.primary_connection,
            self.nm.primary_connection_type,
        )

    def rescan_networks(self) -> None:
        """rescan_networks Scan for available networks."""
        if (
            self.primary_wifi_interface == "/"
            or self.primary_wifi_interface is None
        ):
            return
        try:
            self.primary_wifi_interface.request_scan({})
        except Exception as e:
            raise NetworkManagerRescanError(f"Network rescan failed: {e}")

    def get_available_networks(self) -> typing.Dict:
        """get_available_networks Scan for networks, get the information about each network.

        Returns:
            typing.List[dict] | None: A list that contains the information about every available found networks. None if nothing is found or the scan failed.
        - Implemented with map built-in python method instead of for loops. Don't know the performance difference, but tried to not use for loops in these methods just to try.
        """
        # This will only work on wifi, because we can scan networks
        if (
            self.primary_wifi_interface == "/"
            or self.primary_wifi_interface is None
        ):
            return {"error": "No primary interface found"}

        # Make sure we scan for networks first
        if self.rescan_networks():
            if (
                self.primary_wifi_interface.device_type
                == enums.DeviceType.WIFI
            ):
                # Get information about all scanned networks.
                _aps: typing.List[AccessPoint] = list(
                    map(
                        lambda ap_path: AccessPoint(ap_path),
                        self.primary_wifi_interface.access_points,
                    )
                )
                _info_networks: typing.Dict = dict(
                    map(
                        lambda ap: (
                            f"{ap.ssid.decode('utf-8')}",
                            {
                                "security": self.get_security_type(ap),
                                "frequency": ap.frequency,
                                "channel": ap.frequency,
                                "signal_level": ap.strength,
                                "max_bitrate": ap.max_bitrate,
                                "BSSID": ap.hw_address,
                            },
                        ),
                        _aps,
                    )
                )
                return _info_networks
        return {"error": "No available networks"}

    def get_security_type(self, ap: AccessPoint) -> typing.Tuple:
        """get_security_type Get the security type from a network AccessPoint

        Args:
            ap (AccessPoint): The AccessPoint of the network.

        Returns:
            typing.Tuple: A Tuple containing all the flags about the WpaSecurityFlags ans AccessPointCapabilities
            - `(flags, wpa_flags, rsn_flags)`



        Check: For more information about the flags
            :py:class:`WpaSecurityFlags` and `ÀccessPointCapabilities` from :py:module:`python-sdbus-networkmanager.enums`
        """
        if ap is None:
            return None

        _sec_rsn: typing.List[WpaSecurityFlags] = list(
            map(lambda sec: sec, list(WpaSecurityFlags(ap.rsn_flags)))
        )
        _sec_wpa: typing.List[WpaSecurityFlags] = list(
            map(lambda wpa: wpa, list(WpaSecurityFlags(ap.wpa_flags)))
        )
        _sec_flags: typing.List[AccessPointCapabilities] = list(
            map(lambda flags: flags, list(AccessPointCapabilities(ap.flags)))
        )

        if len(_sec_flags) == 0:
            return ("Open", "")

        return (_sec_flags, _sec_wpa, _sec_rsn)

    def get_saved_networks(self) -> typing.List[typing.Dict | None]:
        """get_saved_networks Gets a list with the names and ids of all saved networks on the device.

        Returns:
            typing.List[dict] | None: List that contains the names and ids of all saved networks on the device.



        I admit that this implementation is way to complicated, I don't even think it's great on memory and time, but i didn't use for loops so mission achieved.
        """
        if self.nm is None:
            return [{"error": "No network manager"}]

        _connections: typing.List[str] = (
            NetworkManagerSettings().list_connections()
        )

        _network_settings: typing.List[NetworkManagerConnectionProperties] = (
            list(
                map(
                    lambda _settings: NetworkConnectionSettings(
                        _settings
                    ).get_settings(),
                    iter(_connections),
                )
            )
        )

        _known_networks_parameters: typing.List[typing.Dict | None] = list(
            filter(
                lambda network_entry: network_entry is not None,
                list(
                    map(
                        lambda network_properties: (
                            {
                                "SSID": network_properties["802-11-wireless"][
                                    "ssid"
                                ][1].decode(),
                                "UUID": network_properties["connection"][
                                    "uuid"
                                ][1],
                                # "CONNECTION_PATH": connection
                            }
                            if network_properties["connection"]["type"][1]
                            == "802-11-wireless"
                            else None
                        ),
                        _network_settings,
                    )
                ),
            )
        )

        return _known_networks_parameters

    def get_saved_networks_with_for(self) -> typing.List[dict]:
        """get_saved_networks_with_for Gets a list with the names and ids of all saved networks on the device.

        Returns:
            typing.List[dict]: List that contains the names and ids of all saved networks on the device.


        This implementation is equal to the klipper screen implementation, this one uses for loops and is simpler.
        https://github.com/KlipperScreen/KlipperScreen/blob/master/ks_includes/sdbus_nm.py Alfredo Monclues (alfrix) 2024
        """
        if self.nm is None:
            return []
        known_networks = []
        for connection in NetworkManagerSettings().list_connections():
            saved_con = NetworkConnectionSettings(connection)
            conn = saved_con.get_settings()
            if conn["connection"]["type"][1] == "802-11-wireless":
                known_networks.append(
                    {
                        "SSID": conn["802-11-wireless"]["ssid"][1].decode(),
                        "UUID": conn["connection"]["uuid"][1],
                        "SECURITY_TYPE": conn["802-11-wireless-security"][
                            "key_mgmt"
                        ][1].decode(),
                        "CONNECTION_PATH": connection,
                    }
                )

        return known_networks

    def get_saved_ssid_names(self) -> typing.List[str]:
        """Get a list with the current saved network ssid names

        Returns:
            typing.List[str]: List that contains the names of the saved ssid network names
        """

        _saved_ssids: typing.List[str] = list(
            map(
                lambda saved_network: (saved_network["SSID"]),
                self.get_saved_networks_with_for(),
            )
        )

        return _saved_ssids

    def is_known(self, ssid: str) -> bool:
        """Whether or not a network is known

        Args:
            ssid (str): The networks ssid

        Returns:
            bool: True if the network is known otherwise False
        """
        return any(
            net["SSID"] == ssid for net in self.get_saved_networks_with_for()
        )

    def add_wifi_network(self, ssid: str, psk: str) -> typing.Dict:
        """Add and Save a network to the device.

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
        if (
            self.primary_wifi_interface is None
            or self.primary_wifi_interface == "/"
        ):
            return {"status": "error", "msg": "No Available interface"}

        # Connections with the same if result in failure, so get ids first.
        # TODO: Get connections by id, calculate a new id that doesn't conflict with any other,
        # TODO: Pass that new id to the properties NetworkManagerConnectionProperties on the "connection" -> "id"
        # TODO: If the id exists, delete the connection with the same id or just not add it before the other one is manually deleted
        # TODO: The id can be the ssid name, but i think this fucks up if the same id is used more than once

        # Get the security type for this network.
        _available_networks: typing.Dict = self.get_available_networks()
        if "error" in _available_networks.keys():
            return {"status": "error", "msg": "No available Networks"}
        # It is recommended to delete the network if it already exists so to not mess up the id's
        if self.is_known(ssid):
            self.delete_network(ssid)

        if ssid in _available_networks.keys():
            _wanted_network: typing.Dict = _available_networks[f"{ssid}"]
            # TODO: Can add timestamp field in here to know the last time the connection was successful fully activated.
            properties: NetworkManagerConnectionProperties = {
                "connection": {
                    "id": ("s", ssid),
                    "uuid": ("s", str(uuid4())),
                    "type": ("s", "802-11-wireless"),
                    "interface-name": (
                        "s",
                        self.primary_wifi_interface.interface,
                    ),
                    "autoconnect": ("b", bool(True)),
                },
                "802-11-wireless": {
                    "mode": ("s", "infrastructure"),
                    "ssid": ("ay", ssid.encode("utf-8")),
                },
                "ipv4": {"method": ("s", "auto")},
                "ipv6": {"method": ("s", "auto")},
            }

            if "security" in _wanted_network.keys():
                _security_types = _wanted_network["security"]
            else:
                return {
                    "status": "error",
                    "msg": "No security type for network, stopping",
                }
            if _security_types[0] is None:
                # The network doesn't have security
                return {"status": "error", "msg": "unknown_security_type"}

            elif (
                AccessPointCapabilities.PRIVACY
                or AccessPointCapabilities.WPS
                or AccessPointCapabilities.WPS_BUTTON
                or AccessPointCapabilities.WPS_PIN in _security_types[0]
            ):
                # There is some sort of security in this case, privacy usually means that there is WEP as per the sdbus networkmanager documentation
                properties["802-11-wireless"]["security"] = (
                    "s",
                    "802-11-wireless-security",
                )

                if (
                    WpaSecurityFlags.P2P_WEP104
                    or WpaSecurityFlags.P2P_WEP40
                    or WpaSecurityFlags.BROADCAST_WEP104
                    or WpaSecurityFlags.BROADCAST_WEP40
                ) in (_security_types[1] or _security_types[2]):
                    properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "none"),
                        "wep-key-type": ("u", 2),
                        "wep-key0": ("s", psk),
                        "auth-alg": ("s", "shared"),
                    }
                elif (
                    WpaSecurityFlags.P2P_TKIP
                    or WpaSecurityFlags.BROADCAST_TKIP
                ) in (_security_types[1] or _security_types[2]):
                    # * TKip
                    # raise NotImplementedError
                    return {
                        "status": "error",
                        "msg": "Security type P2P_TKIP OR BRADCAST_TKIP not supported",
                    }
                elif (
                    WpaSecurityFlags.P2P_CCMP
                    or WpaSecurityFlags.BROADCAST_CCMP
                ) in (_security_types[1] or _security_types[2]):
                    # * AES/CCMP WPA2
                    properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "wpa-psk"),
                        "psk": ("s", psk),
                        "pairwise": ("as", ["ccmp"]),
                    }

                elif (WpaSecurityFlags.AUTH_PSK) in (
                    _security_types[1] or _security_types[2]
                ):
                    # * AUTH_PSK -> WPA-PSK
                    properties["802-11-wireless-security"] = {
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
                    properties["802-11-wireless-security"] = {
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
                    properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "sae"),
                        "psk": ("s", psk),
                    }
                elif (WpaSecurityFlags.AUTH_OWE) in (
                    _security_types[1] or _security_types[2]
                ):
                    # * OWE
                    properties["802-11-wireless-security"] = {
                        "key-mgmt": ("s", "owe"),
                        "psk": ("s", psk),
                    }
                elif (WpaSecurityFlags.AUTH_OWE_TM) in (
                    _security_types[1] or _security_types[2]
                ):
                    # * OWE TM
                    # raise NotImplementedError
                    return {
                        "status": "error",
                        "msg": "Security type  AUTH_OWE_TM not supported",
                    }

                elif (WpaSecurityFlags.AUTH_EAP_SUITE_B) in (
                    _security_types[1] or _security_types[2]
                ):
                    # * EAP SUITE B
                    # raise NotImplementedError
                    return {
                        "status": "error",
                        "msg": "Security type EAP_SUITE_B not supported",
                    }

                try:
                    NetworkManagerSettings().add_connection(properties)
                    return {
                        "status": "success",
                        "msg": "Network added successfully",
                    }
                except NmConnectionFailedError as e:
                    return {
                        "status": "exception",
                        "msg": f"Exception occurred could not connect to network: {e} ",
                    }
                except (
                    NmConnectionPropertyNotFoundError
                    or NmConnectionInvalidPropertyError
                ) as e:
                    return {
                        "status": "exception",
                        "msg": f"Error configuring properties for the network, internal error  : {e}",
                    }
                except Exception as e:
                    return {
                        "status": "exception",
                        "msg": f"Could not connect to network: {e}",
                    }

        return {"status": "failure", "msg": "Unable to add network connection"}

    def disconnect_network(self) -> bool:
        """disconnect_network Disconnect the wireless device and prevent it from reconnecting.

        Returns:
            bool:
            - True -> wifi interface is not and can perform the disconnection
            - False -> Wifi interface is none and the disconnect command is not run.
        """
        if (
            self.primary_wifi_interface == "/"
            or self.primary_wifi_interface is None
        ):
            return False
        self.primary_wifi_interface.disconnect()
        return True

    def get_connection_path_by_ssid(self, ssid: str) -> str | None:
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
        if len(_saved_networks) == 0 or _saved_networks is None:
            return "There are no saved networks, must add a new network connection first."

        # *Get the connection path by ssid
        for saved_network in _saved_networks:
            if saved_network["SSID"].lower() == ssid.lower():
                # print(self.nm.primary_connection)
                _connection_path = saved_network["CONNECTION_PATH"]

        return _connection_path

    def get_security_type_by_ssid(self, ssid: str) -> str | typing.Dict:
        """Get the security type for a saved network by its ssid.

        Args:
            ssid (str): SSID of a saved network

        Returns:
            str | typing.Dict: _description_
        """
        if not isinstance(ssid, str):
            return {"error": "ssid Argument must be of type string"}

        if self.nm is None:
            return {"error": "No network manager instance available"}
        _security_type: str = ""
        _saved_networks = self.get_saved_networks_with_for()
        if len(_saved_networks) == 0 or _saved_networks is None:
            return {"error": f"There is no saved network with {ssid} name."}

        # * Get the actual security type
        for network in _saved_networks:
            if network["SSID"].lower() == ssid.lower():
                _security_type = network["SECURITY_TYPE"]

        return _security_type

    def get_connection_signal_by_ssid(self, ssid: str) -> typing.Dict | int:
        """Get the signal strength for a ssid

        Args:
            ssid (str): Ssid we wan't to scan

        Returns:
            typing.Dict | int: If an error occurs the method return a dictionary with the key error, the value is the errors message.
                                In the case we are able to scan
                                The method returns the signal strength in %
        """
        if not isinstance(ssid, str):
            return {"error": "ssid argument must be of type string"}
        if self.nm is None:
            return {"error": "No Network Manager instance available"}
        if (
            self.primary_wifi_interface == "/"
            or self.primary_wifi_interface is None
        ):
            return {"error": "No wifi interface"}

        _signal: int = 0
        if self.rescan_networks():
            if (
                self.primary_wifi_interface.device_type
                == enums.DeviceType.WIFI
            ):
                # Get information on scanned networks:
                _aps: typing.List[AccessPoint] = list(
                    map(
                        lambda ap_path: AccessPoint(ap_path),
                        self.primary_wifi_interface.access_points,
                    )
                )

                for ap in _aps:
                    if ap.ssid.decode("utf-8").lower() == ssid.lower():
                        return ap.strength

        return 0

    def connect_network(self, ssid: str) -> str | bool:
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
        if _connection_path is None:
            return f"No saved connection path for the SSID: {ssid}"
        try:
            if self.nm.primary_connection == _connection_path:
                return f"Network connection already established with {ssid} "

            active_path = self.nm.activate_connection(str(_connection_path))

        except Exception as e:
            raise Exception(
                f"Unkown error while trying to connect to {ssid} network. \n Exception {e}"
            )

        return active_path

    def delete_network(self, ssid: str) -> typing.Dict | str:
        """Deletes a saved network given a ssid

        Args:
            ssid (str): The networks ssid to be deleted

        Raises:
            ValueError: If the ssid argument is not of type string
            Exception: If an unexpected error occurred when deleting the network.

        Returns:
            typing.Dict: Status key with the outcome of the networks deletion.
        """
        if not isinstance(ssid, str):
            logging.debug(
                f"Argument type error, ssid expected a string and received : {type(ssid)} with value {ssid}"
            )
            raise TypeError(
                f"Path argument must be of type string, inserted type: {type(ssid)}"
            )

        # * Check if the ssid is a valid saved network or not
        if not self.is_known(ssid):
            return f"There is no saved network connection with ssid: {ssid}"

        _path = self.get_connection_path_by_ssid(ssid)

        try:
            NetworkConnectionSettings(settings_path=str(_path)).delete()
            return {"status": "success"}
        except Exception as e:
            logging.debug(f"Unkown Error detected exception: {e}")
            return {"status": "error"}

    def create_hotspot(
        self, ssid: str = "PrinterHotspot", password: str = "123456789"
    ) -> typing.Dict:
        # * Delete the old hotspot connection, if it exists
        self.delete_old_hotspot_connection()

        # * Create and add a hotspot connection if there is none
        properties: NetworkManagerConnectionProperties = {
            "connection": {
                "id": ("s", str(ssid)),
                "uuid": ("s", str(uuid4())),
                "type": ("s", "802-11-wireless"),
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
                "psk": ("s", str(password)),
                "pmf": ("u", 1),
                "pairwise": ("as", ["ccmp"]),
            },
            "ipv4": {
                "method": ("s", "shared"),
            },
            "ipv6": {"method": ("s", "ignore")},
        }

        try:
            NetworkManagerSettings().add_connection(properties)
            return {"status": "success"}
        except Exception as e:
            logging.debug(
                f"Error occurred while adding a hotspot connection: {e.args}"
            )
            return {"status": "error, exception"}

    def delete_old_hotspot_connection(self) -> None:
        self.delete_network(self.hotspot_ssid)

    def get_hotspot_ssid(self) -> str:
        return self.hotspot_ssid

    def set_hotspot_ssid(self, ssid: str) -> None:
        self.hotspot_ssid = ssid
        self.create_hotspot(ssid=ssid)

    def update_connection_settings(
        self,
        ssid: typing.Optional["str"] = None,
        password: typing.Optional["str"] = None,
        new_ssid: typing.Optional["str"] = None,
    ) -> typing.Dict:
        """Update the settings for a connection with a specified ssid and or a password

        Args:
            ssid (str | None): SSID of the network we want to update
            password
        Returns:
            typing.Dict: status dictionary with possible keys "error" and "status"
        """

        if self.nm is None:
            return {"status": "error", "error": "No network manager"}

        _connection_path = self.get_connection_path_by_ssid(str(ssid))

        if _connection_path is None:
            return {
                "status": "error",
                "error": "No saved connection with the specified ssid.",
            }
        try:
            con_settings = NetworkConnectionSettings(str(_connection_path))
            properties = con_settings.get_settings()
            if new_ssid is not None:
                if ssid == self.hotspot_ssid:
                    self.hotspot_ssid = new_ssid
                properties["connection"]["id"] = ("s", str(new_ssid))
                properties["802-11-wireless"]["ssid"] = (
                    "ay",
                    new_ssid.encode("utf-8"),
                )
            if password is not None:
                if ssid == self.hotspot_ssid:
                    self.hotspot_password = password
                properties["802-11-wireless-security"]["psk"] = (
                    "s",
                    str(password),
                )

            con_settings.update(properties)

            return {"status": "updated"}
        except Exception:
            return {"status": "error", "error": "Unexpected error"}


class SdbusNetworkManagerDummy:
    """Class that controls the linux NetworkManager tool using the sdbus library.

    - Check and get available interfaces..
    - Scans for available networks using the wireless interface.
    - Connect to an available network using wireless interface.
    - Methods to Create, Activate and deactivate a Hotspot.
    - Get the current ip address of the machine.
    - Prefer wired connection over wireless if available.
    """

    def __init__(self):
        self.hotspot_ssid: str = "PrinterHotspot"
        self.hotspot_password: str = "123456789"
        self.hotspot_active: bool = False
        self.saved_networks_ssids: typing.List
        self.nm = "NetworkManager"
        self.available_wired_interfaces = self.get_wired_interfaces()
        self.available_wireless_interfaces = self.get_wireless_interfaces()

        self.primary_wifi_interface = "path/wirelesssDummy"
        self.primary_wired_interface = "path/wireddDummy"
        self.wireless_active: bool = True

    def get_available_interfaces(self) -> typing.List[str]:
        """get_available_interfaces Gets the names of all available interfaces

        Returns:
            typing.List[str]: List of strings with the available names of all interfaces
        """
        return ["device/wlan0Dummy", "device/loDummy", "device/eth0Dummy"]

    def wifi_enabled(self) -> bool:
        """wifi_enabled Returns a boolean if wireless is enabled on the device.

        Returns:
            bool: True if device is enabled | False if not
        """
        print(self.wireless_active)
        return self.wireless_active

    def toggle_wifi(self, toggle: bool):
        """toggle_wifi Enable/Disable wifi

        Args:
            toggle (bool):

            - True -> Enable wireless

            - False -> Disable wireless

        Raises:
            ValueError: Raised when the argument is not of type boolean.

        """
        self.wireless_active = not self.wireless_active
        return

    def toggle_hotspot(self, toggle: bool):
        """Activate/Deactivate device hotspot

        Args:
            toggle (bool): toggle option, True to activate Hotspot, False otherwise

        Raises:
            ValueError: If the toggle argument is not a Boolean.
        """
        # TODO: toggle Hotspot, function to activate or deactivate the device hotspot
        self.hotspot_active = not self.hotspot_active

    def hotspot_enabled(self) -> typing.Optional["bool"]:
        """Returns a boolean indicating whether the device hotspot is on or not .

        Returns:
            bool: True if Hotspot is activated, False otherwise.
        """
        # TODO: Hotspot enbaled or not
        return self.hotspot_active

    def get_wired_interfaces(self) -> typing.List:
        """get_wired_interfaces Get only the names for the available wired (Ethernet) interfaces.

        Returns:
            typing.List[str]: List containing the names of all wired(Ethernet) interfaces.
        """
        return ["path/wiredDummy/1", "path/wiredDummy/2"]

    def get_wireless_interfaces(self) -> typing.List:
        """get_wireless_interfaces Get only the names of wireless interfaces.

        Returns:
            typing.List[str]: A list containing the names of wireless interfaces.
        """
        # Each interface type has a device flag that is exposed in enums.DeviceType.<device such as Ethernet or Wifi>
        return [
            "path/wirelessDummy/1",
            "path/wirelessDummy/2",
        ]

    def get_current_ip_addr(self) -> typing.List[str] | None:
        """get_current_ip_addr Gets the current connection ip address.

        Returns:
            str: A string containing the current ip address
        """

        return ["1092.12312.1222.11"]

    def get_primary_interface(self):
        """get_primary_interface Return the primary interface,
            If a there is a connection, returns the interface that is being currently used.

            If there is no connection and wifi is available return de wireless interface.

            If there is no wireless interface and no active connection return the first wired interface that is not (lo).

        Returns:
            typing.List:
        """
        return "path/wlan0Dummy"

    def rescan_networks(self) -> None:
        """rescan_networks Scan for available networks.

        Returns:
            bool | None: True if the scan was successful, False otherwise. None if there is no primary wifi interface to use for the scan.
        """
        return

    def get_available_networks(self):
        """get_available_networks Scan for networks, get the information about each network.

        Returns:
            typing.List[dict] | None: A list that contains the information about every available found networks. None if nothing is found or the scan failed.
        - Implemented with map built-in python method instead of for loops. Don't know the performance difference, but tried to not use for loops in these methods just to try.
        """
        # This will only work on wifi, because we can scan networks
        return (
            [
                {
                    "ssid": "BLOCKS",
                    "security": "wpa",
                    "frequency": 344,
                    "channel": 2,
                    "signal_level": "-12",
                    "max_bitrate": "1222",
                    "BSSID": "12:312:je:22",
                },
                {
                    "ssid": "MEO",
                    "security": "wpa",
                    "frequency": 344,
                    "channel": 2,
                    "signal_level": "-12",
                    "max_bitrate": "1222",
                    "BSSID": "12:312:je:22",
                },
                {
                    "ssid": "SkyNet",
                    "security": "wpa2",
                    "frequency": 5180,
                    "channel": 36,
                    "signal_level": "-45",
                    "max_bitrate": "867",
                    "BSSID": "a2:3f:5d:8c:01:aa",
                },
                {
                    "ssid": "CoffeeShop_WiFi",
                    "security": "open",
                    "frequency": 2412,
                    "channel": 1,
                    "signal_level": "-68",
                    "max_bitrate": "144",
                    "BSSID": "bc:85:56:de:12:39",
                },
                {
                    "ssid": "HomeNetwork5G",
                    "security": "wpa3",
                    "frequency": 5745,
                    "channel": 149,
                    "signal_level": "-38",
                    "max_bitrate": "1300",
                    "BSSID": "e3:55:76:9a:cd:ef",
                },
                {
                    "ssid": "PublicLibraryNet",
                    "security": "wpa2",
                    "frequency": 2437,
                    "channel": 6,
                    "signal_level": "-72",
                    "max_bitrate": "300",
                    "BSSID": "00:1a:2b:3c:4d:5e",
                },
                {
                    "ssid": "Device_AP_8934",
                    "security": "open",
                    "frequency": 2462,
                    "channel": 11,
                    "signal_level": "-80",
                    "max_bitrate": "54",
                    "BSSID": "de:ad:be:ef:00:99",
                },
                {
                    "ssid": "IoT_Network",
                    "security": "wpa2",
                    "frequency": 2422,
                    "channel": 3,
                    "signal_level": "-59",
                    "max_bitrate": "72",
                    "BSSID": "aa:bb:cc:dd:ee:ff",
                },
                {
                    "ssid": "FastLane",
                    "security": "wpa3",
                    "frequency": 5200,
                    "channel": 40,
                    "signal_level": "-33",
                    "max_bitrate": "2400",
                    "BSSID": "11:22:33:44:55:66",
                },
                {
                    "ssid": "GUEST1234",
                    "security": "wpa",
                    "frequency": 2462,
                    "channel": 11,
                    "signal_level": "-50",
                    "max_bitrate": "600",
                    "BSSID": "77:88:99:aa:bb:cc",
                },
            ],
        )

    def get_security_type(self, ap: AccessPoint) -> typing.Tuple:
        """get_security_type Get the security type from a network AccessPoint

        Args:
            ap (AccessPoint): The AccessPoint of the network.

        Returns:
            typing.Tuple: A Tuple containing all the flags about the WpaSecurityFlags ans AccessPointCapabilities
            - `(flags, wpa_flags, rsn_flags)`



        Check: For more information about the flags
            :py:class:`WpaSecurityFlags` and `ÀccessPointCapabilities` from :py:module:`python-sdbus-networkmanager.enums`
        """
        return ("aps", "wpa", "jdjj")

    def get_saved_networks(self) -> typing.List[typing.Dict | None]:
        """get_saved_networks Gets a list with the names and ids of all saved networks on the device.

        Returns:
            typing.List[dict] | None: List that contains the names and ids of all saved networks on the device.



        I admit that this implementation is way to complicated, I don't even think it's great on memory and time, but i didn't use for loops so mission achieved.
        """
        return [
            {"SSID": "BLOCKS", "UUID": "OOAISUDFOASODFJ"},
            {"SSID": "PrinterHotspot", "UUID": "OOAISUDFOASODFJ"},
            {"SSID": "SkyNet", "UUID": "91UJDKSLA9321KJD"},
            {"SSID": "PublicLibraryNet", "UUID": "LKSJDOIQWEUR9283"},
            {"SSID": "FastLane", "UUID": "UQWEIJASD8237AJD"},
            {"SSID": "GUEST1234", "UUID": "1287JDKALQWEIJSN"},
        ]

    def get_saved_networks_with_for(self):
        """get_saved_networks_with_for Gets a list with the names and ids of all saved networks on the device.

        Returns:
            typing.List[dict]: List that contains the names and ids of all saved networks on the device.


        This implementation is equal to the klipper screen implementation, this one uses for loops and is simpler.
        https://github.com/KlipperScreen/KlipperScreen/blob/master/ks_includes/sdbus_nm.py Alfredo Monclues (alfrix) 2024
        """
        return [
            {"SSID": "BLOCKS", "UUID": "OOAISUDFOASODFJ"},
            {"SSID": "PrinterHotspot", "UUID": "OOAISUDFOASODFJ"},
            {"SSID": "SkyNet", "UUID": "91UJDKSLA9321KJD"},
            {"SSID": "PublicLibraryNet", "UUID": "LKSJDOIQWEUR9283"},
            {"SSID": "FastLane", "UUID": "UQWEIJASD8237AJD"},
            {"SSID": "GUEST1234", "UUID": "1287JDKALQWEIJSN"},
        ]

    def get_saved_ssid_names(self) -> typing.List[str]:
        """Get a list with the current saved network ssid names

        Returns:
            typing.List[str]: List that contains the names of the saved ssid network names
        """
        return [
            "BLOCKS",
            "PrinterHotspot",
            "SkyNet",
            "PublicLibraryNet",
            "FastLane",
            "GUEST1234",
        ]

    def is_known(self, ssid: str):
        """Whether or not a network is known

        Args:
            ssid (str): The networks ssid

        Returns:
            bool: True if the network is known otherwise False
        """
        pass

    def add_wifi_network(self, ssid: str, psk: str) -> typing.Dict:
        """Add and Save a network to the device.

        Args:
            ssid (str): Networks SSID
            psk (str): Networks password

        Raises:
            NotImplementedError: Some network security types are not yet available so there is no way to connect to them.

        Returns:
            typing.Dict: Dictionary with a status key that reports whether or not the connection was saved and connected.

            On the returned dictionary a key value "error" can appear if an error occurred, the value will say what the error was.
        """
        print(ssid)
        print(psk)
        return {"status": "error", "msg": "dummy"}

    def disconnect_network(self):
        """disconnect_network Disconnect the wireless device and prevent it from reconnecting.

        Returns:
            bool:
            - True -> wifi interface is not and can perform the disconnection
            - False -> Wifi interface is none and the disconnect command is not run.
        """
        pass

    def get_connection_path_by_ssid(self, ssid: str) -> str | None:
        """Given a ssid, get the connection path, if it's saved

        Raises:
            ValueError: If the ssid was not of type string.

        Returns:
            str: connection path
        """
        pass

    def get_security_type_by_ssid(self, ssid: str) -> str | typing.Dict:
        """Get the security type for a saved network by its ssid.

        Args:
            ssid (str): SSID of a saved network

        Returns:
            str | typing.Dict: _description_
        """
        return "wpa"

    def get_connection_signal_by_ssid(self, ssid: str) -> typing.Dict | int:
        """Get the signal strength for a ssid

        Args:
            ssid (str): Ssid we wan't to scan

        Returns:
            typing.Dict | int: If an error occurs the method return a dictionary with the key error, the value is the errors message.
                                In the case we are able to scan
                                The method returns the signal strength in %
        """
        return 14

    def connect_network(self, ssid: str):
        """Connect to a saved network given an ssid

        Raises:
            ValueError: Raised if the ssid argument is not of type string.
            Exception: Raised if there was an error while trying to connect.

        Returns:
            str: The active connection path, or a Message.
        """
        print(f"Connecto to network {ssid}")

    def delete_network(self, ssid: str):
        """Deletes a saved network given a ssid

        Args:
            ssid (str): The networks ssid to be deleted

        Raises:
            ValueError: If the ssid argument is not of type string
            Exception: If an unexpected error occurred when deleting the network.

        Returns:
            typing.Dict: Status key with the outcome of the networks deletion.
        """
        print(f"Deleted network {ssid}")

    def create_hotspot(
        self, ssid: str = "PrinterHotspot", password: str = "123456789"
    ):
        print(f"Created hotspot {ssid}, {password}")

    def delete_old_hotspot_connection(self) -> None:
        print("Deleted old hotspot ")

    def get_hotspot_ssid(self):
        print("Get hostpot ssid")

    def set_hotspot_ssid(self, ssid: str) -> None:
        print(f"Set hotspot ssid {ssid}")

    def update_connection_settings(
        self,
        ssid: typing.Optional["str"] = None,
        password: typing.Optional["str"] = None,
        new_ssid: typing.Optional["str"] = None,
    ):
        """Update the settings for a connection with a specified ssid and or a password

        Args:
            ssid (str | None): SSID of the network we want to update
            password
        Returns:
            typing.Dict: status dictionary with possible keys "error" and "status"
        """
        print(f"Updated a network connection {ssid} | {password} | {new_ssid}")
