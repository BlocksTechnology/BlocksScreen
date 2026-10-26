#!/bin/bash
# A Moonraker reclone drops the mmu_server.py link or its info/exclude line, and Happy-Hare's hook only runs on HH changes.
set -uo pipefail

if [ -z "${COMPONENT_PATH:-}" ]; then
    echo "[hook:moonraker] no COMPONENT_PATH"
    exit 0
fi

# RF50 layout: Happy-Hare and moonraker are siblings in one home.
_hh="$(dirname "$COMPONENT_PATH")/Happy-Hare"
_src="$_hh/components/mmu_server.py"
_dst="$COMPONENT_PATH/moonraker/components/mmu_server.py"
if [ ! -f "$_src" ]; then
    # A failed Happy-Hare provision removes the checkout but leaves its link behind.
    if [ -L "$_dst" ] && [ "$(readlink "$_dst")" = "$_src" ]; then
        rm -f "$_dst" && echo "[hook:moonraker] removed dangling $_dst"
    fi
    echo "[hook:moonraker] no Happy-Hare checkout - nothing to link"
    exit 0
fi

# An update restarts moonraker.service after this hook; a boot reclone (empty-tree PREV_HASH) does not.
_pending=${BS_UPDATER_PENDING_RESTARTS:-}
if [ "${PREV_HASH:-}" != "4b825dc642cb6eb9a060e54bf8d69288fbee4904" ] \
        || [ "$(readlink "$_dst" 2>/dev/null || true)" = "$_src" ]; then
    _pending="$_pending moonraker.service"
fi
# Never fail: a failed hook rolls back the Moonraker update over an optional link.
COMPONENT_PATH="$_hh" PREV_HASH="" NEW_HASH="" BS_UPDATER_PENDING_RESTARTS="$_pending" \
    bash "$(dirname "$0")/Happy-Hare.sh" || echo "[hook:moonraker] WARN: relinking mmu_server failed"
exit 0
