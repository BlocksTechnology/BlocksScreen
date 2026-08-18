#!/usr/bin/env bash
# Read-only Raspberry Pi power audit: input budget, PMIC rails, USB draw, throttling and headroom.
# Nothing here writes config, restarts a service, or touches the printer. --stress is the one opt-in load.
set -u

VERBOSE=0
WATCH=0
STRESS=0
BURN=0
BED=0
FORCE=0
ASSUME_YES=0

usage() {
    cat <<'EOF'
Usage: bs-power.sh [options]

  -v            verbose: per-rail table and full USB device list
  --watch N     sample every second for N seconds, report min/max and any event
  --stress N    run an N-second CPU load and report voltage sag (refuses while printing)
  --burn N      staged ramp, N seconds per stage, to measure real headroom (refuses while printing)
  --bed TEMP    heat the bed from cold and test whether the 24V heater pulls down the Pi 5V rail
  --force       allow --stress and --burn even when the printer state cannot be determined
  --yes         skip the --bed confirmation prompt (required when stdin is not a tty)
  -h            this help

Read-only by default. Run as any user; a few nodes need root and are marked when skipped.
EOF
}

while [ $# -gt 0 ]; do
    case "$1" in
    -v) VERBOSE=1 ;;
    --watch)
        WATCH="${2:-30}"
        shift
        ;;
    --stress)
        STRESS="${2:-20}"
        shift
        ;;
    --burn)
        BURN="${2:-20}"
        shift
        ;;
    --bed)
        BED="${2:-60}"
        shift
        ;;
    --force) FORCE=1 ;;
    --yes) ASSUME_YES=1 ;;
    -h | --help)
        usage
        exit 0
        ;;
    *)
        echo "unknown option: $1" >&2
        usage
        exit 2
        ;;
    esac
    shift
done

C_OK=''
C_BAD=''
C_WARN=''
C_DIM=''
C_OFF=''
if [ -t 1 ]; then
    C_OK=$'\033[32m'
    C_BAD=$'\033[31m'
    C_WARN=$'\033[33m'
    C_DIM=$'\033[2m'
    C_OFF=$'\033[0m'
fi

hdr() { printf '\n%s== %s ==%s\n' "$C_DIM" "$1" "$C_OFF"; }
kv() { printf '  %-28s %s\n' "$1" "$2"; }
ok() { printf '  %sOK%s   %s\n' "$C_OK" "$C_OFF" "$1"; }
bad() { printf '  %sBAD%s  %s\n' "$C_BAD" "$C_OFF" "$1"; }
warn() { printf '  %sWARN%s %s\n' "$C_WARN" "$C_OFF" "$1"; }
note() { printf '  %s%s%s\n' "$C_DIM" "$1" "$C_OFF"; }

# Reads a sysfs or procfs node, returning empty rather than an error when it is absent.
sysread() { [ -r "$1" ] && tr -d '\0' <"$1" 2>/dev/null; }

have() { command -v "$1" >/dev/null 2>&1; }

VCG=$(command -v vcgencmd 2>/dev/null)
vc() { [ -n "$VCG" ] && "$VCG" "$@" 2>/dev/null; }

# A device-tree cell is big-endian u32, so od is the portable way to read it as a number.
dtnum() {
    [ -r "$1" ] || return 1
    od -An -tu4 --endian=big "$1" 2>/dev/null | tr -d ' \n'
}

MODEL=$(sysread /proc/device-tree/model)
IS_PI5=0
case "$MODEL" in *"Raspberry Pi 5"*) IS_PI5=1 ;; esac

# ---------------------------------------------------------------- identity

hdr "IDENTITY"
kv "model" "${MODEL:-unknown}"
kv "serial" "$(awk '/^Serial/{print $3}' /proc/cpuinfo 2>/dev/null)"
kv "kernel" "$(uname -r)"
kv "os" "$(. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME")"
kv "firmware" "$(vc version | head -1)"
kv "uptime" "$(awk '{printf "%.1f h", $1/3600}' /proc/uptime)"
kv "loadavg" "$(awk '{print $1", "$2", "$3}' /proc/loadavg)"
[ -n "$VCG" ] || warn "vcgencmd not found: rail, throttle and config readings unavailable"

# ------------------------------------------------------------- power input

hdr "POWER IN (what the Pi believes it may draw)"

EXT5V=$(vc pmic_read_adc EXT5V_V | sed -n 's/.*=\([0-9.]*\)V/\1/p')
BATTV=$(vc pmic_read_adc BATT_V | sed -n 's/.*=\([0-9.]*\)V/\1/p')

if [ -n "$EXT5V" ]; then
    kv "input voltage (EXT5V)" "$EXT5V V"
    # Below 4.75V the SoC is out of spec, and 4.8V is where sag starts costing USB stability.
    awk -v v="$EXT5V" 'BEGIN{exit !(v < 4.75)}' && bad "input voltage below 4.75V spec minimum"
    awk -v v="$EXT5V" 'BEGIN{exit !(v >= 4.75 && v < 4.90)}' && warn "input voltage sagging, check supply and cable"
    awk -v v="$EXT5V" 'BEGIN{exit !(v >= 4.90)}' && ok "input voltage healthy"
else
    note "input voltage not readable (needs a Pi 5 with PMIC support)"
fi
[ -n "$BATTV" ] && kv "RTC battery" "$BATTV V"

# max_current is what the firmware concluded, whether by PD negotiation or by EEPROM override.
MAXCUR=''
for n in /proc/device-tree/chosen/power/max_current \
    /proc/device-tree/chosen/power/max_current_ma \
    /sys/firmware/devicetree/base/chosen/power/max_current; do
    MAXCUR=$(dtnum "$n") && [ -n "$MAXCUR" ] && break
done
if [ -n "$MAXCUR" ]; then
    kv "firmware PSU budget" "$MAXCUR mA"
else
    note "firmware PSU budget node not present"
fi

PSUCFG=''
if have rpi-eeprom-config; then
    PSUCFG=$(rpi-eeprom-config 2>/dev/null | sed -n 's/^PSU_MAX_CURRENT=//p')
fi
kv "PSU_MAX_CURRENT (eeprom)" "${PSUCFG:-unset}"

USBMAX=$(vc get_config usb_max_current_enable | cut -d= -f2)
kv "usb_max_current_enable" "${USBMAX:-0}"

if [ "$IS_PI5" = 1 ]; then
    # PSU_MAX_CURRENT does NOT raise the port limit, only usb_max_current_enable does: forums.raspberrypi.com t=388128.
    USB_BUDGET=600
    [ "${USBMAX:-0}" = 1 ] && USB_BUDGET=1600
    kv "effective USB budget" "$USB_BUDGET mA"

    if [ "${USBMAX:-0}" != 1 ]; then
        bad "USB ports capped at 600mA: one USB3 stick's inrush can exceed this and cut VBUS to every port"
        note "fix: append usb_max_current_enable=1 to /boot/firmware/config.txt and reboot"
        [ -n "$PSUCFG" ] &&
            bad "PSU_MAX_CURRENT=$PSUCFG is set but does not raise the port limit: it only hides the warning"
    fi
    # The 900mA belief is cosmetic, and it is the only automatic signal that a box has an undersized PSU.
    if [ -z "$PSUCFG" ] && [ "${MAXCUR:-0}" -lt 5000 ] 2>/dev/null; then
        note "firmware assumes a ${MAXCUR:-3000}mA supply: cosmetic, and worth keeping as an undersized-PSU tell"
    fi
    if [ -n "$PSUCFG" ] && [ "${MAXCUR:-0}" -lt "$PSUCFG" ] 2>/dev/null; then
        bad "PSU_MAX_CURRENT=$PSUCFG is set but firmware reports ${MAXCUR}mA: the eeprom write did not take"
    fi
fi

# -------------------------------------------------------------- pmic rails

hdr "POWER RAILS (measured by the PMIC)"

RAILS=$(vc pmic_read_adc)
RAILW=''
if [ -n "$RAILS" ]; then
    RAILTBL=$(printf '%s\n' "$RAILS" | awk '
        {
            n=$1; val=$2
            sub(/^[^=]*=/, "", val); sub(/[AV]$/, "", val)
            key=n; sub(/_[AV]$/, "", key)
            if (n ~ /_A$/) cur[key]=val+0; else volt[key]=val+0
        }
        END {
            for (k in cur) {
                if (!(k in volt)) continue
                p = cur[k] * volt[k]; tot += p
                printf "  %-14s %8.4f A  %7.4f V  %7.3f W\n", k, cur[k], volt[k], p
            }
            printf "TOTAL %.4f\n", tot
        }' | sort)
    RAILW=$(printf '%s\n' "$RAILTBL" | sed -n 's/^TOTAL //p')
    [ "$VERBOSE" = 1 ] && printf '%s\n' "$RAILTBL" | grep -v '^TOTAL'
    if [ -n "$RAILW" ]; then
        kv "instrumented rails" "$(awk -v w="$RAILW" 'BEGIN{printf "%.2f W", w}')"
        # jfikar's linear fit against a USB-C meter, correcting for rails the PMIC does not see.
        kv "board total (calibrated)" "$(awk -v w="$RAILW" 'BEGIN{printf "%.2f W", w*1.1451+0.5879}')"
        note "calibration real=pmic*1.1451+0.5879 (jfikar/RPi5-power); excludes USB VBUS, NVMe and HATs"
    fi
else
    note "no PMIC rail data (Pi 4 and earlier do not expose this)"
fi

# ------------------------------------------------------------- usb loading

hdr "POWER OUT (USB devices and their declared draw)"

USB_TOTAL=0
USB_ROWS=''
for d in /sys/bus/usb/devices/*; do
    [ -r "$d/bMaxPower" ] || continue
    p=$(sysread "$d/bMaxPower")
    ma=${p%mA}
    case "${ma:-x}" in '' | *[!0-9]*) continue ;; esac
    dev=$(basename "$d")
    case "$dev" in usb*) continue ;; esac
    prod=$(sysread "$d/product")
    vid=$(sysread "$d/idVendor")
    pid=$(sysread "$d/idProduct")
    spd=$(sysread "$d/speed")
    drv=''
    for i in "$d":*; do
        [ -e "$i/driver" ] && drv="$drv $(basename "$(readlink -f "$i/driver")")"
    done
    USB_TOTAL=$((USB_TOTAL + ma))
    USB_ROWS="$USB_ROWS$(printf '  %-8s %6smA %7sM %-24s %s:%s %s\n' \
        "$dev" "$ma" "${spd:-?}" "${prod:-unknown}" "$vid" "$pid" "${drv# }")"$'\n'
done

if [ -n "$USB_ROWS" ]; then
    [ "$VERBOSE" = 1 ] && printf '%s' "$USB_ROWS"
    kv "devices attached" "$(printf '%s' "$USB_ROWS" | grep -c .)"
    kv "declared draw total" "$USB_TOTAL mA"
    if [ "$IS_PI5" = 1 ]; then
        kv "against budget" "$(awk -v u="$USB_TOTAL" -v b="$USB_BUDGET" 'BEGIN{printf "%.0f%% of %dmA", u*100/b, b}')"
        if [ "$USB_TOTAL" -gt "$USB_BUDGET" ]; then
            bad "declared USB draw exceeds the port budget: over-current trips are expected under load"
        elif [ "$USB_TOTAL" -gt $((USB_BUDGET * 80 / 100)) ]; then
            warn "declared USB draw is above 80% of budget, leaving no room for inrush"
        else
            ok "USB draw within budget"
        fi
    fi
    note "declared is bMaxPower, a descriptor claim; actual draw is usually lower at idle and higher at inrush"
else
    note "no USB devices with a readable bMaxPower"
fi

# A bus-powered hub carrying high-draw devices is the classic hidden over-subscription.
for d in /sys/bus/usb/devices/*; do
    [ -r "$d/bDeviceClass" ] || continue
    [ "$(sysread "$d/bDeviceClass")" = "09" ] || continue
    dev=$(basename "$d")
    hp=$(sysread "$d/bMaxPower")
    kids=0
    kidma=0
    for c in /sys/bus/usb/devices/"$dev".*; do
        [ -r "$c/bMaxPower" ] || continue
        kids=$((kids + 1))
        k=$(sysread "$c/bMaxPower")
        k=${k%mA}
        case "${k:-x}" in '' | *[!0-9]*) continue ;; esac
        kidma=$((kidma + k))
    done
    [ "$kids" = 0 ] && continue
    kv "hub $dev" "self-declared $hp, $kids devices drawing ${kidma}mA"
    # A hub declaring 100mA is bus powered, and 100mA cannot legally feed downstream ports.
    if [ "${hp%mA}" -le 100 ] 2>/dev/null && [ "$kidma" -gt 100 ]; then
        bad "hub $dev appears bus powered but carries ${kidma}mA of devices: fit a powered hub"
    fi
done

# --------------------------------------------------------- throttle status

hdr "THROTTLING AND UNDERVOLTAGE"

TH=$(vc get_throttled | cut -d= -f2)
if [ -n "$TH" ]; then
    kv "get_throttled" "$TH"
    thv=$((TH))
    b() { [ $((thv & (1 << $1))) -ne 0 ] && echo yes || echo no; }
    if [ "$thv" = 0 ]; then
        ok "no undervoltage or throttling, now or since boot"
    else
        [ "$(b 0)" = yes ] && bad "undervoltage RIGHT NOW"
        [ "$(b 1)" = yes ] && warn "arm frequency capped right now"
        [ "$(b 2)" = yes ] && bad "currently throttled"
        [ "$(b 3)" = yes ] && warn "soft temperature limit active"
        [ "$(b 16)" = yes ] && bad "undervoltage has occurred since boot"
        [ "$(b 17)" = yes ] && warn "arm frequency capping has occurred since boot"
        [ "$(b 18)" = yes ] && warn "throttling has occurred since boot"
        [ "$(b 19)" = yes ] && warn "soft temperature limit reached since boot"
    fi
fi

# The hwmon index moves between boards and kernels, so never hardcode it.
for h in /sys/class/hwmon/hwmon*; do
    [ "$(sysread "$h/name")" = rpi_volt ] || continue
    a=$(sysread "$h/in0_lcrit_alarm")
    kv "hwmon $(basename "$h") lcrit" "${a:-n/a}"
    [ "${a:-0}" = 1 ] && bad "kernel undervoltage alarm is set"
done

UV=$(journalctl -k --no-pager 2>/dev/null | grep -ci 'under-voltage')
OC=$(journalctl -k --no-pager 2>/dev/null | grep -ci 'over-current change')
kv "undervoltage log lines" "${UV:-0}"
kv "over-current log lines" "${OC:-0}"
[ "${OC:-0}" -gt 0 ] && bad "kernel has logged over-current events: USB VBUS has been cut at least once"

# Sysfs counters can read zero while the journal shows trips, so both are reported.
for p in /sys/bus/usb/devices/*-port*/over_current_count; do
    [ -r "$p" ] || continue
    c=$(sysread "$p")
    [ "${c:-0}" = 0 ] && continue
    port=$(basename "$(dirname "$p")")
    bad "port $port over_current_count=$c"
done

# ------------------------------------------------------------ thermal load

hdr "THERMAL AND CLOCKS"
if [ -n "$VCG" ]; then
    kv "soc temperature" "$(vc measure_temp | cut -d= -f2)"
    kv "core voltage" "$(vc measure_volts core | cut -d= -f2)"
    kv "arm clock" "$(awk -v h="$(vc measure_clock arm | cut -d= -f2)" 'BEGIN{printf "%.0f MHz", h/1000000}')"
    kv "core clock" "$(awk -v h="$(vc measure_clock core | cut -d= -f2)" 'BEGIN{printf "%.0f MHz", h/1000000}')"
fi
for f in /sys/class/thermal/thermal_zone*/temp; do
    [ -r "$f" ] || continue
    kv "$(basename "$(dirname "$f")")" "$(awk -v t="$(sysread "$f")" 'BEGIN{printf "%.1f C", t/1000}')"
done

# ------------------------------------------------------------- input ledger

hdr "ESTIMATED INPUT DRAW"

if [ -n "$RAILW" ] && [ -n "$EXT5V" ]; then
    awk -v rw="$RAILW" -v usb="$USB_TOTAL" -v v="$EXT5V" 'BEGIN {
        board = rw * 1.1451 + 0.5879
        usbw  = usb / 1000.0 * 5.0
        tot   = board + usbw
        printf "  %-28s %.2f W\n", "board (calibrated rails)", board
        printf "  %-28s %.2f W   (%dmA declared)\n", "usb peripherals", usbw, usb
        printf "  %-28s %.2f W\n", "estimated total", tot
        printf "  %-28s %.2f A  at %.2f V\n", "estimated input current", tot / v, v
    }'
    note "board figure is measured and calibrated; the USB figure is a descriptor sum, so treat the total as +/-20%"
    note "fan, HDMI 5V pin and anything on the GPIO 5V rail are NOT included"
    note "only an inline DC meter or a DC clamp on the positive lead gives a true input reading"
else
    note "insufficient data for an input estimate"
fi

# ------------------------------------------------------------------- watch

if [ "$WATCH" != 0 ]; then
    hdr "WATCH ${WATCH}s"
    note "insert or remove peripherals now to see the transient"
    vmin=99
    vmax=0
    wmax=0
    i=0
    oc0=$(journalctl -k --no-pager 2>/dev/null | grep -ci 'over-current change')
    while [ "$i" -lt "$WATCH" ]; do
        v=$(vc pmic_read_adc EXT5V_V | sed -n 's/.*=\([0-9.]*\)V/\1/p')
        w=$(vc pmic_read_adc | awk '
            { n=$1; val=$2; sub(/^[^=]*=/,"",val); sub(/[AV]$/,"",val)
              key=n; sub(/_[AV]$/,"",key)
              if (n ~ /_A$/) cur[key]=val+0; else volt[key]=val+0 }
            END { for (k in cur) if (k in volt) t += cur[k]*volt[k]; printf "%.3f", t }')
        t=$(vc get_throttled | cut -d= -f2)
        [ -n "$v" ] && {
            vmin=$(awk -v a="$vmin" -v b="$v" 'BEGIN{print (b<a)?b:a}')
            vmax=$(awk -v a="$vmax" -v b="$v" 'BEGIN{print (b>a)?b:a}')
        }
        [ -n "$w" ] && wmax=$(awk -v a="$wmax" -v b="$w" 'BEGIN{print (b>a)?b:a}')
        [ "$VERBOSE" = 1 ] && printf '  %3ds  %sV  %sW  throttled=%s\n' "$i" "${v:-?}" "${w:-?}" "${t:-?}"
        [ "${t:-0x0}" != "0x0" ] && bad "throttled=$t at t=${i}s"
        i=$((i + 1))
        sleep 1
    done
    oc1=$(journalctl -k --no-pager 2>/dev/null | grep -ci 'over-current change')
    kv "input voltage min/max" "$vmin V / $vmax V"
    kv "rail power peak" "$wmax W"
    kv "over-current events" "$((oc1 - oc0)) during the window"
    [ "$((oc1 - oc0))" -gt 0 ] && bad "VBUS was cut during the watch window"
    awk -v a="$vmin" -v b="$vmax" 'BEGIN{exit !(b-a > 0.15)}' &&
        warn "input voltage moved more than 150mV: the supply or cabling is loaded near its limit"
fi

# ------------------------------------------------------------------ stress

# Never load the SoC mid-print: a thermal or voltage event during a job ruins the part.
require_idle_printer() {
    local st
    st=$(curl -s --max-time 3 \
        'http://127.0.0.1:7125/printer/objects/query?print_stats' 2>/dev/null |
        sed -n 's/.*"state": *"\([a-z]*\)".*/\1/p')
    case "$st" in
    printing | paused)
        bad "printer state is '$st': refusing to run a load test"
        exit 1
        ;;
    '')
        if [ "$FORCE" != 1 ]; then
            bad "cannot reach moonraker to confirm the printer is idle: rerun with --force if you are sure"
            exit 1
        fi
        warn "printer state unknown, proceeding because --force was given"
        ;;
    *) note "printer state '$st', safe to load" ;;
    esac
}

if [ "$STRESS" != 0 ]; then
    hdr "STRESS ${STRESS}s"
    require_idle_printer

    v0=$(vc pmic_read_adc EXT5V_V | sed -n 's/.*=\([0-9.]*\)V/\1/p')
    kv "idle input voltage" "${v0:-?} V"
    n=$(nproc)
    for _ in $(seq "$n"); do
        timeout "$STRESS" awk 'BEGIN{for(;;)x+=1}' &
    done
    sleep $((STRESS / 2))
    v1=$(vc pmic_read_adc EXT5V_V | sed -n 's/.*=\([0-9.]*\)V/\1/p')
    w1=$(vc pmic_read_adc | awk '
        { n=$1; val=$2; sub(/^[^=]*=/,"",val); sub(/[AV]$/,"",val)
          key=n; sub(/_[AV]$/,"",key)
          if (n ~ /_A$/) cur[key]=val+0; else volt[key]=val+0 }
        END { for (k in cur) if (k in volt) t += cur[k]*volt[k]; printf "%.3f", t }')
    t1=$(vc get_throttled | cut -d= -f2)
    wait
    kv "loaded input voltage" "${v1:-?} V"
    kv "loaded rail power" "${w1:-?} W"
    kv "loaded temperature" "$(vc measure_temp | cut -d= -f2)"
    kv "throttled under load" "${t1:-?}"
    if [ -n "$v0" ] && [ -n "$v1" ]; then
        awk -v a="$v0" -v b="$v1" 'BEGIN{printf "  %-28s %.3f V\n", "voltage sag under load", a-b}'
        awk -v a="$v0" -v b="$v1" 'BEGIN{exit !(a-b > 0.20)}' &&
            bad "supply sags more than 200mV under CPU load: the PSU or its cabling is undersized"
        awk -v a="$v0" -v b="$v1" 'BEGIN{exit !(a-b <= 0.20)}' &&
            ok "supply holds up under CPU load"
    fi
    [ "${t1:-0x0}" != "0x0" ] && bad "throttling occurred under load: $t1"
fi

# ------------------------------------------------------------------- burn

# Adds one load domain per stage so the limit that binds first is measured rather than guessed.
if [ "$BURN" != 0 ]; then
    hdr "BURN ${BURN}s per stage"
    require_idle_printer

    ext5v() { vc pmic_read_adc EXT5V_V | sed -n 's/.*=\([0-9.]*\)V/\1/p'; }
    rail_w() {
        vc pmic_read_adc | awk '
            { n=$1; val=$2; sub(/^[^=]*=/,"",val); sub(/[AV]$/,"",val)
              key=n; sub(/_[AV]$/,"",key)
              if (n ~ /_A$/) cur[key]=val+0; else volt[key]=val+0 }
            END { for (k in cur) if (k in volt) t += cur[k]*volt[k]; printf "%.3f", t }'
    }

    NC=$(nproc 2>/dev/null)
    case "${NC:-x}" in '' | *[!0-9]*) NC=4 ;; esac
    LIMIT=$((BURN * 10 + 120))
    HAVE_SNG=0
    have stress-ng && HAVE_SNG=1
    [ "$HAVE_SNG" = 1 ] || note "stress-ng not installed: falling back to awk loops, which understate real SoC draw"

    # Only a removable disk is ever read, and only for reading, so no printer storage is touched.
    BURN_USB=''
    for b in /sys/block/sd*; do
        [ "$(sysread "$b/removable")" = 1 ] || continue
        BURN_USB="/dev/$(basename "$b")"
        break
    done
    [ "$(id -u)" = 0 ] || BURN_USB=''

    BURN_PIDS=''
    burn_stop() {
        [ -n "$BURN_PIDS" ] && kill $BURN_PIDS 2>/dev/null
        BURN_PIDS=''
        sleep 1
    }
    trap 'burn_stop; echo; note "burn aborted, load killed"; exit 130' INT TERM

    spawn() {
        "$@" >/dev/null 2>&1 &
        BURN_PIDS="$BURN_PIDS $!"
    }
    load_cpu() {
        if [ "$HAVE_SNG" = 1 ]; then
            spawn stress-ng --cpu "$1" --cpu-method matrixprod --timeout "${LIMIT}s"
        else
            i=0
            while [ "$i" -lt "$1" ]; do
                spawn timeout "$LIMIT" awk 'BEGIN{for(;;){x+=1.000001;y=x*x}}'
                i=$((i + 1))
            done
        fi
    }
    load_ram() {
        if [ "$HAVE_SNG" = 1 ]; then
            spawn stress-ng --vm 2 --vm-bytes 25% --timeout "${LIMIT}s"
        else
            spawn timeout "$LIMIT" awk 'BEGIN{n=3000000;for(i=0;i<n;i++)a[i]=i;for(;;){s=0;for(i=0;i<n;i++)s+=a[i]}}'
        fi
    }
    # iflag=direct bypasses the page cache so this is sustained real bus traffic, not a memory read.
    load_usb() {
        [ -n "$BURN_USB" ] || return 0
        spawn timeout "$LIMIT" sh -c "while :; do dd if=$BURN_USB of=/dev/null bs=1M count=4000 iflag=direct 2>/dev/null; done"
    }
    apply_load() {
        burn_stop
        [ "$1" -gt 0 ] && load_cpu "$1"
        [ "$2" = 1 ] && load_ram
        [ "$3" = 1 ] && load_usb
        sleep 2
        return 0
    }

    # Averages only the settled second half of each stage so ramp-up does not pull the mean.
    burn_measure() {
        local d="$1" i=0 half v w th tc vsum=0 vn=0
        S_VMIN=99
        S_WMAX=0
        S_TMAX=0
        S_TH=0x0
        half=$((d / 2))
        while [ "$i" -lt "$d" ]; do
            v=$(ext5v)
            w=$(rail_w)
            th=$(vc get_throttled | cut -d= -f2)
            tc=$(sysread /sys/class/thermal/thermal_zone0/temp)
            case "${v:-x}" in '' | *[!0-9.]*) v='' ;; esac
            case "${w:-x}" in '' | *[!0-9.]*) w='' ;; esac
            [ -n "$v" ] && S_VMIN=$(awk -v a="$S_VMIN" -v b="$v" 'BEGIN{print (b<a)?b:a}')
            [ -n "$w" ] && S_WMAX=$(awk -v a="$S_WMAX" -v b="$w" 'BEGIN{print (b>a)?b:a}')
            case "${tc:-x}" in '' | *[!0-9]*) ;; *) S_TMAX=$(awk -v a="$S_TMAX" -v b="$tc" 'BEGIN{print (b>a)?b:a}') ;; esac
            case "${th:-0x0}" in 0x0) ;; *) S_TH="$th" ;; esac
            if [ "$i" -ge "$half" ] && [ -n "$v" ]; then
                vsum=$(awk -v s="$vsum" -v b="$v" 'BEGIN{printf "%.6f", s+b}')
                vn=$((vn + 1))
            fi
            i=$((i + 1))
            sleep 1
        done
        S_VAVG=$(awk -v s="$vsum" -v n="$vn" 'BEGIN{if(n>0)printf "%.5f", s/n}')
        return 0
    }

    ABORT=0
    stage() {
        burn_measure "$BURN"
        awk -v l="$1" -v w="$S_WMAX" -v vm="$S_VMIN" -v va="${S_VAVG:-0}" -v t="$S_TMAX" -v th="$S_TH" \
            'BEGIN{printf "  %-22s %6.2f W %8.4f V %8.4f V %5.1f C  %s\n", l, w, vm, va, t/1000, th}'
        case "$S_TH" in
        0x0) ;;
        *)
            bad "throttle or undervoltage bits set during '$1': $S_TH"
            ABORT=1
            ;;
        esac
        awk -v t="$S_TMAX" 'BEGIN{exit !(t / 1000 >= 80)}' && {
            bad "SoC reached 80C during '$1': thermal is the binding limit, not power"
            ABORT=1
        }
        return 0
    }

    oc0=$(journalctl -k --no-pager 2>/dev/null | grep -ci 'over-current change')
    note "each stage holds ${BURN}s; loads are additive and rebuilt from scratch every stage"
    printf '  %-22s %8s %10s %10s %7s  %s\n' stage rails Vmin Vavg temp throttled

    apply_load 0 0 0
    stage "0 idle"
    IDLE_W=$S_WMAX
    IDLE_V=${S_VAVG:-0}
    PEAK_W=$S_WMAX
    PEAK_V=${S_VAVG:-0}
    PEAK_T=$S_TMAX
    PEAK_LBL="0 idle"

    for spec in "1 cpu x1|1|0|0" "2 cpu x$NC|$NC|0|0" "3 cpu+ram|$NC|1|0" "4 cpu+ram+usb|$NC|1|1"; do
        [ "$ABORT" = 0 ] || break
        lbl=${spec%%|*}
        rest=${spec#*|}
        c=${rest%%|*}
        rest=${rest#*|}
        r=${rest%%|*}
        u=${rest#*|}
        if [ "$u" = 1 ] && [ -z "$BURN_USB" ]; then
            note "skipping '$lbl': no removable USB disk found, or not running as root"
            continue
        fi
        apply_load "$c" "$r" "$u"
        stage "$lbl"
        PEAK_LBL="$lbl"
        PEAK_W=$S_WMAX
        PEAK_V=${S_VAVG:-0}
        PEAK_T=$S_TMAX
    done

    burn_stop
    trap - INT TERM
    oc1=$(journalctl -k --no-pager 2>/dev/null | grep -ci 'over-current change')
    [ "$((oc1 - oc0))" -gt 0 ] && bad "VBUS was cut $((oc1 - oc0)) time(s) during the burn: USB is the binding limit"

    hdr "HEADROOM ANALYSIS"
    kv "peak stage" "$PEAK_LBL"
    if [ -n "$BURN_USB" ]; then kv "usb load device" "$BURN_USB"; else kv "usb load device" "none, stage skipped"; fi

    # Source impedance from the idle-to-peak step is what turns a single reading into a projection.
    awk -v iw="$IDLE_W" -v pw="$PEAK_W" -v iv="$IDLE_V" -v pv="$PEAK_V" -v pt="$PEAK_T" \
        -v usb="$USB_TOTAL" -v budget="${USB_BUDGET:-0}" '
    BEGIN {
        dw = pw - iw; dv = iv - pv
        printf "  %-28s %.2f W\n", "rail power idle to peak", dw
        printf "  %-28s %.4f V\n", "voltage sag idle to peak", dv
        if (dw <= 0.2) { print "  not enough load delta to derive impedance: raise the stage time"; exit }
        di = dw / 0.9 / pv
        printf "  %-28s %.3f A\n", "input current step", di
        r = 0
        # Two runs stepped 0.59A/0.76A and produced 104/82 mOhm from an identical sag: under ~1A the step sits inside the EXT5V ADC noise floor, so dV/dI tracks drift, not resistance.
        if (di < 1.0) {
            print "  step is under 1A: impedance and brownout projections suppressed, they are noise here"
        } else if (dv > 0.002) {
            r = dv / di
            printf "  %-28s %.0f mOhm  (supply plus cable)\n", "source impedance", r * 1000
            head = (pv - 4.70) / r
            printf "  %-28s %.2f A more before 4.70V\n", "projected sag headroom", head
        } else {
            print "  sag is below the ADC noise floor: impedance is too low to measure, which is a good sign"
        }
        board = pw * 1.1451 + 0.5879
        tot = board + usb / 1000.0 * 5.0
        printf "  %-28s %.2f W  = %.2f A at %.2f V\n", "estimated draw at peak", tot, tot / pv, pv
        if (r > 0) printf "  %-28s %.2f A total\n", "projected brownout current", tot / pv + (pv - 4.70) / r
        printf "  %-28s %.1f C of 80 C\n", "thermal headroom", 80 - pt / 1000
        printf "  %-28s %d mA of %d mA declared\n", "usb budget headroom", budget - usb, budget
    }'
    note "rail power excludes USB VBUS, so the USB stage shows up as sag and heat, not as rail watts"
    note "the PSU nameplate rating is not readable in software: compare the projected figures to it yourself"
fi

# --bed: does the 24V bed heater pull down the Pi's 5V rail? Answers "shared/coupled supply" vs "independent".
if [ "$BED" != 0 ]; then
    hdr "bed heater / 5V rail coupling test"
    MURL=http://127.0.0.1:7125

    case "$BED" in
    '' | *[!0-9]*) bad "--bed needs an integer temperature in C" && exit 2 ;;
    esac
    if [ "$BED" -lt 40 ] || [ "$BED" -gt 110 ]; then
        bad "--bed $BED is outside the sane 40-110 C range"
        exit 2
    fi
    [ -n "$VCG" ] || {
        bad "vcgencmd not available: cannot sample the 5V rail"
        exit 1
    }
    have curl || {
        bad "curl not available: cannot drive the bed"
        exit 1
    }

    bed_v5() { vc pmic_read_adc EXT5V_V | sed -n 's/.*=\([0-9.]*\)V/\1/p'; }
    bed_thr() { vc get_throttled | cut -d= -f2; }
    # Moonraker returns one flat object here, so splitting on separators and taking the value field is enough.
    bed_read() {
        curl -s --max-time 3 "$MURL/printer/objects/query?heater_bed" 2>/dev/null |
            tr ',{}' '\n\n\n' | awk -F': *' '
                /"temperature"/ {t=$2}
                /"target"/      {g=$2}
                /"power"/       {p=$2}
                END {if (t=="") exit 1; printf "%.2f %.2f %.4f\n", t, g, p}'
    }
    bed_klippy() { curl -s --max-time 3 "$MURL/printer/info" 2>/dev/null | sed -n 's/.*"state": *"\([a-z]*\)".*/\1/p'; }
    bed_off() { curl -s --max-time 5 -X POST "$MURL/printer/gcode/script?script=M140%20S0" >/dev/null 2>&1; }

    # This mode commands a heater, so an unreachable moonraker is a hard stop and --force must not bypass it.
    BSTATE=$(curl -s --max-time 3 "$MURL/printer/objects/query?print_stats" 2>/dev/null |
        sed -n 's/.*"state": *"\([a-z]*\)".*/\1/p')
    case "$BSTATE" in
    printing | paused)
        bad "printer state is '$BSTATE': refusing to command the bed"
        exit 1
        ;;
    '')
        bad "cannot reach moonraker: refusing to command the bed (--force does not apply here)"
        exit 1
        ;;
    *) note "printer state '$BSTATE'" ;;
    esac
    KST=$(bed_klippy)
    [ "$KST" = ready ] || {
        bad "klippy state is '${KST:-unknown}', not ready"
        exit 1
    }

    BR=$(bed_read) || {
        bad "no heater_bed object: is this printer configured with a heated bed?"
        exit 1
    }
    B_T0=$(echo "$BR" | cut -d' ' -f1)
    awk -v t="$B_T0" -v g="$BED" 'BEGIN{exit !(t > g - 5)}' && {
        bad "bed is already at ${B_T0}C: this test needs a cold start to see full heater duty"
        exit 1
    }

    warn "this will heat the bed to ${BED}C at full power. Do not touch the bed."
    if [ "$ASSUME_YES" != 1 ]; then
        [ -t 0 ] || {
            bad "stdin is not a tty: rerun with --yes"
            exit 1
        }
        printf '  type yes to continue: '
        read -r ANS
        [ "$ANS" = yes ] || {
            note "aborted"
            exit 0
        }
    fi

    BED_LOG=$(mktemp /tmp/bs-bed-XXXXXX.tsv)
    # Any exit path must leave the bed off, including ctrl-c: a hot bed left on unattended is the real hazard.
    bed_cleanup() {
        bed_off
        note "bed commanded off"
    }
    trap 'bed_cleanup; exit 130' INT TERM
    trap 'bed_cleanup' EXIT

    bed_sample() {
        local r t pw v th
        r=$(bed_read) || return 0
        t=$(echo "$r" | cut -d' ' -f1)
        pw=$(echo "$r" | cut -d' ' -f3)
        v=$(bed_v5)
        th=$(bed_thr)
        printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$pw" "$t" "${v:-0}" "${th:-NA}" >>"$BED_LOG"
    }

    note "phase 1: 20s baseline, bed off"
    bed_off
    i=0
    while [ "$i" -lt 20 ]; do
        bed_sample base "$i"
        sleep 1
        i=$((i + 1))
    done

    note "phase 2: heating to ${BED}C (600s cap)"
    curl -s --max-time 5 -X POST "$MURL/printer/gcode/script?script=M140%20S${BED}" >/dev/null 2>&1
    i=0
    while [ "$i" -lt 600 ]; do
        bed_sample heat "$i"
        R=$(bed_read) || break
        CT=$(echo "$R" | cut -d' ' -f1)
        KS=$(bed_klippy)
        if [ "$KS" != ready ]; then
            bad "klippy went to '$KS' during the ramp: this is the failure being hunted, see klippy.log"
            break
        fi
        awk -v t="$CT" -v g="$BED" 'BEGIN{exit !(t >= g - 0.5)}' && break
        sleep 1
        i=$((i + 1))
    done

    note "phase 3: 60s hold, capturing pwm on/off transitions"
    i=0
    while [ "$i" -lt 60 ]; do
        bed_sample hold "$i"
        sleep 1
        i=$((i + 1))
    done

    note "phase 4: bed off, 10s settle, 20s baseline"
    bed_off
    sleep 10
    i=0
    while [ "$i" -lt 20 ]; do
        bed_sample post "$i"
        sleep 1
        i=$((i + 1))
    done

    kv "samples" "$(wc -l <"$BED_LOG") in $BED_LOG"

    # The verdict is gated on 3 sigma of the measured baseline noise, so ADC jitter cannot masquerade as coupling.
    awk -F'\t' '
    {
        if ($1 == "base" || $1 == "post") { n++; s += $5; ss += $5 * $5; if (bmin == 0 || $5 < bmin) bmin = $5 }
        if ($3 >= 0.8) { hn++; hs += $5 }
        if ($3 > maxduty) maxduty = $3
        if ($5 > 0 && (vmin == 0 || $5 < vmin)) vmin = $5
        if ($6 != "0x0" && $6 != "NA") thr = $6
        cn++; cx += $3; cy += $5; cxy += $3 * $5; cxx += $3 * $3; cyy += $5 * $5
    }
    END {
        if (n < 10) { printf "  inconclusive: only %d baseline samples\n", n; exit }
        mean = s / n
        var = ss / n - mean * mean
        sd = (var > 0) ? sqrt(var) : 0
        printf "  %-28s %.4f V (sd %.4f V, min %.3f V)\n", "baseline 5V", mean, sd, bmin
        printf "  %-28s %.2f\n", "peak bed duty", maxduty
        if (hn < 5) {
            printf "  %-28s %s\n", "verdict", "INCONCLUSIVE: bed never held >=80% duty for 5s"
            exit
        }
        hm = hs / hn
        d = mean - hm
        printf "  %-28s %.4f V over %d samples\n", "5V at >=80% duty", hm, hn
        printf "  %-28s %.1f mV\n", "shift under load", d * 1000
        den = sqrt((cxx - cx * cx / cn) * (cyy - cy * cy / cn))
        if (den > 0) printf "  %-28s %.3f\n", "corr(bed duty, 5V)", (cxy - cx * cy / cn) / den
        printf "  %-28s %.3f V\n", "lowest 5V sample", vmin
        thr3 = 3 * sd
        printf "  %-28s %.1f mV\n", "3-sigma noise floor", thr3 * 1000
        if (thr != "") { printf "  VERDICT BAD: throttled bits set during the test (%s)\n", thr; exit }
        if (vmin < 4.80) { printf "  VERDICT BAD: 5V dropped to %.3f V, below the 4.80 V margin\n", vmin; exit }
        if (d < thr3) { print  "  VERDICT OK: no shift above the measured noise floor, rails look independent"; exit }
        if (d < 0.050) { printf "  VERDICT WARN: %.1f mV shift is real but small: watch it in a closed chassis\n", d * 1000; exit }
        printf "  VERDICT BAD: %.1f mV shift tracks bed duty, the 5V supply is coupled to the 24V domain\n", d * 1000
        print  "  this is a hardware fix: bigger DC-DC, thicker/shorter 5V leads, or bulk capacitance at the Pi"
    }' "$BED_LOG"

    note "a negative result here does not clear the 24V domain: the Pi cannot see 24V rail sag at all"
fi

echo
