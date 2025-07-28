import typing

from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_label import BlocksLabel
from PyQt6 import QtCore, QtGui, QtWidgets


class ConfirmWidget(QtWidgets.QWidget):
    on_accept: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="on_accept"
    )
    on_reject: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="on_reject"
    )

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUI()
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.thumbnail: QtGui.QImage = QtGui.QImage()
        self.confirm_button.clicked.connect(
            lambda: self.on_accept.emit(str(self.cf_file_name._text))
        )
        self.reject_button.clicked.connect(self.on_reject.emit)

    @QtCore.pyqtSlot(str, dict, name="on_show_widget")
    def on_show_widget(self, text: str, filedata: dict | None = None) -> None:
        self.cf_file_name.setText(str(text))
        if not filedata:
            return
        _thumbnails = filedata.get("thumbnail_images")

        if _thumbnails:
            _biggest_thumbnail = _thumbnails[len(_thumbnails) - 1]
            self.thumbnail = QtGui.QImage(_biggest_thumbnail)

        _total_filament = filedata.get("filament_total")
        _estimated_time = filedata.get("estimated_time")
        self.cf_info.setText(
            "Total Filament:"
            + str(_total_filament)
            + "\n"
            + "Slicer time: "
            + str(_estimated_time)
        )
        self.repaint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        _scene = QtWidgets.QGraphicsScene()
        if not self.thumbnail.isNull():
            _graphics_rect = self.cf_thumbnail.rect().toRectF()
            _image_rect = self.thumbnail.rect()

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
                QtGui.QPixmap.fromImage(self.thumbnail).scaled(
                    int(scaled_width),
                    int(scaled_height),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
            )
            _scene.addItem(_item_scaled)
            self.cf_thumbnail.setScene(_scene)

        else:
            self.cf_thumbnail.setScene(_scene)

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
        self.confirm_title_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.confirm_title_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.confirm_title_label.setObjectName("confirm_title_label")
        self.cf_header_title.addWidget(self.confirm_title_label)
        self.verticalLayout_4.addLayout(self.cf_header_title)
        self.cf_content_vertical_layout = QtWidgets.QHBoxLayout()
        self.cf_content_vertical_layout.setObjectName(
            "cf_content_vertical_layout"
        )
        self.cf_content_horizontal_layout = QtWidgets.QVBoxLayout()
        self.cf_content_horizontal_layout.setObjectName(
            "cf_content_horizontal_layout"
        )
        self.cf_info = QtWidgets.QLabel(parent=self)
        self.cf_info.setEnabled(True)
        self.cf_info.setMinimumSize(QtCore.QSize(200, 60))
        self.cf_info.setMaximumSize(QtCore.QSize(250, 60))
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
        self.cf_file_name = BlocksLabel(parent=self)
        self.cf_file_name.setEnabled(True)
        self.cf_file_name.setMinimumSize(QtCore.QSize(250, 80))
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
        self.cf_confirm_layout = QtWidgets.QVBoxLayout()
        self.cf_confirm_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetFixedSize
        )
        self.cf_confirm_layout.setContentsMargins(0, 0, 0, 0)
        self.cf_confirm_layout.setSpacing(2)
        self.cf_confirm_layout.setObjectName("cf_confirm_layout")
        self.confirm_button = BlocksCustomButton(parent=self)
        self.confirm_button.setMinimumSize(QtCore.QSize(200, 60))
        self.confirm_button.setMaximumSize(QtCore.QSize(200, 60))
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
        self.reject_button.setMinimumSize(QtCore.QSize(200, 60))
        self.reject_button.setMaximumSize(QtCore.QSize(200, 60))
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
        self.cf_thumbnail = QtWidgets.QGraphicsView(parent=self)
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
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.verticalLayout_4.addLayout(self.cf_content_vertical_layout)

        self.confirm_title_label.setText("Print File?")
        self.confirm_button.setText("Accept")
        self.reject_button.setText("Cancel")
