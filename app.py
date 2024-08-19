import logging
import sys
from collections import deque
from functools import partial

from PyQt6.QtCore import QEvent, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPaintEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen, QStackedWidget

# * Panels
from panels.connectionWindow import ConnectionWindow
from panels.controlTab import ControlTab
from panels.filamentTab import FilamentTab
from panels.networkWindow import NetworkControlWindow
from panels.printTab import PrintTab
from panels.utilitiesTab import UtilitiesTab

# * UI
from qt_ui.Blocks_Screen_Lemos_ui import Ui_MainWindow
from qt_ui.ui_util import CustomNumpad, CustomQPushButton

# * Resources
from resources.background_resources_rc import *
from resources.button_resources_rc import *
from resources.main_menu_resources_rc import *
from resources.system_resources_rc import *

# * System imports
from scripts import events
from scripts.bo_includes.bo_files import Files
from scripts.bo_includes.bo_machine import MachineControl
from scripts.bo_includes.bo_printer import Printer
from scripts.events import ReceivedFileDataEvent, WebSocketMessageReceivedEvent
from scripts.moonrakerComm import MoonWebSocket
from scripts.moonrest import MoonRest

_logger = logging.getLogger(__name__)
"""
    QSplashScreen
    Functions ->
        finish()
        message()
        pixmap()
        setPixmap()
        
    Virtual Functions ->
        drawContents()
        
    Slots ->
    
        clearMessage()
        showMessage()

    More Info on ->
        https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QSplashScreen.html#qsplashscreen
    
"""


class MainWindow(QMainWindow):
    # @ Signals
    app_initialize = pyqtSignal(name="app-start-websocket-connection")
    printer_state_signal = pyqtSignal(str, name="printer_state")
    printer_object_list_received_signal = pyqtSignal(list, name="object_list_received")
    printer_object_report_signal = pyqtSignal(list, name="object_report_received")
    gcode_response_report_signal = pyqtSignal(list, name="gcode_response_received")

    call_numpad_signal = pyqtSignal(
        int, str, str, "PyQt_PyObject", QStackedWidget, name="call_numpad"
    )

    call_network_panel = pyqtSignal( name="visibilityChange_networkPanel")
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.objects_subscriptions: dict = {}
        self._moonRest = MoonRest()
        self.ws = MoonWebSocket(self)
        self.mc = MachineControl(self)

        # @ Structures
        self.file_data = Files(parent=self, ws=self.ws)
        self.index_stack = deque(maxlen=4)
        self.printer = Printer(parent=self, ws=self.ws)
        # @ UI Elements
        self.numpad_object = CustomNumpad(self)
        self.numpad_object.hide()
        # @ Panels
        self.start_window = ConnectionWindow(self, self.ws)
        self.installEventFilter(self.start_window)
        self.printPanel = PrintTab(
            self.ui.printTab, self.file_data, self.ws, self.printer
        )
        self.filamentPanel = FilamentTab(self.ui.filamentTab)
        self.controlPanel = ControlTab(self.ui.controlTab, self.ws, self.printer)
        self.utilitiesPanel = UtilitiesTab(self.ui.utilitiesTab)
        self.networkPanel = NetworkControlWindow(self.ui.centralwidget)
        
        
        # @ Slot connections
        self.app_initialize.connect(slot=self.start_websocket_connection)
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
        self.controlPanel.request_back_button_pressed.connect(
            slot=self.global_back_button_pressed
        )
        self.controlPanel.request_change_page.connect(slot=self.global_change_page)
        # * Utilities panel
        self.utilitiesPanel.request_back_button_pressed.connect(
            slot=self.global_back_button_pressed
        )
        self.utilitiesPanel.request_change_page.connect(slot=self.global_change_page)
        # # * Network panel
        # self.networkPanel.request_back_button_pressed.connect(
        #     slot=self.global_back_button_pressed
        # )
        # self.networkPanel.request_change_page.connect(slot=self.global_change_page)

        # * Main page - Top bar Buttons 
        self.ui.extruder_temp_btn.clicked.connect(
            partial(self.global_change_page, 2, 4)
        )
        self.ui.extruder1_temp_bnt.clicked.connect(
            partial(self.global_change_page, 2, 4)
        )
        self.ui.bed_temp_btn.clicked.connect(partial(self.global_change_page, 2, 4))
        self.ui.chamber_temp_btn.clicked.connect(partial(self.global_change_page, 2, 4))
        self.ui.filament_type_1.clicked.connect(partial(self.global_change_page, 1, 1))
        self.ui.filament_type_2.clicked.connect(partial(self.global_change_page, 1, 1))
        ##* Also connect to files list when connection is achieved to imidiatly get the files
        self.ws.connected_signal.connect(slot=self.file_data.request_file_list.emit)
        self.start_window.retry_connection_clicked.connect(slot=self.ws.retry)

        self.start_window.restart_klipper_clicked.connect(
            slot=self.mc.restart_klipper_service
        )
        self.start_window.reboot_clicked.connect(slot=self.mc.machine_restart)

        # If the user changes tab, the indexes of all stacked widgets reset
        self.ui.mainTabWidget.currentChanged.connect(slot=self.reset_tab_indexes)
        self.printer_object_report_signal.connect(self.printer.report_received)
        self.gcode_response_report_signal.connect(self.printer.gcode_response_report)

        self.printer_object_list_received_signal.connect(
            self.printer.object_list_received
        )

        self.printer.extruder_update_signal.connect(self.extruder_temperature_change)
        self.printer.heater_bed_update_signal.connect(
            self.heater_bed_temperature_change
        )


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

        # * Network page visibility and calling, there are two places from which you can call the network page, main page and connectivity page 
        # self.call_network_panel.connect(self.networkPanel.visibilityChange)
        
        self.call_network_panel.connect(self.networkPanel.call_network_panel)
        self.start_window.wifi_clicked.connect(self.call_network_panel.emit)
        self.ui.wifi_signal.clicked.connect(self.call_network_panel.emit)
        
        # @ Force main panel to be displayed on startup
        self.ui.mainTabWidget.setCurrentIndex(0)

        

        
        
    @pyqtSlot(name="activate_manual_tab_change")
    def enable_tab_bar(self) -> None:
        if (
            self.ui.mainTabWidget.isTabEnabled(1)
            and self.ui.mainTabWidget.isTabEnabled(2)
            and self.ui.mainTabWidget.isTabEnabled(3)
            and self.ui.mainTabWidget.isTabEnabled(4)
            and self.ui.top_bar.isEnabled()
        ):
            self.ui.mainTabWidget.setTabEnabled(1, True)
            self.ui.mainTabWidget.setTabEnabled(2, True)
            self.ui.mainTabWidget.setTabEnabled(3, True)
            self.ui.mainTabWidget.setTabEnabled(4, True)
            self.ui.top_bar.setEnabled(True)

    @pyqtSlot(name="block_manual_tab_change")
    def disable_tab_bar(self) -> bool:
        """disable_tab_bar
            Disables the tab bar so to not change the tab.

        Returns:
            bool: True if the TabBar was disabled
        """

        self.ui.mainTabWidget.setTabEnabled(1, False)
        self.ui.mainTabWidget.setTabEnabled(2, False)
        self.ui.mainTabWidget.setTabEnabled(3, False)
        self.ui.mainTabWidget.setTabEnabled(4, False)
        self.ui.top_bar.setEnabled(False)

        return (
            False
            if self.ui.mainTabWidget.isTabEnabled(1)
            and self.ui.mainTabWidget.isTabEnabled(2)
            and self.ui.mainTabWidget.isTabEnabled(3)
            and self.ui.mainTabWidget.isTabEnabled(4)
            and self.ui.top_bar.isEnabled()
            else True
        )

    # def calculate_tab_size(self) -> int:
    #     """calculate_tab_size
    #         For a QTabBar Widget calculates the number of accesible tabs

    #     Returns:
    #         int: The number of tabs
    #     """
    #     # TODO
    #     pass

    def reset_tab_indexes(self):
        """reset_tab_indexes
        Used to garentee all tabs reset to their first page once the user leaves the tab
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
        match self.ui.mainTabWidget.currentIndex():
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
        match self.ui.mainTabWidget.currentIndex():
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
                "Tab index argument is not of type integer, field must be integer."
            )
        if not isinstance(panel_index, int):
            _logger.debug(
                "Panel page index is not of type integet, field must be integer."
            )
        current_page = [
            self.ui.mainTabWidget.currentIndex(),
            self.current_panel_index(),
        ]
        requested_page = [tab_index, panel_index]
        # * Return if user is already on the requested page
        if requested_page == current_page:
            _logger.debug("User already on the requested page.")
            return
        # * Add to the stack of indexes the indexes of current tab and page in tab to later be able to come back to them
        self.index_stack.append(current_page)
        # * Go to the requested tab and page
        self.ui.mainTabWidget.setCurrentIndex(tab_index)
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
        self.ui.mainTabWidget.setCurrentIndex(self.index_stack[-1][0])
        self.set_current_panel_index(
            self.index_stack[-1][1]
        )  # From the same position, use the tab and stacked widget page indexes
        self.index_stack.pop()  # Remove the last position.

        self.printer_object_report_signal.connect(self.printer.report_received)
        self.printer_object_list_received_signal.connect(
            self.printer.object_list_received
        )

        _logger.debug("Sucessfully went back a page.")

    @pyqtSlot(name="start_websocket_connection")
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
        if event.type() == WebSocketMessageReceivedEvent.type():
            if isinstance(event, WebSocketMessageReceivedEvent):
                self.messageReceivedEvent(event)
                return True
            return False

        return super().event(event)
    
   
    def messageReceivedEvent(self, event: WebSocketMessageReceivedEvent) -> None:
        """messageReceivedEvent
            Helper method that handles the event messages received from the websocket

        Args:
            event (WebSocketMessageReceivedEvent): The message event with all its contents

        Raises:
            Exception: When a klippy status change comes from the websocket, tries to send another event
            corresponding to the incoming status. If the QApplication instance is of type None raises an exception
            because the event cannot be sent.
        """
        _response: dict = event.packet
        _method = event.method
        _params = event.params if event.params is not None else None

        if "server.file" in _method:
            file_data_event = ReceivedFileDataEvent(_response, _method, _params)
            try:
                QApplication.sendEvent(self.file_data, file_data_event)
            except Exception as e:
                _logger.error(
                    f"Error emitting event for file related information received from websocket | error message received: {e}"
                )

        elif "error" in _method:
            # ! Here i received an error message from the websocket, but it doesn't mean it's closed the connection
            # ! But it might say that klipper had an error with something and has reported back
            pass
        elif "machine" in _method:
            # * Handle machine related stuff
            pass
        elif "printer.info" in _method:
            # print(_response)
            pass
        elif "printer.print" in _method:
            if "start" in _method and "ok" in _response:
                self.printer_state_signal.emit("printing")
            elif "pause" in _method and "ok" in _response:
                self.printer_state_signal.emit("paused")
            elif "resume" in _method and "ok" in _response:
                self.printer_state_signal.emit("printing")
            elif "cancel" in _method and "ok" in _response:
                self.printer_state_signal.emit("canceled")

        elif "printer.objects" in _method:
            if "list" in _method:
                _object_list: list = _response["objects"]
                self.printer_object_list_received_signal[list].emit(_object_list)

            if "subscribe" in _method:
                _objects_response_list = [_response["status"], _response["eventtime"]]
                self.printer_object_report_signal[list].emit(_objects_response_list)
                # TODO: This
                # ! Don't display chamber temperatures if there is no chamber, should do the
                if not self.printer.has_chamber:
                    self.ui.chamber_temperature_frame.hide()
            if "query" in _method:
                # Comes from querying an object
                if isinstance(_response["status"], dict):
                    _object_report = [_response["status"]]
                    _object_report_keys = _response["status"].items()
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
                if hasattr(events, f"Klippy{_state_call}Event"):
                    _klippy_event_callback = getattr(
                        events, f"Klippy{_state_call}Event"
                    )
                    if callable(_klippy_event_callback):
                        try:
                            event = _klippy_event_callback(
                                data=f"Moonraker reported klippy is {_state_call}"
                            )
                            instance = QApplication.instance()
                            if instance is not None:
                                instance.sendEvent(self, event)
                            else:
                                raise Exception("QApplication.instance is None type.")
                        except Exception as e:
                            _logger.debug(
                                f"Unable to send internal klippy {_state_call} notification: {e}"
                            )
        elif "notify_filelist_changed" in _method:
            self.file_data.request_file_list.emit()
        elif "notify_update_response" in _method:
            # * Handle update manager message about updates
            pass
        elif "notify_service_state_changed" in _method:
            # * Handle service changes, such as klipper or moonraker restart or start, anything like that.
            pass
        elif "notify_gcode_response" in _method:
            # * Handle klipper gcode responses.
            _gcode_reponse = _response["params"]
            self.gcode_response_report_signal.emit(_gcode_reponse)
        elif "notify_history_changed" in _method:
            # * Handle received notification when a file stop printing for whatever reason
            # This is where i receive notifications about the current print progress, such as canceled
            pass
        elif "notify_status_update" in _method:
            # * Handle object subscriptions messages
            _object_report = _response["params"]
            self.printer_object_report_signal[list].emit(_object_report)

    @pyqtSlot(str, str, float, name="extruder_update")
    def extruder_temperature_change(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        # TODO: This needs to be better, this method is a little hardcoded, we need, not to insert the extruder name, but make it dynamic
        if extruder_name == "extruder":
            if field == "temperature":
                # _last_text = self.ui.nozzle_1_temp.text()
                # if not -1 < int(_last_text) - int(new_value)  < 1:
                # self.ui.nozzle_1_temp.setText(f"{str(new_value)} / 0 °C")
                self.ui.actual_temp.setText(f"{new_value:.1f}")

            elif field == "target":
                # TODO: Replace with a new label to update the target temperature
                self.ui.target_temp.setText(f"{new_value:.1f}")
                pass
        if extruder_name == "extruder1":
            if field == "temperature":
                # _last_text = self.ui.nozzle_1_temp.text()
                # if not -1 < int(_last_text) - int(new_value)  < 1:
                # self.ui.nozzle_1_temp.setText(f"{str(new_value)} / 0 °C")
                self.ui.actual_temp_4.setText(f"{new_value:.1f}")

            elif field == "target":
                # TODO: Replace with a new label to update the target temperature
                self.ui.target_temp_4.setText(f"{new_value:.1f}")
                pass

    @pyqtSlot(str, str, float, name="heater_bed_update")
    def heater_bed_temperature_change(
        self, name: str, field: str, new_value: float
    ) -> None:
        if field == "temperature":
            self.ui.actual_temp_2.setText(f"{new_value:.1f}")
        elif field == "target":
            self.ui.target_temp_2.setText(f"{new_value:.1f}")


    def paintEvent(self, a0: QPaintEvent | None) -> None:
        self.updateGeometry()
        return super().paintEvent(a0)
    
    
if __name__ == "__main__":
    app = QApplication([])
    pixmap = QPixmap("Blocks_Screen/media/logoblocks.png")
    splash = QSplashScreen(pixmap)
    # splash.setGeometry(main_window)
    splash.showNormal()
    splash.showMessage("Loading")

    # @ Someone said that .processEvents sometimes crashes the system
    app.processEvents()

    # There is another way i can do this, by passing the .ui file to .py and then use that .py file in my app.
    # I can do this with the command pyuic6 -o <pythonfile>.py -x <uifile>.ui
    # Then i get a .py file from the .ui file
    main_window = MainWindow()
    main_window.show()
    main_window.app_initialize.emit()
    splash.finish(main_window)
    sys.exit(app.exec())
