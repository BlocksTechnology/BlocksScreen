from PyQt6 import QtCore, QtGui, QtWidgets
from utils.blocks_button import BlocksCustomButton
from utils.blocks_label import BlocksLabel


class ConfirmWidget(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUI()

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
        self.cf_info.setMinimumSize(QtCore.QSize(230, 60))
        self.cf_info.setMaximumSize(QtCore.QSize(250, 60))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
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
        font.setFamily("Montserrat")
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
        self.confirm_yes_text_label = BlocksCustomButton(parent=self)
        self.confirm_yes_text_label.setMinimumSize(QtCore.QSize(150, 60))
        self.confirm_yes_text_label.setMaximumSize(QtCore.QSize(150, 60))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.confirm_yes_text_label.setFont(font)
        self.confirm_yes_text_label.setMouseTracking(False)
        self.confirm_yes_text_label.setTabletTracking(True)
        self.confirm_yes_text_label.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.confirm_yes_text_label.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.confirm_yes_text_label.setStyleSheet("")
        self.confirm_yes_text_label.setAutoDefault(False)
        self.confirm_yes_text_label.setFlat(True)
        self.confirm_yes_text_label.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.confirm_yes_text_label.setObjectName("confirm_yes_text_label")
        self.cf_confirm_layout.addWidget(
            self.confirm_yes_text_label,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.confirm_no_text_label = BlocksCustomButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.confirm_no_text_label.sizePolicy().hasHeightForWidth()
        )
        self.confirm_no_text_label.setSizePolicy(sizePolicy)
        self.confirm_no_text_label.setMinimumSize(QtCore.QSize(150, 60))
        self.confirm_no_text_label.setMaximumSize(QtCore.QSize(150, 60))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(18)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.confirm_no_text_label.setFont(font)
        self.confirm_no_text_label.setMouseTracking(False)
        self.confirm_no_text_label.setTabletTracking(True)
        self.confirm_no_text_label.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.confirm_no_text_label.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.confirm_no_text_label.setStyleSheet("")
        self.confirm_no_text_label.setAutoDefault(False)
        self.confirm_no_text_label.setFlat(True)
        self.confirm_no_text_label.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.confirm_no_text_label.setObjectName("confirm_no_text_label")
        self.cf_confirm_layout.addWidget(
            self.confirm_no_text_label,
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
