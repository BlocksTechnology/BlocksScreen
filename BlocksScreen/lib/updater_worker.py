"""Async D-Bus client worker for the blockscreen daemon"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from contextlib import aclosing, suppress
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Coroutine

import sdbus
from PyQt6 import QtCore

if TYPE_CHECKING:
    from updater.dbus_service import UpdaterInterface

_log = logging.getLogger(__name__)


def _dbus_daemon(bus: Any) -> Any:
    """Proxy to org.freedesktop.DBus; imported lazily to keep module import Qt-only."""
    from sdbus_async.dbus_daemon import FreedesktopDbus

    return FreedesktopDbus(bus=bus)


_RECONNECT_DELAYS = (5.0, 15.0, 30.0, 60.0)

# Max silence from a busy daemon; progress signals refresh the deadline.
_BUSY_IDLE_LIMIT = 360.0

_DAEMON_BUS_NAME = "com.blockscreen.Updater"
_UPDATER_UNIT = "BlocksScreen-updater.service"

# Reconnect attempts before asking systemd to start a unit it has given up on.
_ESCALATE_AFTER = 3


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
    update_rejected = QtCore.pyqtSignal()  # daemon refused the request (already busy)
    request_reconnect = QtCore.pyqtSignal()
    proxy_connected = QtCore.pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._loop = asyncio.new_event_loop()
        self._listener_tasks: list[asyncio.Task] = []
        self._watchdog_tasks: set[asyncio.Task] = set()
        # Strong refs for one-shot tasks: the loop only holds weak ones.
        self._bg_tasks: set[asyncio.Task] = set()
        # Created on the asyncio thread in _async_initialize, not here.
        self._busy_false_event: asyncio.Event | None = None
        self._proxy: UpdaterInterface | None = None
        self._reconnect_attempt: int = 0
        self._reconnecting: bool = False
        self._shutting_down: bool = False
        self._last_activity: float = 0.0
        # Unique bus name of the live daemon; a change means it restarted.
        self._daemon_owner: str = ""
        self._owner_task: asyncio.Task | None = None
        self._escalated: bool = False
        # Serializes the reconnect and owner-watch entry points into _connect().
        self._init_lock = asyncio.Lock()
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True, name="UpdaterAsyncLoop"
        )
        self._thread.start()

    def _track_task(self, task: asyncio.Task) -> asyncio.Task:
        """Hold a strong ref until done: the loop's own task set is weak and can collect it mid-await."""
        self._bg_tasks.add(task)
        task.add_done_callback(self._bg_tasks.discard)
        return task

    def _run_loop(self) -> None:
        """Entry point for the asyncio daemon thread."""
        asyncio.set_event_loop(self._loop)
        # Recreated per thread: an asyncio.Lock binds to the loop of its first await.
        self._init_lock = asyncio.Lock()
        try:
            self._system_bus = sdbus.sd_bus_open_system()
        except Exception as exc:  # noqa: BLE001
            _log.error("sd_bus_open_system failed: %s - restarting thread in 10s", exc)
            self._loop.close()
            if not self._shutting_down:
                self._restart_loop_thread(delay=10.0)
            return
        # Outlives _async_initialize's listener teardown: it is what triggers it.
        self._owner_task = self._loop.create_task(
            self._watch_daemon_owner(), name="updater_owner_watch"
        )
        self._track_task(
            self._loop.create_task(self._async_initialize(), name="updater_init")
        )
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
                _log.info("skipping asyncio thread restart - shutting down")
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

    async def _async_initialize(self, expect_owner: str = "") -> None:
        """Serialized (re)connect; ``expect_owner`` skips a resync for an already-connected owner."""
        async with self._init_lock:
            if expect_owner and expect_owner == self._daemon_owner:
                _log.debug("owner %s already connected - skipping resync", expect_owner)
                return
            await self._connect()

    async def _connect(self) -> None:
        """Connect proxy and start all signal listener tasks."""
        from updater.dbus_service import UpdaterInterface

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

        _log.info("proxy created, starting listeners")
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

        # One sleep(0) per task lets each listener register its subscription.
        for _ in listeners:
            await asyncio.sleep(0)

        try:
            # Bounded: an unresponsive daemon holding an open socket must not hang reconnect forever.
            async with asyncio.timeout(10):
                busy = await self._proxy.get_busy()
        except (sdbus.SdBusBaseError, TimeoutError) as exc:
            # Proxy is lazy; this first call proves the daemon is reachable.
            _log.warning("get_busy failed on (re)connect: %s - scheduling retry", exc)
            self.daemon_unavailable.emit()
            self._schedule_reconnect()
            return

        # Reset only once the daemon answers: new_proxy() is lazy and always "succeeds",
        # so resetting earlier pins backoff at 5s and starves the escalation threshold.
        self._reconnect_attempt = 0
        self._escalated = False
        self._daemon_owner = await self._name_owner()

        if busy:
            self._busy_false_event.clear()
        else:
            self._busy_false_event.set()
        _log.info("connected to owner %s, busy=%s", self._daemon_owner, busy)
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
            self._track_task(
                asyncio.get_running_loop().create_task(
                    self._delayed_reconnect(delay), name="reconnect"
                )
            )
        except RuntimeError:
            self._reconnecting = False
            _log.warning("_schedule_reconnect called outside running loop - skipped")

    async def _delayed_reconnect(self, delay: float) -> None:
        """Sleep for ``delay`` seconds then re-run ``_async_initialize``.

        Every exit path clears ``_reconnecting`` explicitly rather than via finally:
        _async_initialize may legitimately re-arm it, and finally would clobber that.
        """
        try:
            await asyncio.sleep(delay)
            if self._shutting_down:
                self._reconnecting = False
                return
            # Nothing owns the name after several tries: activation itself is failing.
            if (
                self._reconnect_attempt >= _ESCALATE_AFTER
                and not await self._name_owner()
            ):
                await self._escalate_restart()
            await self._async_initialize()
        except asyncio.CancelledError:
            self._reconnecting = False
            raise
        except Exception:  # noqa: BLE001
            # Never leave the latch stuck: it would silence every future reconnect.
            self._reconnecting = False
            _log.error("reconnect attempt failed - rescheduling", exc_info=True)
            self._schedule_reconnect()

    # --- Daemon lifecycle tracking ----------------------------------

    async def _watch_daemon_owner(self) -> None:
        """Resync on every owner change of the daemon's bus name (crash + systemd restart).

        Signal match rules use the well-known name, so listeners survive a restart -
        but the new instance never re-emits busy_changed, leaving a mid-update UI stuck
        until the 6-minute busy watchdog. This turns that into a millisecond recovery.
        """
        while not self._shutting_down:
            try:
                signals = _dbus_daemon(self._system_bus).name_owner_changed
                async with aclosing(aiter(signals)) as stream:
                    # Seeded after subscribing so no change can slip through the gap.
                    self._daemon_owner = await self._name_owner()
                    async for name, _old, new_owner in stream:
                        if name != _DAEMON_BUS_NAME or new_owner == self._daemon_owner:
                            continue
                        if not new_owner:
                            self._daemon_owner = ""
                            # No reconnect armed: systemd restarts it, and arming one would double-connect; if systemd gave up, the next call escalates via _handle_proxy_error.
                            _log.error("updater daemon left the bus - awaiting restart")
                            self.daemon_unavailable.emit()
                            continue
                        _log.warning(
                            "updater daemon restarted (owner=%s) - resyncing", new_owner
                        )
                        # _async_initialize owns _daemon_owner: setting it here would
                        # make its own duplicate-resync guard skip this connect.
                        await self._async_initialize(new_owner)
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001
                # Losing the watch must not be terminal: it is the fast recovery path.
                _log.error("daemon owner watch failed - retrying in 10s", exc_info=True)
            # Also covers a stream that ends without raising, which would else hot-spin.
            if not self._shutting_down:
                await asyncio.sleep(10.0)

    async def _name_owner(self) -> str:
        """Unique-name owner of the daemon bus name, empty when unowned or unreachable."""
        try:
            async with asyncio.timeout(5):
                return await _dbus_daemon(self._system_bus).get_name_owner(
                    _DAEMON_BUS_NAME
                )
        except (sdbus.SdBusBaseError, TimeoutError, OSError, ImportError):
            # NameHasNoOwner for an activatable-but-stopped unit lands here too.
            _log.debug("GetNameOwner(%s) failed", _DAEMON_BUS_NAME, exc_info=True)
            return ""

    async def _escalate_restart(self) -> None:
        """Ask systemd once to start a unit it has given up on (stale unit without StartLimitIntervalSec=0)."""
        if self._escalated:
            return
        # Latched until the next successful connect so a dead unit is not hammered.
        self._escalated = True
        _log.error(
            "daemon absent after %d attempts - asking systemd to start %s",
            self._reconnect_attempt,
            _UPDATER_UNIT,
        )
        # argv must match the NOPASSWD sudoers rules from install-updater.sh exactly.
        for args in (
            ("reset-failed", _UPDATER_UNIT),
            ("--no-block", "restart", _UPDATER_UNIT),
        ):
            await self._run_systemctl(args)

    async def _run_systemctl(self, args: tuple[str, ...]) -> None:
        """Run one sudo systemctl command, logging instead of raising on any failure."""
        label = " ".join(args)
        try:
            proc = await asyncio.create_subprocess_exec(
                "sudo",
                "-n",
                "/usr/bin/systemctl",
                *args,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE,
            )
        except OSError:
            _log.error("systemctl %s could not be spawned", label, exc_info=True)
            return
        try:
            async with asyncio.timeout(30):
                _, err = await proc.communicate()
        except TimeoutError:
            # Reap it: an orphaned sudo would hold the PIPE and the child slot forever.
            _log.error("systemctl %s timed out - killing", label)
            with suppress(ProcessLookupError):
                proc.kill()
            with suppress(Exception):
                await proc.wait()
            return
        if proc.returncode:
            _log.error(
                "systemctl %s rc=%s: %s",
                label,
                proc.returncode,
                err.decode(errors="replace").strip(),
            )

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

    def trigger_recover(self, name: str, hard: bool) -> None:
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

    def trigger_bless(self, name: str = "BlocksScreen") -> None:
        """Mark the running build healthy so the daemon records it as last_good."""
        if not self._require_proxy():
            return
        self._submit(self._call_bless(name))

    def shutdown(self) -> None:
        """Cancel all tasks and stop the event loop; close() runs in _run_loop after stop."""
        self._shutting_down = True

        def _cancel_and_stop() -> None:
            if self._owner_task is not None:
                self._owner_task.cancel()
            for task in self._listener_tasks:
                task.cancel()
            for task in list(self._watchdog_tasks) + list(self._bg_tasks):
                task.cancel()
            self._loop.stop()

        try:
            self._loop.call_soon_threadsafe(_cancel_and_stop)
        except RuntimeError:
            _log.warning(
                "shutdown: loop already closed (crashed during restart window)"
            )

    def _submit(self, coro: Coroutine[Any, Any, None]) -> None:
        """Submit a coroutine to the asyncio loop, emit daemon_unavailable if loop is closed."""
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
        and re-emit here - an endless toast/request storm without this guard.
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
                self.update_rejected.emit()
        except sdbus.SdBusBaseError as exc:
            self._handle_proxy_error(exc, "update_all")

    async def _call_update(self, name: str) -> None:
        """Call update_component for a single named component."""
        try:
            accepted = await self._proxy.update_component(name)
            if not accepted:
                _log.warning("update_component(%r) was rejected: daemon is busy", name)
                self.update_rejected.emit()
        except sdbus.SdBusBaseError as exc:
            self._handle_proxy_error(exc, "update_component")

    async def _call_status(self) -> None:
        """Ask the daemon to broadcast a fresh status_ready signal."""
        try:
            await self._proxy.request_status()
        except sdbus.SdBusBaseError as exc:
            self._handle_proxy_error(exc, "request_status")

    async def _call_recover(self, name: str, hard: bool) -> None:
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

    async def _call_bless(self, name: str) -> None:
        """Bless the current build; empty hash lets the daemon resolve HEAD."""
        try:
            await self._proxy.bless_healthy(name, "")
        except sdbus.SdBusBaseError as exc:
            self._handle_proxy_error(exc, "bless_healthy")

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
            self._touch_activity()
            self.rollback_done.emit(name, success)

    async def _listen_recover_done(self) -> None:
        """Forward recover_done D-Bus signals to the Qt recover_done signal."""
        async for name, success in self._proxy.recover_done:
            self._touch_activity()
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
        when a busy daemon stops reporting entirely - not on long updates.
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
                    "busy watchdog: no daemon activity for %.0fs - daemon unavailable",
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
