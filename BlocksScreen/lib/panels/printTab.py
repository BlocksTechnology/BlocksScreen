import logging
import os
import pathlib
import typing
from functools import partial

import helper_methods
from configfile import BlocksScreenConfig, get_configparser
from lib.files import Files
from lib.moonrakerComm import MoonWebSocket
from lib.panels.widgets.Common.basePopup import BasePopup
from lib.panels.widgets.metadataPage import FileMetadataWidget
from lib.panels.widgets.Common.numpadPage import CustomNumpad
from lib.panels.widgets.PrintTab.babystepPage import BabystepPage
from lib.panels.widgets.PrintTab.confirmPage import ConfirmWidget
from lib.panels.widgets.PrintTab.filesPage import FilesPage
from lib.panels.widgets.PrintTab.jobStatusPage import JobStatusWidget
from lib.panels.widgets.PrintTab.sensorsPanel import SensorsWindow
from lib.panels.widgets.PrintTab.tunePage import TuneWidget
from lib.panels.widgets.Common.slider_selector_page import SliderPage
from lib.printer import Printer
from lib.utils import gcode_loader
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.display_button import DisplayButton
from lib.utils.usb_import import UsbImportTask, remember_import
from PyQt6 import QtCore, QtGui, QtWidgets

if typing.TYPE_CHECKING:
    from devices.amu import AMUManager

USB_SETTLE_TIMEOUT_MS = 120_000  # Happy Hare pre-processing of a large file

logger = logging.getLogger(__name__)


class PrintTab(QtWidgets.QStackedWidget):
    """Print tab: files, confirm, job status and tuning pages."""

    request_query_print_stats: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="request_query_print_stats"
    )

    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-back"
    )
    request_change_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, int, name="request_change_page"
    )

    request_change_tab: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, name="request_change_tab"
    )

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )
    on_cancel_print: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="on_cancel_print"
    )
    call_load_panel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, str, bool, name="call-load-panel"
    )
    call_cancel_panel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="call-load-panel"
    )
    in_case_error = QtCore.pyqtSignal(name="in-case-error")
    notify: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, int, bool, name="notify"
    )

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        file_data: Files,
        ws: MoonWebSocket,
        printer: Printer,
        amu_manager: "AMUManager | None" = None,
    ) -> None:
        super().__init__(parent)
        self.amu_manager: "AMUManager | None" = amu_manager
        self._active_z_offset: float = 0.0
        self._pending_save_offset: float = 0.0
        self._finish_print_handled: bool = False
        self._cancel_z_snapshot: float = 0.0
        self._z_apply_command: str = "Z_OFFSET_APPLY_ENDSTOP"
        self._usb_import_task: UsbImportTask | None = None
        self._usb_key: str = ""
        self._usb_local: str = ""
        self._usb_created: set[str] = set()
        # Moonraker announces a new gcode only once its pre-processing is done.
        self._usb_settle_timer = QtCore.QTimer(self)
        self._usb_settle_timer.setSingleShot(True)
        self._usb_settle_timer.setInterval(USB_SETTLE_TIMEOUT_MS)
        self._usb_settle_timer.timeout.connect(self._on_usb_settle_timeout)

        self.setupMainPrintPage()
        self.ws: MoonWebSocket = ws
        # Embedded-thumbnail fallback for USB gcodes.
        gcode_loader.configure(ws._moonRest)
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

        self.metadataPage_widget = FileMetadataWidget(self)
        self.addWidget(self.metadataPage_widget)
        self.confirmPage_widget.show_metadata.connect(
            self.metadataPage_widget.on_show_widget
        )
        self.confirmPage_widget.show_metadata.connect(
            lambda: self.change_page(self.indexOf(self.metadataPage_widget))
        )
        self.confirmPage_widget.show_metadata.connect(
            self.file_data.request_print_duration
        )
        self.metadataPage_widget.back_btn.clicked.connect(self.back_button)
        self.file_data.fileinfo.connect(self.filesPage_widget.on_fileinfo)
        self.file_data.fileinfo.connect(self.confirmPage_widget.on_fileinfo)
        self.file_data.fileinfo.connect(self.metadataPage_widget.on_fileinfo)

        self.file_data.on_dirs.connect(self.filesPage_widget.on_directories)

        self.filesPage_widget.request_dir_info[str].connect(
            self.file_data.request_dir_info[str]
        )
        self.filesPage_widget.request_dir_info.connect(self.file_data.request_dir_info)
        self.file_data.on_file_list.connect(self.filesPage_widget.on_file_list)
        self.file_data.file_added.connect(self.filesPage_widget.on_file_added)
        self.file_data.file_added.connect(self._on_usb_file_added)
        self.file_data.file_removed.connect(self.filesPage_widget.on_file_removed)
        self.file_data.file_modified.connect(self.filesPage_widget.on_file_modified)
        self.file_data.dir_added.connect(self.filesPage_widget.on_dir_added)
        self.file_data.dir_removed.connect(self.filesPage_widget.on_dir_removed)
        self.file_data.full_refresh_needed.connect(
            self.filesPage_widget.on_full_refresh_needed
        )
        self.file_data.usb_files_loaded.connect(
            self.filesPage_widget.on_usb_files_loaded
        )
        self.jobStatusPage_widget = JobStatusWidget(self)
        self.in_case_error.connect(self.jobStatusPage_widget.handleErrors)
        self.addWidget(self.jobStatusPage_widget)
        self.confirmPage_widget.on_accept.connect(self.start_print)
        self.jobStatusPage_widget.show_request.connect(
            lambda: self.change_page(self.indexOf(self.jobStatusPage_widget))
        )
        self.jobStatusPage_widget.call_cancel_panel.connect(self.call_cancel_panel)
        self.jobStatusPage_widget.hide_request.connect(
            lambda: self.change_page(self.indexOf(self.print_page))
        )
        self.jobStatusPage_widget.show_metadata.connect(
            self.metadataPage_widget.on_show_widget
        )
        self.jobStatusPage_widget.show_metadata.connect(
            lambda: self.change_page(self.indexOf(self.metadataPage_widget))
        )
        self.jobStatusPage_widget.show_metadata.connect(
            self.file_data.request_print_duration
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
        self.printer.flowguard_update.connect(
            self.jobStatusPage_widget.on_flowguard_update
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
        self.tune_page.tune_change_filament_btn.clicked.connect(
            lambda: self.request_change_page.emit(1, 2)
        )
        self.jobStatusPage_widget.tune_clicked.connect(
            lambda: self.change_page(self.indexOf(self.tune_page))
        )
        self.tune_page.request_back.connect(self.back_button)
        self.printer.printer_config.connect(self.tune_page.on_printer_config)
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
        self.printer.print_stats_update[str, str].connect(
            self.babystepPage.on_print_state_update
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
        self.ws.klippy_state_signal.connect(self.on_klippy_state)

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """Unblock tabs if on standby."""
        if isinstance(value, str) and "state" in field and value == "standby":
            self.call_load_panel.emit(False, "", False)
            self.on_cancel_print.emit()
            if not self._finish_print_handled and self._cancel_z_snapshot != 0:
                self._active_z_offset = self._cancel_z_snapshot
                self.save_config()
                self._finish_print_handled = True
                self.save_config_btn.setVisible(True)
            self._cancel_z_snapshot = 0.0

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
        try:
            self.numpadPage.value_selected.disconnect()
        except (RuntimeError, TypeError):
            pass
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
        try:
            self.sliderPage.value_selected.disconnect()
        except (RuntimeError, TypeError):
            pass
        self.sliderPage.value_selected.connect(callback)
        self.sliderPage.set_name(name)
        self.sliderPage.set_slider_minimum(min_value)
        self.sliderPage.set_slider_maximum(max_value)
        self.sliderPage.set_slider_position(int(current_value))
        self.change_page(self.indexOf(self.sliderPage))

    @QtCore.pyqtSlot(str, name="start_print")
    def start_print(self, file: str) -> None:
        """Start *file* on the job status page unless PRINT_START would refuse it."""
        # A refused PRINT_START runs on_error CANCEL_PRINT, which HH v3 reopens as a job.
        if self.amu_manager is not None and (
            reason := self.amu_manager.print_start_refusal()
        ):
            logger.warning("Print start of %s blocked: %s", file, reason)
            self.notify.emit("PrintTab", reason, 2, True)
            return
        if helper_methods.is_usb_path(file):
            self._start_usb_import(file)
            return
        self.jobStatusPage_widget.on_print_start(file)

    def _start_usb_import(self, file: str) -> None:
        """Copy a USB gcode to the gcodes root off-thread, then print the copy."""
        # Printing from the stick would fail mid-job if it is pulled or glitches.
        if self._usb_import_task is not None:
            logger.info("USB import already running, ignoring %s", file)
            return
        self._usb_created.clear()
        self._usb_import_task = UsbImportTask(pathlib.Path(self.gcode_path), file)
        self._usb_import_task.signals.done.connect(self._on_usb_import_done)
        self.call_load_panel.emit(True, "Copying file from USB...\nPlease wait", False)
        QtCore.QThreadPool.globalInstance().start(self._usb_import_task)

    @QtCore.pyqtSlot(str, str, str, bool, str, name="on_usb_import_done")
    def _on_usb_import_done(
        self, usb_file: str, local_file: str, key: str, reused: bool, error: str
    ) -> None:
        """Print a reused copy now, a new one once Moonraker has processed it."""
        if error:
            self._usb_import_task = None
            self.call_load_panel.emit(False, "", False)
            self.notify.emit("PrintTab", f"USB print failed: {error}", 2, True)
            return
        logger.info("Local copy of %s is %s", usb_file, local_file)
        self._usb_key, self._usb_local = key, local_file
        # Printing before Happy Hare rewrites the file runs the unprocessed gcode.
        if reused or local_file in self._usb_created:
            self._usb_print_local_copy()
        else:
            self._usb_settle_timer.start()

    @QtCore.pyqtSlot(dict, name="on_usb_file_added")
    def _on_usb_file_added(self, item: dict) -> None:
        """Release a waiting USB print when Moonraker announces its local copy."""
        if self._usb_import_task is None:
            return
        name = str(item.get("path", "")).removeprefix("/")
        self._usb_created.add(name)  # may beat the worker's done signal
        if name == self._usb_local:
            self._usb_print_local_copy()

    @QtCore.pyqtSlot(name="on_usb_settle_timeout")
    def _on_usb_settle_timeout(self) -> None:
        """Print anyway if Moonraker never announced the copy."""
        logger.warning("No create_file for %s, printing it as is", self._usb_local)
        self._usb_print_local_copy()

    def _usb_print_local_copy(self) -> None:
        """Index the settled local copy and start printing it."""
        self._usb_settle_timer.stop()
        local = self._usb_local
        try:
            remember_import(pathlib.Path(self.gcode_path), self._usb_key, local)
        except OSError as e:
            logger.warning("Could not index USB copy %s: %s", local, e)
        self._usb_import_task = None
        self._usb_key = self._usb_local = ""
        self.call_load_panel.emit(False, "", False)
        logger.info("Printing local copy %s", local)
        self.jobStatusPage_widget.on_print_start(local)

    @QtCore.pyqtSlot(str, str, name="delete_file")
    @QtCore.pyqtSlot(str, name="delete_file")
    def delete_file(self, filename: str, directory: str = "gcodes") -> None:
        """Handle Delete file signal, shows confirmation dialog."""
        self.BasePopup.set_message("Are you sure you want to delete this file?")
        try:
            self.BasePopup.accepted.disconnect()
        except (RuntimeError, TypeError):
            pass
        self.BasePopup.accepted.connect(
            lambda: self._on_delete_file_confirmed(filename, directory)
        )
        self.BasePopup.open()

    def save_config(self) -> None:
        """Handle Save configuration behaviour, shows confirmation dialog"""
        self._pending_save_offset = self._active_z_offset
        self.BasePopup_z_offset.set_message(
            f"The Z-Offset is now {self._pending_save_offset + 0.0:.3f} mm.\n"
            "Would you like to save this change permanently?\n"
            "The machine will restart."
        )
        self.BasePopup_z_offset.cancel_button_text("Later")
        try:
            self.BasePopup_z_offset.accepted.disconnect(self.update_configuration_file)
        except (RuntimeError, TypeError):
            pass
        self.BasePopup_z_offset.accepted.connect(self.update_configuration_file)
        self.BasePopup_z_offset.open()

    def update_configuration_file(self) -> None:
        """Runs the `SAVE_CONFIG` gcode"""
        try:
            self.BasePopup_z_offset.accepted.disconnect(self.update_configuration_file)
        except (RuntimeError, TypeError):
            pass
        self.run_gcode_signal.emit(
            f"SET_GCODE_OFFSET Z={self._pending_save_offset:.3f} MOVE=0"
        )
        self.run_gcode_signal.emit(self._z_apply_command)
        self.run_gcode_signal.emit("SAVE_CONFIG")
        self.babystepPage.bbp_z_offset_title_label.setText(
            f"Z: {self._pending_save_offset + 0.0:.3f}mm"
        )
        self.save_config_btn.setVisible(False)

    @QtCore.pyqtSlot(str, name="on_klippy_state")
    def on_klippy_state(self, state: str) -> None:
        """Dismiss the Z-offset save popup and reset save state on unexpected shutdown."""
        if state in ("ready", "startup"):
            return
        self.BasePopup_z_offset.reject()
        self.save_config_btn.setVisible(False)
        self.babystepPage.baby_stepchange = False

    @QtCore.pyqtSlot(str, list, name="activate_save_button")
    def activate_save_button(self, name: str, value: list) -> None:
        """Sync the `Save config` popup with the save_config_pending state"""
        if not value or name != "homing_origin" or len(value) <= 2:
            return
        self._active_z_offset = value[2]
        self.save_config_btn.setVisible(
            not self.printer.uses_true_zero_offset and round(value[2], 3) != 0
        )

    def _on_delete_file_confirmed(self, filename: str, directory: str) -> None:
        """Handle confirmed file deletion after user accepted the dialog."""
        self.file_data.on_request_delete_file(filename, directory)
        self.request_back.emit()
        self.filesPage_widget.reset_dir()
        try:
            self.BasePopup.accepted.disconnect()
        except (RuntimeError, TypeError):
            pass

    def handle_cancel_print(self) -> None:
        """Handles the print cancel action"""
        if (
            not self._finish_print_handled
            and not self.printer.uses_true_zero_offset
            and self._active_z_offset != 0
            and self.babystepPage.baby_stepchange
        ):
            self._cancel_z_snapshot = self._active_z_offset
        self.ws.api.cancel_print()
        self.call_load_panel.emit(True, "Cancelling print...\nPlease wait", False)

    def change_page(self, index: int) -> None:
        """Request page change to global manager."""
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
        self._cancel_z_snapshot = 0.0
        self.printer.on_subscribe_config("stepper_z", self._on_stepper_z_config)

    def _on_stepper_z_config(self, config: dict | list) -> None:
        """Select the correct Z-offset apply command based on endstop type."""
        if not isinstance(config, dict):
            return
        stepper_z = config.get("stepper_z", {})
        if stepper_z.get("endstop_pin") == "probe:z_virtual_endstop":
            self._z_apply_command = "Z_OFFSET_APPLY_PROBE"
        else:
            self._z_apply_command = "Z_OFFSET_APPLY_ENDSTOP"

    @QtCore.pyqtSlot(name="finish_print_signal")
    def finish_print_signal(self) -> None:
        """Behaviour when the print ends — but only once."""
        if self._finish_print_handled:
            return
        self.on_cancel_print.emit()
        if self._active_z_offset != 0 and self.babystepPage.baby_stepchange:
            if not self.printer.uses_true_zero_offset:
                self.save_config()
            self._finish_print_handled = True
        self.save_config_btn.setVisible(
            not self.printer.uses_true_zero_offset
            and round(self._active_z_offset, 3) != 0
        )

    def setupMainPrintPage(self) -> None:
        """Setup UI for print page"""
        self.setObjectName("print_tab")
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
        self.main_print_btn.setText(_translate("printStackedWidget", "Print"))
        self.main_print_btn.setProperty(
            "class", _translate("printStackedWidget", "menu_btn")
        )
        self.main_text_label.setText(_translate("printStackedWidget", "Printer ready"))
