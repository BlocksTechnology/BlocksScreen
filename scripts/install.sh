#!/bin/bash 

# This script install Blocks Screen on Debian devices, intended to be used with Klipper.
# This Modified from KlipperScreen (alfrix) installation script aswell as Klippain-shaketune (Frix-x) installation script.


MOONRAKER_CONFIG="${HOME}/printer_data/config/moonraker.conf"
KLIPPER_PATH="${HOME}/klipper"
KLIPPER_VENV_PATH="${HOME}/klippy-env"

USER_CONFIG_PATH="${HOME}/printer_data/config"

SCRIPT_PATH=$(dirname -- "$(readlink -f -- "$0")")
echo ${SCRIPT_PATH}
BS_PATH=$(dirname "$SCRIPT_PATH")
echo ${BS_PATH}
BSENV="${BLOCKSSCREEN_VENV:-${HOME}/.BlocksScreen-env}"
echo ${BSENV}
PYTHON_VERSION=3.11.2


XSERVER="xinit xinput x11-xserver-utils xserver-xorg-input-evdev xserver-xorg-input-libinput xserver-xorg-legacy xserver-xorg-video-fbdev"
CAGE="cage seatd xwayland"
PYOBJECT="pkg-config python3-dev"
MISC="autoconf python3-venv libdbus-glib-1-dev udiskie"
# QTMISC="'^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev libxcb-cursor0 opencv-python-headless"
QTMISC=" ^libxcb.*-dev libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev libxcb-cursor0"

Red='\033[0;31m'
Green='\033[0;32m'
Blue='\033[0;34m'
Cyan='\033[0;36m'
Normal='\033[0m'

echo_info (){
    printf "${Blue}$1${Normal}\n"
}

echo_text ()
{
    printf "${Normal}$1${Cyan}\n"
}

echo_error ()
{
    printf "${Red}$1${Normal}\n"
}

echo_ok ()
{
    printf "${Green}$1${Normal}\n"
}

function install_graphical_backend(){
    while true; do 
        if [ -z "$BACKEND" ]; then 
            echo_text ""
            echo_text "Choose graphical backend"
            echo_info "Default is Xserver"
            echo_text "Wayland is Experimental needs kms/drm drivers doesn't support DPMS and may need autologin"
            echo_text ""
            echo_info "Press enter for default (XServer)"
            read -r -e -p "Backend Xserver or Wayland (cage)? [X/w]" BACKEND
            if [[ "$BACKEND" =~ ^[wW]$ ]]; then 
                echo_text "Installing Wayland Cage Kiosk"
                if sudo apt install -y $CAGE; then 
                    echo_ok "Installed Cage"
                    BACKEND="W"
                    break
                else 
                    echo_error "Installation of Cage dependencies failed ($CAGE)"
                    exit 1
                fi 
            else 
                echo_text "Installing Xserver"
                if sudo apt install -y $XSERVER; then 
                    echo_ok "Installed X"
                    update_x11
                    BACKEND="X"
                    break
                else 
                    echo_erro "Installation of X-server dependencies failed ($XSERVER)"
                    exit 1 
                fi 
            fi 
        fi 
    done
}

function install_packages(){
    echo_info "Updating package data"
    sudo apt update 

    
    echo_text "Checking for broken packages...."
    if dpkg-query -W -f='${db:Status-Abbrev} ${binary:Package}\n' | grep -E "^.[^nci]"; then 
        echo_text "Detected brocken packages. Attemping to fix"
        sudo apt -f install 

        if dpkg-query -W -f='${db:Status-Abbrev} ${binary:Package}\n' | grep -E "^.[^nci]"; then 
            echo_error "Unable to fix broken packages. These must be fixed before BlocksScreen can be installed"
            exit 1
        fi 

    else 
        echo_info "No broken packages"
    fi 

    echo_text "Installing dependencies"
    sudo apt install -y $OPTIONAL
    echo "$_"

    if sudo apt install -y $PYFOBJECT; then 
        echo_ok "Installed PyGobject dependencies"
    else
        echo_error "Installation of PyGobject dependencies failed ($PYGOBJECT)"
        exit 1
    fi 

    if sudo apt install -y $MISC; then 
        echo_ok "Installed Misc packages"
    else 
        echo_error "Installation of Misc packages failed ($MISC)"
        exit 1
    fi 

    if sudo apt-get install -y $QTMISC; then
        echo_ok "Installed PyQt6 dependencies"
    else 
        echo_error "Installation of PyQT dependencie packages failed ($QTMISC)"
        exit 1
    fi
}

function check_requirements(){
    echo_info "Checking Python version > "$VERSION
    python3 --version 

    if ! python3 -c 'import sys; exit(1) if sys.version_info <= ('$VERSION') else exit(0)'; then 
        echo_error 'Not supported'
        exit 1
    fi
}


function install_app_python_version(){
    echo_info "Checking python version on target 3.11.2; Installing if needed"
    if python${PYTHON_VERSION:0:4} --version &>/dev/null; then 
        echo_ok "Python $PYTHON_VERSION is already installed."
    else 
        echo_error "BlocksScreen requires python $PYTHON_VERSION, Installing ...."

        echo_info "Downloading Python 3.11.2"
        # Download the specific Python version
        sudo wget -P /usr/src/ https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz #Download to a dir
    
        sudo tar xzf /usr/src/Python-$PYTHON_VERSION.tgz -C /usr/src/   #Unpack to a dir 

        # Remove the tgz file 
        sudo rm -rf /usr/src/Python-$PYTHON_VERSION.tgz 

        # Install python 
        sudo chmod +x /usr/src/Python-$PYTHON_VERSION/configure

        sudo sh /usr/src/Python-$PYTHON_VERSION/configure --enable-optimizations --prefix=/usr/local
        
        sudo make -j $(nproc) # Compile software and try to use all cores 
        echo_info "Using $(nproc) Cores to compile python 3.11.2" 
        echo_info "Prociding with compiling and installation with 'make altinstall'"
        sudo make altinstall 
        
        if python3.${PYTHON_VERSION:0:4} --version &>/dev/null; then 

            echo_ok "Python $PYTHON_VERSION installed successfully"
        else 
            echo_error "Python version $PYTHON_VERSION was not installed for some reason. Exiting"
            exit 1
        fi

    fi 

    echo_info "Python Verification ended"
}

function create_virtualenv(){
    
    install_app_python_version

    if [ "${BSENV}" = "/" ]; then 
        echo_error "Failed to resolve venv location. Aborting."
        exit 1
    fi 

    if [ -d "$BSENV" ]; then 
        echo_text "Removing old virtual enviroment"
        rm -rf "${BSENV}"
    fi 

    echo_text "Creating virtual enviroment"
    python${PYTHON_VERSION:0:4} -m venv "${BSENV}"

    if ! . "${BSENV}/bin/activate"; then 
        echo_error "Could not activate the enviroment, try deleting ${BSENV} and retry"
        exit 1
    fi 

    if [[ "$(uname -m)" =~ armv[67]l ]]; then 
        echo_text "Using armv[67]l! Adding pywheels.org as extra index..."
        pip3 --disable-pip-version-check install --extra-index-url https://www.piwheels.org/simple -r ${BS_PATH}/scripts/requirements.txt
    else 
        pip3 --disable-pip-version-check install -r ${BS_PATH}/scripts/requirements.txt
    fi 
    if [ $? -gt 0 ]; then 
        echo_error "Error: pip install exited with status code $?"
        echo_text "Trying again with new tools..."
        sudo apt install -y build-essentials cmake libsystmed-dev 
        if [[ "$(uname -m)" =~ armv[67]l ]]; then 
            echo_text "Adding piwheels.org as extra index..."
            echo_info "Installing with pip setuptools and app requirements"
            pip3 install --extra-index-url https://www.piwheels.org/simple --upgrade pip setuptools 
            pip3 install --extra-index-url https.//www.piwheels.org/simple -r ${BS_PATH}/scripts/requirements.txt
        else 
            echo_info "Upgrading pip and Installing with pip setuptools and app requirements"
            pip3 install --upgrade pip setuptools 
            pip3 install -r ${BS_PATH}/scripts/requirements.txt 
            printf "\n"
        fi 
        if [ $? -gt 0 ]; then 
            echo_error "Unable to install dependencies, aborting install."
            deactivate
            exit 1
        fi 
    fi 
    deactivate
    if [ "${BSENV}" = "/" ]; then  
        echo_info "Blocks Screen Virtual enviroment created."
    fi

}

function install_systemd_service(){
    echo_info "Installing BlocksScreen unit file"
    
    SERVICE=$(cat "$SCRIPT_PATH"/BlocksScreen.service)
    SERVICE=${SERVICE//BS_USER/$USER}
    SERVICE=${SERVICE//BS_ENV/$BSENV}
    SERVICE=${SERVICE//BS_DIR/$BS_PATH}
    SERVICE=${SERVICE//BS_BACKEND//$BACKEND}

    echo "$SERVICE" | sudo tee /etc/systemd/system/BlocksScreen.service > /dev/null 
    sudo systemctl unmask BlocksScreen.service 
    sudo systemctl daemon-reload
    sudo systemctl enable BlocksScreen
    sudo systemctl set-default multi-user.target 
    sudo adduser "$USER" tty 

    if systemctl status "BlocksScreen.service" &>/dev/null; then
        echo_ok "BlocksScreen service exists. Successfully installed"
        # Display success image
        # feh --fullscreen /path/to/success_image.png
    else
        echo_error "BlocksScreen service does not exist. Please fix that."
        # Display failure image
        # feh --fullscreen /path/to/failure_image.png
    fi
}

function create_policy(){
    POLKIT_DIR="/etc/polkit-1/rules.d"
    POLKIT_USR_DIR="/usr/share/polkit-1/rules.d"

    echo_text "Installing BlocksScreen PolicyKit Rules"
    sudo groupadd -f blocksscreen
    sudo groupadd -f network 
    sudo usermod -aG plugdev "$USER"
    sudo adduser "$USER" netdev 
    sudo adduser "$USER" network 

    if [ ! -x "$(command -v pkaction)" ]; then 
        echo "Policykit not installed"
        return 
    fi 

    POLKIT_VERSION="$( pkaction --version | grep -Po "(\d+\.?\d*)" )"
    echo_info "PolicyKit Version ${POLKIT_VERSION} Detected"
    if [ "$POLKIT_VERSION" = "0.105" ]; then 
        # install legacy pkla
        create_policy_legacy
        return 
    fi 

    RULE_FILE=""
    if [ -d $POLKIT_USR_DIR ]; then 
        RULE_FILE="${POLKIT_USR_DIR}/BlocksScreen.rules"
    elif [ -d $POLKIT_DIR ]; then 
        RULE_FILE="${POLKIT_DIR}/BlocksScreen.rules"
    else 
        echo_error "PolicyKit rules folder not detected"
        exit 1
    fi 
    echo_text "Installing PolicyKit Rules to ${RULE_FILE}..."
    sudo rm -r ${RULE_FILE}

    BS_GID=$( getent group blocksscreen | awk -F: '{printf "%d", $3}' )
    sudo tee ${RULE_FILE} > /dev/null << EOF 
polkit.addRule(function(action, subject) {
    polkit.log("Second Rule Evaluating action: " + action.id + " for user: " + subject.user);
    if ((action.id == "org.freedesktop.login1.power-off" ||
         action.id == "org.freedesktop.login1.power-off-multiple-sessions" ||
         action.id == "org.freedesktop.login1.reboot" ||
         action.id == "org.freedesktop.login1.reboot-multiple-sessions" ||
         action.id == "org.freedesktop.login1.halt" ||
         action.id == "org.freedesktop.login1.halt-multiple-sessions" ||
         action.id == "org.freedesktop.NetworkManager.settings.modify.system" ||
         action.id == "org.freedesktop.NetworkManager.reload" ||
         action.id.startsWith("org.freedesktop.NetworkManager")) && 
         (subject.user == "$USER" || subject.isInGroup("blocksscreen"))) {
                 return polkit.Result.YES;
         }
});
EOF
}

function create_udisks_policy(){
    RULE_FILE=""
    if [ -d $POLKIT_USR_DIR ]; then 
        RULE_FILE="${POLKIT_USR_DIR}/50-udisks2.rules"
    elif [ -d $POLKIT_DIR ]; then 
        RULE_FILE="${POLKIT_DIR}/50-udisks2.rules"
    else 
        echo_error "PolicyKit rules folder not detected"
        exit 1
    fi 
    echo_text "Installing PolicyKit Rules to ${RULE_FILE}..."
    sudo rm -r ${RULE_FILE}
    
    BS_GID=$( getent group blocksscreen | awk -F: '{printf "%d", $3}' )

    sudo tee ${RULE_FILE} > /dev/null << EOF 
polkit.addRule(function(action, subject) {
    if (action.id.startsWith("org.freedesktop.udisks2.") && 
    subject.isInGroup("blocksscreen") && subject.user == "$USER") {
        return polkit.Result.YES;
    }
});
EOF
}
function create_policy_legacy(){
    RULE_FILE="/etc/polkit-1/localauthority/50-local.d/20-blocksscreen.pkla"
    sudo tee ${RULE_FILE} > /dev/null << EOF 
[BlocksScreen] 
Identity=unix-user:$USER
Action=org.freedesktop.login1.power-off; 
       org.freedesktop.login1.power-off-multiple-sessions; 
       org.freedesktop.login1.reboot; 
       org.freedesktop.login1.reboot-multiple-sessions; 
       org.freedesktop.login1.halt; 
       org.freedesktop.login1.halt-multiple-sessions; 
       org.freedesktop.NetworkManager.*
ResultAny=yes
EOF
}

function update_x11(){
    sudo tee /etc/X11/Xwrapper.config > /dev/null << EOF
allowed_users=anybody
needs_root_rights=yes
EOF
}

# fix fbturbo

function add_desktop_file(){
    echo_info "Adding desktop file"
    mkdir -p "$HOME"/.local/share/applications/
    cp "$SCRIPT_PATH"/BlocksScreen.desktop "$HOME"/.local/share/applications/BlocksScreen.desktop
    sudo cp "$SCRIPT_PATH"/../resources/logoblocks.png /usr/share/icons/hicolor/scalable/apps/BlocksScreen.png
}

function start_BlocksScreen(){
    echo_info "Starting Blocks Screen service"
    sudo systemctl restart BlocksScreen.service
}

# function add_updater{
#     update_section=$(grep -c '\[update_manager[a-z ]* Blocks Screen\)]' $BLOCKS_SCREEN_CONFIG || true)
#     if [ "$update_section" -eq 0 ]; then 
#         echo -n "[INSTALL] Adding update manager to moonraker.conf...."
#         cat $(BLOCKS_SCREEN_PATH)/moonraker.conf >> $MOONRAKER_CONFIG
# }

function restart_klipper(){
    echo_info "Restarting Klipper"
    sudo systemctl restart klipper
}

function restart_moonraker(){
    echo_info "Restarting Moonraker"
    sudo systemctl restart moonraker 
}

function is_package_installed(){
    dpkg -s "$1" &> /dev/null
    return $?
}


# function add_updater{
#     # TODO: Add updater to moonraker.conf, so BlocksScreen is always updated 
#     update_section=$(grep -c '\[update_manager[a-z ]* Blocks-Screen\]' $MOONRAKER_CONFIG || true)
#     if [ "$update_section" -eq 0 ]; then 
#         echo_text -n "[INSTALL] Adding update manager to moonraker.conf..."
#         cat ${SCRIPT_PATH}/moonraker.conf >> $MOONRAKER_CONFIG
#     fi 
# }


# function link_klipper_extras(){
#     # TODO: Get files from blocks screen klipper extras and create symlinks to klipper/extras/* | or just copy them to that directory 
#     if [ ! -d "${KLIPPER_PATH}/klippy/extras/BlocksScreen" ]; then 
#         echo "[HELPER] Linking BlocksScreen extras to klippy extras directory;" 
#         # TODO: Need to create a symlinks to all extras on Blocks Screen klipper_extras/
#         ln -frsn ${SCRIPT_PATH}/klipper_extras/* ${KLIPPER_PATH}/klippy/extras/*
#     fi
#     # find * -name '*.py' -exec ln -sf $PWD/{} ~/klipper/klippy/extras/{} \; 
# }

printf "\n===================================\n"
echo_info "-Blocks Screen installation script-"
printf "\n===================================\n"


# Run the actual installation 
echo_ok "Starting Blocks Screen installation"
install_graphical_backend
install_systemd_service
install_packages
create_virtualenv
create_policy

# fix fbturbo
add_desktop_file 

restart_klipper
restart_moonraker


start_BlocksScreen
if [ -z "$START" ] || [ "$START" -eq 0 ]; then 
    echo_ok "Blocks Screen was installed"
else 
    echo "Starting Blocks Screen"
    start_BlocksScreen
fi 