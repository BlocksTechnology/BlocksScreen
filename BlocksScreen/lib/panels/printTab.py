import logging
import os
import typing
from functools import partial

from configfile import BlocksScreenConfig, get_configparser
from lib.files import Files
from lib.moonrakerComm import MoonWebSocket
from lib.panels.widgets.babystepPage import BabystepPage
from lib.panels.widgets.basePopup import BasePopup
from lib.panels.widgets.confirmPage import ConfirmWidget
from lib.panels.widgets.filesPage import FilesPage
from lib.panels.widgets.jobStatusPage import JobStatusWidget
from lib.panels.widgets.loadWidget import LoadingOverlayWidget
from lib.panels.widgets.numpadPage import CustomNumpad
from lib.panels.widgets.sensorsPanel import SensorsWindow
from lib.panels.widgets.slider_selector_page import SliderPage
from lib.panels.widgets.tunePage import TuneWidget
from lib.printer import Printer
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.display_button import DisplayButton
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(name="logs/BlocksScreen.log")


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

    request_query_print_stats: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="request_query_print_stats"
    )

    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-back"
    )
    request_change_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, int, name="request_change_page"
    )

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )
    on_cancel_print: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="on_cancel_print"
    )

    _z_offset: float = 0.0
    _active_z_offset: float = 0.0
    _finish_print_handled: bool = False

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
        self.config: BlocksScreenConfig = get_configparser()
        # TODO: Get the gcode path from the configfile by asking the websocket first
        self.gcode_path = os.path.expanduser("~/printer_data/gcodes")
        self.setMouseTracking(True)

        self.sliderPage = SliderPage(self)
        self.addWidget(self.sliderPage)
        self.sliderPage.request_back.connect(self.back_button)
        self.numpadPage = CustomNumpad(self)
        self.numpadPage.request_back.connect(self.back_button)
        self.addWidget(self.numpadPage)

        self.load_screen = BasePopup(self, floating=False, dialog=False)
        self.load_widget = LoadingOverlayWidget(
            self, LoadingOverlayWidget.AnimationGIF.DEFAULT
        )
        self.load_screen.add_widget(self.load_widget)

        self.file_data: Files = file_data
        self.filesPage_widget = FilesPage(self)
        self.addWidget(self.filesPage_widget)

        self.BasePopup = BasePopup(self)
        self.BasePopup_z_offset = BasePopup(self, floating=True)

        self.confirmPage_widget = ConfirmWidget(self)
        self.addWidget(self.confirmPage_widget)
        self.confirmPage_widget.back_btn.clicked.connect(self.back_button)
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
        self.filesPage_widget.request_file_metadata.connect(
            self.file_data.request_file_metadata
        )
        self.file_data.fileinfo.connect(self.filesPage_widget.on_fileinfo)

        self.filesPage_widget.request_file_list[str].connect(
            self.file_data.request_file_list
        )
        self.filesPage_widget.request_file_list.connect(
            self.file_data.request_file_list
        )
        self.file_data.on_dirs.connect(self.filesPage_widget.on_directories)
        self.filesPage_widget.request_dir_info[str].connect(
            self.file_data.request_dir_info[str]
        )
        self.filesPage_widget.request_dir_info.connect(self.file_data.request_dir_info)
        self.file_data.on_file_list.connect(self.filesPage_widget.on_file_list)
        self.jobStatusPage_widget = JobStatusWidget(self)
        self.addWidget(self.jobStatusPage_widget)
        self.confirmPage_widget.on_accept.connect(
            self.jobStatusPage_widget.on_print_start
        )
        self.jobStatusPage_widget.show_request.connect(
            lambda: self.change_page(self.indexOf(self.jobStatusPage_widget))
        )
        self.jobStatusPage_widget.hide_request.connect(
            lambda: self.change_page(self.indexOf(self.print_page))
        )
        self.jobStatusPage_widget.request_file_info.connect(
            self.file_data.on_request_fileinfo
        )
        self.file_data.fileinfo.connect(self.jobStatusPage_widget.on_fileinfo)
        self.jobStatusPage_widget.print_start.connect(self.ws.api.start_print)
        self.jobStatusPage_widget.print_resume.connect(self.ws.api.resume_print)
        self.jobStatusPage_widget.print_cancel.connect(self.handle_cancel_print)
        self.jobStatusPage_widget.print_pause.connect(self.ws.api.pause_print)
        self.jobStatusPage_widget.print_finish.connect(self.finish_print_signal)
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
        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)
        self.printer.gcode_move_update[str, list].connect(
            self.jobStatusPage_widget.on_gcode_move_update
        )
        self.printer.request_available_objects_signal.connect(self.klipper_ready_signal)
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
        self.printer.print_stats_update[str, str].connect(
            self.tune_page.on_print_stats_update
        )
        self.printer.gcode_move_update[str, float].connect(
            self.tune_page.on_gcode_move_update
        )
        self.printer.gcode_move_update[str, list].connect(
            self.babystepPage.on_gcode_move_update
        )
        self.printer.gcode_move_update[str, list].connect(self.activate_save_button)
        self.tune_page.run_gcode.connect(self.ws.api.run_gcode)
        self.tune_page.request_sliderPage[str, int, "PyQt_PyObject"].connect(
            self.on_slidePage_request
        )
        self.tune_page.request_sliderPage[str, int, "PyQt_PyObject", int, int].connect(
            self.on_slidePage_request
        )
        self.tune_page.request_numpad[str, int, "PyQt_PyObject", int, int].connect(
            self.on_numpad_request
        )
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
        self.confirmPage_widget.on_delete.connect(self.delete_file)
        self.change_page(self.indexOf(self.print_page))  # force set the initial page
        self.save_config_btn.clicked.connect(self.save_config)
        self.BasePopup_z_offset.accepted.connect(self.update_configuration_file)

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """
        unblocks tabs if on standby
        """
        if isinstance(value, str):
            if "state" in field:
                if value in ("standby"):
                    self.on_cancel_print.emit()

    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", name="on_numpad_request")
    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", int, int, name="on_numpad_request")
    def on_numpad_request(
        self,
        name: str,
        current_value: int,
        callback,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        """Handle numpad request"""
        self.numpadPage.value_selected.connect(callback)
        self.numpadPage.set_name(name)
        self.numpadPage.set_value(current_value)
        self.numpadPage.set_min_value(min_value)
        self.numpadPage.set_max_value(max_value)
        self.numpadPage.firsttime = True
        self.change_page(self.indexOf(self.numpadPage))

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
        """Handle slider page request"""
        self.sliderPage.value_selected.connect(callback)
        self.sliderPage.set_name(name)
        self.sliderPage.set_slider_position(int(current_value))
        self.sliderPage.set_slider_minimum(min_value)
        self.sliderPage.set_slider_maximum(max_value)
        self.change_page(self.indexOf(self.sliderPage))

    @QtCore.pyqtSlot(str, str, name="delete_file")
    @QtCore.pyqtSlot(str, name="delete_file")
    def delete_file(self, filename: str, directory: str = "gcodes") -> None:
        """Handle Delete file signal, shows confirmation dialog"""
        self.BasePopup.set_message("Are you sure you want to delete this file?")
        self.BasePopup.accepted.connect(
            lambda: self._on_delete_file_confirmed(filename, directory)
        )
        self.BasePopup.open()

    def save_config(self) -> None:
        """Handle Save configuration behaviour, shows confirmation dialog"""
        if self._finish_print_handled:
            self.run_gcode_signal.emit("Z_OFFSET_APPLY_PROBE")
            self._z_offset = self._active_z_offset
            self.babystepPage.bbp_z_offset_title_label.setText(
                f"Z: {self._z_offset:.3f}mm"
            )
        self.BasePopup_z_offset.set_message(
            f"The Z‑Offset is now {self._active_z_offset:.3f} mm.\n"
            "Would you like to save this change permanently?\n"
            "The machine will restart."
        )
        self.BasePopup_z_offset.cancel_button_text("Later")
        self.BasePopup_z_offset.open()

    def update_configuration_file(self):
        """Runs the `SAVE_CONFIG` gcode"""
        self.run_gcode_signal.emit("Z_OFFSET_APPLY_PROBE")
        self.run_gcode_signal.emit("SAVE_CONFIG")
        self.BasePopup_z_offset.disconnect()

    @QtCore.pyqtSlot(str, list, name="activate_save_button")
    def activate_save_button(self, name: str, value: list) -> None:
        """Sync the `Save config` popup with the save_config_pending state"""
        if not value:
            return

        if name == "homing_origin":
            self._active_z_offset = value[2]
            self.save_config_btn.setVisible(value[2] != 0)

    def _on_delete_file_confirmed(self, filename: str, directory: str) -> None:
        """Handle confirmed file deletion after user accepted the dialog"""
        self.file_data.on_request_delete_file(filename, directory)
        self.request_back.emit()
        self.filesPage_widget.reset_dir()
        self.BasePopup.disconnect()

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

    def handle_cancel_print(self) -> None:
        """Handles the print cancel action"""
        self.ws.api.cancel_print()
        self.loadscreen.show()
        self.loadscreen.setModal(True)
        self.loadwidget.set_status_message("Cancelling print...\nPlease wait")

    def change_page(self, index: int) -> None:
        """Requests a page change page to the global manager

        Args:
            index (int): page index
        """
        self.request_change_page.emit(0, index)

    @QtCore.pyqtSlot(name="request-back")
    def back_button(self) -> None:
        """Goes back to the previous page"""
        self.request_back.emit()

    @QtCore.pyqtSlot(name="klipper_ready_signal")
    def klipper_ready_signal(self) -> None:
        """React to klipper ready signal"""
        self.babystepPage.baby_stepchange = False
        self._finish_print_handled = False

    @QtCore.pyqtSlot(name="finish_print_signal")
    def finish_print_signal(self) -> None:
        """Behaviour when the print ends — but only once."""
        if self._finish_print_handled:
            return
        if self._active_z_offset != 0 and self.babystepPage.baby_stepchange:
            self.save_config()
            self._finish_print_handled = True

    def setupMainPrintPage(self) -> None:
        """Setup UI for print page"""
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
            QtGui.QPixmap(":/background/media/graphics/scroll_list_window.svg"),
        )
        self.print_page = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.print_page.sizePolicy().hasHeightForWidth())
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
        self.main_print_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.main_print_btn.setStyleSheet("")
        self.main_print_btn.setAutoDefault(False)
        self.main_print_btn.setFlat(True)
        self.main_print_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/print.svg")
        )
        self.main_print_btn.setObjectName("main_print_btn")
        self.save_config_btn = DisplayButton(parent=self.print_page)
        self.save_config_btn.setGeometry(QtCore.QRect(540, 20, 170, 50))
        font.setPointSize(8)
        font.setFamily("Montserrat")
        self.save_config_btn.setFont(font)
        self.save_config_btn.setMouseTracking(False)
        self.save_config_btn.setTabletTracking(True)
        self.save_config_btn.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.save_config_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/save.svg")
        )
        self.save_config_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.save_config_btn.setStyleSheet("")
        self.save_config_btn.setAutoDefault(False)
        self.save_config_btn.setFlat(True)
        self.save_config_btn.setMinimumSize(QtCore.QSize(170, 50))
        self.save_config_btn.setMaximumSize(QtCore.QSize(170, 50))
        self.save_config_btn.setText("Save\nZ-Offset")
        self.save_config_btn.hide()
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
        self.main_text_label.setStyleSheet("background: transparent; color: white;")
        self.main_text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_text_label.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.NoTextInteraction
        )
        self.main_text_label.setObjectName("main_text_label")
        self.addWidget(self.print_page)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("printStackedWidget", "StackedWidget"))
        self.main_print_btn.setText(_translate("printStackedWidget", "Print"))
        self.main_print_btn.setProperty(
            "class", _translate("printStackedWidget", "menu_btn")
        )
        self.main_text_label.setText(_translate("printStackedWidget", "Printer ready"))
