"""Tests for the BUG-10 helpers in bs-common.sh: Moonraker-pull hand-off, idle wait, stale stamps."""

from __future__ import annotations

import fcntl
import os
import re
import subprocess
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
_FN = _SCRIPTS / "bs-common.sh"


def _shim(tmp_path: Path, name: str, body: str) -> Path:
    shim = tmp_path / "bin"
    shim.mkdir(exist_ok=True)
    fake = shim / name
    fake.write_text(f"#!/bin/bash\n{body}\n")
    fake.chmod(0o755)
    return shim


def _run(tmp_path: Path, script: str, **env: str) -> subprocess.CompletedProcess[str]:
    path = f"{tmp_path / 'bin'}:{os.environ.get('PATH', '')}"
    return subprocess.run(
        ["bash", "-c", f'set -euo pipefail; . "{_FN}"; {script}'],
        capture_output=True,
        check=False,
        env={**os.environ, "PATH": path, **env},
        text=True,
        timeout=20,
    )


@pytest.mark.parametrize(
    ("line", "inside"),
    [
        ("0::/system.slice/moonraker.service", True),
        ("0::/system.slice/BlocksScreen-updater.service", False),
        ("0::/system.slice/bs-post-merge-0123456789ab.service", False),
        ("0::/user.slice/user-1000.slice/session-3.scope", False),
    ],
)
def test_moonraker_cgroup_detection(tmp_path: Path, line: str, inside: bool) -> None:
    cg = tmp_path / "cgroup"
    cg.write_text(line + "\n")
    res = _run(tmp_path, f'bs_in_moonraker_cgroup "{cg}"')
    assert (res.returncode == 0) is inside


def _triggers(tmp_path: Path) -> list[str]:
    res = _run(tmp_path, 'printf "%s\\n" "${BS_UPDATER_INSTALL_TRIGGERS[@]}"')
    return res.stdout.split()


def _grep_hits(regex: str, line: str) -> bool:
    res = subprocess.run(
        ["grep", "-E", regex], input=line + "\n", text=True, capture_output=True
    )
    return res.returncode == 0


def test_post_merge_trigger_regex_matches_exactly_the_array(tmp_path: Path) -> None:
    # post-merge derives its diff regex from the same array the stamp hash covers.
    merge = (_SCRIPTS / "post-merge").read_text()
    assert "bs_updater_install_trigger_regex" in merge
    assert "\\.service$" not in merge
    triggers = _triggers(tmp_path)
    assert len(triggers) == len(set(triggers)) >= 9
    regex = _run(tmp_path, "bs_updater_install_trigger_regex").stdout.strip()
    for name in triggers:
        assert _grep_hits(regex, f"scripts/{name}"), name
        decoys = [name + "x", "x" + name, name.replace(".", "_"), f"other/{name}"]
        for decoy in decoys:
            assert not _grep_hits(regex, f"scripts/{decoy}"), decoy


def test_install_hash_covers_every_trigger(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    triggers = _triggers(tmp_path)
    for name in triggers:
        (scripts / name).write_text("a\n")
    base = _run(tmp_path, f'bs_updater_install_hash "{scripts}"').stdout.strip()
    assert re.fullmatch(r"[0-9a-f]{32}", base)
    for name in triggers:
        (scripts / name).write_text("b\n")
        changed = _run(tmp_path, f'bs_updater_install_hash "{scripts}"').stdout.strip()
        assert changed != base, name
        (scripts / name).write_text("a\n")


def test_install_hash_changes_with_a_listed_file(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "install-updater.sh").write_text("a\n")
    first = _run(tmp_path, f'bs_updater_install_hash "{scripts}"').stdout
    (scripts / "unrelated.sh").write_text("x\n")
    assert _run(tmp_path, f'bs_updater_install_hash "{scripts}"').stdout == first
    (scripts / "install-updater.sh").write_text("b\n")
    assert _run(tmp_path, f'bs_updater_install_hash "{scripts}"').stdout != first


def _wait(
    tmp_path: Path, replies: list[str], cap: int = 1800, prints: list[str] | None = None
) -> tuple[int, int]:
    # curl replays one reply per call per endpoint ("fail" = unreachable); sleep is a no-op.
    feed = tmp_path / "replies"
    feed.write_text("\n".join(replies) + "\n")
    pfeed = tmp_path / "prints"
    pfeed.write_text("\n".join(prints or []) + "\n")
    count = tmp_path / "calls"
    count.write_text("")
    pcount = tmp_path / "pcalls"
    pcount.write_text("")
    _shim(
        tmp_path,
        "curl",
        f'case "$*" in *print_stats*) echo x >>"{pcount}"; '
        f'r=$(sed -n "$(wc -l <"{pcount}")p" "{pfeed}"); '
        '[ -z "$r" ] && exit 7; '
        'printf \'{"result":{"status":{"print_stats":{"state": "%s"}}}}\' "$r"; exit 0 ;; esac; '
        f'echo x >>"{count}"; r=$(sed -n "$(wc -l <"{count}")p" "{feed}"); '
        '[ "$r" = fail ] && exit 7; printf \'{"result":{"busy":%s}}\' "${r:-false}"',
    )
    _shim(tmp_path, "sleep", "exit 0")
    conf = tmp_path / "moonraker.conf"
    conf.write_text("[server]\nport: 7125\n")
    res = _run(tmp_path, f'bs_wait_moonraker_idle "{conf}" {cap}')
    return res.returncode, len(count.read_text().splitlines())


def test_wait_polls_until_moonraker_idle(tmp_path: Path) -> None:
    assert _wait(tmp_path, ["true", "true", "false"]) == (0, 3)


@pytest.mark.parametrize("replies", [["fail"], ["false"]])
def test_wait_returns_at_once_when_idle_or_down(
    tmp_path: Path, replies: list[str]
) -> None:
    assert _wait(tmp_path, replies) == (0, 1)


def test_wait_gives_up_at_the_cap(tmp_path: Path) -> None:
    assert _wait(tmp_path, ["true"] * 10, cap=10) == (1, 3)


def test_wait_holds_uncapped_while_printing_or_paused(tmp_path: Path) -> None:
    # Print time does not count against the cap: 5 print polls, then one idle update poll.
    prints = ["printing", "paused", "printing", "paused", "printing", "standby"]
    assert _wait(tmp_path, ["false"], cap=0, prints=prints) == (0, 1)


def _settle(
    tmp_path: Path, *, busy: str, pid_now: str, flag: bool = True
) -> tuple[bool, bool]:
    # Returns (moonraker restarted, owed flag still present); the patch happened at PID 100.
    log = tmp_path / "sudo.log"
    _shim(tmp_path, "sudo", f'echo "$*" >>"{log}"')
    _shim(tmp_path, "systemctl", f'echo "{pid_now}"')
    _shim(tmp_path, "sleep", "exit 0")
    _shim(
        tmp_path,
        "curl",
        f'case "$*" in *print_stats*) exit 7 ;; esac; printf \'{{"busy":{busy}}}\'',
    )
    conf = tmp_path / "moonraker.conf"
    conf.write_text("[server]\nport: 7125\n")
    owed = tmp_path / "owed"
    if flag:
        owed.write_text("100\n")
    _run(tmp_path, f'bs_settle_moonraker_restart "{conf}" "{owed}" 0 100')
    restarted = log.exists() and "restart moonraker" in log.read_text()
    return restarted, owed.exists()


def test_settle_restarts_when_moonraker_never_reloaded(tmp_path: Path) -> None:
    assert _settle(tmp_path, busy="false", pid_now="100") == (True, False)


def test_settle_skips_restart_after_moonraker_self_restart(tmp_path: Path) -> None:
    assert _settle(tmp_path, busy="false", pid_now="200") == (False, False)


def test_settle_keeps_the_debt_when_the_update_outlasts_the_cap(
    tmp_path: Path,
) -> None:
    assert _settle(tmp_path, busy="true", pid_now="100") == (False, True)


def test_settle_is_a_noop_without_debt(tmp_path: Path) -> None:
    assert _settle(tmp_path, busy="false", pid_now="100", flag=False) == (False, False)


def test_code_hash_matches_the_daemon(tmp_path: Path) -> None:
    from updater.__main__ import code_hash

    pkg = _SCRIPTS.parent / "updater"
    res = _run(tmp_path, f'bs_updater_code_hash "{_SCRIPTS.parent}"')
    assert res.stdout.strip() == code_hash(pkg)


def test_code_hash_parity_with_odd_filenames(tmp_path: Path) -> None:
    # A divergence from the daemon's hash means a restart loop, so cover spaces and case.
    from updater.__main__ import code_hash

    pkg = tmp_path / "repo" / "updater"
    pkg.mkdir(parents=True)
    for name, body in {
        "__main__.py": "a\n",
        "my mod.py": "space\n",
        "my.py": "dot\n",
        "Zed.py": "upper\n",
        "components.yaml": "k: v\n",
    }.items():
        (pkg / name).write_text(body)
    res = _run(tmp_path, f'bs_updater_code_hash "{pkg.parent}"')
    assert res.stdout.strip() == code_hash(pkg)


def _stale(tmp_path: Path, *, age: int, recorded: str | None) -> bool:
    # Daemon active for age s; recorded = its hash, 'match' = the tree's, None = absent.
    repo = tmp_path / "repo"
    (repo / "updater").mkdir(parents=True)
    (repo / "updater" / "a.py").write_text("x = 1\n")
    home = tmp_path / "home"
    rec = home / ".cache" / "blockscreen" / "updater-code-hash"
    rec.parent.mkdir(parents=True)
    if recorded == "match":
        from updater.__main__ import code_hash

        recorded = code_hash(repo / "updater")
    if recorded is not None:
        rec.write_text(recorded + "\n")
    uptime = float(Path("/proc/uptime").read_text().split()[0])
    since = max(int(uptime) - age, 1) * 1_000_000
    _shim(tmp_path, "systemctl", f'echo "{since}"')
    res = _run(tmp_path, f'bs_updater_code_stale "{repo}"', _BSENV_HOME=str(home))
    return res.returncode == 0


def test_code_stale_when_the_daemon_runs_other_code(tmp_path: Path) -> None:
    assert _stale(tmp_path, age=600, recorded="0" * 64)


def test_code_stale_when_an_old_daemon_never_recorded(tmp_path: Path) -> None:
    assert _stale(tmp_path, age=600, recorded=None)


def test_code_not_stale_for_a_fresh_daemon(tmp_path: Path) -> None:
    assert not _stale(tmp_path, age=5, recorded=None)


def test_code_not_stale_when_hashes_match(tmp_path: Path) -> None:
    assert not _stale(tmp_path, age=600, recorded="match")


def _busy(tmp_path: Path, *, held: bool = False) -> bool:
    # systemctl shim: the deploy unit is never active.
    _shim(tmp_path, "systemctl", "exit 3")
    home = tmp_path / "home"
    lock = home / ".cache" / "blockscreen" / "updater.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open("w") as f:
        if held:
            fcntl.flock(f, fcntl.LOCK_EX)
        res = _run(tmp_path, "bs_updater_install_busy", _BSENV_HOME=str(home))
    return res.returncode == 0


def test_install_busy_while_update_lock_held(tmp_path: Path) -> None:
    assert _busy(tmp_path, held=True)


def test_install_not_busy_when_idle(tmp_path: Path) -> None:
    assert not _busy(tmp_path)
