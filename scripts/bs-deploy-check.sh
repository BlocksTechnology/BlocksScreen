#!/bin/bash
# Runs as root via ExecStartPre=-+ in BlocksScreen.service.
# Triggers install-updater.sh if any required infrastructure file is missing,
# making the machine self-healing on reboot/restart.
set -euo pipefail

SCRIPT_DIR="$(dirname -- "$(readlink -f -- "$0")")"

if [[ -f /etc/systemd/system/BlocksScreen-deploy.path ]] && \
   [[ -f /usr/share/dbus-1/system-services/com.blockscreen.Updater.service ]] && \
   [[ -f /etc/dbus-1/system.d/com.blockscreen.Updater.conf ]]; then
    exit 0
fi

echo "[bs-deploy-check] Missing updater infrastructure — bootstrapping in background"
# Detached transient unit: never blocks BlocksScreen.service startup (ExecStartPre).
systemd-run --unit=bs-bootstrap --collect /bin/bash "$SCRIPT_DIR/bs-bootstrap.sh" 2>/dev/null \
    || exec /bin/bash "$SCRIPT_DIR/install-updater.sh"
