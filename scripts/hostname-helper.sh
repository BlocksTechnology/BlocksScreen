#!/bin/bash

set -eu

BRAND_PREFIX="BLOCKS"
MODEL="RF50"
SERIAL="$(awk '/Serial/ {print $3}' /proc/cpuinfo)"

CUSTOM_HOSTNAME=$BRAND_PREFIX-$MODEL-$(awk '/Serial/ {print $3}' /proc/cpuinfo)

echo $CUSTOM_HOSTNAME
echo "$CUSTOM_HOSTNAME" > /etc/hostname
