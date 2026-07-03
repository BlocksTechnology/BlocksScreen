#!/bin/bash
# Ensure an X authority cookie exists before the xorg session starts.
#
# Bare `xinit` (unlike `startx`) never generates the cookie that
# `-auth $XAUTH` expects, so a machine migrating from the old single-service
# topology has no ~/.Xauthority and X.Org crash-loops on "Failed to open
# authorization file". Regenerate it as `startx` does. An empty file fails
# like a missing one, hence `-s`. Always exits 0 so a prereq failure never
# masks X.Org's own error.
#
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
# SPDX-License-Identifier: AGPL-3.0-or-later

set -u
umask 077

_XAUTH="${1:-${XAUTHORITY:-$HOME/.Xauthority}}"

[ -s "$_XAUTH" ] && exit 0

_cookie="$(mcookie 2>/dev/null)"
[ -z "$_cookie" ] && exit 0

: > "$_XAUTH" 2>/dev/null || exit 0
xauth -f "$_XAUTH" add :0 . "$_cookie" 2>/dev/null || true
xauth -f "$_XAUTH" add "$(hostname)/unix:0" . "$_cookie" 2>/dev/null || true
exit 0
