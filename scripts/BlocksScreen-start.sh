#!/bin/bash

# BlocksScreen.sh . Modified from KlipperScreen.sh

# moonraker-sudo (mnrkrsudo)
# Provides a specified Group that is intended to elevate user privileges
# to help moonraker with sudo actions, if in CustomPIOS Images with
# Module "password-for-sudo".
#
# Partially used functions from Arcsine
#
# Copyright (C) 2020 Stephan Wendel <me@stephanwe.de>
#
# This file may be distributed under the terms of the GNU GPLv3 license

XDG_RUNTIME_DIR=/run/user/$(id -u)
export XDG_RUNTIME_DIR

SCRIPT_PATH=$(dirname $(realpath $0))
if [ -f $SCRIPT_PATH/launch_BlocksScreen.sh ]; then
    echo "Running $SCRIPT_PATH/launch_BlocksScreen.sh"
    $SCRIPT_PATH/launch_BlocksScrenn.sh
    exit $?
fi

if [[ "$BACKEND" =~ ^[wW]$ ]]; then
    echo "Running BlocksScreen on Cage"
    /usr/bin/cage -ds $BS_XCLIENT
else
    echo "Running BlocksScreen on X in display :0 by default"
    /usr/bin/xinit $BS_XCLIENT
fi
