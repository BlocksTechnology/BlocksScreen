import typing

import PyQt6
import PyQt6.QtCore
import PyQt6.QtWidgets
import lib.ui.probeHelperPage_ui as probeHelperUI
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, pyqtSlot


class ProbeHelper(PyQt6.QtWidgets.QWidget, probeHelperUI.Ui_probe_offset_page):
    request_back: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = pyqtSignal(
        name="request_back"
    )
    run_gcode_signal: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = pyqtSignal(
        str, name="run_gcode"
    )

    def __init__(self, parent: QtWidgets.QWidget | None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self._zhop_value: float = 0.0
        self.helper_start: bool = False
        self.move_001.toggled.connect(lambda: self.handle_zhop_change(new_value=0.01))
        self.move_0025.toggled.connect(lambda: self.handle_zhop_change(new_value=0.025))
        self.move_005.toggled.connect(lambda: self.handle_zhop_change(new_value=0.005))
        self.move_01.toggled.connect(lambda: self.handle_zhop_change(new_value=0.1))
        self.move_1.toggled.connect(lambda: self.handle_zhop_change(new_value=1.0))
        
        
        
        self.mb_raise_nozzle.clicked.connect(
            lambda: self.run_gcode_signal.emit(f"TESTZ Z={self._zhop_value}\nM400")
        )
        self.mb_lower_nozzle.clicked.connect(
            lambda: self.run_gcode_signal.emit(f"TESTZ Z=-{self._zhop_value}\nM400")
        )
        self.accept_button.clicked.connect(
            lambda: self.run_gcode_signal.emit("Z_OFFSET_APPLY_PROBE\nM400")
        )
        self.abort_button.clicked.connect(lambda: self.run_gcode_signal.emit("ABORT"))
        # self.start_probe_helper_button.clicked.connect(
        #     lambda: self.run_gcode_signal.emit("PROBE_CABLIBRATE\nM400")
        #     and (self.start_probe_helper_button.disable())
        # )
        self.hide()

    @pyqtSlot(float, name="handle_zhop_change")
    def handle_zhop_change(self, new_value: float) -> None:
        if new_value == self._zhop_value:
            return
        self._zhop_value = new_value

    @pyqtSlot(float, name="handle_old_z_offset")
    def handle_old_z_offset(self, offset: float):
        self.old_offset_info.setText(str(offset) + "mm")

    @pyqtSlot(float, name="")
    def handle_received_current_z_offset(self, offset: float):
        self.current_offset_icon.setText(str(offset) + "mm")

    def show(self) -> None:
        return super().show()
