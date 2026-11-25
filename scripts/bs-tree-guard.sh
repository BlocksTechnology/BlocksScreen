#!/bin/bash
# shellcheck disable=SC2329 # the component heal is reached only through the EXIT trap
# Boot guard: restores tracked files a power cut left empty, before any unit runs from the tree.
# Installed outside the tree by install-updater.sh: an in-tree healer can be emptied by the same cut.
# Usage: bs-tree-guard.sh BS_PATH HOME_DIR. Always exits 0, a failed heal must not block boot.
set -uo pipefail

BS_PATH="${1:?usage: bs-tree-guard.sh BS_PATH HOME_DIR}"
HOME_DIR="${2:?usage: bs-tree-guard.sh BS_PATH HOME_DIR}"
_tag="[bs-tree-guard]"

# Root-run git would leave root-owned files the updater cannot rewrite; $1 is the tree's owner.
_as_user() {
    local user=$1
    shift
    if [[ "$(id -u)" == 0 && "$user" != root ]]; then runuser -u "$user" -- "$@"; else "$@"; fi
}

# Regular files in REPO that are empty on disk but not in HEAD, one per line.
_broken_paths() {
    local repo=$1 user=$2 meta path
    while IFS=$'\t' read -r -d '' meta path; do
        [[ "$meta" == 100* && "${meta##* }" != 0 ]] || continue
        [[ -f "$repo/$path" && ! -s "$repo/$path" ]] && printf '%s\n' "$path"
    done < <(_as_user "$user" git -C "$repo" ls-tree -r -l -z --full-tree HEAD)
}

# Git trees of the other components, read like load_components: bundled list, user override, home only.
# The user override is editable by the user, so paths must resolve under home and git runs as each tree's owner.
_component_repos() {
    local p home bs
    home=$(realpath -m -- "$HOME_DIR")
    bs=$(realpath -m -- "$BS_PATH")
    sed -n 's/^[[:space:]-]*path:[[:space:]]*//p' "$BS_PATH/updater/components.yaml" \
        "$HOME_DIR/printer_data/config/blockscreen_updater.yaml" 2>/dev/null |
        sed "s/[[:space:]]*#.*//; s/^[\"']//; s/[\"']$//" | sort -u |
        while IFS= read -r p; do
            [[ "$p" == \~/* ]] && p="$HOME_DIR/${p#\~/}"
            p=$(realpath -e -- "$p" 2>/dev/null) || continue
            [[ "$p" == "$home"/* && "$p" != "$bs" && -d "$p/.git" ]] && printf '%s\n' "$p"
        done
}

# Offline heal only: an unreadable HEAD needs the updater's boot repair (network, prev_hash).
_heal_component() {
    local repo=$1 user head_ref broken tag
    tag="$_tag $(basename "$repo"):"
    user=$(stat -c %U "$repo")
    rm -f "$repo/.git/index.lock"
    find "$repo/.git" -maxdepth 1 -type f -name '*_HEAD' -empty -delete 2>/dev/null
    head_ref=$(sed -n 's/^ref: //p' "$repo/.git/HEAD" 2>/dev/null)
    # The head ref is kept: once gone, git silently falls back to an older packed-refs commit.
    find "$repo/.git/refs" -type f -empty ! -path "$repo/.git/$head_ref" -delete 2>/dev/null
    if [[ -n "$head_ref" && -f "$repo/.git/$head_ref" && ! -s "$repo/.git/$head_ref" ]] \
        || ! _as_user "$user" git -C "$repo" cat-file -e 'HEAD^{tree}' 2>/dev/null; then
        echo "$tag HEAD unreadable, left to the updater's boot repair"
        return 0
    fi
    if ! _as_user "$user" git -C "$repo" ls-files >/dev/null 2>&1; then
        echo "$tag index unreadable, rebuilding"
        rm -f "$repo/.git/index"
        _as_user "$user" git -C "$repo" reset -q 2>/dev/null
    fi
    broken=$(_broken_paths "$repo" "$user")
    [[ -n "$broken" ]] || return 0
    if _as_user "$user" git -C "$repo" --literal-pathspecs checkout HEAD --pathspec-from-file=- <<<"$broken" 2>/dev/null; then
        sync -f "$repo"
        echo "$tag $(wc -l <<<"$broken") empty tracked files restored from HEAD"
    else
        echo "$tag $(wc -l <<<"$broken") empty tracked files, restore failed, needs an Update or a reclone"
    fi
}

_heal_components() {
    local repo
    while IFS= read -r repo; do _heal_component "$repo"; done < <(_component_repos)
}
# Runs on every exit below, so the list is read after the BlocksScreen heal restored components.yaml.
trap _heal_components EXIT

[[ -d "$BS_PATH/.git" ]] || exit 0

_owner=$(stat -c %U "$BS_PATH")
_as_owner() { _as_user "$_owner" "$@"; }
_git() { _as_owner git -C "$BS_PATH" "$@"; }

# Local branch names, loose and packed; read by hand since git refuses a repo with an empty HEAD.
_local_branches() {
    {
        (cd "$BS_PATH/.git/refs/heads" 2>/dev/null && find . -type f | sed 's|^\./||')
        sed -n 's|^[0-9a-f]* refs/heads/||p' "$BS_PATH/.git/packed-refs" 2>/dev/null
    } | sort -u
}

_branch_tip() {
    if [[ -f "$BS_PATH/.git/refs/heads/$1" ]]; then
        tr -d '[:space:]' <"$BS_PATH/.git/refs/heads/$1"
    else
        awk -v r="refs/heads/$1" '$2 == r { print $1 }' "$BS_PATH/.git/packed-refs" 2>/dev/null
    fi
}

# Branch an emptied HEAD named: the reflog's last checkout, the only local branch, or the one branch at HEAD's last tip.
_lost_head_branch() {
    local b branches tip
    branches=$(_local_branches)
    b=$(grep -aoE 'checkout: moving from [^ ]+ to [^ ]+$' "$BS_PATH/.git/logs/HEAD" 2>/dev/null | tail -n1)
    b=${b##* to }
    # A checkout to a commit or tag names no local branch, so it falls through.
    if [[ -z "$b" ]] || ! grep -qxF -- "$b" <<<"$branches"; then
        b=""
        [[ -n "$branches" && "$(wc -l <<<"$branches")" == 1 ]] && b=$branches
    fi
    if [[ -z "$b" ]]; then
        tip=$(grep -aoE '^[0-9a-f]{40,64} [0-9a-f]{40,64} ' "$BS_PATH/.git/logs/HEAD" 2>/dev/null |
            tail -n1 | cut -d' ' -f2)
        [[ -n "$tip" ]] || return 1
        b=$(while IFS= read -r x; do [[ "$(_branch_tip "$x")" == "$tip" ]] && printf '%s\n' "$x"; done <<<"$branches")
        [[ -n "$b" && "$(wc -l <<<"$b")" == 1 ]] || return 1
    fi
    git check-ref-format --branch "$b" >/dev/null 2>&1 && printf '%s' "$b"
}

# git reads an empty HEAD as "not a git repository", which would fail every step below.
if ! grep -qE '^(ref: refs/heads/.+|[0-9a-f]{40,64})$' "$BS_PATH/.git/HEAD" 2>/dev/null; then
    if _b=$(_lost_head_branch); then
        printf 'ref: refs/heads/%s\n' "$_b" | _as_owner tee "$BS_PATH/.git/HEAD" >/dev/null
        sync -f "$BS_PATH/.git"
        echo "$_tag HEAD damaged, pointed it back at $_b"
    else
        # The updater never repairs HEAD, so the journal line must say what a person has to do.
        echo "$_tag HEAD damaged and its branch unknown, needs a manual fix: echo 'ref: refs/heads/<branch>' > $BS_PATH/.git/HEAD"
        exit 0
    fi
fi

# Read before pruning: once an empty loose branch ref is gone, git falls back to an older packed-refs entry.
_head_ref=$(sed -n 's/^ref: //p' "$BS_PATH/.git/HEAD" 2>/dev/null)
_branch=${_head_ref#refs/heads/}
_ref_lost=0
[[ -n "$_head_ref" && -f "$BS_PATH/.git/$_head_ref" && ! -s "$BS_PATH/.git/$_head_ref" ]] && _ref_lost=1
# The commit the tree was on, to tell a reset from a rollback; a lost ref keeps it only in its reflog.
if [[ "$_ref_lost" == 1 ]]; then
    _installed=$(grep -aoE '^[0-9a-f]{40,64} [0-9a-f]{40,64} ' "$BS_PATH/.git/logs/$_head_ref" 2>/dev/null |
        tail -n1 | cut -d' ' -f2)
else
    _installed=$(_git rev-parse -q --verify HEAD 2>/dev/null)
fi

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

# Literal pathspecs: a tracked name with glob characters must not match other files.
_restore() {
    _git --literal-pathspecs checkout HEAD --pathspec-from-file=- <<<"$1"
}

# Resets to the first target that works, so one damaged target does not end the recovery.
_reset_chain() {
    local good was=${_installed:0:8}
    find "$BS_PATH/.git/objects" -type f -empty -delete 2>/dev/null
    good=$(tr -d '[:space:]' 2>/dev/null <"$HOME_DIR/.cache/blockscreen/last_good_commit")
    if [[ -n "$good" ]] && _git cat-file -e "$good^{tree}" 2>/dev/null && _git reset -q --hard "$good"; then
        if [[ "$good" == "$_installed" ]]; then
            echo "$_tag reset to last good ${good:0:8}"
        else
            # A cut right after a pull lands here before the new commit is blessed; Update re-applies it.
            echo "$_tag rolled back to last good ${good:0:8} from ${was:-an unknown commit}"
        fi
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
    _broken=$(_broken_paths "$BS_PATH" "$_owner")
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
