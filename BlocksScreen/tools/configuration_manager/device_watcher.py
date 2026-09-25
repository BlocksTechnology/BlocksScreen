"""Hotplug side of the device templates.

`DeviceConfigWatcher` listens to the discovery daemon through
`DeviceDiscoveryClient` and, when a serial device matching a template shows
up, has `DeviceConfigManager` update printer.cfg. It then emits
`config_changed` with the profile names so the UI can offer a Klipper
restart - the new config only takes effect after one.

Unplugging is only logged: the next boot's sync reverts what the device
added, which avoids rewriting printer.cfg over a USB glitch mid-print.
"""

from __future__ import annotations

import logging
import typing

from devices.discovery.client import DeviceDiscoveryClient
from devices.discovery.serial_devices import Device, device_from_json
from PyQt6 import QtCore

if typing.TYPE_CHECKING:
    from .device_configurator import DeviceConfigManager

_logger = logging.getLogger(__name__)


class DeviceConfigWatcher(QtCore.QObject):
    """Applies device templates to printer.cfg as the daemon reports devices."""

    config_changed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        list, name="device-config-changed"
    )

    # Events inside this window are applied together: a burst of udev
    # activity, or a daemon misbehaving and flooding events, costs one
    # printer.cfg read/write instead of one per message on the GUI thread.
    COALESCE_MS = 300

    def __init__(
        self,
        manager: DeviceConfigManager,
        client: DeviceDiscoveryClient | None = None,
        parent: QtCore.QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._manager = manager
        self._pending: dict[str, Device] = {}
        self._flush_timer = QtCore.QTimer(self)
        self._flush_timer.setSingleShot(True)
        self._flush_timer.setInterval(self.COALESCE_MS)
        self._flush_timer.timeout.connect(self._flush)
        self._client = client if client is not None else DeviceDiscoveryClient()
        # The client emits from its reader thread; these queue onto the
        # thread this watcher lives in (the GUI thread), so file writes and
        # the UI prompt happen there.
        self._client.device_added.connect(self._on_device_added)
        self._client.device_removed.connect(self._on_device_removed)
        self._client.snapshot_ready.connect(self._on_snapshot)

    def start(self) -> None:
        """Start listening to the daemon (signals are already connected)."""
        self._client.start()

    def stop(self) -> None:
        """Stop listening."""
        self._flush_timer.stop()
        self._client.stop()

    # Slots never raise: an exception escaping a Qt slot reaches CrashHandler,
    # which exits BlocksScreen. A broken daemon or template must cost at most
    # a log line, never the screen.

    @QtCore.pyqtSlot(dict)
    def _on_device_added(self, device: dict) -> None:
        self._queue([device])

    @QtCore.pyqtSlot(list)
    def _on_snapshot(self, devices: list) -> None:
        # Normally a no-op (boot sync already applied the same devices), but
        # covers devices plugged in during startup or while the daemon restarted.
        self._queue(devices)

    @QtCore.pyqtSlot(dict)
    def _on_device_removed(self, device: dict) -> None:
        _logger.info(
            "Device removed: %s (printer.cfg is reconciled at next boot)",
            device.get("symlink_name") or device.get("name"),
        )

    def _queue(self, raw_devices: list) -> None:
        try:
            for raw in raw_devices:
                if isinstance(raw, dict) and raw.get("connection") == "Serial":
                    dev = device_from_json(raw)
                    if dev.symlink_name:
                        self._pending[dev.symlink_name] = dev
        except Exception:  # pylint: disable=broad-except
            _logger.exception("Ignoring unusable device report")
        if self._pending and not self._flush_timer.isActive():
            self._flush_timer.start()

    def _flush(self) -> None:
        devices = list(self._pending.values())
        self._pending.clear()
        if not devices:
            return
        try:
            changed = self._manager.apply_devices(devices)
        except Exception:  # pylint: disable=broad-except
            _logger.exception("Applying device templates failed")
            return
        if changed:
            _logger.info("Device templates applied: %s", ", ".join(changed))
            self.config_changed.emit(changed)
