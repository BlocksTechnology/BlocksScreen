"""The updater CLI (status/update/recover) must import without sdbus present."""

from __future__ import annotations

import builtins
import fcntl
import sys

import pytest


@pytest.fixture
def _no_sdbus(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "sdbus" or name.startswith("sdbus."):
            raise ModuleNotFoundError("No module named 'sdbus'")
        return real_import(name, *args, **kwargs)

    for mod in [m for m in sys.modules if m == "updater" or m.startswith("updater.")]:
        monkeypatch.delitem(sys.modules, mod, raising=False)
    monkeypatch.delitem(sys.modules, "sdbus", raising=False)
    monkeypatch.setattr(builtins, "__import__", fake_import)
    yield


def test_cli_module_imports_without_sdbus(_no_sdbus):
    import updater  # noqa: F401
    import updater.__main__ as cli

    assert hasattr(cli, "main")
    # The non-daemon subcommands must be constructible without sdbus.
    parser = cli.build_parser()
    args = parser.parse_args(["status"])
    assert args.command == "status"


def test_package_does_not_pull_in_sdbus(_no_sdbus):
    import updater  # noqa: F401

    assert "sdbus" not in sys.modules


def test_cli_lock_rejects_concurrent_run(monkeypatch, tmp_path):
    """A second mutating CLI run exits when the lock is already held."""
    # Local import: this module's other tests mask sdbus before importing updater.
    from updater import __main__ as cli

    lock_path = tmp_path / "updater_cli.lock"
    monkeypatch.setattr(cli, "_cli_lock_path", lambda: lock_path)
    holder = open(lock_path, "w")
    fcntl.flock(holder, fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        with pytest.raises(SystemExit):
            with cli._cli_lock():
                pass
    finally:
        fcntl.flock(holder, fcntl.LOCK_UN)
        holder.close()
