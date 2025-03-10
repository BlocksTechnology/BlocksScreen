import logging 

from PyQt6.QtCore import QEvent, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QFrame 
import PyQt6.QtGui as QtGui
from lib.moonrakerComm import MoonWebSocket
from lib.ui.filamentSensorsPage_ui import Ui_filament_sensors_page

# TODO: Add buttons that toggle on and of the available printer sensors 
class SensorsWindow(QFrame): 
    
    def __init__(self, parent, ws: MoonWebSocket, *args, **kwargs): 
        super(SensorsWindow, self).__init__(parent, *args, **kwargs)

        self.parent_window = parent
        self.panel = Ui_filament_sensors_page()
        self.panel.setupUi(self)
        
        self.ws = ws 

        self.setGeometry(self.frameRect())
        self.setEnabled(False)

        
        
        
        logging.info("[SensorWindow] Initialized")

    
    
    def add_sensor_row(self, name) -> None: 
        self.sensor_widget = self.
        self.panel.fs_content_layout.addChildWidget(_sensor_row)