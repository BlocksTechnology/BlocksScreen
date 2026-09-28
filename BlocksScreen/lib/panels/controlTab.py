from __future__ import annotations

import contextlib
import logging
import re
import typing

from lib.moonrakerComm import MoonWebSocket
from lib.panels.widgets.Common.basePopup import BasePopup
from lib.panels.widgets.ControlTab.axisPage import AxisPage
from lib.panels.widgets.ControlTab.extruderPage import ExtruderPage
from lib.panels.widgets.ControlTab.fansPage import FansPage
from lib.panels.widgets.ControlTab.printcorePage import SwapPrintcorePage
from lib.panels.widgets.ControlTab.probeHelperPage import ProbeHelper
from lib.panels.widgets.ControlTab.temperaturePage import TemperaturePage
from lib.panels.widgets.Common.numpadPage import CustomNumpad
from lib.panels.widgets.Common.slider_selector_page import SliderPage
from lib.printer import Printer
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.icon_button import IconButton
from lib.utils.menu_grid import fixed_menu_grid
from PyQt6 import QtCore, QtGui, QtWidgets

_logger = logging.getLogger(__name__)


class ControlTab(QtWidgets.QStackedWidget):
    """Printer Control Stacked Widget"""

    request_back_button = QtCore.pyqtSignal(name="request-back-button")
    request_change_page = QtCore.pyqtSignal(int, int, name="request-change-page")
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    disable_popups: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="disable-popups"
    )
    lock_ui: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="lock-ui"
    )
    request_file_info: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request-file-info"
    )
    call_load_panel = QtCore.pyqtSignal(bool, str, bool, name="call-load-panel")
    toggle_conn_page = QtCore.pyqtSignal(bool, name="call-load-panel")

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        ws: MoonWebSocket,
        printer: Printer,
        /,
    ) -> None:
        super().__init__(parent)
        self._setup_ui()

        self.back_button.clicked.connect(lambda: self._button_change(False))
        self.ws: MoonWebSocket = ws
        self.printer: Printer = printer
        self._true_zero_state: bool | None = None
        self._motion_active: bool = False
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.ztilt_state = False
        self.ztilt_result_screen = BasePopup(self, False, False)
        self.ztilt_result_screen_timer = QtCore.QTimer()
        self.ztilt_result_screen_timer.setSingleShot(True)
        self.ztilt_result_screen_timer.setInterval(5000)
        self.ztilt_result_screen_timer.timeout.connect(self.ztilt_result_screen.hide)
        self.probe_helper_page = ProbeHelper(self)
        self.addWidget(self.probe_helper_page)
        self.probe_helper_page.toggle_conn_page.connect(self.toggle_conn_page)
        self.probe_helper_page.disable_popups.connect(self.disable_popups)
        self.probe_helper_page.lock_ui.connect(self.lock_ui)
        self.probe_helper_page.call_load_panel.connect(self.call_load_panel)

        self.printcores_page = SwapPrintcorePage(self)
        self.addWidget(self.printcores_page)

        self.fans_page = FansPage(self)
        self.addWidget(self.fans_page)
        self.fans_page.request_back.connect(self.request_back_button)
        self.fans_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.fans_page.request_slider_page.connect(self.on_slidePage_request)

        self.sliderPage = SliderPage(self)
        self.addWidget(self.sliderPage)
        self.sliderPage.request_back.connect(self.request_back_button)

        self.axis_page = AxisPage(self)
        self.addWidget(self.axis_page)
        self.axis_page.request_back.connect(self.request_back_button)
        self.axis_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.printer.toolhead_update[str, list].connect(
            self.axis_page.on_toolhead_update
        )

        self.extruder_page = ExtruderPage(self, printer)
        self.addWidget(self.extruder_page)
        self.extruder_page.request_back.connect(self.request_back_button)
        self.extruder_page.run_gcode_signal.connect(self.run_gcode_signal)

        self.temperature_page = TemperaturePage(self)
        self.addWidget(self.temperature_page)
        self.temperature_page.request_back.connect(self.request_back_button)
        self.temperature_page.request_numpad.connect(self.on_numpad_request)
        self.temperature_page.run_gcode_signal.connect(self.run_gcode_signal)

        self.numpadPage = CustomNumpad(self)
        self.numpadPage.setMaximumHeight(400)
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

        self.printer.printer_config.connect(self.temperature_page.on_printer_config)
        self.printer.request_object_subscription_signal.connect(self._on_object_list)
        self.run_gcode_signal.connect(self.ws.api.run_gcode)
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

    def _menu(self, active: bool) -> list[tuple[str, str, typing.Callable]]:
        # (text, icon, slot) for each grid button, in grid order
        if active:
            return [
                (
                    "Auto Home",
                    ":/motion/media/btn_icons/home_all.svg",
                    lambda: self.run_gcode_signal.emit("G28\nM400"),
                ),
                (
                    "Disable\nSteppers",
                    ":/motion/media/btn_icons/disable_steppers.svg",
                    lambda: self.run_gcode_signal.emit("M84\nM400"),
                ),
                (
                    "Axis",
                    ":/motion/media/btn_icons/axis_maintenance.svg",
                    lambda: self.change_page(self.indexOf(self.axis_page)),
                ),
                (
                    "Extruder",
                    ":/extruder_related/media/btn_icons/extrude.svg",
                    lambda: self.change_page(self.indexOf(self.extruder_page)),
                ),
            ]
        return [
            (
                "Motion\nControl",
                ":/motion/media/btn_icons/axis_maintenance.svg",
                lambda: self._button_change(True),
            ),
            (
                "Temp.\nControl",
                ":/temperature_related/media/btn_icons/temperature.svg",
                lambda: self.change_page(self.indexOf(self.temperature_page)),
            ),
            (
                "Nozzle\nCalibration",
                ":/z_levelling/media/btn_icons/bed_levelling.svg",
                lambda: self.change_page(self.indexOf(self.probe_helper_page)),
            ),
            (
                "Z-Tilt",
                ":/z_levelling/media/btn_icons/bed_levelling.svg",
                self.handle_ztilt,
            ),
            (
                "Fans",
                ":/temperature_related/media/btn_icons/fan.svg",
                lambda: self.change_page(self.indexOf(self.fans_page)),
            ),
            (
                "Swap\nPrint Core",
                ":/ui/media/btn_icons/LEDs.svg",
                self.show_swapcore,
            ),
        ]

    def _button_change(self, active: bool):
        self._motion_active = active
        for btn in self.cp_buttons:
            with contextlib.suppress(RuntimeError, TypeError):
                btn.clicked.disconnect()
        for btn, (text, icon, slot) in zip(self.cp_buttons, self._menu(active)):
            btn.setText(text)
            btn.setPixmap(QtGui.QPixmap(icon))
            btn.clicked.connect(slot)
        self.cp_header_title.setText("Motion" if active else "Control")
        self.back_button.setVisible(active)
        self.Hblank.setVisible(active)
        self._show_blank(active)
        self._apply_true_zero_layout()
        self.repaint()

    def _show_blank(self, on: bool) -> None:
        self.blank.setVisible(on)
        self.cp_button_5.setVisible(not on)

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        self._button_change(False)
        return super().showEvent(a0)

    def _handle_z_tilt_object_update(self, value, state):
        if not self.isVisible():
            return
        if state:
            self.call_load_panel.emit(False, "", False)
            self.ztilt_result_screen.set_message("Z-axis calibration was successful.")
            self.ztilt_result_screen.show()
            self.ztilt_result_screen_timer.start()

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
        with contextlib.suppress(RuntimeError, TypeError):
            self.sliderPage.value_selected.disconnect()
        self.sliderPage.value_selected.connect(callback)
        self.sliderPage.set_name(name)
        self.sliderPage.set_slider_minimum(min_value)
        self.sliderPage.set_slider_maximum(max_value)
        self.sliderPage.set_slider_position(int(current_value))
        self.change_page(self.indexOf(self.sliderPage))

    def handle_printcoreupdate(self, value: dict):
        _swapping = value.get("swapping")
        if _swapping is None or _swapping == "idle":
            return

        if _swapping == "in_pos":
            self.call_load_panel.emit(False, "", False)
            self.printcores_page.show()
            self.disable_popups.emit(True)
            self.printcores_page.setText(
                "Please Insert Print Core \n \n Afterwards click continue"
            )
        if _swapping == "unloading":
            self.call_load_panel.emit(True, "Unloading print core", False)
        if _swapping == "cleaning":
            self.call_load_panel.emit(True, "Cleaning print core", False)

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
                        self.call_load_panel.emit(False, "", False)
                        self.ztilt_result_screen.set_message(
                            "Something went wrong during Z-axis calibration."
                        )
                        self.ztilt_result_screen.show()
                        self.ztilt_result_screen_timer.start()
                        return
                    self.call_load_panel.emit(
                        True,
                        f"Retries: {retries_done}/{retries_total}"
                        f" | Range: {probed_range:.6f}"
                        f" | Tolerance: {tolerance:.6f}",
                        False,
                    )

    def handle_ztilt(self):
        """Handle Z-Tilt Adjustment"""
        self.call_load_panel.emit(
            True, "Please wait, performing Z-axis calibration.", False
        )
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
        self._true_zero_state = None
        self._apply_true_zero_layout()

    @QtCore.pyqtSlot(dict, name="_on_object_list")
    def _on_object_list(self, objects: dict) -> None:
        """Track whether the printer reports a true zero offset probe"""
        has_true_zero = self.printer.uses_true_zero_offset
        if has_true_zero == self._true_zero_state:
            return
        self._true_zero_state = has_true_zero
        self._apply_true_zero_layout()

    def _apply_true_zero_layout(self) -> None:
        """With true zero, show Fans in the nozzle-calibration slot instead."""
        if self._motion_active:
            return
        has_true_zero = bool(self._true_zero_state)
        with contextlib.suppress(RuntimeError, TypeError):
            self.cp_button_3.clicked.disconnect()
        if has_true_zero:
            self.cp_button_3.setText("Fans")
            self.cp_button_3.setPixmap(
                QtGui.QPixmap(":/temperature_related/media/btn_icons/fan.svg")
            )
            self.cp_button_3.clicked.connect(
                lambda: self.change_page(self.indexOf(self.fans_page))
            )
            self._show_blank(True)
        else:
            self.cp_button_3.setText("Nozzle\nCalibration")
            self.cp_button_3.setPixmap(
                QtGui.QPixmap(":/z_levelling/media/btn_icons/bed_levelling.svg")
            )
            self.cp_button_3.clicked.connect(
                lambda: self.change_page(self.indexOf(self.probe_helper_page))
            )
            self._show_blank(False)

    def show_swapcore(self):
        """Show swap printcore"""
        self.run_gcode_signal.emit("CHANGE_PRINTCORES")
        self.call_load_panel.emit(True, "Preparing to swap print core", False)

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

        with contextlib.suppress(RuntimeError, TypeError):
            self.numpadPage.value_selected.disconnect()
        self.numpadPage.value_selected.connect(callback)
        self.numpadPage.set_name(name)
        self.numpadPage.set_value(current_value)
        self.numpadPage.set_min_value(min_value)
        self.numpadPage.set_max_value(max_value)
        self.change_page(self.indexOf(self.numpadPage))

    def change_page(self, index):
        """Handles changing page"""
        self.request_change_page.emit(2, index)

    def _setup_ui(self) -> None:
        """Build the control tab page: header, back button, and option grid."""
        self.resize(710, 410)
        root = QtWidgets.QWidget()
        root.setObjectName("control_page")
        root.setMinimumSize(QtCore.QSize(710, 410))
        root.setMaximumSize(QtCore.QSize(710, 410))

        self.blank = QtWidgets.QWidget()
        self.blank.setMinimumSize(QtCore.QSize(250, 80))
        self.blank.setMaximumSize(QtCore.QSize(250, 80))

        self.Hblank = QtWidgets.QWidget()
        self.Hblank.setMinimumSize(QtCore.QSize(60, 60))
        self.Hblank.setMaximumSize(QtCore.QSize(60, 60))

        self.verticalLayout = QtWidgets.QVBoxLayout(root)
        self.verticalLayout.setObjectName("verticalLayout")

        self.cp_header_layout = QtWidgets.QHBoxLayout()
        self.cp_header_layout.setObjectName("cp_header_layout")

        self.cp_header_layout.addWidget(self.Hblank)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.cp_header_title = QtWidgets.QLabel(parent=root)
        self.cp_header_title.setSizePolicy(sizePolicy)
        self.cp_header_title.setMinimumSize(QtCore.QSize(0, 60))
        self.cp_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.cp_header_title.setFont(font)
        self.cp_header_title.setStyleSheet("background: transparent; color: white;")
        self.cp_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
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
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)

        self.cp_buttons: list[BlocksCustomButton] = []
        for i in range(6):
            btn = BlocksCustomButton(parent=root)
            btn.setSizePolicy(sizePolicy)
            btn.setFixedSize(QtCore.QSize(250, 80))
            btn.setFont(font)
            self.cp_content_layout.addWidget(btn, i // 2, i % 2, 1, 1)
            self.cp_buttons.append(btn)
        (
            self.cp_button_1,
            self.cp_button_2,
            self.cp_button_3,
            self.cp_button_4,
            self.cp_button_5,
            self.cp_button_6,
        ) = self.cp_buttons

        self.cp_content_layout.addWidget(self.blank, 2, 0, 1, 1)
        self.blank.hide()

        self.verticalLayout.addWidget(fixed_menu_grid(root, self.cp_content_layout))
        self.addWidget(root)
