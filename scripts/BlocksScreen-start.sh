#!/bin/bash

# BlocksScreen start script
#
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
#
# Based on the work :
# https://github.com/KlipperScreen/KlipperScreen/blob/master/scripts/KlipperScreen-start.sh
# Copyright (C) KlipperScreen contributors
#
# This file is part of BlocksScreen.
#
# BlocksScreen is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlocksScreen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BlocksScreen. If not, see <https://www.gnu.org/licenses/>.
# 
# SPDX-License-Identifier: AGPL-3.0-or-later


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
    exec /usr/bin/cage -ds $BS_XCLIENT
else
    echo "Running BlocksScreen on X in display :0 by default"
    exec /usr/bin/xinit $BS_XCLIENT
fi
