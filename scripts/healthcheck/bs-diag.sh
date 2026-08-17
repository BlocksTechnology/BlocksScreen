#!/usr/bin/env bash
# Single entry point for the BlocksScreen field diagnostics: runs bs-healthcheck, bs-usb-diag and bs-power.
#
# The field has no SSH, so an operator gets one command and one transcript. Everything reachable from
# the default path is read-only: nothing here restarts a service, writes printer config, holds a lock
# or sends gcode. The mutating and load-testing modes (--fix, --stress, --burn, --bed) are reachable
# only by naming the tool explicitly, never from `all`.
#
# Usage:
#   bs-diag.sh                     same as `all`: health, then USB forensics, then power
#   bs-diag.sh all [-q|--json]     read-only sweep across every tool
#   bs-diag.sh health [OPTS...]    acceptance suite            (bs-healthcheck.sh, OPTS passed through)
#   bs-diag.sh fix [--force]       apply the known-safe remediations, refused mid-print without --force
#   bs-diag.sh usb [OPTS...]       USB fault forensics         (bs-usb-diag.sh,   OPTS passed through)
#   bs-diag.sh power [OPTS...]     Pi power budget and rails   (bs-power.sh,      OPTS passed through)
#   bs-diag.sh selftest [OPTS...]  UI functional selftest      (bs-selftest.py,   OPTS passed through)
#   bs-diag.sh list                show the tools, whether each is present, and its own help
#
# `health` already chains `usb --check` and `selftest` internally, so `all` adds the full USB
# forensic report and the power audit on top of it rather than repeating them. `fix` is the only
# mutating path here and it is never reachable from `all`.
set -u

HERE=$(dirname -- "$(readlink -f -- "$0")")
HEALTH="$HERE/bs-healthcheck.sh"
USBDIAG="$HERE/bs-usb-diag.sh"
POWER="$HERE/bs-power.sh"
SELFTEST="$HERE/bs-selftest.py"

if [ -t 1 ]; then
    C_HDR=$'\033[1;36m' C_BAD=$'\033[31m' C_OFF=$'\033[0m'
else
    C_HDR='' C_BAD='' C_OFF=''
fi

usage() { sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'; }

# A missing tool has to be loud: a silent skip reads as a pass and trains the operator to ignore output.
run_tool() {
    local label="$1" tool="$2"
    shift 2
    [ -f "$tool" ] || {
        printf '%sMISSING%s %s not found beside %s\n' "$C_BAD" "$C_OFF" "$(basename -- "$tool")" "$(basename -- "$0")" >&2
        return 127
    }
    printf '\n%s===== %s =====%s\n' "$C_HDR" "$label" "$C_OFF"
    case "$tool" in
        *.py) "${PYTHON:-python3}" "$tool" "$@" ;;
        *) bash "$tool" "$@" ;;
    esac
}

CMD="${1:-all}"
[ $# -gt 0 ] && shift

case "$CMD" in
    -h | --help | help)
        usage
        exit 0
        ;;
    health)
        run_tool "health: acceptance suite" "$HEALTH" "$@"
        exit $?
        ;;
    fix)
        run_tool "fix: known-safe remediations" "$HEALTH" --fix "$@"
        exit $?
        ;;
    usb)
        run_tool "usb: fault forensics" "$USBDIAG" "$@"
        exit $?
        ;;
    power)
        run_tool "power: rails and budget" "$POWER" "$@"
        exit $?
        ;;
    selftest)
        run_tool "selftest: ui" "$SELFTEST" "$@"
        exit $?
        ;;
    list)
        for t in "$HEALTH" "$USBDIAG" "$POWER" "$SELFTEST"; do
            if [ -f "$t" ]; then
                printf 'present  %s\n' "$t"
            else
                printf '%sMISSING  %s%s\n' "$C_BAD" "$t" "$C_OFF"
            fi
        done
        exit 0
        ;;
    all) ;;
    *)
        echo "unknown command: $CMD" >&2
        usage >&2
        exit 2
        ;;
esac

# `all` forwards only the presentation flags, so no mutating or load-testing mode can be reached from it.
HFLAGS=""
for a in "$@"; do
    case "$a" in
        -q | --json | -v | --deep | --strict) HFLAGS="$HFLAGS $a" ;;
        *)
            echo "'all' accepts only -q, --json, -v, --deep, --strict: use 'bs-diag.sh health $a' to pass it through" >&2
            exit 2
            ;;
    esac
done

RC=0
bump() { [ "$1" -gt "$RC" ] && RC="$1"; return 0; }

# shellcheck disable=SC2086
run_tool "health: acceptance suite" "$HEALTH" $HFLAGS
bump $?
run_tool "usb: fault forensics" "$USBDIAG"
bump $?
run_tool "power: rails and budget" "$POWER"
bump $?

printf '\n%s===== bs-diag done, worst exit %d =====%s\n' "$C_HDR" "$RC" "$C_OFF"
exit "$RC"
