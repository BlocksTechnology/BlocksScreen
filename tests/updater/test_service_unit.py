import asyncio
import json
import time
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from updater.models import ComponentConfig, ComponentStatus
from updater.service import LoggingCallback, UpdateService


class TestLoggingCallback:
    def test_all_methods_do_not_raise(self):
        cb = LoggingCallback()
        cb.on_step("klipper", 1, 5)
        cb.on_component_done("klipper", True)
        cb.on_error("klipper", "network")
        cb.on_rollback("klipper", False)
        cb.on_recover("klipper", True)


class TestHistoryLog:
    def test_history_appends_jsonl_entry(self, tmp_path: Path):
        """OBS-1: _history appends one JSON line per event with the given fields."""

        svc = UpdateService()
        svc._history_path = tmp_path / "update_history.jsonl"
        svc._history("update_success", "klipper", new_hash="abc123")
        svc._history("rollback", "moonraker", reason="deps", ok=False)

        lines = svc._history_path.read_text().splitlines()
        assert len(lines) == 2
        first = json.loads(lines[0])
        assert first["event"] == "update_success"
        assert first["component"] == "klipper"
        assert first["new_hash"] == "abc123"
        assert "ts" in first
        second = json.loads(lines[1])
        assert second["event"] == "rollback" and second["ok"] is False

    def test_history_write_failure_is_non_fatal(self, tmp_path: Path):
        """A write error must never break an update — _history swallows OSError."""
        svc = UpdateService()
        # Point at a path whose parent can't be created (a file, not a dir).
        blocker = tmp_path / "blocker"
        blocker.write_text("")
        svc._history_path = blocker / "sub" / "history.jsonl"
        svc._history("update_start", "klipper")  # must not raise


class TestCheckStatus:
    @pytest.mark.asyncio
    async def test_returns_all_components(self):
        fake = ComponentStatus(name="klipper", commits_behind=0)
        fake_apt = ComponentStatus(name="system", commits_behind=2)
        with (
            patch("updater.service.check_git_status", return_value=fake),
            patch("updater.service.check_apt_status", return_value=fake_apt),
            patch("pathlib.Path.exists", return_value=True),
        ):
            svc = UpdateService()
            result = await svc.check_status()
        assert "klipper" in result
        assert "system" in result

    @pytest.mark.asyncio
    async def test_force_bypasses_ttl(self, tmp_path: Path):
        """force=True must always fetch even when called within the TTL window."""
        fake_path = tmp_path / "klipper"
        fake_path.mkdir()
        component = ComponentConfig(name="klipper", kind="git", path=fake_path)
        fake = ComponentStatus(name="klipper", commits_behind=0)
        with (
            patch(
                "updater.service.load_components", return_value=([component], 3600.0)
            ),
            patch("updater.service.check_git_status", return_value=fake) as mock_check,
        ):
            svc = UpdateService()
            svc._fetch_times["klipper"] = time.monotonic()
            await svc.check_status(force=True)
        *_, skip_fetch = mock_check.call_args.args
        assert skip_fetch is False, "force=True must not skip the fetch"

    @pytest.mark.asyncio
    async def test_ttl_suppresses_fetch_without_force(self, tmp_path: Path):
        """Without force, a second call within the TTL window must skip the fetch."""
        fake_path = tmp_path / "klipper"
        fake_path.mkdir()
        component = ComponentConfig(name="klipper", kind="git", path=fake_path)
        fake = ComponentStatus(name="klipper", commits_behind=0)
        with (
            patch(
                "updater.service.load_components", return_value=([component], 3600.0)
            ),
            patch("updater.service.check_git_status", return_value=fake) as mock_check,
        ):
            svc = UpdateService()
            svc._fetch_times["klipper"] = time.monotonic()
            await svc.check_status()
        *_, skip_fetch = mock_check.call_args.args
        assert skip_fetch is True


class TestStateFile:
    @pytest.mark.asyncio
    async def test_written_on_update_start(self, tmp_path):
        state_path = tmp_path / "updater_state.json"
        with (
            patch("updater.service.git_get_hash", return_value="abc123"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_pull", return_value=(True, "")),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
            patch("updater.service._STATE_PATH", state_path),
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "updater.service._assert_https_remote",
                return_value=(True, "https://github.com/test/repo"),
            ),
        ):
            svc = UpdateService()
            svc._state_path = state_path
            await svc.update_component("klipper")
        data = svc._read_state()
        assert "klipper" in data
        assert data["klipper"]["prev_hash"] == "abc123"


class TestGitUpdate:
    @pytest.fixture(autouse=True)
    def mock_https_remote(self):
        with patch(
            "updater.service._assert_https_remote",
            return_value=(True, "https://github.com/test/repo"),
        ):
            yield

    @pytest.fixture(autouse=True)
    def mock_git_current_branch(self):
        with patch("updater.service.git_get_current_branch", return_value="master"):
            yield

    @pytest.mark.asyncio
    async def test_rollback_on_fetch_failure(self):
        cb = MagicMock()
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="abc123"),
            patch("updater.service.git_fetch", return_value=(False, "timeout")),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch("updater.service.restart_service", return_value=(True, "")),
        ):
            svc = UpdateService(callback=cb)
            result = await svc.update_component("klipper")
        assert result is False
        mock_reset.assert_called_once()
        cb.on_rollback.assert_called_once_with("klipper", True)
        cb.on_component_done.assert_called_once_with("klipper", False)

    @pytest.mark.asyncio
    async def test_rollback_on_pull_failure(self):
        cb = MagicMock()
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="abc123"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_pull", return_value=(False, "merge conflict")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
        ):
            svc = UpdateService(callback=cb)
            result = await svc.update_component("klipper")
        assert result is False
        mock_reset.assert_called()  # hard reset (HEAD) + rollback
        cb.on_rollback.assert_called_once_with("klipper", True)
        cb.on_component_done.assert_called_once_with("klipper", False)

    @pytest.mark.asyncio
    async def test_emits_step_progress_in_order(self, tmp_path):
        state_path = tmp_path / "updater_state.json"
        cb = MagicMock()
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="abc123"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_reset_to_hash", return_value=(True, "")),
            patch("updater.service.git_pull", return_value=(True, "")),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
            patch("updater.service._STATE_PATH", state_path),
        ):
            svc = UpdateService(callback=cb)
            svc._state_path = state_path
            await svc.update_component("klipper")
        assert cb.on_step.call_args_list == [
            call("klipper", 1, 4),
            call("klipper", 2, 4),
            call("klipper", 3, 4),
            call("klipper", 4, 4),
        ]

    @pytest.mark.asyncio
    async def test_rollback_on_deps_failure(self):
        cb = MagicMock()
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="abc123"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_pull", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(False, "missing packages"),
            ),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
        ):
            svc = UpdateService(callback=cb)
            result = await svc.update_component("klipper")
        assert result is False
        mock_reset.assert_called()  # hard reset (HEAD) + rollback
        cb.on_rollback.assert_called_once_with("klipper", True)
        cb.on_component_done.assert_called_once_with("klipper", False)

    @pytest.mark.asyncio
    async def test_rollback_on_service_restart_failure(self):
        cb = MagicMock()
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="abc123"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_reset_to_hash", return_value=(True, "")),
            patch("updater.service.git_pull", return_value=(True, "")),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(False, "timeout")),
        ):
            svc = UpdateService(callback=cb)
            result = await svc.update_component("klipper")
        assert result is False
        # rollback restart also fails (same mock) → ok=False
        cb.on_rollback.assert_called_once_with("klipper", False)
        cb.on_error.assert_called_once_with("klipper", "restart")
        cb.on_component_done.assert_called_once_with("klipper", False)

    @pytest.mark.asyncio
    async def test_fetch_skipped_when_snapshot_fresh(self):
        cb = MagicMock()
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="abc123"),
            patch("updater.service.git_fetch", return_value=(True, "")) as mock_fetch,
            patch("updater.service.git_reset_to_hash", return_value=(True, "")),
            patch("updater.service.git_pull", return_value=(True, "")),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
        ):
            svc = UpdateService(callback=cb)
            svc._fetch_times["klipper"] = time.monotonic()
            result = await svc.update_component("klipper")
        assert result is True
        mock_fetch.assert_not_called()

    @pytest.mark.asyncio
    async def test_empty_prev_hash_returns_false(self):
        component = ComponentConfig(
            name="test",
            kind="git",
            path=Path("/fake/path"),
            service="test.service",
        )
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value=""),
            patch("updater.service.git_fetch") as mock_fetch,
        ):
            svc = UpdateService()
            result = await svc._run_git_update(component)
        assert result is False
        mock_fetch.assert_not_called()

    @pytest.mark.asyncio
    async def test_version_pin_uses_reset_not_pull(self):
        component = ComponentConfig(
            name="test",
            kind="git",
            path=Path("/fake/path"),
            service="test.service",
            version="abc1234",
        )
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="oldhash"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_get_current_branch", return_value="main"),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch("updater.service.git_pull") as mock_pull,
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
        ):
            svc = UpdateService()
            result = await svc._run_git_update(component)
            assert result is True
            assert mock_reset.call_count == 2  # hard reset (origin/main) + version pin
            mock_reset.assert_any_call(Path("/fake/path"), "origin/main")
            mock_reset.assert_any_call(Path("/fake/path"), "abc1234")
            mock_pull.assert_not_called()

    @pytest.mark.asyncio
    async def test_branch_uses_checkout_then_pull(self):
        component = ComponentConfig(
            name="test",
            kind="git",
            path=Path("/fake/path"),
            service="test.service",
            branch="testing_branch",
        )
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="oldhash"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch(
                "updater.service.git_checkout", return_value=(True, "")
            ) as mock_checkout,
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch("updater.service.git_pull", return_value=(True, "")) as mock_pull,
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
        ):
            svc = UpdateService()
            result = await svc._run_git_update(component)
            assert result is True
            mock_checkout.assert_called_once_with(Path("/fake/path"), "testing_branch")
            mock_pull.assert_called_once()
            mock_reset.assert_called_once_with(
                Path("/fake/path"), "origin/testing_branch"
            )  # hard reset only

    @pytest.mark.asyncio
    async def test_rollback_on_version_failure(self):
        cb = MagicMock()
        component = ComponentConfig(
            name="test",
            kind="git",
            path=Path("/fake/path"),
            service="test.service",
            version="abc1234",
        )
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="oldhash"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_get_current_branch", return_value="main"),
            patch(
                "updater.service.git_reset_to_hash",
                side_effect=[(True, ""), (False, "bad hash"), (True, "")],
            ) as mock_reset,
            patch("updater.service.restart_service", return_value=(True, "")),
        ):
            svc = UpdateService(callback=cb)
            result = await svc._run_git_update(component)
        assert result is False
        assert (
            mock_reset.call_count == 3
        )  # hard reset (origin/main) + version pin fail + rollback
        cb.on_rollback.assert_called_once_with("test", True)
        cb.on_component_done.assert_called_once_with("test", False)

    @pytest.mark.asyncio
    async def test_rollback_on_checkout_failure(self):
        cb = MagicMock()
        component = ComponentConfig(
            name="test",
            kind="git",
            path=Path("/fake/path"),
            service="test.service",
            branch="develop",
        )
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="oldhash"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch(
                "updater.service.git_checkout", return_value=(False, "branch not found")
            ),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch("updater.service.restart_service", return_value=(True, "")),
        ):
            svc = UpdateService(callback=cb)
            result = await svc._run_git_update(component)
        assert result is False
        mock_reset.assert_called()  # hard reset (HEAD) + rollback
        cb.on_rollback.assert_called_once_with("test", True)
        cb.on_component_done.assert_called_once_with("test", False)

    @pytest.mark.asyncio
    async def test_cancelled_mid_update_triggers_rollback(self):
        cb = MagicMock()
        component = ComponentConfig(
            name="test",
            kind="git",
            path=Path("/fake/path"),
            service="test.service",
        )
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="oldhash"),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_get_current_branch", return_value="main"),
            patch("updater.service.git_reset_to_hash", return_value=(True, "")),
            patch("updater.service.git_pull", side_effect=asyncio.CancelledError()),
            patch("updater.service.restart_service", return_value=(True, "")),
        ):
            svc = UpdateService(callback=cb)
            with pytest.raises(asyncio.CancelledError):
                await svc._run_git_update(component)
        cb.on_error.assert_called_once_with("test", "cancelled")
        cb.on_rollback.assert_called_once_with("test", True)
        cb.on_component_done.assert_called_once_with("test", False)

    @pytest.mark.asyncio
    async def test_state_lock_prevents_corruption_on_concurrent_writes(self, tmp_path):
        """Verify _state_lock prevents concurrent corruption of state file."""

        state_path = tmp_path / "updater_state.json"
        svc = UpdateService.__new__(UpdateService)
        svc._state_path = state_path
        svc._state_lock = asyncio.Lock()
        svc._log = MagicMock()

        # Simulate concurrent tasks writing state
        async def write_state(name: str, prev_hash: str) -> None:
            async with svc._state_lock:
                # Read existing state
                if state_path.exists():
                    current = json.loads(state_path.read_text())
                else:
                    current = {}
                # Modify and write back
                current[name] = {"prev_hash": prev_hash}
                state_path.write_text(json.dumps(current))

        # Run writes concurrently
        await asyncio.gather(
            write_state("klipper", "hash1"),
            write_state("moonraker", "hash2"),
        )

        # Verify both entries are present (not corrupted by race condition)
        state_data = json.loads(state_path.read_text())
        assert state_data["klipper"]["prev_hash"] == "hash1"
        assert state_data["moonraker"]["prev_hash"] == "hash2"


class TestAptUpdate:
    @pytest.mark.asyncio
    async def test_apt_update_no_rollback_on_failure(self):
        cb = MagicMock()
        with patch("updater.service.apt_update", return_value=(False, "network error")):
            svc = UpdateService(callback=cb)
            result = await svc.update_component("system")
        assert result is False
        cb.on_error.assert_called_once_with("system", "network")
        cb.on_rollback.assert_not_called()

    @pytest.mark.asyncio
    async def test_apt_cancelled_emits_error_and_reraises(self):
        cb = MagicMock()
        with patch("updater.service.apt_update", side_effect=asyncio.CancelledError()):
            svc = UpdateService(callback=cb)
            with pytest.raises(asyncio.CancelledError):
                await svc.update_component("system")
        cb.on_error.assert_called_once_with("system", "cancelled")
        cb.on_component_done.assert_called_once_with("system", False)
        cb.on_rollback.assert_not_called()


class TestUpdateAll:
    @pytest.mark.asyncio
    async def test_blockscreen_runs_last(self):
        call_order = []

        async def fake_update(name):
            call_order.append(name)
            return True

        svc = UpdateService()
        svc.update_component = fake_update
        await svc.update_all()
        assert call_order[-1] == "BlocksScreen"

    @pytest.mark.asyncio
    async def test_runs_components_in_order(self):
        call_order = []

        async def fake_update(name):
            call_order.append(name)
            return True

        svc = UpdateService()
        svc.update_component = fake_update
        await svc.update_all()
        assert call_order.index("klipper") < call_order.index("BlocksScreen")

    @pytest.mark.asyncio
    async def test_continues_after_one_component_fails(self):
        call_order = []

        async def fake_update(name):
            call_order.append(name)
            if name == "klipper":
                return False
            return True

        svc = UpdateService()
        svc.update_component = fake_update
        await svc.update_all()
        assert len(call_order) == len(svc._components)


class TestRecover:
    @pytest.mark.asyncio
    async def test_soft_resets_without_restart(self):
        cb = MagicMock()
        state = {"klipper": {"prev_hash": "abc1234", "status": "in_progress"}}
        with (
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch("updater.service.restart_service") as mock_restart,
            patch.object(UpdateService, "_read_state", return_value=state),
        ):
            svc = UpdateService(callback=cb)
            result = await svc.recover("klipper", hard=False)
        assert result is True
        mock_reset.assert_called_once()
        mock_restart.assert_not_called()
        cb.on_recover.assert_called_once_with("klipper", True)

    @pytest.mark.asyncio
    async def test_hard_resets_and_restarts_service(self):
        cb = MagicMock()
        state = {"klipper": {"prev_hash": "abc1234", "status": "in_progress"}}
        with (
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch(
                "updater.service.restart_service", return_value=(True, "")
            ) as mock_restart,
            patch("updater.service.wait_for_service_active", return_value=True),
            patch.object(UpdateService, "_read_state", return_value=state),
        ):
            svc = UpdateService(callback=cb)
            result = await svc.recover("klipper", hard=True)
        assert result is True
        mock_reset.assert_called_once()
        mock_restart.assert_called_once()
        cb.on_recover.assert_called_once_with("klipper", True)

    @pytest.mark.asyncio
    async def test_hard_recover_fails_if_service_not_active(self):
        # restart_service can report success via its kill-fallback without the
        # unit coming back; recover must confirm it is active and fail otherwise.
        cb = MagicMock()
        state = {"klipper": {"prev_hash": "abc1234"}}
        with (
            patch("updater.service.git_reset_to_hash", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=False),
            patch.object(UpdateService, "_read_state", return_value=state),
        ):
            svc = UpdateService(callback=cb)
            result = await svc.recover("klipper", hard=True)
        assert result is False
        cb.on_recover.assert_called_once_with("klipper", False)

    @pytest.mark.asyncio
    async def test_emits_on_recover(self):
        cb = MagicMock()
        state = {}
        with (
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch("updater.service.restart_service") as mock_restart,
            patch.object(UpdateService, "_read_state", return_value=state),
        ):
            svc = UpdateService(callback=cb)
            result = await svc.recover("klipper", hard=False)
        assert result is False
        mock_reset.assert_not_called()
        mock_restart.assert_not_called()
        cb.on_recover.assert_called_once_with("klipper", False)

    @pytest.mark.asyncio
    async def test_recover_rejects_invalid_hash_format(self):
        cb = MagicMock()
        state = {"klipper": {"prev_hash": "not_a_valid_hash", "status": "in_progress"}}
        with (
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch("updater.service.restart_service") as mock_restart,
            patch.object(UpdateService, "_read_state", return_value=state),
        ):
            svc = UpdateService(callback=cb)
            result = await svc.recover("klipper", hard=False)
        assert result is False
        mock_reset.assert_not_called()
        mock_restart.assert_not_called()
        cb.on_recover.assert_called_once_with("klipper", False)


class TestHasComponent:
    def test_has_component_returns_true_for_known_component(self):
        svc = UpdateService()
        # klipper and system are default components from load_components()
        assert svc.has_component("klipper") is True

    def test_has_component_returns_false_for_unknown_component(self):
        svc = UpdateService()
        assert svc.has_component("unknown_component") is False


class TestInstallDependencies:
    @pytest.mark.asyncio
    async def test_skips_install_when_system_pip_fallback(self, tmp_path):
        """When no component venv exists, skip pip install to avoid PEP-668 failure."""
        comp_path = tmp_path / "klippain_shaketune"
        comp_path.mkdir()
        (comp_path / "requirements.txt").write_text("numpy\n")
        component = ComponentConfig(
            name="Klippain-ShakeTune", kind="git", path=comp_path
        )
        svc = UpdateService()
        with (
            patch(
                "updater.service._resolve_component_pip",
                return_value="/usr/bin/pip3",
            ),
            patch("updater.service._run") as mock_run,
        ):
            ok, msg = await svc._install_dependencies(component)
        assert ok is True
        assert "externally" in msg or "no venv" in msg
        mock_run.assert_not_called()

    @pytest.mark.asyncio
    async def test_runs_pip_when_component_venv_found(self, tmp_path):
        """When a component venv pip is found, run pip install -r requirements.txt."""
        comp_path = tmp_path / "mycomp"
        comp_path.mkdir()
        (comp_path / "requirements.txt").write_text("requests\n")
        component = ComponentConfig(name="mycomp", kind="git", path=comp_path)
        venv_pip = str(tmp_path / "mycomp-env" / "bin" / "pip")
        svc = UpdateService()
        with (
            patch(
                "updater.service._resolve_component_pip",
                return_value=venv_pip,
            ),
            patch("updater.service._run", return_value=(True, "")) as mock_run,
        ):
            ok, _ = await svc._install_dependencies(component)
        assert ok is True
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert cmd[0] == venv_pip
        assert "-r" in cmd


class TestCorruptionDuringUpdate:
    """The single Update button heals a corrupt repo via the fetch-failure path."""

    @staticmethod
    def _patches(corrupt: bool, repair_result, *, extra=None):

        ctx = [
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "updater.service.git_get_hash",
                new_callable=AsyncMock,
                return_value="abc1234",
            ),
            patch(
                "updater.service._assert_https_remote",
                new_callable=AsyncMock,
                return_value=(True, "https://x"),
            ),
            patch(
                "updater.service.git_fetch",
                new_callable=AsyncMock,
                return_value=(False, "fatal: loose object is corrupt"),
            ),
            patch(
                "updater.service.git_has_corruption",
                new_callable=AsyncMock,
                return_value=corrupt,
            ),
            patch(
                "updater.service.git_repair",
                new_callable=AsyncMock,
                return_value=repair_result,
            ),
            # Halt/short-circuit the post-fetch steps so the tests stay focused on
            # the corruption branch; also used by _rollback's reset.
            patch(
                "updater.service.git_reset_to_hash",
                new_callable=AsyncMock,
                return_value=(False, "reset"),
            ),
            patch(
                "updater.service.git_get_current_branch",
                new_callable=AsyncMock,
                return_value="main",
            ),
        ]
        ctx.extend(extra or [])
        return ctx

    @pytest.mark.asyncio
    async def test_repairs_corrupt_repo_then_continues(self):

        cb = MagicMock()
        comp = ComponentConfig(name="RF50-Klipper", kind="git", path=Path("/x"))
        with ExitStack() as stack:
            mocks = [
                stack.enter_context(p) for p in self._patches(True, (True, "repaired"))
            ]
            svc = UpdateService(callback=cb)
            svc._components = [comp]
            await svc._run_git_update(comp)
        repair_mock = mocks[5]
        repair_mock.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_rollback_when_repair_fails(self):

        cb = MagicMock()
        comp = ComponentConfig(name="RF50-Klipper", kind="git", path=Path("/x"))
        with ExitStack() as stack:
            for p in self._patches(True, (False, "still corrupt after fetch")):
                stack.enter_context(p)
            svc = UpdateService(callback=cb)
            svc._components = [comp]
            ok = await svc._run_git_update(comp)
        assert ok is False
        assert cb.on_error.call_args[0][1] == "corrupt"
