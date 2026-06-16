#!/bin/bash
# Runs after a successful BlocksScreen git update (via updater daemon).
# Uses only sudo-free mechanisms: symlink + dbus-send (polkit) for service
# file changes, flag file + BlocksScreen-deploy.path for install-updater.sh.
set -euo pipefail

if [ -z "${COMPONENT_PATH:-}" ] || [ -z "${PREV_HASH:-}" ] || [ -z "${NEW_HASH:-}" ]; then
    exit 0
fi

_set_deploy_flag() {
    local _flag="${HOME}/.config/blockscreen/.run-install-updater"
    mkdir -p "$(dirname "$_flag")"
    touch "$_flag"
    echo "[hook:BlocksScreen] deploy flag set — BlocksScreen-deploy.path will run install-updater.sh"
}

# --- BlocksScreen.service changed ---
if ! git -C "$COMPONENT_PATH" diff --quiet "$PREV_HASH" "$NEW_HASH" \
        -- scripts/BlocksScreen.service 2>/dev/null; then

    echo "[hook:BlocksScreen] unit file changed — reinstalling"

    _env_dir="${HOME}/.config/blockscreen"
    _env_file="${_env_dir}/env"
    if [[ ! -f "$_env_file" ]]; then
        echo "[hook:BlocksScreen] creating EnvironmentFile at $_env_file"
        _bsenv="${BLOCKSSCREEN_VENV:-${HOME}/.BlocksScreen-env}"
        _backend=$(grep -oP 'BACKEND=\K\S+' /etc/systemd/system/BlocksScreen.service 2>/dev/null || echo "X")
        mkdir -p "$_env_dir"
        printf 'BS_DIR=%s\nBSENV=%s\nBS_BACKEND=%s\n' \
            "$COMPONENT_PATH" "$_bsenv" "$_backend" \
            > "$_env_file"
        echo "[hook:BlocksScreen] EnvironmentFile written"
    fi

    if [[ ! -L /etc/systemd/system/BlocksScreen.service ]]; then
        sudo cp "$COMPONENT_PATH/scripts/BlocksScreen.service" \
            /etc/systemd/system/BlocksScreen.service 2>/dev/null || {
            echo "[hook:BlocksScreen] sudo cp blocked — triggering deploy to bootstrap symlink"
            _set_deploy_flag
        }
    fi

    dbus-send --system --print-reply \
        --dest=org.freedesktop.systemd1 \
        /org/freedesktop/systemd1 \
        org.freedesktop.systemd1.Manager.Reload 2>/dev/null || \
        sudo systemctl daemon-reload 2>/dev/null || true
    echo "[hook:BlocksScreen] daemon-reload done"
fi

# --- BlocksScreen-xorg.service changed ---
if ! git -C "$COMPONENT_PATH" diff --quiet "$PREV_HASH" "$NEW_HASH" \
        -- scripts/BlocksScreen-xorg.service 2>/dev/null; then

    echo "[hook:BlocksScreen] xorg unit file changed — reinstalling"

    if [[ -f "$COMPONENT_PATH/scripts/BlocksScreen-xorg.service" ]] && \
       [[ ! -L /etc/systemd/system/BlocksScreen-xorg.service ]]; then
        sudo cp "$COMPONENT_PATH/scripts/BlocksScreen-xorg.service" \
            /etc/systemd/system/BlocksScreen-xorg.service 2>/dev/null || true
    fi

    dbus-send --system --print-reply \
        --dest=org.freedesktop.systemd1 \
        /org/freedesktop/systemd1 \
        org.freedesktop.systemd1.Manager.Reload 2>/dev/null || \
        sudo systemctl daemon-reload 2>/dev/null || true
    echo "[hook:BlocksScreen] daemon-reload done (xorg service)"
fi

# --- install-updater.sh changed (checked independently) ---
if ! git -C "$COMPONENT_PATH" diff --quiet "$PREV_HASH" "$NEW_HASH" \
        -- scripts/install-updater.sh 2>/dev/null; then
    echo "[hook:BlocksScreen] install-updater.sh changed — setting deploy flag"
    _set_deploy_flag
fi
