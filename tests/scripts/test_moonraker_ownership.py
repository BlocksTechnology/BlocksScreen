"""Tests for bs-common.sh single-ownership of Moonraker update_manager blocks."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_FN = Path(__file__).resolve().parents[2] / "scripts" / "bs-common.sh"

_CONF = """\
[update_manager]
enable_system_updates: False

[update_manager mainsail]
type: web

[update_manager klipper]
type: git_repo
path: ~/klipper

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
    assert "#[update_manager klipper]" in out  # updater owns klipper, not moonraker
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


_MIGRATE_CONF = """\
[server]
host: 0.0.0.0

[update_manager]
enable_system_updates: False

[update_manager BlocksScreen]
type: git_repo
primary_branch: master
managed_services: klipper moonraker

[update_manager other]
primary_branch: master
"""


def _migrate(conf: Path) -> str:
    # Shim sudo: the function ends with `sudo systemctl restart moonraker`; real
    # sudo would prompt on a dev TTY (test hang) or bounce services on the printer.
    shim = conf.parent / "bin"
    shim.mkdir(exist_ok=True)
    fake_sudo = shim / "sudo"
    fake_sudo.write_text("#!/bin/sh\nexit 0\n")
    fake_sudo.chmod(0o755)
    env = {**os.environ, "PATH": f"{shim}:{os.environ.get('PATH', '')}"}
    subprocess.run(
        [
            "bash",
            "-c",
            f'. "{_FN}"; bs_migrate_moonraker_conf "{conf}" test',
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        timeout=20,
    )
    return conf.read_text()


def test_migrate_fixes_blocksscreen_branch_and_services(tmp_path: Path) -> None:
    conf = tmp_path / "moonraker.conf"
    conf.write_text(_MIGRATE_CONF)
    out = _migrate(conf)
    bs = out.split("[update_manager BlocksScreen]")[1].split("[update_manager other]")[
        0
    ]
    assert "primary_branch: main" in bs  # origin/master does not exist upstream
    assert "managed_services: BlocksScreen" in bs
    # Patches are scoped to the BlocksScreen section: others keep their values.
    assert "primary_branch: master" in out.split("[update_manager other]")[1]


def test_migrate_is_idempotent(tmp_path: Path) -> None:
    conf = tmp_path / "moonraker.conf"
    conf.write_text(_MIGRATE_CONF)
    first = _migrate(conf)
    second = _migrate(conf)
    assert first == second
