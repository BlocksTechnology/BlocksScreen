"""Tests for install-updater.sh _apt_installed, the guard that skips no-op apt-get installs."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "install-updater.sh"

# Fake dpkg-query: prints the status named in $FAKE_<pkg>, else fails like an unknown package.
_FAKE_DPKG_QUERY = """#!/bin/bash
pkg="${@: -1}"
var="FAKE_${pkg//[^a-zA-Z0-9]/_}"
[[ -n "${!var:-}" ]] || exit 1
printf '%s' "${!var}"
"""


def _installed(tmp_path: Path, pkgs: list[str], states: dict[str, str]) -> int:
    shim = tmp_path / "bin"
    shim.mkdir(exist_ok=True)
    fake = shim / "dpkg-query"
    fake.write_text(_FAKE_DPKG_QUERY)
    fake.chmod(0o755)
    env = {**os.environ, "PATH": f"{shim}:{os.environ.get('PATH', '')}"}
    env.update(
        {f"FAKE_{p.replace('-', '_').replace('.', '_')}": s for p, s in states.items()}
    )
    # Only the function: running the whole installer would touch the system.
    script = f"eval \"$(sed -n '/^_apt_installed() {{/,/^}}/p' '{_SCRIPT}')\"; _apt_installed \"$@\""
    return subprocess.run(
        ["bash", "-c", script, "bash", *pkgs],
        check=False,
        env=env,
        timeout=20,
    ).returncode


def test_all_installed_skips_install(tmp_path: Path) -> None:
    states = {"libsystemd-dev": "installed", "python3-dev": "installed"}
    assert _installed(tmp_path, ["libsystemd-dev", "python3-dev"], states) == 0


@pytest.mark.parametrize("state", ["half-configured", "config-files", "unpacked"])
def test_partial_state_still_installs(tmp_path: Path, state: str) -> None:
    states = {"libsystemd-dev": "installed", "python3-dev": state}
    assert _installed(tmp_path, ["libsystemd-dev", "python3-dev"], states) == 1


def test_unknown_package_still_installs(tmp_path: Path) -> None:
    states = {"libusb-1.0-0": "installed"}
    assert _installed(tmp_path, ["libusb-1.0-0", "libudev1"], states) == 1
