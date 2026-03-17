import typing

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.icon_button import IconButton


class AxisMaintenancePage(QtWidgets.QWidget):
    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    set_dialog_popup = QtCore.pyqtSignal(str, "PyQt_PyObject", name="set-dialog-popup")

    show_waiting_page = QtCore.pyqtSignal(int, str, int, bool, name="show-waiting-page")

    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(AxisMaintenancePage, self).__init__(parent)
        self._setup_ui()

        self.axes_back_btn.clicked.connect(self.request_back_button)
        self.axis_x_btn.clicked.connect(lambda: self.axis_maintenance("x"))
        self.axis_y_btn.clicked.connect(lambda: self.axis_maintenance("y"))
        self.axis_z_btn.clicked.connect(lambda: self.axis_maintenance("z"))

    def axis_maintenance(self, axis: str) -> None:
        """Routine, checks axis movement for printer debugging"""
        # self.current_process = Process.AXIS_MAINTENANCE
        self.current_object = axis
        self.run_gcode_signal.emit(f"G28 {axis.upper()}\nM400")
        self.set_dialog_popup.emit(
            f"Insert oil on the {axis.upper()} axis before confirming.",
            self.dialog_asnwer,
        )
        self.show_waiting_page.emit(-1, f"Homing {axis.upper()} axis...", 5000, True)

    def dialog_asnwer(self):
        print("." * 999)
        self.call_load_panel.emit(False, "")

    def _setup_ui(self) -> None:
        self.setObjectName("axes_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem12 = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem12)
        self.lcd_settings_header_layout = QtWidgets.QHBoxLayout()
        self.lcd_settings_header_layout.setObjectName("lcd_settings_header_layout")
        spacerItem13 = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.lcd_settings_header_layout.addItem(spacerItem13)
        self.lcd_settings_title_label = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lcd_settings_title_label.sizePolicy().hasHeightForWidth()
        )
        self.lcd_settings_title_label.setSizePolicy(sizePolicy)
        self.lcd_settings_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.lcd_settings_title_label.setFont(font)
        self.lcd_settings_title_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.lcd_settings_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lcd_settings_title_label.setObjectName("lcd_settings_title_label")
        self.lcd_settings_header_layout.addWidget(self.lcd_settings_title_label)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.axes_back_btn = IconButton(parent=self)
        self.axes_back_btn.setSizePolicy(sizePolicy)
        self.axes_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.axes_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.axes_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.axes_back_btn.setObjectName("axes_back_btn")
        self.lcd_settings_header_layout.addWidget(self.axes_back_btn)
        self.verticalLayout.addLayout(self.lcd_settings_header_layout)

        spacerItem14 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout.addItem(spacerItem14)
        self.lcd_settings_content_layout = QtWidgets.QGridLayout()
        self.lcd_settings_content_layout.setObjectName("lcd_settings_content_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        self.axis_x_btn = BlocksCustomButton(parent=self)
        self.axis_x_btn.setSizePolicy(sizePolicy)
        self.axis_x_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.axis_x_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.axis_x_btn.setFont(font)
        self.axis_x_btn.setObjectName("axis_x_btn")
        self.lcd_settings_content_layout.addWidget(
            self.axis_x_btn,
            0,
            0,
            1,
            4,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.axis_z_btn = BlocksCustomButton(parent=self)
        self.axis_z_btn.setSizePolicy(sizePolicy)
        self.axis_z_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.axis_z_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.axis_z_btn.setFont(font)
        self.axis_z_btn.setObjectName("axis_z_btn")
        self.horizontalLayout_2.addWidget(self.axis_z_btn)

        self.axis_y_btn = BlocksCustomButton(parent=self)
        self.axis_y_btn.setSizePolicy(sizePolicy)
        self.axis_y_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.axis_y_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.axis_y_btn.setFont(font)
        self.axis_y_btn.setObjectName("axis_y_btn")
        self.horizontalLayout_2.addWidget(self.axis_y_btn)
        self.lcd_settings_content_layout.addLayout(self.horizontalLayout_2, 1, 0, 1, 4)
        self.verticalLayout.addLayout(self.lcd_settings_content_layout)
        spacerItem15 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout.addItem(spacerItem15)

        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.lcd_settings_title_label.setText(
            _translate("utilitiesStackedWidget", "Axis Maintenance")
        )
        self.lcd_settings_title_label.setProperty(
            "class", _translate("utilitiesStackedWidget", "title_text")
        )
        self.axes_back_btn.setText(_translate("utilitiesStackedWidget", "Back"))
        self.axes_back_btn.setProperty(
            "class", _translate("utilitiesStackedWidget", "menu_btn")
        )
        self.axes_back_btn.setProperty(
            "button_type", _translate("utilitiesStackedWidget", "icon")
        )
        self.axis_x_btn.setText(_translate("utilitiesStackedWidget", "X"))
        self.axis_x_btn.setProperty(
            "class", _translate("utilitiesStackedWidget", "menu_btn")
        )
        self.axis_x_btn.setProperty(
            "button_type", _translate("utilitiesStackedWidget", "normal")
        )
        self.axis_z_btn.setText(_translate("utilitiesStackedWidget", "Z"))
        self.axis_z_btn.setProperty(
            "class", _translate("utilitiesStackedWidget", "menu_btn")
        )
        self.axis_y_btn.setText(_translate("utilitiesStackedWidget", "Y"))
        self.axis_y_btn.setProperty(
            "class", _translate("utilitiesStackedWidget", "menu_btn")
        )
