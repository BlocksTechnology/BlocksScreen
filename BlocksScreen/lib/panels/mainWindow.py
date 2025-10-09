import logging
import typing
from collections import deque

import events
from configfile import BlocksScreenConfig, get_configparser
from lib.files import Files
from lib.machine import MachineControl
from lib.moonrakerComm import MoonWebSocket
from lib.panels.controlTab import ControlTab
from lib.panels.filamentTab import FilamentTab
from lib.panels.networkWindow import NetworkControlWindow
from lib.panels.printTab import PrintTab
from lib.panels.utilitiesTab import UtilitiesTab
from lib.panels.widgets.connectionPage import ConnectionPage
from lib.panels.widgets.popupDialogWidget import Popup
from lib.printer import Printer
from lib.ui.mainWindow_ui import Ui_MainWindow  # With header

# from lib.ui.mainWindow_v2_ui import Ui_MainWindow # No header
from lib.ui.resources.background_resources_rc import *
from lib.ui.resources.font_rc import *
from lib.ui.resources.graphic_resources_rc import *
from lib.ui.resources.icon_resources_rc import *
from lib.ui.resources.main_menu_resources_rc import *
from lib.ui.resources.system_resources_rc import *
from lib.ui.resources.top_bar_resources_rc import *
from PyQt6 import QtCore, QtGui, QtWidgets
from screensaver import ScreenSaver

_logger = logging.getLogger(name="logs/BlocksScreen.log")


class MainWindow(QtWidgets.QMainWindow):
    bo_ws_startup = QtCore.pyqtSignal(name="bo_start_websocket_connection")
    printer_state_signal = QtCore.pyqtSignal(str, name="printer_state")
    query_object_list = QtCore.pyqtSignal(list, name="query_object_list")
    printer_object_report_signal = QtCore.pyqtSignal(
        list, name="handle_report_received"
    )
    gcode_response = QtCore.pyqtSignal(list, name="gcode_response")
    handle_error_response = QtCore.pyqtSignal(list, name="handle_error_response")
    call_network_panel = QtCore.pyqtSignal(name="call-network-panel")
    on_update_message: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="on-update-message"
    )

    def __init__(self):
        super(MainWindow, self).__init__()
        self.config: BlocksScreenConfig = get_configparser()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.screensaver = ScreenSaver(self)

        self.ui.main_content_widget.setCurrentIndex(0)
        self.popup = Popup(self)
        self.ws = MoonWebSocket(self)
        self.mc = MachineControl(self)
        self.file_data = Files(self, self.ws)
        self.index_stack = deque(maxlen=4)
        self.printer = Printer(self, self.ws)
        self.conn_window = ConnectionPage(self, self.ws)
        self.installEventFilter(self.conn_window)
        self.printPanel = PrintTab(
            self.ui.printTab, self.file_data, self.ws, self.printer
        )
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

        self.printPanel.request_change_page.connect(slot=self.global_change_page)
        self.filamentPanel.request_back.connect(slot=self.global_back)
        self.filamentPanel.request_change_page.connect(slot=self.global_change_page)
        self.controlPanel.request_back_button.connect(slot=self.global_back)
        self.controlPanel.request_change_page.connect(slot=self.global_change_page)
        self.utilitiesPanel.request_back.connect(slot=self.global_back)
        self.utilitiesPanel.request_change_page.connect(slot=self.global_change_page)
        self.utilitiesPanel.update_available.connect(self.on_update_available)

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

        # self.ws.connected_signal.connect(
        #     slot=self.file_data.request_file_list.emit
        # )
        # self.ws.connected_signal.connect(
        #     slot=self.file_data.request_dir_info.emit
        # )

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
        self.ui.main_content_widget.currentChanged.connect(slot=self.reset_tab_indexes)
        self.call_network_panel.connect(self.networkPanel.show_network_panel)
        self.conn_window.wifi_button_clicked.connect(self.call_network_panel.emit)
        self.ui.wifi_button.clicked.connect(self.call_network_panel.emit)
        self.handle_error_response.connect(
            self.controlPanel.probe_helper_page.handle_error_response
        )

        self.on_update_message.connect(self.utilitiesPanel._on_update_message)

        self.ui.extruder_temp_display.display_format = "upper_downer"
        self.ui.bed_temp_display.display_format = "upper_downer"

        if self.config.has_section("server"):
            # @ Start websocket connection with moonraker
            self.bo_ws_startup.emit()

        self.reset_tab_indexes()

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

        Returns:
            bool: True if the TabBar was disabled
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

    def disable_popups(self) -> None:
        self.popup_bool = False

    def reset_tab_indexes(self):
        """Used to grantee all tabs reset to their first page once the user leaves the tab"""
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

    @QtCore.pyqtSlot(int, int, name="request_change_page")
    def global_change_page(self, tab_index: int, panel_index: int) -> None:
        """Changes panels pages globally

        Args:
            tab_index (int): The tab index of the panel
            panel_index (int): The index of the panel page
        """
        if not isinstance(tab_index, int):
            _logger.debug(
                f"Tab index argument expected type int, got {type(tab_index)}"
            )
        if not isinstance(panel_index, int):
            _logger.debug(f"Panel page index expected type int, {type(panel_index)}")
        self.printPanel.loadscreen.hide()
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
            f"Requested page change -> Tab index :{requested_page[0]}, pane panel index : {requested_page[1]}"
        )

    @QtCore.pyqtSlot(name="request-back")
    def global_back(self) -> None:
        """Requests to go back a page globally"""
        if not len(self.index_stack):
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
        """Helper method that handles the event messages
        received from the websocket


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
            raise Exception("No method found on message received from websocket")
        if not _data:
            return

        if "server.file" in _method:
            file_data_event = events.ReceivedFileData(_data, _method, _metadata)
            try:
                QtWidgets.QApplication.postEvent(self.file_data, file_data_event)
            except Exception as e:
                _logger.error(
                    f"Error posting event for file related information \
                        received from websocket | error message received: {e}"
                )
        elif "machine" in _method:
            if "ok" in _data:
                # Can here capture if 'ok' if a request for an update was successful
                return
            if "update" in _method:
                if ("status" or "refresh") in _method:
                    self.on_update_message.emit(_data)
        elif "printer.info" in _method:
            # {
            #     "state": "ready",
            #     "state_message": "Printer is ready",
            #     "hostname": "my-pi-hostname",
            #     "software_version": "v0.9.1-302-g900c7396",
            #     "cpu_info": "4 core ARMv7 Processor rev 4 (v7l)",
            #     "klipper_path": "/home/pi/klipper",
            #     "python_path": "/home/pi/klippy-env/bin/python",
            #     "log_file": "/tmp/klippy.log",
            #     "config_file": "/home/pi/printer.cfg",
            # }
            ...
        elif "printer.print" in _method:
            if "start" in _method and "ok" in _data:
                self.printer_state_signal.emit("printing")
            elif "pause" in _method and "ok" in _data:
                self.printer_state_signal.emit("paused")
            elif "resume" in _method and "ok" in _data:
                self.printer_state_signal.emit("printing")
            elif "cancel" in _method and "ok" in _data:
                self.printer_state_signal.emit("canceled")

        elif "printer.objects" in _method:
            if "list" in _method:
                _object_list: list = _data["objects"]
                self.query_object_list[list].emit(_object_list)

            if "subscribe" in _method:
                _objects_response_list = [_data["status"], _data["eventtime"]]
                self.printer_object_report_signal[list].emit(_objects_response_list)

            if "query" in _method:
                if isinstance(_data["status"], dict):
                    _object_report = [_data["status"]]
                    _object_report_keys = _data["status"].items()
                    _object_report_list_dict: list = []
                    for index, key in enumerate(_object_report_keys):
                        _helper_dict: dict = {key[0]: key[1]}
                        _object_report_list_dict.append(_helper_dict)

                    self.printer_object_report_signal[list].emit(
                        _object_report_list_dict
                    )

        elif "notify_klippy" in _method:
            _split = _method.split("_")
            if len(_split) > 2:
                status_type = _split[2]
                _state_upper = status_type[0].upper()
                _state_call = f"{_state_upper}{status_type[1:]}"
                _logger.debug(
                    f"Notify_klippy_{_state_call} Received from object subscription."
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
                                _logger.info(f"Event {_klippy_event_callback} sent")
                                instance.postEvent(self, _event)
                            else:
                                raise Exception("QApplication.instance is None type.")
                        except Exception as e:
                            _logger.debug(
                                f"Unable to send internal klippy {_state_call} notification: {e}"
                            )
        elif "notify_filelist_changed" in _method:
            _file_change_list = _data.get("params")
            if _file_change_list:
                fileaction = _file_change_list[0].get("action")
                filepath = (
                    _file_change_list[0].get("item").get("path")
                )  # TODO : NOTIFY_FILELIST_CHANGED, I DON'T KNOW IF I REALLY WANT TO SEND NOTIFICATIONS ON FILE CHANGES.
            ...
            # self.file_data.request_file_list.emit()

        elif "notify_update_response" in _method:
            ...
        elif "notify_service_state_changed" in _method:
            entry = _data.get("params")
            if entry:
                service_entry: dict = entry[0]
                service_name, service_info = service_entry.popitem()
                if self.disable_popups:
                    return
                self.popup.new_message(
                    message_type=Popup.MessageType.INFO,
                    message=f"""{service_name} service changed state to 
                    {service_info.get("sub_state")}
                    """,
                )
        elif "notify_gcode_response" in _method:
            _gcode_response = _data.get("params")
            self.gcode_response[list].emit(_gcode_response)
            if _gcode_response:
                _gcode_msg_type, _message = str(_gcode_response[0]).split(
                    " ", maxsplit=1
                )
                _msg_type = Popup.MessageType.UNKNOWN
                if _gcode_msg_type == "!!":
                    _msg_type = Popup.MessageType.ERROR
                elif _gcode_msg_type == "//":
                    _msg_type = Popup.MessageType.INFO
                if self.disable_popups:
                    return
                # self.popup.new_message(
                #     message_type=_msg_type, message=str(_message)
                # )

        elif "error" in _method:
            self.handle_error_response[list].emit([_data, _metadata])
            if "metadata" in _data.get("message", "").lower():
                # Quick fix, don't care about no metadata errors
                return
            if self.disable_popups:
                return
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message=str(_data),
            )

        elif "notify_cpu_throttled" in _method:
            if self.disable_popups:
                return
            self.popup.new_message(
                message_type=Popup.MessageType.WARNING,
                message=f"CPU THROTTLED: {_data} | {_metadata}",
            )

        elif "notify_history_changed" in _method:
            ...
        elif "notify_status_update" in _method:
            _object_report = _data["params"]
            self.printer_object_report_signal[list].emit(_object_report)

    @QtCore.pyqtSlot(str, str, float, name="on_extruder_update")
    def on_extruder_update(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        # TODO: Add the text dynamically considering the amount of extruders
        if extruder_name == "extruder":
            if field == "temperature":
                self.ui.extruder_temp_display.setText(f"{new_value:.1f}")
                ...
            elif field == "target":
                self.ui.extruder_temp_display.secondary_text = (
                    f"{round(int(new_value)):.0f}"
                )

    @QtCore.pyqtSlot(str, str, float, name="on_heater_bed_update")
    def on_heater_bed_update(self, name: str, field: str, new_value: float) -> None:
        # TODO: Add the text dynamically considering the amount of extruders
        if field == "temperature":
            self.ui.bed_temp_display.setText(f"{new_value:.1f}")

        elif field == "target":
            self.ui.bed_temp_display.secondary_text = f"{round(int(new_value)):.0f}"

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        # TODO: If tab bar is disabled gray it out
        self.updateGeometry()
        if a0 is None:
            return  # TEST: Maybe this return fucks up the app
        return super().paintEvent(a0)

    @QtCore.pyqtSlot(str, name="set_header_filament_type")
    def set_header_filament_type(self, type: str):
        self.ui.filament_type_icon.setText(f"{type}")
        self.ui.filament_type_icon.update()

    @QtCore.pyqtSlot(str, name="set_header_nozzle_diameter")
    def set_header_nozzle_diameter(self, diam: str):
        self.ui.nozzle_size_icon.setText(f"{diam}mm")
        self.ui.nozzle_size_icon.update()

    def closeEvent(self, a0: typing.Optional[QtGui.QCloseEvent]) -> None:
        _loggers = [
            logging.getLogger(name) for name in logging.root.manager.loggerDict
        ]  # Get available logger handlers
        for logger in _loggers:  # noqa: F402
            if hasattr(logger, "cancel"):
                _callback = getattr(logger, "cancel")
                if callable(_callback):
                    _callback()
        self.ws.wb_disconnect()
        self.close()
        if a0 is None:
            return  # TEST Maybe this return fucks up the app
        QtWidgets.QMainWindow.closeEvent(self, a0)
        super().closeEvent(a0)

    def event(self, event: QtCore.QEvent) -> bool:
        """Receives PyQt Events, reimplemented method from the QEvent class"""
        if event.type() == events.WebSocketMessageReceived.type():
            if isinstance(event, events.WebSocketMessageReceived):
                self.messageReceivedEvent(event)
                return True
            return False
        elif event.type() == events.PrintStart.type():
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
        elif (
            event.type() == events.PrintError.type()
            or event.type() == events.PrintComplete.type()
            or event.type() == events.PrintCancelled.type()
        ):
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
        self.adjustSize()
        return super().sizeHint()
