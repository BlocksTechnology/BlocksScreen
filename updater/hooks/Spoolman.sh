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

# Spoolman needs a built client dir to start; stub both old (client/dist) and new (client_v2/build) layouts since we only need the API, not an npm build.
for _client_dir in client/dist client_v2/build; do
    mkdir -p "$_client_dir"
    if [ ! -f "$_client_dir/index.html" ]; then
        printf '<!doctype html><title>Spoolman</title>\n' >"$_client_dir/index.html"
    fi
done

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
fi

if ! systemctl is-active --quiet Spoolman.service 2>/dev/null; then
    echo "[hook:Spoolman] enabling and starting Spoolman.service"
    sudo systemctl enable --now Spoolman.service 2>/dev/null || {
        echo "[hook:Spoolman] WARN: could not enable/start Spoolman.service - continuing"
    }
fi

# Moonraker gives up on a dead Spoolman at startup, so let the API answer before restarting it.
for _i in $(seq 30); do
    curl -sf -m 2 http://localhost:7912/api/v1/health 2>/dev/null | grep -q healthy && break
    [ "$_i" -eq 30 ] && echo "[hook:Spoolman] WARN: API still unhealthy after 30s - moonraker may not connect"
    sleep 1
done

# The venv only exists as of this hook, so patch moonraker here: any earlier caller saw no venv and skipped.
_home=$(dirname "$COMPONENT_PATH")
_conf="$_home/printer_data/config/moonraker.conf"
_common="${BS_DIR:-$_home/BlocksScreen}/scripts/bs-common.sh"
if [ -r "$_common" ] && [ -f "$_conf" ]; then
    # shellcheck source=/dev/null
    . "$_common"
    if bs_ensure_spoolman_moonraker "$_conf" "hook:Spoolman"; then
        sudo systemctl restart moonraker.service 2>/dev/null || true
    fi
fi
echo "[hook:Spoolman] done"
