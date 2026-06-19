"""Tests for bs-common.sh single-ownership of Moonraker update_manager blocks."""

from __future__ import annotations

import subprocess
from pathlib import Path

_FN = Path(__file__).resolve().parents[2] / "scripts" / "bs-common.sh"

_CONF = """\
[update_manager]
enable_system_updates: False

[update_manager mainsail]
type: web

[update_manager RF50-Klipper]
type: git_repo
path: ~/RF50-Klipper

[update_manager crowsnest]
type: git_repo
path: ~/crowsnest
"""


def _run(conf: Path) -> str:
    # Exit code is non-zero on a no-op re-run (nothing changed) by design, so we
    # assert on resulting file content rather than the return code.
    subprocess.run(
        [
            "bash",
            "-c",
            f'. "{_FN}"; bs_disable_overlapping_update_managers "{conf}" test',
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    return conf.read_text()


def test_owned_blocks_commented_others_untouched(tmp_path: Path) -> None:
    conf = tmp_path / "moonraker.conf"
    conf.write_text(_CONF)
    out = _run(conf)
    assert "#[update_manager RF50-Klipper]" in out
    assert "#[update_manager crowsnest]" in out
    assert "[update_manager mainsail]" in out  # web client kept
    assert "#[update_manager mainsail]" not in out
    assert "enable_system_updates: False" in out  # system section untouched


def test_idempotent(tmp_path: Path) -> None:
    conf = tmp_path / "moonraker.conf"
    conf.write_text(_CONF)
    first = _run(conf)
    second = _run(conf)
    assert first == second  # no double-comment on re-run
