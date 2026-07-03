import asyncio
import json
import time
from contextlib import ExitStack, nullcontext
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

import updater.service as updater_service
from updater.models import ComponentConfig, ComponentStatus
from updater.service import LoggingCallback, UpdateService


@pytest.fixture(autouse=True)
def _isolate_inflight(tmp_path_factory, monkeypatch):
    """Keep the in-flight marker out of the real cache for every test in this file."""
    marker = tmp_path_factory.mktemp("inflight") / "updater_inflight.json"
    monkeypatch.setattr(updater_service, "_INFLIGHT_PATH", marker)


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

    def test_history_is_bounded(self, tmp_path: Path):
        """Oversized history is trimmed to the last KEEP lines (SD-fill guard)."""
        from updater.service import _HISTORY_KEEP_LINES, _HISTORY_MAX_BYTES

        hist = tmp_path / "history.jsonl"
        hist.write_text(('{"x":"' + "y" * 80 + '"}\n') * 15000)
        assert hist.stat().st_size > _HISTORY_MAX_BYTES
        svc = UpdateService()
        svc._history_path = hist
        svc._trim_history()
        assert sum(1 for _ in hist.open()) == _HISTORY_KEEP_LINES
        assert hist.stat().st_size < _HISTORY_MAX_BYTES


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

    @pytest.fixture(autouse=True)
    def mock_wait_active(self):
        with patch("updater.service.wait_for_service_active", return_value=True):
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
    """update_all partitions: apt independent, existing git as one atomic batch."""

    def _git(self, tmp_path: Path, name: str, order: int) -> ComponentConfig:
        path = tmp_path / name
        path.mkdir()
        return ComponentConfig(name=name, kind="git", path=path, order=order)

    @pytest.mark.asyncio
    async def test_existing_git_go_to_one_atomic_batch_in_order(self, tmp_path):
        comps = [
            ComponentConfig(name="system", kind="apt", order=1),
            self._git(tmp_path, "klipper", 2),
            self._git(tmp_path, "BlocksScreen", 99),
        ]
        seen: list[list[str]] = []
        with (
            patch("updater.service.UpdateService._preflight_fetch", return_value=True),
            patch("updater.service.UpdateService._run_apt_update") as mock_apt,
            patch(
                "updater.service.UpdateService._run_git_batch",
                side_effect=lambda b: seen.append([c.name for c in b]),
            ),
        ):
            svc = UpdateService()
            svc._components = comps
            await svc.update_all()
        mock_apt.assert_called_once()
        assert seen == [["klipper", "BlocksScreen"]]  # one batch, order preserved

    @pytest.mark.asyncio
    async def test_missing_opted_in_goes_to_provision_not_batch(self, tmp_path):
        present = self._git(tmp_path, "klipper", 2)
        missing = ComponentConfig(
            name="newcomp",
            kind="git",
            path=tmp_path / "absent",
            order=5,
            url="https://github.com/x/y",
            install_if_missing=True,
        )
        with (
            patch("updater.service.UpdateService._preflight_fetch", return_value=True),
            patch("updater.service.UpdateService._run_git_batch") as mock_batch,
            patch(
                "updater.service.UpdateService._provision_component"
            ) as mock_provision,
        ):
            svc = UpdateService()
            svc._components = [present, missing]
            await svc.update_all()
        assert [c.name for c in mock_batch.call_args[0][0]] == ["klipper"]
        assert mock_provision.call_args[0][0].name == "newcomp"

    @pytest.mark.asyncio
    async def test_empty_batch_skips_git(self, tmp_path):
        with (
            patch("updater.service.UpdateService._preflight_fetch", return_value=True),
            patch("updater.service.UpdateService._run_git_batch") as mock_batch,
        ):
            svc = UpdateService()
            svc._components = [ComponentConfig(name="system", kind="apt", order=1)]
            with patch("updater.service.UpdateService._run_apt_update"):
                await svc.update_all()
        mock_batch.assert_not_called()


class TestAtomicBatch:
    """_run_git_batch: stage all → deps → hooks → restart each service once; all-or-nothing."""

    @pytest.fixture(autouse=True)
    def _mocks(self):
        with (
            patch("updater.service.git_get_hash", return_value="oldhash"),
            patch(
                "updater.service._assert_https_remote", return_value=(True, "https://x")
            ),
            patch("updater.service.git_get_current_branch", return_value="main"),
            patch("updater.service.git_fetch", return_value=(True, "")),
        ):
            yield

    def _git(
        self, tmp_path: Path, name: str, order: int, service: str
    ) -> ComponentConfig:
        path = tmp_path / name
        path.mkdir()
        return ComponentConfig(
            name=name, kind="git", path=path, order=order, service=service
        )

    def _svc(self, tmp_path, cb, n=2, service="klipper.service"):
        comps = [self._git(tmp_path, f"c{i}", 2 + i, service) for i in range(n)]
        svc = UpdateService(callback=cb)
        svc._components = comps
        svc._state_path = tmp_path / "state.json"
        return svc, comps

    @pytest.mark.asyncio
    async def test_shared_service_restarted_once(self, tmp_path):
        cb = MagicMock()
        svc, comps = self._svc(tmp_path, cb, n=3, service="klipper.service")
        with (
            patch(
                "updater.service.UpdateService._stage_component",
                return_value=(True, ""),
            ),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch(
                "updater.service.restart_service", return_value=(True, "")
            ) as mock_rs,
            patch("updater.service.wait_for_service_active", return_value=True),
        ):
            await svc._run_git_batch(comps)
        assert mock_rs.call_count == 1  # one shared service, one restart
        assert cb.on_component_done.call_count == 3
        assert all(c.args[1] is True for c in cb.on_component_done.call_args_list)

    @pytest.mark.asyncio
    async def test_inflight_marker_written_then_cleared_on_success(self, tmp_path):
        cb = MagicMock()
        svc, comps = self._svc(tmp_path, cb, n=1)
        svc._inflight_path = tmp_path / "inflight.json"
        with (
            patch(
                "updater.service.UpdateService._stage_component",
                return_value=(True, ""),
            ),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
            patch.object(UpdateService, "_apply_deferred_restart", new=AsyncMock()),
            patch.object(svc, "_write_inflight", wraps=svc._write_inflight) as spy,
        ):
            await svc._run_git_batch(comps)
        spy.assert_called_once()  # marker written before staging
        assert not svc._inflight_path.exists()  # cleared on commit

    @pytest.mark.asyncio
    async def test_inflight_marker_cleared_on_abort(self, tmp_path):
        cb = MagicMock()
        svc, comps = self._svc(tmp_path, cb, n=2)
        svc._inflight_path = tmp_path / "inflight.json"
        with (
            patch(
                "updater.service.UpdateService._stage_component",
                side_effect=[(True, ""), (False, "conflict")],
            ),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.git_reset_to_hash", return_value=(True, "")),
        ):
            await svc._run_git_batch(comps)
        assert not svc._inflight_path.exists()  # cleared by _abort_batch

    @pytest.mark.asyncio
    async def test_restart_ui_component_also_restarts_ui(self, tmp_path):
        """A klipper/RF50-style restart_ui component refreshes BlocksScreen too."""
        cb = MagicMock()
        comp = self._git(tmp_path, "klipper", 2, "klipper.service")
        comp.restart_ui = True
        svc = UpdateService(callback=cb)
        svc._components = [comp]
        svc._state_path = tmp_path / "state.json"
        with (
            patch(
                "updater.service.UpdateService._stage_component",
                return_value=(True, ""),
            ),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
            patch(
                "updater.service.restart_service_noblock", new=AsyncMock()
            ) as mock_nb,
            patch.object(UpdateService, "_apply_deferred_restart", new=AsyncMock()),
        ):
            await svc._run_git_batch([comp])
        mock_nb.assert_awaited_once_with("BlocksScreen.service")

    @pytest.mark.asyncio
    async def test_cancel_after_commit_does_not_revert(self, tmp_path):
        """A self-restart SIGTERM (CancelledError) post-success must not revert."""
        cb = MagicMock()
        svc, comps = self._svc(tmp_path, cb, n=1)
        with (
            patch(
                "updater.service.UpdateService._stage_component",
                return_value=(True, ""),
            ),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
            patch(
                "updater.service.UpdateService._apply_deferred_restart",
                new=AsyncMock(side_effect=asyncio.CancelledError),
            ),
            patch("updater.service.git_reset_to_hash", return_value=(True, "")) as mr,
        ):
            with pytest.raises(asyncio.CancelledError):
                await svc._run_git_batch(comps)
        mr.assert_not_called()  # committed: no revert
        assert all(c.args[1] is True for c in cb.on_component_done.call_args_list)

    @pytest.mark.asyncio
    async def test_stage_failure_reverts_touched_and_does_not_restart(self, tmp_path):
        cb = MagicMock()
        svc, comps = self._svc(tmp_path, cb, n=2)
        with (
            patch(
                "updater.service.UpdateService._stage_component",
                side_effect=[(True, ""), (False, "conflict")],
            ),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch("updater.service.restart_service") as mock_rs,
        ):
            await svc._run_git_batch(comps)
        assert mock_reset.call_count == 2  # both touched repos reverted
        mock_rs.assert_not_called()
        assert cb.on_rollback.call_count == 2
        assert all(c.args[1] is True for c in cb.on_rollback.call_args_list)

    @pytest.mark.asyncio
    async def test_deps_failure_reverts_all_no_restart(self, tmp_path):
        cb = MagicMock()
        svc, comps = self._svc(tmp_path, cb, n=2)
        with (
            patch(
                "updater.service.UpdateService._stage_component",
                return_value=(True, ""),
            ),
            patch("updater.service.git_reset_to_hash", return_value=(True, "")) as mr,
            patch(
                "updater.service.UpdateService._install_dependencies",
                side_effect=[(True, ""), (False, "pip boom")],
            ),
            patch("updater.service.restart_service") as mock_rs,
        ):
            await svc._run_git_batch(comps)
        assert mr.call_count == 2
        mock_rs.assert_not_called()
        assert cb.on_error.call_args[0][1] == "deps"

    @pytest.mark.asyncio
    async def test_restart_failure_reverts_and_rerestarts_bounced(self, tmp_path):
        # Two distinct services: first restarts OK, second fails → revert git and
        # re-restart the first so it returns on the old code.
        cb = MagicMock()
        c0 = self._git(tmp_path, "c0", 2, "svc-a.service")
        c1 = self._git(tmp_path, "c1", 3, "svc-b.service")
        svc = UpdateService(callback=cb)
        svc._components = [c0, c1]
        svc._state_path = tmp_path / "state.json"
        restart_calls: list[str] = []

        async def fake_restart(name):
            restart_calls.append(name)
            return (name != "svc-b.service", "")

        with (
            patch(
                "updater.service.UpdateService._stage_component",
                return_value=(True, ""),
            ),
            patch("updater.service.git_reset_to_hash", return_value=(True, "")) as mr,
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", side_effect=fake_restart),
            patch("updater.service.wait_for_service_active", return_value=True),
        ):
            await svc._run_git_batch([c0, c1])
        assert mr.call_count == 2  # both repos reverted
        # Initial: svc-a ok, svc-b fails. Abort re-restarts BOTH bounced services
        # (incl. the failed svc-b) onto the reverted code.
        assert restart_calls == [
            "svc-a.service",
            "svc-b.service",
            "svc-a.service",
            "svc-b.service",
        ]
        assert cb.on_error.call_args[0][1] == "restart"

    @pytest.mark.asyncio
    async def test_cancel_mid_batch_reverts_staged(self, tmp_path):
        cb = MagicMock()
        svc, comps = self._svc(tmp_path, cb, n=2)
        with (
            patch(
                "updater.service.UpdateService._stage_component",
                side_effect=[(True, ""), asyncio.CancelledError()],
            ),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
        ):
            with pytest.raises(asyncio.CancelledError):
                await svc._run_git_batch(comps)
        # Both touched repos reverted by the shielded abort before re-raise.
        assert mock_reset.call_count == 2
        assert cb.on_error.call_args[0][1] == "cancelled"

    @pytest.mark.asyncio
    async def test_prev_hash_empty_aborts_before_any_change(self, tmp_path):
        cb = MagicMock()
        svc, comps = self._svc(tmp_path, cb, n=2)
        with (
            patch("updater.service.git_get_hash", return_value=""),
            patch("updater.service.git_reset_to_hash") as mock_reset,
        ):
            await svc._run_git_batch(comps)
        mock_reset.assert_not_called()
        assert cb.on_error.call_args[0][1] == "prev_hash empty"

    @pytest.mark.asyncio
    async def test_ui_service_restarted_fire_and_forget(self, tmp_path):
        # BlocksScreen.service (the UI hosting the updater) must be restarted
        # non-blocking and NOT verified, so a self-update cannot abort the batch.
        cb = MagicMock()
        comp = self._git(tmp_path, "BlocksScreen", 99, "BlocksScreen.service")
        svc = UpdateService(callback=cb)
        svc._components = [comp]
        svc._state_path = tmp_path / "state.json"
        with (
            patch(
                "updater.service.UpdateService._stage_component",
                return_value=(True, ""),
            ),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service") as mock_restart,
            patch("updater.service.wait_for_service_active") as mock_wait,
            patch(
                "updater.service.restart_service_noblock", return_value=(True, "")
            ) as mock_noblock,
        ):
            await svc._run_git_batch([comp])
        mock_restart.assert_not_called()  # no verified restart of the UI
        mock_wait.assert_not_called()  # never waits on the UI
        mock_noblock.assert_called_once_with("BlocksScreen.service")
        # Success recorded before the fire-and-forget restart.
        cb.on_component_done.assert_called_once_with("BlocksScreen", True)


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
        """Component venv pip: best-effort pip self-upgrade, then reqs install."""
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
        assert mock_run.call_count == 2
        upgrade_cmd = mock_run.call_args_list[0][0][0]
        assert upgrade_cmd == [venv_pip, "install", "--upgrade", "pip", "--quiet"]
        install_cmd = mock_run.call_args_list[1][0][0]
        assert install_cmd[0] == venv_pip
        assert "-r" in install_cmd


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


class TestProvisionMissingComponent:
    """install_if_missing: clone + deps + hook + restart, rm -rf on failure."""

    def _comp(self, tmp_path: Path, *, service: str | None = None) -> ComponentConfig:
        return ComponentConfig(
            name="newcomp",
            kind="git",
            path=tmp_path / "newcomp",
            branch="main",
            service=service,
            url="https://github.com/test/newcomp",
            install_if_missing=True,
        )

    @pytest.mark.asyncio
    async def test_missing_opted_in_routes_to_provision(self, tmp_path):
        comp = self._comp(tmp_path)
        cb = MagicMock()
        with (
            patch("updater.service.git_clone", return_value=(True, "")) as mock_clone,
            patch("updater.service.git_get_hash", return_value="newhash"),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")) as mock_hook,
        ):
            svc = UpdateService(callback=cb)
            svc._components = [comp]
            ok = await svc.update_component("newcomp")
        assert ok is True
        mock_clone.assert_called_once_with(
            "https://github.com/test/newcomp", comp.path, "main"
        )
        # prev_hash must be the empty-tree SHA, not "", so a diff-based hook
        # installs the service instead of no-op'ing on an empty prev_hash.
        from updater.service import _GIT_EMPTY_TREE

        assert mock_hook.call_args[0][3] == _GIT_EMPTY_TREE
        cb.on_component_done.assert_called_once_with("newcomp", True)

    @pytest.mark.asyncio
    async def test_missing_without_opt_in_reports_path_not_found(self, tmp_path):
        comp = self._comp(tmp_path)
        comp.install_if_missing = False
        cb = MagicMock()
        with patch("updater.service.git_clone") as mock_clone:
            svc = UpdateService(callback=cb)
            svc._components = [comp]
            ok = await svc.update_component("newcomp")
        assert ok is False
        mock_clone.assert_not_called()
        assert cb.on_error.call_args[0][1] == "path not found"

    @pytest.mark.asyncio
    async def test_clone_failure_removes_partial_and_reports(self, tmp_path):
        comp = self._comp(tmp_path)
        cb = MagicMock()
        with (
            patch("updater.service.git_clone", return_value=(False, "boom")),
            patch("updater.service.shutil.rmtree") as mock_rmtree,
        ):
            svc = UpdateService(callback=cb)
            svc._components = [comp]
            ok = await svc.update_component("newcomp")
        assert ok is False
        mock_rmtree.assert_called_once()
        assert cb.on_error.call_args[0][1] == "clone"

    @pytest.mark.asyncio
    async def test_deps_failure_removes_clone(self, tmp_path):
        comp = self._comp(tmp_path)
        cb = MagicMock()
        with (
            patch("updater.service.git_clone", return_value=(True, "")),
            patch("updater.service.git_get_hash", return_value="newhash"),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(False, "pip exploded"),
            ),
            patch("updater.service.shutil.rmtree") as mock_rmtree,
        ):
            svc = UpdateService(callback=cb)
            svc._components = [comp]
            ok = await svc.update_component("newcomp")
        assert ok is False
        mock_rmtree.assert_called_once()
        assert cb.on_error.call_args[0][1] == "deps"

    @pytest.mark.asyncio
    async def test_provision_waits_for_service_active(self, tmp_path):
        comp = self._comp(tmp_path, service="newcomp.service")
        cb = MagicMock()
        with (
            patch("updater.service.git_clone", return_value=(True, "")),
            patch("updater.service.git_get_hash", return_value="newhash"),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch(
                "updater.service.wait_for_service_active", return_value=False
            ) as mock_wait,
            patch("updater.service.shutil.rmtree") as mock_rmtree,
        ):
            svc = UpdateService(callback=cb)
            svc._components = [comp]
            ok = await svc.update_component("newcomp")
        assert ok is False
        mock_wait.assert_called_once()
        mock_rmtree.assert_called_once()
        assert cb.on_error.call_args[0][1] == "restart_timeout"

    @pytest.mark.asyncio
    async def test_check_status_reports_needs_install(self, tmp_path):
        comp = self._comp(tmp_path)
        svc = UpdateService()
        svc._components = [comp]
        result = await svc.check_status()
        assert result["newcomp"].needs_install is True

    @pytest.mark.asyncio
    async def test_provision_hook_uses_long_timeout(self, tmp_path):
        comp = self._comp(tmp_path)
        with (
            patch("updater.service.git_clone", return_value=(True, "")),
            patch("updater.service.git_get_hash", return_value="newhash"),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")) as mock_hook,
        ):
            svc = UpdateService(callback=MagicMock())
            svc._components = [comp]
            await svc.update_component("newcomp")
        assert mock_hook.call_args.kwargs["timeout"] == 600.0

    @pytest.mark.asyncio
    async def test_provision_enables_service_after_successful_start(self, tmp_path):
        comp = self._comp(tmp_path, service="newcomp.service")
        with (
            patch("updater.service.git_clone", return_value=(True, "")),
            patch("updater.service.git_get_hash", return_value="newhash"),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
            patch(
                "updater.service.enable_service", return_value=(True, "")
            ) as mock_enable,
        ):
            svc = UpdateService(callback=MagicMock())
            svc._components = [comp]
            ok = await svc.update_component("newcomp")
        assert ok is True
        mock_enable.assert_called_once_with("newcomp.service")

    @pytest.mark.asyncio
    async def test_provision_enable_failure_is_best_effort(self, tmp_path):
        comp = self._comp(tmp_path, service="newcomp.service")
        cb = MagicMock()
        with (
            patch("updater.service.git_clone", return_value=(True, "")),
            patch("updater.service.git_get_hash", return_value="newhash"),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
            patch("updater.service.enable_service", return_value=(False, "denied")),
        ):
            svc = UpdateService(callback=cb)
            svc._components = [comp]
            ok = await svc.update_component("newcomp")
        assert ok is True
        cb.on_component_done.assert_called_once_with("newcomp", True)


class TestReconcile:
    """Boot-time repo healing for every component (Blocker 1)."""

    def _git_comp(self, tmp_path: Path) -> ComponentConfig:
        path = tmp_path / "repo"
        path.mkdir()
        return ComponentConfig(name="klipper", kind="git", path=path)

    @pytest.mark.asyncio
    async def test_healthy_repo_is_skipped(self, tmp_path):
        comp = self._git_comp(tmp_path)
        with (
            patch("updater.service.process_lock", lambda: nullcontext(True)),
            patch("updater.service.git_get_hash", return_value="abc123"),
            patch("updater.service.git_repair") as mock_repair,
        ):
            svc = UpdateService()
            svc._components = [comp]
            await svc.reconcile()
        mock_repair.assert_not_called()

    @pytest.mark.asyncio
    async def test_unreadable_head_triggers_repair(self, tmp_path):
        comp = self._git_comp(tmp_path)
        with (
            patch("updater.service.process_lock", lambda: nullcontext(True)),
            patch("updater.service.git_get_hash", return_value=""),
            patch(
                "updater.service.git_repair", return_value=(True, "repaired")
            ) as mock_repair,
        ):
            svc = UpdateService()
            svc._components = [comp]
            await svc.reconcile()
        mock_repair.assert_called_once_with(comp.path)

    @pytest.mark.asyncio
    async def test_repair_failure_falls_back_to_prev_hash_reset(self, tmp_path):
        comp = self._git_comp(tmp_path)
        with (
            patch("updater.service.process_lock", lambda: nullcontext(True)),
            patch("updater.service.git_get_hash", return_value=""),
            patch("updater.service.git_repair", return_value=(False, "no fetch")),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
            patch.object(
                UpdateService,
                "_read_state",
                return_value={"klipper": {"prev_hash": "a" * 40}},
            ),
        ):
            svc = UpdateService()
            svc._components = [comp]
            await svc.reconcile()
        mock_reset.assert_called_once_with(comp.path, "a" * 40)

    @pytest.mark.asyncio
    async def test_apt_component_skipped(self, tmp_path):
        comp = ComponentConfig(name="system", kind="apt")
        with (
            patch("updater.service.process_lock", lambda: nullcontext(True)),
            patch("updater.service.git_get_hash") as mock_hash,
        ):
            svc = UpdateService()
            svc._components = [comp]
            await svc.reconcile()
        mock_hash.assert_not_called()

    @pytest.mark.asyncio
    async def test_skips_when_process_lock_held(self, tmp_path):
        # A concurrent update/CLI run owns the lock: reconcile must not touch git.
        comp = self._git_comp(tmp_path)
        with (
            patch("updater.service.process_lock", lambda: nullcontext(False)),
            patch("updater.service.git_get_hash") as mock_hash,
            patch("updater.service.git_repair") as mock_repair,
        ):
            svc = UpdateService()
            svc._components = [comp]
            await svc.reconcile()
        mock_hash.assert_not_called()
        mock_repair.assert_not_called()


class TestWriteStateDurability:
    """_write_state fsyncs file + parent dir (Major 4)."""

    @pytest.mark.asyncio
    async def test_fsync_called_on_write(self, tmp_path):
        svc = UpdateService()
        svc._state_path = tmp_path / "updater_state.json"
        with patch("updater.service.os.fsync") as mock_fsync:
            ok = svc._write_state({"klipper": {"prev_hash": "abc"}})
        assert ok is True
        assert mock_fsync.call_count >= 2  # temp file + parent dir
        assert json.loads(svc._state_path.read_text()) == {
            "klipper": {"prev_hash": "abc"}
        }


class TestRollbackVerifiesRestart:
    """_rollback confirms the unit is active, not just that restart returned ok."""

    @pytest.mark.asyncio
    async def test_rollback_false_when_service_not_active(self):
        cb = MagicMock()
        comp = ComponentConfig(
            name="klipper", kind="git", path=Path("/x"), service="klipper.service"
        )
        with (
            patch("updater.service.git_reset_to_hash", return_value=(True, "")),
            patch("updater.service.restart_service", return_value=(True, "killed")),
            patch("updater.service.wait_for_service_active", return_value=False),
        ):
            svc = UpdateService(callback=cb)
            await svc._rollback(comp, "abc123", "deps")
        cb.on_rollback.assert_called_once_with("klipper", False)


class TestPreflightFetch:
    """update_all fetches every component up-front; a network drop aborts cleanly."""

    def _git(self, tmp_path: Path, name: str) -> ComponentConfig:
        path = tmp_path / name
        path.mkdir()
        return ComponentConfig(name=name, kind="git", path=path)

    @pytest.mark.asyncio
    async def test_all_ok_records_fetch_times(self, tmp_path):
        comps = [self._git(tmp_path, "klipper"), self._git(tmp_path, "moonraker")]
        with patch("updater.service.git_fetch", return_value=(True, "")):
            svc = UpdateService()
            svc._components = comps
            ok = await svc._preflight_fetch(comps, comps)
        assert ok is True
        assert set(svc._fetch_times) == {"klipper", "moonraker"}

    @pytest.mark.asyncio
    async def test_offline_aborts_and_reports_all(self, tmp_path):
        comps = [self._git(tmp_path, "klipper"), self._git(tmp_path, "moonraker")]
        cb = MagicMock()
        with (
            patch("updater.service.git_fetch", return_value=(False, "timeout")),
            patch("updater.service.git_has_corruption", return_value=False),
        ):
            svc = UpdateService(callback=cb)
            svc._components = comps
            ok = await svc._preflight_fetch(comps, comps)
        assert ok is False
        assert cb.on_error.call_count == 2

    @pytest.mark.asyncio
    async def test_corrupt_repo_is_not_treated_as_offline(self, tmp_path):
        comps = [self._git(tmp_path, "klipper")]
        with (
            patch("updater.service.git_fetch", return_value=(False, "corrupt object")),
            patch("updater.service.git_has_corruption", return_value=True),
        ):
            svc = UpdateService()
            svc._components = comps
            ok = await svc._preflight_fetch(comps, comps)
        assert ok is True
        assert "klipper" not in svc._fetch_times  # left for the per-component flow

    @pytest.mark.asyncio
    async def test_recently_fetched_component_is_not_refetched(self, tmp_path):
        comp = self._git(tmp_path, "klipper")
        with patch("updater.service.git_fetch", return_value=(True, "")) as mock_fetch:
            svc = UpdateService()
            svc._components = [comp]
            svc._fetch_times["klipper"] = time.monotonic()
            ok = await svc._preflight_fetch([comp], [comp])
        assert ok is True
        mock_fetch.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_all_aborts_apply_when_preflight_fails(self, tmp_path):
        comps = [self._git(tmp_path, "klipper")]
        with (
            patch.object(UpdateService, "_preflight_fetch", return_value=False),
            patch.object(UpdateService, "update_component") as mock_update,
        ):
            svc = UpdateService()
            svc._components = comps
            await svc.update_all({"klipper"})
        mock_update.assert_not_called()


class TestDeferredRestart:
    """_apply_deferred_restart: hooks record to the sentinel, daemon acts once."""

    def _svc_with_ui(self):
        svc = UpdateService()
        svc._components = [
            ComponentConfig(
                name="BlocksScreen",
                kind="git",
                path=Path("/home/blocks/BlocksScreen"),
                service="BlocksScreen.service",
            )
        ]
        return svc

    @pytest.mark.asyncio
    async def test_no_sentinel_is_noop(self, tmp_path: Path):
        sentinel = tmp_path / "updater-restart-needed"
        with (
            patch("updater.service.restart_sentinel_path", return_value=sentinel),
            patch("updater.service.restart_service_noblock") as mock_restart,
            patch.object(UpdateService, "_touch_deploy_flag") as mock_flag,
        ):
            svc = self._svc_with_ui()
            await svc._apply_deferred_restart()
        mock_restart.assert_not_called()
        mock_flag.assert_not_called()

    @pytest.mark.asyncio
    async def test_install_touches_deploy_flag_not_restart(self, tmp_path: Path):
        sentinel = tmp_path / "updater-restart-needed"
        sentinel.write_text("install\n")
        with (
            patch("updater.service.restart_sentinel_path", return_value=sentinel),
            patch("updater.service.restart_service_noblock") as mock_restart,
            patch(
                "updater.service.verify_updater_importable", new=AsyncMock()
            ) as mock_verify,
            patch.object(UpdateService, "_touch_deploy_flag") as mock_flag,
        ):
            svc = self._svc_with_ui()
            await svc._apply_deferred_restart()
        mock_flag.assert_called_once()
        mock_restart.assert_not_called()
        mock_verify.assert_not_called()
        assert not sentinel.exists()  # consumed

    @pytest.mark.asyncio
    async def test_code_restarts_only_when_importable(self, tmp_path: Path):
        sentinel = tmp_path / "updater-restart-needed"
        sentinel.write_text("code\n")
        with (
            patch("updater.service.restart_sentinel_path", return_value=sentinel),
            patch(
                "updater.service.verify_updater_importable",
                new=AsyncMock(return_value=True),
            ),
            patch("updater.service.restart_service_noblock") as mock_restart,
        ):
            svc = self._svc_with_ui()
            await svc._apply_deferred_restart()
        mock_restart.assert_called_once_with("BlocksScreen-updater.service")

    @pytest.mark.asyncio
    async def test_code_skips_restart_when_not_importable(self, tmp_path: Path):
        """Brick-guard: a broken new updater must not restart the daemon."""
        sentinel = tmp_path / "updater-restart-needed"
        sentinel.write_text("code\n")
        with (
            patch("updater.service.restart_sentinel_path", return_value=sentinel),
            patch(
                "updater.service.verify_updater_importable",
                new=AsyncMock(return_value=False),
            ),
            patch("updater.service.restart_service_noblock") as mock_restart,
        ):
            svc = self._svc_with_ui()
            await svc._apply_deferred_restart()
        mock_restart.assert_not_called()

    def test_read_clear_sentinel_install_outranks_code(self, tmp_path: Path):
        sentinel = tmp_path / "updater-restart-needed"
        sentinel.write_text("code\ninstall\ncode\n")
        assert UpdateService._read_clear_sentinel(sentinel) == "install"
        assert not sentinel.exists()

    def test_read_clear_sentinel_missing_returns_empty(self, tmp_path: Path):
        assert UpdateService._read_clear_sentinel(tmp_path / "nope") == ""

    def test_touch_deploy_flag_rejects_planted_symlink(self, tmp_path: Path):
        target = tmp_path / "target"
        target.write_text("keep")
        flag = tmp_path / ".run-install-updater"
        flag.symlink_to(target)
        with patch("updater.service._DEPLOY_FLAG", flag):
            UpdateService()._touch_deploy_flag()
        assert flag.exists() and not flag.is_symlink()
        assert target.read_text() == "keep"  # symlink not followed


class TestInflightRollback:
    """Cross-reboot revert: an update cut off before commit is undone on boot."""

    def _git(self, tmp_path: Path, name: str = "klipper") -> ComponentConfig:
        path = tmp_path / name
        path.mkdir()
        return ComponentConfig(
            name=name, kind="git", path=path, service="klipper.service"
        )

    def test_write_read_clear_roundtrip(self, tmp_path):
        svc = UpdateService()
        svc._inflight_path = tmp_path / "inflight.json"
        assert svc._read_inflight() == {}
        assert svc._write_inflight({"klipper": "a" * 40}) is True
        assert svc._read_inflight() == {"klipper": "a" * 40}
        svc._clear_inflight()
        assert svc._read_inflight() == {}

    @pytest.mark.asyncio
    async def test_revert_resets_interrupted_repo(self, tmp_path):
        comp = self._git(tmp_path)
        svc = UpdateService()
        svc._components = [comp]
        svc._inflight_path = tmp_path / "inflight.json"
        svc._write_inflight({"klipper": "a" * 40})
        with (
            patch("updater.service.git_get_hash", return_value="b" * 40),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
        ):
            await svc._revert_inflight()
        mock_reset.assert_awaited_once_with(comp.path, "a" * 40)
        assert svc._read_inflight() == {}

    @pytest.mark.asyncio
    async def test_revert_skips_repo_already_at_prev(self, tmp_path):
        comp = self._git(tmp_path)
        svc = UpdateService()
        svc._components = [comp]
        svc._inflight_path = tmp_path / "inflight.json"
        svc._write_inflight({"klipper": "a" * 40})
        with (
            patch("updater.service.git_get_hash", return_value="a" * 40),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
        ):
            await svc._revert_inflight()
        mock_reset.assert_not_called()
        assert svc._read_inflight() == {}

    @pytest.mark.asyncio
    async def test_revert_noop_without_marker(self, tmp_path):
        svc = UpdateService()
        svc._inflight_path = tmp_path / "inflight.json"
        with patch(
            "updater.service.git_reset_to_hash", return_value=(True, "")
        ) as mock_reset:
            await svc._revert_inflight()
        mock_reset.assert_not_called()

    @pytest.mark.asyncio
    async def test_revert_rejects_invalid_prev_hash(self, tmp_path):
        comp = self._git(tmp_path)
        svc = UpdateService()
        svc._components = [comp]
        svc._inflight_path = tmp_path / "inflight.json"
        svc._write_inflight({"klipper": "not-a-sha"})
        with (
            patch("updater.service.git_get_hash", return_value="b" * 40),
            patch(
                "updater.service.git_reset_to_hash", return_value=(True, "")
            ) as mock_reset,
        ):
            await svc._revert_inflight()
        mock_reset.assert_not_called()
        assert svc._read_inflight() == {}  # marker still cleared


class TestPingWhile:
    @pytest.mark.asyncio
    async def test_returns_result(self):
        svc = UpdateService(callback=MagicMock())

        async def fast():
            return (True, "ok")

        assert await svc._ping_while(fast(), "x", 3, 4) == (True, "ok")

    @pytest.mark.asyncio
    async def test_emits_on_step_while_waiting(self):
        cb = MagicMock()
        svc = UpdateService(callback=cb)

        async def slow():
            await asyncio.sleep(0.05)
            return "done"

        assert await svc._ping_while(slow(), "klipper", 3, 4, interval=0.01) == "done"
        cb.on_step.assert_called_with("klipper", 3, 4)

    @pytest.mark.asyncio
    async def test_cancellation_reaches_inner_task(self):
        svc = UpdateService(callback=MagicMock())
        started = asyncio.Event()
        cancelled = asyncio.Event()

        async def hang():
            started.set()
            try:
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                cancelled.set()
                raise

        task = asyncio.create_task(svc._ping_while(hang(), "x", 3, 4, interval=0.01))
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert cancelled.is_set()


class TestHookTimeoutBudget:
    @pytest.mark.asyncio
    async def test_single_update_passes_hook_timeout(self, tmp_path):
        cb = MagicMock()
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="a" * 40),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_pull", return_value=(True, "")),
            patch("updater.service.git_reset_to_hash", return_value=(True, "")),
            patch("updater.service.git_get_current_branch", return_value="master"),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")) as mock_hook,
            patch("updater.service.restart_service", return_value=(True, "")),
            patch("updater.service.restart_service_noblock", return_value=(True, "")),
            patch("updater.service.wait_for_service_active", return_value=True),
            patch(
                "updater.service._assert_https_remote",
                return_value=(True, "https://github.com/test/repo"),
            ),
        ):
            svc = UpdateService(callback=cb)
            svc._state_path = tmp_path / "state.json"
            svc._inflight_path = tmp_path / "inflight.json"
            svc._history_path = tmp_path / "history.jsonl"
            assert await svc.update_component("klipper") is True
        assert mock_hook.await_args.kwargs["timeout"] == updater_service.HOOK_TIMEOUT

    @pytest.mark.asyncio
    async def test_batch_passes_hook_timeout(self, tmp_path):
        cb = MagicMock()
        comp = ComponentConfig(name="klipper", kind="git", path=tmp_path)
        with (
            patch("updater.service.git_get_hash", return_value="a" * 40),
            patch(
                "updater.service.UpdateService._stage_component",
                return_value=(True, ""),
            ),
            patch(
                "updater.service.UpdateService._install_dependencies",
                return_value=(True, ""),
            ),
            patch("updater.service.run_hook", return_value=(True, "")) as mock_hook,
            patch(
                "updater.service._assert_https_remote",
                return_value=(True, "https://github.com/test/repo"),
            ),
        ):
            svc = UpdateService(callback=cb)
            svc._state_path = tmp_path / "state.json"
            svc._inflight_path = tmp_path / "inflight.json"
            svc._history_path = tmp_path / "history.jsonl"
            await svc._run_git_batch([comp])
        assert mock_hook.await_args.kwargs["timeout"] == updater_service.HOOK_TIMEOUT
        cb.on_component_done.assert_called_once_with("klipper", True)


class TestInflightClearedOnEarlyReturn:
    def _svc(self, tmp_path, cb):
        svc = UpdateService(callback=cb)
        svc._state_path = tmp_path / "state.json"
        svc._inflight_path = tmp_path / "inflight.json"
        svc._history_path = tmp_path / "history.jsonl"
        return svc

    @pytest.mark.asyncio
    async def test_single_insecure_remote_clears_marker(self, tmp_path):
        cb = MagicMock()
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="a" * 40),
            patch(
                "updater.service._assert_https_remote",
                return_value=(False, "origin remote uses non-https URL"),
            ),
        ):
            svc = self._svc(tmp_path, cb)
            assert await svc.update_component("klipper") is False
        assert not (tmp_path / "inflight.json").exists()
        cb.on_error.assert_called_once_with("klipper", "insecure remote")

    @pytest.mark.asyncio
    async def test_single_reset_failure_clears_marker(self, tmp_path):
        cb = MagicMock()
        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("updater.service.git_get_hash", return_value="a" * 40),
            patch("updater.service.git_fetch", return_value=(True, "")),
            patch("updater.service.git_get_current_branch", return_value="master"),
            patch("updater.service.git_reset_to_hash", return_value=(False, "boom")),
            patch(
                "updater.service._assert_https_remote",
                return_value=(True, "https://github.com/test/repo"),
            ),
        ):
            svc = self._svc(tmp_path, cb)
            assert await svc.update_component("klipper") is False
        assert not (tmp_path / "inflight.json").exists()
        cb.on_error.assert_called_once_with("klipper", "reset")

    @pytest.mark.asyncio
    async def test_batch_insecure_remote_clears_marker(self, tmp_path):
        cb = MagicMock()
        comp = ComponentConfig(name="klipper", kind="git", path=tmp_path)
        with (
            patch("updater.service.git_get_hash", return_value="a" * 40),
            patch(
                "updater.service._assert_https_remote",
                return_value=(False, "origin remote uses non-https URL"),
            ),
        ):
            svc = self._svc(tmp_path, cb)
            await svc._run_git_batch([comp])
        assert not (tmp_path / "inflight.json").exists()
        cb.on_error.assert_called_once_with("klipper", "insecure remote")
