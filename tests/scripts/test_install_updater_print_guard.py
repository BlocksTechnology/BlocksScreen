"""Tests for install-updater.sh's print guard: no build or restart may start under a live job."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
_SCRIPT = _SCRIPTS / "install-updater.sh"
_CALL = "_wait_print_idle"


def _lines() -> list[str]:
    return _SCRIPT.read_text().splitlines()


def _calls() -> list[int]:
    return [i for i, line in enumerate(_lines()) if line.strip() == _CALL]


def _first(needle: str) -> int:
    return next(i for i, line in enumerate(_lines()) if needle in line)


def test_guard_runs_before_the_first_system_change() -> None:
    first_sudo = next(
        i for i, line in enumerate(_lines()) if re.match(r"\s*sudo ", line)
    )
    assert _calls()[0] < first_sudo


def test_guard_runs_before_pip_takes_the_venv_lock() -> None:
    lock = _first("flock -w 300 201")
    assert any(lock - 12 < i < lock for i in _calls())


def test_guard_runs_again_before_device_discovery_build() -> None:
    build = _first("if _setup_device_discovery; then")
    assert any(build - 5 < i < build for i in _calls())


def test_guard_is_the_only_direct_caller_of_the_wait() -> None:
    direct = [line for line in _lines() if "bs_wait_moonraker_idle" in line]
    assert len(direct) == 1


def _run_guard(tmp_path: Path, **env: str) -> str:
    # Real guard body with the wait stubbed to leave a marker.
    body = re.search(r"^_wait_print_idle\(\) \{.*\}$", _SCRIPT.read_text(), re.M)
    assert body
    marker = tmp_path / "waited"
    script = (
        f'bs_wait_moonraker_idle() {{ echo "$@" >"{marker}"; }}\n'
        f"_MOONRAKER_CONF=/x/moonraker.conf\n{body.group(0)}\nset -e\n{_CALL}\n"
    )
    res = subprocess.run(
        ["bash", "-c", script],
        capture_output=True,
        check=False,
        env={
            **{k: v for k, v in os.environ.items() if k != "BS_SKIP_PRINT_WAIT"},
            **env,
        },
        text=True,
        timeout=20,
    )
    assert res.returncode == 0
    return marker.read_text().strip() if marker.exists() else ""


def test_guard_waits_uncapped_by_default(tmp_path: Path) -> None:
    assert _run_guard(tmp_path) == "/x/moonraker.conf 0"


def test_guard_bypass_skips_the_wait(tmp_path: Path) -> None:
    assert _run_guard(tmp_path, BS_SKIP_PRINT_WAIT="1") == ""


def test_deploy_check_fallback_sets_the_bypass() -> None:
    # The fallback runs inside BlocksScreen.service ExecStartPre: a print wait would hold the UI back.
    text = (_SCRIPTS / "bs-deploy-check.sh").read_text()
    assert re.search(r"BS_SKIP_PRINT_WAIT=1 exec .*install-updater\.sh", text)
