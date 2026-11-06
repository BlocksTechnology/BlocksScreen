import subprocess  # nosec: B404
from unittest.mock import MagicMock

import pytest
from BlocksScreen.lib import machine
from BlocksScreen.lib.machine import MachineControl


@pytest.fixture
def run(monkeypatch):
    mock = MagicMock(return_value=MagicMock(stdout="out", stderr=""))
    monkeypatch.setattr(machine.subprocess, "run", mock)
    return mock


@pytest.fixture
def mc(qtbot):
    return MachineControl(None)


def _commands(run):
    return [c.args[0] for c in run.call_args_list]


@pytest.mark.parametrize(
    "error",
    [
        subprocess.CalledProcessError(1, ["sudo"], stderr="a password is required"),
        subprocess.TimeoutExpired(["sudo"], 5),
        FileNotFoundError(),
    ],
)
def test_failed_command_returns_none(mc, run, error):
    run.side_effect = error
    assert mc.restart_klipper_mcu_service() is None


def test_klipper_restart_starts_host_mcu_first(mc, run):
    mc.restart_klipper_service()
    assert _commands(run) == [
        ["sudo", "systemctl", "start", "klipper-mcu.service"],
        ["sudo", "systemctl", "restart", "klipper.service", "--no-block"],
    ]


def test_klipper_restart_runs_when_host_mcu_start_fails(mc, run):
    run.side_effect = [
        subprocess.CalledProcessError(5, ["sudo"], stderr=""),
        run.return_value,
    ]
    assert mc.restart_klipper_service() == "out\n"
    assert run.call_count == 2
