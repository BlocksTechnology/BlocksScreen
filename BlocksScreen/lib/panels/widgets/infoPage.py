import typing

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton


class InfoPage(QtWidgets.QWidget):
    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(InfoPage, self).__init__(parent)

        self._setup_ui()

        self.info_back_btn.clicked.connect(self.request_back_button.emit)

    def _setup_ui(self) -> None:
        self.setObjectName("info_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem)

        self.info_header_layout = QtWidgets.QHBoxLayout()
        self.info_header_layout.setObjectName("info_header_layout")
        spacerItem1 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.info_header_layout.addItem(spacerItem1)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.info_title_label = QtWidgets.QLabel(parent=self)
        self.info_title_label.setSizePolicy(sizePolicy)
        self.info_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.info_title_label.setFont(font)
        self.info_title_label.setStyleSheet("background: transparent; color: white;")
        self.info_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_title_label.setObjectName("info_title_label")
        self.info_header_layout.addWidget(self.info_title_label)

        self.info_back_btn = IconButton(parent=self)
        self.info_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.info_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.info_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.info_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.info_back_btn.setObjectName("info_back_btn")
        self.info_header_layout.addWidget(self.info_back_btn)
        self.verticalLayout.addLayout(self.info_header_layout)

        self.info_content_layout = QtWidgets.QVBoxLayout()
        self.info_content_layout.setObjectName("info_content_layout")

        self.frame = BlocksCustomFrame(parent=self)
        self.frame.setMinimumSize(QtCore.QSize(350, 260))
        self.frame.setMaximumSize(QtCore.QSize(350, 290))
        self.frame.setObjectName("frame")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setPointSize(20)

        self.kv_label = QtWidgets.QLabel(parent=self.frame)
        self.kv_label.setGeometry(QtCore.QRect(0, 10, 351, 81))
        self.kv_label.setSizePolicy(sizePolicy)
        self.kv_label.setFont(font)
        self.kv_label.setStyleSheet("color:white")
        self.kv_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.kv_label.setObjectName("kv_label")

        self.smth_label = QtWidgets.QLabel(parent=self.frame)
        self.smth_label.setGeometry(QtCore.QRect(0, 110, 351, 81))
        self.smth_label.setSizePolicy(sizePolicy)
        self.smth_label.setFont(font)
        self.smth_label.setStyleSheet("color:white")
        self.smth_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.smth_label.setObjectName("smth_label")

        self.info_content_layout.addWidget(
            self.frame, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.verticalLayout.addLayout(self.info_content_layout)

        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.info_title_label.setText(_translate("utilitiesStackedWidget", "Info"))
        self.info_back_btn.setText(_translate("utilitiesStackedWidget", "Back"))
        self.kv_label.setText(
            _translate("utilitiesStackedWidget", "Model: Blocks RF50")
        )
        self.smth_label.setText(
            _translate("utilitiesStackedWidget", "www.blockstec.com ")
        )
