"""Unit test for MainWindow._on_klippy_state auto-restart guard"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from BlocksScreen.lib.panels.mainWindow import MainWindow


def _make_fake_window(*, manual_restart_pending: bool) -> SimpleNamespace:
    return SimpleNamespace(
        _klippy_ready=False,
        _update_in_progress=False,
        _klipper_auto_restart_pending=False,
        _post_update_reconnect=False,
        _klipper_restart_timeout=MagicMock(),
        updater_worker=MagicMock(),
        conn_window=SimpleNamespace(manual_restart_pending=manual_restart_pending),
        loadwidget=MagicMock(),
        loadscreen=MagicMock(),
        ws=MagicMock(),
    )


class TestKlippyDisconnectedAutoRestartGuard:
    def test_auto_restarts_when_no_manual_restart_pending(self) -> None:
        fake_window = _make_fake_window(manual_restart_pending=False)

        MainWindow._on_klippy_state(fake_window, "disconnected")

        fake_window.ws.api.restart_service.assert_called_once_with("klipper")
        fake_window.loadscreen.show.assert_called_once()
        assert fake_window._klipper_auto_restart_pending is True

    def test_skips_auto_restart_when_manual_restart_pending(self) -> None:
        fake_window = _make_fake_window(manual_restart_pending=True)

        MainWindow._on_klippy_state(fake_window, "disconnected")

        fake_window.ws.api.restart_service.assert_not_called()
        fake_window.loadscreen.show.assert_not_called()
        assert fake_window._klipper_auto_restart_pending is False
