from collections import deque
from functools import partial
import sys
from PyQt6.QtCore import QEvent, pyqtSignal, pyqtSlot, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt6.QtGui import QDragLeaveEvent, QPixmap


# * System imports
from scripts.moonrakerComm import MoonWebSocket
from scripts.moonrest import MoonRest
from scripts.events import *
from scripts.bo_includes.bo_machine import MachineControl
from scripts.bo_includes.bo_files import *

# * Panels
from panels.connectionWindow import ConnectionWindow
from panels.printTab import PrintTab
from panels.filamentTab import FilamentTab
from panels.controlTab import ControlTab
from panels.utilitiesTab import UtilitiesTab
from panels.connectionWindow import ConnectionWindow


from resources.background_resources_rc import *
from resources.button_resources_rc import *
from resources.main_menu_resources_rc import *
from resources.system_resources_rc import *

from qt_ui.Blocks_Screen_Lemos_ui import Ui_MainWindow

import logging

# My Logger object
logging.basicConfig(
    format="'%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s",
    filename=r"E:\gitHub\Blocks_Screen\logFile.log",
    encoding="utf-8",
    level=logging.DEBUG,
)
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
    QUERY_KLIPPY_TIMEOUT: int = 5000
    # @ Signals
    app_initialize = pyqtSignal(name="app-start-websocket-connection")
    printer_state_signal = pyqtSignal(str, name="printer_state")

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._moonRest = MoonRest()
        self.ws = MoonWebSocket(self)
        self.mc = MachineControl(self)

        # @ Install event filter
        self.installEventFilter(self)

        # @ Timeout
        self.query_klippy_status_timer = QtCore.QTimer()
        self.query_klippy_status_timer.start(self.QUERY_KLIPPY_TIMEOUT)
        self.query_klippy_status_timer.timeout.connect(
            self.ws.query_klippy_status_signal.emit
        )

        # @ Structures
        self.file_data = Files(parent=self, ws=self.ws)
        self.installEventFilter(self.file_data)
        self.index_stack = deque(maxlen=4)
        
        # @ Panels
        self.start_window = ConnectionWindow(self, self.ws)
        self.printPanel = PrintTab(self.ui.printTab, self.file_data, self.ws)
        self.filamentPanel = FilamentTab(self.ui.filamentTab)
        self.controlPanel = ControlTab(self.ui.controlTab)
        self.utilitiesPanel = UtilitiesTab(self.ui.utilitiesTab)
        self.ui.mainTabWidget.setCurrentIndex(0) # Make it so Print panel is the first to be displayed
    
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

    @pyqtSlot(name="start_websocket_connection")
    def start_websocket_connection(self):
        self.ws.start()
        self.ws.try_connection()

    # @pyqtSlot()
    # @pyqtSlot((str))
    # @pyqtSlot(name="websocket_connection_lost")
    # def websocket_connection_lost(self, reason: str):
    #     self.start_window.show_panel(reason)

    def event(self, event: QEvent) -> bool:
        if event.type() == WebSocketMessageReceivedEvent.type():
            self.messageReceivedEvent(event)
            return True
        return super().event(event)

    def messageReceivedEvent(self, event):
        _response: dict = event.packet
        _method = event.method
        _params = event.params if event.params is not None else None

        if "server.file" in _method:
            # * Handle file related stuff
            file_data_event = ReceivedFileDataEvent(_response, _method, _params)
            try:
                QtCore.QCoreApplication.instance().sendEvent(
                    self.file_data, file_data_event
                )
            except Exception as e:
                _logger.error(
                    f"Error emitting event for file related information received from websocket"
                )
        elif "machine" in _method:
            # * Handle machine related stuff
            pass
        elif "printer.print" in _method:
            # * Hangle print related stuff
            # Can have state variables here, like the printer is currently printing, or stopped or anything
            if "start" in _method and "ok" in _response:
                self.printer_state_signal.emit("printing")
            elif "pause" in _method and "ok" in _response:
                self.printer_state_signal.emit("paused")
            elif "resume" in _method and "ok" in _response:
                self.printer_state_signal.emit("printing")
            elif "cancel" in _method and "ok" in _response:
                self.printer_state_signal.emit("canceled")

        elif "printer.objects" in _method:
            # * Handle printer objects related stuff
            pass

        elif "notify_klippy_ready" in _method:
            # * Handle klipper ready notification
            # TODO Maybe this will error, because i subclass QEvent, but it's not of type qevent but a subclass of it so it's also a qevent
            try:
                kp_ready = KlippyReadyEvent(data="Moonraker reported klippy is ready")
                QtCore.QCoreApplication.instance().customEvent(kp_ready)
            except Exception as e:
                _logger.debug(f"Unable to send internal klippy ready notification: {e}")
        elif "notify_klippy_shutdown" in _method:
            # * Handle klipper shutdown notification
            try:
                kp_shutdown = KlippyShudownEvent(
                    data="Moonraker reported klippy shutdown"
                )
                QtCore.QCoreApplication.instance().customEvent(kp_shutdown)
            except:
                _logger.debug(f"Unable to send internal klippy shutdown signal: {e}")
        elif "notify_klippy_disconnected" in _method:
            # * Handle klippy disconnected event
            try:
                kp_disconnected = KlippyDisconnectedEvent(
                    data="Websocket reported klippy disconnection"
                )
                # TODO: Check if it's better to implicitly specify where the signal goes
                QtCore.QCoreApplication.instance().customEvent(kp_disconnected)
            except Exception as e:
                _logger.debug(
                    f"Unable to send internal klippy disconnected signal: {e}"
                )
        elif "notify_filelist_changed" in _method:
            # * Handle filelist changed notification
            # * Notification called when user uploads, deletes or moves a
            # * file or directory

            # * Send to files a request to update all files
            self.file_data.request_file_list.emit()

        elif "notify_update_response" in _method:
            # * Handle update manager message about updates
            pass
        elif "notify_service_state_changed" in _method:
            # * Handle service changes like klipper service just started or any other than moonraker
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
            pass
        # TODO: Guess today is the day i handle the object subscriptions


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


""" 
    MECANISMO NR 1
    
        Eventos -> ser rapidos ou ter um queue 

            rapidos -> sendEvent(local, event)
            queue -> postEvent()


        Podem ser vistos em qualquer parte do programa ou podem ser explicitamente transmitidos
        para uma classe.
        
        
        Qualquer classe que seja um "child" de uma outra do QT
        
            def event(self, event):         Sempre chamada quando existe um event 
                <qualquer coisa>
        
    MECANISMO NR 2 
    
        SINALS & SLOTS 
    
        
"""
