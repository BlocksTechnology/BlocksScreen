#!/bin/bash
# Ensure an X authority cookie exists before the xorg session starts.
#
# Bare `xinit` never writes the cookie `-auth $XAUTH` expects, so regenerate it like `startx` does; always exits 0 so a prereq failure never masks X.Org's own error.
# Non-empty isn't enough: the local-socket entry is keyed on hostname, and a rename after the file was written leaves a cookie nothing matches, so X rejects every connection forever.
#
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
# SPDX-License-Identifier: AGPL-3.0-or-later

set -u
umask 077

_XAUTH="${1:-${XAUTHORITY:-$HOME/.Xauthority}}"
_host="$(hostname)"

[ -s "$_XAUTH" ] && xauth -f "$_XAUTH" list "${_host}/unix:0" 2>/dev/null \
    | grep -q . && exit 0

_cookie="$(mcookie 2>/dev/null)"
[ -z "$_cookie" ] && exit 0

: > "$_XAUTH" 2>/dev/null || exit 0
xauth -f "$_XAUTH" add :0 . "$_cookie" 2>/dev/null || true
xauth -f "$_XAUTH" add "${_host}/unix:0" . "$_cookie" 2>/dev/null || true
exit 0
