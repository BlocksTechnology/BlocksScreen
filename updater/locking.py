"""Cross-process advisory lock shared by the updater daemon and the CLI.

A single flock-backed lockfile is the only thing serializing mutating git/apt
work between the long-running daemon and a `python -m updater update` CLI run:
the daemon's asyncio locks are in-process only. Both sides acquire the same path
non-blocking, so whoever is second fails fast instead of corrupting a repo.
"""

from __future__ import annotations

import contextlib
import fcntl
from collections.abc import Iterator
from pathlib import Path


def _runtime_dir() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            return d
        except OSError:
            continue
    # Both unavailable (broken home): return the cache path so the caller's open()
    # surfaces the error rather than silently falling back to world-writable /tmp.
    return cache


def lock_path() -> Path:
    """Return a user-owned lock path, preferring the runtime dir over the cache."""
    return _runtime_dir() / "updater.lock"


def restart_sentinel_path() -> Path:
    """Return the sentinel a self-update hook writes instead of restarting.

    Hooks running under the updater append `install`/`code` here rather than
    restarting the daemon mid-batch; the daemon reads it once the batch is done.
    Preferring /run (tmpfs) means it clears on reboot, so a crash can never
    trigger a spurious restart later — the safe floor is 'adopt on next reboot'.
    """
    return _runtime_dir() / "updater-restart-needed"


@contextlib.contextmanager
def process_lock() -> Iterator[bool]:
    """Acquire the shared updater lock non-blocking.

    Yields True if acquired, False if another updater process (daemon or CLI)
    holds it. The fd stays open for the whole `with` block — closing it on exit
    is what releases the lock.
    """
    f = open(lock_path(), "w")  # noqa: SIM115, PTH123
    try:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        yield True
    finally:
        f.close()
