#!/bin/bash
# Give each board a hostname derived from its CPU serial, before the network comes up.
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
}

# Sourcing (tests) only defines the functions.
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main
fi
