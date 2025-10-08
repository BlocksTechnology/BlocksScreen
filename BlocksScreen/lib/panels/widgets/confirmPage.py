import typing

from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_label import BlocksLabel
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

import helper_methods


import os




class ConfirmWidget(QtWidgets.QWidget):
    on_accept: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, list, name="on_accept"
    )
    on_reject: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="on_reject"
    )

    on_delete: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str,str,name="on_delete"
    )

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUI()
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.thumbnail: QtGui.QImage = QtGui.QImage()
        self._thumbnails: typing.List = []
        self.confirm_button.clicked.connect(
            lambda: self.on_accept.emit(
                str(self.cf_file_name._text), self._thumbnails
            )
        )
        self.reject_button.clicked.connect(self.on_reject.emit)
        self.delete_btn.clicked.connect(lambda: self.on_delete.emit(self.direcotry,self.filename))
     

    @QtCore.pyqtSlot(str, dict, name="on_show_widget")
    def on_show_widget(self, text: str, filedata: dict | None = None) -> None:

        directory = os.path.dirname(text)
        filename = os.path.basename(text)

        self.direcotry = directory
        self.filename = filename


        self.cf_file_name.setText(self.filename)
        if not filedata:
            return
        self._thumbnails = filedata.get("thumbnail_images", [])

        if self._thumbnails:
            _biggest_thumbnail = self._thumbnails[
                -1
            ]  # Show last which is biggest
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
            _total_filament = str("%.2f" %_total_filament) + "kg"
        else:
            _total_filament = str("%.2f" %_total_filament) + "g"

        self.cf_info.setText(
            "Total Filament:"
            + "\n"
            + _total_filament
            + "\n"
            + "Slicer time: "
            +"\n"
            + time_str
            + "\n"
        )

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

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
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
        if not self.thumbnail:
            self.cf_thumbnail.close()
        return super().showEvent(a0)

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        return super().hideEvent(a0)

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
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cf_header_title = QtWidgets.QHBoxLayout()
        self.cf_header_title.setObjectName("cf_header_title")

        self.delete_btn = IconButton(self)
        self.delete_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.delete_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.delete_btn.setFlat(True)
        self.delete_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/troubleshoot.svg")
        )
        self.cf_header_title.addWidget(
            self.delete_btn, 0, QtCore.Qt.AlignmentFlag.AlignLeft
        )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )


        self.confirm_title_label = QtWidgets.QLabel(parent=self)
        self.confirm_title_label.setMinimumSize(QtCore.QSize(0, 60))
        self.confirm_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.confirm_title_label.setFont(font)
        self.confirm_title_label.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.confirm_title_label.setSizePolicy(sizePolicy)
        self.confirm_title_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.confirm_title_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.confirm_title_label.setObjectName("confirm_title_label")
        self.cf_header_title.addWidget(self.confirm_title_label)
        self.spacer = QtWidgets.QSpacerItem(
            60, 60, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.spacer.setGeometry(QtCore.QRect(0, 0, 60, 60))
        self.cf_header_title.addItem(self.spacer)
        self.verticalLayout_4.addLayout(self.cf_header_title)
        self.cf_content_vertical_layout = QtWidgets.QHBoxLayout()
        self.cf_content_vertical_layout.setObjectName(
            "cf_content_vertical_layout"
        )
        self.cf_content_horizontal_layout = QtWidgets.QVBoxLayout()
        self.cf_content_horizontal_layout.setObjectName(
            "cf_content_horizontal_layout"
        )
        self.cf_file_name = BlocksLabel(parent=self)
        self.cf_file_name.setEnabled(True)
        self.cf_file_name.setMinimumSize(QtCore.QSize(250, 0))
        self.cf_file_name.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(14)
        self.cf_file_name.setFont(font)
        self.cf_file_name.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.cf_file_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cf_file_name.setWordWrap(True)
        self.cf_file_name.setObjectName("cf_file_name")
        self.cf_content_horizontal_layout.addWidget(
            self.cf_file_name, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.cf_info = QtWidgets.QLabel(parent=self)
        self.cf_info.setEnabled(True)
        self.cf_info.setMinimumSize(QtCore.QSize(200, 60))
        self.cf_info.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(14)
        self.cf_info.setFont(font)
        self.cf_info.setStyleSheet("background: transparent; color: white;")
        self.cf_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cf_info.setWordWrap(True)
        self.cf_info.setObjectName("cf_info")
        self.cf_content_horizontal_layout.addWidget(
            self.cf_info,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.cf_confirm_layout = QtWidgets.QVBoxLayout()
        self.cf_confirm_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetFixedSize
        )
        self.cf_confirm_layout.setContentsMargins(0, 0, 0, 0)
        self.cf_confirm_layout.setSpacing(2)
        self.cf_confirm_layout.setObjectName("cf_confirm_layout")
        self.confirm_button = BlocksCustomButton(parent=self)
        self.confirm_button.setMinimumSize(QtCore.QSize(250, 70))
        self.confirm_button.setMaximumSize(QtCore.QSize(250, 70))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(18)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.confirm_button.setFont(font)
        self.confirm_button.setMouseTracking(False)
        self.confirm_button.setTabletTracking(True)
        self.confirm_button.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.confirm_button.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.confirm_button.setStyleSheet("")
        self.confirm_button.setAutoDefault(False)
        self.confirm_button.setFlat(True)
        self.confirm_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.confirm_button.setObjectName("confirm_button")
        self.cf_confirm_layout.addWidget(
            self.confirm_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.reject_button = BlocksCustomButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.reject_button.sizePolicy().hasHeightForWidth()
        )
        self.reject_button.setSizePolicy(sizePolicy)
        self.reject_button.setMinimumSize(QtCore.QSize(250, 70))
        self.reject_button.setMaximumSize(QtCore.QSize(250, 70))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(18)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        self.reject_button.setFont(font)
        self.reject_button.setMouseTracking(False)
        self.reject_button.setTabletTracking(True)
        self.reject_button.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.reject_button.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.reject_button.setStyleSheet("")
        self.reject_button.setAutoDefault(False)
        self.reject_button.setFlat(True)
        self.reject_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.reject_button.setObjectName("reject")
        self.cf_confirm_layout.addWidget(
            self.reject_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.cf_content_horizontal_layout.addLayout(self.cf_confirm_layout)
        self.cf_content_vertical_layout.addLayout(
            self.cf_content_horizontal_layout
        )
        self.cf_thumbnail = QtWidgets.QGraphicsView(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.cf_thumbnail.sizePolicy().hasHeightForWidth()
        )
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
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.verticalLayout_4.addLayout(self.cf_content_vertical_layout)

        self.confirm_title_label.setText("Print File?")
        self.confirm_button.setText("Accept")
        self.reject_button.setText("Cancel")
