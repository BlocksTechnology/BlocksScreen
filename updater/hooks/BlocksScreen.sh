#!/bin/bash
# Post-update hook: sudo-free unit sync + deploy-flag mechanics only.
set -euo pipefail

if [ -z "${COMPONENT_PATH:-}" ] || [ -z "${PREV_HASH:-}" ] || [ -z "${NEW_HASH:-}" ]; then
    exit 0
fi

_set_deploy_flag() {
    # Mid-batch: record to the sentinel; setting the flag now would fire deploy mid-batch.
    if [ -n "${BS_UPDATER_SELF_UPDATE:-}" ] && [ -n "${BS_UPDATER_RESTART_SENTINEL:-}" ]; then
        mkdir -p "$(dirname "$BS_UPDATER_RESTART_SENTINEL")" 2>/dev/null || true
        echo "install" >>"$BS_UPDATER_RESTART_SENTINEL"
        echo "[hook:BlocksScreen] under updater: deferring install-updater to post-batch"
        return
    fi
    local _flag="${HOME}/.config/blockscreen/.run-install-updater"
    mkdir -p "$(dirname "$_flag")"
    touch "$_flag"
    echo "[hook:BlocksScreen] deploy flag set - BlocksScreen-deploy.path will run install-updater.sh"
}

if ! git -C "$COMPONENT_PATH" diff --quiet "$PREV_HASH" "$NEW_HASH" \
        -- scripts/BlocksScreen.service 2>/dev/null; then

    echo "[hook:BlocksScreen] unit file changed - reinstalling"

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
            echo "[hook:BlocksScreen] sudo cp blocked - triggering deploy to bootstrap symlink"
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

if ! git -C "$COMPONENT_PATH" diff --quiet "$PREV_HASH" "$NEW_HASH" \
        -- scripts/BlocksScreen-xorg.service 2>/dev/null; then

    echo "[hook:BlocksScreen] xorg unit file changed - reinstalling"

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

# Same set as post-merge: only install-updater.sh deploys these, so any change must re-run it.
if ! git -C "$COMPONENT_PATH" diff --quiet "$PREV_HASH" "$NEW_HASH" \
        -- scripts/install-updater.sh scripts/bs-apt-helper.sh \
        scripts/BlocksScreen-updater.service scripts/BlocksScreen-bootstrap.service \
        scripts/com.blockscreen.Updater.conf scripts/com.blockscreen.Updater.service \
        scripts/requirements-pip.txt \
        2>/dev/null; then
    echo "[hook:BlocksScreen] install files changed - setting deploy flag"
    _set_deploy_flag
fi

# updater/ changed: defer a daemon self-restart to post-batch (mid-batch it would revert the batch).
if ! git -C "$COMPONENT_PATH" diff --quiet "$PREV_HASH" "$NEW_HASH" -- updater/ 2>/dev/null; then
    if [ -n "${BS_UPDATER_SELF_UPDATE:-}" ] && [ -n "${BS_UPDATER_RESTART_SENTINEL:-}" ]; then
        mkdir -p "$(dirname "$BS_UPDATER_RESTART_SENTINEL")" 2>/dev/null || true
        echo "code" >>"$BS_UPDATER_RESTART_SENTINEL"
        echo "[hook:BlocksScreen] updater code changed - deferring daemon restart to post-batch"
    fi
fi

# Manifest changed: the restarted daemon applies the changed entries in the same Update.
if ! git -C "$COMPONENT_PATH" diff --quiet "$PREV_HASH" "$NEW_HASH" \
        -- updater/components.yaml 2>/dev/null; then
    _followup="${HOME}/.cache/blockscreen/updater_followup"
    # Oldest base wins across chained updates; the try count resets.
    _base=$(head -n1 "$_followup" 2>/dev/null || true)
    mkdir -p "$(dirname "$_followup")"
    printf '%s\n' "${_base:-$PREV_HASH}" >"$_followup.tmp" && mv -f "$_followup.tmp" "$_followup"
    echo "[hook:BlocksScreen] components.yaml changed - follow-up queued"
fi
