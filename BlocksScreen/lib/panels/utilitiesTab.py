import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum, auto
from lib.moonrakerComm import MoonWebSocket
from lib.printer import Printer
from lib.utils.blocks_button import BlocksCustomButton
from lib.panels.widgets.basePopup import BasePopup
from lib.panels.widgets.UtilitiesTab.infoPage import InfoPage
from lib.panels.widgets.UtilitiesTab.ledsPage import LedsPage
from lib.panels.widgets.UtilitiesTab.ledssliderPage import LedsSliderPage
from lib.panels.widgets.UtilitiesTab.troubleshootPage import TroubleshootPage
from lib.panels.widgets.UtilitiesTab.inputshaperPage import InputShaperPage
from lib.panels.widgets.UtilitiesTab.inputshaperResultPage import InputShaperResultsPage
from lib.panels.widgets.UtilitiesTab.axismaintPage import AxisMaintenancePage
from lib.panels.widgets.UtilitiesTab.routineCheckPage import RoutineCheckPage
from lib.panels.widgets.UtilitiesTab.rc_page import RoutineCheckAnswerPage


class Process(Enum):
    FAN = auto()
    AXIS = auto()
    BED_HEATER = auto()
    EXTRUDER = auto()
    AXIS_MAINTENANCE = auto()


class UtilitiesTab(QtWidgets.QStackedWidget):
    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    request_change_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, int, name="request-change-page"
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    subscribe_config: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [list, "PyQt_PyObject"],
        [str, "PyQt_PyObject"],
        name="on-subscribe-config",
    )
    show_update_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="show-update-page"
    )
    on_object_list = QtCore.pyqtSignal(list, name="on-object-list")
    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")

    def __init__(
        self, parent: QtWidgets.QWidget, ws: MoonWebSocket, printer: Printer
    ) -> None:
        super().__init__(parent)

        self._setupUi()

        self.ws = ws
        self.printer: Printer = printer
        self.troubleshoot_page: TroubleshootPage = TroubleshootPage(self)

        self.run_gcode_signal.connect(self.ws.api.run_gcode)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self.info_page = InfoPage(self)
        self.addWidget(self.info_page)
        self.info_page.request_back.connect(self.request_back_button)

        self.leds_slider_page = LedsSliderPage(self)
        self.addWidget(self.leds_slider_page)
        self.leds_slider_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.leds_slider_page.request_back.connect(
            lambda: self.request_back_button.emit()
        )
        self.leds_slider_page.request_change_page.connect(self.change_page)

        self.leds_page = LedsPage(self)
        self.addWidget(self.leds_page)
        self.on_object_list.connect(self.leds_page.on_object_list)
        self.leds_page.request_ledslider_page.connect(self.on_leds_slider_request)
        self.leds_page.request_back.connect(lambda: self.request_back_button.emit())

        self.is_page = InputShaperResultsPage(self)
        self.addWidget(self.is_page)
        self.printer.gcode_response.connect(self.is_page.handle_gcode_response)
        self.is_page.call_load_panel.connect(self.call_load_panel)
        self.is_page.run_gcode_signal.connect(self.run_gcode_signal)

        self.input_shaper_page = InputShaperPage(self)
        self.addWidget(self.input_shaper_page)
        self.input_shaper_page.request_is_results_page.connect(
            lambda: self.change_page(self.indexOf(self.is_page))
        )
        self.input_shaper_page.request_back_button.connect(lambda: self.change_page(0))
        self.input_shaper_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.input_shaper_page.call_load_panel.connect(self.call_load_panel)
        self.input_shaper_page.set_aut.connect(self.is_page.set_aut)

        self.axis_page = AxisMaintenancePage(self)
        self.addWidget(self.axis_page)
        self.axis_page.request_back_button.connect(self.request_back_button)
        self.axis_page.set_dialog_popup.connect(self.set_dialog_axismaintenace_popup)
        self.axis_page.show_waiting_page.connect(self.show_waiting_page)
        self.axis_page.call_load_panel.connect(self.call_load_panel)
        self.axis_page.run_gcode_signal.connect(self.run_gcode_signal)

        self.routine_check_page = RoutineCheckPage(self)
        self.addWidget(self.routine_check_page)
        self.routine_check_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.routine_check_page.request_back_button.connect(self.request_back_button)
        self.on_object_list.connect(self.routine_check_page.on_object_list)
        self.routine_check_page.set_rc_page.connect(self.set_rc_page)
        self.routine_check_page.show_waiting_page.connect(self.show_waiting_page)
        self.routine_check_page.request_troubleshoot_page.connect(
            self.troubleshoot_request
        )

        self.rc_page = RoutineCheckAnswerPage(self)
        self.addWidget(self.rc_page)
        self.rc_page.on_rc_asnwer.connect(self.routine_check_page.on_routine_answer)
        self.rc_page.request_back_button.connect(self.request_back_button)

        self.utilities_info_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.info_page))
        )
        self.utilities_leds_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.leds_page))
        )
        self.utilities_axes_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.axis_page))
        )
        self.utilities_routine_check_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.routine_check_page))
        )
        self.utilities_input_shaper_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.input_shaper_page))
        )

        self.update_btn.clicked.connect(lambda: self.show_update_page[bool].emit(False))

        self.is_page.action_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.input_shaper_page))
        )

        self.dialogpopup = BasePopup(self, False, True)
        self.addWidget(self.dialogpopup)

        self.subscribe_config[str, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )
        self.subscribe_config[list, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )

        self.printer.printer_config.connect(self.on_printer_config_received)

    def on_leds_slider_request(self, led: any, name=str, single=bool):
        self.change_page(self.indexOf(self.leds_slider_page))
        self.leds_slider_page.set_slider(led_state=led, name=name, single=single)

    def on_printer_config_received(self, config: dict) -> None:
        """Handle printer configuration"""
        for axis in ("x", "y", "z"):
            self.subscribe_config[str, "PyQt_PyObject"].emit(
                f"stepper_{axis}", self.axis_page.on_object_config
            )

    def set_rc_page(self, title: str, message: str):
        self.rc_page.setTitle(title)
        self.rc_page.setMessage(message)

    @QtCore.pyqtSlot(str, "PyQt_PyObject", name="set-dialog-popup")
    def set_dialog_axismaintenace_popup(self, label: str, accept: "PyQt_PyObject"):
        """Set text on routine page"""
        self.dialogpopup.set_message(label)
        try:
            self.dialogpopup.disconnect()
        except:
            pass
        self.dialogpopup.accepted.connect(accept)

    @QtCore.pyqtSlot(str, int, bool, name="show-waiting-page")
    def show_waiting_page(self, label: str, time_ms: int, popup: bool):
        """Show placeholder page"""
        self.call_load_panel.emit(True, label)
        if popup:
            QtCore.QTimer.singleShot(time_ms, lambda: self.dialogpopup.open())
        else:
            QtCore.QTimer.singleShot(
                time_ms, lambda: self.change_page(self.indexOf(self.rc_page))
            )

    @QtCore.pyqtSlot(name="request-troubleshoot-page")
    def troubleshoot_request(self) -> None:
        """Show troubleshoot page"""
        self.troubleshoot_page.show()

    def change_page(self, index: int):
        """Request change page by index"""
        self.request_change_page.emit(3, index)

    def _setupUi(self):
        self.resize(710, 410)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 410))
        self.setMaximumSize(QtCore.QSize(710, 410))

        widget = QtWidgets.QWidget()
        widget.setMinimumSize(QtCore.QSize(710, 410))
        widget.setMaximumSize(QtCore.QSize(710, 410))
        widget.setObjectName("utilities_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)

        self.utilities_header_layout = QtWidgets.QHBoxLayout()
        self.utilities_header_layout.setObjectName("utilities_header_layout")

        self.utilities_title_label = QtWidgets.QLabel(parent=self)
        self.utilities_title_label.setSizePolicy(sizePolicy)
        self.utilities_title_label.setMinimumSize(QtCore.QSize(0, 60))
        self.utilities_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.utilities_title_label.setFont(font)
        self.utilities_title_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.utilities_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.utilities_title_label.setObjectName("utilities_title_label")

        self.utilities_header_layout.addWidget(self.utilities_title_label)
        self.verticalLayout.addLayout(self.utilities_header_layout)
        self.utilities_content_layout = QtWidgets.QGridLayout()

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)

        self.utilities_content_layout.setObjectName("utilities_content_layout")
        self.utilities_axes_btn = BlocksCustomButton(parent=self)
        self.utilities_axes_btn.setSizePolicy(sizePolicy)
        self.utilities_axes_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_axes_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_axes_btn.setFont(font)
        self.utilities_axes_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/motion/media/btn_icons/axis_maintenance.svg"),
        )
        self.utilities_axes_btn.setObjectName("utilities_axes_btn")

        self.utilities_content_layout.addWidget(self.utilities_axes_btn, 1, 1, 1, 1)

        self.update_btn = BlocksCustomButton(parent=self)
        self.update_btn.setSizePolicy(sizePolicy)
        self.update_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.update_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.update_btn.setFont(font)
        self.update_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/system/media/btn_icons/update-software-icon.svg"),
        )

        self.update_btn.setObjectName("update_btn")

        self.utilities_content_layout.addWidget(self.update_btn, 2, 0, 1, 1)
        self.utilities_routine_check_btn = BlocksCustomButton(parent=self)
        self.utilities_routine_check_btn.setSizePolicy(sizePolicy)
        self.utilities_routine_check_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_routine_check_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_routine_check_btn.setFont(font)
        self.utilities_routine_check_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/routine.svg")
        )
        self.utilities_routine_check_btn.setObjectName("utilities_routine_check_btn")

        self.utilities_content_layout.addWidget(
            self.utilities_routine_check_btn, 1, 0, 1, 1
        )

        self.utilities_input_shaper_btn = BlocksCustomButton(parent=self)
        self.utilities_input_shaper_btn.setSizePolicy(sizePolicy)
        self.utilities_input_shaper_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_input_shaper_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_input_shaper_btn.setFont(font)
        self.utilities_input_shaper_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/input_shaper/media/btn_icons/input_shaper.svg"),
        )
        self.utilities_input_shaper_btn.setObjectName("utilities_input_shaper_btn")

        self.utilities_content_layout.addWidget(
            self.utilities_input_shaper_btn, 2, 1, 1, 1
        )

        self.utilities_info_btn = BlocksCustomButton(parent=self)
        self.utilities_info_btn.setSizePolicy(sizePolicy)
        self.utilities_info_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_info_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_info_btn.setFont(font)
        self.utilities_info_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/info.svg")
        )

        self.utilities_info_btn.setObjectName("utilities_info_btn")

        self.utilities_content_layout.addWidget(self.utilities_info_btn, 0, 0, 1, 1)
        self.utilities_leds_btn = BlocksCustomButton(parent=self)
        self.utilities_leds_btn.setSizePolicy(sizePolicy)
        self.utilities_leds_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_leds_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_leds_btn.setFont(font)
        self.utilities_leds_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/LEDs.svg")
        )
        self.utilities_leds_btn.setObjectName("utilities_leds_btn")
        self.utilities_content_layout.addWidget(self.utilities_leds_btn, 0, 1, 1, 1)

        self.verticalLayout.addLayout(self.utilities_content_layout)

        widget.setLayout(self.verticalLayout)
        self.addWidget(widget)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "StackedWidget"))
        self.utilities_title_label.setText(_translate("self", "Utilities"))
        self.utilities_axes_btn.setText(_translate("self", "Axis\nMaint."))
        self.update_btn.setText(_translate("self", "Update"))
        self.utilities_routine_check_btn.setText(_translate("self", "Routine\nCheck"))
        self.utilities_input_shaper_btn.setText(_translate("self", "Input\nShaper"))
        self.utilities_info_btn.setText(_translate("self", "Info"))
        self.utilities_leds_btn.setText(_translate("self", "LED's"))
