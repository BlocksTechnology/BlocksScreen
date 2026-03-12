"""Network Manager Package

Architecture:
    NetworkManager (manager.py)
        └── Main thread interface with signals/slots
        └── Non-blocking API
        └── Caches state for quick access

    NetworkManagerWorker (worker.py)
        └── Runs in dedicated Thread
        └── Owns asyncio event loop
        └── Handles all D-Bus async operations

    Models (models.py)
        └── Data classes for type safety
        └── Enums for states and types
"""

from .manager import NetworkManager
from .models import (
    UNSUPPORTED_SECURITY_TYPES,
    ConnectionPriority,
    ConnectionResult,
    ConnectivityState,
    HotspotConfig,
    HotspotSecurity,
    NetworkInfo,
    NetworkState,
    NetworkStatus,
    PendingOperation,
    SavedNetwork,
    SecurityType,
    VlanInfo,
    WifiIconKey,
    is_connectable_security,
    is_hidden_ssid,
    signal_to_bars,
)

__all__ = [
    "NetworkManager",
    "ConnectionPriority",
    "ConnectionResult",
    "ConnectivityState",
    "HotspotConfig",
    "HotspotSecurity",
    "NetworkInfo",
    "NetworkState",
    "NetworkStatus",
    "PendingOperation",
    "SavedNetwork",
    "SecurityType",
    "UNSUPPORTED_SECURITY_TYPES",
    "VlanInfo",
    "WifiIconKey",
    # Utilities
    "is_connectable_security",
    "is_hidden_ssid",
    "signal_to_bars",
]
