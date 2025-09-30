from PyQt6 import QtCore, QtWidgets, QtGui
import typing
import logging

from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.icon_button import IconButton


class UpdatePage(QtWidgets.QWidget):
    request_update_klipper: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-klipper"
    )
    request_update_moonraker: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-moonraker"
    )
    request_update_client: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="update-client"
    )
    request_update_system: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-system"
    )
    request_full_update: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-full"
    )
    request_update_status: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="update-status"
    )
    request_refresh_update: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="update-refresh"
    )
    request_recover_repo: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str], [str, bool], name="recover-repo"
    )
    request_rollback_update: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="rollback-update"
    )

    def __init__(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()

        self._setupUI()

    def _setupUI(self) -> None:
        font_id = QtGui.QFontDatabase.addApplicationFont(
            ":/font/media/fonts for text/Momcake-Bold.ttf"
        )
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.update_page_content_layout = QtWidgets.QVBoxLayout()
        self.update_page_content_layout.setContentsMargins(15, 15, 2, 2)

        self.header_content_layout = QtWidgets.QHBoxLayout()
        self.header_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.header_title = QtWidgets.QLabel(self)
        self.header_title.setMinimumSize(QtCore.QSize(100, 60))
        self.header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily(font_family)
        font.setPointSize(24)
        palette = self.header_title.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.header_title.setFont(font)
        self.header_title.setPalette(palette)
        self.header_title.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header_title.setObjectName("header-title")
        self.header_title.setText("Update Manager")
        self.header_content_layout.addWidget(self.header_title, 0)
        self.update_back_btn = IconButton(self)
        self.update_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.update_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.update_back_btn.setFlat(True)
        self.update_back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.header_content_layout.addWidget(self.update_back_btn, 0)
        self.update_page_content_layout.addLayout(self.header_content_layout, 0)

        self.main_content_layout = QtWidgets.QHBoxLayout()
        self.main_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.update_btn = BlocksCustomButton()
        self.update_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.update_btn.setMaximumSize(QtCore.QSize(250, 80))
        font.setPointSize(18)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.update_btn.sizePolicy().hasHeightForWidth())
        self.update_btn.setSizePolicy(sizePolicy)
        self.update_btn.setFont(font)
        self.update_btn.setMouseTracking(True)
        self.update_btn.setTabletTracking(True)
        self.update_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.update_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.update_btn.setAutoDefault(True)
        self.update_btn.setFlat(True)
        self.update_btn.setText("Update")
        self.main_content_layout.addWidget(self.update_btn, 0)

        self.infobox_frame = BlocksCustomFrame()
        self.infobox_frame.setMinimumSize(QtCore.QSize(400, 300))

        self.info_box_layout = QtWidgets.QVBoxLayout()
        font = QtGui.QFont()
        font.setFamily(font_family)
        font.setPointSize(20)
        self.version_box = QtWidgets.QHBoxLayout()
        self.version_title = QtWidgets.QLabel(self)
        self.version_title.setText("Version: ")
        self.version_title.setMinimumSize(QtCore.QSize(200, 60))
        self.version_title.setMaximumSize(QtCore.QSize(200, 60))
        palette = self.version_title.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.version_title.setFont(font)
        self.version_title.setPalette(palette)
        self.version_title.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.version_tracking_info = QtWidgets.QLabel(self)
        self.version_tracking_info.setMinimumSize(QtCore.QSize(200, 60))
        self.version_tracking_info.setMaximumSize(QtCore.QSize(16777215, 60))
        palette = self.version_tracking_info.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.version_tracking_info.setFont(font)
        self.version_tracking_info.setPalette(palette)
        self.version_tracking_info.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.version_tracking_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.version_tracking_info.setObjectName("version-tracking")
        self.version_tracking_info.setText(
            "v0.0.1-alpha"
        )  # TODO: This needs to be retrieved
        self.version_box.addWidget(self.version_title, 0)
        self.version_box.addWidget(self.version_tracking_info, 0)
        self.info_box_layout.addLayout(self.version_box, 1)

        self.infobox_frame.setLayout(self.info_box_layout)
        self.main_content_layout.addWidget(self.infobox_frame, 1)
        self.update_page_content_layout.addLayout(self.main_content_layout, 1)
        self.setLayout(self.update_page_content_layout)
