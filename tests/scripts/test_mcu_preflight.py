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
    assert problems == ["CANBUS_BRIDGE: running 1, new build absent"]


def test_comms_catches_crystal_to_internal_clock() -> None:
    running = {"MCU": "stm32h723xx", "RESERVE_PINS_crystal": "PH0,PH1"}
    problems = pf.comms_problems({"MCU": "stm32h723xx"}, running)
    assert problems == ["RESERVE_PINS_crystal: running 'PH0,PH1', new build absent"]


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


def test_a_crash_in_a_check_is_never_a_comms_change(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _crash(*_args: object) -> list[str]:
        raise AttributeError("boom")

    monkeypatch.setattr(pf, "comms_problems", _crash)
    dict_file = tmp_path / "klipper.dict"
    dict_file.write_text("{}")
    monkeypatch.setattr(pf, "running_constants", lambda *_a: {"MCU": "x"})
    assert pf.main(["comms", "--dict", str(dict_file), "--section", "mcu"]) == 4


def test_unreachable_moonraker_is_not_a_missing_baseline(tmp_path: Path) -> None:
    dict_file = tmp_path / "klipper.dict"
    dict_file.write_text("{}")
    argv = ["comms", "--dict", str(dict_file), "--section", "mcu"]
    assert pf.main(argv + ["--url", "http://127.0.0.1:9"]) == 5


@pytest.mark.parametrize(
    ("new_bitrate", "bridge", "rc"),
    [("1000000", 1, 0), ("500000", 1, 1), ("500000", None, 0)],
)
def test_bridge_bitrate_must_match_its_can_nodes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    new_bitrate: str,
    bridge: int | None,
    rc: int,
) -> None:
    # The bridge exports no CANBUS_FREQUENCY: T1 on .151 passed a 1M -> 500k bridge build.
    running = {"MCU": "stm32h723xx", "CANBUS_BRIDGE": bridge}
    monkeypatch.setattr(pf, "running_constants", lambda *_a: running)
    monkeypatch.setattr(pf, "can_node_bitrates", lambda *_a: {"mcu Toolhead": 1000000})
    dict_file = tmp_path / "klipper.dict"
    dict_file.write_text(json.dumps({"config": running}))
    config = tmp_path / ".config"
    config.write_text(f"CONFIG_CANBUS_FREQUENCY={new_bitrate}\n")
    argv = ["comms", "--dict", str(dict_file), "--section", "mcu"]
    assert pf.main(argv + ["--config", str(config)]) == rc


def test_failed_can_node_query_names_the_nodes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    def _fail(*_args: object) -> dict:
        raise OSError("timed out")

    running = {"MCU": "stm32h723xx", "CANBUS_BRIDGE": 1}
    monkeypatch.setattr(pf, "running_constants", lambda *_a: running)
    monkeypatch.setattr(pf, "can_node_bitrates", _fail)
    dict_file = tmp_path / "klipper.dict"
    dict_file.write_text(json.dumps({"config": running}))
    config = tmp_path / ".config"
    config.write_text("CONFIG_CANBUS_FREQUENCY=1000000\n")
    argv = ["comms", "--dict", str(dict_file), "--section", "mcu"]
    assert pf.main(argv + ["--config", str(config)]) == 5
    assert "CAN nodes behind [mcu]" in caplog.text


def test_bridge_bitrate_problem_names_the_node() -> None:
    nodes = {"mcu Toolhead": 1000000, "mcu eddy": 500000}
    assert pf.bridge_bitrate_problems("500000", nodes) == [
        "CANBUS_FREQUENCY: [mcu Toolhead] runs 1000000, new bridge build 500000"
    ]


def test_combine_bin_pads_katapult_up_to_the_app() -> None:
    image = pf.combine_bin(b"K" * 10, b"APP", 0x8000000, 0x8000010)
    assert image == b"K" * 10 + b"\xff" * 6 + b"APP"
    with pytest.raises(ValueError, match="overlaps"):
        pf.combine_bin(b"K" * 17, b"APP", 0x8000000, 0x8000010)
    with pytest.raises(ValueError, match="not above"):
        pf.combine_bin(b"K", b"APP", 0x8000000, 0x8000000)


def _uf2_block(target: int, flags: int = 0x2000, family: int = 0xE48BFF56) -> bytes:
    head = struct.pack(
        "<IIIIIIII", 0x0A324655, 0x9E5D5157, flags, target, 256, 7, 9, family
    )
    return head + bytes(476) + struct.pack("<I", 0x0AB16F30)


def test_combine_uf2_appends_app_pages_and_renumbers() -> None:
    katapult = _uf2_block(0x10000000) + _uf2_block(0x10000100)
    image, pages = pf.combine_uf2(katapult, b"\x01" * 300, 0x10004000)
    assert pages == 4 and len(image) == 4 * 512
    for number in range(4):
        block = image[number * 512 : (number + 1) * 512]
        flags, _, size, no, total, family = struct.unpack_from("<IIIIII", block, 8)
        assert (flags, size, no, total, family) == (0x2000, 256, number, 4, 0xE48BFF56)
        assert struct.unpack_from("<I", block, 508) == (0x0AB16F30,)
    assert struct.unpack_from("<I", image, 3 * 512 + 12) == (0x10004100,)
    tail = image[3 * 512 + 32 : 3 * 512 + 32 + 256]
    assert tail == b"\x01" * 44 + b"\xff" * 212


@pytest.mark.parametrize(
    ("katapult", "app_addr", "match"),
    [
        (_uf2_block(0x10003F00), 0x10003F00, "aligned"),
        (_uf2_block(0x10004000), 0x10004000, "overlaps"),
        (_uf2_block(0x10000000)[:-1], 0x10004000, "multiple"),
        (b"\x00" * 512, 0x10004000, "magic"),
        (_uf2_block(0x10000000) + _uf2_block(0x10000100, family=1), 0x10004000, "main"),
        (_uf2_block(0x10000000, flags=0x2001), 0x10004000, "main"),
    ],
)
def test_combine_uf2_refuses_unsafe_input(
    katapult: bytes, app_addr: int, match: str
) -> None:
    with pytest.raises(ValueError, match=match):
        pf.combine_uf2(katapult, b"\x01", app_addr)


def test_combine_cli_prints_pages_and_refuses_overlap(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "k.uf2").write_bytes(_uf2_block(0x10000000))
    (tmp_path / "k.bin").write_bytes(b"K" * 0x3000)
    (tmp_path / "app.bin").write_bytes(b"\x01" * 512)
    out = tmp_path / "out"
    common = ["--app", str(tmp_path / "app.bin"), "--out", str(out)]
    uf2 = ["combine-uf2", "--katapult", str(tmp_path / "k.uf2"), "--app-addr"]
    assert pf.main(uf2 + ["0x10004000"] + common) == 0
    assert capsys.readouterr().out == "3\n" and out.stat().st_size == 3 * 512
    out.unlink()
    binary = ["combine-bin", "--katapult", str(tmp_path / "k.bin"), "--boot-addr"]
    assert pf.main(binary + ["0x8000000", "--app-addr", "0x8002000"] + common) == 1
    assert not out.exists()


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
    assert rc == 4
    assert sum(c.endswith("--list") for c in calls) == 2


def test_dfu_unlistable_after_verified_leave_is_ok(tmp_path: Path) -> None:
    rc, calls = _run_flash_dfu(tmp_path, LIST="fail")
    assert rc == 0
    assert not list(tmp_path.glob("*.dfu-list.txt"))


def test_dfu_unlistable_without_readback_is_unverified(tmp_path: Path) -> None:
    rc, calls = _run_flash_dfu(tmp_path, LIST="fail", READBACK="fail")
    assert rc == 3
    assert _targets(calls)[-1] == "0x08000000:leave"


def test_dfu_list_error_after_a_failed_write_still_retries(tmp_path: Path) -> None:
    rc, calls = _run_flash_dfu(tmp_path, LIST="fail", WRITE="fail")
    assert rc == 4
    assert sum(" -D " in c for c in calls) == 2


@pytest.mark.parametrize("env", [{"READBACK": "fail"}, {"WRITE": "fail"}])
def test_dfu_board_gone_from_usb_is_a_failure(tmp_path: Path, env: dict) -> None:
    rc, calls = _run_flash_dfu(tmp_path, GONE="1", **env)
    assert rc == 1
    assert sum(" -D " in c for c in calls) == 1  # no rewrite to an absent board
    assert not any(":leave" in c for c in calls)


@pytest.mark.parametrize("env", [{"READBACK": "bad"}, {"WRITE": "fail"}])
def test_dfu_never_leaves_after_a_bad_write(tmp_path: Path, env: dict) -> None:
    rc, calls = _run_flash_dfu(tmp_path, **env)
    assert rc == 4
    assert sum(" -D " in c for c in calls) == 2  # one rewrite while still in DFU
    assert not any(":leave" in c for c in calls)


# cmd_flash with every hardware step stubbed; sudo calls, flashes and results go to $LOG.
# RUNNING="th=v1 mcu=v1" is what Klipper reports per section after the flash.
_FLASH_STUBS = r"""
sudo() { echo "sudo $*" >>"$LOG"; }
build_firmware() { return 0; }
use_build() { :; }
preflight_firmware() { [[ " ${BAD:-} " != *" $1 "* ]]; }
flash_can() { echo "flash_can $1" >>"$LOG"; [ -n "${CAN_OK:-}" ]; }
flash_dfu() { echo "flash_dfu $1" >>"$LOG"; echo "dfu_write $5 ${6##*/}" >>"$LOG"; return "${DFU_RC:-0}"; }
build_katapult_firmware() { :; }
MCU_CONFIG_DIR=${MCU_DIR:-$MCU_CONFIG_DIR}
probe_can_mcu() { [[ " ${IN_KATAPULT:-} " == *" $1 "* ]] && echo "stm32g0b1|" || echo "|"; }
_summary_box() {
    printf 'failed: %s\n' "${failed[@]}" >>"$LOG"
    printf 'flashed: %s\n' "${flashed[@]}" >>"$LOG"
}
save_uuid_cache() { :; }
record_flash() { echo "record_flash $3" >>"$LOG"; }
check_host_power() { [ -z "${UNDERVOLT:-}" ]; }
hold_klipper() { :; }
release_klipper() { :; }
ensure_can_up() { :; }
sleep() { :; }
python3() { :; }
config_meta() { [[ "$1" == *th.cfg ]] && echo th || echo mcu; }
versions_match() { [ -n "$1" ] && [ "$1" = "$2" ]; }
query_moonraker_versions() {
    local kv
    for kv in ${RUNNING:-}; do MOONRAKER_VERSIONS["${kv%=*}"]="${kv#*=}"; done
}
verify_klipper_ready() { [ -n "${READY:-}" ]; }
write_versions_file() { :; }
CONTEXT=${CTX:-local} FORCE=${FORCE_FLAG:-true} FLASH_ORDER_LOCKED=false SRC_VERSION=v1
FLASH_NAMES=(${NAMES:-})
ALLOW_UNDERVOLTAGE=${ALLOW_UV:-false}
DISCOVERED=("toolhead|can|aaa|$TH_CFG|${VER:-}|${TH_FOUND:-true}" "octopus|dfu|${DFU_ID-SER}|$BRIDGE_CFG|${VER:-}|true")
"""


def _run_cmd_flash(tmp_path: Path, **env: str) -> tuple[int, str, list[str]]:
    (tmp_path / "th.cfg").write_text("CONFIG_CANBUS=y\n")
    (tmp_path / "bridge.cfg").write_text("CONFIG_USBCANBUS=y\n")
    for name in ("toolhead", "octopus"):
        (tmp_path / name).mkdir(exist_ok=True)
        if not (tmp_path / name / ".config").exists():
            (tmp_path / name / ".config").write_text("CONFIG_X=y\n")
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
    assert not any(c.startswith("record_flash") for c in calls)  # nothing was written


def test_one_failed_preflight_flashes_nothing(tmp_path: Path) -> None:
    rc, _, calls = _run_cmd_flash(tmp_path, BAD="toolhead")
    assert rc == 1
    assert not any("systemctl stop" in c or c.startswith("flash_") for c in calls)
    assert (
        "failed: octopus (dfu) - not flashed, another board failed its checks" in calls
    )


@pytest.mark.parametrize("allow", ["false", "true"])
def test_undervoltage_needs_its_own_flag(tmp_path: Path, allow: str) -> None:
    rc, _, calls = _run_cmd_flash(tmp_path, UNDERVOLT="1", ALLOW_UV=allow, CAN_OK="1")
    flashed = any(c.startswith("flash_") for c in calls)
    assert flashed == (allow == "true")
    assert rc == (0 if allow == "true" else 1)


def test_flash_counts_once_klipper_runs_the_new_version(tmp_path: Path) -> None:
    rc, _, calls = _run_cmd_flash(
        tmp_path, CTX="pi", CAN_OK="1", READY="1", RUNNING="th=v1 mcu=v1"
    )
    assert rc == 0
    assert calls.count("record_flash ok") == 2
    assert (tmp_path / "toolhead.flashed.config").exists()


def test_old_version_after_the_flash_is_a_failure(tmp_path: Path) -> None:
    rc, _, calls = _run_cmd_flash(
        tmp_path, CTX="pi", CAN_OK="1", READY="1", RUNNING="th=v0 mcu=v1"
    )
    assert rc == 1
    assert "failed: toolhead (can) - still runs the old version" in calls
    assert not (tmp_path / "toolhead.flashed.config").exists()


def test_verified_write_with_silent_klipper_still_counts(tmp_path: Path) -> None:
    rc, _, calls = _run_cmd_flash(tmp_path, CTX="pi", CAN_OK="1", RUNNING="th=v1")
    assert rc == 0
    assert "flashed: octopus (dfu) - running version unconfirmed" in calls


def test_unverified_write_with_silent_klipper_needs_a_person(tmp_path: Path) -> None:
    rc, out, calls = _run_cmd_flash(
        tmp_path, CTX="pi", CAN_OK="1", DFU_RC="3", RUNNING="th=v1"
    )
    assert rc == 4
    assert "failed: octopus (dfu) - unconfirmed" in calls
    assert "Needs someone at the printer: [octopus]" in out


def test_board_left_in_dfu_needs_the_24v_cut(tmp_path: Path) -> None:
    rc, out, _ = _run_cmd_flash(tmp_path, CAN_OK="1", DFU_RC="4")
    assert rc == 4
    assert "switch the printer's 24 V supply off" in out
    assert out.rindex("fit the BOOT0 jumper") > out.rindex("Needs someone")


def test_failed_write_with_klipper_ready_needs_no_person(tmp_path: Path) -> None:
    rc, _, _ = _run_cmd_flash(tmp_path, CTX="pi", READY="1", RUNNING="th=v0 mcu=v0")
    assert rc == 1


def test_failed_can_node_retries_in_katapult_and_skips_bridge(tmp_path: Path) -> None:
    rc, _, calls = _run_cmd_flash(tmp_path, IN_KATAPULT="aaa")
    assert rc == 4
    assert calls.count("flash_can toolhead") == 2
    assert "flash_dfu octopus" not in calls
    assert "failed: octopus (dfu) - skipped, CAN node failed" in calls
    assert (
        calls.count("record_flash failed") == 1
    )  # the toolhead only, never written bridge


@pytest.mark.parametrize(
    ("names", "found", "rc"),
    [("toolhead", "false", 1), ("nosuch", "true", 1), ("", "false", 0)],
    ids=["named undetected", "unknown name", "flash-all skips undetected"],
)
def test_named_board_not_found_fails_the_run(
    tmp_path: Path, names: str, found: str, rc: int
) -> None:
    got, _, calls = _run_cmd_flash(
        tmp_path, NAMES=names, TH_FOUND=found, VER="v1", FORCE_FLAG="false", DFU_ID=""
    )
    assert got == rc
    assert not any(c.startswith("flash_") for c in calls)


@pytest.mark.parametrize("katapult", [True, False])
def test_dfu_board_behind_katapult_gets_katapult_and_app(
    tmp_path: Path, katapult: bool
) -> None:
    (tmp_path / "mcu").mkdir()
    if katapult:
        (tmp_path / "mcu" / "octopus.katapult.config").write_text("X=y\n")
    (tmp_path / "octopus.katapult").mkdir()
    (tmp_path / "octopus.katapult" / ".config").write_text(
        "CONFIG_FLASH_BOOT_ADDRESS=0x8000000\n"
    )
    app_cfg = tmp_path / "octopus" / ".config"
    app_cfg.parent.mkdir()
    app_cfg.write_text(
        "CONFIG_FLASH_BOOT_ADDRESS=0x8000000\nCONFIG_FLASH_APPLICATION_ADDRESS=0x8002000\n"
    )
    rc, _, calls = _run_cmd_flash(tmp_path, CAN_OK="1", MCU_DIR=str(tmp_path / "mcu"))
    if katapult:
        assert rc == 0 and "dfu_write 0x8000000 klipper.full.bin" in calls
    else:
        assert rc == 1 and not any(c.startswith("flash_") for c in calls)


@pytest.mark.parametrize(("dfu_id", "flashed"), [("SER", True), ("", False)])
def test_board_present_in_rom_dfu_is_never_version_skipped(
    tmp_path: Path, dfu_id: str, flashed: bool
) -> None:
    _, _, calls = _run_cmd_flash(tmp_path, FORCE_FLAG="false", VER="v1", DFU_ID=dfu_id)
    assert "flash_can toolhead" not in calls
    assert ("flash_dfu octopus" in calls) == flashed


def test_vanished_can_node_gets_reset_instructions(tmp_path: Path) -> None:
    _, out, calls = _run_cmd_flash(tmp_path)
    assert calls.count("flash_can toolhead") == 1
    assert "double-press its reset" in out


def _run_snippet(body: str, **env: str) -> subprocess.CompletedProcess:
    script = f'. "{_SCRIPTS / "flash_mcus.sh"}"\n{body}'
    return subprocess.run(
        ["bash", "-c", script],
        capture_output=True,
        text=True,
        timeout=30,
        env={"PATH": "/usr/bin:/bin", **env},
    )


def test_flash_can_reports_a_failed_flashtool(tmp_path: Path) -> None:
    tool = tmp_path / "flashtool.py"
    tool.write_text("import sys\nprint('Flash Failed')\nsys.exit(1)\n")
    res = _run_snippet(
        'KATAPULT_SCRIPT="$TOOL"; flash_can toolhead aaa; echo "rc=$?"',
        HOME=str(tmp_path),
        TOOL=str(tool),
    )
    assert "rc=1" in res.stdout


def test_bootloader_uuids_lists_katapult_nodes_only(tmp_path: Path) -> None:
    tool = tmp_path / "flashtool.py"
    tool.write_text(
        "print('Detected UUID: aaa, Application: Katapult')\n"
        "print('Detected UUID: bbb, Application: Klipper')\n"
    )
    res = _run_snippet(
        'KATAPULT_SCRIPT="$TOOL"; KATAPULT_OK=true; bootloader_uuids',
        HOME=str(tmp_path),
        TOOL=str(tool),
    )
    assert res.stdout.split() == ["aaa"]


_DISCOVER_STUBS = """
CONTEXT=pi KATAPULT_OK=true SRC_VERSION=v1 MCU_CONFIG_DIR="$CFG"
ensure_klipper_running() { :; }; query_moonraker_versions() { return 1; }
scan_dfu_devices() { :; }; ensure_can_up() { :; }; find_dfu_device() { :; }
bootloader_uuids() { [ "$STATE" = katapult ] && echo aaa; }
probe_can_mcu() { echo "stm32g0b1xx|"; }
klipper_can_query() { [ "$STATE" = klipper ] && echo "aaa|Klipper"; }
UUID_CACHE_MAP=([stm32g0b1]=aaa)
discover >/dev/null 2>&1; printf '%s\\n' "${DISCOVERED[@]}"
"""


@pytest.mark.parametrize("state", ["katapult", "klipper"])
def test_can_node_is_matched_in_katapult_and_in_klipper(
    tmp_path: Path, state: str
) -> None:
    # Katapult names the chip stm32g0b1xx: a node left there by a failed flash must still match.
    (tmp_path / "ebb.config").write_text(
        "# mcu_type: stm32g0b1\n# klipper_section: mcu Toolhead\n# katapult_dfu: 0483:df11\n"
    )
    res = _run_snippet(_DISCOVER_STUBS, CFG=str(tmp_path), STATE=state)
    assert res.stdout.startswith("ebb|can|aaa|"), res.stdout + res.stderr


# Prints what Klipper's lib/rp2040_flash/main.c prints, per $MODE; exits 0 like it does.
_RP2040_TOOL = """#!/bin/bash
echo "Loaded UF2 image with ${PAGES:-2} pages" >&2
[ "${MODE:-}" = absent ] && { echo "No rp2040 in BOOTSEL mode was found" >&2; exit 0; }
echo "Flashing..." >&2
[ "${MODE:-}" = noreboot ] || echo "Rebooting device" >&2
exit 0
"""


@pytest.mark.parametrize(
    ("env", "ok"),
    [
        ({}, True),
        ({"WANT": "5", "PAGES": "5"}, True),
        ({"PAGES": "0"}, False),
        ({"MODE": "absent"}, False),
        ({"MODE": "noreboot"}, False),
        ({"DEVICES": "2"}, False),
    ],
)
def test_bootsel_needs_every_page_and_the_reboot(
    tmp_path: Path, env: dict, ok: bool
) -> None:
    tool = tmp_path / "klipper" / "lib" / "rp2040_flash" / "rp2040_flash"
    tool.parent.mkdir(parents=True)
    tool.write_text(_RP2040_TOOL)
    tool.chmod(0o755)
    uf2 = tmp_path / "klipper.uf2"
    uf2.write_bytes(bytes(1024))
    res = _run_snippet(
        'sudo() { "$@"; }\n'
        'lsusb() { local i; for ((i = 0; i < ${DEVICES:-1}; i++)); do echo "ID $2"; done; }\n'
        'flash_bootsel eddy 2e8a:0003 "$UF2" "${WANT:-}"; echo "rc=$?"',
        HOME=str(tmp_path),
        UF2=str(uf2),
        **env,
    )
    assert ("rc=0" in res.stdout) == ok
    if "DEVICES" in env:
        assert "Loaded UF2" not in res.stdout + res.stderr
