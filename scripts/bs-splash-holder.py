#!/usr/bin/env python3 -S
"""Boot-time splash holder for tty8.

Activates tty8 immediately at boot (VT switch does not require fb0), then
watches for /dev/fb0 and the splash cache from the main loop, writing the
splash as soon as both exist and re-writing it whenever the cache changes
(bs-splash.py regenerates it at xorg startup).  No deadline: on Pi 5 KMS,
/dev/fb0 can appear ~90 s after boot, well after any sensible startup
timeout, so the holder simply keeps watching for as long as it runs.

KDSETMODE is intentionally NOT called: setting tty8 to KD_GRAPHICS+VT_AUTO
would cause VT_ACTIVATE(7) to return -EINVAL when bs-splash.py tries to switch
FROM tty8 at startup.
"""

import fcntl
import json
import os
import signal
import sys
import time

_CACHE = "/home/blocks/.cache/blockscreen/splash.raw"
_FB0 = "/dev/fb0"
_VT_ACTIVATE = 0x5606
_VT_WAITACTIVE = 0x5607
_VT_NUM = 8
_POLL_INTERVAL = 0.5
_STATUS_PATH = "/run/blockscreen/updater_status.json"

_running = True
_status_mtime: float = 0.0
_cache_mtime: float = 0.0  # mtime of the cache version last written to fb0


def _log(msg: str) -> None:
    sys.stderr.write(f"bs-splash-holder: {msg}\n")
    sys.stderr.flush()


def _activate_tty8() -> None:
    for dev in ("/dev/tty0", "/dev/console"):
        try:
            fd = os.open(dev, os.O_WRONLY | os.O_NOCTTY)
            fcntl.ioctl(fd, _VT_ACTIVATE, _VT_NUM)
            try:
                fcntl.ioctl(fd, _VT_WAITACTIVE, _VT_NUM)
            except OSError:
                pass
            os.close(fd)
            _log(f"tty{_VT_NUM} activated via {dev}")
            return
        except OSError as e:
            _log(f"VT_ACTIVATE {_VT_NUM} on {dev} failed: {e}")


def _write_splash_if_updated() -> None:
    """Write the cached splash to fb0 when fb0 exists and the cache changed."""
    global _cache_mtime
    try:
        mtime = os.stat(_CACHE).st_mtime
    except OSError:
        return
    if mtime == _cache_mtime or not os.path.exists(_FB0):
        return
    try:
        with (
            open(_CACHE, "rb", buffering=0) as src,
            open(_FB0, "wb", buffering=0) as dst,
        ):
            dst.write(src.read())
        _cache_mtime = mtime
        _log("splash written to fb0")
    except OSError as e:
        _log(f"fb0 write failed: {e}")


def _show_update_status() -> None:
    try:
        with open(_STATUS_PATH) as _f:
            s = json.load(_f)
        msg = f"  Updating {s['name']}… step {s['step']}/{s['total']}".encode()
        with open("/dev/tty8", "wb") as _tty:
            _tty.write(b"\x1b[20;1H\x1b[2K" + msg)
    except (OSError, KeyError, ValueError):
        pass


def _on_sigterm(_sig: int, _frame: object) -> None:
    global _running
    _running = False


signal.signal(signal.SIGTERM, _on_sigterm)

# Switch to tty8 immediately - VT switch does not require fb0.
_activate_tty8()

# Clear tty8 and hide the cursor (no bare text): the screen stays black until the
# splash image is written to fb0 below, so the user only ever sees the logo splash.
try:
    with open("/dev/tty8", "wb") as _tty:
        _tty.write(b"\x1b[2J\x1b[H\x1b[?25l")
except OSError:
    pass

while _running:
    _write_splash_if_updated()
    try:
        mtime = os.stat(_STATUS_PATH).st_mtime
        if mtime != _status_mtime:
            _status_mtime = mtime
            _show_update_status()
    except OSError:
        pass
    time.sleep(_POLL_INTERVAL)
