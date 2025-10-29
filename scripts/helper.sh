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
SERVICE_TEMPLATE_NAME="set-hostname@.service"
HELPER_SCRIPT="hostname-helper.sh"
SCRIPTS_PATH="scripts/"
function configure_hostname_setter(){
	echo_info "Starting hostname setter tool..."
    
	has_file "$SERVICE_TEMPLATE_NAME"
	# Add service to system 
    # echo "${SCRIPTS_PATH}${SERVICE_TEMPLATE_NAME}"
	# chmod +x "${SCRIPTS_PATH}${SERVICE_TEMPLATE_NAME}"
	sudo cp "${SCRIPTS_PATH}${SERVICE_TEMPLATE_NAME}" /etc/systemd/system/
	sudo systemctl enable "$SERVICE_TEMPLATE_NAME"



	echo_info "file exists"
}

function has_file(){    
    if [ -e "$SCRIPTS_PATH"$1 ]; then
        echo_ok "File $1 exists"
		return 0
	else
        echo_error "File $1 does not exist"
		return 1
	fi
}
configure_hostname_setter
