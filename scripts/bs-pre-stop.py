#!/usr/bin/env python3 -S
"""ExecStop — write splash to fb0 before the Qt process is fully dead.

X.Org stays alive (BlocksScreen-xorg.service is independent), so no VT switch
is needed.  Writing the splash to fb0 is a best-effort hint; in KMS mode the
vc4 driver may or may not honour fb0 writes while X holds DRM master.
ExecStopPost (bs-stop.py) repeats the write after the process is fully gone.
"""

import os
import sys
import time

_CACHE = "/home/blocks/.cache/blockscreen/splash.raw"
_RETRIES = 3
_RETRY_DELAY = 0.1


def _log(msg: str) -> None:
    sys.stderr.write(f"bs-pre-stop: {msg}\n")
    sys.stderr.flush()


for _attempt in range(_RETRIES):
    try:
        if os.path.exists(_CACHE):
            with (
                open(_CACHE, "rb", buffering=0) as _src,
                open("/dev/fb0", "wb", buffering=0) as _dst,
            ):
                _dst.write(_src.read())
        break
    except OSError as _e:
        if _attempt < _RETRIES - 1:
            time.sleep(_RETRY_DELAY)
        else:
            _log(f"fb0 write failed after {_RETRIES} attempts: {_e}")
