from functools import partial

from lib.utils.icon_button import IconButton
from lib.utils.numpad_button import NumpadButton
from PyQt6 import QtCore, QtGui, QtWidgets


class CustomNumpad(QtWidgets.QWidget):
    """A custom numpad for inserting integer values"""

    value_selected = QtCore.pyqtSignal(str, int, name="value_selected")
    request_back = QtCore.pyqtSignal(name="request_back")

    def __init__(
        self,
        parent,
    ) -> None:
        super().__init__(parent)
        self.setupUI()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.current_value: str = "0"
        self.name: str = ""
        self.min_value: int = 0
        self.max_value: int = 100
        self.numpad_0.clicked.connect(lambda: self.value_inserted("0"))
        self.numpad_1.clicked.connect(lambda: self.value_inserted("1"))
        self.numpad_2.clicked.connect(lambda: self.value_inserted("2"))
        self.numpad_3.clicked.connect(lambda: self.value_inserted("3"))
        self.numpad_4.clicked.connect(lambda: self.value_inserted("4"))
        self.numpad_5.clicked.connect(lambda: self.value_inserted("5"))
        self.numpad_6.clicked.connect(lambda: self.value_inserted("6"))
        self.numpad_7.clicked.connect(lambda: self.value_inserted("7"))
        self.numpad_8.clicked.connect(lambda: self.value_inserted("8"))
        self.numpad_9.clicked.connect(lambda: self.value_inserted("9"))
        self.numpad_enter.clicked.connect(lambda: self.value_inserted("enter"))
        self.numpad_enter.clicked.connect(self.value_selected.disconnect)
        self.numpad_clear.clicked.connect(lambda: self.value_inserted("clear"))
        self.numpad_back_btn.clicked.connect(self.back_button)

    def value_inserted(self, value: str) -> None:
        """Handle number insertion on the numpad

        Args:
            value (int | str): value
        """
        if value.isnumeric():
            self.current_value = str(self.current_value) + str(value)
            self.inserted_value.setText(str(self.current_value))

        if "enter" in value and str(self.current_value).isnumeric():
            self.value_selected[str, int].emit(
                self.name, int(self.current_value)
            )
            self.request_back.emit()

        elif "clear" in value:
            self.current_value = self.current_value[
                : len(self.current_value) - 1
            ]

            self.inserted_value.setText(str(self.current_value))

    def back_button(self):
        self.request_back.emit()

    def set_name(self, name: str) -> None:
        """Sets the header name for the page"""
        self.name = name
        self.numpad_title.setText(name)
        self.update()

    def set_value(self, value: int) -> None:
        self.current_value = str(value)
        self.inserted_value.setText(str(value))

    def set_min_value(self, min_value: int) -> None:
        self.min_value = min_value

    def set_max_value(self, max_value: int) -> None:
        self.max_value = max_value

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        """paintEvent
            Repaints the widget with custom controls

        Args:
            a0 (QtGui.QPaintEvent | None): The event for repainting

        """
        # if self.current_object is not None:
        # self.value_name.setText(self.current_object)
        # self.numpad_title.setText(self.current_object)

        # if self.isVisible():
        #     if (
        #         self.current_object is not None
        #         and "fan" in self.current_object
        #     ):
        #         pass

    def setupUI(self) -> None:
        self.setObjectName("customNumpad")
        self.setEnabled(True)
        self.resize(710, 410)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.layoutWidget = QtWidgets.QWidget(parent=self)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 9, 691, 62))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMaximumSize
        )
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.numpad_title = QtWidgets.QLabel(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.numpad_title.setFont(font)
        self.numpad_title.setAutoFillBackground(False)
        palette = QtGui.QPalette()
        palette.setColor(palette.ColorRole.Window, QtGui.QColor("#FFFFFF00"))
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.numpad_title.setPalette(palette)
        self.numpad_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.numpad_title.setObjectName("numpad_title")
        self.gridLayout.addWidget(self.numpad_title, 0, 0, 1, 1)
        self.numpad_back_btn = IconButton(parent=self.layoutWidget)
        self.numpad_back_btn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.numpad_back_btn.sizePolicy().hasHeightForWidth()
        )
        self.numpad_back_btn.setSizePolicy(sizePolicy)
        self.numpad_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.numpad_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.numpad_back_btn.setStyleSheet("")
        self.numpad_back_btn.setText("")
        self.numpad_back_btn.setIconSize(QtCore.QSize(16, 16))
        self.numpad_back_btn.setCheckable(False)
        self.numpad_back_btn.setChecked(False)
        self.numpad_back_btn.setFlat(True)
        self.numpad_back_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/ui/media/btn_icons/back.svg"),
        )
        self.numpad_back_btn.setObjectName("numpad_back_btn")
        self.gridLayout.addWidget(self.numpad_back_btn, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.layoutWidget1 = QtWidgets.QWidget(parent=self)
        self.layoutWidget1.setGeometry(QtCore.QRect(9, 72, 691, 61))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.inserted_value = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.inserted_value.setMinimumSize(QtCore.QSize(500, 0))
        self.inserted_value.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(20)
        self.inserted_value.setFont(font)
        self.inserted_value.setAutoFillBackground(False)
        self.inserted_value.setPalette(palette)
        self.inserted_value.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.inserted_value.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.inserted_value.setLineWidth(0)
        self.inserted_value.setScaledContents(False)
        self.inserted_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignBottom
            | QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.inserted_value.setIndent(0)
        self.inserted_value.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        self.inserted_value.setObjectName("inserted_value")
        self.verticalLayout_2.addWidget(
            self.inserted_value,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignBottom,
        )
        self.line = QtWidgets.QFrame(parent=self.layoutWidget1)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(120, 141, 464, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMaximumSize
        )
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.numpad_6 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_6.sizePolicy().hasHeightForWidth()
        )
        self.numpad_6.setSizePolicy(sizePolicy)
        self.numpad_6.setMinimumSize(QtCore.QSize(150, 63))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_6.setFont(font)
        self.numpad_6.setTabletTracking(False)
        self.numpad_6.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_6.setFlat(True)
        self.numpad_6.setObjectName("numpad_6")
        self.gridLayout_2.addWidget(
            self.numpad_6, 1, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.numpad_9 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_9.sizePolicy().hasHeightForWidth()
        )
        self.numpad_9.setSizePolicy(sizePolicy)
        self.numpad_9.setMinimumSize(QtCore.QSize(150, 63))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_9.setFont(font)
        self.numpad_9.setTabletTracking(False)
        self.numpad_9.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.numpad_9.setFlat(True)
        self.numpad_9.setObjectName("numpad_9")
        self.gridLayout_2.addWidget(
            self.numpad_9, 0, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.numpad_8 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_8.sizePolicy().hasHeightForWidth()
        )
        self.numpad_8.setSizePolicy(sizePolicy)
        self.numpad_8.setMinimumSize(QtCore.QSize(150, 63))
        self.numpad_8.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_8.setFont(font)
        self.numpad_8.setTabletTracking(False)
        self.numpad_8.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_8.setFlat(True)
        self.numpad_8.setObjectName("numpad_8")
        self.gridLayout_2.addWidget(
            self.numpad_8, 0, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.numpad_2 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_2.sizePolicy().hasHeightForWidth()
        )
        self.numpad_2.setSizePolicy(sizePolicy)
        self.numpad_2.setMinimumSize(QtCore.QSize(150, 63))
        self.numpad_2.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_2.setFont(font)
        self.numpad_2.setTabletTracking(False)
        self.numpad_2.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_2.setFlat(True)
        self.numpad_2.setObjectName("numpad_2")
        self.gridLayout_2.addWidget(
            self.numpad_2, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.numpad_0 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_0.sizePolicy().hasHeightForWidth()
        )
        self.numpad_0.setSizePolicy(sizePolicy)
        self.numpad_0.setMinimumSize(QtCore.QSize(150, 63))
        self.numpad_0.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_0.setFont(font)
        self.numpad_0.setTabletTracking(False)
        self.numpad_0.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_0.setFlat(True)
        self.numpad_0.setObjectName("numpad_0")
        self.gridLayout_2.addWidget(
            self.numpad_0, 3, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.numpad_3 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_3.sizePolicy().hasHeightForWidth()
        )
        self.numpad_3.setSizePolicy(sizePolicy)
        self.numpad_3.setMinimumSize(QtCore.QSize(150, 63))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_3.setFont(font)
        self.numpad_3.setTabletTracking(False)
        self.numpad_3.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_3.setFlat(True)
        self.numpad_3.setObjectName("numpad_3")
        self.gridLayout_2.addWidget(
            self.numpad_3, 2, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.numpad_4 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_4.sizePolicy().hasHeightForWidth()
        )
        self.numpad_4.setSizePolicy(sizePolicy)
        self.numpad_4.setMinimumSize(QtCore.QSize(150, 63))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_4.setFont(font)
        self.numpad_4.setTabletTracking(False)
        self.numpad_4.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_4.setFlat(True)
        self.numpad_4.setObjectName("numpad_4")
        self.gridLayout_2.addWidget(
            self.numpad_4, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.numpad_5 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_5.sizePolicy().hasHeightForWidth()
        )
        self.numpad_5.setSizePolicy(sizePolicy)
        self.numpad_5.setMinimumSize(QtCore.QSize(150, 63))
        self.numpad_5.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_5.setFont(font)
        self.numpad_5.setTabletTracking(False)
        self.numpad_5.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_5.setFlat(True)
        self.numpad_5.setObjectName("numpad_5")
        self.gridLayout_2.addWidget(
            self.numpad_5, 1, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.numpad_1 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_1.sizePolicy().hasHeightForWidth()
        )
        self.numpad_1.setSizePolicy(sizePolicy)
        self.numpad_1.setMinimumSize(QtCore.QSize(150, 63))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_1.setFont(font)
        self.numpad_1.setTabletTracking(False)
        self.numpad_1.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_1.setFlat(True)
        self.numpad_1.setObjectName("numpad_1")
        self.gridLayout_2.addWidget(
            self.numpad_1, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.numpad_enter = IconButton(parent=self.gridLayoutWidget)
        self.numpad_enter.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.numpad_enter.sizePolicy().hasHeightForWidth()
        )
        self.numpad_enter.setSizePolicy(sizePolicy)
        self.numpad_enter.setMinimumSize(QtCore.QSize(60, 60))
        self.numpad_enter.setMaximumSize(QtCore.QSize(60, 60))
        self.numpad_enter.setStyleSheet("")
        self.numpad_enter.setText("")
        self.numpad_enter.setIconSize(QtCore.QSize(16, 16))
        self.numpad_enter.setCheckable(False)
        self.numpad_enter.setChecked(False)
        self.numpad_enter.setFlat(True)
        self.numpad_enter.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg"),
        )
        self.numpad_enter.setObjectName("numpad_enter")
        self.gridLayout_2.addWidget(
            self.numpad_enter, 3, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.numpad_7 = NumpadButton(parent=self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.numpad_7.sizePolicy().hasHeightForWidth()
        )
        self.numpad_7.setSizePolicy(sizePolicy)
        self.numpad_7.setMinimumSize(QtCore.QSize(150, 63))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(29)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_7.setFont(font)
        self.numpad_7.setTabletTracking(False)
        self.numpad_7.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_7.setFlat(True)
        self.numpad_7.setObjectName("numpad_7")
        self.gridLayout_2.addWidget(self.numpad_7, 0, 0, 1, 1)
        self.numpad_clear = IconButton(parent=self.gridLayoutWidget)
        self.numpad_clear.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.numpad_clear.sizePolicy().hasHeightForWidth()
        )
        self.numpad_clear.setSizePolicy(sizePolicy)
        self.numpad_clear.setMinimumSize(QtCore.QSize(60, 60))
        self.numpad_clear.setMaximumSize(QtCore.QSize(60, 60))
        self.numpad_clear.setStyleSheet("")
        self.numpad_clear.setText("")
        self.numpad_clear.setIconSize(QtCore.QSize(16, 16))
        self.numpad_clear.setCheckable(False)
        self.numpad_clear.setChecked(False)
        self.numpad_clear.setFlat(True)
        self.numpad_clear.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/dialog/media/btn_icons/no.svg"),
        )
        self.numpad_clear.setObjectName("numpad_clear")
        self.gridLayout_2.addWidget(
            self.numpad_clear, 3, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.retranslateUI()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUI(self) -> None:
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("customNumpad", "Form"))
        self.numpad_title.setText(
            _translate("customNumpad", "Target Temperature")
        )
        self.numpad_back_btn.setProperty(
            "button_type", _translate("customNumpad", "icon")
        )
        self.inserted_value.setText(_translate("customNumpad", "TextLabel"))
        self.numpad_6.setText(_translate("customNumpad", "6"))
        self.numpad_6.setProperty(
            "position", _translate("customNumpad", "right")
        )
        self.numpad_9.setText(_translate("customNumpad", "9"))
        self.numpad_9.setProperty(
            "position", _translate("customNumpad", "right")
        )
        self.numpad_8.setText(_translate("customNumpad", "8"))
        self.numpad_2.setText(_translate("customNumpad", "2"))
        self.numpad_0.setText(_translate("customNumpad", "0"))
        self.numpad_0.setProperty(
            "position", _translate("customNumpad", "down")
        )
        self.numpad_3.setText(_translate("customNumpad", "3"))
        self.numpad_3.setProperty(
            "position", _translate("customNumpad", "right")
        )
        self.numpad_4.setText(_translate("customNumpad", "4"))
        self.numpad_4.setProperty(
            "position", _translate("customNumpad", "left")
        )
        self.numpad_5.setText(_translate("customNumpad", "5"))
        self.numpad_1.setText(_translate("customNumpad", "1"))
        self.numpad_1.setProperty(
            "position", _translate("customNumpad", "left")
        )
        self.numpad_enter.setProperty(
            "button_type", _translate("customNumpad", "icon")
        )
        self.numpad_7.setText(_translate("customNumpad", "7"))
        self.numpad_7.setProperty(
            "position", _translate("customNumpad", "left")
        )
        self.numpad_clear.setProperty(
            "button_type", _translate("customNumpad", "icon")
        )
