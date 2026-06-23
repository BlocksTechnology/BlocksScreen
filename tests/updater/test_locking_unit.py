"""Tests for the cross-process updater lock."""

from __future__ import annotations

import updater.locking as locking
from updater.locking import lock_path, process_lock, restart_sentinel_path


def test_lock_path_is_under_home_or_run(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    p = lock_path()
    assert p.name == "updater.lock"


def test_restart_sentinel_path_name(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    p = restart_sentinel_path()
    assert p.name == "updater-restart-needed"
    # Shares the runtime dir with the lock so both clear/live together.
    assert p.parent == lock_path().parent


def test_acquire_then_second_attempt_fails(monkeypatch, tmp_path):
    monkeypatch.setattr(locking, "lock_path", lambda: tmp_path / "updater.lock")
    with process_lock() as first:
        assert first is True
        # A second independent open()+flock of the same file must fail fast.
        with process_lock() as second:
            assert second is False
    # Released after the outer context — re-acquire succeeds.
    with process_lock() as third:
        assert third is True
