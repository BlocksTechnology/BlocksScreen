#!/bin/bash
set -euo pipefail

Red='\033[0;31m'
Green='\033[0;32m'
Blue='\033[0;34m'
Normal='\033[0m'

echo_info() { printf "${Blue}%s${Normal}\n" "$1"; }
echo_ok() { printf "${Green}%s${Normal}\n" "$1"; }
echo_error() { printf "${Red}%s${Normal}\n" "$1"; }

exec 200>/tmp/blockscreen-install-updater.lock
flock -x -w 30 200 || { echo_error "Another install-updater.sh is already running"; exit 1; }

SCRIPT_PATH=$(dirname -- "$(readlink -f -- "$0")")
BS_PATH=$(dirname "$SCRIPT_PATH")
# Service always runs as 'blocks'; derive home from that, not the caller's identity.
# Callers vary (sudo, post-merge hook, root shell) so SUDO_USER/$USER are unreliable.
_BSENV_USER="blocks"
_BSENV_HOME=$(getent passwd "$_BSENV_USER" | cut -d: -f6)
BSENV="${BLOCKSSCREEN_VENV:-${_BSENV_HOME}/.BlocksScreen-env}"

echo_info "Installing D-Bus policy ..."
sudo cp "$SCRIPT_PATH/com.blockscreen.Updater.conf" /etc/dbus-1/system.d/
sudo systemctl reload dbus || true
echo_ok "D-Bus policy installed"

echo_info "Installing D-Bus activation file ..."
sudo cp "$SCRIPT_PATH/com.blockscreen.Updater.service" /usr/share/dbus-1/system-services/
echo_ok "D-Bus activation file installed"

echo_info "Installing BlocksScreen-updater service ..."
SERVICE=$(cat "$SCRIPT_PATH/BlocksScreen-updater.service")
SERVICE=${SERVICE//BS_DIR/$BS_PATH}
SERVICE=${SERVICE//BSENV/$BSENV}
SERVICE=${SERVICE//BS_PRIMARY_HOME/$_BSENV_HOME}
echo "$SERVICE" | sudo tee /etc/systemd/system/BlocksScreen-updater.service >/dev/null
sudo systemctl daemon-reload
sudo systemctl enable BlocksScreen-updater.service
sudo systemctl restart BlocksScreen-updater.service || true
echo_ok "BlocksScreen-updater service installed and started"

echo_info "Installing sudoers rules for updater ..."
SUDOERS_FILE="/etc/sudoers.d/blockscreen-updater"
SUDOERS_TMP=$(mktemp)
printf 'blocks ALL=(ALL) NOPASSWD: /usr/bin/apt-get update\n' >>"$SUDOERS_TMP"
printf 'blocks ALL=(ALL) NOPASSWD: /usr/bin/apt-get install --only-upgrade -y *\n' >>"$SUDOERS_TMP"
printf 'blocks ALL=(ALL) NOPASSWD: /usr/bin/apt-get install -y --quiet *\n' >>"$SUDOERS_TMP"
printf 'blocks ALL=(ALL) NOPASSWD: /usr/bin/apt-get autoremove -y\n' >>"$SUDOERS_TMP"
printf 'blocks ALL=(ALL) NOPASSWD: /usr/bin/systemctl reboot\n' >>"$SUDOERS_TMP"
printf 'blocks ALL=(ALL) NOPASSWD: /usr/bin/chvt 7\n' >>"$SUDOERS_TMP"
printf 'blocks ALL=(ALL) NOPASSWD: /usr/bin/bash %s/scripts/install-updater.sh\n' "$BS_PATH" >>"$SUDOERS_TMP"
# Derive allowed restart targets from components.yaml instead of wildcard
_COMP_YAML="$BS_PATH/updater/components.yaml"
if [[ -f "$_COMP_YAML" ]]; then
    while IFS= read -r _svc; do
        printf 'blocks ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart %s\n' "$_svc" >>"$SUDOERS_TMP"
    done < <(grep '^\s*service:' "$_COMP_YAML" | awk '{print $2}' | sort -u)
else
    for _svc in klipper.service moonraker.service crowsnest.service KlipperScreen.service BlocksScreen.service; do
        printf 'blocks ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart %s\n' "$_svc" >>"$SUDOERS_TMP"
    done
fi
if sudo visudo -cf "$SUDOERS_TMP" >/dev/null 2>&1; then
    sudo install -m 0440 "$SUDOERS_TMP" "$SUDOERS_FILE"
    echo_ok "Sudoers rules installed"
else
    echo_error "Sudoers syntax check failed — skipping sudoers install"
fi
rm -f "$SUDOERS_TMP"

echo_info "Installing polkit rule for daemon-reload ..."
POLKIT_RULE='/etc/polkit-1/rules.d/10-blockscreen-reload.rules'
sudo tee "$POLKIT_RULE" >/dev/null <<'EOF'
polkit.addRule(function(action, subject) {
    if (action.id === "org.freedesktop.systemd1.reload-daemon" &&
        subject.isInGroup("blocksscreen")) {
        return polkit.Result.YES;
    }
});
EOF
sudo chmod 644 "$POLKIT_RULE"
echo_ok "Polkit rule installed"

echo_info "Converting BlocksScreen.service copy to symlink (enables sudo-free hook) ..."
_BS_SVC_SRC="$BS_PATH/scripts/BlocksScreen.service"
_BS_SVC_DEST="/etc/systemd/system/BlocksScreen.service"
if [[ -f "$_BS_SVC_DEST" && ! -L "$_BS_SVC_DEST" ]]; then
    sudo rm "$_BS_SVC_DEST"
fi
if [[ ! -L "$_BS_SVC_DEST" ]]; then
    sudo systemctl link "$_BS_SVC_SRC"
    sudo systemctl unmask BlocksScreen.service 2>/dev/null || true
fi
sudo systemctl daemon-reload
echo_ok "BlocksScreen.service is a symlink — hook no longer needs sudo cp"

echo_info "Setting up apt cache directory for blocks user ..."
sudo mkdir -p "$_BSENV_HOME/.cache/blockscreen"
sudo chown "$_BSENV_USER:blocksscreen" "$_BSENV_HOME/.cache"
sudo chmod 750 "$_BSENV_HOME/.cache"
sudo chown -R blocks:blocksscreen "$_BSENV_HOME/.cache/blockscreen"
sudo chmod 775 "$_BSENV_HOME/.cache/blockscreen"
echo_ok "Apt cache directory ready"

echo_info "Adding blocks to video group (required for framebuffer splash) ..."
sudo usermod -aG video blocks 2>/dev/null || true
echo_ok "blocks added to video group"

echo_info "Allowing blocks to operate on repos owned by primary user ..."
sudo git config --system --add safe.directory '*'
echo_ok "Git safe.directory configured"

echo_info "Setting git repo permissions for updater ..."
COMPONENTS_YAML="$BS_PATH/updater/components.yaml"
if [[ -f "$COMPONENTS_YAML" ]]; then
    grep '^\s*path:' "$COMPONENTS_YAML" | awk '{print $2}' | while read -r repo_path; do
        expanded="${repo_path/#\~/$_BSENV_HOME}"
        if [[ -d "$expanded/.git" ]]; then
            sudo chgrp -R blocksscreen "$expanded" || true
            sudo chmod -R g+rwX "$expanded" || true
            echo_ok "  permissions set: $expanded"
        fi
    done
else
    find "$_BSENV_HOME" -maxdepth 2 -name ".git" -type d 2>/dev/null | while read -r gitdir; do
        repodir=$(dirname "$gitdir")
        sudo chgrp -R blocksscreen "$repodir" || true
        sudo chmod -R g+rwX "$repodir" || true
    done
fi
echo_ok "Git repo permissions set"

echo_info "Installing BlocksScreen-deploy path unit (sudo-free hook trigger) ..."
DEPLOY_SVC=$(cat "$SCRIPT_PATH/BlocksScreen-deploy.service")
DEPLOY_SVC=${DEPLOY_SVC//BS_DIR/$BS_PATH}
DEPLOY_SVC=${DEPLOY_SVC//BS_PRIMARY_HOME/$_BSENV_HOME}
echo "$DEPLOY_SVC" | sudo tee /etc/systemd/system/BlocksScreen-deploy.service >/dev/null
DEPLOY_PATH=$(cat "$SCRIPT_PATH/BlocksScreen-deploy.path")
DEPLOY_PATH=${DEPLOY_PATH//BS_PRIMARY_HOME/$_BSENV_HOME}
echo "$DEPLOY_PATH" | sudo tee /etc/systemd/system/BlocksScreen-deploy.path >/dev/null
sudo systemctl daemon-reload
sudo systemctl enable --now BlocksScreen-deploy.path
echo_ok "BlocksScreen-deploy path unit installed"

echo_info "Installing BlocksScreen-bootstrap service ..."
_BOOTSTRAP_SRC="$SCRIPT_PATH/BlocksScreen-bootstrap.service"
_BOOTSTRAP_DEST="/etc/systemd/system/BlocksScreen-bootstrap.service"
if [[ -f "$_BOOTSTRAP_DEST" && ! -L "$_BOOTSTRAP_DEST" ]]; then
    sudo rm "$_BOOTSTRAP_DEST"
fi
if [[ ! -L "$_BOOTSTRAP_DEST" ]]; then
    sudo systemctl link "$_BOOTSTRAP_SRC"
fi
sudo systemctl daemon-reload
echo_ok "BlocksScreen-bootstrap service installed (symlink)"

echo_info "Installing post-merge hook ..."
chmod +x "$SCRIPT_PATH/post-merge" "$SCRIPT_PATH/bs-stop.sh" "$SCRIPT_PATH/bs-splash.py"
git -C "$BS_PATH" update-index --chmod=+x scripts/post-merge 2>/dev/null || true
git -C "$BS_PATH" config core.hooksPath scripts
echo_ok "post-merge hook installed"

echo_info "Installing Python requirements ..."
apt-get install -y --quiet libsystemd-dev python3-dev 2>/dev/null || true
# xsetroot is used as belt-and-suspenders cursor hiding alongside the Xorg -nocursor server flag.
sudo apt-get install -y --quiet x11-xserver-utils 2>/dev/null || true
# sdbus is pinned to 0.12.0 (working aarch64 wheel); --no-binary forces a clean source build
# only on a fresh venv. --upgrade-strategy=only-if-needed skips already-satisfied packages.
"$BSENV/bin/pip" install --quiet --only-binary :all: --no-binary sdbus,sdbus-networkmanager \
    --upgrade-strategy=only-if-needed \
    -r "$BS_PATH/scripts/requirements.txt" || true
echo_ok "Python requirements installed"

echo_info "Pre-generating framebuffer splash cache ..."
"$BSENV/bin/python3.11" "$SCRIPT_PATH/bs-splash.py" --precompute 2>/dev/null || true
echo_ok "Splash cache ready"

echo_ok "BlocksScreen updater setup complete"
