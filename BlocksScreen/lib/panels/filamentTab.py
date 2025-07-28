import enum
import typing
from functools import partial


from lib.printer import Printer
from lib.filament import Filament
from lib.ui.filamentStackedWidget_ui import Ui_filamentStackedWidget
from PyQt6.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPaintEngine, QPaintEvent, QResizeEvent
from PyQt6.QtWidgets import QStackedWidget, QWidget


class FilamentTab(QStackedWidget):
    request_filament_change_page = pyqtSignal(name="filament_change_page")
    request_filament_load = pyqtSignal(name="filament_load_t1")
    request_back = pyqtSignal(name="request_back")
    request_change_page = pyqtSignal(int, int, name="request_change_page")
    request_toolhead_count = pyqtSignal(int, name="toolhead_number_received")
    run_gcode = pyqtSignal(str, name="run_gcode")

    class FilamentTypes(enum.Enum):
        PLA = Filament(name="PLA", temperature=220)

    class FilamentStates(enum.Enum):
        LOADED = enum.auto()
        UNLOADED = enum.auto()
        UNKNOWN = -1

        def __repr__(self) -> str:
            return "<%s.%s>" % (self.__class__.__name__, self._name_)

    def __init__(self, parent: QWidget, printer: Printer, ws, /) -> None:
        super().__init__(parent)

        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)

        self.ws = ws
        self.printer = printer
        self.toolhead_count: int = 0

        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type: Filament | None = None

        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(
            self.back_button
        )
        # REFACTOR self.panel.load_custom_btn.clicked.connect(partial(self.change_page, 2))
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)

        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=220)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=240)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=250)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=250)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=270)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, temp=230)
        )

        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.run_gcode.connect(self.ws.api.run_gcode)

    @pyqtSlot(int, int, name="load_filament")
    def load_filament(self, toolhead: int = 0, temp: int = 220) -> None:
        # if not self.has_load_unload_objects:
        #     return  # {"error": "No load/unload routines"}
        # if not self._filament_state == self.FilamentStates.UNLOADED:
        #     return  # {"error": "Filament already loaded"}
        # if toolhead == 0:
        #     self.run_gcode.emit(f"LOAD_FILAMENT TEMPERATURE={temp}")
        # else:
        self.run_gcode.emit(
            f"LOAD_FILAMENT TOOLHEAD=load_toolhead TEMPERATURE={temp}"
        )

    @pyqtSlot(str, int, name="unload_filament")
    def unload_filament(self, toolhead: str = "0", temp: int = 220) -> None:
        # if not self.has_load_unload_objects:
        #     return  # {"error": "No load/unload routines"}
        # if not self._filament_state == self.FilamentStates.LOADED:
        #     return  # {"error": "No loaded filament"}

        # self.find_routine_objects()
        if toolhead == 0:
            self.run_gcode.emit(f"UNLOAD_FILAMENT TEMPERATURE={temp}")
        else:
            self.run_gcode.emit(
                f"UNLOAD_FILAMENT TOOLHEAD={toolhead} TEMPERATURE={temp}"
            )

    @property
    def filament_state(self):
        return self._filament_state

    def change_page(self, index):
        self.request_change_page.emit(1, index)

    def back_button(self):
        self.request_back.emit()

    def sizeHint(self) -> QSize:
        return super().sizeHint()

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        if self.panel.load_page.isVisible() and self.toolhead_count == 1:
            self.panel.load_header_page_title.setText("Load Toolhead")
        if a0 is not None:
            return super().paintEvent(a0)

    def removeWidget(self, w: QWidget | None) -> None:
        if w is not None:
            return super().removeWidget(w)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        if a0 is not None:
            return super().resizeEvent(a0)

    def find_routine_objects(self):
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False
