#!/bin/bash
# Provision/update Spoolman: run-from-source (not pip-installable), so deps go in
# via uv (provided in the BlocksScreen venv by install-updater.sh). SQLite default
# means no sudo here; the unit is laid down + enabled by install-updater/updater.
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

# Spoolman won't start without client/dist (a clone has no prebuilt UI); the API
# is all we need, so a stub satisfies the mount without an npm build.
mkdir -p client/dist
if [ ! -f client/dist/index.html ]; then
    printf '<!doctype html><title>Spoolman</title>\n' >client/dist/index.html
fi

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
fi
echo "[hook:Spoolman] done"
