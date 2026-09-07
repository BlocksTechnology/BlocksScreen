import typing
from enum import Enum, auto

from lib.moonrakerComm import MoonWebSocket
from lib.panels.widgets.Common.basePopup import BasePopup
from lib.panels.widgets.UtilitiesTab.axisMaintPage import AxisMaintPage
from lib.panels.widgets.UtilitiesTab.infoPage import InfoPage
from lib.panels.widgets.UtilitiesTab.InputShaPage import InputShaperPage
from lib.panels.widgets.UtilitiesTab.ledsPage import LedsPage
from lib.panels.widgets.UtilitiesTab.routinePage import RoutineCheckPage
from lib.panels.widgets.UtilitiesTab.troubleshootPage import TroubleshootPage
from lib.printer import Printer
from lib.utils.blocks_button import BlocksCustomButton
from PyQt6 import QtCore, QtGui, QtWidgets


class Process(Enum):
    AXIS = auto()


class UtilitiesTab(QtWidgets.QStackedWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-back"
    )
    request_change_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, int, name="request-change-page"
    )
    request_available_objects_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="get-available-objects")
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    request_numpad_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int,
        str,
        str,
        "PyQt_PyObject",
        QtWidgets.QStackedWidget,
        name="request-numpad",
    )
    subscribe_config: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [list, "PyQt_PyObject"],
        [str, "PyQt_PyObject"],
        name="on-subscribe-config",
    )
    on_update_message: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="handle-update-message"
    )

    update_available: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="update-available"
    )

    show_update_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="show-update-page"
    )
    call_load_panel = QtCore.pyqtSignal(bool, str, bool, name="call-load-panel")

    on_object_list = QtCore.pyqtSignal(list, name="on-object-list")

    def __init__(
        self, parent: QtWidgets.QWidget, ws: MoonWebSocket, printer: Printer
    ) -> None:
        super().__init__(parent)

        self.info_page: InfoPage = InfoPage(self)
        self.leds_page: LedsPage = LedsPage(self)
        self.axes_page: AxisMaintPage = AxisMaintPage(self)
        self.routines_page: RoutineCheckPage = RoutineCheckPage(self)
        self.troubleshoot_page: TroubleshootPage = TroubleshootPage(self)

        # currently using the logic only so theres no duplicate (logic flag disables render/update Ui)
        self.is_page: InputShaperPage = InputShaperPage(self, logic=True)
        self.is_page.hide()

        self.setupUi()

        self.ws = ws
        self.printer: Printer = printer

        # --- UI Setup ---
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.up_update_btn.clicked.connect(
            lambda: self.show_update_page[bool].emit(False)
        )

        # --- Page Navigation ---
        self.up_input_shaper_btn.clicked.connect(self.ask_input_shaper)

        self.up_leds_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.leds_page))
        )
        self.up_axes_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.axes_page))
        )
        self.up_info_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.info_page))
        )
        self.up_routine_check_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.routines_page))
        )
        self.axes_page.axes_back_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.utilitiesPage))
        )
        self.troubleshoot_page.tb_back_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.utilitiesPage))
        )

        # --- Info ---
        self.info_page.request_back_button.connect(self.request_back)

        # --- LEDs ---
        self.leds_page.request_back_button.connect(self.request_back)
        self.leds_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.on_object_list.connect(self.leds_page.on_object_list)

        # --- Routines ---
        self.routines_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.routines_page.request_back.connect(self.request_back)
        self.routines_page.call_load_panel.connect(self.call_load_panel)
        self.routines_page.request_tb_page.connect(self.troubleshoot_request)
        self.printer.toolhead_update[str, str].connect(
            self.routines_page.on_toolhead_update
        )
        self.printer.printer_config.connect(
            self.routines_page.on_printer_config_received
        )
        self.routines_page.subscribe_config.connect(self.subscribe_config)
        self.on_object_list.connect(self.routines_page.on_object_list)

        # --- Axis Maintenance ---
        self.axes_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.axes_page.call_load_panel.connect(self.call_load_panel)
        self.axes_page.request_back.connect(self.request_back)

        # ---- Input Shaper ----
        self.is_popup: BasePopup = BasePopup(self, dialog=True, floating=True)
        self.is_popup.set_message(
            "Run the automatic input shaper?\n\nThe printer will calibrate both axes."
        )
        self.is_popup.confirm_button_text("Yes")
        self.is_popup.cancel_button_text("No")
        self.is_popup.confirm_button.clicked.connect(self.run_input_shaper)
        self.is_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.is_page.call_load_panel.connect(self.call_load_panel)
        self.printer.gcode_response.connect(self.is_page.handle_gcode_response)

        # --- Websocket/Printer Signals ---
        self.run_gcode_signal.connect(self.ws.api.run_gcode)

        self.subscribe_config[str, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )
        self.subscribe_config[list, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )

    def ask_input_shaper(self) -> None:
        """Ask whether to run the automatic input shaper."""
        self.is_popup.show()

    def run_input_shaper(self) -> None:
        """Start the automatic input shaper calibration."""
        self.is_popup.hide()
        self.is_page.handle_is("SHAPER_CALIBRATE")

    def troubleshoot_request(self) -> None:
        """Show troubleshoot page"""
        self.troubleshoot_page.show()

    def change_page(self, index: int):
        """Request change page by index"""
        self.call_load_panel.emit(False, "", False)
        self.troubleshoot_page.hide()
        if index < self.count():
            self.request_change_page.emit(3, index)

    @QtCore.pyqtSlot(name="request-back")
    def back_button(self) -> None:
        """Request back"""
        self.request_back.emit()

    def setupUi(self):

        self.setObjectName("utilitiesTab")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )

        self.resize(710, 410)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 410))
        self.setMaximumSize(QtCore.QSize(710, 410))
        self.utilitiesPage = QtWidgets.QWidget()
        self.utilitiesPage.setObjectName("utilitiesPage")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.utilitiesPage)
        self.verticalLayout.setObjectName("verticalLayout")

        self.up_header_layout = QtWidgets.QHBoxLayout()
        self.up_header_layout.setObjectName("up_header_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.up_title_label = QtWidgets.QLabel(parent=self.utilitiesPage)
        self.up_title_label.setSizePolicy(sizePolicy)
        self.up_title_label.setMinimumSize(QtCore.QSize(0, 60))
        self.up_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.up_title_label.setFont(font)
        self.up_title_label.setStyleSheet("background: transparent; color: white;")
        self.up_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.up_title_label.setObjectName("up_title_label")
        self.up_header_layout.addWidget(self.up_title_label)
        self.verticalLayout.addLayout(self.up_header_layout)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)

        self.up_content_layout = QtWidgets.QGridLayout()
        self.up_content_layout.setObjectName("up_content_layout")

        self.up_info_btn = BlocksCustomButton(parent=self.utilitiesPage)
        self.up_info_btn.setSizePolicy(sizePolicy)
        self.up_info_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.up_info_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.up_info_btn.setFont(font)
        self.up_info_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/info.svg")
        )
        self.up_info_btn.setObjectName("up_info_btn")
        self.up_content_layout.addWidget(self.up_info_btn, 0, 0, 1, 1)

        self.up_leds_btn = BlocksCustomButton(parent=self.utilitiesPage)
        self.up_leds_btn.setSizePolicy(sizePolicy)
        self.up_leds_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.up_leds_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.up_leds_btn.setFont(font)
        self.up_leds_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/LEDs.svg")
        )
        self.up_leds_btn.setObjectName("up_leds_btn")
        self.up_content_layout.addWidget(self.up_leds_btn, 0, 1, 1, 1)

        self.up_routine_check_btn = BlocksCustomButton(parent=self.utilitiesPage)
        self.up_routine_check_btn.setSizePolicy(sizePolicy)
        self.up_routine_check_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.up_routine_check_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.up_routine_check_btn.setFont(font)
        self.up_routine_check_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/routine.svg")
        )
        self.up_routine_check_btn.setObjectName("up_routine_check_btn")
        self.up_content_layout.addWidget(self.up_routine_check_btn, 1, 0, 1, 1)

        self.up_axes_btn = BlocksCustomButton(parent=self.utilitiesPage)
        self.up_axes_btn.setSizePolicy(sizePolicy)
        self.up_axes_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.up_axes_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.up_axes_btn.setFont(font)
        self.up_axes_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/motion/media/btn_icons/axis_maintenance.svg"),
        )
        self.up_content_layout.addWidget(self.up_axes_btn, 1, 1, 1, 1)

        self.up_update_btn = BlocksCustomButton(parent=self.utilitiesPage)
        self.up_update_btn.setSizePolicy(sizePolicy)
        self.up_update_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.up_update_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.up_update_btn.setFont(font)
        self.up_update_btn.setPixmap(
            QtGui.QPixmap(":/system/media/btn_icons/update-software-icon.svg")
        )

        self.up_update_btn.setObjectName("up_update_btn")
        self.up_content_layout.addWidget(self.up_update_btn, 2, 0, 1, 1)

        self.up_input_shaper_btn = BlocksCustomButton(parent=self.utilitiesPage)
        self.up_input_shaper_btn.setSizePolicy(sizePolicy)
        self.up_input_shaper_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.up_input_shaper_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.up_input_shaper_btn.setFont(font)
        self.up_input_shaper_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/input_shaper/media/btn_icons/input_shaper.svg"),
        )
        self.up_content_layout.addWidget(self.up_input_shaper_btn, 2, 1, 1, 1)

        self.verticalLayout.addLayout(self.up_content_layout)
        self.addWidget(self.utilitiesPage)

        # Info

        self.addWidget(self.info_page)

        # Leds Page

        self.addWidget(self.leds_page)

        # Routine Page

        self.addWidget(self.routines_page)

        # Axis maintenance Page

        self.addWidget(self.axes_page)

        # Input Shaper Page

        # self.addWidget(self.is_page)

        self.setCurrentIndex(0)

        _translate = QtCore.QCoreApplication.translate

        self.up_title_label.setText(_translate("self", "Utilities"))
        self.up_info_btn.setText(_translate("self", "Info"))
        self.up_leds_btn.setText(_translate("self", "LED's"))
        self.up_routine_check_btn.setText(_translate("self", "Routine\nCheck"))
        self.up_axes_btn.setText(_translate("self", "Axis\nMaint."))
        self.up_update_btn.setText(_translate("self", "Update"))
        self.up_input_shaper_btn.setText(_translate("self", "Input\nShaper"))
