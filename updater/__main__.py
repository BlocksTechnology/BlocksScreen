import argparse
import asyncio
import logging
import signal

import sdbus

from updater.dbus_service import UpdaterDbusService
from updater.service import LoggingCallback, UpdateService


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
    sdbus.sd_notify(0, "READY=1")
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    loop.add_signal_handler(signal.SIGINT, stop_event.set)
    while not stop_event.is_set():
        sdbus.sd_notify(0, "WATCHDOG=1")
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=15.0)
        except asyncio.TimeoutError:
            pass
    _log.info("updater daemon shutting down")


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
            if args.name is None:
                await svc.update_all()
            else:
                await svc.update_component(args.name)
        case "status":
            result = await svc.check_status()
            for s in sorted(result.values(), key=lambda c: c.name):
                if s.error:
                    print(f"{s.name}: ERROR — {s.error}")
                elif s.packages_upgradable > 0:
                    print(f"{s.name}: {s.packages_upgradable} packages upgradable")
                elif s.commits_behind > 0:
                    print(f"{s.name}: {s.commits_behind} commits behind")
                else:
                    print(f"{s.name}: up to date")
        case "recover":
            await svc.recover(args.name, hard=args.hard)
        case None:
            await svc.update_all()


if __name__ == "__main__":
    asyncio.run(main())
