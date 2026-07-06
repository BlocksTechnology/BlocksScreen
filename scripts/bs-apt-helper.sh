#!/bin/bash
# bs-apt-helper: the only apt entry sudoers grants 'blocks'; fixed argvs stop option injection.
set -euo pipefail

APT_GET=/usr/bin/apt-get
DPKG=/usr/bin/dpkg
LOCK=(-o DPkg::Lock::Timeout=60)
CONF=(-o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold)
export DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a

usage() {
    echo "usage: bs-apt-helper {update|upgrade <pkg...>|autoremove|fix-broken|dselect-upgrade|set-selections}" >&2
    exit 2
}

verb="${1:-}"
[ $# -ge 1 ] && shift
case "$verb" in
    update)
        [ $# -eq 0 ] || usage
        exec "$APT_GET" "${LOCK[@]}" update
        ;;
    upgrade)
        [ $# -ge 1 ] || usage
        for p in "$@"; do
            # Debian name shape; first char alnum so '-options' can't pass.
            [[ "$p" =~ ^[a-zA-Z0-9][a-zA-Z0-9+.-]*$ ]] || {
                echo "bs-apt-helper: invalid package name: $p" >&2
                exit 2
            }
        done
        exec "$APT_GET" "${LOCK[@]}" "${CONF[@]}" install --only-upgrade -y "$@"
        ;;
    autoremove)
        [ $# -eq 0 ] || usage
        exec "$APT_GET" "${LOCK[@]}" autoremove -y
        ;;
    fix-broken)
        [ $# -eq 0 ] || usage
        exec "$APT_GET" "${LOCK[@]}" "${CONF[@]}" -f install -y
        ;;
    dselect-upgrade)
        [ $# -eq 0 ] || usage
        exec "$APT_GET" "${LOCK[@]}" "${CONF[@]}" dselect-upgrade -y
        ;;
    set-selections)
        [ $# -eq 0 ] || usage
        exec "$DPKG" --set-selections
        ;;
    *)
        usage
        ;;
esac
