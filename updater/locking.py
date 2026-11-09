"""Cross-process advisory lock shared by the updater daemon and the CLI."""

from __future__ import annotations

import contextlib
import fcntl
from collections.abc import Iterator
from pathlib import Path


def _runtime_dir() -> Path:
    """Return a 0700 runtime dir (tmpfs first) so no one else can plant a sentinel."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: let open() fail loudly instead of falling back to /tmp.
    return cache


def lock_path() -> Path:
    """Return a user-owned lock path, preferring the runtime dir over the cache."""
    return _runtime_dir() / "updater.lock"


def restart_sentinel_path() -> Path:
    """Return the sentinel a self-update hook writes instead of restarting mid-batch."""
    return _runtime_dir() / "updater-restart-needed"


@contextlib.contextmanager
def process_lock() -> Iterator[bool]:
    """Acquire the shared updater lock non-blocking; an OSError counts as not held."""
    try:
        f = open(lock_path(), "w")  # noqa: SIM115, PTH123
    except OSError:
        yield False
        return
    try:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        yield True
    finally:
        f.close()
