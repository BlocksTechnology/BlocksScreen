#!/bin/bash
# flash_mcus.sh - Blocks Klipper MCU Flasher
# Copyright (C) 2026 Guilherme Costa <gmmcosta15@blockstec.com>
# Modes:
#   ./flash_mcus.sh                       interactive TUI (requires TTY)
#   ./flash_mcus.sh --list-json           discover MCUs, emit JSON, exit
#   ./flash_mcus.sh --flash <name...>     flash named MCUs
#   ./flash_mcus.sh --flash-all           flash all outdated MCUs (no interaction)
#   ./flash_mcus.sh --versions            report MCU vs host versions (read-only)
#   --force                               bypass version check (any mode)
#
# Versions file: $MCU_VERSIONS_FILE (default ~/printer_data/logs/mcu_versions.json).
# Per MCU: running version, needs_flash, last flash result.
#
# Config files in mcu_config/<name>.config - leading comment lines declare interface:
#   # mcu_type: rp2040              -> CAN flash (matched by chip type)
#   # klipper_section: mcu MyBoard  -> printer.cfg section (UUID auto-discovery + version query)
#   # serial: usb-Katapult_*        -> USB Katapult flash (glob under /dev/serial/by-id/)
#   # linux: klipper-mcu            -> Linux host MCU (systemd service name)
#   # bootsel: 2e8a:0003            -> BOOTSEL/picoboot flash (VID:PID)
#   # dfu: 0483:df11                -> STM32 DFU flash (dfu-util)
#   # dfu_mem: 8*128Kg              -> memory-name filter to disambiguate multiple DFU devices
#   # dfu_addr: 0x08000000          -> flash address (default 0x08000000)
#   # dfu_alt: 0                    -> alt interface (default 0)
#
# To add a new board:
#   1. cd ~/klipper && make menuconfig -> cp .config mcu_config/<name>.config
#   2. Add the relevant headers above (only what the board supports)
#   3. CAN boards: also create mcu_config/<name>.katapult.config from ~/katapult make menuconfig
#      and add # katapult_bootsel: <vid:pid>  or  # katapult_dfu: <vid:pid>  at the top
#   4. UUID is read automatically from printer.cfg on first run (klipper_section must match)

CAN_INTERFACE="can0"
CAN_SPEED=1000000
KLIPPER_DIR="$HOME/klipper"
PRINTER_CFG="${HOME}/printer_data/config/printer.cfg"
KATAPULT_DIR="$HOME/katapult"
# flashtool.py superseded flash_can.py; fall back for older Katapult checkouts.
KATAPULT_SCRIPT="$KATAPULT_DIR/scripts/flashtool.py"
[ -f "$KATAPULT_SCRIPT" ] || [ ! -f "$KATAPULT_DIR/scripts/flash_can.py" ] ||
    KATAPULT_SCRIPT="$KATAPULT_DIR/scripts/flash_can.py"
KATAPULT_REPO="https://github.com/Arksine/katapult"
SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
MCU_CONFIG_DIR="$SCRIPT_DIR/mcu_config"
UUID_CACHE="$MCU_CONFIG_DIR/.uuid_cache"
MOONRAKER_URL="${MOONRAKER_URL:-http://localhost:7125}"
VERSIONS_PY="$SCRIPT_DIR/mcu_versions.py"
PREFLIGHT_PY="$SCRIPT_DIR/mcu_preflight.py"
MCU_VERSIONS_FILE="${MCU_VERSIONS_FILE:-$HOME/printer_data/logs/mcu_versions.json}"
# Out-of-tree builds; ~/klipper/.config and ~/klipper/out are never modified.
FW_BUILD_ROOT="${FW_BUILD_ROOT:-${XDG_CACHE_HOME:-$HOME/.cache}/blocks-flash}"
FW_OUT=""            # out/ dir of the last build_firmware, trailing slash (Klipper OUT=)
FW_BIN=""            # klipper.bin of the last build_firmware
declare -a FW_MAKE_ARGS=() # KCONFIG_CONFIG/OUT of the last build, reused by `make flash`
KLIPPER_HOLD_DROPIN="/run/systemd/system/klipper.service.d/50-flash-mcus-hold.conf"
FLASH_LOCK="$FW_BUILD_ROOT/flash.lock"

RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
CYAN=$'\033[0;36m'
BOLD=$'\033[1m'
DIM=$'\033[2m'
RESET=$'\033[0m'
BOX_W=56

ok() { echo -e "  ${GREEN}[ OK ]${RESET}  $*" >&2; }
warn() { echo -e "  ${YELLOW}[ !! ]${RESET}  $*" >&2; }
err() { echo -e "  ${RED}[FAIL]${RESET}  $*" >&2; }
info() { echo -e "  ${DIM}[    ]${RESET}  $*" >&2; }
skip() { echo -e "  ${CYAN}[SKIP]${RESET}  $*" >&2; }
_indent() { sed 's/^/        /'; }
_indent4() { sed 's/^/    /'; }

header() {
    local text="$*"
    local pad=$((BOX_W - ${#text} - 4))
    [ "$pad" -lt 1 ] && pad=1
    echo "" >&2
    echo -e "  ${BOLD}${CYAN}┌─ ${text} $(_box_hline "$pad")┐${RESET}" >&2
}

# Repeat a single Unicode char n times - pure bash, no subprocesses.
_str_repeat() {
    local s='' i
    for ((i = 0; i < $2; i++)); do s+="$1"; done
    printf '%s' "$s"
}
_box_hline() { _str_repeat '─' "$1"; }
_box_rule() { printf '  \033[2m%s%s%s\033[0m\n' "$1" "$(_box_hline "$BOX_W")" "$2" >&2; }
_box_top() { _box_rule "╭" "╮"; }
_box_bottom() { _box_rule "╰" "╯"; }
_box_sep() { _box_rule "├" "┤"; }

# Strip ANSI escape sequences without spawning subprocesses.
_strip_ansi() {
    local s="$1"
    while [[ "$s" =~ $'\e'\[[0-9\;]*m ]]; do s="${s//${BASH_REMATCH[0]}/}"; done
    printf '%s' "$s"
}
_box_line() {
    local line="$1" plain pad
    plain=$(_strip_ansi "$line")
    pad=$((BOX_W - ${#plain} - 1))
    [ "$pad" -lt 0 ] && pad=0
    printf '  \033[2m│\033[0m %s%*s\033[2m│\033[0m\n' "$line" "$pad" '' >&2
}
_box_empty() { _box_line ""; }

_box_center() {
    local line="$1" plain total_pad left_pad right_pad
    plain=$(_strip_ansi "$line")
    total_pad=$((BOX_W - 1 - ${#plain}))
    [ "$total_pad" -lt 0 ] && total_pad=0
    left_pad=$((total_pad / 2))
    right_pad=$((total_pad - left_pad))
    printf '  \033[2m│\033[0m%*s%s%*s\033[2m│\033[0m\n' "$left_pad" '' "$line" "$right_pad" '' >&2
}

CONTEXT="laptop"
KATAPULT_OK=false

detect_context() {
    if ip link show "$CAN_INTERFACE" >/dev/null 2>&1; then
        CONTEXT="pi"
    elif sudo ip link set "$CAN_INTERFACE" up type can bitrate "$CAN_SPEED" 2>/dev/null; then
        CONTEXT="pi"
        sudo ip link set "$CAN_INTERFACE" down 2>/dev/null || true
    elif [ -f "$PRINTER_CFG" ] && [ -f /proc/device-tree/model ]; then
        # printer.cfg present + ARM device tree -> we're on the printer machine even if can0 isn't up yet
        CONTEXT="pi"
    fi
}

ensure_katapult() {
    if [ -f "$KATAPULT_SCRIPT" ]; then
        KATAPULT_OK=true
        ok "Katapult found"
        return 0
    fi
    warn "Katapult not found - cloning from $KATAPULT_REPO..."
    if git clone "$KATAPULT_REPO" "$KATAPULT_DIR" 2>&1 | _indent4; then
        ok "Katapult cloned"
        KATAPULT_OK=true
    else
        warn "Clone failed - CAN unavailable; USB falls back to klipper make flash"
        KATAPULT_OK=false
    fi
}

declare -A UUID_CACHE_MAP
declare -A MOONRAKER_VERSIONS # klipper_section -> mcu_version (live from Moonraker)

_load_kv_file() {
    local file="$1"
    local -n _map=$2
    [ -f "$file" ] || return 0
    while IFS='=' read -r key val; do
        [[ "$key" =~ ^[[:space:]]*# || -z "$key" || -z "$val" ]] && continue
        _map["$key"]="$val"
    done <"$file"
}

_save_kv_file() {
    local file="$1"
    local -n _map=$2
    local tmp
    tmp=$(mktemp "$file.XXXXXX")
    for key in "${!_map[@]}"; do
        echo "${key}=${_map[$key]}"
    done >"$tmp"
    mv "$tmp" "$file"
}

load_uuid_cache() { _load_kv_file "$UUID_CACHE" UUID_CACHE_MAP; }
save_uuid_cache() { _save_kv_file "$UUID_CACHE" UUID_CACHE_MAP; }

# Auto-populate UUID_CACHE_MAP from printer.cfg using # klipper_section: headers
# in each .config file.  No-ops silently if printer.cfg doesn't exist.
load_uuids_from_printer_cfg() {
    [ -f "$PRINTER_CFG" ] || return 0
    shopt -s nullglob
    for cfg in "$MCU_CONFIG_DIR"/*.config; do
        [[ "$(basename "$cfg")" == .* || "$cfg" == *.katapult.config ]] && continue
        local mcu_type="" klipper_section=""
        while IFS='=' read -r key val; do
            case "$key" in
            mcu_type) mcu_type="$val" ;;
            klipper_section) klipper_section="$val" ;;
            esac
        done < <(parse_config_metadata "$cfg")
        [ -z "$mcu_type" ] || [ -z "$klipper_section" ] && continue
        [ -n "${UUID_CACHE_MAP[$mcu_type]}" ] && continue # already in cache
        local uuid
        uuid=$(awk -v sec="[$klipper_section]" '
            /^\[/ {
                line=$0; sub(/[[:space:]]*#.*/, "", line); sub(/[[:space:]]*$/, "", line)
                if (line == sec) { in_sec=1; next }
                in_sec=0; next
            }
            in_sec && /canbus_uuid/ { gsub(/.*canbus_uuid[[:space:]]*:[[:space:]]*/, ""); gsub(/[[:space:]]*$/, ""); print; exit }
        ' "$PRINTER_CFG")
        if [ -n "$uuid" ]; then
            UUID_CACHE_MAP["$mcu_type"]="$uuid"
            info "UUID from printer.cfg: $mcu_type -> $uuid"
        fi
    done
    shopt -u nullglob
}

# Ensure Klipper and Moonraker are running.  Starts them if stopped.
# Waits up to 15s for Moonraker to respond (Klipper may take longer to
# connect all MCUs, but Moonraker itself starts quickly).
ensure_klipper_running() {
    local need_start=false

    if ! systemctl is-active --quiet klipper 2>/dev/null; then
        info "Klipper is not running - starting..."
        sudo systemctl start klipper 2>/dev/null || true
        need_start=true
    fi
    if ! systemctl is-active --quiet moonraker 2>/dev/null; then
        info "Moonraker is not running - starting..."
        sudo systemctl start moonraker 2>/dev/null || true
        need_start=true
    fi

    if $need_start; then
        local waited=0
        while [ "$waited" -lt 15 ]; do
            if curl -sf --max-time 2 "$MOONRAKER_URL/printer/info" >/dev/null 2>&1; then
                ok "Moonraker is ready"
                break
            fi
            sleep 1
            ((waited++))
        done
        if [ "$waited" -ge 15 ]; then
            warn "Moonraker did not respond within 15s - version query may fail"
            return 1
        fi
    fi

    # Wait for klippy_state to reach "ready" - CAN MCUs need time to reconnect.
    # If can0 is down (bridge MCU in DFU), Klipper will never reach "ready" -
    # cap the wait to 5s so discover() doesn't stall for 30s on every rescan.
    local max_wait=30
    ip link show can0 up >/dev/null 2>&1 || max_wait=5
    local waited=0 state=""
    while [ "$waited" -lt "$max_wait" ]; do
        state=$(python3 "$VERSIONS_PY" state --url "$MOONRAKER_URL") || true
        case "$state" in
        ready)
            ok "Klipper is ready (all MCUs connected)"
            return 0
            ;;
        error)
            warn "Klipper entered error state - MCU versions may be incomplete"
            return 1
            ;;
        shutdown)
            warn "Klipper is in shutdown state - MCU versions may be incomplete"
            return 1
            ;;
        esac
        # "startup" or empty - keep waiting
        [ "$waited" -eq 0 ] && info "Waiting for Klipper to connect to all MCUs..."
        sleep 1
        ((waited++))
    done
    warn "Klipper did not reach ready state within ${max_wait}s - MCU versions may be incomplete"
    return 1
}

# Keep Klipper stopped while flashing, since front-ends may restart it on disconnect.
# A runtime drop-in with an unmet condition skips every start (systemd.unit(5));
# `mask --runtime` cannot override a unit in /etc. /run is cleared on reboot.
hold_klipper() {
    sudo mkdir -p "${KLIPPER_HOLD_DROPIN%/*}" || return 1
    sudo tee "$KLIPPER_HOLD_DROPIN" >/dev/null <<EOF || return 1
# Written by flash_mcus.sh; Klipper start is blocked until flashing ends.
[Unit]
ConditionPathExists=${KLIPPER_HOLD_DROPIN}.unblock
EOF
    sudo systemctl daemon-reload
}

release_klipper() {
    [ -f "$KLIPPER_HOLD_DROPIN" ] || return 0
    sudo rm -f "$KLIPPER_HOLD_DROPIN"
    sudo systemctl daemon-reload
}

# Held on fd 9 for the whole run; the kernel drops it on any exit, SIGKILL included.
take_flash_lock() {
    mkdir -p "$FW_BUILD_ROOT" || return 1
    exec 9>"$FLASH_LOCK" || return 1
    flock -n 9
}

# With the lock taken, a hold left behind belongs to a killed run (SIGKILL, OOM).
recover_stale_hold() {
    [ -f "$KLIPPER_HOLD_DROPIN" ] || return 0
    warn "Removing a Klipper start block left by an interrupted flash"
    release_klipper && sudo systemctl start klipper
}

# Wait for "ready"; FIRMWARE_RESTART up to twice if an MCU is left in shutdown or error.
verify_klipper_ready() {
    local attempt
    for attempt in 1 2; do
        ensure_klipper_running && return 0
        info "Sending FIRMWARE_RESTART (attempt $attempt/2)..."
        curl -sf -X POST --max-time 5 "$MOONRAKER_URL/printer/firmware_restart" >/dev/null 2>&1 || true
        sleep 3
    done
    ensure_klipper_running
}

# Fill MOONRAKER_VERSIONS[<klipper_section>] from Moonraker (python3, no jq dependency).
query_moonraker_versions() {
    MOONRAKER_VERSIONS=()
    [ "$CONTEXT" = "laptop" ] && return 0

    local lines sec_name ver
    lines=$(python3 "$VERSIONS_PY" query --url "$MOONRAKER_URL") || {
        warn "Could not query Moonraker for MCU versions"
        return 1
    }
    while IFS=$'\t' read -r sec_name ver; do
        [ -z "$sec_name" ] || [ -z "$ver" ] && continue
        MOONRAKER_VERSIONS["$sec_name"]="$ver"
        info "[$sec_name] firmware: $ver"
    done <<<"$lines"
}

# Refresh the versions file; non-fatal.
write_versions_file() {
    python3 "$VERSIONS_PY" report --url "$MOONRAKER_URL" --source "$SRC_VERSION" \
        --state-file "$MCU_VERSIONS_FILE" "$@" || true
}

# Append a flash result to the versions file, keyed by klipper_section.
record_flash() {
    local cfg="$1" iface="$2" result="$3" section=""
    while IFS='=' read -r key val; do
        [ "$key" = "klipper_section" ] && section="$val"
    done < <(parse_config_metadata "$cfg")
    [ -z "$section" ] && return 0
    python3 "$VERSIONS_PY" record --state-file "$MCU_VERSIONS_FILE" --section "$section" \
        --version "$SRC_VERSION" --interface "$iface" --result "$result" || true
}

# Git hash of a version string, display only.
extract_git_hash() { [[ "$1" =~ -(g[0-9a-f]{7,40}) ]] && echo "${BASH_REMATCH[1]}" || echo ""; }

# Same format Klipper embeds in firmware (scripts/buildcommands.py).
get_source_version() {
    git -C "$KLIPPER_DIR" describe --always --tags --long --dirty 2>/dev/null | tr -d '\n'
}

# Prefix match: git abbreviates hashes to varying lengths.
versions_match() {
    [ -z "$1" ] && return 1
    python3 "$VERSIONS_PY" match "$1" "$2"
}

ensure_can_up() {
    ip link show "$CAN_INTERFACE" up >/dev/null 2>&1 && return 0
    info "Bringing up $CAN_INTERFACE at ${CAN_SPEED} bps..."
    if ! ip link show "$CAN_INTERFACE" >/dev/null 2>&1; then
        sudo modprobe gs_usb 2>/dev/null || true
        # Register Klipper/candleLight VID:PIDs with gs_usb so it binds to
        # already-plugged-in devices (kernel doesn't auto-bind unknown PIDs).
        for _new_id in "1d50 606f" "1d50 614e"; do
            echo "$_new_id" | sudo tee /sys/bus/usb/drivers/gs_usb/new_id \
                >/dev/null 2>&1 || true
        done
        # Re-fire USB add events so udev hotplug rules create the interface.
        sudo udevadm trigger --subsystem-match=usb --action=add 2>/dev/null || true
        sleep 2 # allow the interface to appear
    fi
    # Try with explicit type+bitrate (new interface), then plain up (interface
    # already typed as CAN - re-specifying 'type can' on an existing CAN
    # interface returns EBUSY/EINVAL on some kernels).
    if sudo ip link set "$CAN_INTERFACE" up type can bitrate "$CAN_SPEED" 2>/dev/null ||
        sudo ip link set "$CAN_INTERFACE" up 2>/dev/null; then
        sleep 1
        return 0
    fi
    warn "$CAN_INTERFACE not available (no CAN device detected)"
    return 1
}

bootloader_uuids() {
    $KATAPULT_OK || return
    python3 "$KATAPULT_SCRIPT" -i "$CAN_INTERFACE" -q 2>&1 |
        awk '/Detected UUID/ { gsub(/,/, "", $3); print $3 }'
}

# Query ALL CAN UUIDs (running Klipper + Katapult bootloader) via Klipper's
# canbus_query.py.  Falls back silently if the script is missing.
# Output: one "uuid|app" line per device (app = "Klipper" or "Katapult").
klipper_can_query() {
    local query_script="$KLIPPER_DIR/scripts/canbus_query.py"
    [ -x "$query_script" ] || [ -f "$query_script" ] || return 0
    timeout 5 python3 "$query_script" "$CAN_INTERFACE" 2>/dev/null |
        awk '/canbus_uuid=/ {
            uuid=$0; sub(/.*canbus_uuid=/, "", uuid); sub(/,.*/, "", uuid)
            app=$0;  sub(/.*Application: */, "", app); sub(/[[:space:]]*$/, "", app)
            print uuid "|" app
        }'
}

# Chip type of a CAN node in Katapult. Output: "mcu_type|".
# `-s` sends no bootloader jump (flashtool.py CanSocket.run); Klipper ignores its admin cmds.
probe_can_mcu() {
    local output
    output=$(timeout 10 python3 "$KATAPULT_SCRIPT" -i "$CAN_INTERFACE" \
        -u "$1" -s 2>&1 | tr -d '\0' || true)
    awk 'BEGIN{IGNORECASE=1} /MCU type:/ {mcu=tolower($NF)} END{print mcu "|"}' <<<"$output"
}

trigger_can_bootloader() {
    python3 "$KATAPULT_SCRIPT" -i "$CAN_INTERFACE" -u "$1" -r 2>&1 | _indent4
}

# First match of a glob; relative patterns resolve under /dev/serial/by-id/.
resolve_serial() {
    local pattern="$1"
    [[ "$pattern" == /* ]] || pattern="/dev/serial/by-id/$pattern"
    local -a matches
    shopt -s nullglob
    # shellcheck disable=SC2206
    matches=($pattern)
    shopt -u nullglob
    [ "${#matches[@]}" -gt 0 ] && echo "${matches[0]}"
}

# Katapult device, else its running-Klipper counterpart; never opens the port.
find_usb_device() {
    local pattern="$1" dev
    dev=$(resolve_serial "$pattern") && { echo "$dev"; return 0; }
    [[ "$pattern" == *Katapult_* ]] || return 1
    resolve_serial "${pattern/Katapult_/Klipper_}"
}

# Cached lsusb output - refreshed at the start of each scan_dfu_devices() call.
# Avoids spawning lsusb for every bootsel_present() check per discover() cycle.
_LSUSB_CACHE=""
_lsusb() {
    [ -z "$_LSUSB_CACHE" ] && _LSUSB_CACHE=$(lsusb 2>/dev/null)
    printf '%s\n' "$_LSUSB_CACHE"
}
bootsel_present() { _lsusb | grep -qi "ID $1 "; }

# Install a udev rule granting non-root access to STM32 DFU devices (0483:df11).
# One-time setup - subsequent runs skip if the rule file already exists.
_install_dfu_udev_rule() {
    local rule_file="/etc/udev/rules.d/99-blocks-dfu.rules"
    [ -f "$rule_file" ] && return 0
    info "Installing udev rule for DFU device access (one-time setup)..."
    # MODE=0664 + TAG uaccess: group-writable and accessible to the active login session.
    local rule='SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="df11", MODE="0664", GROUP="plugdev", TAG+="uaccess"'
    if sudo -n sh -c "printf '%s\n' '$rule' > '$rule_file' \
            && udevadm control --reload-rules \
            && udevadm trigger --subsystem-match=usb --action=add" 2>/dev/null; then
        ok "udev rule installed - DFU access no longer requires sudo"
        sleep 1 # allow udev to apply ACL to any currently-connected device
    else
        warn "Could not install udev rule (sudo -n failed) - DFU scan will use sudo"
    fi
}

flash_bootsel() {
    local name="$1" vid_pid="$2"
    info "Flashing [$name] via BOOTSEL (FLASH_DEVICE=$vid_pid)..."
    # Use a temp file - rp2040_flash may emit null bytes that corrupt bash
    # variables ($() truncates at \0), making grep on the variable unreliable.
    local _tmp
    _tmp=$(mktemp)
    make -C "$KLIPPER_DIR" "${FW_MAKE_ARGS[@]}" flash FLASH_DEVICE="$vid_pid" >"$_tmp" 2>&1
    local make_rc=$?
    cat "$_tmp" | _indent
    # rp2040_flash exits 0 even when no device is found; detect via output.
    # "Loaded UF2 image with 0 pages" appears on both success and failure - ignore it.
    if [ "$make_rc" -ne 0 ] ||
        grep -qi "No rp2040 in BOOTSEL mode was found" "$_tmp"; then
        rm -f "$_tmp"
        err "[$name] BOOTSEL flash failed (device not found or disconnected)"
        return 1
    fi
    rm -f "$_tmp"
    ok "[$name] flashed via BOOTSEL"
    return 0
}

DFU_SCAN_RESULT=""

# Populate DFU_SCAN_RESULT with one line per device+alt:
#   "vidpid|serial|alt|addr|mem_name"
scan_dfu_devices() {
    DFU_SCAN_RESULT=""
    _LSUSB_CACHE="" # refresh USB device list at the start of each scan
    command -v dfu-util >/dev/null 2>&1 || {
        warn "dfu-util not found - DFU scanning disabled"
        return 0
    }
    # Temp file: sudo must run as a direct command, not inside $() - nested subshells
    # break sudo credential/USB access on some systems. Stdout+stderr both captured
    # (2>&1) because some dfu-util/libusb builds emit "Found DFU:" to stderr.
    local list _dfu_tmp
    _dfu_tmp=$(mktemp)

    _dfu_scan_once() {
        dfu-util --list >"$_dfu_tmp" 2>&1 || true
        list=$(<"$_dfu_tmp")
        [[ "$list" == *"Found DFU:"* ]] && return 0
        sudo -n dfu-util --list >"$_dfu_tmp" 2>&1 || true
        list=$(<"$_dfu_tmp")
        [[ "$list" == *"Found DFU:"* ]]
    }

    _dfu_scan_once || {
        # Device in lsusb but not accessible - likely missing udev rule.
        if _lsusb | grep -qi "0483:df11"; then
            local _attempt
            for _attempt in 1 2 3; do
                info "DFU device visible in lsusb but not accessible by dfu-util (attempt $_attempt/3)..."
                [ "$_attempt" -eq 1 ] && _install_dfu_udev_rule || sleep 1
                _dfu_scan_once && break
            done
        fi
    }
    rm -f "$_dfu_tmp"
    [ -z "$list" ] && return 0
    while IFS= read -r line; do
        # Found DFU: [0483:df11] ver=..., alt=0, name="@Internal Flash   /0x08000000/8*128Kg", serial="305A35703231"
        [[ "$line" =~ ^Found\ DFU:\ \[([0-9a-fA-F:]+)\].*alt=([0-9]+).*name=\"([^\"]*)\".*serial=\"([^\"]*)\" ]] || continue
        local vidpid="${BASH_REMATCH[1]}" alt="${BASH_REMATCH[2]}" name="${BASH_REMATCH[3]}" serial="${BASH_REMATCH[4]}"
        local addr="0x08000000"
        [[ "$name" =~ /0x([0-9a-fA-F]+)/ ]] && addr="0x${BASH_REMATCH[1]}"
        DFU_SCAN_RESULT+="${vidpid}|${serial}|${alt}|${addr}|${name}"$'\n'
    done <<<"$list"
}

# Find first DFU device matching vid:pid and optional mem_name substring (alt=0 only).
# Outputs "serial|alt|addr" or empty string.
find_dfu_device() {
    local vidpid="$1" mem_pattern="${2:-}"
    [ -z "$DFU_SCAN_RESULT" ] && return 1
    echo "$DFU_SCAN_RESULT" | awk -F'|' -v vp="$vidpid" -v mp="$mem_pattern" '
        $1 == vp && $3 == "0" && (mp == "" || index($5, mp)) { print $2 "|" $3 "|" $4; exit }
    '
}

# Remove a claimed DFU serial from DFU_SCAN_RESULT so no other config can match it.
claim_dfu_serial() {
    local serial="$1"
    [ -z "$serial" ] && return 0
    local new=""
    while IFS= read -r line; do
        [[ "$line" == *"|${serial}|"* ]] && continue
        new+="${line}"$'\n'
    done <<<"$DFU_SCAN_RESULT"
    DFU_SCAN_RESULT="$new"
}

# Trigger MCU to DFU via CAN UUID, then wait up to 12s for it to appear in dfu-util.
# Outputs "serial|alt|addr" on success; returns 1 on timeout.
trigger_to_dfu() {
    local name="$1" uuid="$2" vidpid="$3" mem_pattern="${4:-}"
    info "Triggering [$name] to DFU via CAN (UUID: $uuid)..."
    trigger_can_bootloader "$uuid" >&2 || true
    info "Waiting for DFU device..."
    local i
    for ((i = 1; i <= 12; i++)); do
        sleep 1
        scan_dfu_devices
        local result
        result=$(find_dfu_device "$vidpid" "$mem_pattern")
        [ -n "$result" ] && echo "$result" && return 0
    done
    return 1
}

# Compare the first <size> bytes of flash at <addr> with <image>.
# Returns 0 match, 1 mismatch, 2 readback unavailable (e.g. read protection).
_dfu_readback_matches() {
    local readback="$1" image="$2" addr="$3"
    shift 3
    local output size
    size=$(stat -c%s "$image") || return 2
    rm -f "$readback"
    # -U refuses an existing file (O_EXCL), hence the rm above.
    output=$(sudo dfu-util "$@" -s "${addr}:${size}" -U "$readback" 2>&1) || {
        echo "$output" | tail -n 3 | _indent >&2
        return 2
    }
    [ -f "$readback" ] || return 2
    cmp -s "$image" "$readback"
}

# Return 0 if <serial> is on the DFU list, 1 if it is not, 2 if dfu-util --list failed.
_dfu_listed() {
    local serial="$1" list="$2" rc=0
    # Direct redirect, not $(): sudo USB access breaks in nested subshells.
    # shellcheck disable=SC2024 # root runs dfu-util only, the file is ours
    sudo dfu-util --list >"$list" 2>&1 || rc=2
    [ "$rc" -eq 0 ] && { grep -qF "serial=\"$serial\"" "$list" || rc=1; }
    rm -f "$list"
    return "$rc"
}

# Return 0 once <serial> drops off the DFU list, 1 if it is still there after the
# wait, 2 if dfu-util --list never answered (absence of the serial proves nothing).
_dfu_left() {
    local serial="$1" list="$2" _i _rc _seen=false
    for ((_i = 0; _i < ${DFU_LEAVE_WAIT:-5}; _i++)); do
        sleep 1
        _rc=0
        _dfu_listed "$serial" "$list" || _rc=$?
        [ "$_rc" -eq 1 ] && return 0
        [ "$_rc" -eq 0 ] && _seen=true
    done
    $_seen && return 1
    return 2
}

# Write <image> at <addr>, read it back, and leave DFU only once it matches.
# A :leave on the write would jump into an unverified image, so it is a separate
# command after the readback; a mismatch is rewritten while the ROM still runs.
# Returns 0 verified, 3 booted but unverified (no readback), 1 failed.
flash_dfu() {
    local name="$1" vidpid="$2" serial="$3" alt="${4:-0}" addr="${5:-0x08000000}"
    local image="${6:-$FW_BIN}" opts="${7:-}"
    local -a dev=(-d "$vidpid" -S "$serial" -a "$alt")
    local readback="${image%.bin}.readback.bin" list="${image%.bin}.dfu-list.txt"
    local output rc attempt verify try left
    for attempt in 1 2; do
        info "Flashing [$name] via DFU (serial: $serial, addr: $addr, attempt $attempt/2)..."
        rc=0
        output=$(sudo dfu-util "${dev[@]}" -s "${addr}${opts:+:$opts}" -D "$image" 2>&1) || rc=$?
        echo "$output" | _indent >&2
        if echo "$output" | grep -qiE "No DFU capable USB device|Cannot open DFU device|unable to open"; then
            err "[$name] DFU device not found (serial: $serial) - board not in DFU mode or disconnected"
            [ "$attempt" -gt 1 ] &&
                warn "  The first write may have left a partial image: power-cycle it into DFU mode and re-run."
            return 1
        fi
        if [ "$rc" -ne 0 ]; then
            warn "[$name] DFU write failed (exit $rc)"
            if ! _dfu_listed "$serial" "$list"; then
                err "[$name] MCU disconnected during the flash - reconnect and retry"
                warn "  The board may be in an unknown state. Power-cycle it and re-enter DFU mode before retrying."
                return 1
            fi
            continue
        fi
        info "Reading back [$name] to verify..."
        for try in 1 2; do
            verify=0
            _dfu_readback_matches "$readback" "$image" "$addr" "${dev[@]}" || verify=$?
            [ "$verify" -ne 2 ] && break
            [ "$try" -eq 1 ] && warn "[$name] readback failed - retrying it once"
        done
        [ "$verify" -eq 1 ] && {
            warn "[$name] readback does not match the image"
            continue
        }
        # Read protection keeps the board listed; a board gone from USB never booted our leave.
        if [ "$verify" -eq 2 ] && ! _dfu_listed "$serial" "$list"; then
            rm -f "$readback"
            err "[$name] board dropped off USB after the write - the image in flash is unverified"
            warn "  Power-cycle it into DFU mode and re-run."
            return 1
        fi
        [ "$verify" -eq 2 ] && warn "[$name] flash readback unavailable - leaving DFU with the write unverified"
        # Exit status is not checked: the ROM often resets before answering the request.
        sudo dfu-util "${dev[@]}" -s "${addr}:leave" 2>&1 | tail -n 2 | _indent >&2
        rm -f "$readback"
        left=0
        _dfu_left "$serial" "$list" || left=$?
        if [ "$left" -eq 2 ]; then
            warn "[$name] dfu-util --list failed - cannot confirm the board left DFU"
            warn "[$name] flashed via DFU, boot unconfirmed - the post-flash version check decides"
            return 3
        fi
        if [ "$left" -eq 1 ]; then
            err "[$name] still in DFU mode after the leave request"
            if [ "$verify" -eq 0 ]; then
                warn "  The image is verified - power-cycle the board to boot it."
            else
                warn "  Power-cycle the board; it boots the unverified image in flash."
            fi
            return 1
        fi
        if [ "$verify" -eq 0 ]; then
            ok "[$name] flashed via DFU, readback verified"
            return 0
        fi
        warn "[$name] flashed via DFU, readback unverified - the post-flash version check decides"
        return 3
    done
    err "[$name] DFU flash failed - the board is still in DFU mode, nothing was booted"
    warn "  Re-run to retry. A power cycle boots whatever is in flash, possibly a partial image."
    return 1
}

# Set DFU_VIDPID/DFU_MEM/DFU_ADDR/DFU_ALT/DFU_MCU_TYPE from a config's metadata.
dfu_params() {
    local cfg="$1" katapult_vid="" katapult_mem="" _key _val
    DFU_VIDPID="" DFU_MEM="" DFU_ADDR="0x08000000" DFU_ALT="0" DFU_MCU_TYPE=""
    while IFS='=' read -r _key _val; do
        case "$_key" in
        dfu) DFU_VIDPID="$_val" ;;
        dfu_mem) DFU_MEM="$_val" ;;
        dfu_addr) DFU_ADDR="$_val" ;;
        dfu_alt) DFU_ALT="$_val" ;;
        mcu_type) DFU_MCU_TYPE="$_val" ;;
        katapult_dfu) katapult_vid="$_val" ;;
        katapult_dfu_mem) katapult_mem="$_val" ;;
        esac
    done < <(parse_config_metadata "$cfg")
    # No dfu: header (e.g. a CAN toolhead): Katapult holds the start of flash.
    if [ -z "$DFU_VIDPID" ] && [ -n "$katapult_vid" ]; then
        DFU_VIDPID="$katapult_vid"
        DFU_MEM="${katapult_mem:-$DFU_MEM}"
        local app_addr
        app_addr=$(grep -oP 'CONFIG_FLASH_APPLICATION_ADDRESS=\K0x[0-9a-fA-F]+' "$cfg" 2>/dev/null || true)
        [ -n "$app_addr" ] && DFU_ADDR="$app_addr"
    fi
    return 0
}

parse_config_metadata() {
    local cfg="$1"
    while IFS= read -r line; do
        [[ "$line" =~ ^[[:space:]]*# ]] || break
        [[ "$line" =~ ^#[[:space:]]*([a-z_]+):[[:space:]]*(.+) ]] || continue
        local key="${BASH_REMATCH[1]}" val="${BASH_REMATCH[2]}"
        case "$key" in
        serial | dfu_mem | katapult_dfu_mem | klipper_section | linux)
            val="${val%"${val##*[![:space:]]}"}"
            ;;
        mcu_type | bootsel | dfu | dfu_addr | dfu_alt | katapult_bootsel | katapult_dfu)
            val="${val// /}"
            ;;
        *) continue ;;
        esac
        echo "${key}=${val}"
    done <"$cfg"
}

# Build <src> with <cfg> into $FW_BUILD_ROOT/<tag>; sets FW_OUT and FW_MAKE_ARGS.
_make_build() {
    local src="$1" cfg="$2" tag="$3" err_msg="$4"
    local dir="$FW_BUILD_ROOT/$tag"
    mkdir -p "$dir" || return 1
    cp "$cfg" "$dir/.config" || return 1
    [[ "$dir" == "$FW_BUILD_ROOT"/?* ]] && rm -rf "${dir:?}/out"
    FW_OUT="$dir/out/"
    FW_MAKE_ARGS=("KCONFIG_CONFIG=$dir/.config" "OUT=$FW_OUT")
    make -C "$src" "${FW_MAKE_ARGS[@]}" -s olddefconfig 2>&1 | _indent
    if [ "${PIPESTATUS[0]}" -eq 0 ]; then
        make -C "$src" "${FW_MAKE_ARGS[@]}" -j"$(nproc)" -s 2>&1 | _indent
        [ "${PIPESTATUS[0]}" -eq 0 ] && return 0
    fi
    err "$err_msg"
    return 1
}

is_linux_config() { grep -q '^CONFIG_MACH_LINUX=y' "$1"; }

build_firmware() {
    local cfg="$1" name="$2" iface="$3"
    info "Building firmware for [$name] ($iface)..."
    _make_build "$KLIPPER_DIR" "$cfg" "$name" "Build failed for [$name]" || return 1
    use_build "$name" "$cfg"
    if [ ! -f "$FW_BIN" ]; then
        err "Build completed but $(basename "$FW_BIN") not found in $FW_OUT"
        warn "Files in out/: $(ls "$FW_OUT" 2>/dev/null || echo '(empty)')"
        return 1
    fi
    ok "Firmware built ($FW_OUT)"
}

# Point FW_OUT/FW_MAKE_ARGS/FW_BIN at the build_firmware output for <name>.
use_build() {
    local name="$1" cfg="$2" dir="$FW_BUILD_ROOT/$1"
    FW_OUT="$dir/out/"
    FW_MAKE_ARGS=("KCONFIG_CONFIG=$dir/.config" "OUT=$FW_OUT")
    FW_BIN="${FW_OUT}klipper.bin"
    is_linux_config "$cfg" && FW_BIN="${FW_OUT}klipper.elf"
    return 0
}

# Refuse a build that cannot boot, lands at the wrong address, or changes how the
# host reaches the MCU: chip, CAN/USB/crystal pins and bridge mode versus the running
# MCU, crystal frequency versus the last flashed .config (the MCU does not report it).
preflight_firmware() {
    local name="$1" iface="$2" cfg="$3" rc=0 section
    is_linux_config "$cfg" && return 0
    local -a at=()
    if [ "$iface" = "dfu" ]; then
        dfu_params "$cfg"
        at=(--at "$DFU_ADDR")
    fi
    local check_rc=0
    python3 "$PREFLIGHT_PY" image --config "$FW_BUILD_ROOT/$name/.config" \
        --image "$FW_BIN" "${at[@]}" || check_rc=$?
    case "$check_rc" in
    0) ;;
    4) err "[$name] image check could not run - not flashing"; return 1 ;;
    *) err "[$name] built image failed its sanity checks - not flashing"; return 1 ;;
    esac
    local flashed="$FW_BUILD_ROOT/$name.flashed.config"
    if [ -f "$flashed" ]; then
        python3 "$PREFLIGHT_PY" flashed --new "$FW_BUILD_ROOT/$name/.config" \
            --flashed "$flashed" || check_rc=$?
        case "$check_rc" in
        0) ;;
        4) err "[$name] crystal check could not run - not flashing"; return 1 ;;
        *) rc=1 ;;
        esac
    fi
    section=$(parse_config_metadata "$cfg" | sed -n 's/^klipper_section=//p')
    if [ "$CONTEXT" = "pi" ] && [ -n "$section" ]; then
        local comms_rc=0
        python3 "$PREFLIGHT_PY" comms --dict "${FW_OUT}klipper.dict" --section "$section" \
            --url "$MOONRAKER_URL" || comms_rc=$?
        case "$comms_rc" in
        0) ;;
        3) warn "[$name] no running firmware to compare - comms settings unchecked" ;;
        # An internal error is no comms change, so --allow-comms-change must not cover it.
        4) err "[$name] comms check could not run - not flashing"; return 1 ;;
        *) rc=1 ;;
        esac
    fi
    [ "$rc" -eq 0 ] && return 0
    if $ALLOW_COMMS_CHANGE; then
        warn "[$name] comms settings change accepted (--allow-comms-change)"
        return 0
    fi
    err "[$name] the new build changes how the host reaches this MCU - not flashing"
    err "  If intended, re-run with --allow-comms-change, with physical access to the board."
    return 1
}

# Sets FW_OUT/FW_MAKE_ARGS to the Katapult build.
build_katapult_firmware() {
    local name="$1" katapult_cfg="$2"
    info "Building Katapult for [$name]..."
    _make_build "$KATAPULT_DIR" "$katapult_cfg" "$name.katapult" \
        "Katapult build failed for [$name]" || return 1
    # A Katapult that disagrees with the app on pins or clock is unreachable once flashed.
    if ! python3 "$PREFLIGHT_PY" pair --klipper "$FW_BUILD_ROOT/$name/.config" \
        --katapult "$FW_BUILD_ROOT/$name.katapult/.config"; then
        err "[$name] Katapult config does not match the Klipper config - not flashing"
        return 1
    fi
    ok "Katapult built"
}

# Wait up to $timeout seconds for a Katapult node UUID to appear on CAN.
wait_for_katapult_node() {
    local uuid="$1" timeout="${2:-20}"
    info "Waiting for [$uuid] as Katapult node (up to ${timeout}s)..."
    local i
    for ((i = 1; i <= timeout; i++)); do
        sleep 1
        bootloader_uuids | grep -qF "$uuid" && {
            ok "[$uuid] online as Katapult"
            return 0
        }
    done
    err "[$uuid] did not appear as Katapult node within ${timeout}s"
    return 1
}

# Build and flash Katapult onto an MCU that has no Katapult bootloader.
# Requires a USB cable from the MCU to the Pi; if absent, prints instructions.
bootstrap_katapult() {
    local name="$1" cfg="$2"
    local katapult_bootsel="" katapult_dfu="" katapult_dfu_mem=""
    while IFS='=' read -r _k _v; do
        case "$_k" in
        katapult_bootsel) katapult_bootsel="$_v" ;;
        katapult_dfu) katapult_dfu="$_v" ;;
        katapult_dfu_mem) katapult_dfu_mem="$_v" ;;
        esac
    done < <(parse_config_metadata "$cfg")

    local katapult_cfg="$MCU_CONFIG_DIR/${name}.katapult.config"
    if [ ! -f "$katapult_cfg" ]; then
        warn "[$name] no Katapult config ($katapult_cfg) - cannot bootstrap"
        warn "  Build Katapult manually and flash via BOOTSEL/DFU, then re-run."
        return 1
    fi
    if [ -z "$katapult_bootsel" ] && [ -z "$katapult_dfu" ]; then
        warn "[$name] no katapult_bootsel/katapult_dfu declared in config - cannot bootstrap"
        return 1
    fi

    # Build first: a board found in DFU/BOOTSEL is flashed at once, not left waiting.
    build_katapult_firmware "$name" "$katapult_cfg" || return 1

    if [ -n "$katapult_bootsel" ]; then
        info "[$name] waiting for BOOTSEL device ($katapult_bootsel, up to 8s)..."
        local i
        for ((i = 1; i <= 8; i++)); do
            bootsel_present "$katapult_bootsel" && break
            sleep 1
        done
        if ! bootsel_present "$katapult_bootsel"; then
            warn "[$name] BOOTSEL device ($katapult_bootsel) not found after 8s"
            warn "  Connect a USB cable from [$name] to the Pi and re-run."
            return 1
        fi
        info "Flashing Katapult on [$name] via BOOTSEL..."
        local _kat_tmp _kat_rc
        _kat_tmp=$(mktemp)
        make -C "$KATAPULT_DIR" "${FW_MAKE_ARGS[@]}" flash FLASH_DEVICE="$katapult_bootsel" \
            >"$_kat_tmp" 2>&1
        _kat_rc=$?
        cat "$_kat_tmp" | _indent
        # rp2040_flash exits 0 even when no device is found - check output too.
        if [ "$_kat_rc" -ne 0 ] ||
            grep -qi "No rp2040 in BOOTSEL mode was found" "$_kat_tmp"; then
            rm -f "$_kat_tmp"
            err "[$name] Katapult BOOTSEL flash failed (device not found or disconnected)"
            return 1
        fi
        rm -f "$_kat_tmp"
        ok "Katapult installed on [$name]"
        sleep 2
        return 0
    fi

    if [ -n "$katapult_dfu" ]; then
        local boot_addr
        boot_addr=$(grep -oP '^CONFIG_FLASH_BOOT_ADDRESS=\K0x[0-9a-fA-F]+' \
            "$FW_BUILD_ROOT/$name.katapult/.config" || echo 0x08000000)
        python3 "$PREFLIGHT_PY" image --config "$FW_BUILD_ROOT/$name.katapult/.config" \
            --image "${FW_OUT}katapult.bin" --at "$boot_addr" --bootloader || {
            err "[$name] Katapult image failed its sanity checks - not flashing"
            return 1
        }
        info "[$name] waiting for DFU device ($katapult_dfu, up to 8s)..."
        local i dfu_result=""
        for ((i = 1; i <= 8; i++)); do
            scan_dfu_devices
            dfu_result=$(find_dfu_device "$katapult_dfu" "$katapult_dfu_mem")
            [ -n "$dfu_result" ] && break
            sleep 1
        done
        if [ -z "$dfu_result" ]; then
            warn "[$name] DFU device ($katapult_dfu) not found after 8s"
            warn "  Connect a USB cable from [$name] to the Pi and re-run."
            return 1
        fi
        local dfu_serial="${dfu_result%%|*}"
        # Mass erase drops the old app, so Katapult stays in its bootloader for the CAN flash.
        local _dfu_rc=0
        flash_dfu "$name Katapult" "$katapult_dfu" "$dfu_serial" 0 "$boot_addr" \
            "${FW_OUT}katapult.bin" "mass-erase:force" || _dfu_rc=$?
        # Unverified (3) is fine here: the caller waits for Katapult to answer on CAN.
        if [ "$_dfu_rc" -eq 0 ] || [ "$_dfu_rc" -eq 3 ]; then
            ok "Katapult installed on [$name]"
            sleep 2
            return 0
        fi
        err "[$name] Katapult DFU flash failed"
        return 1
    fi
}

flash_can() {
    local name="$1" uuid="$2"
    info "Flashing [$name] via CAN (UUID: $uuid)..."
    local _output _rc=0
    _output=$(python3 "$KATAPULT_SCRIPT" -i "$CAN_INTERFACE" -u "$uuid" \
        -f "$FW_BIN" 2>&1 | tr -d '\0')
    _rc=${PIPESTATUS[0]}
    echo "$_output" | _indent >&2
    if [ "$_rc" -eq 0 ]; then
        ok "[$name] flashed via CAN"
        return 0
    fi
    # Return 2 specifically for "no Katapult" so cmd_flash can attempt auto-bootstrap.
    echo "$_output" | grep -q "Error sending command \[CONNECT\]" && return 2
    err "[$name] CAN flash failed"
    return 1
}

flash_usb() {
    local name="$1" serial="$2"
    if $KATAPULT_OK; then
        info "Flashing [$name] via USB ($serial)..."
        python3 "$KATAPULT_SCRIPT" -d "$serial" \
            -f "$FW_BIN" 2>&1 | _indent
        if [ "${PIPESTATUS[0]}" -eq 0 ]; then
            ok "[$name] flashed via USB"
            return 0
        fi
        warn "Katapult USB failed - falling back to klipper make flash"
    fi
    info "Flashing [$name] via klipper make flash ($serial)..."
    make -C "$KLIPPER_DIR" "${FW_MAKE_ARGS[@]}" flash FLASH_DEVICE="$serial" 2>&1 | _indent
    if [ "${PIPESTATUS[0]}" -eq 0 ]; then
        ok "[$name] flashed via klipper make flash"
        return 0
    fi
    err "[$name] all flash methods failed"
    return 1
}

# Install the Linux host MCU via Klipper's flash-linux.sh (restarts the service).
flash_linux() {
    local name="$1" svc="$2"
    info "Installing [$name] Linux MCU ($svc)..."
    make -C "$KLIPPER_DIR" "${FW_MAKE_ARGS[@]}" flash 2>&1 | _indent
    if [ "${PIPESTATUS[0]}" -eq 0 ]; then
        ok "[$name] installed, $svc restarted"
        return 0
    fi
    err "[$name] Linux MCU install failed"
    return 1
}

# Scans CAN bus (Pi context only), DFU devices, USB/BOOTSEL, then matches each
# mcu_config/*.config to a detected device.
#
# Populates global DISCOVERED[] - one entry per config file.
# Entry format: "name|iface|id|cfg|fw_ver|detected"
#   iface:    can | usb | dfu | bootsel | linux | none  (declared interface type)
#   id:       UUID (CAN), serial path (USB), VID:PID (BOOTSEL), service (linux), or empty
#   fw_ver:   running firmware version string, or empty if unknown/not detected
#   detected: true | false
declare -a DISCOVERED=()
SRC_VERSION=""
CAN_AVAILABLE=false

discover() {
    DISCOVERED=()
    CAN_AVAILABLE=false
    _LSUSB_CACHE=""
    local -A uuid_to_mcu=()
    local -A uuid_to_version=()

    [ -z "$SRC_VERSION" ] && SRC_VERSION=$(get_source_version)
    local src_hash
    src_hash=$(extract_git_hash "$SRC_VERSION")
    info "Klipper source: ${SRC_VERSION:-unknown}  (hash: ${src_hash:-?})"

    if [ "$CONTEXT" = "pi" ]; then
        header "Querying MCU firmware versions..."
        ensure_klipper_running
        query_moonraker_versions && write_versions_file --quiet
    fi

    # Reverse UUID cache, used by CAN step 2.
    local -A _uuid_cache_rev=() _mcu_type_to_uuid=()
    for _ct in "${!UUID_CACHE_MAP[@]}"; do
        _uuid_cache_rev["${UUID_CACHE_MAP[$_ct]}"]="$_ct"
    done

    header "Scanning DFU devices..."
    scan_dfu_devices

    if [ "$CONTEXT" = "pi" ]; then
        header "Scanning CAN bus ($CAN_INTERFACE)..."
        if ensure_can_up; then
            CAN_AVAILABLE=true

            # Build set of bridge mcu_types - triggering them drops can0, so skip.
            local -A bridge_types=()
            for cfg_b in "$MCU_CONFIG_DIR"/*.config; do
                [[ "$(basename "$cfg_b")" == .* || "$cfg_b" == *.katapult.config ]] && continue
                is_canbus_bridge "$cfg_b" || continue
                while IFS='=' read -r key val; do
                    [ "$key" = "mcu_type" ] && bridge_types["$val"]=1
                done < <(parse_config_metadata "$cfg_b")
            done

            # 1) Katapult bootloader query (devices in bootloader mode).
            local boot_uuids=""
            if $KATAPULT_OK; then
                boot_uuids=$(bootloader_uuids)
                for uuid in $boot_uuids; do
                    info "Probing UUID $uuid..."
                    local probe_result mcu_type fw_version
                    probe_result=$(probe_can_mcu "$uuid")
                    mcu_type="${probe_result%%|*}"
                    fw_version="${probe_result##*|}"
                    if [ -n "$mcu_type" ]; then
                        uuid_to_mcu["$uuid"]="$mcu_type"
                        uuid_to_version["$uuid"]="$fw_version"
                        UUID_CACHE_MAP["$mcu_type"]="$uuid"
                        _uuid_cache_rev["$uuid"]="$mcu_type"
                        ok "UUID $uuid -> $mcu_type  (in Katapult)"
                    fi
                done
            fi

            # 2) Klipper CAN query - discovers ALL CAN nodes (running + bootloader).
            #    For UUIDs already known from step 1, skip.  For new UUIDs, resolve
            #    mcu_type from the UUID cache (populated from printer.cfg or prior runs).
            local klipper_line klipper_uuid klipper_app
            while IFS='|' read -r klipper_uuid klipper_app; do
                [ -z "$klipper_uuid" ] && continue
                [ -n "${uuid_to_mcu[$klipper_uuid]+_}" ] && continue # already known
                # Skip bridge MCUs (resolved via cache reverse lookup).
                local _skip_bridge=false
                for _bt in "${!bridge_types[@]}"; do
                    [[ "${UUID_CACHE_MAP[$_bt]:-}" == "$klipper_uuid" ]] && _skip_bridge=true && break
                done
                $_skip_bridge && continue

                # Resolve mcu_type from cache via reverse map (O(1) lookup).
                local resolved_type="${_uuid_cache_rev[$klipper_uuid]:-}"

                if [ -n "$resolved_type" ]; then
                    uuid_to_mcu["$klipper_uuid"]="$resolved_type"
                    uuid_to_version["$klipper_uuid"]=""
                    info "[$resolved_type] UUID $klipper_uuid - ${klipper_app:-running}"
                else
                    # Unknown UUID - try Katapult probe if in bootloader, else log it.
                    if [[ "${klipper_app:-}" == *Katapult* ]] && $KATAPULT_OK; then
                        local probe_r probe_t probe_v
                        probe_r=$(probe_can_mcu "$klipper_uuid")
                        probe_t="${probe_r%%|*}"
                        probe_v="${probe_r##*|}"
                        if [ -n "$probe_t" ]; then
                            uuid_to_mcu["$klipper_uuid"]="$probe_t"
                            uuid_to_version["$klipper_uuid"]="$probe_v"
                            UUID_CACHE_MAP["$probe_t"]="$klipper_uuid"
                            ok "UUID $klipper_uuid -> $probe_t  fw: ${probe_v:-unknown}"
                            continue
                        fi
                    fi
                    warn "UUID $klipper_uuid - ${klipper_app:-unknown app}, mcu_type unknown (not in cache)"
                fi
            done < <(klipper_can_query)

            # 3) Register remaining cached UUIDs not yet seen (running, no CAN query match).
            #    Skip bridge MCUs (handled by DFU path).
            for mcu_type in "${!UUID_CACHE_MAP[@]}"; do
                [ "${bridge_types[$mcu_type]+_}" ] && continue
                local cached_uuid="${UUID_CACHE_MAP[$mcu_type]}"
                [ -n "${uuid_to_mcu[$cached_uuid]+_}" ] && continue # already registered
                uuid_to_mcu["$cached_uuid"]="$mcu_type"
                uuid_to_version["$cached_uuid"]=""
                info "[$mcu_type] UUID $cached_uuid - running (from cache)"
            done
        fi # ensure_can_up
    fi

    for _u in "${!uuid_to_mcu[@]}"; do
        _mcu_type_to_uuid["${uuid_to_mcu[$_u]}"]="$_u"
    done

    header "Matching configs to detected devices..."
    local -a _katapult_deferred=()
    shopt -s nullglob
    for cfg in "$MCU_CONFIG_DIR"/*.config; do
        [[ "$(basename "$cfg")" == .* || "$cfg" == *.katapult.config ]] && continue
        local name
        name=$(basename "$cfg" .config)

        local can_mcu_type="" usb_serial_pattern="" bootsel_id=""
        local dfu_vidpid="" dfu_mem="" dfu_addr="0x08000000" dfu_alt="0"
        local katapult_dfu="" katapult_dfu_mem="" klipper_section="" linux_svc=""
        while IFS='=' read -r key val; do
            case "$key" in
            mcu_type) can_mcu_type="$val" ;;
            serial) usb_serial_pattern="$val" ;;
            bootsel) bootsel_id="$val" ;;
            dfu) dfu_vidpid="$val" ;;
            dfu_mem) dfu_mem="$val" ;;
            dfu_addr) dfu_addr="$val" ;;
            dfu_alt) dfu_alt="$val" ;;
            katapult_dfu) katapult_dfu="$val" ;;
            katapult_dfu_mem) katapult_dfu_mem="$val" ;;
            klipper_section) klipper_section="$val" ;;
            linux) linux_svc="$val" ;;
            esac
        done < <(parse_config_metadata "$cfg")

        # Live firmware version from Moonraker (if available)
        local moonraker_ver=""
        [ -n "$klipper_section" ] && moonraker_ver="${MOONRAKER_VERSIONS[$klipper_section]:-}"

        local added=false

        # Physical DFU - loop through ALL matching devices so that multiple boards are listed
        if [ -n "$dfu_vidpid" ]; then
            local dfu_result
            dfu_result=$(find_dfu_device "$dfu_vidpid" "$dfu_mem")
            while [ -n "$dfu_result" ]; do
                local dfu_serial="${dfu_result%%|*}"
                # No readable firmware version in DFU mode -> always flash (like BOOTSEL)
                DISCOVERED+=("$name|dfu|$dfu_serial|$cfg||true")
                ok "[$name] matched DFU (physical)  serial=$dfu_serial"
                claim_dfu_serial "$dfu_serial"
                added=true
                dfu_result=$(find_dfu_device "$dfu_vidpid" "$dfu_mem")
            done
        fi

        # Physical BOOTSEL - each physical device is checked independently so that
        # multiple boards of the same type (e.g. two eddy_duo, one via CAN and one
        # in BOOTSEL mode) both appear as separate rows.
        if [ -n "$bootsel_id" ] && bootsel_present "$bootsel_id"; then
            DISCOVERED+=("$name|bootsel|$bootsel_id|$cfg||true")
            ok "[$name] matched BOOTSEL  vid:pid=$bootsel_id"
            added=true
        fi

        if [ -n "$usb_serial_pattern" ]; then
            local resolved
            # flashtool on a usb-Klipper port reboots it into the bootloader.
            resolved=$(find_usb_device "$usb_serial_pattern") || true
            if [ -n "$resolved" ]; then
                DISCOVERED+=("$name|usb|$resolved|$cfg|$moonraker_ver|true")
                ok "[$name] matched USB  serial=$resolved"
                added=true
            fi
        fi

        # CAN lookup via pre-built reverse map.
        if [ -n "$can_mcu_type" ] && [ "$CONTEXT" = "pi" ]; then
            local matched_uuid="${_mcu_type_to_uuid[$can_mcu_type]:-}"
            if [ -n "$matched_uuid" ]; then
                local _fwv="${uuid_to_version[$matched_uuid]:-$moonraker_ver}"
                DISCOVERED+=("$name|can|$matched_uuid|$cfg|$_fwv|true")
                ok "[$name] matched CAN  mcu_type=$can_mcu_type  uuid=$matched_uuid"
                added=true
            fi
        fi

        if [ -n "$linux_svc" ] && ! $added && [ "$CONTEXT" = "pi" ] &&
            { systemctl cat "$linux_svc" >/dev/null 2>&1 || [ -x /usr/local/bin/klipper_mcu ]; }; then
            DISCOVERED+=("$name|linux|$linux_svc|$cfg|$moonraker_ver|true")
            ok "[$name] matched Linux MCU  service=$linux_svc"
            added=true
        fi

        # DFU triggerable - no physical DFU device present yet, but UUID is cached
        # so we can trigger it via CAN at flash time (or the user can use BOOT0+RESET).
        if [ -n "$dfu_vidpid" ] && ! $added &&
            [ -n "$can_mcu_type" ] && [ -n "${UUID_CACHE_MAP[$can_mcu_type]:-}" ] &&
            [ "$CONTEXT" = "pi" ]; then
            DISCOVERED+=("$name|dfu||$cfg|$moonraker_ver|true")
            if $CAN_AVAILABLE; then
                info "[$name] DFU-triggerable via CAN (UUID: ${UUID_CACHE_MAP[$can_mcu_type]})"
            else
                info "[$name] DFU-triggerable (UUID cached; CAN not up - will try at flash time or hold BOOT0+RESET)"
            fi
            added=true
        fi

        # Katapult DFU fallback - deferred to second pass so that primary
        # dfu+dfu_mem matches (more specific) claim devices first.
        local _deferred=false
        if [ -n "$katapult_dfu" ] && ! $added; then
            # Store can_mcu_type so the second pass can determine iface without grep.
            _katapult_deferred+=("$name|$katapult_dfu|$katapult_dfu_mem|$cfg|$moonraker_ver|$can_mcu_type")
            _deferred=true
        fi

        # Not detected - add entry so TUI shows it grayed out.
        # Report the highest-priority declared interface (CAN > DFU > USB > BOOTSEL).
        if ! $added && ! $_deferred; then
            local iface="none"
            [ -n "$linux_svc" ] && iface="linux"
            [ -n "$bootsel_id" ] && iface="bootsel"
            [ -n "$usb_serial_pattern" ] && iface="usb"
            [ -n "$dfu_vidpid" ] && iface="dfu"
            [ -n "$can_mcu_type" ] && iface="can"
            DISCOVERED+=("$name|$iface||$cfg||false")
            warn "[$name] not detected (declared interface: $iface)"
        fi
    done

    # Second pass: katapult_dfu fallback for configs that weren't matched above.
    # Runs after primary dfu+dfu_mem matches have claimed their devices.
    for _kd_entry in "${_katapult_deferred[@]}"; do
        local _kd_name _kd_vidpid _kd_mem _kd_cfg _kd_moonver _kd_can_mcu_type
        IFS='|' read -r _kd_name _kd_vidpid _kd_mem _kd_cfg _kd_moonver _kd_can_mcu_type <<<"$_kd_entry"
        # Check this config wasn't matched by a later (non-katapult) path
        local _already=false
        for entry in "${DISCOVERED[@]}"; do
            local _en
            IFS='|' read -r _en _ _ _ _ _ <<<"$entry"
            [[ "$_en" == "$_kd_name" ]] && _already=true && break
        done
        $_already && continue
        local dfu_result
        dfu_result=$(find_dfu_device "$_kd_vidpid" "$_kd_mem")
        if [ -n "$dfu_result" ]; then
            while [ -n "$dfu_result" ]; do
                local dfu_serial="${dfu_result%%|*}"
                DISCOVERED+=("$_kd_name|dfu|$dfu_serial|$_kd_cfg|$_kd_moonver|true")
                ok "[$_kd_name] matched DFU (katapult_dfu)  serial=$dfu_serial"
                claim_dfu_serial "$dfu_serial"
                dfu_result=$(find_dfu_device "$_kd_vidpid" "$_kd_mem")
            done
        else
            # Determine iface from stored metadata (no grep needed).
            local iface="none"
            [ -n "$_kd_can_mcu_type" ] && iface="can"
            [ -n "$_kd_vidpid" ] && iface="dfu"
            DISCOVERED+=("$_kd_name|$iface||$_kd_cfg||false")
            warn "[$_kd_name] not detected (declared interface: $iface)"
        fi
    done

    shopt -u nullglob
}

json_str() { printf '"%s"' "${1//\"/\\\"}"; }
json_bool() { [ "$1" = "true" ] && printf 'true' || printf 'false'; }
json_null_or_str() { [ -z "$1" ] && printf 'null' || json_str "$1"; }

# Emits a JSON object to stdout describing all discovered MCUs.
# On klipper dir missing: emits JSON error object, exits 1.
cmd_list_json() {
    if [ ! -d "$KLIPPER_DIR" ]; then
        printf '{"error":%s,"context":%s,"mcus":[]}\n' \
            "$(json_str "klipper dir not found: $KLIPPER_DIR")" \
            "$(json_str "$CONTEXT")"
        exit 1
    fi

    discover 2>/dev/null # suppress human-readable output

    local mcu_array="" first=true
    for entry in "${DISCOVERED[@]}"; do
        IFS='|' read -r name iface id cfg fw_ver detected <<<"$entry"

        local needs_update="null"
        if [ "$detected" = "true" ]; then
            if versions_match "$fw_ver" "$SRC_VERSION"; then
                needs_update="false"
            else
                needs_update="true"
            fi
        fi

        local iface_json section=""
        [ "$iface" = "none" ] && iface_json="null" || iface_json=$(json_str "$iface")
        while IFS='=' read -r key val; do
            [ "$key" = "klipper_section" ] && section="$val"
        done < <(parse_config_metadata "$cfg")

        [ "$first" = "true" ] && first=false || mcu_array+=","
        mcu_array+=$(printf '\n    {"name":%s,"config":%s,"interface":%s,"detected":%s,"id":%s,"current_version":%s,"source_version":%s,"needs_update":%s,"klipper_section":%s}' \
            "$(json_str "$name")" \
            "$(json_str "$cfg")" \
            "$iface_json" \
            "$(json_bool "$detected")" \
            "$(json_null_or_str "$id")" \
            "$(json_null_or_str "$fw_ver")" \
            "$(json_str "$SRC_VERSION")" \
            "$needs_update" \
            "$(json_null_or_str "$section")")
    done

    printf '{"context":%s,"source_version":%s,"versions_file":%s,"mcus":[%s\n]}\n' \
        "$(json_str "$CONTEXT")" \
        "$(json_str "$SRC_VERSION")" \
        "$(json_str "$MCU_VERSIONS_FILE")" \
        "$mcu_array"
}

_summary_box() {
    local title="$1"
    echo "" >&2
    _box_top
    _box_line "${BOLD}${title}${RESET}"
    _box_sep
    local _item
    for _item in "${flashed[@]}"; do _box_line "  ${GREEN}[OK]${RESET} $_item"; done
    for _item in "${skipped_utd[@]}"; do _box_line "  ${CYAN}[->]${RESET} $_item"; done
    for _item in "${skipped_missing[@]}"; do _box_line "  ${YELLOW}[!!]${RESET} $_item - not found"; done
    for _item in "${failed[@]}"; do _box_line "  ${RED}[XX]${RESET} $_item"; done
    _box_bottom
}

# Warn on host under-voltage: a brown-out mid-transfer leaves a board half-written.
check_host_power() {
    command -v vcgencmd >/dev/null 2>&1 || return 0
    local throttled
    throttled=$(vcgencmd get_throttled 2>/dev/null) || return 0
    throttled="${throttled#*=}"
    [[ "$throttled" =~ ^0x[0-9a-fA-F]+$ ]] || return 0
    # Bit 0 = under-voltage now (Raspberry Pi vcgencmd get_throttled docs).
    if ((throttled & 0x1)); then
        warn "Host is under-voltage now (get_throttled=$throttled) - check the PSU before flashing"
    fi
    return 0
}

# Returns 0 if the config file is a USB-CAN bridge firmware (must flash last).
is_canbus_bridge() { grep -q "^CONFIG_USBCANBUS=y" "$1"; }

# Flashes MCUs from DISCOVERED[].
# FLASH_NAMES[] - if non-empty, only flash named MCUs; otherwise all outdated.
# FORCE=true     - bypass version check.
# Bridge MCUs (CONFIG_USBCANBUS=y) are always flashed last - they provide can0;
# flashing them first would drop the CAN bus mid-session.
declare -a FLASH_NAMES=()
FORCE=false
ALLOW_COMMS_CHANGE=false # flash even if the build changes CAN/USB/clock settings
FLASH_ORDER_LOCKED=false # true when TUI user explicitly set the order

cmd_flash() {
    local -a to_flash=()
    flashed=() failed=() skipped_utd=() skipped_missing=()

    # When FLASH_NAMES is set, iterate in FLASH_NAMES order (preserves user ordering).
    # Use a consume-from-remaining approach so that multiple entries with the same
    # name (e.g. two octopus boards both in DFU) each match a distinct DISCOVERED row.
    local -a iterate_list=()
    if [ ${#FLASH_NAMES[@]} -gt 0 ]; then
        local -a _remaining=("${DISCOVERED[@]}")
        for req in "${FLASH_NAMES[@]}"; do
            local _idx=0
            for entry in "${_remaining[@]}"; do
                local _n
                IFS='|' read -r _n _ _ _ _ _ <<<"$entry"
                if [[ "${_n,,}" == "${req,,}" ]]; then
                    iterate_list+=("$entry")
                    unset '_remaining[$_idx]'
                    _remaining=("${_remaining[@]}")
                    break
                fi
                ((_idx++))
            done
        done
    else
        iterate_list=("${DISCOVERED[@]}")
    fi

    for entry in "${iterate_list[@]}"; do
        IFS='|' read -r name iface id cfg fw_ver detected <<<"$entry"

        if [ "$detected" = "false" ]; then
            warn "[$name] not detected - skipping"
            skipped_missing+=("$name")
            continue
        fi

        # Version check (skip BOOTSEL - no readable version; always flash)
        # When user explicitly selected MCUs (FLASH_NAMES non-empty), honour the
        # selection and flash even if already up to date - same as --force.
        if ! $FORCE && [ ${#FLASH_NAMES[@]} -eq 0 ] && [ "$iface" != "bootsel" ] && versions_match "$fw_ver" "$SRC_VERSION"; then
            skip "[$name ($iface)] already up to date - skipping"
            skipped_utd+=("$name ($iface)")
            continue
        fi

        to_flash+=("$entry")
    done

    if [ ${#to_flash[@]} -eq 0 ]; then
        _summary_box "Nothing to flash"
        save_uuid_cache
        return 0
    fi

    # Re-order: bridge MCUs (USB-CAN) last - unless user explicitly set the order.
    if ! $FLASH_ORDER_LOCKED; then
        local -a normal_mcus=() bridge_mcus=()
        for entry in "${to_flash[@]}"; do
            IFS='|' read -r _ _ _ cfg _ _ <<<"$entry"
            if is_canbus_bridge "$cfg"; then
                bridge_mcus+=("$entry")
            else
                normal_mcus+=("$entry")
            fi
        done
        [ ${#bridge_mcus[@]} -gt 0 ] &&
            info "Bridge MCUs will flash last (can0 dependency): $(printf '[%s] ' "${bridge_mcus[@]%%|*}")"
        to_flash=("${normal_mcus[@]}" "${bridge_mcus[@]}")
    fi

    if [ "$CONTEXT" = "pi" ]; then
        local print_state
        print_state=$(python3 "$VERSIONS_PY" print-state --url "$MOONRAKER_URL") || true
        if [[ "$print_state" == "printing" || "$print_state" == "paused" ]]; then
            err "A print is $print_state - flashing would stop Klipper mid-print. Aborting."
            return 1
        fi
    fi

    # Build and check everything while Klipper still runs: a bad build touches no MCU,
    # the running constants are still readable, and no board waits in DFU for a compile.
    header "Building firmware..."
    local -a _ready=()
    local -A _built=()
    for entry in "${to_flash[@]}"; do
        IFS='|' read -r name iface id cfg fw_ver detected <<<"$entry"
        if [ -z "${_built[$name]:-}" ]; then
            build_firmware "$cfg" "$name" "$iface" && _built[$name]=1 || _built[$name]=0
        fi
        use_build "$name" "$cfg"
        if [ "${_built[$name]}" = 1 ] && preflight_firmware "$name" "$iface" "$cfg"; then
            _ready+=("$entry")
        else
            failed+=("$name ($iface) - not flashed")
            record_flash "$cfg" "$iface" failed
        fi
    done
    to_flash=("${_ready[@]}")
    if [ ${#to_flash[@]} -eq 0 ]; then
        save_uuid_cache
        _summary_box "Flash Summary"
        return 1
    fi
    check_host_power

    # Interrupts (incl. SSH hangup) finish the current step, then Klipper is restarted.
    local _flash_aborted=false _saved_traps
    _saved_traps=$(trap -p INT TERM HUP TSTP)
    trap 'warn "Signal caught - finishing current flash step before stopping..."; _flash_aborted=true' INT TERM HUP
    trap '' TSTP # block Ctrl-Z completely

    header "Stopping Klipper..."
    if [ "$CONTEXT" = "pi" ]; then
        hold_klipper || warn "Could not block Klipper restarts - a UI may restart it mid-flash"
    fi
    sudo systemctl stop klipper 2>/dev/null || true
    sleep 2
    [ "$CONTEXT" = "pi" ] && ensure_can_up

    local _flash_idx=0 _flash_total=${#to_flash[@]}
    local _bridge_flashed=false _can_failed=false
    for entry in "${to_flash[@]}"; do
        IFS='|' read -r name iface id cfg fw_ver detected <<<"$entry"
        if $_flash_aborted; then
            failed+=("$name ($iface) - interrupted")
            continue
        fi
        # A failed CAN node is only reachable for a retry through the bridge it sits behind.
        if $_can_failed && ! $FLASH_ORDER_LOCKED && is_canbus_bridge "$cfg"; then
            warn "[$name] skipped: a CAN node behind this bridge failed - fix it first"
            failed+=("$name ($iface) - skipped, CAN node failed")
            continue
        fi
        ((_flash_idx++))
        header "[$name] ($iface) - ${_flash_idx}/${_flash_total}"
        local ok_flag=0 _note=""
        use_build "$name" "$cfg"
        case "$iface" in
        can)
            local _can_rc=0
            flash_can "$name" "$id" || _can_rc=$?
            if [ "$_can_rc" -eq 0 ]; then
                ok_flag=1
            elif [ "$_can_rc" -eq 2 ]; then
                # CONNECT error: Katapult not in bootloader mode.
                # Try firmware restart first - works when Katapult is installed
                # but Klipper is running (e.g. EBB-36 connected via CAN).
                # On success, Katapult comes up on CAN and no USB is needed.
                info "[$name] Katapult not responding - triggering firmware restart..."
                trigger_can_bootloader "$id" >&2 || true
                if wait_for_katapult_node "$id" 10 && flash_can "$name" "$id"; then
                    ok_flag=1
                else
                    # Katapult not installed - attempt USB bootstrap.
                    info "[$name] restart failed - attempting Katapult bootstrap via USB..."
                    if bootstrap_katapult "$name" "$cfg" &&
                        wait_for_katapult_node "$id" &&
                        flash_can "$name" "$id"; then
                        ok_flag=1
                    fi
                fi
            fi
            # Broken comms leave the node in Katapult; one more write usually lands.
            if [ "$ok_flag" -eq 0 ] && bootloader_uuids | grep -qF "$id"; then
                warn "[$name] still in Katapult - retrying the flash once"
                flash_can "$name" "$id" && ok_flag=1
            fi
            if [ "$ok_flag" -eq 0 ]; then
                _can_failed=true
                # Katapult boots the app even after a failed verify, so a node gone from
                # both Klipper and Katapult is a half-written app: only a reset recovers it.
                warn "  If [$name] no longer answers on $CAN_INTERFACE, double-press its reset"
                warn "  button to enter Katapult, then re-run this script."
            fi
            ;;
        usb) flash_usb "$name" "$id" && ok_flag=1 ;;
        bootsel) flash_bootsel "$name" "$id" && ok_flag=1 ;;
        linux) flash_linux "$name" "$id" && ok_flag=1 ;;
        dfu)
            dfu_params "$cfg"
            local dfu_vidpid="$DFU_VIDPID" dfu_mem="$DFU_MEM" dfu_addr="$DFU_ADDR"
            local dfu_alt="$DFU_ALT" dfu_mcu_type="$DFU_MCU_TYPE"
            info "[$name] DFU $dfu_vidpid at $dfu_addr"
            warn "  Some boards drive heater outputs while in ROM DFU - stay with the printer."
            local dfu_serial="$id"
            if [ -z "$dfu_serial" ]; then
                # Check if already in DFU mode (pre-triggered above).
                scan_dfu_devices
                local _pre
                _pre=$(find_dfu_device "$dfu_vidpid" "$dfu_mem")
                if [ -n "$_pre" ]; then
                    dfu_serial="${_pre%%|*}"
                    info "[$name] already in DFU mode (serial: $dfu_serial)"
                else
                    local trigger_uuid="${UUID_CACHE_MAP[$dfu_mcu_type]:-}"
                    if [ -n "$trigger_uuid" ]; then
                        local dfu_result
                        if dfu_result=$(trigger_to_dfu "$name" "$trigger_uuid" "$dfu_vidpid" "$dfu_mem"); then
                            dfu_serial="${dfu_result%%|*}"
                        fi
                    fi
                fi
            fi
            if [ -n "$dfu_serial" ]; then
                local _dfu_rc=0
                flash_dfu "$name" "$dfu_vidpid" "$dfu_serial" "${dfu_alt:-0}" "${dfu_addr:-0x08000000}" ||
                    _dfu_rc=$?
                [ "$_dfu_rc" -eq 0 ] && ok_flag=1
                [ "$_dfu_rc" -eq 3 ] && ok_flag=1 && _note=" - readback unverified"
            else
                err "[$name] DFU trigger failed - $CAN_INTERFACE unavailable"
                err "  The board must be powered (24V PSU on) and $CAN_INTERFACE must be up."
                err "  Option 1: power on the printer, then re-run this script."
                err "  Option 2: hold BOOT0 on the board, press RESET, release BOOT0, then re-run with --force."
            fi
            ;;
        esac
        is_canbus_bridge "$cfg" && _bridge_flashed=true
        if [ "$ok_flag" -eq 1 ]; then
            flashed+=("$name ($iface)$_note")
            record_flash "$cfg" "$iface" ok
            # Baseline for the next run's crystal check (preflight_firmware).
            is_linux_config "$cfg" ||
                cp -f "$FW_BUILD_ROOT/$name/.config" "$FW_BUILD_ROOT/$name.flashed.config"
        else
            failed+=("$name ($iface)")
            record_flash "$cfg" "$iface" failed
        fi
    done

    trap - INT TERM HUP TSTP
    eval "$_saved_traps" # e.g. the TUI's terminal restore

    save_uuid_cache

    header "Starting Klipper..."
    release_klipper
    if $_bridge_flashed; then
        # The bridge re-enumerates after flashing; Klipper cannot connect until can0 is back.
        local _w
        for ((_w = 0; _w < 10; _w++)); do
            ip link show "$CAN_INTERFACE" up >/dev/null 2>&1 && break
            sleep 1
        done
        ensure_can_up >/dev/null 2>&1 || true
    fi
    sudo systemctl start klipper 2>/dev/null || true
    $_flash_aborted && warn "Flash was interrupted - Klipper has been restarted"

    _summary_box "Flash Summary"

    if [ "$CONTEXT" = "pi" ]; then
        header "Verifying running versions..."
        verify_klipper_ready
        write_versions_file >&2
    fi

    [ ${#failed[@]} -gt 0 ] && return 1 || return 0
}

# Build checklist args from DISCOVERED[].
build_checklist_args() {
    local -n _args=$1  # nameref - caller passes array name
    local -n _count=$2 # nameref - number of items added
    local src_hash
    src_hash=$(extract_git_hash "$SRC_VERSION")
    _count=0

    # Two passes: assign order numbers to "needs update" items (bridges last)
    local -a _names=() _descs_base=() _states=() _cfgs=()
    for entry in "${DISCOVERED[@]}"; do
        IFS='|' read -r name iface id cfg fw_ver detected <<<"$entry"
        [ "$detected" = "false" ] && continue

        local fw_hash desc_base state
        fw_hash=$(extract_git_hash "$fw_ver")
        if versions_match "$fw_ver" "$SRC_VERSION"; then
            desc_base="$(printf '%-7s │ %-9s             │ ' "$iface" "${fw_hash:-?}")${GREEN}[OK] up to date${RESET}"
            state="OFF"
        else
            desc_base="$(printf '%-7s │ %-9s -> %-9s │ ' "$iface" "${fw_hash:-none}" "${src_hash:-?}")${YELLOW}[!!] needs flash${RESET}"
            state="ON"
        fi
        _names+=("$name")
        _descs_base+=("$desc_base")
        _states+=("$state")
        _cfgs+=("$cfg")
    done

    # Single-pass classification: split indices into normal vs bridge, then emit both.
    local total=${#_names[@]} i
    local -a _norm_idx=() _bridge_idx=()
    for ((i = 0; i < total; i++)); do
        if is_canbus_bridge "${_cfgs[$i]}"; then
            _bridge_idx+=("$i")
        else
            _norm_idx+=("$i")
        fi
    done
    for i in "${_norm_idx[@]}" "${_bridge_idx[@]}"; do
        _args+=("${_names[$i]}" "${_descs_base[$i]}" "${_states[$i]}")
        ((_count++))
    done
}

# Custom interactive selector - shows [N] flash-order numbers instead of [*].
tui_select() {
    local -n _cl_args=$1
    local total=$((${#_cl_args[@]} / 3))
    [ "$total" -eq 0 ] && return 1

    local -a _names=() _descs=() _sel_order=()
    local _next_num=1 i
    for ((i = 0; i < ${#_cl_args[@]}; i += 3)); do
        _names+=("${_cl_args[$i]}")
        _descs+=("${_cl_args[$((i + 1))]}")
        if [[ "${_cl_args[$((i + 2))]}" == "ON" ]]; then
            _sel_order+=("$_next_num")
            ((_next_num++))
        else
            _sel_order+=(0)
        fi
    done

    local cursor=0
    local _old_stty
    _old_stty=$(stty -g)

    _tui_cleanup() {
        printf '\033[?25h' >&2
        stty "$_old_stty" 2>/dev/null
    }
    trap '_tui_cleanup; exit 130' INT TERM
    stty -echo -icanon min 1 time 0
    printf '\033[?25l' >&2

    _tui_render() {
        printf '\033[2J\033[H' >&2
        printf '\n' >&2
        printf '  \033[1;36m  Blocks Klipper MCU Flasher  |  %s  \033[0m\n' "$CONTEXT" >&2
        printf '\n' >&2
        printf '    \033[1m%-3s %-12s %-6s   %-8s        %-16s\033[0m\n' \
            "   " "MCU" "Iface" "Version" "Status" >&2
        printf '    %s\n\n' \
            "────────────────┼────────┼──────────────────────────────────────────" >&2
        local i
        for ((i = 0; i < total; i++)); do
            local marker
            if [ "${_sel_order[$i]}" -gt 0 ]; then
                printf -v marker '[%d]' "${_sel_order[$i]}"
            else
                marker='[ ]'
            fi
            if [ "$i" -eq "$cursor" ]; then
                printf '  \033[44;97m  %-3s %-12s %s  \033[0m\n' "$marker" "${_names[$i]}" "${_descs[$i]}" >&2
            else
                printf '    %-3s %-12s %s\n' "$marker" "${_names[$i]}" "${_descs[$i]}" >&2
            fi
        done
        printf '\n  \033[2m  up/dn: navigate  |  SPACE: toggle  |  ENTER: flash  |  R: rescan  |  ESC: quit\033[0m\n' >&2
    }

    _tui_render

    while true; do
        local _byte
        IFS= read -r -d '' -n1 _byte
        case "$_byte" in
        $'\x1b')
            local _b2="" _b3=""
            IFS= read -r -d '' -t 0.1 -n1 _b2 || true
            if [ -z "$_b2" ]; then
                _tui_cleanup
                trap - INT TERM
                return 1
            fi
            IFS= read -r -d '' -t 0.1 -n1 _b3 || true
            case "$_b3" in
            A) ((cursor > 0)) && ((cursor--)) ;;
            B) ((cursor < total - 1)) && ((cursor++)) ;;
            esac
            ;;
        ' ')
            if [ "${_sel_order[$cursor]}" -gt 0 ]; then
                local _removed="${_sel_order[$cursor]}"
                _sel_order[$cursor]=0
                for ((i = 0; i < total; i++)); do
                    [ "${_sel_order[$i]}" -gt "$_removed" ] && ((_sel_order[$i]--))
                done
                ((_next_num--))
            else
                _sel_order[$cursor]=$_next_num
                ((_next_num++))
            fi
            ;;
        'r' | 'R')
            # Manual rescan: re-discover all MCUs.
            _tui_cleanup
            trap - INT TERM
            return 2
            ;;
        $'\n' | $'\r' | '')
            break
            ;;
        esac
        _tui_render
    done

    _tui_cleanup
    trap - INT TERM

    # Build reverse map , then emit in order.
    local -A _order_map=()
    for ((i = 0; i < total; i++)); do
        [ "${_sel_order[$i]}" -gt 0 ] && _order_map["${_sel_order[$i]}"]="$i"
    done
    FLASH_NAMES=()
    local n
    for ((n = 1; n < _next_num; n++)); do
        local _idx="${_order_map[$n]:-}"
        [ -n "$_idx" ] && FLASH_NAMES+=("${_names[$_idx]}")
    done

    return 0
}

# Display a message box and wait for keypress.
tui_msgbox() {
    local title="$1" body="$2"
    local _old_stty
    _old_stty=$(stty -g)
    echo "" >&2
    echo -e "  ${BOLD}${CYAN}── ${title} ──${RESET}" >&2
    echo "" >&2
    echo -e "$body" >&2
    echo "" >&2
    echo -e "  ${DIM}Press any key to continue...${RESET}" >&2
    stty -echo -icanon min 1 time 0
    IFS= read -r -d '' -n1 _ || true
    stty "$_old_stty"
}

cmd_tui() {
    while true; do
        discover

        local -a checklist_args=()
        local item_count=0
        build_checklist_args checklist_args item_count

        if [ "$item_count" -eq 0 ]; then
            tui_msgbox "No MCUs Detected" \
                "  All configured MCUs are offline or unreachable."
            return 0
        fi

        tui_select checklist_args
        local tui_rc=$?
        [ "$tui_rc" -eq 1 ] && return 0 # ESC - exit TUI
        [ "$tui_rc" -eq 2 ] && continue # DFU change or R key - re-discover

        [ ${#FLASH_NAMES[@]} -eq 0 ] && {
            info "Nothing selected."
            continue
        }

        # Apply default bridge-last ordering
        local -a normal_names=() bridge_names=()
        for _fn in "${FLASH_NAMES[@]}"; do
            local _matched_cfg=""
            for entry in "${DISCOVERED[@]}"; do
                local _en _ei _eid _ecfg
                IFS='|' read -r _en _ei _eid _ecfg _ _ <<<"$entry"
                [[ "$_en" == "$_fn" ]] && _matched_cfg="$_ecfg" && break
            done
            if [ -n "$_matched_cfg" ] && is_canbus_bridge "$_matched_cfg"; then
                bridge_names+=("$_fn")
            else
                normal_names+=("$_fn")
            fi
        done
        FLASH_NAMES=("${normal_names[@]}" "${bridge_names[@]}")

        # Toggle order defines the flash order
        FLASH_ORDER_LOCKED=true

        echo "" >&2
        echo -e "  ${BOLD}Flash order:${RESET}" >&2
        local _si=1
        for _fn in "${FLASH_NAMES[@]}"; do
            info "  ${_si}. ${_fn}"
            ((_si++))
        done
        [ ${#bridge_names[@]} -gt 0 ] &&
            warn "Bridge MCUs placed last (CAN bus dependency)"

        cmd_flash
        local flash_rc=$?

        local result_body=""
        [ ${#flashed[@]} -gt 0 ] && result_body+="  ${GREEN}[OK] Flashed${RESET}      : ${flashed[*]}\n"
        [ ${#skipped_utd[@]} -gt 0 ] && result_body+="  ${CYAN}[->] Up to date${RESET}  : ${skipped_utd[*]}\n"
        [ ${#skipped_missing[@]} -gt 0 ] && result_body+="  ${YELLOW}[!!] Not found${RESET}   : ${skipped_missing[*]}\n"
        [ ${#failed[@]} -gt 0 ] && result_body+="  ${RED}[XX] Failed${RESET}      : ${failed[*]}\n"

        local result_title
        if [ "$flash_rc" -eq 0 ]; then
            result_title="Flash Complete"
        else
            result_title="Flash Finished With Errors"
        fi

        tui_msgbox "$result_title" "$result_body"
    done
}

main() {
    local mode="tui"
    FLASH_NAMES=()
    FORCE=false
    local parse_flash_names=false

    for arg in "$@"; do
        if $parse_flash_names; then
            # Collect names after --flash until we hit another flag
            [[ "$arg" == --* ]] && parse_flash_names=false || {
                FLASH_NAMES+=("$arg")
                continue
            }
        fi
        case "$arg" in
        --list-json) mode="json" ;;
        --flash)
            mode="flash"
            parse_flash_names=true
            ;;
        --flash-all) mode="flash" ;;
        --versions) mode="versions" ;;
        --release) mode="release" ;;
        --force) FORCE=true ;;
        --allow-comms-change) ALLOW_COMMS_CHANGE=true ;;
        --help | -h)
            cat >&2 <<'EOF'
Blocks Klipper MCU Flasher

USAGE:
  flash_mcus.sh                         Interactive TUI (requires TTY)
  flash_mcus.sh --list-json            Discover MCUs, emit JSON on stdout, exit 0
  flash_mcus.sh --flash <name...>      Flash named MCUs (e.g. octopus eddy_duo)
  flash_mcus.sh --flash-all            Flash all outdated MCUs non-interactively
  flash_mcus.sh --versions             Report MCU vs host versions, update the versions file
  flash_mcus.sh --release              Remove a Klipper start block left by a killed flash
  flash_mcus.sh --help                 Show this help

OPTIONS:
  --force   Bypass version check - flash even if MCU firmware is up to date
  --allow-comms-change
            Flash even if the build changes the MCU, clock, CAN or USB settings the
            running firmware reports (the host may lose the MCU; keep physical access)

CONFIG FILES:
  mcu_config/<name>.config - Klipper build config with interface headers:
    # mcu_type: rp2040         -> CAN flash (matched by chip type)
    # klipper_section: mcu     -> Moonraker version query key
    # serial: usb-Katapult_*   -> USB Katapult flash
    # bootsel: 2e8a:0003       -> BOOTSEL/picoboot flash
    # dfu: 0483:df11           -> STM32 DFU flash
    # dfu_mem: 8*128Kg         -> DFU memory filter (disambiguates devices)
    # dfu_addr: 0x08000000     -> DFU flash address (default 0x08000000)
    # linux: klipper-mcu       -> Linux host MCU (installs klipper_mcu)

ENVIRONMENT:
  MOONRAKER_URL      default http://localhost:7125 (--versions works against a remote host)
  MCU_VERSIONS_FILE  default ~/printer_data/logs/mcu_versions.json
  FW_BUILD_ROOT      out-of-tree build dir, default ~/.cache/blocks-flash

EXIT CODES:
  0   Success (or nothing to flash); --versions: all Klipper MCUs current
  1   One or more MCUs failed to flash; --versions: Moonraker unreachable
  2   --versions: one or more MCUs need a flash

NOTE: Ctrl-C and Ctrl-Z are blocked during active flash operations to
      prevent firmware corruption. The script finishes the current step
      then stops if interrupted.
EOF
            exit 0
            ;;
        *) warn "Unknown argument: $arg" ;;
        esac
    done

    [ "$mode" = "tui" ] && [ ! -t 0 ] && mode="flash"

    # Read-only, compared against the running host (Klipper's own mismatch rule).
    if [ "$mode" = "versions" ]; then
        python3 "$VERSIONS_PY" report --url "$MOONRAKER_URL" --state-file "$MCU_VERSIONS_FILE"
        exit $?
    fi

    if [ "$mode" = "release" ]; then
        take_flash_lock || {
            err "A flash is running; it releases Klipper when it ends"
            exit 1
        }
        [ -f "$KLIPPER_HOLD_DROPIN" ] || info "No Klipper start block found"
        recover_stale_hold
        exit $?
    fi

    [ ! -d "$MCU_CONFIG_DIR" ] && {
        echo "ERROR: $MCU_CONFIG_DIR not found"
        exit 1
    }
    if [ "$mode" != "json" ] && [ ! -d "$KLIPPER_DIR" ]; then
        echo "ERROR: $KLIPPER_DIR not found"
        exit 1
    fi

    detect_context
    if [ "$CONTEXT" = "pi" ]; then
        if take_flash_lock; then
            recover_stale_hold
            trap release_klipper EXIT # the only EXIT trap: a hold never outlives this run
        elif [ "$mode" != "json" ]; then
            err "Another flash_mcus.sh is running"
            exit 1
        fi
    fi
    ensure_katapult 2>/dev/null || true
    load_uuid_cache
    load_uuids_from_printer_cfg 2>/dev/null || true

    if [ "$mode" != "json" ]; then
        SRC_VERSION=$(get_source_version)
        local src_hash
        src_hash=$(extract_git_hash "$SRC_VERSION")
        echo "" >&2
        _box_top
        _box_center "${BOLD}Blocks Klipper MCU Flasher${RESET}"
        _box_sep
        _box_line "${DIM}Context :${RESET}  ${CYAN}${CONTEXT}${RESET}"
        _box_line "${DIM}Source  :${RESET}  ${src_hash:-unknown}"
        if $FORCE; then
            _box_line "${YELLOW}Mode    :  FORCE -- skipping version check${RESET}"
        fi
        _box_bottom
    fi

    case "$mode" in
    json) cmd_list_json ;;
    flash)
        discover
        cmd_flash
        ;;
    tui) cmd_tui ;;
    esac
}

# Allow sourcing for tests.
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    main "$@"
fi
