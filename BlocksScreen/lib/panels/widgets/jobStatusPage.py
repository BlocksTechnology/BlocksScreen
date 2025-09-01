import logging
import typing


from helper_methods import calculate_current_layer, estimate_print_time
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_label import BlocksLabel
from lib.utils.display_button import DisplayButton
<<<<<<< HEAD
=======
from lib.utils.blocks_progressbar import CustomProgressBar
>>>>>>> origin/main
from lib.panels.widgets import dialogPage
import events

from PyQt6 import QtCore, QtGui, QtWidgets


class ClickableGraphicsView(QtWidgets.QGraphicsView):
    clicked = QtCore.pyqtSignal()


def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    if event.button() == QtCore.Qt.MouseButton.LeftButton:
        self.clicked.emit()
    super(ClickableGraphicsView, self).mousePressEvent(event)


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

        self.CBVSmallThumbnail.clicked.connect(self.showthumbnail)
        self.CBVBigThumbnail.clicked.connect(self.hidethumbnail)

        self.smalthumbnail = QtGui.QImage(
            "BlocksScreen/lib/ui/resources/media/smalltest.png"
        )
        self.bigthumbnail = QtGui.QImage(
            "BlocksScreen/lib/ui/resources/media/thumbnailmissing.png"
        )
        self.CBVSmallThumbnail.installEventFilter(self)
        self.CBVBigThumbnail.installEventFilter(self)

    def eventFilter(self, source, event):
        if (
            source == self.CBVSmallThumbnail
            and event.type() == QtCore.QEvent.Type.MouseButtonPress
        ):
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.showthumbnail()

        if (
            source == self.CBVBigThumbnail
            and event.type() == QtCore.QEvent.Type.MouseButtonPress
        ):
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.hidethumbnail()

        return super().eventFilter(source, event)

    def showthumbnail(self):
        self.contentWidget.hide()
        self.progressWidget.hide()
        self.headerWidget.hide()
        self.btnWidget.hide()
        self.smallthumb_widget.hide()
        self.bigthumb_widget.show()

    def hidethumbnail(self):
        self.contentWidget.show()
        self.progressWidget.show()
        self.headerWidget.show()
        self.btnWidget.show()
        self.smallthumb_widget.show()
        self.bigthumb_widget.hide()

>>>>>>> origin/main
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
            self.print_cancel.emit()  # Emit the print_cancel signal
        elif button_name == "Cancel":
<<<<<<< HEAD
            ...
            
    @QtCore.pyqtSlot(str, name="on_print_start")
    def on_print_start(self, file: str) -> None:
=======
            pass

    @QtCore.pyqtSlot(str, list, name="on_print_start")
    def on_print_start(self, file: str, thumbnail: list) -> None:
>>>>>>> origin/main
        """Start a print job, show job status page"""
        self._current_file_name = file
        self.js_file_name_label.setText(self._current_file_name)
        self.layer_display_button.setText("?")
        self.print_time_display_button.setText("?")
        print(thumbnail)
        self.smalthumbnail = thumbnail[1]
        self.bigthumbnail = thumbnail[1]

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
        if (
            fileinfo["thumbnail_images"] is not None
            and len(fileinfo["thumbnail_images"]) > 0
        ):
            # Assign the first thumbnail to both by default
            self.smalthumbnail = fileinfo["thumbnail_images"][1]
            self.bigthumbnail = fileinfo["thumbnail_images"][2]

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
            print(f"Print status update received: {field} -> {value}")
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
                self.printing_progress_bar.setValue(self.print_progress)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        _scene = QtWidgets.QGraphicsScene()
        if not self.smalthumbnail.isNull():
            _graphics_rect = self.CBVSmallThumbnail.rect().toRectF()
            _image_rect = self.smalthumbnail.rect()

            scaled_width = _image_rect.width()
            scaled_height = _image_rect.height()
            adjusted_x = (_graphics_rect.width() - scaled_width) // 2.0
            adjusted_y = (_graphics_rect.height() - scaled_height) // 2.0

            adjusted_rect = QtCore.QRectF(
                _image_rect.x() + adjusted_x,
                _image_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            _scene.setSceneRect(adjusted_rect)
            _item_scaled = QtWidgets.QGraphicsPixmapItem(
                QtGui.QPixmap.fromImage(self.smalthumbnail).scaled(
                    int(scaled_width),
                    int(scaled_height),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
            )
            _scene.addItem(_item_scaled)
            self.CBVSmallThumbnail.setScene(_scene)
        _scene = QtWidgets.QGraphicsScene()

        if not self.bigthumbnail.isNull():
            _graphics_rect = self.CBVBigThumbnail.rect().toRectF()
            _image_rect = self.bigthumbnail.rect()

            scaled_width = _image_rect.width()
            scaled_height = _image_rect.height()
            adjusted_x = (_graphics_rect.width() - scaled_width) // 2.0
            adjusted_y = (_graphics_rect.height() - scaled_height) // 2.0

            adjusted_rect = QtCore.QRectF(
                _image_rect.x() + adjusted_x,
                _image_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            _scene.setSceneRect(adjusted_rect)
            _item_scaled = QtWidgets.QGraphicsPixmapItem(
                QtGui.QPixmap.fromImage(self.bigthumbnail).scaled(
                    int(scaled_width),
                    int(scaled_height),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
            )
            _scene.addItem(_item_scaled)
            self.CBVBigThumbnail.setScene(_scene)

    def setupUI(self) -> None:
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        # ----------------------------------size policy

        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 420))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        # ---------------------------------Widgets
        self.bigthumb_widget = QtWidgets.QWidget(self)
        self.bigthumb_widget.setGeometry(
            QtCore.QRect(0, 0, self.width(), self.height())
        )
        self.bigthumb_widget.setObjectName("bigthumb_widget")

        self.headerWidget = QtWidgets.QWidget(self)
        self.headerWidget.setGeometry(QtCore.QRect(11, 11, 691, 62))
        self.headerWidget.setObjectName("headerWidget")

        self.btnWidget = QtWidgets.QWidget(self)
        self.btnWidget.setGeometry(QtCore.QRect(10, 80, 691, 90))
        self.btnWidget.setObjectName("btnWidget")

        self.progressWidget = QtWidgets.QWidget(self)
        self.progressWidget.setGeometry(QtCore.QRect(10, 170, 471, 241))
        self.progressWidget.setObjectName("progressWidget")

        self.contentWidget = QtWidgets.QWidget(self)
        self.contentWidget.setGeometry(QtCore.QRect(480, 170, 221, 241))
        self.contentWidget.setObjectName("contentWidget")

        self.smallthumb_widget = QtWidgets.QLabel(self)
        self.smallthumb_widget.setGeometry(QtCore.QRect(10, 170, 471, 241))
        self.smallthumb_widget.setObjectName("smallthumb_widget")

        # ---------------------------------layout

        self.smalllayout = QtWidgets.QHBoxLayout(self.smallthumb_widget)

        self.biglayout = QtWidgets.QHBoxLayout(self.bigthumb_widget)

        self.job_status_header_layout = QtWidgets.QHBoxLayout(
            self.headerWidget
        )
        self.job_status_header_layout.setSpacing(20)
        self.job_status_header_layout.setObjectName("job_status_header_layout")

        self.job_status_progress_layout = QtWidgets.QVBoxLayout(
            self.progressWidget
        )
        self.job_status_progress_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinimumSize
        )

        self.job_status_btn_layout = QtWidgets.QHBoxLayout(self.btnWidget)
        self.job_status_btn_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinimumSize
        )

        self.job_content_layout = QtWidgets.QVBoxLayout(self.contentWidget)
        self.job_content_layout.setObjectName("job_content_layout")

        self.job_status_btn_layout.setContentsMargins(5, 5, 5, 5)
        self.job_status_btn_layout.setSpacing(5)
        self.job_status_btn_layout.setObjectName("job_status_btn_layout")

        self.job_stats_display_layout = QtWidgets.QVBoxLayout()
        self.job_stats_display_layout.setObjectName("job_stats_display_layout")

        # -----------------------------Fonts
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)

        # ------------------------------Header

        self.js_file_name_icon = BlocksLabel(parent=self)

        self.js_file_name_icon.setSizePolicy(sizePolicy)
        self.js_file_name_icon.setMinimumSize(QtCore.QSize(60, 60))
        self.js_file_name_icon.setMaximumSize(QtCore.QSize(60, 60))
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

        self.js_file_name_label = BlocksLabel(parent=self)
        self.js_file_name_label.setEnabled(True)
        self.js_file_name_label.setSizePolicy(sizePolicy)
        self.js_file_name_label.setMinimumSize(QtCore.QSize(200, 80))
        self.js_file_name_label.setMaximumSize(QtCore.QSize(16777215, 60))

        self.js_file_name_label.setFont(font)
        self.js_file_name_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.js_file_name_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.js_file_name_label.setObjectName("js_file_name_label")

        self.job_status_header_layout.addWidget(self.js_file_name_icon)
        self.job_status_header_layout.addWidget(self.js_file_name_label)


        # -----------------------------buttons


        font.setPointSize(18)

        self.pause_printing_btn = BlocksCustomButton(self)
        self.pause_printing_btn.setSizePolicy(sizePolicy)
        self.pause_printing_btn.setMinimumSize(QtCore.QSize(200, 80))
        self.pause_printing_btn.setMaximumSize(QtCore.QSize(200, 80))
        self.pause_printing_btn.setFont(font)
        self.pause_printing_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/pause.svg")
        )
        self.pause_printing_btn.setObjectName("pause_printing_btn")

        self.stop_printing_btn = BlocksCustomButton(self)
        self.stop_printing_btn.setSizePolicy(sizePolicy)
        self.stop_printing_btn.setMinimumSize(QtCore.QSize(200, 80))
        self.stop_printing_btn.setMaximumSize(QtCore.QSize(200, 80))

        self.stop_printing_btn.setFont(font)
        self.stop_printing_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/stop.svg")
        )
        self.stop_printing_btn.setObjectName("stop_printing_btn")

        self.tune_menu_btn = BlocksCustomButton(self)
        self.tune_menu_btn.setSizePolicy(sizePolicy)

        self.tune_menu_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.tune_menu_btn.setMaximumSize(QtCore.QSize(200, 80))

        self.tune_menu_btn.setFont(font)
        self.tune_menu_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/tune.svg")
        )
        self.tune_menu_btn.setObjectName("tune_menu_btn")

        self.job_status_btn_layout.addWidget(self.pause_printing_btn)
        self.job_status_btn_layout.addWidget(self.stop_printing_btn)
        self.job_status_btn_layout.addWidget(self.tune_menu_btn)

        self.tune_menu_btn.setText("Tune")
        self.stop_printing_btn.setText("Cancel")
        self.pause_printing_btn.setText("Pause")

        # -----------------------------Progress bar

        self.printing_progress_bar = CustomProgressBar()
        self.printing_progress_bar.setMinimumHeight(150)

        self.printing_progress_bar.setObjectName("printing_progress_bar")
        self.printing_progress_bar.setSizePolicy(sizePolicy)

        self.job_status_progress_layout.addWidget(self.printing_progress_bar)

        # -----------------------------SMALL-THUMBNAIL

        self.CBVSmallThumbnail = ClickableGraphicsView(self.smallthumb_widget)
        self.CBVSmallThumbnail.setSizePolicy(sizePolicy)
        self.CBVSmallThumbnail.setMaximumSize(QtCore.QSize(48, 48))
        self.CBVSmallThumbnail.setStyleSheet(
            "QGraphicsView{\nbackground-color:transparent;\n}"
        )
        self.CBVSmallThumbnail.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.CBVSmallThumbnail.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.CBVSmallThumbnail.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        self.CBVSmallThumbnail.setBackgroundBrush(brush)
        self.CBVSmallThumbnail.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing
            | QtGui.QPainter.RenderHint.SmoothPixmapTransform
            | QtGui.QPainter.RenderHint.TextAntialiasing
        )
        self.CBVSmallThumbnail.setObjectName("CBVSmallThumbnail")

        self.smalllayout.addWidget(self.CBVSmallThumbnail)

        # -----------------------------Big-Thumbnail
        self.CBVBigThumbnail = ClickableGraphicsView()
        self.CBVBigThumbnail.setSizePolicy(sizePolicy)
        self.CBVBigThumbnail.setMaximumSize(QtCore.QSize(300, 300))
        self.CBVBigThumbnail.setStyleSheet(
            "QGraphicsView{\nbackground-color:transparent;\n}"
        )
        # "QGraphicsView{\nbackground-color:grey;border-radius:10px;\n}" grey background
        self.CBVBigThumbnail.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.CBVBigThumbnail.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.CBVBigThumbnail.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.CBVBigThumbnail.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.CBVBigThumbnail.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        self.CBVBigThumbnail.setBackgroundBrush(brush)
        self.CBVBigThumbnail.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing
            | QtGui.QPainter.RenderHint.SmoothPixmapTransform
            | QtGui.QPainter.RenderHint.TextAntialiasing
        )
        self.CBVBigThumbnail.setViewportUpdateMode(
            QtWidgets.QGraphicsView.ViewportUpdateMode.SmartViewportUpdate
        )

        self.CBVBigThumbnail.setObjectName("CBVBigThumbnail")
        self.biglayout.addWidget(self.CBVBigThumbnail)
        self.bigthumb_widget.hide()

        # -----------------------------display buttons

        self.layer_display_button = DisplayButton(self)
        self.layer_display_button.button_type = "display_secondary"
        self.layer_display_button.setEnabled(False)
        self.layer_display_button.setSizePolicy(sizePolicy)

        self.layer_display_button.setMinimumSize(QtCore.QSize(200, 80))

        self.layer_display_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/layers.svg")
        )
        self.layer_display_button.setObjectName("layer_display_button")

        self.print_time_display_button = DisplayButton(self)
        self.print_time_display_button.button_type = "display_secondary"
        self.print_time_display_button.setEnabled(False)
        self.print_time_display_button.setSizePolicy(sizePolicy)

        self.print_time_display_button.setMinimumSize(QtCore.QSize(200, 80))

        self.print_time_display_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/time.svg")
        )
        self.print_time_display_button.setObjectName(
            "print_time_display_button"
        )

        self.job_stats_display_layout.addWidget(
            self.layer_display_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.job_stats_display_layout.addWidget(
            self.print_time_display_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.job_content_layout.addLayout(self.job_stats_display_layout)
