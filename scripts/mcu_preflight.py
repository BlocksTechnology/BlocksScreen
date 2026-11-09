#!/usr/bin/env python3
"""Pre-flash checks that refuse a firmware image likely to leave an MCU unreachable.

image: vector table, link address and size of a built image (ARM Cortex-M layout).
pair: a Katapult build must share chip, clock, CAN pins and app address with Klipper.
comms: constants of the new klipper.dict versus the running MCU's `mcu_constants`.

Exit codes: 0 pass, 1 problems found (printed to stderr), 3 no baseline to compare.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import struct
import sys
import urllib.parse
from pathlib import Path

from mcu_versions import moonraker_get

_LOG = logging.getLogger("mcu_preflight")
_KCONFIG_RE = re.compile(r"^(CONFIG_\w+)=(.*)$")
# Resolved STM32 CAN pin choice; the MMENU/CMENU symbols are only the menu prompt.
_STM32_CAN_PINS_RE = re.compile(r"^CONFIG_STM32_CANBUS_P\w+$")
_RP2040_BASE = 0x10000000
_STM32_APP_START_RE = re.compile(r"^CONFIG_STM32_APP_START_([0-9A-Fa-f]+)$")
# Constants that decide whether the host still reaches the MCU after the flash.
COMMS_KEYS = (
    "MCU",
    "CLOCK_FREQ",
    "CANBUS_FREQUENCY",
    "CANBUS_BRIDGE",
    "SERIAL_BAUD",
    "RESERVE_PINS_CAN",
    "RESERVE_PINS_USB",
    "RESERVE_PINS_USB1",
    "RESERVE_PINS_serial",
)
# Kconfig symbols Katapult and the Klipper app it launches must agree on.
PAIR_KEYS = (
    "CONFIG_MCU",
    "CONFIG_CLOCK_REF_FREQ",
    "CONFIG_CANBUS_FREQUENCY",
    "CONFIG_RPXXXX_CANBUS_GPIO_RX",
    "CONFIG_RPXXXX_CANBUS_GPIO_TX",
)


def read_kconfig(path: Path) -> dict[str, str]:
    """Parse `CONFIG_X=value` lines; string values lose their quotes."""
    cfg: dict[str, str] = {}
    for line in path.read_text().splitlines():
        match = _KCONFIG_RE.match(line.strip())
        if match:
            cfg[match.group(1)] = match.group(2).strip('"')
    return cfg


def _addr(cfg: dict[str, str], key: str) -> int | None:
    try:
        return int(cfg[key], 0)
    except (KeyError, ValueError):
        return None


def image_problems(
    cfg: dict[str, str],
    image: bytes,
    write_addr: int | None = None,
    bootloader: bool = False,
) -> list[str]:
    """Problems with an image for `cfg`; `bootloader` means Katapult's own image."""
    if not image:
        return ["image is empty"]
    rp2040 = cfg.get("CONFIG_MACH_RPXXXX") == "y"
    if not rp2040 and cfg.get("CONFIG_MACH_STM32") != "y":
        return []  # vector layout only known for Cortex-M targets
    # rp2040 builds a raw .bin only above a bootloader (klipper src/rp2040/Makefile).
    if rp2040 and (bootloader or cfg.get("CONFIG_RPXXXX_HAVE_BOOTLOADER") != "y"):
        return []
    load = _addr(
        cfg,
        "CONFIG_FLASH_BOOT_ADDRESS"
        if bootloader
        else "CONFIG_FLASH_APPLICATION_ADDRESS",
    )
    ram_start = _addr(cfg, "CONFIG_RAM_START")
    ram_size = _addr(cfg, "CONFIG_RAM_SIZE")
    flash_size = _addr(cfg, "CONFIG_FLASH_SIZE")
    if load is None or ram_start is None or ram_size is None:
        return ["config lacks FLASH/RAM addresses, cannot check the image"]
    problems = []
    if write_addr is not None and write_addr != load:
        problems.append(
            f"image linked for 0x{load:x} but would be written at 0x{write_addr:x}"
        )
    if len(image) < 8:
        return problems + [f"image is {len(image)} bytes, too short for a vector table"]
    stack, reset = struct.unpack_from("<II", image)
    if not ram_start < stack <= ram_start + ram_size:
        problems.append(
            f"initial stack 0x{stack:08x} outside RAM 0x{ram_start:x}+0x{ram_size:x}"
        )
    if not reset & 1:
        problems.append(f"reset vector 0x{reset:08x} is not a Thumb address")
    if not load <= (reset & ~1) < load + len(image):
        problems.append(f"reset vector 0x{reset:08x} points outside the image")
    base = _RP2040_BASE if rp2040 else _addr(cfg, "CONFIG_FLASH_BOOT_ADDRESS")
    if flash_size and base is not None and load + len(image) > base + flash_size:
        problems.append(f"image ends past flash (0x{load + len(image):x})")
    return problems


def _launch_addr(katapult: dict[str, str]) -> int | None:
    # Unresolved stm32 configs carry only the choice; map it as katapult src/stm32/Kconfig.
    launch = _addr(katapult, "CONFIG_LAUNCH_APP_ADDRESS")
    if launch is None and katapult.get("CONFIG_MACH_STM32") == "y":
        for key, value in katapult.items():
            match = _STM32_APP_START_RE.match(key)
            if match and value == "y":
                return 0x8000000 + int(match.group(1), 16)
    return launch


def pair_problems(klipper: dict[str, str], katapult: dict[str, str]) -> list[str]:
    """Mismatches that make Katapult unreachable or unable to launch the app."""
    problems = [
        f"{key}: Klipper {klipper[key]!r}, Katapult {katapult[key]!r}"
        for key in PAIR_KEYS
        if key in klipper and key in katapult and klipper[key] != katapult[key]
    ]
    pins = [
        {k for k, v in cfg.items() if v == "y" and _STM32_CAN_PINS_RE.match(k)}
        for cfg in (klipper, katapult)
    ]
    if all(pins) and pins[0] != pins[1]:
        problems.append(
            f"CAN pins: Klipper {sorted(pins[0])}, Katapult {sorted(pins[1])}"
        )
    app = _addr(klipper, "CONFIG_FLASH_APPLICATION_ADDRESS")
    launch = _launch_addr(katapult)
    if app is not None and launch is not None and app != launch:
        problems.append(
            f"app address: Klipper 0x{app:x}, Katapult launches 0x{launch:x}"
        )
    return problems


def comms_problems(new: dict, running: dict) -> list[str]:
    """Comms constants that differ between the running MCU and the new build."""
    return [
        f"{key}: running {running.get(key)!r}, new build {new.get(key)!r}"
        for key in COMMS_KEYS
        if str(running.get(key)) != str(new.get(key))
    ]


def running_constants(base_url: str, section: str, timeout: float = 5.0) -> dict:
    """`mcu_constants` of a Klipper MCU section, empty when it never connected."""
    query = f"{urllib.parse.quote(section)}=mcu_constants"
    status = moonraker_get(base_url, f"/printer/objects/query?{query}", timeout)
    return (status["status"].get(section) or {}).get("mcu_constants") or {}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pre-flash firmware checks.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    image = sub.add_parser("image")
    image.add_argument("--config", type=Path, required=True)
    image.add_argument("--image", type=Path, required=True)
    image.add_argument("--at", type=lambda v: int(v, 0))
    image.add_argument("--bootloader", action="store_true")
    pair = sub.add_parser("pair")
    pair.add_argument("--klipper", type=Path, required=True)
    pair.add_argument("--katapult", type=Path, required=True)
    comms = sub.add_parser("comms")
    comms.add_argument("--dict", type=Path, required=True)
    comms.add_argument("--section", required=True)
    comms.add_argument("--url", default="http://localhost:7125")
    return parser


def _run(args: argparse.Namespace) -> list[str] | None:
    if args.cmd == "image":
        return image_problems(
            read_kconfig(args.config), args.image.read_bytes(), args.at, args.bootloader
        )
    if args.cmd == "pair":
        return pair_problems(read_kconfig(args.klipper), read_kconfig(args.katapult))
    try:
        running = running_constants(args.url, args.section)
    except (OSError, ValueError, KeyError) as exc:
        _LOG.warning("no running baseline for [%s]: %s", args.section, exc)
        return None
    if not running:
        _LOG.warning("no running baseline for [%s]: never connected", args.section)
        return None
    return comms_problems(json.loads(args.dict.read_text()).get("config", {}), running)


def main(argv: list[str] | None = None) -> int:
    """CLI entry; see the module docstring for exit codes."""
    logging.basicConfig(level=logging.WARNING, format="mcu_preflight: %(message)s")
    args = _build_parser().parse_args(argv)
    try:
        problems = _run(args)
    except (OSError, ValueError) as exc:
        _LOG.error("%s", exc)
        return 1
    if problems is None:
        return 3
    for problem in problems:
        _LOG.error("%s", problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
