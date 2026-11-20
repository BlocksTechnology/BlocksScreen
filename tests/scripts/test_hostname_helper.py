"""Guard: hostname-helper.sh keeps /etc/hosts tidy and regenerates cloned identity."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

_HELPER = Path(__file__).resolve().parents[2] / "scripts" / "hostname-helper.sh"
_NAME = "BLOCKS-RF50-2eb3f7e8fe6b454e"
_BASE = "127.0.0.1\tlocalhost\n::1\t\tlocalhost ip6-localhost ip6-loopback\n"


def _ensure(hosts: Path) -> str:
    """Source the helper with root writes stubbed out and run ensure_hosts_entry."""
    script = f'source "{_HELPER}"; as_root() {{ "$@"; }}; ensure_hosts_entry "$1" "$2"'
    res = subprocess.run(
        ["bash", "-c", script, "bash", _NAME, str(hosts)],
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    return res.stdout


@pytest.mark.parametrize(
    "before",
    [
        # Release-2.0 prepended a space-separated line per boot, #305 rewrote them to tabs.
        f"127.0.1.1 {_NAME}\n127.0.1.1 {_NAME}\n" + _BASE + f"127.0.1.1\t{_NAME}\n",
        _BASE + "127.0.1.1\told-name\n",
        _BASE,
    ],
    ids=["duplicates", "stale-name", "missing"],
)
def test_collapses_to_one_entry(tmp_path: Path, before: str) -> None:
    hosts = tmp_path / "hosts"
    hosts.write_text(before)
    _ensure(hosts)
    lines = hosts.read_text().splitlines()
    assert [ln for ln in lines if ln.startswith("127.0.1.1")] == [f"127.0.1.1\t{_NAME}"]
    assert "127.0.0.1\tlocalhost" in lines


def test_correct_file_is_left_alone(tmp_path: Path) -> None:
    hosts = tmp_path / "hosts"
    hosts.write_text(_BASE + f"127.0.1.1\t{_NAME}\n")
    before = hosts.stat().st_mtime_ns
    assert "Rewriting" not in _ensure(hosts)
    assert hosts.stat().st_mtime_ns == before


_MACHINE_ID = Path("etc/machine-id")
_DBUS_MACHINE_ID = Path("var/lib/dbus/machine-id")
_HOST_KEY = Path("etc/ssh/ssh_host_ed25519_key.pub")
_MARKER = Path("var/lib/blocksscreen/identity-serial")
_IMAGE_ID = "0" * 31 + "1\n"
_IMAGE_KEY = "ssh-ed25519 IMAGE-KEY root@image\n"
_SERIAL = "1000000000000001"
_OTHER_SERIAL = "1000000000000002"


@pytest.fixture
def cloned_root(tmp_path: Path) -> Path:
    """Fake root filesystem carrying the identity shared by a cloned image."""
    root = tmp_path / "root"
    for rel, content in (
        (_MACHINE_ID, _IMAGE_ID),
        (_DBUS_MACHINE_ID, _IMAGE_ID),
        (_HOST_KEY, _IMAGE_KEY),
    ):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(content)
    return root


def _ensure_identity(root: Path, serial: str, path: str | None = None) -> None:
    """Source the helper with root writes stubbed out and run ensure_identity."""
    script = f'source "{_HELPER}"; as_root() {{ "$@"; }}; ensure_identity "$1" "$2"'
    subprocess.run(
        ["bash", "-c", script, "bash", serial, str(root)],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
        env={**os.environ, "PATH": path or os.environ["PATH"]},
    )


@pytest.mark.skipif(shutil.which("ssh-keygen") is None, reason="needs ssh-keygen")
def test_identity_regenerates_once_per_serial(cloned_root: Path) -> None:
    _ensure_identity(cloned_root, _SERIAL)
    machine_id = (cloned_root / _MACHINE_ID).read_text()
    assert re.fullmatch(r"[0-9a-f]{32}\n", machine_id) and machine_id != _IMAGE_ID
    assert os.readlink(cloned_root / _DBUS_MACHINE_ID) == "/etc/machine-id"
    host_key = (cloned_root / _HOST_KEY).read_text()
    assert host_key.startswith("ssh-ed25519 ") and host_key != _IMAGE_KEY
    assert not (cloned_root / "etc/ssh/.hostkeys-new").exists()
    assert (cloned_root / _MARKER).read_text() == f"{_SERIAL}\n"

    _ensure_identity(cloned_root, _SERIAL)
    assert (cloned_root / _MACHINE_ID).read_text() == machine_id

    # Same SD card moved to another board.
    _ensure_identity(cloned_root, _OTHER_SERIAL)
    assert (cloned_root / _MACHINE_ID).read_text() != machine_id


def test_identity_keygen_failure_keeps_keys_and_retries(
    cloned_root: Path, tmp_path: Path
) -> None:
    stubs = tmp_path / "bin"
    stubs.mkdir()
    keygen = stubs / "ssh-keygen"
    keygen.write_text("#!/bin/sh\nexit 1\n")
    keygen.chmod(0o755)
    _ensure_identity(cloned_root, _SERIAL, path=f"{stubs}:{os.environ['PATH']}")
    assert (cloned_root / _HOST_KEY).read_text() == _IMAGE_KEY
    assert not (cloned_root / _MARKER).exists()


@pytest.mark.parametrize(
    ("state", "expected"),
    [("initializing", 0), ("starting", 1), ("running", 1), ("degraded", 1)],
)
def test_identity_only_before_basic_target(
    tmp_path: Path, state: str, expected: int
) -> None:
    systemctl = tmp_path / "systemctl"
    systemctl.write_text(f"#!/bin/sh\necho {state}\nexit 1\n")
    systemctl.chmod(0o755)
    res = subprocess.run(
        ["bash", "-c", f'source "{_HELPER}"; early_boot'],
        capture_output=True,
        timeout=10,
        env={**os.environ, "PATH": f"{tmp_path}:{os.environ['PATH']}"},
    )
    assert res.returncode == expected
