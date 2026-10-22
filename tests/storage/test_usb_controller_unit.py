"""USBManager.close must not let the queued `finished` restart the monitor."""

import importlib.util
import pathlib
import sys
import types
from unittest.mock import MagicMock

import pytest
from PyQt6 import QtCore

_STORAGE = pathlib.Path(__file__).resolve().parents[2] / "BlocksScreen/devices/storage"
_PKG = "_usb_controller_under_test"


class _FakeUdisks(QtCore.QObject):
    """UDisksDBusAsync signal surface, no D-Bus or thread."""

    Priority = QtCore.QThread.Priority
    hardware_detected = QtCore.pyqtSignal(str)
    hardware_removed = QtCore.pyqtSignal(str)
    device_added = QtCore.pyqtSignal(str, dict)
    device_removed = QtCore.pyqtSignal(str, str)
    device_mounted = QtCore.pyqtSignal(str, str)
    device_unmounted = QtCore.pyqtSignal(str)
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None, gcodes_dir=None):
        super().__init__(parent)
        self.active = False
        self.starts = 0

    def start(self, _priority=None):
        self.starts += 1
        self.active = True

    def close(self):
        self.active = False


@pytest.fixture
def usb_controller(monkeypatch):
    """Load usb_controller by path with udisks2 and BannerPopup stubbed."""
    pkg = types.ModuleType(_PKG)
    pkg.__path__ = [str(_STORAGE)]
    monkeypatch.setitem(sys.modules, _PKG, pkg)
    monkeypatch.setitem(
        sys.modules,
        f"{_PKG}.udisks2",
        types.SimpleNamespace(UDisksDBusAsync=_FakeUdisks),
    )
    monkeypatch.setitem(
        sys.modules,
        "lib.panels.widgets.Common.bannerPopup",
        types.SimpleNamespace(BannerPopup=MagicMock),
    )
    spec = importlib.util.spec_from_file_location(
        f"{_PKG}.usb_controller", _STORAGE / "usb_controller.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_finished_after_close_does_not_restart(qapp, usb_controller):
    parent = QtCore.QObject()
    mgr = usb_controller.USBManager(parent, gcodes_dir=None)
    assert mgr.udisks.starts == 1
    mgr.close()
    mgr.udisks.finished.emit()
    assert mgr.udisks.starts == 1


def test_finished_without_close_restarts(qapp, usb_controller):
    parent = QtCore.QObject()
    mgr = usb_controller.USBManager(parent, gcodes_dir=None)
    mgr.udisks.close()
    mgr.udisks.finished.emit()
    assert mgr.udisks.starts == 2


def test_pending_full_restart_dropped_on_close(qapp, usb_controller):
    parent = QtCore.QObject()
    mgr = usb_controller.USBManager(parent, gcodes_dir=None)
    mgr.restart()
    assert mgr.need_restart
    mgr.close()
    mgr.udisks.finished.emit()
    assert mgr.udisks.starts == 1
