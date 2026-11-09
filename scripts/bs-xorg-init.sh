#!/bin/bash
# xinit client: one-time display setup, then holds X alive for BlocksScreen.service (DISPLAY=:0).
#
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
# SPDX-License-Identifier: AGPL-3.0-or-later

# Root shows the splash for X's lifetime, so no gap between UI windows is ever blank.
feh --no-fehbg --bg-fill "$HOME/.cache/blockscreen/splash.png" 2>/dev/null \
    || xsetroot -solid '#141414' 2>/dev/null || true

# 1×1 blank XBM - hides the X11 root-window cursor (Pi 5 SWcursor honours this)
printf '%s\n' \
    '#define bs_blank_width 1' \
    '#define bs_blank_height 1' \
    'static unsigned char bs_blank_bits[] = { 0x00 };' \
    > /tmp/bs-blank.xbm 2>/dev/null || true
xsetroot -cursor /tmp/bs-blank.xbm /tmp/bs-blank.xbm 2>/dev/null || true

# Backs up 97-bs-resolution.conf: Pi 5 EDID can fail, leaving a low mode that KMS upscales.
_out=$(xrandr 2>/dev/null | awk '/ connected/{print $1; exit}')
_mode=$(xrandr 2>/dev/null | awk '/ connected/{f=1;next} f && /^[[:space:]]+[0-9]+x[0-9]+/{print $1; exit}')
[ -n "$_out" ] && [ -n "$_mode" ] && xrandr --output "$_out" --mode "$_mode" 2>/dev/null || true

exec sleep infinity
