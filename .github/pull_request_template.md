<!-- Title: type(scope): summary, types: feat fix docs refactor test chore perf. Base branch: dev.
     `make pr` fills the title, base, labels, reviewers and the change list for you. -->

# PR Checklist
<!-- Delete this section once everything is ticked -->
- [ ] Title follows Conventional Commits, e.g. `fix(updater): retry apt lock on timeout`; CI rejects anything else
- [ ] Opened from a feature, bugfix or refactor branch against **dev**
- [ ] Labels added and a reviewer requested
- [ ] `make check` passes
- [ ] CI results checked once the PR is open; failing checks mean changes requested

# Description
- [ ] Feature
- [ ] Bug Fix
- [ ] Code Refactor
- [ ] Documentation

<!-- Summary of the changes and the issue they fix. A bug from another PR: reference it as #123.
     "Closes #123" only works on PRs into main, so close issues manually after merging into dev -->

## Changes
-

# Motivation
<!-- Why this change is needed. Delete if not applicable -->

# Tests
<!-- Tests run with logs or reports, and the setup: simulator or printer, config. Delete if not applicable -->
- [ ] Tested on simulator / printer

# Screenshots
<!-- UI changes only. Delete if not applicable -->

# Future work
<!-- Follow-ups tied to this PR, non-breaking only. Delete if not applicable -->
