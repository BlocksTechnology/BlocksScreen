#!/usr/bin/env bash
# Steps the clock from an HTTP Date header while NTP is unsynced; boxes have no RTC and blocked NTP never heals.
set -euo pipefail

SYNC_FLAG=${BS_CLOCK_SYNC_FLAG:-/run/systemd/timesync/synchronized}
read -ra HOSTS <<<"${BS_CLOCK_HOSTS:-http://github.com http://deb.debian.org}"
MIN_STEP_S=120
BS_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
IMF_RE='^[A-Z][a-z]{2}, [0-9]{2} [A-Z][a-z]{2} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2} GMT$'

log() { echo "[bs-clock-sync] $*"; }

# Plain HTTP on purpose: TLS cannot validate while the clock is wrong.
_http_epoch() {
    local hdr
    hdr=$(curl -sSI --max-time 10 "$1" 2>/dev/null | tr -d '\r' | sed -n 's/^[Dd]ate: //p;T;q') || return 1
    [[ $hdr =~ $IMF_RE ]] || return 1
    date -u -d "$hdr" +%s
}

[[ -e $SYNC_FLAG ]] && exit 0

remote="" source_host=""
for host in "${HOSTS[@]}"; do
    if remote=$(_http_epoch "$host"); then
        source_host=$host
        break
    fi
done
[[ -n $source_host ]] || exit 0

# Never step before the installed code's commit time, so a bogus header cannot rewind far.
floor=${BS_CLOCK_FLOOR:-$(git -c safe.directory="$BS_PATH" -C "$BS_PATH" log -1 --format=%ct 2>/dev/null || echo 0)}
if ((remote < floor)); then
    log "ignoring $source_host date $remote: older than BlocksScreen HEAD ($floor)"
    exit 0
fi

now=$(date -u +%s)
step=$((remote - now))
if ((${step#-} < MIN_STEP_S)); then
    exit 0
fi
date -u -s "@$remote" >/dev/null
log "clock stepped by ${step} s from $source_host"
if command -v fake-hwclock >/dev/null; then
    fake-hwclock save >/dev/null 2>&1 || true
fi
