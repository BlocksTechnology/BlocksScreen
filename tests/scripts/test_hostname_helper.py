"""Guard: hostname-helper.sh leaves exactly one 127.0.1.1 line in /etc/hosts."""

from __future__ import annotations

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
