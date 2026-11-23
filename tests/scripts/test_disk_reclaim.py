"""Tests for bs-common.sh disk helpers used by the start script on a full disk."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

_FN = Path(__file__).resolve().parents[2] / "scripts" / "bs-common.sh"


def _run(tmp_path: Path, frees: list[int], call: str) -> tuple[int, Path]:
    # df shim serves one free-MiB value per call; sudo shim only logs, never escalates.
    shim = tmp_path / "bin"
    shim.mkdir(exist_ok=True)
    (tmp_path / "frees").write_text("\n".join(map(str, frees)) + "\n")
    df = shim / "df"
    df.write_text(
        "#!/bin/sh\n"
        f'f="{tmp_path}/frees"; v=$(head -n1 "$f"); tail -n +2 "$f" >"$f.n"; mv "$f.n" "$f"\n'
        'echo "Filesystem 1M-blocks Used Available Capacity Mounted"\n'
        'echo "/dev/root 1000 900 $v 90% /"\n'
    )
    sudo = shim / "sudo"
    sudo.write_text(f'#!/bin/sh\necho "$@" >>"{tmp_path}/sudo.log"\n')
    for f in (df, sudo):
        f.chmod(0o755)
    env = {**os.environ, "PATH": f"{shim}:{os.environ.get('PATH', '')}"}
    res = subprocess.run(
        ["bash", "-c", f'. "{_FN}"; {call}'], check=False, env=env, timeout=20
    )
    return res.returncode, tmp_path / "sudo.log"


def test_disk_still_low_after_reclaim(tmp_path: Path) -> None:
    home = tmp_path / "home"
    (home / ".cache" / "pip" / "wheels").mkdir(parents=True)
    rc, log = _run(tmp_path, [50, 80], f'bs_disk_low "{tmp_path}" "{home}"')
    assert rc == 0
    assert not (home / ".cache" / "pip").exists()
    assert "bs-apt-helper clean" in log.read_text()


def test_reclaim_freed_enough(tmp_path: Path) -> None:
    rc, _ = _run(tmp_path, [50, 900], f'bs_disk_low "{tmp_path}" "{tmp_path}"')
    assert rc == 1


def test_enough_space_skips_reclaim(tmp_path: Path) -> None:
    rc, log = _run(tmp_path, [900], f'bs_disk_low "{tmp_path}" "{tmp_path}"')
    assert rc == 1
    assert not log.exists()


def test_purge_pycache_keeps_sources(tmp_path: Path) -> None:
    pkg = tmp_path / "pkg"
    (pkg / "__pycache__").mkdir(parents=True)
    (pkg / "__pycache__" / "m.cpython-311.pyc").write_bytes(b"\0")
    (pkg / "m.py").write_text("x = 1\n")
    rc, _ = _run(tmp_path, [], f'bs_purge_pycache "{pkg}"')
    assert rc == 0
    assert not (pkg / "__pycache__").exists() and (pkg / "m.py").exists()
