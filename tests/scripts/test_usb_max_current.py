"""Tests for bs-common.sh bs_ensure_usb_max_current config.txt placement."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_FN = Path(__file__).resolve().parents[2] / "scripts" / "bs-common.sh"

# Stock Raspberry Pi OS tail with a user edit that leaves a conditional section open.
_CONFIG = """\
dtparam=audio=on

[cm4]
otg_mode=1

[cm5]
dtoverlay=dwc2,dr_mode=host"""


def _ensure(cfg: Path) -> subprocess.CompletedProcess[str]:
    # Pass-through sudo shim: the helper writes via `sudo tee`, a tmp file needs no root.
    shim = cfg.parent / "bin"
    shim.mkdir(exist_ok=True)
    fake_sudo = shim / "sudo"
    fake_sudo.write_text('#!/bin/sh\nexec "$@"\n')
    fake_sudo.chmod(0o755)
    env = {**os.environ, "PATH": f"{shim}:{os.environ.get('PATH', '')}"}
    return subprocess.run(
        ["bash", "-c", f'. "{_FN}"; bs_ensure_usb_max_current "{cfg}" test'],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        timeout=20,
    )


def test_setting_lands_under_all_not_the_open_section(tmp_path: Path) -> None:
    cfg = tmp_path / "config.txt"
    cfg.write_text(_CONFIG)
    assert _ensure(cfg).returncode == 0
    tail = cfg.read_text().split("[cm5]")[1]
    assert tail.index("[all]") < tail.index("usb_max_current_enable=1")


def test_idempotent(tmp_path: Path) -> None:
    cfg = tmp_path / "config.txt"
    cfg.write_text(_CONFIG)
    _ensure(cfg)
    first = cfg.read_text()
    assert _ensure(cfg).returncode == 0
    assert cfg.read_text() == first
    assert first.count("usb_max_current_enable=1") == 1
