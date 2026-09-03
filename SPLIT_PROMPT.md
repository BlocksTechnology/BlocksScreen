Split PR #306 (branch `fix/network-manager-hardening`, head `f863e99`) into a stack of 6
smaller PRs. #306 is 2299/1075 across 10 files with 158 hunks in `worker.py` alone, too big
to review. Do not modify `f863e99` - it is the frozen reference for the full combined diff.

## Hard rules
- NEVER run `git commit`, `git push`, or anything writing to a remote. I commit and push
  manually. Create branches locally, stage nothing, and give me one-line
  `type(scope): summary` commit messages to run myself.
- Comments: one-liners only, and only where genuinely necessary. No em dashes.
- The network layer stays fully async on sdbus signal watching. Do not introduce
  `sdbus_block`. Do not change the sdbus 0.14.1 pin. Do not redesign to polling.
- Behaviour must not change across the whole stack. The end state of PR 5 must be diff-identical
  to `f863e99` for the 10 files involved. Verify with `git diff f863e99 <final-branch-head>`
  at the end - it must be empty.

## Split by theme, not by commit
The 18 commits interleave: `afbb3ed → a0df3f3 → da76dec → cd49b35 → 7ac1839` is one chain of
successive fixes to the same ethernet bug, so cherry-picking commits reproduces the
intermediate broken states. Split by theme instead.

Stacked: each branch off the previous, all targeting `dev`. PRs 2-6 all touch the same
`worker.py` regions so they cannot be independent. Each PR body must say "stacked on #N,
review after it merges".

Target roughly 250-650 changed lines per PR. Sizes below are estimates from `git diff --numstat`
plus per-method line spans; the named new methods account for only 762 of `worker.py`'s 1720
changed lines, so the remaining ~958 lines of in-place edits are the least certain part of the
allocation. If a PR lands above ~700 lines, split it further rather than shipping it oversized.

1. `feat(keyboard): full-screen numeric keypad for IP and mask fields`  (~240 lines)
   `keyboardPage.py`, `tests/util/test_keyboard_page_unit.py`, plus the ~15-line
   `_on_show_keyboard(numeric=True)` hunk in `networkWindow.py` (~L3705/L3752-3758). That
   hunk is the only keyboard/network coupling and is additive - it needs no worker change.
   Merges first, independent of the rest.

2. `chore(network): drop per-poll debug logs and add missing docstrings`  (~300-400 lines)
   The per-poll debug-log removal that was spamming the log directory, comment compression to
   one-liners, and ALL the docstring additions from `f863e99`. Goes early on purpose: it buys
   the docstr-coverage margin that every later PR needs (see the trap below). Safest and most
   mechanical PR in the stack.

3. `refactor(network): extract helpers and cut cyclomatic complexity`  (~600-700 lines)
   Behaviour-neutral motion only. The complexity-extraction helpers: `_gather_ap_properties`,
   `_gather_settings`, `_backup_and_drop_existing`, `_rollback_failed_add`, `_backup_profile`,
   `_restore_profile`, `_vlan_*`, `_prefix_to_mask`, `_parse_ipv4_settings`, `_unwrap`,
   `_setting`, `_delete_connections_where`, `_delete_all_connections_by_id`, `_find_ap_props`,
   `_reload_connections`. Plus `models.py`. Each extracted helper needs its own docstring here -
   PR 2 covers pre-existing gaps, not methods this PR introduces. Reviewer should be able to
   read the whole thing as pure motion.

4. `fix(network): enforce one active link and persist ethernet-off intent`  (~450 lines)
   `_set_wired_profiles_autoconnect`, `_ensure_wired_autoconnect`, the exclusivity logic in
   `manager.py`/`worker.py`, and the `networkWindow.py` toggle handlers including the loading
   guard armed before link changes. Highest review value - this is where the field bugs were.
   Policy: exactly one of Wi-Fi / ethernet / hotspot active, enforced on USER TOGGLES ONLY.
   Background and automatic state handlers must never drop a link behind the user's back.

5. `fix(network): recover stale D-Bus paths and support full radio off`  (~550 lines)
   `_primary_paths_alive`, `_log_stale`, `_recover_signal_sources`, `_cached_path_is_valid`,
   `_device_path_for_iface`, `_reset_signal_proxies`, `_async_bootstrap`,
   `_wifi_hardware_enabled`, `_ensure_networking_enabled`, `_wifi_enable_preflight`,
   `_apply_wifi_radio`, `_log_radio_state`, `_scan_networks_once`, `_request_scan_if_allowed`.
   Plus `tests/network/test_sdbus_integration.py`.

6. `fix(network): show live signal strength and classify auth failures`  (~600 lines)
   `_active_ap_signal`, `_wifi_signal_and_security`, `_signal_map_once`, `_read_connectivity`,
   `_is_wifi_ap_mode`, `_wifi_activation_failed`, `_wifi_device_state`, `_classify_settings_error`,
   `_validate_psk`, `_resolve_current_ip`, `_wait_for_profile_ip`, remaining `networkWindow.py`
   display code, `tests/network/test_network_ui.py`.

`tests/network/test_worker_unit.py` (+466/-63) splits across 3-6, each test landing with the code
it covers. `tests/network/conftest.py` fixtures go to the earliest PR that needs them.
`networkWindow.py` (+312/-318) splits across 1, 4 and 6.

## Gates - run per branch, not once at the end
Every PR must pass all 5 gates standing alone:
- `.venv/bin/ruff check .` and `.venv/bin/ruff format --diff .`
- `.venv/bin/pylint -j$(nproc) --recursive=y BlocksScreen/` (baseline 8.31/10, must not drop)
- `.venv/bin/pytest tests/ --doctest-modules --cov=BlocksScreen/` (baseline 1515 passed, 30 skipped)
- `.venv/bin/docstr-coverage BlocksScreen/ --exclude '.*/BlocksScreen/lib/ui/.*' --fail-under=80 --skip-magic --skip-init --skip-private --skip-property`
- `.venv/bin/bandit -c pyproject.toml -r . -o /tmp/bandit.json -f json` then filter out `.venv`
  paths in Python. Piping `-f json` to stdout yields nothing, and `[tool.bandit] exclude_dirs`
  does not exclude `.venv`.

TRAP: docstr-coverage baseline is 80.1% against `--fail-under=80` - one docstring from red. This
is why PR 2 lands the docstring work before anything else. Check this gate on every branch, PR 1
included.

Also keep `ruff check --select C901 --isolated --target-version=py311` clean over
`BlocksScreen/lib/network/`, `networkWindow.py` and `keyboardPage.py` (threshold 10, not a CI gate).

## PR bodies
Read `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md` first and follow it; drop the
checklist section as the template instructs, and delete any section marked not applicable.
Titles must be Conventional Commits (`feat|fix|docs|refactor|test|chore|perf`) - CI enforces this
and it drives version bumps. Keep bodies as summarised as possible.

The RF50 result (168 pass / 0 fail / 5 skip, 7m29s, zero tracebacks, RSS steady at 21.6 MB) belongs
to the COMBINED head. Cite it as such in each body, do not claim it as per-PR validation. I will
re-run the harness once on the final stacked head.

Carry these into the last PR's Future work: AP-mode hotspot detection and the toggle-bounce fix are
both deployed but UNVERIFIED on hardware; the 5 skipped radio-cycling phases need console or
ethernet SSH; coalesce the redundant `_build_signal_map` fan-out; stale-path recovery double-logs
the same warning at an identical timestamp; `NameOwnerChanged` would be a cleaner NM-restart trigger;
`worker.py` still wants a structural split. Expect a merge conflict with #245 (performance).

## Do not touch
`scripts/healthcheck/` (separate work), anything under `.semgrep/` (local-only, never committed),
`bs-net-test.sh` (deliberately untracked via `.git/info/exclude`), `Makefile` and `pyproject.toml`
(reserved for #245).
