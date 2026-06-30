#!/bin/bash
# Provision/update Spoolman. Spoolman has a flat repo layout and is run from
# source (not pip-installable as a package), so its locked dependencies are
# installed with uv into an in-tree .venv, exactly as upstream's installer does.
# uv is provided in the BlocksScreen venv by install-updater.sh. SQLite default
# means no system packages, so this hook needs no sudo: the unit is laid down by
# install-updater.sh and enabled by the updater after a successful first start.
# BlocksScreen uses Spoolman's REST API via moonraker, so a backend-only install
# needs no web-client build.
set -euo pipefail

if [ -z "${COMPONENT_PATH:-}" ]; then
    echo "[hook:Spoolman] no COMPONENT_PATH"
    exit 1
fi

_uv="${BLOCKSSCREEN_VENV:-${HOME}/.BlocksScreen-env}/bin/uv"
if [ ! -x "$_uv" ]; then
    _uv=$(command -v uv || true)
fi
if [ -z "$_uv" ] || [ ! -x "$_uv" ]; then
    echo "[hook:Spoolman] uv not found - cannot provision (expected in BlocksScreen venv)"
    exit 1
fi

cd "$COMPONENT_PATH"
"$_uv" sync --no-dev

# Spoolman's app mounts client/dist with check_dir=True and refuses to start
# without it. A git clone has no prebuilt frontend (only the release zip does).
# BlocksScreen uses the REST API, so a placeholder satisfies the mount without an
# npm client build.
mkdir -p client/dist
if [ ! -f client/dist/index.html ]; then
    printf '<!doctype html><title>Spoolman</title>\n' >client/dist/index.html
fi

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
fi
echo "[hook:Spoolman] done"
