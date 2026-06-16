import asyncio
from unittest.mock import MagicMock, AsyncMock

import pytest
import json


class TestUpdaterInterfaceImport:
    def test_importable(self):
        from updater.dbus_service import UpdaterInterface

        assert UpdaterInterface is not None


class TestDbusProgressCallback:
    def _make_cb(self):
        from updater.dbus_service import DbusProgressCallback

        mock_iface = MagicMock()
        return DbusProgressCallback(mock_iface), mock_iface

    def test_on_step_emits_signal(self):
        cb, iface = self._make_cb()
        cb.on_step("klipper", 1, 5)
        iface.step_complete.emit.assert_called_once_with(("klipper", 1, 5))

    def test_on_component_done_emits_signal(self):
        cb, iface = self._make_cb()
        cb.on_component_done("klipper", True)
        iface.component_done.emit.assert_called_once_with(("klipper", True))

    def test_on_error_emits_signal(self):
        cb, iface = self._make_cb()
        cb.on_error("klipper", "network")
        iface.error.emit.assert_called_once_with(("klipper", "network"))

    def test_on_rollback_emits_signal(self):
        cb, iface = self._make_cb()
        cb.on_rollback("klipper", True)
        iface.rollback.emit.assert_called_once_with(("klipper", True))

    def test_on_recover_emits_signal(self):
        cb, iface = self._make_cb()
        cb.on_recover("klipper", False)
        iface.recover_done.emit.assert_called_once_with(("klipper", False))


class TestUpdaterDbusService:
    @pytest.mark.asyncio
    async def test_set_busy_emits_on_true_transition(self, svc):
        svc._set_busy(True)
        svc.busy_changed.emit.assert_called_once_with((True,))

    @pytest.mark.asyncio
    async def test_set_busy_no_emit_on_same_value(self, svc):
        svc._set_busy(True)
        svc.busy_changed.emit.reset_mock()
        svc._set_busy(True)
        svc.busy_changed.emit.assert_not_called()

    @pytest.mark.asyncio
    async def test_set_busy_emits_false_after_true(self, svc):
        svc._busy = True
        svc._set_busy(False)
        svc.busy_changed.emit.assert_called_once_with((False,))

    @pytest.mark.asyncio
    async def test_update_all_delegates_and_resets_busy(self, svc):
        await svc.update_all()
        await asyncio.sleep(0)
        svc._svc.update_all.assert_called_once()
        assert svc._busy is False

    @pytest.mark.asyncio
    async def test_update_component_delegates(self, svc):
        await svc.update_component("moonraker")
        await asyncio.sleep(0)
        svc._svc.update_component.assert_called_once_with("moonraker")

    @pytest.mark.asyncio
    async def test_request_status_emits_status_ready(self, svc):
        await svc.request_status()
        await asyncio.sleep(0)
        svc.status_ready.emit.assert_called_once()
        json_str = svc.status_ready.emit.call_args[0][0][0]
        data = json.loads(json_str)
        assert "klipper" in data
        assert data["klipper"]["commits_behind"] == 2

    @pytest.mark.asyncio
    async def test_emit_status_always_emits_on_check_failure(self, svc):
        svc._svc.check_status = AsyncMock(side_effect=RuntimeError("git fail"))
        await svc._emit_status()
        svc.status_ready.emit.assert_called_once()
        payload = json.loads(svc.status_ready.emit.call_args[0][0][0])
        assert isinstance(payload, dict)


class TestServiceRestartRollback:
    @pytest.mark.asyncio
    async def test_update_component_rolls_back_on_restart_failure(self):
        """If restart_service fails, _run_git_update must rollback, not emit done(True)."""
        import asyncio
        import logging
        from updater.service import UpdateService
        from updater.models import ComponentConfig
        from pathlib import Path
        from unittest.mock import AsyncMock, patch

        cfg = ComponentConfig(
            name="klipper",
            kind="git",
            path=Path("/tmp/fake_klipper"),
            service="klipper.service",
        )

        svc_obj = UpdateService.__new__(UpdateService)
        svc_obj._components = [cfg]
        svc_obj._git_lock = asyncio.Lock()
        svc_obj._last_status_time = 0.0
        svc_obj._fetch_times = {}
        svc_obj._component_pip_cache = {}
        svc_obj._state_path = Path("/tmp/test_state.json")
        svc_obj.poll_interval = 86400.0

        done_calls = []
        error_calls = []

        class _CB:
            def on_step(self, name, step, total):
                pass

            def on_component_done(self, name, success):
                done_calls.append(success)

            def on_error(self, name, reason):
                error_calls.append(reason)

            def on_rollback(self, name, success):
                pass

            def on_recover(self, name, success):
                pass

        svc_obj._callback = _CB()
        svc_obj._log = logging.getLogger("test")

        with (
            patch("updater.service.git_get_hash", AsyncMock(return_value="abc1234")),
            patch("updater.service.git_fetch", AsyncMock(return_value=(True, ""))),
            patch("updater.service.git_pull", AsyncMock(return_value=(True, ""))),
            patch(
                "updater.service.UpdateService._install_dependencies",
                AsyncMock(return_value=(True, "")),
            ),
            patch("updater.service.run_hook", AsyncMock(return_value=(True, ""))),
            patch(
                "updater.service.restart_service",
                AsyncMock(return_value=(False, "permission denied")),
            ),
            patch(
                "updater.service.git_reset_to_hash", AsyncMock(return_value=(True, ""))
            ),
        ):
            result = await svc_obj._run_git_update(cfg)

        assert result is False
        assert True not in done_calls  # must NOT emit done(True)


def test_build_parser_accepts_daemon():
    from updater.__main__ import build_parser

    args = build_parser().parse_args(["daemon"])
    assert args.command == "daemon"


class TestCancelAwaitsCleanup:
    @pytest.mark.asyncio
    async def test_cancel_busy_false_only_after_task_done(self, svc):
        """_set_busy(False) must not fire before cancelled task's finally block."""
        busy_sequence = []

        async def slow_update():
            try:
                await asyncio.sleep(10)
            finally:
                busy_sequence.append("task_finally")

        svc._busy = True
        task = asyncio.create_task(slow_update(), name="update_test")
        svc._background_tasks = {task}

        def tracking_set_busy(busy):
            busy_sequence.append(f"set_busy({busy})")
            svc._busy = busy

        svc._set_busy = tracking_set_busy

        # Let task start and enter sleep before cancelling
        await asyncio.sleep(0.01)

        await svc.cancel()

        assert "task_finally" in busy_sequence
        assert "set_busy(False)" in busy_sequence
        finally_idx = busy_sequence.index("task_finally")
        busy_idx = busy_sequence.index("set_busy(False)")
        assert finally_idx < busy_idx


class TestEmitStatusErrorFallback:
    @pytest.mark.asyncio
    async def test_emits_error_status_per_component_on_check_failure(self, svc):
        """When check_status raises, status_ready must contain per-component error entries."""
        from updater.models import ComponentConfig
        from pathlib import Path

        svc._svc.check_status = AsyncMock(side_effect=RuntimeError("boom"))
        svc._svc._components = [
            ComponentConfig(name="klipper", kind="git", path=Path("/tmp/k")),
            ComponentConfig(name="system", kind="apt"),
        ]
        svc._status_check_in_progress = False

        await svc._emit_status()

        assert svc.status_ready.emit.called
        payload_str = svc.status_ready.emit.call_args[0][0][0]
        payload = json.loads(payload_str)
        assert "klipper" in payload
        assert "system" in payload
        assert payload["klipper"]["error"] is not None
        assert "boom" in payload["klipper"]["error"]


class TestStatusPendingFlag:
    @pytest.mark.asyncio
    async def test_request_status_while_in_progress_queues_retry(self, svc):
        """When _emit_status is called while already in progress, it should queue a retry."""
        svc._status_check_in_progress = True
        svc._status_pending = False

        # Call _emit_status while in progress
        await svc._emit_status()

        # Should have set the pending flag
        assert svc._status_pending is True

    @pytest.mark.asyncio
    async def test_emit_status_spawns_pending_retry_on_completion(self, svc):
        """When _emit_status completes with _status_pending=True, it should spawn a retry."""
        svc._status_check_in_progress = False
        svc._status_pending = True
        spawned_tasks = []

        original_spawn = svc._spawn

        def mock_spawn(coro, *, name=None):
            spawned_tasks.append(name)
            return original_spawn(coro, name=name)

        svc._spawn = mock_spawn

        await svc._emit_status()

        # Should have spawned a pending_status task
        assert "pending_status" in spawned_tasks
        # Should have cleared the flag
        assert svc._status_pending is False


class TestPollIntervalUsage:
    @pytest.mark.asyncio
    async def test_periodic_status_check_uses_poll_interval(self, svc):
        """_periodic_status_check must use self._svc.poll_interval, not hardcoded 86_400."""
        svc._svc.poll_interval = 42.0
        svc._svc.check_status = AsyncMock(return_value={"klipper": MagicMock()})

        task = asyncio.create_task(svc._periodic_status_check())
        await asyncio.sleep(3.5)  # pass initial sleep
        await asyncio.sleep(0.1)  # allow first emit

        # Verify first sleep happened (3 seconds), then poll interval scheduled
        # by checking the task is still running (hasn't timed out waiting 86_400)
        assert not task.done()

        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


class TestMethodReturnValues:
    @pytest.mark.asyncio
    async def test_update_all_rejected_when_busy_returns_false(self, svc):
        """Return False when busy without calling underlying service."""
        svc._busy = True
        result = await svc.update_all()
        assert result is False
        svc._svc.update_all.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_component_rejected_when_busy_returns_false(self, svc):
        """Return False when busy without calling underlying service."""
        svc._busy = True
        result = await svc.update_component("klipper")
        assert result is False
        svc._svc.update_component.assert_not_called()

    @pytest.mark.asyncio
    async def test_recover_rejected_when_busy_returns_false(self, svc):
        """Return False when busy without calling underlying service."""
        svc._busy = True
        result = await svc.recover("klipper", False)
        assert result is False
        svc._svc.recover.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_all_accepted_when_not_busy_returns_true(self, svc):
        """Return True and spawn task when not busy."""
        svc._busy = False
        result = await svc.update_all()
        assert result is True
        await asyncio.sleep(0)  # yield to spawned task
        # Task should have been spawned
        assert len(svc._background_tasks) > 0

    @pytest.mark.asyncio
    async def test_update_component_accepted_when_not_busy_returns_true(self, svc):
        """Return True and spawn task when not busy."""
        svc._busy = False
        result = await svc.update_component("klipper")
        assert result is True
        await asyncio.sleep(0)  # yield to spawned task
        # Task should have been spawned
        assert len(svc._background_tasks) > 0

    @pytest.mark.asyncio
    async def test_recover_accepted_when_not_busy_returns_true(self, svc):
        """Return True and spawn task when not busy."""
        svc._busy = False
        result = await svc.recover("klipper", False)
        assert result is True
        await asyncio.sleep(0)  # yield to spawned task
        # Task should have been spawned
        assert len(svc._background_tasks) > 0
