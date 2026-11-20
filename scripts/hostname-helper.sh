#!/bin/bash
# Give each board a hostname from its CPU serial and, early in boot, its own machine identity.
# Pass --install-only to refresh the unit without renaming the running system.

set -eu

Red='\033[0;31m'
Green='\033[0;32m'
Blue='\033[0;34m'
Normal='\033[0m'

echo_ok() {
    printf "${Green}%s${Normal}\n" "$1"
}

echo_info() {
    printf "${Blue}%s${Normal}\n" "$1"
}

echo_error() {
    printf "${Red}%s${Normal}\n" "$1"
}

SERVICE_PATH="/etc/systemd/system/set-hostname.service"
SCRIPT_PATH="$(readlink -f "$0")"
BRAND_PREFIX="BLOCKS"
MODEL="RF50"
INSTALL_ONLY=false
[ "${1:-}" = "--install-only" ] && INSTALL_ONLY=true

# The unit already runs as root and sudo may not resolve this early in boot, so only escalate when needed.
as_root() {
    if [ "$(id -u)" -eq 0 ]; then
        "$@"
    else
        sudo "$@"
    fi
}

# Kept in a function so a stale copy on a field box can be compared against and replaced.
service_unit() {
    cat <<EOF
[Unit]
Description=Set hostname based on CPU info
DefaultDependencies=no
After=systemd-remount-fs.service
Before=network-pre.target sysinit.target
Wants=network-pre.target

[Service]
Type=oneshot
ExecStart=$SCRIPT_PATH
RemainAfterExit=yes

[Install]
WantedBy=sysinit.target
EOF
}

install_service() {
    # The old guard skipped whenever the file existed, so every field box kept its broken unit forever.
    if [ "$(cat "$SERVICE_PATH" 2>/dev/null || true)" = "$(service_unit)" ]; then
        echo_ok "Service '$SERVICE_PATH' already current. Skipping installation"
        return 0
    fi
    echo_info "Installing hostname service..."
    service_unit | as_root tee "$SERVICE_PATH" >/dev/null
    as_root systemctl daemon-reload
    as_root systemctl enable set-hostname.service
}

ensure_hosts_entry() {
    local want="$1" file="${2:-/etc/hosts}" fixed
    # Collapse to one 127.0.1.1 line: the Release-2.0 script prepended another on every boot.
    fixed="$(awk -v h="$want" '
        /^127\.0\.1\.1[[:space:]]/ { if (!done) print "127.0.1.1\t" h; done = 1; next }
        { print }
        END { if (!done) print "127.0.1.1\t" h }' "$file")"
    if [ "$fixed" = "$(cat "$file")" ]; then
        return 0
    fi
    echo_info "Rewriting the 127.0.1.1 entry in $file..."
    printf '%s\n' "$fixed" | as_root tee "$file" >/dev/null
}

set_hostname() {
    local want="$1" current
    # Reading the file avoids hostnamectl, which needs a D-Bus that does not exist this early in boot.
    current="$(tr -d '[:space:]' </etc/hostname 2>/dev/null || true)"
    if [ "$current" = "$want" ]; then
        echo_ok "Hostname already set to $want. No action needed"
    else
        echo_info "Setting hostname to $want..."
        printf '%s\n' "$want" | as_root tee /etc/hostname >/dev/null
        # hostname(1) calls sethostname(2) directly, so it needs no D-Bus and no reboot to take effect.
        as_root hostname "$want" 2>/dev/null || true
    fi
    # Runs on unchanged hostnames too, so boxes updated from Release-2.0 shed their duplicate lines.
    ensure_hosts_entry "$want"
}

new_machine_id() {
    local root="$1" id tmp
    id="$(tr -d '-' </proc/sys/kernel/random/uuid)"
    if ! [[ "$id" =~ ^[0-9a-f]{32}$ ]]; then
        echo_error "Could not generate a machine-id"
        return 1
    fi
    # Atomic replace: an empty or missing machine-id makes systemd re-run first-boot presets.
    tmp="$root/etc/.machine-id.new"
    # Called from `||`, which disables set -e, so each step checks itself.
    printf '%s\n' "$id" | as_root tee "$tmp" >/dev/null || return 1
    as_root chmod 0444 "$tmp" || return 1
    as_root mv -f "$tmp" "$root/etc/machine-id" || return 1
    # A regular-file copy would keep the old id for dbus.
    if [ -d "$root/var/lib/dbus" ]; then
        as_root ln -sfn /etc/machine-id "$root/var/lib/dbus/machine-id" || return 1
    fi
}

stage_ssh_host_keys() {
    local stage="$1"
    as_root rm -rf "$stage"
    if ! as_root mkdir -p "$stage/etc/ssh" || ! as_root ssh-keygen -A -f "$stage" >/dev/null; then
        as_root rm -rf "$stage"
        echo_error "ssh-keygen failed, keeping the current identity"
        return 1
    fi
}

install_ssh_host_keys() {
    local root="$1" stage="$2" key
    # Key types ssh-keygen -A no longer makes would stay shared with every other board.
    for key in "$root"/etc/ssh/ssh_host_*; do
        [ -e "$stage/etc/ssh/${key##*/}" ] || as_root rm -f "$key" || return 1
    done
    # Rename over the old keys so sshd never finds none.
    as_root mv -f "$stage"/etc/ssh/ssh_host_* "$root/etc/ssh/" || return 1
    as_root rm -rf "$stage"
}

# Only v2 keys ("nm-v2:") are hashed with the machine-id; NM writes a fresh v2 key when none exists.
drop_v1_nm_secret_key() {
    local key="$1/var/lib/NetworkManager/secret_key"
    as_root test -f "$key" || return 0
    [ "$(as_root head -c 6 "$key")" = "nm-v2:" ] && return 0
    as_root rm -f "$key"
}

# Before basic.target nothing has read the identity; unlike a unit flag, this also works under old unit files.
early_boot() {
    [ "$(systemctl is-system-running 2>/dev/null || true)" = "initializing" ]
}

ensure_identity() {
    local serial="$1" root="${2:-}" marker stage keys=false
    marker="$root/var/lib/blocksscreen/identity-serial"
    stage="$root/etc/ssh/.hostkeys-new"
    # Cloned images share machine-id (NetworkManager's IPv6 address seed) and SSH host keys.
    if [ "$(cat "$marker" 2>/dev/null || true)" = "$serial" ]; then
        return 0
    fi
    echo_info "First boot on this board, regenerating machine-id and SSH host keys..."
    # Keys are staged first: a failure leaves the old identity whole, and without the marker the next boot retries.
    if command -v ssh-keygen >/dev/null; then
        stage_ssh_host_keys "$stage" || return 0
        keys=true
    fi
    if ! new_machine_id "$root"; then
        as_root rm -rf "$stage"
        return 0
    fi
    if $keys; then
        install_ssh_host_keys "$root" "$stage" || return 0
    fi
    drop_v1_nm_secret_key "$root" || return 0
    # Flush the new identity before the marker that claims it.
    sync
    as_root mkdir -p "$(dirname "$marker")"
    printf '%s\n' "$serial" | as_root tee "$marker" >/dev/null
    sync
    echo_ok "Machine identity regenerated"
}

main() {
    echo_info "Script running on $SCRIPT_PATH..."
    install_service
    $INSTALL_ONLY && exit 0

    SERIAL="$(awk '/^Serial/ {print $3; exit}' /proc/cpuinfo 2>/dev/null || true)"
    # A blank serial would name every board BLOCKS-RF50-, which is the collision this script exists to prevent.
    case "$SERIAL" in
        '' | *[!0-9a-fA-F]* | 0000000000000000)
            echo_error "No usable CPU serial in /proc/cpuinfo, leaving hostname unchanged"
            exit 0
            ;;
    esac

    set_hostname "$BRAND_PREFIX-$MODEL-$SERIAL"
    early_boot && ensure_identity "$SERIAL"
    return 0
}

# Sourcing (tests) only defines the functions.
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main
fi
