#!/usr/bin/env bash
# BlocksScreen box acceptance + health test: validates every install artifact, service, config patch and runtime subsystem.
# Usage: ./bs-healthcheck.sh [-q|--json] [-v] [--deep] [--strict] [--only S] [--skip S] [--fix] [--force] [--list]
#   -q         one-line PASS/FAIL summary only (fleet sweeps over ssh)
#   --json     machine-readable result object, implies quiet
#   -v         print the captured output of failing checks
#   --deep     add slow/network checks (remote branches, source compile, update refresh, sudo rights)
#   --strict   treat WARN as failure (exit code only, JSON rows keep their real tier)
#   --only S   run only these comma-separated sections (see --list)
#   --skip S   run everything except these sections
#   --fix      apply the known-safe remediations (spoolman, install artifacts, logs mode, asvc, env, journal, can0)
#   --force    allow --fix while a print is running (refused by default, the restarts disrupt the job)
#   --list     list section names and exit
#   --expect-branch N=B[,N=B]   branch each component must be on, overrides the manifest (env BS_EXPECT_BRANCH)
# Read-only and safe during a print by default. Only --fix changes anything.
# Exit: 0 all checks passed, 1 one or more failed, 2 bad usage.

set -u

SECTIONS="host system services ui install config klipper moonraker spoolman network updater repos python usb selftest deep"

QUIET=false
JSON=false
VERBOSE=false
DEEP=false
STRICT=false
FIX=false
FORCE=false
ONLY=""
SKIP=""
# Ground truth for branches is the operator, not the box's own manifest: "Name=branch,Name=branch".
EXPECT_BRANCH="${BS_EXPECT_BRANCH:-}"

usage() { awk 'NR>1 && /^#/ {sub(/^# ?/, ""); print; next} NR>1 {exit}' "$0"; }

while [ $# -gt 0 ]; do
    case "$1" in
        -q | --quiet) QUIET=true ;;
        --json)
            JSON=true
            QUIET=true
            ;;
        -v | --verbose) VERBOSE=true ;;
        --deep) DEEP=true ;;
        --strict) STRICT=true ;;
        --fix) FIX=true ;;
        --force) FORCE=true ;;
        --only)
            ONLY="${2:-}"
            shift
            ;;
        --only=*) ONLY="${1#*=}" ;;
        --skip)
            SKIP="${2:-}"
            shift
            ;;
        --skip=*) SKIP="${1#*=}" ;;
        --expect-branch)
            EXPECT_BRANCH="${2:-}"
            shift
            ;;
        --expect-branch=*) EXPECT_BRANCH="${1#*=}" ;;
        --list)
            echo "$SECTIONS" | tr ' ' '\n'
            exit 0
            ;;
        -h | --help)
            usage
            exit 0
            ;;
        *)
            echo "unknown arg: $1" >&2
            exit 2
            ;;
    esac
    shift
done

# A typo in --only/--skip would otherwise silently run nothing at all.
for _s in $(echo "$ONLY,$SKIP" | tr ',' ' '); do
    echo " $SECTIONS " | grep -q " $_s " || {
        echo "unknown section: $_s (try --list)" >&2
        exit 2
    }
done

# Resolve the real target user/home even under sudo, same trick as BlocksScreen-start.sh.
BS_USER="${SUDO_USER:-$(id -un)}"
# Walk up to the repo root instead of counting directories, so this script survives being moved.
BS_PATH=$(dirname -- "$(readlink -f -- "$0")")
while [ "$BS_PATH" != / ] && [ ! -d "$BS_PATH/BlocksScreen" ]; do
    BS_PATH=$(dirname -- "$BS_PATH")
done
[ -d "$BS_PATH/BlocksScreen" ] || BS_PATH=$(dirname -- "$(dirname -- "$(readlink -f -- "$0")")")
# sudo -i, cron and a console root login all leave SUDO_USER unset: without this fallback every path
# check points at /root and user_writable() degrades to root's always-true test -w.
if [ "$BS_USER" = root ] && [ -d "$BS_PATH/BlocksScreen" ]; then
    BS_USER=$(stat -c '%U' "$BS_PATH" 2>/dev/null || echo root)
fi
BS_HOME=$(getent passwd "$BS_USER" | cut -d: -f6)
[ -n "$BS_HOME" ] || BS_HOME="$HOME"
[ -d "$BS_PATH/BlocksScreen" ] || BS_PATH="$BS_HOME/BlocksScreen"
BSENV="${BLOCKSSCREEN_VENV:-$BS_HOME/.BlocksScreen-env}"
CONF="$BS_HOME/printer_data/config/moonraker.conf"
MOON="http://localhost:7125"
SPOOL="http://localhost:7912"
IS_ROOT=false
[ "$(id -u)" = "0" ] && IS_ROOT=true

# Colour only on a real terminal, so piped/--json output and dumb terminals stay plain. NO_COLOR opts out.
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ] && [ "${TERM:-dumb}" != dumb ]; then
    C_PASS=$'\033[32m'
    C_WARN=$'\033[33m'
    C_FAIL=$'\033[31m'
    C_SKIP=$'\033[90m'
    C_HDR=$'\033[1;36m'
    C_DIM=$'\033[90m'
    C_OFF=$'\033[0m'
else
    C_PASS='' C_WARN='' C_FAIL='' C_SKIP='' C_HDR='' C_DIM='' C_OFF=''
fi

PASS_N=0
WARN_N=0
FAIL_N=0
SKIP_N=0
FAILED_NAMES=""
WARNED_NAMES=""
JSON_ROWS=""
STATE=""
MACROS=""
CUR_SECTION=""
JOURNAL_OK=""

say() { $QUIET || echo "$@"; }
hdr() { $QUIET || printf '\n%s== %s ==%s\n' "$C_HDR" "$1" "$C_OFF"; }
info() { $QUIET || printf '      %s%s%s\n' "$C_DIM" "$*" "$C_OFF"; }
# Remediation chatter goes to stderr so --json keeps stdout a single parseable object.
note() { printf 'FIX: %s\n' "$*" >&2; }

# enabled <section> : honour --only/--skip, --deep gates the deep section.
enabled() {
    local s="$1"
    if [ -n "$ONLY" ]; then
        echo ",$ONLY," | grep -qF ",$s," || return 1
    else
        [ "$s" = "deep" ] && ! $DEEP && return 1
    fi
    [ -n "$SKIP" ] && echo ",$SKIP," | grep -qF ",$s," && return 1
    return 0
}

json_row() {
    JSON_ROWS="$JSON_ROWS${JSON_ROWS:+,}{\"section\":\"$CUR_SECTION\",\"name\":\"$1\",\"status\":\"$2\"}"
}

# record <PASS|WARN|FAIL|SKIP> <name> [captured output]
record() {
    local status="$1" name="$2" out="${3:-}" c=""
    case "$status" in
        PASS)
            PASS_N=$((PASS_N + 1))
            c="$C_PASS"
            ;;
        WARN)
            WARN_N=$((WARN_N + 1))
            WARNED_NAMES="$WARNED_NAMES${WARNED_NAMES:+, }$name"
            c="$C_WARN"
            ;;
        FAIL)
            FAIL_N=$((FAIL_N + 1))
            FAILED_NAMES="$FAILED_NAMES${FAILED_NAMES:+, }$name"
            c="$C_FAIL"
            ;;
        SKIP)
            SKIP_N=$((SKIP_N + 1))
            c="$C_SKIP"
            ;;
    esac
    say "$c$status$C_OFF  $name"
    if $VERBOSE && [ -n "$out" ] && [ "$status" != "PASS" ]; then
        echo "$out" | sed "s/^/        $C_DIM| /; s/\$/$C_OFF/"
    fi
    json_row "$name" "$status"
}

# check <name> <cmd...> : hard requirement, failure fails the box.
check() {
    local name="$1" out
    shift
    if out=$("$@" 2>&1); then record PASS "$name"; else record FAIL "$name" "$out"; fi
}

# warn <name> <cmd...> : advisory, does not fail the box unless --strict.
warn() {
    local name="$1" out
    shift
    if out=$("$@" 2>&1); then record PASS "$name"; else record WARN "$name" "$out"; fi
}

# rwarn <name> <cmd...> : soft twin of rcheck, a SKIP beats a WARN we could not actually verify.
rwarn() {
    local name="$1"
    shift
    if $IS_ROOT; then
        warn "$name" "$@"
    else
        record SKIP "$name (needs root)"
    fi
}

# rcheck <name> <cmd...> : needs root to read, reported SKIP when unprivileged.
rcheck() {
    local name="$1"
    shift
    if $IS_ROOT; then
        check "$name" "$@"
    else
        record SKIP "$name (needs root)"
    fi
}

# Journal ACLs hide system units from unprivileged readers and Storage=none hides them from everyone,
# so "! journalctl | grep -q bad" passes on a box full of tracebacks. Probe once, then SKIP not PASS.
journal_readable() {
    [ -n "$JOURNAL_OK" ] || {
        if [ -n "$(journalctl -u systemd-journald -b -n 1 --no-pager 2>/dev/null)" ]; then
            JOURNAL_OK=yes
        else
            JOURNAL_OK=no
        fi
    }
    [ "$JOURNAL_OK" = yes ]
}

# jcheck / jwarn <name> <cmd...> : journal-backed twins, SKIP rather than pass vacuously.
jcheck() {
    if journal_readable; then check "$@"; else record SKIP "$1 (no journal access)"; fi
}
jwarn() {
    if journal_readable; then warn "$@"; else record SKIP "$1 (no journal access)"; fi
}

# --- predicates (kept as commands so check() stays a plain runner) ---

file_has() { grep -qE "$2" "$1" 2>/dev/null; }
grep_count_is_one() { [ "$(grep -cE "$1" "$2" 2>/dev/null)" = "1" ]; }
curl_matches() { curl -s -m "$1" "$2" 2>/dev/null | grep -q "$3"; }
unit_active() { systemctl is-active --quiet "$1"; }
unit_enabled() { systemctl is-enabled "$1" >/dev/null 2>&1; }
unit_prop_is() { [ "$(systemctl show "$1" -p "$2" --value 2>/dev/null)" = "$3" ]; }
unit_prop_isnt() { [ "$(systemctl show "$1" -p "$2" --value 2>/dev/null)" != "$3" ]; }
in_group() { id -nG "$BS_USER" 2>/dev/null | tr ' ' '\n' | grep -qx "$1"; }
mode_is() { [ "$(stat -c '%a' "$1" 2>/dev/null)" = "$2" ]; }
owner_is() { [ "$(stat -c '%U:%G' "$1" 2>/dev/null)" = "$2" ]; }
group_is() { [ "$(stat -c '%G' "$1" 2>/dev/null)" = "$2" ]; }
is_symlink() { [ -L "$1" ]; }
proc_running() { pgrep -f "$1" >/dev/null 2>&1; }
str_is() { [ "$1" = "$2" ]; }
not_grep() { ! grep -qE "$2" "$1" 2>/dev/null; }

# Free space in MiB on the filesystem holding $1, must be >= $2.
free_mb_at_least() {
    local kb
    kb=$(df -Pk "$1" 2>/dev/null | awk 'NR==2 {print $4}')
    case "${kb:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$((kb / 1024))" -ge "$2" ]
}

free_inodes_pct_at_least() {
    local used
    used=$(df -Pi "$1" 2>/dev/null | awk 'NR==2 {gsub(/%/, "", $5); print $5}')
    case "${used:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$((100 - used))" -ge "$2" ]
}

rootfs_writable() { ! grep -qE ' / [^ ]+ ro[, ]' /proc/mounts; }

# test -w is always true for root, so under sudo ask the real owner instead or the check is vacuous.
user_writable() {
    if $IS_ROOT; then
        # No unprivileged identity resolved means the answer is unproven, not "writable".
        [ "$BS_USER" != root ] || {
            echo "cannot verify writability: no unprivileged user resolved"
            return 1
        }
        su -s /bin/sh -c "test -w '$1'" "$BS_USER" 2>/dev/null
    else
        test -w "$1"
    fi
}

# A freshly flashed image that never ran resize2fs shows up as a suspiciously small root partition.
rootfs_expanded() {
    local kb
    kb=$(df -Pk / 2>/dev/null | awk 'NR==2 {print $2}')
    case "${kb:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$((kb / 1024 / 1024))" -ge 8 ]
}

read_model() {
    local f=/proc/device-tree/model
    [ -r "$f" ] && tr -d '\0' <"$f" || echo unknown
}

# Age in seconds of a systemd timestamp, read from the Monotonic twin because date -d only parses the active TZ abbreviation.
unit_ts_age() {
    local us up
    us=$(systemctl show "$1" -p "${2}Monotonic" --value 2>/dev/null)
    case "${us:-x}" in '' | 0 | *[!0-9]*) return 1 ;; esac
    up=$(awk '{printf "%.0f", $1 * 1000000}' /proc/uptime 2>/dev/null)
    case "${up:-x}" in '' | *[!0-9]*) return 1 ;; esac
    echo $(((up - us) / 1000000))
}

# Seconds since the epoch for a systemd timestamp property, fails when unset.
unit_ts() {
    local age
    age=$(unit_ts_age "$1" "$2") || return 1
    echo $(($(date +%s) - age))
}

# WatchdogUSec renders as "30s" on systemd >= 250 and as raw microseconds on older builds.
watchdog_sec() {
    local v
    v=$(systemctl show "$1" -p WatchdogUSec --value 2>/dev/null)
    case "$v" in
        *ms) echo 0 ;;
        *min*) echo $((${v%%min*} * 60)) ;;
        *s) echo "${v%s}" ;;
        '' | *[!0-9]*) echo 0 ;;
        *) echo $((v / 1000000)) ;;
    esac
}

# The Qt loop pings WATCHDOG=1 every WatchdogSec/2, so a fresh stamp proves the event loop is pumping.
# The window has to come from the unit: a hardcoded one wider than WatchdogSec can never be reached
# because systemd kills and restarts the unit first, which makes it a check that can only pass.
watchdog_fresh() {
    local age w
    w=$(watchdog_sec BlocksScreen)
    [ "$w" -gt 0 ] || {
        echo "WatchdogSec=0: systemd is not enforcing UI liveness at all"
        return 1
    }
    age=$(unit_ts_age BlocksScreen WatchdogTimestamp) || return 1
    [ "$age" -lt "$w" ] || {
        echo "watchdog stamp ${age}s old vs WatchdogSec=${w}s (event loop about to be killed)"
        return 1
    }
}

# A stalled event loop shows up as a systemd kill and a restart, never as an old timestamp.
no_watchdog_kill() {
    local hits
    hits=$(journalctl -u BlocksScreen -b --no-pager 2>/dev/null | grep -i 'watchdog timeout' | tail -3)
    [ -z "$hits" ] || {
        echo "$hits"
        return 1
    }
}

# StartLimitIntervalSec=0 is the unit-file key, systemd 252 only exposes StartLimitIntervalUSec at runtime.
start_limit_disabled() {
    local v
    v=$(systemctl show "$1" -p StartLimitIntervalUSec --value 2>/dev/null)
    case "$v" in 0 | 0s | 0us | infinity) return 0 ;; esac
    echo "$1 StartLimitIntervalUSec=${v:-<unset>}"
    return 1
}

# A crash/fault log only matters when it was written by the current run.
log_predates_start() {
    local st
    [ -f "$1" ] || return 0
    st=$(unit_ts BlocksScreen ActiveEnterTimestamp) || return 0
    [ "$(stat -c '%Y' "$1" 2>/dev/null || echo 0)" -lt "$st" ]
}

file_fresher_than() {
    local age
    [ -f "$1" ] || return 1
    age=$(($(date +%s) - $(stat -c '%Y' "$1")))
    [ "$age" -lt "$2" ]
}

# Journal for a unit since it last started, as a relative age so no timestamp string is ever parsed.
journal_since_start() {
    local age
    age=$(unit_ts_age "$1" ActiveEnterTimestamp) || {
        journalctl -u "$1" -b 2>/dev/null
        return
    }
    journalctl -u "$1" --since "-$((age + 2))s" 2>/dev/null
}

no_traceback_since_start() {
    ! journal_since_start BlocksScreen | grep -q 'Traceback (most recent call last)'
}

# A panel that never enumerated leaves every connector disconnected, which reads as a dead box on the bench.
display_connected() {
    grep -lx connected /sys/class/drm/*/status >/dev/null 2>&1 || {
        echo "no connected DRM connector (panel unplugged or overlay missing)"
        return 1
    }
}

# X starts fine with no touch device, so an unplugged digitiser only shows up when someone taps the screen.
touchscreen_present() {
    local d
    for d in /dev/input/event*; do
        [ -e "$d" ] || continue
        udevadm info -q property "$d" 2>/dev/null | grep -q '^ID_INPUT_TOUCHSCREEN=1' && return 0
    done
    echo "no ID_INPUT_TOUCHSCREEN device (digitiser unplugged)"
    return 1
}

# Xorg owns one VT: if the active console moved, the operator sees a text console instead of the app.
xorg_vt_active() {
    local want cur
    want=$(pgrep -a Xorg 2>/dev/null | grep -o 'vt[0-9]*' | head -1 | tr -dc '0-9')
    [ -n "$want" ] || return 0
    cur=$(fgconsole 2>/dev/null | tr -dc '0-9')
    [ -n "$cur" ] || return 0
    [ "$cur" = "$want" ] || {
        echo "active VT is $cur, Xorg is on vt$want"
        return 1
    }
}

# A UI that has ballooned gets OOM-killed mid-print on a box nobody can SSH into.
ui_rss_below_mb() {
    local pid kb
    pid=$(pgrep -f 'BlocksScreen/BlocksScreen.py' 2>/dev/null | head -1)
    [ -n "$pid" ] || return 0
    kb=$(ps -o rss= -p "$pid" 2>/dev/null | tr -dc '0-9')
    case "${kb:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$((kb / 1024))" -lt "$1" ] || {
        echo "UI RSS $((kb / 1024)) MiB (limit $1)"
        return 1
    }
}

boot_counter_clear() {
    local f="$BS_HOME/.cache/blockscreen/boot_attempts" n
    [ -f "$f" ] || return 0
    n=$(tr -dc '0-9' <"$f")
    [ -z "$n" ] || [ "$n" -lt 2 ]
}

last_good_is_head() {
    local f="$BS_HOME/.cache/blockscreen/last_good_commit"
    [ -f "$f" ] || return 1
    [ "$(cat "$f")" = "$(git -C "$BS_PATH" rev-parse HEAD 2>/dev/null)" ]
}

git_ok() { git -C "$1" cat-file -e HEAD 2>/dev/null; }
# Print what is dirty, a bare "not clean" leaves the operator with nowhere to go.
git_clean() {
    local out
    out=$(git -C "$1" status --porcelain 2>/dev/null | head -8)
    [ -z "$out" ] || { echo "$out"; return 1; }
}
git_attached() { [ "$(git -C "$1" rev-parse --abbrev-ref HEAD 2>/dev/null)" != "HEAD" ]; }
git_no_lock() { [ ! -f "$1/.git/index.lock" ]; }
git_branch_is() { [ "$(git -C "$1" rev-parse --abbrev-ref HEAD 2>/dev/null)" = "$2" ]; }
git_remote_has_branch() {
    local rc
    GIT_TERMINAL_PROMPT=0 GIT_SSH_COMMAND='ssh -oBatchMode=yes -oStrictHostKeyChecking=accept-new' \
        timeout 25 git ls-remote --heads --exit-code "$1" "$2" >/dev/null 2>&1
    rc=$?
    # Only rc 2 proves the ref is gone: 128 is transport and 124 is our own timeout. Failing the box
    # for those turns every bench run without internet into a wall of failures nobody can act on.
    case $rc in
        0) return 0 ;;
        2)
            echo "branch $2 missing on $1 (updates for this component are dead)"
            return 1
            ;;
        *)
            echo "remote $1 unreachable (rc=$rc), branch existence unproven"
            return 0
            ;;
    esac
}
git_system_safe_dir() { git config --system --get-all safe.directory 2>/dev/null | grep -qx "$1"; }
git_config_is() { [ "$(git -C "$1" config --get "$2" 2>/dev/null)" = "$3" ]; }

# Without an upstream ref the updater cannot compare against origin, so the box silently never reports updates.
git_has_upstream() {
    git -C "$1" rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1 || {
        echo "no upstream for $(git -C "$1" rev-parse --abbrev-ref HEAD 2>/dev/null) (branch never pushed or tracking lost)"
        return 1
    }
}

# Local commits made on a field box are lost by the updater's hard reset, so flag them before they are.
git_not_ahead() {
    local n
    git -C "$1" rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1 || return 0
    n=$(git -C "$1" rev-list --count '@{u}..HEAD' 2>/dev/null)
    case "${n:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$n" -eq 0 ] || {
        echo "$n local commit(s) ahead of upstream (a hard-reset update will discard them)"
        return 1
    }
}

# A stray .orig from a hand-edit leaves the repo dirty forever, which disables that component's updates.
no_merge_leftovers() {
    local hits
    hits=$(find "$1" -maxdepth 3 \( -name '*.orig' -o -name '*.rej' \) 2>/dev/null | head -5)
    [ -z "$hits" ] && return 0
    echo "merge leftovers (repo stays dirty, update_manager skips it):"
    echo "$hits"
    return 1
}

# A truncated package still imports and yields only its ~9 dunders, which crash-looped a field updater 10662x.
venv_import() {
    # Under sudo a written __pycache__ is root-owned and breaks the next import as the UI user.
    PYTHONDONTWRITEBYTECODE=1 "$BSENV/bin/python3.11" \
        -c "import $1 as _m; assert len(dir(_m)) > 15, 'empty module (truncated install)'" 2>&1
}

# Truncation can also hit a package this box does not import at startup, so sweep the tree.
venv_no_truncated_files() {
    local hits
    hits=$(find "$BSENV/lib" \( -name '*.so' -o \( -name '*.py' ! -name '__init__.py' \) \) -size 0 2>/dev/null | head -5)
    [ -z "$hits" ] && return 0
    echo "zero-length files in venv (interrupted pip or power cut):"
    echo "$hits"
    return 1
}
venv_import_updater() {
    cd "$BS_PATH" && PYTHONDONTWRITEBYTECODE=1 "$BSENV/bin/python3.11" -c "import updater" 2>&1
}

reqs_hash_current() {
    local want have
    want=$(md5sum "$BS_PATH/scripts/requirements.txt" 2>/dev/null | cut -d' ' -f1)
    have=$(cat "$BSENV/.blockscreen-reqs-hash" 2>/dev/null)
    [ -n "$want" ] && [ "$want" = "$have" ]
}

# A venv restored from another image keeps the donor's pyvenv.cfg, so pip installs land somewhere nobody runs.
venv_prefix_ok() {
    local p
    p=$("$BSENV/bin/python3.11" -c 'import sys; print(sys.prefix)' 2>/dev/null)
    [ "$p" = "$BSENV" ] || {
        echo "sys.prefix=$p, expected $BSENV (venv relocated or copied)"
        return 1
    }
}

# The bounded-retry sentinel survives only while pip keeps failing, so its presence means a partly installed venv.
no_pip_retry_sentinel() {
    local f="$BSENV/.blockscreen-reqs-attempt"
    [ -f "$f" ] || return 0
    echo "pip retry sentinel present: $(cat "$f") (requirements never installed cleanly)"
    return 1
}

# busctl list merges acquired and activatable names, and com.blockscreen.Updater.service alone makes
# ours activatable, so only --acquired tells a live daemon from a dead one. Never Ping here: that
# would bus-activate the service and break the read-only contract.
dbus_name_available() {
    busctl --system list --acquired --no-legend 2>/dev/null |
        grep -q '^com\.blockscreen\.Updater[[:space:]]' || {
        echo "name not acquired on the system bus (daemon down, only activatable)"
        return 1
    }
}

updater_running() {
    systemctl is-active --quiet BlocksScreen-updater ||
        pgrep -f 'updater\.dbus_service|updater/main\.py|updater\.cli' >/dev/null 2>&1
}

# StartLimitIntervalSec=0 means a crash-looping daemon reports "activating" forever, never "failed".
updater_not_crashlooping() {
    local n
    n=$(systemctl show BlocksScreen-updater -p NRestarts --value 2>/dev/null)
    case "$n" in '' | *[!0-9]*) return 0 ;; esac
    [ "$n" -lt 5 ] && return 0
    echo "BlocksScreen-updater restarted ${n}x this boot (crash loop, updates dead)"
    return 1
}

# flock dies with its holder, so a leftover file is harmless and "held by nobody" is unobservable.
# The real fault is a live holder that is not the daemon or one of its children: the next update blocks.
no_stale_updater_lock() {
    local f holders pid kids p
    command -v fuser >/dev/null 2>&1 || return 0
    pid=$(systemctl show BlocksScreen-updater -p MainPID --value 2>/dev/null)
    case "${pid:-x}" in '' | *[!0-9]*) pid=0 ;; esac
    kids=$(pgrep -P "$pid" 2>/dev/null | tr '\n' ' ')
    for f in /run/blockscreen/updater.lock "$BS_HOME/.cache/blockscreen/updater.lock"; do
        [ -f "$f" ] || continue
        holders=$(fuser "$f" 2>/dev/null | tr -s ' ' '\n' | grep -E '^[0-9]+$')
        for p in $holders; do
            case " $pid $kids " in *" $p "*) continue ;; esac
            echo "$f held by pid $p ($(ps -o args= -p "$p" 2>/dev/null | cut -c1-60)), not the updater"
            return 1
        done
    done
    return 0
}

no_updater_errors() {
    ! journalctl -u BlocksScreen-updater -b 2>/dev/null |
        grep -Eiq 'traceback|brick|CRITICAL|aborting update'
}

# A wedged _run leaves a long-lived child under the daemon: the box looks idle and every future update is dead.
no_wedged_updater_child() {
    local pid kid age cmd
    pid=$(systemctl show BlocksScreen-updater -p MainPID --value 2>/dev/null)
    case "${pid:-x}" in '' | 0 | *[!0-9]*) return 0 ;; esac
    for kid in $(pgrep -P "$pid" 2>/dev/null); do
        age=$(ps -o etimes= -p "$kid" 2>/dev/null | tr -dc '0-9')
        case "${age:-x}" in '' | *[!0-9]*) continue ;; esac
        [ "$age" -lt 900 ] && continue
        cmd=$(ps -o args= -p "$kid" 2>/dev/null | cut -c1-80)
        echo "updater child pid $kid running ${age}s: $cmd (wedged subprocess, updates blocked)"
        return 1
    done
    return 0
}

# The daemon rewrites this file at every step, so a cold one left mid-sequence means an update died halfway.
updater_status_complete() {
    local f=/run/blockscreen/updater_status.json s t
    [ -f "$f" ] || return 0
    file_fresher_than "$f" 900 && return 0
    s=$(grep -o '"step":[ ]*[0-9]*' "$f" | tr -dc '0-9')
    t=$(grep -o '"total":[ ]*[0-9]*' "$f" | tr -dc '0-9')
    [ -n "$s" ] && [ -n "$t" ] && [ "$s" != "$t" ] || return 0
    echo "last update stopped at step $s of $t: $(cat "$f")"
    return 1
}

# Stale apt lists make the update count read zero, so the operator is told a box is current when it is not.
apt_lists_fresh() {
    local newest age
    newest=$(find /var/lib/apt/lists -maxdepth 1 -name '*_Packages*' -printf '%T@\n' 2>/dev/null | sort -rn | head -1 | cut -d. -f1)
    case "${newest:-x}" in '' | *[!0-9]*) return 0 ;; esac
    age=$(($(date +%s) - newest))
    [ "$age" -lt 604800 ] || {
        echo "apt lists $((age / 86400)) days old (apt-get update has not run)"
        return 1
    }
}

# Anchored to the UI's own start so a successful --fix plus restart is not judged by pre-fix lines.
no_proxy_errors() { ! journal_since_start BlocksScreen | grep -q '32601'; }

proxy_works() {
    curl -s -m 5 -X POST "$MOON/server/spoolman/proxy" -H 'Content-Type: application/json' \
        -d '{"request_method":"GET","path":"/v1/spool"}' 2>/dev/null | grep -q '"result"'
}

# /server/info keeps loaded and failed components in separate arrays, so slice before matching.
moon_component_array() {
    curl -s -m 5 "$MOON/server/info" 2>/dev/null | tr -d ' \n' |
        sed "s/.*\"$1\":\[//; s/\].*//"
}
moon_component_loaded() { moon_component_array components | grep -q "\"$1\""; }
moon_no_failed_components() {
    local f
    f=$(moon_component_array failed_components)
    [ -z "$f" ] || { echo "failed_components: $f"; return 1; }
}

# The effective config only lists components that actually loaded, unlike orig which mirrors the file.
server_config_has_spoolman() {
    curl -s -m 5 "$MOON/server/config" 2>/dev/null | tr -d ' \n' |
        sed 's/,"orig":.*//; s/.*"config"://' | grep -q '"spoolman"'
}

mtime() { stat -c '%Y' "$1" 2>/dev/null || echo 0; }

# The provisioning race: the venv landed after the UI start script already gave up on editing moonraker.conf.
spoolman_section_present() { grep -q '^\[spoolman\]' "$CONF" 2>/dev/null; }
no_spoolman_venv_race() {
    [ -d "$BS_HOME/Spoolman/.venv" ] || return 0
    spoolman_section_present && return 0
    echo "Spoolman/.venv exists but [spoolman] missing from moonraker.conf"
    return 1
}
moonraker_read_current_conf() {
    local st
    st=$(unit_ts moonraker ActiveEnterTimestamp) || return 0
    [ "$(mtime "$CONF")" -le "$st" ] ||
        { echo "moonraker.conf edited after moonraker started, restart pending"; return 1; }
}
# Scoped to Spoolman: RF50-Klipper/katapult legitimately have no venv and log the same line.
no_missing_venv_in_updater_log() {
    ! journalctl -u BlocksScreen-updater -b 2>/dev/null |
        grep -q 'No venv found for [^,]*/Spoolman,'
}

# moonraker.asvc is a case-sensitive allowlist, a missing entry silently breaks update restarts.
asvc_has() { grep -qx "$1" "$BS_HOME/printer_data/moonraker.asvc" 2>/dev/null; }
no_restart_denied() {
    ! journalctl -u moonraker -b 2>/dev/null | grep -q 'not permitted to restart service'
}

# Klipper print_stats state, empty when moonraker/klipper is unreachable.
printer_state() {
    curl -s -m 5 "$MOON/printer/objects/query?print_stats" 2>/dev/null |
        tr '{},' '\n' | grep '"state"' | head -1 | cut -d'"' -f4
}
get_state() {
    [ -n "$STATE" ] || STATE=$(printer_state)
    echo "$STATE"
}

has_macro() { echo "$MACROS" | grep -qi "gcode_macro $1"; }

# The files klipper actually loads: printer.cfg plus its includes. Recursing the whole tree instead
# picks up .bak files, dated backups and staged cfgs for boards this variant does not ship.
active_cfgs() {
    local dir="$BS_HOME/printer_data/config" root inc g
    root="$dir/printer.cfg"
    [ -f "$root" ] || return 0
    echo "$root"
    awk '/^\[include /{sub(/^\[include[ \t]+/, ""); sub(/\].*$/, ""); sub(/[ \t]+$/, ""); print}' "$root" |
        while read -r inc; do
            case "$inc" in
                *'*'*) for g in "$dir"/$inc; do [ -f "$g" ] && echo "$g"; done ;;
                *) [ -f "$dir/$inc" ] && echo "$dir/$inc" ;;
            esac
        done
}

# A board that was never flashed or never enumerated leaves its serial path absent, which klippy reports late and vaguely.
printer_serials_exist() {
    local p bad="" files
    files=$(active_cfgs)
    [ -n "$files" ] || return 0
    # Split on the colon, not on whitespace: klipper accepts "serial:/dev/x" with no space after it.
    for p in $(grep -hE '^[[:space:]]*serial:' $files 2>/dev/null |
        sed 's/^[[:space:]]*serial:[[:space:]]*//; s/[[:space:]]*[#;].*$//; s/[[:space:]]*$//' |
        grep '^/dev/' | sort -u); do
        [ -e "$p" ] || bad="$bad $p"
    done
    [ -z "$bad" ] || {
        echo "serial device(s) absent (board unflashed, unplugged or renamed):$bad"
        return 1
    }
}

# A board left on an older Klipper build still connects, then fails in ways that look like wiring faults.
mcu_versions_match() {
    local host name v bad=""
    host=$(curl -s -m 5 "$MOON/printer/info" 2>/dev/null | tr '{},' '\n' | grep '"software_version"' | cut -d'"' -f4)
    [ -n "$host" ] || return 0
    for name in $(echo "$MACROS" | grep -o '"mcu[^"]*"' | tr -d '"' | tr ' ' '~' | sort -u); do
        v=$(curl -s -m 5 --get --data-urlencode "$(echo "$name" | tr '~' ' ')" "$MOON/printer/objects/query" 2>/dev/null |
            tr '{},' '\n' | grep '"mcu_version"' | head -1 | cut -d'"' -f4)
        [ -z "$v" ] || [ "$v" = "$host" ] || bad="$bad $(echo "$name" | tr '~' ' ')=$v"
    done
    [ -z "$bad" ] || {
        echo "host klipper $host, mcu firmware:$bad (reflash needed)"
        return 1
    }
}

# An MCU shutdown is the signature of a wiring, power or crystal fault on a freshly built machine.
no_mcu_faults() {
    local f="$BS_HOME/printer_data/logs/klippy.log" out
    [ -f "$f" ] || return 0
    out=$(tail -n 4000 "$f" 2>/dev/null |
        grep -Ei 'Lost communication with MCU|MCU .*shutdown|Timer too close|Unable to connect' | tail -3)
    [ -z "$out" ] || { echo "$out"; return 1; }
}

# An ADC or heater fault on a freshly built machine is an unplugged or shorted probe, not a tuning problem.
no_adc_faults() {
    local f="$BS_HOME/printer_data/logs/klippy.log" out
    [ -f "$f" ] || return 0
    out=$(tail -n 4000 "$f" 2>/dev/null |
        grep -Ei 'ADC out of range|not heating at expected rate|Thermistor .*out of range|Heater .*above maximum' | tail -3)
    [ -z "$out" ] || { echo "$out"; return 1; }
}

# The last Stats line is klipper's own link and load telemetry, which is the only in-log evidence of a
# marginal cable or an overloaded board before it turns into a shutdown mid-print.
klippy_stats_line() {
    local f="$BS_HOME/printer_data/logs/klippy.log"
    [ -f "$f" ] || return 1
    tail -n 3000 "$f" 2>/dev/null | grep '^Stats ' | tail -1 | grep .
}

# Klipper prints one key set per MCU on the same line, so report the worst board rather than the first.
kstat_max() {
    local line
    line=$(klippy_stats_line) || return 1
    printf '%s\n' "$line" | tr ' ' '\n' | grep "^$1=" | cut -d= -f2 |
        awk 'BEGIN { m = "" } { if (m == "" || $1 + 0 > m + 0) m = $1 } END { if (m != "") print m }' | grep .
}

# Invalid bytes are data the host could not parse at all: a bad cable, a bad crimp or EMI, never config.
no_invalid_serial_bytes() {
    local v
    v=$(kstat_max bytes_invalid) || return 0
    case "${v:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$v" -eq 0 ] || {
        echo "bytes_invalid=$v, corrupt data on the MCU link (cable, crimp or EMI)"
        return 1
    }
}

# Retransmits recover silently, but a healthy build sits in single digits: more means a marginal link.
few_serial_retransmits() {
    local v
    v=$(kstat_max bytes_retransmit) || return 0
    case "${v:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$v" -le 500 ] || {
        echo "bytes_retransmit=$v, link is retrying often (cable, hub or USB port)"
        return 1
    }
}

# Klipper's own rule of thumb: avg + 3*stddev over 2.5ms means the board is running out of time.
mcu_task_headroom_ok() {
    local avg sd
    avg=$(kstat_max mcu_task_avg) || return 0
    sd=$(kstat_max mcu_task_stddev) || return 0
    case "${avg:-x}" in '' | *[!0-9.eE+-]*) return 0 ;; esac
    case "${sd:-x}" in '' | *[!0-9.eE+-]*) return 0 ;; esac
    awk -v a="$avg" -v s="$sd" 'BEGIN { exit (a + 3 * s > 0.0025) ? 1 : 0 }' || {
        echo "mcu_task_avg=$avg stddev=$sd exceeds klipper's 2.5ms budget"
        return 1
    }
}

# adj is the crystal speed klipper measured: more than 1% off nominal is a clock or power defect.
mcu_clock_sane() {
    local line
    line=$(klippy_stats_line) || return 0
    printf '%s\n' "$line" | tr ' ' '\n' | awk -F= '
        /^freq=/ { f = $2 + 0 }
        /^adj=/ {
            a = $2 + 0
            if (f > 0 && a > 0) {
                d = (a - f) / f
                if (d < 0) d = -d
                if (d > 0.01) { printf "clock drift %.2f%% (freq=%d adj=%d)\n", d * 100, f, a; bad = 1 }
            }
        }
        END { exit bad ? 1 : 0 }'
}

# print_stall counts the times the host could not feed the MCU in time, the step before Timer too close.
no_print_stalls() {
    local v
    v=$(kstat_max print_stall) || return 0
    case "${v:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$v" -eq 0 ] || {
        echo "print_stall=$v, the host fell behind feeding the MCU"
        return 1
    }
}

# A configured [mcu rpi] is a second klipper process: without its unit and socket klippy never connects.
linux_mcu_backed() {
    local files
    files=$(active_cfgs)
    [ -n "$files" ] || return 0
    grep -hqE '^[[:space:]]*\[mcu[[:space:]]+rpi\]' $files 2>/dev/null || return 0
    systemctl is-active --quiet klipper-mcu 2>/dev/null || {
        echo "[mcu rpi] configured but klipper-mcu.service is not active"
        return 1
    }
    [ -S /tmp/klipper_host_mcu ] || {
        echo "[mcu rpi] configured but /tmp/klipper_host_mcu socket is missing"
        return 1
    }
}

# Our units failing is a defect, a distro unit failing (e2scrub_reap, man-db) is noise, so name them either way.
failed_units() { systemctl list-units --state=failed --no-legend --plain 2>/dev/null | awk '{print $1}'; }
no_failed_units() {
    local u
    u=$(failed_units | tr '\n' ' ')
    [ -z "${u// /}" ] || {
        echo "failed units: $u"
        return 1
    }
}
no_failed_bs_units() {
    local u
    u=$(failed_units | grep -i blocksscreen | tr '\n' ' ')
    [ -z "${u// /}" ] || {
        echo "failed units: $u"
        return 1
    }
}
time_synced() { timedatectl show -p NTPSynchronized --value 2>/dev/null | grep -q yes; }
# Bits 0-3 are throttling right now, bits 16-19 only record that it happened earlier this boot.
not_throttled() {
    local v
    command -v vcgencmd >/dev/null 2>&1 || return 0
    v=$(vcgencmd get_throttled 2>/dev/null | cut -d= -f2)
    case "${v:-x}" in '' | x | *[!0-9a-fA-Fx]*) return 0 ;; esac
    [ "$v" != "0x0" ] || return 0
    if [ $((v & 0xF)) -ne 0 ]; then
        echo "throttled=$v (active right now: PSU sag or overheating)"
    else
        echo "throttled=$v (historic only since boot, not active)"
    fi
    return 1
}

cpu_temp_ok() {
    local t
    t=$(cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null) || return 0
    case "${t:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$((t / 1000))" -lt 80 ]
}

# Vendor tooling logs the card's unclean power-off tally, the practical stand-in for SD SMART data.
no_unsafe_shutdowns() {
    local n
    n=$(journalctl -b 2>/dev/null | grep -o 'Unsafe Shutdown Count: *[0-9]*' | tail -1 | tr -dc '0-9')
    [ -z "$n" ] && return 0
    [ "$n" -lt 10 ] || {
        echo "Unsafe Shutdown Count: $n"
        return 1
    }
}

# printer_data/config/config is the intended layout, only a third level is an accident (configurator._cleanup_nested).
no_nested_config_dir() {
    local p="$BS_HOME/printer_data/config/config/config"
    # -L as well as -e, the nest is a symlink and a broken one is invisible to -e alone.
    [ ! -L "$p" ] && [ ! -e "$p" ]
}
# Moonraker keeps the last of two same-named sections, so a duplicated one silently reverts our patched settings.
no_duplicate_conf_sections() {
    local dup
    dup=$(grep -oE '^\[[^]]+\]' "$1" 2>/dev/null | sort | uniq -d | tr '\n' ' ')
    [ -z "${dup// /}" ] || {
        echo "duplicated sections in $1: $dup"
        return 1
    }
}

# Klipper aborts the whole config on an include it cannot find, so the box comes up with no printer at all.
includes_resolve() {
    local dir="$1" f inc bad=""
    for f in "$dir"/*.cfg; do
        [ -f "$f" ] || continue
        while read -r inc; do
            case "$inc" in *'*'*) continue ;; esac
            [ -e "$dir/$inc" ] || bad="$bad $inc"
        done < <(awk '/^\[include /{sub(/^\[include[ \t]+/, ""); sub(/\].*$/, ""); sub(/[ \t]+$/, ""); print}' "$f")
    done
    [ -z "$bad" ] || {
        echo "missing [include] targets:$bad"
        return 1
    }
}

# Older builds log "Removed neste dir", so match the shorter prefix or the check misses them.
no_renesting_this_boot() { ! journalctl -u BlocksScreen -b 2>/dev/null | grep -q 'Removed neste'; }

# A USB stick pulled from the file browser logs I/O errors on sd*, only the boot device is a health signal.
no_kernel_errors() {
    local out root
    root=$(findmnt -no SOURCE / 2>/dev/null | sed 's|/dev/||; s|p\?[0-9]*$||')
    out=$(journalctl -k -b 2>/dev/null | grep -Ei 'Out of memory|segfault|BUG:|I/O error' |
        awk -v r="$root" '$0 ~ /dev sd[a-z]/ && $0 !~ ("dev " r) { next } { print }' | tail -5)
    [ -z "$out" ] || { echo "$out"; return 1; }
}

# Name the override file and show its head, the point of the check is which pins were forced.
no_updater_override() {
    local p="$BS_HOME/printer_data/config/blockscreen_updater.yaml"
    [ -f "$p" ] || return 0
    echo "override present: $p"
    grep -vE '^\s*(#|$)' "$p" 2>/dev/null | head -6
    return 1
}

mem_available_mb_at_least() {
    local kb
    kb=$(awk '/MemAvailable/ {print $2}' /proc/meminfo 2>/dev/null)
    case "${kb:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$((kb / 1024))" -ge "$1" ]
}

# A half-configured package leaves apt refusing every later install, which kills the Update button silently.
dpkg_consistent() {
    local out
    out=$(dpkg --audit 2>/dev/null | head -6)
    [ -z "$out" ] || { echo "$out"; return 1; }
}

# The journal is the only field diagnostic, and an unbounded one is also the usual way a small SD fills up.
journal_size_below_mb() {
    local mb
    mb=$(journalctl --disk-usage 2>/dev/null | grep -oE '[0-9.]+[KMGT]' | tail -1 |
        awk '{ n = $0 + 0; u = substr($0, length($0));
               if (u == "K") n /= 1024; else if (u == "G") n *= 1024; else if (u == "T") n *= 1048576;
               printf "%d", n }')
    case "${mb:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$mb" -lt "$1" ] || {
        echo "journal using ${mb} MiB (limit $1)"
        return 1
    }
}

# Editing a repo-symlinked unit is the common cause, so this is advisory: it only means systemd holds an older copy.
no_daemon_reload_pending() {
    local u
    for u in "$@"; do
        systemctl show "$u" -p NeedDaemonReload --value 2>/dev/null | grep -q yes && {
            echo "$u changed on disk since the last daemon-reload"
            return 1
        }
    done
    return 0
}

has_default_route() { ip route show default 2>/dev/null | grep -q .; }
dns_resolves() { getent hosts github.com >/dev/null 2>&1; }

# Commissioning means the operator reaches Mainsail from a laptop, which a localhost probe never proves.
lan_moonraker_ok() {
    local ip
    ip=$(hostname -I 2>/dev/null | awk '{print $1}')
    [ -n "$ip" ] || return 0
    curl_matches 6 "http://$ip:7125/server/info" '"result"' || {
        echo "moonraker unreachable on LAN address $ip (bound to localhost or firewalled)"
        return 1
    }
}

# Mainsail loads over the LAN and then 401s on every call when the box subnet is missing from trusted_clients.
lan_client_trusted() {
    local ip out
    ip=$(hostname -I 2>/dev/null | awk '{print $1}')
    [ -n "$ip" ] || return 0
    out=$(curl -s -m 6 "http://$ip:7125/printer/info" 2>/dev/null)
    case "$out" in '' | *'"result"'*) return 0 ;; esac
    echo "moonraker denies API calls from $ip: $(echo "$out" | head -c 100) (add the subnet to trusted_clients)"
    return 1
}

# A box commissioned at bench-side signal strength drops off the network once it is in its final position.
wifi_signal_ok() {
    local s
    command -v nmcli >/dev/null 2>&1 || return 0
    s=$(nmcli -t -f ACTIVE,SIGNAL dev wifi 2>/dev/null | awk -F: '$1 == "yes" { print $2; exit }' | tr -dc '0-9')
    case "${s:-x}" in '' | *[!0-9]*) return 0 ;; esac
    [ "$s" -ge 40 ] || {
        echo "wifi signal ${s}%"
        return 1
    }
}
github_reachable() {
    curl -s -m 8 -o /dev/null -w '%{http_code}' https://github.com 2>/dev/null |
        grep -qE '^(200|301|302)$'
}

# chvt moved into the updater sudoers file, so ask sudo about the capability instead of a filename only old images have.
chvt_nopasswd() {
    local vt rc=0
    for vt in 7 8; do
        sudo -n -l -U "$BS_USER" /usr/bin/chvt "$vt" >/dev/null 2>&1 || {
            echo "$BS_USER may not run 'chvt $vt' without a password"
            rc=1
        }
    done
    return $rc
}

# Field boxes carry a unit whose ExecStart points at a path that no longer exists, so the hostname never gets set.
hostname_unit_ok() {
    local u=/etc/systemd/system/set-hostname.service target
    [ -f "$u" ] || {
        echo "$u missing (hostname stays the image default)"
        return 1
    }
    target=$(awk -F= '/^ExecStart=/ {print $2; exit}' "$u")
    [ -x "$target" ] || {
        echo "ExecStart=$target is not executable (stale unit from an older install)"
        return 1
    }
    unit_enabled set-hostname.service || {
        echo "set-hostname.service is not enabled"
        return 1
    }
}

# A cloned image keeps the donor hostname, so two boxes collide on mDNS and the operator flashes the wrong one.
hostname_matches_serial() {
    local serial want
    serial=$(awk '/^Serial/ {print $3; exit}' /proc/cpuinfo 2>/dev/null)
    case "${serial:-x}" in '' | x | *[!0-9a-fA-F]* | 0000000000000000) return 0 ;; esac
    want="BLOCKS-RF50-$serial"
    [ "$(hostname)" = "$want" ] || {
        echo "hostname is $(hostname), expected $want (set-hostname never ran, or this is a clone)"
        return 1
    }
}

# A box shipped with a pending reboot applies half its kernel/libc upgrade at the customer site instead.
no_reboot_required() {
    [ -f /var/run/reboot-required ] || [ -f /run/reboot-required ] || return 0
    echo "reboot pending: $(cat /run/reboot-required.pkgs 2>/dev/null | tr '\n' ' ')"
    return 1
}

# An unmapped 127.0.1.1 makes sudo and avahi hang on every lookup, which shows up as a box that is just slow.
hosts_maps_hostname() {
    local h
    h=$(hostname)
    grep -qE "^127\.0\.1\.1[[:space:]]+.*\<$h\>" /etc/hosts 2>/dev/null || {
        echo "/etc/hosts has no 127.0.1.1 entry for '$h' (sudo/avahi lookups stall)"
        return 1
    }
}

# The helper is installed byte-for-byte, so any drift means an old copy that predates the apt fixes.
apt_helper_current() {
    local src="$BS_PATH/scripts/bs-apt-helper.sh" dst=/usr/local/sbin/bs-apt-helper
    [ -f "$src" ] || return 0
    [ -x "$dst" ] || {
        echo "$dst missing (updater apt path falls back to a raw apt, or fails)"
        return 1
    }
    cmp -s "$src" "$dst" || {
        echo "$dst differs from $src (stale helper from an older install)"
        return 1
    }
}

# Without this rule every apt step of an update prompts for a password nobody can type on a touchscreen.
apt_helper_nopasswd() {
    sudo -n -l -U "$BS_USER" /usr/local/sbin/bs-apt-helper update >/dev/null 2>&1 || {
        echo "$BS_USER may not run bs-apt-helper without a password (apt updates will hang)"
        return 1
    }
}

polkit_rule_present() {
    [ -f /usr/share/polkit-1/rules.d/90-BlocksScreen.rules ] ||
        [ -f /etc/polkit-1/rules.d/90-BlocksScreen.rules ] ||
        [ -f /etc/polkit-1/localauthority/50-local.d/20-blocksscreen.pkla ]
}

# Components declared in the updater manifest, one "name|path|branch|url" row each.
components() {
    local f="$BS_PATH/updater/components.yaml"
    [ -f "$f" ] || return 1
    awk '
        function v(s) { gsub(/^[ \t]*["\x27]|["\x27][ \t]*$/, "", s); return s }
        /^  - name:/ { if (n != "") print n "|" p "|" b "|" u; n = v($3); p = ""; b = ""; u = "" }
        /^    path:/   { p = v($2) }
        /^    branch:/ { b = v($2) }
        /^    url:/    { u = v($2) }
        END { if (n != "") print n "|" p "|" b "|" u }
    ' "$f"
}

# awk exits 0 on a manifest it cannot parse and both consumers then iterate nothing, so the repo and
# deep checks vanish while the summary still reads ALL PASS. Assert the row count instead.
components_ok() {
    local n
    n=$(components | grep -c '|')
    case "${n:-x}" in '' | *[!0-9]*) n=0 ;; esac
    [ "$n" -ge 6 ] || {
        echo "parsed $n components, expected >= 6 (manifest format changed, repo+deep checks would silently vanish)"
        return 1
    }
}

# Branch ground truth is the operator, not the box manifest: "Name=branch,Name=branch", empty when unset.
# A local override pins a component deliberately, so its branch is the expectation, not a deviation.
override_branch_for() {
    local p="$BS_HOME/printer_data/config/blockscreen_updater.yaml" out
    [ -f "$p" ] || return 1
    out=$(awk -v want="$1" '
        /^[[:space:]]*-?[[:space:]]*name:/ { n = $NF; gsub(/["\x27]/, "", n) }
        /^[[:space:]]*branch:/ { b = $NF; gsub(/["\x27]/, "", b); if (n == want) { print b; exit } }
    ' "$p")
    [ -n "$out" ] || return 1
    echo "$out"
}

expect_branch_for() {
    local pair
    for pair in $(echo "$EXPECT_BRANCH" | tr ',' ' '); do
        [ "${pair%%=*}" = "$1" ] && {
            echo "${pair#*=}"
            return 0
        }
    done
    return 1
}

# --- sections ---

sec_host() {
    local serial expect
    info "host    $(hostname)   $(date '+%F %T')"
    info "kernel  $(uname -r)   uptime$(uptime -p 2>/dev/null | sed 's/^up//')"
    info "model   $(read_model)"
    info "user    $BS_USER   home=$BS_HOME   repo=$BS_PATH"
    info "printer state: $(get_state)"
    serial=$(awk '/Serial/ {print $3}' /proc/cpuinfo 2>/dev/null)
    # A cloned SD card keeps the donor hostname, so a mismatch means duplicate identities on the fleet.
    if [ -n "$serial" ]; then
        expect="BLOCKS-RF50-$serial"
        warn "hostname matches board serial" str_is "$(hostname)" "$expect"
        [ "$(hostname)" = "$expect" ] || info "hostname $(hostname), serial says $expect"
    fi
    check "repo checkout present" test -d "$BS_PATH/.git"
}

sec_system() {
    check "root filesystem writable" rootfs_writable
    warn "root filesystem expanded (>= 8 GiB)" rootfs_expanded
    check "free space on / >= 500 MiB" free_mb_at_least / 500
    check "free space on home >= 500 MiB" free_mb_at_least "$BS_HOME" 500
    warn "free inodes on / >= 10%" free_inodes_pct_at_least / 10
    warn "available memory >= 100 MiB" mem_available_mb_at_least 100
    check "no failed BlocksScreen units" no_failed_bs_units
    warn "no failed systemd units" no_failed_units
    warn "clock synchronised (NTP)" time_synced
    warn "no undervoltage/throttling" not_throttled
    warn "CPU temperature < 80 C" cpu_temp_ok
    jwarn "no OOM/segfault/IO errors in kernel log" no_kernel_errors
    jwarn "SD unsafe shutdown count below 10" no_unsafe_shutdowns
    warn "persistent journal (/var/log/journal)" test -d /var/log/journal
    warn "journal below 400 MiB" journal_size_below_mb 400
    check "dpkg database consistent" dpkg_consistent
    warn "no pending reboot" no_reboot_required
}

sec_services() {
    local u n
    for u in BlocksScreen BlocksScreen-xorg BlocksScreen-updater klipper moonraker Spoolman; do
        check "$u active" unit_active "$u"
    done
    for u in BlocksScreen BlocksScreen-xorg BlocksScreen-updater BlocksScreen-deploy.path; do
        check "$u enabled" unit_enabled "$u"
    done
    # Active but not enabled survives now and dies at the next boot, the classic half-provisioned box.
    for u in klipper moonraker Spoolman; do
        check "$u enabled" unit_enabled "$u"
    done
    warn "BlocksScreen-splash-holder enabled" unit_enabled BlocksScreen-splash-holder
    warn "udiskie active (USB automount)" unit_active udiskie
    # Load-bearing: a box with no SSH must never be rate-limited out of restarting.
    for u in BlocksScreen BlocksScreen-xorg BlocksScreen-updater; do
        check "$u start rate limiting disabled" start_limit_disabled "$u"
    done
    warn "no pending daemon-reload" no_daemon_reload_pending BlocksScreen BlocksScreen-xorg BlocksScreen-updater Spoolman
    check "BlocksScreen is Type=notify" unit_prop_is BlocksScreen Type notify
    check "BlocksScreen watchdog armed" unit_prop_isnt BlocksScreen WatchdogUSec 0
    jcheck "no watchdog kill this boot" no_watchdog_kill
    check "default target is multi-user" str_is "$(systemctl get-default 2>/dev/null)" multi-user.target
    for u in BlocksScreen BlocksScreen-xorg BlocksScreen-updater Spoolman moonraker klipper; do
        n=$(systemctl show "$u" -p NRestarts --value 2>/dev/null)
        case "${n:-x}" in '' | *[!0-9]*) continue ;; esac
        info "$(printf '%-24s NRestarts=%s' "$u" "$n")"
        # Name stays constant across runs so JSON rows are diffable, the count goes in the detail.
        # Both branches record or a healthy box emits no row at all and JSON runs stop being comparable.
        if [ "$n" -gt 3 ]; then
            record WARN "$u restart count sane" "restarted $n times, crash loop behind an active state?"
        else
            record PASS "$u restart count sane"
        fi
    done
    return 0
}

sec_ui() {
    check "UI process running" proc_running "BlocksScreen/BlocksScreen.py"
    check "UI watchdog fresh (event loop alive)" watchdog_fresh
    check "X server socket present" test -S /tmp/.X11-unix/X0
    check "Xorg process running" pgrep -x Xorg
    check "Xorg owns the active VT" xorg_vt_active
    check "touchscreen input device present" touchscreen_present
    warn "display connector connected" display_connected
    warn "UI memory below 700 MiB" ui_rss_below_mb 700
    check "no crash log from this run" log_predates_start "$BS_PATH/logs/blocksscreen_crash.log"
    check "no fault log from this run" log_predates_start "$BS_PATH/logs/blocksscreen_fault.log"
    jcheck "no traceback in journal since start" no_traceback_since_start
    check "boot_attempts counter cleared" boot_counter_clear
    warn "last_good_commit matches HEAD" last_good_is_head
    warn "UI log written in the last 10 min" file_fresher_than "$BS_PATH/logs/BlocksScreen.log" 600
    warn "splash raw cache precomputed" test -f "$BS_HOME/.cache/blockscreen/splash.raw"
    warn "splash png present" test -f "$BS_HOME/.cache/blockscreen/splash.png"
    check "logs dir is setgid 2775" mode_is "$BS_PATH/logs" 2775
    check "logs dir group is blocksscreen" group_is "$BS_PATH/logs" blocksscreen
}

sec_install() {
    local g
    # The three artifacts bs-deploy-check.sh watches: any one missing re-runs install-updater.sh.
    check "dbus policy installed" test -f /etc/dbus-1/system.d/com.blockscreen.Updater.conf
    check "dbus service file installed" test -f /usr/share/dbus-1/system-services/com.blockscreen.Updater.service
    check "deploy path unit installed" test -f /etc/systemd/system/BlocksScreen-deploy.path
    check "deploy service installed" test -f /etc/systemd/system/BlocksScreen-deploy.service
    check "updater unit installed" test -f /etc/systemd/system/BlocksScreen-updater.service
    check "Spoolman unit installed" test -f /etc/systemd/system/Spoolman.service
    check "xorg unit installed" test -f /etc/systemd/system/BlocksScreen-xorg.service
    check "apt helper installed" test -x /usr/local/sbin/bs-apt-helper
    check "apt helper owned by root" owner_is /usr/local/sbin/bs-apt-helper root:root
    check "apt helper mode 755" mode_is /usr/local/sbin/bs-apt-helper 755
    check "BlocksScreen.service is a repo symlink" is_symlink /etc/systemd/system/BlocksScreen.service
    rcheck "sudoers: updater rules present" test -f /etc/sudoers.d/blockscreen-updater
    rcheck "sudoers: updater rules parse" visudo -cf /etc/sudoers.d/blockscreen-updater
    rcheck "sudoers: updater rules mode 440" mode_is /etc/sudoers.d/blockscreen-updater 440
    rcheck "sudoers: chvt 7/8 permitted" chvt_nopasswd
    # polkit rules.d is root-only, so an unprivileged run cannot see these files and must not claim they are missing.
    rcheck "polkit: daemon-reload rule" test -f /etc/polkit-1/rules.d/10-blockscreen-reload.rules
    rwarn "polkit: NetworkManager/power rule" polkit_rule_present
    check "Xwrapper allows any user" file_has /etc/X11/Xwrapper.config '^allowed_users=anybody'
    check "Xwrapper keeps root rights" file_has /etc/X11/Xwrapper.config '^needs_root_rights=yes'
    warn "kiosk xorg snippet" test -f /etc/X11/xorg.conf.d/99-bs-kiosk.conf
    warn "resolution xorg snippet" test -f /etc/X11/xorg.conf.d/97-bs-resolution.conf
    warn "NetworkManager any-user policy" test -f /etc/NetworkManager/conf.d/any-user.conf
    check "set-hostname unit installed and enabled" hostname_unit_ok
    check "hostname derived from CPU serial" hostname_matches_serial
    check "/etc/hosts maps this hostname" hosts_maps_hostname
    check "apt helper matches repo copy" apt_helper_current
    rcheck "sudoers: apt helper permitted" apt_helper_nopasswd
    check "env file present" test -f "$BS_HOME/.config/blockscreen/env"
    check "env file declares BS_DIR" file_has "$BS_HOME/.config/blockscreen/env" '^BS_DIR='
    check "env file declares BSENV" file_has "$BS_HOME/.config/blockscreen/env" '^BSENV='
    check "group blocksscreen exists" getent group blocksscreen
    for g in tty video plugdev netdev blocksscreen; do
        check "$BS_USER in group $g" in_group "$g"
    done
    warn "$BS_USER in group network" in_group network
    check "cache dir present" test -d "$BS_HOME/.cache/blockscreen"
    check "git hooks path is scripts" git_config_is "$BS_PATH" core.hooksPath scripts
    check "post-merge hook executable" test -x "$BS_PATH/scripts/post-merge"
    warn "system safe.directory for repo" git_system_safe_dir "$BS_PATH"
    warn "desktop entry installed" test -f "$BS_HOME/.local/share/applications/BlocksScreen.desktop"
    warn "app icon installed" test -f /usr/share/icons/hicolor/scalable/apps/BlocksScreen.png
}

sec_config() {
    check "moonraker.conf exists" test -f "$CONF"
    check "moonraker.conf has [update_manager BlocksScreen]" file_has "$CONF" '^\[update_manager BlocksScreen\]'
    check "system updates disabled in moonraker" file_has "$CONF" '^enable_system_updates: *False'
    check "managed_services migrated off klipper/moonraker" not_grep "$CONF" '^managed_services: *klipper +moonraker'
    warn "single-owner marker for overlapping repos" file_has "$CONF" 'blocksscreen-single-owner'
    check "exactly one [spoolman] section" grep_count_is_one '^\[spoolman\]' "$CONF"
    check "no duplicated moonraker.conf sections" no_duplicate_conf_sections "$CONF"
    check "every [include] resolves" includes_resolve "$BS_HOME/printer_data/config"
    check "no merge leftovers in config" no_merge_leftovers "$BS_HOME/printer_data/config"
    check "no config/config/config over-nest" no_nested_config_dir
    jwarn "no config re-nesting this boot" no_renesting_this_boot
    check "BlocksScreen.cfg exists" test -f "$BS_HOME/printer_data/config/BlocksScreen.cfg"
    check "BlocksScreen.cfg has [server]" file_has "$BS_HOME/printer_data/config/BlocksScreen.cfg" '^\[server\]'
    check "printer.cfg exists" test -f "$BS_HOME/printer_data/config/printer.cfg"
    check "gcodes dir writable" user_writable "$BS_HOME/printer_data/gcodes"
    check "config dir writable" user_writable "$BS_HOME/printer_data/config"
    warn "updater override absent (stock manifest)" no_updater_override
    if [ -f "$CONF" ]; then
        info "moonraker.conf     $(stat -c '%y' "$CONF" 2>/dev/null)"
        info "moonraker.conf.bak $(stat -c '%y' "$CONF.bak" 2>/dev/null || echo missing)"
    fi
}

sec_klipper() {
    local st m
    check "klippy reachable" curl_matches 5 "$MOON/printer/info" '"state"'
    st=$(curl -s -m 5 "$MOON/printer/info" 2>/dev/null | tr '{},' '\n' | grep '"state":' | head -1 | cut -d'"' -f4)
    info "klippy state: ${st:-unknown}"
    check "klippy state is ready" str_is "$st" ready
    check "printer objects queryable" curl_matches 5 "$MOON/printer/objects/list" '"objects"'
    MACROS=$(curl -s -m 5 "$MOON/printer/objects/list" 2>/dev/null | tr ',' '\n')
    if [ -n "$MACROS" ]; then
        # BLOCKSCREEN_DEV is an env var read by mainWindow, never a gcode macro, so it is not listed here.
        for m in CLEAN_NOZZLE CHANGE_PRINTCORES; do
            warn "macro $m defined" has_macro "$m"
        done
    fi
    check "mcu object present" has_macro_free_mcu
    check "configured serial devices exist" printer_serials_exist
    check "host mcu service backs [mcu rpi]" linux_mcu_backed
    warn "mcu firmware matches host klipper" mcu_versions_match
    check "no MCU fault in klippy.log" no_mcu_faults
    check "no thermistor or heater fault in klippy.log" no_adc_faults
    check "no corrupt bytes on the mcu link" no_invalid_serial_bytes
    warn "mcu link retransmits low" few_serial_retransmits
    warn "mcu task time within budget" mcu_task_headroom_ok
    check "mcu clock within 1% of nominal" mcu_clock_sane
    warn "no print stalls recorded" no_print_stalls
}

# The mcu object only exists once klippy connected to the board, so it doubles as an MCU check.
has_macro_free_mcu() { echo "$MACROS" | grep -q '"mcu"'; }

# Moonraker nests each app under version_info, so split on the object keys to name the ones that are behind.
behind_components() {
    echo "$1" | sed 's/"\([A-Za-z0-9_.-]*\)": *{/\n@@\1 /g' |
        awk '/^@@/ { name = substr($1, 3) }
             /"commits_behind_count": *[1-9]/ {
                 match($0, /"commits_behind_count": *[0-9]+/)
                 n = substr($0, RSTART, RLENGTH); sub(/.*: */, "", n)
                 print name ": " n " commit(s) behind"
             }'
}

sec_moonraker() {
    local upd behind detail
    check "moonraker API up (:7125)" curl_matches 5 "$MOON/server/info" '"result"'
    check "moonraker reports klippy_connected" curl_matches 5 "$MOON/server/info" '"klippy_connected": *true'
    warn "moonraker has no unexpected warnings" moon_unexpected_warnings
    check "machine info available" curl_matches 5 "$MOON/machine/system_info" '"system_info"'
    check "no failed moonraker components" moon_no_failed_components
    check "moonraker allowed to restart our services" asvc_ok
    jwarn "no restart denied by moonraker.asvc this boot" no_restart_denied
    warn "moonraker detected every component version" version_detect_ok
    warn "web assets up to date" web_versions_current
    upd=$(curl -s -m 20 "$MOON/machine/update/status?refresh=false" 2>/dev/null)
    # An error payload counts zero components behind and would read as "up to date", passing hardest
    # on the one box whose only field remediation path is already broken.
    case "$upd" in
        *'"version_info"'*)
            behind=$(echo "$upd" | tr ',' '\n' | grep -c '"commits_behind_count": *[1-9]')
            if [ "$behind" -gt 0 ]; then
                detail=$(behind_components "$upd")
                # Fall back to the raw fields if moonraker ever reshapes the payload, a named component is the whole point.
                [ -n "$detail" ] || detail=$(echo "$upd" | tr ',' '\n' | grep -E 'commits_behind_count|corrupt')
                record FAIL "all components up to date" "$detail"
            else
                record PASS "all components up to date"
            fi
            ;;
        *'"error"'*)
            record FAIL "update status readable" "$(echo "$upd" | tr -d '\n' | cut -c1-200)"
            ;;
        *)
            record WARN "update status unavailable (moonraker down or slow)"
            ;;
    esac
}

not_curl_match() { ! curl -s -m 5 "$1" 2>/dev/null | grep -q "$2"; }

# Only BlocksScreen is asserted: moonraker permits klipper and moonraker implicitly, and our updater restarts Spoolman itself.
asvc_ok() {
    asvc_has BlocksScreen || {
        echo "BlocksScreen missing from $BS_HOME/printer_data/moonraker.asvc"
        # A pre-rename image carries the old unit name instead, which is the usual cause.
        asvc_has BlocksPrinter && echo "found legacy BlocksPrinter entry, image predates the current installer"
        return 1
    }
}

# git describe --tags cannot name a version on a fork, moonraker then reports "?" and disables updates.
version_detect_ok() {
    local v
    v=$(update_status | tr ',' '\n' | grep -E '"[a-z_]*version[a-z_]*": *"\?"')
    [ -z "$v" ] || {
        echo "undetected versions:"
        echo "$v"
        return 1
    }
}

update_status() { curl -s -m 20 "$MOON/machine/update/status?refresh=false" 2>/dev/null; }

# Apps whose local version differs from the remote one, "name local -> remote" per line.
outdated_apps() {
    update_status | tr -d ' \n' | awk 'BEGIN { RS = "\"name\":\"" }
        NR > 1 {
            n = substr($0, 1, index($0, "\"") - 1)
            v = ""; rv = ""
            if (match($0, /"version":"[^"]*"/))        v  = substr($0, RSTART + 11, RLENGTH - 12)
            if (match($0, /"remote_version":"[^"]*"/)) rv = substr($0, RSTART + 18, RLENGTH - 19)
            if (v != "" && rv != "" && v != rv && v != "?" && rv != "?") print n " " v " -> " rv
        }'
}

web_versions_current() {
    local o
    o=$(outdated_apps)
    [ -z "$o" ] || {
        echo "$o"
        return 1
    }
}

# Our forks sit on non-official remotes by design, so those warnings are expected and never faults.
moon_unexpected_warnings() {
    local w
    # Char scan, not sed: warning strings contain commas and brackets ("[update_manager BlocksScreen]").
    w=$(curl -s -m 5 "$MOON/server/info" 2>/dev/null | tr -d '\n' |
        awk '{
            i = index($0, "\"warnings\":")
            if (i == 0) exit
            $0 = substr($0, i + 11)
            i = index($0, "[")
            if (i == 0) exit
            instr = 0; esc = 0; cur = ""
            for (p = i + 1; p <= length($0); p++) {
                c = substr($0, p, 1)
                if (esc)          { cur = cur c; esc = 0; continue }
                if (c == "\\")    { esc = 1; continue }
                if (c == "\"")    { if (instr) { print cur; cur = "" } ; instr = !instr; continue }
                if (instr)        { cur = cur c; continue }
                if (c == "]")     { exit }
            }
        }' | grep -v '^ *$' |
        grep -Ev 'not on official remote/branch|Failed to detect current version|No valid tag|unofficial')
    [ -z "$w" ] || {
        echo "$w"
        return 1
    }
}

sec_spoolman() {
    check "Spoolman .venv provisioned" test -d "$BS_HOME/Spoolman/.venv"
    check "Spoolman API healthy (:7912)" curl_matches 5 "$SPOOL/api/v1/health" healthy
    check "spoolman database present" test -f "$BS_HOME/.local/share/spoolman/spoolman.db"
    # Slice the components array: a bare grep also matches failed_components, passing in the broken case.
    check "moonraker loaded spoolman component" moon_component_loaded spoolman
    check "moonraker effective config has spoolman" server_config_has_spoolman
    # Moonraker serialises with json.dumps defaults, so the wire form is '"key": value'.
    check "moonraker connected to spoolman" curl_matches 5 "$MOON/server/spoolman/status" '"spoolman_connected": *true'
    check "spoolman proxy call the UI makes" proxy_works
    jcheck "no -32601 in UI log since UI start" no_proxy_errors
    # The provisioning race: venv landed after the UI start script gave up editing moonraker.conf.
    check "[spoolman] section present in moonraker.conf" spoolman_section_present
    check "no venv-vs-conf provisioning race" no_spoolman_venv_race
    check "moonraker started after last moonraker.conf edit" moonraker_read_current_conf
    jcheck "no 'No venv found for' in updater log this boot" no_missing_venv_in_updater_log
}

sec_network() {
    check "NetworkManager active" unit_active NetworkManager
    check "default route present" has_default_route
    warn "DNS resolves github.com" dns_resolves
    warn "https://github.com reachable" github_reachable
    check "moonraker answers on the LAN address" lan_moonraker_ok
    warn "moonraker accepts LAN clients" lan_client_trusted
    warn "wifi signal >= 40%" wifi_signal_ok
    info "addresses:   $(hostname -I 2>/dev/null)"
    info "connections: $(nmcli -t -f NAME,TYPE,DEVICE con show --active 2>/dev/null | tr '\n' ' ')"
}

sec_updater() {
    local errs
    check "updater D-Bus name available" dbus_name_available
    check "updater not crash-looping" updater_not_crashlooping
    check "no stale updater lock" no_stale_updater_lock
    jcheck "no updater errors since boot" no_updater_errors
    check "no wedged updater subprocess" no_wedged_updater_child
    check "last update ran to completion" updater_status_complete
    warn "apt lists refreshed in the last 7 days" apt_lists_fresh
    check "components manifest readable" components_ok
    warn "deploy trigger consumed" test ! -f "$BS_HOME/.config/blockscreen/.run-install-updater"
    warn "requirements sentinel current" reqs_hash_current
    if ! $QUIET; then
        errs=$(journalctl -u BlocksScreen-updater -b 2>/dev/null |
            grep -Ei 'error|abort|failed|traceback|brick' | tail -10)
        if [ -n "$errs" ]; then
            info "recent updater errors:"
            echo "$errs" | sed 's/^/        | /'
        fi
    fi
    return 0
}

sec_repos() {
    local name path branch url dirty want
    [ -n "$EXPECT_BRANCH" ] && info "expected branches: $EXPECT_BRANCH"
    while IFS='|' read -r name path branch url; do
        [ -n "$name" ] || continue
        path=$(echo "$path" | sed "s|^~|$BS_HOME|")
        if [ ! -d "$path/.git" ]; then
            record WARN "$name checkout present"
            continue
        fi
        dirty=$(git -C "$path" status --porcelain 2>/dev/null | head -1)
        info "$(printf '%-16s %-32s %s %s' "$name" \
            "$(git -C "$path" rev-parse --abbrev-ref HEAD 2>/dev/null)" \
            "$(git -C "$path" rev-parse --short HEAD 2>/dev/null)" \
            "${dirty:+DIRTY}")"
        check "$name HEAD object intact" git_ok "$path"
        check "$name not detached" git_attached "$path"
        check "$name has no index.lock" git_no_lock "$path"
        warn "$name working tree clean" git_clean "$path"
        check "$name has no merge leftovers" no_merge_leftovers "$path"
        check "$name tracks an upstream branch" git_has_upstream "$path"
        warn "$name not ahead of upstream" git_not_ahead "$path"
        warn "$name group is blocksscreen" group_is "$path" blocksscreen
        # The operator's expectation is ground truth, the manifest is only advisory: it ships wrong branches.
        if want=$(expect_branch_for "$name"); then
            check "$name on expected branch" git_branch_is "$path" "$want"
        elif want=$(override_branch_for "$name"); then
            check "$name on override branch ($want)" git_branch_is "$path" "$want"
        elif [ -n "$branch" ]; then
            warn "$name on manifest branch" git_branch_is "$path" "$branch"
        fi
    done < <(components)
    return 0
}

sec_python() {
    local m
    check "venv python3.11 present" test -x "$BSENV/bin/python3.11"
    info "python: $("$BSENV/bin/python3.11" --version 2>&1)"
    check "venv prefix is $BSENV" venv_prefix_ok
    check "no pip retry sentinel left behind" no_pip_retry_sentinel
    # The NM binding is imported as sdbus_async.networkmanager, there is no top-level sdbus_networkmanager module.
    for m in PyQt6.QtWidgets sdbus sdbus_async.networkmanager websocket requests yaml PIL.Image qrcode numpy; do
        check "import $m" venv_import "$m"
    done
    check "updater package importable" venv_import_updater
    check "no truncated venv files" venv_no_truncated_files
    warn "pip dependency tree consistent" "$BSENV/bin/pip" check
}

# USB faults get their own script because the forensics are long and the operator needs to run them
# on their own during a repro: see bs-usb-diag.sh --watch.
sec_usb() {
    local diag st name det
    diag="$(dirname -- "$(readlink -f -- "$0")")/bs-usb-diag.sh"
    if [ ! -r "$diag" ]; then
        record SKIP "usb fault diagnostics" "bs-usb-diag.sh not found beside this script"
        return 0
    fi
    # Read in this shell, not down a pipe: record() has to reach the parent's counters.
    while IFS=$'\t' read -r st name det; do
        [ -n "$name" ] || continue
        record "$st" "$name" "$det"
    done < <(timeout 180 bash "$diag" --check 2>/dev/null)
    info "full forensics: sudo $diag        live repro: sudo $diag --watch"
}

# The UI can run, answer D-Bus and still render blank buttons, so the rendering path is exercised in
# python by a separate file: it needs PyQt6 from the venv, which shell cannot check for us.
sec_selftest() {
    local self st name det py
    self="$(dirname -- "$(readlink -f -- "$0")")/bs-selftest.py"
    if [ ! -r "$self" ]; then
        record SKIP "blocksscreen selftest" "bs-selftest.py not found beside this script"
        return 0
    fi
    py="$BSENV/bin/python3.11"
    [ -x "$py" ] || py="$BSENV/bin/python3"
    if [ ! -x "$py" ]; then
        record SKIP "blocksscreen selftest" "no venv python at $BSENV/bin"
        return 0
    fi
    # Run as the owning user: root has a different HOME, so BlocksScreen.cfg would not be found, and
    # a root-created Qt runtime dir would then be left behind for the service to trip over.
    # Read in this shell, not down a pipe: record() has to reach the parent's counters.
    local -a pre=()
    [ "$(id -u)" = 0 ] && pre=(runuser -u "$BS_USER" --)
    local rows
    rows=$(
        timeout 300 "${pre[@]}" env \
            QT_QPA_PLATFORM=offscreen \
            XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/tmp}" \
            HOME="$BS_HOME" \
            "$py" "$self" 2>/dev/null
    )
    # No rows at all means the interpreter died before its first assertion, which must not read as a
    # clean section: a silent zero-assertion pass is the false PASS this suite exists to prevent.
    if [ -z "$rows" ]; then
        record FAIL "blocksscreen selftest" "produced no output, $py could not run $self"
        return 0
    fi
    # Read in this shell, not down a pipe: record() has to reach the parent's counters.
    while IFS=$'\t' read -r st name det; do
        [ -n "$name" ] || continue
        record "$st" "$name" "$det"
    done <<<"$rows"
}

sec_deep() {
    local name path branch url
    check "all repo sources compile" "$BSENV/bin/python3.11" -c '
import pathlib, sys
bad = []
for root in sys.argv[1:]:
    for f in pathlib.Path(root).rglob("*.py"):
        try:
            compile(f.read_text(errors="replace"), str(f), "exec")
        except SyntaxError as e:
            bad.append("%s:%s: %s" % (f, e.lineno, e.msg))
print("\n".join(bad))
sys.exit(1 if bad else 0)
' "$BS_PATH/BlocksScreen" "$BS_PATH/updater"
    # Known field trap: a component pinned to a branch deleted upstream breaks updates fleet-wide.
    # With no route to github every probe is unprovable, so skip the lot rather than guess.
    if github_reachable; then
        while IFS='|' read -r name path branch url; do
            [ -n "$branch" ] && [ -n "$url" ] || continue
            check "$name branch $branch exists on origin" git_remote_has_branch "$url" "$branch"
        done < <(components)
    else
        record SKIP "remote branch existence (github unreachable)"
    fi
    warn "update status refresh succeeds" curl_matches 60 "$MOON/machine/update/status?refresh=true" '"version_info"'
    rcheck "sudo rights list cleanly" sudo -n -l -U "$BS_USER"
    return 0
}

# --- run ---

# set -u with no -e means an abort inside a section body skips the summary entirely, and with --json
# skips the whole object, while the exit status still looks like an ordinary failure.
INCOMPLETE=1
trap '[ "$INCOMPLETE" = 0 ] || printf "\n*** RUN INCOMPLETE: aborted during section %s, counts below are partial ***\n" "$CUR_SECTION" >&2' EXIT

for s in $SECTIONS; do
    enabled "$s" || continue
    CUR_SECTION="$s"
    hdr "$s"
    "sec_$s" || record FAIL "section $s completed" "section handler returned $?"
done
INCOMPLETE=0
CUR_SECTION="result"

# Every --fix below restarts services or re-arms the installer, so the guard belongs above all of
# them rather than inside the first. An unknown state means moonraker is unreachable and klipper keeps
# printing without it, so that case has to refuse too.
if $FIX; then
    STATE=$(printer_state)
    case "${STATE:-unknown}" in
        printing | paused | unknown | '')
            if $FORCE; then
                note "printer state is ${STATE:-unknown}, --force given, applying fixes anyway"
            else
                note "fixes not applied: printer state is ${STATE:-unknown} (re-run with --force or after the job)"
                FIX=false
            fi
            ;;
    esac
fi

# Opt-in remediation for the known [spoolman] provisioning race, mirrors the manual two-step fix.
if $FIX && [ -f "$CONF" ] && ! grep -q '^\[spoolman\]' "$CONF"; then
    if $FIX; then
        note "applying fix: [spoolman]"
        cp "$CONF" "$CONF.healthcheck.$(date +%Y%m%d%H%M%S).bak"
        printf '\n[spoolman]\nserver: localhost:7912\n' >>"$CONF"
        sudo -n systemctl restart moonraker.service &&
            sleep 8 &&
            sudo -n systemctl restart BlocksScreen.service ||
            note "restart failed, no passwordless sudo? restart moonraker + BlocksScreen by hand"
        note "added [spoolman], re-run to verify"
    fi
fi

# Missing install artifacts are repaired by the deploy path watcher, which only needs its trigger file.
if $FIX && { [ ! -f /etc/systemd/system/BlocksScreen-deploy.path ] ||
    [ ! -f /usr/share/dbus-1/system-services/com.blockscreen.Updater.service ] ||
    [ ! -f /etc/dbus-1/system.d/com.blockscreen.Updater.conf ] ||
    [ ! -x /usr/local/sbin/bs-apt-helper ]; }; then
    note "applying fix: install artifacts"
    mkdir -p "$BS_HOME/.config/blockscreen"
    touch "$BS_HOME/.config/blockscreen/.run-install-updater"
    # Created as root under sudo, and a root-owned config dir is a fault the UI cannot recover from.
    $IS_ROOT && [ "$BS_USER" != root ] &&
        chown -R "$BS_USER" "$BS_HOME/.config/blockscreen" 2>/dev/null
    note "armed the deploy trigger, install-updater.sh runs via the path unit, re-run to verify"
fi

# A group-writable setgid logs dir is what lets both the UI user and root append to the same files.
if $FIX && [ -d "$BS_PATH/logs" ] && [ "$(stat -c '%a' "$BS_PATH/logs" 2>/dev/null)" != 2775 ]; then
    note "applying fix: logs dir mode"
    chmod 2775 "$BS_PATH/logs" && note "logs dir set to 2775" || note "chmod failed on $BS_PATH/logs"
fi

# moonraker.asvc is a case-sensitive allowlist, so a missing entry silently breaks every update restart.
if $FIX && ! asvc_has BlocksScreen; then
    note "applying fix: moonraker.asvc"
    printf 'BlocksScreen\n' >>"$BS_HOME/printer_data/moonraker.asvc"
    $IS_ROOT && [ "$BS_USER" != root ] &&
        chown "$BS_USER" "$BS_HOME/printer_data/moonraker.asvc" 2>/dev/null
    note "added BlocksScreen to moonraker.asvc, restart moonraker to load it"
fi

# BlocksScreen-start.sh sources this env file, so a missing BS_DIR or BSENV starts the UI against the wrong tree.
if $FIX; then
    ENVF="$BS_HOME/.config/blockscreen/env"
    if [ ! -f "$ENVF" ] || ! grep -q '^BS_DIR=' "$ENVF" || ! grep -q '^BSENV=' "$ENVF"; then
        note "applying fix: env file"
        mkdir -p "$BS_HOME/.config/blockscreen"
        grep -q '^BS_DIR=' "$ENVF" 2>/dev/null || printf 'BS_DIR=%s\n' "$BS_PATH" >>"$ENVF"
        grep -q '^BSENV=' "$ENVF" 2>/dev/null || printf 'BSENV=%s\n' "$BSENV" >>"$ENVF"
        $IS_ROOT && [ "$BS_USER" != root ] &&
            chown -R "$BS_USER" "$BS_HOME/.config/blockscreen" 2>/dev/null
        note "wrote $ENVF, re-run to verify"
    fi
fi

# One retained boot makes every crash older than the last reboot uncorrelatable, which is most of them.
if $FIX && $IS_ROOT && [ "$(journalctl --list-boots 2>/dev/null | wc -l)" -lt 4 ]; then
    note "applying fix: journal retention"
    mkdir -p /etc/systemd/journald.conf.d /var/log/journal
    printf '[Journal]\nStorage=persistent\nSystemMaxUse=200M\nSystemMaxFiles=20\n' \
        >/etc/systemd/journald.conf.d/10-blocksscreen.conf
    systemd-tmpfiles --create --prefix /var/log/journal >/dev/null 2>&1
    systemctl restart systemd-journald 2>/dev/null ||
        note "journald restart failed, retention applies at the next boot"
    note "journal set to persistent 200M, older boots accumulate from here"
fi

# restart-ms 0 leaves a bus-off CAN link dead until someone reboots, and the field has no SSH.
if $FIX && $IS_ROOT && [ -f /etc/network/interfaces.d/can0 ] &&
    ! grep -q 'restart-ms' /etc/network/interfaces.d/can0; then
    note "applying fix: can0 restart-ms"
    cp /etc/network/interfaces.d/can0 "/etc/network/interfaces.d/can0.healthcheck.$(date +%Y%m%d%H%M%S).bak"
    # Native stanza first (ifupdown ignores options it does not know, so it can never abort ifup), then a
    # pre-up fallback for builds whose can method lacks it, with || true so a failure cannot strand can0 down.
    printf '    restart-ms 100\n    pre-up ip link set $IFACE type can restart-ms 100 || true\n' \
        >>/etc/network/interfaces.d/can0
    note "can0 will self-heal from bus-off after the next reboot, the running link keeps restart-ms=0"
fi

# --strict only moves the bar for the exit code: counters and rows keep the tier each check was recorded at.
RC=0
[ "$FAIL_N" -gt 0 ] && RC=1
$STRICT && [ "$WARN_N" -gt 0 ] && RC=1

if $JSON; then
    printf '{"host":"%s","pass":%d,"warn":%d,"fail":%d,"skip":%d,"strict":%s,"result":"%s","failed":"%s","warned":"%s","checks":[%s]}\n' \
        "$(hostname)" "$PASS_N" "$WARN_N" "$FAIL_N" "$SKIP_N" \
        "$($STRICT && echo true || echo false)" \
        "$([ "$RC" -eq 0 ] && echo PASS || echo FAIL)" \
        "$FAILED_NAMES" "$WARNED_NAMES" "$JSON_ROWS"
    exit "$RC"
fi

hdr "result"
say "$C_PASS$PASS_N passed$C_OFF, $C_WARN$WARN_N warned$C_OFF, $C_FAIL$FAIL_N failed$C_OFF, $C_SKIP$SKIP_N skipped$C_OFF"
[ "$WARN_N" -gt 0 ] && say "${C_WARN}WARNINGS:$C_OFF $WARNED_NAMES"
if [ "$RC" -eq 0 ]; then
    $QUIET && echo "$(hostname): PASS ($PASS_N checks, $WARN_N warn)" || echo "${C_PASS}ALL PASS$C_OFF"
    exit 0
fi
if [ "$FAIL_N" -eq 0 ]; then
    $QUIET && echo "$(hostname): FAIL (strict, $WARN_N warn) $WARNED_NAMES" ||
        echo "${C_WARN}STRICT: $WARN_N WARNING(S):$C_OFF $WARNED_NAMES"
    exit 1
fi
$QUIET && echo "$(hostname): FAIL ($FAIL_N) $FAILED_NAMES" ||
    echo "${C_FAIL}$FAIL_N CHECK(S) FAILED:$C_OFF $FAILED_NAMES"
exit 1
