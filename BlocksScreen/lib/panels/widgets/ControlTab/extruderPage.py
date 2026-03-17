import typing

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.check_button import BlocksCustomCheckButton
from lib.utils.icon_button import IconButton
from lib.utils.blocks_label import BlocksLabel
from lib.utils.blocks_button import BlocksCustomButton
from lib.printer import Printer


class ExtruderPage(QtWidgets.QWidget):
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )

    request_back = QtCore.pyqtSignal(name="request-back-button")

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        printer: Printer,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("probe_offset_page")
        self._setupUi()

        self.update()

        self.printer: Printer = printer
        self.timers = []

        self.exp_extrude_btn.clicked.connect(
            lambda: self.handle_extrusion(True)
        )  # True for extrusion
        self.exp_unextrude_btn.clicked.connect(
            lambda: self.handle_extrusion(False)
        )  # False for retraction

        self.exp_back_btn.clicked.connect(self.request_back.emit)
        self.extrude_select_length_10_btn.toggled.connect(
            lambda: self.handle_toggle_extrude_length(
                caller=self.extrude_select_length_10_btn, value=10
            )
        )
        self.extrude_select_length_50_btn.toggled.connect(
            lambda: self.handle_toggle_extrude_length(
                caller=self.extrude_select_length_50_btn, value=50
            )
        )
        self.extrude_select_length_100_btn.toggled.connect(
            lambda: self.handle_toggle_extrude_length(
                caller=self.extrude_select_length_100_btn, value=100
            )
        )
        self.extrude_select_feedrate_2_btn.toggled.connect(
            lambda: self.handle_toggle_extrude_feedrate(
                caller=self.extrude_select_feedrate_2_btn, value=2
            )
        )
        self.extrude_select_feedrate_5_btn.toggled.connect(
            lambda: self.handle_toggle_extrude_feedrate(
                caller=self.extrude_select_feedrate_5_btn, value=5
            )
        )
        self.extrude_select_feedrate_10_btn.toggled.connect(
            lambda: self.handle_toggle_extrude_feedrate(
                caller=self.extrude_select_feedrate_10_btn, value=10
            )
        )

    @QtCore.pyqtSlot(str, name="handle-extrusion")
    def handle_extrusion(self, extrude: bool) -> None:
        """Slot that requests an extrusion/unextrusion move

        Args:
            extrude (bool): If True extrudes otherwise unextrudes.
        """
        can_extrude = bool(self.printer.heaters_object["extruder"]["can_extrude"])
        if not can_extrude:
            self.extrude_page_message = "Temperature too cold to extrude"
            self.exp_info_label.setText(self.extrude_page_message)
            return
        if extrude:
            self.run_gcode_signal.emit(
                f"M83\nG1 E{self.extrude_length} F{self.extrude_feedrate * 60}\nM82\nM400"
            )
            self.extrude_page_message = "Extruding"
            self.exp_info_label.setText(self.extrude_page_message)
        else:
            self.run_gcode_signal.emit(
                f"M83\nG1 E-{self.extrude_length} F{self.extrude_feedrate * 60}\nM82\nM400"
            )
            self.extrude_page_message = "Retracting"
            self.exp_info_label.setText(self.extrude_page_message)
        # This block of code schedules a method to be called in x amount of milliseconds
        _sch_time_s = float(
            self.extrude_length / self.extrude_feedrate
        )  # calculate the amount of time it'll take for the operation
        self.extrude_page_message = "Ready"
        self.register_timed_callback(
            int(_sch_time_s + 2.0) * 1000,  # In milliseconds
            lambda: self.exp_info_label.setText(self.extrude_page_message),
        )

    def register_timed_callback(self, time: int, callback: callable) -> None:
        """Registers timed callback and starts the timeout"""
        _timer = QtCore.QTimer()
        _timer.setSingleShot(True)
        _timer.timeout.connect(callback)
        _timer.start(int(time))
        self.timers.append(_timer)

    @QtCore.pyqtSlot(bool, "PyQt_PyObject", int, name="select-extrude-feedrate")
    def handle_toggle_extrude_feedrate(self, checked: bool, caller, value: int) -> None:
        """Slot to change the extruder feedrate, mainly used for toggle buttons

        Args:
            checked (bool): Button checked state
            caller (PyQtObject): The button that called this slot
            value (int): New value for the extruder feedrate
        """
        if value == self.extrude_feedrate:
            return
        self.extrude_feedrate = value

    @QtCore.pyqtSlot(bool, "PyQt_PyObject", int, name="select-extrude-length")
    def handle_toggle_extrude_length(self, checked: bool, caller, value: int) -> None:
        """Slot that changes the extrude length, mainly used for toggle buttons

        Args:
            checked (bool): Button checked state
            caller (PyQtObject): The button that called this slot
            value (int): New value for the extrude length
        """
        if self.extrude_length == value:
            return
        self.extrude_length = value

    def _setupUi(self) -> None:
        widget = QtWidgets.QWidget(parent=self)
        widget.setMinimumSize(QtCore.QSize(710, 410))
        widget.setMaximumSize(QtCore.QSize(710, 410))
        self.setObjectName("fans_page")
        self.extrude_page = QtWidgets.QWidget()
        self.extrude_page.setMinimumSize(QtCore.QSize(710, 400))
        self.extrude_page.setMaximumSize(QtCore.QSize(720, 420))
        self.extrude_page.setObjectName("extrude_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.extrude_page)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem)
        self.exp_header_layout = QtWidgets.QHBoxLayout()
        self.exp_header_layout.setObjectName("exp_header_layout")
        spacerItem1 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.exp_header_layout.addItem(spacerItem1)
        self.exp_title_label = QtWidgets.QLabel(parent=self.extrude_page)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.exp_title_label.sizePolicy().hasHeightForWidth()
        )
        self.exp_title_label.setSizePolicy(sizePolicy)
        self.exp_title_label.setMinimumSize(QtCore.QSize(0, 60))
        self.exp_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.exp_title_label.setFont(font)
        self.exp_title_label.setStyleSheet("background: transparent; color: white;")
        self.exp_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.exp_title_label.setObjectName("exp_title_label")
        self.exp_header_layout.addWidget(self.exp_title_label)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(20)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.exp_back_btn = IconButton(parent=self.extrude_page)

        self.exp_back_btn.setSizePolicy(sizePolicy)
        self.exp_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.exp_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.exp_back_btn.setFont(font)
        self.exp_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.exp_back_btn.setObjectName("exp_back_btn")

        self.exp_header_layout.addWidget(
            self.exp_back_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.verticalLayout.addLayout(self.exp_header_layout)
        self.exp_vertical_content_layout = QtWidgets.QVBoxLayout()
        self.exp_vertical_content_layout.setContentsMargins(5, 5, 5, 5)
        self.exp_vertical_content_layout.setObjectName("exp_vertical_content_layout")

        font = QtGui.QFont()
        font.setPointSize(14)

        self.exp_length_group_box = QtWidgets.QGroupBox(parent=self.extrude_page)
        self.exp_length_group_box.setMinimumSize(QtCore.QSize(0, 80))
        self.exp_length_group_box.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.exp_length_group_box.setFont(font)
        self.exp_length_group_box.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.exp_length_group_box.setFlat(True)
        self.exp_length_group_box.setObjectName("exp_length_group_box")

        self.layoutWidget = QtWidgets.QWidget(parent=self.exp_length_group_box)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 20, 681, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.exp_length_content_layout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.exp_length_content_layout.setContentsMargins(5, 5, 5, 5)
        self.exp_length_content_layout.setSpacing(5)
        self.exp_length_content_layout.setObjectName("exp_length_content_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(50)

        self.extrude_select_length_group = QtWidgets.QButtonGroup(self)
        self.extrude_select_length_group.setObjectName("extrude_select_length_group")

        self.extrude_select_length_10_btn = BlocksCustomCheckButton(
            parent=self.layoutWidget
        )
        self.extrude_select_length_10_btn.setSizePolicy(sizePolicy)
        self.extrude_select_length_10_btn.setFont(font)
        self.extrude_select_length_10_btn.setCheckable(True)
        self.extrude_select_length_10_btn.setChecked(True)
        self.extrude_select_length_10_btn.setObjectName("extrude_select_length_10_btn")

        self.extrude_select_length_group.addButton(self.extrude_select_length_10_btn)
        self.exp_length_content_layout.addWidget(self.extrude_select_length_10_btn)

        self.extrude_select_length_50_btn = BlocksCustomCheckButton(
            parent=self.layoutWidget
        )
        self.extrude_select_length_50_btn.setSizePolicy(sizePolicy)
        self.extrude_select_length_50_btn.setFont(font)
        self.extrude_select_length_50_btn.setCheckable(True)
        self.extrude_select_length_50_btn.setObjectName("extrude_select_length_50_btn")

        self.extrude_select_length_group.addButton(self.extrude_select_length_50_btn)
        self.exp_length_content_layout.addWidget(self.extrude_select_length_50_btn)

        self.extrude_select_length_100_btn = BlocksCustomCheckButton(
            parent=self.layoutWidget
        )
        self.extrude_select_length_100_btn.setSizePolicy(sizePolicy)
        self.extrude_select_length_100_btn.setFont(font)
        self.extrude_select_length_100_btn.setCheckable(True)
        self.extrude_select_length_100_btn.setObjectName(
            "extrude_select_length_100_btn"
        )

        self.extrude_select_length_group.addButton(self.extrude_select_length_100_btn)
        self.exp_length_content_layout.addWidget(self.extrude_select_length_100_btn)
        self.exp_vertical_content_layout.addWidget(self.exp_length_group_box)

        font = QtGui.QFont()
        font.setPointSize(14)

        self.exp_feedrate_group_box = QtWidgets.QGroupBox(parent=self.extrude_page)
        self.exp_feedrate_group_box.setMinimumSize(QtCore.QSize(0, 80))
        self.exp_feedrate_group_box.setFont(font)
        self.exp_feedrate_group_box.setObjectName("exp_feedrate_group_box")

        self.layoutWidget1 = QtWidgets.QWidget(parent=self.exp_feedrate_group_box)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 19, 681, 61))
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.exp_feedrate_content_layout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.exp_feedrate_content_layout.setContentsMargins(5, 5, 5, 5)
        self.exp_feedrate_content_layout.setSpacing(5)
        self.exp_feedrate_content_layout.setObjectName("exp_feedrate_content_layout")

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)

        self.extrude_select_feedrate_group = QtWidgets.QButtonGroup(self)
        self.extrude_select_feedrate_group.setObjectName(
            "extrude_select_feedrate_group"
        )

        self.extrude_select_feedrate_2_btn = BlocksCustomCheckButton(
            parent=self.layoutWidget1
        )
        self.extrude_select_feedrate_2_btn.setSizePolicy(sizePolicy)
        self.extrude_select_feedrate_2_btn.setFont(font)
        self.extrude_select_feedrate_2_btn.setCheckable(True)
        self.extrude_select_feedrate_2_btn.setChecked(True)
        self.extrude_select_feedrate_2_btn.setObjectName(
            "extrude_select_feedrate_2_btn"
        )

        self.extrude_select_feedrate_group.addButton(self.extrude_select_feedrate_2_btn)
        self.exp_feedrate_content_layout.addWidget(self.extrude_select_feedrate_2_btn)

        self.extrude_select_feedrate_5_btn = BlocksCustomCheckButton(
            parent=self.layoutWidget1
        )
        self.extrude_select_feedrate_5_btn.setSizePolicy(sizePolicy)
        self.extrude_select_feedrate_5_btn.setFont(font)
        self.extrude_select_feedrate_5_btn.setCheckable(True)
        self.extrude_select_feedrate_5_btn.setObjectName(
            "extrude_select_feedrate_5_btn"
        )

        self.extrude_select_feedrate_group.addButton(self.extrude_select_feedrate_5_btn)
        self.exp_feedrate_content_layout.addWidget(self.extrude_select_feedrate_5_btn)

        self.extrude_select_feedrate_10_btn = BlocksCustomCheckButton(
            parent=self.layoutWidget1
        )
        self.extrude_select_feedrate_10_btn.setSizePolicy(sizePolicy)
        self.extrude_select_feedrate_10_btn.setFont(font)
        self.extrude_select_feedrate_10_btn.setCheckable(True)
        self.extrude_select_feedrate_10_btn.setObjectName(
            "extrude_select_feedrate_10_btn"
        )
        self.extrude_select_feedrate_group.addButton(
            self.extrude_select_feedrate_10_btn
        )
        self.exp_feedrate_content_layout.addWidget(self.extrude_select_feedrate_10_btn)
        self.exp_vertical_content_layout.addWidget(self.exp_feedrate_group_box)

        self.exp_movement_content_layout = QtWidgets.QVBoxLayout()
        self.exp_movement_content_layout.setContentsMargins(-1, 5, -1, -1)
        self.exp_movement_content_layout.setSpacing(0)
        self.exp_movement_content_layout.setObjectName("exp_movement_content_layout")

        self.exp_buttons_layout = QtWidgets.QHBoxLayout()
        self.exp_buttons_layout.setContentsMargins(5, 5, 5, 5)
        self.exp_buttons_layout.setObjectName("exp_buttons_layout")

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(20)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self.exp_unextrude_btn = BlocksCustomButton(parent=self.extrude_page)
        self.exp_unextrude_btn.setSizePolicy(sizePolicy)
        self.exp_unextrude_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.exp_unextrude_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.exp_unextrude_btn.setFont(font)
        self.exp_unextrude_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/extruder_related/media/btn_icons/extrude.svg"),
        )
        self.exp_unextrude_btn.setObjectName("exp_unextrude_btn")

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(16)

        self.exp_buttons_layout.addWidget(self.exp_unextrude_btn)
        self.exp_nozzle_icon_label = BlocksLabel(parent=self.extrude_page)
        self.exp_nozzle_icon_label.setMinimumSize(QtCore.QSize(60, 60))
        self.exp_nozzle_icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.exp_nozzle_icon_label.setFont(font)
        self.exp_nozzle_icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.exp_nozzle_icon_label.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/extruder_related/media/btn_icons/nozzle.svg"),
        )
        self.exp_nozzle_icon_label.setObjectName("exp_nozzle_icon_label")
        self.exp_buttons_layout.addWidget(self.exp_nozzle_icon_label)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(20)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        self.exp_extrude_btn = BlocksCustomButton(parent=self.extrude_page)
        self.exp_extrude_btn.setSizePolicy(sizePolicy)
        self.exp_extrude_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.exp_extrude_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.exp_extrude_btn.setFont(font)
        self.exp_extrude_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/extruder_related/media/btn_icons/extrude.svg"),
        )
        self.exp_extrude_btn.setObjectName("exp_extrude_btn")

        self.exp_buttons_layout.addWidget(self.exp_extrude_btn)
        self.exp_movement_content_layout.addLayout(self.exp_buttons_layout)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)

        self.exp_info_layout = QtWidgets.QHBoxLayout()
        self.exp_info_layout.setContentsMargins(5, 5, 5, 5)
        self.exp_info_layout.setObjectName("exp_info_layout")

        self.exp_info_label = QtWidgets.QLabel(parent=self.extrude_page)
        self.exp_info_label.setSizePolicy(sizePolicy)
        self.exp_info_label.setFont(font)
        self.exp_info_label.setStyleSheet("background: transparent; color: white;")
        self.exp_info_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.exp_info_label.setObjectName("exp_info_label")
        self.exp_info_layout.addWidget(self.exp_info_label)
        self.exp_movement_content_layout.addLayout(self.exp_info_layout)
        self.exp_movement_content_layout.setStretch(1, 1)
        self.exp_vertical_content_layout.addLayout(self.exp_movement_content_layout)
        self.exp_vertical_content_layout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.exp_vertical_content_layout)
        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.exp_title_label.setText(_translate("controlStackedWidget", "Extrude"))
        self.exp_back_btn.setText(_translate("controlStackedWidget", "Back"))
        self.exp_length_group_box.setTitle(
            _translate("controlStackedWidget", "Extrude Length (mm)")
        )
        self.extrude_select_length_10_btn.setText(
            _translate("controlStackedWidget", "10")
        )
        self.extrude_select_length_50_btn.setText(
            _translate("controlStackedWidget", "50")
        )
        self.extrude_select_length_100_btn.setText(
            _translate("controlStackedWidget", "100")
        )
        self.exp_feedrate_group_box.setTitle(
            _translate("controlStackedWidget", "Extrude Feedrate (mm/s)")
        )
        self.extrude_select_feedrate_2_btn.setText(
            _translate("controlStackedWidget", "2")
        )
        self.extrude_select_feedrate_5_btn.setText(
            _translate("controlStackedWidget", "5")
        )
        self.extrude_select_feedrate_10_btn.setText(
            _translate("controlStackedWidget", "10")
        )
        self.exp_unextrude_btn.setText(_translate("controlStackedWidget", "Retract"))
        self.exp_extrude_btn.setText(_translate("controlStackedWidget", "Extrude"))
        self.exp_info_label.setText(
            _translate("controlStackedWidget", "Nozzle heating to extrude")
        )
