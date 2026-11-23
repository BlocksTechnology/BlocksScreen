#!/bin/bash
# Boot guard: restores tracked files a power cut left empty, before any unit runs from the tree.
# Installed outside the tree by install-updater.sh: an in-tree healer can be emptied by the same cut.
# Usage: bs-tree-guard.sh BS_PATH HOME_DIR. Always exits 0, a failed heal must not block boot.
set -uo pipefail

BS_PATH="${1:?usage: bs-tree-guard.sh BS_PATH HOME_DIR}"
HOME_DIR="${2:?usage: bs-tree-guard.sh BS_PATH HOME_DIR}"
_tag="[bs-tree-guard]"
[[ -d "$BS_PATH/.git" ]] || exit 0

_owner=$(stat -c %U "$BS_PATH")
# Root-run git would leave root-owned files the updater cannot rewrite.
_as_owner() {
    if [[ "$(id -u)" == 0 && "$_owner" != root ]]; then runuser -u "$_owner" -- "$@"; else "$@"; fi
}
_git() { _as_owner git -C "$BS_PATH" "$@"; }

# Nothing else has started yet, so any lock is stale; an empty ref aborts every fetch.
rm -f "$BS_PATH/.git/index.lock"
find "$BS_PATH/.git/refs" -type f -empty -delete 2>/dev/null

# Regular files that are empty on disk but not in HEAD, one per line.
_broken_paths() {
    local meta path
    while IFS=$'\t' read -r -d '' meta path; do
        [[ "$meta" == 100* && "${meta##* }" != 0 ]] || continue
        [[ -f "$BS_PATH/$path" && ! -s "$BS_PATH/$path" ]] && printf '%s\n' "$path"
    done < <(_git ls-tree -r -l -z --full-tree HEAD)
}

# Literal pathspecs: a tracked name with glob characters must not match other files.
_restore() {
    _git --literal-pathspecs checkout HEAD --pathspec-from-file=- <<<"$1" 2>/dev/null && return 0
    # The index itself may be the truncated file: rebuild it from HEAD, worktree untouched.
    rm -f "$BS_PATH/.git/index"
    _git reset -q 2>/dev/null
    _git --literal-pathspecs checkout HEAD --pathspec-from-file=- <<<"$1"
}

healed=0
if ! _git cat-file -e 'HEAD^{tree}' 2>/dev/null; then
    echo "$_tag HEAD unreadable, pruning empty objects"
    find "$BS_PATH/.git/objects" -type f -empty -delete 2>/dev/null
    _good=$(tr -d '[:space:]' <"$HOME_DIR/.cache/blockscreen/last_good_commit" 2>/dev/null)
    _branch=$(_git symbolic-ref --short HEAD 2>/dev/null)
    if [[ -n "$_good" ]] && _git cat-file -e "$_good^{tree}" 2>/dev/null; then
        _git reset -q --hard "$_good" && healed=1 && echo "$_tag reset to last good ${_good:0:8}"
    elif [[ -n "$_branch" ]] && _as_owner timeout 60 git -C "$BS_PATH" fetch -q origin "$_branch" 2>/dev/null; then
        _git reset -q --hard "origin/$_branch" && healed=1 && echo "$_tag reset to origin/$_branch"
    else
        echo "$_tag cannot heal offline, leaving recovery to the updater"
    fi
else
    _broken=$(_broken_paths)
    if [[ -n "$_broken" ]]; then
        echo "$_tag $(wc -l <<<"$_broken") empty tracked files, restoring from HEAD"
        if _restore "$_broken"; then
            healed=1
        else
            echo "$_tag restore failed"
        fi
    fi
fi
[[ "$healed" == 1 ]] || exit 0

sync -f "$BS_PATH"
# Units symlinked into the tree were loaded empty at boot and skipped.
systemctl daemon-reload
for _unit in BlocksScreen.service BlocksScreen-clock.timer; do
    systemctl is-enabled --quiet "$_unit" 2>/dev/null && systemctl --no-block start "$_unit"
done
systemctl --no-block start BlocksScreen-bootstrap.service
# A deploy that ran an empty install-updater.sh already consumed its flag.
_as_owner mkdir -p "$HOME_DIR/.config/blockscreen"
_as_owner touch "$HOME_DIR/.config/blockscreen/.run-install-updater"
echo "$_tag healed, deploy re-armed"
exit 0
