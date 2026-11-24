#!/bin/bash
# Install RF50-Klipper's crowsnest.conf; the configurator only links *.cfg, so it never reached boxes.
set -uo pipefail

if [ -z "${COMPONENT_PATH:-}" ]; then
    echo "[hook:RF50-Klipper] no COMPONENT_PATH"
    exit 0
fi

_src="$COMPONENT_PATH/crowsnest.conf"
if [ ! -f "$_src" ]; then
    echo "[hook:RF50-Klipper] no crowsnest.conf in repo - nothing to install"
    exit 0
fi

# RF50 layout: RF50-Klipper and printer_data are siblings in one home.
_home=$(dirname "$COMPONENT_PATH")
_dst="$_home/printer_data/config/crowsnest.conf"
if [ ! -d "$(dirname "$_dst")" ]; then
    echo "[hook:RF50-Klipper] $(dirname "$_dst") not found - skipping"
    exit 0
fi

# Older templates pin a by-path no box has; installing one would kill the camera.
_dev=$(sed -n 's/#.*//; s/^[[:space:]]*device:[[:space:]]*//p' "$_src" | head -n1 | tr -d '[:space:]')
if [ -z "$_dev" ] || [ ! -e "$_dev" ]; then
    echo "[hook:RF50-Klipper] camera ${_dev:-<none>} not present - crowsnest.conf left as is"
    exit 0
fi

# Hash of the last installed template; local edits are kept until the template changes.
_state="$_home/.rf50_backups/.crowsnest.conf.template"
_sum=$(sha256sum "$_src" | cut -d' ' -f1)
_record() {
    mkdir -p "$(dirname "$_state")" && printf '%s\n' "$_sum" >"$_state" ||
        echo "[hook:RF50-Klipper] WARN: could not record the installed template"
}
if [ -e "$_dst" ] && [ "$(cat "$_state" 2>/dev/null)" = "$_sum" ]; then
    echo "[hook:RF50-Klipper] template unchanged - local crowsnest.conf kept"
    exit 0
fi

# A copy, not a link: a rollback resets the repo without rerunning this hook.
if [ -f "$_dst" ] && [ ! -L "$_dst" ] && cmp -s "$_src" "$_dst"; then
    _record
    echo "[hook:RF50-Klipper] crowsnest.conf up to date"
    exit 0
fi

# Never fail: a failed hook rolls back the RF50-Klipper update over a camera config.
if [ -e "$_dst" ] || [ -L "$_dst" ]; then
    # Same name scheme as the configurator's replaced-file backups.
    _bak="$_home/.rf50_backups/crowsnest.conf.$(date +%Y%m%dT%H%M%S)"
    # Two runs within one second must not overwrite the first backup.
    _n=1
    _base="$_bak"
    while [ -e "$_bak" ] || [ -L "$_bak" ]; do
        _bak="$_base.$_n"
        _n=$((_n + 1))
    done
    if ! mkdir -p "$(dirname "$_bak")" || ! cp -P "$_dst" "$_bak"; then
        echo "[hook:RF50-Klipper] WARN: could not back up $_dst - left as is"
        exit 0
    fi
    echo "[hook:RF50-Klipper] backed up $_dst to $_bak"
fi
if ! cp "$_src" "$_dst.bs-tmp" || ! mv -f "$_dst.bs-tmp" "$_dst"; then
    rm -f "$_dst.bs-tmp"
    echo "[hook:RF50-Klipper] WARN: could not install $_dst"
    exit 0
fi
_record
echo "[hook:RF50-Klipper] installed $_dst"

if [[ " ${BS_UPDATER_PENDING_RESTARTS:-} " == *" crowsnest.service "* ]]; then
    echo "[hook:RF50-Klipper] caller restarts crowsnest"
    exit 0
fi
if [ -n "${BS_UPDATER_PRINTING:-}" ]; then
    echo "[hook:RF50-Klipper] print running - crowsnest.conf loads on the next crowsnest start"
    exit 0
fi

echo "[hook:RF50-Klipper] restarting crowsnest.service"
# Blocking, so a failed restart is reported; argv must match the sudoers rule.
if sudo -n systemctl restart crowsnest.service 2>/dev/null; then
    echo "[hook:RF50-Klipper] done"
else
    echo "[hook:RF50-Klipper] WARN: could not restart crowsnest.service"
fi
exit 0
