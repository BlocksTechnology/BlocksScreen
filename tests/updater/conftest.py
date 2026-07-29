"""Shared fixutres for updater tests.

Mocks sdbus before any updater.dbus_service import so tests run
withouth a real D-Bus session bus.
"""

import sys
from unittest.mock import AsyncMock, MagicMock

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
    s._background_tasks = set()
    s._status_check_in_progress = False
    s._status_pending = False
    s.busy_changed = MagicMock()
    s.status_ready = MagicMock()
    s.error = MagicMock()
    return s
