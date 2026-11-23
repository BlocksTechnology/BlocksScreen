"""Tests for bs-common.sh healing a moonraker.conf torn by a power cut (BUG-5)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_FN = Path(__file__).resolve().parents[2] / "scripts" / "bs-common.sh"

# Already migrated: a healthy run patches nothing, so any restart comes from the heal.
_GOOD = """\
[server]
host: 0.0.0.0
port: 7125

[update_manager]
enable_system_updates: False

[update_manager BlocksScreen]
type: git_repo
primary_branch: main
managed_services: BlocksScreen

# blocksscreen-single-owner-v2 applied by BlocksScreen-start
"""
_MARK = "\n# blocksscreen-single-owner-v2 applied by BlocksScreen-start\n"


def _torn_tail() -> bytes:
    """T5b shape: the appended marker's data block lost behind the kept size."""
    body = _GOOD.replace(_MARK, "").encode()
    return body + b"\0" * len(_MARK)


def _migrate(cfg: Path) -> tuple[str, list[str]]:
    """Run bs_migrate_moonraker_conf with a logging sudo shim -> (stdout, sudo calls)."""
    shim = cfg.parent / "bin"
    shim.mkdir(exist_ok=True)
    calls = cfg.parent / "sudo.calls"
    sudo = shim / "sudo"
    sudo.write_text(f'#!/bin/sh\necho "$*" >> "{calls}"\nexit 0\n')
    sudo.chmod(0o755)
    env = {**os.environ, "PATH": f"{shim}:{os.environ.get('PATH', '')}"}
    res = subprocess.run(
        ["bash", "-c", f'. "{_FN}"; bs_migrate_moonraker_conf "{cfg}" test'],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        timeout=20,
    )
    made = calls.read_text().splitlines() if calls.exists() else []
    return res.stdout, made


def _conf(tmp_path: Path) -> Path:
    cfg_dir = tmp_path / "printer_data" / "config"
    cfg_dir.mkdir(parents=True)
    return cfg_dir / "moonraker.conf"


def test_torn_tail_restored_from_bak_and_moonraker_restarted(tmp_path: Path) -> None:
    conf = _conf(tmp_path)
    conf.write_bytes(_torn_tail())
    Path(f"{conf}.bak").write_text(_GOOD)
    out, sudo = _migrate(conf)
    assert conf.read_text() == _GOOD
    assert "restored from" in out
    assert "systemctl restart moonraker.service" in sudo
    assert (conf.parent / ".moonraker.conf.torn").read_bytes() == _torn_tail()


def test_torn_bak_falls_back_to_stripped_conf(tmp_path: Path) -> None:
    conf = _conf(tmp_path)
    conf.write_bytes(_torn_tail())
    # The pre-fix guard (grep [server]) backed up torn confs, so .bak can be torn too.
    Path(f"{conf}.bak").write_bytes(_torn_tail())
    out, sudo = _migrate(conf)
    healed = conf.read_text()
    assert "\0" not in healed
    assert healed.count("blocksscreen-single-owner-v2") == 1  # marker re-added once
    assert "restored from stripped" in out
    assert sudo == ["systemctl restart moonraker.service"]
    # .bak = the healed conf just before this run re-added the marker.
    assert Path(f"{conf}.bak").read_text() == _GOOD.replace(_MARK, "")


def test_all_nul_conf_restored_from_moonraker_backup(tmp_path: Path) -> None:
    conf = _conf(tmp_path)
    conf.write_bytes(b"\0" * 2048)
    (conf.parent / ".moonraker.conf.bkp").write_text("[server]\nhost = 0.0.0.0\n")
    out, sudo = _migrate(conf)
    assert conf.read_text().startswith("[server]\nhost = 0.0.0.0\n")
    assert "restored from" in out and ".moonraker.conf.bkp" in out
    assert "systemctl restart moonraker.service" in sudo


def test_empty_conf_with_no_sane_copy_is_left_untouched(tmp_path: Path) -> None:
    conf = _conf(tmp_path)
    conf.write_bytes(b"")
    Path(f"{conf}.bak").write_bytes(b"\0" * 64)
    out, sudo = _migrate(conf)
    assert conf.read_bytes() == b""  # no marker appended over the damage
    assert Path(f"{conf}.bak").read_bytes() == b"\0" * 64
    assert "no sane copy" in out
    assert sudo == []


def test_healthy_conf_is_not_rewritten(tmp_path: Path) -> None:
    conf = _conf(tmp_path)
    conf.write_text(_GOOD)
    Path(f"{conf}.bak").write_text("[server]\nstale: yes\n")
    out, sudo = _migrate(conf)
    assert conf.read_text() == _GOOD
    assert Path(f"{conf}.bak").read_text() == _GOOD
    assert out == ""
    assert sudo == []


def test_unparseable_conf_never_overwrites_bak(tmp_path: Path) -> None:
    conf = _conf(tmp_path)
    conf.write_text("[server]\nhost: 0.0.0.0\nnot an option line\n")
    Path(f"{conf}.bak").write_text(_GOOD)
    _migrate(conf)
    assert Path(f"{conf}.bak").read_text() == _GOOD


def test_marker_patch_writes_durably(tmp_path: Path) -> None:
    conf = _conf(tmp_path)
    conf.write_text(
        _GOOD.replace(_MARK, "\n[update_manager klipper]\ntype: git_repo\n")
    )
    shim = conf.parent / "bin"
    shim.mkdir()
    log = conf.parent / "sync.calls"
    (shim / "sync").write_text(f'#!/bin/sh\necho "$*" >> "{log}"\n')
    (shim / "sync").chmod(0o755)
    env = {**os.environ, "PATH": f"{shim}:{os.environ.get('PATH', '')}"}
    subprocess.run(
        ["bash", "-c", f'. "{_FN}"; bs_disable_overlapping_update_managers "{conf}" t'],
        check=False,
        env=env,
        timeout=20,
    )
    assert conf.read_text().endswith("# blocksscreen-single-owner-v2 applied by t\n")
    synced = log.read_text().splitlines()
    assert synced[-1] == str(conf.parent)  # dir fsync after the rename
    assert ".moonraker.conf." in synced[0]  # temp fsync before the rename
