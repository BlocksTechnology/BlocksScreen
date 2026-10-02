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
    w._reconnect_task = None
    w._busy_false_event = asyncio.Event()
    w._last_activity = 0.0
    w._proxy = MagicMock()
    w._shutting_down = False
    w._last_busy = False
    w._last_provisioning = False
    w._provisioning_signals = 0
    w._printing = None
    w._daemon_owner = ""
    w._owner_task = None
    w._escalated = False
    w._init_lock = asyncio.Lock()
    w._system_bus = MagicMock()
    return w


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


class _Msg:
    """NameOwnerChanged message; a callable payload runs on read (stop or fail)."""

    def __init__(self, contents):
        self._contents = contents

    def get_contents(self):
        return self._contents() if callable(self._contents) else self._contents


class TestDaemonOwnerWatch:
    """Crash recovery: NameOwnerChanged resync instead of the 6-minute busy watchdog."""

    @staticmethod
    def _subscribe(worker, *batches, owner=""):
        """Each subscribe delivers the next batch before the seed; returns the slots."""
        slots = []
        pending = iter(batches)

        async def _match(*args):
            for event in next(pending):
                args[4](_Msg(event))
            slots.append(MagicMock())
            return slots[-1]

        worker._system_bus.match_signal_async = _match
        return slots, _dbus_module(
            MagicMock(get_name_owner=AsyncMock(return_value=owner))
        )

    @staticmethod
    def _stop(worker):
        def _read():
            worker._shutting_down = True
            return ("org.other.Thing", "", "")

        return _read

    @pytest.mark.asyncio
    async def test_new_owner_triggers_resync(self, worker):
        worker._async_initialize = AsyncMock()
        _, dbus = self._subscribe(worker, [(_BUS, "", ":1.5"), self._stop(worker)])
        with dbus:
            await worker._watch_daemon_owner()
        # Owner passed through, not stored here: _async_initialize owns that field.
        worker._async_initialize.assert_awaited_once_with(":1.5")

    @pytest.mark.asyncio
    async def test_owner_lost_emits_unavailable_and_schedules_reconnect(
        self, worker, qtbot
    ):
        """A stopped unit is bus-activated again by the retry, so the worker retries."""
        received = []
        worker.daemon_unavailable.connect(lambda: received.append(True))
        worker._async_initialize = AsyncMock()
        worker._schedule_reconnect = MagicMock()
        _, dbus = self._subscribe(
            worker, [(_BUS, ":1.5", ""), self._stop(worker)], owner=":1.5"
        )
        with dbus:
            await worker._watch_daemon_owner()
        assert received == [True]
        worker._async_initialize.assert_not_awaited()
        worker._schedule_reconnect.assert_called_once_with()

    @pytest.mark.asyncio
    async def test_other_names_and_repeat_owner_ignored(self, worker):
        worker._async_initialize = AsyncMock()
        events = [("org.other.Thing", "", ":1.9"), (_BUS, ":1.5", ":1.5")]
        _, dbus = self._subscribe(worker, [*events, self._stop(worker)], owner=":1.5")
        with dbus:
            await worker._watch_daemon_owner()
        worker._async_initialize.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_subscribes_before_seeding(self, worker):
        """Seeding first would miss a restart landing between seed and subscribe."""
        slots, _ = self._subscribe(worker, [self._stop(worker)])
        seen = []

        async def _owner(_name):
            seen.append(len(slots))
            return ""

        with _dbus_module(MagicMock(get_name_owner=_owner)):
            await worker._watch_daemon_owner()
        assert seen == [1]

    @pytest.mark.asyncio
    async def test_watch_survives_subscribe_failure(self, worker):
        """Losing the watch must retry, not kill the fast recovery path."""
        worker._system_bus.match_signal_async = AsyncMock(
            side_effect=RuntimeError("bus dropped")
        )

        async def _sleep(_delay):
            worker._shutting_down = True

        with patch("asyncio.sleep", _sleep):
            await worker._watch_daemon_owner()  # must return, not raise

    @pytest.mark.asyncio
    async def test_slot_closed_when_body_raises(self, worker):
        """An unclosed match slot keeps queueing signals until GC."""
        worker._async_initialize = AsyncMock(side_effect=RuntimeError("boom"))
        slots, dbus = self._subscribe(worker, [(_BUS, "", ":1.9"), (_BUS, "", ":1.10")])

        async def _sleep(_delay):
            worker._shutting_down = True

        with dbus, patch("asyncio.sleep", _sleep):
            await worker._watch_daemon_owner()
        slots[0].close.assert_called_once_with()
        worker._async_initialize.assert_awaited_once_with(":1.9")

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("reseed", "resyncs"), [(":1.6", True), (":1.5", False)])
    async def test_reseed_after_gap_resyncs_new_owner(self, worker, reseed, resyncs):
        """A restart while the watch was down emits no signal: the re-seed must catch it."""
        worker._async_initialize = AsyncMock()

        def _drop():
            raise RuntimeError("bus dropped")

        _, dbus = self._subscribe(worker, [_drop], [self._stop(worker)])
        fake = MagicMock(get_name_owner=AsyncMock(side_effect=[":1.5", reseed]))

        async def _sleep(_delay):
            pass

        with dbus, _dbus_module(fake), patch("asyncio.sleep", _sleep):
            await worker._watch_daemon_owner()
        if resyncs:
            worker._async_initialize.assert_awaited_once_with(reseed)
        else:
            worker._async_initialize.assert_not_awaited()


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
        proc.communicate = AsyncMock(side_effect=[TimeoutError, (b"", b"")])
        with patch("asyncio.create_subprocess_exec", AsyncMock(return_value=proc)):
            await worker._run_systemctl(("reset-failed", _UNIT))
        proc.kill.assert_called_once()
        # Reaped via communicate so the stderr PIPE is drained, not a bare wait().
        assert proc.communicate.await_count == 2

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

    @pytest.mark.asyncio
    async def test_superseded_reconnect_keeps_new_latch(self, worker):
        """A cancelled stale retry must not clear the latch its replacement armed."""
        worker._async_initialize = AsyncMock(side_effect=asyncio.CancelledError)
        worker._reconnecting = True
        worker._reconnect_task = MagicMock()  # the replacement retry
        with patch("asyncio.sleep", AsyncMock()), pytest.raises(asyncio.CancelledError):
            await worker._delayed_reconnect(5.0)
        assert worker._reconnecting is True

    @pytest.mark.asyncio
    async def test_connect_cancels_pending_retry(self, worker, mock_sdbus):
        """An owner-watch resync plus a sleeping retry would connect twice."""
        pending = MagicMock()
        worker._reconnect_task = pending
        worker._reconnecting = True
        worker._schedule_reconnect = MagicMock()
        new_proxy = MagicMock(side_effect=mock_sdbus.SdBusBaseError("gone"))
        fake_mod = SimpleNamespace(
            UpdaterInterface=SimpleNamespace(new_proxy=new_proxy)
        )
        with patch.dict(sys.modules, {"updater.dbus_service": fake_mod}):
            await worker._connect()
        pending.cancel.assert_called_once()
        assert worker._reconnect_task is None
        assert worker._reconnecting is False
        worker._schedule_reconnect.assert_called_once()


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


class TestReplayBusy:
    def test_replays_true_only(self, worker, qtbot):
        received: list[bool] = []
        worker.busy_changed.connect(received.append)
        worker.replay_busy()
        assert received == []
        worker._last_busy = True
        worker.replay_busy()
        assert received == [True]

    def test_replays_provisioning_before_busy(self, worker, qtbot):
        order: list[str] = []
        worker.provisioning_changed.connect(lambda v: order.append(f"prov={v}"))
        worker.busy_changed.connect(lambda v: order.append(f"busy={v}"))
        worker._last_busy = worker._last_provisioning = True
        worker.replay_busy()
        assert order == ["prov=True", "busy=True"]


class TestGetProvisioning:
    @pytest.mark.asyncio
    async def test_old_daemon_without_method_is_not_provisioning(self, worker):
        import sdbus

        worker._proxy.get_provisioning = AsyncMock(
            side_effect=sdbus.SdBusBaseError("unknown method")
        )
        assert await worker._get_provisioning() is False

    @pytest.mark.asyncio
    async def test_returns_daemon_answer(self, worker):
        worker._proxy.get_provisioning = AsyncMock(return_value=True)
        assert await worker._get_provisioning() is True


class TestPollProvisioning:
    @pytest.mark.asyncio
    async def test_poll_seeds_the_value(self, worker):
        worker._proxy.get_provisioning = AsyncMock(return_value=True)
        await worker._poll_provisioning(True)
        assert worker._last_provisioning is True

    @pytest.mark.asyncio
    async def test_not_busy_skips_the_poll(self, worker):
        worker._proxy.get_provisioning = AsyncMock(return_value=True)
        await worker._poll_provisioning(False)
        assert worker._last_provisioning is False
        worker._proxy.get_provisioning.assert_not_called()

    @pytest.mark.asyncio
    async def test_signal_during_poll_wins(self, worker):
        async def slow_poll():
            # The listener delivers the real transition while the poll is in flight.
            worker._last_provisioning = False
            worker._provisioning_signals += 1
            return True

        worker._proxy.get_provisioning = slow_poll
        await worker._poll_provisioning(True)
        assert worker._last_provisioning is False


class TestSetPrinting:
    def test_only_changes_are_sent(self, worker):
        with patch(
            "asyncio.run_coroutine_threadsafe", side_effect=lambda c, loop: c.close()
        ) as mock_rctf:
            worker.trigger_set_printing(True)
            worker.trigger_set_printing(True)
        mock_rctf.assert_called_once()
        assert worker._printing is True

    @pytest.mark.asyncio
    async def test_unknown_state_is_not_sent(self, worker):
        worker._proxy.set_printing = AsyncMock()
        await worker._call_set_printing()
        worker._proxy.set_printing.assert_not_called()

    @pytest.mark.asyncio
    async def test_old_daemon_without_method_is_not_retried(self, worker):
        import sdbus

        worker._printing = True
        worker._proxy.set_printing = AsyncMock(
            side_effect=sdbus.dbus_exceptions.DbusUnknownMethodError("unknown method")
        )
        await worker._call_set_printing()
        worker._proxy.set_printing.assert_awaited_once()
        assert not worker._reconnecting

    @pytest.mark.asyncio
    async def test_failed_send_is_retried_with_the_current_state(self, worker):
        import sdbus

        sent = []

        async def send(printing):
            sent.append(printing)
            if len(sent) == 1:
                worker._printing = False
                raise sdbus.SdBusBaseError("timeout")

        worker._printing = True
        worker._proxy.set_printing = send
        with patch("asyncio.sleep", new=AsyncMock()):
            await worker._call_set_printing()
        assert sent == [True, False]

    @pytest.mark.asyncio
    async def test_gives_up_after_three_tries(self, worker):
        import sdbus

        worker._printing = True
        worker._proxy.set_printing = AsyncMock(side_effect=sdbus.SdBusBaseError("down"))
        with patch("asyncio.sleep", new=AsyncMock()):
            await worker._call_set_printing()
        assert worker._proxy.set_printing.await_count == 3
        assert not worker._reconnecting
