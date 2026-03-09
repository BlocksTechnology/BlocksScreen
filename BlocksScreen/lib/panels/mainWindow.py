import logging
import typing
from collections import deque

import events
from configfile import BlocksScreenConfig, get_configparser
from devices.storage.usb_controller import USBManager
from lib.files import Files
from lib.machine import MachineControl
from lib.moonrakerComm import MoonWebSocket
from lib.network import WifiIconKey
from lib.panels.controlTab import ControlTab
from lib.panels.filamentTab import FilamentTab
from lib.panels.networkWindow import NetworkControlWindow, PixmapCache
from lib.panels.printTab import PrintTab
from lib.panels.utilitiesTab import UtilitiesTab
from lib.panels.widgets.basePopup import BasePopup
from lib.panels.widgets.cancelPage import CancelPage
from lib.panels.widgets.connectionPage import ConnectionPage
from lib.panels.widgets.loadWidget import LoadingOverlayWidget
from lib.panels.widgets.notificationPage import NotificationPage
from lib.panels.widgets.updatePage import UpdatePage
from lib.printer import Printer
from lib.ui.mainWindow_ui import Ui_MainWindow  # With header
from lib.ui.resources.background_resources_rc import *
from lib.ui.resources.font_rc import *
from lib.ui.resources.graphic_resources_rc import *
from lib.ui.resources.icon_resources_rc import *
from lib.ui.resources.main_menu_resources_rc import *
from lib.ui.resources.system_resources_rc import *
from lib.ui.resources.top_bar_resources_rc import *
from logger import LogManager
from PyQt6 import QtCore, QtGui, QtWidgets
from screensaver import ScreenSaver

_logger = logging.getLogger(__name__)


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

    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")

    def __init__(self):
        """Set up UI, instantiate subsystems, and wire all inter-component signals."""
        super(MainWindow, self).__init__()
        self.config: BlocksScreenConfig = get_configparser()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.screensaver = ScreenSaver(self)
        self._popup_toggle: bool = False
        self.ui.main_content_widget.setCurrentIndex(0)
        self.ws = MoonWebSocket(self)
        self.notiPage = NotificationPage(self)
        self.mc = MachineControl(self)
        self.file_data = Files(self, self.ws)
        self.index_stack = deque(maxlen=4)
        self.printer = Printer(self, self.ws)
        self.conn_window = ConnectionPage(self, self.ws)
        self.update_page = UpdatePage(self)
        self.update_page.hide()

        self.conn_window.call_cancel_panel.connect(self.handle_cancel_print)
        self.installEventFilter(self.conn_window)
        self.printPanel = PrintTab(
            self.ui.printTab, self.file_data, self.ws, self.printer
        )
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.BlankCursor)

        self.filamentPanel = FilamentTab(self.ui.filamentTab, self.printer, self.ws)
        self.controlPanel = ControlTab(self.ui.controlTab, self.ws, self.printer)
        self.utilitiesPanel = UtilitiesTab(self.ui.utilitiesTab, self.ws, self.printer)
        self.networkPanel = NetworkControlWindow(self)
        self.bo_ws_startup.connect(slot=self.bo_start_websocket_connection)
        self.ws.connecting_signal.connect(self.conn_window.on_websocket_connecting)
        self.ws.connected_signal.connect(
            self.conn_window.on_websocket_connection_achieved
        )
        self.ws.connection_lost.connect(self.conn_window.on_websocket_connection_lost)
        self.printer.webhooks_update.connect(self.conn_window.webhook_update)
        self.printPanel.request_back.connect(slot=self.global_back)
        self.printPanel.on_cancel_print.connect(slot=self.on_cancel_print)

        self.show_notifications.connect(self.notiPage.new_notication)

        self.printPanel.request_change_page.connect(slot=self.global_change_page)
        self.filamentPanel.request_back.connect(slot=self.global_back)
        self.filamentPanel.request_change_page.connect(slot=self.global_change_page)
        self.controlPanel.request_back_button.connect(slot=self.global_back)
        self.controlPanel.request_change_page.connect(slot=self.global_change_page)
        self.utilitiesPanel.request_back.connect(slot=self.global_back)
        self.utilitiesPanel.request_change_page.connect(slot=self.global_change_page)
        self.utilitiesPanel.update_available.connect(self.on_update_available)
        self.ui.notification_btn.clicked.connect(self.notiPage.show_notification_panel)
        self.ui.extruder_temp_display.clicked.connect(
            lambda: self.global_change_page(
                self.ui.main_content_widget.indexOf(self.ui.controlTab),
                self.controlPanel.indexOf(self.controlPanel.panel.temperature_page),
            )
        )
        self.ui.bed_temp_display.clicked.connect(
            lambda: self.global_change_page(
                self.ui.main_content_widget.indexOf(self.ui.controlTab),
                self.controlPanel.indexOf(self.controlPanel.panel.temperature_page),
            )
        )
        self.ui.filament_type_icon.clicked.connect(
            lambda: self.global_change_page(
                self.ui.main_content_widget.indexOf(self.ui.filamentTab),
                self.filamentPanel.indexOf(self.filamentPanel.panel.load_page),
            )
        )
        self.ui.filament_type_icon.setText("PLA")
        self.ui.filament_type_icon.update()
        self.ui.nozzle_size_icon.setText("0.4mm")
        self.ui.nozzle_size_icon.update()

        self.conn_window.retry_connection_clicked.connect(slot=self.ws.retry_wb_conn)
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
        self.run_gcode_signal.connect(self.ws.api.run_gcode)

        self.ui.main_content_widget.currentChanged.connect(slot=self.reset_tab_indexes)
        self.call_network_panel.connect(self.networkPanel.show_network_panel)
        self.call_notification_panel.connect(self.notiPage.show_notification_panel)
        self.networkPanel.update_wifi_icon.connect(self.change_wifi_icon)
        self.conn_window.wifi_button_clicked.connect(self.call_network_panel.emit)
        self.conn_window.notification_btn_clicked.connect(
            self.call_notification_panel.emit
        )
        self.ui.wifi_button.clicked.connect(self.call_network_panel.emit)
        self.handle_error_response.connect(
            self.controlPanel.probe_helper_page.handle_error_response
        )
        self.controlPanel.disable_popups.connect(self.popup_toggle)
        self.on_update_message.connect(self.update_page.handle_update_message)
        self.update_page.request_full_update.connect(self.ws.api.full_update)
        self.update_page.request_recover_repo[str].connect(
            self.ws.api.recover_corrupt_repo
        )
        self.update_page.request_recover_repo[str, bool].connect(
            self.ws.api.recover_corrupt_repo
        )
        self.update_page.request_refresh_update.connect(
            self.ws.api.refresh_update_status
        )
        self.update_page.request_refresh_update[str].connect(
            self.ws.api.refresh_update_status
        )
        self.update_page.request_rollback_update.connect(self.ws.api.rollback_update)
        self.update_page.request_update_client.connect(self.ws.api.update_client)
        self.update_page.request_update_klipper.connect(self.ws.api.update_klipper)
        self.update_page.request_update_moonraker.connect(self.ws.api.update_moonraker)
        self.update_page.request_update_status.connect(self.ws.api.update_status)
        self.update_page.request_update_system.connect(self.ws.api.update_system)
        self.update_page.update_back_btn.clicked.connect(self.update_page.hide)
        self.utilitiesPanel.show_update_page.connect(self.show_update_page)
        self.conn_window.update_button_clicked.connect(self.show_update_page)
        self.ui.extruder_temp_display.display_format = "upper_downer"
        self.ui.bed_temp_display.display_format = "upper_downer"

        self.controlPanel.call_load_panel.connect(self.show_LoadScreen)
        self.filamentPanel.call_load_panel.connect(self.show_LoadScreen)
        self.printPanel.call_load_panel.connect(self.show_LoadScreen)
        self.utilitiesPanel.call_load_panel.connect(self.show_LoadScreen)
        self.conn_window.call_load_panel.connect(self.show_LoadScreen)

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
        self.printPanel.call_cancel_panel.connect(self.handle_cancel_print)

        if self.config.has_section("server"):
            self.bo_ws_startup.emit()
        self.reset_tab_indexes()

    @QtCore.pyqtSlot(bool, name="show-cancel-page")
    def handle_cancel_print(self, show: bool = True):
        """Slot for displaying update Panel"""
        if not show:
            self.cancelpage.hide()
            return

        self.cancelpage.setGeometry(0, 0, self.width(), self.height())
        self.cancelpage.raise_()
        self.cancelpage.updateGeometry()
        self.cancelpage.repaint()
        self.cancelpage.show()

    @QtCore.pyqtSlot(bool, str, name="show-load-page")
    def show_LoadScreen(self, show: bool = True, msg: str = ""):
        """Show or hide the loading overlay, guarded by the calling panel's visibility."""
        _sender = self.sender()

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
            self.update_page.setParent(self.ui.main_content_widget)
            current_index = self.ui.main_content_widget.currentIndex()
            tab_rect = self.ui.main_content_widget.tabBar().tabRect(current_index)
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

    @QtCore.pyqtSlot(name="on-cancel-print")
    def on_cancel_print(self):
        """Slot for cancel print signal"""
        self.enable_tab_bar()
        self.ui.extruder_temp_display.clicked.disconnect()
        self.ui.bed_temp_display.clicked.disconnect()
        self.ui.filament_type_icon.setDisabled(False)
        self.ui.nozzle_size_icon.setDisabled(False)
        self.ui.extruder_temp_display.clicked.connect(
            lambda: self.global_change_page(
                self.ui.main_content_widget.indexOf(self.ui.controlTab),
                self.controlPanel.indexOf(self.controlPanel.panel.temperature_page),
            )
        )
        self.ui.bed_temp_display.clicked.connect(
            lambda: self.global_change_page(
                self.ui.main_content_widget.indexOf(self.ui.controlTab),
                self.controlPanel.indexOf(self.controlPanel.panel.temperature_page),
            )
        )

    @QtCore.pyqtSlot(bool, name="update-available")
    def on_update_available(self, state: bool = False):
        """Signal render for red dot on utilities tab icon"""
        self.ui.main_content_widget.setNotification(3, state)
        self.repaint()

    def enable_tab_bar(self) -> bool:
        """Enables the tab bar

            `This method is only used when a print job is ongoing, so the printTab is never disabled`

        Returns:
            bool: True if the TabBar was disabled
        """

        self.ui.main_content_widget.setTabEnabled(
            self.ui.main_content_widget.indexOf(self.ui.filamentTab), True
        )
        self.ui.main_content_widget.setTabEnabled(
            self.ui.main_content_widget.indexOf(self.ui.controlTab), True
        )
        self.ui.main_content_widget.setTabEnabled(
            self.ui.main_content_widget.indexOf(self.ui.utilitiesTab), True
        )
        self.ui.header_main_layout.setEnabled(True)
        return all(
            [
                not self.ui.main_content_widget.isTabEnabled(
                    self.ui.main_content_widget.indexOf(self.ui.filamentTab)
                ),
                not self.ui.main_content_widget.isTabEnabled(
                    self.ui.main_content_widget.indexOf(self.ui.controlTab)
                ),
                not self.ui.main_content_widget.isTabEnabled(
                    self.ui.main_content_widget.indexOf(self.ui.utilitiesTab)
                ),
                not self.ui.header_main_layout.isEnabled(),
            ]
        )

    def disable_tab_bar(self) -> bool:
        """Disables the tab bar so to not change the tab.

        `This method is only used when a print job is ongoing, so the printTab is never disabled`


        ---

        Returns:
            boolean: True if the TabBar was disabled
        """
        self.ui.main_content_widget.setTabEnabled(
            self.ui.main_content_widget.indexOf(self.ui.filamentTab), False
        )
        self.ui.main_content_widget.setTabEnabled(
            self.ui.main_content_widget.indexOf(self.ui.controlTab), False
        )
        self.ui.main_content_widget.setTabEnabled(
            self.ui.main_content_widget.indexOf(self.ui.utilitiesTab), False
        )
        self.ui.header_main_layout.setEnabled(False)
        return all(
            [
                not self.ui.main_content_widget.isTabEnabled(
                    self.ui.main_content_widget.indexOf(self.ui.filamentTab)
                ),
                not self.ui.main_content_widget.isTabEnabled(
                    self.ui.main_content_widget.indexOf(self.ui.controlTab)
                ),
                not self.ui.main_content_widget.isTabEnabled(
                    self.ui.main_content_widget.indexOf(self.ui.utilitiesTab)
                ),
                not self.ui.header_main_layout.isEnabled(),
            ]
        )

    @QtCore.pyqtSlot(bool, name="toggle-popups")
    def popup_toggle(self, toggle: bool) -> None:
        """Toggles app popups"""
        self._popup_toggle = toggle

    def reset_tab_indexes(self):
        """
        Used to grantee all tabs reset to their
        first page once the user leaves the tab
        """
        self.update_page.hide()
        self.printPanel.setCurrentIndex(0)
        self.filamentPanel.setCurrentIndex(0)
        self.controlPanel.setCurrentIndex(0)
        self.utilitiesPanel.setCurrentIndex(0)
        self.networkPanel.setCurrentIndex(0)

    def current_panel_index(self) -> int:
        """Helper function to get the index of the current page in the current tab

        Returns:
            int: The index os the page
        """
        match self.ui.main_content_widget.currentIndex():
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
        match self.ui.main_content_widget.currentIndex():
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
        self.ui.wifi_button.setPixmap(HeaderWifiIconProvider.get_pixmap(icon_key))

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

        self.show_LoadScreen(False)
        current_page = [
            self.ui.main_content_widget.currentIndex(),
            self.current_panel_index(),
        ]
        requested_page = [tab_index, panel_index]
        if requested_page == current_page:
            _logger.debug("User is already on the requested page")
            return
        self.index_stack.append(current_page)
        self.ui.main_content_widget.setCurrentIndex(tab_index)
        self.set_current_panel_index(panel_index)
        _logger.debug(
            f"Requested page change -> Tab index : {requested_page[0]} | panel index : {requested_page[1]}",
        )

    @QtCore.pyqtSlot(name="request-back")
    def global_back(self) -> None:
        """Requests to go back a page globally"""
        if not bool(self.index_stack):
            _logger.debug("Index stack is empty, cannot go back any further")
            return
        self.ui.main_content_widget.setCurrentIndex(self.index_stack[-1][0])
        self.set_current_panel_index(self.index_stack[-1][1])
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
                    _object_report = [data["status"]]
                    _object_report_keys = data["status"].items()
                    _object_report_list_dict: list = []
                    for _, key in enumerate(_object_report_keys):
                        _helper_dict: dict = {key[0]: key[1]}
                        _object_report_list_dict.append(_helper_dict)
                    self.printer_object_report_signal[list].emit(
                        _object_report_list_dict
                    )

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
                        _event = _klippy_event_callback(
                            data=f"Moonraker reported klippy is {_state_call}"
                        )
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

    @api_handler
    def _handle_notify_gcode_response_message(self, method, data, metadata) -> None:
        """Handle websocket gcode responses messages"""
        _gcode_response = data.get("params")
        self.gcode_response[list].emit(_gcode_response)
        if _gcode_response:
            if self._popup_toggle:
                return
            _gcode_msg_type, _message = str(_gcode_response[0]).split(" ", maxsplit=1)
            popupWhitelist = ["filament runout", "no filament"]
            if _message.lower() not in popupWhitelist or _gcode_msg_type != "!!":
                return
            self.show_notifications.emit("mainwindow", _message, 3, True)

    @api_handler
    def _handle_error_message(self, method, data, metadata) -> None:
        """Handle error messages from Moonraker API."""
        self.handle_error_response[list].emit([data, metadata])
        if self._popup_toggle:
            return

        text = data.get("message", str(data)) if isinstance(data, dict) else str(data)
        lower_text = text.lower()

        # Metadata errors - silent, handled by files_manager
        if "metadata" in lower_text:
            self.file_data.handle_metadata_error(text)
            return

        # File not found - silent
        if "file" in lower_text and "does not exist" in lower_text:
            return

        # Directory not found - navigate back + show popup
        if "does not exist" in lower_text:
            self.printPanel.filesPage_widget.on_directory_error()

        # Show popup for all other errors (including directory errors)
        self.show_notifications.emit("mainwindow", str(text), 3, True)
        _logger.error(text)

    @api_handler
    def _handle_notify_cpu_throttled_message(self, method, data, metadata) -> None:
        """Handle websocket cpu throttled messages"""
        if self._popup_toggle:
            return
        self.show_notifications.emit("mainwindow", data, 2, False)

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
                self.ui.extruder_temp_display.setText(f"{new_value:.1f}")
            elif field == "target":
                self.ui.extruder_temp_display.secondary_text = (
                    f"{round(int(new_value)):.0f}"
                )

    @QtCore.pyqtSlot(str, str, float, name="on-heater-bed-update")
    def on_heater_bed_update(self, name: str, field: str, new_value: float) -> None:
        """Handles heater_bed printer object updates"""
        if field == "temperature":
            self.ui.bed_temp_display.setText(f"{new_value:.1f}")
        elif field == "target":
            self.ui.bed_temp_display.secondary_text = f"{round(int(new_value)):.0f}"

    @QtCore.pyqtSlot(str, name="set-header-filament-type")
    def set_header_filament_type(self, type: str):
        """Sets header filament text label"""
        self.ui.filament_type_icon.setText(f"{type}")
        self.ui.filament_type_icon.update()

    @QtCore.pyqtSlot(str, name="set-header-nozzle-diameter")
    def set_header_nozzle_diameter(self, diam: str):
        """Sets header nozzle diameter text label"""
        self.ui.nozzle_size_icon.setText(f"{diam}mm")
        self.ui.nozzle_size_icon.update()

    def closeEvent(self, a0: typing.Optional[QtGui.QCloseEvent]) -> None:
        """Handles GUI closing"""
        try:
            self.networkPanel.close()
        except Exception as e:
            _logger.warning("Network panel shutdown error: %s", e)

        self.ws.wb_disconnect()
        LogManager.shutdown()
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
            self.disable_tab_bar()
            self.ui.extruder_temp_display.clicked.disconnect()
            self.ui.bed_temp_display.clicked.disconnect()
            self.ui.filament_type_icon.setDisabled(True)
            self.ui.nozzle_size_icon.setDisabled(True)
            self.ui.extruder_temp_display.clicked.connect(
                lambda: self.global_change_page(
                    self.ui.main_content_widget.indexOf(self.ui.printTab),
                    self.printPanel.indexOf(self.printPanel.tune_page),
                )
            )
            self.ui.bed_temp_display.clicked.connect(
                lambda: self.global_change_page(
                    self.ui.main_content_widget.indexOf(self.ui.printTab),
                    self.printPanel.indexOf(self.printPanel.tune_page),
                )
            )
            return False

        if event.type() in (
            events.PrintError.type(),
            events.PrintComplete.type(),
            events.PrintCancelled.type(),
        ):
            if event.type() == events.PrintCancelled.type():
                self.handle_cancel_print()
            self.enable_tab_bar()
            self.ui.extruder_temp_display.clicked.disconnect()
            self.ui.bed_temp_display.clicked.disconnect()
            self.ui.filament_type_icon.setDisabled(False)
            self.ui.nozzle_size_icon.setDisabled(False)
            self.ui.extruder_temp_display.clicked.connect(
                lambda: self.global_change_page(
                    self.ui.main_content_widget.indexOf(self.ui.controlTab),
                    self.controlPanel.indexOf(self.controlPanel.panel.temperature_page),
                )
            )
            self.ui.bed_temp_display.clicked.connect(
                lambda: self.global_change_page(
                    self.ui.main_content_widget.indexOf(self.ui.controlTab),
                    self.controlPanel.indexOf(self.controlPanel.panel.temperature_page),
                )
            )
            return False
        return super().event(event)

    def sizeHint(self) -> QtCore.QSize:
        """Sets default size for the widget"""
        self.adjustSize()
        return super().sizeHint(QtCore.QSize(800, 480))
