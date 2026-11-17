"""Header layout stays live while the tab bar is locked for a print."""

from unittest.mock import MagicMock

from PyQt6 import QtWidgets

from BlocksScreen.lib.panels.mainWindow import MainWindow


class _HeaderHost:
    """Borrows only the real header build and print-lock methods from MainWindow."""

    _setup_header = MainWindow._setup_header
    _make_temp_display = MainWindow._make_temp_display
    _make_header_icon = MainWindow._make_header_icon
    disable_tab_bar = MainWindow.disable_tab_bar
    enable_tab_bar = MainWindow.enable_tab_bar
    on_temp_sensor_update = MainWindow.on_temp_sensor_update

    def __init__(self) -> None:
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.resize(800, 60)
        self.main_content_widget = MagicMock()
        self.controlTab = self.utilitiesTab = None
        self._setup_header()
        self.chamber_temp_display.hide()


def test_chamber_shown_mid_print_is_laid_out(qtbot) -> None:
    """BlocksScreen restarted mid-print: chamber appears after the lock, not at 0,0."""
    host = _HeaderHost()
    qtbot.addWidget(host.main_widget)
    host.main_widget.show()
    QtWidgets.QApplication.processEvents()

    host.disable_tab_bar()
    host.on_temp_sensor_update("Chamber", "temperature", 27.0)
    QtWidgets.QApplication.processEvents()

    bed_x = host.bed_temp_display.geometry().x()
    assert host.chamber_temp_display.geometry().x() > bed_x
    assert host.wifi_button.geometry().x() > host.chamber_temp_display.geometry().x()
