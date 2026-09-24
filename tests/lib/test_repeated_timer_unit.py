import sys
import threading
import time
from types import SimpleNamespace

from BlocksScreen.lib.utils.RepeatedTimer import RepeatedTimer


def test_stop_during_callback_does_not_rearm():
    """stopTimer() called while the callback is running must stop the timer."""
    in_callback = threading.Event()
    release = threading.Event()
    calls = []

    def slow_cb():
        calls.append(1)
        in_callback.set()
        release.wait(timeout=2)

    rt = RepeatedTimer(0.01, slow_cb)
    assert in_callback.wait(timeout=2), "callback never ran"

    rt.stopTimer()  # stop while the callback is still executing
    release.set()

    time.sleep(0.2)  # give any erroneous re-arm time to fire
    assert rt.running is False
    assert len(calls) == 1, f"timer re-armed after stop: {len(calls)} calls"


def test_normal_repeat_still_fires():
    calls = []
    rt = RepeatedTimer(0.01, lambda: calls.append(1))
    time.sleep(0.1)
    rt.stopTimer()
    assert len(calls) >= 2


def test_stop_racing_start_never_joins_unstarted_thread(monkeypatch):
    """stopTimer() during startTimer() must wait for the start, not join an unstarted thread."""
    entered, release = threading.Event(), threading.Event()

    class _SlowStart(threading.Thread):
        def start(self):
            entered.set()
            release.wait(timeout=2)
            super().start()

    rt = RepeatedTimer(10, lambda: None)
    rt.stopTimer()
    monkeypatch.setattr(
        sys.modules[RepeatedTimer.__module__],
        "threading",
        SimpleNamespace(
            Thread=_SlowStart,
            Event=threading.Event,
            Lock=threading.Lock,
            current_thread=threading.current_thread,
        ),
    )
    errors = []

    def stop():
        try:
            rt.stopTimer()
        except RuntimeError as e:
            errors.append(e)

    starter = threading.Thread(target=rt.startTimer)
    starter.start()
    assert entered.wait(timeout=2), "startTimer never reached Thread.start"
    stopper = threading.Thread(target=stop)
    stopper.start()
    stopper.join(timeout=0.2)  # stays blocked on the lock until start() returns
    release.set()
    starter.join(timeout=2)
    stopper.join(timeout=2)
    assert errors == []
    assert rt.running is False
