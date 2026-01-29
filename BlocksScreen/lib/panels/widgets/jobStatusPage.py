import logging
import typing

import events
from helper_methods import calculate_current_layer, estimate_print_time
from lib.panels.widgets.basePopup import BasePopup
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_label import BlocksLabel
from lib.utils.blocks_progressbar import CustomProgressBar
from lib.utils.display_button import DisplayButton
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger("logs/BlocksScreen.log")


class JobStatusWidget(QtWidgets.QWidget):
    """Job status widget page, page shown when there is a active print job.

    Enables mid print printer tuning and inspection of print progress.


    Args:
        QtWidgets (QtWidgets.QWidget): Parent widget
    """

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
    print_finish: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="print_finish"
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
    request_query_print_stats: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="request_query_print_stats"
    )
    request_file_info: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request_file_info"
    )
    call_cancel_panel = QtCore.pyqtSignal(bool, name="call-load-panel")

    _internal_print_status: str = ""
    _current_file_name: str = ""
    file_metadata: dict = {}
    total_layers = "?"

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.thumbnail_graphics = []
        self.layer_fallback = False
        self._setupUI()
        self.cancel_print_dialog = BasePopup(self, floating=True)
        self.tune_menu_btn.clicked.connect(self.tune_clicked.emit)
        self.pause_printing_btn.clicked.connect(self.pause_resume_print)
        self.stop_printing_btn.clicked.connect(self.handleCancel)

    @QtCore.pyqtSlot(name="toggle-thumbnail-expansion")
    def toggle_thumbnail_expansion(self) -> None:
        """Toggle thumbnail expansion"""
        if not self.thumbnail_view.scene():
            return
        if not self.thumbnail_view.isVisible():
            self.thumbnail_view.show()
            self.progressWidget.hide()
            self.contentWidget.hide()
            self.printing_progress_bar.hide()
            self.btnWidget.hide()
            self.headerWidget.hide()
            return
        self.thumbnail_view.hide()
        self.progressWidget.show()
        self.contentWidget.show()
        self.printing_progress_bar.show()
        self.btnWidget.show()
        self.headerWidget.show()
        self.show()

    def showEvent(self, a0) -> None:
        """Reimplemented method, handle `show` Event"""
        if self._current_file_name:
            self.request_file_info.emit(self._current_file_name)

    def eventFilter(self, sender_obj: QtCore.QObject, event: events.QEvent) -> bool:
        """Filter events,

        currently only filters events from `self.thumbnail_view` QGraphicsView widget
        """
        if (
            sender_obj == self.thumbnail_view
            and event.type() == QtCore.QEvent.Type.MouseButtonPress
        ):
            self.toggle_thumbnail_expansion()
            return True
        return super().eventFilter(sender_obj, event)

    def _load_thumbnails(self, *thumbnails) -> None:
        """Pre-load available thumbnails for the current print object"""
        self.thumbnail_graphics = list(
            filter(
                lambda thumb: not thumb.isNull(),
                [QtGui.QPixmap(thumb) for thumb in thumbnails],
            )
        )
        if not self.thumbnail_graphics:
            logger.debug("Unable to load thumbnails, no thumbnails provided")
            return
        self.create_thumbnail_widget()
        self.thumbnail_view.installEventFilter(self)
        scene = QtWidgets.QGraphicsScene()
        _biggest_thumb = self.thumbnail_graphics[-1]
        self.thumbnail_view.setSceneRect(
            QtCore.QRectF(
                self.rect().x(),
                self.rect().y(),
                _biggest_thumb.width(),
                _biggest_thumb.height(),
            )
        )
        scaled = QtGui.QPixmap(_biggest_thumb).scaled(
            _biggest_thumb.width(),
            _biggest_thumb.height(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        item = QtWidgets.QGraphicsPixmapItem(scaled)
        scene.addItem(item)
        self.thumbnail_view.setFrameRect(
            QtCore.QRect(
                0, 0, self.contentsRect().width(), self.contentsRect().height()
            )
        )
        self.thumbnail_view.setScene(scene)
        self.printing_progress_bar.set_inner_pixmap(self.thumbnail_graphics[-1])
        self.printing_progress_bar.thumbnail_clicked.connect(
            self.toggle_thumbnail_expansion
        )

    @QtCore.pyqtSlot(name="handle-cancel")
    def handleCancel(self) -> None:
        """Handle cancel print job dialog"""
        self.cancel_print_dialog.set_message(
            "Are you sure you \n want to cancel \n the current print job?"
        )
        self.cancel_print_dialog.accepted.connect(self.print_cancel)
        self.cancel_print_dialog.open()

    @QtCore.pyqtSlot(str, name="on_print_start")
    def on_print_start(self, file: str) -> None:
        """Start a print job, show job status page"""
        self._current_file_name = file
        self.js_file_name_label.setText(self._current_file_name)
        self.layer_display_button.setText("?")
        self.print_time_display_button.setText("?")
        self.printing_progress_bar.reset()
        self._internal_print_status = "printing"
        self.request_file_info.emit(file)
        self.print_start.emit(file)
        print_start_event = events.PrintStart(
            self._current_file_name, self.file_metadata
        )
        try:
            instance = QtWidgets.QApplication.instance()
            if instance:
                instance.postEvent(self.window(), print_start_event)
            else:
                raise TypeError("QApplication.instance expected non None value")
        except Exception as e:
            logger.debug("Unexpected error while posting print job start event: %s", e)

    @QtCore.pyqtSlot(dict, name="on_fileinfo")
    def on_fileinfo(self, fileinfo: dict) -> None:
        """Handle received file information/metadata"""
        if not self.isVisible():
            return
        self.total_layers = str(fileinfo.get("layer_count", "---"))
        self.layer_display_button.setText("---")
        self.layer_display_button.secondary_text = str(self.total_layers)
        self.file_metadata = fileinfo
        self._load_thumbnails(*fileinfo.get("thumbnail_images", []))

    @QtCore.pyqtSlot(name="pause_resume_print")
    def pause_resume_print(self) -> None:
        """Handle pause/resume print job button clicked"""
        self.pause_printing_btn.setEnabled(False)
        if self._internal_print_status == "printing":
            self._internal_print_status = "paused"
            self.print_pause.emit()
        elif self._internal_print_status == "paused":
            self._internal_print_status = "printing"
            self.print_resume.emit()

    def _handle_print_state(self, state: str) -> None:
        """Handle print state change received from
        printer_status object updated
        """
        valid_states = {"printing", "paused"}
        invalid_states = {"cancelled", "complete", "error", "standby"}
        lstate = state.lower()
        if lstate in valid_states:
            self._internal_print_status = lstate
            if lstate == "paused":
                self.pause_printing_btn.setText(" Resume")
                self.pause_printing_btn.setPixmap(
                    QtGui.QPixmap(":/ui/media/btn_icons/play.svg")
                )
            elif lstate == "printing":
                self.pause_printing_btn.setText("Pause")
                self.pause_printing_btn.setPixmap(
                    QtGui.QPixmap(":/ui/media/btn_icons/pause.svg")
                )
            self.pause_printing_btn.setEnabled(True)
            self.request_query_print_stats.emit({"print_stats": ["filename"]})
            self.call_cancel_panel.emit(False)
            self.show_request.emit()
            lstate = "start"
        elif lstate in invalid_states:
            if lstate != "standby":
                self.print_finish.emit()
            self._internal_print_status = ""
            self._current_file_name = ""
            self.total_layers = "?"
            self.file_metadata.clear()
            self.hide_request.emit()
            # if hasattr(self, "thumbnail_view"):
            #     getattr(self, "thumbnail_view").deleteLater()
        # Send Event on Print state
        if hasattr(events, str("Print" + lstate.capitalize())):
            event_obj = getattr(events, str("Print" + lstate.capitalize()))
            event = event_obj(self._current_file_name, self.file_metadata)
            instance = QtWidgets.QApplication.instance()
            if instance:
                instance.postEvent(self.window(), event)
                return
            logger.error(
                "QApplication.instance expected non None value,\
                    Unable to post event %s",
                str("Print" + lstate.capitalize()),
            )

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """Processes the information that comes from the printer object "print_stats"
            Displays information on the ui accordingly.

        Args:
            field (str): The name of the updated field.
            value (dict | float | str): The value for the field.
        """
        if isinstance(value, str):
            if "state" in field:
                self._handle_print_state(value)
            if "filename" in field:
                self._current_file_name = value
                if self.js_file_name_label.text().lower() != value.lower():
                    self.js_file_name_label.setText(self._current_file_name)
                if self.isVisible():
                    self.request_file_info.emit(value)
        if not self.file_metadata:
            return
        if not self.isVisible():
            return
        if isinstance(value, dict):
            self.layer_fallback = False
            if "total_layer" in value.keys():
                self.total_layers = value["total_layer"]
                if value["total_layer"] is not None:
                    self.layer_display_button.secondary_text = str(self.total_layers)

                else:
                    self.total_layers = "---"
                    self.layer_fallback = True

            if "current_layer" in value.keys():
                if value["current_layer"] is not None:
                    _current_layer = value["current_layer"]
                    self.layer_display_button.setText(f"{int(_current_layer)}")
                else:
                    self.layer_display_button.setText("---")
                    self.layer_fallback = True
        elif isinstance(value, float):
            if "total_duration" in field:
                _time = estimate_print_time(int(value))
                _print_time_string = (
                    f"{_time[0]}Day {_time[1]}H {_time[2]}min {_time[3]} s"
                    if _time[0] != 0
                    else f"{_time[1]}H {_time[2]}min {_time[3]}s"
                )
                self.print_time_display_button.setText(_print_time_string)

    @QtCore.pyqtSlot(str, list, name="on_gcode_move_update")
    def on_gcode_move_update(self, field: str, value: list) -> None:
        """Handle gcode move"""
        if not self.isVisible():
            return
        if "gcode_position" in field:
            if self._internal_print_status == "printing":
                if self.layer_fallback:
                    object_height = float(self.file_metadata.get("object_height", -1.0))
                    layer_height = float(self.file_metadata.get("layer_height", -1.0))
                    first_layer_height = float(
                        self.file_metadata.get("first_layer_height", -1.0)
                    )
                    _current_layer = calculate_current_layer(
                        z_position=value[2],
                        object_height=object_height,
                        layer_height=layer_height,
                        first_layer_height=first_layer_height,
                    )

                    total_layer = (
                        (object_height) / layer_height if layer_height > 0 else -1
                    )
                    self.layer_display_button.secondary_text = (
                        f"{int(total_layer)}" if total_layer != -1 else "---"
                    )
                    self.layer_display_button.setText(
                        f"{int(_current_layer)}" if _current_layer != -1 else "---"
                    )

    @QtCore.pyqtSlot(str, float, name="virtual_sdcard_update")
    @QtCore.pyqtSlot(str, bool, name="virtual_sdcard_update")
    def virtual_sdcard_update(self, field: str, value: float | bool) -> None:
        """Handle virtual sdcard

        Args:
            field (str): Name of the updated field on the virtual_sdcard object
            value (float | bool): The updated information for the corresponding field
        """
        if not self.isVisible():
            return
        if "progress" == field:
            self.printing_progress_bar.setValue(value)

    def _setupUI(self) -> None:
        """Setup widget ui"""
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 420))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
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
        self.job_status_header_layout = QtWidgets.QHBoxLayout(self.headerWidget)
        self.job_status_header_layout.setSpacing(20)
        self.job_status_header_layout.setObjectName("job_status_header_layout")
        self.job_status_progress_layout = QtWidgets.QVBoxLayout(self.progressWidget)
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
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        self.js_file_name_icon = BlocksLabel(parent=self)
        self.js_file_name_icon.setSizePolicy(sizePolicy)
        self.js_file_name_icon.setMinimumSize(QtCore.QSize(60, 60))
        self.js_file_name_icon.setMaximumSize(QtCore.QSize(60, 60))
        self.js_file_name_icon.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.js_file_name_icon.setStyleSheet("background: transparent; color: white;")
        self.js_file_name_icon.setText("")
        self.js_file_name_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
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
        self.js_file_name_label.setStyleSheet("background: transparent; color: white;")
        self.js_file_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.js_file_name_label.setObjectName("js_file_name_label")
        self.job_status_header_layout.addWidget(self.js_file_name_icon)
        self.job_status_header_layout.addWidget(self.js_file_name_label)
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
        self.printing_progress_bar = CustomProgressBar(self)
        self.printing_progress_bar.setMinimumHeight(150)
        self.printing_progress_bar.setObjectName("printing_progress_bar")
        self.printing_progress_bar.setSizePolicy(sizePolicy)
        self.job_status_progress_layout.addWidget(self.printing_progress_bar)
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
        self.print_time_display_button.button_type = "normal"
        self.print_time_display_button.setEnabled(False)
        self.print_time_display_button.setSizePolicy(sizePolicy)
        self.print_time_display_button.setMinimumSize(QtCore.QSize(200, 80))
        self.print_time_display_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/time.svg")
        )
        self.print_time_display_button.setObjectName("print_time_display_button")
        self.job_stats_display_layout.addWidget(
            self.layer_display_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.job_stats_display_layout.addWidget(
            self.print_time_display_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.job_content_layout.addLayout(self.job_stats_display_layout)

    def create_thumbnail_widget(self) -> None:
        """Create thumbnail graphics view widget"""
        self.thumbnail_view = QtWidgets.QGraphicsView()
        self.thumbnail_view.setMinimumSize(QtCore.QSize(48, 48))
        self.thumbnail_view.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self.thumbnail_view.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.thumbnail_view.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.thumbnail_view.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.thumbnail_view.setObjectName("thumbnail_scene")
        _thumbnail_palette = QtGui.QPalette()
        _thumbnail_palette.setColor(
            QtGui.QPalette.ColorRole.Window, QtGui.QColor(0, 0, 0, 0)
        )
        _thumbnail_palette.setColor(
            QtGui.QPalette.ColorRole.Base, QtGui.QColor(0, 0, 0, 0)
        )
        self.thumbnail_view.setPalette(_thumbnail_palette)
        _thumbnail_brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        _thumbnail_brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        self.thumbnail_view.setBackgroundBrush(_thumbnail_brush)
        self.thumbnail_view.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing
            | QtGui.QPainter.RenderHint.SmoothPixmapTransform
            | QtGui.QPainter.RenderHint.LosslessImageRendering
        )
        self.thumbnail_view.setViewportUpdateMode(
            QtWidgets.QGraphicsView.ViewportUpdateMode.SmartViewportUpdate
        )
        self.thumbnail_view.setObjectName("thumbnail_scene")
        self.thumbnail_view_layout = QtWidgets.QHBoxLayout(self)
        self.thumbnail_view_layout.addWidget(self.thumbnail_view)
        self.thumbnail_view.hide()
