#!/usr/bin/env python3
"""Pre-flash checks that refuse a firmware image likely to leave an MCU unreachable.

image: vector table, link address and size of a built image (ARM Cortex-M layout).
pair: a Katapult build must share chip, clock, CAN pins and app address with Klipper.
comms: constants of the new klipper.dict versus the running MCU's `mcu_constants`.
flashed: clock Kconfig of the new build versus the last successfully flashed one.
combine-bin / combine-uf2: Katapult plus app as one ROM bootloader image; uf2 prints pages.

Exit codes: 0 pass, 1 problems found (printed to stderr), 3 the MCU never connected
(no baseline), 4 the check itself could not run, 5 Moonraker gave no answer to compare.
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
_RP2040_SECTOR = 0x1000
_UF2_BLOCK = 512
_UF2_PAGE = 256
_UF2_MAGIC = (0x0A324655, 0x9E5D5157, 0x0AB16F30)
_UF2_NOT_MAIN_FLASH = 0x1
_UF2_FAMILY_PRESENT = 0x2000
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
    "RESERVE_PINS_crystal",
)
# Not exported as MCU constants, so the last flashed .config is the only baseline.
FLASHED_KEYS = (
    "CONFIG_MCU",
    "CONFIG_CLOCK_REF_FREQ",
    "CONFIG_STM32_CLOCK_REF_INTERNAL",
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


def combine_bin(katapult: bytes, app: bytes, boot_addr: int, app_addr: int) -> bytes:
    """Katapult and app as one image written at `boot_addr`, 0xFF (erased) between."""
    gap = app_addr - boot_addr
    if gap <= 0:
        raise ValueError(f"app 0x{app_addr:x} is not above Katapult 0x{boot_addr:x}")
    if len(katapult) > gap:
        raise ValueError(f"Katapult is {len(katapult)} bytes, overlaps the app")
    return katapult + b"\xff" * (gap - len(katapult)) + app


def _uf2_blocks(data: bytes) -> list[bytearray]:
    if not data or len(data) % _UF2_BLOCK:
        raise ValueError(f"UF2 size {len(data)} is not a multiple of {_UF2_BLOCK}")
    blocks = []
    for off in range(0, len(data), _UF2_BLOCK):
        block = bytearray(data[off : off + _UF2_BLOCK])
        start0, start1 = struct.unpack_from("<II", block)
        (end,) = struct.unpack_from("<I", block, _UF2_BLOCK - 4)
        if (start0, start1, end) != _UF2_MAGIC:
            raise ValueError(f"UF2 block {off // _UF2_BLOCK} has bad magic")
        blocks.append(block)
    return blocks


def combine_uf2(katapult_uf2: bytes, app: bytes, app_addr: int) -> tuple[bytes, int]:
    """Katapult UF2 plus the app as UF2 pages at `app_addr`; returns (image, pages).

    Block renumbering follows Katapult scripts/uf2_append_boot_signature.py `renumerate`.
    """
    if app_addr % _RP2040_SECTOR:
        raise ValueError(f"app 0x{app_addr:x} is not 4 KiB sector aligned")
    if not app:
        raise ValueError("app image is empty")
    blocks = _uf2_blocks(katapult_uf2)
    flags, _, _, _, _, family = struct.unpack_from("<IIIIII", blocks[0], 8)
    for block in blocks:
        bflags, target, size, _, _, bfamily = struct.unpack_from("<IIIIII", block, 8)
        # rp2040_flash skips any other block, so the expected page count would lie.
        if (
            (bflags, bfamily, size) != (flags, family, _UF2_PAGE)
            or not (flags & _UF2_FAMILY_PRESENT)
            or flags & _UF2_NOT_MAIN_FLASH
        ):
            raise ValueError(f"Katapult block at 0x{target:x} is not a main flash page")
        if target + size > app_addr:
            raise ValueError(f"Katapult page 0x{target:x} overlaps the app")
    for off in range(0, len(app), _UF2_PAGE):
        page = app[off : off + _UF2_PAGE].ljust(_UF2_PAGE, b"\xff")
        block = bytearray(_UF2_BLOCK)
        struct.pack_into(
            "<IIIIIIII",
            block,
            0,
            _UF2_MAGIC[0],
            _UF2_MAGIC[1],
            flags,
            app_addr + off,
            _UF2_PAGE,
            0,
            0,
            family,
        )
        block[32 : 32 + _UF2_PAGE] = page
        struct.pack_into("<I", block, _UF2_BLOCK - 4, _UF2_MAGIC[2])
        blocks.append(block)
    for number, block in enumerate(blocks):
        struct.pack_into("<II", block, 20, number, len(blocks))
    return b"".join(blocks), len(blocks)


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


def _shown(value: object) -> str:
    return "absent" if value is None else repr(value)


def comms_problems(new: dict, running: dict) -> list[str]:
    """Comms constants that differ between the running MCU and the new build."""
    # Presence is the setting: Klipper emits RESERVE_PINS_* per choice (9bc3a29e).
    return [
        f"{key}: running {_shown(running.get(key))}, new build {_shown(new.get(key))}"
        for key in COMMS_KEYS
        if str(running.get(key)) != str(new.get(key))
    ]


def flashed_problems(new: dict[str, str], flashed: dict[str, str]) -> list[str]:
    """Clock Kconfig symbols that differ between the last flashed build and the new one."""
    return [
        f"{key}: last flash {flashed.get(key)!r}, new build {new.get(key)!r}"
        for key in FLASHED_KEYS
        if flashed.get(key) != new.get(key)
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
    flashed = sub.add_parser("flashed")
    flashed.add_argument("--new", type=Path, required=True)
    flashed.add_argument("--flashed", type=Path, required=True)
    comms = sub.add_parser("comms")
    comms.add_argument("--dict", type=Path, required=True)
    comms.add_argument("--section", required=True)
    comms.add_argument("--url", default="http://localhost:7125")
    for name in ("combine-bin", "combine-uf2"):
        combine = sub.add_parser(name)
        combine.add_argument("--katapult", type=Path, required=True)
        combine.add_argument("--app", type=Path, required=True)
        combine.add_argument("--app-addr", type=lambda v: int(v, 0), required=True)
        combine.add_argument("--out", type=Path, required=True)
        if name == "combine-bin":
            combine.add_argument("--boot-addr", type=lambda v: int(v, 0), required=True)
    return parser


def _combine(args: argparse.Namespace) -> list[str]:
    katapult, app = args.katapult.read_bytes(), args.app.read_bytes()
    try:
        if args.cmd == "combine-bin":
            image = combine_bin(katapult, app, args.boot_addr, args.app_addr)
        else:
            image, pages = combine_uf2(katapult, app, args.app_addr)
    except ValueError as exc:
        return [str(exc)]
    args.out.write_bytes(image)
    if args.cmd == "combine-uf2":
        sys.stdout.write(f"{pages}\n")
    return []


class NoBaselineError(Exception):
    """Moonraker did not answer, so the running constants are unknown."""


def _run(args: argparse.Namespace) -> list[str] | None:
    if args.cmd.startswith("combine-"):
        return _combine(args)
    if args.cmd == "image":
        return image_problems(
            read_kconfig(args.config), args.image.read_bytes(), args.at, args.bootloader
        )
    if args.cmd == "pair":
        return pair_problems(read_kconfig(args.klipper), read_kconfig(args.katapult))
    if args.cmd == "flashed":
        return flashed_problems(read_kconfig(args.new), read_kconfig(args.flashed))
    try:
        running = running_constants(args.url, args.section)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        msg = f"Moonraker gave no constants for [{args.section}]: {exc}"
        raise NoBaselineError(msg) from exc
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
    except NoBaselineError as exc:
        _LOG.error("%s", exc)
        return 5
    # Any crash must stay 4: exit 1 is a comms change, which --allow-comms-change passes.
    except Exception as exc:  # pylint: disable=broad-exception-caught
        _LOG.error("check failed: %r", exc)
        return 4
    if problems is None:
        return 3
    for problem in problems:
        _LOG.error("%s", problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
