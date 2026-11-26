"""Shared fixutres for updater tests.

Mocks sdbus before any updater.dbus_service import so tests run
withouth a real D-Bus session bus.
"""

import asyncio
import importlib
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class _FakeDbusBase:
    """Real Python base class so inheritance does not raise TypeError"""

    def __init__(self, *a, **kw) -> None:
        pass

    def __init_subclass__(cls, **kw) -> None:
        super().__init_subclass__()


@pytest.fixture(scope="module", autouse=True)
def mock_sdbus():
    mock = MagicMock()
    mock.DbusInterfaceCommonAsync = _FakeDbusBase
    mock.dbus_signal_async = lambda *a, **kw: lambda fn: fn
    mock.dbus_method_async = lambda *a, **kw: lambda fn: fn
    with pytest.MonkeyPatch.context() as mp:
        for key in ("sdbus", "updater", "updater.dbus_service"):
            mp.delitem(sys.modules, key, raising=False)
        mp.setitem(sys.modules, "sdbus", mock)
        yield mock


def _rebase(value, real: Path, home: Path):
    """Map a path (or tuple of paths) under the real home onto the test home."""
    if isinstance(value, tuple):
        return tuple(_rebase(v, real, home) for v in value)
    if isinstance(value, Path) and value.is_relative_to(real):
        return home / value.relative_to(real)
    return value


@pytest.fixture(autouse=True)
def hermetic_home(tmp_path, monkeypatch):
    """Import-time home paths and the lock dir point at tmp, never the real ~/.cache."""
    # mock_sdbus re-imports the package, so the cached submodule is not its attribute.
    locking = importlib.import_module("updater.locking")
    real, home = Path.home(), tmp_path / "home"
    run = home / ".cache" / "blockscreen"
    run.mkdir(parents=True)
    monkeypatch.setattr(locking, "_runtime_dir", lambda: run)
    for name, mod in list(sys.modules.items()):
        if name != "updater" and not name.startswith("updater."):
            continue
        for attr, value in list(vars(mod).items()):
            rebased = _rebase(value, real, home)
            if rebased is not value:
                monkeypatch.setattr(mod, attr, rebased)
    return home


@pytest.fixture(autouse=True)
def printing():
    """Klipper idle unless a test sets return_value; never dials a real klippy.sock."""
    m = AsyncMock(return_value=False)
    with (
        patch("updater.service.klipper_printing", m),
        patch("updater.dbus_service.klipper_printing", m),
    ):
        yield m


@pytest.fixture(autouse=True)
def apt_lists_partial(tmp_path):
    """Host apt state never leaks in; tests create or touch this path to simulate a refresh."""
    path = tmp_path / "apt-lists-partial"
    with patch("updater.service._APT_LISTS_PARTIAL", path):
        yield path


@pytest.fixture(autouse=True)
def no_real_sudo(monkeypatch):
    """Unmocked repair paths must not run real sudo: no tty trips Howdy, then pam_faillock."""
    executor = importlib.import_module("updater.executor")
    monkeypatch.setattr(executor, "SUDO", "/usr/bin/false")


@pytest.fixture(autouse=True)
def moonraker():
    """Moonraker unreachable; never dials the host's real :7125."""
    with (
        patch("updater.service.moonraker_repo_hashes", AsyncMock(return_value=None)),
        patch("updater.service.moonraker_refresh_repo", AsyncMock(return_value=None)),
    ):
        yield


@pytest.fixture(autouse=True)
def disk():
    """Plenty of free space; never wipes the host's caches or bytecode."""
    free = MagicMock(return_value=10_000.0)
    inodes = MagicMock(return_value=1_000_000.0)
    # Real reclaim returns free space after.
    reclaim = AsyncMock(side_effect=lambda path=None: free(path))
    with (
        patch("updater.service.free_disk_mb", free),
        patch("updater.service.free_disk_inodes", inodes),
        patch("updater.service.reclaim_disk", reclaim),
        patch("updater.service.purge_pycache", MagicMock(return_value=0)) as purge,
    ):
        yield MagicMock(free=free, inodes=inodes, reclaim=reclaim, purge=purge)


@pytest.fixture
def svc():
    """UpdaterDbusService with mocked UpdateService and signals."""
    from updater.dbus_service import UpdaterDbusService
    from updater.models import ComponentConfig, ComponentStatus

    mock_svc = MagicMock()
    mock_svc.update_all = AsyncMock()
    mock_svc.update_component = AsyncMock()
    mock_svc.check_status = AsyncMock(
        return_value={
            "klipper": ComponentStatus(name="klipper", commits_behind=2),
        }
    )
    mock_svc.recover = AsyncMock()
    mock_svc.has_fetch_failures = MagicMock(return_value=False)
    mock_svc.provision_missing = AsyncMock(return_value=False)
    mock_svc.run_followup = AsyncMock(return_value=(False, False))
    mock_svc.background_apt_upgrade = AsyncMock()
    mock_svc.daemon_restart_pending = False
    mock_svc.update_committed = False
    mock_svc.reconcile = AsyncMock(return_value=True)
    mock_svc.reconcile_if_pending = AsyncMock()
    mock_svc.sync_moonraker = AsyncMock(return_value=True)
    mock_svc.deploy_pending = MagicMock(return_value=False)
    mock_svc.followup_pending = MagicMock(return_value=False)
    # Units stay live while the flag is set unless a test says otherwise.
    mock_svc.deploy_running = AsyncMock(side_effect=lambda: mock_svc.deploy_pending())
    mock_svc.deploy_flag_stamp = MagicMock(return_value=1)
    mock_svc._components = [
        ComponentConfig(name="moonraker", kind="git"),
        ComponentConfig(name="klipper", kind="git"),
        ComponentConfig(name="system", kind="apt"),
    ]
    mock_svc.has_component = MagicMock(
        side_effect=lambda n: any(c.name == n for c in mock_svc._components)
    )
    mock_svc.component_stubs = MagicMock(
        side_effect=lambda: [(c.name, c.kind) for c in mock_svc._components]
    )
    s = UpdaterDbusService.__new__(UpdaterDbusService)
    s._svc = mock_svc
    s._busy = False
    s._provisioning = False
    s._provisioned = False
    s._followed_up = False
    s._followup_hold = False
    s._followup_running = False
    s._boot_pass_done = True
    s._deploy_hold = None
    s._capped_flag = None
    s._background_tasks = set()
    s._closing = False
    s._status_check_in_progress = False
    s._status_pending = False
    s._moonraker_sync = None
    s._git_guard = asyncio.Lock()
    s.busy_changed = MagicMock()
    s.provisioning_changed = MagicMock()
    s.status_ready = MagicMock()
    s.error = MagicMock()
    return s


@pytest.fixture
async def reconciled(svc):
    """svc whose boot reconcile already finished, so the periodic check can provision."""
    svc._reconcile_task = asyncio.get_running_loop().create_future()
    svc._reconcile_task.set_result(None)
    return svc
