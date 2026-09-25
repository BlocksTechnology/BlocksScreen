"""Client side of the device discovery service.

The daemon itself lives in the separate DeviceDiscovery repo and runs as
device-discoveryd.service; this package only talks to its Unix socket.

- `DeviceDiscoveryClient`: long-lived Qt client (snapshot + hotplug signals)
- `fetch_snapshot`: one-shot blocking query, no Qt event loop needed
- `serial_devices.SerialScanner`: drop-in replacement for tools/serial_scanner.py
"""

from .client import DeviceDiscoveryClient, default_socket_path, fetch_snapshot

__all__ = ["DeviceDiscoveryClient", "default_socket_path", "fetch_snapshot"]
