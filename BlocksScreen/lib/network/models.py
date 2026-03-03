"""Data models for the NetworkManager subsystem."""

import sys
from dataclasses import dataclass
from enum import Enum, IntEnum


class SecurityType(str, Enum):
    """Wi-Fi security types."""

    OPEN = "open"
    WEP = "wep"
    WPA_PSK = "wpa-psk"
    WPA2_PSK = "wpa2-psk"
    WPA3_SAE = "sae"
    WPA_EAP = "wpa-eap"
    OWE = "owe"
    UNKNOWN = "unknown"


# Security types this device cannot connect to.
UNSUPPORTED_SECURITY_TYPES: frozenset[str] = frozenset(
    {
        SecurityType.WEP.value,
        SecurityType.WPA_EAP.value,
        SecurityType.OWE.value,
        SecurityType.OPEN.value,
    }
)


def is_connectable_security(security: "SecurityType | str") -> bool:
    """Return True if this device can connect to *security* type."""
    return security not in UNSUPPORTED_SECURITY_TYPES


class ConnectivityState(IntEnum):
    """NetworkManager connectivity states."""

    UNKNOWN = 0
    NONE = 1
    PORTAL = 2
    LIMITED = 3
    FULL = 4


class ConnectionPriority(IntEnum):
    """Autoconnect priority levels for saved connections (higher = \
    preferred)."""

    LOW = 20
    MEDIUM = 50
    HIGH = 90
    HIGHEST = 100


class PendingOperation(IntEnum):
    """Identifies which network transition is currently in-flight."""

    NONE = 0
    WIFI_ON = 1
    WIFI_OFF = 2
    HOTSPOT_ON = 3
    HOTSPOT_OFF = 4
    CONNECT = 5
    ETHERNET_ON = 6
    ETHERNET_OFF = 7
    WIFI_STATIC_IP = 8  # static IP or resetting to DHCP on a Wi-Fi profile
    VLAN_DHCP = 9  # VLAN with DHCP (long-running, up to 45 s)


class NetworkStatus(IntEnum):
    """State of a Wi-Fi network from the device's perspective.

    Values are ordered so that higher values indicate a "more connected"
    state.  This lets callers use comparison operators for grouping::

        is_saved  <->  network.network_status >= NetworkStatus.SAVED
        is_active <->  network.network_status == NetworkStatus.ACTIVE

    ``is_open`` is **not** encoded here because it is a property of the
    network's *security type*, not its connection state.  Use
    ``NetworkInfo.is_open`` (derived from ``security_type``) instead.
    """

    DISCOVERED = 0  # Seen in scan, not saved — protected security
    OPEN = 1  # Seen in scan, not saved — open (no passphrase)
    SAVED = 2  # Profile saved on this device
    ACTIVE = 3  # Currently connected
    HIDDEN = 4  # Hidden-network placeholder

    @property
    def label(self) -> str:
        """Human-readable status label for UI display."""
        return _STATUS_LABELS[self]

    @staticmethod
    def update_status_label(status: "NetworkStatus", label: str) -> None:
        """Update the human-readable label for a given network status."""
        _STATUS_LABELS[status] = sys.intern(label)


_STATUS_LABELS: dict[NetworkStatus, str] = {
    NetworkStatus.DISCOVERED: sys.intern("Protected"),
    NetworkStatus.OPEN: sys.intern("Open"),
    NetworkStatus.SAVED: sys.intern("Saved"),
    NetworkStatus.ACTIVE: sys.intern("Active"),
    NetworkStatus.HIDDEN: sys.intern("Hidden"),
}


SIGNAL_EXCELLENT_THRESHOLD = 75
SIGNAL_GOOD_THRESHOLD = 50
SIGNAL_FAIR_THRESHOLD = 25
SIGNAL_MINIMUM_THRESHOLD = 5


def signal_to_bars(signal: int) -> int:
    """Convert signal strength percentage (0-100) to bar count (0-4)."""
    if signal < SIGNAL_MINIMUM_THRESHOLD:
        return 0
    if signal >= SIGNAL_EXCELLENT_THRESHOLD:
        return 4
    if signal >= SIGNAL_GOOD_THRESHOLD:
        return 3
    if signal > SIGNAL_FAIR_THRESHOLD:
        return 2
    return 1


class WifiIconKey(IntEnum):
    """Lightweight icon key for the header Wi-Fi status icon.

    Encodes signal bars (0-4), protection status, and special states
    into a single integer for cheap cross-thread signalling via
    pyqtSignal(int).

    Encoding: ethernet = -1, hotspot = 10, wifi = bars * 2 + is_protected
    Range: -1, 0..10
    """

    ETHERNET = -1

    WIFI_0_OPEN = 0
    WIFI_0_PROTECTED = 1
    WIFI_1_OPEN = 2
    WIFI_1_PROTECTED = 3
    WIFI_2_OPEN = 4
    WIFI_2_PROTECTED = 5
    WIFI_3_OPEN = 6
    WIFI_3_PROTECTED = 7
    WIFI_4_OPEN = 8
    WIFI_4_PROTECTED = 9

    HOTSPOT = 10

    @classmethod
    def from_bars(cls, bars: int, is_protected: bool) -> "WifiIconKey":
        """Encode bar count (0-4) + protection flag into a WifiIconKey."""
        if not 0 <= bars <= 4:
            raise ValueError(f"Bars must be 0-4 (got {bars})")
        return cls(bars * 2 + int(is_protected))

    @classmethod
    def from_signal(cls, signal_strength: int, is_protected: bool) -> "WifiIconKey":
        """Convert raw signal strength + protection to a WifiIconKey."""
        return cls.from_bars(signal_to_bars(signal_strength), is_protected)

    @property
    def bars(self) -> int:
        """Signal bars (0-4). Raises ValueError for ETHERNET/HOTSPOT."""
        if self is WifiIconKey.ETHERNET or self is WifiIconKey.HOTSPOT:
            raise ValueError(f"{self.name} has no bar count")
        return self.value // 2

    @property
    def is_protected(self) -> bool:
        """Whether the network is protected.
        Raises ValueError for ETHERNET/HOTSPOT."""
        if self is WifiIconKey.ETHERNET or self is WifiIconKey.HOTSPOT:
            raise ValueError(f"{self.name} has no protection status")
        return bool(self.value % 2)


@dataclass(frozen=True, slots=True)
class NetworkInfo:
    """Represents a single Wi-Fi access point discovered during a scan.

    Connection state is encoded in *network_status* (a single ``int``
    the same width as the four booleans it replaced).  Security openness
    is derived from *security_type* via the ``is_open`` property.
    """

    ssid: str = ""
    signal_strength: int = 0
    network_status: NetworkStatus = NetworkStatus.DISCOVERED
    bssid: str = ""
    frequency: int = 0
    max_bitrate: int = 0
    security_type: SecurityType | str = SecurityType.UNKNOWN

    @property
    def is_open(self) -> bool:
        """True when the AP broadcasts no security flags."""
        return self.security_type == SecurityType.OPEN

    @property
    def is_saved(self) -> bool:
        """True when a profile for this network exists on the device."""
        return self.network_status >= NetworkStatus.SAVED

    @property
    def is_active(self) -> bool:
        """True when the device is currently connected to this AP."""
        return self.network_status == NetworkStatus.ACTIVE

    @property
    def is_hidden(self) -> bool:
        """True for hidden-network placeholders."""
        return self.network_status == NetworkStatus.HIDDEN

    @property
    def status(self) -> str:
        """Human-readable status label (Active > Saved > Open > Protected)."""
        return self.network_status.label


@dataclass(frozen=True, slots=True)
class SavedNetwork:
    """Represents a saved (known) Wi-Fi connection profile."""

    ssid: str = ""
    uuid: str = ""
    connection_path: str = ""
    security_type: str = ""
    mode: str = "infrastructure"
    priority: int = ConnectionPriority.MEDIUM.value
    signal_strength: int = 0
    timestamp: int = 0  # Unix time of last successful activation
    is_dhcp: bool = True  # True = auto (DHCP), False = manual (static IP)


@dataclass(frozen=True, slots=True)
class ConnectionResult:
    """Outcome of a connection/network operation."""

    success: bool = False
    message: str = ""
    error_code: str = ""
    data: dict[str, object] | None = None


@dataclass(frozen=True, slots=True)
class VlanInfo:
    """Snapshot of an active VLAN connection."""

    vlan_id: int = 0
    ip_address: str = ""
    interface: str = ""
    gateway: str = ""
    dns_servers: tuple[str, ...] = ()
    is_dhcp: bool = False


@dataclass(frozen=True, slots=True)
class NetworkState:
    """Snapshot of the current network state."""

    connectivity: ConnectivityState = ConnectivityState.UNKNOWN
    current_ssid: str | None = None
    current_ip: str = ""
    wifi_enabled: bool = False
    hotspot_enabled: bool = False
    primary_interface: str = ""
    signal_strength: int = 0
    security_type: str = ""
    ethernet_connected: bool = False
    ethernet_carrier: bool = False
    active_vlans: tuple[VlanInfo, ...] = ()


class HotspotSecurity(str, Enum):
    """Supported hotspot security protocols.

    The *value* is the internal key passed through manager -> worker;
    the NM ``key-mgmt`` and cipher settings are resolved at profile
    creation time in ``create_and_activate_hotspot``.
    """

    WPA1 = "wpa1"
    WPA2_PSK = "wpa-psk"  # WPA2-PSK (CCMP) — default

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Return True if *value* matches a known security key."""
        return value in cls._value2member_map_


@dataclass(slots=True)
class HotspotConfig:
    """Mutable configuration for the access-point / hotspot."""

    ssid: str = "PrinterHotspot"
    password: str = "123456789"
    band: str = "bg"
    channel: int = 6
    security: str = HotspotSecurity.WPA2_PSK.value


# Patterns that indicate a hidden or invalid SSID
_HIDDEN_INDICATORS = frozenset({"unknown", "hidden", "<hidden>"})


def is_hidden_ssid(ssid: str | None) -> bool:
    """Return True if *ssid* is blank, whitespace, null-bytes, or a
    well-known hidden-network placeholder.

    Handles: None, "", "   ", "\\x00\\x00", "unknown", "UNKNOWN",
    "hidden", "<hidden>", "<HIDDEN>".
    """
    if not ssid:
        return True
    stripped = ssid.strip()
    if not stripped:
        return True
    if stripped[0] == "\x00" and all(c == "\x00" for c in stripped):
        return True
    return stripped.lower() in _HIDDEN_INDICATORS
