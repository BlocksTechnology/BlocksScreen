import math
import os
import typing
from functools import partial

from lib.bo.files import Files
from lib.bo.printer import Printer
from lib.moonrakerComm import MoonWebSocket
from lib.panels.sensorsWindow import SensorsWindow
from lib.ui.printStackedWidget_ui import Ui_printStackedWidget
from lib.ui.slider_selector_page import SliderPage
from PyQt6 import QtCore, QtGui, QtWidgets
from utils.blocks_button import BlocksCustomButton
from utils.display_button import DisplayButton


class PrintTab(QtWidgets.QStackedWidget):
    """PrintTab -> QStackedWidget UI panel that has the following panels:

    - Main page: Simple page with a message field and a button to start a print;
    - File list page: A file list where displayed files are selectable to be printed;
    - Confirm page: A page to confirm or not if the selected file is to be printed;
    - Print page: A page for controlling the ongoing job, Pause/Resume and stop functionality
    - Tune page: Accessible only from the print page;
    - Babystep page: Control the z_offset during a ongoing print;
    - Change page: A page that permits changing the filament, stops the print -> change the filament -> resume the print;

    On the tune page, the user can additionally change the temperature/speed of the extruder(s), heated bed, fan(s) and the print velocity

    Args:
        QStackedWidget (QStackedWidget): This class is inherited from QStackedWidget from Qt6

    __init__:
        parent (QWidget | QObject): The parent for this tab.
        file_data (Files): Class object that handles printer files.
        ws (MoonWebSocket): Moonraker websocket instance.
        printer (Printer): Class object that handles printer objects information.

    """

    request_file_thumbnail: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(str, name="get_file_thumbnail")
    )
    request_print_file_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(str, name="start_print")
    )
    request_print_resume_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="resume_print")
    )
    request_print_stop_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="stop_print")
    )
    request_print_pause_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="pause_print")
    )
    request_query_print_stats: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(dict, name="request_query_print_stats")
    )
    request_block_manual_tab_change: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="block_manual_tab_change")
    )
    request_activate_manual_tab_change: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="activate_manual_tab_change")
    )
    request_back_button_pressed: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="request_back_button_pressed")
    )
    request_change_page: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(int, int, name="request_change_page")
    )
    printer_state_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(str, name="printer_state_updated")
    )
    verify_printer_state_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="verify_printer_state")
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )
    request_numpad_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(
            int,
            str,
            str,
            "PyQt_PyObject",
            QtWidgets.QStackedWidget,
            name="request_numpad",
        )
    )

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        file_data: Files,
        ws: MoonWebSocket,
        printer: Printer,
    ) -> None:
        # super(PrintTab, self).__init__(parent)
        super().__init__(parent)
        self.panel = Ui_printStackedWidget()
        self.panel.setupUi(self)
        self.change_page(
            self.indexOf(self.panel.print_page)
        )  # force set the initial page

        self.file_data: Files = file_data
        self.ws: MoonWebSocket = ws
        self.printer: Printer = printer

        self._internal_print_status: str = ""
        self._current_z_position: float = 0.0
        self.speed_factor_override: float = 100.0
        self._current_file_name: str = ""
        self._z_offset: float = 0.05
        self.tune_display_buttons: dict = {}

        self.setMouseTracking(True)
        self.sensorsPanel = SensorsWindow(self)
        self.addWidget(self.sensorsPanel)

        self.panel.sensors_menu_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.sensorsPanel))
        )
        self.printer.request_object_subscription_signal.connect(
            self.sensorsPanel.handle_available_fil_sensors
        )
        self.sensorsPanel.panel.fs_back_button.clicked.connect(
            self.back_button
        )
        self.sensorsPanel.run_gcode_signal.connect(self.ws.api.run_gcode)

        self.printer.filament_motion_sensor_update.connect(
            self.sensorsPanel.handle_fil_state_change
        )
        self.printer.filament_switch_sensor_update.connect(
            self.sensorsPanel.handle_fil_state_change
        )

        # TODO: Get the gcode path from the configfile by asking the websocket first
        self.gcode_path = os.path.expanduser("~/printer_data/gcodes")
        self.currentChanged.connect(self.view_changed)
        self.panel.listWidget.itemClicked.connect(self.fileItemClicked)
        self.panel.confirm_no_text_label.clicked.connect(self.back_button)
        self.panel.confirm_yes_text_label.clicked.connect(self.print_start)
        self.request_print_file_signal.connect(self.ws.api.start_print)
        self.request_print_stop_signal.connect(self.ws.api.cancel_print)
        self.request_print_resume_signal.connect(self.ws.api.resume_print)
        self.request_print_pause_signal.connect(self.ws.api.pause_print)
        self.request_query_print_stats.connect(self.ws.api.object_query)
        self.panel.stop_printing_btn.clicked.connect(
            self.request_print_stop_signal.emit
        )
        self.panel.pause_printing_btn.clicked.connect(self.pause_resume_print)

        self.panel.main_print_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.files_page))
        )
        self.panel.tune_menu_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.tune_page))
        )
        self.panel.tune_babystep_menu_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.babystep_page))
        )
        # File List Screen
        self.request_file_thumbnail.connect(self.file_data.get_file_thumbnail)
        self.panel.back_btn.clicked.connect(self.back_button)
        self.panel.tune_back_btn.clicked.connect(self.back_button)
        self.panel.babystep_back_btn.clicked.connect(self.back_button)
        self.printer.virtual_sdcard_update[str, bool].connect(
            self.virtual_sdcard_update
        )
        self.printer.virtual_sdcard_update[str, float].connect(
            self.virtual_sdcard_update
        )
        self.printer.virtual_sdcard_update.connect(self.virtual_sdcard_update)
        self.printer.print_stats_update[str, str].connect(
            self.on_print_stats_update
        )
        self.printer.print_stats_update[str, dict].connect(
            self.on_print_stats_update
        )
        self.printer.print_stats_update[str, float].connect(
            self.on_print_stats_update
        )
        self.printer.idle_timeout_update[str, str].connect(
            self.on_idle_timeout_update
        )
        self.printer.idle_timeout_update[str, float].connect(
            self.on_idle_timeout_update
        )
        self.printer.idle_timeout_update.connect(self.on_idle_timeout_update)
        self.printer.display_update[str, str].connect(self.on_display_update)
        self.printer.display_update[str, float].connect(self.on_display_update)
        self.printer.gcode_move_update[str, list].connect(
            self.on_gcode_move_update
        )
        self.printer.gcode_move_update[str, bool].connect(
            self.on_gcode_move_update
        )
        self.printer.gcode_move_update[str, float].connect(
            self.on_gcode_move_update
        )

        self.panel.bbp_close_to_bed.clicked.connect(
            self.move_nozzle_close_to_bed
        )
        self.panel.bbp_away_from_bed.clicked.connect(
            self.move_nozzle_far_to_bed
        )
        self.panel.bbp_nozzle_offset_01.toggled.connect(
            self.handle_z_offset_change
        )
        self.panel.bbp_nozzle_offset_025.toggled.connect(
            self.handle_z_offset_change
        )
        self.panel.bbp_nozzle_offset_05.toggled.connect(
            self.handle_z_offset_change
        )
        self.panel.bbp_nozzle_offset_1.toggled.connect(
            self.handle_z_offset_change
        )

        self.run_gcode_signal.connect(self.ws.api.run_gcode)
        # @ Get the temperatures for the objects
        self.printer.extruder_update.connect(
            self.on_extruder_temperature_change
        )
        self.printer.heater_bed_update.connect(
            self.on_heater_bed_temperature_change
        )
        self.printer.fan_update[str, str, float].connect(
            self.on_fan_object_update
        )
        self.printer.fan_update[str, str, int].connect(
            self.on_fan_object_update
        )
        # Numpad
        self.panel.bed_display.clicked.connect(
            partial(
                self.request_numpad_signal.emit,
                0,
                "heater_bed",
                self.panel.bed_display.text(),
                self.handle_numpad_change,
                self,
            )
        )
        self.panel.extruder_display.clicked.connect(
            partial(
                self.request_numpad_signal.emit,
                0,
                "extruder",
                self.panel.extruder_display.text(),
                self.handle_numpad_change,
                self,
            )
        )

        self.slider_page = SliderPage(self)
        self.addWidget(self.slider_page)
        self.slider_page.request_back.connect(self.back_button)

        self.panel.speed_display.clicked.connect(
            lambda: (
                self.change_page(self.indexOf(self.slider_page)),
                self.slider_page.set_name("Speed"),
                self.slider_page.set_slider_pos(
                    self.speed_factor_override * 100
                ),
            )[-1]
        )

        self.panel.ReloadButton.clicked.connect(
            lambda: (
                self.file_data.request_file_list.emit(),
                self.add_file_entries(),
            )[-1]
        )

    @QtCore.pyqtSlot(str, int, name="numpad_new_value")
    @QtCore.pyqtSlot(str, float, name="numpad_new_value")
    def handle_numpad_change(self, name: str, new_value: int | float) -> None:
        """Handles inputs form numpad
        Args:
            name (str): Name of the object that is to be updated
            new_value (int | float): New value for the object
        """
        if isinstance(new_value, float):
            if name.startswith("fan") and 0 <= new_value <= 100:
                _new_range = int((new_value / 100) * 255)
                self.run_gcode_signal.emit(f"M106 S{_new_range}")
            elif name.startswith("speed") and 0 <= new_value <= 10000:
                self.run_gcode_signal.emit(f"M220 S{int(new_value)}")
                self.speed_factor_override = new_value

        elif isinstance(new_value, int):
            self.run_gcode_signal.emit(
                f"SET_HEATER_TEMPERATURE HEATER={name} TARGET={new_value}"
            )

    @QtCore.pyqtSlot(str, str, float, name="on_fan_update")
    @QtCore.pyqtSlot(str, str, int, name="on_fan_update")
    def on_fan_object_update(
        self, name: str, field: str, new_value: int | float
    ) -> None:
        """Parse information from fan printer objects

        Args:
            name (str): Name of the fan object
            field (str): Name of the updated field
            new_value (int | float): New value for field
        """
        if "speed" in field:
            # Dynamically get the button name (always ends with {fan name}_display)

            if hasattr(self.panel, f"{name}_display"):
                _fan_display = getattr(self.panel, f"{name}_display")

            if not self.tune_display_buttons.get(name):
                _new_display_button = self.create_display_button(name)
                _new_display_button.setParent(self.panel.tune_page)
                _new_display_button.setMinimumSize(QtCore.QSize(150, 60))
                _new_display_button.setMaximumSize(QtCore.QSize(150, 60))
                self.panel.tune_display_buttons_layout.addWidget(
                    _new_display_button
                )

                if "blower" in name:
                    _new_display_button.icon_pixmap = QtGui.QPixmap(
                        ":/temperature_related/media/btn_icons/blower.svg"
                    )
                else:
                    _new_display_button.icon_pixmap = QtGui.QPixmap(
                        ":/temperature_related/media/btn_icons/fan.svg"
                    )

                _new_display_button.clicked.connect(
                    lambda: (
                        self.change_page(self.indexOf(self.slider_page)),
                        self.slider_page.set_name(str(name)),
                        self.slider_page.set_slider_pos(
                            self.tune_display_buttons.get(name).get("speed")  # type: ignore
                        ),
                    )[-1]
                )
                self.tune_display_buttons.update(
                    {
                        name: {
                            "display_button": _new_display_button,
                            "speed": -1,
                        }
                    }
                )
                self.panel.tune_display_buttons_layout.addWidget(
                    _new_display_button
                )

            _display_button = self.tune_display_buttons.get(name)
            if not _display_button:
                return
            _display_button.update({"speed": f"{new_value * 100:.0f}"})
            _display_button.get("display_button").setText(
                f"{new_value * 100:.0f}"
            )

    def create_display_button(self, name: str) -> DisplayButton:
        """Creates a DisplayButton and returns it

        Args:
            name (str): Name for the display button

        Returns:
            DisplayButton: The created DisplayButton object
        """
        _display_button = DisplayButton()
        _display_button.setObjectName(str(name + "_display"))
        _display_button.setMinimumSize(QtCore.QSize(150, 40))
        _display_button.setMaximumSize(QtCore.QSize(150, 60))
        _display_button.setText("")
        _display_button.setCheckable(False)
        _display_button.setFlat(True)
        return _display_button

    @QtCore.pyqtSlot(str, str, float, name="on_extruder_update")
    def on_extruder_temperature_change(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        """Processes the information that comes from the printer object "extruder"

        Args:
            extruder_name (str): Name of the extruder object
            field (str): Name of the updated field
            new_value (float): New value for the field
        """
        if field == "temperature":
            self.panel.extruder_display.setText(f"{new_value:.1f}")

    @QtCore.pyqtSlot(str, str, float, name="on_heater_bed_update")
    def on_heater_bed_temperature_change(
        self, name: str, field: str, new_value: float
    ) -> None:
        """Processes the information that comes from the printer object "heater_bed"

        Args:
            name (str): Name of the heater bed object.
            field (str): Name od the updated field.
            new_value (float): New value for the fields.
        """
        if field == "temperature":
            self.panel.bed_display.setText(f"{new_value:.1f}")

    @QtCore.pyqtSlot(str, str, float)
    @QtCore.pyqtSlot(str, str, name="on_idle_timeout_update")
    @QtCore.pyqtSlot(str, float, name="on_idle_timeout_update")
    def on_idle_timeout_update(self, field: str, value: int | float) -> None:
        """Processes the information that comes form the printer object "idle_timeout"

        Args:
            field (str): Name of the updated field.
            value (int | float): New value for the field.
        """
        pass

    @QtCore.pyqtSlot(str, float, name="on_gcode_move_update")
    @QtCore.pyqtSlot(str, bool, name="on_gcode_move_update")
    @QtCore.pyqtSlot(str, list, name="on_gcode_move_update")
    def on_gcode_move_update(
        self, field: str, value: bool | float | list
    ) -> None:
        """Processes the information that comes from the printer object "gcode_move"

        Args:
            field (str): Name of the updated field
            value (bool | float | list): New value for the field
        """
        if isinstance(value, list):
            if "gcode_position" in field:  # Without offsets
                self._current_z_position = value[2]
                if self._internal_print_status == "printing":
                    self._calculate_current_layer(z_position=value[2])
            elif (
                "homing_origin" in field
            ):  # The actual amount of offset applied to each axis
                if self.panel.babystep_page.isVisible():
                    self.panel.bbp_z_offset_current_value.setText(
                        str(value[2]) if value[2] is not None else "?"
                    )

        if isinstance(value, float):
            if "speed_factor" in field:
                self.speed_factor_override = value
                self.panel.speed_display.setText(str(f"{value * 100}%"))

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(
        self, field: str, value: dict | float | str
    ) -> None:
        """Processes the information that comes from the printer object "print_stats"
            Displays information on the ui accordingly.

        Args:
            field (str): The name of the updated field.
            value (dict | float | str): The value for the field.
        """
        if isinstance(value, str):
            if "filename" in field:
                # self.panel.cf_file_name.setText(str(value))
                self._current_file_name = value
                if (
                    self.panel.js_file_name_label.text().lower()
                    != value.lower()
                ):
                    self.panel.js_file_name_label.setText(
                        self._current_file_name
                    )

            if "state" in field:
                if value.lower() == "printing" or value == "paused":
                    self.request_query_print_stats.emit(
                        {"print_stats": ["filename"]}
                    )

                    self.show_print_page()
                    print("HERE")
                elif value in ("cancelled", "complete", "error", "standby"):
                    # TODO: Print cancelled or complete or standby

                    self._current_file_name = ""
                    self._current_z_position = 0
                    self.change_page(0)
                self._internal_print_status = value

        if self.panel.job_status_page.isVisible() and (
            self._internal_print_status == "printing"
            or self._internal_print_status == "paused"
        ):
            _file_metadata = self.file_data.files_metadata.get(
                self._current_file_name
            )
            if _file_metadata is None:
                return
            self.panel.layer_display_button.secondary_text = (  # type:ignore
                _file_metadata.get("layer_count", "?")
            )
            if isinstance(value, dict):
                if "total_layer" in value.keys():
                    # Only available if SET_PRINT_STATS_INFO TOTAL_LAYER=<value>
                    # gcode command is ran
                    if value["total_layer"] is not None:
                        _total_layers = value["total_layer"]
                        self.panel.layer_display_button.secondary_text = (  # type:ignore
                            str(_total_layers)
                        )

                if "current_layer" in value.keys():
                    # Only available if SET_PRINT_STATS_INFO CURRENT_LAYER=<value>
                    # gcode command is ran
                    if value["current_layer"] is not None:
                        _current_layer = value["current_layer"]
                        if _current_layer is not None:
                            self.panel.layer_display_button.setText(
                                f"{int(_current_layer)}"
                                if _current_layer != -1
                                else "?"
                            )

            elif isinstance(value, float):
                if "total_duration" in field:
                    self.print_total_duration = value
                    _time = self._estimate_print_time(
                        int(self.print_total_duration)
                    )
                    _print_time_string = (
                        f"{_time[0]}Day {_time[1]}H {_time[2]}min {_time[3]} s"
                        if _time[0] != 0
                        else f"{_time[1]}H {_time[2]}min {_time[3]}s"
                    )
                    self.panel.print_time_display_button.setText(
                        _print_time_string
                    )
                elif "print_duration" in field:
                    self.current_print_duration_seconds = value
                    # _time = self._estimate_print_time(
                    #     int(self.current_print_duration_seconds)
                    # )
                    # _print_time_string = (
                    #     f"{_time[0]}Day {_time[1]}H {_time[2]}min {_time[3]} s"
                    #     if _time[0] != 0
                    #     else f"{_time[1]}H {_time[2]}min {_time[3]}s"
                    # )
                    # self.panel.remaining_time_text_label.setText(_print_time_string)
                elif "filament_used" in field:
                    self.filament_used_mm = value

    @QtCore.pyqtSlot(str, float, name="virtual_sdcard_update")
    @QtCore.pyqtSlot(str, bool, name="virtual_sdcard_update")
    def virtual_sdcard_update(self, field: str, value: float | bool) -> None:
        """Slot for incoming printer object virtual_sdcard information update

        Args:
            field (str): Name of the updated field on the virtual_sdcard object
            value (float | bool): The updated information for the corresponding field
        """
        if isinstance(value, bool):
            self.sdcard_read = value
        elif isinstance(value, float):
            if "progress" == field:
                self.print_progress = value
                self.panel.printing_progress_bar.setValue(
                    int(math.trunc(self.print_progress * 100))
                )
                self.panel.progress_value_label.setText(
                    f"{math.trunc(self.print_progress * 100)}"
                )

    @QtCore.pyqtSlot(str, str, name="on_display_update")
    @QtCore.pyqtSlot(str, float, name="on_display_update")
    def on_display_update(self, field: str, value: str | float) -> None:
        """Slot for incoming printer object display information update

        Args:
            field (str): Name of the update field on the display object
            value (str | float ): The updated information for the corresponding field
        """
        if isinstance(value, float):
            # * Print progress as per M73
            if "progress" in field:
                pass
        elif isinstance(value, str):
            pass

    def print_start(self) -> None:
        """Start a print job, **INTERNAL USE ONLY**"""
        self.request_print_file_signal.emit(self._current_file_name)
        self.show_print_page()

    def show_print_page(self) -> None:
        """Helper method to change the current panel to the printing page"""
        if (
            not self.panel.job_status_page.isVisible()
            and self._current_file_name
        ):
            print(self._current_file_name)
            self.total_layers = "?"
            self.panel.js_file_name_label.setText(self._current_file_name)

            self.panel.printing_progress_bar.reset()
            self._internal_print_status = "printing"

            # self.total_layers = self.file_data.files_metadata.get(self._current_file_name).get("layer_count", "?")
            # TEST: Sometimes when adding a new file, when the screen is running, the gui fails to get the file's metadata and results in an error
            _file_metadata = self.file_data.files_metadata.get(
                self._current_file_name
            )
            if _file_metadata:
                self.total_layers = str(_file_metadata.get("layer_count", "?"))

            self.panel.layer_display_button.secondary_text = str(
                self.total_layers
            )
            self.change_page(self.indexOf(self.panel.job_status_page))

    @QtCore.pyqtSlot(name="pause_resume_print")
    def pause_resume_print(self) -> None:
        """Handles what signal to emit to the printer when a printing job is ongoing

        Can either be:

        - A pause is suppose to happen -> request a pause

        - A resume is suppose to happen -> request a resume
        """
        if self._internal_print_status == "printing":
            self.request_print_pause_signal.emit()
            self._internal_print_status = "paused"
            self.panel.pause_printing_btn.setText("Pause")
            self.panel.pause_printing_btn.setIconPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/pause.svg")
            )
        elif self._internal_print_status == "paused":
            self.request_print_resume_signal.emit()
            self._internal_print_status = "printing"
            self.panel.pause_printing_btn.setText("Resume")
            self.panel.pause_printing_btn.setIconPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/resume.svg")
            )

            # TODO: Set pixmap change the icon

    def add_file_entries(self) -> None:
        """Inserts the currently available gcode files on the QListWidget"""
        self.panel.listWidget.clear()
        index = 0
        print("here")
        for item in self.file_data.file_list:
            # TODO: Add a file icon before the name
            _item = QtWidgets.QListWidgetItem()
            _item_widget = QtWidgets.QWidget()
            _item_layout = QtWidgets.QHBoxLayout()
            _item_text = QtWidgets.QLabel()
            _item_text.setText(str(item["path"]))
            _item_text.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignLeft
                & QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            _item_layout.addWidget(_item_text)
            _item_widget.setLayout(_item_layout)
            _item.setSizeHint(_item_widget.sizeHint())
            _item.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.panel.listWidget.addItem(_item)
            self.panel.listWidget.setItemWidget(_item, _item_widget)
            index += 1

    @QtCore.pyqtSlot(name="request_nozzle_close_to_bed")
    def move_nozzle_close_to_bed(self) -> None:
        """Slot for Babystep button to get closer to the bed."""
        self.run_gcode_signal.emit(
            f"SET_GCODE_OFFSET Z_ADJUST=-{self._z_offset} MOVE=1"  # Z_ADJUST adds the value to the existing offset
        )

    @QtCore.pyqtSlot(name="request_nozzle_far_to_bed")
    def move_nozzle_far_to_bed(self) -> None:
        """Slot for Babystep button to get far from the bed."""
        self.run_gcode_signal.emit(
            f"SET_GCODE_OFFSET Z_ADJUST=+{self._z_offset} MOVE=1"  # Z_ADJUST adds the value to the existing offset
        )

    @QtCore.pyqtSlot(name="handle_z_offset_change")
    def handle_z_offset_change(self) -> None:
        """Helper method for changing the value for Babystep.

        When a button is clicked, and the button has the mm value i the text,
        it'll change the internal value **z_offset** to the same has the button

        ***

        Possible values are: 0.01, 0.025, 0.05, 0.1 **mm**
        """
        _possible_z_values: typing.List = [0.01, 0.025, 0.05, 0.1]
        _sender: QtCore.QObject | None = self.sender()
        if _sender is not None and isinstance(_sender, QtWidgets.QLabel):
            if float(_sender.text()) in _possible_z_values:
                if self._z_offset == float(_sender.text()):
                    return
                self._z_offset = float(_sender.text())

    @QtCore.pyqtSlot(int, name="currentChanged")
    def view_changed(self, window_index: int) -> None:
        """Slot for the currentChanged signal

        It receives an index which represents the current window showing

        Args:
            window_index (int): Current QStackedWidget index

        """
        if window_index == 1:
            # * On files panel
            self.add_file_entries()

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem, name="file_item_clicked")
    def fileItemClicked(self, item: QtWidgets.QListWidgetItem) -> None:
        """Slot for List Item clicked

        Args:
            item (QListWidgetItem): Clicked item
        """
        # * Get the filename from the list item pressed
        _current_item: QtWidgets.QWidget = self.panel.listWidget.itemWidget(
            item
        )
        if _current_item is not None:
            self._current_file_name = _current_item.findChild(
                QtWidgets.QLabel
            ).text()  # type: ignore
            if self._current_file_name:
                self.panel.cf_file_name.setText(str(self._current_file_name))
            self.change_page(self.indexOf(self.panel.confirm_page))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """
        REFACTOR: Instead of using a background svg pixmap just draw the
                background with with the correct styles and everything
        """
        # if self.panel.files_page.isVisible():

        #     painter = QtGui.QPainter()
        #     painter.begin(self)
        #     painter.setCompositionMode(
        #         painter.CompositionMode.CompositionMode_SourceOver
        #     )
        #     painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        #     painter.setRenderHint(
        #         painter.RenderHint.SmoothPixmapTransform, True
        #     )
        #     painter.setRenderHint(
        #         painter.RenderHint.LosslessImageRendering, True
        #     )
        #     list_area_rect = self.panel.listWidget.geometry()
        #     _scaled_pixmap = self.background.scaled(
        #         int(list_area_rect.size().width()),
        #         int(list_area_rect.size().height()),
        #         QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        #         QtCore.Qt.TransformationMode.SmoothTransformation,
        #     )
        #     painter.drawPixmap(
        #         list_area_rect, _scaled_pixmap, self.background.rect()
        #     )
        #     painter.end()

        if self.panel.confirm_page.isVisible():
            if not self._current_file_name:
                return

            _item_metadata: dict = self.file_data.files_metadata[
                self._current_file_name
            ]
            if "estimated_time" in _item_metadata.keys():
                _time = self._estimate_print_time(
                    _item_metadata["estimated_time"]
                )
                _print_time_string = (
                    f"{_time[0]}Day {_time[1]}H {_time[2]}min {_time[3]} s"
                    if _time[0] != 0
                    else f"{_time[1]}H {_time[2]}min {_time[3]}s"
                )
                self.panel.print_time_display_button.setText(
                    _print_time_string
                )

            _scene = QtWidgets.QGraphicsScene()
            if "thumbnails" in _item_metadata:
                # _image = self.request_file_thumbnail.emit(
                #     self._current_file_name
                # )
                _image = self.file_data.get_file_thumbnail(
                    self._current_file_name
                )
                if _image:
                    # _scene.setSceneRect(_image.rect().toRectF())

                    _graphics_rect = self.panel.cf_thumbnail.rect().toRectF()
                    _image_rect = _image.rect()

                    scaled_width = _image_rect.width()
                    scaled_height = _image_rect.height()
                    adjusted_x = (_graphics_rect.width() - scaled_width) // 2.0
                    adjusted_y = (
                        _graphics_rect.height() - scaled_height
                    ) // 2.0

                    adjusted_rect = QtCore.QRectF(
                        _image_rect.x() + adjusted_x,
                        _image_rect.y() + adjusted_y,
                        scaled_width,
                        scaled_height,
                    )
                    _scene.setSceneRect(adjusted_rect)
                    _item_scaled = QtWidgets.QGraphicsPixmapItem(
                        QtGui.QPixmap.fromImage(_image).scaled(
                            int(scaled_width),
                            int(scaled_height),
                            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                            QtCore.Qt.TransformationMode.SmoothTransformation,
                        )
                    )
                    _scene.addItem(_item_scaled)
                    self.panel.cf_thumbnail.setScene(_scene)

            else:
                self.panel.cf_thumbnail.setScene(_scene)
        else:
            if self.panel.cf_thumbnail.isVisible():
                self.panel.cf_thumbnail.close()
        if self.panel.tune_page.isVisible():
            self.panel.speed_display.setText(
                str(f"{self.speed_factor_override * 100}%")
            )
        if self.panel.babystep_page.isVisible():
            _button_name_str = f"nozzle_offset_{self._z_offset}"
            if hasattr(self.panel, _button_name_str):
                _button_attr = getattr(self.panel, _button_name_str)
                if callable(_button_attr) and isinstance(
                    _button_attr, BlocksCustomButton
                ):
                    _button_attr.setChecked(True)

        return super().paintEvent(a0)

    def convert_bytes_to_mb(self, bytes: int | float) -> float:
        """Converts byte size to megabyte size

        Args:
            bytes (int | float): bytes

        Returns:
            mb: float that represents the number of mb
        """
        _relation = 2 ** (-20)
        return bytes * _relation

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

    def _calculate_current_layer(self, z_position) -> int:
        """Calculated the current printing layer given the GCODE z position received by the
            gcode_move object update.


            Also updates the label where the current layer should be displayed

        Returns:
            int: Current layer
        """
        _file_metadata = self.file_data.files_metadata.get(
            self._current_file_name
        )
        if not _file_metadata:
            return -1
        _object_height: float = _file_metadata.get("object_height")
        _normal_layer_height: float = _file_metadata.get("layer_height")
        _first_layer_height: float = _file_metadata.get("first_layer_height")

        if (
            not _object_height
            or not _normal_layer_height
            or not _first_layer_height
        ):
            return -1
        if z_position == 0:
            return -1

        _current_layer = (
            1 + (z_position - _first_layer_height) / _normal_layer_height
        )
        self.panel.layer_display_button.setText(
            f"{int(_current_layer)}" if _current_layer != -1 else "?"
        )

        return int(_current_layer)

    def change_page(self, index: int) -> None:
        """Requests a page change page to the global manager

        Args:
            index (int): page index
        """
        self.request_change_page.emit(0, index)

    def back_button(self) -> None:
        """Goes back to the previous page"""
        self.request_back_button_pressed.emit()

    def _estimate_print_time(self, seconds: int):
        """Convert time in seconds format to days, hours, minutes, seconds.

        Args:
            seconds (int): Seconds

        Returns:
            list: list that contains the converted information [days, hours, minutes, seconds]
        """
        num_min, seconds = divmod(seconds, 60)
        num_hours, minutes = divmod(num_min, 60)
        days, hours = divmod(num_hours, 24)
        return [days, hours, minutes, seconds]
