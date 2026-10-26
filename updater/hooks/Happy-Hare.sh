#!/bin/bash
# Link Happy-Hare's Moonraker component, as HH install.sh link_mmu_plugins does, without its printer.cfg edits.
set -euo pipefail

if [ -z "${COMPONENT_PATH:-}" ]; then
    echo "[hook:Happy-Hare] no COMPONENT_PATH"
    exit 1
fi

_src="$COMPONENT_PATH/components/mmu_server.py"
if [ ! -f "$_src" ]; then
    echo "[hook:Happy-Hare] $_src missing - bad checkout"
    exit 1
fi

# RF50 layout: Happy-Hare, moonraker and printer_data are siblings in one home.
_home=$(dirname "$COMPONENT_PATH")
_moonraker="$_home/moonraker"
_components="$_moonraker/moonraker/components"
if [ ! -d "$_components" ]; then
    echo "[hook:Happy-Hare] $_components not found - Moonraker not installed, skipping"
    exit 0
fi

_dst="$_components/mmu_server.py"
_linked=false
if [ "$(readlink "$_dst" 2>/dev/null || true)" != "$_src" ]; then
    ln -sfn "$_src" "$_dst"
    _linked=true
    echo "[hook:Happy-Hare] linked $_dst -> $_src"
fi

# Moonraker reports untracked .py files as a repo anomaly; info/exclude is never committed or cleaned.
_exclude=$(git -C "$_moonraker" rev-parse --git-path info/exclude 2>/dev/null || true)
# Relative to the repo unless absolute; --path-format=absolute needs git 2.31.
[[ -z "$_exclude" || "$_exclude" == /* ]] || _exclude="$_moonraker/$_exclude"
_pattern="/moonraker/components/mmu_server.py"
_add_exclude() {
    mkdir -p "$(dirname "$_exclude")" || return 1
    if [ -s "$_exclude" ] && [ -n "$(tail -c1 "$_exclude")" ]; then
        echo >>"$_exclude" || return 1
    fi
    echo "$_pattern" >>"$_exclude"
}
# Cosmetic only, so a failure must not fail the hook: a failed provision deletes the checkout under the link.
if [ -n "$_exclude" ] && ! grep -qxF "$_pattern" "$_exclude" 2>/dev/null; then
    if _add_exclude; then
        echo "[hook:Happy-Hare] added $_pattern to $_exclude"
    else
        echo "[hook:Happy-Hare] WARN: could not write $_exclude - Moonraker may report its repo dirty"
    fi
fi

if [[ " ${BS_UPDATER_PENDING_RESTARTS:-} " == *" moonraker.service "* ]]; then
    echo "[hook:Happy-Hare] link only - caller restarts Moonraker"
    exit 0
fi
if [ -n "${BS_UPDATER_PRINTING:-}" ]; then
    echo "[hook:Happy-Hare] print running - mmu_server loads on the next Moonraker restart"
    exit 0
fi

if ! $_linked && [ -n "${PREV_HASH:-}" ] && [ -n "${NEW_HASH:-}" ] \
        && git -C "$COMPONENT_PATH" diff --quiet "$PREV_HASH" "$NEW_HASH" \
            -- components/mmu_server.py 2>/dev/null; then
    echo "[hook:Happy-Hare] mmu_server.py unchanged - no Moonraker restart"
    exit 0
fi

# Moonraker only loads the component when moonraker.conf has the section.
_conf="$_home/printer_data/config/moonraker.conf"
if ! grep -q '^\[mmu_server\]' "$_conf" 2>/dev/null; then
    echo "[hook:Happy-Hare] no [mmu_server] in $_conf - no Moonraker restart"
    exit 0
fi

echo "[hook:Happy-Hare] restarting moonraker.service to load mmu_server"
# Blocking, so later steps never race Moonraker's startup; argv must match sudoers.
if ! sudo -n systemctl restart moonraker.service 2>/dev/null; then
    echo "[hook:Happy-Hare] WARN: could not restart moonraker.service - loads on next restart"
    exit 0
fi
for _ in $(seq 30); do
    if systemctl is-active --quiet moonraker.service; then
        echo "[hook:Happy-Hare] done"
        exit 0
    fi
    sleep 1
done
echo "[hook:Happy-Hare] WARN: moonraker.service not active after restart"
