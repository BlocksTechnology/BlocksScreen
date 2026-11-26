#!/bin/bash
# bs-apt-helper: the only apt entry sudoers grants 'blocks'; fixed argvs stop option injection.
set -euo pipefail

APT_GET=/usr/bin/apt-get
DPKG=/usr/bin/dpkg
APT_MARK=/usr/bin/apt-mark
LISTS=/var/lib/apt/lists
LOCK=(-o DPkg::Lock::Timeout=60)
CONF=(-o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold)
# apt 2.6 default true: one linux-libc-dev upgrade drags in the kernel metas.
BYSRC=(-o APT::Get::Upgrade-By-Source-Package=false)
export DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a

usage() {
    echo "usage: bs-apt-helper {update|download <pkg...>|upgrade <pkg...>|hold <pkg...>|autoremove|autoclean|clean|clear-lists|configure|fix-broken|dselect-upgrade|set-selections}" >&2
    exit 2
}

check_names() {
    [ $# -ge 1 ] || usage
    for p in "$@"; do
        # Debian name shape; first char alnum so '-options' can't pass.
        [[ "$p" =~ ^[a-zA-Z0-9][a-zA-Z0-9+.-]*$ ]] || {
            echo "bs-apt-helper: invalid package name: $p" >&2
            exit 2
        }
    done
}

verb="${1:-}"
[ $# -ge 1 ] && shift
case "$verb" in
    update)
        [ $# -eq 0 ] || usage
        exec "$APT_GET" "${LOCK[@]}" update
        ;;
    download)
        check_names "$@"
        exec "$APT_GET" "${LOCK[@]}" "${BYSRC[@]}" install --only-upgrade --download-only -y "$@"
        ;;
    upgrade)
        check_names "$@"
        exec "$APT_GET" "${LOCK[@]}" "${CONF[@]}" "${BYSRC[@]}" install --only-upgrade -y "$@"
        ;;
    hold)
        check_names "$@"
        exec "$APT_MARK" hold "$@"
        ;;
    autoremove)
        [ $# -eq 0 ] || usage
        exec "$APT_GET" "${LOCK[@]}" autoremove -y
        ;;
    autoclean)
        [ $# -eq 0 ] || usage
        exec "$APT_GET" "${LOCK[@]}" autoclean
        ;;
    clear-lists)
        [ $# -eq 0 ] || usage
        # Corrupt lists fail every update; apt refetches them all.
        exec /usr/bin/find "$LISTS" -maxdepth 1 -type f ! -name lock -delete
        ;;
    configure)
        [ $# -eq 0 ] || usage
        exec "$DPKG" --force-confdef --force-confold --configure -a
        ;;
    clean)
        [ $# -eq 0 ] || usage
        exec "$APT_GET" "${LOCK[@]}" clean
        ;;
    fix-broken)
        [ $# -eq 0 ] || usage
        exec "$APT_GET" "${LOCK[@]}" "${CONF[@]}" "${BYSRC[@]}" -f install -y
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
