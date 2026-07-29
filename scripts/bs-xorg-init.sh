#!/bin/bash
# X.Org permanent-session init: runs as xinit client, keeps X alive indefinitely.
# Display setup is done once here; BlocksScreen.service attaches separately via DISPLAY=:0.
#
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
# SPDX-License-Identifier: AGPL-3.0-or-later

xsetroot -solid '#141414' 2>/dev/null || true

# 1×1 blank XBM - hides the X11 root-window cursor (Pi 5 SWcursor honours this)
printf '%s\n' \
    '#define bs_blank_width 1' \
    '#define bs_blank_height 1' \
    'static unsigned char bs_blank_bits[] = { 0x00 };' \
    > /tmp/bs-blank.xbm 2>/dev/null || true
xsetroot -cursor /tmp/bs-blank.xbm /tmp/bs-blank.xbm 2>/dev/null || true

# Force correct display mode (belt to 97-bs-resolution.conf's suspenders:
# EDID can fail on Pi 5, leaving X at a lower resolution that KMS upscales)
_out=$(xrandr 2>/dev/null | awk '/ connected/{print $1; exit}')
_mode=$(xrandr 2>/dev/null | awk '/ connected/{f=1;next} f && /^[[:space:]]+[0-9]+x[0-9]+/{print $1; exit}')
[ -n "$_out" ] && [ -n "$_mode" ] && xrandr --output "$_out" --mode "$_mode" 2>/dev/null || true

# Hold X alive indefinitely - BlocksScreen Qt process connects via DISPLAY=:0
exec sleep infinity
