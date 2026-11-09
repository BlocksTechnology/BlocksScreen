"""Tests for bs-common.sh bs_selfheal_engaged (start-script rollback hand-off)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
_FN = _SCRIPTS / "bs-common.sh"


def _engaged(tmp_path: Path, state: object, *, daemon_active: bool = True) -> bool:
    # systemctl shim: the helper only asks whether the daemon unit is active.
    shim = tmp_path / "bin"
    shim.mkdir(exist_ok=True)
    fake = shim / "systemctl"
    fake.write_text(f"#!/bin/sh\nexit {0 if daemon_active else 3}\n")
    fake.chmod(0o755)
    path = tmp_path / "updater_state.json"
    if state is not None:
        path.write_text(state if isinstance(state, str) else json.dumps(state))
    env = {**os.environ, "PATH": f"{shim}:{os.environ.get('PATH', '')}"}
    res = subprocess.run(
        ["bash", "-c", f'. "{_FN}"; bs_selfheal_engaged "{path}" "{sys.executable}"'],
        check=False,
        env=env,
        timeout=20,
    )
    return res.returncode == 0


@pytest.mark.parametrize("attempt", [1, 2, 3])
def test_engaged_while_ladder_runs(tmp_path: Path, attempt: int) -> None:
    assert _engaged(tmp_path, {"BlocksScreen": {"fast_attempt": attempt}})


@pytest.mark.parametrize(
    "state",
    [
        None,
        "{not json",
        "[]",
        {},
        {"BlocksScreen": "x"},
        {"BlocksScreen": {}},
        {"BlocksScreen": {"fast_attempt": 0}},
        {"BlocksScreen": {"fast_attempt": True}},
        {"BlocksScreen": {"fast_attempt": "2"}},
        {"klipper": {"fast_attempt": 2}},
    ],
)
def test_not_engaged_without_active_ladder(tmp_path: Path, state: object) -> None:
    assert not _engaged(tmp_path, state)


def test_dead_daemon_hands_rollback_back(tmp_path: Path) -> None:
    # A stale fast_attempt must not disable the legacy rollback when nobody is healing.
    state = {"BlocksScreen": {"fast_attempt": 2}}
    assert not _engaged(tmp_path, state, daemon_active=False)


def test_saturated_ladder_hands_rollback_back(tmp_path: Path) -> None:
    (tmp_path / "selfheal_fault.json").write_text("{}")
    assert not _engaged(tmp_path, {"BlocksScreen": {"fast_attempt": 3}})


def test_start_script_consults_helper_before_rolling_back() -> None:
    text = (_SCRIPTS / "BlocksScreen-start.sh").read_text()
    assert text.index("bs_selfheal_engaged") < text.index('reset --hard "$_last_good"')
