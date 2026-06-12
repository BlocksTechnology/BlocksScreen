#!/bin/bash
# ExecStopPost: set tty7 to KD_GRAPHICS, switch to it, paint splash from cache.
# tty7 is in KD_TEXT after X/Cage exits; setting KD_GRAPHICS before chvt prevents
# fbcon from overwriting fb0. bs-splash.py (ExecStartPre) takes over KD_GRAPHICS
# on tty7 when the service restarts. tty7 must match TTYPath in the service unit.
CACHE=/home/blocks/.cache/blockscreen/splash.raw
python3 -c "import fcntl; t=open('/dev/tty7','w'); fcntl.ioctl(t.fileno(),0x4B3A,1); t.close()" 2>/dev/null || true
/usr/bin/chvt 7
if [[ -f "$CACHE" ]]; then
    dd if="$CACHE" of=/dev/fb0 bs=4M 2>/dev/null || true
fi
