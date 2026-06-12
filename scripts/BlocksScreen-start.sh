#!/bin/bash

# BlocksScreen start script
#
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
#
# Based on the work :
# https://github.com/KlipperScreen/KlipperScreen/blob/master/scripts/KlipperScreen-start.sh
# Copyright (C) KlipperScreen contributors
#
# This file is part of BlocksScreen.
#
# BlocksScreen is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlocksScreen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BlocksScreen. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

XDG_RUNTIME_DIR=/run/user/$(id -u)
export XDG_RUNTIME_DIR

SCRIPT_PATH=$(dirname $(realpath $0))
BS_PATH=$(dirname "$SCRIPT_PATH")
_BSENV_HOME=$(getent passwd "$(id -un)" | cut -d: -f6)
BSENV="${BLOCKSSCREEN_VENV:-${_BSENV_HOME}/.BlocksScreen-env}"

# Switch to tty8 immediately so tty1 is hidden during startup (even before splash-holder is installed)
sudo chvt 8 2>/dev/null || true
printf '\033[2J\033[H\033[?25l  BlocksScreen loading...\n' > /dev/tty8 2>/dev/null || true

if ! "$BSENV/bin/python3.11" -c "import yaml" 2>/dev/null; then
    "$BSENV/bin/pip" install --quiet "PyYAML==6.0.1" >>/tmp/bs-pip.log 2>&1 || true
fi
# libsystemd-dev must be present before any pip sdbus source build, regardless of
# whether sdbus is already importable — the requirements install forces --no-binary sdbus.
if ! dpkg -s libsystemd-dev >/dev/null 2>&1; then
    sudo apt-get install -y --quiet libsystemd-dev python3-dev 2>/dev/null || true
fi
if ! command -v feh >/dev/null 2>&1; then
    sudo apt-get install -y --quiet feh 2>/dev/null || true
fi
if ! command -v xsetroot >/dev/null 2>&1; then
    sudo apt-get install -y --quiet x11-xserver-utils 2>/dev/null || true
fi
# On Pi 5 vc4 modesetting, hardware cursor planes ignore -nocursor.
# SWcursor routes cursor through X11 software path so -nocursor and
# xsetroot can actually suppress it.
_XORG_KIOSK="/etc/X11/xorg.conf.d/99-bs-kiosk.conf"
if [ ! -f "$_XORG_KIOSK" ]; then
    sudo mkdir -p "/etc/X11/xorg.conf.d" 2>/dev/null || true
    printf '%s\n' \
        'Section "Device"' \
        '    Identifier "modesetting"' \
        '    Driver "modesetting"' \
        '    Option "SWcursor" "true"' \
        'EndSection' \
        | sudo tee "$_XORG_KIOSK" >/dev/null 2>/dev/null || true
fi
# Force X.Org to use the native fb0 resolution.
# On Pi 5, EDID can fail so xrandr --auto finds no preferred mode and
# X.Org stays at a lower resolution; KMS then upscales, making the
# splash logo appear zoomed.  Writing a Screen section with the fb0
# resolution makes X.Org select the correct mode at startup.
_FB_SIZE=$(cat /sys/class/graphics/fb0/virtual_size 2>/dev/null || true)
_FB_W=${_FB_SIZE%,*}
_FB_H=${_FB_SIZE#*,}
_XORG_RES="/etc/X11/xorg.conf.d/97-bs-resolution.conf"
if [ -n "$_FB_W" ] && [ -n "$_FB_H" ] && [ "$_FB_W" -gt 0 ] 2>/dev/null; then
    _XORG_RES_WANT=$(printf 'Section "Screen"\n    Identifier "Screen0"\n    DefaultDepth 24\n    SubSection "Display"\n        Depth 24\n        Modes "%s"\n    EndSubSection\nEndSection\n' "${_FB_W}x${_FB_H}")
    _XORG_RES_HAVE=$(cat "$_XORG_RES" 2>/dev/null || true)
    if [ "$_XORG_RES_HAVE" != "$_XORG_RES_WANT" ]; then
        sudo mkdir -p "/etc/X11/xorg.conf.d" 2>/dev/null || true
        printf '%s' "$_XORG_RES_WANT" | sudo tee "$_XORG_RES" >/dev/null 2>/dev/null || true
    fi
fi
if ! "$BSENV/bin/python3.11" -c "import sdbus" 2>/dev/null; then
    "$BSENV/bin/pip" install --quiet --force-reinstall --no-binary sdbus,sdbus-networkmanager \
        "sdbus==0.12.0" "sdbus-networkmanager==2.0.0" >>/tmp/bs-pip.log 2>&1 || true
fi
REQS_HASH=$(md5sum "$BS_PATH/scripts/requirements.txt" | cut -d' ' -f1)
SENTINEL="$BSENV/.blockscreen-reqs-hash"
if [ ! -f "$SENTINEL" ] || [ "$(cat "$SENTINEL")" != "$REQS_HASH" ]; then
    if "$BSENV/bin/pip" install --quiet \
        --only-binary :all: \
        --no-binary sdbus,sdbus-networkmanager \
        --upgrade-strategy=only-if-needed \
        -r "$BS_PATH/scripts/requirements.txt"; then
        echo "$REQS_HASH" >"$SENTINEL"
    fi
fi

git -C "$BS_PATH" config core.hooksPath scripts 2>/dev/null || true

# ── Moonraker config migration (idempotent) ──────────────────────────────────
_MOONRAKER_CONF="$_BSENV_HOME/printer_data/config/moonraker.conf"
if [ -f "$_MOONRAKER_CONF" ]; then
    cp "$_MOONRAKER_CONF" "${_MOONRAKER_CONF}.bak" 2>/dev/null || true
    _mr_patched=false
    if ! grep -q "enable_system_updates" "$_MOONRAKER_CONF"; then
        sed -i '/^\[update_manager\]$/a enable_system_updates: False' "$_MOONRAKER_CONF"
        _mr_patched=true
        echo "[BlocksScreen-start] moonraker.conf: disabled system apt upgrades"
    fi
    if grep -q "managed_services: klipper moonraker" "$_MOONRAKER_CONF"; then
        sed -i '/^\[update_manager BlocksScreen\]/,/^\[/ s/managed_services: klipper moonraker/managed_services: BlocksScreen/' "$_MOONRAKER_CONF"
        _mr_patched=true
        echo "[BlocksScreen-start] moonraker.conf: fixed BlocksScreen managed_services"
    fi
    if $_mr_patched; then
        sudo systemctl restart moonraker.service 2>/dev/null || true
    fi
fi
# ─────────────────────────────────────────────────────────────────────────────

# Remove stale git index lock left by an interrupted update (e.g. power loss during git reset)
rm -f "$BS_PATH/.git/index.lock"

# Recover from corrupt loose objects (empty files written by an interrupted git fetch/reset).
# git cat-file -e HEAD fails when the commit object is missing/empty; symbolic-ref still works
# because .git/HEAD is a plain-text ref file, not a commit object.
_bs_branch=$(git -C "$BS_PATH" symbolic-ref --short HEAD 2>/dev/null || echo "")
if ! git -C "$BS_PATH" cat-file -e HEAD 2>/dev/null; then
    echo "BlocksScreen: corrupt git objects detected — pruning empty objects and re-fetching"
    find "$BS_PATH/.git/objects" -type f -empty -delete 2>/dev/null || true
    if [ -n "$_bs_branch" ]; then
        git -C "$BS_PATH" fetch origin "$_bs_branch" 2>/dev/null || true
        git -C "$BS_PATH" reset --hard "origin/$_bs_branch" 2>/dev/null || true
    fi
fi

# ── Crash-loop auto-rollback (last_good_commit only — see migration note) ──
# A bad update can pass compileall yet crash at runtime. The app records
# last_good_commit + zeroes boot_attempts ~5s after a stable start. Here we
# count each boot; after N failures with HEAD != last_good, revert to it.
# No prev_hash fallback: it could revert across the dev->update-manager
# migration boundary and leave a half-swapped service topology.
_BOOT_DIR="$_BSENV_HOME/.cache/blockscreen"
_MAX_BOOT_ATTEMPTS=3
mkdir -p "$_BOOT_DIR" 2>/dev/null || true
_attempts=$(cat "$_BOOT_DIR/boot_attempts" 2>/dev/null || echo 0)
case "$_attempts" in ''|*[!0-9]*) _attempts=0 ;; esac
_attempts=$((_attempts + 1))
printf '%s\n' "$_attempts" > "$_BOOT_DIR/.boot_attempts.tmp" 2>/dev/null \
    && mv -f "$_BOOT_DIR/.boot_attempts.tmp" "$_BOOT_DIR/boot_attempts" 2>/dev/null || true
echo "[BlocksScreen-start] boot attempt $_attempts"
_last_good=$(tr -d '[:space:]' < "$_BOOT_DIR/last_good_commit" 2>/dev/null || echo "")
_cur_head=$(git -C "$BS_PATH" rev-parse HEAD 2>/dev/null || echo "")
if [ "$_attempts" -ge "$_MAX_BOOT_ATTEMPTS" ] && [ -n "$_last_good" ] \
   && [ -n "$_cur_head" ] && [ "$_last_good" != "$_cur_head" ]; then
    echo "BlocksScreen: crash loop ($_attempts boots) — rolling back to ${_last_good:0:8}"
    if git -C "$BS_PATH" reset --hard "$_last_good" 2>/dev/null; then
        rm -f "$BSENV/.blockscreen-reqs-hash"
        printf '0\n' > "$_BOOT_DIR/boot_attempts" 2>/dev/null || true
    fi
fi
# ─────────────────────────────────────────────────────────────────────────

# If any source file fails to compile the working tree is corrupt (partial file write).
# Hard-reset to HEAD to restore all tracked files to the last known-good commit.
if ! "$BSENV/bin/python3.11" -m compileall -q \
      "$BS_PATH/BlocksScreen" "$BS_PATH/updater" 2>/dev/null; then
    echo "BlocksScreen: source check failed — running git reset --hard HEAD to recover"
    git -C "$BS_PATH" reset --hard HEAD 2>/dev/null || true
fi

if [ ! -f /etc/systemd/system/BlocksScreen-updater.service ]; then
    sudo bash "$SCRIPT_PATH/install-updater.sh"
fi

# Bootstrap splash-holder service on first install only.
# Post-merge handles updates when scripts/BlocksScreen-splash-holder.service changes.
_HOLDER_SRC="$SCRIPT_PATH/BlocksScreen-splash-holder.service"
_HOLDER_DST="/etc/systemd/system/BlocksScreen-splash-holder.service"
if [ ! -f "$_HOLDER_DST" ]; then
    sudo cp "$_HOLDER_SRC" "$_HOLDER_DST" || true
    sudo systemctl daemon-reload || true
    sudo systemctl enable BlocksScreen-splash-holder.service 2>/dev/null || true
fi
if ! systemctl is-active --quiet BlocksScreen-splash-holder.service; then
    sudo systemctl start --no-block BlocksScreen-splash-holder.service || true
fi

# Keep service files in sync with repo copies so Wants/After stay current after git updates.
_BS_SVC_SRC="$SCRIPT_PATH/BlocksScreen.service"
_BS_SVC_DST="/etc/systemd/system/BlocksScreen.service"
_XORG_SVC_SRC="$SCRIPT_PATH/BlocksScreen-xorg.service"
_XORG_SVC_DST="/etc/systemd/system/BlocksScreen-xorg.service"
_HOLDER_SVC_SRC="$SCRIPT_PATH/BlocksScreen-splash-holder.service"
_HOLDER_SVC_DST="/etc/systemd/system/BlocksScreen-splash-holder.service"
_need_reload=false
if ! diff -q "$_BS_SVC_DST" "$_BS_SVC_SRC" >/dev/null 2>&1; then
    sudo cp "$_BS_SVC_SRC" "$_BS_SVC_DST" || true
    _need_reload=true
fi
if [ -f "$_XORG_SVC_SRC" ] && ! diff -q "$_XORG_SVC_DST" "$_XORG_SVC_SRC" >/dev/null 2>&1; then
    sudo cp "$_XORG_SVC_SRC" "$_XORG_SVC_DST" || true
    _need_reload=true
fi
if [ -f "$_HOLDER_SVC_SRC" ] && ! diff -q "$_HOLDER_SVC_DST" "$_HOLDER_SVC_SRC" >/dev/null 2>&1; then
    sudo cp "$_HOLDER_SVC_SRC" "$_HOLDER_SVC_DST" || true
    # reenable to update WantedBy symlink (e.g. multi-user.target → sysinit.target)
    sudo systemctl reenable BlocksScreen-splash-holder.service 2>/dev/null || true
    _need_reload=true
fi
$_need_reload && { sudo systemctl daemon-reload || true; }

if [ -f $SCRIPT_PATH/launch_BlocksScreen.sh ]; then
    echo "Running $SCRIPT_PATH/launch_BlocksScreen.sh"
    $SCRIPT_PATH/launch_BlocksScreen.sh
    exit $?
fi

_XCLIENT="${BSENV}/bin/python3.11 ${BS_PATH}/BlocksScreen/BlocksScreen.py"

# Bootstrap BlocksScreen-xorg.service (X.Org permanent session).
# The sync block above may have already copied the file; enable independently.
if [ -f "$_XORG_SVC_DST" ]; then
    if ! systemctl is-enabled --quiet BlocksScreen-xorg.service 2>/dev/null; then
        sudo systemctl enable BlocksScreen-xorg.service 2>/dev/null || true
    fi
    if ! systemctl is-active --quiet BlocksScreen-xorg.service; then
        sudo systemctl start --no-block BlocksScreen-xorg.service || true
    fi
fi

if [[ "${BS_BACKEND:-X}" =~ ^[wW]$ ]]; then
    echo "Running BlocksScreen on Cage"
    timeout 3 /usr/bin/plymouth quit 2>/dev/null || true
    pkill -x plymouthd 2>/dev/null || true
    exec /usr/bin/cage -ds $_XCLIENT
else
    echo "Running BlocksScreen on X (DISPLAY=:0)"
    # Wait for X.Org socket — up to 15 s on first boot, instant on Qt restart
    for _i in $(seq 1 30); do
        [ -S /tmp/.X11-unix/X0 ] && break
        sleep 0.5
    done
    # Fallback: xorg service not yet installed (e.g. power cut mid-update before hook ran).
    # Start X inline so the machine stays functional; next successful update installs the
    # permanent service and eliminates this path.
    if [ ! -S /tmp/.X11-unix/X0 ] && \
       ! systemctl is-active --quiet BlocksScreen-xorg.service 2>/dev/null; then
        echo "X.Org service not active — starting X inline (transitional)" >&2
        exec /usr/bin/xinit "$_XCLIENT" -- :0 vt7 -keeptty -novtswitch -nocursor \
            -auth /home/blocks/.Xauthority
    fi
    sudo chvt 7 2>/dev/null || true
    exec $_XCLIENT
fi
