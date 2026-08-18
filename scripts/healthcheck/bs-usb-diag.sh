#!/usr/bin/env bash
# USB fault forensics for boxes where inserting a flash drive shuts klipper down.
#
# The failure this exists to explain: a USB 3.0+ stick makes klipper report "Lost communication with MCU" or "Timer too close", and there are four physically distinct causes needing different fixes, so guessing is expensive:
#
#   1. power    the stick's inrush trips the port current limit, the hub cuts VBUS for the whole
#               port group, and the MCU browns out with it            -> dmesg "over-current change"
#   2. bus      a broken UAS bridge makes the xhci controller reset the link, which bounces sibling
#               ports including the MCU's                             -> "uas_eh_device_reset_handler"
#   3. enum     link training fails and retries in a loop, holding the controller and stalling the
#               MCU's serial transfers past klipper's deadline        -> "error -71", "error -110"
#   4. load     mounting exfat/ntfs through FUSE spikes host cpu and the MCU misses its window
#                                                                     -> klipper "Timer too close"
#
# Read-only in every mode. Never mounts, never sends gcode, never restarts a service.
#
# Usage:
#   bs-usb-diag.sh                 forensic report on the current box + correlated history
#   bs-usb-diag.sh --watch [SECS]  live capture while the operator inserts the suspect drive
#   bs-usb-diag.sh --monitor [SECS] same capture, passive: safe during a print, plug nothing
#   bs-usb-diag.sh --check         TSV assertions for bs-healthcheck.sh
#   bs-usb-diag.sh --history       only the historic MCU-shutdown vs USB-event correlation

set -u

MODE=report
WATCH_SECS=180
FORCE=false
MONITOR=false
QUIET=false
NO_REPORT=false

while [ $# -gt 0 ]; do
    case "$1" in
        --watch)
            MODE=watch
            case "${2:-}" in '' | -*) ;; *)
                WATCH_SECS=$2
                shift
                ;;
            esac
            ;;
        --monitor)
            MODE=watch
            MONITOR=true
            case "${2:-}" in '' | -*) ;; *)
                WATCH_SECS=$2
                shift
                ;;
            esac
            ;;
        --check) MODE=check ;;
        --history) MODE=history ;;
        --force) FORCE=true ;;
        -q | --quiet) QUIET=true ;;
        --no-report) NO_REPORT=true ;;
        -h | --help)
            sed -n '2,25p' "$0"
            exit 0
            ;;
        *)
            echo "unknown option: $1" >&2
            exit 2
            ;;
    esac
    shift
done
case "${WATCH_SECS:-x}" in '' | *[!0-9]*) WATCH_SECS=180 ;; esac

BS_USER="${SUDO_USER:-$(id -un)}"
# Walk up to the repo root instead of counting directories, so this script survives being moved.
BS_PATH=$(dirname -- "$(readlink -f -- "$0")")
while [ "$BS_PATH" != / ] && [ ! -d "$BS_PATH/BlocksScreen" ]; do
    BS_PATH=$(dirname -- "$BS_PATH")
done
[ -d "$BS_PATH/BlocksScreen" ] || BS_PATH=$(dirname -- "$(dirname -- "$(readlink -f -- "$0")")")
if [ "$BS_USER" = root ] && [ -d "$BS_PATH/BlocksScreen" ]; then
    BS_USER=$(stat -c '%U' "$BS_PATH" 2>/dev/null || echo root)
fi
BS_HOME=$(getent passwd "$BS_USER" | cut -d: -f6)
[ -n "$BS_HOME" ] || BS_HOME="$HOME"
LOGDIR="$BS_HOME/printer_data/logs"
CFGDIR="$BS_HOME/printer_data/config"
MOON="http://localhost:7125"
IS_ROOT=false
[ "$(id -u)" = "0" ] && IS_ROOT=true

# The field has no SSH, so the report has to land where moonraker already serves logs to the UI.
REPORT=""
if [ "$MODE" != check ] && ! $NO_REPORT && [ -d "$LOGDIR" ]; then
    REPORT="$LOGDIR/bs-usb-diag-$(date +%Y%m%d-%H%M%S).log"
    : >"$REPORT" 2>/dev/null || REPORT=""
    [ -n "$REPORT" ] && $IS_ROOT && [ "$BS_USER" != root ] && chown "$BS_USER" "$REPORT" 2>/dev/null
fi

if [ -t 1 ] && [ "$MODE" != check ]; then
    C_HDR=$'\033[1;36m' C_OK=$'\033[32m' C_WARN=$'\033[33m' C_BAD=$'\033[31m' C_OFF=$'\033[0m'
else
    C_HDR="" C_OK="" C_WARN="" C_BAD="" C_OFF=""
fi

out() {
    $QUIET || printf '%s\n' "$*"
    [ -n "$REPORT" ] && printf '%s\n' "$*" >>"$REPORT"
    return 0
}
hdr() { out ""; out "${C_HDR}== $* ==${C_OFF}"; }
ok() { out "  ${C_OK}ok${C_OFF}   $*"; }
bad() { out "  ${C_BAD}BAD${C_OFF}  $*"; }
susp() { out "  ${C_WARN}????${C_OFF} $*"; }
kv() { out "$(printf '  %-28s %s' "$1" "$2")"; }

# --check speaks TSV so the healthcheck can record each row at its own tier.
emit() { printf '%s\t%s\t%s\n' "$1" "$2" "${3:-}"; }

# ---------------------------------------------------------------- sysfs helpers

# Every USB device node, one "syspath" per line, interfaces excluded.
usb_devs() {
    local d
    for d in /sys/bus/usb/devices/*; do
        [ -f "$d/idVendor" ] || continue
        echo "$d"
    done
}

sysread() { cat "$1" 2>/dev/null | head -1 | tr -d '\0'; }

# The interface drivers bound under one device, space separated ("uas", "usb-storage", "cdc_acm").
dev_drivers() {
    local i out=""
    for i in "$1":*; do
        [ -L "$i/driver" ] || continue
        out="$out $(basename "$(readlink -f "$i/driver")")"
    done
    echo "${out# }"
}

dev_label() {
    local v p m pr
    v=$(sysread "$1/idVendor")
    p=$(sysread "$1/idProduct")
    m=$(sysread "$1/manufacturer")
    pr=$(sysread "$1/product")
    echo "$v:$p ${m:-?} ${pr:-?}"
}

# 5000 and 10000 are SuperSpeed: the speeds that carry the inrush and the RF noise.
dev_is_ss() {
    case "$(sysread "$1/speed")" in 5000 | 10000 | 20000) return 0 ;; esac
    return 1
}

# Root hub a device hangs off, which is the blast radius of a controller-level reset.
dev_roothub() {
    local b
    b=$(basename "$1")
    echo "usb${b%%-*}"
}

# The tty's USB device node: /sys/class/tty/ttyACM0/device is the interface, its parent is the device.
tty_usbdev() {
    local p
    p=$(readlink -f "/sys/class/tty/$(basename "$1")/device" 2>/dev/null) || return 1
    while [ -n "$p" ] && [ "$p" != / ]; do
        [ -f "$p/idVendor" ] && {
            echo "$p"
            return 0
        }
        p=$(dirname "$p")
    done
    return 1
}

# The config files klipper actually loads, so backups and other-variant cfgs stay out.
active_cfgs() {
    local root inc g
    root="$CFGDIR/printer.cfg"
    [ -f "$root" ] || return 0
    echo "$root"
    awk '/^\[include /{sub(/^\[include[ \t]+/, ""); sub(/\].*$/, ""); sub(/[ \t]+$/, ""); print}' "$root" |
        while read -r inc; do
            case "$inc" in
                *'*'*) for g in "$CFGDIR"/$inc; do [ -f "$g" ] && echo "$g"; done ;;
                *) [ -f "$CFGDIR/$inc" ] && echo "$CFGDIR/$inc" ;;
            esac
        done
}

# Serial paths klipper is configured to open, as written (by-id, by-path or a bare node).
mcu_serials() {
    local files
    files=$(active_cfgs)
    [ -n "$files" ] || return 0
    # Strip the inline comment too: klipper takes # and ; as inline prefixes, and the stock printer.cfg ships one on the serial: line itself.
    grep -hE '^[[:space:]]*serial:' $files 2>/dev/null |
        sed 's/^[[:space:]]*serial:[[:space:]]*//; s/[[:space:]]*[#;].*$//; s/[[:space:]]*$//' |
        grep '^/dev/' | sort -u
}

# ------------------------------------------------------------- journal / klippy

JOURNAL_OK=""
journal_readable() {
    [ -n "$JOURNAL_OK" ] || {
        if [ -n "$(journalctl -k -n 1 --no-pager 2>/dev/null)" ]; then JOURNAL_OK=yes; else JOURNAL_OK=no; fi
    }
    [ "$JOURNAL_OK" = yes ]
}

# The four mechanisms, as they actually appear in the kernel ring buffer.
USB_PAT='over-current|overcurrent|Cannot enable|not enough power|insufficient available bus power'
USB_PAT="$USB_PAT|uas_eh_|reset (SuperSpeed|high-speed|full-speed|low-speed)|xhci_hcd.*(Error|halt|dying|WARN|Timeout)"
USB_PAT="$USB_PAT|device descriptor read|unable to enumerate|error -71|error -110|error -32|device not accepting address"
USB_PAT="$USB_PAT|USB disconnect|usb_serial_generic_read_bulk_callback|disconnected from ttyUSB|disconnected from ttyACM"
USB_PAT="$USB_PAT|Under-voltage|Voltage normalised|hwmon.*critical"
# Re-enumeration lines aren't faults, but a disconnect without a matching "new ... USB device" is a dead port, while one every few seconds is a reset loop: the operator needs both.
USB_PAT="$USB_PAT|new (SuperSpeed|high-speed|full-speed|low-speed)[^ ]* USB device"

kernel_usb_events() { journalctl -k -o short-unix --no-pager "$@" 2>/dev/null | grep -aE "$USB_PAT"; }

# klippy.log rotations, newest last so the correlator sees history in order.
klippy_logs() {
    local f
    for f in "$LOGDIR"/klippy.log.[0-9]* "$LOGDIR"/klippy.log; do
        [ -f "$f" ] && echo "$f"
    done
}

# Correlate every klipper shutdown against kernel USB activity in the same seconds: klippy.log has no per-line clock, but every "Start printer" / "Stats <monotonic>:" line shares one monotonic base, so a shutdown can be placed on the wall clock within one stats interval (1s) and lined up against journal timestamps.
correlate() {
    local window="${1:-25}"
    command -v python3 >/dev/null 2>&1 || {
        echo "python3 missing, correlation unavailable"
        return 2
    }
    journal_readable || {
        echo "kernel journal unreadable, correlation unavailable"
        return 2
    }
    kernel_usb_events --since "-45 days" >/tmp/.bs-usb-events.$$ 2>/dev/null
    klippy_logs >/tmp/.bs-usb-logs.$$
    # Klippy logs outlive the journal by months, so a shutdown older than the journal's first entry has no USB data at all, which must not read the same as data that shows nothing.
    local floor
    floor=$(journalctl -k -o short-unix --no-pager --since "-45 days" 2>/dev/null | head -1 | cut -d' ' -f1)
    python3 - "$window" /tmp/.bs-usb-events.$$ /tmp/.bs-usb-logs.$$ "${floor:-0}" <<'PYEOF'
import re
import sys

window = float(sys.argv[1])
try:
    floor = float(sys.argv[4])
except (IndexError, ValueError):
    floor = 0.0
events = []
with open(sys.argv[2], errors="replace") as fh:
    for line in fh:
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        try:
            events.append((float(parts[0]), parts[1].rstrip()))
        except ValueError:
            continue
events.sort()

SHUT = re.compile(
    r"Lost communication with MCU|Timer too close|Rescheduled timer in the past"
    r"|Unable to open serial port|Unable to connect|shutdown: |Transition to shutdown state"
    r"|mcu_protocol_error|Move queue overflow|Attempt to update TRSYNC|communication error"
)
START = re.compile(r"Start printer at .*\(([0-9.]+) ([0-9.]+)\)")
STATS = re.compile(r"^Stats ([0-9.]+):")
LOAD = re.compile(r"sysload=([0-9.]+)")
AWAKE = re.compile(r"mcu_awake=([0-9.]+)")
RETR = re.compile(r"bytes_retransmit=([0-9]+)")
INVAL = re.compile(r"bytes_invalid=([0-9]+)")

hits = []
with open(sys.argv[3]) as fh:
    logs = [x.strip() for x in fh if x.strip()]

for path in logs:
    base_epoch = base_mono = None
    now_mono = None
    last_stats = ""
    try:
        src = open(path, errors="replace")
    except OSError:
        continue
    with src:
        for line in src:
            m = START.search(line)
            if m:
                base_epoch, base_mono = float(m.group(1)), float(m.group(2))
                now_mono = base_mono
                continue
            m = STATS.match(line)
            if m:
                now_mono = float(m.group(1))
                last_stats = line.rstrip()
                continue
            # Klipper prints its own source into tracebacks, so self._error("Unable to connect") lands in the log looking like a real event; real messages start at column 0, traceback/source lines are indented.
            if line[:1].isspace() or line.startswith(("File \"", "Traceback")):
                continue
            if not SHUT.search(line):
                continue
            when = None
            if base_epoch is not None and now_mono is not None:
                when = base_epoch + (now_mono - base_mono)
            hits.append((when, path, line.strip()[:160], last_stats))

if not hits:
    print("no klipper shutdown events found in %d log file(s)" % len(logs))
    sys.exit(0)

# One shutdown cascades into a dozen lines, so collapse anything inside the same window; a rotated log that begins mid-session carries no epoch anchor, so those collapse by message instead.
merged = []
seen_untimed = set()
for when, path, text, stats in hits:
    if when is None:
        key = (path, text[:60])
        if key in seen_untimed:
            continue
        seen_untimed.add(key)
    elif merged and merged[-1][0] is not None and when - merged[-1][0] < window:
        continue
    merged.append((when, path, text, stats))

if floor:
    print("kernel journal covers %s onward, anything older cannot be correlated" % __import__(
        "time").strftime("%Y-%m-%d %H:%M:%S", __import__("time").localtime(floor)))

verdicts = []
for when, path, text, stats in merged:
    print("")
    stamp = "time unknown, log starts mid-session" if when is None else __import__("time").strftime(
        "%Y-%m-%d %H:%M:%S", __import__("time").localtime(when)
    )
    print("SHUTDOWN %s  (%s)" % (stamp, path.rsplit("/", 1)[-1]))
    print("  klipper: %s" % text)
    near = []
    if when is not None:
        near = [(t, msg) for t, msg in events if abs(t - when) <= window]
    nodata = when is None or (floor and when < floor - window)
    if near:
        for t, msg in near[:14]:
            print("  usb %+6.1fs %s" % (t - when, msg[:150]))
    elif when is None:
        print("  usb        (rotated log has no timestamp anchor, cannot correlate)")
    elif nodata:
        print("  usb        (predates the kernel journal, no data)")
    else:
        print("  usb        (no kernel USB activity within +/-%ds)" % window)

    blob = " ".join(m for _, m in near)
    cause = []
    if re.search(r"over-current|overcurrent|Cannot enable|not enough power", blob):
        cause.append("POWER: the port current limit tripped and VBUS was cut for the whole port group")
    if re.search(r"uas_eh_|reset SuperSpeed", blob):
        cause.append("BUS: a UAS/xhci device reset bounced the link the MCU shares")
    if re.search(r"error -71|error -110|error -32|device descriptor read|unable to enumerate|not accepting address", blob):
        cause.append("ENUM: link training failed and retried, stalling the controller")
    if re.search(r"Under-voltage", blob):
        cause.append("POWER: the SoC itself browned out (PSU cannot carry the stick's inrush)")
    if re.search(r"USB disconnect|disconnected from tty", blob):
        cause.append("LINK: the MCU's own serial device disconnected")
    if "Timer too close" in text and not near:
        sl = LOAD.search(stats)
        cause.append(
            "LOAD: host overload with no USB fault logged (sysload=%s at the last stats line)"
            % (sl.group(1) if sl else "?")
        )
    if re.search(r"Emergency|M112|Button Pressed|emergency stop", text):
        cause = ["OPERATOR: emergency stop, not a fault"]
    if not cause:
        if when is None:
            cause.append("NO DATA: rotated log has no timestamp anchor, correlation impossible")
        elif nodata:
            cause.append("NO DATA: predates the kernel journal, USB state then is unknowable")
        else:
            cause.append("UNKNOWN: no USB or load signature, look at wiring/EMI")
    for c in cause:
        print("  cause -> %s" % c)
    verdicts.extend(cause)
    for label, rx in (("sysload", LOAD), ("mcu_awake", AWAKE), ("retransmit", RETR), ("invalid", INVAL)):
        m = rx.search(stats)
        if m:
            print("  stats  %-10s %s" % (label, m.group(1)))

print("")
print("%d distinct shutdown event(s)" % len(merged))
kinds = sorted({c.split(":")[0] for c in verdicts})
print("dominant class(es): %s" % ", ".join(kinds))
PYEOF
    local rc=$?
    rm -f /tmp/.bs-usb-events.$$ /tmp/.bs-usb-logs.$$
    return $rc
}

# ------------------------------------------------------------------- assertions
# Each returns 0/1 and prints the detail, so both the report and --check share one implementation.

MCU_DEVS=""
MCU_HUBS=""
resolve_mcus() {
    local s node dev
    MCU_DEVS="" MCU_HUBS=""
    for s in $(mcu_serials); do
        node=$(readlink -f "$s" 2>/dev/null) || continue
        [ -e "$node" ] || continue
        case "$node" in /dev/tty*) ;; *) continue ;; esac
        dev=$(tty_usbdev "$node") || continue
        MCU_DEVS="$MCU_DEVS $dev"
        MCU_HUBS="$MCU_HUBS $(dev_roothub "$dev")"
    done
    MCU_DEVS="${MCU_DEVS# }"
    MCU_HUBS="$(echo "$MCU_HUBS" | tr ' ' '\n' | sort -u | tr '\n' ' ')"
}

# A bare /dev/ttyUSB0 is assigned in enumeration order, so inserting storage can hand klipper the wrong device on next boot; by-id and by-path survive it.
a_serial_pinned() {
    local s loose=""
    for s in $(mcu_serials); do
        case "$s" in /dev/serial/by-id/* | /dev/serial/by-path/*) ;; *) loose="$loose $s" ;; esac
    done
    [ -z "$loose" ] || {
        echo "serial pinned by bare device node:$loose (enumeration order moves it when storage appears)"
        return 1
    }
}

# Returns 2, not 0, when no port exposes the counter: a Pi 5 can log 58 over-current trips with over_current_count still reading 0, so a green tick here would prove nothing on the worst boxes.
a_no_overcurrent_counters() {
    local f n hits="" seen=0
    for f in /sys/bus/usb/devices/*-port*/over_current_count; do
        [ -f "$f" ] || continue
        n=$(sysread "$f")
        case "${n:-x}" in '' | *[!0-9]*) continue ;; esac
        seen=1
        [ "$n" -gt 0 ] && hits="$hits $(basename "$(dirname "$f")")=$n"
    done
    [ -z "$hits" ] || {
        echo "ports have latched over-current events:$hits (a stick tripped the limit and VBUS was cut)"
        return 1
    }
    [ "$seen" = 1 ] || {
        echo "no port exposes over_current_count on this kernel, see the kernel-log check instead"
        return 2
    }
}

a_no_overcurrent_journal() {
    local hits
    journal_readable || return 0
    hits=$(journalctl -k -b --no-pager 2>/dev/null | grep -aiE 'over-current|overcurrent|Cannot enable.*USB cable' | tail -4)
    [ -z "$hits" ] || {
        echo "$hits"
        return 1
    }
}

a_no_uas_resets() {
    local hits
    journal_readable || return 0
    hits=$(journalctl -k -b --no-pager 2>/dev/null | grep -aE 'uas_eh_|reset SuperSpeed' | tail -4)
    [ -z "$hits" ] || {
        echo "$hits"
        return 1
    }
}

a_no_enum_errors() {
    local hits
    journal_readable || return 0
    hits=$(journalctl -k -b --no-pager 2>/dev/null |
        grep -aE 'error -71|error -110|device descriptor read|unable to enumerate|not accepting address' | tail -4)
    [ -z "$hits" ] || {
        echo "$hits"
        return 1
    }
}

# "disconnected from ttyACM" is usbserial-driver wording, so a cdc_acm board (Beacon, most native-USB MCUs) can drop off the bus all boot without matching it: match its own bus address too.
a_no_mcu_disconnect() {
    local hits pat d esc
    journal_readable || return 0
    pat='disconnected from ttyUSB|disconnected from ttyACM|usb_serial_generic_read_bulk_callback'
    resolve_mcus
    for d in $MCU_DEVS; do
        esc=$(printf '%s' "$d" | sed 's/\./\\./g')
        pat="$pat|usb $esc: USB disconnect|cdc_acm $esc:[^ ]*: device disconnected"
    done
    hits=$(journalctl -k -b --no-pager 2>/dev/null | grep -aE "$pat" | tail -4)
    [ -z "$hits" ] || {
        echo "$hits"
        return 1
    }
}

# usbcore autosuspends idle ports, and a resumed port renegotiates while klipper is mid-transfer.
a_mcu_autosuspend_off() {
    local d ctrl bad=""
    resolve_mcus
    [ -n "$MCU_DEVS" ] || return 0
    for d in $MCU_DEVS; do
        ctrl=$(sysread "$d/power/control")
        [ "$ctrl" = auto ] && bad="$bad $(basename "$d")"
    done
    [ -z "$bad" ] || {
        echo "MCU port(s)$bad set to power/control=auto (a resume renegotiates mid-print)"
        return 1
    }
}

# On a Pi4/CM4 every A port is behind one xhci controller, so this is advisory, not a defect.
a_mcu_not_sharing_ss_hub() {
    local d shared=""
    resolve_mcus
    [ -n "$MCU_DEVS" ] || return 0
    for d in $(usb_devs); do
        case " $MCU_DEVS " in *" $d "*) continue ;; esac
        dev_is_ss "$d" || continue
        case "$MCU_HUBS" in *"$(dev_roothub "$d")"*) shared="$shared $(basename "$d")($(dev_label "$d"))" ;; esac
    done
    [ -z "$shared" ] || {
        echo "SuperSpeed device(s) on the MCU's controller:$shared (a controller reset takes the MCU with it)"
        return 1
    }
}

# UAS is the single most common source of xhci resets on Pi-class hosts.
a_no_uas_bound() {
    local d drv hits=""
    for d in $(usb_devs); do
        drv=$(dev_drivers "$d")
        case "$drv" in *uas*) hits="$hits $(basename "$d")($(dev_label "$d"))" ;; esac
    done
    [ -z "$hits" ] || {
        echo "bound to the uas driver:$hits -- pin usb-storage.quirks=VID:PID:u in cmdline.txt to force BOT"
        return 1
    }
}

# ntfs-3g and exfat-fuse cost several times more host cpu than the in-kernel drivers, and klipper's deadline is measured in milliseconds.
a_no_fuse_storage() {
    local hits
    hits=$(awk '$3 ~ /fuse/ && $1 ~ /^\/dev\// {print $1" ("$3" on "$2")"}' /proc/mounts 2>/dev/null)
    [ -z "$hits" ] || {
        echo "$hits mounted through FUSE (userspace filesystem, spikes cpu during transfers)"
        return 1
    }
}

# a_no_fuse_storage only fires once a bad stick is already mounted (after the print died); this fires before one ever is, since no in-kernel driver means every customer stick takes FUSE.
a_exfat_in_kernel() {
    local missing=""
    grep -qw exfat /proc/filesystems 2>/dev/null || modinfo exfat >/dev/null 2>&1 || missing="exfat"
    grep -qw ntfs3 /proc/filesystems 2>/dev/null || modinfo ntfs3 >/dev/null 2>&1 || missing="$missing ntfs3"
    [ -z "${missing// /}" ] || {
        echo "no in-kernel driver for:$missing (Windows formats sticks over 32GB as exfat, so they land on FUSE)"
        return 1
    }
}

# Raising the Pi's own budget hides an oversubscribed hub, it doesn't fix it: the hub still has one upstream lead, and a bus-powered one may only draw 500mA through it regardless of its children.
a_hub_not_oversubscribed() {
    local h c n sum name hits=""
    for h in /sys/bus/usb/devices/*/; do
        name=$(basename "$h")
        # Root hubs are fed by the board, not by an upstream port, so their subtree total means nothing.
        case "$name" in usb*) continue ;; esac
        [ "$(sysread "$h/bDeviceClass")" = 09 ] || continue
        sum=0
        for c in "$h"*/bMaxPower; do
            [ -f "$c" ] || continue
            n=$(sysread "$c" | tr -dc '0-9')
            [ -n "$n" ] || n=0
            sum=$((sum + n))
        done
        [ "$sum" -gt 500 ] && hits="$hits $name=${sum}mA"
    done
    [ -z "${hits// /}" ] || {
        echo "hub subtree draw exceeds the 500mA a bus-powered hub may take upstream:$hits (fit a self-powered hub)"
        return 1
    }
}

# Live firmware says what booted, config.txt says what boots next, and they diverge exactly when the box is at risk: a line added but never rebooted, or a reflash that silently dropped it again.
a_usb_current_budget() {
    local model cfg f live=x persisted=0
    model=$(sysread /proc/device-tree/model)
    case "$model" in *"Raspberry Pi 5"*) ;; *)
        echo "not a Pi 5, usb_max_current_enable does not exist on this board"
        return 2
        ;;
    esac
    if command -v vcgencmd >/dev/null 2>&1; then
        cfg=$(vcgencmd get_config usb_max_current_enable 2>/dev/null | cut -d= -f2)
        case "${cfg:-x}" in 0 | 1) live=$cfg ;; esac
    fi
    for f in /boot/firmware/config.txt /boot/config.txt; do
        [ -r "$f" ] || continue
        grep -qE '^[[:space:]]*usb_max_current_enable[[:space:]]*=[[:space:]]*1' "$f" && persisted=1
        break
    done
    if [ "$live" = x ]; then
        [ "$persisted" = 1 ] || {
            echo "firmware unreadable and no usb_max_current_enable=1 in config.txt: ports may be capped at 600mA"
            return 1
        }
        echo "vcgencmd unavailable: config.txt carries the line but the running budget was not verified"
        return 2
    fi
    [ "$live" = 1 ] || {
        [ "$persisted" = 1 ] &&
            echo "usb_max_current_enable=1 is in config.txt but has not been applied: reboot to raise the budget"
        echo "Pi 5 running with usb_max_current_enable unset: ports are capped at 600mA total, below one USB3 stick's inrush"
        return 1
    }
    [ "$persisted" = 1 ] || {
        echo "budget is raised in the running firmware but config.txt does not carry it: the next reboot drops back to 600mA"
        return 1
    }
}

# Klipper's 'mcu' rides CAN behind the gs_usb adapter, so an MCU loss with no USB disconnect lands here.
a_can_link_healthy() {
    local i ifs d st berr c v bad=""
    command -v ip >/dev/null 2>&1 || return 2
    ifs=$(ip -o link show type can 2>/dev/null | sed -n 's/^[0-9]\{1,\}: \([^:@ ]\{1,\}\).*/\1/p')
    [ -n "$ifs" ] || {
        echo "no CAN interface on this box"
        return 2
    }
    for i in $ifs; do
        d=$(ip -details link show "$i" 2>/dev/null)
        case "$d" in *"state UP"*) ;; *) bad="$bad $i:link-down" ;; esac
        st=$(printf '%s' "$d" | grep -oE 'state (ERROR-ACTIVE|ERROR-WARNING|ERROR-PASSIVE|BUS-OFF|STOPPED|SLEEPING)' | tail -1 | awk '{print $2}')
        case "${st:-ERROR-ACTIVE}" in ERROR-ACTIVE) ;; *) bad="$bad $i:$st" ;; esac
        berr=$(printf '%s' "$d" | grep -oE 'berr-counter tx [0-9]+ rx [0-9]+' | awk '{print $3 + $5}')
        [ "${berr:-0}" -gt 0 ] 2>/dev/null && bad="$bad $i:berr=$berr"
        for c in rx_errors tx_errors rx_dropped tx_dropped rx_over_errors; do
            v=$(sysread "/sys/class/net/$i/statistics/$c")
            [ "${v:-0}" -gt 0 ] 2>/dev/null && bad="$bad $i:$c=$v"
        done
    done
    [ -z "$bad" ] || {
        echo "CAN link degraded:$bad (tx_dropped is the txqueue overflowing, the classic 'Lost communication with MCU')"
        return 1
    }
}

# restart-ms 0 leaves a bus-off CAN link dead until someone reboots, and the field has no SSH.
a_can_recovery_sane() {
    local i ifs d rms qlen bad=""
    command -v ip >/dev/null 2>&1 || return 2
    ifs=$(ip -o link show type can 2>/dev/null | sed -n 's/^[0-9]\{1,\}: \([^:@ ]\{1,\}\).*/\1/p')
    [ -n "$ifs" ] || {
        echo "no CAN interface on this box"
        return 2
    }
    for i in $ifs; do
        d=$(ip -details link show "$i" 2>/dev/null)
        rms=$(printf '%s' "$d" | grep -oE 'restart-ms [0-9]+' | tail -1 | awk '{print $2}')
        [ "${rms:-0}" -gt 0 ] 2>/dev/null || bad="$bad $i:restart-ms=0"
        qlen=$(sysread "/sys/class/net/$i/tx_queue_len")
        [ "${qlen:-0}" -ge 128 ] 2>/dev/null || bad="$bad $i:txqueuelen=${qlen:-?}"
    done
    [ -z "$bad" ] || {
        echo "CAN recovery weak:$bad (bus-off self-heals only with restart-ms>0, txqueuelen<128 drops frames under load)"
        return 1
    }
}

# A silently read-only boot partition makes every config.txt fix a no-op while tee still prints success.
a_boot_config_writable() {
    local f mp opts fs
    command -v findmnt >/dev/null 2>&1 || return 2
    for f in /boot/firmware/config.txt /boot/config.txt; do
        [ -f "$f" ] && break
    done
    [ -f "$f" ] || {
        echo "no config.txt on this box"
        return 2
    }
    fs=$(findmnt -n -o FSTYPE -T "$f" 2>/dev/null)
    mp=$(findmnt -n -o TARGET -T "$f" 2>/dev/null)
    opts=$(findmnt -n -o OPTIONS -T "$f" 2>/dev/null)
    case ",$opts," in *,ro,*)
        echo "$mp is mounted read-only: config.txt writes fail while tee still echoes success"
        return 1
        ;;
    esac
    case "$fs" in vfat | msdos) ;; *)
        echo "$f is on $fs, not the vfat boot partition: firmware reads a different file than this one"
        return 1
        ;;
    esac
}

# The field has no SSH, so a journal that dies at reboot leaves a recurring fault permanently undiagnosable.
a_journal_persistent() {
    local boots
    journal_readable || return 2
    [ -d /var/log/journal ] || {
        echo "journal is volatile (no /var/log/journal): every reboot erases the only field evidence"
        return 1
    }
    boots=$(journalctl --list-boots --no-pager 2>/dev/null | grep -cE '^ *-?[0-9]+ +[0-9a-f]{32}')
    [ "${boots:-0}" -ge 2 ] || {
        echo "only ${boots:-0} boot retained: anything before the last reboot cannot be correlated"
        return 1
    }
}

# An SD or eMMC stall freezes userspace long enough for klipper to miss timers and drop the MCU.
a_no_storage_io_errors() {
    local hits
    journal_readable || return 2
    hits=$(journalctl -k -b --no-pager 2>/dev/null |
        grep -aE '(mmc[0-9]+|mmcblk[0-9]+|nvme[0-9]+n[0-9]+)[: ].*(error|timeout|timed out|reset|recovery failed)|EXT4-fs .*(error|remounting)' |
        tail -4)
    [ -z "$hits" ] || {
        echo "$hits"
        return 1
    }
}

# A bus-powered hub browning out drops its children with no kernel message, so the sibling cluster is the only trace.
a_no_hub_brownout() {
    local oc hit
    journal_readable || return 2
    oc=$(journalctl -k -b --no-pager 2>/dev/null | grep -acE 'over-?current')
    [ "${oc:-0}" = 0 ] || return 0
    hit=$(journalctl -k -b -o short-unix --no-pager 2>/dev/null |
        grep -aE 'usb [0-9]+-[0-9.]+: USB disconnect' | awk '
        {
            ts = $1 + 0
            dev = ""
            for (i = 1; i <= NF; i++) if ($i == "usb") { dev = $(i + 1); sub(/:$/, "", dev); break }
            if (dev == "") next
            n = split(dev, part, ".")
            if (n < 2) next
            hub = part[1]
            for (j = 2; j < n; j++) hub = hub "." part[j]
            k++; T[k] = ts; H[k] = hub; D[k] = dev
        }
        END {
            for (a = 1; a <= k; a++) {
                split("", seen, ":")
                seen[D[a]] = 1
                c = 1
                for (b = a + 1; b <= k; b++) {
                    if (T[b] - T[a] > 5) break
                    if (H[b] == H[a] && !(D[b] in seen)) { seen[D[b]] = 1; c++ }
                }
                if (c >= 2) { printf "hub %s lost %d children within 5s\n", H[a], c; exit }
            }
        }')
    [ -z "$hit" ] || {
        echo "$hit with no over-current logged: signature of a bus-powered hub browning out, not the Pi limiter"
        return 1
    }
}

a_no_correlated_shutdown() {
    local rpt hits
    rpt=$(correlate 25 2>/dev/null)
    case "$rpt" in
        *unavailable*) return 0 ;;
        *"no klipper shutdown events found"*) return 0 ;;
    esac
    # An operator E-stop and an unexplained stop are not USB faults: only a named mechanism counts,
    # otherwise every box that ever had its button pressed fails this assertion forever.
    hits=$(echo "$rpt" | grep -E 'cause -> (POWER|BUS|ENUM|LINK|LOAD)' | sort -u)
    [ -n "$hits" ] || return 0
    echo "$(echo "$rpt" | grep -c '^SHUTDOWN') shutdown(s) in the logs, USB/load-attributable:"
    echo "$hits" | head -8
    return 1
}

# ---------------------------------------------------------------------- report

r_host() {
    hdr "host and power"
    kv "model" "$(sysread /proc/device-tree/model || echo unknown)"
    kv "kernel" "$(uname -r)"
    kv "cmdline" "$(sysread /proc/cmdline | tr ' ' '\n' | grep -E 'usb|dwc' | tr '\n' ' ')"
    if command -v vcgencmd >/dev/null 2>&1; then
        local t
        t=$(vcgencmd get_throttled 2>/dev/null | cut -d= -f2)
        kv "throttled" "$t"
        case "${t:-x}" in '' | x | *[!0-9a-fA-Fx]*) ;; *)
            [ $((t & 0x1)) -ne 0 ] && bad "undervoltage RIGHT NOW: the PSU cannot carry the current load"
            [ $((t & 0x10000)) -ne 0 ] && susp "undervoltage happened earlier this boot (sticky bit)"
            ;;
        esac
        kv "usb_max_current_enable" "$(vcgencmd get_config usb_max_current_enable 2>/dev/null | cut -d= -f2)"
    fi
    local f n
    for f in /sys/bus/usb/devices/*-port*/over_current_count; do
        [ -f "$f" ] || continue
        n=$(sysread "$f")
        case "${n:-0}" in '' | 0 | *[!0-9]*) continue ;; esac
        bad "$(basename "$(dirname "$f")") over_current_count=$n"
    done
}

r_topology() {
    hdr "usb topology"
    resolve_mcus
    local d mark drv
    for d in $(usb_devs); do
        mark="  "
        case " $MCU_DEVS " in *" $d "*) mark="MCU" ;; esac
        dev_is_ss "$d" && [ "$mark" = "  " ] && mark="SS "
        drv=$(dev_drivers "$d")
        out "$(printf '  %s %-10s %-6s %-7s %-22s %s' \
            "$mark" "$(basename "$d")" "$(sysread "$d/speed")" \
            "$(sysread "$d/bMaxPower")" "${drv:--}" "$(dev_label "$d")")"
    done
    out ""
    kv "MCU serial(s)" "$(mcu_serials | tr '\n' ' ')"
    kv "MCU root hub(s)" "${MCU_HUBS:-none resolved}"
}

r_checks() {
    hdr "risk factors"
    local name fn tier detail rc
    # Same tiers as do_check: an operator who cannot tell a blocker from an advisory learns to skim
    # past both, so a FAIL prints BAD and only a WARN prints ????.
    while IFS='|' read -r fn tier name; do
        [ -n "$fn" ] || continue
        detail=$("$fn" 2>&1)
        rc=$?
        case "$rc" in
            0) ok "$name" && continue ;;
            2) susp "$name (not measurable here)" ;;
            *) case "$tier" in FAIL) bad "$name" ;; *) susp "$name" ;; esac ;;
        esac
        [ -n "$detail" ] && out "$(echo "$detail" | sed 's/^/         /')"
    done <<'ROWS'
a_serial_pinned|WARN|MCU serial pinned by stable path
a_no_overcurrent_counters|FAIL|no latched port over-current counters
a_no_overcurrent_journal|FAIL|no over-current in this boot's kernel log
a_no_uas_resets|WARN|no UAS/xhci device resets this boot
a_no_enum_errors|WARN|no USB enumeration errors this boot
a_no_mcu_disconnect|FAIL|MCU serial never disconnected this boot
a_mcu_autosuspend_off|WARN|autosuspend off on the MCU port
a_mcu_not_sharing_ss_hub|WARN|no SuperSpeed device on the MCU's controller
a_no_uas_bound|WARN|no storage bound to the uas driver
a_no_fuse_storage|WARN|no FUSE-mounted storage
a_exfat_in_kernel|WARN|exfat/ntfs handled in-kernel, not by FUSE
a_hub_not_oversubscribed|WARN|no hub carrying more than its upstream share
a_usb_current_budget|FAIL|USB current budget raised
a_can_link_healthy|FAIL|CAN link to the MCU clean
a_can_recovery_sane|WARN|CAN can self-heal from bus-off
a_boot_config_writable|FAIL|boot config.txt actually writable
a_journal_persistent|WARN|kernel journal survives a reboot
a_no_storage_io_errors|WARN|no SD/eMMC I/O errors this boot
a_no_hub_brownout|WARN|no hub brownout signature this boot
ROWS
}

r_history() {
    hdr "klipper shutdowns correlated with USB events"
    out "$(correlate 25)"
}

r_advice() {
    hdr "what to do about it"
    out "  POWER  raise the budget (Pi 5: usb_max_current_enable=1 in config.txt with a 5A PSU) or"
    out "         move the stick to a self-powered hub. A tripped port limit cuts VBUS for every"
    out "         port in the group, so the MCU dies with the stick."
    out "  BUS    force the drive off UAS: lsusb for its VID:PID, then append"
    out "         usb-storage.quirks=VID:PID:u to /boot/firmware/cmdline.txt and reboot."
    out "         Confirm with 'lsusb -t' that it binds usb-storage, not uas."
    out "  ENUM   move the MCU to a different controller than the stick, and use a shielded cable"
    out "         with a ferrite. USB3 emits broadband noise across 2.4GHz."
    out "  LOAD   keep gcode and the moonraker database off the stick, mount noatime, and prefer"
    out "         the in-kernel exfat/ntfs3 drivers over the FUSE ones."
    out "  ALWAYS pin the MCU by /dev/serial/by-id/ (or by-path/) so storage cannot renumber it."
}

# ----------------------------------------------------------------------- watch

printer_state() {
    curl -s -m 5 "$MOON/printer/objects/query?print_stats" 2>/dev/null |
        tr '{},' '\n' | grep '"state"' | head -1 | cut -d'"' -f4
}

do_watch() {
    local st start i node d present gone was_gone drops gone_at longest ktmp kpid kseen knew
    st=$(printer_state)
    # --monitor runs the identical loop without the banner: the guard exists only because --watch tells
    # the operator to hot-plug a drive, and observing a print is not the same act as provoking it.
    if ! $MONITOR; then
        case "${st:-unknown}" in
            printing | paused | unknown | '')
                if $FORCE; then
                    out "printer state is ${st:-unknown}, --force given, watching anyway"
                else
                    out "refusing: printer state is ${st:-unknown}. Reproducing this fault kills the job."
                    out "Re-run after the print, or with --force if you accept losing it."
                    return 2
                fi
                ;;
        esac
    fi

    resolve_mcus
    hdr "live capture (${WATCH_SECS}s)"
    if $MONITOR; then
        out "  Passive monitor, printer state ${st:-unknown}. Nothing is plugged, mounted or written."
        out "  Change nothing while this runs: the point is to see what the box does unprovoked."
    else
        out "  Insert the suspect USB drive NOW. Leave it in. Do not touch anything else."
    fi
    out "  Watching kernel USB events, SoC voltage, host load and the MCU device node."
    out ""
    start=$(date +%s)
    i=0
    # Report the transitions, not the level: one line per second says nothing, while the length of each
    # gap is what separates a re-enumeration (under 2s) from a port that stays dead until replug.
    gone=0
    was_gone=0
    drops=0
    gone_at=0
    longest=0
    kseen=0
    knew=0
    kpid=""
    # Kernel lines are drained into the same timeline as the device state on purpose: the operator has
    # to see the over-current or the reset land next to the drop, not in a separate block a minute later.
    ktmp=$(mktemp 2>/dev/null) || ktmp=""
    if [ -n "$ktmp" ]; then
        journalctl -kf -n0 -o short-iso --no-pager >"$ktmp" 2>/dev/null &
        kpid=$!
    fi
    while [ "$i" -lt "$WATCH_SECS" ]; do
        present=""
        for d in $(mcu_serials); do
            node=$(readlink -f "$d" 2>/dev/null)
            if [ -e "${node:-/nonexistent}" ]; then present="$present +"; else present="$present -MISSING($d)"; fi
        done
        case "$present" in
            *MISSING*) gone=1 ;;
            *) gone=0 ;;
        esac
        if [ "$gone" = 1 ] && [ "$was_gone" = 0 ]; then
            drops=$((drops + 1))
            gone_at=$i
            bad "$(date +%T) t=${i}s  MCU serial gone (drop #$drops):$present"
        elif [ "$gone" = 0 ] && [ "$was_gone" = 1 ]; then
            [ $((i - gone_at)) -gt "$longest" ] && longest=$((i - gone_at))
            out "  $(date +%T) t=${i}s  MCU serial back after $((i - gone_at))s"
        fi
        was_gone=$gone
        if [ -n "$ktmp" ]; then
            knew=$(wc -l <"$ktmp" 2>/dev/null)
            case "${knew:-x}" in '' | *[!0-9]*) knew=$kseen ;; esac
            if [ "$knew" -gt "$kseen" ]; then
                sed -n "$((kseen + 1)),${knew}p" "$ktmp" 2>/dev/null | grep -aE "$USB_PAT" |
                    while IFS= read -r kline; do out "  kern  $kline"; done
                kseen=$knew
            fi
        fi
        if [ $((i % 15)) -eq 0 ]; then
            out "$(printf '  %s  t=%3ds  load=%s  throttled=%s  mcu=%s' \
                "$(date +%T)" "$i" "$(cut -d' ' -f1 /proc/loadavg)" \
                "$(command -v vcgencmd >/dev/null 2>&1 && vcgencmd get_throttled 2>/dev/null | cut -d= -f2 || echo n/a)" \
                "$present")"
        fi
        sleep 1
        i=$((i + 1))
    done
    [ -n "$kpid" ] && kill "$kpid" 2>/dev/null
    [ -n "$ktmp" ] && rm -f "$ktmp"

    hdr "mcu link during the capture"
    if [ "$drops" -gt 0 ]; then
        bad "MCU serial dropped $drops time(s), longest gap ${longest}s"
        out "  Under 2s per gap is the device re-enumerating: port power or link reset, not a dead board."
        out "  A gap that never closes is a port held down until the drive is pulled."
    else
        ok "MCU serial stayed present for the whole capture"
    fi

    hdr "kernel USB events during the capture"
    local ev
    ev=$(journalctl -k -o short-iso --no-pager --since "@$start" 2>/dev/null | grep -aE "$USB_PAT")
    if [ -n "$ev" ]; then out "$ev"; else out "  (none)"; fi

    hdr "storage that appeared"
    local d2 drv
    for d2 in $(usb_devs); do
        drv=$(dev_drivers "$d2")
        case "$drv" in
            *uas* | *usb-storage*)
                out "  $(basename "$d2")  speed=$(sysread "$d2/speed")  power=$(sysread "$d2/bMaxPower")  driver=$drv  $(dev_label "$d2")"
                case "$drv" in
                    *uas*) susp "     bound to uas: append usb-storage.quirks=$(sysread "$d2/idVendor"):$(sysread "$d2/idProduct"):u to cmdline.txt" ;;
                esac
                ;;
        esac
    done

    hdr "klipper reaction"
    local kl
    kl=$(tail -400 "$LOGDIR/klippy.log" 2>/dev/null |
        grep -aE 'Lost communication|Timer too close|shutdown:|Transition to shutdown|Unable to open serial' | tail -8)
    if [ -n "$kl" ]; then
        bad "klipper faulted during the capture:"
        out "$kl"
    else
        ok "klipper stayed up for the whole capture"
    fi
    r_checks
}

# ----------------------------------------------------------------------- modes

do_check() {
    local row fn tier need name d
    # Field 4 marks the rows that read the journal: without it they would silently pass on a box
    # whose journal is unreadable, which is the exact false PASS this suite exists to prevent.
    for row in \
        "a_no_correlated_shutdown|FAIL|J|no klipper shutdown attributable to USB" \
        "a_no_overcurrent_counters|FAIL|-|no latched USB over-current counters" \
        "a_no_overcurrent_journal|FAIL|J|no USB over-current this boot" \
        "a_no_mcu_disconnect|FAIL|J|MCU serial never disconnected this boot" \
        "a_serial_pinned|WARN|-|MCU serial pinned by stable path" \
        "a_no_uas_resets|WARN|J|no UAS/xhci device resets this boot" \
        "a_no_enum_errors|WARN|J|no USB enumeration errors this boot" \
        "a_mcu_autosuspend_off|WARN|-|autosuspend off on the MCU port" \
        "a_no_uas_bound|WARN|-|no storage bound to the uas driver" \
        "a_no_fuse_storage|WARN|-|no FUSE-mounted storage" \
        "a_mcu_not_sharing_ss_hub|WARN|-|no SuperSpeed device on the MCU's controller" \
        "a_exfat_in_kernel|WARN|-|exfat/ntfs handled in-kernel, not by FUSE" \
        "a_hub_not_oversubscribed|WARN|-|no hub carrying more than its upstream share" \
        "a_usb_current_budget|FAIL|-|USB current budget raised" \
        "a_can_link_healthy|FAIL|-|CAN link to the MCU clean" \
        "a_boot_config_writable|FAIL|-|boot config.txt actually writable" \
        "a_can_recovery_sane|WARN|-|CAN can self-heal from bus-off" \
        "a_journal_persistent|WARN|-|kernel journal survives a reboot" \
        "a_no_storage_io_errors|WARN|J|no SD/eMMC I/O errors this boot" \
        "a_no_hub_brownout|WARN|J|no hub brownout signature this boot"; do
        IFS='|' read -r fn tier need name <<<"$row"
        if [ "$need" = J ] && ! journal_readable; then
            emit SKIP "$name" "kernel journal unreadable"
            continue
        fi
        d=$("$fn" 2>&1)
        case $? in
            0) emit PASS "$name" ;;
            2) emit SKIP "$name" "$(echo "$d" | tr '\n' ';' | cut -c1-300)" ;;
            *) emit "$tier" "$name" "$(echo "$d" | tr '\n' ';' | cut -c1-300)" ;;
        esac
    done
}

case "$MODE" in
    check) do_check ;;
    history) r_history ;;
    watch) do_watch ;;
    report)
        out "BlocksScreen USB fault forensics  $(date -Is)  host=$(hostname)"
        r_host
        r_topology
        r_checks
        r_history
        r_advice
        ;;
esac

if [ -n "$REPORT" ]; then
    $QUIET || printf '\nreport written to %s (downloadable from the UI, no SSH needed)\n' "$REPORT"
fi
