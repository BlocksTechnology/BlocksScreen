from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_label import BlocksLabel
from PyQt6 import QtCore, QtGui, QtWidgets


class CancelPage(QtWidgets.QWidget):
    """Update GUI Page,
    retrieves from moonraker available clients and adds functionality
    for updating or recovering them
    """

    def __init__(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self._setupUI()
        self.confirm_button.clicked.connect(self.hide)
        self.refuse_button.clicked.connect(self.hide)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

    def set_pixmap(self, pixmap: QtGui.QPixmap) -> None:
        if not hasattr(self, "_scene"):
            self._scene = QtWidgets.QGraphicsScene(self)
            self.cf_thumbnail.setScene(self._scene)

        # Scene rectangle (available display area)
        graphics_rect = self.cf_thumbnail.rect().toRectF()

        # Scale pixmap preserving aspect ratio
        pixmap = pixmap.scaled(
            graphics_rect.size().toSize(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

        adjusted_x = (graphics_rect.width() - pixmap.width()) / 2.0
        adjusted_y = (graphics_rect.height() - pixmap.height()) / 2.0

        if not hasattr(self, "_pixmap_item"):
            self._pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self._scene.addItem(self._pixmap_item)
        else:
            self._pixmap_item.setPixmap(pixmap)

        self._pixmap_item.setPos(adjusted_x, adjusted_y)
        self._scene.setSceneRect(graphics_rect)

    def set_file_name(self, file_name: str) -> None:
        self.cf_file_name.setText(file_name)

    def _setupUI(self) -> None:
        """Setup widget ui"""
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setObjectName("cancelPage")
        self.setStyleSheet(
            """#cancelPage {
                background-image: url(:/background/media/1st_background.png);
            }"""
        )
        self.setMinimumSize(QtCore.QSize(800, 480))
        self.setMaximumSize(QtCore.QSize(800, 480))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cf_header_title = QtWidgets.QHBoxLayout()
        self.cf_header_title.setObjectName("cf_header_title")

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
        self.cf_info_tf.setText("Print job was\ncancelled")
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(20)

        self.cf_info_tf.setFont(font)
        self.cf_info_tf.setStyleSheet("background: transparent; color: white;")

        self.cf_info_tf.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_layout.addWidget(self.cf_info_tf)

        self.cf_info_tr = QtWidgets.QLabel(parent=self.info_frame)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.cf_info_tr.setFont(font)
        self.cf_info_tr.setStyleSheet("background: transparent; color: white;")
        self.cf_info_tr.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.cf_info_tr.setText("Do you want to reprint?")
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
        self.confirm_button.setText("Reprint")
        # 2. Align buttons to the right
        self.cf_confirm_layout.addWidget(
            self.confirm_button, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.refuse_button = BlocksCustomButton(parent=self.info_frame)
        self.refuse_button.setMinimumSize(QtCore.QSize(250, 70))
        self.refuse_button.setMaximumSize(QtCore.QSize(250, 70))
        self.refuse_button.setFont(font)
        self.refuse_button.setFlat(True)
        self.refuse_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.refuse_button.setText("Ignore")
        # 2. Align buttons to the right
        self.cf_confirm_layout.addWidget(
            self.refuse_button, 0, QtCore.Qt.AlignmentFlag.AlignCenter
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
            self.cf_thumbnail, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.verticalLayout_4.addLayout(self.cf_content_vertical_layout)
