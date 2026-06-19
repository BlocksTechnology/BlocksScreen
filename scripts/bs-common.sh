#!/bin/bash
# Shared helpers sourced by BlocksScreen-start.sh and post-merge. Definitions
# only, no side effects. Callers run as `blocks` (NOPASSWD sudo on deployment).

# Idempotently patch moonraker.conf. $1 = conf path, $2 = log tag.
bs_migrate_moonraker_conf() {
    local conf="$1" tag="${2:-bs-common}" patched=false
    [ -f "$conf" ] || return 0
    cp "$conf" "${conf}.bak" 2>/dev/null || true
    if ! grep -q "enable_system_updates" "$conf"; then
        sed -i '/^\[update_manager\]$/a enable_system_updates: False' "$conf"
        patched=true
        echo "[$tag] moonraker.conf: disabled system apt upgrades"
    fi
    if grep -q "managed_services: klipper moonraker" "$conf"; then
        sed -i '/^\[update_manager BlocksScreen\]/,/^\[/ s/managed_services: klipper moonraker/managed_services: BlocksScreen/' "$conf"
        patched=true
        echo "[$tag] moonraker.conf: fixed BlocksScreen managed_services"
    fi
    if ! grep -q "blocksscreen-single-owner" "$conf"; then
        bs_disable_overlapping_update_managers "$conf" "$tag" && patched=true
    fi
    $patched && sudo systemctl restart moonraker.service 2>/dev/null || true
    return 0
}

# Disable Moonraker management of repos the BlocksScreen daemon now owns, so a
# Mainsail "Update All" can't trip on them. Grep-gated marker so it runs once.
bs_disable_overlapping_update_managers() {
    local conf="$1" tag="${2:-bs-common}"
    [ -f "$conf" ] || return 1
    grep -q "blocksscreen-single-owner" "$conf" && return 1
    local owned="RF50-Klipper happy-hare Klippain-ShakeTune mainsail-config crowsnest"
    local tmp
    tmp="$(mktemp)" || return 1
    awk -v owned="$owned" '
        BEGIN { n = split(owned, a, " "); for (i = 1; i <= n; i++) own[a[i]] = 1 }
        /^\[/ {
            insec = 0
            if ($0 ~ /^\[update_manager [^]]+\]/) {
                name = $0; sub(/^\[update_manager /, "", name); sub(/\].*/, "", name)
                if (name in own) insec = 1
            }
        }
        { if (insec) print "#" $0; else print }
    ' "$conf" > "$tmp" && cat "$tmp" > "$conf"
    rm -f "$tmp"
    printf '\n# blocksscreen-single-owner applied by %s\n' "$tag" >> "$conf"
    echo "[$tag] moonraker.conf: disabled Moonraker management of daemon-owned repos"
}

# Sync repo unit files → /etc/systemd/system, reload on change, ensure X.Org is
# enabled+running. Idempotent. $1 = repo scripts dir, $2 = log tag.
bs_sync_service_files() {
    local src_dir="$1" tag="${2:-bs-common}" need_reload=false
    _bs_sync_one() {
        local src="$1" dst="$2"
        [ -f "$src" ] || return 0
        if ! diff -q "$dst" "$src" >/dev/null 2>&1; then
            sudo cp "$src" "$dst" && echo "[$tag] updated $(basename "$dst")" || true
            need_reload=true
        fi
    }
    # Never clobber the symlink install-updater.sh creates for BlocksScreen.service.
    [[ -L /etc/systemd/system/BlocksScreen.service ]] ||
        _bs_sync_one "$src_dir/BlocksScreen.service" /etc/systemd/system/BlocksScreen.service
    _bs_sync_one "$src_dir/BlocksScreen-xorg.service" /etc/systemd/system/BlocksScreen-xorg.service
    _bs_sync_one "$src_dir/BlocksScreen-splash-holder.service" /etc/systemd/system/BlocksScreen-splash-holder.service
    if $need_reload; then
        sudo systemctl daemon-reload || true
        # reenable to refresh the WantedBy symlink (e.g. multi-user → sysinit target)
        [ -f /etc/systemd/system/BlocksScreen-splash-holder.service ] &&
            sudo systemctl reenable BlocksScreen-splash-holder.service 2>/dev/null || true
    fi
    if [ -f /etc/systemd/system/BlocksScreen-xorg.service ]; then
        systemctl is-enabled --quiet BlocksScreen-xorg.service 2>/dev/null ||
            sudo systemctl enable BlocksScreen-xorg.service 2>/dev/null || true
        systemctl is-active --quiet BlocksScreen-xorg.service ||
            sudo systemctl start --no-block BlocksScreen-xorg.service 2>/dev/null || true
    fi
    return 0
}
