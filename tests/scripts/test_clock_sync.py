"""Tests for scripts/bs-clock-sync.sh (HTTP Date clock fallback)."""

from __future__ import annotations

import os
import subprocess
import time
from email.utils import formatdate
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "bs-clock-sync.sh"


def _run(
    tmp_path: Path,
    date_header: str | None,
    *,
    synced: bool = False,
    floor: int = 0,
) -> tuple[str, str]:
    """Run the script with curl/date shims; return (stdout, recorded date -s args)."""
    shim = tmp_path / "bin"
    shim.mkdir()
    log = tmp_path / "set.log"
    curl = shim / "curl"
    if date_header is None:
        curl.write_text("#!/bin/sh\nexit 6\n")
    else:
        curl.write_text(
            f"#!/bin/sh\nprintf 'HTTP/1.1 301\\r\\nDate: {date_header}\\r\\n'\n"
        )
    date = shim / "date"
    date.write_text(
        "#!/bin/bash\n"
        f'for a in "$@"; do [[ $a == -s ]] && {{ echo "$*" >>"{log}"; exit 0; }}; done\n'
        'exec /bin/date "$@"\n'
    )
    (shim / "fake-hwclock").write_text("#!/bin/sh\nexit 0\n")
    for f in shim.iterdir():
        f.chmod(0o755)
    flag = tmp_path / "synchronized"
    if synced:
        flag.touch()
    env = {
        **os.environ,
        "PATH": f"{shim}:{os.environ.get('PATH', '')}",
        "BS_CLOCK_SYNC_FLAG": str(flag),
        "BS_CLOCK_HOSTS": "http://a.invalid",
        "BS_CLOCK_FLOOR": str(floor),
    }
    res = subprocess.run(
        ["bash", str(_SCRIPT)], capture_output=True, text=True, env=env, timeout=20
    )
    assert res.returncode == 0, res.stderr
    return res.stdout, log.read_text() if log.exists() else ""


def _http_date(offset_s: int) -> str:
    return formatdate(time.time() + offset_s, usegmt=True)


@pytest.mark.parametrize(
    ("header", "synced", "floor"),
    [
        (_http_date(86400), True, 0),  # NTP synced: never touches the clock
        (None, False, 0),  # offline
        ("garbage", False, 0),  # malformed header
        (_http_date(30), False, 0),  # within MIN_STEP_S
        (_http_date(-86400), False, int(time.time())),  # older than BlocksScreen HEAD
    ],
)
def test_clock_left_alone(tmp_path: Path, header, synced, floor) -> None:
    assert _run(tmp_path, header, synced=synced, floor=floor)[1] == ""


@pytest.mark.parametrize("offset", [30 * 86400, -3600])
def test_clock_stepped_both_ways(tmp_path: Path, offset: int) -> None:
    out, set_args = _run(tmp_path, _http_date(offset))
    target = int(set_args.split("@")[1])
    assert abs(target - (time.time() + offset)) < 5
    assert "clock stepped" in out
