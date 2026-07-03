import threading
import time

from BlocksScreen.lib.utils.RepeatedTimer import RepeatedTimer

def test_stop_during_callback_does_not_rearm():
    """stopTimer() called while the callback is running must stop the timer. """
    in_callback = threading.Event()
    release = threading.Event()
    calls = []

    def slow_cb():
        calls.append(1)
        in_callback.set()
        release.wait(timeout=2)

    rt = RepeatedTimer(0.01, slow_cb)
    assert in_callback.wait(timeout=2), "callback never ran"

    rt.stopTimer()          # stop while the callback is still executing
    release.set()

    time.sleep(0.2)         # give any erroneous re-arm time to fire
    assert rt.running is False
    assert len(calls) == 1, f"timer re-armed after stop: {len(calls)} calls"

def test_normal_repeat_still_fires():
    calls = []
    rt = RepeatedTimer(0.01, lambda: calls.append(1))
    time.sleep(0.1)
    rt.stopTimer()
    assert len(calls) >= 2
