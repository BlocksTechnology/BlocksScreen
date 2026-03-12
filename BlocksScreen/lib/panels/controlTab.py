from __future__ import annotations

import re
import typing

from lib.moonrakerComm import MoonWebSocket
from lib.panels.widgets.numpadPage import CustomNumpad
from lib.panels.widgets.slider_selector_page import SliderPage

from lib.panels.widgets.printcorePage import SwapPrintcorePage
from lib.panels.widgets.probeHelperPage import ProbeHelper
from lib.panels.widgets.fansPage import FansPage
from lib.panels.widgets.axisPage import AxisPage
from lib.panels.widgets.extruderPage import ExtruderPage
from lib.panels.widgets.temperaturePage import TemperaturePage

from lib.printer import Printer

from PyQt6 import QtCore, QtGui, QtWidgets
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.icon_button import IconButton


class ControlTab(QtWidgets.QStackedWidget):
    """Printer Control Stacked Widget"""

    request_back_button = QtCore.pyqtSignal(name="request-back-button")
    request_change_page = QtCore.pyqtSignal(int, int, name="request-change-page")
    request_numpad_signal = QtCore.pyqtSignal(
        int,
        str,
        str,
        "PyQt_PyObject",
        QtWidgets.QStackedWidget,
        name="request-numpad",
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    disable_popups: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="disable-popups"
    )
    request_numpad: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str, int, "PyQt_PyObject"],
        [str, int, "PyQt_PyObject", int, int],
        name="request-numpad",
    )
    request_file_info: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request-file-info"
    )
    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")
    toggle_conn_page = QtCore.pyqtSignal(bool, name="call-load-panel")

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        ws: MoonWebSocket,
        printer: Printer,
        /,
    ) -> None:
        super().__init__(parent)
        self.setupUi()

        self.back_button.clicked.connect(lambda: self._button_change(False))
        self.ws: MoonWebSocket = ws
        self.printer: Printer = printer
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.timers = []
        self.ztilt_state = False

        self.probe_helper_page = ProbeHelper(self)
        self.addWidget(self.probe_helper_page)
        self.probe_helper_page.toggle_conn_page.connect(self.toggle_conn_page)
        self.probe_helper_page.disable_popups.connect(self.disable_popups)
        self.probe_helper_page.call_load_panel.connect(self.call_load_panel)

        self.printcores_page = SwapPrintcorePage(self)
        self.addWidget(self.printcores_page)

        self.fans_page = FansPage(self)
        self.addWidget(self.fans_page)
        self.fans_page.request_back_button.connect(self.request_back_button)
        self.fans_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.fans_page.request_slider_page.connect(self.on_slidePage_request)

        self.sliderPage = SliderPage(self)
        self.addWidget(self.sliderPage)
        self.sliderPage.request_back.connect(self.request_back_button)

        self.axis_page = AxisPage(self)
        self.addWidget(self.axis_page)
        self.axis_page.request_back.connect(self.request_back_button)

        self.extruder_page = ExtruderPage(self, printer)
        self.addWidget(self.extruder_page)
        self.extruder_page.request_back.connect(self.request_back_button)

        self.temperature_page = TemperaturePage(self)
        self.addWidget(self.temperature_page)
        self.temperature_page.request_back.connect(self.request_back_button)
        self.temperature_page.request_numpad.connect(self.on_numpad_request)
        self.temperature_page.run_gcode_signal.connect(self.run_gcode_signal)

        self.numpadPage = CustomNumpad(self)
        self.numpadPage.request_back.connect(self.request_back_button)
        self.addWidget(self.numpadPage)

        self.probe_helper_page.request_page_view.connect(
            lambda: self.change_page(self.indexOf(self.probe_helper_page))
        )
        self.probe_helper_page.query_printer_object.connect(self.ws.api.object_query)
        self.probe_helper_page.run_gcode_signal.connect(self.ws.api.run_gcode)
        self.probe_helper_page.request_back.connect(self.request_back_button)
        self.printer.print_stats_update[str, str].connect(
            self.probe_helper_page.on_print_stats_update
        )
        self.printer.print_stats_update[str, dict].connect(
            self.probe_helper_page.on_print_stats_update
        )
        self.printer.print_stats_update[str, float].connect(
            self.probe_helper_page.on_print_stats_update
        )
        self.printer.available_gcode_cmds.connect(
            self.probe_helper_page.on_available_gcode_cmds
        )
        self.probe_helper_page.subscribe_config[str, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )
        self.probe_helper_page.subscribe_config[list, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )
        self.printer.extruder_update.connect(self.probe_helper_page.on_extruder_update)
        self.printer.gcode_move_update.connect(
            self.probe_helper_page.on_gcode_move_update
        )
        self.printer.manual_probe_update.connect(
            self.probe_helper_page.on_manual_probe_update
        )
        self.printer.printer_config.connect(self.probe_helper_page.on_printer_config)
        self.printer.gcode_response.connect(
            self.probe_helper_page.handle_gcode_response
        )
        self.printer.extruder_update.connect(self.temperature_page.on_extruder_update)
        self.printer.heater_bed_update.connect(
            self.temperature_page.on_heater_bed_update
        )

        self.run_gcode_signal.connect(self.ws.api.run_gcode)
        # # @ object temperature change clicked
        self.printcores_page.pc_accept.clicked.connect(self.handle_swapcore)

        self.ws.klippy_state_signal.connect(self.on_klippy_status)
        self.ws.klippy_state_signal.connect(self.probe_helper_page.on_klippy_status)
        self.printer.on_printcore_update.connect(self.handle_printcoreupdate)
        self.printer.gcode_response.connect(self._handle_gcode_response)
        self.printer.z_tilt_update.connect(self._handle_z_tilt_object_update)

        self.cp_button_6.hide()

        self.printer.fan_update[str, str, float].connect(
            self.fans_page.on_fan_object_update
        )
        self.printer.fan_update[str, str, int].connect(
            self.fans_page.on_fan_object_update
        )
        self._button_change(False)

    def _button_change(self, active: bool):
        for btn in [
            self.cp_button_1,
            self.cp_button_2,
            self.cp_button_3,
            self.cp_button_4,
            self.cp_button_5,
            self.cp_button_6,
        ]:
            try:
                btn.clicked.disconnect()
            except TypeError:
                pass
        if active:
            self.cp_header_title.setText("Montion")
            self.cp_button_1.setText("Auto Home")

            self.cp_button_1.setPixmap(
                QtGui.QPixmap(":/motion/media/btn_icons/home_all.svg")
            )
            self.cp_button_1.clicked.connect(
                lambda: self.run_gcode_signal.emit("G28\nM400")
            )
            self.cp_button_2.setText("Disable\nSteppers")
            self.cp_button_2.clicked.connect(
                lambda: self.run_gcode_signal.emit("M84\nM400")
            )
            self.cp_button_2.setPixmap(
                QtGui.QPixmap(":/motion/media/btn_icons/disable_steppers.svg")
            )
            self.cp_button_3.setText("Axis")
            self.cp_button_3.clicked.connect(
                lambda: self.change_page(self.indexOf(self.axis_page))
            )
            self.cp_button_3.setPixmap(
                QtGui.QPixmap(":/motion/media/btn_icons/axis_maintenance.svg")
            )
            self.cp_button_4.setText("Extruder")
            self.cp_button_4.setPixmap(
                QtGui.QPixmap(":/extruder_related/media/btn_icons/extrude.svg")
            )
            self.cp_button_4.clicked.connect(
                lambda: self.change_page(self.indexOf(self.extruder_page))
            )

            self.back_button.show()
            self.Hblank.show()

            self.cp_content_layout.addWidget(self.blank)
            self.cp_button_5.hide()
        else:
            self.cp_header_title.setText("Control")

            self.cp_button_1.setText("Motion\nControl")
            self.cp_button_1.setPixmap(
                QtGui.QPixmap(":/motion/media/btn_icons/axis_maintenance.svg")
            )
            self.cp_button_1.clicked.connect(lambda: self._button_change(True))

            self.cp_button_2.setText("Temp.\nControl")
            self.cp_button_2.setPixmap(
                QtGui.QPixmap(":/temperature_related/media/btn_icons/temperature.svg")
            )
            self.cp_button_2.clicked.connect(
                lambda: self.change_page(self.indexOf(self.temperature_page))
            )

            self.cp_button_3.setText("Nozzle\nCalibration")
            self.cp_button_3.setPixmap(
                QtGui.QPixmap(":/z_levelling/media/btn_icons/bed_levelling.svg")
            )
            self.cp_button_3.clicked.connect(
                lambda: self.change_page(self.indexOf(self.probe_helper_page))
            )

            self.cp_button_4.setText("Z-Tilt")
            self.cp_button_4.setPixmap(
                QtGui.QPixmap(":/z_levelling/media/btn_icons/bed_levelling.svg")
            )
            self.cp_button_4.clicked.connect(lambda: self.handle_ztilt())

            self.cp_button_5.setText("Fans")
            self.cp_button_5.setPixmap(
                QtGui.QPixmap(":/temperature_related/media/btn_icons/fan.svg")
            )
            self.cp_button_5.clicked.connect(
                lambda: self.change_page(self.indexOf(self.fans_page))
            )

            self.cp_button_6.clicked.connect(self.show_swapcore)

            self.back_button.hide()
            self.Hblank.hide()
            self.cp_content_layout.removeWidget(self.blank)
            self.cp_button_5.show()
            self.retranslateUi()

    def _handle_z_tilt_object_update(self, value, state):
        if state:
            self.call_load_panel.emit(False, "")

    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", name="on_slidePage_request")
    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", int, int, name="on_slidePage_request")
    def on_slidePage_request(
        self,
        name: str,
        current_value: int,
        callback,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        try:
            self.sliderPage.value_selected.disconnect()
        except:
            pass
        self.sliderPage.value_selected.connect(callback)
        self.sliderPage.set_name(name)
        self.sliderPage.set_slider_position(int(current_value))
        self.sliderPage.set_slider_minimum(min_value)
        self.sliderPage.set_slider_maximum(max_value)
        self.change_page(self.indexOf(self.sliderPage))

    def handle_printcoreupdate(self, value: dict):
        if value["swapping"] == "idle":
            return

        if value["swapping"] == "in_pos":
            self.call_load_panel.emit(False, "")
            self.printcores_page.show()
            self.disable_popups.emit(True)
            self.printcores_page.setText(
                "Please Insert Print Core \n \n Afterwards click continue"
            )
        if value["swapping"] == "unloading":
            self.call_load_panel.emit(True, "Unloading print core")
        if value["swapping"] == "cleaning":
            self.call_load_panel.emit(True, "Cleaning print core")

    def _handle_gcode_response(self, messages: list):
        """Handle gcode response for Z-tilt adjustment"""
        pattern = r"Retries:\s*(\d+)/(\d+).*?range:\s*([\d.]+)\s*tolerance:\s*([\d.]+)"

        for msg_list in messages:
            if not msg_list:
                continue

            if (
                "Retries:" in msg_list
                and "range:" in msg_list
                and "tolerance:" in msg_list
            ):
                match = re.search(pattern, msg_list)

                if match:
                    retries_done = int(match.group(1))
                    retries_total = int(match.group(2))
                    probed_range = float(match.group(3))
                    tolerance = float(match.group(4))
                    if retries_done == retries_total:
                        self.call_load_panel.emit(False, "")
                        return
                    self.call_load_panel.emit(
                        True,
                        f"Retries: {retries_done}/{retries_total} | Range: {probed_range:.6f} | Tolerance: {tolerance:.6f}",
                    )

    def handle_ztilt(self):
        """Handle Z-Tilt Adjustment"""
        self.call_load_panel.emit(True, "Please wait, performing Z-axis calibration.")
        self.run_gcode_signal.emit("G28\nM400")
        self.run_gcode_signal.emit("Z_TILT_ADJUST")

    @QtCore.pyqtSlot(str, name="on-klippy-status")
    def on_klippy_status(self, state: str):
        """Handles incoming klippy status changes"""
        if state.lower() == "ready":
            self.printcores_page.hide()
            self.disable_popups.emit(False)
            return
        if state.lower() == "startup":
            self.printcores_page.setText("Almost done \n be patient")
            return

    def show_swapcore(self):
        """Show swap printcore"""
        self.run_gcode_signal.emit("CHANGE_PRINTCORES")
        self.call_load_panel.emit(True, "Preparing to swap print core")

    def handle_swapcore(self):
        """Handle swap printcore routine finish"""
        self.printcores_page.setText("Executing \n Firmware Restart")
        self.run_gcode_signal.emit("FIRMWARE_RESTART")

    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", name="on-numpad-request")
    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", int, int, name="on-numpad-request")
    def on_numpad_request(
        self,
        name: str,
        current_value: int,
        callback,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        """Handles numpad widget request"""
        self.numpadPage.value_selected.connect(callback)
        self.numpadPage.set_name(name)
        self.numpadPage.set_value(current_value)
        self.numpadPage.set_min_value(min_value)
        self.numpadPage.set_max_value(max_value)
        self.change_page(self.indexOf(self.numpadPage))

    def change_page(self, index):
        """Handles changing page"""
        self.request_change_page.emit(2, index)

    def setupUi(self):
        self.resize(710, 410)
        self.blank = QtWidgets.QWidget()
        self.blank.setMinimumSize(QtCore.QSize(250, 80))
        self.blank.setMaximumSize(QtCore.QSize(250, 80))

        self.Hblank = QtWidgets.QWidget(parent=self)
        self.Hblank.setMinimumSize(QtCore.QSize(60, 60))
        self.Hblank.setMaximumSize(QtCore.QSize(60, 60))

        widget = QtWidgets.QWidget()
        widget.setMinimumSize(QtCore.QSize(710, 410))
        widget.setMaximumSize(QtCore.QSize(710, 410))
        self.setObjectName("control_page")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.cp_header_layout = QtWidgets.QHBoxLayout()
        self.cp_header_layout.setObjectName("cp_header_layout")

        self.cp_header_layout.addWidget(self.Hblank)
        self.cp_header_title = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cp_header_title.sizePolicy().hasHeightForWidth()
        )
        self.cp_header_title.setSizePolicy(sizePolicy)
        self.cp_header_title.setMinimumSize(QtCore.QSize(300, 60))
        self.cp_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.cp_header_title.setFont(font)
        self.cp_header_title.setStyleSheet("background: transparent; color: white;")
        self.cp_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cp_header_title.setObjectName("cp_header_title")
        self.cp_header_layout.addWidget(self.cp_header_title)

        self.back_button = IconButton(parent=self)
        self.back_button.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.cp_header_layout.addWidget(self.back_button)

        self.verticalLayout.addLayout(self.cp_header_layout)
        self.cp_content_layout = QtWidgets.QGridLayout()
        self.cp_content_layout.setObjectName("cp_content_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        self.cp_button_1 = BlocksCustomButton(parent=self)
        self.cp_button_1.setSizePolicy(sizePolicy)
        self.cp_button_1.setMinimumSize(QtCore.QSize(250, 80))
        self.cp_button_1.setMaximumSize(QtCore.QSize(250, 80))
        self.cp_button_1.setFont(font)
        self.cp_button_1.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.cp_button_1.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.cp_button_1.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/motion/media/btn_icons/axis_maintenance.svg"),
        )
        self.cp_button_1.setObjectName("cp_button_1")

        self.cp_content_layout.addWidget(self.cp_button_1, 0, 0, 1, 1)

        self.cp_button_2 = BlocksCustomButton(parent=self)
        self.cp_button_2.setSizePolicy(sizePolicy)
        self.cp_button_2.setMinimumSize(QtCore.QSize(10, 80))
        self.cp_button_2.setMaximumSize(QtCore.QSize(250, 80))
        self.cp_button_2.setFont(font)
        self.cp_button_2.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.cp_button_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.cp_button_2.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/temperature_related/media/btn_icons/temperature.svg"),
        )
        self.cp_button_2.setObjectName("cp_button_2")

        self.cp_content_layout.addWidget(self.cp_button_2, 0, 1, 1, 1)

        self.cp_button_3 = BlocksCustomButton(parent=self)
        self.cp_button_3.setSizePolicy(sizePolicy)
        self.cp_button_3.setMinimumSize(QtCore.QSize(10, 80))
        self.cp_button_3.setMaximumSize(QtCore.QSize(250, 80))
        self.cp_button_3.setFont(font)
        self.cp_button_3.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.cp_button_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.cp_button_3.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/z_levelling/media/btn_icons/bed_levelling.svg"),
        )
        self.cp_button_3.setObjectName("cp_button_3")

        self.cp_content_layout.addWidget(self.cp_button_3, 1, 0, 1, 1)

        self.cp_button_4 = BlocksCustomButton(parent=self)
        self.cp_button_4.setSizePolicy(sizePolicy)
        self.cp_button_4.setMinimumSize(QtCore.QSize(10, 80))
        self.cp_button_4.setMaximumSize(QtCore.QSize(250, 80))
        self.cp_button_4.setFont(font)
        self.cp_button_4.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.cp_button_4.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.cp_button_4.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/z_levelling/media/btn_icons/bed_levelling.svg"),
        )
        self.cp_button_4.setObjectName("cp_button_4")

        self.cp_content_layout.addWidget(self.cp_button_4, 1, 1, 1, 1)

        self.cp_button_5 = BlocksCustomButton(parent=self)
        self.cp_button_5.setSizePolicy(sizePolicy)
        self.cp_button_5.setMinimumSize(QtCore.QSize(10, 80))
        self.cp_button_5.setMaximumSize(QtCore.QSize(250, 80))
        self.cp_button_5.setFont(font)
        self.cp_button_5.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.cp_button_5.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.cp_button_5.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/temperature_related/media/btn_icons/fan.svg"),
        )
        self.cp_button_5.setObjectName("cp_button_5")

        self.cp_content_layout.addWidget(self.cp_button_5, 2, 0, 1, 1)

        self.cp_button_6 = BlocksCustomButton(parent=self)
        self.cp_button_6.setSizePolicy(sizePolicy)
        self.cp_button_6.setMinimumSize(QtCore.QSize(10, 80))
        self.cp_button_6.setMaximumSize(QtCore.QSize(250, 80))
        self.cp_button_6.setFont(font)
        self.cp_button_6.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.cp_button_6.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.cp_button_6.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/extruder_related/media/btn_icons/switch_print_core.svg"),
        )
        self.cp_button_6.setObjectName("cp_button_6")

        self.cp_content_layout.addWidget(self.cp_button_6, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.cp_content_layout)
        widget.setLayout(self.verticalLayout)
        self.addWidget(widget)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("controlStackedWidget", "StackedWidget"))
        self.cp_header_title.setText(_translate("controlStackedWidget", "Control"))

        self.cp_button_1.setText(_translate("controlStackedWidget", "Motion\nControl"))
        self.cp_button_2.setText(_translate("controlStackedWidget", "Temp.\nControl"))
        self.cp_button_3.setText(
            _translate("controlStackedWidget", "Nozzle\nCalibration")
        )
        self.cp_button_4.setText(_translate("controlStackedWidget", "Z-Tilt"))
        self.cp_button_5.setText(_translate("controlStackedWidget", "Fans"))
        self.cp_button_6.setText(_translate("controlStackedWidget", "Swap\nPrint Core"))
