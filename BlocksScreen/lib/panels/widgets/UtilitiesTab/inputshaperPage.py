import typing
import re
from lib.panels.widgets.basePopup import BasePopup
from lib.utils.icon_button import IconButton
from helper_methods import normalize

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.panels.widgets.optionCardWidget import OptionCard


class InputShaperPage(QtWidgets.QWidget):
    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    request_is_results_page = QtCore.pyqtSignal(name="request-is-results-page")

    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")

    set_aut = QtCore.pyqtSignal(bool,name="set-aut")


    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(InputShaperPage, self).__init__(parent)

        self._setup_ui()
        self.input_shaper_back_btn.clicked.connect(self.request_back_button.emit)


        self.automatic_is = OptionCard(
            self,
            "Automatic\nInput Shaper",
            "Automatic Input Shaper",
            QtGui.QPixmap(":/input_shaper/media/btn_icons/input_shaper_auto.svg"),
        )  # type: ignore
        self.automatic_is.setObjectName("Automatic_IS_Card")
        self.is_content_layout.addWidget(
            self.automatic_is, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.automatic_is.continue_clicked.connect(
            lambda: self.handle_is("SHAPER_CALIBRATE")
        )

        self.manual_is = OptionCard(
             self,
            "Manual\nInput Shaper",
            "Manual Input Shaper",
            QtGui.QPixmap(":/input_shaper/media/btn_icons/input_shaper_manual.svg"),
        )  # type: ignore
        self.manual_is.setObjectName("Manual_IS_Card")
        self.is_content_layout.addWidget(
            self.manual_is, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.manual_is.continue_clicked.connect(lambda: self.handle_is(""))

        self.dialog_page = BasePopup(self, dialog=True, floating=True)


        self.dialog_page.accepted.connect(
            lambda: self.handle_is("SHAPER_CALIBRATE AXIS=Y")
        )
        self.dialog_page.rejected.connect(
            lambda: self.handle_is("SHAPER_CALIBRATE AXIS=X")
        )

    def handle_is(self, gcode: str) -> None:
            if gcode == "SHAPER_CALIBRATE":
                self.run_gcode_signal.emit("G28\nM400")
                self.set_aut.emit(True)
                self.run_gcode_signal.emit(gcode)
            elif gcode == "":
                self.dialog_page.confirm_background_color("#dfdfdf")
                self.dialog_page.cancel_background_color("#dfdfdf")
                self.dialog_page.cancel_font_color("#000000")
                self.dialog_page.confirm_font_color("#000000")
                self.dialog_page.cancel_button_text("X axis")
                self.dialog_page.confirm_button_text("Y axis")
                self.dialog_page.set_message(
                    "Select the axis you want to execute the input shaper on:"
                )
                self.dialog_page.show()
                return
            else:
                self.set_aut.emit(False)
                self.run_gcode_signal.emit("G28\nM400")
                self.run_gcode_signal.emit(gcode)
                self.request_is_results_page.emit()
            
            self.call_load_panel.emit(True, "Running Input Shaper...")



    def _setup_ui(self) -> None:
        self.setObjectName("input_shaper_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem16 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.verticalLayout.addItem(spacerItem16)
        self.is_header_layout = QtWidgets.QHBoxLayout()
        self.is_header_layout.setObjectName("is_header_layout")

        spacerItem17 = QtWidgets.QSpacerItem(60, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.is_header_layout.addItem(spacerItem17)
        
        self.label_2 = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background: transparent; color: white;")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.is_header_layout.addWidget(self.label_2)
  
        self.input_shaper_back_btn = IconButton(parent=self)
       
        self.input_shaper_back_btn.setSizePolicy(sizePolicy)
        self.input_shaper_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.input_shaper_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.input_shaper_back_btn.setProperty("icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.input_shaper_back_btn.setObjectName("input_shaper_back_btn")

        self.is_header_layout.addWidget(self.input_shaper_back_btn)
        self.verticalLayout.addLayout(self.is_header_layout)
        self.is_content_layout = QtWidgets.QHBoxLayout()
        self.is_content_layout.setObjectName("is_content_layout")
        self.verticalLayout.addLayout(self.is_content_layout)
        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("utilitiesStackedWidget", "Input Shaper"))
        self.input_shaper_back_btn.setText(_translate("utilitiesStackedWidget", "Back"))

