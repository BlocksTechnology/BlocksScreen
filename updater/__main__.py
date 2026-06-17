import argparse
import asyncio
import contextlib
import fcntl
import logging
import os
import signal
import socket
from collections.abc import Iterator
from pathlib import Path

from updater.service import LoggingCallback, UpdateService

# NOTE: sdbus and updater.dbus_service are imported lazily inside _run_daemon so
# the status/update/recover CLI works on an interpreter without sdbus installed.


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
    # Subcommands
    # update [name] , status, recover <name> [--hard]
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

    return parser


async def _run_daemon() -> None:
    """Start the updater D-Bus service on the system bus."""
    import sdbus

    from updater.dbus_service import UpdaterDbusService

    _log = logging.getLogger("updater")
    bus = sdbus.sd_bus_open_system()
    service = UpdaterDbusService()
    service.export_to_dbus("/com/blockscreen/Updater", bus)
    try:
        await bus.request_name_async("com.blockscreen.Updater", 0)
    except sdbus.SdBusBaseError as exc:
        _log.error("failed to claim D-Bus name: %s — another instance running?", exc)
        return
    _log.info("updater daemon running on com.blockscreen.Updater")
    _sd_notify("READY=1")
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    loop.add_signal_handler(signal.SIGINT, stop_event.set)
    while not stop_event.is_set():
        _sd_notify("WATCHDOG=1")
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=15.0)
        except asyncio.TimeoutError:
            pass
    _log.info("updater daemon shutting down")


def _cli_lock_path() -> Path:
    """Return a user-owned path for the CLI lock, preferring the runtime dir."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            return d / "updater_cli.lock"
        except OSError:
            continue
    # Both unavailable (broken home): return the cache path anyway so the caller's
    # open() surfaces the error, rather than fall back to a world-writable /tmp.
    return cache / "updater_cli.lock"


@contextlib.contextmanager
def _cli_lock() -> Iterator[None]:
    """Serialize mutating CLI commands against the daemon and other CLI runs."""
    with open(_cli_lock_path(), "w") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            logging.getLogger("updater").error(
                "updater busy: the daemon or another CLI run holds the lock"
            )
            raise SystemExit(1) from None
        yield


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
                if args.name is None:
                    await svc.update_all()
                else:
                    await svc.update_component(args.name)
        case "status":
            result = await svc.check_status()
            for s in sorted(result.values(), key=lambda c: c.name):
                if s.error:
                    print(f"{s.name}: ERROR: {s.error}")
                elif s.packages_upgradable > 0:
                    print(f"{s.name}: {s.packages_upgradable} packages upgradable")
                elif s.commits_behind > 0:
                    print(f"{s.name}: {s.commits_behind} commits behind")
                else:
                    print(f"{s.name}: up to date")
        case "recover":
            with _cli_lock():
                await svc.recover(args.name, hard=args.hard)
        case None:
            build_parser().print_help()


if __name__ == "__main__":
    asyncio.run(main())
