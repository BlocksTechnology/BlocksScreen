import os
import typing

import helper_methods
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_label import BlocksLabel
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class ConfirmWidget(QtWidgets.QWidget):
    on_accept: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, list, name="on_accept"
    )
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(name="on_reject")
    on_delete: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, name="on_delete"
    )

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUI()
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.thumbnail: QtGui.QImage = QtGui.QImage()
        self._thumbnails: typing.List = []
        self.directory = ""
        self.filename = ""
        self.confirm_button.clicked.connect(
            lambda: self.on_accept.emit(
                str(os.path.join(self.directory, self.filename)), self._thumbnails
            )
        )
        self.back_btn.clicked.connect(self.request_back.emit)
        self.delete_file_button.clicked.connect(
            lambda: self.on_delete.emit(self.directory, self.filename)
        )

    @QtCore.pyqtSlot(str, dict, name="on_show_widget")
    def on_show_widget(self, text: str, filedata: dict | None = None) -> None:
        """Handle widget show"""
        directory = os.path.dirname(text)
        filename = os.path.basename(text)
        self.directory = directory
        self.filename = filename
        self.cf_file_name.setText(self.filename)
        if not filedata:
            return
        self._thumbnails = filedata.get("thumbnail_images", [])
        if self._thumbnails:
            _biggest_thumbnail = self._thumbnails[-1]  # Show last which is biggest
            self.thumbnail = QtGui.QImage(_biggest_thumbnail)
        _total_filament = filedata.get("filament_weight_total")
        _estimated_time = filedata.get("estimated_time")
        if isinstance(_estimated_time, str):
            seconds = 0
        else:
            seconds = _estimated_time

        days, hours, minutes, _ = helper_methods.estimate_print_time(seconds)
        if seconds <= 0:
            time_str = "??"
        elif seconds < 60:
            time_str = "less than 1 minute"
        else:
            if days > 0:
                time_str = f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                time_str = f"{hours}h {minutes}m"
            else:
                time_str = f"{minutes}m"
        if _total_filament == 0:
            _total_filament = "Unknown"
        elif _total_filament > 499:
            _total_filament /= 1000
            _total_filament = str("%.2f" % _total_filament) + "kg"
        else:
            _total_filament = str("%.2f" % _total_filament) + "g"
        filament_label = f"Total Filament: {_total_filament}"
        time_label = f"Slicer time: {time_str}"
        self.cf_info_tf.setText(f"{filament_label}")
        self.cf_info_tr.setText(f"{time_label}")
        self.repaint()

    def estimate_print_time(self, seconds: int) -> list:
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

    def hide(self):
        """Hide widget"""
        self.directory = ""
        self.filename = ""
        return super().hide()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        if not self.isVisible():
            self.directory = ""
            self.filename = ""
        if not hasattr(self, "_scene"):
            self._scene = QtWidgets.QGraphicsScene(self)
            self.cf_thumbnail.setScene(self._scene)

        # Pick thumbnail or fallback logo
        if self.thumbnail.isNull():
            self.thumbnail = QtGui.QImage(
                "BlocksScreen/lib/ui/resources/media/logoblocks400x300.png"
            )

        # Scene rectangle (available display area)
        graphics_rect = self.cf_thumbnail.rect().toRectF()

        # Scale pixmap preserving aspect ratio
        pixmap = QtGui.QPixmap.fromImage(self.thumbnail).scaled(
            graphics_rect.size().toSize(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

        # Centering offsets
        adjusted_x = (graphics_rect.width() - pixmap.width()) / 2.0
        adjusted_y = (graphics_rect.height() - pixmap.height()) / 2.0

        # Update existing pixmap item or create it once
        if not hasattr(self, "_pixmap_item"):
            self._pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self._scene.addItem(self._pixmap_item)
        else:
            self._pixmap_item.setPixmap(pixmap)

        self._pixmap_item.setPos(adjusted_x, adjusted_y)
        self._scene.setSceneRect(graphics_rect)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, Handle widget show event"""
        if not self.thumbnail:
            self.cf_thumbnail.close()
        return super().showEvent(a0)

    def setupUI(self) -> None:
        """Setup widget ui"""
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
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cf_header_title = QtWidgets.QHBoxLayout()
        self.cf_header_title.setObjectName("cf_header_title")

        self.spacer = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.spacer.setGeometry(QtCore.QRect(0, 0, 60, 60))
        self.cf_header_title.addItem(self.spacer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.cf_file_name = BlocksLabel(parent=self)
        self.cf_file_name.setMinimumSize(QtCore.QSize(0, 60))
        self.cf_file_name.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.cf_file_name.setFont(font)
        self.cf_file_name.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.cf_file_name.setSizePolicy(sizePolicy)
        self.cf_file_name.setStyleSheet("background: transparent; color: white;")
        self.cf_file_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cf_file_name.setObjectName("cf_file_name")
        self.cf_header_title.addWidget(self.cf_file_name)

        self.back_btn = IconButton(self)
        self.back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.back_btn.setFlat(True)
        self.back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.cf_header_title.addWidget(
            self.back_btn, 0, QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.verticalLayout_4.addLayout(self.cf_header_title)
        self.cf_content_vertical_layout = QtWidgets.QHBoxLayout()
        self.cf_content_vertical_layout.setObjectName("cf_content_vertical_layout")
        self.cf_content_horizontal_layout = QtWidgets.QVBoxLayout()
        self.cf_content_horizontal_layout.setObjectName("cf_content_horizontal_layout")
        self.info_frame = BlocksCustomFrame(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.info_frame.setSizePolicy(sizePolicy)

        self.info_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.info_layout = QtWidgets.QVBoxLayout(self.info_frame)

        self.cf_info_tf = QtWidgets.QLabel(parent=self.info_frame)
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(14)

        self.cf_info_tf.setFont(font)
        self.cf_info_tf.setStyleSheet("background: transparent; color: white;")

        self.cf_info_tf.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.info_layout.addWidget(self.cf_info_tf)

        self.cf_info_tr = QtWidgets.QLabel(parent=self.info_frame)

        self.cf_info_tr.setFont(font)
        self.cf_info_tr.setStyleSheet("background: transparent; color: white;")
        self.cf_info_tr.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.info_layout.addWidget(self.cf_info_tr)

        self.cf_confirm_layout = QtWidgets.QVBoxLayout()
        self.cf_confirm_layout.setSpacing(15)

        self.confirm_button = BlocksCustomButton(parent=self.info_frame)
        self.confirm_button.setMinimumSize(QtCore.QSize(250, 70))
        self.confirm_button.setMaximumSize(QtCore.QSize(250, 70))
        font = QtGui.QFont("Momcake", 18)
        self.confirm_button.setFont(font)
        self.confirm_button.setFlat(True)
        self.confirm_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.confirm_button.setText("Print")
        # 2. Align buttons to the right
        self.cf_confirm_layout.addWidget(
            self.confirm_button, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.delete_file_button = BlocksCustomButton(parent=self.info_frame)
        self.delete_file_button.setMinimumSize(QtCore.QSize(250, 70))
        self.delete_file_button.setMaximumSize(QtCore.QSize(250, 70))
        self.delete_file_button.setFont(font)
        self.delete_file_button.setFlat(True)
        self.delete_file_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/garbage-icon.svg")
        )
        self.delete_file_button.setText("Delete")
        # 2. Align buttons to the right
        self.cf_confirm_layout.addWidget(
            self.delete_file_button, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.info_layout.addLayout(self.cf_confirm_layout)

        self.cf_content_horizontal_layout.addWidget(self.info_frame)

        self.cf_content_vertical_layout.addLayout(self.cf_content_horizontal_layout)
        self.cf_thumbnail = QtWidgets.QGraphicsView(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.cf_thumbnail.sizePolicy().hasHeightForWidth())
        self.cf_thumbnail.setSizePolicy(sizePolicy)
        self.cf_thumbnail.setMinimumSize(QtCore.QSize(400, 300))
        self.cf_thumbnail.setMaximumSize(QtCore.QSize(400, 300))
        self.cf_thumbnail.setStyleSheet(
            "QGraphicsView{\nbackground-color: transparent;\n}"
        )
        self.cf_thumbnail.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.cf_thumbnail.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.cf_thumbnail.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.cf_thumbnail.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.cf_thumbnail.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        self.cf_thumbnail.setBackgroundBrush(brush)
        self.cf_thumbnail.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing
            | QtGui.QPainter.RenderHint.SmoothPixmapTransform
            | QtGui.QPainter.RenderHint.TextAntialiasing
        )
        self.cf_thumbnail.setViewportUpdateMode(
            QtWidgets.QGraphicsView.ViewportUpdateMode.SmartViewportUpdate
        )
        self.cf_thumbnail.setObjectName("cf_thumbnail")
        self.cf_content_vertical_layout.addWidget(
            self.cf_thumbnail,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.verticalLayout_4.addLayout(self.cf_content_vertical_layout)
