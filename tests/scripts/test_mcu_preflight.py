"""Tests for scripts/mcu_preflight.py and the DFU write path of flash_mcus.sh."""

from __future__ import annotations

import importlib.util
import json
import struct
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(_SCRIPTS))  # mcu_preflight imports its sibling mcu_versions
_spec = importlib.util.spec_from_file_location(
    "mcu_preflight", _SCRIPTS / "mcu_preflight.py"
)
assert _spec and _spec.loader
pf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pf)

STM32 = {
    "CONFIG_MACH_STM32": "y",
    "CONFIG_FLASH_BOOT_ADDRESS": "0x8000000",
    "CONFIG_FLASH_APPLICATION_ADDRESS": "0x8002000",
    "CONFIG_RAM_START": "0x20000000",
    "CONFIG_RAM_SIZE": "0x24000",
    "CONFIG_FLASH_SIZE": "0x80000",
}


def _image(stack: int = 0x20024000, reset: int = 0x8002101, size: int = 0x400) -> bytes:
    return struct.pack("<II", stack, reset) + bytes(size - 8)


@pytest.mark.parametrize(
    "katapult_cfg", sorted((_SCRIPTS / "mcu_config").glob("*.katapult.config"))
)
def test_shipped_katapult_configs_match_their_klipper_config(
    katapult_cfg: Path,
) -> None:
    klipper_cfg = katapult_cfg.with_name(katapult_cfg.name.replace(".katapult", ""))
    problems = pf.pair_problems(
        pf.read_kconfig(klipper_cfg), pf.read_kconfig(katapult_cfg)
    )
    assert problems == []


def test_pair_flags_can_pins_and_app_address() -> None:
    klipper = {**STM32, "CONFIG_STM32_CANBUS_PB0_PB1": "y"}
    katapult = {
        **STM32,
        "CONFIG_STM32_MMENU_CANBUS_PD0_PD1": "y",
        "CONFIG_STM32_CANBUS_PD0_PD1": "y",
        "CONFIG_LAUNCH_APP_ADDRESS": "0x8008000",
    }
    problems = pf.pair_problems(klipper, katapult)
    assert any(p.startswith("CAN pins") for p in problems)
    assert any(p.startswith("app address") for p in problems)


@pytest.mark.parametrize(
    ("image", "write_addr", "expected"),
    [
        (_image(), 0x8002000, None),
        (_image(), 0x8000000, "would be written at"),
        (_image(stack=0x30000000), None, "initial stack"),
        (_image(reset=0x8002100), None, "not a Thumb"),
        (_image(reset=0x8009001), None, "outside the image"),
        (_image(size=0x80000), None, "past flash"),
        (b"\x00" * 4, None, "too short"),
        (b"", None, "empty"),
    ],
)
def test_image_checks(
    image: bytes, write_addr: int | None, expected: str | None
) -> None:
    problems = pf.image_problems(STM32, image, write_addr)
    if expected is None:
        assert problems == []
    else:
        assert any(expected in p for p in problems), problems


_RP2040 = {
    "CONFIG_MACH_RPXXXX": "y",
    "CONFIG_FLASH_APPLICATION_ADDRESS": "0x10004000",
    "CONFIG_RAM_START": "0x20000000",
    "CONFIG_RAM_SIZE": "0x42000",
    "CONFIG_FLASH_SIZE": "0x200000",
}


def test_rp2040_app_above_bootloader_is_checked() -> None:
    cfg = {**_RP2040, "CONFIG_RPXXXX_HAVE_BOOTLOADER": "y"}
    assert pf.image_problems(cfg, _image(stack=0x20042000, reset=0x10004101)) == []
    assert pf.image_problems(cfg, _image(stack=0x20042000, reset=0x10000101))


def test_rp2040_without_bootloader_is_not_checked() -> None:
    # Klipper builds only a uf2 there; BOOTSEL flashing never takes this path.
    assert pf.image_problems(_RP2040, b"\xff" * 16) == []


def test_unresolved_katapult_app_start_choice_is_used() -> None:
    klipper = {**STM32}
    katapult = {"CONFIG_MACH_STM32": "y", "CONFIG_STM32_APP_START_8000": "y"}
    assert pf.pair_problems(klipper, katapult) == [
        "app address: Klipper 0x8002000, Katapult launches 0x8008000"
    ]
    katapult = {"CONFIG_MACH_STM32": "y", "CONFIG_STM32_APP_START_2000": "y"}
    assert pf.pair_problems(klipper, katapult) == []


def test_comms_ignores_unrelated_constants() -> None:
    running = {
        "MCU": "stm32h723xx",
        "CANBUS_BRIDGE": 1,
        "STATS_SUMSQ_BASE": 256,
    }
    assert pf.comms_problems({"MCU": "stm32h723xx", "CANBUS_BRIDGE": 1}, running) == []
    problems = pf.comms_problems({"MCU": "stm32h723xx"}, running)
    assert problems == ["CANBUS_BRIDGE: running 1, new build None"]


def test_comms_catches_crystal_to_internal_clock() -> None:
    running = {"MCU": "stm32h723xx", "RESERVE_PINS_crystal": "PH0,PH1"}
    problems = pf.comms_problems({"MCU": "stm32h723xx"}, running)
    assert problems == ["RESERVE_PINS_crystal: running 'PH0,PH1', new build None"]


_CONSTANTS = {"mcu": {"mcu_constants": {"MCU": "stm32g0b1xx", "CLOCK_FREQ": 64000000}}}


class _Moonraker(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        data = json.dumps({"result": {"status": _CONSTANTS}}).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_args: object) -> None:
        pass


@pytest.fixture
def moonraker_url():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Moonraker)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


@pytest.mark.parametrize(
    ("section", "mcu", "rc"),
    [("mcu", "stm32g0b1xx", 0), ("mcu", "stm32h723xx", 1), ("mcu gone", "x", 3)],
)
def test_comms_cli(
    moonraker_url: str, tmp_path: Path, section: str, mcu: str, rc: int
) -> None:
    dict_file = tmp_path / "klipper.dict"
    dict_file.write_text(json.dumps({"config": {"MCU": mcu, "CLOCK_FREQ": 64000000}}))
    argv = ["comms", "--dict", str(dict_file), "--section", section]
    assert pf.main(argv + ["--url", moonraker_url]) == rc


@pytest.mark.parametrize(
    ("new_ref", "rc"),
    [("CONFIG_CLOCK_REF_FREQ=25000000", 0), ("CONFIG_CLOCK_REF_FREQ=8000000", 1)],
)
def test_flashed_cli_catches_crystal_change(
    tmp_path: Path, new_ref: str, rc: int
) -> None:
    flashed = tmp_path / "flashed.config"
    flashed.write_text('CONFIG_MCU="stm32h723xx"\nCONFIG_CLOCK_REF_FREQ=25000000\n')
    new = tmp_path / "new.config"
    new.write_text(f'CONFIG_MCU="stm32h723xx"\n{new_ref}\n')
    assert pf.main(["flashed", "--new", str(new), "--flashed", str(flashed)]) == rc


def test_unreadable_input_is_not_a_comms_change(tmp_path: Path) -> None:
    missing = str(tmp_path / "missing.config")
    assert pf.main(["flashed", "--new", missing, "--flashed", missing]) == 4


# dfu-util stub: logs calls; the device leaves the --list after :leave unless STUCK=1,
# GONE=1 drops it from the list at once, LIST=fail makes --list itself error out.
# -U writes the image back (READBACK=bad corrupts it, READBACK=fail errors out).
_DFU_STUB = r"""
sudo() { "$@"; }
dfu-util() {
    echo "dfu-util $*" >>"$LOG"
    if [[ "$*" == *--list* ]]; then
        [ "${LIST:-}" = fail ] && return 74
        [ "${GONE:-}" = 1 ] && return 0
        if [ ! -f "$LOG.left" ] || [ "${STUCK:-}" = 1 ]; then
            echo 'Found DFU: [0483:df11] alt=0, serial="SER"'
        fi
        return 0
    fi
    [[ "$*" == *:leave* ]] && touch "$LOG.left"
    local up="" a prev=""
    for a in "$@"; do [ "$prev" = -U ] && up="$a"; prev="$a"; done
    if [ -n "$up" ]; then
        case "${READBACK:-}" in
        bad) printf 'X' >"$up" ;;
        fail) return 74 ;;
        *) cp "$IMAGE" "$up" ;;
        esac
    fi
    [ "${WRITE:-}" = fail ] && [[ "$*" == *" -D "* ]] && return 74
    return 0
}
"""


def _run_flash_dfu(tmp_path: Path, **env: str) -> tuple[int, list[str]]:
    image = tmp_path / "klipper.bin"
    image.write_bytes(_image())
    log = tmp_path / "dfu.log"
    script = (
        f'. "{_SCRIPTS / "flash_mcus.sh"}"; {_DFU_STUB}\n'
        'flash_dfu octopus 0483:df11 SER 0 0x08000000 "$IMAGE"'
    )
    res = subprocess.run(
        ["bash", "-c", script],
        capture_output=True,
        text=True,
        timeout=30,
        env={
            "PATH": "/usr/bin:/bin",
            "HOME": str(tmp_path),
            "IMAGE": str(image),
            "LOG": str(log),
            "DFU_LEAVE_WAIT": "2",
            **env,
        },
    )
    calls = log.read_text().splitlines() if log.exists() else []
    return res.returncode, calls


def _targets(calls: list[str]) -> list[str]:
    return [c.split(" -s ")[1].split()[0] for c in calls if " -s " in c]


def test_dfu_leaves_only_after_matching_readback(tmp_path: Path) -> None:
    rc, calls = _run_flash_dfu(tmp_path)
    assert rc == 0
    assert _targets(calls) == ["0x08000000", "0x08000000:1024", "0x08000000:leave"]
    assert calls[-1].endswith("--list")
    assert not (tmp_path / "klipper.readback.bin").exists()


def test_dfu_without_readback_leaves_but_reports_unverified(tmp_path: Path) -> None:
    rc, calls = _run_flash_dfu(tmp_path, READBACK="fail")
    assert rc == 3
    assert _targets(calls).count("0x08000000:1024") == 2  # readback retried once
    assert _targets(calls)[-1] == "0x08000000:leave"


def test_dfu_still_listed_after_leave_is_a_failure(tmp_path: Path) -> None:
    rc, calls = _run_flash_dfu(tmp_path, STUCK="1")
    assert rc == 1
    assert sum(c.endswith("--list") for c in calls) == 2


def test_dfu_unlistable_after_leave_is_unverified(tmp_path: Path) -> None:
    rc, calls = _run_flash_dfu(tmp_path, LIST="fail")
    assert rc == 3
    assert not list(tmp_path.glob("*.dfu-list.txt"))


@pytest.mark.parametrize("env", [{"READBACK": "fail"}, {"WRITE": "fail"}])
def test_dfu_board_gone_from_usb_is_a_failure(tmp_path: Path, env: dict) -> None:
    rc, calls = _run_flash_dfu(tmp_path, GONE="1", **env)
    assert rc == 1
    assert sum(" -D " in c for c in calls) == 1  # no rewrite to an absent board
    assert not any(":leave" in c for c in calls)


@pytest.mark.parametrize("env", [{"READBACK": "bad"}, {"WRITE": "fail"}])
def test_dfu_never_leaves_after_a_bad_write(tmp_path: Path, env: dict) -> None:
    rc, calls = _run_flash_dfu(tmp_path, **env)
    assert rc == 1
    assert sum(" -D " in c for c in calls) == 2  # one rewrite while still in DFU
    assert not any(":leave" in c for c in calls)


# cmd_flash with every hardware step stubbed; sudo calls and flashes go to $LOG.
_FLASH_STUBS = r"""
sudo() { echo "sudo $*" >>"$LOG"; }
build_firmware() { return 0; }
use_build() { :; }
preflight_firmware() { [[ " ${BAD:-} " != *" $1 "* ]]; }
flash_can() { echo "flash_can $1" >>"$LOG"; return 1; }
flash_dfu() { echo "flash_dfu $1" >>"$LOG"; return 0; }
bootloader_uuids() { echo "${IN_KATAPULT:-}"; }
_summary_box() { printf 'failed: %s\n' "${failed[@]}" >>"$LOG"; }
save_uuid_cache() { :; }
record_flash() { echo "record_flash $3" >>"$LOG"; }
check_host_power() { :; }
release_klipper() { :; }
ensure_can_up() { :; }
sleep() { :; }
CONTEXT=local FORCE=true FLASH_ORDER_LOCKED=false FLASH_NAMES=()
DISCOVERED=("toolhead|can|aaa|$TH_CFG||true" "octopus|dfu|SER|$BRIDGE_CFG||true")
"""


def _run_cmd_flash(tmp_path: Path, **env: str) -> tuple[int, str, list[str]]:
    (tmp_path / "th.cfg").write_text("CONFIG_CANBUS=y\n")
    (tmp_path / "bridge.cfg").write_text("CONFIG_USBCANBUS=y\n")
    log = tmp_path / "flash.log"
    script = f'. "{_SCRIPTS / "flash_mcus.sh"}"; {_FLASH_STUBS}\ncmd_flash'
    res = subprocess.run(
        ["bash", "-c", script],
        capture_output=True,
        text=True,
        timeout=30,
        env={
            "PATH": "/usr/bin:/bin",
            "HOME": str(tmp_path),
            "FW_BUILD_ROOT": str(tmp_path),
            "LOG": str(log),
            "TH_CFG": str(tmp_path / "th.cfg"),
            "BRIDGE_CFG": str(tmp_path / "bridge.cfg"),
            **env,
        },
    )
    calls = log.read_text().splitlines() if log.exists() else []
    return res.returncode, res.stdout + res.stderr, calls


def test_failed_preflight_never_stops_klipper(tmp_path: Path) -> None:
    rc, _, calls = _run_cmd_flash(tmp_path, BAD="toolhead octopus")
    assert rc == 1
    assert not any("systemctl stop" in c or c.startswith("flash_") for c in calls)
    assert calls.count("record_flash failed") == 2


def test_failed_can_node_retries_in_katapult_and_skips_bridge(tmp_path: Path) -> None:
    rc, _, calls = _run_cmd_flash(tmp_path, IN_KATAPULT="aaa")
    assert rc == 1
    assert calls.count("flash_can toolhead") == 2
    assert "flash_dfu octopus" not in calls
    assert "failed: octopus (dfu) - skipped, CAN node failed" in calls


def test_vanished_can_node_gets_reset_instructions(tmp_path: Path) -> None:
    _, out, calls = _run_cmd_flash(tmp_path)
    assert calls.count("flash_can toolhead") == 1
    assert "double-press its reset" in out
