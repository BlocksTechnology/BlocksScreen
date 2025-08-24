import logging
import math
import typing

from helper_methods import calculate_current_layer, estimate_print_time
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_label import BlocksLabel
from lib.utils.display_button import DisplayButton
from lib.panels.widgets import dialogPage
import events

from PyQt6 import QtCore, QtGui, QtWidgets


class JobStatusWidget(QtWidgets.QWidget):
    print_start: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="print_start"
    )
    print_pause: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="print_pause"
    )
    print_resume: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="print_resume"
    )
    print_cancel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="print_cancel"
    )
    tune_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="tune_clicked"
    )
    show_request: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="show_request"
    )
    hide_request: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="hide_request"
    )
    request_query_print_stats: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(dict, name="request_query_print_stats")
    )
    request_file_info: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request_file_info"
    )

    _internal_print_status: str = ""
    _current_file_name: str = ""
    file_metadata: dict = {}
    total_layers = "?"

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.canceldialog = dialogPage.DialogPage(self)

        self.setupUI()
        self.tune_menu_btn.clicked.connect(self.tune_clicked.emit)
        self.pause_printing_btn.clicked.connect(self.pause_resume_print)
        self.stop_printing_btn.clicked.connect(self.handleCancel)

    def handleCancel(self) -> None:
        """Handle the cancel print job dialog"""
        self.canceldialog.set_message(
            "Are you sure you \n want to cancel \n this print job?"
        )
        self.canceldialog.button_clicked.connect(self.on_dialog_button_clicked)
        self.canceldialog.show()

    def on_dialog_button_clicked(self, button_name: str) -> None:
        """Handle dialog button clicks"""
        if button_name == "Confirm":
            print(
                "Confirm button clicked MY GD HELPO ME IDK WHAT AM I DOING I MISS MY WIFI OH GOD HE IS HERE M-MY , NOOOOOOOOOOooOooOO..."
            )
            self.print_cancel.emit()  # Emit the print_cancel signal
        elif button_name == "Cancel":
            print("Cancel button clicked")

    @QtCore.pyqtSlot(str, name="on_print_start")
    def on_print_start(self, file: str) -> None:
        """Start a print job, show job status page"""
        self._current_file_name = file
        self.js_file_name_label.setText(self._current_file_name)
        self.layer_display_button.setText("?")
        self.print_time_display_button.setText("?")
        self.printing_progress_bar.reset()
        self._internal_print_status = "printing"
        self.request_file_info.emit(
            file
        )  # Request file metadata (or file info whatever)

        self.print_start.emit(file)
        print_start_event = events.PrintStart(
            self._current_file_name, self.file_metadata
        )
        try:
            instance = QtWidgets.QApplication.instance()
            if instance:
                print(self.window().objectName())
                instance.postEvent(self.window(), print_start_event)
            else:
                raise TypeError(
                    "QApplication.instance expected non None value"
                )
        except Exception as e:
            logging.info(
                f"Unexpected error while posting print job start event: {e}"
            )

    @QtCore.pyqtSlot(dict, name="on_fileinfo")
    def on_fileinfo(self, fileinfo: dict) -> None:
        self.total_layers = str(fileinfo.get("layer_count", "?"))
        self.layer_display_button.setText("?")
        self.layer_display_button.secondary_text = str(self.total_layers)
        self.file_metadata = fileinfo

    @QtCore.pyqtSlot(name="pause_resume_print")
    def pause_resume_print(self) -> None:
        """Handle pause/resume button clicks"""
        if self._internal_print_status == "printing":
            self.print_pause.emit()
            self._internal_print_status = "paused"
            self.pause_printing_btn.setText("Resume")
            self.pause_printing_btn.setPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/play.svg")
            )
        elif self._internal_print_status == "paused":
            self.print_resume.emit()
            self._internal_print_status = "printing"
            self.pause_printing_btn.setText("Pause")
            self.pause_printing_btn.setPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/pause.svg")
            )

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
                self._current_file_name = value
                if self.js_file_name_label.text().lower() != value.lower():
                    self.js_file_name_label.setText(self._current_file_name)
                    self.request_file_info.emit(value)  # Request file metadata
            if "state" in field:
                if value.lower() == "printing" or value == "paused":
                    self.request_query_print_stats.emit(
                        {"print_stats": ["filename"]}
                    )
                    self.show_request.emit()
                    value = "start"  # This is for event compatibility

                elif value in ("cancelled", "complete", "error", "standby"):
                    self._current_file_name = ""
                    self._internal_print_status = ""
                    self.total_layers = "?"
                    self.file_metadata.clear()
                    self.hide_request.emit()
                    return

                if hasattr(events, str("Print" + value.capitalize())):
                    event_obj = getattr(
                        events, str("Print" + value.capitalize())
                    )
                    event = event_obj(
                        self._current_file_name, self.file_metadata
                    )
                    try:
                        instance = QtWidgets.QApplication.instance()
                        if instance:
                            instance.postEvent(self.window(), event)
                        else:
                            raise TypeError(
                                "QApplication.instance expected non None value"
                            )
                    except Exception as e:
                        logging.info(
                            f"Unexpected error while posting print job start event: {e}"
                        )
                self._internal_print_status = value

        if self.isVisible() and (
            self._internal_print_status == "printing"
            or self._internal_print_status == "paused"
        ):
            self.layer_display_button.secondary_text = (  # type:ignore
                self.file_metadata.get("layer_count", "?")
            )
            if not self.file_metadata:
                return
            if isinstance(value, dict):
                if "total_layer" in value.keys():
                    # Only available if SET_PRINT_STATS_INFO TOTAL_LAYER=<value>
                    # gcode command is ran
                    if value["total_layer"] is not None:
                        self.total_layers = value.get("total_layer", "?")
                        self.layer_display_button.secondary_text = (  # type:ignore
                            str(self.total_layers)
                        )
                if "current_layer" in value.keys():
                    # Only available if SET_PRINT_STATS_INFO CURRENT_LAYER=<value>
                    # gcode command is ran
                    if value["current_layer"] is not None:
                        _current_layer = value["current_layer"]
                        if _current_layer is not None:
                            self.layer_display_button.setText(
                                f"{int(_current_layer)}"
                                if _current_layer != -1
                                else "?"
                            )
            elif isinstance(value, float):
                if "total_duration" in field:
                    self.print_total_duration = value
                    _time = estimate_print_time(int(self.print_total_duration))
                    _print_time_string = (
                        f"{_time[0]}Day {_time[1]}H {_time[2]}min {_time[3]} s"
                        if _time[0] != 0
                        else f"{_time[1]}H {_time[2]}min {_time[3]}s"
                    )
                    self.print_time_display_button.setText(_print_time_string)
                elif "print_duration" in field:
                    self.current_print_duration_seconds = value
                elif "filament_used" in field:
                    self.filament_used_mm = value

    @QtCore.pyqtSlot(str, list, name="on_gcode_move_update")
    def on_gcode_move_update(self, field: str, value: list) -> None:
        """Processes the information that comes from the printer object "gcode_move"

        Args:
            field (str): Name of the updated field
            value (list): New value for the field
        """
        if isinstance(value, list):
            if "gcode_position" in field:  # Without offsets
                if self._internal_print_status == "printing":
                    _current_layer = calculate_current_layer(
                        z_position=value[2],
                        object_height=float(
                            self.file_metadata.get("object_height", -1.0)
                        ),
                        layer_height=float(
                            self.file_metadata.get("layer_height", -1.0)
                        ),
                        first_layer_height=float(
                            self.file_metadata.get("first_layer_height", -1.0)
                        ),
                    )
                    self.layer_display_button.setText(
                        f"{int(_current_layer)}"
                        if _current_layer != -1
                        else "?"
                    )

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
                self.printing_progress_bar.setValue(
                    int(math.trunc(self.print_progress * 100))
                )
                self.progress_value_label.setText(
                    f"{math.trunc(self.print_progress * 100)}"
                )

    def setupUI(self) -> None:
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.job_status_header_layout = QtWidgets.QHBoxLayout()
        self.job_status_header_layout.setContentsMargins(1, 1, 1, 1)
        self.job_status_header_layout.setSpacing(20)
        self.job_status_header_layout.setObjectName("job_status_header_layout")
        self.js_file_name_icon = BlocksLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.js_file_name_icon.sizePolicy().hasHeightForWidth()
        )
        self.js_file_name_icon.setSizePolicy(sizePolicy)
        self.js_file_name_icon.setMinimumSize(QtCore.QSize(60, 60))
        self.js_file_name_icon.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(14)
        self.js_file_name_icon.setFont(font)
        self.js_file_name_icon.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.js_file_name_icon.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.js_file_name_icon.setText("")
        self.js_file_name_icon.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.js_file_name_icon.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/files/media/btn_icons/file_icon.svg"),
        )
        self.js_file_name_icon.setObjectName("js_file_name_icon")
        self.job_status_header_layout.addWidget(self.js_file_name_icon)
        self.js_file_name_label = BlocksLabel(parent=self)
        self.js_file_name_label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.js_file_name_label.sizePolicy().hasHeightForWidth()
        )
        self.js_file_name_label.setSizePolicy(sizePolicy)
        self.js_file_name_label.setMinimumSize(QtCore.QSize(200, 60))
        self.js_file_name_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        self.js_file_name_label.setFont(font)
        self.js_file_name_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.js_file_name_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.js_file_name_label.setObjectName("js_file_name_label")
        self.job_status_header_layout.addWidget(self.js_file_name_label)
        self.verticalLayout_3.addLayout(self.job_status_header_layout)
        self.job_status_content_layout = QtWidgets.QVBoxLayout()
        self.job_status_content_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinimumSize
        )
        self.job_status_content_layout.setContentsMargins(5, 5, 5, 5)
        self.job_status_content_layout.setSpacing(5)
        self.job_status_content_layout.setObjectName(
            "job_status_content_layout"
        )
        self.job_status_control_buttons_layout = QtWidgets.QFrame(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.job_status_control_buttons_layout.sizePolicy().hasHeightForWidth()
        )
        self.job_status_control_buttons_layout.setSizePolicy(sizePolicy)
        self.job_status_control_buttons_layout.setMinimumSize(
            QtCore.QSize(680, 100)
        )
        self.job_status_control_buttons_layout.setFrameShape(
            QtWidgets.QFrame.Shape.NoFrame
        )
        self.job_status_control_buttons_layout.setFrameShadow(
            QtWidgets.QFrame.Shadow.Plain
        )
        self.job_status_control_buttons_layout.setLineWidth(0)
        self.job_status_control_buttons_layout.setObjectName(
            "job_status_control_buttons_layout"
        )
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.job_status_control_buttons_layout
        )
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pause_printing_btn = BlocksCustomButton(
            parent=self.job_status_control_buttons_layout
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pause_printing_btn.sizePolicy().hasHeightForWidth()
        )
        self.pause_printing_btn.setSizePolicy(sizePolicy)
        self.pause_printing_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.pause_printing_btn.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.pause_printing_btn.setFont(font)
        self.pause_printing_btn.setMouseTracking(False)
        self.pause_printing_btn.setTabletTracking(True)
        self.pause_printing_btn.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.pause_printing_btn.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.pause_printing_btn.setStyleSheet("")
        self.pause_printing_btn.setAutoDefault(False)
        self.pause_printing_btn.setFlat(True)
        self.pause_printing_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/pause.svg")
        )
        self.pause_printing_btn.setObjectName("pause_printing_btn")
        self.horizontalLayout.addWidget(self.pause_printing_btn)
        self.stop_printing_btn = BlocksCustomButton(
            parent=self.job_status_control_buttons_layout
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stop_printing_btn.sizePolicy().hasHeightForWidth()
        )
        self.stop_printing_btn.setSizePolicy(sizePolicy)
        self.stop_printing_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.stop_printing_btn.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.stop_printing_btn.setFont(font)
        self.stop_printing_btn.setMouseTracking(False)
        self.stop_printing_btn.setTabletTracking(True)
        self.stop_printing_btn.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.stop_printing_btn.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.stop_printing_btn.setStyleSheet("")
        self.stop_printing_btn.setAutoDefault(False)
        self.stop_printing_btn.setFlat(True)
        self.stop_printing_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/stop.svg")
        )
        self.stop_printing_btn.setObjectName("stop_printing_btn")
        self.horizontalLayout.addWidget(self.stop_printing_btn)
        self.tune_menu_btn = BlocksCustomButton(
            parent=self.job_status_control_buttons_layout
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tune_menu_btn.sizePolicy().hasHeightForWidth()
        )
        self.tune_menu_btn.setSizePolicy(sizePolicy)
        self.tune_menu_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.tune_menu_btn.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tune_menu_btn.setFont(font)
        self.tune_menu_btn.setMouseTracking(False)
        self.tune_menu_btn.setTabletTracking(True)
        self.tune_menu_btn.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.tune_menu_btn.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.tune_menu_btn.setStyleSheet("")
        self.tune_menu_btn.setAutoDefault(False)
        self.tune_menu_btn.setFlat(True)
        self.tune_menu_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/tune.svg")
        )
        self.tune_menu_btn.setObjectName("tune_menu_btn")
        self.horizontalLayout.addWidget(self.tune_menu_btn)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.job_status_content_layout.addWidget(
            self.job_status_control_buttons_layout,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.job_status_progress_layout = QtWidgets.QGridLayout()
        self.job_status_progress_layout.setObjectName(
            "job_status_progress_layout"
        )
        self.progress_text_label = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.progress_text_label.sizePolicy().hasHeightForWidth()
        )
        self.progress_text_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(16)
        self.progress_text_label.setFont(font)
        self.progress_text_label.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.progress_text_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.progress_text_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.progress_text_label.setObjectName("progress_text_label")
        self.job_status_progress_layout.addWidget(
            self.progress_text_label,
            0,
            0,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.progress_value_label = QtWidgets.QLabel(parent=self)
        self.progress_value_label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.progress_value_label.sizePolicy().hasHeightForWidth()
        )
        self.progress_value_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        self.progress_value_label.setFont(font)
        self.progress_value_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.progress_value_label.setObjectName("progress_value_label")
        self.job_status_progress_layout.addWidget(
            self.progress_value_label, 0, 1, 1, 1
        )
        self.printing_progress_bar = QtWidgets.QProgressBar(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.printing_progress_bar.sizePolicy().hasHeightForWidth()
        )
        self.printing_progress_bar.setSizePolicy(sizePolicy)
        self.printing_progress_bar.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.printing_progress_bar.setProperty("value", 24)
        self.printing_progress_bar.setObjectName("printing_progress_bar")
        self.job_status_progress_layout.addWidget(
            self.printing_progress_bar,
            0,
            2,
            1,
            1,
            QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.job_status_content_layout.addLayout(
            self.job_status_progress_layout
        )
        self.job_stats_display_layout = QtWidgets.QHBoxLayout()
        self.job_stats_display_layout.setObjectName("job_stats_display_layout")
        self.layer_display_button = DisplayButton(parent=self)
        self.layer_display_button.button_type = "display_secondary"
        self.layer_display_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.layer_display_button.sizePolicy().hasHeightForWidth()
        )
        self.layer_display_button.setSizePolicy(sizePolicy)
        self.layer_display_button.setMinimumSize(QtCore.QSize(150, 40))
        self.layer_display_button.setMaximumSize(QtCore.QSize(150, 40))
        self.layer_display_button.setText("")
        self.layer_display_button.setCheckable(False)
        self.layer_display_button.setFlat(True)
        self.layer_display_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/layers.svg")
        )
        self.layer_display_button.setObjectName("layer_display_button")
        self.job_stats_display_layout.addWidget(
            self.layer_display_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.print_time_display_button = DisplayButton(parent=self)
        self.print_time_display_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.print_time_display_button.sizePolicy().hasHeightForWidth()
        )
        self.print_time_display_button.setSizePolicy(sizePolicy)
        self.print_time_display_button.setMinimumSize(QtCore.QSize(150, 40))
        self.print_time_display_button.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.SplitHCursor)
        )
        self.print_time_display_button.setText("")
        self.print_time_display_button.setCheckable(False)
        self.print_time_display_button.setFlat(True)
        self.print_time_display_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/time.svg")
        )
        self.print_time_display_button.setObjectName(
            "print_time_display_button"
        )
        self.job_stats_display_layout.addWidget(
            self.print_time_display_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.job_status_content_layout.addLayout(self.job_stats_display_layout)
        self.job_status_content_layout.setStretch(0, 1)
        self.job_status_content_layout.setStretch(1, 1)
        self.job_status_content_layout.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.job_status_content_layout)

        self.setLayout(self.verticalLayout_3)
        self.tune_menu_btn.setText("Tune")
        self.stop_printing_btn.setText("Cancel")
        self.pause_printing_btn.setText("Pause")
