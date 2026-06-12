from __future__ import annotations

import asyncio
import itertools
import json
import logging
import shutil
import tempfile
import time
from asyncio import Lock
from pathlib import Path
from typing import Protocol

from updater.components import load_components
from updater.executor import (
    _GIT_SHA_RE,
    PIP,
    _apt_get_fix_broken,
    _apt_restore_packages,
    _apt_snapshot_packages,
    _assert_https_remote,
    _resolve_component_pip,
    _run,
    apt_autoremove,
    apt_update,
    apt_upgrade,
    check_apt_status,
    check_git_status,
    git_checkout,
    git_fetch,
    git_get_current_branch,
    git_get_hash,
    git_pull,
    git_reset_to_hash,
    restart_service,
    run_hook,
    wait_for_service_active,
)
from updater.models import ComponentConfig, ComponentStatus

_STATE_PATH = Path.home() / ".cache" / "blockscreen" / "updater_state.json"
_HISTORY_PATH = Path.home() / ".cache" / "blockscreen" / "update_history.jsonl"


class ProgressCallback(Protocol):
    def on_step(self, name: str, step: int, total: int) -> None: ...
    def on_component_done(self, name: str, success: bool) -> None: ...
    def on_error(self, name: str, reason: str) -> None: ...
    def on_rollback(self, name: str, success: bool) -> None: ...
    def on_recover(self, name: str, success: bool) -> None: ...


class LoggingCallback:
    def __init__(self) -> None:
        self._log = logging.getLogger("updater")

    def on_step(self, name: str, step: int, total: int) -> None:
        self._log.info("%s step %d/%d", name, step, total)

    def on_component_done(self, name: str, success: bool) -> None:
        if success:
            self._log.info("%s done(ok=True)", name)
        else:
            self._log.error("%s done(ok=False)", name)

    def on_error(self, name: str, reason: str) -> None:
        self._log.error("%s error: %s", name, reason)

    def on_rollback(self, name: str, success: bool) -> None:
        self._log.warning("%s rollback (ok=%s)", name, success)

    def on_recover(self, name: str, success: bool) -> None:
        self._log.info("%s recover (ok=%s)", name, success)


class UpdateService:
    """Async service that orchestrates component status checks and updates."""

    _FETCH_TTL: float = 300.0

    def __init__(self, callback: ProgressCallback | None = None) -> None:
        self._components, self.poll_interval = load_components()
        self._git_lock = Lock()
        self._state_lock = Lock()
        self._callback = callback
        self._last_status_time: float = 0.0
        self._fetch_times: dict[str, float] = {}
        self._component_pip_cache: dict[str, str] = {}
        self._state_path = _STATE_PATH
        self._history_path = _HISTORY_PATH
        self._log = logging.getLogger("updater")

    def has_component(self, name: str) -> bool:
        """Return True if a component with the given name is registered."""
        return any(c.name == name for c in self._components)

    def component_stubs(self) -> list[tuple[str, str]]:
        """Return (name, kind) pairs for all registered components."""
        return [(c.name, c.kind) for c in self._components]

    async def check_status(self, force: bool = False) -> dict[str, ComponentStatus]:
        """Concurrently check status of all components.

        force=True bypasses the fetch TTL so git fetch always runs.
        Use for explicit user-triggered refreshes.
        """
        results: dict[str, ComponentStatus] = {}

        async def _check_one(c: ComponentConfig) -> None:
            if c.kind == "apt":
                status = await check_apt_status(exclude=c.apt_exclude)
            elif c.path is None or not c.path.exists():
                return
            else:
                now = time.monotonic()
                async with self._git_lock:
                    last = self._fetch_times.get(c.name, 0.0)
                    skip_fetch = not force and (now - last) < self._FETCH_TTL
                    if not skip_fetch:
                        self._fetch_times[c.name] = now
                status = await check_git_status(
                    c.name, c.path, c.branch, c.version, skip_fetch
                )
            results[c.name] = status

        gathered = await asyncio.gather(
            *[_check_one(c) for c in self._components], return_exceptions=True
        )
        for res in gathered:
            if isinstance(res, BaseException) and not isinstance(
                res, asyncio.CancelledError
            ):
                self._log.error("check_status component raised: %s", res, exc_info=res)
        async with self._git_lock:
            self._last_status_time = time.monotonic()
        return results

    async def update_component(self, name: str) -> bool:
        """Update a single component by name."""
        component = next((c for c in self._components if c.name == name), None)
        if component is None:
            self._log.error("update_component: unknown component %r", name)
            return self._cb_error_done(name, "unknown component")
        if component.kind == "apt":
            return await self._run_apt_update(component)
        return await self._run_git_update(component)

    async def update_all(self, names: set[str] | None = None) -> None:
        """Update components in order-group batches."""
        components = (
            self._components
            if names is None
            else [c for c in self._components if c.name in names]
        )
        free_mb = shutil.disk_usage(Path.home()).free / 1_048_576
        if free_mb < 200:
            msg = f"insufficient disk space ({free_mb:.0f} MB free, need 200 MB)"
            self._log.error("update_all: %s", msg)
            for c in components:
                self._cb("on_error", c.name, msg)
            return
        sorted_components = sorted(components, key=lambda c: c.order)
        for _, group_iter in itertools.groupby(
            sorted_components, key=lambda c: c.order
        ):
            group = list(group_iter)
            gathered = await asyncio.gather(
                *[self.update_component(c.name) for c in group], return_exceptions=True
            )
            for res in gathered:
                if isinstance(res, BaseException) and not isinstance(
                    res, asyncio.CancelledError
                ):
                    self._log.error(
                        "update_all component raised: %s", res, exc_info=res
                    )

    async def recover(self, name: str, hard: bool = False) -> bool:
        """Reset a component to its last known-good hash."""
        component = next((c for c in self._components if c.name == name), None)
        if component is None:
            self._log.error("component %s not found", name)
            self._cb("on_recover", name, False)
            return False
        state = self._read_state()
        prev_hash = state.get(name, {}).get("prev_hash")
        if prev_hash is None:
            self._cb("on_recover", name, False)
            self._log.error("failed to get prev_hash for %s", name)
            return False
        if not _GIT_SHA_RE.match(prev_hash):
            self._log.error("recover: invalid prev_hash format for %s", name)
            self._cb("on_recover", name, False)
            return False
        ok, err = await git_reset_to_hash(component.path, prev_hash)
        if not ok:
            self._log.error(err)
            self._cb("on_recover", name, False)
            return False
        async with self._git_lock:
            self._fetch_times.pop(name, None)
        if hard and component.service:
            restart_ok, restart_err = await restart_service(component.service)
            if not restart_ok:
                self._log.error("hard recover restart failed: %s", restart_err)
            ok = restart_ok
        self._cb("on_recover", name, ok)
        return ok

    async def _rollback(
        self, component: ComponentConfig, prev_hash: str, reason: str
    ) -> None:
        self._log.warning(
            "%s: rolling back to %s (reason=%s)", component.name, prev_hash[:8], reason
        )
        ok, _ = await git_reset_to_hash(component.path, prev_hash)
        if component.service:
            rs_ok, _ = await restart_service(component.service)
            if not rs_ok:
                self._log.warning("rollback restart failed: %s", component.service)
                ok = False
        self._history(
            "rollback", component.name, reason=reason, reverted_to=prev_hash[:12], ok=ok
        )
        self._cb("on_error", component.name, reason)
        self._cb("on_rollback", component.name, ok)
        self._cb("on_component_done", component.name, False)

    async def _install_dependencies(
        self, component: ComponentConfig
    ) -> tuple[bool, str]:
        """Install requirements.txt with cached pip path lookup to avoid redundant filesystem checks."""
        if component.path is None:
            return (False, "path not found")
        cache_key = str(component.path)
        if cache_key not in self._component_pip_cache:
            self._component_pip_cache[cache_key] = _resolve_component_pip(
                component.path
            )
        pip_path = self._component_pip_cache[cache_key]

        if pip_path == PIP:
            # No component venv found. Modern Debian rejects system pip installs
            # (PEP 668 externally-managed-environment). Deps are managed by the
            # component's own installer (e.g. klipper's klippy-env).
            self._log.info(
                "%s: no component venv — skipping dep install", component.name
            )
            return (True, "no venv — deps managed externally")
        req = component.path / "requirements.txt"
        if not req.exists():
            return (True, "no requirements.txt")
        mode = req.stat().st_mode & 0o777
        if mode & 0o002:
            # SEC: world-writable only; group-writable is permitted (blocksscreen group is trusted)
            return (False, "world-writable permissions")

        return await _run(
            [pip_path, "install", "-r", str(req), "--quiet"], timeout=120.0
        )

    def _cb_error_done(self, name: str, reason: str) -> bool:
        self._cb("on_error", name, reason)
        self._cb("on_component_done", name, False)
        return False

    def _history(self, event: str, name: str, **fields: object) -> None:
        """Append one event to the persistent update-history log (OBS-1).

        journald is volatile on this image, so this on-SD JSONL log is the
        durable record of update outcomes for field diagnosis.
        """
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event": event,
            "component": name,
            **fields,
        }
        try:
            self._history_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with self._history_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError as exc:
            self._log.warning("update history write failed: %s", exc)

    async def _run_git_update(self, component: ComponentConfig) -> bool:
        """Run the 4-step git update flow: fetch/pull/deps/restart, rolling back on failure."""
        if component.path is None or not component.path.exists():
            return self._cb_error_done(component.name, "path not found")

        prev_hash = await git_get_hash(component.path)
        if prev_hash == "":
            self._log.error("prev_hash is empty")
            return self._cb_error_done(component.name, "prev_hash empty")
        async with self._state_lock:
            state = await asyncio.to_thread(self._read_state)
            state[component.name] = {"prev_hash": prev_hash}
            if not await asyncio.to_thread(self._write_state, state):
                return self._cb_error_done(
                    component.name, "failed to persist rollback point"
                )
        ok, reason = await _assert_https_remote(component.path)
        if not ok:
            self._log.error("SEC-4 remote check failed: %s", reason)
            return self._cb_error_done(component.name, "insecure remote")
        self._history("update_start", component.name, prev_hash=prev_hash[:12])
        async with self._git_lock:
            self._fetch_times.pop(component.name, None)
            elapsed = time.monotonic() - self._last_status_time

        try:
            self._cb("on_step", component.name, 1, 4)
            if elapsed >= 30:
                self._log.info(
                    "%s: git_fetch (%.0fs since last status)", component.name, elapsed
                )
                ok, error = await git_fetch(component.path)
                if not ok:
                    self._log.error(error)
                    await self._rollback(component, prev_hash, "network")
                    return False
            else:
                self._log.info(
                    "%s: skipping git_fetch (%.0fs since last status)",
                    component.name,
                    elapsed,
                )

            self._cb("on_step", component.name, 2, 4)
            if component.reset_mode == "hard":
                # Reset to the remote tracking ref, not HEAD, so local commits
                # that diverge from origin are discarded before the pull.
                if component.branch:
                    hard_ref = f"origin/{component.branch}"
                else:
                    _cur = await git_get_current_branch(component.path)
                    hard_ref = f"origin/{_cur}" if _cur else "origin/HEAD"
                ok, err = await git_reset_to_hash(component.path, hard_ref)
                if not ok:
                    self._log.error(
                        "%s: pre-update hard reset failed: %s", component.name, err
                    )
                    return self._cb_error_done(component.name, "reset")

            if component.version:
                ok, err = await git_reset_to_hash(component.path, component.version)
                if not ok:
                    self._log.error(
                        "%s: git_reset_to_hash failed: %s", component.name, err
                    )
                    await self._rollback(component, prev_hash, "version")
                    return False
            elif component.branch:
                ok, err = await git_checkout(component.path, component.branch)
                if not ok:
                    self._log.error("%s: git_checkout failed: %s", component.name, err)
                    await self._rollback(component, prev_hash, "branch")
                    return False
                ok, err = await git_pull(component.path)
                if not ok:
                    self._log.error("%s: git_pull failed: %s", component.name, err)
                    await self._rollback(component, prev_hash, "conflict")
                    return False
            else:
                ok, err = await git_pull(component.path)
                if not ok:
                    self._log.error("%s: git_pull failed: %s", component.name, err)
                    await self._rollback(component, prev_hash, "conflict")
                    return False

            self._cb("on_step", component.name, 3, 4)
            deps_ok, deps_err = await self._install_dependencies(component)
            if not deps_ok:
                self._log.warning("dependencies error: %s", deps_err)
                await self._rollback(component, prev_hash, "deps")
                return False

            self._cb("on_step", component.name, 4, 4)
            new_hash = await git_get_hash(component.path)
            hook_ok, hook_err = await run_hook(
                component.name, component.path, new_hash, prev_hash
            )
            if not hook_ok:
                self._log.error("hook failed for %s: %s", component.name, hook_err)
                await self._rollback(component, prev_hash, "hook")
                return False

            if component.service:
                svc_ok, svc_err = await restart_service(component.service)
                if not svc_ok:
                    self._log.error(
                        "%s: service restart failed: %s", component.name, svc_err
                    )
                    await self._rollback(component, prev_hash, "restart")
                    return False
                active = await wait_for_service_active(component.service, timeout=90.0)
                if not active:
                    self._log.error(
                        "%s: service %r did not become active after restart — rolling back",  # noqa: E501
                        component.name,
                        component.service,
                    )
                    await self._rollback(component, prev_hash, "restart_timeout")
                    return False

            self._history("update_success", component.name, new_hash=new_hash[:12])
            self._cb("on_component_done", component.name, True)
            return True
        except asyncio.CancelledError:
            self._log.warning(
                "%s: update cancelled mid-flight, rolling back to %s",
                component.name,
                prev_hash[:8],
            )
            try:
                await self._rollback(component, prev_hash, "cancelled")
            except Exception:  # noqa: BLE001
                self._log.error(
                    "%s: rollback during cancel failed", component.name, exc_info=True
                )
            raise
        except Exception as exc:  # noqa: BLE001
            self._log.error(
                "%s: unexpected error during update: %s",
                component.name,
                exc,
                exc_info=True,
            )
            try:
                await self._rollback(component, prev_hash, "unexpected_error")
            except Exception:  # noqa: BLE001
                self._log.error(
                    "%s: rollback after unexpected error failed",
                    component.name,
                    exc_info=True,
                )
            return False

    async def _run_apt_update(self, component: ComponentConfig) -> bool:
        _apt_cache = Path.home() / ".cache" / "blockscreen" / "apt_status_cache.json"
        try:
            ok, err = await apt_update()
            if not ok:
                self._log.error("apt_update failed: %s", err)
                _apt_cache.unlink(missing_ok=True)
                return self._cb_error_done(component.name, "network")
            self._cb("on_step", component.name, 1, 2)

            snapshot_ok, snapshot_path = await _apt_snapshot_packages()
            if snapshot_ok:
                self._log.debug("apt package snapshot created: %s", snapshot_path)
            else:
                self._log.warning("apt snapshot failed, continuing without rollback")

            ok, err = await apt_upgrade(exclude=component.apt_exclude)
            if not ok:
                self._log.error("apt_upgrade failed: %s", err)
                _apt_cache.unlink(missing_ok=True)
                rollback_ok, rollback_err = await _apt_get_fix_broken()
                if rollback_ok:
                    self._log.info("apt-get -f install succeeded; state may be fixed")
                else:
                    self._log.error("apt-get -f install also failed: %s", rollback_err)
                if snapshot_path:
                    self._log.warning(
                        "attempting package restore from %s", snapshot_path
                    )
                    restore_ok, restore_err = await _apt_restore_packages(snapshot_path)
                    if restore_ok:
                        self._log.info("package restore succeeded")
                    else:
                        self._log.error(
                            "package restore failed %s, manual intervention needed",
                            restore_err,
                        )
                return self._cb_error_done(component.name, "upgrade")
            self._cb("on_step", component.name, 2, 2)

            autoremove_ok, autoremove_err = await apt_autoremove()
            if not autoremove_ok:
                self._log.warning(
                    "apt autoremove failed (non-fatal): %s", autoremove_err
                )

            self._cb("on_component_done", component.name, True)
            _apt_cache.unlink(missing_ok=True)
            return True
        except asyncio.CancelledError:
            self._log.warning("%s: apt update cancelled", component.name)
            self._cb("on_error", component.name, "cancelled")
            self._cb("on_component_done", component.name, False)
            raise

    def _read_state(self) -> dict:
        try:
            return json.loads(self._state_path.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _write_state(self, data: dict) -> bool:
        try:
            self._state_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            # SEC: atomic write via temp file prevents symlink attacks and partial writes
            with tempfile.NamedTemporaryFile(
                mode="w",
                dir=self._state_path.parent,
                delete=False,
                prefix=".updater_state_",
            ) as f:
                f.write(json.dumps(data, indent=2))
                temp_path = Path(f.name)
            temp_path.chmod(0o600)
            temp_path.replace(self._state_path)
            return True
        except OSError:
            self._log.error("Failed to write state file")
            return False

    async def background_apt_upgrade(self) -> None:
        """Run apt update + upgrade + autoremove silently after every Update click.

        Uses apt-get upgrade (never dist-upgrade) so the Debian release never changes.
        Never reports to the UI — failures are logged only.
        """
        self._log.info("background apt upgrade: starting")
        ok, err = await apt_update()
        if not ok:
            self._log.warning("background apt-get update failed: %s", err)
            return
        ok, err = await apt_upgrade()
        if not ok:
            self._log.warning("background apt upgrade failed: %s", err)
            return
        self._log.info("background apt upgrade: packages done")
        autoremove_ok, autoremove_err = await apt_autoremove()
        if not autoremove_ok:
            self._log.warning(
                "background apt autoremove failed (non-fatal): %s", autoremove_err
            )

    def _cb(self, method: str, *args: object) -> None:
        """Dispatch a callback method; log and continue on any exception."""
        if self._callback is not None:
            try:
                getattr(self._callback, method)(*args)
            except Exception:  # noqa: BLE001
                self._log.error("callback %s raised", method, exc_info=True)
