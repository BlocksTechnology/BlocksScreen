"""Unit tests for BlocksScreen.lib.updater_worker.UpdateWorker."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtCore import QObject


def _make_worker():
    """Create UpdaterWorker without starting the asyncio daemon thread."""
    from BlocksScreen.lib.updater_worker import UpdaterWorker

    with patch.object(UpdaterWorker, "__init__", lambda self: QObject.__init__(self)):
        w = UpdaterWorker()
    loop = asyncio.new_event_loop()
    w._loop = loop
    w._listener_tasks = []
    w._watchdog_tasks = set()
    w._reconnect_attempt = 0
    w._reconnecting = False
    w._busy_false_event = asyncio.Event()
    w._last_activity = 0.0
    w._proxy = MagicMock()
    return w


@pytest.fixture
def worker():
    w = _make_worker()
    yield w
    if not w._loop.is_closed():
        w._loop.close()


class TestTriggerMethods:
    def test_trigger_status_sibmits_to_loop(self, worker):
        with patch(
            "asyncio.run_coroutine_threadsafe", side_effect=lambda c, l: c.close()
        ) as mock_rctf:
            worker.trigger_status()
        mock_rctf.assert_called_once()
        assert mock_rctf.call_args[0][1] is worker._loop

    def test_trigger_update_empty_name_calls_update_all(self, worker):
        with patch(
            "asyncio.run_coroutine_threadsafe", side_effect=lambda c, l: c.close()
        ) as mock_rctf:
            worker.trigger_update("")
        mock_rctf.assert_called_once()

    def test_trigger_update_name_calls_update_component(self, worker):
        with patch(
            "asyncio.run_coroutine_threadsafe", side_effect=lambda c, l: c.close()
        ) as mock_rctf:
            worker.trigger_update("klipper")
        mock_rctf.assert_called_once()

    def test_trigger_recover_submits_coroutine(self, worker):
        with patch(
            "asyncio.run_coroutine_threadsafe", side_effect=lambda c, l: c.close()
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


class TestShutdown:
    def test_shutdown_calls_cancel_on_all_tasks(self, worker):
        mock_task = MagicMock()
        worker._listener_tasks = [mock_task]
        calls = []
        worker._loop.call_soon_threadsafe = lambda fn, *args: calls.append(fn)
        worker.shutdown()
        assert len(calls) == 1  # single _cancel_and_stop callback
