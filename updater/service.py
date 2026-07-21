from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import secrets
import shutil
import tempfile
import time
from asyncio import Lock
from collections.abc import Callable
from pathlib import Path
from typing import Protocol, TypeGuard

from updater.components import load_components
from updater.executor import (
    _GIT_SHA_RE,
    HOOK_TIMEOUT,
    PIP,
    SYSTEMCTL,
    UPDATER_SERVICE,
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
    classify_apt_error,
    enable_service,
    git_checkout,
    git_clone,
    git_fetch,
    git_get_current_branch,
    git_get_hash,
    git_has_corruption,
    git_pull,
    git_ref_hash,
    git_tree_has_path,
    git_repair,
    git_reset_to_hash,
    is_git_repo,
    restart_service,
    restart_service_noblock,
    run_hook,
    verify_updater_importable,
    wait_for_service_active,
)
from updater.locking import process_lock, restart_sentinel_path
from updater.models import ComponentConfig, ComponentStatus

_STATE_PATH = Path.home() / ".cache" / "blockscreen" / "updater_state.json"
# SD-backed batch map name->pre-update hash; present at boot = revert those repos.
_INFLIGHT_PATH = Path.home() / ".cache" / "blockscreen" / "updater_inflight.json"
# Self-heal fault marker: present = fast recovery saturated (golden also looped).
_FAULT_MARKER_PATH = Path.home() / ".cache" / "blockscreen" / "selfheal_fault.json"
_HISTORY_PATH = Path.home() / ".cache" / "blockscreen" / "update_history.jsonl"
# Cap the history so a device running for years cannot fill the SD card.
_HISTORY_MAX_BYTES = 1_000_000
_HISTORY_KEEP_LINES = 2000

# Circuit-breaker backoff for network ops (apt, git fetch): skip while cooling down so a failure can't storm-retry.
_APT_BACKOFF_BASE_S = 30.0
_APT_BACKOFF_MAX_S = 1800.0
_APT_PERMANENT_COOLDOWN_S = 3600.0
_FETCH_BACKOFF_BASE_S = 30.0
_FETCH_BACKOFF_MAX_S = 900.0

# Self-heal: NRestarts polling interval (seconds) for crash-loop detection.
_NRESTARTS_POLL_INTERVAL_S = 15.0
# Trailing window for crash-loop detection: 5+ restarts in 180 seconds.
_NRESTARTS_WINDOW_S = 180.0
_NRESTARTS_THRESHOLD = 5


async def get_service_nrestarts(service: str = "BlocksScreen.service") -> int:
    """Read a systemd unit's NRestarts via `systemctl show` (0 if unavailable)."""
    ok, out = await _run(
        [SYSTEMCTL, "show", service, "-p", "NRestarts", "--value"], timeout=10.0
    )
    value = out.strip() if ok else ""
    return int(value) if value.isdigit() else 0


def _ensure_comp(state: dict, name: str) -> dict:
    """Return state[name] as a dict, replacing a corrupt non-dict entry in place."""
    comp = state.get(name)
    if not isinstance(comp, dict):
        comp = {}
        state[name] = comp
    return comp


def _is_sha(val: object) -> TypeGuard[str]:
    """True only for a syntactically valid git hash (guards corrupt/non-str state)."""
    return isinstance(val, str) and bool(_GIT_SHA_RE.match(val))


class _Backoff:
    """Per-dependency circuit breaker: skip work while cooling_down(); trip() on failure, reset() on success."""

    def __init__(self, base: float, cap: float, permanent: float = 0.0) -> None:
        """Configure the base, capped, and (optional) permanent-failure delays in seconds."""
        self._base = base
        self._cap = cap
        self._permanent = permanent
        self._until = 0.0
        self._delay = 0.0

    def cooling_down(self) -> bool:
        """Return True while the last failure's backoff window has not elapsed."""
        return time.monotonic() < self._until

    def trip(self, *, permanent: bool = False) -> None:
        """Open the breaker: permanent = fixed cooldown, else capped exponential delay + jitter."""
        if permanent and self._permanent:
            delay = self._permanent
        else:
            self._delay = min(max(self._delay * 2, self._base), self._cap)
            delay = self._delay
        jitter = secrets.SystemRandom().uniform(0, delay * 0.1)
        self._until = time.monotonic() + delay + jitter

    def reset(self) -> None:
        """Close the breaker after a success."""
        self._until = 0.0
        self._delay = 0.0


# git's empty tree as provisioning prev_hash: diff hooks see all files as new.
_GIT_EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

# UI services (our D-Bus client): no-block restart so self-update can't kill the batch.
_UI_SERVICE = "BlocksScreen.service"
_FIRE_AND_FORGET_SERVICES = frozenset({_UI_SERVICE})
# Fallback klipper unit for restart_klipper if no klipper component is configured.
_KLIPPER_SERVICE = "klipper.service"

# Self-heal: the UI component name (components.yaml) that the supervisor watches.
_UI_COMPONENT = "BlocksScreen"
# Marker file proving updater exists: absence at target ref aborts update (lack bricks Type=notify host with no self-heal).
_UPDATER_MARKER = "updater/dbus_service.py"
# Forward-heal always targets the curated-stable channel, not the configured branch.
_HEAL_REMOTE_REF = "origin/main"
# Settle window after a rung (debounce plus margin) so a new build can bless first.
_RECOVERY_SETTLE_S = 90.0
# Slow forward-heal cadence base and jitter spread (seconds), per fleet OTA practice.
_FORWARD_HEAL_BASE_S = 1800.0
_FORWARD_HEAL_JITTER_S = 300.0

# Deploy flag for BlocksScreen-deploy.path: runs install-updater.sh in its own cgroup.
_DEPLOY_FLAG = Path.home() / ".config" / "blockscreen" / ".run-install-updater"


class ProgressCallback(Protocol):
    def on_step(self, name: str, step: int, total: int) -> None:
        """Report a numbered progress step for a component."""
        ...

    def on_component_done(self, name: str, success: bool) -> None:
        """Report a component's final success or failure."""
        ...

    def on_error(self, name: str, reason: str) -> None:
        """Report a non-recoverable error for a component."""
        ...

    def on_rollback(self, name: str, success: bool) -> None:
        """Report a rollback attempt's outcome."""
        ...

    def on_recover(self, name: str, success: bool) -> None:
        """Report a recover attempt's outcome."""
        ...


class LoggingCallback:
    def __init__(self) -> None:
        """Create the logging progress callback."""
        self._log = logging.getLogger("updater")

    def on_step(self, name: str, step: int, total: int) -> None:
        """Log a progress step."""
        self._log.info("%s step %d/%d", name, step, total)

    def on_component_done(self, name: str, success: bool) -> None:
        """Log a component's success or failure."""
        if success:
            self._log.info("%s done(ok=True)", name)
        else:
            self._log.error("%s done(ok=False)", name)

    def on_error(self, name: str, reason: str) -> None:
        """Log a component error."""
        self._log.error("%s error: %s", name, reason)

    def on_rollback(self, name: str, success: bool) -> None:
        """Log a rollback outcome."""
        self._log.warning("%s rollback (ok=%s)", name, success)

    def on_recover(self, name: str, success: bool) -> None:
        """Log a recover outcome."""
        self._log.info("%s recover (ok=%s)", name, success)


class UpdateService:
    """Async service that orchestrates component status checks and updates."""

    _FETCH_TTL: float = 300.0

    def __init__(self, callback: ProgressCallback | None = None) -> None:
        """Load components and initialize locks, caches, and self-heal tracking."""
        self._components, self.poll_interval = load_components()
        self._git_lock = Lock()
        self._state_lock = Lock()
        self._apt_lock = Lock()
        self._callback = callback
        self._last_status_time: float = 0.0
        self._fetch_times: dict[str, float] = {}
        self._component_pip_cache: dict[str, str] = {}
        self._apt_backoff = _Backoff(
            _APT_BACKOFF_BASE_S, _APT_BACKOFF_MAX_S, _APT_PERMANENT_COOLDOWN_S
        )
        self._fetch_backoff: dict[str, _Backoff] = {}
        self._state_path = _STATE_PATH
        self._inflight_path = _INFLIGHT_PATH
        self._history_path = _HISTORY_PATH
        self._fault_marker_path = _FAULT_MARKER_PATH
        self._log = logging.getLogger("updater")
        # Self-heal: trailing-window sample ring for crash-loop detection.
        self._nrestarts_samples: dict[str, list[tuple[float, int]]] = {}

    def has_component(self, name: str) -> bool:
        """Return True if a component with the given name is registered."""
        return any(c.name == name for c in self._components)

    def _klipper_service(self) -> str:
        """restart_klipper target: the klipper component's service, else the default."""
        comp = next((c for c in self._components if c.name == "klipper"), None)
        return comp.service if comp and comp.service else _KLIPPER_SERVICE

    def component_stubs(self) -> list[tuple[str, str]]:
        """Return (name, kind) pairs for all registered components."""
        return [(c.name, c.kind) for c in self._components]

    async def check_status(self, force: bool = False) -> dict[str, ComponentStatus]:
        """Concurrently check status of all components."""
        results: dict[str, ComponentStatus] = {}

        async def _check_one(c: ComponentConfig) -> None:
            """Fetch and record one component's status into the results dict."""
            if c.kind == "apt":
                # force bypasses the apt cache, mirroring the git fetch TTL bypass.
                status = await check_apt_status(
                    cache_ttl_seconds=0 if force else 86_400, exclude=c.apt_exclude
                )
            elif c.path is None or not c.path.exists():
                # Missing opted-in comps surface as needs_install; rest stay skipped.
                if c.install_if_missing and c.url:
                    results[c.name] = ComponentStatus(name=c.name, needs_install=True)
                return
            else:
                now = time.monotonic()
                async with self._git_lock:
                    last = self._fetch_times.get(c.name, 0.0)
                    breaker = self._fetch_backoff.get(c.name)
                    skip_fetch = not force and (
                        (now - last) < self._FETCH_TTL
                        or (breaker is not None and breaker.cooling_down())
                    )
                status = await check_git_status(
                    c.name, c.path, c.branch, c.version, skip_fetch
                )
                # Record success; back off a failing fetch per-component so it can't storm the poll.
                if not skip_fetch:
                    async with self._git_lock:
                        if status.error is None:
                            self._fetch_times[c.name] = now
                            self._fetch_backoff.pop(c.name, None)
                        else:
                            self._fetch_backoff.setdefault(
                                c.name,
                                _Backoff(_FETCH_BACKOFF_BASE_S, _FETCH_BACKOFF_MAX_S),
                            ).trip()
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

    async def update_all(self, names: set[str] | None = None) -> bool:
        """Update components: apt independently, existing git as one phased batch."""
        components = (
            self._components
            if names is None
            else [c for c in self._components if c.name in names]
        )
        if not self._check_disk_space(components):
            return False
        sorted_components = sorted(components, key=lambda c: c.order)
        offline = await self._preflight_fetch(sorted_components)

        apt, batch = self._build_apt_and_batch_lists(sorted_components)
        ok = await self._filter_offline_batch(batch, offline)
        ok = await self._filter_nonrepo_batch(batch) and ok
        ok = await self._filter_dead_branch_batch(batch) and ok
        provision = self._build_provision_list(sorted_components)
        return await self._run_update_phases(apt, batch, provision) and ok

    def _build_apt_and_batch_lists(
        self, sorted_components: list[ComponentConfig]
    ) -> tuple[list[ComponentConfig], list[ComponentConfig]]:
        """Partition sorted components into (apt, existing-git-repo batch)."""
        apt = [c for c in sorted_components if c.kind == "apt"]
        batch = [
            c
            for c in sorted_components
            if c.kind == "git" and c.path is not None and c.path.exists()
        ]
        return apt, batch

    def _build_provision_list(
        self, sorted_components: list[ComponentConfig]
    ) -> list[ComponentConfig]:
        """Git components with no local path (incl. just-quarantined) safe to auto-clone."""
        return [
            c
            for c in sorted_components
            if c.kind == "git"
            and (c.path is None or not c.path.exists())
            and c.install_if_missing
            and c.url
        ]

    async def _run_update_phases(
        self,
        apt: list[ComponentConfig],
        batch: list[ComponentConfig],
        provision: list[ComponentConfig],
    ) -> bool:
        """Run apt updates, then the git batch, then provisioning; AND all results."""
        ok = True
        for c in apt:
            ok = await self._run_apt_update(c) and ok
        if batch:
            ok = await self._run_git_batch(batch) and ok
        for c in provision:
            ok = await self._provision_component(c) and ok
        return ok

    def _check_disk_space(self, components: list[ComponentConfig]) -> bool:
        """Return False (and report on_error for each component) if free space < 200 MB."""
        free_mb = shutil.disk_usage(Path.home()).free / 1_048_576
        if free_mb >= 200:
            return True
        msg = f"insufficient disk space ({free_mb:.0f} MB free, need 200 MB)"
        self._log.error("update_all: %s", msg)
        for c in components:
            self._cb_error_done(c.name, msg)
        return False

    async def _filter_offline_batch(
        self, batch: list[ComponentConfig], offline: set[str]
    ) -> bool:
        """Drop offline components from the batch, erroring each individually."""
        # An unreachable remote drops only that component, never the whole update.
        ok = True
        for c in [c for c in batch if c.name in offline]:
            batch.remove(c)
            ok = self._cb_error_done(c.name, "network error during pre-flight fetch")
        return ok

    async def _filter_nonrepo_batch(self, batch: list[ComponentConfig]) -> bool:
        """Drop non-git-repo dirs, quarantining installable ones for a fresh clone."""
        # A dir without .git (tarball install) errors individually, not the batch.
        ok = True
        for c in [c for c in batch if not is_git_repo(c.path)]:
            batch.remove(c)
            if c.install_if_missing and c.url and await self._quarantine_nonrepo(c):
                continue  # path is now absent: the provision pass below clones fresh
            self._log.error("%s: %s is not a git repository - skipping", c.name, c.path)
            ok = self._cb_error_done(
                c.name, "not a git repository - reinstall required"
            )
        return ok

    async def _filter_dead_branch_batch(self, batch: list[ComponentConfig]) -> bool:
        """Drop components whose configured branch no longer resolves upstream."""
        # A dead configured branch must not abort the batch and brick BlocksScreen.
        ok = True
        for c in batch.copy():
            if c.branch and not await git_ref_hash(c.path, f"origin/{c.branch}"):
                batch.remove(c)
                self._log.error(
                    "%s: branch origin/%s does not resolve (deleted upstream?) - skipping",
                    c.name,
                    c.branch,
                )
                ok = self._cb_error_done(
                    c.name, f"branch origin/{c.branch} not found - fix components.yaml"
                )
        return ok

    async def provision_missing(self) -> bool:
        """Clone absent install_if_missing components without waiting for a manual"""
        missing = [
            c
            for c in self._components
            if c.install_if_missing
            and c.url
            and (c.path is None or not c.path.exists())
        ]
        if not missing:
            return False
        provisioned = False
        with process_lock() as acquired:
            if not acquired:
                self._log.info("provision_missing: update in progress, deferring")
                return False
            for c in missing:
                if c.path is None or not c.path.exists():  # recheck under lock
                    await self._provision_component(c)
                    provisioned = True
        return provisioned

    async def _preflight_fetch(
        self, sorted_components: list[ComponentConfig]
    ) -> set[str]:
        """Fetch every existing git component up-front (network phase)."""
        # Non-repo dirs excluded: their fetch failure is not "offline" (see update_all).
        targets = [
            c
            for c in sorted_components
            if c.kind == "git" and c.path is not None and is_git_repo(c.path)
        ]
        offline: set[str] = set()
        # Lock guards only _fetch_times; git_fetch runs outside it (as check_status).
        for c in targets:
            now = time.monotonic()
            async with self._git_lock:
                # Skip if fetched <30s ago; apply phase still skips its own fetch.
                recent = now - self._fetch_times.get(c.name, 0.0) < 30
            if recent:
                continue
            ok, err = await git_fetch(c.path)
            if ok:
                async with self._git_lock:
                    self._fetch_times[c.name] = now
            elif not await git_has_corruption(c.path, hint=err):
                offline.add(c.name)
        if offline:
            self._log.error(
                "update_all: pre-flight fetch failed for %s - continuing without them",
                sorted(offline),
            )
        return offline

    async def _prepare_git_batch_hashes(
        self, batch: list[ComponentConfig]
    ) -> tuple[list[ComponentConfig], dict[str, str], bool]:
        """Snapshot each component's prev_hash; drop (error) those with an empty hash."""
        prev: dict[str, str] = {}
        alive: list[ComponentConfig] = []
        for c in batch:
            ph = await git_get_hash(c.path)
            if ph == "":
                self._log.error("%s: prev_hash empty - skipping", c.name)
                self._cb_error_done(c.name, "prev_hash empty")
                continue
            prev[c.name] = ph
            alive.append(c)
        failed = len(alive) != len(batch)
        return alive, prev, failed

    async def _persist_batch_rollback(self, prev: dict[str, str]) -> bool:
        """Persist per-component prev_hash + the inflight marker under the state lock."""
        async with self._state_lock:
            state = await asyncio.to_thread(self._read_state)
            for name, ph in prev.items():
                # Merge: replacing the entry would wipe the self-heal anchors (last_good/golden).
                _ensure_comp(state, name)["prev_hash"] = ph
            if not await asyncio.to_thread(self._write_state, state):
                return False
            # Mark in-flight so a pre-commit power cut is reverted on next boot.
            if not await asyncio.to_thread(self._write_inflight, prev.copy()):
                return False
        return True

    async def _security_check_batch(
        self, alive: list[ComponentConfig], prev: dict[str, str]
    ) -> tuple[list[ComponentConfig], bool]:
        """Assert an https remote per component, dropping any that fail SEC-4."""
        checked: list[ComponentConfig] = []
        failed = False
        for c in alive:
            sec_ok, reason = await _assert_https_remote(c.path)
            if not sec_ok:
                self._log.error("%s: SEC-4 remote check failed: %s", c.name, reason)
                self._cb_error_done(c.name, "insecure remote")
                failed = True
                continue
            self._history("update_start", c.name, prev_hash=prev[c.name][:12])
            checked.append(c)
        return checked, failed

    async def _batch_stage_phase(
        self,
        alive: list[ComponentConfig],
        prev: dict[str, str],
        touched: list[ComponentConfig],
        pending_revert: dict[str, str],
    ) -> tuple[list[ComponentConfig], bool]:
        """Stage each repo to its target ref, reverting the ones that fail."""
        self._log.info("git batch: stage phase (%d repo(s))", len(alive))
        failed = False
        survivors: list[ComponentConfig] = []
        for c in alive:
            self._cb("on_step", c.name, 1, 4)
            touched.append(c)  # mark before staging so a partial stage is reverted
            ok, reason = await self._stage_component(c)
            if ok:
                survivors.append(c)
                continue
            failed = True
            if not await self._drop_component(c, prev[c.name], reason):
                pending_revert[c.name] = prev[c.name]
            touched.remove(c)
        return survivors, failed

    async def _batch_deps_phase(
        self,
        alive: list[ComponentConfig],
        prev: dict[str, str],
        touched: list[ComponentConfig],
        pending_revert: dict[str, str],
    ) -> tuple[list[ComponentConfig], bool]:
        """Install each survivor's deps, reverting the ones whose install fails."""
        self._log.info("git batch: deps phase")
        failed = False
        survivors: list[ComponentConfig] = []
        for c in alive:
            self._cb("on_step", c.name, 2, 4)
            deps_ok, deps_err = await self._install_dependencies(c)
            if deps_ok:
                survivors.append(c)
                continue
            self._log.warning("%s: deps failed: %s", c.name, deps_err)
            failed = True
            if not await self._drop_component(c, prev[c.name], "deps"):
                pending_revert[c.name] = prev[c.name]
            touched.remove(c)
        return survivors, failed

    async def _batch_hook_phase(
        self,
        alive: list[ComponentConfig],
        prev: dict[str, str],
        touched: list[ComponentConfig],
        pending_revert: dict[str, str],
    ) -> tuple[list[ComponentConfig], dict[str, str], bool]:
        """Run each survivor's post-update hook, reverting the ones whose hook fails."""
        self._log.info("git batch: hook phase")
        new_hashes: dict[str, str] = {}
        failed = False
        survivors: list[ComponentConfig] = []
        for c in alive:
            self._cb("on_step", c.name, 3, 4)
            new_hashes[c.name] = await git_get_hash(c.path)
            self._log.info(
                "git batch hook: %s %s -> %s",
                c.name,
                prev[c.name][:8],
                new_hashes[c.name][:8],
            )
            hook_ok, hook_err = await self._ping_while(
                run_hook(
                    c.name,
                    c.path,
                    new_hashes[c.name],
                    prev[c.name],
                    timeout=HOOK_TIMEOUT,
                ),
                c.name,
                3,
                4,
            )
            if hook_ok:
                survivors.append(c)
                continue
            self._log.error("%s: hook failed: %s", c.name, hook_err)
            failed = True
            if not await self._drop_component(c, prev[c.name], "hook"):
                pending_revert[c.name] = prev[c.name]
            touched.remove(c)
        return survivors, new_hashes, failed

    async def _batch_restart_services(
        self,
        alive: list[ComponentConfig],
        prev: dict[str, str],
        touched: list[ComponentConfig],
        restarted: list[str],
        pending_revert: dict[str, str],
        seen: set[str],
    ) -> tuple[bool, list[ComponentConfig]]:
        """Restart each component's own service once; revert its members on failure."""
        failed = False
        ui_components: list[ComponentConfig] = []
        for c in alive.copy():
            if c not in alive or not c.service or c.service in seen:
                continue
            seen.add(c.service)
            if c.service in _FIRE_AND_FORGET_SERVICES:
                self._log.info(
                    "git batch: deferring self/UI service %s to fire-and-forget",
                    c.service,
                )
                ui_components.append(c)
                continue
            self._cb("on_step", c.name, 4, 4)
            restarted.append(c.service)
            self._log.info("git batch: restarting %s (verified)", c.service)
            if await self._restart_one(c.service):
                continue
            failed = True
            for m in [m for m in alive if m.service == c.service]:
                if not await self._drop_component(m, prev[m.name], "restart"):
                    pending_revert[m.name] = prev[m.name]
                alive.remove(m)
                touched.remove(m)
            # Members reverted: bring the service back up on the old code.
            if not await self._restart_one(c.service):
                self._log.error("%s did not recover after revert", c.service)
            restarted.remove(c.service)
        return failed, ui_components

    async def _batch_restart_klipper_bounce(
        self,
        alive: list[ComponentConfig],
        prev: dict[str, str],
        touched: list[ComponentConfig],
        restarted: list[str],
        pending_revert: dict[str, str],
        seen: set[str],
    ) -> bool:
        """Bounce klipper once for restart_klipper components, reverting them on failure."""
        # Bounce klipper once for restart_klipper components that aren't klipper.
        klipper_svc = self._klipper_service()
        requesters = [
            c for c in alive if c.restart_klipper and c.service != klipper_svc
        ]
        if not requesters or klipper_svc in seen:
            return False
        seen.add(klipper_svc)
        restarted.append(klipper_svc)
        self._log.info("git batch: restarting %s (restart_klipper)", klipper_svc)
        if await self._restart_one(klipper_svc):
            return False
        failed = True
        for m in requesters:
            if not await self._drop_component(m, prev[m.name], "restart"):
                pending_revert[m.name] = prev[m.name]
            alive.remove(m)
            touched.remove(m)
            # Service runs new code: revert it to old code unless a surviving component shares the service.
            shared = any(o.service == m.service for o in alive)
            if m.service and m.service in restarted and not shared:
                if not await self._restart_one(m.service):
                    self._log.error("%s did not recover after revert", m.service)
                restarted.remove(m.service)
        restarted.remove(klipper_svc)
        # Requesters reverted: try to bring klipper back up.
        if not await self._restart_one(klipper_svc):
            self._log.error("%s did not recover after revert", klipper_svc)
        return failed

    async def _batch_restart_phase(
        self,
        alive: list[ComponentConfig],
        prev: dict[str, str],
        touched: list[ComponentConfig],
        restarted: list[str],
        pending_revert: dict[str, str],
    ) -> tuple[bool, list[ComponentConfig]]:
        """Restart each unique service once, reverting all components behind a failed one."""
        # Restart each unique service once; failure reverts all components behind it and re-restarts onto old code.
        self._log.info("git batch: restart phase")
        seen: set[str] = set()
        svc_failed, ui_components = await self._batch_restart_services(
            alive, prev, touched, restarted, pending_revert, seen
        )
        klipper_failed = await self._batch_restart_klipper_bounce(
            alive, prev, touched, restarted, pending_revert, seen
        )
        return svc_failed or klipper_failed, ui_components

    async def _finalize_git_batch(
        self,
        alive: list[ComponentConfig],
        batch: list[ComponentConfig],
        pending_revert: dict[str, str],
        ui_components: list[ComponentConfig],
    ) -> None:
        """Settle the inflight marker and fire-and-forget the UI restarts for survivors."""
        # Shrink the marker before any restart: survivors stand from here on.
        await self._settle_inflight(pending_revert)
        self._log.info(
            "git batch complete: %d/%d component(s) updated; queueing UI restart(s)",
            len(alive),
            len(batch),
        )
        ui_services: set[str] = set()
        for c in ui_components:
            if c not in alive:
                continue
            self._cb("on_step", c.name, 4, 4)
            if c.service:
                ui_services.add(c.service)
        # klipper/RF50 hold config the UI reads at startup: refresh it too.
        if any(c.restart_ui for c in alive):
            ui_services.add(_UI_SERVICE)
        for svc in ui_services:
            self._log.info("git batch: fire-and-forget restart of %s (no wait)", svc)
            await restart_service_noblock(svc)
        await self._apply_deferred_restart()

    async def _git_batch_preflight(
        self, batch: list[ComponentConfig]
    ) -> tuple[list[ComponentConfig], dict[str, str], bool] | None:
        """Snapshot hashes, persist the rollback point, SEC-check remotes. None = abort."""
        alive, prev, failed = await self._prepare_git_batch_hashes(batch)
        if not alive:
            return None
        if not await self._persist_batch_rollback(prev):
            for c in alive:
                self._cb_error_done(c.name, "failed to persist rollback point")
            return None
        alive, sec_failed = await self._security_check_batch(alive, prev)
        failed = failed or sec_failed
        if not alive:
            # Nothing staged: drop the marker (avoids a spurious boot revert).
            await asyncio.to_thread(self._clear_inflight)
            return None
        return alive, prev, failed

    async def _run_batch_phases(
        self,
        alive: list[ComponentConfig],
        prev: dict[str, str],
        touched: list[ComponentConfig],
        restarted: list[str],
        pending_revert: dict[str, str],
        failed: bool,
    ) -> tuple[list[ComponentConfig], dict[str, str], list[ComponentConfig], bool]:
        """Run stage->deps->hook->restart; return (survivors, new_hashes, ui_components, failed)."""
        alive, stage_failed = await self._batch_stage_phase(
            alive, prev, touched, pending_revert
        )
        failed = failed or stage_failed
        alive, deps_failed = await self._batch_deps_phase(
            alive, prev, touched, pending_revert
        )
        failed = failed or deps_failed
        alive, new_hashes, hook_failed = await self._batch_hook_phase(
            alive, prev, touched, pending_revert
        )
        failed = failed or hook_failed
        restart_failed, ui_components = await self._batch_restart_phase(
            alive, prev, touched, restarted, pending_revert
        )
        failed = failed or restart_failed
        return alive, new_hashes, ui_components, failed

    async def _run_git_batch(self, batch: list[ComponentConfig]) -> bool:
        """Apply existing git components with per-component failure isolation."""
        pre = await self._git_batch_preflight(batch)
        if pre is None:
            return False
        alive, prev, failed = pre

        self._log.info(
            "git batch start: %d component(s): %s",
            len(alive),
            ", ".join(f"{c.name}->{c.service or '-'}" for c in alive),
        )
        touched: list[ComponentConfig] = []
        restarted: list[str] = []
        # Repos whose revert failed: kept in in-flight marker so boot reconcile retries them, not committed survivors.
        pending_revert: dict[str, str] = {}
        committed = False
        try:
            alive, new_hashes, ui_components, failed = await self._run_batch_phases(
                alive, prev, touched, restarted, pending_revert, failed
            )
            if not alive:
                await self._settle_inflight(pending_revert)
                return False
            # Persist success BEFORE UI restart: a committed update is never reverted.
            for c in alive:
                self._history(
                    "update_success", c.name, new_hash=new_hashes[c.name][:12]
                )
                self._cb("on_component_done", c.name, True)
            # Durable now; the self-restart's CancelledError must never revert.
            committed = True
            await self._finalize_git_batch(alive, batch, pending_revert, ui_components)
            return not failed
        except asyncio.CancelledError:
            if committed:
                raise
            self._log.warning("git batch cancelled - aborting")
            await self._shielded(
                self._abort_batch(
                    alive, prev, touched, restarted, "cancelled", pending_revert
                ),
                "git batch cancel-abort",
            )
            raise
        except Exception:  # noqa: BLE001
            if committed:
                self._log.error("post-commit error (update stands)", exc_info=True)
                return True
            self._log.error("git batch unexpected error", exc_info=True)
            await self._abort_batch(
                alive, prev, touched, restarted, "unexpected_error", pending_revert
            )
            return False

    async def _abort_batch(
        self,
        batch: list[ComponentConfig],
        prev: dict[str, str],
        touched: list[ComponentConfig],
        restarted: list[str],
        reason: str,
        pending_revert: dict[str, str] | None = None,
    ) -> None:
        """Revert touched repos, re-restart bounced services, report all failed."""
        self._log.warning(
            "aborting batch (reason=%s): reverting %d repo(s)", reason, len(touched)
        )
        pending = dict(pending_revert or {})
        for c in touched:
            ok, _ = await git_reset_to_hash(c.path, prev[c.name])
            if not ok:
                pending[c.name] = prev[c.name]
                self._log.error(
                    "abort: %s reset to %s failed", c.name, prev[c.name][:12]
                )
        # Only unresolved repos stay in the marker for a boot-time retry.
        await self._settle_inflight(pending)
        revert_ok = not pending
        restart_ok = True
        for service in restarted:
            if not await self._restart_one(service):
                restart_ok = False
                self._log.error("abort: %s did not recover after revert", service)
        rollback_ok = revert_ok and restart_ok
        for c in batch:
            self._history(
                "rollback",
                c.name,
                reason=reason,
                reverted_to=prev[c.name][:12],
                ok=rollback_ok,
            )
            self._cb("on_error", c.name, reason)
            self._cb("on_rollback", c.name, rollback_ok)
            self._cb("on_component_done", c.name, False)

    async def _drop_component(
        self, component: ComponentConfig, prev_hash: str, reason: str
    ) -> bool:
        """Revert one failed component and report it; the rest of the batch continues."""
        self._log.warning(
            "%s: dropped from batch (reason=%s), reverting to %s",
            component.name,
            reason,
            prev_hash[:8],
        )
        ok, _ = await git_reset_to_hash(component.path, prev_hash)
        if not ok:
            self._log.error("%s: revert to %s failed", component.name, prev_hash[:12])
        self._history(
            "rollback", component.name, reason=reason, reverted_to=prev_hash[:12], ok=ok
        )
        self._cb("on_error", component.name, reason)
        self._cb("on_rollback", component.name, ok)
        self._cb("on_component_done", component.name, False)
        return ok

    async def _settle_inflight(self, pending_revert: dict[str, str]) -> None:
        """Shrink the in-flight marker to repos whose revert still needs a boot retry."""
        if pending_revert:
            await asyncio.to_thread(self._write_inflight, pending_revert.copy())
        else:
            await asyncio.to_thread(self._clear_inflight)

    async def _apply_deferred_restart(self) -> None:
        """Apply a daemon restart/reinstall hook deferred during this batch."""
        try:
            sentinel = restart_sentinel_path()
            reason = await asyncio.to_thread(self._read_clear_sentinel, sentinel)
            if not reason:
                return
            if reason == "install":
                self._log.info(
                    "deferred: install files changed, touching deploy flag "
                    "(install-updater runs out-of-band)"
                )
                await asyncio.to_thread(self._touch_deploy_flag)
                return
            comp = next(
                (c for c in self._components if c.service in _FIRE_AND_FORGET_SERVICES),
                None,
            )
            path = comp.path if comp else None
            if not await verify_updater_importable(path):
                self._log.error(
                    "deferred: new updater code failed import self-test, keeping "
                    "current daemon; new code adopts on next reboot"
                )
                return
            self._log.info(
                "deferred: updater code changed, clean self-restart of %s",
                UPDATER_SERVICE,
            )
            await restart_service_noblock(UPDATER_SERVICE)
        except Exception:  # noqa: BLE001
            self._log.error("deferred restart handling failed", exc_info=True)

    @staticmethod
    def _read_clear_sentinel(sentinel: Path) -> str:
        """Read+remove the restart sentinel, returning the highest-severity reason."""
        try:
            content = sentinel.read_text()
        except OSError:
            return ""
        with contextlib.suppress(OSError):
            sentinel.unlink()
        words = set(content.split())
        if "install" in words:
            return "install"
        if "code" in words:
            return "code"
        return ""

    def _touch_deploy_flag(self) -> None:
        """Create the deploy flag watched by BlocksScreen-deploy.path."""
        _DEPLOY_FLAG.parent.mkdir(parents=True, exist_ok=True)
        if _DEPLOY_FLAG.is_symlink():
            _DEPLOY_FLAG.unlink()
        _DEPLOY_FLAG.touch()
        # Persist the dirent so a power cut right after this can't drop the flag.
        self._fsync_dir(_DEPLOY_FLAG.parent)

    async def recover(self, name: str, hard: bool = False) -> bool:
        """Reset a component to its last known-good hash."""
        component = next((c for c in self._components if c.name == name), None)
        if component is None:
            self._log.error("component %s not found", name)
            self._cb("on_recover", name, False)
            return False
        comp_state = self._read_state().get(name)
        prev_hash = (
            comp_state.get("prev_hash") if isinstance(comp_state, dict) else None
        )
        if prev_hash is None:
            self._cb("on_recover", name, False)
            self._log.error("failed to get prev_hash for %s", name)
            return False
        if not _is_sha(prev_hash):
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
                # restart may lie (kill fallback); confirm the unit is active.
                restart_ok = await wait_for_service_active(
                    component.service, timeout=90.0
                )
            if not restart_ok:
                self._log.error("hard recover restart failed: %s", restart_err)
            ok = restart_ok
        self._cb("on_recover", name, ok)
        return ok

    async def bless_healthy(self, name: str, hash_val: str) -> bool:
        """Mark a component healthy (known-good) after a debounce; snapshots baseline."""
        component = next((c for c in self._components if c.name == name), None)
        if component is None:
            self._log.error("bless_healthy: component %s not found", name)
            return False
        if not hash_val:
            hash_val = await git_get_hash(component.path)
        if not _GIT_SHA_RE.match(hash_val):
            self._log.error("bless_healthy: invalid hash format for %s", name)
            return False
        nrestarts_baseline = await get_service_nrestarts(_UI_SERVICE)

        def _apply(state: dict) -> None:
            """Set last_good, seed golden once, reset the attempt counter and baseline."""
            comp = _ensure_comp(state, name)
            comp["last_good"] = hash_val
            if not _is_sha(comp.get("golden")):
                comp["golden"] = hash_val  # seed once, or repair a corrupt golden
            comp["fast_attempt"] = 0
            comp["nrestarts_baseline"] = nrestarts_baseline
            comp.pop("last_failed_remote", None)

        ok = await self._mutate_state(_apply)
        if ok:
            self._nrestarts_samples[name] = []
            await asyncio.to_thread(self._clear_fault_marker)
            self._log.info(
                "bless_healthy: %s blessed to %s (baseline=%d)",
                name,
                hash_val[:8],
                nrestarts_baseline,
            )
        return ok

    def _check_crash_loop(self, name: str, nrestarts: int) -> bool:
        """Return True if NRestarts rose by >= 5 within the trailing 180s window."""
        if name not in self._nrestarts_samples:
            self._nrestarts_samples[name] = []  # fresh device: start tracking now
        samples = self._nrestarts_samples[name]
        now = time.monotonic()
        window_start = now - _NRESTARTS_WINDOW_S
        for ts, nr in samples:
            if ts >= window_start:
                delta = nrestarts - nr
                if delta >= _NRESTARTS_THRESHOLD:
                    self._log.warning(
                        "crash-loop detected: %s delta=%d in 180s window", name, delta
                    )
                    return True
                break
        samples.append((now, nrestarts))
        samples[:] = [(ts, nr) for ts, nr in samples if ts >= window_start]
        return False

    def _prime_nrestarts_sample_ring(self) -> None:
        """Initialize sample ring from persisted baseline on daemon start."""
        state = self._read_state()
        for name, comp_state in state.items():
            baseline = comp_state.get("nrestarts_baseline", 0)
            if (
                isinstance(baseline, int)
                and baseline > 0
                and name not in self._nrestarts_samples
            ):
                self._nrestarts_samples[name] = [(time.monotonic(), baseline)]

    async def background_prime_nrestarts(self) -> None:
        """Background task: prime NRestarts sample ring on startup."""
        await asyncio.sleep(0.5)
        await asyncio.to_thread(self._prime_nrestarts_sample_ring)
        self._log.info("NRestarts sample ring primed")

    async def run_recovery_rung(self, name: str, attempt: int) -> bool:
        """Execute one rung of the recovery ladder for a component."""
        component = next((c for c in self._components if c.name == name), None)
        if component is None:
            self._log.error("run_recovery_rung: component %s not found", name)
            return False
        attempt = min(max(attempt, 1), 3)
        # Persist the counter on entry so a skipped/failed rung still escalates next time.
        await self._mutate_state(
            lambda s: _ensure_comp(s, name).update(fast_attempt=attempt)
        )
        comp_state = (await asyncio.to_thread(self._read_state)).get(name, {})
        # entry-counter write above may not have persisted; state may still be corrupt
        if not isinstance(comp_state, dict):
            comp_state = {}
        if attempt == 1:
            return await self._recovery_rung1(component, name, comp_state)
        if attempt == 2:
            return await self._recovery_rung2(component, name)
        return await self._recovery_rung3(component, name, comp_state)

    async def _recovery_rung1(
        self, component: ComponentConfig, name: str, comp_state: dict
    ) -> bool:
        """Recovery rung 1: reset to the stored last_good sha and restart the UI."""
        last_good = comp_state.get("last_good")
        if _is_sha(last_good):
            self._log.info("recovery rung 1: reset to last_good %s", last_good[:8])
            if component.path:
                async with self._git_lock:
                    ok, _ = await git_reset_to_hash(component.path, last_good)
                if not ok:
                    self._log.error("reset to last_good failed")
                    return False
            ok = await self._restart_ui_service()
            if ok:
                self._history(
                    "recovery_rung1", name, ok=True, reverted_to=last_good[:12]
                )
            return ok
        self._log.warning("recovery rung 1: no valid last_good, skipping")
        return False

    async def _recovery_rung2(self, component: ComponentConfig, name: str) -> bool:
        """Recovery rung 2: fetch + reset to the heal remote ref (guarding brick tips)."""
        self._log.info("recovery rung 2: fetch %s and reset", _HEAL_REMOTE_REF)
        if not component.path:
            return False
        async with self._git_lock:
            ok_fetch, _ = await git_fetch(component.path)
            if not ok_fetch:
                self._log.warning("recovery rung 2: fetch failed (offline?)")
                return False
            tip = await git_ref_hash(component.path, _HEAL_REMOTE_REF)
            if not tip:
                self._log.warning("recovery rung 2: %s unresolved", _HEAL_REMOTE_REF)
                return False
            # Never heal the host onto a pre-updater tip (would re-brick, not fix).
            if name == _UI_COMPONENT and not await git_tree_has_path(
                component.path, _HEAL_REMOTE_REF, _UPDATER_MARKER
            ):
                self._log.error(
                    "recovery rung 2: %s lacks the updater package - skipping",
                    _HEAL_REMOTE_REF,
                )
                return False
            ok_reset, _ = await git_reset_to_hash(component.path, _HEAL_REMOTE_REF)
        if not ok_reset:
            self._log.error("reset to %s failed", _HEAL_REMOTE_REF)
            return False
        # Persist the tip before restart so an unbootable tip is never retried.
        await self._mutate_state(
            lambda s: _ensure_comp(s, name).update(last_failed_remote=tip)
        )
        ok = await self._restart_ui_service()
        if ok:
            self._history("recovery_rung2", name, ok=True, reverted_to=tip[:12])
        return ok

    async def _recovery_rung3(
        self, component: ComponentConfig, name: str, comp_state: dict
    ) -> bool:
        """Recovery rung 3: reset to the stored golden sha and restart the UI."""
        golden = comp_state.get("golden")
        if _is_sha(golden):
            self._log.info("recovery rung 3: reset to golden %s", golden[:8])
            if component.path:
                async with self._git_lock:
                    ok, _ = await git_reset_to_hash(component.path, golden)
                if not ok:
                    self._log.error("reset to golden failed")
                    return False
            ok = await self._restart_ui_service()
            if ok:
                self._history("recovery_rung3", name, ok=True, reverted_to=golden[:12])
            return ok
        self._log.warning("recovery rung 3: no valid golden, skipping")
        return False

    async def _restart_ui_service(self) -> bool:
        """Restart the BlocksScreen UI service; return True if successful."""
        restart_ok, restart_err = await restart_service(_UI_SERVICE)
        if restart_ok:
            restart_ok = await wait_for_service_active(_UI_SERVICE, timeout=90.0)
        if not restart_ok:
            self._log.error("restart_ui_service failed: %s", restart_err)
        return restart_ok

    def _rebaseline_samples(self, name: str, nrestarts: int) -> None:
        """Reset the detection ring so only crashes AFTER a rung count toward the next."""
        self._nrestarts_samples[name] = [(time.monotonic(), nrestarts)]

    async def supervise_ui(self) -> None:
        """Poll the UI service NRestarts and drive the recovery ladder on a crash-loop."""
        while True:
            await asyncio.sleep(_NRESTARTS_POLL_INTERVAL_S)
            try:
                nrestarts = await get_service_nrestarts(_UI_SERVICE)
                if self._check_crash_loop(_UI_COMPONENT, nrestarts):
                    await self._handle_crash_loop(nrestarts)
            except Exception:  # noqa: BLE001
                # One bad pass must not kill crash-loop supervision for good.
                self._log.error("supervise_ui pass failed", exc_info=True)

    async def _handle_crash_loop(self, nrestarts: int) -> None:
        """Run one recovery rung for the UI, or saturate if the ladder is exhausted."""
        state = await asyncio.to_thread(self._read_state)
        comp = state.get(_UI_COMPONENT, {})
        raw = comp.get("fast_attempt", 0) if isinstance(comp, dict) else 0
        current = raw if isinstance(raw, int) and not isinstance(raw, bool) else 0
        attempt = current + 1
        if attempt > 3:
            self._log.error("self-heal: fast recovery saturated; staying on golden")
            self._history("recovery_saturated", _UI_COMPONENT, ok=False)
            await asyncio.to_thread(self._write_fault_marker, "fast recovery saturated")
            self._rebaseline_samples(_UI_COMPONENT, nrestarts)
            return
        self._log.warning("self-heal: crash-loop -> recovery attempt %d", attempt)
        ok = await self.run_recovery_rung(_UI_COMPONENT, attempt)
        self._cb("on_recover", _UI_COMPONENT, ok)
        post = await get_service_nrestarts(_UI_SERVICE)
        self._rebaseline_samples(_UI_COMPONENT, post)
        await asyncio.sleep(_RECOVERY_SETTLE_S)

    async def forward_heal_ui(self) -> None:
        """Slowly re-check origin/main and re-attempt an upgrade once a fix ships."""
        while True:
            delay = _FORWARD_HEAL_BASE_S + secrets.randbelow(
                int(_FORWARD_HEAL_JITTER_S) + 1
            )
            await asyncio.sleep(delay)
            try:
                await self._forward_heal_once()
            except Exception as exc:  # noqa: BLE001
                self._log.debug("forward_heal_ui: %s", exc)

    async def _forward_heal_target(
        self, comp_state: dict
    ) -> tuple[ComponentConfig, str] | None:
        """Resolve the new heal tip to upgrade onto, or None if none is safe/available."""
        component = next((c for c in self._components if c.name == _UI_COMPONENT), None)
        if component is None or not component.path:
            return None
        async with self._git_lock:
            ok_fetch, _ = await git_fetch(component.path)
            if not ok_fetch:
                return None  # offline: connectivity gate
            tip = await git_ref_hash(component.path, _HEAL_REMOTE_REF)
        if not tip or tip == comp_state.get("last_failed_remote"):
            return None  # no new stable tip since the last failure
        # Never forward-heal onto a pre-updater tip (would brick, not upgrade).
        if not await git_tree_has_path(
            component.path, _HEAL_REMOTE_REF, _UPDATER_MARKER
        ):
            self._log.warning(
                "forward-heal: %s lacks the updater package - skipping",
                _HEAL_REMOTE_REF,
            )
            return None
        return component, tip

    async def _forward_heal_once(self) -> bool:
        """One forward-heal pass: attempt the new origin/main tip if we are in fallback."""
        state = await asyncio.to_thread(self._read_state)
        comp_state = state.get(_UI_COMPONENT, {})
        if not isinstance(comp_state, dict):
            return False
        raw = comp_state.get("fast_attempt", 0)
        if not (isinstance(raw, int) and not isinstance(raw, bool)) or raw < 2:
            return False  # healthy, not yet in deep fallback, or corrupt counter
        target = await self._forward_heal_target(comp_state)
        if target is None:
            return False
        component, tip = target
        self._log.info(
            "forward-heal: new %s tip %s, upgrading", _HEAL_REMOTE_REF, tip[:8]
        )
        async with self._git_lock:
            ok_reset, _ = await git_reset_to_hash(component.path, _HEAL_REMOTE_REF)
        if not ok_reset:
            return False

        def _apply(s: dict) -> None:
            """Reset the attempt counter and record the healed tip."""
            comp = _ensure_comp(s, _UI_COMPONENT)
            comp["fast_attempt"] = 0
            # Reused as "last remote tip attempted": blocks re-healing to the same tip.
            comp["last_failed_remote"] = tip

        await self._mutate_state(_apply)
        post = await get_service_nrestarts(_UI_SERVICE)
        self._rebaseline_samples(_UI_COMPONENT, post)
        ok = await self._restart_ui_service()
        self._history("forward_heal", _UI_COMPONENT, ok=ok, reverted_to=tip[:12])
        return ok

    def _write_fault_marker(self, reason: str) -> None:
        """Record that fast recovery saturated so a human/telemetry can see it later."""
        try:
            self._fault_marker_path.parent.mkdir(
                mode=0o700, parents=True, exist_ok=True
            )
            self._fault_marker_path.write_text(
                json.dumps({"reason": reason, "ts": time.time()})
            )
        except OSError:
            self._log.warning("failed to write self-heal fault marker")

    def _clear_fault_marker(self) -> None:
        """Clear the saturation fault marker after a successful bless."""
        try:
            self._fault_marker_path.unlink(missing_ok=True)
        except OSError:
            self._log.warning("failed to clear self-heal fault marker")

    async def reconcile(self) -> None:
        """Heal repos left damaged by a power loss mid-update, for every component."""
        with process_lock() as acquired:
            if not acquired:
                self._log.info(
                    "reconcile: another updater holds the lock - skipping boot heal"
                )
                return
            await self._reconcile_locked()

    async def _revert_inflight(self) -> None:
        """Revert any update cut off mid-flight by a power loss before it committed."""
        inflight = await asyncio.to_thread(self._read_inflight)
        if not inflight:
            return
        self._log.warning(
            "reconcile: in-flight marker present - reverting %d interrupted repo(s)",
            len(inflight),
        )
        by_name = {c.name: c for c in self._components}
        unresolved: dict[str, str] = {}  # reverts that failed: kept for next-boot retry
        for name, prev_hash in inflight.items():
            comp = by_name.get(name)
            # Gone component/path or invalid hash can never revert: drop (bounds retries).
            if comp is None or comp.path is None or not comp.path.exists():
                continue
            if not _GIT_SHA_RE.match(prev_hash):
                self._log.error("reconcile: %s in-flight prev_hash invalid", name)
                continue
            async with self._git_lock:
                if await git_get_hash(comp.path) == prev_hash:
                    continue  # already at the pre-update commit
                rok, _ = await git_reset_to_hash(comp.path, prev_hash)
                self._history("boot_rollback", name, ok=rok, reverted_to=prev_hash[:12])
                self._log.warning(
                    "reconcile: %s reverted in-flight update to %s (ok=%s)",
                    name,
                    prev_hash[:8],
                    rok,
                )
                if not rok:
                    unresolved[name] = prev_hash  # keep marker so next boot retries
        # Clear on full success; else persist only the still-failing entries (retry).
        if unresolved:
            await asyncio.to_thread(self._write_inflight, unresolved)
        else:
            await asyncio.to_thread(self._clear_inflight)

    async def _boot_repair_component(self, c: ComponentConfig) -> bool:
        """Repair one git component with an unreadable HEAD at boot; True if recloned."""
        if c.path is None:
            return False
        async with self._git_lock:
            if await git_get_hash(c.path) != "":
                return False
            self._log.warning("reconcile: %s HEAD unreadable - repairing", c.name)
            # No configured branch: git_repair derives the repo's own default.
            ok, msg = await git_repair(c.path, c.branch)
            if ok and await git_get_hash(c.path) != "":
                self._history("boot_repair", c.name, detail=msg[:80])
                return False
            if await self._reclone_component(c) and await git_get_hash(c.path):
                self._history("boot_reclone", c.name)
                return True
            comp_state = (await asyncio.to_thread(self._read_state)).get(c.name, {})
            prev = comp_state.get("prev_hash") if isinstance(comp_state, dict) else None
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
            return False

    async def _boot_reclone_hook(self, c: ComponentConfig) -> None:
        """Best-effort post-reclone hook to rebuild in-repo artifacts (e.g. Spoolman .venv)."""
        if c.path is None:
            return
        try:
            new_hash = await git_get_hash(c.path)
            hook_ok, hook_err = await run_hook(
                c.name, c.path, new_hash, _GIT_EMPTY_TREE, timeout=HOOK_TIMEOUT
            )
            if not hook_ok:
                self._log.warning("%s: post-reclone hook failed: %s", c.name, hook_err)
        except Exception:  # noqa: BLE001
            # Best-effort: a hook crash must not kill the rest of boot heal.
            self._log.warning("%s: post-reclone hook raised", c.name, exc_info=True)

    async def _reconcile_locked(self) -> None:
        """Boot heal under the lock: revert in-flight, repair repos, run reclone hooks, sanitize state."""
        await self._revert_inflight()
        self._log.info("reconcile: boot-checking git components for damage")
        recloned: list[ComponentConfig] = []
        for c in self._components:
            if c.kind != "git" or c.path is None or not c.path.exists():
                continue
            if await self._boot_repair_component(c):
                recloned.append(c)
        # Reclone drops in-repo artifacts; rebuild them best-effort outside _git_lock.
        for c in recloned:
            await self._boot_reclone_hook(c)
        await self._reconcile_self_heal_state()

    async def _reconcile_self_heal_state(self) -> None:
        """Validate self-heal state fields; drop corrupt hashes, clamp counter."""
        async with self._state_lock:
            state = await asyncio.to_thread(self._read_state)
            changed = False
            for name, comp_state in list(state.items()):
                if not isinstance(comp_state, dict):
                    self._log.warning("reconcile: %s entry not a dict - dropping", name)
                    del state[name]
                    changed = True
                    continue
                for field in ("last_good", "golden", "last_failed_remote"):
                    if field in comp_state:
                        val = comp_state[field]
                        if not isinstance(val, str) or not _GIT_SHA_RE.match(val):
                            self._log.warning(
                                "reconcile: %s %s corrupt/invalid - dropping",
                                name,
                                field,
                            )
                            del comp_state[field]
                            changed = True
                if "fast_attempt" in comp_state:
                    val = comp_state["fast_attempt"]
                    if isinstance(val, bool) or not isinstance(val, int):
                        self._log.warning(
                            "reconcile: %s fast_attempt not an int - dropping", name
                        )
                        del comp_state["fast_attempt"]
                        changed = True
                    else:
                        clamped = min(max(val, 0), 3)
                        if clamped != val:
                            self._log.info(
                                "reconcile: %s fast_attempt clamped %d -> %d",
                                name,
                                val,
                                clamped,
                            )
                            comp_state["fast_attempt"] = clamped
                            changed = True
            if changed:
                await asyncio.to_thread(self._write_state, state)

    async def _rollback(
        self, component: ComponentConfig, prev_hash: str, reason: str
    ) -> None:
        """Reset one component to prev_hash, restart its service, and report failure."""
        self._log.warning(
            "%s: rolling back to %s (reason=%s)", component.name, prev_hash[:8], reason
        )
        ok, _ = await git_reset_to_hash(component.path, prev_hash)
        if ok:
            await asyncio.to_thread(self._clear_inflight)
        else:
            # A failed revert keeps the marker so boot _revert_inflight retries it.
            self._log.warning("rollback: revert failed - keeping in-flight marker")
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
            # No venv: PEP 668 blocks system pip; component installer owns deps.
            self._log.info(
                "%s: no component venv - skipping dep install", component.name
            )
            return (True, "no venv - deps managed externally")
        req = component.path / "requirements.txt"
        if not req.exists():
            return (True, "no requirements.txt")
        mode = req.stat().st_mode & 0o777
        if mode & 0o002:
            # SEC: world-writable only; group-writable is permitted (blocksscreen group is trusted)
            return (False, "world-writable permissions")

        # Keep pip current (best-effort: a failed upgrade must not block reqs).
        await _run([pip_path, "install", "--upgrade", "pip", "--quiet"], timeout=120.0)
        # Generous: one aarch64 source build (no wheel) easily exceeds 120s on a Pi.
        return await _run(
            [pip_path, "install", "-r", str(req), "--quiet"], timeout=600.0
        )

    async def _ping_while(
        self, coro, name: str, step: int, total: int, interval: float = 60.0
    ):
        """Await coro, re-emitting on_step every `interval` seconds."""
        task = asyncio.ensure_future(coro)
        try:
            while True:
                done, _ = await asyncio.wait({task}, timeout=interval)
                if done:
                    return task.result()
                self._cb("on_step", name, step, total)
        finally:
            if not task.done():
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task

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
        """Emit on_error and on_component_done(False); return False."""
        self._cb("on_error", name, reason)
        self._cb("on_component_done", name, False)
        return False

    def _history(self, event: str, name: str, **fields: object) -> None:
        """Append one event to the persistent update-history log (OBS-1)."""
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event": event,
            "component": name,
        } | fields
        try:
            self._history_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with self._history_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            self._trim_history()
        except OSError as exc:
            self._log.warning("update history write failed: %s", exc)

    def _trim_history(self) -> None:
        """Cap the on-SD history so a years-running device cannot fill the card."""
        if self._history_path.stat().st_size <= _HISTORY_MAX_BYTES:
            return
        lines = self._history_path.read_text(encoding="utf-8").splitlines()
        tmp = self._history_path.with_name(self._history_path.name + ".tmp")
        tmp.write_text("\n".join(lines[-_HISTORY_KEEP_LINES:]) + "\n", encoding="utf-8")
        tmp.replace(self._history_path)

    def _quarantine_sync(self, path: Path) -> Path | None:
        """Rename a non-repo dir aside (same fs, instant, reversible); None on failure."""
        dest = path.with_name(
            f"{path.name}.pre-updater-{time.strftime('%Y%m%d-%H%M%S')}"
        )
        try:
            os.rename(path, dest)
        except OSError as exc:
            self._log.error("quarantine of %s failed: %s", path, exc)
            return None
        # The venv moved with the dir: a cached pip path would now dangle.
        self._component_pip_cache.pop(str(path), None)
        return dest

    async def _quarantine_nonrepo(self, component: ComponentConfig) -> bool:
        """Move an install_if_missing component's non-repo dir aside for a fresh clone."""
        if component.path is None:
            return False
        dest = await asyncio.to_thread(self._quarantine_sync, component.path)
        if dest is None:
            return False
        self._history("quarantine_nonrepo", component.name, moved_to=dest.name)
        self._log.warning(
            "%s: non-repo dir quarantined to %s; provisioning fresh clone",
            component.name,
            dest,
        )
        return True

    async def _remove_clone(self, component: ComponentConfig) -> None:
        """Delete a freshly-cloned tree (the path did not exist before provisioning)."""
        if component.path is not None:
            await asyncio.to_thread(shutil.rmtree, component.path, ignore_errors=True)

    async def _fail_provision(self, component: ComponentConfig, reason: str) -> bool:
        """Remove the partial clone, log, and report failure."""
        await self._remove_clone(component)
        self._history("install_failed", component.name, reason=reason)
        self._log.warning(
            "%s: provision failed (%s), partial clone removed", component.name, reason
        )
        return self._cb_error_done(component.name, reason)

    async def _provision_restart_service(
        self, component: ComponentConfig
    ) -> str | None:
        """Restart+enable the provisioned service; return a fail reason or None on success."""
        if not component.service:
            return None
        svc_ok, svc_err = await restart_service(component.service)
        if not svc_ok:
            self._log.error("%s: provision restart: %s", component.name, svc_err)
            return "restart"
        if not await wait_for_service_active(component.service, timeout=90.0):
            self._log.error("%s: provisioned service not active", component.name)
            return "restart_timeout"
        # Enable only after a clean start (no boot-looping failed unit).
        en_ok, en_err = await enable_service(component.service)
        if not en_ok:
            self._log.warning(
                "%s: enable failed (runs now, may not persist): %s",
                component.name,
                en_err,
            )
        return None

    async def _provision_component(self, component: ComponentConfig) -> bool:
        """Clone and set up a missing opted-in component."""
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
            hook_ok, hook_err = await self._ping_while(
                run_hook(
                    component.name,
                    component.path,
                    new_hash,
                    _GIT_EMPTY_TREE,
                    timeout=HOOK_TIMEOUT,
                ),
                component.name,
                3,
                4,
            )
            if not hook_ok:
                self._log.error("%s: provision hook: %s", component.name, hook_err)
                return await self._fail_provision(component, "hook")

            self._cb("on_step", component.name, 4, 4)
            reason = await self._provision_restart_service(component)
            if reason:
                return await self._fail_provision(component, reason)

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

    async def _reclone_into_tmp(self, component: ComponentConfig, tmp: Path) -> bool:
        """Clone (+ optional version pin) into a temp dir; rmtree + False on failure."""
        if not component.url:
            return False
        self._log.warning("%s: recloning from %s", component.name, component.url)
        ok, err = await git_clone(component.url, tmp, component.branch)
        if not ok:
            await asyncio.to_thread(shutil.rmtree, tmp, ignore_errors=True)
            self._log.error("%s: reclone clone failed: %s", component.name, err)
            return False
        if component.version:
            vok, verr = await git_reset_to_hash(tmp, component.version)
            if not vok:
                await asyncio.to_thread(shutil.rmtree, tmp, ignore_errors=True)
                self._log.error("%s: reclone pin failed: %s", component.name, verr)
                return False
        return True

    async def _reclone_swap(
        self, component: ComponentConfig, path: Path, tmp: Path, old: Path
    ) -> bool:
        """Atomically swap the fresh tmp clone into place; restore + False on failure."""
        try:
            # move old aside first: renaming onto a nonempty dir is ENOTEMPTY
            if path.exists():
                await asyncio.to_thread(os.rename, path, old)
            await asyncio.to_thread(os.rename, tmp, path)
        except OSError as exc:
            if not path.exists() and old.exists():  # restore after a half-done swap
                with contextlib.suppress(OSError):
                    await asyncio.to_thread(os.rename, old, path)
            await asyncio.to_thread(shutil.rmtree, tmp, ignore_errors=True)
            self._log.error("%s: reclone swap failed: %s", component.name, exc)
            return False
        await asyncio.to_thread(shutil.rmtree, old, ignore_errors=True)
        return True

    async def _reclone_component(self, component: ComponentConfig) -> bool:
        """Reclone an unrepairable repo: fresh clone to a temp dir, then atomic swap."""
        if not component.url or component.path is None:
            return False
        path = component.path
        tmp = path.parent / f".{path.name}.reclone-tmp"
        old = path.parent / f".{path.name}.reclone-old"
        for stale in (tmp, old):  # clear orphans from a crashed prior reclone
            await asyncio.to_thread(shutil.rmtree, stale, ignore_errors=True)
        if not await self._reclone_into_tmp(component, tmp):
            return False
        if not await self._reclone_swap(component, path, tmp, old):
            return False
        # A fresh clone has no in-repo venv: drop any cached pip path for it.
        self._component_pip_cache.pop(str(path), None)
        self._history("reclone", component.name, url=component.url)
        self._log.warning("%s: recloned successfully", component.name)
        return True

    @staticmethod
    def _self_update_target(component: ComponentConfig) -> str:
        """The ref _stage_component would move the host to (version/branch/HEAD)."""
        if component.version:
            return component.version
        if component.branch:
            return f"origin/{component.branch}"
        return "origin/HEAD"

    async def _stage_fetch_gate(
        self, component: ComponentConfig
    ) -> tuple[bool, str] | None:
        """Fetch-gate (30s) + fetch, fsck-repair on corruption. None=proceed, tuple=abort."""
        if component.path is None:
            return (False, "path not found")
        async with self._git_lock:
            # Gate on last *successful* fetch: errored repos always re-fetch here.
            last_fetch = self._fetch_times.pop(component.name, 0.0)
        elapsed = time.monotonic() - last_fetch if last_fetch else float("inf")

        if elapsed >= 30:
            ok, error = await git_fetch(component.path)
            if not ok:
                self._log.error(error)
                # connectivity-only fsck can miss it; pass the fetch error as hint.
                if not await git_has_corruption(component.path, hint=error):
                    return (False, "network")
                self._log.warning("%s: corrupt repo, repairing", component.name)
                rok, rmsg = await git_repair(component.path)
                if rok:
                    self._history("repair", component.name, detail=rmsg[:80])
                elif await self._reclone_component(component):  # deepest rung
                    self._history("repair", component.name, detail="recloned")
                else:
                    return (False, "corrupt")
        return None

    async def _stage_guard_target(
        self, component: ComponentConfig
    ) -> tuple[bool, str] | None:
        """Pre-checkout guards: dead upstream branch + updater-marker brick guard."""
        # A deleted upstream branch must fail here, not strand the repo mid-switch.
        if component.branch and not await git_ref_hash(
            component.path, f"origin/{component.branch}"
        ):
            return (
                False,
                f"branch origin/{component.branch} not found - fix components.yaml",
            )

        # Updater host must never checkout code lacking updater: Type=notify unit lacks sd_notify READY causes crash loop with no self-heal.
        if component.name == _UI_COMPONENT:
            target = self._self_update_target(component)
            if target and not await git_tree_has_path(
                component.path, target, _UPDATER_MARKER
            ):
                self._log.error(
                    "%s: target %s lacks the updater package - refusing brick downgrade",
                    component.name,
                    target,
                )
                return (False, "refusing downgrade past updater")
        return None

    async def _stage_apply_ref(self, component: ComponentConfig) -> tuple[bool, str]:
        """Checkout target branch, then hard-reset / version-pin / soft-pull to the tip."""
        if component.path is None:
            return (False, "path not found")
        # Switch to the target branch FIRST so reset/pull act on the right branch.
        if component.branch:
            # hard mode forces past untracked collisions (build artifacts).
            force = component.reset_mode == "hard"
            ok, err = await git_checkout(component.path, component.branch, force=force)
            if not ok:
                self._log.error("%s: git_checkout failed: %s", component.name, err)
                return (False, "branch")

        if component.reset_mode == "hard":
            # Reset the (now current) branch to its remote tip, discarding divergence.
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
        elif component.reset_mode != "hard":
            # Soft mode: fast-forward (branch already checked out, or default).
            ok, err = await git_pull(component.path)
            if not ok:
                self._log.error("%s: git_pull failed: %s", component.name, err)
                return (False, "conflict")
        return (True, "")

    async def _stage_component(self, component: ComponentConfig) -> tuple[bool, str]:
        """Bring the working tree to its target ref: fetch-gate + reset/checkout/pull."""
        gate = await self._stage_fetch_gate(component)
        if gate is not None:
            return gate
        guard = await self._stage_guard_target(component)
        if guard is not None:
            return guard
        return await self._stage_apply_ref(component)

    async def _restart_one(self, service: str) -> bool:
        """Restart a service and verify it came active (kill-fallback aware)."""
        self._log.info("restarting %s and waiting for active", service)
        ok, err = await restart_service(service)
        if not ok:
            self._log.error("restart %s failed: %s", service, err)
            return False
        if not await wait_for_service_active(service, timeout=90.0):
            self._log.error("%s did not become active after restart", service)
            return False
        self._log.info("%s active after restart", service)
        return True

    async def _preflight_git_update(self, component: ComponentConfig) -> bool | None:
        """Validate path/repo; return None to proceed or a bool to short-circuit."""
        if component.path is None:
            return self._cb_error_done(component.name, "path not found")
        if not component.path.exists():
            if component.install_if_missing and component.url:
                return await self._provision_component(component)
            return self._cb_error_done(component.name, "path not found")
        # Non-repo dir (e.g. pre-updater tarball install): nothing to update or revert.
        if not is_git_repo(component.path):
            if (
                component.install_if_missing
                and component.url
                and await self._quarantine_nonrepo(component)
            ):
                return await self._provision_component(component)
            self._log.error(
                "%s: %s is not a git repository", component.name, component.path
            )
            return self._cb_error_done(
                component.name, "not a git repository - reinstall required"
            )
        return None

    async def _prepare_rollback_point(
        self, component: ComponentConfig
    ) -> tuple[bool, str]:
        """Persist prev_hash rollback point + inflight marker, then verify https remote."""
        prev_hash = await git_get_hash(component.path)
        if prev_hash == "":
            self._log.error("prev_hash is empty")
            return self._cb_error_done(component.name, "prev_hash empty"), ""
        async with self._state_lock:
            state = await asyncio.to_thread(self._read_state)
            # Merge: replacing the entry would wipe the self-heal anchors (last_good/golden).
            _ensure_comp(state, component.name)["prev_hash"] = prev_hash
            if not await asyncio.to_thread(self._write_state, state):
                return (
                    self._cb_error_done(
                        component.name, "failed to persist rollback point"
                    ),
                    "",
                )
            if not await asyncio.to_thread(
                self._write_inflight, {component.name: prev_hash}
            ):
                return (
                    self._cb_error_done(
                        component.name, "failed to write in-flight marker"
                    ),
                    "",
                )
        ok, reason = await _assert_https_remote(component.path)
        if not ok:
            self._log.error("SEC-4 remote check failed: %s", reason)
            # Nothing staged: drop the marker (avoids a spurious boot revert).
            await asyncio.to_thread(self._clear_inflight)
            return self._cb_error_done(component.name, "insecure remote"), ""
        self._history("update_start", component.name, prev_hash=prev_hash[:12])
        return True, prev_hash

    async def _run_git_phases(
        self, component: ComponentConfig, prev_hash: str
    ) -> tuple[bool, str]:
        """Run stage->deps->hook->restart; rollback + return (False, '') on any failure."""
        self._cb("on_step", component.name, 1, 4)
        stage_ok, stage_reason = await self._stage_component(component)
        if not stage_ok:
            # Pre-checkout failures leave the tree untouched: no revert, no restart.
            if (
                stage_reason in ("network", "corrupt")
                or "not found" in stage_reason
                or "refusing" in stage_reason
            ):
                await asyncio.to_thread(self._clear_inflight)
                return self._cb_error_done(component.name, stage_reason), ""
            # checkout/reset/pin/pull may have moved the tree: full rollback.
            await self._rollback(component, prev_hash, stage_reason)
            return False, ""

        self._cb("on_step", component.name, 2, 4)
        deps_ok, deps_err = await self._install_dependencies(component)
        if not deps_ok:
            self._log.warning("dependencies error: %s", deps_err)
            await self._rollback(component, prev_hash, "deps")
            return False, ""

        self._cb("on_step", component.name, 3, 4)
        new_hash = await git_get_hash(component.path)
        hook_ok, hook_err = await self._ping_while(
            run_hook(
                component.name,
                component.path,
                new_hash,
                prev_hash,
                timeout=HOOK_TIMEOUT,
            ),
            component.name,
            3,
            4,
        )
        if not hook_ok:
            self._log.error("hook failed for %s: %s", component.name, hook_err)
            await self._rollback(component, prev_hash, "hook")
            return False, ""

        self._cb("on_step", component.name, 4, 4)
        fire_and_forget = component.service in _FIRE_AND_FORGET_SERVICES
        if (
            component.service
            and not fire_and_forget
            and not await self._restart_one(component.service)
        ):
            await self._rollback(component, prev_hash, "restart")
            return False, ""
        # Bounce klipper too when requested and it isn't the component's own service.
        klipper_svc = self._klipper_service()
        if component.restart_klipper and component.service != klipper_svc:
            if not await self._restart_one(klipper_svc):
                await self._rollback(component, prev_hash, "restart")
                return False, ""
        return True, new_hash

    async def _fire_and_forget_restart(self, component: ComponentConfig) -> None:
        """Post-commit: kick self/UI/klipper-config restart without waiting."""
        fire_and_forget = component.service in _FIRE_AND_FORGET_SERVICES
        # Self/UI service: queue the restart only after success is recorded.
        if fire_and_forget and component.service:
            self._log.info(
                "%s updated; fire-and-forget restart of %s (no wait)",
                component.name,
                component.service,
            )
            await restart_service_noblock(component.service)
        # klipper/RF50 hold config the UI reads at startup: refresh it too.
        elif component.restart_ui:
            self._log.info(
                "%s updated (restart_ui); fire-and-forget restart of %s",
                component.name,
                _UI_SERVICE,
            )
            await restart_service_noblock(_UI_SERVICE)

    async def _run_git_update(self, component: ComponentConfig) -> bool:
        """Update a single existing git component, rolling back on any failure."""
        short = await self._preflight_git_update(component)
        if short is not None:
            return short
        ok, prev_hash = await self._prepare_rollback_point(component)
        if not ok:
            return False

        committed = False
        try:
            phases_ok, new_hash = await self._run_git_phases(component, prev_hash)
            if not phases_ok:
                return False
            self._history("update_success", component.name, new_hash=new_hash[:12])
            self._cb("on_component_done", component.name, True)
            committed = True
            await asyncio.to_thread(self._clear_inflight)
            await self._fire_and_forget_restart(component)
            await self._apply_deferred_restart()
            return True
        except asyncio.CancelledError:
            if committed:
                raise
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
            if committed:
                self._log.error(
                    "%s: post-commit error (update stands)",
                    component.name,
                    exc_info=True,
                )
                return True
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

    def _apt_failed(self, err: str) -> None:
        """Open the apt breaker, classifying the failure as permanent or transient."""
        self._apt_backoff.trip(permanent=classify_apt_error(err) == "permanent")

    async def _run_apt_update(self, component: ComponentConfig) -> bool:
        """Refresh + upgrade apt packages under the apt lock (system component update path)."""
        _apt_cache = Path.home() / ".cache" / "blockscreen" / "apt_status_cache.json"
        async with self._apt_lock:
            return await self._run_apt_update_locked(component, _apt_cache)

    async def _run_apt_update_locked(
        self, component: ComponentConfig, _apt_cache: Path
    ) -> bool:
        """apt refresh, upgrade, and autoremove under the apt lock with snapshot rollback."""
        try:
            if self._apt_backoff.cooling_down():
                self._log.debug("apt cooling down; skipping update")
                return self._cb_error_done(component.name, "apt cooling down")
            ok, err = await apt_update()
            if not ok:
                self._log.error("apt_update failed: %s", err)
                self._apt_failed(err)
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
                self._apt_failed(err)
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
            self._apt_backoff.reset()
            return True
        except asyncio.CancelledError:
            self._log.warning("%s: apt update cancelled", component.name)
            # May have SIGKILLed dpkg; repair the package db before reporting.
            await self._shielded(
                _apt_get_fix_broken(), f"{component.name} apt cancel-repair"
            )
            self._cb("on_error", component.name, "cancelled")
            self._cb("on_component_done", component.name, False)
            raise

    def _read_state(self) -> dict:
        """Return the self-heal state dict, empty on missing/corrupt/wrong-shape."""
        try:
            data = json.loads(self._state_path.read_text())
        except (OSError, ValueError):
            return {}
        # Valid JSON of the wrong shape (torn/corrupt write) must read as empty.
        return data if isinstance(data, dict) else {}

    def _read_inflight(self) -> dict[str, str]:
        """Return the in-flight batch marker as a name->prev_hash dict."""
        try:
            data = json.loads(self._inflight_path.read_text())
        except (OSError, ValueError):
            return {}
        if not isinstance(data, dict):
            return {}
        # Drop corrupt entries so a torn write can't crash the boot revert.
        return {k: v for k, v in data.items() if isinstance(k, str) and _is_sha(v)}

    def _write_inflight(self, mapping: dict[str, str]) -> bool:
        """Atomically record the in-flight batch's name->prev_hash map (fsync'd)."""
        try:
            self._inflight_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                dir=self._inflight_path.parent,
                delete=False,
                prefix=".updater_inflight_",
            ) as f:
                f.write(json.dumps(mapping))
                f.flush()
                os.fsync(f.fileno())
                temp_path = Path(f.name)
            temp_path.chmod(0o600)
            temp_path.replace(self._inflight_path)
            self._fsync_dir(self._inflight_path.parent)
            return True
        except OSError:
            self._log.error("Failed to write in-flight marker")
            return False

    def _clear_inflight(self) -> None:
        """Remove the in-flight marker; the batch reached a terminal outcome."""
        try:
            self._inflight_path.unlink(missing_ok=True)
            self._fsync_dir(self._inflight_path.parent)
        except OSError:
            self._log.warning("Failed to clear in-flight marker")

    def _write_state(self, data: dict) -> bool:
        """Atomically write the self-heal state file (temp, fsync, replace)."""
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
                # fsync file+dir so the rollback point survives a power cut.
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

    async def _mutate_state(self, mutate: Callable[[dict], None]) -> bool:
        """Atomically read-modify-write the state file under the state lock."""
        async with self._state_lock:
            state = await asyncio.to_thread(self._read_state)
            mutate(state)
            return await asyncio.to_thread(self._write_state, state)

    @staticmethod
    def _fsync_dir(path: Path) -> None:
        """fsync a directory so a contained rename survives power loss."""
        with contextlib.suppress(OSError):
            fd = os.open(path, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)

    async def background_apt_upgrade(self) -> None:
        """Run apt update + upgrade + autoremove silently after every Update click."""
        async with self._apt_lock:
            await self._background_apt_upgrade_locked()

    async def _background_apt_upgrade_locked(self) -> None:
        """Silent apt update, upgrade, and autoremove honoring the apt excludes."""
        if self._apt_backoff.cooling_down():
            self._log.debug("apt cooling down; skipping background upgrade")
            return
        self._log.info("background apt upgrade: starting")
        ok, err = await apt_update()
        if not ok:
            self._log.warning("background apt-get update failed: %s", err)
            self._apt_failed(err)
            return
        # Honor the apt excludes: a silent background kernel/firmware bump is the brick risk they prevent.
        exclude = tuple(
            pat for c in self._components if c.kind == "apt" for pat in c.apt_exclude
        )
        ok, err = await apt_upgrade(exclude=exclude)
        if not ok:
            self._log.warning("background apt upgrade failed: %s", err)
            self._apt_failed(err)
            return
        self._apt_backoff.reset()
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
