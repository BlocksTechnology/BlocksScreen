#!/usr/bin/env bash
# make pr: guided pull request creation matching the repo's title lint, labels and PR template.
set -euo pipefail

if ((BASH_VERSINFO[0] < 4 || (BASH_VERSINFO[0] == 4 && BASH_VERSINFO[1] < 4))); then
    echo "error: bash 4.4 or newer is required (found $BASH_VERSION)" >&2
    exit 1
fi
# Without this a failed prompt inside $(...) is ignored and menus loop forever on EOF.
shopt -s inherit_errexit

usage() {
    cat <<'EOF'
Usage: make pr

Opens a pull request for the current branch, step by step:
  1. Checks       gh login, push access, branch, uncommitted changes, base branch, existing PR
  2. Title        one line, type(scope)!: summary as enforced by the PR title lint; also the
                  commit message when you chose to commit your uncommitted changes
  3. Labels       area label (type and breaking come from the title), reviewers, draft; you are the assignee
  4. Local gates  optional make check before anything leaves your machine
  5. Description  the PR template in your editor, Changes prefilled from your commits
  6. Review       every commit and setting is shown; nothing is pushed until you type y

Requires git, the GitHub CLI (gh) logged in, and push access to origin.
EOF
}

case ${1:-} in
    -h | --help) usage; exit 0 ;;
    "") ;;
    *) usage >&2; exit 2 ;;
esac

if [[ -t 2 && -z ${NO_COLOR:-} ]]; then
    BOLD=$'\e[1m' DIM=$'\e[2m' RED=$'\e[31m' GREEN=$'\e[32m' YELLOW=$'\e[33m' CYAN=$'\e[36m' RESET=$'\e[0m'
else
    BOLD="" DIM="" RED="" GREEN="" YELLOW="" CYAN="" RESET=""
fi

# The menus bind fzf's load event and pos() action, both 0.36+; older fzf gets the numbered lists.
USE_FZF=0
if [[ -t 0 && -t 2 ]] && command -v fzf >/dev/null &&
    printf '%s\n' 0.36 "$(fzf --version | cut -d' ' -f1)" | sort -VC; then
    USE_FZF=1
fi

# All output goes to stderr so that functions can return values on stdout.
say() { printf '%s\n' "$*" >&2; }
ok() { say "  ${GREEN}✔${RESET} $*"; }
warn() { say "  ${YELLOW}!${RESET} $*"; }
die() { say "  ${RED}✖ $*${RESET}"; exit 1; }
step() { say ""; say "${BOLD}[$1/6] $2${RESET}"; }
row() { printf '  %s%-12s%s %s\n' "$DIM" "$1" "$RESET" "$2" >&2; }

trim() {
    local s=$1
    s=${s#"${s%%[![:space:]]*}"}
    printf '%s' "${s%"${s##*[![:space:]]}"}"
}

# ask PROMPT [DEFAULT]: one trimmed line from the user; EOF aborts.
ask() {
    local reply hint=""
    if [[ -n ${2:-} ]]; then hint=" ${DIM}[$2]${RESET}"; fi
    read -rp "  ${CYAN}?${RESET} $1$hint: " reply || die "no input, aborting"
    reply=$(trim "$reply")
    printf '%s' "${reply:-${2:-}}"
}

# confirm PROMPT DEFAULT(y|n)
confirm() {
    local reply hint="y/N"
    if [[ $2 == y ]]; then hint="Y/n"; fi
    while true; do
        read -rp "  ${CYAN}?${RESET} $1 ${DIM}[$hint]${RESET} " reply || die "no input, aborting"
        case ${reply:-$2} in
            [yY] | [yY][eE][sS]) return 0 ;;
            [nN] | [nN][oO]) return 1 ;;
        esac
        say "    Answer y or n."
    done
}

# menu PROMPT DEFAULT_INDEX OPTION...: prints the chosen 0-based index; arrow keys via fzf, else a numbered list.
menu() {
    local prompt=$1 default=$2 reply i
    local -a options=("${@:3}")
    if ((USE_FZF)); then
        # The index travels hidden in field 1, so the visible label never has to be parsed back.
        reply=$(for i in "${!options[@]}"; do printf '%d\t%s\n' "$i" "${options[i]}"; done |
            fzf --height=~20 --layout=reverse --no-sort --delimiter='\t' --with-nth=2.. \
                --prompt="  ? $prompt > " --header="↑/↓ move, type to filter, Enter select, Esc abort" \
                --bind "load:pos($((default + 1)))") || die "nothing selected, aborting"
        say "  ${CYAN}?${RESET} $prompt: ${reply#*$'\t'}"
        printf '%s' "${reply%%$'\t'*}"
        return
    fi
    for i in "${!options[@]}"; do
        printf '    %s%d)%s %s\n' "$CYAN" $((i + 1)) "$RESET" "${options[i]}" >&2
    done
    while true; do
        reply=$(ask "$prompt" $((default + 1)))
        # 10# keeps "08" from being parsed as an invalid octal number.
        if [[ $reply =~ ^[0-9]+$ ]] && ((10#$reply >= 1 && 10#$reply <= ${#options[@]})); then
            printf '%s' $((10#$reply - 1))
            return
        fi
        say "    Enter a number from 1 to ${#options[@]}."
    done
}

# pick PROMPT OPTION...: prints the chosen options comma-separated, or nothing; Tab marks several in fzf.
pick() {
    local prompt=$1 reply i joined
    local -a options=("${@:2}") chosen=() numbers=()
    if ((USE_FZF)); then
        # Enter with nothing marked returns the line under the cursor, hence the "(none)" line on top.
        reply=$(printf '%s\n' "(none)" "${options[@]}" |
            fzf --multi --height=~20 --layout=reverse --no-sort \
                --prompt="  ? $prompt > " --header="↑/↓ move, Tab mark, Enter confirm, Esc abort") ||
            die "nothing selected, aborting"
        while read -r i; do
            if [[ $i != "(none)" ]]; then chosen+=("$i"); fi
        done <<<"$reply"
    else
        for i in "${!options[@]}"; do
            printf '    %s%d)%s %s\n' "$CYAN" $((i + 1)) "$RESET" "${options[i]}" >&2
        done
        while true; do
            reply=$(ask "$prompt, numbers separated by spaces (Enter for none)")
            read -ra numbers <<<"${reply//,/ }"
            chosen=()
            for i in "${numbers[@]}"; do
                if [[ $i =~ ^[0-9]+$ ]] && ((10#$i >= 1 && 10#$i <= ${#options[@]})); then
                    chosen+=("${options[10#$i - 1]}")
                else
                    say "    Enter numbers from 1 to ${#options[@]}."
                    continue 2
                fi
            done
            break
        done
    fi
    joined=$(IFS=,; printf '%s' "${chosen[*]}")
    say "  ${CYAN}?${RESET} $prompt: ${joined:-none}"
    printf '%s' "$joined"
}

# True when Description has text besides its type boxes and HTML comments, which may span lines.
has_summary() {
    awk '
        /^#+ / { in_summary = ($0 == "# Description"); next }
        in_summary && /^- \[[ xX]\] / { next }
        in_summary {
            line = $0; text = ""
            while (line != "") {
                if (in_comment) {
                    end = index(line, "-->")
                    if (!end) break
                    line = substr(line, end + 3); in_comment = 0
                } else {
                    start = index(line, "<!--")
                    if (!start) { text = text line; break }
                    text = text substr(line, 1, start - 1)
                    line = substr(line, start + 4); in_comment = 1
                }
            }
            if (text ~ /[^[:space:]]/) found = 1
        }
        END { exit !found }
    ' "$1"
}

# set_gates_box FILE: tick the make check box only when this run's gates passed, also in a reused draft.
set_gates_box() {
    GATES=$gates awk '
        /^- \[[ xX]\] `make check`/ { sub(/\[[ xX]\]/, ENVIRON["GATES"] == "passed" ? "[x]" : "[ ]") }
        { print }
    ' "$1" >"$1.tmp" && mv "$1.tmp" "$1"
}

cd "$(git rev-parse --show-toplevel)"
readonly TEMPLATE=.github/pull_request_template.md
readonly TITLE_MAX=72
readonly TYPES=(feat fix perf refactor docs test chore)
# The PR title lint's rule: a listed type, optional (scope), optional ! for breaking, then ": summary".
TITLE_RE="^($(IFS='|'; printf '%s' "${TYPES[*]}"))(\(([^()]+)\))?(!)?: [^ ]"
readonly TITLE_RE
declare -rA TYPE_LABEL=(
    [feat]=enhancement [fix]=bug [perf]=performance [refactor]=refactor
    [docs]=documentation [test]=testing [chore]=chore
)
# The template's Description checkbox each title type ticks; perf, test and chore have none.
declare -rA TYPE_BOX=([feat]=Feature [fix]="Bug Fix" [refactor]="Code Refactor" [docs]=Documentation)
readonly AREAS=(none ui updater network ci dependencies)

branch="" pushed=0 committed=0
on_exit() {
    local status=$?
    if ((status == 0)); then return; fi
    if ((pushed)); then
        warn "'$branch' was pushed but the PR was not created. Run make pr again to retry with the same description."
    elif ((committed)); then
        warn "Aborted. Nothing was pushed; the new commit stays on '$branch' (undo it with: git reset --soft HEAD~1)."
    else
        warn "Aborted. Nothing was pushed."
    fi
}
trap on_exit EXIT
trap 'say ""; exit 130' INT

# ── 1. Checks ────────────────────────────────────────────────────────────────
step 1 "Checks"
command -v gh >/dev/null || die "the GitHub CLI is required: https://cli.github.com"
# --hostname: a stale token for another host must not block a valid github.com login.
gh auth status --hostname github.com >/dev/null 2>&1 || die "gh is not logged in; run: gh auth login"

branch=$(git branch --show-current)
case $branch in
    "") die "HEAD is detached; switch to your feature branch first" ;;
    main | dev | stage | Release-* | Release/*) die "'$branch' is a shared branch; work on a feature branch (git switch -c fix/short-name)" ;;
esac

origin=$(git remote get-url origin 2>/dev/null) || die "this clone has no 'origin' remote"
repo_info=$(gh repo view "$origin" --json nameWithOwner,viewerPermission,isFork,parent \
    --jq '"\(.nameWithOwner) \(.viewerPermission) \(.isFork) \(.parent.owner.login // "")/\(.parent.name // "")"') ||
    die "cannot read $origin on GitHub"
read -r repo permission is_fork parent <<<"$repo_info"
# gh would open the PR inside the fork, against the fork's own base branch.
if [[ $is_fork == true ]]; then die "origin is a fork of $parent; open the PR on GitHub, or point origin at $parent"; fi
case $permission in
    ADMIN | MAINTAIN | WRITE) ;;
    *) die "you have no push access to $repo; push to your fork and open the PR on GitHub" ;;
esac
ok "Logged in with push access to $repo"

existing_pr=$(gh pr list -R "$repo" --head "$branch" --state open --json url --jq '.[0].url // empty')
if [[ -n $existing_pr ]]; then
    ok "'$branch' already has an open pull request: $existing_pr"
    say "    New commits appear there after a plain 'git push'."
    exit 0
fi

dirty=0 commit_mode=none
if [[ -n $(git status --porcelain --untracked-files=no) ]]; then
    dirty=1
    warn "You have uncommitted changes (left column staged, right column not staged):"
    git status --short --untracked-files=no | sed 's/^/      /' >&2
    # Untracked files are never added: a stray local file must not end up in a PR by accident.
    say "    ${DIM}New files are not listed; git add them first if they belong in the PR.${RESET}"
    options=() modes=()
    if ! git diff --cached --quiet; then
        options+=("Commit the staged changes only")
        modes+=(staged)
    fi
    if ! git diff --quiet; then
        options+=("Stage every change above and commit it")
        modes+=(tracked)
    fi
    options+=("Leave them out of the PR")
    modes+=(none)
    index=$(menu "Uncommitted changes" 0 "${options[@]}")
    commit_mode=${modes[index]}
    if [[ $commit_mode != none ]]; then ok "They are committed in step 2, with the PR title as the message"; fi
fi

# One fetch for all branches: every call to origin can ask for the SSH key passphrase again.
# git's own error stays visible: a network or auth failure is not a missing branch.
git fetch -q --prune origin || die "could not fetch origin (see the error above)"
# dev is first and preselected, so Enter is the usual PR; the rest, most recently active first, are for stacked PRs.
bases=(dev)
while read -r ref; do
    if [[ $ref != HEAD && $ref != dev && $ref != "$branch" ]]; then bases+=("$ref"); fi
done < <(git for-each-ref --sort=-committerdate --format='%(refname:strip=3)' refs/remotes/origin/)

while true; do
    index=$(menu "Merge $branch into" 0 "${bases[@]}")
    base=${bases[index]}
    case $base in
        main | stage | Release-* | Release/*)
            warn "'$base' only receives promotions (dev -> stage -> production); feature work targets dev."
            confirm "Target '$base' anyway?" n || continue
            ;;
    esac
    break
done

commit_count=$(git rev-list --count "origin/$base..HEAD")
if [[ $commit_mode != none ]]; then
    ok "$branch is $commit_count commit(s) ahead of origin/$base, plus the one you are about to make"
else
    ((commit_count > 0)) || die "'$branch' has no commits that are not already on $base; commit your work first"
    ok "$branch is $commit_count commit(s) ahead of origin/$base"
fi
behind=$(git rev-list --count "HEAD..origin/$base")
if ((behind > 0)); then warn "It is also $behind commit(s) behind; rebase if GitHub reports conflicts."; fi

repo_labels=$(gh label list -R "$repo" --limit 500 --json name --jq '.[].name')

# ── 2. Title ─────────────────────────────────────────────────────────────────
step 2 "Title"
# Prefilled: a one-commit PR reuses its subject, otherwise the type is guessed from the branch name.
initial=""
if [[ $commit_mode == none ]] && ((commit_count == 1)); then
    initial=$(git log -1 --format=%s)
else
    case ${branch%%/*} in
        feat | feature) initial="feat: " ;;
        fix | bugfix | hotfix) initial="fix: " ;;
        perf) initial="perf: " ;;
        refactor | ref) initial="refactor: " ;;
        docs | doc) initial="docs: " ;;
        test | tests) initial="test: " ;;
        chore | ci | build) initial="chore: " ;;
    esac
fi
say "    ${DIM}type(scope): summary, type is one of: ${TYPES[*]}; a ! before the colon marks a breaking change${RESET}"
if [[ $commit_mode != none ]]; then say "    ${DIM}It is also the message of the commit made now.${RESET}"; fi
while true; do
    # \001 and \002 tell readline the colour codes take no space, else editing a long line garbles it.
    read -erp $'  \001'"$CYAN"$'\002?\001'"$RESET"$'\002 Title: ' -i "$initial" title || die "no input, aborting"
    title=$(trim "$title")
    title=${title%.}
    initial=$title
    if [[ ! $title =~ $TITLE_RE ]]; then
        warn "Use type(scope): summary, e.g. fix(ui): keep the spool weight after a reload"
        continue
    fi
    type=${BASH_REMATCH[1]} scope=${BASH_REMATCH[3],,} breaking=${BASH_REMATCH[4]}
    if ((${#title} <= TITLE_MAX)); then break; fi
    warn "The title is ${#title} characters; aim for $TITLE_MAX or fewer."
    if confirm "Keep it anyway?" n; then break; fi
done

if [[ $commit_mode != none ]]; then
    # Committed here, before the gates, so step 4 tests exactly what gets pushed.
    if [[ $commit_mode == tracked ]]; then git add -u; fi
    git commit -q -m "$title" || die "git commit failed (see the error above); nothing was committed"
    committed=1
    ok "Committed $(git log -1 --format='%h %s')"
    commit_count=$(git rev-list --count "origin/$base..HEAD")
    dirty=0
    if [[ -n $(git status --porcelain --untracked-files=no) ]]; then dirty=1; fi
fi

# ── 3. Labels and reviewers ──────────────────────────────────────────────────
step 3 "Labels and reviewers"
default=0
for i in "${!AREAS[@]}"; do
    if [[ ${AREAS[i]} == "$scope" ]]; then default=$i; fi
done
index=$(menu "Area" "$default" "${AREAS[@]}")
labels=("${TYPE_LABEL[$type]}")
if ((index > 0)); then labels+=("${AREAS[index]}"); fi
if [[ -n $breaking ]]; then labels+=(breaking); fi

# A label missing on the repo would make gh fail after the push, so drop it up front.
apply=()
for label in "${labels[@]}"; do
    if grep -qxF "$label" <<<"$repo_labels"; then
        apply+=("$label")
    else
        warn "Label '$label' does not exist on $repo yet; skipped."
    fi
done

me=$(gh api user --jq .login)
# GitHub rejects a review request to the PR author, so you are left off the list.
people=()
if collaborators=$(gh api "repos/$repo/collaborators" --paginate --jq '.[].login'); then
    while read -r login; do
        if [[ -n $login && ${login,,} != "${me,,}" ]]; then people+=("$login"); fi
    done <<<"$collaborators"
else
    warn "Could not list collaborators; request reviews on GitHub once the PR is open."
fi
reviewers=""
if ((${#people[@]})); then reviewers=$(pick "Reviewers" "${people[@]}"); fi

draft=no
if confirm "Open as a draft (not ready for review yet)?" n; then draft=yes; fi

# ── 4. Local gates ───────────────────────────────────────────────────────────
step 4 "Local gates"
gates="not run"
if confirm "Run make check now (the CI gates, a few minutes)?" y; then
    if make --no-print-directory check; then
        # The gates ran on the working tree, so a dirty tree did not test exactly what is pushed.
        if ((dirty)); then
            gates="passed with uncommitted changes"
            warn "Gates passed, but on a tree with uncommitted changes; the PR box stays unticked."
        else
            gates=passed
            ok "All gates passed"
        fi
    else
        gates=failed
        warn "Local gates failed; CI will fail the same way."
        confirm "Continue anyway?" n || exit 1
    fi
fi

# ── 5. Description ───────────────────────────────────────────────────────────
step 5 "Description"
body="$(git rev-parse --git-dir)/PR_BODY-${branch//\//-}.md"
if [[ -s $body ]] && confirm "Reuse the description from your previous attempt?" y; then
    ok "Reusing $body"
else
    COMMITS=$(git log --reverse --no-merges --format='- %s' "origin/$base..HEAD") BOX=${TYPE_BOX[$type]:-} awk '
        skip && $0 == "-" { skip = 0; next }
        { skip = 0 }
        ENVIRON["BOX"] != "" && $0 == ("- [ ] " ENVIRON["BOX"]) { $0 = "- [x] " ENVIRON["BOX"] }
        { print }
        $0 == "## Changes" { print ENVIRON["COMMITS"]; skip = 1 }
    ' "$TEMPLATE" >"$body"
fi
set_gates_box "$body"
editor=$(git var GIT_EDITOR)
while true; do
    say "    Opening $editor; save and close it to continue."
    sh -c "$editor \"\$1\"" editor "$body" || die "the editor failed; your draft is kept at $body"
    if has_summary "$body"; then break; fi
    warn "The Description has no summary; reviewers need the what and the why."
    confirm "Open the editor again?" y || exit 1
done
ok "Description ready"

# ── 6. Review ────────────────────────────────────────────────────────────────
step 6 "Review"
labels_text=$(IFS=,; printf '%s' "${apply[*]}")
labels_text=${labels_text//,/, }
row Repository "$repo"
row Title "$title"
row Base "$base <- $branch"
row Labels "${labels_text:-none}"
row Assignee "$me"
row Reviewers "${reviewers:-none}"
row Draft "$draft"
row "Local gates" "$gates"
say ""
say "  ${BOLD}Commits in this PR ($commit_count)${RESET}"
git log --reverse --format='    %h %s' "origin/$base..HEAD" >&2
say ""
# Default no: the push is the one step that cannot be taken back.
confirm "Push '$branch' to origin and open this pull request?" n || exit 1

git push -u origin "$branch" ||
    die "push rejected; if origin/$branch has commits you lack, run 'git pull --rebase' and retry (never force-push a shared branch)"
pushed=1

args=(-R "$repo" --base "$base" --head "$branch" --title "$title" --body-file "$body" --assignee "$me")
for label in "${apply[@]}"; do args+=(--label "$label"); done
if [[ -n $reviewers ]]; then args+=(--reviewer "$reviewers"); fi
if [[ $draft == yes ]]; then args+=(--draft); fi
url=$(gh pr create "${args[@]}")
rm -f "$body"
say ""
ok "${BOLD}Pull request opened:${RESET} $url"
