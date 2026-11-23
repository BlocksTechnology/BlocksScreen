"""Tests for install-updater.sh's print guard: no build or restart may start under a live job."""

from __future__ import annotations

import re
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "install-updater.sh"
_GUARD = 'bs_wait_moonraker_idle "$_MOONRAKER_CONF" 0 || true'


def _lines() -> list[str]:
    return _SCRIPT.read_text().splitlines()


def test_guard_runs_before_the_first_system_change() -> None:
    lines = _lines()
    guard = next(i for i, line in enumerate(lines) if _GUARD in line)
    first_sudo = next(i for i, line in enumerate(lines) if re.match(r"\s*sudo ", line))
    assert guard < first_sudo


def test_guard_runs_again_before_device_discovery_build() -> None:
    lines = _lines()
    build = next(
        i for i, line in enumerate(lines) if "if _setup_device_discovery; then" in line
    )
    assert any(_GUARD in line for line in lines[build - 4 : build])
