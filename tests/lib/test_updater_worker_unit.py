"""Unit tests for BlocksScreen.lib.updater_worker.UpdateWorker."""

import asyncio
import sys
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from PyQt6.QtCore import QObject

_BUS = "com.blockscreen.Updater"
_UNIT = "BlocksScreen-updater.service"


def _make_worker():
    """Create UpdaterWorker without starting the asyncio daemon thread."""
    from BlocksScreen.lib.updater_worker import UpdaterWorker

    with patch.object(UpdaterWorker, "__init__", lambda self: QObject.__init__(self)):
        w = UpdaterWorker()
    loop = asyncio.new_event_loop()
    w._loop = loop
    w._listener_tasks = []
    w._watchdog_tasks = set()
    w._bg_tasks = set()
    w._reconnect_attempt = 0
    w._reconnecting = False
    w._busy_false_event = asyncio.Event()
    w._last_activity = 0.0
    w._proxy = MagicMock()
    w._shutting_down = False
    w._daemon_owner = ""
    w._owner_task = None
    w._escalated = False
    w._init_lock = asyncio.Lock()
    w._system_bus = MagicMock()
    return w


class _FakeDbus:
    """Stand-in for FreedesktopDbus yielding a scripted NameOwnerChanged stream."""

    def __init__(self, owner="", events=(), stop=None):
        self._owner = owner
        self._events = list(events)
        self._stop = stop

    async def get_name_owner(self, service_name):
        return self._owner

    @property
    def name_owner_changed(self):
        events, stop = self._events, self._stop

        async def _gen():
            for event in events:
                yield event
            if stop is not None:
                stop()

        return _gen()


def _dbus_module(fake):
    """Inject a fake sdbus_async.dbus_daemon (tests/network/conftest stubs the parent)."""
    mod = SimpleNamespace(FreedesktopDbus=lambda bus=None: fake)
    return patch.dict(sys.modules, {"sdbus_async.dbus_daemon": mod})


@pytest.fixture
def worker():
    w = _make_worker()
    yield w
    if not w._loop.is_closed():
        w._loop.close()


class TestTriggerMethods:
    def test_trigger_status_sibmits_to_loop(self, worker):
        with patch(
            "asyncio.run_coroutine_threadsafe", side_effect=lambda c, loop: c.close()
        ) as mock_rctf:
            worker.trigger_status()
        mock_rctf.assert_called_once()
        assert mock_rctf.call_args[0][1] is worker._loop

    def test_trigger_update_empty_name_calls_update_all(self, worker):
        with patch(
            "asyncio.run_coroutine_threadsafe", side_effect=lambda c, loop: c.close()
        ) as mock_rctf:
            worker.trigger_update("")
        mock_rctf.assert_called_once()

    def test_trigger_update_name_calls_update_component(self, worker):
        with patch(
            "asyncio.run_coroutine_threadsafe", side_effect=lambda c, loop: c.close()
        ) as mock_rctf:
            worker.trigger_update("klipper")
        mock_rctf.assert_called_once()

    def test_trigger_recover_submits_coroutine(self, worker):
        with patch(
            "asyncio.run_coroutine_threadsafe", side_effect=lambda c, loop: c.close()
        ) as mock_rctf:
            worker.trigger_recover("klipper", True)
        mock_rctf.assert_called_once()

    pytestmark = pytest.mark.filterwarnings("ignore::RuntimeWarning")

    def test_dead_loop_emits_daemon_unavaliable(self, worker, qtbot):
        worker._loop.close()
        received = []
        worker.daemon_unavailable.connect(lambda: received.append(True))
        worker.trigger_status()
        assert received == [True]


class TestListenerCoroutines:
    @pytest.mark.asyncio
    async def test_listen_step_complete_emits_signal(self, worker, qtbot):
        received = []
        worker.step_complete.connect(lambda n, s, t: received.append((n, s, t)))

        async def _gen():
            yield ("klipper", 1, 5)

        worker._proxy.step_complete = _gen()
        await worker._listen_step_complete()
        assert received == [("klipper", 1, 5)]

    @pytest.mark.asyncio
    async def test_listen_component_done_emits_signal(self, worker, qtbot):
        received = []
        worker.component_done.connect(lambda n, s: received.append((n, s)))

        async def _gen():
            yield ("moonraker", False)

        worker._proxy.component_done = _gen()
        await worker._listen_component_done()
        assert received == [("moonraker", False)]

    @pytest.mark.asyncio
    async def test_listen_busy_changed_emits_signal(self, worker, qtbot):
        received = []
        worker.busy_changed.connect(lambda b: received.append(b))

        async def _gen():
            yield True

        worker._proxy.busy_changed = _gen()
        await worker._listen_busy_changed()
        assert received == [True]

    @pytest.mark.asyncio
    async def test_listen_busy_changed_false_does_not_emit_request_reconnect(
        self, worker, qtbot
    ):
        """request_reconnect should NOT be emitted from _listen_busy_changed."""
        busy_changed_received = []
        reconnect_received = []
        worker.busy_changed.connect(lambda b: busy_changed_received.append(b))
        worker.request_reconnect.connect(lambda: reconnect_received.append(True))

        async def _gen():
            yield False

        worker._proxy.busy_changed = _gen()
        await worker._listen_busy_changed()
        assert busy_changed_received == [False]
        assert reconnect_received == []

    @pytest.mark.asyncio
    async def test_listen_status_ready_emtis_signal(self, worker, qtbot):
        received = []
        worker.status_ready.connect(lambda s: received.append(s))

        async def _gen():
            yield '{"klipper":{"name": "klipper"}}'

        worker._proxy.status_ready = _gen()
        await worker._listen_status_ready()
        assert len(received) == 1


class TestListenerDoneCallback:
    def test_sdbus_error_emits_daemon_unavailable(self, worker, qtbot, mock_sdbus):
        received = []
        worker.daemon_unavailable.connect(lambda: received.append(True))
        task = MagicMock()
        task.cancelled.return_value = False
        task.exception.return_value = mock_sdbus.SdBusBaseError("D-Bus gone")
        worker._on_listener_done(task)
        assert received == [True]

    def test_cancelled_task_does_not_emit(self, worker, qtbot):
        received = []
        worker.daemon_unavailable.connect(lambda: received.append(True))
        task = MagicMock()
        task.cancelled.return_value = True
        worker._on_listener_done(task)
        assert received == []

    def test_normal_exit_does_not_emit(self, worker, qtbot):
        received = []
        worker.daemon_unavailable.connect(lambda: received.append(True))
        task = MagicMock()
        task.cancelled.return_value = False
        task.exception.return_value = None
        worker._on_listener_done(task)
        assert received == []


class TestWatchdog:
    @pytest.mark.asyncio
    async def test_watchdog_resolves_when_event_set(self, worker):
        worker._busy_false_event.set()
        await worker._busy_watchdog()  # must not raise or emit

    @pytest.mark.asyncio
    async def test_watchdog_emits_after_idle_limit(self, worker, qtbot):
        received = []
        worker.daemon_unavailable.connect(lambda: received.append(True))
        worker._busy_false_event.clear()
        # Last activity far in the past → idle exceeds the limit → emit at once.
        worker._last_activity = worker._loop.time() - 100_000
        await worker._busy_watchdog()
        assert received == [True]


class TestDaemonOwnerWatch:
    """Crash recovery: NameOwnerChanged resync instead of the 6-minute busy watchdog."""

    @staticmethod
    def _patch_dbus(worker, owner="", events=()):
        def _stop():
            worker._shutting_down = True

        return _dbus_module(_FakeDbus(owner=owner, events=events, stop=_stop))

    @pytest.mark.asyncio
    async def test_new_owner_triggers_resync(self, worker):
        worker._async_initialize = AsyncMock()
        with self._patch_dbus(worker, "", [(_BUS, "", ":1.5")]):
            await worker._watch_daemon_owner()
        # Owner passed through, not stored here: _async_initialize owns that field.
        worker._async_initialize.assert_awaited_once_with(":1.5")

    @pytest.mark.asyncio
    async def test_owner_lost_emits_unavailable_without_resync(self, worker, qtbot):
        received = []
        worker.daemon_unavailable.connect(lambda: received.append(True))
        worker._async_initialize = AsyncMock()
        with self._patch_dbus(worker, ":1.5", [(_BUS, ":1.5", "")]):
            await worker._watch_daemon_owner()
        assert received == [True]
        worker._async_initialize.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_other_names_and_repeat_owner_ignored(self, worker):
        worker._async_initialize = AsyncMock()
        events = [("org.other.Thing", "", ":1.9"), (_BUS, ":1.5", ":1.5")]
        with self._patch_dbus(worker, ":1.5", events):
            await worker._watch_daemon_owner()
        worker._async_initialize.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_watch_survives_stream_failure(self, worker):
        """Losing the watch must retry, not kill the fast recovery path."""
        worker._async_initialize = AsyncMock()

        class _Broken(_FakeDbus):
            @property
            def name_owner_changed(self):
                raise RuntimeError("bus dropped")

        fake = _Broken()

        async def _sleep(_delay):
            worker._shutting_down = True

        with _dbus_module(fake), patch("asyncio.sleep", _sleep):
            await worker._watch_daemon_owner()  # must return, not raise

    @pytest.mark.asyncio
    async def test_stream_closed_when_body_raises(self, worker):
        """Abandoning the generator without aclose leaks its match slot until GC."""
        closed = []

        async def _gen():
            try:
                yield (_BUS, "", ":1.9")
                yield (_BUS, "", ":1.10")
            finally:
                closed.append(True)

        class _Leaky(_FakeDbus):
            @property
            def name_owner_changed(self):
                return _gen()

        worker._async_initialize = AsyncMock(side_effect=RuntimeError("boom"))

        async def _sleep(_delay):
            worker._shutting_down = True

        with _dbus_module(_Leaky()), patch("asyncio.sleep", _sleep):
            await worker._watch_daemon_owner()
        assert closed == [True]
        worker._async_initialize.assert_awaited_once_with(":1.9")


class TestEscalation:
    @pytest.mark.asyncio
    async def test_delayed_reconnect_escalates_when_unowned(self, worker):
        worker._reconnect_attempt = 3
        worker._name_owner = AsyncMock(return_value="")
        worker._escalate_restart = AsyncMock()
        worker._async_initialize = AsyncMock()
        with patch("asyncio.sleep", AsyncMock()):
            await worker._delayed_reconnect(5.0)
        worker._escalate_restart.assert_awaited_once()
        worker._async_initialize.assert_awaited_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("attempt", "owner"), [(3, ":1.7"), (1, "")])
    async def test_no_escalation_when_owned_or_early(self, worker, attempt, owner):
        worker._reconnect_attempt = attempt
        worker._name_owner = AsyncMock(return_value=owner)
        worker._escalate_restart = AsyncMock()
        worker._async_initialize = AsyncMock()
        with patch("asyncio.sleep", AsyncMock()):
            await worker._delayed_reconnect(5.0)
        worker._escalate_restart.assert_not_awaited()
        worker._async_initialize.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_shutdown_during_backoff_skips_reconnect(self, worker):
        worker._reconnecting = True
        worker._async_initialize = AsyncMock()

        async def _sleep(_delay):
            worker._shutting_down = True

        with patch("asyncio.sleep", _sleep):
            await worker._delayed_reconnect(5.0)
        worker._async_initialize.assert_not_awaited()
        assert worker._reconnecting is False

    @pytest.mark.asyncio
    async def test_escalate_uses_exact_sudoers_argv(self, worker):
        """argv order is load-bearing: NOPASSWD rules match it literally."""
        worker._run_systemctl = AsyncMock()
        await worker._escalate_restart()
        assert [c.args[0] for c in worker._run_systemctl.call_args_list] == [
            ("reset-failed", _UNIT),
            ("--no-block", "restart", _UNIT),
        ]

    @pytest.mark.asyncio
    async def test_escalate_latched_until_next_connect(self, worker):
        worker._run_systemctl = AsyncMock()
        await worker._escalate_restart()
        await worker._escalate_restart()
        assert worker._run_systemctl.await_count == 2  # first call only
        assert worker._escalated is True

    @pytest.mark.asyncio
    async def test_run_systemctl_contains_spawn_failure(self, worker):
        with patch("asyncio.create_subprocess_exec", side_effect=OSError("no sudo")):
            await worker._run_systemctl(("reset-failed", _UNIT))  # must not raise

    @pytest.mark.asyncio
    async def test_run_systemctl_passes_sudo_n(self, worker):
        proc = MagicMock(returncode=0)
        proc.communicate = AsyncMock(return_value=(b"", b""))
        with patch(
            "asyncio.create_subprocess_exec", AsyncMock(return_value=proc)
        ) as spawn:
            await worker._run_systemctl(("reset-failed", _UNIT))
        assert spawn.call_args[0] == (
            "sudo",
            "-n",
            "/usr/bin/systemctl",
            "reset-failed",
            _UNIT,
        )

    @pytest.mark.asyncio
    async def test_run_systemctl_kills_on_timeout(self, worker):
        """A hung sudo must be reaped, else it holds the pipe and child slot forever."""
        proc = MagicMock(returncode=None)
        proc.communicate = AsyncMock(side_effect=TimeoutError)
        proc.wait = AsyncMock(return_value=-9)
        with patch("asyncio.create_subprocess_exec", AsyncMock(return_value=proc)):
            await worker._run_systemctl(("reset-failed", _UNIT))
        proc.kill.assert_called_once()
        proc.wait.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_name_owner_empty_on_error(self, worker):
        """NameHasNoOwner/timeouts must read as 'unowned', which is what gates escalation."""
        fake = MagicMock()
        fake.get_name_owner = AsyncMock(side_effect=TimeoutError)
        with _dbus_module(fake):
            assert await worker._name_owner() == ""

    @pytest.mark.asyncio
    async def test_failed_reconnect_clears_latch_and_retries(self, worker):
        """A stuck _reconnecting latch would silence every later reconnect."""
        worker._async_initialize = AsyncMock(side_effect=RuntimeError("boom"))
        worker._schedule_reconnect = MagicMock()
        worker._reconnecting = True
        with patch("asyncio.sleep", AsyncMock()):
            await worker._delayed_reconnect(5.0)
        assert worker._reconnecting is False
        worker._schedule_reconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancelled_reconnect_clears_latch(self, worker):
        worker._async_initialize = AsyncMock(side_effect=asyncio.CancelledError)
        worker._reconnecting = True
        with patch("asyncio.sleep", AsyncMock()), pytest.raises(asyncio.CancelledError):
            await worker._delayed_reconnect(5.0)
        assert worker._reconnecting is False


class TestInitSerialization:
    """Cold boot activates the daemon itself, so the owner watcher must not double-connect."""

    @pytest.mark.asyncio
    async def test_resync_skipped_for_already_connected_owner(self, worker):
        worker._connect = AsyncMock()
        worker._daemon_owner = ":1.5"
        await worker._async_initialize(":1.5")
        worker._connect.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("expect_owner", ["", ":1.6"])
    async def test_connect_runs_for_new_or_unknown_owner(self, worker, expect_owner):
        worker._connect = AsyncMock()
        worker._daemon_owner = ":1.5"
        await worker._async_initialize(expect_owner)
        worker._connect.assert_awaited_once()


class TestShutdown:
    def test_shutdown_calls_cancel_on_all_tasks(self, worker):
        mock_task = MagicMock()
        worker._listener_tasks = [mock_task]
        calls = []
        worker._loop.call_soon_threadsafe = lambda fn, *args: calls.append(fn)
        worker.shutdown()
        assert len(calls) == 1  # single _cancel_and_stop callback

    def test_shutdown_cancels_owner_watch(self, worker):
        owner_task, listener = MagicMock(), MagicMock()
        worker._owner_task = owner_task
        worker._listener_tasks = [listener]
        worker._loop.call_soon_threadsafe = lambda fn, *args: fn()
        worker.shutdown()
        owner_task.cancel.assert_called_once()
        listener.cancel.assert_called_once()
