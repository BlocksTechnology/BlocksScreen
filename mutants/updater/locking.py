"""Cross-process advisory lock shared by the updater daemon and the CLI.

A single flock-backed lockfile serializes mutating git/apt work between the
daemon and a `python -m updater update` CLI run (asyncio locks are in-process
only); both acquire it non-blocking so the second caller fails fast.
"""

from __future__ import annotations

import contextlib
import fcntl
from collections.abc import Iterator
from pathlib import Path


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__runtime_dir__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__runtime_dir__mutmut)
def _runtime_dir() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_orig() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_1() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = None
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_2() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" * "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_3() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() * ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_4() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / "XX.cacheXX" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_5() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".CACHE" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_6() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "XXblockscreenXX"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_7() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "BLOCKSCREEN"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_8() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path(None), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_9() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("XX/run/blockscreenXX"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_10() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/RUN/BLOCKSCREEN"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_11() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=None, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_12() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=None)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_13() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_14() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, )
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_15() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=False, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_16() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=False)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_17() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(None):
                d.chmod(0o700)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_18() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(None)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_19() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(449)
            return d
        except OSError:
            continue
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache


def x__runtime_dir__mutmut_20() -> Path:
    """Return a writable user-owned runtime dir, preferring tmpfs over the cache."""
    cache = Path.home() / ".cache" / "blockscreen"
    for d in (Path("/run/blockscreen"), cache):
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Owner-only: nothing else may plant a sentinel to force a restart.
            with contextlib.suppress(OSError):
                d.chmod(0o700)
            return d
        except OSError:
            break
    # Broken home: return the cache path so open() surfaces the error (no /tmp).
    return cache

mutants_x__runtime_dir__mutmut['_mutmut_orig'] = x__runtime_dir__mutmut_orig # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_1'] = x__runtime_dir__mutmut_1 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_2'] = x__runtime_dir__mutmut_2 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_3'] = x__runtime_dir__mutmut_3 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_4'] = x__runtime_dir__mutmut_4 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_5'] = x__runtime_dir__mutmut_5 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_6'] = x__runtime_dir__mutmut_6 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_7'] = x__runtime_dir__mutmut_7 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_8'] = x__runtime_dir__mutmut_8 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_9'] = x__runtime_dir__mutmut_9 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_10'] = x__runtime_dir__mutmut_10 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_11'] = x__runtime_dir__mutmut_11 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_12'] = x__runtime_dir__mutmut_12 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_13'] = x__runtime_dir__mutmut_13 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_14'] = x__runtime_dir__mutmut_14 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_15'] = x__runtime_dir__mutmut_15 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_16'] = x__runtime_dir__mutmut_16 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_17'] = x__runtime_dir__mutmut_17 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_18'] = x__runtime_dir__mutmut_18 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_19'] = x__runtime_dir__mutmut_19 # type: ignore # mutmut generated
mutants_x__runtime_dir__mutmut['x__runtime_dir__mutmut_20'] = x__runtime_dir__mutmut_20 # type: ignore # mutmut generated
mutants_x_lock_path__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_lock_path__mutmut)
def lock_path() -> Path:
    """Return a user-owned lock path, preferring the runtime dir over the cache."""
    return _runtime_dir() / "updater.lock"


def x_lock_path__mutmut_orig() -> Path:
    """Return a user-owned lock path, preferring the runtime dir over the cache."""
    return _runtime_dir() / "updater.lock"


def x_lock_path__mutmut_1() -> Path:
    """Return a user-owned lock path, preferring the runtime dir over the cache."""
    return _runtime_dir() * "updater.lock"


def x_lock_path__mutmut_2() -> Path:
    """Return a user-owned lock path, preferring the runtime dir over the cache."""
    return _runtime_dir() / "XXupdater.lockXX"


def x_lock_path__mutmut_3() -> Path:
    """Return a user-owned lock path, preferring the runtime dir over the cache."""
    return _runtime_dir() / "UPDATER.LOCK"

mutants_x_lock_path__mutmut['_mutmut_orig'] = x_lock_path__mutmut_orig # type: ignore # mutmut generated
mutants_x_lock_path__mutmut['x_lock_path__mutmut_1'] = x_lock_path__mutmut_1 # type: ignore # mutmut generated
mutants_x_lock_path__mutmut['x_lock_path__mutmut_2'] = x_lock_path__mutmut_2 # type: ignore # mutmut generated
mutants_x_lock_path__mutmut['x_lock_path__mutmut_3'] = x_lock_path__mutmut_3 # type: ignore # mutmut generated
mutants_x_restart_sentinel_path__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_restart_sentinel_path__mutmut)
def restart_sentinel_path() -> Path:
    """Return the sentinel a self-update hook writes instead of restarting mid-batch.

    Hooks append `install`/`code` here; the daemon reads it once the batch ends.
    Prefer /run (tmpfs) so it clears on reboot: a crash can't trigger a spurious
    restart later (safe floor: adopt on next reboot).
    """
    return _runtime_dir() / "updater-restart-needed"


def x_restart_sentinel_path__mutmut_orig() -> Path:
    """Return the sentinel a self-update hook writes instead of restarting mid-batch.

    Hooks append `install`/`code` here; the daemon reads it once the batch ends.
    Prefer /run (tmpfs) so it clears on reboot: a crash can't trigger a spurious
    restart later (safe floor: adopt on next reboot).
    """
    return _runtime_dir() / "updater-restart-needed"


def x_restart_sentinel_path__mutmut_1() -> Path:
    """Return the sentinel a self-update hook writes instead of restarting mid-batch.

    Hooks append `install`/`code` here; the daemon reads it once the batch ends.
    Prefer /run (tmpfs) so it clears on reboot: a crash can't trigger a spurious
    restart later (safe floor: adopt on next reboot).
    """
    return _runtime_dir() * "updater-restart-needed"


def x_restart_sentinel_path__mutmut_2() -> Path:
    """Return the sentinel a self-update hook writes instead of restarting mid-batch.

    Hooks append `install`/`code` here; the daemon reads it once the batch ends.
    Prefer /run (tmpfs) so it clears on reboot: a crash can't trigger a spurious
    restart later (safe floor: adopt on next reboot).
    """
    return _runtime_dir() / "XXupdater-restart-neededXX"


def x_restart_sentinel_path__mutmut_3() -> Path:
    """Return the sentinel a self-update hook writes instead of restarting mid-batch.

    Hooks append `install`/`code` here; the daemon reads it once the batch ends.
    Prefer /run (tmpfs) so it clears on reboot: a crash can't trigger a spurious
    restart later (safe floor: adopt on next reboot).
    """
    return _runtime_dir() / "UPDATER-RESTART-NEEDED"

mutants_x_restart_sentinel_path__mutmut['_mutmut_orig'] = x_restart_sentinel_path__mutmut_orig # type: ignore # mutmut generated
mutants_x_restart_sentinel_path__mutmut['x_restart_sentinel_path__mutmut_1'] = x_restart_sentinel_path__mutmut_1 # type: ignore # mutmut generated
mutants_x_restart_sentinel_path__mutmut['x_restart_sentinel_path__mutmut_2'] = x_restart_sentinel_path__mutmut_2 # type: ignore # mutmut generated
mutants_x_restart_sentinel_path__mutmut['x_restart_sentinel_path__mutmut_3'] = x_restart_sentinel_path__mutmut_3 # type: ignore # mutmut generated


@contextlib.contextmanager
def process_lock() -> Iterator[bool]:
    """Acquire the shared updater lock non-blocking.

    Yields True if acquired, else False (another daemon/CLI holds it). The fd
    stays open for the whole `with` block; closing it on exit releases the lock.
    """
    try:
        f = open(lock_path(), "w")  # noqa: SIM115, PTH123
    except OSError:
        # Disk-full/RO SD: treat as "not acquired" so the caller degrades gracefully.
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
