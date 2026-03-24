import typing

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.blocks_button import BlocksCustomButton


class RoutineCheckAnswerPage(QtWidgets.QWidget):

    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )

    on_rc_asnwer = QtCore.pyqtSignal(str,name="on-rc-asnwer")

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(RoutineCheckAnswerPage, self).__init__(parent)

        self._setup_ui()

        self.rc_yes.clicked.connect(self.on_routine_answer)
        self.rc_no.clicked.connect(self.on_routine_answer)

    def setTitle(self,title:str):
        self.rc_title.setText(title)

    def setMessage(self,message:str):
        self.rc_label.setText(message)

    def on_routine_answer(self):
        if self.sender() == self.rc_yes:
            self.on_rc_asnwer.emit("yes")
        else:
            self.on_rc_asnwer.emit("no")
        self.request_back_button.emit()

    def _setup_ui(self) -> None:
        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem10 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.verticalLayout.addItem(spacerItem10)
        self.rc_header_layout = QtWidgets.QHBoxLayout()
        self.rc_header_layout.setObjectName("rc_header_layout")
        
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
                
        self.rc_title = QtWidgets.QLabel(parent=self)
        self.rc_title.setSizePolicy(sizePolicy)
        self.rc_title.setMinimumSize(QtCore.QSize(0, 60))
        self.rc_title.setFont(font)
        self.rc_title.setStyleSheet("background: transparent; color: white;")
        self.rc_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rc_title.setObjectName("rc_title")

        self.rc_header_layout.addWidget(self.rc_title)
        self.verticalLayout.addLayout(self.rc_header_layout)
        self.rc_content_layout = QtWidgets.QGridLayout()
        self.rc_content_layout.setVerticalSpacing(0)
        self.rc_content_layout.setObjectName("rc_content_layout")



        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)   
        font = QtGui.QFont()
        font.setPointSize(15)
        
        self.rc_label = QtWidgets.QLabel(parent=self)

        self.rc_label.setSizePolicy(sizePolicy)
        self.rc_label.setFont(font)
        self.rc_label.setStyleSheet("color:white")
        self.rc_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rc_label.setObjectName("rc_label")
 
        self.rc_content_layout.addWidget(self.rc_label, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
     
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)


        self.rc_yes = BlocksCustomButton(parent=self)
        self.rc_yes.setSizePolicy(sizePolicy)
        self.rc_yes.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_yes.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_yes.setFont(font)
        self.rc_yes.setProperty("icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg"))
        self.rc_yes.setObjectName("rc_yes")
        self.horizontalLayout_3.addWidget(self.rc_yes)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem11)
        
        self.rc_no = BlocksCustomButton(parent=self)
        self.rc_no.setSizePolicy(sizePolicy)
        self.rc_no.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_no.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_no.setFont(font)
        self.rc_no.setProperty("icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg"))
        self.rc_no.setObjectName("rc_no")
        self.horizontalLayout_3.addWidget(self.rc_no)
        self.rc_content_layout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.rc_content_layout)
 

        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.rc_title.setText(_translate("utilitiesStackedWidget", "label"))
        self.rc_title.setProperty("class", _translate("utilitiesStackedWidget", "title_text"))
        self.rc_label.setText(_translate("utilitiesStackedWidget", "TextLabel"))
        self.rc_yes.setText(_translate("utilitiesStackedWidget", "Yes"))
        self.rc_yes.setProperty("class", _translate("utilitiesStackedWidget", "menu_btn"))
        self.rc_no.setText(_translate("utilitiesStackedWidget", "No"))
        self.rc_no.setProperty("class", _translate("utilitiesStackedWidget", "menu_btn"))