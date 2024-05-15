from collections import deque
from functools import partial
import sys
from PyQt6.QtCore import QEvent, pyqtSignal, pyqtSlot, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt6.QtGui import QDragLeaveEvent, QPixmap

# * System imports
from scripts import events
from scripts.moonrakerComm import MoonWebSocket
from scripts.moonrest import MoonRest
from scripts.events import *
from scripts.bo_includes.bo_machine import MachineControl
from scripts.bo_includes.bo_files import *
from scripts.bo_includes.bo_printer import *

# * Panels
from panels.connectionWindow import ConnectionWindow
from panels.printTab import PrintTab
from panels.filamentTab import FilamentTab
from panels.controlTab import ControlTab
from panels.utilitiesTab import UtilitiesTab

# * Resources
from resources.background_resources_rc import *
from resources.button_resources_rc import *
from resources.main_menu_resources_rc import *
from resources.system_resources_rc import *

# * UI
from qt_ui.Blocks_Screen_Lemos_ui import Ui_MainWindow


import logging

# My Logger object
# logging.basicConfig(
#     format="'%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s",
#     filename=r"E:\gitHub\Blocks_Screen\logFile1.log",
#     encoding="utf-8",
#     level=logging.DEBUG,
# )
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

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.objects_subscriptions: dict = {}
        self._moonRest = MoonRest()
        self.ws = MoonWebSocket(self)
        self.mc = MachineControl(self)
        # @ Force main panel to be displayed on startup
        self.ui.mainTabWidget.setCurrentIndex(0)
        # @ Install event filter

        # @ Structures
        self.file_data = Files(parent=self, ws=self.ws)
        self.index_stack = deque(maxlen=4)        
        self.printer = Printer(parent=self,ws= self.ws)
        # @ Panels
        self.start_window = ConnectionWindow(self, self.ws)
        self.installEventFilter(self.start_window)
        self.printPanel = PrintTab(self.ui.printTab, self.file_data, self.ws, self.printer)
        self.filamentPanel = FilamentTab(self.ui.filamentTab)
        self.controlPanel= ControlTab(self.ui.controlTab, self.ws, self.printer)
        self.utilitiesPanel = UtilitiesTab(self.ui.utilitiesTab)
        # @ Slot connections
        self.app_initialize.connect(slot=self.start_websocket_connection)

        self.ws.connecting_signal.connect(slot=self.start_window.websocket_connecting)
        self.ws.connected_signal.connect(
            slot=self.start_window.websocket_connection_achieved
        )
        self.ws.connection_lost.connect(
            slot=self.start_window.websocket_connection_lost
        )
        self.printPanel.request_back_button_pressed.connect(slot=self.global_back_button_pressed)
        self.printPanel.request_change_page.connect(slot=self.global_change_page)
        self.filamentPanel.request_back_button_pressed.connect(slot=self.global_back_button_pressed)
        self.filamentPanel.request_change_page.connect(slot=self.global_change_page)
        self.controlPanel.request_back_button_pressed.connect(slot=self.global_back_button_pressed)
        self.controlPanel.request_change_page.connect(slot=self.global_change_page) 
        self.utilitiesPanel.request_back_button_pressed.connect(slot=self.global_back_button_pressed)
        self.utilitiesPanel.request_change_page.connect(slot=self.global_change_page)
        # All the buttons on the top bar that send the user to the Temperature page
        self.ui.nozzle_1_temp.clicked.connect(partial(self.global_change_page, 2, 4))
        self.ui.nozzle_2_temp.clicked.connect(partial(self.global_change_page, 2, 4))
        self.ui.hot_bed_temp.clicked.connect(partial(self.global_change_page, 2, 4))
        self.ui.chamber_temp.clicked.connect(partial(self.global_change_page, 2, 4))
        # # All the buttons on the top bar that send the user to the Load page
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
        self.printer_object_list_received_signal.connect(
            self.printer.object_list_received
        )

        self.printer.extruder_update_signal.connect(self.extruder_temperature_change)
        self.printer.heater_bed_update_signal.connect(
            self.heater_bed_temperature_change
        )

    # Used to garantee all tabs reset to their first page once the user leaves the tab
    def reset_tab_indexes(self):
        self.printPanel.setCurrentIndex(0)
        self.filamentPanel.setCurrentIndex(0)
        self.controlPanel.setCurrentIndex(0)
        self.utilitiesPanel.setCurrentIndex(0)
    
    # Helper function to get the index of the current page in the current tab  
    def current_panel_index(self):
        match self.ui.mainTabWidget.currentIndex():
            case 0:
                return self.printPanel.currentIndex()
            case 1:
                return self.filamentPanel.currentIndex()
            case 2:
                return self.controlPanel.currentIndex()
            case 3:
                return self.utilitiesPanel.currentIndex()

    # Helper function to set the index of the current page in the current tab  
    def set_current_panel_index(self, panel_index):
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
    def global_change_page(self, tab_index, panel_index):
        current_page = [self.ui.mainTabWidget.currentIndex(), self.current_panel_index()]
        requested_page = [tab_index, panel_index]
        
        # Return if user is already on the requested page
        if (requested_page == current_page):
            return
        
        # Add to the stack of indexes the indexes of current tab and page in tab to later be able to come back to them
        self.index_stack.append(current_page)
        # Go to the requested tab and page
        self.ui.mainTabWidget.setCurrentIndex(tab_index)
        self.set_current_panel_index(panel_index)
        # print("Requesting Tab ", tab_index, " and page index: ", panel_index)   
                
    @pyqtSlot(name="request_back_button_pressed")
    def global_back_button_pressed(self):
        # Just a safety measure to avoid accessing an inexistant position of the index_stack
        if (not len(self.index_stack)):
            return
        # From the last position of the stack use the first value of its tuple, tab index
        self.ui.mainTabWidget.setCurrentIndex(self.index_stack[-1][0])                 
        self.set_current_panel_index(self.index_stack[-1][1])  # From the same position, use the tab and stacked widget page indexes
        #print(self.index_stack)                                                         
        self.index_stack.pop() # Remove the last position.

        self.printer_object_report_signal.connect(self.printer.report_received)
        self.printer_object_list_received_signal.connect(
            self.printer.object_list_received
        )

        self.printer.extruder_update_signal.connect(self.extruder_temperature_change)
        self.printer.heater_bed_update_signal.connect(
            self.heater_bed_temperature_change
        )
        # self.printer.idle_timeout_update_signal.connect(self.idle_timeout_update)

    @pyqtSlot(name="start_websocket_connection")
    def start_websocket_connection(self):
        self.ws.start()
        self.ws.try_connection()

    def event(self, event: QEvent) -> bool:
        if event.type() == WebSocketMessageReceivedEvent.type():
            if isinstance(event, WebSocketMessageReceivedEvent):
                self.messageReceivedEvent(event)
                return True
            return False
        # if event.type() == KlippyReadyEvent.type():
        #     print("Received event ready type ")
        return super().event(event)

    def messageReceivedEvent(self, event: WebSocketMessageReceivedEvent):
        _response: dict = event.packet
        _method = event.method
        _params = event.params if event.params is not None else None

        if "server.file" in _method:
            file_data_event = ReceivedFileDataEvent(_response, _method, _params)
            try:
                QApplication.sendEvent(self.file_data, file_data_event)
            except Exception as e:
                _logger.error(
                    f"Error emitting event for file related information received from websocket"
                )
        elif "machine" in _method:
            # * Handle machine related stuff
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

        elif "notify_klippy" in _method:
            _split = _method.split("_")
            if len(_split) > 2:
                _state_upper = _split[2].upper()
                _state_call = f"{_state_upper}{_split[2][1:]}"
                _logger.debug(
                    f"Notify_klippy {_state_call} Received from object subscription."
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
                            QApplication.instance().sendEvent(self, event)
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
            # * Handle service changes like klipper service just started or any other than moonraker
            # watch for klipper service and moonraker service in here and any other service that
            # we might need for controling our software.
            # Îf any of them fails make the app respond to it

            pass
        elif "notify_gcode_response" in _method:
            # * Handle klipper gcode responses.
            # When the printer stop ptinting and there is a need to restart the firmware or restart klipper i
            # get a message here, can be messages such as mcu lost ocnnection or thermocouple reader fault
            # Or MCU shutdown or anything like that
            # Can even receive a klipper shudown message here
            # THese are all messages that require for the connection panel to show up
            # Because i'll always need to restart klipper and other functionalities are disabled except the wifi shit
            # This field will receive alot of print updates, such as "Must home axis first"
            pass
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
    ):
        if field == "temperature":
            # _last_text = self.ui.nozzle_1_temp.text()
            # if not -1 < int(_last_text) - int(new_value)  < 1:
            # self.ui.nozzle_1_temp.setText(f"{str(new_value)} / 0 °C")
            self.ui.nozzle_1_temp.setText(f"{str(new_value)}")

        elif field == "target":
            # TODO: Replace with a new label to update the target temperature
            pass

    @pyqtSlot(str, str, float, name="heater_bed_update")
    def heater_bed_temperature_change(self, name: str, field: str, new_value: float):
        self.ui.hot_bed_temp.setText(str(new_value))


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
