"""Hotplug side of the device templates.

`DeviceConfigWatcher` listens to the discovery daemon through
`DeviceDiscoveryClient` and, when a serial device matching a template shows
up, has `DeviceConfigManager` update printer.cfg. It then emits
`config_changed` with the profile names so the UI can restart Klipper - the
new config only takes effect after one.

Templates that need the user's OK (`confirm: true`, the AMU) are not
applied straight away: `confirmation_required` asks the UI first, and the
change is only written when the UI calls `accept()`. `decline()` leaves
printer.cfg alone until that device is plugged in again.

When the daemon isn't reachable (not installed, not started yet, crashed),
/dev/serial/by-id is polled instead so hotplug still works.

Unplugging is only logged: the next boot's sync reverts what the device
added, which avoids rewriting printer.cfg over a USB glitch mid-print.
"""

from __future__ import annotations

import logging
import typing

from devices.discovery.client import DeviceDiscoveryClient
from devices.discovery.serial_devices import Device, SerialScanner, device_from_json
from PyQt6 import QtCore

if typing.TYPE_CHECKING:
    from .device_configurator import DeviceConfigManager

_logger = logging.getLogger(__name__)


# pylint: disable-next=too-many-instance-attributes
class DeviceConfigWatcher(QtCore.QObject):
    """Applies device templates to printer.cfg as the daemon reports devices."""

    config_changed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        list, name="device-config-changed"
    )
    confirmation_required: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        list, name="device-config-confirmation-required"
    )

    # Events inside this window are applied together: a burst of udev
    # activity, or a daemon misbehaving and flooding events, costs one
    # printer.cfg read/write instead of one per message on the GUI thread.
    COALESCE_MS = 300
    # /dev/serial/by-id poll interval while the daemon is unreachable.
    POLL_MS = 2000

    def __init__(
        self,
        manager: DeviceConfigManager,
        client: DeviceDiscoveryClient | None = None,
        parent: QtCore.QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._manager = manager
        self._pending: dict[str, Device] = {}
        # Serial devices plugged in right now, by by-id name.
        self._present: dict[str, Device] = {}
        # Profiles the UI is asking about, and the ones the user declined
        # (asked again only once their device is unplugged and replugged).
        self._asking: set[str] = set()
        self._declined: set[str] = set()
        self._flush_timer = QtCore.QTimer(self)
        self._flush_timer.setSingleShot(True)
        self._flush_timer.setInterval(self.COALESCE_MS)
        self._flush_timer.timeout.connect(self._flush)
        self._poll_timer = QtCore.QTimer(self)
        self._poll_timer.setInterval(self.POLL_MS)
        self._poll_timer.timeout.connect(self._poll)
        self._client = client if client is not None else DeviceDiscoveryClient()
        # The client emits from its reader thread; these queue onto the
        # thread this watcher lives in (the GUI thread), so file writes and
        # the UI prompt happen there.
        self._client.device_added.connect(self._on_device_added)
        self._client.device_removed.connect(self._on_device_removed)
        self._client.snapshot_ready.connect(self._on_snapshot)
        self._client.daemon_connected.connect(self._on_daemon_connected)
        self._client.daemon_disconnected.connect(self._on_daemon_disconnected)

    def start(self) -> None:
        """Start listening to the daemon (signals are already connected)."""
        self._client.start()

    def stop(self) -> None:
        """Stop listening."""
        self._flush_timer.stop()
        self._poll_timer.stop()
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
        self._present.clear()
        self._queue(devices)
        self._forget_declined()

    @QtCore.pyqtSlot(dict)
    def _on_device_removed(self, device: dict) -> None:
        name = device.get("symlink_name") if isinstance(device, dict) else None
        _logger.info(
            "Device removed: %s (printer.cfg is reconciled at next boot)",
            name or (device.get("name") if isinstance(device, dict) else device),
        )
        if name:
            self._present.pop(name, None)
            self._pending.pop(name, None)
        self._forget_declined()

    @QtCore.pyqtSlot()
    def _on_daemon_connected(self) -> None:
        # The daemon's snapshot follows and takes over from the poll.
        if self._poll_timer.isActive():
            _logger.info("device_discoveryd reachable again, stopping by-id polling")
        self._poll_timer.stop()

    @QtCore.pyqtSlot()
    def _on_daemon_disconnected(self) -> None:
        if not self._poll_timer.isActive():
            _logger.info("device_discoveryd unreachable, polling /dev/serial/by-id")
            self._poll()
            self._poll_timer.start()

    def _poll(self) -> None:
        try:
            current = {d.symlink_name: d for d in SerialScanner.legacy_scan()}
        except Exception:  # pylint: disable=broad-except
            _logger.exception("Polling /dev/serial/by-id failed")
            return
        for name in set(self._present) - set(current):
            self._on_device_removed({"symlink_name": name})
        added = [d for n, d in current.items() if n not in self._present]
        if added:
            self._add_devices(added)

    def _queue(self, raw_devices: list) -> None:
        devices = []
        try:
            for raw in raw_devices:
                if isinstance(raw, dict) and raw.get("connection") == "Serial":
                    dev = device_from_json(raw)
                    if dev.symlink_name:
                        devices.append(dev)
        except Exception:  # pylint: disable=broad-except
            _logger.exception("Ignoring unusable device report")
        self._add_devices(devices)

    def _add_devices(self, devices: list[Device]) -> None:
        for dev in devices:
            if dev.symlink_name not in self._present:
                self._log_device(dev)
            self._present[dev.symlink_name] = dev
            self._pending[dev.symlink_name] = dev
        if self._pending and not self._flush_timer.isActive():
            self._flush_timer.start()

    def _log_device(self, dev: Device) -> None:
        """Log a newly seen serial device and whether a profile recognises it.

        The one place that says why a board did or didn't trigger anything:
        its USB ID (from the daemon or sysfs) and the profiles that match.
        """
        try:
            matches = self._manager.matching_profiles(dev)
        except Exception:  # pylint: disable=broad-except
            _logger.exception("Matching device profiles failed")
            matches = []
        _logger.info(
            "Serial device seen: %s path=%s usb_id=%s:%s profiles=%s",
            dev.symlink_name,
            dev.device_path or "-",
            dev.vid_hex or "-",
            dev.pid_hex or "-",
            ", ".join(matches) or "none",
        )

    def _forget_declined(self) -> None:
        """Drop declines (and open questions) whose device is no longer plugged in."""
        if not self._declined and not self._asking:
            return
        try:
            still = set(
                self._manager.pending_confirmation(list(self._present.values()))
            )
        except Exception:  # pylint: disable=broad-except
            _logger.exception("Checking pending device confirmations failed")
            return
        self._declined &= still
        self._asking &= still

    def _flush(self) -> None:
        devices = list(self._pending.values())
        self._pending.clear()
        if not devices:
            return
        self._apply(devices)
        try:
            waiting = self._manager.pending_confirmation(list(self._present.values()))
        except Exception:  # pylint: disable=broad-except
            _logger.exception("Checking pending device confirmations failed")
            return
        ask = [n for n in waiting if n not in self._declined and n not in self._asking]
        skipped = sorted(set(waiting) - set(ask))
        if skipped:
            _logger.info(
                "Not asking again for %s (declined or already asking)",
                ", ".join(skipped),
            )
        if ask:
            self._asking.update(ask)
            _logger.info("Device templates waiting for the user: %s", ", ".join(ask))
            self.confirmation_required.emit(ask)

    def _apply(self, devices: list[Device]) -> None:
        try:
            changed = self._manager.apply_devices(devices)
        except Exception:  # pylint: disable=broad-except
            _logger.exception("Applying device templates failed")
            return
        if changed:
            _logger.info("Device templates applied: %s", ", ".join(changed))
            self.config_changed.emit(changed)

    @QtCore.pyqtSlot(list, name="accept-device-config")
    def accept(self, names: list) -> None:
        """The user accepted these profiles: remember that and apply them now."""
        self._asking.difference_update(names)
        self._declined.difference_update(names)
        try:
            self._manager.accept(names)
        except Exception:  # pylint: disable=broad-except
            _logger.exception("Recording accepted device templates failed")
            return
        _logger.info("User accepted device templates: %s", ", ".join(names))
        self._apply(list(self._present.values()))

    @QtCore.pyqtSlot(list, name="decline-device-config")
    def decline(self, names: list) -> None:
        """The user declined these profiles: leave printer.cfg alone until replug."""
        self._asking.difference_update(names)
        self._declined.update(names)
        _logger.info("User declined device templates: %s", ", ".join(names))
