from functools import partial
import math
from PyQt6 import QtWidgets
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QStackedWidget, QWidget, QListWidgetItem, QLabel
from PyQt6.QtCore import (
    pyqtSlot,
    pyqtSignal,
    Qt,
)
from PyQt6 import QtCore, QtGui
import typing
from scripts.events import *
from qt_ui.printStackedWidget_ui import Ui_printStackedWidget
from qt_ui.ui_util import CustomQPushButton
import os
from scripts.bo_includes.bo_files import *
from scripts.bo_includes.bo_printer import *
import logging

_logger = logging.getLogger(__name__)


class PrintTab(QStackedWidget):
    request_print_file_signal = pyqtSignal(str, name="start_print")
    request_print_resume_signal = pyqtSignal(name="resume_print")
    request_print_stop_signal = pyqtSignal(name="stop_print")
    request_print_pause_signal = pyqtSignal(name="pause_print")

    request_block_manual_tab_change = pyqtSignal(name="block_manual_tab_change")
    request_activate_manual_tab_change = pyqtSignal(name="activate_manual_tab_change")

    request_back_button_pressed = pyqtSignal(name="request_back_button_pressed")
    request_change_page = pyqtSignal(int, int, name="request_change_page")

    printer_state_signal = pyqtSignal(str, name="printer_state_updated")

    verify_printer_state_signal = pyqtSignal(name="verify_printer_state")
    
    run_gcode_signal = pyqtSignal(str, name="run_gcode")

    def __init__(
        self,
        parent: typing.Optional["QWidget"],
        file_data: Files,
        ws: MoonWebSocket,
        printer: Printer,
    ) -> None:
        super(PrintTab, self).__init__(parent)
        self.main_panel = parent
        self.file_data: Files = file_data
        self.ws: MoonWebSocket = ws
        self.printer: Printer = printer
        self.background: QtGui.QPixmap | None = None

        self._internal_print_status: str = ""
        self.printer_stats_object_state: str = ""
        self._current_z_position: float
        self._z_offset: float = 0.05
        self.panel = Ui_printStackedWidget()
        self.panel.setupUi(self)
        self.panel.listWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        ##@ Force showing the base panel
        self.change_page(0)

        #  virtual sdcard Path
        # TODO: Get this path from the configfile by asking the websocket first
        # @ GCode directory paths
        self.gcode_path = os.path.expanduser("~/printer_data/gcodes")

        # @ Slot connections
        self.currentChanged.connect(self.view_changed)
        # @ Signals for QListItems
        self.panel.listWidget.itemClicked.connect(self.fileItemClicked)
        ##@ Signals for confirm page
        self.panel.confirm_no_text_label.clicked.connect(self.back_button)
        self.panel.confirm_yes_text_label.clicked.connect(self.print_start)
        ##@ Signals for printing operations
        self.request_print_file_signal.connect(self.ws.api.start_print)
        self.request_print_stop_signal.connect(self.ws.api.cancel_print)
        self.request_print_resume_signal.connect(self.ws.api.resume_print)
        self.request_print_pause_signal.connect(self.ws.api.pause_print)
        self.panel.stop_printing_btn.clicked.connect(
            self.request_print_stop_signal.emit
        )
        self.panel.pause_printing_btn.clicked.connect(self.pause_resume_print)
        # Connecting buttons in the panel routing tree
        # Main Screen
        self.panel.main_print_btn.clicked.connect(partial(self.change_page, 1))
        self.panel.tune_menu_btn.clicked.connect(partial(self.change_page, 4))
        self.panel.tune_babystep_menu_btn.clicked.connect(partial(self.change_page, 5))

        # File List Screen
        self.panel.back_btn.clicked.connect(partial(self.back_button))
        self.panel.tune_back_btn.clicked.connect(partial(self.back_button))

        self.printer.virtual_sdcard_update_signal[str, bool].connect(
            self.virtual_sdcard_update
        )
        self.printer.virtual_sdcard_update_signal[str, float].connect(
            self.virtual_sdcard_update
        )
        self.printer.virtual_sdcard_update_signal.connect(self.virtual_sdcard_update)
        self.printer.print_stats_update_signal[str, str].connect(
            self.print_stats_update
        )
        self.printer.print_stats_update_signal[str, dict].connect(
            self.print_stats_update
        )
        self.printer.print_stats_update_signal[str, float].connect(
            self.print_stats_update
        )
        self.printer.idle_timeout_update_signal[str, str].connect(
            self.idle_timeout_update
        )
        self.printer.idle_timeout_update_signal[str, float].connect(
            self.idle_timeout_update
        )
        self.printer.idle_timeout_update_signal.connect(self.idle_timeout_update)

        self.printer.display_update_signal[str, str].connect(self.display_update)
        self.printer.display_update_signal[str, float].connect(self.display_update)

        self.printer.gcode_move_update_signal[str, list].connect(self.gcode_move_update)
        self.printer.gcode_move_update_signal[str, bool].connect(self.gcode_move_update)
        self.printer.gcode_move_update_signal[str, float].connect(
            self.gcode_move_update
        )

        self.panel.nozzle_close_to_bed.clicked.connect(self.move_nozzle_close_to_bed)
        self.panel.nozzle_far_to_bed.clicked.connect(self.move_nozzle_far_to_bed)

        self.panel.nozzle_offset_001.clicked.connect(self.z_offset_change)
        self.panel.nozzle_offset_005.clicked.connect(self.z_offset_change)
        self.panel.nozzle_offset_01.clicked.connect(self.z_offset_change)
        self.panel.nozzle_offset_025.clicked.connect(self.z_offset_change)
        self.panel.nozzle_offset_05.clicked.connect(self.z_offset_change)

        self.run_gcode_signal.connect(self.ws.api.run_gcode)

        # @ Get the temperatures for the objects
        self.printer.extruder_update_signal.connect(self.extruder_temperature_change)
        self.printer.heater_bed_update_signal.connect(self.heater_bed_temperature_change)
        self.printer.fan_update_signal[str, str, float].connect(self.fan_object_update)
        self.printer.fan_update_signal[str, str, int].connect(self.fan_object_update)
        
        # TODO: The chamber configuration
        # self.printer.
        # self.printer.chamber_object_updated.connect()

        ## @ Show the panel
        self.show()
    
    
    
    @pyqtSlot(str, str, float, name="fan_update")
    @pyqtSlot(str, str, int, name="fan_update")
    def fan_object_update(self, name:str, field:str, new_value: int | float): 
        pass
    
    
    @pyqtSlot(str, str, float, name="extruder_update")
    def extruder_temperature_change(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        pass
        # if field == "temperature":
        #     # _last_text = self.ui.nozzle_1_temp.text()
        #     # if not -1 < int(_last_text) - int(new_value)  < 1:
        #     # self.ui.nozzle_1_temp.setText(f"{str(new_value)} / 0 °C")
        #     self.ui.actual_temp.setText(f"{new_value:.1f}")

        # elif field == "target":
        #     # TODO: Replace with a new label to update the target temperature
        #     self.ui.target_temp.setText(f"{new_value:.1f}")
        #     pass

    @pyqtSlot(str, str, float, name="heater_bed_update")
    def heater_bed_temperature_change(
        self, name: str, field: str, new_value: float
    ) -> None:
        pass
        # print("[INFO] heater_bed_temperature changed ")
        # if field == "temperature":
        #     self.ui.actual_temp_2.setText(f"{new_value:.1f}")
        # elif field == "target":
        #     self.ui.target_temp_2.setText(f"{new_value:.1f}")

    
    @pyqtSlot(str, str, float)
    @pyqtSlot(str, str, name="idle_timeout_update")
    @pyqtSlot(str, float, name="idle_timeout_update")
    def idle_timeout_update(self, field: str, value: int | float) -> None:
        """idle_timeout_update Processes the information that comes form the printer object "idle_timeout"

        Args:
            field (str): Name of the updated field.
            value (int | float): New value for the field.
        """
        pass

    @pyqtSlot(str, float, name="gcode_move_update")
    @pyqtSlot(str, bool, name="gcode_move_update")
    @pyqtSlot(str, list, name="gcode_move_update")
    def gcode_move_update(self, field: str, value: bool | float | list) -> None:
        """gcode_move_update Processes the information that comes from the printer object "gcode_move"

        Args:
            field (str): Name of the updated field
            value (bool | float | list): New value for the field
        """
        if isinstance(value, list):
            if "gcode_position" in field:
                self._current_z_position = value[2]
                if self._internal_print_status == "printing":
                    self._calculate_current_layer()

    @pyqtSlot(str, dict, name="print_stats_update")
    @pyqtSlot(str, float, name="print_stats_update")
    @pyqtSlot(str, str, name="print_stats_update")
    def print_stats_update(self, field: str, value: dict | float | str) -> None:
        """print_stats_update Processes the information that comes from the printer object "print_stats"
            Displays information on the ui accordingly.

        Args:
            field (str): The name of the field that was updated.
            value (dict | float | str): The value of the field.
        """

        if isinstance(value, str):
            if "filename" in field:
                self._current_file_name = value
            if "state" in field:
                self.printer_stats_object_state = value
                if value == "printing" or value == "paused":
                    self.show_print_page()
                elif value == "cancelled" or value == "complete" or value == "standby":
                    # TODO: Print cacelled or complete or stanby
                    self.change_page(0)
                self._internal_print_status = value
        if self.panel.printing_page.isVisible() and (
            self._internal_print_status == "printing"
            or self._internal_print_status == "paused"
        ):
            if isinstance(value, dict):
                print(value)
                if "total_layer" in value.keys():
                    if value["total_layer"] is not None:
                        self.current_print_file_total_layer = value["total_layer"]
                        self.panel.total_layer.setText(
                            str(self.current_print_file_total_layer)
                        )
                if "current_layer" in value.keys():
                    if value["current_layer"] is not None:

                        self.current_print_file_current_layer = value["current_layer"]
                        self.panel.current_layer.setText(
                            str(self.current_print_file_current_layer)
                        )

            elif isinstance(value, float):
                if "total_duration" in field:
                    self.print_total_duration = value
                    _time = self._estimate_print_time(int(self.print_total_duration))
                    _print_time_string = (
                        f"{_time[0]}Day {_time[1]}H {_time[2]}min {_time[3]} s"
                        if _time[0] != 0
                        else f"{_time[1]}H {_time[2]}min {_time[3]}s"
                    )
                    self.panel.remaining_time_text_label.setText(_print_time_string)
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

    @pyqtSlot(str, float, name="virtual_sdcard_update")
    @pyqtSlot(str, bool, name="virtual_sdcard_update")
    def virtual_sdcard_update(self, field: str, value: float | bool) -> None:
        """virtual_sdcard_update Slot for incoming printer object virtual_sdcard information update

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
                # int(f"{round(self.print_progress * 100):.0f}")
                # int(f"{self.print_progress * 100:.0f}")
                self.panel.progress_value_label.setText(
                    f"{math.trunc(self.print_progress * 100)}"
                )

    @pyqtSlot(str, str, name="display_update")
    @pyqtSlot(str, float, name="display_update")
    def display_update(self, field: str, value: str | float) -> None:
        """display_update Slot for incoming printer object display information update

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
        """print_start

        Start a print job, *INTERNAL USE ONLY*
        """
        # * Emit the print file signal and send to the websocket the request
        self.request_print_file_signal.emit(self._current_file_name)
        self.show_print_page()
        _logger.debug(
            f"Requested print job of file {self._current_file_name} on {self.__class__.__name__}\
                in method: {sys._getframe().f_code.co_name}"
        )

    def show_print_page(self) -> None:
        """show_print_page
        Helper method to change the current panel to the printing one
        """
        if (
            not self.panel.printing_page.isVisible()
            and self._current_file_name is not None
        ):
            self.panel.file_printing_text_label.setText(self._current_file_name)
            self.panel.printing_progress_bar.reset()
            self._internal_print_status = "printing"
            self.total_layers = self.file_data.files_metadata[self._current_file_name][
                "layer_count"
            ]
            # * Request block tab change on the main menu
            self.request_block_manual_tab_change.emit()
            self.panel.total_layer.setText(str(self.total_layers))

            self.change_page(3)

    @pyqtSlot(name="pause_resume_print")
    def pause_resume_print(self) -> None:
        """pause_resume_print Handles what signal to emit to the printer when a printing job is ongoing

        Can either be:

        - A pause is supose to happen -> request a pause

        - A resume is suppose to happen -> request a resume
        """
        # TODO: Maybe i have to wait for the websocket to respond if it's really printing
        if self._internal_print_status == "printing":
            # * It's printing
            self.request_print_pause_signal.emit()
            self._internal_print_status = "paused"
        elif (
            self._internal_print_status == "paused"
            and self.printer_stats_object_state == "paused"
        ):
            # * It's paused
            self.request_print_resume_signal.emit()
            self._internal_print_status = "printing"

    @pyqtSlot(name="print_state")
    def print_state(self) -> None:
        """print_state -> Slot for received signal about the current printing state of the machine

        States:
        - Printing

        - Paused

        - Canceled

        Args:
            state (str): _description_
        """
        # TODO Maybe i can do this more dinamically
        # print("here")
        # print(f"Print state verification {self.printer_stats_object_state}")
        if self._internal_print_status != "" and self.printer_stats_object_state != "":
            # print(self._internal_print_status)
            # print(self.printer_stats_object_state)
            if self._internal_print_status == self.printer_stats_object_state:
                self.printer_state_signal.emit()

        # if "printing" in state:
        #     # * Indicate that it is printing
        #     self._internal_print_status = "printing"
        #     self.panel.pause_printing_btn.setText("Pause")

        # elif "paused" in state:
        #     self._internal_print_status = "paused"
        #     self.panel.pause_printing_btn.setText("Resume")

        # elif "canceled" in state:
        #     self._intewrnal_print_status = "canceled"
        #     # self.panel.
        # elif "error" in state:
        #     self._internal_print_status = "error"
        _logger.debug(
            f"Verified Printer state on {self.__class__.__name__} | Method {sys._getframe().f_code.co_name} "
        )

    def add_file_entries(self) -> None:
        """add_file_entries ->

        Inserts the currently available gcode files on the QListWidget
        """
        # * Delete table contents
        self.panel.listWidget.clear()
        index = 0
        for item in self.file_data.file_list:
            # TODO: Add a file icon before the name
            # * Add a row
            _item = QtWidgets.QListWidgetItem()
            _item_widget = QWidget()
            _item_layout = QtWidgets.QHBoxLayout()
            _item_text = QtWidgets.QLabel()
            # * Add text
            _item_text.setText(str(item["path"]))
            # _file_size = "{:.2f}".format(self.convert_bytes_to_mb(item["size"]))
            # _item_size = QtWidgets.QlistWidgetItem(f" {_file_size} MB")
            # * Add items to the layout
            _item_layout.addWidget(_item_text)
            # * Set item widget layout
            _item_widget.setLayout(_item_layout)
            _item.setSizeHint(_item_widget.sizeHint())
            # * Set item Flags, make it not editable with the ~
            _item.setFlags(~Qt.ItemFlag.ItemIsEditable)
            # * Add items
            self.panel.listWidget.addItem(_item)
            self.panel.listWidget.setItemWidget(_item, _item_widget)
            index += 1

    @pyqtSlot(name="request_noozle_close_to_bed")
    def move_nozzle_close_to_bed(self) -> None:
        self.run_gcode_signal.emit(
            f"SET_GCODE_OFFSET Z_ADJUST=-{self._z_offset} MOVE=1"
        )

    @pyqtSlot(name="request_noozle_far_to_bed")
    def move_nozzle_far_to_bed(self) -> None:
        self.run_gcode_signal.emit(
            f"SET_GCODE_OFFSET Z_ADJUST=+{self._z_offset} MOVE=1"
        )

    @pyqtSlot(name="z_offset_change")
    def z_offset_change(self) -> None:
        _possible_z_values: typing.List = [0.001, 0.005, 0.01, 0.025, 0.05]
        _sender: QObject | None = self.sender()
        # print(f"Changing the value for the z_offset to {_sender.text()}")
        if _sender is not None and isinstance(_sender, QLabel):
            if float(_sender.text()) in _possible_z_values:
                print(f"changed the zz_offset value to {self._z_offset}")
                self._z_offset = float(_sender.text())
                _logger.debug(f"z_offset changed to {self._z_offset}")

    @pyqtSlot(int, name="currentChanged")
    def view_changed(self, window_index: int) -> None:
        """view_changed ->
            Slot for the current displayed panel

        Args:
            window_index (int): Current QStackedWidget index

        Returns:
            _type_: None
        """
        if window_index == 1:
            # * On files panel
            self.add_file_entries()

    @pyqtSlot(QListWidgetItem, name="file_item_clicked")
    def fileItemClicked(self, item: QListWidgetItem) -> None:
        """fileItemClicked->
            Slot for List Item clicked

        Args:
            item (QListWidgetItem): Clicked item
        """
        # * Get the filename from the list item pressed
        _current_item: QWidget | None = self.panel.listWidget.itemWidget(item)
        if not _current_item is None:
            self._current_file_name = _current_item.findChild(QtWidgets.QLabel).text()
            self.panel.confirm_file_name_text_label.setText(self._current_file_name)
            self.change_page(2)

    def paintEvent(self, a0: QPaintEvent) -> None:
        """paintEvent->
            Paints UI aspects on the current panel, such as images

        Args:
            a0 (QPaintEvent): _description_
        """
        if self.background is None:
            return
        if self.panel.file_area.isVisible():
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_SourceOver
            )
            painter.setRenderHint(painter.RenderHint.Antialiasing, True)
            painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)
            list_area_rect = self.panel.file_area.geometry()
            # * Scale the pixmap to the correct Dimensions
            # TODO: Background is not really in SVG mode
            _scaled_pixmap = self.background.scaled(
                int(list_area_rect.size().width()),
                int(list_area_rect.size().height()),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawPixmap(list_area_rect, _scaled_pixmap, self.background.rect())
            painter.end()

        if self.panel.confirm_page.isVisible():
            _item_metadata: dict = self.file_data.files_metadata[
                self._current_file_name
            ]
            if "estimated_time" in _item_metadata.keys():
                # * Place the estimated time the file takes to print first, updated with print_stats after
                _time = self._estimate_print_time(_item_metadata["estimated_time"])
                _print_time_string = (
                    f"{_time[0]}Day {_time[1]}H {_time[2]}min {_time[3]} s"
                    if _time[0] != 0
                    else f"{_time[1]}H {_time[2]}min {_time[3]}s"
                )
                self.panel.remaining_time_text_label.setText(_print_time_string)
            # * Paint the thumbnail on the image
            _scene = QtWidgets.QGraphicsScene()
            if "thumbnails" in _item_metadata:
                _item_thumbnail = _item_metadata["thumbnails"][1]["relative_path"]
                # TODO: Better paths, need to do this in a better way
                # * Add thumbnail path to python paths
                path = os.path.join(
                    os.path.dirname(
                        os.path.join(self.gcode_path, self._current_file_name)
                    ),
                    _item_thumbnail,
                )
                # * Check if the directory is accessible
                if os.access(path, os.R_OK):
                    # * Add the thumbnail to the GraphicsView
                    _image = QtGui.QImage(path)
                    _scene.setSceneRect(_image.rect().toRectF())
                    _item = QtWidgets.QGraphicsPixmapItem(
                        QtGui.QPixmap.fromImage(_image).scaled(
                            _image.rect().width(),
                            _image.rect().height(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation,
                        )
                    )
                    _scene.addItem(_item)
                    self.panel.confirm_print_preview_graphics.setScene(_scene)
                    # print(self.panel.confirm_print_preview_graphics.geometry())
                    self.panel.confirm_print_preview_graphics.setFrameRect(
                        _image.rect()
                    )
            else:
                self.panel.confirm_print_preview_graphics.setScene(_scene)
        else:

            if self.panel.confirm_print_preview_graphics.isVisible():
                self.panel.confirm_print_preview_graphics.close()

        if self.panel.babystep_page.isVisible(): 
            # * If there is a z_offset value already paint the button a little greyer to indicate that is the current offset
            _button_name_str = f"nozzle_offset_{self._z_offset}"
            if hasattr(self.panel, _button_name_str): 
                _button_attr = getattr(self.panel, _button_name_str)
                # TODO: This will have to change if the button goes from QPushButton to QCustomPushButton
                if callable(_button_attr) and isinstance(_button_attr, CustomQPushButton):
                    _button_attr.setChecked(True)
            # _button_to_check = 
            
            # self.panel.nozzle_offset_001.setChecked(True)
            
            
            
        return super().paintEvent(a0)

    def convert_bytes_to_mb(self, bytes: int | float) -> float:
        """convert_bytes_to_mb-> Converts byte size to megabyte size

        Args:
            bytes (int | float): bytes

        Returns:
            mb: float that represents the number of mb
        """
        _relation = 2 ** (-20)
        return bytes * _relation

    def setProperty(self, name: str, value: typing.Any) -> bool:
        """setProperty-> Intercept the set property method

        Args:
            name (str): Name of the dynamic property
            value (typing.Any): Value for the dynamic property

        Returns:
            bool: Returns to the super class
        """
        if name == "backgroundPixmap":
            self.background = value
        return super().setProperty(name, value)

    def _calculate_current_layer(self) -> int:
        """_calculate_current_layer
            Calculated the current printing layer given the GCODE z position received by the
            gcode_move object update.


            Also updates the label where the current layer should be displayed

        Returns:
            int: Current layer
        """
        _object_height: float = self.file_data.files_metadata[self._current_file_name][
            "object_height"
        ]
        _normal_layer_height: float = self.file_data.files_metadata[
            self._current_file_name
        ]["layer_height"]
        _first_layer_height: float = self.file_data.files_metadata[
            self._current_file_name
        ]["first_layer_height"]

        # _current_layer = int(1 + (_object_height - _first_layer_height) / _normal_layer_height)

        _current_layer = (
            1 + (self._current_z_position - _first_layer_height) / _normal_layer_height
        )
        self.panel.current_layer.setText(f"{int(_current_layer)}")

        return int(_current_layer)

    def change_page(self, index: int) -> None:
        """change_page Requests a change page, to the global page thingy

        Args:
            index (int): The index of the page we wan't to go
        """
        # Emits with the request its tab index and its page index
        self.request_change_page.emit(0, index)

    def back_button(self) -> None:
        """back_button Goes back to the previous page"""
        self.request_back_button_pressed.emit()

    def _estimate_print_time(self, seconds: int):
        """_estimate_print_time Convert time in seconds format to days, hours, minutes, seconds.

        Args:
            seconds (int): Seconds

        Returns:
            list: list that contains the converted information [days, hours, minutes, seconds]
        """
        num_min, seconds = divmod(seconds, 60)
        num_hours, minutes = divmod(num_min, 60)
        days, hours = divmod(num_hours, 24)
        return [days, hours, minutes, seconds]


# TODO: Add folder icon to the topbar of the files list
# TODO: Add A icon such as ">" to indicate that when you press the file you get the information and go to the next page
