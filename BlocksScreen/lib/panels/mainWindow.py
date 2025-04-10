import logging
import typing
from collections import deque
from functools import partial

# * System imports
import events
from events import ReceivedFileData, WebSocketMessageReceived
from lib.bo.files import Files
from lib.bo.machine import MachineControl
from lib.bo.printer import Printer
from lib.moonrakerComm import MoonWebSocket

# * Panels
from lib.panels.connectionWindow import ConnectionWindow
from lib.panels.controlTab import ControlTab
from lib.panels.filamentTab import FilamentTab
from lib.panels.networkWindow import NetworkControlWindow
from lib.panels.printTab import PrintTab
from lib.panels.utilitiesTab import UtilitiesTab

# * UI
from lib.ui.mainWindow_ui import Ui_MainWindow  # With header

# from lib.ui.mainWindow_v2_ui import Ui_MainWindow # No header
# * Resources
from lib.ui.resources.background_resources_rc import *
from lib.ui.resources.button_resources_rc import *
from lib.ui.resources.graphic_resources_rc import *
from lib.ui.resources.icon_resources_rc import *
from lib.ui.resources.main_menu_resources_rc import *
from lib.ui.resources.system_resources_rc import *
from lib.ui.resources.top_bar_resources_rc import *

# * PyQt6 imports
from PyQt6.QtCore import QEvent, QSize, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QCloseEvent, QPaintEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from utils.ui import CustomNumpad

_logger = logging.getLogger(name="logs/BlocksScreen.log")


class MainWindow(QMainWindow):
    bo_startup = pyqtSignal(name="bo-start-websocket-connection")
    printer_state_signal = pyqtSignal(str, name="printer_state")
    on_object_list = pyqtSignal(list, name="on_object_list")
    printer_object_report_signal = pyqtSignal(list, name="handle_report_received")

    handle_gcode_response = pyqtSignal(list, name="handle_gcode_response")
    handle_error_response = pyqtSignal(list, name="handle_error_response")

    call_numpad_signal = pyqtSignal(
        int, str, str, "PyQt_PyObject", QStackedWidget, name="call_numpad"
    )
    call_network_panel = pyqtSignal(name="visibilityChange_networkPanel")

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.objects_subscriptions: dict = {}
        self.ws = MoonWebSocket(self)
        self.mc = MachineControl(self)

        self.file_data = Files(self, self.ws)
        self.index_stack = deque(maxlen=4)
        self.printer = Printer(self, self.ws)

        self.numpad_object = CustomNumpad(self)
        self.numpad_object.hide()

        self.start_window = ConnectionWindow(self, self.ws)
        self.installEventFilter(self.start_window)
        self.printPanel = PrintTab(
            self.ui.printTab, self.file_data, self.ws, self.printer
        )
        self.filamentPanel = FilamentTab(self.ui.filamentTab, self.printer, self.ws)
        self.controlPanel = ControlTab(self.ui.controlTab, self.ws, self.printer)
        self.utilitiesPanel = UtilitiesTab(self.ui.utilitiesTab)
        self.networkPanel = NetworkControlWindow(self)

        # @ Slot connections
        self.bo_startup.connect(slot=self.start_websocket_connection)
        # * Websocket state signals
        self.ws.connecting_signal.connect(slot=self.start_window.websocket_connecting)
        self.ws.connected_signal.connect(
            slot=self.start_window.websocket_connection_achieved
        )
        self.ws.connection_lost.connect(
            slot=self.start_window.websocket_connection_lost
        )
        self.ws.klippy_state_signal.connect(self.ws.api.request_printer_info)

        # * Print panel
        self.printPanel.request_back_button_pressed.connect(
            slot=self.global_back_button_pressed
        )
        self.printPanel.request_change_page.connect(slot=self.global_change_page)
        # * Filament panel
        self.filamentPanel.request_back_button_pressed.connect(
            slot=self.global_back_button_pressed
        )
        self.filamentPanel.request_change_page.connect(slot=self.global_change_page)
        # * Control panel
        self.controlPanel.request_back_button.connect(
            slot=self.global_back_button_pressed
        )
        self.controlPanel.request_change_page.connect(slot=self.global_change_page)
        # * Utilities panel
        self.utilitiesPanel.request_back_button_pressed.connect(
            slot=self.global_back_button_pressed
        )
        self.utilitiesPanel.request_change_page.connect(slot=self.global_change_page)

        # * Main page - Top bar Buttons
        self.ui.extruder_temp_display.clicked.connect(
            partial(self.global_change_page, 2, 4)
        )

        self.ui.bed_temp_display.clicked.connect(partial(self.global_change_page, 2, 4))

        self.ui.filament_type_icon.clicked.connect(
            partial(self.global_change_page, 1, 1)
        )
        self.ui.filament_type_icon.setText("PLA")
        self.ui.filament_type_icon.update()
        self.ui.nozzle_size_icon.setText("0.4mm")
        self.ui.nozzle_size_icon.update()
        ##* Also connect to files list when connection is achieved to imm1ediately get the files
        self.ws.connected_signal.connect(slot=self.file_data.request_file_list.emit)
        self.start_window.retry_connection_clicked.connect(slot=self.ws.retry)
        self.start_window.firmware_restart_clicked.connect(
            slot=self.ws.api.firmware_restart
        )
        self.start_window.restart_klipper_clicked.connect(
            slot=self.mc.restart_klipper_service
        )
        self.start_window.reboot_clicked.connect(slot=self.mc.machine_restart)

        # *  To Printer object
        self.printer_object_report_signal.connect(
            self.printer.on_object_report_received
        )
        self.handle_gcode_response.connect(self.printer.gcode_response_report)
        self.on_object_list.connect(self.printer.on_object_list)
        # * From Printer Object
        self.printer.on_extruder_update.connect(self.extruder_temperature_change)
        self.printer.on_heater_bed_update.connect(self.heater_bed_temperature_change)

        self.ui.main_content_widget.currentChanged.connect(slot=self.reset_tab_indexes)

        # * Pages that need the Numpad
        self.call_numpad_signal.connect(self.numpad_object.call_numpad)
        self.numpad_object.request_change_page.connect(self.global_change_page)
        self.controlPanel.request_numpad_signal.connect(
            partial(self.call_numpad_signal.emit)
        )
        self.printPanel.request_numpad_signal.connect(
            partial(self.call_numpad_signal.emit)
        )

        self.printPanel.request_block_manual_tab_change.connect(self.disable_tab_bar)
        self.printPanel.request_activate_manual_tab_change.connect(self.enable_tab_bar)

        # * Network panel call
        self.call_network_panel.connect(self.networkPanel.call_network_panel)
        self.start_window.wifi_button_clicked.connect(self.call_network_panel.emit)
        self.ui.wifi_button.clicked.connect(self.call_network_panel.emit)

        #####
        self.handle_error_response.connect(
            self.controlPanel.probe_helper_page.handle_error_response
        )
        #####

        # @ Force main panel to be displayed on startup
        self.reset_tab_indexes()
        self.ui.main_content_widget.setCurrentIndex(0)

    @pyqtSlot(name="activate_manual_tab_change")
    def enable_tab_bar(self) -> None:
        if (
            self.ui.main_content_widget.isTabEnabled(1)
            and self.ui.main_content_widget.isTabEnabled(2)
            and self.ui.main_content_widget.isTabEnabled(3)
            and self.ui.main_content_widget.isTabEnabled(4)
            and self.ui.header_main_layout.isEnabled()
        ):
            self.ui.main_content_widget.setTabEnabled(1, True)
            self.ui.main_content_widget.setTabEnabled(2, True)
            self.ui.main_content_widget.setTabEnabled(3, True)
            self.ui.main_content_widget.setTabEnabled(4, True)
            self.ui.header_main_layout.setEnabled(True)

    @pyqtSlot(name="block_manual_tab_change")
    def disable_tab_bar(self) -> bool:
        """disable_tab_bar
            Disables the tab bar so to not change the tab.

        Returns:
            bool: True if the TabBar was disabled
        """

        self.ui.main_content_widget.setTabEnabled(1, False)
        self.ui.main_content_widget.setTabEnabled(2, False)
        self.ui.main_content_widget.setTabEnabled(3, False)
        self.ui.main_content_widget.setTabEnabled(4, False)
        self.ui.header_main_layout.setEnabled(False)

        return (
            False
            if self.ui.main_content_widget.isTabEnabled(1)
            and self.ui.main_content_widget.isTabEnabled(2)
            and self.ui.main_content_widget.isTabEnabled(3)
            and self.ui.main_content_widget.isTabEnabled(4)
            and self.ui.header_main_layout.isEnabled()
            else True
        )

    def reset_tab_indexes(self):
        """reset_tab_indexes
        Used to grantee all tabs reset to their first page once the user leaves the tab
        """
        self.printPanel.setCurrentIndex(0)
        self.filamentPanel.setCurrentIndex(0)
        self.controlPanel.setCurrentIndex(0)
        self.utilitiesPanel.setCurrentIndex(0)
        self.networkPanel.setCurrentIndex(0)

    def current_panel_index(self) -> int:
        """current_panel_index
            Helper function to get the index of the current page in the current tab
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
        """set_current_panel_index
            Helper function to set the index of the current page in the current tab

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

    @pyqtSlot(int, int, name="request_change_page")
    def global_change_page(self, tab_index: int, panel_index: int) -> None:
        """global_change_page Changes panels pages globally

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
        current_page = [
            self.ui.main_content_widget.currentIndex(),
            self.current_panel_index(),
        ]
        requested_page = [tab_index, panel_index]
        # * Return if user is already on the requested page
        if requested_page == current_page:
            _logger.debug("User is already on the requested page")
            return
        # * Add to the stack of indexes the indexes of current tab and page in tab to later be able to come back to them
        self.index_stack.append(current_page)
        # * Go to the requested tab and page
        self.ui.main_content_widget.setCurrentIndex(tab_index)
        self.set_current_panel_index(panel_index)
        _logger.debug(
            f"Requested page change -> Tab index :{requested_page[0]}, pane panel index : {requested_page[1]}"
        )

    @pyqtSlot(name="request_back_button_pressed")
    def global_back_button_pressed(self) -> None:
        """global_back_button_pressed

        Requests to go back a page globally
        """
        # * Just a safety measure to avoid accessing an inexistant position of the index_stack
        if not len(self.index_stack):
            _logger.debug("Index stack is empty cannot got further back.")
            return
        # * From the last position of the stack use the first value of its tuple, tab index
        self.ui.main_content_widget.setCurrentIndex(self.index_stack[-1][0])
        self.set_current_panel_index(
            self.index_stack[-1][1]
        )  # From the same position, use the tab and stacked widget page indexes
        self.index_stack.pop()  # Remove the last position.

        _logger.debug("Successfully went back a page.")

    @pyqtSlot(name="bo-start-websocket-connection")
    def start_websocket_connection(self) -> None:
        """start_websocket_connection

        Starts the Websocket connection
        """
        self.ws.start()
        self.ws.try_connection()

    def event(self, event: QEvent) -> bool:
        """event Receives PyQt Events, this method is reimplemented from the QEvent class

        Args:
            event (QEvent): An Event

        Returns:
            bool: If the event is handled or not
        """

        if event.type() == WebSocketMessageReceived.type():
            if isinstance(event, WebSocketMessageReceived):
                self.messageReceivedEvent(event)
                return True
            return False
        return super().event(event)

    def messageReceivedEvent(self, event: WebSocketMessageReceived) -> None:
        """messageReceivedEvent
            Helper method that handles the event messages received from the websocket

        Args:
            event (WebSocketMessageReceivedEvent): The message event with all its contents

        Raises:
            Exception: When a klippy status change comes from the websocket, tries to send another event
            corresponding to the incoming status. If the QApplication instance is of type None raises an exception
            because the event cannot be sent.
        """

        _method = event.method
        _data = event.data
        _metadata = event.metadata

        if _method is None:
            print("has no method on the received websocket response ")
            raise Exception("Message received from websocket has no method")
        if _data is None:
            print("No data on the received websocket response ")
            raise Exception("Message received from websocket has no data")

        if "server.file" in _method:
            file_data_event = ReceivedFileData(_data, _method, _metadata)
            try:
                QApplication.postEvent(self.file_data, file_data_event)
            except Exception as e:
                _logger.error(
                    f"Error emitting event for file related information received from websocket | error message received: {e}"
                )
        elif "machine" in _method:
            ...
        elif "printer.info" in _method:
            pass
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
                self.on_object_list[list].emit(_object_list)

            if "subscribe" in _method:
                _objects_response_list = [_data["status"], _data["eventtime"]]
                self.printer_object_report_signal[list].emit(_objects_response_list)
                # TODO: This
                # ! Don't display chamber temperatures if there is no chamber, should do the
                if not self.printer.has_chamber:
                    # self.ui.chamber_temperature_frame.hide()
                    ...
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
                            instance = QApplication.instance()
                            if not isinstance(_event, QEvent):
                                return
                            if instance is not None:
                                _logger.info(f"Event {_klippy_event_callback} sent")
                                instance.sendEvent(self, _event)
                            else:
                                raise Exception("QApplication.instance is None type.")
                        except Exception as e:
                            _logger.debug(
                                f"Unable to send internal klippy {_state_call} notification: {e}"
                            )
        elif "notify_filelist_changed" in _method:
            self.file_data.request_file_list.emit()
        elif "notify_update_response" in _method:
            ...
        elif "notify_service_state_changed" in _method:
            ...
        elif "notify_gcode_response" in _method:
            # TODO: Handle different types of gcode responses can be  !! or // messages
            _gcode_response = _data["params"]
            self.handle_gcode_response[list].emit(_gcode_response)
        elif "error" in _method:
            self.handle_error_response[list].emit([_data, _metadata])
        elif "notify_history_changed" in _method:
            ...
        elif "notify_status_update" in _method:
            _object_report = _data["params"]
            self.printer_object_report_signal[list].emit(_object_report)

    @pyqtSlot(str, str, float, name="extruder_update")
    def extruder_temperature_change(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        # TODO: Add the text dynamically considering the amount of extruders
        if extruder_name == "extruder":
            if field == "temperature":
                self.ui.extruder_temp_display.setText(f"{new_value:.1f}")
                ...
            elif field == "target":
                self.ui.extruder_temp_display.setSecondaryText(f"{new_value:.1f}")

    @pyqtSlot(str, str, float, name="heater_bed_update")
    def heater_bed_temperature_change(
        self, name: str, field: str, new_value: float
    ) -> None:
        # TODO: Add the text dynamically considering the amount of extruders
        if field == "temperature":
            self.ui.bed_temp_display.setText(f"{new_value:.1f}")

        elif field == "target":
            self.ui.bed_temp_display.setSecondaryText(f"{new_value:.1f}")

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        # TODO: If tab bar is disabled gray it out
        self.updateGeometry()
        if a0 is None:
            return  # TEST: Maybe this return fucks up the app
        return super().paintEvent(a0)

    @pyqtSlot(str, name="set_header_filament_type")
    def set_header_filament_type(self, type: str):
        self.ui.filament_type_icon.setText(f"{type}")
        self.ui.filament_type_icon.update()

    @pyqtSlot(str, name="set_header_nozzle_diameter")
    def set_header_nozzle_diameter(self, diam: str):
        self.ui.nozzle_size_icon.setText(f"{diam}mm")
        self.ui.nozzle_size_icon.update()

    def closeEvent(self, a0: typing.Optional[QCloseEvent]) -> None:
        _loggers = [
            logging.getLogger(name) for name in logging.root.manager.loggerDict
        ]  # Get available logger handlers
        for logger in _loggers:  # noqa: F402
            if hasattr(logger, "cancel"):
                _callback = getattr(logger, "cancel")
                if callable(_callback):
                    _callback()
        self.ws.disconnect()
        self.close()
        if a0 is None:
            return  # TEST Maybe this return fucks up the app
        QMainWindow.closeEvent(self, a0)
        super().closeEvent(a0)

    def sizeHint(self) -> QSize:
        self.adjustSize()

        return super().sizeHint()
