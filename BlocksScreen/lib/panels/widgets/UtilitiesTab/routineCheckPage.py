import typing
import re
from lib.utils.icon_button import IconButton
from helper_methods import normalize

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.blocks_button import BlocksCustomButton



class RoutineCheckPage(QtWidgets.QWidget):
    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(RoutineCheckPage, self).__init__(parent)

        self._setup_ui()
        self.routine_check_back_btn.clicked.connect(self.request_back_button)
 

    def _setup_ui(self) -> None:
        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))

        self.routines_page = QtWidgets.QWidget()
        self.routines_page.setObjectName("routines_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.routines_page)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.verticalLayout.addItem(spacerItem6)
        self.routines_header_layout = QtWidgets.QHBoxLayout()
        self.routines_header_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.routines_header_layout.setObjectName("routines_header_layout")
        spacerItem7 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.routines_header_layout.addItem(spacerItem7)
        self.routines_page_title = QtWidgets.QLabel(parent=self.routines_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.routines_page_title.sizePolicy().hasHeightForWidth())
        self.routines_page_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.routines_page_title.setFont(font)
        self.routines_page_title.setStyleSheet("background: transparent; color: white;")
        self.routines_page_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.routines_page_title.setObjectName("routines_page_title")
        self.routines_header_layout.addWidget(self.routines_page_title)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.routine_check_back_btn = IconButton(parent=self.routines_page)
        self.routine_check_back_btn.setSizePolicy(sizePolicy)
        self.routine_check_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.routine_check_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.routine_check_back_btn.setProperty("icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.routine_check_back_btn.setObjectName("routine_check_back_btn")
        self.routines_header_layout.addWidget(self.routine_check_back_btn)
        self.verticalLayout.addLayout(self.routines_header_layout)

        spacerItem8 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.verticalLayout.addItem(spacerItem8)
        self.routines_content_layout = QtWidgets.QGridLayout()
        self.routines_content_layout.setVerticalSpacing(20)
        self.routines_content_layout.setObjectName("routines_content_layout")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        self.rc_bheat = BlocksCustomButton(parent=self.routines_page)
        self.rc_bheat.setSizePolicy(sizePolicy)
        self.rc_bheat.setFont(font)
        self.rc_bheat.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_bheat.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_bheat.setProperty("icon_pixmap", QtGui.QPixmap(":/temperature_related/media/btn_icons/temperature_plate.svg"))
        self.rc_bheat.setObjectName("rc_bheat")
        self.routines_content_layout.addWidget(self.rc_bheat, 0, 1, 1, 1)

        self.rc_fans = BlocksCustomButton(parent=self.routines_page)
        self.rc_fans.setSizePolicy(sizePolicy)
        self.rc_fans.setFont(font)
        self.rc_fans.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_fans.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_fans.setProperty("icon_pixmap", QtGui.QPixmap(":/fan_related/media/btn_icons/fan_cage.svg"))
        self.rc_fans.setObjectName("rc_fans")
        self.routines_content_layout.addWidget(self.rc_fans, 0, 0, 1, 1)

        self.rc_axis = BlocksCustomButton(parent=self.routines_page)
        self.rc_axis.setSizePolicy(sizePolicy)
        self.rc_axis.setFont(font)
        self.rc_axis.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_axis.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_axis.setProperty("icon_pixmap", QtGui.QPixmap(":/motion/media/btn_icons/axis_maintenance.svg"))
        self.rc_axis.setObjectName("rc_axis")
        self.routines_content_layout.addWidget(self.rc_axis, 1, 1, 1, 1)

        self.rc_ext = BlocksCustomButton(parent=self.routines_page)
        self.rc_ext.setSizePolicy(sizePolicy)
        self.rc_ext.setFont(font)
        self.rc_ext.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_ext.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_ext.setProperty("icon_pixmap", QtGui.QPixmap(":/extruder_related/media/btn_icons/nozzle.svg"))
        self.rc_ext.setObjectName("rc_ext")
        self.routines_content_layout.addWidget(self.rc_ext, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.routines_content_layout)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem9)


        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.routines_page_title.setText(_translate("utilitiesStackedWidget", "Routine Check"))
        self.routines_page_title.setProperty("class", _translate("utilitiesStackedWidget", "title_text"))
        self.routine_check_back_btn.setText(_translate("utilitiesStackedWidget", "Back"))
        self.routine_check_back_btn.setProperty("class", _translate("utilitiesStackedWidget", "menu_btn"))
        self.routine_check_back_btn.setProperty("button_type", _translate("utilitiesStackedWidget", "icon"))
        self.rc_bheat.setText(_translate("utilitiesStackedWidget", "Bed Heater"))
        self.rc_bheat.setProperty("class", _translate("utilitiesStackedWidget", "menu_btn"))
        self.rc_fans.setText(_translate("utilitiesStackedWidget", "Fans"))
        self.rc_fans.setProperty("class", _translate("utilitiesStackedWidget", "menu_btn"))
        self.rc_axis.setText(_translate("utilitiesStackedWidget", "Axis"))
        self.rc_axis.setProperty("class", _translate("utilitiesStackedWidget", "menu_btn"))
        self.rc_ext.setText(_translate("utilitiesStackedWidget", "Extruder"))
        self.rc_ext.setProperty("class", _translate("utilitiesStackedWidget", "menu_btn"))


