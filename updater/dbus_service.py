"""D-Bus interface definition and progress callback for the updater daemon."""

from __future__ import annotations

import asyncio
import dataclasses
import json
import logging
from collections.abc import Awaitable, Callable
from functools import partial
from pathlib import Path

import sdbus

from updater.locking import process_lock
from updater.models import ComponentStatus
from updater.service import UpdateService

_log = logging.getLogger(__name__)
_STATUS_PATH = Path("/run/blockscreen/updater_status.json")
_FETCH_RETRY_INTERVAL_S = 300.0
_RECONCILE_RETRY_S = 5.0
_BOOT_DELAY_S = 3.0
_SHUTDOWN_DRAIN_S = 60.0  # < systemd's 90s stop timeout


class DbusProgressCallback:
    """Forward ProgressCallback events to D-Bus signals (decouples UpdateService"""

    def __init__(self, iface: UpdaterInterface) -> None:
        """Bind the callback to the D-Bus interface whose signals it emits."""
        self._iface = iface

    def on_step(self, name: str, step: int, total: int) -> None:
        """Emit step_complete and write the current step to the status file."""
        self._iface.step_complete.emit((name, step, total))
        try:
            _STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
            tmp = _STATUS_PATH.with_suffix(".tmp")
            tmp.write_text(json.dumps({"name": name, "step": step, "total": total}))
            tmp.replace(_STATUS_PATH)
        except OSError as e:
            _log.debug("status write failed: %s", e)

    def on_component_done(self, name: str, success: bool) -> None:
        """Emit the component_done signal."""
        self._iface.component_done.emit((name, success))

    def on_error(self, name: str, reason: str) -> None:
        """Emit the error signal."""
        self._iface.error.emit((name, reason))

    def on_rollback(self, name: str, success: bool) -> None:
        """Emit the rollback signal."""
        self._iface.rollback.emit((name, success))

    def on_recover(self, name: str, success: bool) -> None:
        """Emit the recover_done signal."""
        self._iface.recover_done.emit((name, success))


class UpdaterInterface(
    sdbus.DbusInterfaceCommonAsync,
    interface_name="com.blockscreen.Updater",
):
    """D-Bus contract shared by server and client proxy: signals declared once,"""

    @sdbus.dbus_signal_async("sii")
    def step_complete(self) -> tuple[str, int, int]:
        """Emitted after each numbered update step: (name, step, total)."""
        raise NotImplementedError

    @sdbus.dbus_signal_async("sb")
    def component_done(self) -> tuple[str, bool]:
        """Emitted when a component update finishes: (name, success)."""
        raise NotImplementedError

    @sdbus.dbus_signal_async("ss")
    def error(self) -> tuple[str, str]:
        """Emitted on a non-recoverable error: (name, reason)."""
        raise NotImplementedError

    @sdbus.dbus_signal_async("sb")
    def rollback(self) -> tuple[str, bool]:
        """Emitted after a rollback attempt: (name, success)."""
        raise NotImplementedError

    @sdbus.dbus_signal_async("sb")
    def recover_done(self) -> tuple[str, bool]:
        """Emitted after a recover() call completes: (name, success)."""
        raise NotImplementedError

    @sdbus.dbus_signal_async("s")
    def status_ready(self) -> tuple[str]:
        """Emitted with a JSON-encoded dict[str, ComponentStatus] payload."""
        raise NotImplementedError

    @sdbus.dbus_signal_async("b")
    def busy_changed(self) -> tuple[bool]:
        """Emitted on True↔False transition only (state-machine guard)."""
        raise NotImplementedError

    @sdbus.dbus_signal_async("b")
    def provisioning_changed(self) -> tuple[bool]:
        """Emitted on True↔False transition while a missing component is being installed."""
        raise NotImplementedError

    def __init__(self) -> None:
        """Start idle: busy rises only once a reachable install actually begins."""
        super().__init__()
        self._svc = UpdateService(callback=DbusProgressCallback(self))
        self._busy: bool = False
        self._provisioning: bool = False
        self._provisioned: bool = False
        self._background_tasks: set[asyncio.Task] = set()
        self._closing: bool = False
        self._status_check_in_progress: bool = False
        self._status_pending: bool = False
        self._invalid_requests: int = 0
        self._reconcile_task = self._spawn(
            self._boot_reconcile(), name="boot_reconcile"
        )
        self._spawn(self._svc.background_prime_nrestarts(), name="boot_prime_nrestarts")
        self._spawn(self._periodic_status_check(), name="periodic_status_check")
        self._spawn(self._svc.supervise_ui(), name="supervise_ui")
        self._spawn(self._svc.forward_heal_ui(), name="forward_heal_ui")

    def _spawn(self, coro, *, name: str | None = None) -> asyncio.Task:
        """Create a task and hold a strong reference so GC cannot cancel it."""
        task = asyncio.get_running_loop().create_task(coro, name=name)
        self._background_tasks.add(task)
        task.add_done_callback(self._task_done)
        if self._closing:
            task.cancel()
        return task

    async def shutdown(self) -> None:
        """Cancel background tasks, including late spawns, before the loop closes."""
        self._closing = True
        loop = asyncio.get_running_loop()
        deadline = loop.time() + _SHUTDOWN_DRAIN_S
        while pending := [t for t in self._background_tasks if not t.done()]:
            if (remaining := deadline - loop.time()) <= 0:
                _log.warning(
                    "shutdown: %d task(s) still running after %.0fs; "
                    "boot heal reverts any in-flight update",
                    len(pending),
                    _SHUTDOWN_DRAIN_S,
                )
                return
            for task in pending:
                task.cancel()
            # gather would wait out shielded rollbacks
            await asyncio.wait(pending, timeout=remaining)

    async def _boot_reconcile(self) -> None:
        """Run the boot heal; retry in the background while the lock is held."""
        if not await self._svc.reconcile():
            # The start script takes this lock on every UI start; a cold boot races it.
            _log.info("reconcile: another updater holds the lock - deferring boot heal")
            self._spawn(self._retry_reconcile(), name="boot_reconcile_retry")

    async def _retry_reconcile(self) -> None:
        """Poll until the lock frees and the deferred boot heal has run."""
        while True:
            await asyncio.sleep(_RECONCILE_RETRY_S)
            if await self._svc.reconcile():
                _log.info("reconcile: deferred boot heal done")
                return

    def _task_done(self, task: asyncio.Task) -> None:
        """Drop the task ref and log its exception now, not at some later GC."""
        self._background_tasks.discard(task)
        if task.cancelled():
            return
        exc = task.exception()
        if exc is not None:
            _log.error("task %r failed", task.get_name(), exc_info=exc)

    def _provision_busy(self, busy: bool) -> None:
        self._set_provisioning(busy)
        self._set_busy(busy)

    def _set_provisioning(self, provisioning: bool) -> None:
        if provisioning != self._provisioning:
            self._provisioning = provisioning
            self.provisioning_changed.emit((provisioning,))

    def _set_busy(self, busy: bool) -> None:
        """Emit busy_changed only on state transitions to avoid redundant signals."""
        if busy != self._busy:
            self._busy = busy
            _log.info("busy_changed -> %s", busy)
            self.busy_changed.emit((busy,))

    def _validate_component_name(self, name: str) -> bool:
        """SEC: verify component exists to prevent abuse on unknown names."""
        is_valid = self._svc.has_component(name)
        if not is_valid:
            self._invalid_requests += 1
            if self._invalid_requests > 10:
                _log.warning(
                    "excessive invalid component requests (%d), "
                    "possible fuzzing attack",
                    self._invalid_requests,
                )
        else:
            self._invalid_requests = 0
        return is_valid

    async def _emit_status(self, force: bool = False) -> None:
        """Run check_status() and emit status_ready; emits error status per component on failure."""
        if self._status_check_in_progress:
            _log.debug("_emit_status: already in progress, queueing retry")
            self._status_pending = True
            return
        self._status_check_in_progress = True
        try:
            status = await self._svc.check_status(force=force)
        except Exception as exc:  # noqa: BLE001
            _log.error("check_status failed: %s", exc)
            status = {
                name: ComponentStatus(
                    name=name,
                    kind=kind,
                    error=f"status check failed: {exc}",
                )
                for name, kind in self._svc.component_stubs()
            }
        finally:
            self._status_check_in_progress = False
            if self._status_pending:
                self._status_pending = False
                self._spawn(self._emit_status(), name="pending_status")
        payload = {name: dataclasses.asdict(s) for name, s in status.items()}
        _log.info("emitting status_ready with %d components", len(payload))
        try:
            json_payload = json.dumps(payload)
        except (TypeError, ValueError) as e:
            _log.error("failed to serialize status JSON: %s", e)
            json_payload = json.dumps(
                {
                    name: {"name": name, "kind": "unknown", "error": str(e)}
                    for name in payload
                }
            )
        self.status_ready.emit((json_payload,))

    async def _periodic_status_check(self) -> None:
        """Provision once; emit status per poll, sooner on fetch failure or deferral."""
        await asyncio.sleep(_BOOT_DELAY_S)
        while True:
            try:
                if not self._provisioned:
                    await asyncio.wait({self._reconcile_task})
                    deferred = await self._svc.provision_missing(self._provision_busy)
                    self._provisioned = not deferred
                    _log.info("provisioning pass done (deferred=%s)", deferred)
                await self._emit_status()
            except Exception as exc:  # noqa: BLE001
                _log.error("periodic_check failed: %s", exc)
            interval = self._svc.poll_interval
            if self._svc.has_fetch_failures():
                interval = min(_FETCH_RETRY_INTERVAL_S, interval)
                _log.info("fetch failures pending - re-polling in %.0fs", interval)
            elif not self._provisioned:
                interval = min(_FETCH_RETRY_INTERVAL_S, interval)
                _log.info("provisioning deferred - re-polling in %.0fs", interval)
            await asyncio.sleep(interval)

    @sdbus.dbus_method_async(result_signature="b")
    async def update_all(self) -> bool:
        """D-Bus method: fire-and-forget; reply is sent immediately, update runs as a task."""
        if self._busy:
            return False
        self._set_busy(busy=True)
        self._spawn(self._run_update_all(), name="update_all")
        return True

    @sdbus.dbus_method_async(input_signature="s", result_signature="b")
    async def update_component(self, name: str) -> bool:
        """D-Bus method: fire-and-forget; reply is sent immediately, update runs as a task."""
        if self._busy:
            return False
        if not self._validate_component_name(name):
            _log.warning("update_component called with unknown component %r", name)
            return False
        self._set_busy(busy=True)
        self._spawn(self._run_update_component(name), name=f"update_{name}")
        return True

    @sdbus.dbus_method_async(input_signature="sb", result_signature="b")
    async def recover(self, name: str, hard: bool) -> bool:
        """D-Bus method: fire-and-forget; reply is sent immediately, recover runs as a task."""
        if self._busy:
            return False
        if not self._validate_component_name(name):
            _log.warning("recover called with unknown component %r", name)
            return False
        self._set_busy(busy=True)
        self._spawn(self._run_recover(name, hard), name=f"recover_{name}")
        return True

    @sdbus.dbus_method_async(input_signature="b")
    async def set_printing(self, printing: bool) -> None:
        """D-Bus method: the UI reports an active job; unattended work waits for it."""
        if printing != self._svc.printing:
            _log.info("printing -> %s", printing)
            self._svc.printing = printing

    @sdbus.dbus_method_async(input_signature="ss", result_signature="b")
    async def bless_healthy(self, name: str, hash_val: str) -> bool:
        """D-Bus method: bless a component as healthy (known-good)."""
        if not self._validate_component_name(name):
            _log.warning("bless_healthy called with unknown component %r", name)
            return False
        return await self._svc.bless_healthy(name, hash_val)

    async def _run_with_lock(
        self,
        work: Callable[[], Awaitable[object]],
        label: str,
        target: str,
    ) -> bool:
        """Run work() under the cross-process lock, then clear busy; True if the lock was held."""
        ran = False
        try:
            with process_lock() as acquired:
                if not acquired:
                    _log.warning("%s: a CLI run holds the lock; skipping", label)
                    self.error.emit((target, "another update is running"))
                    return False
                ran = True
                await self._svc.reconcile_if_pending()
                await work()
        except Exception as exc:  # noqa: BLE001
            _log.error("_run_%s failed: %s", label, exc, exc_info=True)
        finally:
            # a running install owns busy
            if ran or not self._provisioning:
                self._set_busy(busy=False)
        return ran

    async def _run_update_all(self) -> None:
        """Update dirty components; no background apt if a restart may SIGKILL dpkg."""
        ran = await self._run_with_lock(
            self._update_all_locked, "update_all", "updater"
        )
        if ran and self._svc.daemon_restart_pending:
            _log.info("background apt upgrade skipped: daemon restart pending")
        elif ran:
            self._spawn(
                self._svc.background_apt_upgrade(), name="background_apt_upgrade"
            )

    async def _update_all_locked(self) -> None:
        """Update dirty components and errored git repos (update self-heals those)."""
        statuses = await self._svc.check_status()
        dirty = {
            name
            for name, s in statuses.items()
            if s.commits_behind
            or s.packages_upgradable > 0
            or s.has_local_changes
            or s.needs_install
            or s.branch_mismatch
            or (s.error is not None and s.kind != "apt")
        }
        if dirty:
            await self._svc.update_all(dirty)
        else:
            _log.info("update_all: no dirty components found")

    async def _run_update_component(self, name: str) -> None:
        """Run a single-component update under the process lock; always clears busy."""
        await self._run_with_lock(
            partial(self._svc.update_component, name), "update_component", name
        )

    async def _run_recover(self, name: str, hard: bool) -> None:
        """Run a recover under the process lock; always clears busy."""
        await self._run_with_lock(
            partial(self._svc.recover, name, hard), "recover", name
        )

    @sdbus.dbus_method_async()
    async def request_status(self) -> None:
        """D-Bus method: reply immediately, status arrives via status_ready signal."""
        _log.info("request_status called")
        self._spawn(self._emit_status(force=True), name="request_status")

    @sdbus.dbus_method_async(result_signature="b")
    async def get_busy(self) -> bool:
        """D-Bus method: return current busy state so reconnecting clients can sync."""
        return self._busy

    @sdbus.dbus_method_async(result_signature="b")
    async def get_provisioning(self) -> bool:
        """D-Bus method: True while a missing component is being installed."""
        return self._provisioning

    @sdbus.dbus_method_async()
    async def cancel(self) -> None:
        """D-Bus method: cancel the task, then wait (not re-cancel) for its rollback."""
        if self._provisioning:
            _log.info("cancel() ignored: component install in progress")
            return
        cancelled_tasks: list[asyncio.Task] = []
        for task in list(self._background_tasks):
            name = task.get_name()
            if name.startswith(("update_", "recover_")):
                task.cancel()
                cancelled_tasks.append(task)
                _log.info("cancelled task %r", name)
        if cancelled_tasks:
            _done, pending = await asyncio.wait(cancelled_tasks, timeout=150.0)
            if pending:
                _log.error(
                    "cancel() cleanup timed out after 150s; %d task(s) still running",
                    len(pending),
                )
        self._set_busy(busy=False)
        if not cancelled_tasks:
            _log.info("cancel() called but no active operation task found")


UpdaterDbusService = UpdaterInterface
