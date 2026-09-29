import typing

from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class InfoPage(QtWidgets.QWidget):
    """Info page of the utilities tab."""

    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super().__init__(parent)

        self._setup_ui()
        self.info_back_btn.clicked.connect(self.request_back_button.emit)

    def _setup_ui(self) -> None:
        self.setObjectName("info_page")

        spacerItem = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        spacerItem1 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addItem(spacerItem)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.info_header_layout = QtWidgets.QHBoxLayout()
        self.info_header_layout.setObjectName("info_header_layout")
        self.info_header_layout.addItem(spacerItem1)

        self.info_title_label = QtWidgets.QLabel(parent=self)
        self.info_title_label.setSizePolicy(sizePolicy)
        self.info_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.info_title_label.setFont(font)
        self.info_title_label.setStyleSheet("background: transparent; color: white;")
        self.info_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_header_layout.addWidget(self.info_title_label)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )

        self.info_back_btn = IconButton(parent=self)
        self.info_back_btn.setSizePolicy(sizePolicy)
        self.info_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.info_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.info_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.info_header_layout.addWidget(self.info_back_btn)
        self.verticalLayout_2.addLayout(self.info_header_layout)

        self.info_content_layout = QtWidgets.QVBoxLayout()
        self.info_content_layout.setObjectName("info_content_layout")

        self.frame = BlocksCustomFrame(parent=self)
        self.frame.setMinimumSize(QtCore.QSize(350, 260))
        self.frame.setMaximumSize(QtCore.QSize(350, 290))

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        font = QtGui.QFont()
        font.setPointSize(20)

        self.kv_label = QtWidgets.QLabel(parent=self.frame)
        self.kv_label.setGeometry(QtCore.QRect(0, 10, 351, 81))
        self.kv_label.setSizePolicy(sizePolicy)
        self.kv_label.setFont(font)
        self.kv_label.setStyleSheet("color:white")
        self.kv_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.kv_label.setObjectName("kv_label")

        font = QtGui.QFont()
        font.setPointSize(20)

        self.smth_label = QtWidgets.QLabel(parent=self.frame)
        self.smth_label.setGeometry(QtCore.QRect(0, 110, 351, 81))
        self.smth_label.setSizePolicy(sizePolicy)
        self.smth_label.setFont(font)
        self.smth_label.setStyleSheet("color:white")
        self.smth_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_content_layout.addWidget(
            self.frame, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.verticalLayout_2.addLayout(self.info_content_layout)

        _translate = QtCore.QCoreApplication.translate

        self.info_title_label.setText(_translate("self", "Info"))
        self.info_title_label.setProperty("class", _translate("self", "title_text"))
        self.info_back_btn.setText(_translate("self", "Back"))
        self.info_back_btn.setProperty("class", _translate("self", "menu_btn"))
        self.info_back_btn.setProperty("button_type", _translate("self", "icon"))
        self.kv_label.setText(_translate("self", "Model: Blocks RF50"))
        self.smth_label.setText(_translate("self", "www.blockstec.com "))
