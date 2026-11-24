#!/bin/bash
# Shared helpers sourced by BlocksScreen-start.sh, bs-bootstrap.sh and post-merge. Definitions
# only, no side effects. Callers run as `blocks` (NOPASSWD sudo on deployment).

# Idempotently patch moonraker.conf. $1 = conf path, $2 = log tag, $3 = defer (sets BS_MOONRAKER_RESTART_OWED).
bs_migrate_moonraker_conf() {
    local conf="$1" tag="${2:-bs-common}" patched=false
    [ -f "$conf" ] || return 0
    if bs_heal_moonraker_conf "$conf" "$tag"; then
        patched=true
    fi
    # Patching a torn conf would bury the damage under a fresh marker.
    bs_moonraker_conf_torn "$conf" && return 0
    # Back up only a conf that parses: never overwrite a good .bak with a corrupt one.
    if bs_moonraker_conf_sane "$conf" && ! cmp -s "$conf" "${conf}.bak"; then
        local bak_tmp
        bak_tmp="$(mktemp -p "$(dirname "$conf")" .moonraker.conf.XXXXXX)" || bak_tmp=""
        if [ -n "$bak_tmp" ] && ! { cp "$conf" "$bak_tmp" && _bs_replace_file "$bak_tmp" "${conf}.bak"; }; then
            rm -f "$bak_tmp"
        fi
    fi
    # Gate on the section existing: else the sed no-ops but patched=true restarts moonraker every boot.
    if ! grep -q "enable_system_updates" "$conf" && grep -q '^\[update_manager\]$' "$conf"; then
        _bs_conf_sed "$conf" '/^\[update_manager\]$/a enable_system_updates: False'
        patched=true
        echo "[$tag] moonraker.conf: disabled system apt upgrades"
    fi
    # Scope checks to the BlocksScreen section so an unrelated match can't re-patch every boot.
    local bs_um_section
    bs_um_section=$(sed -n '/^\[update_manager BlocksScreen\]/,/^\[/p' "$conf" 2>/dev/null)
    if printf '%s\n' "$bs_um_section" | grep -q "managed_services: klipper moonraker"; then
        _bs_conf_sed "$conf" '/^\[update_manager BlocksScreen\]/,/^\[/ s/managed_services: klipper moonraker/managed_services: BlocksScreen/'
        patched=true
        echo "[$tag] moonraker.conf: fixed BlocksScreen managed_services"
    fi
    # Old installers wrote primary_branch: master, which does not exist upstream;
    # moonraker refuses to manage a repo whose primary branch is gone.
    if printf '%s\n' "$bs_um_section" | grep -q "^primary_branch: master$"; then
        _bs_conf_sed "$conf" '/^\[update_manager BlocksScreen\]/,/^\[/ s/^primary_branch: master$/primary_branch: main/'
        patched=true
        echo "[$tag] moonraker.conf: fixed BlocksScreen primary_branch (master -> main)"
    fi
    if bs_disable_overlapping_update_managers "$conf" "$tag"; then
        patched=true
    fi
    if bs_ensure_spoolman_moonraker "$conf" "$tag"; then
        patched=true
    fi
    # Moonraker only reads the allowlist at startup, so reuse the restart this function already decides on.
    if bs_ensure_asvc "${conf%/config/moonraker.conf}/moonraker.asvc" "$tag"; then
        patched=true
    fi
    if [ "${3:-}" = defer ]; then
        # shellcheck disable=SC2034  # read by the caller
        BS_MOONRAKER_RESTART_OWED=$patched
    else
        $patched && sudo systemctl restart moonraker.service 2>/dev/null || true
    fi
    return 0
}

# Durable replace keeping mode and owner like `sed -i`: fsync the temp, rename it over $2, fsync the dir. A power cut keeps old or new, never NULs.
_bs_replace_file() {
    chmod --reference="$2" "$1" 2>/dev/null || true
    chown --reference="$2" "$1" 2>/dev/null || true
    sync "$1" && mv -f "$1" "$2" && sync "$(dirname "$2")" && return 0
    rm -f "$1"
    return 1
}

# Durable `sed -i` (which renames without fsync). $1 = file, $2 = sed script.
_bs_conf_sed() {
    local tmp
    tmp="$(mktemp -p "$(dirname "$1")" ".$(basename "$1").XXXXXX")" || return 1
    if sed "$2" "$1" >"$tmp"; then
        _bs_replace_file "$tmp" "$1"
    else
        rm -f "$tmp"
        return 1
    fi
}

# True for the power-cut signature: empty, or data blocks lost behind a kept size (NUL bytes). $1 = file.
bs_moonraker_conf_torn() {
    [ -s "$1" ] || return 0
    [ "$(tr -d '\000' <"$1" | wc -c)" != "$(wc -c <"$1")" ]
}

# True when $1 can serve as moonraker.conf: not torn, parses like Moonraker (configparser, no interpolation, includes followed), has [server].
bs_moonraker_conf_sane() {
    [ -s "$1" ] && ! bs_moonraker_conf_torn "$1" || return 1
    python3 - "$1" 2>/dev/null <<'PY'
import configparser
import pathlib
import sys


def sections(path: pathlib.Path, seen: set[pathlib.Path]) -> set[str]:
    # Include rules follow Moonraker's confighelper._parse_file.
    if path.resolve() in seen:
        raise configparser.Error(f"recursive include {path}")
    seen.add(path.resolve())
    parser = configparser.ConfigParser(interpolation=None)
    with open(path, encoding="utf-8") as f:
        parser.read_file(f)
    found = set()
    for sec in parser.sections():
        if not sec.startswith("include "):
            found.add(sec)
            continue
        inc = sec[8:].strip()
        if inc.startswith("/"):
            target = pathlib.Path(inc).resolve()
            paths = sorted(target.parent.glob(target.name))
        else:
            paths = sorted(path.parent.glob(inc))
        if not paths:
            raise configparser.Error(f"no files match [{sec}]")
        for inc_path in paths:
            found |= sections(inc_path, seen)
    return found


try:
    ok = "server" in sections(pathlib.Path(sys.argv[1]), set())
except (OSError, UnicodeDecodeError, ValueError, configparser.Error):
    ok = False
sys.exit(0 if ok else 1)
PY
}

# Restore a torn moonraker.conf from the newest sane source: .bak, NULs stripped, Moonraker's .bkp. $1 conf, $2 tag.
bs_heal_moonraker_conf() {
    local conf="$1" tag="${2:-bs-common}" src tmp dropped
    [ -f "$conf" ] && bs_moonraker_conf_torn "$conf" || return 1
    cp -f "$conf" "$(dirname "$conf")/.$(basename "$conf").torn" 2>/dev/null || true
    tmp="$(mktemp -p "$(dirname "$conf")" .moonraker.conf.XXXXXX)" || return 1
    for src in "${conf}.bak" stripped "$(dirname "$conf")/.$(basename "$conf").bkp"; do
        if [ "$src" = stripped ]; then
            tr -d '\000' <"$conf" >"$tmp" || continue
        else
            cp -f "$src" "$tmp" 2>/dev/null || continue
        fi
        bs_moonraker_conf_sane "$tmp" || continue
        dropped=""
        [ "$src" = "${conf}.bak" ] && dropped=$(tr -d '\000' <"$conf" | diff "$tmp" - |
            awk -v p="[$tag] moonraker.conf: not in .bak, dropped: " '/^> .*[^[:space:]]/ { print p substr($0, 3); if (++n == 20) exit }')
        # Stop on a failed rename: every source would fail the same way.
        if ! _bs_replace_file "$tmp" "$conf"; then
            echo "[$tag] moonraker.conf: torn by a power cut, restore from $src failed"
            return 1
        fi
        echo "[$tag] moonraker.conf: torn by a power cut, restored from $src"
        [ -z "$dropped" ] || printf '%s\n' "$dropped"
        return 0
    done
    rm -f "$tmp"
    echo "[$tag] moonraker.conf: torn by a power cut, no sane copy to restore"
    return 1
}

# Point Moonraker at a locally-provisioned Spoolman so the UI's spoolman_proxy
# works. Idempotent; only acts when Spoolman is installed and [spoolman] is
# absent. Returns 0 only on change, so the caller restarts moonraker.
bs_ensure_spoolman_moonraker() {
    local conf="$1" tag="${2:-bs-common}"
    [ -f "$conf" ] || return 1
    local spoolman_dir="${conf%/printer_data/config/moonraker.conf}/Spoolman"
    [ -d "$spoolman_dir/.venv" ] || return 1
    grep -q '^\[spoolman\]' "$conf" && return 1
    # Same-dir temp + atomic rename: a power cut mid-append could truncate the conf.
    local tmp
    tmp="$(mktemp -p "$(dirname "$conf")" .moonraker.conf.XXXXXX)" || return 1
    if ! { cat "$conf" && printf '\n[spoolman]\nserver: localhost:7912\n'; } >"$tmp"; then
        rm -f "$tmp"
        return 1
    fi
    _bs_replace_file "$tmp" "$conf" || return 1
    echo "[$tag] moonraker.conf: added [spoolman] (server: localhost:7912)"
    return 0
}

# Append a line, restoring the missing final newline first, else the append lands on the previous line.
_bs_append_line() {
    local f="$1" line="$2"
    [ -s "$f" ] && [ -n "$(tail -c 1 "$f" 2>/dev/null)" ] && printf '\n' >>"$f"
    printf '%s\n' "$line" >>"$f"
}

# Moonraker refuses to restart units absent from moonraker.asvc, so old images break UI updates silently.
bs_ensure_asvc() {
    local asvc="$1" tag="${2:-bs-common}" changed=false
    # Moonraker seeds its default allowlist only when the file is absent; creating it here would drop those.
    [ -e "$asvc" ] || return 1
    [ -w "$asvc" ] || return 1
    # Pre-rename images called the unit BlocksPrinter; the entry now names a service that does not exist.
    if grep -qx 'BlocksPrinter' "$asvc" 2>/dev/null; then
        sed -i '/^BlocksPrinter$/d' "$asvc" 2>/dev/null && changed=true &&
            echo "[$tag] moonraker.asvc: dropped legacy BlocksPrinter entry"
    fi
    if ! grep -qx 'BlocksScreen' "$asvc" 2>/dev/null; then
        _bs_append_line "$asvc" BlocksScreen && changed=true &&
            echo "[$tag] moonraker.asvc: added BlocksScreen"
    fi
    $changed
}

# install.sh runs only at flash time, so re-assert the artifacts old images shipped wrong or not at all.
bs_ensure_install_state() {
    local bs_path="$1" bsenv="$2" tag="${3:-bs-common}" user home env_file logs k
    # post-merge runs under a root pull and sets _BSENV_USER: never derive /root.
    user="${_BSENV_USER:-$(id -un)}"
    home=$(getent passwd "$user" | cut -d: -f6)
    [ -n "$home" ] || return 0
    env_file="$home/.config/blockscreen/env"
    mkdir -p "$home/.config/blockscreen" 2>/dev/null || true
    # EnvironmentFile is optional (-) in the unit, so a missing env file degrades silently instead of failing.
    for k in "BS_DIR=$bs_path" "BSENV=$bsenv" "BS_BACKEND=${BS_BACKEND:-X}"; do
        grep -q "^${k%%=*}=" "$env_file" 2>/dev/null && continue
        _bs_append_line "$env_file" "$k" 2>/dev/null &&
            echo "[$tag] env: declared ${k%%=*}"
    done
    # A root-created dir would block the hook's deploy flag, which runs as the service user.
    if [ "$(id -u)" = 0 ]; then
        chown "$user" "$home/.config/blockscreen" "$env_file" 2>/dev/null || true
    fi
    logs="$bs_path/logs"
    # Without setgid, files the updater writes as root land root-owned and the UI cannot rotate them.
    if [ -d "$logs" ] && [ "$(stat -c %a "$logs" 2>/dev/null)" != "2775" ]; then
        # Images flashed before install.sh grew the groupadd have no blocksscreen group, so chown would no-op.
        sudo groupadd -f blocksscreen 2>/dev/null || true
        sudo chown blocks:blocksscreen "$logs" 2>/dev/null || true
        sudo chmod 2775 "$logs" 2>/dev/null &&
            echo "[$tag] logs: restored setgid 2775"
    fi
    return 0
}

# Pi 5 ports cap at 600mA combined vs the fleet's 824mA declared draw; not a proven fix for the RF50 MCU shutdowns (cause unknown), shipped because the oversubscription is real regardless, takes effect after reboot.
bs_ensure_usb_max_current() {
    local f="${1:-/boot/firmware/config.txt}" tag="${2:-bs-common}" mnt opts remounted=false
    [ -f "$f" ] || return 0
    if grep -qE '^[[:space:]]*usb_max_current_enable[[:space:]]*=[[:space:]]*1[[:space:]]*$' "$f" 2>/dev/null; then
        return 0
    fi
    mnt=$(findmnt -no TARGET --target "$f" 2>/dev/null) || mnt=""
    if [ -n "$mnt" ]; then
        opts=$(findmnt -no OPTIONS "$mnt" 2>/dev/null)
        case ",$opts," in
        *,ro,*)
            # ro without ro in fstab means the kernel remounted a damaged FAT (errors=remount-ro): never write to it.
            case ",$(findmnt --fstab -no OPTIONS "$mnt" 2>/dev/null)," in
            *,ro,*) ;;
            *)
                echo "[$tag] $mnt went read-only unexpectedly, usb_max_current_enable NOT applied"
                return 1
                ;;
            esac
            echo "[$tag] $mnt is mounted read-only, remounting rw to write usb_max_current_enable"
            sudo mount -o remount,rw "$mnt" 2>/dev/null || {
                echo "[$tag] remount rw of $mnt failed, usb_max_current_enable NOT applied"
                return 1
            }
            remounted=true
            ;;
        esac
    fi
    # [all] closes whatever conditional section ([pi4], [cm5], ...) is still open at EOF.
    printf '\n[all]\nusb_max_current_enable=1\n' | sudo tee -a "$f" >/dev/null 2>&1
    sync
    if $remounted; then
        sudo mount -o remount,ro "$mnt" 2>/dev/null ||
            echo "[$tag] WARN: could not restore $mnt to read-only"
    fi
    # tee's exit status isn't proof of a landed write (a prior field attempt silently no-op'd against a ro remount), so read the file back before trusting it.
    if ! grep -qE '^[[:space:]]*usb_max_current_enable[[:space:]]*=[[:space:]]*1[[:space:]]*$' "$f" 2>/dev/null; then
        echo "[$tag] write to $f did not land, usb_max_current_enable NOT applied"
        return 1
    fi
    echo "[$tag] usb_max_current_enable=1 written to $f, takes effect after reboot"
    return 0
}

# Mirrors updater.models.MIN_FREE_MB: below it a tree reset or pyc write can truncate files.
BS_MIN_FREE_MB=200

# Free MiB on the filesystem holding $1.
bs_free_mb() {
    df -Pm "$1" 2>/dev/null | awk 'NR == 2 { print $4 }'
}

# Drop re-downloadable caches (pip, uv, apt archives); user data is never touched. $1 = home.
bs_reclaim_disk() {
    rm -rf "$1/.cache/pip" "$1/.cache/uv" 2>/dev/null || true
    timeout 30 sudo -n /usr/local/sbin/bs-apt-helper clean >/dev/null 2>&1 || true
}

# Reclaim when short; true (0) while the disk is still below BS_MIN_FREE_MB. $1 = path, $2 = home.
bs_disk_low() {
    local before free
    before=$(bs_free_mb "$1")
    [ -n "$before" ] || return 1
    [ "$before" -ge "$BS_MIN_FREE_MB" ] && return 1
    bs_reclaim_disk "$2"
    free=$(bs_free_mb "$1")
    [ -n "$free" ] || return 1
    echo "BlocksScreen: reclaim freed $((free - before)) MB, $free MB free"
    [ "$free" -lt "$BS_MIN_FREE_MB" ]
}

# Delete __pycache__ under each arg: CPython keeps a truncated .pyc from a full disk forever.
bs_purge_pycache() {
    find "$@" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
}

# True while a live updater daemon runs its UI recovery ladder (fast_attempt > 0, not saturated). $1 = state file, $2 = python.
bs_selfheal_engaged() {
    local state="$1" py="$2"
    [ -f "$state" ] && [ -x "$py" ] || return 1
    [ -f "${state%/*}/selfheal_fault.json" ] && return 1
    systemctl is-active --quiet BlocksScreen-updater.service 2>/dev/null || return 1
    "$py" - "$state" 2>/dev/null <<'PY'
import json, sys
try:
    with open(sys.argv[1], encoding="utf-8") as f:
        comp = json.load(f).get("BlocksScreen")
except (OSError, ValueError, AttributeError):
    sys.exit(1)
n = comp.get("fast_attempt") if isinstance(comp, dict) else 0
sys.exit(0 if type(n) is int and n > 0 else 1)
PY
}

# True inside moonraker.service, where a Mainsail pull runs the hook. $1 = cgroup file (tests).
bs_in_moonraker_cgroup() {
    grep -q '/moonraker\.service$' "${1:-/proc/self/cgroup}" 2>/dev/null
}

# Files under scripts/ whose change owes an install-updater.sh run: the one list behind the stamp hash and post-merge's diff regex.
BS_UPDATER_INSTALL_TRIGGERS=(
    install-updater.sh bs-apt-helper.sh
    BlocksScreen-updater.service BlocksScreen-bootstrap.service
    BlocksScreen-clock.service BlocksScreen-clock.timer
    com.blockscreen.Updater.conf com.blockscreen.Updater.service
    requirements-pip.txt bs-tree-guard.sh BlocksScreen-tree-guard.service
)

# Hash of the install trigger files, stamped by install-updater.sh. $1 = scripts dir.
bs_updater_install_hash() {
    (cd "$1" 2>/dev/null && md5sum "${BS_UPDATER_INSTALL_TRIGGERS[@]}" 2>/dev/null) | md5sum | cut -d' ' -f1
}

# grep -E regex matching the `git diff --name-only` lines of the install trigger files.
bs_updater_install_trigger_regex() {
    local f out=""
    for f in "${BS_UPDATER_INSTALL_TRIGGERS[@]}"; do
        out+="${out:+|}^scripts/${f//./\\.}\$"
    done
    printf '%s\n' "$out"
}

# True while an update batch or the deploy unit may run install-updater.sh.
bs_updater_install_busy() {
    local f
    for f in /run/blockscreen/updater.lock "$_BSENV_HOME/.cache/blockscreen/updater.lock"; do
        [ -e "$f" ] && ! flock -n "$f" true 2>/dev/null && return 0
    done
    systemctl is-active --quiet BlocksScreen-deploy.service 2>/dev/null
}

# Twin of updater.__main__.code_hash: updater/*.py + components.yaml, C-sorted. $1 = BS_PATH.
bs_updater_code_hash() {
    local f
    printf '%s\n' "$1"/updater/*.py "$1/updater/components.yaml" | LC_ALL=C sort | while IFS= read -r f; do
        cat -- "$f" 2>/dev/null || true
    done | sha256sum | cut -d' ' -f1
}

# True when the daemon has run >2 min on code other than what is on disk. $1 = BS_PATH.
bs_updater_code_stale() {
    local f want since now
    since=$(systemctl show -p ActiveEnterTimestampMonotonic --value BlocksScreen-updater.service 2>/dev/null)
    now=$(cut -d. -f1 /proc/uptime 2>/dev/null)
    case "$since$now" in '' | *[!0-9]*) return 1 ;; esac
    # A fresh daemon may not have recorded its hash yet.
    [ "$since" -gt 0 ] && [ $((now - since / 1000000)) -ge 120 ] || return 1
    want=$(bs_updater_code_hash "$1")
    for f in /run/blockscreen/updater-code-hash "$_BSENV_HOME/.cache/blockscreen/updater-code-hash"; do
        [ "$(cat "$f" 2>/dev/null)" = "$want" ] && return 1
    done
    return 0
}

# Wait out a Moonraker update (capped, rc 1) or a print (uncapped); unreachable = idle. $1 conf, $2 cap s.
bs_wait_moonraker_idle() {
    local url status waited=0
    url="http://127.0.0.1:$(sed -n '/^\[server\]/,/^\[/ s/^port:[[:space:]]*\([0-9][0-9]*\).*/\1/p' "$1" 2>/dev/null | head -n1)"
    [ "$url" = "http://127.0.0.1:" ] && url="${url}7125"
    while :; do
        # A print or pause (even overnight) keeps bootstrap waiting here, holding its flock, on purpose.
        # Captured, not piped to grep -q: under pipefail curl's SIGPIPE reads as idle.
        status=$(curl -fsm 5 "$url/printer/objects/query?print_stats=state" 2>/dev/null) || status=""
        case "$status" in *'"state": "printing"'* | *'"state":"printing"'* | *'"state": "paused"'* | *'"state":"paused"'*)
            sleep 30
            continue
            ;;
        esac
        status=$(curl -fsm 5 "$url/machine/update/status" 2>/dev/null) || return 0
        case "$status" in *'"busy": true'* | *'"busy":true'*) ;; *) return 0 ;; esac
        [ "$waited" -ge "${2:-1800}" ] && return 1
        sleep 5
        waited=$((waited + 5))
    done
}

# Restart moonraker for a conf patch once idle. $1 conf, $2 owed flag, $3 cap s, $4 pre-patch PID.
bs_settle_moonraker_restart() {
    [ -e "$2" ] || return 0
    local pid="${4:-}"
    [ -n "$pid" ] || pid=$(systemctl show -p MainPID --value moonraker.service 2>/dev/null)
    if ! bs_wait_moonraker_idle "$1" "${3:-1800}"; then
        echo "[bs-common] moonraker still updating - restart stays owed to the next start"
        return 0
    fi
    # New PID = Moonraker already reloaded, e.g. at the end of Update All.
    if [ "$(systemctl show -p MainPID --value moonraker.service 2>/dev/null)" = "$pid" ]; then
        echo "[bs-common] restarting moonraker for the patched moonraker.conf"
        sudo systemctl restart moonraker.service 2>/dev/null || true
    fi
    rm -f "$2"
}

# Disable Moonraker management of repos the BlocksScreen daemon now owns, so a
# Mainsail "Update All" can't trip on them. Grep-gated marker so it runs once.
bs_disable_overlapping_update_managers() {
    local conf="$1" tag="${2:-bs-common}"
    # Bump the version whenever `owned` grows, else already-migrated boxes never pick it up.
    local mark="blocksscreen-single-owner-v2"
    [ -f "$conf" ] || return 1
    grep -q "$mark" "$conf" && return 1
    local owned="klipper RF50-Klipper happy-hare Klippain-ShakeTune mainsail-config crowsnest"
    local tmp
    # Same-dir temp + atomic rename: a power cut can never truncate moonraker.conf.
    tmp="$(mktemp -p "$(dirname "$conf")" .moonraker.conf.XXXXXX)" || return 1
    # The marker rides in the temp: an unsynced `>>` append left NULs in place of it (BUG-5).
    if { awk -v owned="$owned" '
        BEGIN { n = split(owned, a, " "); for (i = 1; i <= n; i++) own[a[i]] = 1 }
        # A commented header also closes the section, else re-runs double-comment it.
        /^#*\[/ {
            insec = 0
            if ($0 ~ /^\[update_manager [^]]+\]/) {
                name = $0; sub(/^\[update_manager /, "", name); sub(/\].*/, "", name)
                if (name in own) insec = 1
            }
        }
        { if (insec) print "#" $0; else print }
    ' "$conf" && printf '\n# %s applied by %s\n' "$mark" "$tag"; } > "$tmp"; then
        _bs_replace_file "$tmp" "$conf" || return 1
    else
        rm -f "$tmp"
        return 1
    fi
    echo "[$tag] moonraker.conf: disabled Moonraker management of daemon-owned repos"
}

# Sync repo unit files → /etc/systemd/system, reload on change, ensure X.Org is
# enabled+running. Idempotent. $1 = repo scripts dir, $2 = log tag.
bs_sync_service_files() {
    local src_dir="$1" tag="${2:-bs-common}" need_reload=false
    _bs_sync_one() {
        local src="$1" dst="$2"
        # An empty source is a torn checkout: installing it would disable the unit.
        [ -s "$src" ] || return 0
        if ! diff -q "$dst" "$src" >/dev/null 2>&1; then
            # Atomic install: a truncated BlocksScreen.service unit cannot self-heal.
            sudo cp "$src" "${dst}.new" && sudo mv -Tf "${dst}.new" "$dst" \
                && echo "[$tag] updated $(basename "$dst")" || true
            need_reload=true
        fi
    }
    # Never clobber the symlink install-updater.sh creates for BlocksScreen.service.
    [[ -L /etc/systemd/system/BlocksScreen.service ]] ||
        _bs_sync_one "$src_dir/BlocksScreen.service" /etc/systemd/system/BlocksScreen.service
    _bs_sync_one "$src_dir/BlocksScreen-xorg.service" /etc/systemd/system/BlocksScreen-xorg.service
    _bs_sync_one "$src_dir/BlocksScreen-splash-holder.service" /etc/systemd/system/BlocksScreen-splash-holder.service
    if $need_reload; then
        sudo systemctl daemon-reload || true
        # reenable to refresh the WantedBy symlink (e.g. multi-user → sysinit target)
        [ -f /etc/systemd/system/BlocksScreen-splash-holder.service ] &&
            sudo systemctl reenable BlocksScreen-splash-holder.service 2>/dev/null || true
    fi
    if [ -f /etc/systemd/system/BlocksScreen-xorg.service ]; then
        systemctl is-enabled --quiet BlocksScreen-xorg.service 2>/dev/null ||
            sudo systemctl enable BlocksScreen-xorg.service 2>/dev/null || true
        systemctl is-active --quiet BlocksScreen-xorg.service ||
            sudo systemctl start --no-block BlocksScreen-xorg.service 2>/dev/null || true
    fi
    return 0
}
