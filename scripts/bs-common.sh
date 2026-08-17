#!/bin/bash
# Shared helpers sourced by BlocksScreen-start.sh and post-merge. Definitions
# only, no side effects. Callers run as `blocks` (NOPASSWD sudo on deployment).

# Idempotently patch moonraker.conf. $1 = conf path, $2 = log tag.
bs_migrate_moonraker_conf() {
    local conf="$1" tag="${2:-bs-common}" patched=false
    [ -f "$conf" ] || return 0
    cp "$conf" "${conf}.bak" 2>/dev/null || true
    # Gate on the section existing: else the sed no-ops but patched=true restarts moonraker every boot.
    if ! grep -q "enable_system_updates" "$conf" && grep -q '^\[update_manager\]$' "$conf"; then
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
    if bs_ensure_spoolman_moonraker "$conf" "$tag"; then
        patched=true
    fi
    # Moonraker only reads the allowlist at startup, so reuse the restart this function already decides on.
    if bs_ensure_asvc "${conf%/config/moonraker.conf}/moonraker.asvc" "$tag"; then
        patched=true
    fi
    $patched && sudo systemctl restart moonraker.service 2>/dev/null || true
    return 0
}

# Point Moonraker at a locally-provisioned Spoolman so the UI's spoolman_proxy
# works. Idempotent; only acts when Spoolman is installed and [spoolman] is
# absent. Returns 0 only on change, so the caller restarts moonraker.
bs_ensure_spoolman_moonraker() {
    local conf="$1" tag="${2:-bs-common}"
    [ -f "$conf" ] || return 1
    local spoolman_dir="${conf%/printer_data/config/moonraker.conf}/Spoolman"
    [ -d "$spoolman_dir/.venv" ] || return 1
    grep -q '^\[spoolman\]' "$conf" && return 1
    printf '\n[spoolman]\nserver: localhost:7912\n' >>"$conf"
    echo "[$tag] moonraker.conf: added [spoolman] (server: localhost:7912)"
    return 0
}

# Append a line, restoring the missing final newline first, else the append lands on the previous line.
_bs_append_line() {
    local f="$1" line="$2"
    [ -s "$f" ] && [ -n "$(tail -c 1 "$f" 2>/dev/null)" ] && printf '\n' >>"$f"
    printf '%s\n' "$line" >>"$f"
}

# Moonraker refuses to restart units absent from moonraker.asvc, so old images break UI updates silently.
bs_ensure_asvc() {
    local asvc="$1" tag="${2:-bs-common}" changed=false
    [ -e "$asvc" ] || : >"$asvc" 2>/dev/null || return 1
    [ -w "$asvc" ] || return 1
    # Pre-rename images called the unit BlocksPrinter; the entry now names a service that does not exist.
    if grep -qx 'BlocksPrinter' "$asvc" 2>/dev/null; then
        sed -i '/^BlocksPrinter$/d' "$asvc" 2>/dev/null && changed=true &&
            echo "[$tag] moonraker.asvc: dropped legacy BlocksPrinter entry"
    fi
    if ! grep -qx 'BlocksScreen' "$asvc" 2>/dev/null; then
        _bs_append_line "$asvc" BlocksScreen && changed=true &&
            echo "[$tag] moonraker.asvc: added BlocksScreen"
    fi
    $changed
}

# install.sh runs only at flash time, so re-assert the artifacts old images shipped wrong or not at all.
bs_ensure_install_state() {
    local bs_path="$1" bsenv="$2" tag="${3:-bs-common}" home env_file logs k
    home=$(getent passwd "$(id -un)" | cut -d: -f6)
    [ -n "$home" ] || return 0
    env_file="$home/.config/blockscreen/env"
    mkdir -p "$home/.config/blockscreen" 2>/dev/null || true
    # EnvironmentFile is optional (-) in the unit, so a missing env file degrades silently instead of failing.
    for k in "BS_DIR=$bs_path" "BSENV=$bsenv" "BS_BACKEND=${BS_BACKEND:-X}"; do
        grep -q "^${k%%=*}=" "$env_file" 2>/dev/null && continue
        _bs_append_line "$env_file" "$k" 2>/dev/null &&
            echo "[$tag] env: declared ${k%%=*}"
    done
    logs="$bs_path/logs"
    # Without setgid, files the updater writes as root land root-owned and the UI cannot rotate them.
    if [ -d "$logs" ] && [ "$(stat -c %a "$logs" 2>/dev/null)" != "2775" ]; then
        # Images flashed before install.sh grew the groupadd have no blocksscreen group, so chown would no-op.
        sudo groupadd -f blocksscreen 2>/dev/null || true
        sudo chown blocks:blocksscreen "$logs" 2>/dev/null || true
        sudo chmod 2775 "$logs" 2>/dev/null &&
            echo "[$tag] logs: restored setgid 2775"
    fi
    return 0
}

# Pi 5 ports are capped at 600mA combined unless raised; the fleet's declared USB draw is 824mA.
# NOT a proven fix for the RF50 MCU shutdowns (root cause unknown) - shipped anyway because the
# oversubscription itself is real regardless of causation. Only takes effect after the next reboot.
bs_ensure_usb_max_current() {
    local f="${1:-/boot/firmware/config.txt}" tag="${2:-bs-common}" mnt opts
    [ -f "$f" ] || return 0
    if grep -qE '^[[:space:]]*usb_max_current_enable[[:space:]]*=[[:space:]]*1[[:space:]]*$' "$f" 2>/dev/null; then
        return 0
    fi
    mnt=$(findmnt -no TARGET --target "$f" 2>/dev/null) || mnt=""
    if [ -n "$mnt" ]; then
        opts=$(findmnt -no OPTIONS "$mnt" 2>/dev/null)
        case ",$opts," in
        *,ro,*)
            echo "[$tag] $mnt is mounted read-only, remounting rw to write usb_max_current_enable"
            sudo mount -o remount,rw "$mnt" 2>/dev/null || {
                echo "[$tag] remount rw of $mnt failed, usb_max_current_enable NOT applied"
                return 1
            }
            ;;
        esac
    fi
    printf '\nusb_max_current_enable=1\n' | sudo tee -a "$f" >/dev/null 2>&1
    sync
    # tee's exit status is not proof of a landed write: a prior field attempt silently no-op'd against
    # a read-only remount while tee still reported success. Read the file back before trusting it.
    if ! grep -qE '^[[:space:]]*usb_max_current_enable[[:space:]]*=[[:space:]]*1[[:space:]]*$' "$f" 2>/dev/null; then
        echo "[$tag] write to $f did not land, usb_max_current_enable NOT applied"
        return 1
    fi
    echo "[$tag] usb_max_current_enable=1 written to $f, takes effect after reboot"
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
    # Same-dir temp + atomic rename: a power cut can never truncate moonraker.conf.
    tmp="$(mktemp -p "$(dirname "$conf")" .moonraker.conf.XXXXXX)" || return 1
    if awk -v owned="$owned" '
        BEGIN { n = split(owned, a, " "); for (i = 1; i <= n; i++) own[a[i]] = 1 }
        /^\[/ {
            insec = 0
            if ($0 ~ /^\[update_manager [^]]+\]/) {
                name = $0; sub(/^\[update_manager /, "", name); sub(/\].*/, "", name)
                if (name in own) insec = 1
            }
        }
        { if (insec) print "#" $0; else print }
    ' "$conf" > "$tmp"; then
        chmod --reference="$conf" "$tmp" 2>/dev/null || true
        mv -f "$tmp" "$conf"
    else
        rm -f "$tmp"
        return 1
    fi
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
            # Atomic install: a truncated BlocksScreen.service unit cannot self-heal.
            sudo cp "$src" "${dst}.new" && sudo mv -Tf "${dst}.new" "$dst" \
                && echo "[$tag] updated $(basename "$dst")" || true
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
