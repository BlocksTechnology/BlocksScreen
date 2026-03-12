import typing

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.check_button import BlocksCustomCheckButton
from lib.utils.icon_button import IconButton


class AxisPage(QtWidgets.QWidget):
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )

    request_slider_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, int, "PyQt_PyObject", int, int, name="request_slider_page"
    )

    request_back = QtCore.pyqtSignal(name="request_back")

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.setObjectName("probe_offset_page")
        self._setupUi()

        self.update()

        self.move_length: float = 1.0
        self.move_speed: float = 25.0

        self.mva_back_btn.clicked.connect(self.request_back.emit)
        self.mva_home_x_btn.clicked.connect(
            lambda: self.run_gcode_signal.emit("G28 X\nM400")
        )
        self.mva_home_y_btn.clicked.connect(
            lambda: self.run_gcode_signal.emit("G28 Y\nM400")
        )
        self.mva_home_z_btn.clicked.connect(
            lambda: self.run_gcode_signal.emit("G28 Z\nM400")
        )
        self.mva_home_all_btn.clicked.connect(
            lambda: self.run_gcode_signal.emit("G28\nM400")
        )

        self.mva_up_btn.clicked.connect(lambda: self.handle_move_axis("Y"))
        self.mva_down_btn.clicked.connect(lambda: self.handle_move_axis("Y-"))
        self.mva_right_btn.clicked.connect(lambda: self.handle_move_axis("X"))
        self.mva_left_btn.clicked.connect(lambda: self.handle_move_axis("X-"))
        self.mva_z_up.clicked.connect(
            lambda: self.handle_move_axis("Z-")  # Move nozzle closer to bed
        )
        self.mva_z_down.clicked.connect(
            lambda: self.handle_move_axis("Z")  # Move nozzle away from bed
        )

        self.mva_select_length_1_btn.toggled.connect(
            lambda checked: self.handle_select_move_length(checked, value=1.0)
        )
        self.mva_select_length_10_btn.toggled.connect(
            lambda checked: self.handle_select_move_length(checked, value=10.0)
        )
        self.mva_select_length_100_btn.toggled.connect(
            lambda checked: self.handle_select_move_length(checked, value=100.0)
        )
        self.mva_select_speed_25_btn.toggled.connect(
            lambda checked: self.handle_select_move_speed(checked, value=25.0)
        )
        self.mva_select_speed_50_btn.toggled.connect(
            lambda checked: self.handle_select_move_speed(checked, value=50.0)
        )
        self.mva_select_speed_100_btn.toggled.connect(
            lambda checked: self.handle_select_move_speed(checked, value=100.0)
        )

    @QtCore.pyqtSlot(bool, float, name="handle-select-move-speed")
    def handle_select_move_speed(self, checked: bool, value: float) -> None:
        """Slot that changes the move speed of manual move commands, mainly used
        for toggle buttons

        Args:
            checked (bool): Button checked state
            value (float): New move speed value
        """
        if self.move_speed == value:
            return
        self.move_speed = value

    @QtCore.pyqtSlot(bool, float, name="handle-select-move-length")
    def handle_select_move_length(self, checked: bool, value: float) -> None:
        """Slot that changes the move length of manual move commands,
        mainly used for toggle buttons


        Args:
            checked (bool): Button checked state
            value (float): New length value
        """
        if self.move_length == value:
            return
        self.move_length = value

    @QtCore.pyqtSlot(str, name="handle-move-axis")
    def handle_move_axis(self, axis: str) -> None:
        """Slot that requests manual move command

        Args:
            axis (str): String that contains one of the following axis `
                ['X',
                'X-'
                ,'Y'
                ,'Y-'
                ,'Z'
                ,'Z-']`. [^1]

        ---

        [^1]: The **-** symbol indicates the negative direction for that axis

        """
        if axis not in ["X", "X-", "Y", "Y-", "Z", "Z-"]:
            return
        self.run_gcode_signal.emit(
            f"G91\nG0 {axis}{float(self.move_length)} F{float(self.move_speed * 60)}\nG90\nM400"
        )

    def _setupUi(self) -> None:
        widget = QtWidgets.QWidget(parent=self)
        widget.setMinimumSize(QtCore.QSize(710, 410))
        widget.setMaximumSize(QtCore.QSize(710, 410))
        self.setObjectName("move_axis_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mva_header_layout = QtWidgets.QHBoxLayout()
        self.mva_header_layout.setObjectName("mva_header_layout")
        spacerItem2 = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.mva_header_layout.addItem(spacerItem2)
        self.mva_title_label = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mva_title_label.sizePolicy().hasHeightForWidth()
        )
        self.mva_title_label.setSizePolicy(sizePolicy)
        self.mva_title_label.setMinimumSize(QtCore.QSize(0, 0))
        self.mva_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.mva_title_label.setFont(font)
        self.mva_title_label.setStyleSheet("background: transparent; color: white;")
        self.mva_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mva_title_label.setObjectName("mva_title_label")
        self.mva_header_layout.addWidget(self.mva_title_label)

        self.mva_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.mva_back_btn.setSizePolicy(sizePolicy)
        self.mva_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.mva_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.mva_back_btn.setObjectName("mva_back_btn")
        self.mva_header_layout.addWidget(
            self.mva_back_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.verticalLayout.addLayout(self.mva_header_layout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mva_home_axis_layout = QtWidgets.QVBoxLayout()
        self.mva_home_axis_layout.setContentsMargins(5, 5, 5, 5)
        self.mva_home_axis_layout.setObjectName("mva_home_axis_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)

        self.mva_home_x_btn = IconButton(parent=self)
        self.mva_home_x_btn.setSizePolicy(sizePolicy)
        self.mva_home_x_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_home_x_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_home_x_btn.setObjectName("mva_home_x_btn")
        self.mva_home_x_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/motion/media/btn_icons/home_x.svg")
        )
        self.mva_home_axis_layout.addWidget(
            self.mva_home_x_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.mva_home_y_btn = IconButton(parent=self)
        self.mva_home_y_btn.setSizePolicy(sizePolicy)
        self.mva_home_y_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_home_y_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_home_y_btn.setObjectName("mva_home_y_btn")
        self.mva_home_y_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/motion/media/btn_icons/home_y.svg")
        )
        self.mva_home_axis_layout.addWidget(
            self.mva_home_y_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.mva_home_z_btn = IconButton(parent=self)
        self.mva_home_z_btn.setSizePolicy(sizePolicy)
        self.mva_home_z_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_home_z_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_home_z_btn.setObjectName("mva_home_z_btn")
        self.mva_home_z_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/motion/media/btn_icons/home_z.svg")
        )
        self.mva_home_axis_layout.addWidget(
            self.mva_home_z_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.mva_home_all_btn = IconButton(parent=self)
        self.mva_home_all_btn.setSizePolicy(sizePolicy)
        self.mva_home_all_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_home_all_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_home_all_btn.setObjectName("mva_home_all_btn")
        self.mva_home_all_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/motion/media/btn_icons/home_all.svg")
        )
        self.mva_home_axis_layout.addWidget(
            self.mva_home_all_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.horizontalLayout_2.addLayout(self.mva_home_axis_layout)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_2 = QtWidgets.QLabel(parent=self)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:white")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.mva_select_length_1_btn = BlocksCustomCheckButton(parent=self)
        self.mva_select_length_1_btn.setMinimumSize(QtCore.QSize(90, 90))
        self.mva_select_length_1_btn.setMaximumSize(QtCore.QSize(90, 90))
        self.mva_select_length_1_btn.setFont(font)
        self.mva_select_length_1_btn.setCheckable(True)
        self.mva_select_length_1_btn.setChecked(True)
        self.mva_select_length_1_btn.setObjectName("mva_select_length_1_btn")
        self.horizontalLayout_3.addWidget(self.mva_select_length_1_btn)

        self.mva_select_length_10_btn = BlocksCustomCheckButton(parent=self)
        self.mva_select_length_10_btn.setMinimumSize(QtCore.QSize(90, 90))
        self.mva_select_length_10_btn.setMaximumSize(QtCore.QSize(90, 90))
        self.mva_select_length_10_btn.setFont(font)
        self.mva_select_length_10_btn.setCheckable(True)
        self.mva_select_length_10_btn.setObjectName("mva_select_length_10_btn")
        self.horizontalLayout_3.addWidget(self.mva_select_length_10_btn)

        self.mva_select_length_100_btn = BlocksCustomCheckButton(parent=self)
        self.mva_select_length_100_btn.setMinimumSize(QtCore.QSize(90, 90))
        self.mva_select_length_100_btn.setMaximumSize(QtCore.QSize(90, 90))
        self.mva_select_length_100_btn.setFont(font)
        self.mva_select_length_100_btn.setCheckable(True)
        self.mva_select_length_100_btn.setObjectName("mva_select_length_100_btn")
        self.horizontalLayout_3.addWidget(self.mva_select_length_100_btn)

        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.label = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))

        self.label.setFont(font)
        self.label.setStyleSheet("color:white")
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.mva_select_speed_25_btn = BlocksCustomCheckButton(parent=self)
        self.mva_select_speed_25_btn.setMinimumSize(QtCore.QSize(90, 90))
        self.mva_select_speed_25_btn.setMaximumSize(QtCore.QSize(90, 90))
        self.mva_select_speed_25_btn.setFont(font)
        self.mva_select_speed_25_btn.setCheckable(True)
        self.mva_select_speed_25_btn.setChecked(True)
        self.mva_select_speed_25_btn.setObjectName("mva_select_speed_25_btn")
        self.horizontalLayout_4.addWidget(self.mva_select_speed_25_btn)

        self.mva_select_speed_50_btn = BlocksCustomCheckButton(parent=self)
        self.mva_select_speed_50_btn.setMinimumSize(QtCore.QSize(90, 90))
        self.mva_select_speed_50_btn.setMaximumSize(QtCore.QSize(90, 90))
        self.mva_select_speed_50_btn.setFont(font)
        self.mva_select_speed_50_btn.setCheckable(True)
        self.mva_select_speed_50_btn.setObjectName("mva_select_speed_50_btn")
        self.horizontalLayout_4.addWidget(self.mva_select_speed_50_btn)

        self.mva_select_speed_100_btn = BlocksCustomCheckButton(parent=self)
        self.mva_select_speed_100_btn.setMinimumSize(QtCore.QSize(90, 90))
        self.mva_select_speed_100_btn.setMaximumSize(QtCore.QSize(90, 90))
        self.mva_select_speed_100_btn.setFont(font)
        self.mva_select_speed_100_btn.setCheckable(True)
        self.mva_select_speed_100_btn.setObjectName("mva_select_speed_100_btn")
        self.horizontalLayout_4.addWidget(self.mva_select_speed_100_btn)

        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(0, 5, 0, 5)
        self.gridLayout_2.setObjectName("gridLayout_2")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)

        self.mva_left_btn = IconButton(parent=self)
        self.mva_left_btn.setSizePolicy(sizePolicy)
        self.mva_left_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_left_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_left_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/arrow_icons/media/btn_icons/left_arrow.svg")
        )
        self.mva_left_btn.setObjectName("mva_left_btn")
        self.gridLayout_2.addWidget(
            self.mva_left_btn, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight
        )

        self.mva_right_btn = IconButton(parent=self)
        self.mva_right_btn.setSizePolicy(sizePolicy)
        self.mva_right_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_right_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_right_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg"),
        )
        self.mva_right_btn.setObjectName("mva_right_btn")
        self.gridLayout_2.addWidget(
            self.mva_right_btn, 1, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft
        )

        self.mva_down_btn = IconButton(parent=self)
        self.mva_down_btn.setSizePolicy(sizePolicy)
        self.mva_down_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_down_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_down_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/arrow_icons/media/btn_icons/down_arrow.svg")
        )
        self.mva_down_btn.setObjectName("mva_down_btn")
        self.gridLayout_2.addWidget(
            self.mva_down_btn, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignTop
        )

        self.mva_up_btn = IconButton(parent=self)
        self.mva_up_btn.setSizePolicy(sizePolicy)
        self.mva_up_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_up_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_up_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/arrow_icons/media/btn_icons/up_arrow.svg")
        )
        self.mva_up_btn.setObjectName("mva_up_btn")
        self.gridLayout_2.addWidget(
            self.mva_up_btn, 0, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignBottom
        )

        self.mva_middle = IconButton(parent=self)
        self.mva_middle.setSizePolicy(sizePolicy)
        self.mva_middle.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_middle.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_middle.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/center_arrows.svg")
        )
        self.mva_middle.setObjectName("mva_middle")

        self.gridLayout_2.addWidget(self.mva_middle, 1, 1, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout_2)

        self.mva_z_layout = QtWidgets.QVBoxLayout()
        self.mva_z_layout.setObjectName("mva_z_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)

        self.mva_z_up = IconButton(parent=self)
        self.mva_z_up.setSizePolicy(sizePolicy)
        self.mva_z_up.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_z_up.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_z_up.setIconSize(QtCore.QSize(16, 16))
        self.mva_z_up.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/arrow_icons/media/btn_icons/up_arrow.svg")
        )
        self.mva_z_up.setObjectName("mva_z_up")
        self.mva_z_layout.addWidget(
            self.mva_z_up, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.mva_z_down = IconButton(parent=self)
        self.mva_z_down.setSizePolicy(sizePolicy)
        self.mva_z_down.setMinimumSize(QtCore.QSize(60, 60))
        self.mva_z_down.setMaximumSize(QtCore.QSize(60, 60))
        self.mva_z_down.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/arrow_icons/media/btn_icons/down_arrow.svg")
        )
        self.mva_z_down.setObjectName("mva_z_down")
        self.mva_z_layout.addWidget(
            self.mva_z_down, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.horizontalLayout_5.addLayout(self.mva_z_layout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.mva_x_label = QtWidgets.QLabel(parent=self)
        self.mva_x_label.setEnabled(True)

        self.mva_x_label.setFont(font)
        self.mva_x_label.setStyleSheet("background: transparent; color: white;")
        self.mva_x_label.setObjectName("mva_x_label")
        self.horizontalLayout_6.addWidget(
            self.mva_x_label, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.mva_x_value_label = QtWidgets.QLabel(parent=self)
        self.mva_x_value_label.setEnabled(True)

        self.mva_x_value_label.setFont(font)
        self.mva_x_value_label.setStyleSheet("background: transparent; color: white;")
        self.mva_x_value_label.setObjectName("mva_x_value_label")
        self.horizontalLayout_6.addWidget(self.mva_x_value_label)
        self.mva_y_label = QtWidgets.QLabel(parent=self)
        self.mva_y_label.setEnabled(True)

        self.mva_y_label.setFont(font)
        self.mva_y_label.setStyleSheet("background: transparent; color: white;")
        self.mva_y_label.setObjectName("mva_y_label")
        self.horizontalLayout_6.addWidget(
            self.mva_y_label, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.mva_y_value_label = QtWidgets.QLabel(parent=self)
        self.mva_y_value_label.setEnabled(True)

        self.mva_y_value_label.setFont(font)
        self.mva_y_value_label.setStyleSheet("background: transparent; color: white;")
        self.mva_y_value_label.setObjectName("mva_y_value_label")
        self.horizontalLayout_6.addWidget(self.mva_y_value_label)
        self.mva_z_label = QtWidgets.QLabel(parent=self)
        self.mva_z_label.setEnabled(True)

        self.mva_z_label.setFont(font)
        self.mva_z_label.setStyleSheet("background: transparent; color: white;")
        self.mva_z_label.setObjectName("mva_z_label")
        self.horizontalLayout_6.addWidget(
            self.mva_z_label, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.mva_z_value_label = QtWidgets.QLabel(parent=self)
        self.mva_z_value_label.setEnabled(True)

        self.mva_z_value_label.setFont(font)
        self.mva_z_value_label.setStyleSheet("background: transparent; color: white;")
        self.mva_z_value_label.setObjectName("mva_z_value_label")
        self.horizontalLayout_6.addWidget(self.mva_z_value_label)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.mva_x_label.setText(_translate("controlStackedWidget", "X:"))
        self.mva_y_label.setText(_translate("controlStackedWidget", "Y:"))
        self.mva_z_label.setText(_translate("controlStackedWidget", "Z:"))
        self.mva_z_value_label.setText(_translate("controlStackedWidget", "0"))
        self.mva_y_value_label.setText(_translate("controlStackedWidget", "0"))
        self.mva_x_value_label.setText(_translate("controlStackedWidget", "0"))
        self.mva_title_label.setText(_translate("controlStackedWidget", "Move Axis"))
        self.mva_title_label.setProperty(
            "class", _translate("controlStackedWidget", "title_text")
        )
        self.mva_back_btn.setText(_translate("controlStackedWidget", "Back"))
        self.mva_back_btn.setProperty(
            "class", _translate("controlStackedWidget", "menu_btn")
        )
        self.mva_back_btn.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_z_up.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_z_down.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_home_x_btn.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_home_y_btn.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_home_z_btn.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_home_all_btn.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_select_speed_25_btn.setText(_translate("controlStackedWidget", "25"))
        self.mva_select_speed_50_btn.setText(_translate("controlStackedWidget", "50"))
        self.mva_select_speed_100_btn.setText(_translate("controlStackedWidget", "100"))
        self.label.setText(_translate("controlStackedWidget", "Move Speed mm/s"))
        self.mva_select_length_1_btn.setText(_translate("controlStackedWidget", "1"))
        self.mva_select_length_10_btn.setText(_translate("controlStackedWidget", "10"))
        self.mva_select_length_100_btn.setText(
            _translate("controlStackedWidget", "100")
        )
        self.label_2.setText(_translate("controlStackedWidget", "Move Length mm"))
        self.mva_left_btn.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_right_btn.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_down_btn.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_up_btn.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
        self.mva_middle.setProperty(
            "button_type", _translate("controlStackedWidget", "icon")
        )
