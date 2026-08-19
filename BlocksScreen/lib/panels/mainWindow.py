import logging
import os
import re
import typing
from collections import deque

import events
from configfile import BlocksScreenConfig, get_configparser
from devices.amu import AMUManager
from devices.storage import USBManager
from lib.files import Files
from lib.klipper_message_filter import (  # noqa: F405
    MessageSource,
    Severity,
    match_message,
)
from lib.machine import MachineControl
from lib.moonrakerComm import MoonWebSocket
from lib.network import WifiIconKey
from lib.panels.controlTab import ControlTab
from lib.panels.filamentTab import FilamentTab
from lib.panels.networkWindow import NetworkControlWindow, PixmapCache
from lib.panels.printTab import PrintTab
from lib.panels.utilitiesTab import UtilitiesTab
from lib.panels.widgets.common.basePopup import BasePopup
from lib.panels.widgets.MainWindow.cancelPage import CancelPage
from lib.panels.widgets.MainWindow.connectionPage import ConnectionPage
from lib.panels.widgets.common.loadWidget import LoadingOverlayWidget
from lib.panels.widgets.MainWindow.notificationPage import NotificationPage
from lib.panels.widgets.MainWindow.updatePage import UpdatePage
from lib.printer import Printer
from lib.ui.resources.background_resources_rc import *
from lib.ui.resources.font_rc import *
from lib.ui.resources.graphic_resources_rc import *
from lib.ui.resources.icon_resources_rc import *
from lib.ui.resources.main_menu_resources_rc import *
from lib.ui.resources.system_resources_rc import *
from lib.ui.resources.top_bar_resources_rc import *
from lib.updater_worker import UpdaterWorker
from lib.utils.blocks_tabwidget import NotificationQTabWidget
from lib.utils.display_button import DisplayButton
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets
from screensaver import ScreenSaver

_logger = logging.getLogger(__name__)

_MACRO_ERROR_RE = re.compile(
    r"Error evaluating 'gcode_macro ([^:]+):gcode'.*CommandError", re.IGNORECASE
)


def api_handler(func):
    """Decorator for methods that handle api responses"""

    def wrapper(*args, **kwargs):
        """Decorator for api_handler"""
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            _logger.error("Caught Exception in %s : %s ", func.__name__, e)
            raise

    return wrapper


class HeaderWifiIconProvider:
    """Resolves WifiIconKey integer values to cached QPixmaps for the header bar."""

    _WIFI_PATHS: dict[tuple[int, bool], str] = {
        (
            b,
            p,
        ): f":/network/media/btn_icons/network/{b}bar_wifi{'_protected' if p else ''}.svg"
        for b in range(5)
        for p in (False, True)
    }
    _ETHERNET_PATH = ":/network/media/btn_icons/network/ethernet_connected.svg"
    _HOTSPOT_PATH = ":/network/media/btn_icons/hotspot.svg"

    @classmethod
    def get_pixmap(cls, icon_key: int) -> QtGui.QPixmap:
        """Resolve an icon key to a QPixmap (cached via PixmapCache)."""
        key = WifiIconKey(icon_key)
        if key is WifiIconKey.ETHERNET:
            return PixmapCache.get(cls._ETHERNET_PATH)
        if key is WifiIconKey.HOTSPOT:
            return PixmapCache.get(cls._HOTSPOT_PATH)
        path = cls._WIFI_PATHS.get(
            (key.bars, key.is_protected), cls._WIFI_PATHS[(0, False)]
        )
        return PixmapCache.get(path)


class MainWindow(QtWidgets.QMainWindow):
    """GUI MainWindow, handles most of the app logic"""

    bo_ws_startup = QtCore.pyqtSignal(name="bo_start_websocket_connection")
    printer_state_signal = QtCore.pyqtSignal(str, name="printer_state")
    query_object_list = QtCore.pyqtSignal(list, name="query_object_list")
    printer_object_report_signal = QtCore.pyqtSignal(
        list, name="handle_report_received"
    )
    gcode_response = QtCore.pyqtSignal(list, name="gcode_response")
    handle_error_response = QtCore.pyqtSignal(list, name="handle_error_response")
    call_network_panel = QtCore.pyqtSignal(name="call-network-panel")
    call_notification_panel = QtCore.pyqtSignal(name="call-notification-panel")
    call_update_panel = QtCore.pyqtSignal(name="call-update-panel")
    on_update_message: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="on-update-message"
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )
    show_notifications: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, int, bool, name="show-notifications"
    )
    in_case_error = QtCore.pyqtSignal(name="in-case-error")

    call_load_panel = QtCore.pyqtSignal(bool, str, bool, name="call-load-panel")

    def __init__(self):
        """Set up UI, instantiate subsystems, and wire all inter-component signals."""
        super(MainWindow, self).__init__()
        self.config: BlocksScreenConfig = get_configparser()
        self._setup_ui()
        self.screensaver = ScreenSaver(self)
        self._popup_toggle: bool = False
        self._update_in_progress: bool = False
        self._post_update_reconnect: bool = False
        self._reconnect_retries: int = 0
        self._reconnect_timer = QtCore.QTimer(self)
        self._reconnect_timer.setSingleShot(False)
        self._reconnect_timer.setInterval(15_000)
        self._reconnect_timer.timeout.connect(self._on_reconnect_timer)
        self._klippy_ready: bool = False
        self._klipper_auto_restart_pending: bool = False
        self._klipper_restart_timeout = QtCore.QTimer(self)
        self._klipper_restart_timeout.setSingleShot(True)
        self._klipper_restart_timeout.setInterval(30_000)
        self._klipper_restart_timeout.timeout.connect(self._on_klipper_restart_timeout)
        self.main_content_widget.setCurrentIndex(0)

        usb_config = self.config.get_section("usb_manager", fallback=None)
        gdir = None
        if usb_config:
            gdir = usb_config.get("gcodes_dir", default=None)
        self.usb_manager: USBManager = USBManager(parent=self, gcodes_dir=gdir)
        self.ws = MoonWebSocket(self)
        self.amu_manager: AMUManager = AMUManager(ws=self.ws, parent=self)
        self.notiPage = NotificationPage(self)
        self.mc = MachineControl(self)
        self.file_data = Files(self, self.ws)
        self.index_stack = deque(maxlen=4)
        self.printer = Printer(self, self.ws)
        bs_config = self.config.get_section("blockscreen", fallback=None)
        if bs_config:
            self.printer.force_true_zero_offset = bs_config.getboolean(
                "true_zero_probe", default=False
            )
        self.conn_window = ConnectionPage(self, self.ws)
        self.update_page = UpdatePage()
        self.printer.print_stats_update[str, str].connect(
            self.update_page.set_printing_state
        )
        self.printer.extruder_update.connect(self.update_page.set_heater_target)
        self.printer.heater_bed_update.connect(self.update_page.set_heater_target)
        self.updater_worker = UpdaterWorker()
        self._bless_armed = False
        self.update_page.hide()
        self.conn_window.call_cancel_panel.connect(self.handle_cancel_print)
        self.installEventFilter(self.conn_window)
        self.printPanel = PrintTab(self.printTab, self.file_data, self.ws, self.printer)
        if not os.environ.get("BLOCKSCREEN_DEV"):
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.BlankCursor)
        self.filamentPanel = FilamentTab(
            self.filamentTab, self.printer, self.ws, self.config, self.amu_manager
        )
        self.controlPanel = ControlTab(self.controlTab, self.ws, self.printer)
        self.utilitiesPanel = UtilitiesTab(self.utilitiesTab, self.ws, self.printer)

        self.networkPanel = NetworkControlWindow(self)
        self.bo_ws_startup.connect(slot=self.bo_start_websocket_connection)
        self.ws.connecting_signal.connect(self.conn_window.on_websocket_connecting)
        self.ws.connected_signal.connect(
            self.conn_window.on_websocket_connection_achieved
        )
        self.ws.connected_signal.connect(self._arm_health_bless)
        self.ws.connection_lost.connect(self.conn_window.on_websocket_connection_lost)
        self.ws.klippy_state_signal.connect(self._on_klippy_state)
        self.ws.klippy_state_signal.connect(self.conn_window.on_klippy_state)
        self.printer.webhooks_update.connect(self.conn_window.webhook_update)
        self.printPanel.request_back.connect(slot=self.global_back)
        self.printPanel.on_cancel_print.connect(slot=self.on_cancel_print)
        self.in_case_error.connect(self.printPanel.in_case_error)

        self.show_notifications.connect(self.notiPage.new_notication)

        self.printPanel.request_change_page.connect(slot=self.global_change_page)
        self.filamentPanel.request_back.connect(slot=self.global_back)
        self.filamentPanel.request_change_page.connect(slot=self.global_change_page)
        self.controlPanel.request_back_button.connect(slot=self.global_back)
        self.controlPanel.request_change_page.connect(slot=self.global_change_page)
        self.utilitiesPanel.request_back.connect(slot=self.global_back)
        self.utilitiesPanel.request_change_page.connect(slot=self.global_change_page)
        self.utilitiesPanel.update_available.connect(self.on_update_available)
        self.notification_btn.clicked.connect(self.notiPage.show_notification_panel)
        self.extruder_temp_display.clicked.connect(
            lambda: self.global_change_page(
                self.main_content_widget.indexOf(self.controlTab),
                self.controlPanel.indexOf(self.controlPanel.temperature_page),
            )
        )
        self.bed_temp_display.clicked.connect(
            lambda: self.global_change_page(
                self.main_content_widget.indexOf(self.controlTab),
                self.controlPanel.indexOf(self.controlPanel.temperature_page),
            )
        )
        self.filament_type_icon.clicked.connect(
            lambda: self.global_change_page(
                self.main_content_widget.indexOf(self.filamentTab),
                2,
            )
        )
        self.filament_type_icon.setText("PLA")
        self.filament_type_icon.update()
        self.nozzle_size_icon.setText("0.4mm")
        self.nozzle_size_icon.update()
        self.conn_window.retry_connection_clicked.connect(slot=self.ws.retry_wb_conn)
        self.conn_window.firmware_restart_clicked.connect(
            slot=self.mc.restart_klipper_mcu_service
        )
        self.conn_window.firmware_restart_clicked.connect(
            slot=self.ws.api.firmware_restart
        )
        self.conn_window.restart_klipper_clicked.connect(
            slot=self.mc.restart_klipper_service
        )
        self.conn_window.reboot_clicked.connect(slot=self.mc.machine_restart)

        self.printer_object_report_signal.connect(
            self.printer.on_object_report_received
        )
        self.gcode_response.connect(self.printer.gcode_response)
        self.query_object_list.connect(self.printer.on_object_list)
        self.query_object_list.connect(self.utilitiesPanel.on_object_list)
        self.printer.extruder_update.connect(self.on_extruder_update)
        self.printer.heater_bed_update.connect(self.on_heater_bed_update)
        self.printer.sensor_update.connect(self.on_temp_sensor_update)
        self.printer.object_updated.connect(self.amu_manager.on_object_updated)
        self.amu_manager.run_gcode_signal.connect(self.ws.api.run_gcode)
        self.run_gcode_signal.connect(self.ws.api.run_gcode)

        self.main_content_widget.currentChanged.connect(slot=self.reset_tab_indexes)
        self.call_network_panel.connect(self.networkPanel.show_network_panel)
        self.call_notification_panel.connect(self.notiPage.show_notification_panel)
        self.networkPanel.update_wifi_icon.connect(self.change_wifi_icon)
        self.conn_window.wifi_button_clicked.connect(self.call_network_panel.emit)
        self.conn_window.notification_button_clicked.connect(
            self.call_notification_panel.emit
        )
        self.wifi_button.clicked.connect(self.call_network_panel.emit)
        self.handle_error_response.connect(
            self.controlPanel.probe_helper_page.handle_error_response
        )
        self.controlPanel.probe_helper_page.show_notifications.connect(
            self._on_probe_notification
        )
        self.controlPanel.disable_popups.connect(self.popup_toggle)
        self.updater_worker.status_ready.connect(self.update_page.handle_status_ready)
        self.updater_worker.busy_changed.connect(self.update_page.handle_busy_changed)
        self.updater_worker.daemon_unavailable.connect(self.on_updater_unavailable)
        self.updater_worker.daemon_unavailable.connect(
            self.update_page.handle_daemon_unavailable
        )
        self.controlPanel.lock_ui.connect(self.set_ui_lock)
        self.updater_worker.request_reconnect.connect(self._on_post_update_reconnect)
        self.updater_worker.proxy_connected.connect(
            self.update_page._request_status_debounced
        )
        self.ws.connected_signal.connect(self._on_moonraker_connected_post_update)
        self.update_page.request_update.connect(self.updater_worker.trigger_update)
        self.update_page.request_status.connect(self.updater_worker.trigger_status)
        self.update_page.request_cancel.connect(self.updater_worker.trigger_cancel)
        self.update_page.update_available.connect(self.on_update_available)
        self.update_page.call_load_panel.connect(self.show_loadscreen)
        self.update_page.disable_popups.connect(self.popup_toggle)
        self.update_page.update_back_btn.clicked.connect(self.update_page.hide)
        self.updater_worker.step_complete.connect(self.update_page.handle_step_complete)
        self.updater_worker.error_occurred.connect(
            self.update_page.handle_error_occurred
        )
        self.updater_worker.update_rejected.connect(
            self.update_page.handle_update_rejected
        )
        self.updater_worker.rollback_done.connect(self.update_page.handle_rollback_done)
        self.updater_worker.recover_done.connect(self.update_page.handle_recover_done)
        self.ws.klippy_state_signal.connect(self._on_klippy_state)
        self.utilitiesPanel.show_update_page.connect(self.show_update_page)
        self.conn_window.update_button_clicked.connect(self.show_update_page)
        self.extruder_temp_display.display_format = "upper_downer"
        self.bed_temp_display.display_format = "upper_downer"

        self.controlPanel.call_load_panel.connect(self.show_loadscreen)
        self.filamentPanel.call_load_panel.connect(self.show_loadscreen)
        self.printPanel.call_load_panel.connect(self.show_loadscreen)
        self.utilitiesPanel.call_load_panel.connect(self.show_loadscreen)
        self.conn_window.call_load_panel.connect(self.show_loadscreen)

        self.filamentPanel.request_change_tab.connect(self.global_change_tab)
        self.printPanel.request_change_tab.connect(self.global_change_tab)

        self.loadscreen = BasePopup(self, floating=False, dialog=False)
        self.loadwidget = LoadingOverlayWidget(
            self, LoadingOverlayWidget.AnimationGIF.DEFAULT
        )
        self.loadscreen.add_widget(self.loadwidget)
        self.controlPanel.toggle_conn_page.connect(self.conn_window.set_toggle)
        self.cancelpage = CancelPage(self, ws=self.ws)
        self.cancelpage.request_file_info.connect(self.file_data.on_request_fileinfo)
        self.cancelpage.run_gcode.connect(self.ws.api.run_gcode)
        self.printer.print_stats_update[str, str].connect(
            self.cancelpage.on_print_stats_update
        )
        self.printer.print_stats_update[str, dict].connect(
            self.cancelpage.on_print_stats_update
        )
        self.printer.print_stats_update[str, float].connect(
            self.cancelpage.on_print_stats_update
        )
        self.file_data.fileinfo.connect(self.cancelpage._show_screen_thumbnail)
        # Reprint routes through on_print_start for the same full reset as a fresh print.
        self.cancelpage.reprint_start.connect(
            self.printPanel.jobStatusPage_widget.on_print_start
        )
        self.printPanel.call_cancel_panel.connect(self.handle_cancel_print)
        self.printer.display_update.connect(self._handle_display_status)

        # Source of truth for job activity; keeps print tab off the main page mid-job.
        self._print_state = "standby"
        self.printer.print_stats_update[str, str].connect(self._track_print_state)

        self.print_status = "idle"
        self.chamber_temp_display.hide()

        if self.config.has_section("server"):
            self.bo_ws_startup.emit()
        self.reset_tab_indexes()
        self.conn_window.show()

    @QtCore.pyqtSlot(str, str, name="handleDisplayUpdate")
    @QtCore.pyqtSlot(str, float, name="handleDisplayUpdate")
    def _handle_display_status(self, name, value: str | float) -> None:
        if isinstance(value, str):
            if value == "" or value.isspace():
                return
            self.show_notifications.emit("M117", str(value), Severity.INFO.value, True)

    @QtCore.pyqtSlot(bool, name="show-cancel-page")
    def handle_cancel_print(self, show: bool = True):
        """Slot for displaying update Panel"""
        if not show:
            self.cancelpage.hide()
            return
        # Defer so a concurrent E-stop (klippy shutdown) is seen before we decide.
        QtCore.QTimer.singleShot(0, self._show_cancel_page_if_operational)

    def _show_cancel_page_if_operational(self) -> None:
        # E-stop/shutdown aborts the print with an error too; the connection page handles that, not the cancel page.
        if not self._klippy_ready:
            return
        self.cancelpage.setGeometry(0, 0, self.width(), self.height())
        self.cancelpage.raise_()
        self.cancelpage.updateGeometry()
        self.cancelpage.repaint()
        self.cancelpage.show()

    @QtCore.pyqtSlot(bool, str, bool, name="show-load-page")
    def show_loadscreen(
        self, show: bool = True, msg: str = "", force: bool = False
    ) -> None:
        """Show or hide the loading overlay, guarded by the calling panel's visibility."""
        _sender = self.sender()
        if not force:
            if _sender is self.update_page:
                self._update_in_progress = show
            if not show and self._post_update_reconnect:
                return
            elif not show and self._update_in_progress:
                return
            elif not show and self._klipper_auto_restart_pending:
                return

            if _sender == self.filamentPanel:
                if not self.filamentPanel.isVisible():
                    return
            if _sender == self.controlPanel:
                if not self.controlPanel.isVisible():
                    return
            if _sender == self.printPanel:
                if not self.printPanel.isVisible():
                    return
            if _sender == self.utilitiesPanel:
                if not self.utilitiesPanel.isVisible():
                    return

        self.loadwidget.set_status_message(msg)
        if show:
            self.loadscreen.show()
        else:
            self.loadscreen.hide()

    @QtCore.pyqtSlot(bool, name="show-update-page")
    def show_update_page(self, fullscreen: bool):
        """Slot for displaying update Panel"""
        if not fullscreen:
            self.update_page.setParent(self.main_content_widget)
            current_index = self.main_content_widget.currentIndex()
            tab_rect = self.main_content_widget.tabBar().tabRect(current_index)
            width = tab_rect.width()
            _parent_size = self.update_page.parent().size()
            self.update_page.setGeometry(
                width, 0, _parent_size.width() - width, _parent_size.height()
            )
        else:
            self.update_page.setParent(self)
            self.update_page.setGeometry(0, 0, self.width(), self.height())

        self.update_page.raise_()
        self.update_page.updateGeometry()
        self.update_page.repaint()
        self.update_page.show()

    @QtCore.pyqtSlot(str, name="on-klippy-state")
    def _on_klippy_state(self, state: str) -> None:
        self._klippy_ready = state == "ready"
        if state == "shutdown":
            if self._update_in_progress:
                _logger.warning("Klipper E-stop detected — cancelling active update")
                self.updater_worker.trigger_cancel()
        elif (
            state == "disconnected"
            and not self._klipper_auto_restart_pending
            and not self._update_in_progress
            and not self.conn_window.manual_restart_pending
        ):
            _logger.info("Klipper disconnected — auto-restarting service")
            self._klipper_auto_restart_pending = True
            self.loadwidget.set_status_message("Restarting Klipper...")
            self.loadscreen.show()
            self._klipper_restart_timeout.start()
            self.ws.api.restart_service("klipper")
        elif state == "ready" and self._klipper_auto_restart_pending:
            _logger.info("Klipper back online after auto-restart")
            self._klipper_auto_restart_pending = False
            self._klipper_restart_timeout.stop()
            if not self._post_update_reconnect:
                self.loadscreen.hide()

    @QtCore.pyqtSlot(name="arm-health-bless")
    def _arm_health_bless(self) -> None:
        """On first moonraker connect, arm a one-shot to bless this build as healthy."""
        if self._bless_armed:
            return
        self._bless_armed = True
        QtCore.QTimer.singleShot(60_000, self._emit_health_bless)

    @QtCore.pyqtSlot(name="emit-health-bless")
    def _emit_health_bless(self) -> None:
        """Bless the running build if moonraker is still reachable after the debounce."""
        if not getattr(self.ws, "connected", False):
            _logger.info("health bless skipped: moonraker not connected")
            return
        _logger.info("health bless: marking current build as known-good")
        self.updater_worker.trigger_bless()

    @QtCore.pyqtSlot(name="on-klipper-restart-timeout")
    def _on_klipper_restart_timeout(self) -> None:
        _logger.warning(
            "Klipper auto-restart timed out after 30 s — showing connection page"
        )
        self._klipper_auto_restart_pending = False
        self.loadscreen.hide()

    @QtCore.pyqtSlot(name="on-cancel-print")
    def on_cancel_print(self):
        """Slot for cancel print signal"""
        self.enable_tab_bar()
        try:
            self.extruder_temp_display.clicked.disconnect()
            self.bed_temp_display.clicked.disconnect()
        except TypeError:
            pass
        self.extruder_temp_display.clicked.connect(
            lambda: self.global_change_page(
                self.main_content_widget.indexOf(self.controlTab),
                self.controlPanel.indexOf(self.controlPanel.temperature_page),
            )
        )
        self.bed_temp_display.clicked.connect(
            lambda: self.global_change_page(
                self.main_content_widget.indexOf(self.controlTab),
                self.controlPanel.indexOf(self.controlPanel.temperature_page),
            )
        )

    @QtCore.pyqtSlot(name="on-updater-unavailable")
    def on_updater_unavailable(self) -> None:
        """Handle updater daemon going offline: dismiss loading overlay and hide update page."""
        _logger.warning(
            "updater daemon unavailable: clearing flags (update_in_progress=%s, post_update_reconnect=%s)",
            self._update_in_progress,
            self._post_update_reconnect,
        )
        self._post_update_reconnect = False
        self._update_in_progress = False
        self._reconnect_timer.stop()
        # update_page.handle_daemon_unavailable (connected to the same signal)
        # resets the page; routing through handle_busy_changed here would issue
        # a status request that fails and re-emits daemon_unavailable — a storm.
        self.show_loadscreen(False, "")

    @QtCore.pyqtSlot(name="on-post-update-reconnect")
    def _on_post_update_reconnect(self) -> None:
        """Called when an update finishes: hold the loading screen and retry Moonraker until it's up."""
        _logger.debug(
            "_on_post_update_reconnect: ws.connected=%s update_in_progress=%s",
            self.ws.connected,
            self._update_in_progress,
        )
        if self.ws.connected:
            # Moonraker never restarted — overlay will be dismissed by handle_status_ready
            # once the post-update status refresh completes (via _post_update_status_pending).
            return
        self._post_update_reconnect = True
        self._reconnect_retries = 0
        self.loadwidget.set_status_message("Reconnecting...")
        self.ws.retry_wb_conn()
        self._reconnect_timer.start()

    _MAX_RECONNECT_RETRIES: int = 10  # 10 × 15 s = 2.5 min before giving up

    @QtCore.pyqtSlot(name="on-reconnect-timer")
    def _on_reconnect_timer(self) -> None:
        if not self._post_update_reconnect:
            self._reconnect_timer.stop()
            return
        if self.ws.connected:
            _logger.debug("post-update: Moonraker reconnected, hiding loadscreen")
            self._post_update_reconnect = False
            self._update_in_progress = False
            self._reconnect_retries = 0
            self._reconnect_timer.stop()
            self.loadscreen.hide()
            return
        self._reconnect_retries += 1
        if self._reconnect_retries >= self._MAX_RECONNECT_RETRIES:
            _logger.warning(
                "post-update reconnect gave up after %d retries",
                self._reconnect_retries,
            )
            self._post_update_reconnect = False
            self._update_in_progress = False
            self._reconnect_timer.stop()
            self.loadscreen.hide()
            return
        _logger.info(
            "post-update reconnect retry %d/%d",
            self._reconnect_retries,
            self._MAX_RECONNECT_RETRIES,
        )
        self.ws.retry_wb_conn()

    @QtCore.pyqtSlot(name="on-moonraker-connected-post-update")
    def _on_moonraker_connected_post_update(self) -> None:
        if self._post_update_reconnect:
            _logger.info("Moonraker reconnected after update, hiding loading screen")
            self._post_update_reconnect = False
            self._update_in_progress = False
            self._reconnect_retries = 0
            self._reconnect_timer.stop()
            self.loadscreen.hide()

    @QtCore.pyqtSlot(bool, name="update-available")
    def on_update_available(self, state: bool = False):
        """Signal render for red dot on utilities tab icon and Update button"""
        self.main_content_widget.setNotification(3, state)
        self.utilitiesPanel.panel.update_btn.setShowNotification(state)
        self.repaint()

    def enable_tab_bar(self) -> bool:
        """Enables the tab bar

            `This method is only used when a print job is ongoing, so the printTab is never disabled`

        Returns:
            bool: True if the TabBar was disabled
        """

        self.main_content_widget.setTabEnabled(
            self.main_content_widget.indexOf(self.controlTab), True
        )
        self.main_content_widget.setTabEnabled(
            self.main_content_widget.indexOf(self.utilitiesTab), True
        )
        self.header_main_layout.setEnabled(True)
        return all(
            [
                not self.main_content_widget.isTabEnabled(
                    self.main_content_widget.indexOf(self.controlTab)
                ),
                not self.main_content_widget.isTabEnabled(
                    self.main_content_widget.indexOf(self.utilitiesTab)
                ),
                not self.header_main_layout.isEnabled(),
            ]
        )

    def disable_tab_bar(self) -> bool:
        """Disables the tab bar so to not change the tab.

        `This method is only used when a print job is ongoing, so the printTab is never disabled`


        ---

        Returns:
            boolean: True if the TabBar was disabled
        """
        self.main_content_widget.setTabEnabled(
            self.main_content_widget.indexOf(self.controlTab), False
        )
        self.main_content_widget.setTabEnabled(
            self.main_content_widget.indexOf(self.utilitiesTab), False
        )
        self.header_main_layout.setEnabled(False)
        return all(
            [
                not self.main_content_widget.isTabEnabled(
                    self.main_content_widget.indexOf(self.controlTab)
                ),
                not self.main_content_widget.isTabEnabled(
                    self.main_content_widget.indexOf(self.utilitiesTab)
                ),
                not self.header_main_layout.isEnabled(),
            ]
        )

    @QtCore.pyqtSlot(bool, name="toggle-popups")
    def popup_toggle(self, toggle: bool) -> None:
        """Toggles app popups"""
        self._popup_toggle = toggle

    @QtCore.pyqtSlot(bool, name="set-ui-lock")
    def set_ui_lock(self, locked: bool) -> None:
        """Lock or unlock navigation during calibration.

        Disables all tabs except controlTab (where calibration lives) and
        the header, so the user cannot navigate away mid-calibration.
        """
        for tab in (
            self.printTab,
            self.filamentTab,
            self.utilitiesTab,
        ):
            self.main_content_widget.setTabEnabled(
                self.main_content_widget.indexOf(tab), not locked
            )
        self.header_main_layout.setEnabled(not locked)

    @QtCore.pyqtSlot(str, str, name="track_print_state")
    def _track_print_state(self, field: str, value: str) -> None:
        """Track ``print_stats.state`` as the source of truth for job activity."""
        if field == "state":
            self._print_state = value

    def _is_job_active(self) -> bool:
        """True while a job occupies the printer; paused included so runout pauses hold the page."""
        return self._print_state in ("printing", "paused")

    def _print_tab_index(self) -> int:
        """Tab index of the print tab in the main content widget."""
        return self.main_content_widget.indexOf(self.printTab)

    def _job_status_index(self) -> int:
        """Panel index of the job-status page inside the print tab."""
        return self.printPanel.indexOf(self.printPanel.jobStatusPage_widget)

    def _main_print_index(self) -> int:
        """Panel index of the main print page inside the print tab."""
        return self.printPanel.indexOf(self.printPanel.print_page)

    def _guard_print_panel(self, tab_index: int, panel_index: int) -> int:
        """Redirect the main print page to job status while a job is active."""
        if (
            tab_index == self._print_tab_index()
            and panel_index == self._main_print_index()
            and self._is_job_active()
        ):
            return self._job_status_index()
        return panel_index

    def reset_tab_indexes(self):
        """
        Used to grantee all tabs reset to their
        first page once the user leaves the tab
        """
        self.filamentPanel.setCurrentIndex(0)

        if self._is_job_active():
            self.printPanel.setCurrentIndex(self._job_status_index())
            return
        self.printPanel.setCurrentIndex(0)
        self.controlPanel.setCurrentIndex(0)
        self.utilitiesPanel.setCurrentIndex(0)
        self.networkPanel.setCurrentIndex(0)
        self.update_page.hide()

    def current_panel_index(self) -> int:
        """Helper function to get the index of the current page in the current tab

        Returns:
            int: The index os the page
        """
        match self.main_content_widget.currentIndex():
            case 0:
                return self.printPanel.currentIndex()
            case 1:
                return self.filamentPanel.currentIndex()
            case 2:
                return self.controlPanel.currentIndex()
            case 3:
                return self.utilitiesPanel.currentIndex()
        return -1

    def set_current_panel_index(self, panel_index: int) -> None:
        """Helper function to set the index of the current page in the current tab

        Args:
            panel_index (int): The index of the page we want to go to
        """
        match self.main_content_widget.currentIndex():
            case 0:
                self.printPanel.setCurrentIndex(panel_index)
            case 1:
                self.filamentPanel.setCurrentIndex(panel_index)
            case 2:
                self.controlPanel.setCurrentIndex(panel_index)
            case 3:
                self.utilitiesPanel.setCurrentIndex(panel_index)

    @QtCore.pyqtSlot(int)
    def change_wifi_icon(self, icon_key: int) -> None:
        """Change the icon of the netowrk by a key enum match

        Args:
            icon_key (int): WifiIconKey mapping for the current network state
        """
        self.wifi_button.setPixmap(HeaderWifiIconProvider.get_pixmap(icon_key))

    @QtCore.pyqtSlot(int, int, name="request-change-page")
    def global_change_page(self, tab_index: int, panel_index: int) -> None:
        """Changes panels pages globally

        Args:
            tab_index (int): The tab index of the panel
            panel_index (int): The index of the panel page
        """
        if not isinstance(tab_index, int):
            _logger.debug(
                "Tab index argument expected type int, got %s", str(type(tab_index))
            )
        if not isinstance(panel_index, int):
            _logger.debug(
                "Panel page index expected type int, %s", str(type(panel_index))
            )

        self.show_loadscreen(False)
        panel_index = self._guard_print_panel(tab_index, panel_index)
        current_page = [
            self.main_content_widget.currentIndex(),
            self.current_panel_index(),
        ]
        requested_page = [tab_index, panel_index]
        if requested_page == current_page:
            _logger.debug("User is already on the requested page")
            return
        self.index_stack.append(current_page)
        self.main_content_widget.setCurrentIndex(tab_index)
        self.set_current_panel_index(panel_index)
        _logger.debug(
            f"Requested page change -> Tab index : {requested_page[0]} | panel index : {requested_page[1]}",
        )

    def global_change_tab(self, tab_index: int) -> None:
        """Changes the current tab while keeping the current panel page index if possible

        Args:
            tab_index (int): The index of the tab to change to
        """
        if not isinstance(tab_index, int):
            _logger.debug(
                "Tab index argument expected type int, got %s", str(type(tab_index))
            )
            return
        self.main_content_widget.setCurrentIndex(tab_index)
        _logger.debug(
            f"Requested tab change -> Tab index : {tab_index}",
        )

    @QtCore.pyqtSlot(name="request-back")
    def global_back(self) -> None:
        """Requests to go back a page globally"""
        if not bool(self.index_stack):
            _logger.debug("Index stack is empty, cannot go back any further")
            return
        _tab, _panel = self.index_stack[-1]
        _panel = self._guard_print_panel(_tab, _panel)
        self.main_content_widget.setCurrentIndex(_tab)
        self.set_current_panel_index(_panel)
        self.index_stack.pop()  # Remove the last position.
        _logger.debug("Successfully went back a page.")

    @QtCore.pyqtSlot(name="bo-start-websocket-connection")
    def bo_start_websocket_connection(self) -> None:
        """Starts the Websocket connection with moonraker"""
        self.ws.start()
        self.ws.try_connection()

    def messageReceivedEvent(self, event: events.WebSocketMessageReceived) -> None:
        """Helper method that handles dispatching websocket
        event messages to their respective handlers

        Args:
            event (events.WebSocketMessageReceivedEvent): The message event with all its contents

        Raises:
            Exception: When a klippy status change comes from the
            websocket, tries to send another event
            corresponding to the incoming status.
            If the QApplication instance is of type
            None raises an exception because the event
            cannot be sent.
        """
        _method = event.method
        _data = event.data
        _metadata = event.metadata
        if not _method:
            return
        if not _data:
            return
        api_reference = _method.split(".")
        if "klippy" in _method:
            api_reference = "notify_klippy"
        method_handle = f"_handle_{api_reference[0]}_message"
        if hasattr(self, method_handle):
            obj = getattr(self, method_handle)
            if callable(obj):
                obj(_method, _data, _metadata)

    @api_handler
    def _handle_server_message(self, method, data, metadata) -> None:
        """Route file-related WebSocket messages to the Files subsystem."""
        if "file" in method:
            file_data_event = events.ReceivedFileData(data, method, metadata)
            try:
                QtWidgets.QApplication.postEvent(self.file_data, file_data_event)
            except Exception as e:
                _logger.error(
                    (
                        "Error posting event for file related information",
                        "received from websocket | error message received: %s",
                    ),
                    str(e),
                )

    @api_handler
    def _handle_machine_message(self, method, data, metadata) -> None:
        """Route machine-state WebSocket messages to the update signal."""
        if "ok" in data:
            return
        if "update" in method:
            if ("status" or "refresh") in method:
                self.on_update_message.emit(dict(data))

    @api_handler
    def _handle_notify_update_response_message(self, method, data, metadata) -> None:
        """Handle update response messages"""
        self.on_update_message.emit(
            dict(dict(data.get("params", {})[0]))
        )  # Also necessary, notify klippy can also signal update complete

    @api_handler
    def _handle_notify_update_refreshed_message(self, method, data, metadata) -> None:
        """Handle update refreshed messages"""
        self.on_update_message.emit(dict(data.get("params", {})[0]))

    @api_handler
    def _handle_printer_message(self, method, data, metadata) -> None:
        """Handle Printer messages"""
        if "info" in method:
            # TODO: Handle info
            ...
        if "print" in method:
            if "start" in method and "ok" in data:
                self.printer_state_signal.emit("printing")
            elif "pause" in method and "ok" in data:
                self.printer_state_signal.emit("paused")
            elif "resume" in method and "ok" in data:
                self.printer_state_signal.emit("printing")
            elif "cancel" in method and "ok" in data:
                self.printer_state_signal.emit("canceled")
        if "objects" in method:
            if "list" in method:
                _object_list: list = data["objects"]
                self.query_object_list[list].emit(_object_list)
            if "subscribe" in method:
                _objects_response_list = [data["status"], data["eventtime"]]
                self.printer_object_report_signal[list].emit(_objects_response_list)
            if "query" in method:
                if isinstance(data["status"], dict):
                    _object_report_list = [data["status"], data["eventtime"]]
                    self.printer_object_report_signal[list].emit(_object_report_list)

    @api_handler
    def _handle_notify_klippy_message(self, method, data, metadata) -> None:
        """Handle websocket notifications for klippy events"""
        _split = method.split("_")
        if len(_split) > 2:
            status_type = _split[2]
            _state_upper = status_type[0].upper()
            _state_call = f"{_state_upper}{status_type[1:]}"
            _logger.debug(
                "Notify_klippy_ %s Received from object subscription.",
                str(_state_call),
            )
            if hasattr(events, f"Klippy{_state_call}"):
                _klippy_event_callback = getattr(
                    events,
                    f"Klippy{_state_call}",
                )
                if callable(_klippy_event_callback):
                    try:
                        _event = _klippy_event_callback(data="")
                        instance = QtWidgets.QApplication.instance()
                        if not isinstance(_event, QtCore.QEvent):
                            return
                        if instance:
                            _logger.info("Event %s sent", str(_klippy_event_callback))
                            instance.postEvent(self, _event)
                        else:
                            raise Exception("QApplication.instance is None type.")
                    except Exception as e:
                        _logger.debug(
                            "Unable to send internal klippy %s notification: %s",
                            str(_state_call),
                            str(e),
                        )
            if not self._popup_toggle and status_type in (
                "shutdown",
                "error",
                "disconnected",
            ):
                self._emit_filtered_notification(
                    MessageSource.KLIPPY_STATE,
                    status_type,
                    source_id="klippy_state",
                    fallback=False,
                    show_popup=True,
                )

    @api_handler
    def _handle_notify_filelist_changed_message(self, method, data, metadata) -> None:
        """Handle websocket file list messages"""
        self.file_data.handle_filelist_changed(data)

    @api_handler
    def _handle_notify_service_state_changed_message(
        self, method, data, metadata
    ) -> None:
        """Handle websocket service messages"""
        entry = data.get("params")
        if entry:
            if self._popup_toggle:
                return
            service_entry: dict = entry[0]
            service_name, service_info = service_entry.popitem()
            self.show_notifications.emit(
                "mainwindow",
                str(
                    f"{service_name} service changed state to \n{service_info.get('sub_state')}"
                ),
                1,
                False,
            )

    def _emit_filtered_notification(
        self,
        source: MessageSource,
        text: str,
        *,
        source_id: str = "mainwindow",
        fallback: bool,
        show_popup: bool,
    ) -> bool:
        rule = match_message(source, text)

        if rule is not None:
            if rule.severity == Severity.IGNORE:
                return True
            if rule.severity == Severity.ERROR:
                self.show_loadscreen(False, "", True)
                self.in_case_error.emit()

            self.show_notifications.emit(
                source_id, rule.full_display, rule.severity.value, show_popup
            )
            return True

        elif fallback:
            self.show_notifications.emit(
                source_id, text, Severity.ERROR.value, show_popup
            )
            self.show_loadscreen(False, "", True)
            self.in_case_error.emit()
            return True
        return False

    @QtCore.pyqtSlot(str, str, int, bool)
    def _on_probe_notification(
        self, _source: str, text: str, _severity: int, show_popup: bool
    ) -> None:
        if not self._emit_filtered_notification(
            MessageSource.GCODE_ERROR,
            text,
            source_id="probe_helper",
            fallback=False,
            show_popup=show_popup,
        ):
            self._emit_filtered_notification(
                MessageSource.MOONRAKER_ERROR,
                text,
                source_id="probe_helper",
                fallback=True,
                show_popup=show_popup,
            )

    @api_handler
    def _handle_notify_gcode_response_message(self, method, data, metadata) -> None:
        """Handle websocket gcode responses messages"""
        _gcode_response = data.get("params")
        self.gcode_response[list].emit(_gcode_response)
        if _gcode_response:
            if self._popup_toggle:
                return
            parts = str(_gcode_response[0]).split(" ", maxsplit=1)
            if len(parts) != 2:
                return
            _gcode_msg_type, _message = parts

            if _gcode_msg_type in ["SCREEN", "echo:"]:
                self.show_notifications.emit(
                    _gcode_msg_type, _message, Severity.INFO.value, True
                )
                return
            elif _gcode_msg_type == "LOAD":
                self.show_loadscreen(True, _message, False)
                return

            elif _gcode_msg_type == "!!":
                source = MessageSource.GCODE_ERROR
                m = _MACRO_ERROR_RE.search(_message)
                if m:
                    _message = f"macro failed: {m.group(1)}"

            else:
                return

            self._emit_filtered_notification(
                source,
                _message,
                fallback=True,
                show_popup=True,
            )

    @api_handler
    def _handle_error_message(self, method, data, metadata) -> None:
        """Handle error messages from Moonraker API."""
        self.handle_error_response[list].emit([data, metadata])
        if self._popup_toggle:
            return

        if not self._klippy_ready:
            return

        text = data.get("message", str(data)) if isinstance(data, dict) else str(data)
        lower_text = text.lower()

        if "metadata" in lower_text:
            self.file_data.handle_metadata_error(text)
            return

        if "file" in lower_text and "does not exist" in lower_text:
            return

        if "does not exist" in lower_text:
            self.printPanel.filesPage_widget.on_directory_error()

        if not self._emit_filtered_notification(
            MessageSource.MOONRAKER_ERROR, text, fallback=False, show_popup=True
        ):
            self._emit_filtered_notification(
                MessageSource.GCODE_ERROR, text, fallback=True, show_popup=True
            )
        _logger.error(text)

    @api_handler
    def _handle_notify_cpu_throttled_message(self, method, data, metadata) -> None:
        """Handle websocket cpu throttled messages"""
        if self._popup_toggle:
            return
        try:
            flags = {
                "Under-Voltage Detected": 1 << 0,
                "Frequency Capped": 1 << 1,
                "Currently Throttled": 1 << 2,
                "Temperature Limit Active": 1 << 3,
            }
            _bits = data.get("bits", None)
            if not _bits:
                self.show_notifications.emit(
                    "mainwindow", "Cpu throttled unknown reason", 2, True
                )
                return
            _active_flags = [name for name, mask in flags.items() if _bits & mask]
            for flag in _active_flags:
                self._emit_filtered_notification(
                    MessageSource.CPU_THROTTLE, flag, fallback=True, show_popup=True
                )
        except Exception:
            logging.debug("Error emitting notification for cpu throttled notification.")
            return

    @api_handler
    def _handle_notify_status_update_message(self, method, data, metadata) -> None:
        """Handle websocket printer objects status update messages"""
        _object_report = data["params"]
        self.printer_object_report_signal[list].emit(_object_report)

    @QtCore.pyqtSlot(str, str, float, name="on-extruder-update")
    def on_extruder_update(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        """Handles extruder printer object updates"""
        if extruder_name == "extruder":
            if field == "temperature":
                self.extruder_temp_display.setText(f"{new_value:.0f}")
            elif field == "target":
                self.extruder_temp_display.secondary_text = (
                    f"{round(int(new_value)):.0f}°C"
                )

    @QtCore.pyqtSlot(str, str, float, name="on-heater-bed-update")
    def on_heater_bed_update(self, name: str, field: str, new_value: float) -> None:
        """Handles heater_bed printer object updates"""
        if field == "temperature":
            self.bed_temp_display.setText(f"{new_value:.0f}")
        elif field == "target":
            self.bed_temp_display.secondary_text = f"{round(int(new_value)):.0f}°C"

    @QtCore.pyqtSlot(str, str, float, name="sensor_update")
    def on_temp_sensor_update(self, name: str, field: str, value: float) -> None:
        """Handles Chamber temperature if a sensor with that name exists"""
        if name == "Chamber":
            if self.chamber_temp_display.isHidden():
                self.chamber_temp_display.show()
            if field == "temperature":
                self.chamber_temp_display.setText(f"{round(int(value)):.0f}°C")
            elif field == "humidity":
                self.chamber_temp_display.setSecondaryText(f"{round(int(value)):.0f}%")

    @QtCore.pyqtSlot(str, name="set-header-filament-type")
    def set_header_filament_type(self, type: str):
        """Sets header filament text label"""
        self.filament_type_icon.setText(f"{type}")
        self.filament_type_icon.update()

    @QtCore.pyqtSlot(str, name="set-header-nozzle-diameter")
    def set_header_nozzle_diameter(self, diam: str):
        """Sets header nozzle diameter text label"""
        self.nozzle_size_icon.setText(f"{diam}mm")
        self.nozzle_size_icon.update()

    def closeEvent(self, a0: QtGui.QCloseEvent | None) -> None:
        """Handles GUI closing"""
        try:
            self.networkPanel.close()
            self.usb_manager.close()
            self.updater_worker.shutdown()
        except Exception as e:
            _logger.warning("Error shutting down: %s", e)
        self.ws.wb_disconnect()
        if a0 is None:
            return
        QtWidgets.QMainWindow.closeEvent(self, a0)
        super().closeEvent(a0)

    def event(self, event: QtCore.QEvent) -> bool:
        """Receives PyQt Events, reimplemented method from the QEvent class"""
        if event.type() == events.WebSocketMessageReceived.type():
            if isinstance(event, events.WebSocketMessageReceived):
                self.messageReceivedEvent(event)
                return True
            return False
        if event.type() == events.PrintStart.type():
            self.print_status = "printing"
            self.disable_tab_bar()
            try:
                self.extruder_temp_display.clicked.disconnect()
                self.bed_temp_display.clicked.disconnect()
            except TypeError:
                pass
            self.extruder_temp_display.clicked.connect(
                lambda: self.global_change_page(
                    self.main_content_widget.indexOf(self.printTab),
                    self.printPanel.indexOf(self.printPanel.tune_page),
                )
            )
            self.bed_temp_display.clicked.connect(
                lambda: self.global_change_page(
                    self.main_content_widget.indexOf(self.printTab),
                    self.printPanel.indexOf(self.printPanel.tune_page),
                )
            )
            return False

        if event.type() in (
            events.PrintError.type(),
            events.PrintComplete.type(),
            events.PrintCancelled.type(),
        ):
            self.print_status = "idle"
            if event.type() == events.PrintCancelled.type():
                self.handle_cancel_print()
            self.enable_tab_bar()
            try:
                self.extruder_temp_display.clicked.disconnect()
                self.bed_temp_display.clicked.disconnect()
            except TypeError:
                pass
            self.extruder_temp_display.clicked.connect(
                lambda: self.global_change_page(
                    self.main_content_widget.indexOf(self.controlTab),
                    self.controlPanel.indexOf(self.controlPanel.temperature_page),
                )
            )
            self.bed_temp_display.clicked.connect(
                lambda: self.global_change_page(
                    self.main_content_widget.indexOf(self.controlTab),
                    self.controlPanel.indexOf(self.controlPanel.temperature_page),
                )
            )
            return False
        return super().event(event)

    def sizeHint(self) -> QtCore.QSize:
        """Sets default size for the widget"""
        self.adjustSize()
        return QtCore.QSize(800, 480)

    def _setup_ui(self) -> None:
        """Build the main window chrome: header bar, tab widget, and tab pages."""
        self.setObjectName("MainWindow")
        self.resize(800, 480)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.setMaximumSize(QtCore.QSize(1024, 600))
        self.setSizeIncrement(QtCore.QSize(1, 1))
        self.setBaseSize(QtCore.QSize(800, 480))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        self.setPalette(palette)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
        self.setTabletTracking(True)
        icon = QtGui.QIcon.fromTheme("applications-other")
        self.setWindowIcon(icon)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.setStyleSheet(
            "MainWindow >  {\n    url(:/font/media/fonts for text/Momcake-Thin.ttf);\n}"
        )
        self.setAnimated(False)
        self.main_widget = QtWidgets.QWidget(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.main_widget.sizePolicy().hasHeightForWidth())
        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setMinimumSize(QtCore.QSize(800, 480))
        self.main_widget.setMaximumSize(QtCore.QSize(1024, 600))
        self.main_widget.setSizeIncrement(QtCore.QSize(1, 1))
        self.main_widget.setBaseSize(QtCore.QSize(800, 480))
        self.main_widget.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
        self.main_widget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.main_widget.setStyleSheet(
            "#main_widget{background-image: url(:/background/media/1st_background.png);}\n"
            ""
        )
        self.main_widget.setObjectName("main_widget")
        self.main_content_widget = NotificationQTabWidget(parent=self.main_widget)
        self.main_content_widget.setEnabled(True)
        self.main_content_widget.setGeometry(QtCore.QRect(0, 60, 800, 420))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.main_content_widget.sizePolicy().hasHeightForWidth()
        )
        self.main_content_widget.setSizePolicy(sizePolicy)
        self.main_content_widget.setMinimumSize(QtCore.QSize(800, 400))
        self.main_content_widget.setMaximumSize(QtCore.QSize(1024, 720))
        self.main_content_widget.setBaseSize(QtCore.QSize(800, 400))
        self.main_content_widget.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor)
        )
        self.main_content_widget.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.main_content_widget.setAutoFillBackground(False)
        self.main_content_widget.setStyleSheet(
            "#main_content_widget{\n"
            "background-image: url(:/background/media/1st_background.png);\n"
            "}\n"
            "QTabBar::tab{\n"
            "    min-width: 80px;\n"
            "    max-width: 80px;\n"
            "    min-height: 100px;\n"
            "    max-height: 100px;\n"
            "    background: transparent;\n"
            "}\n"
            "\n"
            ""
        )
        self.main_content_widget.setTabPosition(QtWidgets.QTabWidget.TabPosition.West)
        self.main_content_widget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.main_content_widget.setIconSize(QtCore.QSize(60, 60))
        self.main_content_widget.setElideMode(QtCore.Qt.TextElideMode.ElideLeft)
        self.main_content_widget.setUsesScrollButtons(False)
        self.main_content_widget.setDocumentMode(True)
        self.main_content_widget.setTabsClosable(False)
        self.main_content_widget.setMovable(False)
        self.main_content_widget.setObjectName("main_content_widget")
        self.printTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.printTab.sizePolicy().hasHeightForWidth())
        self.printTab.setSizePolicy(sizePolicy)
        self.printTab.setMinimumSize(QtCore.QSize(720, 420))
        self.printTab.setMaximumSize(QtCore.QSize(1024, 720))
        self.printTab.setBaseSize(QtCore.QSize(1024, 420))
        self.printTab.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
        self.printTab.setObjectName("printTab")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_home.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_home_pressed.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_home_blocked.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.main_content_widget.addTab(self.printTab, icon, "")
        self.filamentTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.filamentTab.sizePolicy().hasHeightForWidth())
        self.filamentTab.setSizePolicy(sizePolicy)
        self.filamentTab.setMinimumSize(QtCore.QSize(720, 420))
        self.filamentTab.setMaximumSize(QtCore.QSize(1024, 720))
        self.filamentTab.setBaseSize(QtCore.QSize(1024, 420))
        self.filamentTab.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
        self.filamentTab.setObjectName("filamentTab")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_filament.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_filament_pressed.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_filamente_blocked.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.main_content_widget.addTab(self.filamentTab, icon1, "")
        self.controlTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.controlTab.sizePolicy().hasHeightForWidth())
        self.controlTab.setSizePolicy(sizePolicy)
        self.controlTab.setMinimumSize(QtCore.QSize(720, 420))
        self.controlTab.setMaximumSize(QtCore.QSize(1024, 720))
        self.controlTab.setBaseSize(QtCore.QSize(720, 420))
        self.controlTab.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
        self.controlTab.setObjectName("controlTab")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_control.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_control_pressed.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_control_blocked.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.main_content_widget.addTab(self.controlTab, icon2, "")
        self.utilitiesTab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.utilitiesTab.sizePolicy().hasHeightForWidth())
        self.utilitiesTab.setSizePolicy(sizePolicy)
        self.utilitiesTab.setMinimumSize(QtCore.QSize(720, 420))
        self.utilitiesTab.setMaximumSize(QtCore.QSize(1024, 720))
        self.utilitiesTab.setBaseSize(QtCore.QSize(1024, 420))
        self.utilitiesTab.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))
        self.utilitiesTab.setObjectName("utilitiesTab")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_utilities.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.Off,
        )
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_utilities_pressed.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/media/main_menu/ICON_utilities_blocked.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.main_content_widget.addTab(self.utilitiesTab, icon3, "")
        self.main_header_layout = QtWidgets.QGroupBox(parent=self.main_widget)
        self.main_header_layout.setEnabled(True)
        self.main_header_layout.setGeometry(QtCore.QRect(0, 0, 800, 60))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.main_header_layout.sizePolicy().hasHeightForWidth()
        )
        self.main_header_layout.setSizePolicy(sizePolicy)
        self.main_header_layout.setMinimumSize(QtCore.QSize(800, 60))
        self.main_header_layout.setMaximumSize(QtCore.QSize(1024, 80))
        self.main_header_layout.setSizeIncrement(QtCore.QSize(1, 1))
        self.main_header_layout.setBaseSize(QtCore.QSize(800, 60))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.main_header_layout.setFont(font)
        self.main_header_layout.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor)
        )
        self.main_header_layout.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.main_header_layout.setStyleSheet(
            "QWidget {\n"
            "    background-color: rgb(50,50,50);\n"
            "    color:rgb(255,255,255);\n"
            "    border-color : rgb(60,60,60);\n"
            "    selection-background-color: rgb(60,60,60);\n"
            "    gridline-color:rgb(60,60,60);\n"
            "    selection-color:rgb(60,60,60);\n"
            "}\n"
            "\n"
            "QGroupBox{\n"
            "    background-color: rgb(50,50,50);\n"
            "    border: none; \n"
            "    border-color : rgb(60,60,60);\n"
            "    selection-background-color: rgb(60,60,60);\n"
            "    gridline-color:rgb(60,60,60);\n"
            "    selection-color:rgb(60,60,60);\n"
            "    \n"
            "}\n"
            "\n"
            "QFrame > *{\n"
            "    background-color: rgb(50, 50, 50);\n"
            "    selection-background-color: rgb(60, 60, 60);\n"
            "    gridline-color: rgb(60, 60, 60);\n"
            "    color: rgb(255, 255, 255); \n"
            "    selection-color: rgb(60, 60, 60);\n"
            "    border-bottom-color: rgb(60, 60, 60);\n"
            "    \n"
            "}\n"
            "\n"
            "\n"
            "QPushButton:pressed{\n"
            "    border: none;\n"
            "    background: transparent;\n"
            "}"
        )
        self.main_header_layout.setTitle("")
        self.main_header_layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignJustify | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.main_header_layout.setFlat(True)
        self.main_header_layout.setCheckable(False)
        self.main_header_layout.setObjectName("main_header_layout")
        self.header_main_layout = QtWidgets.QHBoxLayout(self.main_header_layout)
        self.header_main_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinimumSize
        )
        self.header_main_layout.setContentsMargins(5, 0, 5, 0)
        self.header_main_layout.setSpacing(10)
        self.header_main_layout.setObjectName("header_main_layout")
        self.notification_btn = IconButton(parent=self.main_header_layout)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.notification_btn.sizePolicy().hasHeightForWidth()
        )
        self.notification_btn.setSizePolicy(sizePolicy)
        self.notification_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.notification_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.notification_btn.setText("")
        self.notification_btn.setIconSize(QtCore.QSize(60, 60))
        self.notification_btn.setFlat(True)
        self.notification_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/notification.svg")
        )
        self.notification_btn.setObjectName("notification_btn")
        self.header_main_layout.addWidget(
            self.notification_btn, 0, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.extruder_temp_display = DisplayButton(parent=self.main_header_layout)
        self.extruder_temp_display.setMinimumSize(QtCore.QSize(140, 60))
        self.extruder_temp_display.setMaximumSize(QtCore.QSize(160, 60))
        self.extruder_temp_display.setFlat(True)
        self.extruder_temp_display.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/extruder_related/media/btn_icons/nozzle_topbar.svg"),
        )
        self.extruder_temp_display.setObjectName("extruder_temp_display")
        self.header_main_layout.addWidget(
            self.extruder_temp_display, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.bed_temp_display = DisplayButton(parent=self.main_header_layout)
        self.bed_temp_display.setMinimumSize(QtCore.QSize(140, 60))
        self.bed_temp_display.setMaximumSize(QtCore.QSize(160, 60))
        self.bed_temp_display.setFlat(True)
        self.bed_temp_display.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(
                ":/temperature_related/media/btn_icons/temperature_plate.svg"
            ),
        )
        self.bed_temp_display.setObjectName("bed_temp_display")
        self.header_main_layout.addWidget(
            self.bed_temp_display, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.chamber_temp_display = DisplayButton(parent=self.main_header_layout)
        self.chamber_temp_display.setMinimumSize(QtCore.QSize(140, 60))
        self.chamber_temp_display.setMaximumSize(QtCore.QSize(160, 60))
        self.chamber_temp_display.setFlat(True)
        self.chamber_temp_display.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/top_bar_icons/media/topbar/chamber_temp_topbar.svg"),
        )
        self.chamber_temp_display.setProperty(
            "secondary_pixmap",
            QtGui.QPixmap(":/temperature_related/media/btn_icons/humidity.svg"),
        )
        self.chamber_temp_display.setObjectName("chamber_temp_display")
        self.header_main_layout.addWidget(
            self.chamber_temp_display, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.filament_type_icon = IconButton(parent=self.main_header_layout)
        self.filament_type_icon.setMinimumSize(QtCore.QSize(60, 60))
        self.filament_type_icon.setMaximumSize(QtCore.QSize(60, 60))
        self.filament_type_icon.setFlat(True)
        self.filament_type_icon.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/filament_related/media/btn_icons/load_filament.svg"),
        )
        self.filament_type_icon.setObjectName("filament_type_icon")
        self.header_main_layout.addWidget(
            self.filament_type_icon, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.nozzle_size_icon = IconButton(parent=self.main_header_layout)
        self.nozzle_size_icon.setMinimumSize(QtCore.QSize(60, 60))
        self.nozzle_size_icon.setMaximumSize(QtCore.QSize(60, 60))
        self.nozzle_size_icon.setFlat(True)
        self.nozzle_size_icon.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(
                ":/temperature_related/media/btn_icons/standart_temperature.svg"
            ),
        )
        self.nozzle_size_icon.setObjectName("nozzle_size_icon")
        self.header_main_layout.addWidget(
            self.nozzle_size_icon, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.wifi_button = IconButton(parent=self.main_header_layout)
        self.wifi_button.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.wifi_button.sizePolicy().hasHeightForWidth())
        self.wifi_button.setSizePolicy(sizePolicy)
        self.wifi_button.setMinimumSize(QtCore.QSize(60, 60))
        self.wifi_button.setMaximumSize(QtCore.QSize(60, 60))
        self.wifi_button.setStyleSheet("")
        self.wifi_button.setText("")
        self.wifi_button.setIconSize(QtCore.QSize(16, 16))
        self.wifi_button.setCheckable(False)
        self.wifi_button.setChecked(False)
        self.wifi_button.setFlat(True)
        self.wifi_button.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/network/media/btn_icons/network/3bar_wifi.svg"),
        )
        self.wifi_button.setObjectName("wifi_button")
        self.header_main_layout.addWidget(
            self.wifi_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop,
        )
        self.header_main_layout.setStretch(1, 1)
        self.header_main_layout.setStretch(2, 1)
        self.header_main_layout.setStretch(3, 1)
        self.setCentralWidget(self.main_widget)

        self.setWindowTitle("MainWindow")
        self.notification_btn.setProperty(
            "button_type", "icon_text"
        )
        self.extruder_temp_display.setText("extruder")
        self.extruder_temp_display.setProperty(
            "button_type", "secondary_display"
        )
        self.extruder_temp_display.setProperty(
            "name", "extruder_temperature_display"
        )
        self.bed_temp_display.setText("bed")
        self.bed_temp_display.setProperty(
            "button_type", "secondary_display"
        )
        self.chamber_temp_display.setText("chamber")
        self.chamber_temp_display.setProperty(
            "display_format", "dual"
        )
        self.chamber_temp_display.setProperty(
            "button_type", "display_secondary"
        )
        self.filament_type_icon.setText("Filament")
        self.filament_type_icon.setProperty(
            "button_type", "icon_text"
        )
        self.nozzle_size_icon.setText("nozzle")
        self.nozzle_size_icon.setProperty(
            "button_type", "icon_text"
        )
        self.wifi_button.setProperty("button_type", "icon")
        self.main_content_widget.setCurrentIndex(3)
