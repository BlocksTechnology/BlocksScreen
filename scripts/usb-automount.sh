#!/bin/bash

ACTION=$1                                   # Add or remove usb drive
DEVICE_NAME=$2                                  # Usb dev name
LABEL=$3                                    # Usb drive name

NAME="${LABEL:-$DEVNAME}"                   # Use devname if no label is available
MOUNT_POINT="/media/$NAME"                  # Default mount point
BASE_TARGET="/home/blocks/printer_data/gcodes"  # Default symlink creation target
LINK_PATH="$BASE_TARGET/USB-$NAME"              # Default symlink

if [ "$ACTION" == "add" ]; then
    /usr/bin/systemd-mount --no-block --collect --options=uid=1000,gid=1000,umask=000 "/dev/$DEVICE_NAME" "$MOUNT_POINT"
    FINAL_LINK="$LINK_PATH"
    COUNTER=1
    while [ -e "$FINAL_LINK" ] || [ -L "$FINAL_LINK" ]; do
        FINAL_LINK="${LINK_PATH}-$COUNTER"
        ((COUNTER++))
    done
    /usr/bin/ln -sfT "$MOUNT_POINT" "$FINAL_LINK"
elif [ "$ACTION" == "remove" ]; then
    /usr/bin/systemd-umount --lazy "/dev/$DEVICE_NAME"
    /usr/bin/rm -rf "$MOUNT_POINT"
    find "$BASE_TARGET" -maxdepth 1 -lname "$MOUNT_POINT" -delete
fi