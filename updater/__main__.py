import argparse
import asyncio
import contextlib
import logging
import os
import signal
import socket
import sys
from collections.abc import Iterator

from updater.locking import code_hash, code_hash_path, process_lock
from updater.models import ComponentStatus
from updater.service import LoggingCallback, UpdateService


def _sd_notify(msg: str) -> None:
    """Send a notification to systemd via NOTIFY_SOCKET (python-sdbus has no sd_notify)."""
    sock_path = os.environ.get("NOTIFY_SOCKET", "")
    if not sock_path:
        return
    if sock_path.startswith("@"):
        sock_path = "\0" + sock_path[1:]
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as s:
            s.sendto(msg.encode(), sock_path)
    except OSError as exc:
        logging.getLogger("updater").warning("sd_notify(%s) failed: %s", msg, exc)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser with update, status, and recover subcommands."""
    parser = argparse.ArgumentParser(prog="python -m updater")
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command")
    upd = sub.add_parser("update")
    upd.add_argument("name", nargs="?", default=None)

    sub.add_parser("status")

    sub.add_parser("daemon")

    rec = sub.add_parser("recover")
    rec.add_argument("name")
    rec.add_argument("--hard", action="store_true")

    bles = sub.add_parser("bless")
    bles.add_argument("name")
    bles.add_argument("hash", nargs="?", default="")

    return parser


def _record_code_hash() -> None:
    """Record the loaded code so bs-bootstrap can restart a daemon a Moonraker pull left stale."""
    path = code_hash_path()
    tmp = path.with_name(path.name + ".new")
    try:
        tmp.write_text(code_hash() + "\n")
        tmp.replace(path)
    except OSError as exc:
        logging.getLogger("updater").warning("could not record code hash: %s", exc)


async def _run_daemon() -> None:
    """Start the D-Bus service; sdbus is imported here so the CLI runs without it."""
    import sdbus

    from updater.dbus_service import UpdaterDbusService

    _record_code_hash()
    _log = logging.getLogger("updater")
    bus = sdbus.sd_bus_open_system()
    service = UpdaterDbusService()
    service.export_to_dbus("/com/blockscreen/Updater", bus)
    try:
        await bus.request_name_async("com.blockscreen.Updater", 0)
    except sdbus.SdBusBaseError as exc:
        # Not READY: Restart=always retries until the name frees.
        _log.error("failed to claim D-Bus name: %s - another instance running?", exc)
        raise SystemExit(1) from exc
    _log.info("updater daemon running on com.blockscreen.Updater")
    _sd_notify("READY=1")
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    loop.add_signal_handler(signal.SIGINT, stop_event.set)
    await _serve(stop_event, _watchdog_ping_interval(), service.yaml_broken)
    _log.info("updater daemon shutting down")
    await service.shutdown()


# How often an idle daemon checks whether a venv heal repaired PyYAML.
_YAML_PROBE_S = 60.0


async def _yaml_repaired(python: str = sys.executable) -> bool:
    """Return True when a fresh interpreter imports a working PyYAML."""
    # A fresh process, since the truncated module stays cached in this one's sys.modules.
    proc = await asyncio.create_subprocess_exec(
        python,
        "-I",
        "-c",
        "import yaml; yaml.safe_load, yaml.YAMLError",
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    try:
        return await asyncio.wait_for(proc.wait(), timeout=10.0) == 0
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        return False


async def _serve(
    stop_event: asyncio.Event, ping_interval: float, yaml_broken: bool
) -> None:
    """Ping the watchdog until stopped, or until PyYAML heals so Restart=always reloads components."""
    loop = asyncio.get_running_loop()
    next_probe = loop.time() + _YAML_PROBE_S
    while not stop_event.is_set():
        _sd_notify("WATCHDOG=1")
        if yaml_broken and loop.time() >= next_probe:
            if await _yaml_repaired():
                logging.getLogger("updater").warning(
                    "PyYAML repaired - restarting to load components"
                )
                return
            next_probe = loop.time() + _YAML_PROBE_S
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=ping_interval)
        except asyncio.TimeoutError:
            pass


def _watchdog_ping_interval() -> float:
    """Half of systemd's WatchdogSec (per sd_notify(3)), or 15s if unset/invalid."""
    try:
        watchdog_usec = int(os.environ.get("WATCHDOG_USEC", "0"))
    except ValueError:
        watchdog_usec = 0
    return watchdog_usec / 2_000_000 if watchdog_usec > 0 else 15.0


@contextlib.contextmanager
def _cli_lock() -> Iterator[None]:
    """Serialize mutating CLI commands against the daemon and other CLI runs."""
    with process_lock() as acquired:
        if not acquired:
            logging.getLogger("updater").error(
                "updater busy: the daemon or another CLI run holds the lock"
            )
            raise SystemExit(1) from None
        yield


def _print_component_status(s: ComponentStatus, verbose: bool) -> None:
    """Print a one-line status summary for a component (+ verbose detail line)."""
    if s.error:
        print(f"{s.name}: ERROR: {s.error}")
    elif s.branch_mismatch:
        print(f"{s.name}: branch switch needed")
    elif s.needs_install:
        print(f"{s.name}: install required")
    elif s.packages_upgradable > 0:
        print(f"{s.name}: {s.packages_upgradable} packages upgradable")
    elif s.commits_behind > 0:
        print(f"{s.name}: {s.commits_behind} commits behind")
    elif s.has_local_changes:
        print(f"{s.name}: local changes")
    else:
        print(f"{s.name}: up to date")
    if verbose:
        print(
            f"    branch={s.current_branch or '?'} mismatch={s.branch_mismatch} "
            f"behind={s.commits_behind} needs_install={s.needs_install} "
            f"local_changes={s.has_local_changes} pkgs={s.packages_upgradable} "
            f"hash={s.current_hash[:8]}"
        )


async def main() -> None:
    """Parse CLI args and dispatch to the appropriate UpdateService method."""
    args = build_parser().parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    match args.command:
        case "daemon":
            await _run_daemon()
            return
        case _:
            pass
    svc = UpdateService(callback=LoggingCallback())
    match args.command:
        case "update":
            with _cli_lock():
                await svc.reconcile_if_pending()
                if args.name is None:
                    ok = await svc.update_all()
                else:
                    ok = await svc.update_component(args.name)
            if not ok:
                raise SystemExit(1)
        case "status":
            result = await svc.check_status()
            for s in sorted(result.values(), key=lambda c: c.name):
                _print_component_status(s, args.verbose)
        case "recover":
            with _cli_lock():
                await svc.reconcile_if_pending()
                if not await svc.recover(args.name, hard=args.hard):
                    raise SystemExit(1)
        case "bless":
            with _cli_lock():
                ok = await svc.bless_healthy(args.name, args.hash)
                if not ok:
                    raise SystemExit(1)
        case None:
            build_parser().print_help()


if __name__ == "__main__":
    asyncio.run(main())
