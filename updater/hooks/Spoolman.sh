#!/bin/bash
# Provision Spoolman via uv (run-from-source, not pip-installable); SQLite default = no sudo; unit installed by install-updater.
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

# Stub client/dist (a clone has no prebuilt UI); the API is all we need, no npm build.
mkdir -p client/dist
if [ ! -f client/dist/index.html ]; then
    printf '<!doctype html><title>Spoolman</title>\n' >client/dist/index.html
fi

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
fi

if ! systemctl is-active --quiet Spoolman.service 2>/dev/null; then
    echo "[hook:Spoolman] enabling and starting Spoolman.service"
    sudo systemctl enable --now Spoolman.service 2>/dev/null || {
        echo "[hook:Spoolman] WARN: could not enable/start Spoolman.service - continuing"
    }
fi
echo "[hook:Spoolman] done"
