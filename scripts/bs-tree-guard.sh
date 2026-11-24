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

# Read before pruning: once an empty loose branch ref is gone, git falls back to an older packed-refs entry.
_head_ref=$(sed -n 's/^ref: //p' "$BS_PATH/.git/HEAD" 2>/dev/null)
_branch=${_head_ref#refs/heads/}
_ref_lost=0
[[ -n "$_head_ref" && -f "$BS_PATH/.git/$_head_ref" && ! -s "$BS_PATH/.git/$_head_ref" ]] && _ref_lost=1

# Nothing else has started yet, so any lock is stale; an empty ref aborts every fetch.
rm -f "$BS_PATH/.git/index.lock"
find "$BS_PATH/.git/refs" -type f -empty -delete 2>/dev/null
# Same for pseudo-refs: an empty ORIG_HEAD fails every later pull as "reference broken".
find "$BS_PATH/.git" -maxdepth 1 -type f -name '*_HEAD' -empty -delete 2>/dev/null
# A truncated index fails every git command that reads it, reset --hard included; worktree untouched.
if ! _git ls-files >/dev/null 2>&1; then
    echo "$_tag index unreadable, rebuilding"
    rm -f "$BS_PATH/.git/index"
    _git reset -q 2>/dev/null
fi

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
    _git --literal-pathspecs checkout HEAD --pathspec-from-file=- <<<"$1"
}

# Resets to the first target that works, so one damaged target does not end the recovery.
_reset_chain() {
    local good
    find "$BS_PATH/.git/objects" -type f -empty -delete 2>/dev/null
    good=$(tr -d '[:space:]' 2>/dev/null <"$HOME_DIR/.cache/blockscreen/last_good_commit")
    if [[ -n "$good" ]] && _git cat-file -e "$good^{tree}" 2>/dev/null && _git reset -q --hard "$good"; then
        echo "$_tag reset to last good ${good:0:8}"
        return 0
    fi
    # Moonraker's soft recovery resets to the local remote ref without fetching; the network is rarely up yet.
    if [[ -n "$_branch" ]] && _git cat-file -e "refs/remotes/origin/$_branch^{tree}" 2>/dev/null \
        && _git reset -q --hard "refs/remotes/origin/$_branch"; then
        echo "$_tag reset to local origin/$_branch"
        return 0
    fi
    if [[ -n "$_branch" ]] && _as_owner timeout 60 git -C "$BS_PATH" fetch -q origin "$_branch" 2>/dev/null \
        && _git reset -q --hard "origin/$_branch"; then
        echo "$_tag reset to origin/$_branch"
        return 0
    fi
    echo "$_tag cannot heal offline, leaving recovery to the updater"
    return 1
}

healed=0
full=1
if [[ "$_ref_lost" == 1 ]] || ! _git cat-file -e 'HEAD^{tree}' 2>/dev/null; then
    echo "$_tag HEAD unreadable, pruning empty objects"
    _reset_chain && healed=1
else
    _broken=$(_broken_paths)
    # Units, the installer and its sources live in scripts/; other files need no redeploy.
    grep -q '^scripts/' <<<"$_broken" || full=0
    if [[ -n "$_broken" ]]; then
        echo "$_tag $(wc -l <<<"$_broken") empty tracked files, restoring from HEAD"
        if _restore "$_broken"; then
            healed=1
        else
            # Usually an emptied loose object: unpacked objects are not fsynced by default.
            echo "$_tag restore failed, resetting"
            full=1
            _reset_chain && healed=1
        fi
    fi
fi
[[ "$healed" == 1 ]] || exit 0

sync -f "$BS_PATH"
if [[ "$full" == 0 ]]; then
    echo "$_tag healed"
    exit 0
fi
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
