"""Tests for install-updater.sh _reqs_current, the guard that skips a no-op requirements install."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "install-updater.sh"
_HASH = "0123456789abcdef0123456789abcdef"


def _current(venv: Path, req_hash: str) -> bool:
    # Only the function: running the whole installer would touch the system.
    script = (
        f"eval \"$(sed -n '/^_reqs_current() {{/,/^}}/p' '{_SCRIPT}')\"; "
        '_reqs_current "$@"'
    )
    return (
        subprocess.run(
            ["bash", "-c", script, "bash", req_hash, str(venv)],
            check=False,
            timeout=20,
        ).returncode
        == 0
    )


@pytest.mark.parametrize(
    ("sentinel", "attempt", "req_hash", "want"),
    [
        (_HASH, None, _HASH, True),
        (_HASH, f"{_HASH} 3", _HASH, False),  # bs-bootstrap gave up: still retried
        ("stale", None, _HASH, False),
        (None, None, _HASH, False),
        (_HASH, None, "", False),  # requirements.txt unreadable
    ],
)
def test_reqs_current(
    tmp_path: Path,
    sentinel: str | None,
    attempt: str | None,
    req_hash: str,
    want: bool,
) -> None:
    if sentinel is not None:
        (tmp_path / ".blockscreen-reqs-hash").write_text(f"{sentinel}\n")
    if attempt is not None:
        (tmp_path / ".blockscreen-reqs-attempt").write_text(f"{attempt}\n")
    assert _current(tmp_path, req_hash) is want


_FIRST = "install -r req.txt"
_RETRY = "install --no-cache-dir -r req.txt"


@pytest.mark.parametrize(
    ("fails", "want_rc", "want_calls"),
    [
        ("none", 0, [_FIRST]),
        (f'"{_FIRST}"', 0, [_FIRST, _RETRY]),  # truncated wheel in the pip cache
        ("*", 1, [_FIRST, _RETRY]),
    ],
)
def test_pip_install_retries_without_cache(
    tmp_path: Path, fails: str, want_rc: int, want_calls: list[str]
) -> None:
    calls = tmp_path / "calls"
    pip = tmp_path / "bin" / "pip"
    pip.parent.mkdir()
    pip.write_text(
        f'#!/bin/bash\necho "$*" >> {calls}\ncase "$*" in {fails}) exit 1;; esac\n'
    )
    pip.chmod(0o755)
    script = (
        f"eval \"$(sed -n '/^_pip_install() {{/,/^}}/p' '{_SCRIPT}')\"; "
        '_as_blocks() { "$@"; }; BSENV="$1"; shift; _pip_install "$@"'
    )
    rc = subprocess.run(
        ["bash", "-c", script, "bash", str(tmp_path), "-r", "req.txt"],
        check=False,
        timeout=20,
    ).returncode
    assert rc == want_rc
    assert calls.read_text().splitlines() == want_calls
