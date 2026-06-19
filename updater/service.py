from __future__ import annotations

import asyncio
import json
import logging
import os
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
    git_clone,
    git_fetch,
    git_get_current_branch,
    git_get_hash,
    git_has_corruption,
    git_pull,
    git_repair,
    git_reset_to_hash,
    restart_service,
    restart_service_noblock,
    run_hook,
    wait_for_service_active,
)
from updater.models import ComponentConfig, ComponentStatus

_STATE_PATH = Path.home() / ".cache" / "blockscreen" / "updater_state.json"
_HISTORY_PATH = Path.home() / ".cache" / "blockscreen" / "update_history.jsonl"

# git's empty-tree object: used as the prev_hash when provisioning so a
# diff-based hook (`git diff <prev> <new>`) sees every file as newly added and
# performs a full install, instead of no-op'ing on an empty prev_hash.
_GIT_EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

# Services that host the updater's own D-Bus client (the UI). They are restarted
# non-blocking and never waited on, so a self-update cannot tear down or abort
# the in-flight batch; new UI code loads on the queued restart, daemon code on
# the next reboot.
_FIRE_AND_FORGET_SERVICES = frozenset({"BlocksScreen.service"})


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
        self._apt_lock = Lock()
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
                # force bypasses the apt cache, mirroring the git fetch TTL bypass.
                status = await check_apt_status(
                    cache_ttl_seconds=0 if force else 86_400, exclude=c.apt_exclude
                )
            elif c.path is None or not c.path.exists():
                # A missing opted-in component surfaces as needs_install so the
                # one Update button reaches it; everything else stays skipped.
                if c.install_if_missing and c.url:
                    results[c.name] = ComponentStatus(name=c.name, needs_install=True)
                return
            else:
                now = time.monotonic()
                async with self._git_lock:
                    last = self._fetch_times.get(c.name, 0.0)
                    skip_fetch = not force and (now - last) < self._FETCH_TTL
                status = await check_git_status(
                    c.name, c.path, c.branch, c.version, skip_fetch
                )
                # Record fetch time only after a successful check so a failed
                # (offline) fetch is retried on the next poll instead of being
                # suppressed for the full TTL.
                if not skip_fetch and status.error is None:
                    async with self._git_lock:
                        self._fetch_times[c.name] = now
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
        """Update components: apt independently, existing git as one atomic batch.

        apt packages and missing-component provisioning are independent of the git
        code set, so they run outside the all-or-nothing batch.
        """
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
        if not await self._preflight_fetch(sorted_components, components):
            return

        apt = [c for c in sorted_components if c.kind == "apt"]
        batch = [
            c
            for c in sorted_components
            if c.kind == "git" and c.path is not None and c.path.exists()
        ]
        provision = [
            c
            for c in sorted_components
            if c.kind == "git"
            and (c.path is None or not c.path.exists())
            and c.install_if_missing
            and c.url
        ]
        for c in apt:
            await self._run_apt_update(c)
        if batch:
            await self._run_git_batch(batch)
        for c in provision:
            await self._provision_component(c)

    async def _preflight_fetch(
        self, sorted_components: list[ComponentConfig], all_components: list
    ) -> bool:
        """Fetch every existing git component up-front (network phase).

        Decoupling the download from the apply means a mid-sequence connection
        drop aborts before anything is checked out, instead of leaving an
        applied/unapplied skew across components. A pre-fetched component skips
        its own fetch in the apply phase (recorded fetch time). Repos that need
        cloning or are corrupt are left to self-heal in their own flow.
        """
        targets = [
            c
            for c in sorted_components
            if c.kind == "git" and c.path is not None and c.path.exists()
        ]
        offline: list[str] = []
        async with self._git_lock:
            for c in targets:
                now = time.monotonic()
                # Skip a component the status check just fetched (<30s ago); its
                # recorded time still lets the apply phase skip its own fetch.
                if now - self._fetch_times.get(c.name, 0.0) < 30:
                    continue
                ok, err = await git_fetch(c.path)
                if ok:
                    self._fetch_times[c.name] = now
                elif not await git_has_corruption(c.path, hint=err):
                    offline.append(c.name)
        if offline:
            msg = "network error during pre-flight fetch — no components changed"
            self._log.error("update_all: %s (failed: %s)", msg, offline)
            for c in all_components:
                self._cb("on_error", c.name, msg)
            return False
        return True

    async def _run_git_batch(self, batch: list[ComponentConfig]) -> None:
        """Apply existing git components all-or-nothing.

        Stage every repo, then deps, then hooks, then restart each unique service
        once. While staging/deps/hooks run nothing has been restarted, so the live
        services still execute the old code — an abort then just reverts git and
        restarts nothing. A restart-phase failure reverts git AND re-restarts the
        services already bounced so they come back on the old code.
        """
        prev: dict[str, str] = {}
        for c in batch:
            ph = await git_get_hash(c.path)
            if ph == "":
                self._log.error("%s: prev_hash empty — aborting batch", c.name)
                for b in batch:
                    self._cb_error_done(b.name, "prev_hash empty")
                return
            prev[c.name] = ph
        async with self._state_lock:
            state = await asyncio.to_thread(self._read_state)
            for name, ph in prev.items():
                state[name] = {"prev_hash": ph}
            if not await asyncio.to_thread(self._write_state, state):
                for b in batch:
                    self._cb_error_done(b.name, "failed to persist rollback point")
                return
        for c in batch:
            ok, reason = await _assert_https_remote(c.path)
            if not ok:
                self._log.error("%s: SEC-4 remote check failed: %s", c.name, reason)
                for b in batch:
                    self._cb_error_done(b.name, "insecure remote")
                return
            self._history("update_start", c.name, prev_hash=prev[c.name][:12])

        touched: list[ComponentConfig] = []
        restarted: list[str] = []
        try:
            for c in batch:
                self._cb("on_step", c.name, 1, 4)
                touched.append(c)  # mark before staging so a partial stage is reverted
                ok, reason = await self._stage_component(c)
                if not ok:
                    await self._abort_batch(batch, prev, touched, restarted, reason)
                    return
            for c in batch:
                self._cb("on_step", c.name, 2, 4)
                deps_ok, deps_err = await self._install_dependencies(c)
                if not deps_ok:
                    self._log.warning("%s: deps failed: %s", c.name, deps_err)
                    await self._abort_batch(batch, prev, touched, restarted, "deps")
                    return
            new_hashes: dict[str, str] = {}
            for c in batch:
                self._cb("on_step", c.name, 3, 4)
                new_hashes[c.name] = await git_get_hash(c.path)
                hook_ok, hook_err = await run_hook(
                    c.name, c.path, new_hashes[c.name], prev[c.name]
                )
                if not hook_ok:
                    self._log.error("%s: hook failed: %s", c.name, hook_err)
                    await self._abort_batch(batch, prev, touched, restarted, "hook")
                    return
            # Restart each unique non-self service once and verify it. Mark bounced
            # before the restart so an abort re-restarts even a service that failed
            # its health check, onto the reverted code. Self/UI services are deferred.
            seen: set[str] = set()
            ui_components: list[ComponentConfig] = []
            for c in batch:
                if not c.service or c.service in seen:
                    continue
                seen.add(c.service)
                if c.service in _FIRE_AND_FORGET_SERVICES:
                    ui_components.append(c)
                    continue
                self._cb("on_step", c.name, 4, 4)
                restarted.append(c.service)
                if not await self._restart_one(c.service):
                    await self._abort_batch(batch, prev, touched, restarted, "restart")
                    return
            # All verified services are up: the batch has succeeded. Record success
            # and persist BEFORE the fire-and-forget UI restart, which tears down the
            # D-Bus client, so a completed update can never be reverted by it.
            for c in batch:
                self._history(
                    "update_success", c.name, new_hash=new_hashes[c.name][:12]
                )
                self._cb("on_component_done", c.name, True)
            for c in ui_components:
                self._cb("on_step", c.name, 4, 4)
                await restart_service_noblock(c.service)
        except asyncio.CancelledError:
            self._log.warning("git batch cancelled — aborting")
            await self._shielded(
                self._abort_batch(batch, prev, touched, restarted, "cancelled"),
                "git batch cancel-abort",
            )
            raise
        except Exception:  # noqa: BLE001
            self._log.error("git batch unexpected error", exc_info=True)
            await self._abort_batch(batch, prev, touched, restarted, "unexpected_error")

    async def _abort_batch(
        self,
        batch: list[ComponentConfig],
        prev: dict[str, str],
        touched: list[ComponentConfig],
        restarted: list[str],
        reason: str,
    ) -> None:
        """Revert touched repos, re-restart bounced services, report all failed."""
        self._log.warning(
            "aborting batch (reason=%s): reverting %d repo(s)", reason, len(touched)
        )
        for c in touched:
            await git_reset_to_hash(c.path, prev[c.name])
        restart_ok = True
        for service in restarted:
            if not await self._restart_one(service):
                restart_ok = False
                self._log.error("abort: %s did not recover after revert", service)
        for c in batch:
            self._history(
                "rollback",
                c.name,
                reason=reason,
                reverted_to=prev[c.name][:12],
                ok=restart_ok,
            )
            self._cb("on_error", c.name, reason)
            self._cb("on_rollback", c.name, restart_ok)
            self._cb("on_component_done", c.name, False)

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
            if restart_ok:
                # restart_service can fall back to `systemctl kill` and report
                # success without the unit coming back, so confirm it is active.
                restart_ok = await wait_for_service_active(
                    component.service, timeout=90.0
                )
            if not restart_ok:
                self._log.error("hard recover restart failed: %s", restart_err)
            ok = restart_ok
        self._cb("on_recover", name, ok)
        return ok

    async def reconcile(self) -> None:
        """Heal repos left damaged by a power loss mid-update, for every component.

        start.sh only repairs the BlocksScreen repo; this covers klipper/moonraker/
        config repos too. The gate is the cheap `rev-parse HEAD` (mirrors start.sh's
        `cat-file -e HEAD`) so a healthy boot pays almost nothing; deeper corruption
        is caught on demand by the normal update flow. Offline-safe: git_repair
        fetches when it can, else we reset to the last recorded good hash.
        """
        for c in self._components:
            if c.kind != "git" or c.path is None or not c.path.exists():
                continue
            async with self._git_lock:
                if await git_get_hash(c.path) != "":
                    continue
                self._log.warning("reconcile: %s HEAD unreadable — repairing", c.name)
                ok, msg = await git_repair(c.path)
                if ok:
                    self._history("boot_repair", c.name, detail=msg[:80])
                    continue
                prev = (
                    (await asyncio.to_thread(self._read_state))
                    .get(c.name, {})
                    .get("prev_hash")
                )
                if prev and _GIT_SHA_RE.match(prev):
                    rok, _ = await git_reset_to_hash(c.path, prev)
                    self._history("boot_reset", c.name, ok=rok, reverted_to=prev[:12])
                    self._log.warning(
                        "reconcile: %s reset to %s (ok=%s)", c.name, prev[:8], rok
                    )
                else:
                    self._log.error(
                        "reconcile: %s unrepairable, no recorded prev_hash", c.name
                    )

    async def _rollback(
        self, component: ComponentConfig, prev_hash: str, reason: str
    ) -> None:
        self._log.warning(
            "%s: rolling back to %s (reason=%s)", component.name, prev_hash[:8], reason
        )
        ok, _ = await git_reset_to_hash(component.path, prev_hash)
        if component.service and not await self._restart_one(component.service):
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

        # pip itself is pinned/owned by bs-bootstrap, not refreshed here: a pip
        # self-upgrade would mutate the venv on a network round-trip before the
        # reqs install, adding a failure surface for no in-flow benefit.
        return await _run(
            [pip_path, "install", "-r", str(req), "--quiet"], timeout=120.0
        )

    async def _shielded(self, coro, label: str) -> None:
        """Run cleanup to completion, surviving repeated cancels of the caller."""
        task = asyncio.ensure_future(coro)
        while True:
            try:
                await asyncio.shield(task)
                return
            except asyncio.CancelledError:
                if task.done():
                    return
                self._log.warning(
                    "%s: cleanup still running, ignoring repeat cancel", label
                )
            except Exception:  # noqa: BLE001
                self._log.error("%s failed", label, exc_info=True)
                return

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

    async def _remove_clone(self, component: ComponentConfig) -> None:
        """Delete a freshly-cloned tree (the path did not exist before provisioning)."""
        if component.path is not None:
            await asyncio.to_thread(shutil.rmtree, component.path, ignore_errors=True)

    async def _fail_provision(self, component: ComponentConfig, reason: str) -> bool:
        """Remove the partial clone, log it to history, and report the failure."""
        await self._remove_clone(component)
        self._history("install_failed", component.name, reason=reason)
        self._log.warning(
            "%s: provision failed (%s), partial clone removed", component.name, reason
        )
        return self._cb_error_done(component.name, reason)

    async def _provision_component(self, component: ComponentConfig) -> bool:
        """Clone and set up a missing opted-in component.

        A fresh component has no prev_hash to roll back to, so any failure deletes
        the partial clone (clean slate to retry next Update) rather than rolling
        back. Service install is delegated to the component's hook, mirroring the
        existing update flow.
        """
        if not component.url:
            return self._cb_error_done(component.name, "no clone url")
        self._log.info("%s: provisioning via clone %s", component.name, component.url)
        self._history("install_start", component.name, url=component.url)
        try:
            self._cb("on_step", component.name, 1, 4)
            ok, err = await git_clone(component.url, component.path, component.branch)
            if not ok:
                self._log.error("%s: clone failed: %s", component.name, err)
                return await self._fail_provision(component, "clone")

            if component.version:
                ok, err = await git_reset_to_hash(component.path, component.version)
                if not ok:
                    self._log.error("%s: pin failed: %s", component.name, err)
                    return await self._fail_provision(component, "version")

            self._cb("on_step", component.name, 2, 4)
            new_hash = await git_get_hash(component.path)
            deps_ok, deps_err = await self._install_dependencies(component)
            if not deps_ok:
                self._log.warning("%s: provision deps: %s", component.name, deps_err)
                return await self._fail_provision(component, "deps")

            self._cb("on_step", component.name, 3, 4)
            hook_ok, hook_err = await run_hook(
                component.name, component.path, new_hash, _GIT_EMPTY_TREE
            )
            if not hook_ok:
                self._log.error("%s: provision hook: %s", component.name, hook_err)
                return await self._fail_provision(component, "hook")

            self._cb("on_step", component.name, 4, 4)
            if component.service:
                svc_ok, svc_err = await restart_service(component.service)
                if not svc_ok:
                    self._log.error(
                        "%s: provision restart: %s", component.name, svc_err
                    )
                    return await self._fail_provision(component, "restart")
                if not await wait_for_service_active(component.service, timeout=90.0):
                    self._log.error(
                        "%s: provisioned service not active", component.name
                    )
                    return await self._fail_provision(component, "restart_timeout")

            self._history("install_success", component.name, new_hash=new_hash[:12])
            self._cb("on_component_done", component.name, True)
            return True
        except asyncio.CancelledError:
            self._log.warning(
                "%s: provision cancelled, removing partial clone", component.name
            )
            await self._shielded(
                self._remove_clone(component), f"{component.name} provision-cleanup"
            )
            raise
        except Exception:  # noqa: BLE001
            self._log.error(
                "%s: unexpected error during provision", component.name, exc_info=True
            )
            return await self._fail_provision(component, "unexpected_error")

    async def _stage_component(self, component: ComponentConfig) -> tuple[bool, str]:
        """Bring the working tree to its target ref: fetch-gate + reset/checkout/pull.

        No deps/hook/restart and no rollback — the caller decides what to do on
        failure. Returns (ok, reason) where reason is one of
        network/corrupt/reset/version/branch/conflict.
        """
        if component.path is None:
            return (False, "path not found")
        async with self._git_lock:
            # Gate the update-fetch on this component's last *successful* fetch, not
            # the last status check: an errored/corrupt repo has no recorded fetch
            # time, so it always re-fetches here (and then self-heals).
            last_fetch = self._fetch_times.pop(component.name, 0.0)
        elapsed = time.monotonic() - last_fetch if last_fetch else float("inf")

        if elapsed >= 30:
            ok, error = await git_fetch(component.path)
            if not ok:
                self._log.error(error)
                # fsck --connectivity-only can miss the object corruption that
                # broke the fetch, so pass the fetch error as a hint.
                if not await git_has_corruption(component.path, hint=error):
                    return (False, "network")
                self._log.warning("%s: corrupt repo, repairing", component.name)
                rok, rmsg = await git_repair(component.path)
                if not rok:
                    return (False, "corrupt")
                self._history("repair", component.name, detail=rmsg[:80])

        if component.reset_mode == "hard":
            # Reset to the remote tracking ref, not HEAD, so local commits that
            # diverge from origin are discarded before the pull.
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
                return (False, "reset")

        if component.version:
            ok, err = await git_reset_to_hash(component.path, component.version)
            if not ok:
                self._log.error("%s: version pin failed: %s", component.name, err)
                return (False, "version")
        elif component.branch:
            ok, err = await git_checkout(component.path, component.branch)
            if not ok:
                self._log.error("%s: git_checkout failed: %s", component.name, err)
                return (False, "branch")
            ok, err = await git_pull(component.path)
            if not ok:
                self._log.error("%s: git_pull failed: %s", component.name, err)
                return (False, "conflict")
        else:
            ok, err = await git_pull(component.path)
            if not ok:
                self._log.error("%s: git_pull failed: %s", component.name, err)
                return (False, "conflict")
        return (True, "")

    async def _restart_one(self, service: str) -> bool:
        """Restart a service and verify it came active (kill-fallback aware)."""
        ok, err = await restart_service(service)
        if not ok:
            self._log.error("restart %s failed: %s", service, err)
            return False
        if not await wait_for_service_active(service, timeout=90.0):
            self._log.error("%s did not become active after restart", service)
            return False
        return True

    async def _run_git_update(self, component: ComponentConfig) -> bool:
        """Update a single existing git component, rolling back on any failure.

        Shares its git mechanics (_stage_component) with the multi-component batch;
        keeps its own per-component rollback since a single update has no peers to
        coordinate.
        """
        if component.path is None:
            return self._cb_error_done(component.name, "path not found")
        if not component.path.exists():
            if component.install_if_missing and component.url:
                return await self._provision_component(component)
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

        try:
            self._cb("on_step", component.name, 1, 4)
            stage_ok, stage_reason = await self._stage_component(component)
            if not stage_ok:
                # A failed pre-update reset changed nothing, so there is nothing
                # to roll back; every other stage failure leaves a dirty tree.
                if stage_reason == "reset":
                    return self._cb_error_done(component.name, "reset")
                await self._rollback(component, prev_hash, stage_reason)
                return False

            self._cb("on_step", component.name, 2, 4)
            deps_ok, deps_err = await self._install_dependencies(component)
            if not deps_ok:
                self._log.warning("dependencies error: %s", deps_err)
                await self._rollback(component, prev_hash, "deps")
                return False

            self._cb("on_step", component.name, 3, 4)
            new_hash = await git_get_hash(component.path)
            hook_ok, hook_err = await run_hook(
                component.name, component.path, new_hash, prev_hash
            )
            if not hook_ok:
                self._log.error("hook failed for %s: %s", component.name, hook_err)
                await self._rollback(component, prev_hash, "hook")
                return False

            self._cb("on_step", component.name, 4, 4)
            fire_and_forget = component.service in _FIRE_AND_FORGET_SERVICES
            if (
                component.service
                and not fire_and_forget
                and not await self._restart_one(component.service)
            ):
                await self._rollback(component, prev_hash, "restart")
                return False

            self._history("update_success", component.name, new_hash=new_hash[:12])
            self._cb("on_component_done", component.name, True)
            # Self/UI service: queue the restart only after success is recorded.
            if fire_and_forget and component.service:
                await restart_service_noblock(component.service)
            return True
        except asyncio.CancelledError:
            self._log.warning(
                "%s: update cancelled mid-flight, rolling back to %s",
                component.name,
                prev_hash[:8],
            )
            await self._shielded(
                self._rollback(component, prev_hash, "cancelled"),
                f"{component.name} cancel-rollback",
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
        async with self._apt_lock:
            return await self._run_apt_update_locked(component, _apt_cache)

    async def _run_apt_update_locked(
        self, component: ComponentConfig, _apt_cache: Path
    ) -> bool:
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
            # The cancelled subprocess may have been a SIGKILLed dpkg; repair
            # the package database before reporting back.
            await self._shielded(
                _apt_get_fix_broken(), f"{component.name} apt cancel-repair"
            )
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
                # fsync the file + parent dir so the rollback point survives a
                # power cut: rename-without-fsync can otherwise zero the file.
                f.flush()
                os.fsync(f.fileno())
                temp_path = Path(f.name)
            temp_path.chmod(0o600)
            temp_path.replace(self._state_path)
            self._fsync_dir(self._state_path.parent)
            return True
        except OSError:
            self._log.error("Failed to write state file")
            return False

    @staticmethod
    def _fsync_dir(path: Path) -> None:
        try:
            fd = os.open(path, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        except OSError:
            pass

    async def background_apt_upgrade(self) -> None:
        """Run apt update + upgrade + autoremove silently after every Update click.

        Uses apt-get upgrade (never dist-upgrade) so the Debian release never changes.
        Never reports to the UI — failures are logged only.
        """
        async with self._apt_lock:
            await self._background_apt_upgrade_locked()

    async def _background_apt_upgrade_locked(self) -> None:
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
