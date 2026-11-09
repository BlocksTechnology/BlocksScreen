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
    assert mc.restart_moonraker_service() is None


def _loaded(state: str = "loaded") -> MagicMock:
    return MagicMock(stdout=f"{state}\n", stderr="")


def test_klipper_restart_queues_host_mcu_first_without_blocking(mc, run):
    run.side_effect = [_loaded(), run.return_value, run.return_value]
    mc.restart_klipper_service()
    assert _commands(run)[1:] == [
        ["sudo", "-n", "systemctl", "--no-block", "start", "klipper-mcu.service"],
        ["sudo", "-n", "systemctl", "--no-block", "restart", "klipper.service"],
    ]


def test_klipper_restart_skips_missing_host_mcu_unit(mc, run):
    run.side_effect = [_loaded("not-found"), run.return_value]
    mc.restart_klipper_service()
    assert _commands(run)[1:] == [
        ["sudo", "-n", "systemctl", "--no-block", "restart", "klipper.service"],
    ]


def test_klipper_restart_runs_when_host_mcu_start_fails(mc, run):
    run.side_effect = [
        _loaded(),
        subprocess.CalledProcessError(5, ["sudo"], stderr=""),
        run.return_value,
    ]
    assert mc.restart_klipper_service() == "out\n"
    assert run.call_count == 3


def test_host_mcu_load_state_is_queried_once(mc, run):
    run.return_value = _loaded()
    mc.restart_klipper_service()
    mc.restart_klipper_service()
    shows = [c for c in _commands(run) if c[:2] == ["systemctl", "show"]]
    assert len(shows) == 1


def test_failed_load_state_query_is_retried(mc, run):
    run.side_effect = [
        FileNotFoundError(),
        run.return_value,
        _loaded(),
        run.return_value,
        run.return_value,
    ]
    mc.restart_klipper_service()
    mc.restart_klipper_service()
    assert [
        "sudo",
        "-n",
        "systemctl",
        "--no-block",
        "start",
        "klipper-mcu.service",
    ] in (_commands(run))
