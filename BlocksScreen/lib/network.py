import hashlib
import logging
import typing
from uuid import uuid4


import sdbus

from PyQt6 import QtCore

from sdbus_block.networkmanager import (
    AccessPoint,
    AccessPointCapabilities,
    ActiveConnection,
    IPv4Config,
    NetworkConnectionSettings,
    NetworkManagerConnectivityState,
    NetworkDeviceGeneric,
    NetworkManagerState,
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


class NetworkManagerRescanError(Exception):
    """Exception raised when rescanning the network fails."""

    def __init__(self, error):
        super(NetworkManagerRescanError, self).__init__()
        self.error = error



class SdbusNetworkManager(QtCore.QObject):
    def __init__(self, parent: typing.Optional[QtCore.QObject]):
        super(SdbusNetworkManager, self).__init__()
        self.system_dbus = sdbus.sd_bus_open_system()

        if not self.system_dbus:
            print("No systembus ")
            return
        self.known_networks = []
        self.saved_networks_ssids: typing.List
        self.hotspot_ssid: str = "PrinterHotspot"
        self.hotspot_password: str = hashlib.sha256(
            "123456789".encode()
        ).hexdigest()  # "123456789"

        sdbus.set_default_bus(self.system_dbus)

        try:
            self.nm = NetworkManager()
        except Exception as e:
            logging.debug(
                f"Exception occurred when getting NetworkManager: {e}"
            )

        self.check_nm_status()

        self.available_wired_interfaces = self.get_wired_interfaces()
        self.available_wireless_interfaces = self.get_wireless_interfaces()
        self.primary_wifi_interface: typing.Union[
            NetworkDeviceWireless, None
        ] = (
            self.get_wireless_interfaces()[0]
            if len(self.get_wireless_interfaces()) > 0
            else None
        )
        self.primary_wired_interface: typing.Union[
            NetworkDeviceWired, None
        ] = (
            self.get_wired_interfaces()[0]
            if len(self.get_wired_interfaces()) > 0
            else None
        )

        if not self.is_known(self.hotspot_ssid):
            self.create_hotspot(self.hotspot_ssid, self.hotspot_password)

        self.rescan_networks()


    def get_available_interfaces(self) -> typing.List[str]:
        """Gets the names of all available interfaces

        Returns:
            typing.List[str]: List of strings with the available names of all interfaces
        """

        return [
            NetworkDeviceGeneric(device).interface
            for device in self.nm.get_devices()
        ]

    def wifi_enabled(self) -> bool:
        """Returns a boolean if wireless is enabled on the device.

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
            raise TypeError("toggle expected boolean")
        self.nm.wireless_enabled = toggle

    def toggle_hotspot(self, toggle: bool):
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
                self.nm.reload()
                if self.nm.check_connectivity() == (
                    NetworkManagerConnectivityState.FULL
                    | NetworkManagerConnectivityState.LIMITED
                ):
                    logging.info(f"AP {self.hotspot_ssid} up!")
                return
            if old_ssid:
                self.connect_network(old_ssid)
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

    def get_current_ssid(self) -> str:
        if self.nm.primary_connection == "/":
            return ""
        try:
            active_con = ActiveConnection(
                self.nm.primary_connection
            ).connection
            con = NetworkConnectionSettings(active_con)
            settings = con.get_settings()
            return str(settings["802-11-wireless"]["ssid"][1].decode())
        except Exception as e:
            logging.info(f"Unexpected error occurred: {e}")
            return ""


    def get_current_ip_addr(self) -> typing.List[str]:

        """Get the current connection ip address.

        Returns:
            str: A string containing the current ip address
        """
        if self.nm.primary_connection == "/":
            logging.info("There is no NetworkManager active connection.")
            return ""
        _device_ip4_conf_path = ActiveConnection(
            self.nm.primary_connection
        ).ip4_config
        if _device_ip4_conf_path == "/":
            logging.info(
                "NetworkManager reports no IP configuration for the interface"
            )
            return ""
        ip4_conf = IPv4Config(_device_ip4_conf_path)
        return [
            address_data["address"][1]
            for address_data in ip4_conf.address_data
        ][0]

    def get_primary_interface(
        self,
    ) -> typing.Union[
        NetworkDeviceWired, NetworkDeviceWireless, typing.Tuple, str
    ]:
        """Get the primary interface,
            If a there is a connection, returns the interface that is being currently used.

            If there is no connection and wifi is available return de wireless interface.

            If there is no wireless interface and no active connection return the first wired interface that is not (lo).

        Returns:
            typing.List:
        """
        if self.nm.primary_connection == "/":
            if self.primary_wifi_interface:
                return self.primary_wifi_interface
            elif self.primary_wired_interface:
                return self.primary_wired_interface
            else:
                return "/"
        gateway = ActiveConnection(self.nm.primary_connection).devices[0]
        return (
            NetworkDeviceGeneric(gateway).interface,
            self.nm.primary_connection,
            self.nm.primary_connection_type,
        )

    def rescan_networks(self) -> bool:
        """rescan_networks Scan for available networks."""
        if (
            self.primary_wifi_interface == "/"
            or not self.primary_wifi_interface
        ):
            return False
        try:
            self.primary_wifi_interface.request_scan({})
            return True
        except Exception:
            raise NetworkManagerRescanError("Network scan failed")
        finally:
            return False

    def get_available_networks(self) -> typing.Dict:
        """get_available_networks Scan for networks, get the information about each network.

        Returns:
            typing.List[dict] | None: A list that contains the information about every available found networks. None if nothing is found or the scan failed.
        - Implemented with map built-in python method instead of for loops. Don't know the performance difference, but tried to not use for loops in these methods just to try.
        """
        if (
            self.primary_wifi_interface == "/"
            or not self.primary_wifi_interface
        ):
            return {"error": "No primary interface found"}

        if self.rescan_networks():
            if (
                self.primary_wifi_interface.device_type
                == enums.DeviceType.WIFI
            ):
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
        if not self.nm:
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

    def get_saved_networks_with_for(self) -> typing.List:
        """Get a list with the names and ids of all saved networks on the device.

        Returns:
            typing.List[dict]: List that contains the names and ids of all saved networks on the device.


        This implementation is equal to the klipper screen implementation, this one uses for loops and is simpler.
        https://github.com/KlipperScreen/KlipperScreen/blob/master/ks_includes/sdbus_nm.py Alfredo Monclues (alfrix) 2024
        """
        if not self.nm:
            return []
        saved_networks = []
        for connection in NetworkManagerSettings().list_connections():
            saved_con = NetworkConnectionSettings(connection)
            conn = saved_con.get_settings()
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
        return any(
            net.get("SSID", "") == ssid
            for net in self.get_saved_networks_with_for()
        )

    def add_wifi_network(
        self, ssid: str, psk: str, priority: int = 0
    ) -> typing.Dict:
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
            not self.primary_wifi_interface
            or self.primary_wifi_interface == "/"
        ):
            return {"status": "error", "msg": "No Available interface"}

        psk = hashlib.sha256(psk.encode()).hexdigest()
        _available_networks: typing.Dict = self.get_available_networks()
        if "error" in _available_networks.keys():
            return {"status": "error", "msg": "No available Networks"}
        if self.is_known(ssid):
            self.delete_network(ssid)

        if ssid in _available_networks.keys():
            _wanted_network: typing.Dict = _available_networks[f"{ssid}"]
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
                    "autoconnect-priority": ("u", priority),
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
                return {"status": "error", "msg": "unknown_security_type"}

            elif (
                AccessPointCapabilities.PRIVACY
                or AccessPointCapabilities.WPS
                or AccessPointCapabilities.WPS_BUTTON
                or AccessPointCapabilities.WPS_PIN in _security_types[0]
            ):
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
                    NetworkManagerSettings().reload_connections()

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

    def disconnect_network(self) -> None:
        """Disconnect the active connection"""
        if (
            self.primary_wifi_interface == "/"
            or not self.primary_wifi_interface
        ):
            return

        self.primary_wifi_interface.disconnect()

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

    def get_security_type_by_ssid(
        self, ssid: str
    ) -> typing.Union[str, typing.Dict]:
        """Get the security type for a saved network by its ssid.

        Args:
            ssid (str): SSID of a saved network

        Returns:
            str | typing.Dict: _description_
        """
        if not isinstance(ssid, str):
            return {"error": "ssid Argument must be of type string"}
        if not self.nm:
            return {"error": "No network manager instance available"}
        _security_type: str = ""
        _saved_networks = self.get_saved_networks_with_for()
        if not _saved_networks:
            return {"error": f"There is no saved network with {ssid} name."}
        if len(_saved_networks) == 0:
            return {"error": f"There is no saved network with {ssid} name."}
        for network in _saved_networks:
            if network["SSID"].lower() == ssid.lower():
                _security_type = network["SECURITY_TYPE"]

        return _security_type

    def get_connection_signal_by_ssid(self, ssid: str) -> int:
        """Get the signal strength for a ssid

        Args:
            ssid (str): Ssid we wan't to scan

        Returns:
            typing.Dict | int: If an error occurs the method return a dictionary with the key error, the value is the errors message.
                                In the case we are able to scan
                                The method returns the signal strength in %
        """
        if not isinstance(ssid, str):
            return -1
        if not self.nm:
            return -1
        if (
            self.primary_wifi_interface == "/"
            or not self.primary_wifi_interface
        ):
            return -1

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
        return -1

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

            active_path = self.nm.activate_connection(str(_connection_path))

        except Exception as e:
            raise Exception(
                f"Unknown error while trying to connect to {ssid} network: {e}"
            )
        return active_path

    def delete_network(self, ssid: str) -> typing.Union[typing.Dict, None]:
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
            raise TypeError("SSID argument is of type string")
        if not self.is_known(ssid):
            logging.debug(f"No known network with SSID {ssid}")
            return

        _path = self.get_connection_path_by_ssid(ssid)

        try:
            NetworkConnectionSettings(settings_path=str(_path)).delete()
            return {"status": "success"}
        except Exception as e:
            logging.debug(f"Unexpected exception detected: {e}")
            return {"status": "error"}

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
            NetworkManagerSettings().add_connection(properties)
            return {"status": "success"}
        except Exception as e:
            logging.debug(
                f"Error occurred while adding hotspot connection: {e.args}"
            )
            return {"status": "error, exception"}

    def get_hotspot_ssid(self) -> str:
        return self.hotspot_ssid

    def set_hotspot_ssid(self, ssid: str) -> None:
        self.hotspot_ssid = ssid
        self.create_hotspot(ssid=ssid)

    def set_network_priority(self, ssid: str, priority: str) -> None:
        if not self.nm:
            return
        ...
        # Get Networks by ssid
        # con_settings = NetworkConnectionSettings(a connection path for the connection with the specified ssid)
        # properties = con_settings.get_settings()
        # profile = con_settings.get_profile()
        # properties["connection"]["autoconnect-priority"] = ("u", priority)
        # con_settings.update(properties)

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
            con_settings = NetworkConnectionSettings(str(_connection_path))
            properties = con_settings.get_settings()
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

    def get_current_ssid(self) -> str:
        return "Blocks"

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
        self.hotspot_active = toggle

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
        print("added network", ssid)
        print(psk)
        return {"status": "asdas", "msg": "dummy"}

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
        return random.randint(1, 100)

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
        print(self.hotspot_ssid)
        return self.hotspot_ssid

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
        print(new_ssid)
        print(f"Updated a network connection {ssid} | {password} | {new_ssid}")
        return {"status": "AUGH", "msg": "dummy"}

