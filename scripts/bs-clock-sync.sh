#!/usr/bin/env bash
# Sets the clock from verified HTTPS Date headers when NTP cannot sync (no RTC battery).
set -euo pipefail

# Read by updater/executor.py to tell a clock fault from a network fault.
MARKER=${BS_CLOCK_MARKER:-/run/blocksscreen-clock-verified}
# Kill switch; outside the repo so updates keep it.
DISABLE_FILE=${BS_CLOCK_DISABLE_FILE:-/etc/blocksscreen-clock.disabled}
# Independent operators with sub-second Date headers; entry: name[=addr:port].
read -ra SOURCES <<<"${BS_CLOCK_SOURCES:-deb.debian.org www.cloudflare.com www.google.com www.apple.com}"
CAFILE=${BS_CLOCK_CAFILE:-}
MOONRAKER=${BS_MOONRAKER_URL:-http://127.0.0.1:7125}
# Restored forward-only at boot, so a backward step must be saved here too.
TIMESYNC_CLOCK=${BS_CLOCK_TIMESYNC_FILE:-/var/lib/systemd/timesync/clock}
# Per TLS connection; worst case run = 2 x sources x this + 5 s.
TIMEOUT_S=${BS_CLOCK_TIMEOUT:-8}
# Also the clock jump that voids the verified marker.
MIN_STEP_S=120
AGREE_S=5
BS_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
UPTIME_FILE=${BS_CLOCK_UPTIME_FILE:-/proc/uptime}
IMF_RE='^[A-Z][a-z]{2}, [0-9]{2} [A-Z][a-z]{2} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} GMT$'

log() { echo "[bs-clock-sync] $*"; }

_tls() {
    local name=$1 addr=$2
    shift 2
    # openssl does not fall back from a dead IPv6 route.
    timeout "$TIMEOUT_S" openssl s_client -4 -connect "$addr" -servername "$name" \
        -verify_hostname "$name" -verify_return_error ${CAFILE:+-CAfile "$CAFILE"} "$@"
}

# Cert dates are skipped on fetch: the local clock is what is in doubt.
_https_offset() {
    local name=${1%%=*} addr=${1#*=} hdr local_s remote out
    [[ $1 == *=* ]] || addr="$name:443"
    hdr=$(printf 'HEAD / HTTP/1.1\r\nHost: %s\r\nUser-Agent: BlocksScreen-clock\r\nConnection: close\r\n\r\n' "$name" |
        _tls "$name" "$addr" -quiet -no_check_time 2>/dev/null |
        tr -d '\r' | sed -n '/^$/q;s/^date: //Ip;T;q') || true
    # Sampled after the first handshake; a later read biases the offset on slow links.
    local_s=$(date -u +%s)
    [[ $hdr =~ $IMF_RE ]] || return 1
    remote=$(date -u -d "$hdr" +%s) || return 1
    # tlsdate --leap: the cert must be valid at the claimed time.
    out=$(_tls "$name" "$addr" -attime "$remote" </dev/null 2>&1) || true
    [[ $out == *"Verify return code: 0 (ok)"* ]] || return 1
    echo $((remote - local_s))
}

_boot_s() {
    local up rest
    read -r up rest <"$UPTIME_FILE"
    echo "${up%.*}"
}

# Marker = wall and boot time at verification; a later jump between them voids it.
_marker_valid() {
    local wall boot d
    read -r wall boot 2>/dev/null <"$MARKER" || return 1
    [[ $wall =~ ^[0-9]+$ && $boot =~ ^[0-9]+$ ]] || return 1
    d=$((($(date -u +%s) - wall) - ($(_boot_s) - boot)))
    ((${d#-} < MIN_STEP_S))
}

_printing() {
    curl -s --max-time 5 "$MOONRAKER/printer/objects/query?print_stats=state" 2>/dev/null |
        grep -qE '"state": ?"(printing|paused)"'
}

_ntp_synced() {
    [[ $(timedatectl show -p NTPSynchronized --value 2>/dev/null) == yes ]]
}

[[ -e $DISABLE_FILE ]] && exit 0
_ntp_synced && exit 0
_marker_valid && exit 0

# First two agreeing sources win; one bad source can neither block nor move the clock.
offsets=()
step=""
for src in "${SOURCES[@]}"; do
    off=$(_https_offset "$src") || continue
    for prev in "${offsets[@]}"; do
        d=$((prev - off))
        if ((${d#-} <= AGREE_S)); then
            step=$(((prev + off) / 2))
            break 2
        fi
    done
    offsets+=("$off")
done
if [[ -z $step ]]; then
    log "no 2 of ${#offsets[@]} answering sources agree within ${AGREE_S} s; clock unchanged"
    exit 0
fi

if ((${step#-} >= MIN_STEP_S)); then
    target=$(($(date -u +%s) + step))
    # No real date predates the installed commit.
    floor=${BS_CLOCK_FLOOR:-$(git -c safe.directory="$BS_PATH" -C "$BS_PATH" log -1 --format=%ct 2>/dev/null || echo 0)}
    if ((target < floor)); then
        log "ignoring source date $target: older than BlocksScreen HEAD ($floor)"
        exit 0
    fi
    # Moonraker job history uses wall time.
    if _printing; then
        log "print in progress; clock step of ${step} s deferred"
        exit 0
    fi
    # NTP may have synced since the offset was measured.
    if _ntp_synced; then
        log "NTP synchronized during the run; clock step of ${step} s skipped"
        exit 0
    fi
    date -u -s "@$target" >/dev/null
    log "clock stepped by ${step} s"
    if command -v fake-hwclock >/dev/null; then
        fake-hwclock save >/dev/null 2>&1 || true
    fi
    if [[ -e $TIMESYNC_CLOCK ]]; then
        touch "$TIMESYNC_CLOCK" || true
    fi
fi
echo "$(date -u +%s) $(_boot_s)" >"$MARKER"
