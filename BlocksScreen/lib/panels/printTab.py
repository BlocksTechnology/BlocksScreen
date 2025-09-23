import os
import typing
from functools import partial

from lib.panels.widgets.babystepPage import BabystepPage
from lib.panels.widgets.tunePage import TuneWidget
from lib.files import Files
from lib.moonrakerComm import MoonWebSocket
from lib.panels.widgets.confirmPage import ConfirmWidget
from lib.panels.widgets.filesPage import FilesPage
from lib.panels.widgets.jobStatusPage import JobStatusWidget
from lib.panels.widgets.sensorsPanel import SensorsWindow
from lib.printer import Printer
from lib.panels.widgets.slider_selector_page import SliderPage
from lib.utils.blocks_button import BlocksCustomButton
from lib.panels.widgets.numpadPage import CustomNumpad
from PyQt6 import QtCore, QtGui, QtWidgets


class PrintTab(QtWidgets.QStackedWidget):
    """QStackedWidget that contains the following widget panels:

    - Main page: Simple page with a message field and a button to start a print;
    - File list page: A file list where displayed files are selectable to be printed;
    - Confirm page: A page to confirm or not if the selected file is to be printed;
    - Print page: A page for controlling the ongoing job, Pause/Resume and stop functionality
    - Tune page: Accessible only from the print page;
    - Babystep page: Control the z_offset during a ongoing print;
    - Change page: A page that permits changing the filament, stops the print -> change the filament -> resume the print;

    Args:
        QStackedWidget (QStackedWidget): This class is inherited from QStackedWidget from Qt6

    __init__:
        parent (QWidget | QObject): The parent for this tab.
        file_data (Files): Class object that handles printer files.
        ws (MoonWebSocket): Moonraker websocket instance.
        printer (Printer): Class object that handles printer objects information.

    """

    request_query_print_stats: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(dict, name="request_query_print_stats")
    )

    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-back"
    )
    request_change_page: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(int, int, name="request_change_page")
    )

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )
    _z_offset: float = 0.0

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        file_data: Files,
        ws: MoonWebSocket,
        printer: Printer,
    ) -> None:
        super().__init__(parent)

        self.setupMainPrintPage()
        self.ws: MoonWebSocket = ws
        self.printer: Printer = printer

        # TODO: Get the gcode path from the configfile by asking the websocket first
        self.gcode_path = os.path.expanduser("~/printer_data/gcodes")
        self.setMouseTracking(True)

        self.sliderPage = SliderPage(self)
        self.addWidget(self.sliderPage)
        self.sliderPage.request_back.connect(self.back_button)
        self.numpadPage = CustomNumpad(self)
        self.numpadPage.request_back.connect(self.back_button)
        self.addWidget(self.numpadPage)

        self.file_data: Files = file_data
        self.filesPage_widget = FilesPage(self)
        self.addWidget(self.filesPage_widget)

        self.confirmPage_widget = ConfirmWidget(self)
        self.addWidget(self.confirmPage_widget)
        self.confirmPage_widget.reject_button.clicked.connect(self.back_button)
        self.filesPage_widget.file_selected.connect(
            self.confirmPage_widget.on_show_widget
        )
        self.filesPage_widget.file_selected.connect(
            lambda: self.change_page(self.indexOf(self.confirmPage_widget))
        )
        self.filesPage_widget.back_btn.clicked.connect(self.back_button)
        self.filesPage_widget.request_file_info.connect(
            self.file_data.on_request_fileinfo
        )
        self.file_data.fileinfo.connect(self.filesPage_widget._on_fileinfo)
        self.filesPage_widget.request_file_list_refresh.connect(
            self.file_data.request_file_list
        )
        self.file_data.on_file_list.connect(self.filesPage_widget._on_file_list)

        self.jobStatusPage_widget = JobStatusWidget(self)
        self.addWidget(self.jobStatusPage_widget)

        self.confirmPage_widget.on_accept.connect(
            self.jobStatusPage_widget.on_print_start
        )
        self.jobStatusPage_widget.show_request.connect(
            lambda: self.change_page(self.indexOf(self.jobStatusPage_widget))
        )
        self.jobStatusPage_widget.hide_request.connect(
            # lambda: self.change_page(self.indexOf(self.panel.print_page))
            lambda: self.change_page(self.indexOf(self.print_page))
        )
        self.jobStatusPage_widget.request_file_info.connect(
            self.file_data.on_request_fileinfo
        )
        self.file_data.fileinfo.connect(self.jobStatusPage_widget.on_fileinfo)
        self.jobStatusPage_widget.print_start.connect(self.ws.api.start_print)
        self.jobStatusPage_widget.print_resume.connect(
            self.ws.api.resume_print
        )
        self.jobStatusPage_widget.print_cancel.connect(
            self.ws.api.cancel_print
        )
        self.jobStatusPage_widget.print_pause.connect(self.ws.api.pause_print)
        self.jobStatusPage_widget.request_query_print_stats.connect(
            self.ws.api.object_query
        )

        self.printer.virtual_sdcard_update[str, bool].connect(
            self.jobStatusPage_widget.virtual_sdcard_update
        )
        self.printer.virtual_sdcard_update[str, float].connect(
            self.jobStatusPage_widget.virtual_sdcard_update
        )
        self.printer.virtual_sdcard_update.connect(
            self.jobStatusPage_widget.virtual_sdcard_update
        )
        self.printer.print_stats_update[str, str].connect(
            self.jobStatusPage_widget.on_print_stats_update
        )
        self.printer.print_stats_update[str, dict].connect(
            self.jobStatusPage_widget.on_print_stats_update
        )
        self.printer.print_stats_update[str, float].connect(
            self.jobStatusPage_widget.on_print_stats_update
        )

        self.printer.gcode_move_update[str, list].connect(
            self.jobStatusPage_widget.on_gcode_move_update
        )

        self.babystepPage = BabystepPage(self)
        self.babystepPage.request_back.connect(self.back_button)
        self.addWidget(self.babystepPage)

        self.tune_page = TuneWidget(self)
        self.addWidget(self.tune_page)
        self.jobStatusPage_widget.tune_clicked.connect(
            lambda: self.change_page(self.indexOf(self.tune_page))
        )
        self.tune_page.request_back.connect(self.back_button)
        self.printer.extruder_update.connect(
            self.tune_page.on_extruder_temperature_change
        )
        self.printer.heater_bed_update.connect(
            self.tune_page.on_heater_bed_temperature_change
        )
        self.printer.fan_update[str, str, float].connect(
            self.tune_page.on_fan_object_update
        )
        self.printer.fan_update[str, str, int].connect(
            self.tune_page.on_fan_object_update
        )
        self.printer.gcode_move_update[str, float].connect(
            self.tune_page.on_gcode_move_update
        )
        self.printer.gcode_move_update[str, list].connect(
            self.babystepPage.on_gcode_move_update
        )
        self.tune_page.run_gcode.connect(self.ws.api.run_gcode)
        self.tune_page.request_sliderPage[str, int, "PyQt_PyObject"].connect(
            self.on_slidePage_request
        )
        self.tune_page.request_sliderPage[
            str, int, "PyQt_PyObject", int, int
        ].connect(self.on_slidePage_request)
        self.tune_page.request_numpad[
            str, int, "PyQt_PyObject", int, int
        ].connect(self.on_numpad_request)
        self.tune_page.request_numpad[
            str,
            int,
            "PyQt_PyObject",
        ].connect(self.on_numpad_request)
        self.tune_page.request_bbpPage.connect(
            lambda: self.change_page(self.indexOf(self.babystepPage))
        )
        self.tune_page.request_sensorsPage.connect(
            lambda: self.change_page(self.indexOf(self.sensorsPanel))
        )

        self.sensorsPanel = SensorsWindow(self)
        self.addWidget(self.sensorsPanel)

        self.printer.request_object_subscription_signal.connect(
            self.sensorsPanel.handle_available_fil_sensors
        )
        self.sensorsPanel.request_back.connect(self.back_button)
        self.sensorsPanel.run_gcode_signal.connect(self.ws.api.run_gcode)

        self.printer.filament_motion_sensor_update.connect(
            self.sensorsPanel.handle_fil_state_change
        )
        self.printer.filament_switch_sensor_update.connect(
            self.sensorsPanel.handle_fil_state_change
        )
        self.main_print_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.filesPage_widget))
        )
        self.babystepPage.run_gcode.connect(self.ws.api.run_gcode)

        self.run_gcode_signal.connect(self.ws.api.run_gcode)

        self.change_page(
            self.indexOf(self.print_page)
        )  # force set the initial page

    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", name="on_numpad_request")
    @QtCore.pyqtSlot(
        str, int, "PyQt_PyObject", int, int, name="on_numpad_request"
    )
    def on_numpad_request(
        self,
        name: str,
        current_value: int,
        callback,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        self.numpadPage.value_selected.connect(callback)
        self.numpadPage.set_name(name)
        self.numpadPage.set_value(current_value)
        self.numpadPage.set_min_value(min_value)
        self.numpadPage.set_max_value(max_value)
        self.change_page(self.indexOf(self.numpadPage))

    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", name="on_slidePage_request")
    @QtCore.pyqtSlot(
        str, int, "PyQt_PyObject", int, int, name="on_slidePage_request"
    )
    def on_slidePage_request(
        self,
        name: str,
        current_value: int,
        callback,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        self.sliderPage.value_selected.connect(callback)
        self.sliderPage.set_name(name)
        self.sliderPage.set_slider_position(int(current_value))
        self.sliderPage.set_slider_minimum(min_value)
        self.sliderPage.set_slider_maximum(max_value)
        self.change_page(self.indexOf(self.sliderPage))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        REFACTOR: Instead of using a background svg pixmap just draw the
                background with with the correct styles and everything
        """
        if self.babystepPage.isVisible():
            _button_name_str = f"nozzle_offset_{self._z_offset}"
            if hasattr(self, _button_name_str):
                _button_attr = getattr(self, _button_name_str)
                if callable(_button_attr) and isinstance(
                    _button_attr, BlocksCustomButton
                ):
                    _button_attr.setChecked(True)

        return super().paintEvent(a0)

    def setProperty(self, name: str, value: typing.Any) -> bool:
        """Intercept the set property method

        Args:
            name (str): Name of the dynamic property
            value (typing.Any): Value for the dynamic property

        Returns:
            bool: Returns to the super class
        """
        if name == "backgroundPixmap":
            self.background = value
        return super().setProperty(name, value)

    def change_page(self, index: int) -> None:
        """Requests a page change page to the global manager

        Args:
            index (int): page index
        """
        self.request_change_page.emit(0, index)

    def back_button(self) -> None:
        """Goes back to the previous page"""
        self.request_back.emit()

    def setupMainPrintPage(self) -> None:
        self.setObjectName("printStackedWidget")
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.resize(710, 410)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 410))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setProperty(
            "backgroundPixmap",
            QtGui.QPixmap(
                ":/background/media/graphics/scroll_list_window.svg"
            ),
        )
        self.print_page = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.print_page.sizePolicy().hasHeightForWidth()
        )
        self.print_page.setSizePolicy(sizePolicy)
        self.print_page.setMinimumSize(QtCore.QSize(710, 400))
        self.print_page.setMaximumSize(QtCore.QSize(720, 420))
        self.print_page.setObjectName("print_page")
        self.main_print_btn = BlocksCustomButton(parent=self.print_page)
        self.main_print_btn.setGeometry(QtCore.QRect(230, 120, 250, 80))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.main_print_btn.sizePolicy().hasHeightForWidth()
        )
        self.main_print_btn.setSizePolicy(sizePolicy)
        self.main_print_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.main_print_btn.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.main_print_btn.setFont(font)
        self.main_print_btn.setMouseTracking(False)
        self.main_print_btn.setTabletTracking(True)
        self.main_print_btn.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.main_print_btn.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.main_print_btn.setStyleSheet("")
        self.main_print_btn.setAutoDefault(False)
        self.main_print_btn.setFlat(True)
        self.main_print_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/print.svg")
        )
        self.main_print_btn.setObjectName("main_print_btn")
        self.main_text_label = QtWidgets.QLabel(parent=self.print_page)
        self.main_text_label.setEnabled(True)
        self.main_text_label.setGeometry(QtCore.QRect(105, 180, 500, 200))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.main_text_label.sizePolicy().hasHeightForWidth()
        )
        self.main_text_label.setSizePolicy(sizePolicy)
        self.main_text_label.setMinimumSize(QtCore.QSize(0, 200))
        self.main_text_label.setMaximumSize(QtCore.QSize(500, 200))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        self.main_text_label.setFont(font)
        self.main_text_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.main_text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_text_label.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.NoTextInteraction
        )
        self.main_text_label.setObjectName("main_text_label")
        self.addWidget(self.print_page)

        
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(
            _translate("printStackedWidget", "StackedWidget")
        )
        self.main_print_btn.setText(_translate("printStackedWidget", "Print"))
        self.main_print_btn.setProperty(
            "class", _translate("printStackedWidget", "menu_btn")
        )
        self.main_text_label.setText(
            _translate("printStackedWidget", "Printer ready")
        )
        
