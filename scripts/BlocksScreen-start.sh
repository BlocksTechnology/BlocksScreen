#!/bin/bash

# BlocksScreen start script
#
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
#
# Based on the work :
# https://github.com/KlipperScreen/KlipperScreen/blob/master/scripts/KlipperScreen-start.sh
# Copyright (C) KlipperScreen contributors
#
# Modified from the work referenced above
#
# This file is distributed under the terms of the GNU General Public License v3.
# See https://www.gnu.org/licenses/gpl-3.0.html for details.

XDG_RUNTIME_DIR=/run/user/$(id -u)
export XDG_RUNTIME_DIR

SCRIPT_PATH=$(dirname $(realpath $0))
if [ -f $SCRIPT_PATH/launch_BlocksScreen.sh ]; then
    echo "Running $SCRIPT_PATH/launch_BlocksScreen.sh"
    $SCRIPT_PATH/launch_BlocksScreen.sh
    exit $?
fi

if [[ "$BACKEND" =~ ^[wW]$ ]]; then
    echo "Running BlocksScreen on Cage"
    /usr/bin/cage -ds $BS_XCLIENT
else
    echo "Running BlocksScreen on X in display :0 by default"
    /usr/bin/xinit $BS_XCLIENT
fi
