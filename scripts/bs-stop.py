#!/usr/bin/env python3 -S
"""ExecStopPost — write splash to fb0 after Qt process is fully gone.

X.Org stays alive (BlocksScreen-xorg.service is independent), so no VT switch
is needed.  The Qt restart is handled by systemd's Restart=always on the
BlocksScreen.service unit; X.Org never releases DRM master across restarts.
"""

import os
import sys
import time

_CACHE = "/home/blocks/.cache/blockscreen/splash.raw"
_RETRIES = 3
_RETRY_DELAY = 0.1

for _attempt in range(_RETRIES):
    try:
        if os.path.exists(_CACHE):
            with (
                open(_CACHE, "rb", buffering=0) as src,
                open("/dev/fb0", "wb", buffering=0) as dst,
            ):
                dst.write(src.read())
        break
    except OSError as e:
        if _attempt < _RETRIES - 1:
            time.sleep(_RETRY_DELAY)
        else:
            sys.stderr.write(
                f"bs-stop: fb0 write failed after {_RETRIES} attempts: {e}\n"
            )
