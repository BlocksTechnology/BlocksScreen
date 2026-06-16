"""Async D-Bus client worker for the blockscreen daemon"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Coroutine

import sdbus
from PyQt6 import QtCore

if TYPE_CHECKING:
    from updater.dbus_service import UpdaterInterface

_log = logging.getLogger(__name__)


_RECONNECT_DELAYS = (5.0, 15.0, 30.0, 60.0)

# Max seconds of *silence* from a busy daemon before declaring it gone.
# Progress signals refresh the deadline, so long multi-component updates
# (big apt upgrades, several klipper restarts) never trip it as long as
# the daemon keeps reporting steps.
_BUSY_IDLE_LIMIT = 360.0


class UpdaterWorker(QtCore.QObject):
    """Async D-Bus client for the blockscreen updater daemon.

    Owns an asyncio event loop on a dedicated daemon thread.
    All D-Bus operations execute as coroutines on that loop.
    Results are bridged back to Qt via pyqtSignals
    """

    status_ready = QtCore.pyqtSignal(str)
    step_complete = QtCore.pyqtSignal(str, int, int)
    component_done = QtCore.pyqtSignal(str, bool)
    error_occurred = QtCore.pyqtSignal(str, str)
    rollback_done = QtCore.pyqtSignal(str, bool)
    recover_done = QtCore.pyqtSignal(str, bool)
    busy_changed = QtCore.pyqtSignal(bool)
    daemon_unavailable = QtCore.pyqtSignal()
    request_reconnect = QtCore.pyqtSignal()
    proxy_connected = QtCore.pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._loop = asyncio.new_event_loop()
        self._listener_tasks: list[asyncio.Task] = []
        self._watchdog_tasks: set[asyncio.Task] = set()
        # Created on the asyncio thread in _async_initialize, not here.
        self._busy_false_event: asyncio.Event | None = None
        self._proxy: UpdaterInterface | None = None
        self._reconnect_attempt: int = 0
        self._reconnecting: bool = False
        self._shutting_down: bool = False
        self._last_activity: float = 0.0
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True, name="UpdaterAsyncLoop"
        )
        self._thread.start()

    def _run_loop(self) -> None:
        """Entry point for the asyncio daemon thread."""
        asyncio.set_event_loop(self._loop)
        try:
            self._system_bus = sdbus.sd_bus_open_system()
        except Exception as exc:  # noqa: BLE001
            _log.error("sd_bus_open_system failed: %s — restarting thread in 10s", exc)
            self._loop.close()
            if not self._shutting_down:
                self._restart_loop_thread(delay=10.0)
            return
        self._loop.create_task(self._async_initialize(), name="updater_init")
        try:
            self._loop.run_forever()
        except Exception as exc:  # noqa: BLE001
            _log.error("asyncio event loop crashed: %s", exc, exc_info=True)
        finally:
            self._loop.close()
            if not self._shutting_down:
                self._restart_loop_thread(delay=5.0)

    def _restart_loop_thread(self, delay: float = 5.0) -> None:
        """Recreate the asyncio loop and daemon thread after a fatal error."""
        _log.info("scheduling asyncio thread restart in %.0fs", delay)

        def _do_restart() -> None:
            time.sleep(delay)
            if self._shutting_down:
                _log.info("skipping asyncio thread restart — shutting down")
                return
            _log.info("restarting asyncio daemon thread")
            self._loop = asyncio.new_event_loop()
            self._thread = threading.Thread(
                target=self._run_loop, daemon=True, name="UpdaterAsyncLoop"
            )
            self._thread.start()

        threading.Thread(
            target=_do_restart, daemon=True, name="UpdaterLoopRestart"
        ).start()

    async def _async_initialize(self) -> None:
        """Connect proxy and start all signal listener tasks."""
        from updater.dbus_service import UpdaterInterface  # noqa: PLC0415

        if self._busy_false_event is not None:
            self._busy_false_event.set()
        self._busy_false_event = asyncio.Event()
        self._reconnecting = False

        try:
            self._proxy = UpdaterInterface.new_proxy(
                "com.blockscreen.Updater",
                "/com/blockscreen/Updater",
                bus=self._system_bus,
            )
        except sdbus.SdBusBaseError as exc:
            _log.error("updater daemon unavailable: %s", exc)
            self.daemon_unavailable.emit()
            self._schedule_reconnect()
            return

        self._reconnect_attempt = 0
        self._reconnecting = False
        _log.info("proxy connected (reconnect_attempt reset to 0), starting listeners")
        for task in self._listener_tasks:
            task.cancel()
        self._listener_tasks.clear()
        listeners = [
            self._listen_status_ready,
            self._listen_step_complete,
            self._listen_component_done,
            self._listen_error,
            self._listen_rollback,
            self._listen_recover_done,
            self._listen_busy_changed,
        ]
        for fn in listeners:
            task = asyncio.create_task(fn(), name=fn.__name__)
            self._listener_tasks.append(task)
            task.add_done_callback(self._on_listener_done)

        # Let each listener enter its async-for and register its D-Bus signal
        # subscription before we poll current state (one sleep(0) per task).
        for _ in listeners:
            await asyncio.sleep(0)

        try:
            busy = await self._proxy.get_busy()
        except sdbus.SdBusBaseError as exc:
            # Proxy creation is lazy; this first real call is what proves the
            # daemon is actually reachable. Treat failure as daemon-down.
            _log.warning("get_busy failed on (re)connect: %s — scheduling retry", exc)
            self.daemon_unavailable.emit()
            self._schedule_reconnect()
            return
        if busy:
            self._busy_false_event.clear()
        else:
            self._busy_false_event.set()
        _log.info("get_busy() on reconnect → %s", busy)
        self.busy_changed.emit(busy)
        if not busy:
            self.request_reconnect.emit()

        self.proxy_connected.emit()

    def _on_listener_done(self, task: asyncio.Task) -> None:
        """Emit daemon_unavailable and schedule reconnect if a listener exits unexpectedly."""
        if task.cancelled():
            return
        exc = task.exception()
        if exc is not None:
            _log.error(
                "listener task %s failed: %s", task.get_name(), exc, exc_info=exc
            )
            if isinstance(exc, Exception) and not self._reconnecting:
                _log.warning(
                    "daemon_unavailable: emitting signal and scheduling reconnect"
                )
                self.daemon_unavailable.emit()
                self._schedule_reconnect()

    def _schedule_reconnect(self) -> None:
        """Schedule _async_initialize retry with exponential backoff.

        Idempotent: if a reconnect is already pending this is a no-op, so it is
        safe to call from every failing listener without spawning duplicate tasks.
        """
        if self._reconnecting:
            return
        self._reconnecting = True
        self._reconnect_attempt += 1
        delay = _RECONNECT_DELAYS[
            min(self._reconnect_attempt - 1, len(_RECONNECT_DELAYS) - 1)
        ]
        _log.info(
            "scheduling reconnect in %.0fs (attempt %d)", delay, self._reconnect_attempt
        )
        try:
            asyncio.get_running_loop().create_task(
                self._delayed_reconnect(delay), name="reconnect"
            )
        except RuntimeError:
            self._reconnecting = False
            _log.warning("_schedule_reconnect called outside running loop — skipped")

    async def _delayed_reconnect(self, delay: float) -> None:
        """Sleep for ``delay`` seconds then re-run ``_async_initialize``."""
        await asyncio.sleep(delay)
        await self._async_initialize()

    def _require_proxy(self) -> bool:
        """Return True if the D-Bus proxy is ready; emit daemon_unavailable and return False otherwise."""
        if self._proxy is None:
            self.daemon_unavailable.emit()
            return False
        return True

    # --- Public API (QT -> asyncio thread) ---------------------------

    def trigger_update(self, name: str = "") -> None:
        """Queue an update; name='' updates all components."""
        if not self._require_proxy():
            return
        coro = self._call_update_all() if not name else self._call_update(name)
        self._submit(coro)

    def trigger_status(self) -> None:
        """Request a status check; result arrives via status_ready signal."""
        if not self._require_proxy():
            return
        _log.debug("trigger_status called")
        self._submit(self._call_status())

    def trigger_recover(self, name: str, hard: bool) -> None:  # noqa: FBT001
        """Request recovery for a component."""
        if not self._require_proxy():
            return
        self._submit(self._call_recover(name, hard))

    def trigger_cancel(self) -> None:
        """Cancel any running update; no-op if nothing is in progress."""
        if not self._require_proxy():
            return
        _log.info("trigger_cancel: cancelling active update (E-stop)")
        self._submit(self._call_cancel())

    def shutdown(self) -> None:
        """Cancel all tasks and stop the event loop; close() runs in _run_loop after stop."""  # noqa: E501
        self._shutting_down = True

        def _cancel_and_stop() -> None:
            for task in self._listener_tasks:
                task.cancel()
            for task in list(self._watchdog_tasks):
                task.cancel()
            self._loop.stop()

        try:
            self._loop.call_soon_threadsafe(_cancel_and_stop)
        except RuntimeError:
            _log.warning(
                "shutdown: loop already closed (crashed during restart window)"
            )

    def _submit(self, coro: Coroutine[Any, Any, None]) -> None:
        """Submit a coroutine to the asyncio loop, emit daemon_unavailable if loop is closed."""  # noqa: E501
        try:
            asyncio.run_coroutine_threadsafe(coro, self._loop)
        except RuntimeError:
            coro.close()
            _log.error("asyncio loop is closed, daemon is unavailable")
            self.daemon_unavailable.emit()

    # --- Internal coroutines ---------------------------------------

    def _handle_proxy_error(self, exc: Exception, method: str) -> None:
        """Log a D-Bus call failure, emit daemon_unavailable, and schedule a reconnect.

        While a reconnect is already pending the emit is suppressed: the UI's
        daemon-unavailable handler triggers a status refresh, which would fail
        and re-emit here — an endless toast/request storm without this guard.
        """
        _log.error("%s D-Bus call failed: %s", method, exc)
        if not self._reconnecting:
            self.daemon_unavailable.emit()
        self._schedule_reconnect()

    async def _call_update_all(self) -> None:
        """Call update_all on the proxy; log a warning if the daemon rejects it as busy."""
        try:
            accepted = await self._proxy.update_all()
            if not accepted:
                _log.warning("update_all was rejected: daemon is busy")
        except sdbus.SdBusBaseError as exc:
            self._handle_proxy_error(exc, "update_all")

    async def _call_update(self, name: str) -> None:
        """Call update_component for a single named component."""
        try:
            accepted = await self._proxy.update_component(name)
            if not accepted:
                _log.warning("update_component(%r) was rejected: daemon is busy", name)
        except sdbus.SdBusBaseError as exc:
            self._handle_proxy_error(exc, "update_component")

    async def _call_status(self) -> None:
        """Ask the daemon to broadcast a fresh status_ready signal."""
        try:
            await self._proxy.request_status()
        except sdbus.SdBusBaseError as exc:
            self._handle_proxy_error(exc, "request_status")

    async def _call_recover(self, name: str, hard: bool) -> None:  # noqa: FBT001
        """Call recover on the proxy; hard=True performs a full reinstall."""
        try:
            accepted = await self._proxy.recover(name, hard)
            if not accepted:
                _log.warning("recover(%r) was rejected: daemon is busy", name)
        except sdbus.SdBusBaseError as exc:
            self._handle_proxy_error(exc, "recover")

    async def _call_cancel(self) -> None:
        """Send a cancel request to abort the running update."""
        try:
            await self._proxy.cancel()
        except sdbus.SdBusBaseError as exc:
            self._handle_proxy_error(exc, "cancel")

    # --- Signal listeners ------------------------------------------

    async def _listen_status_ready(self) -> None:
        """Forward status_ready D-Bus signals to the Qt status_ready signal."""
        async for json_str in self._proxy.status_ready:
            _log.debug("status_ready received (%d bytes)", len(json_str))
            self.status_ready.emit(json_str)

    def _touch_activity(self) -> None:
        """Record daemon liveness; refreshes the busy-watchdog deadline."""
        self._last_activity = self._loop.time()

    async def _listen_step_complete(self) -> None:
        """Forward step_complete D-Bus signals to the Qt step_complete signal."""
        async for name, step, total in self._proxy.step_complete:
            self._touch_activity()
            self.step_complete.emit(name, step, total)

    async def _listen_component_done(self) -> None:
        """Forward component_done D-Bus signals to the Qt component_done signal."""
        async for name, success in self._proxy.component_done:
            self._touch_activity()
            self.component_done.emit(name, success)

    async def _listen_error(self) -> None:
        """Forward error D-Bus signals to the Qt error_occurred signal."""
        async for name, reason in self._proxy.error:
            self._touch_activity()
            self.error_occurred.emit(name, reason)

    async def _listen_rollback(self) -> None:
        """Forward rollback D-Bus signals to the Qt rollback_done signal."""
        async for name, success in self._proxy.rollback:
            self.rollback_done.emit(name, success)

    async def _listen_recover_done(self) -> None:
        """Forward recover_done D-Bus signals to the Qt recover_done signal."""
        async for name, success in self._proxy.recover_done:
            self.recover_done.emit(name, success)

    async def _listen_busy_changed(self) -> None:
        """Forward busy_changed signals and manage the busy_false_event + watchdog task."""
        if self._busy_false_event is None:
            _msg = "_busy_false_event not initialized"
            raise RuntimeError(_msg)
        async for busy in self._proxy.busy_changed:
            _log.info("busy_changed received: %s", busy)
            self._touch_activity()
            if busy:
                self._busy_false_event.clear()
                task = asyncio.create_task(self._busy_watchdog(), name="busy_watchdog")
                self._watchdog_tasks.add(task)
                task.add_done_callback(self._watchdog_tasks.discard)
            else:
                self._busy_false_event.set()
            self.busy_changed.emit(busy)

    async def _busy_watchdog(self) -> None:
        """Emit daemon_unavailable after _BUSY_IDLE_LIMIT seconds of daemon silence.

        Any progress signal (step_complete, component_done, error, busy_changed)
        refreshes the deadline via _touch_activity, so the watchdog only fires
        when a busy daemon stops reporting entirely — not on long updates.
        """
        if self._busy_false_event is None:
            _msg = "_busy_false_event not initialized"
            raise RuntimeError(_msg)
        while True:
            if self._busy_false_event.is_set():
                return
            idle = self._loop.time() - self._last_activity
            remaining = _BUSY_IDLE_LIMIT - idle
            if remaining <= 0:
                _log.error(
                    "busy watchdog: no daemon activity for %.0fs — daemon unavailable",
                    idle,
                )
                self.daemon_unavailable.emit()
                self._schedule_reconnect()
                return
            try:
                async with asyncio.timeout(remaining):
                    await self._busy_false_event.wait()
                return
            except TimeoutError:
                continue
