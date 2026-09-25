#!/bin/bash
# Runs after a DeviceDiscovery git update or first clone (via updater daemon).
# Rebuilds the daemon (build.sh is incremental and daemon-only, well inside
# run_hook's HOOK_TIMEOUT); the updater then restarts device-discoveryd.service.
#
# First-time setup (apt build deps, systemd unit) needs root, which hooks do
# not have, so it is not done here: the hook asks for install-updater.sh, which
# runs as root once the update batch is done.
set -euo pipefail

if [ -z "${COMPONENT_PATH:-}" ]; then
    exit 0
fi

UNIT="device-discoveryd.service"

if [ ! -x "$COMPONENT_PATH/bin/device_discoveryd" ] || \
   [ "$(systemctl show --property=LoadState --value "$UNIT" 2>/dev/null)" != "loaded" ]; then
    if [ -n "${BS_UPDATER_SELF_UPDATE:-}" ] && [ -n "${BS_UPDATER_RESTART_SENTINEL:-}" ]; then
        mkdir -p "$(dirname "$BS_UPDATER_RESTART_SENTINEL")" 2>/dev/null || true
        echo "install" >>"$BS_UPDATER_RESTART_SENTINEL"
        echo "[hook:DeviceDiscovery] not set up yet: deferring first-time setup to install-updater"
    else
        echo "[hook:DeviceDiscovery] not set up yet: run install-updater.sh or $COMPONENT_PATH/scripts/install.sh"
    fi
    exit 0
fi

exec "$COMPONENT_PATH/scripts/build.sh"
