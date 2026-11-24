"""UDisksDBusAsync.close() must never hang or abort the app."""

import os
import pathlib
import subprocess  # nosec B404
import sys

import pytest

_SRC = pathlib.Path(__file__).resolve().parents[2] / "BlocksScreen"

# A GIL deadlock or qFatal is only observable from outside the process.
_CHILD = """
import gc, importlib.util, pathlib, sys, types
from PyQt6 import QtCore, sip

src = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(src))
pkg = types.ModuleType("_u")
pkg.__path__ = [str(src / "devices/storage")]
sys.modules["_u"] = pkg
spec = importlib.util.spec_from_file_location("_u.udisks2", src / "devices/storage/udisks2.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["_u.udisks2"] = mod
spec.loader.exec_module(mod)
mod._STOP_WAIT_MS = 300


class Monitor(mod.UDisksDBusAsync):
    def __init__(self, parent, mode):
        QtCore.QThread.__init__(self, parent)
        self.loop, self.controlled_devs, self._active, self.mode = None, {}, False, mode

    def run(self):
        if self.mode == "self":  # SdBusBaseError path
            self.close()
            self.returned = True
            return
        while True:  # busy past the stop deadline
            sum(range(1000))


app = QtCore.QCoreApplication(sys.argv)
owner = QtCore.QObject()
mon = Monitor(owner, sys.argv[2])
mon.start()
if sys.argv[2] == "self":
    assert mon.wait(5000)
    assert getattr(mon, "returned", False), "close() killed its own thread"
else:
    QtCore.QThread.msleep(200)
    mon.close()
    assert not sip.ispyowned(mon), "detached monitor still Python-owned"
    assert mon in mod._DETACHED
    sip.delete(owner)  # as USBManager.close() does
    del mon
    gc.collect()
sum(range(10**6))
sys.stdout.write("alive\\n")
sys.stdout.flush()
"""


@pytest.mark.parametrize("mode", ["stuck", "self"])
def test_close_never_wedges_the_process(mode: str) -> None:
    env = {**os.environ, "QT_QPA_PLATFORM": "offscreen"}
    try:
        res = subprocess.run(  # nosec B603
            [sys.executable, "-I", "-c", _CHILD, str(_SRC), mode],
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"{mode}: close() wedged the process (QThread.terminate)")
    assert res.stdout == "alive\n", res.stderr
    assert res.returncode == 0, res.stderr
    assert "Destroyed while thread" not in res.stderr
