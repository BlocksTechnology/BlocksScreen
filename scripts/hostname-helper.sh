#!/bin/bash

set -eu


Red='\033[0;31m'
Green='\033[0;32m'
Blue='\033[0;34m'
Normal='\033[0m'

echo_ok ()
{
    printf "${Green}$1${Normal}\n"
}
echo_info (){
    printf "${Blue}$1${Normal}\n"
}

echo_error ()
{
    printf "${Red}$1${Normal}\n"
}
SERVICE_PATH="/etc/systemd/system/set-hostname.service"
SCRIPT_PATH="$(readlink -f "$0")"
echo_info "Script running on $SCRIPT_PATH..."
BRAND_PREFIX="BLOCKS"
MODEL="RF50"
SERIAL="$(awk '/Serial/ {print $3}' /proc/cpuinfo)"
CUSTOM_HOSTNAME=$BRAND_PREFIX-$MODEL-$(awk '/Serial/ {print $3}' /proc/cpuinfo)

function install_service(){
    if [ ! -f "$SERVICE_PATH" ]; then
    
        echo_info "Missing service file, installing..."
        cat <<EOF | sudo tee "$SERVICE_PATH" > /dev/null
[Unit]
Description=Set hostname based on CPU info
DefaultDependencies=no
Before=network-pre.target 
After=network-pre.target 

[Service]
Type=oneshot
ExecStart=$SCRIPT_PATH
RemainAfterExit=yes

[Install]
WantedBy=sysinit.target
EOF
    sudo systemctl daemon-reload
    sudo systemctl enable set-hostname.service 
    sudo systemctl start set-hostname.service
    else 
        echo_ok "Service '$SERVICE_PATH' already exists. Skipping installation"
    fi
}
function set_hostname(){
    local CURRENT_HOSTNAME=$(hostnamectl --static)
    if [ "$CURRENT_HOSTNAME" = "$1"  ]; then
        echo_ok "Hostname already set to $1. No action needed"
    else 
        echo_info "Setting hostname to $1..."
        sudo sed -i "1s/^/127.0.1.1 $1\n/" /etc/hosts
        sudo hostnamectl set-hostname $1
        echo "Hostname updated. Rebooting to apply"
        sleep 5
        reboot
    fi
}



install_service
set_hostname $CUSTOM_HOSTNAME