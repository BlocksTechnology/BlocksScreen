"""UpdateService end to end against real git repos: update, rollback, heal, install."""

UI_FILES = {
    "updater/dbus_service.py": "# marker\n",
    "scripts/install-updater.sh": "v1\n",
}


def _klipper(harness, **fields: object):
    """Installed klipper one commit behind its origin; returns (origin, old, new)."""
    origin = harness.remote("klipper")
    harness.install(origin)
    old = harness.head("klipper")
    new = origin.commit({"klippy.py": "v2\n"})
    harness.component("klipper", service="klipper.service", **fields)
    return origin, old, new


def _rollbacks(harness, name: str) -> list[dict]:
    return [
        e
        for e in harness.history()
        if e["component"] == name and e["event"] == "rollback"
    ]


async def test_update_moves_to_origin_tip_and_restarts(harness):
    _, old, new = _klipper(harness)
    harness.venv_pip("klipper")
    svc, rec = harness.service()

    assert await svc.update_all({"klipper"}) is True

    assert harness.head("klipper") == new
    assert harness.state_file()["klipper"]["prev_hash"] == old
    assert harness.events("klipper") == ["update_start", "update_success"]
    assert not harness.inflight.exists()
    assert [s[1] for s in rec.of("on_step")] == [1, 2, 3, 4]
    assert rec.of("on_component_done") == [("klipper", True)]
    calls = harness.calls()
    assert "systemctl restart klipper.service" in calls
    assert "systemctl is-active klipper.service" in calls
    # No requirements.txt: the venv is found but pip is never asked to install.
    assert not [c for c in calls if c.startswith("venv-pip")]


async def test_deps_install_runs_component_venv_pip(harness):
    origin, _, _ = _klipper(harness)
    req = origin.commit({"requirements.txt": "pyserial\n"})
    harness.venv_pip("klipper")
    svc, _ = harness.service()

    assert await svc.update_all({"klipper"}) is True

    assert harness.head("klipper") == req
    req_path = harness.home / "klipper" / "requirements.txt"
    assert f"venv-pip install -r {req_path} --quiet" in harness.calls()


async def test_hook_failure_reverts(harness):
    _, old, _ = _klipper(harness)
    harness.hook("klipper", "exit 3\n")
    svc, rec = harness.service()

    assert await svc.update_all({"klipper"}) is False

    assert harness.head("klipper") == old
    [rb] = _rollbacks(harness, "klipper")
    assert (rb["reason"], rb["reverted_to"], rb["ok"]) == ("hook", old[:12], True)
    assert rec.of("on_error") == [("klipper", "hook")]
    assert rec.of("on_rollback") == [("klipper", True)]
    assert "systemctl restart klipper.service" not in harness.calls()
    assert not harness.inflight.exists()


async def test_hook_receives_hashes(harness):
    _, old, new = _klipper(harness)
    out = harness.root / "hook.env"
    harness.hook(
        "klipper",
        f'echo "$COMPONENT_NAME $PREV_HASH $NEW_HASH $COMPONENT_PATH" >"{out}"\n',
    )
    svc, _ = harness.service()

    assert await svc.update_all({"klipper"}) is True

    assert out.read_text().split() == [
        "klipper",
        old,
        new,
        str(harness.home / "klipper"),
    ]


async def test_restart_failure_reverts(harness):
    _, old, _ = _klipper(harness)
    harness.fail_restart("klipper.service")
    svc, rec = harness.service()

    assert await svc.update_all({"klipper"}) is False

    assert harness.head("klipper") == old
    assert [rb["reason"] for rb in _rollbacks(harness, "klipper")] == ["restart"]
    assert rec.of("on_component_done") == [("klipper", False)]


async def test_deps_failure_reverts(harness):
    origin, old, _ = _klipper(harness)
    origin.commit({"requirements.txt": "broken-dep\n"})
    harness.venv_pip("klipper", 'case "$*" in *"-r "*) exit 1 ;; esac\nexit 0\n')
    svc, _ = harness.service()

    assert await svc.update_all({"klipper"}) is False

    assert harness.head("klipper") == old
    assert [rb["reason"] for rb in _rollbacks(harness, "klipper")] == ["deps"]


async def test_one_failure_does_not_block_the_rest(harness):
    _, k_old, _ = _klipper(harness)
    moon = harness.remote("moonraker")
    harness.install(moon)
    m_new = moon.commit({"moonraker.py": "v2\n"})
    harness.component("moonraker", service="moonraker.service")
    harness.hook("klipper", "exit 1\n")
    svc, rec = harness.service()

    assert await svc.update_all({"klipper", "moonraker"}) is False

    assert harness.head("klipper") == k_old
    assert harness.head("moonraker") == m_new
    assert sorted(rec.of("on_component_done")) == [
        ("klipper", False),
        ("moonraker", True),
    ]
    assert harness.events("moonraker") == ["update_start", "update_success"]


async def test_dead_branch_is_skipped_untouched(harness):
    origin = harness.remote("klipper")
    harness.install(origin)
    old = harness.head("klipper")
    harness.component("klipper", service="klipper.service", branch="gone")
    svc, rec = harness.service()

    assert await svc.update_all({"klipper"}) is False

    assert harness.head("klipper") == old
    assert rec.of("on_error") == [
        ("klipper", "branch origin/gone not found - fix components.yaml")
    ]
    assert harness.history() == []


async def test_branch_switch_follows_components_yaml(harness):
    origin = harness.remote("klipper")
    harness.install(origin)
    feature = origin.commit({"feature.py": "x\n"}, branch="feature")
    harness.component("klipper", service="klipper.service", branch="feature")
    svc, _ = harness.service()

    assert await svc.update_all({"klipper"}) is True

    assert harness.branch("klipper") == "feature"
    assert harness.head("klipper") == feature


async def test_hard_reset_discards_local_edits(harness):
    _, _, new = _klipper(harness)
    (harness.home / "klipper" / "README").write_text("edited on the printer\n")
    svc, _ = harness.service()

    status = await svc.check_status(force=True)
    assert status["klipper"].has_local_changes
    assert status["klipper"].commits_behind == 1
    assert await svc.update_all({"klipper"}) is True

    assert harness.head("klipper") == new
    assert (harness.home / "klipper" / "README").read_text() == "klipper\n"


async def test_non_https_remote_is_refused(harness):
    origin, old, _ = _klipper(harness)
    harness.git(
        "remote", "set-url", "origin", str(origin.bare), cwd=harness.home / "klipper"
    )
    svc, rec = harness.service()

    assert await svc.update_all({"klipper"}) is False

    assert harness.head("klipper") == old
    assert rec.of("on_error") == [("klipper", "insecure remote")]
    assert not harness.inflight.exists()


async def test_ui_tip_without_updater_is_refused(harness):
    origin = harness.remote("BlocksScreen", UI_FILES)
    harness.install(origin)
    old = harness.head("BlocksScreen")
    origin.commit({"updater/dbus_service.py": None}, msg="drop updater")
    harness.component("BlocksScreen", service="BlocksScreen.service")
    svc, rec = harness.service()

    assert await svc.update_all({"BlocksScreen"}) is False

    assert harness.head("BlocksScreen") == old
    assert rec.of("on_error") == [("BlocksScreen", "refusing downgrade past updater")]


async def test_install_file_change_hands_off_to_deploy(harness):
    origin = harness.remote("BlocksScreen", UI_FILES)
    harness.install(origin)
    new = origin.commit({"scripts/install-updater.sh": "v2\n"})
    harness.component("BlocksScreen", service="BlocksScreen.service")
    harness.real_hook("BlocksScreen")
    svc, _ = harness.service()

    assert await svc.update_all({"BlocksScreen"}) is True

    assert harness.head("BlocksScreen") == new
    assert harness.deploy_flag.exists()
    assert not harness.sentinel.exists()
    assert svc.deploy_pending()
    assert svc.daemon_restart_pending
    calls = harness.calls()
    assert "systemctl --no-block restart BlocksScreen.service" in calls
    # The UI is fire-and-forget: never a blocking restart of our own screen.
    assert "systemctl restart BlocksScreen.service" not in calls


async def test_plain_ui_change_sets_no_deploy_flag(harness):
    origin = harness.remote("BlocksScreen", UI_FILES)
    harness.install(origin)
    origin.commit({"README": "docs\n"})
    harness.component("BlocksScreen", service="BlocksScreen.service")
    harness.real_hook("BlocksScreen")
    svc, _ = harness.service()

    assert await svc.update_all({"BlocksScreen"}) is True

    assert not harness.deploy_flag.exists()
    assert not svc.daemon_restart_pending
    assert "systemctl --no-block restart BlocksScreen.service" in harness.calls()


async def test_reconcile_reverts_power_cut_batch(harness):
    _, old, new = _klipper(harness)
    path = harness.home / "klipper"
    # Power cut mid-batch: the tree moved, the marker still names the rollback point.
    harness.git("pull", "-q", cwd=path)
    assert harness.head("klipper") == new
    harness.inflight.parent.mkdir(parents=True, exist_ok=True)
    harness.inflight.write_text(f'{{"klipper": "{old}"}}')
    svc, _ = harness.service()

    assert await svc.reconcile() is True

    assert harness.head("klipper") == old
    assert "boot_rollback" in harness.events("klipper")
    assert not harness.inflight.exists()


async def test_recover_returns_to_prev_hash(harness):
    _, old, new = _klipper(harness)
    svc, rec = harness.service()
    assert await svc.update_all({"klipper"}) is True
    assert harness.head("klipper") == new
    restarts_before = harness.calls().count("systemctl restart klipper.service")

    assert await svc.recover("klipper", hard=True) is True

    assert harness.head("klipper") == old
    assert rec.of("on_recover") == [("klipper", True)]
    assert (
        harness.calls().count("systemctl restart klipper.service")
        == restarts_before + 1
    )


async def test_single_component_update_and_rollback(harness):
    _, old, new = _klipper(harness)
    svc, _ = harness.service()
    assert await svc.update_component("klipper") is True
    assert harness.head("klipper") == new
    assert not harness.inflight.exists()

    harness.hook("klipper", "exit 1\n")
    harness.git("reset", "-q", "--hard", old, cwd=harness.home / "klipper")
    svc2, rec = harness.service()

    assert await svc2.update_component("klipper") is False

    assert harness.head("klipper") == old
    assert rec.of("on_rollback") == [("klipper", True)]


async def test_provision_missing_clones_and_enables(harness):
    origin = harness.remote("klipper")
    harness.component("klipper", service="klipper.service", install_if_missing=True)
    svc, rec = harness.service()
    busy: list[bool] = []

    assert await svc.provision_missing(busy.append) is False

    assert busy == [True, False]
    assert harness.head("klipper") == harness.git("rev-parse", "HEAD", cwd=origin.bare)
    assert harness.events("klipper") == ["install_start", "install_success"]
    assert rec.of("on_component_done") == [("klipper", True)]
    assert "systemctl enable klipper.service" in harness.calls()


async def test_provision_waits_while_printing(harness):
    harness.remote("klipper")
    harness.component("klipper", install_if_missing=True)
    harness.printing.return_value = True
    svc, _ = harness.service()
    busy: list[bool] = []

    assert await svc.provision_missing(busy.append) is True

    assert busy == []
    assert not (harness.home / "klipper").exists()


async def test_provision_offline_never_raises_busy(harness):
    harness.component("klipper", install_if_missing=True)  # no origin exists
    svc, _ = harness.service()
    busy: list[bool] = []

    assert await svc.provision_missing(busy.append) is True

    assert busy == []
    assert not (harness.home / "klipper").exists()
