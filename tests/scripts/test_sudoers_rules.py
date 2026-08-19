"""Guard: apt privilege now flows only through the root-owned bs-apt-helper.

sudo matches the FULL argv, so the daemon's apt argvs and the sudoers rules
install-updater.sh emits must agree. The wrapper is the single grant; its own
argument validation is what makes the trailing '*' safe.
"""

from __future__ import annotations

import fnmatch
import re
import subprocess
from pathlib import Path

import pytest

import updater.executor as executor
from updater.executor import _apt_cmd

_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
_INSTALLER = _SCRIPTS / "install-updater.sh"
_HELPER = _SCRIPTS / "bs-apt-helper.sh"

_WRAPPER_RULE = "/usr/local/sbin/bs-apt-helper *"


def _sudoers_rules() -> list[str]:
    """Extract every literal NOPASSWD rule body emitted by install-updater.sh."""
    return re.findall(
        r"printf 'blocks ALL=\(ALL\) NOPASSWD: ([^']+?)(?:\\n)?'",
        _INSTALLER.read_text(),
    )


def _daemon_apt_argvs() -> list[list[str]]:
    """The sudo apt argvs the daemon builds (mirrors executor call sites)."""
    return [
        _apt_cmd("update"),
        _apt_cmd("upgrade", ["vim", "curl"]),
        _apt_cmd("autoremove"),
        _apt_cmd("fix-broken"),
        _apt_cmd("dselect-upgrade"),
    ]


class TestSudoersRules:
    def test_wrapper_rule_emitted(self):
        assert _WRAPPER_RULE in _sudoers_rules()

    def test_deployed_path_pins_all_three_sides(self):
        # executor constant == sudoers rule command == installer destination.
        rule_path = _WRAPPER_RULE.split()[0]
        assert str(executor.APT_HELPER) == rule_path
        assert f"mv -Tf /usr/local/sbin/.bs-apt-helper.new {rule_path}" in (
            _INSTALLER.read_text()
        )

    def test_no_direct_apt_rules_remain(self):
        for rule in _sudoers_rules():
            assert "apt-get" not in rule and "/usr/bin/dpkg" not in rule, (
                f"direct apt/dpkg rule bypasses the wrapper: {rule!r}"
            )

    def test_wrapper_argvs_match_rule(self):
        for argv in _daemon_apt_argvs():
            cmd = " ".join(argv[1:])
            assert fnmatch.fnmatch(cmd, _WRAPPER_RULE), f"unmatched argv: {cmd!r}"


class TestWrapperValidation:
    """The wrapper must reject anything but its fixed verbs and clean names.

    All cases exit before reaching apt, so they run unprivileged.
    """

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["/bin/bash", str(_HELPER), *args], capture_output=True, timeout=10
        )

    @pytest.mark.parametrize(
        "args",
        [
            [],
            ["badverb"],
            ["upgrade"],  # needs at least one package
            ["upgrade", "-o"],  # option injection
            ["upgrade", "--reinstall"],
            ["upgrade", "vim;rm"],  # shell metachars
            ["upgrade", "vim", "-oAPT::Update::Pre-Invoke::=x"],
            ["update", "extra"],  # fixed verbs take no args
            ["autoremove", "extra"],
            ["set-selections", "extra"],
        ],
    )
    def test_rejects(self, args):
        assert self._run(*args).returncode == 2

    def test_valid_package_names_pass_validation(self):
        # Passes validation, then fails at apt (no root): anything but exit 2.
        res = self._run("upgrade", "libstdc++6", "python3.11-dev")
        assert res.returncode != 2
