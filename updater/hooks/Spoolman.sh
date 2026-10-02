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

# Stub both old (client/dist) and new (client_v2/build) layouts; the API is all we need, no npm build.
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

# Fail before touching moonraker.conf: a failed install is rolled back, but the conf edit would not be.
_healthy=false
for _i in $(seq 60); do
    if curl -sf -m 2 http://localhost:7912/api/v1/health 2>/dev/null | grep -q healthy; then
        _healthy=true
        break
    fi
    sleep 2
done
if ! $_healthy; then
    echo "[hook:Spoolman] API unhealthy after 120s - failing so the install rolls back"
    exit 1
fi

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
