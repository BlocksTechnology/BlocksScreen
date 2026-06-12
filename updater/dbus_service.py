"""D-Bus interface definition and progress callback for the updater daemon."""

from __future__ import annotations

import asyncio
import dataclasses
import json
import logging
from pathlib import Path

import sdbus

from updater.models import ComponentStatus
from updater.service import UpdateService

_log = logging.getLogger(__name__)
_STATUS_PATH = Path("/run/blockscreen/updater_status.json")


class DbusProgressCallback:
    """Adapter that forwards ProgressCallback events to D-Bus signals.

    Holds a reference to the server interface so each on_* call invokes
    the corresponding signal's .emit() — decoupling UpdateService from D-Bus.
    """

    def __init__(self, iface: UpdaterInterface) -> None:
        self._iface = iface

    def on_step(self, name: str, step: int, total: int) -> None:
        self._iface.step_complete.emit((name, step, total))
        try:
            _STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
            tmp = _STATUS_PATH.with_suffix(".tmp")
            tmp.write_text(json.dumps({"name": name, "step": step, "total": total}))
            tmp.replace(_STATUS_PATH)
        except OSError as e:
            _log.debug("status write failed: %s", e)

    def on_component_done(self, name: str, success: bool) -> None:  # noqa: FBT001
        self._iface.component_done.emit((name, success))

    def on_error(self, name: str, reason: str) -> None:
        self._iface.error.emit((name, reason))

    def on_rollback(self, name: str, success: bool) -> None:  # noqa: FBT001
        self._iface.rollback.emit((name, success))

    def on_recover(self, name: str, success: bool) -> None:  # noqa: FBT001
        self._iface.recover_done.emit((name, success))


class UpdaterInterface(
    sdbus.DbusInterfaceCommonAsync,
    interface_name="com.blockscreen.Updater",
):
    """D-Bus interface contract shared by server and client proxy.

    Signals are declared once here, sdbus replaces each descriptor with
    emit machinery on the server side and an async-iterable on the client.
    """

    # ── Signals ──────────────────────────────────────────────────────────

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

    # ── Lifecycle ────────────────────────────────────────────────────────

    def __init__(self) -> None:
        super().__init__()
        self._svc = UpdateService(callback=DbusProgressCallback(self))
        self._busy: bool = False
        self._background_tasks: set[asyncio.Task] = set()
        self._status_check_in_progress: bool = False
        self._status_pending: bool = False
        self._invalid_requests: int = 0
        self._spawn(self._periodic_status_check(), name="periodic_status_check")

    # ── Private helpers ───────────────────────────────────────────────────

    def _spawn(self, coro, *, name: str | None = None) -> asyncio.Task:
        """Create a task and hold a strong reference so GC cannot cancel it."""
        task = asyncio.get_running_loop().create_task(coro, name=name)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)
        return task

    def _set_busy(self, busy: bool) -> None:  # noqa: FBT001
        """Emit busy_changed only on state transitions to avoid redundant signals."""
        if busy != self._busy:
            self._busy = busy
            _log.info("busy_changed -> %s", busy)
            self.busy_changed.emit((busy,))

    def _validate_component_name(self, name: str) -> bool:
        """SEC: verify component exists to prevent abuse on unknown names.

        Also rate-limits invalid requests to detect/prevent fuzzing attacks.
        """
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
        """Run check_status() and emit status_ready; emits error status per component on failure."""  # noqa: E501
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
        """Emit status shortly after startup, then at the configured poll interval."""
        await asyncio.sleep(3.0)
        while True:
            try:
                await self._emit_status()
            except Exception as exc:  # noqa: BLE001
                _log.error("periodic_check failed: %s", exc)
            await asyncio.sleep(self._svc.poll_interval)

    # ── D-Bus methods ────────────────────────────────────────────────────

    @sdbus.dbus_method_async(result_signature="b")
    async def update_all(self) -> bool:
        """D-Bus method: fire-and-forget; reply is sent immediately, update runs as a task."""  # noqa: E501
        if self._busy:
            return False
        self._set_busy(busy=True)
        self._spawn(self._run_update_all(), name="update_all")
        return True

    @sdbus.dbus_method_async(input_signature="s", result_signature="b")
    async def update_component(self, name: str) -> bool:
        """D-Bus method: fire-and-forget; reply is sent immediately, update runs as a task."""  # noqa: E501
        if self._busy:
            return False
        if not self._validate_component_name(name):  # SEC: reject unknown components
            _log.warning("update_component called with unknown component %r", name)
            return False
        self._set_busy(busy=True)
        self._spawn(self._run_update_component(name), name=f"update_{name}")
        return True

    @sdbus.dbus_method_async(input_signature="sb", result_signature="b")
    async def recover(self, name: str, hard: bool) -> bool:  # noqa: FBT001
        """D-Bus method: fire-and-forget; reply is sent immediately, recover runs as a task."""  # noqa: E501
        if self._busy:
            return False
        if not self._validate_component_name(name):  # SEC: reject unknown components
            _log.warning("recover called with unknown component %r", name)
            return False
        self._set_busy(busy=True)
        self._spawn(self._run_recover(name, hard), name=f"recover_{name}")
        return True

    async def _run_update_all(self) -> None:
        try:
            statuses = await self._svc.check_status()
            dirty = {
                name
                for name, s in statuses.items()
                if s.commits_behind or s.packages_upgradable > 0 or s.has_local_changes
            }
            if dirty:
                await self._svc.update_all(dirty)
            else:
                _log.info("update_all: no dirty components found")
        except Exception as exc:  # noqa: BLE001
            _log.error("_run_update_all failed: %s", exc, exc_info=True)
        finally:
            self._set_busy(busy=False)
        self._spawn(self._svc.background_apt_upgrade(), name="background_apt_upgrade")

    async def _run_update_component(self, name: str) -> None:
        try:
            await self._svc.update_component(name)
        except Exception as exc:  # noqa: BLE001
            _log.error("_run_update_component failed: %s", exc, exc_info=True)
        finally:
            self._set_busy(busy=False)

    async def _run_recover(self, name: str, hard: bool) -> None:  # noqa: FBT001
        try:
            await self._svc.recover(name, hard)
        except Exception as exc:  # noqa: BLE001
            _log.error("_run_recover failed: %s", exc, exc_info=True)
        finally:
            self._set_busy(busy=False)

    @sdbus.dbus_method_async()
    async def request_status(self) -> None:
        """D-Bus method: reply immediately, status arrives via status_ready signal."""
        _log.info("request_status called")
        self._spawn(self._emit_status(force=True), name="request_status")

    @sdbus.dbus_method_async(result_signature="b")
    async def get_busy(self) -> bool:
        """D-Bus method: return current busy state so reconnecting clients can sync."""
        return self._busy

    @sdbus.dbus_method_async()
    async def cancel(self) -> None:
        """D-Bus method: cancel the running update or recover task and wait for cleanup."""
        cancelled_tasks: list[asyncio.Task] = []
        for task in list(self._background_tasks):
            name = task.get_name() or ""
            if name.startswith(("update_", "recover_")):
                task.cancel()
                cancelled_tasks.append(task)
                _log.info("cancelled task %r", name)
        if cancelled_tasks:
            try:
                async with asyncio.timeout(10.0):
                    await asyncio.gather(*cancelled_tasks, return_exceptions=True)
            except TimeoutError:
                _log.error(
                    "cancel() cleanup timed out after 10s; tasks may still be running"
                )
        self._set_busy(busy=False)
        if not cancelled_tasks:
            _log.info("cancel() called but no active operation task found")


UpdaterDbusService = UpdaterInterface
