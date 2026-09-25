#!/bin/bash
# Runs after a successful DeviceDiscovery git update (via updater daemon).
# Rebuilds the daemon; the updater then restarts device-discoveryd.service.
# run_hook kills hooks after 60 s, which is why build.sh is incremental and
# daemon-only. One-time setup (apt deps, systemd unit) is the repo's
# scripts/install.sh, not this hook - hooks have no reliable sudo.
set -euo pipefail

if [ -z "${COMPONENT_PATH:-}" ]; then
    exit 0
fi

exec "$COMPONENT_PATH/scripts/build.sh"
