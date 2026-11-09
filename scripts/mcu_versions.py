#!/usr/bin/env python3
"""Klipper MCU firmware versions from Moonraker, with per-MCU flash history.

Versions compare by git hash, as embedded by Klipper scripts/buildcommands.py.
State file adapted from hackra76/klipper-mcu-automatic-update-script and
fbeauKmi/update_klipper_and_mcus; Moonraker as version source from mjonuschat/aldis.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = 1
# buildcommands.py: `git describe --always --tags --long --dirty`, so a tag always
# carries -<count>-g<hash>; without tags --always gives the bare hash.
_DESCRIBE_RE = re.compile(r"^(?:v\S*?-\d+-g)?([0-9a-f]{7,40})(?=-|$)")
_LOG = logging.getLogger("mcu_versions")


def git_hash(version: str) -> str:
    """Return the git hash of a Klipper version string, or ''."""
    match = _DESCRIBE_RE.match(version or "")
    return match.group(1) if match else ""


def is_klipper_version(version: str) -> bool:
    """True for Klipper firmware versions; other devices report their own format."""
    return bool(git_hash(version))


def versions_match(running: str, source: str) -> bool:
    """True when the running firmware was built from the source tree."""
    running_hash, source_hash = git_hash(running), git_hash(source)
    if running_hash and source_hash:
        # git abbreviates to the shortest unique length, which differs per checkout.
        short, long_ = sorted((running_hash, source_hash), key=len)
        return long_.startswith(short)
    if running and source:
        return running.removesuffix("-dirty") == source.removesuffix("-dirty")
    return False


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _get(base_url: str, path: str, timeout: float) -> dict:
    url = base_url.rstrip("/") + path
    if urllib.parse.urlsplit(url).scheme not in ("http", "https"):
        raise ValueError(f"unsupported Moonraker URL: {url}")
    request = urllib.request.Request(url)
    api_key = os.environ.get("MOONRAKER_API_KEY")
    if api_key:
        request.add_header("X-Api-Key", api_key)
    # Scheme is validated above, so file:// and custom openers are unreachable.
    with urllib.request.urlopen(request, timeout=timeout) as resp:  # nosec B310
        return json.load(resp)["result"]


def query_moonraker(base_url: str, timeout: float = 5.0) -> dict:
    """Return host version, klippy state and every `mcu*` object's version and chip."""
    info = _get(base_url, "/printer/info", timeout)
    objects = _get(base_url, "/printer/objects/list", timeout)["objects"]
    sections = [o for o in objects if o == "mcu" or o.startswith("mcu ")]
    mcus: dict[str, dict] = {}
    if sections:
        query = "&".join(urllib.parse.quote(s) for s in sections)
        status = _get(base_url, f"/printer/objects/query?{query}", timeout)["status"]
        for section in sections:
            obj = status.get(section) or {}
            mcus[section] = {
                "version": obj.get("mcu_version") or "",
                "chip": (obj.get("mcu_constants") or {}).get("MCU", ""),
            }
    return {
        "host_version": info.get("software_version", ""),
        "klippy_state": info.get("state", ""),
        "mcus": mcus,
    }


def query_print_state(base_url: str, timeout: float = 5.0) -> str:
    """Return print_stats.state (standby, printing, paused, ...)."""
    status = _get(base_url, "/printer/objects/query?print_stats=state", timeout)
    return (status["status"].get("print_stats") or {}).get("state", "")


def load_state(path: Path | None) -> dict:
    """Read the state file, or an empty state when it is missing or unreadable."""
    if path is None or not path.is_file():
        return {"schema": SCHEMA, "mcus": {}}
    try:
        state = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        _LOG.warning("ignoring unreadable %s: %s", path, exc)
        return {"schema": SCHEMA, "mcus": {}}
    if not isinstance(state, dict) or not isinstance(state.get("mcus"), dict):
        _LOG.warning("ignoring malformed %s", path)
        return {"schema": SCHEMA, "mcus": {}}
    return state


def save_state(path: Path | None, state: dict) -> bool:
    """Write the state atomically; False when its directory is missing or unwritable."""
    if path is None or not path.parent.is_dir():
        return False
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
        with os.fdopen(fd, "w") as fh:
            json.dump(state, fh, indent=2, sort_keys=True)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except (OSError, TypeError, ValueError) as exc:
        _LOG.warning("could not write %s: %s", path, exc)
        if tmp is not None:
            Path(tmp).unlink(missing_ok=True)
        return False
    return True


def merge_report(state: dict, live: dict, source_version: str) -> dict:
    """Fold a live Moonraker query into the state, keeping flash history and gone MCUs."""
    target = source_version or live["host_version"]
    now = _now()
    state.update(
        schema=SCHEMA,
        updated=now,
        host_version=live["host_version"],
        source_version=target,
        klippy_state=live["klippy_state"],
    )
    for entry in state["mcus"].values():
        entry["connected"] = False
    for section, data in live["mcus"].items():
        entry = state["mcus"].setdefault(section, {})
        klipper = is_klipper_version(data["version"])
        entry.update(
            connected=True,
            chip=data["chip"],
            running_version=data["version"],
            klipper=klipper,
            needs_flash=(not versions_match(data["version"], target))
            if klipper
            else None,
            last_seen=now,
        )
    return state


def record_flash(
    state: dict, section: str, version: str, interface: str, result: str
) -> dict:
    """Store one flash attempt under the MCU's Klipper section."""
    entry = state["mcus"].setdefault(section, {})
    entry["last_flash"] = {
        "time": _now(),
        "version": version,
        "interface": interface,
        "result": result,
    }
    return state


def format_table(state: dict) -> str:
    """Human table: section, chip, running hash, status, last flash."""
    target = state.get("source_version", "")
    rows = [f"source {target or '?'}  (host {state.get('host_version') or '?'})"]
    for section in sorted(state["mcus"]):
        entry = state["mcus"][section]
        if not entry.get("connected"):
            status = "not connected"
        elif not entry.get("klipper"):
            status = "not Klipper, skipped"
        elif entry.get("needs_flash"):
            status = "NEEDS FLASH"
        else:
            status = "up to date"
        running = entry.get("running_version", "")
        flash = entry.get("last_flash") or {}
        last = f"{flash['time']} {flash['result']}" if flash else "never by this tool"
        if not entry.get("klipper"):
            last = "-"
        rows.append(
            f"  {section:<16} {entry.get('chip', ''):<14} "
            f"{git_hash(running) or running or '?':<12} {status:<22} last flash: {last}"
        )
    return "\n".join(rows) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Klipper MCU firmware versions.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("query", "state", "print-state", "report"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--url", default="http://localhost:7125")
    match = sub.add_parser("match")
    match.add_argument("running")
    match.add_argument("source")
    report = sub.choices["report"]
    report.add_argument("--source", default="")
    report.add_argument("--state-file", type=Path)
    report.add_argument("--json", action="store_true")
    report.add_argument("--quiet", action="store_true")
    record = sub.add_parser("record")
    record.add_argument("--state-file", type=Path, required=True)
    record.add_argument("--section", required=True)
    record.add_argument("--version", required=True)
    record.add_argument("--interface", required=True)
    record.add_argument("--result", choices=("ok", "failed"), required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry; report exits 2 when any Klipper MCU needs a flash."""
    logging.basicConfig(level=logging.WARNING, format="mcu_versions: %(message)s")
    args = _build_parser().parse_args(argv)
    out = sys.stdout
    if args.cmd == "match":
        return 0 if versions_match(args.running, args.source) else 1
    if args.cmd == "record":
        state = load_state(args.state_file)
        record_flash(state, args.section, args.version, args.interface, args.result)
        return 0 if save_state(args.state_file, state) else 1
    try:
        if args.cmd == "print-state":
            out.write(query_print_state(args.url) + "\n")
            return 0
        live = query_moonraker(args.url)
    except (OSError, ValueError, KeyError) as exc:
        # `state` is polled while Klippy starts, when failures are expected.
        if args.cmd != "state":
            _LOG.warning("Moonraker query failed at %s: %s", args.url, exc)
        return 1
    if args.cmd == "state":
        out.write(live["klippy_state"] + "\n")
        return 0
    if args.cmd == "query":
        for section, data in live["mcus"].items():
            out.write(f"{section}\t{data['version']}\n")
        return 0
    state = merge_report(load_state(args.state_file), live, args.source)
    if args.state_file and not args.state_file.parent.is_dir():
        _LOG.warning("state not written, %s does not exist", args.state_file.parent)
    else:
        save_state(args.state_file, state)
    if args.json:
        out.write(json.dumps(state, indent=2, sort_keys=True) + "\n")
    elif not args.quiet:
        out.write(format_table(state))
    outdated = any(
        e.get("connected") and e.get("needs_flash") for e in state["mcus"].values()
    )
    return 2 if outdated else 0


if __name__ == "__main__":
    sys.exit(main())
