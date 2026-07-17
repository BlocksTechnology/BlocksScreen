#!/bin/bash
# Deferred bootstrap: everything heavy or network-dependent that the UI does
# NOT need to start. Launched detached (transient unit) by BlocksScreen-start.sh
# and bs-deploy-check.sh, runs as root, is idempotent and flock-guarded.
# Anything that cannot complete now (e.g. offline) is retried on the next boot
# or finished by the next update (post-merge installs requirements too).
set -u

exec 200>/tmp/blockscreen-bootstrap.lock
flock -n 200 || exit 0

SCRIPT_PATH=$(dirname -- "$(readlink -f -- "$0")")
BS_PATH=$(dirname "$SCRIPT_PATH")
_BSENV_USER="blocks"
_BSENV_HOME=$(getent passwd "$_BSENV_USER" | cut -d: -f6)
BSENV="${BLOCKSSCREEN_VENV:-${_BSENV_HOME}/.BlocksScreen-env}"
_as_blocks() { runuser -u "$_BSENV_USER" -- "$@"; }

echo "[bs-bootstrap] starting"

# 1. Build/display dependencies (network; skipped silently when offline).
_missing=""
dpkg -s libsystemd-dev >/dev/null 2>&1 || _missing="$_missing libsystemd-dev python3-dev"
command -v feh >/dev/null 2>&1 || _missing="$_missing feh"
command -v xsetroot >/dev/null 2>&1 || _missing="$_missing x11-xserver-utils"
if [ -n "$_missing" ]; then
    # shellcheck disable=SC2086
    apt-get -o DPkg::Lock::Timeout=60 install -y --quiet $_missing 2>/dev/null \
        || echo "[bs-bootstrap] apt install deferred (offline or dpkg busy):$_missing"
fi

# 2. Python deps. PyYAML is required by the updater daemon's component loader.
_as_blocks "$BSENV/bin/python3.11" -c "import yaml" 2>/dev/null \
    || _as_blocks "$BSENV/bin/pip" install --quiet "PyYAML==6.0.3" || true
# Emergency repair only - requirements.txt below carries the canonical pin.
_as_blocks "$BSENV/bin/python3.11" -c "import sdbus" 2>/dev/null \
    || _as_blocks "$BSENV/bin/pip" install --quiet \
        --no-binary sdbus,sdbus-networkmanager \
        "sdbus==0.12.0" "sdbus-networkmanager==2.0.0" || true

# 3. Full pinned requirements when the set changed (also done by post-merge).
REQS_HASH=$(md5sum "$BS_PATH/scripts/requirements.txt" | cut -d' ' -f1)
SENTINEL="$BSENV/.blockscreen-reqs-hash"
ATTEMPT="$BSENV/.blockscreen-reqs-attempt"
if [ ! -f "$SENTINEL" ] || [ "$(cat "$SENTINEL")" != "$REQS_HASH" ]; then
    if _as_blocks "$BSENV/bin/pip" install --quiet \
        --only-binary :all: \
        --no-binary sdbus,sdbus-networkmanager \
        --upgrade-strategy=only-if-needed \
        -r "$BS_PATH/scripts/requirements.txt"; then
        echo "$REQS_HASH" >"$SENTINEL"
        chown "$_BSENV_USER" "$SENTINEL" 2>/dev/null || true
        rm -f "$ATTEMPT" 2>/dev/null || true
    else
        # pip resolves -r atomically: a single dep without an aarch64 wheel
        # rejects the whole set, the sentinel never advances, and bootstrap
        # re-thrashes this install on every boot. Bound the retries - keep
        # trying for a few boots (covers transient/offline failures), then
        # accept the partial venv so a deterministically-failing set stops
        # thrashing the boot path.
        _prev=$(cut -d' ' -f1 "$ATTEMPT" 2>/dev/null || true)
        _cnt=$(cut -d' ' -f2 "$ATTEMPT" 2>/dev/null || true)
        case "$_cnt" in '' | *[!0-9]*) _cnt=0 ;; esac
        if [ "$_prev" = "$REQS_HASH" ]; then _cnt=$((_cnt + 1)); else _cnt=1; fi
        echo "$REQS_HASH $_cnt" >"$ATTEMPT"
        chown "$_BSENV_USER" "$ATTEMPT" 2>/dev/null || true
        if [ "$_cnt" -ge 3 ]; then
            echo "[bs-bootstrap] requirements failed ${_cnt}x; giving up to stop boot thrash (venv left as-is)"
            echo "$REQS_HASH" >"$SENTINEL"
            chown "$_BSENV_USER" "$SENTINEL" 2>/dev/null || true
        fi
    fi
fi

# 4. Updater stack (local files only - works offline).
# Verify each critical artifact: an old-installer box can have the service but no apt helper.
if [ ! -f /etc/systemd/system/BlocksScreen-updater.service ] \
    || [ ! -x /usr/local/sbin/bs-apt-helper ]; then
    bash "$SCRIPT_PATH/install-updater.sh" || true
fi

# 5. Splash holder unit (local).
_HOLDER_SRC="$SCRIPT_PATH/BlocksScreen-splash-holder.service"
_HOLDER_DST="/etc/systemd/system/BlocksScreen-splash-holder.service"
if [ ! -f "$_HOLDER_DST" ]; then
    # Atomic install: a truncated-but-present unit would never be retried by the [ ! -f ] guard.
    if cp "$_HOLDER_SRC" "${_HOLDER_DST}.new" && mv -Tf "${_HOLDER_DST}.new" "$_HOLDER_DST"; then
        systemctl daemon-reload || true
        systemctl enable BlocksScreen-splash-holder.service 2>/dev/null || true
    fi
fi
systemctl is-active --quiet BlocksScreen-splash-holder.service \
    || systemctl start --no-block BlocksScreen-splash-holder.service || true

# 6. Precompute splash cache (needs Pillow; skips gracefully until installed).
_as_blocks "$BSENV/bin/python3.11" "$SCRIPT_PATH/bs-splash.py" --precompute 2>/dev/null || true

echo "[bs-bootstrap] done"
