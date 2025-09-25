from lib.utils.icon_button import IconButton
from lib.utils.blocks_label import BlocksLabel
from lib.utils.numpad_button import NumpadButton

from PyQt6 import QtCore, QtGui, QtWidgets


class CustomNumpad(QtWidgets.QWidget):
    """A custom numpad for inserting integer values"""

    value_selected = QtCore.pyqtSignal(str, int, name="value_selected")
    request_back = QtCore.pyqtSignal(name="request_back")
    start_glow_animation = QtCore.pyqtSignal(name="start_glow_animation")

    def __init__(
        self,
        parent,
    ) -> None:
        super().__init__(parent)
        self.setupUI()
        self.current_value: str = "0"
        self.name: str = ""
        self.min_value: int = 0
        self.max_value: int = 100
        self.firsttime: bool = True

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
        self.numpad_clear.clicked.connect(lambda: self.value_inserted("clear"))
        self.numpad_back_btn.clicked.connect(self.back_button)
        self.start_glow_animation.connect(
            self.inserted_value.start_glow_animation
        )

    def value_inserted(self, value: str) -> None:
        """Handle number insertion on the numpad

        Args:
            value (int | str): value
        """
        if self.firsttime and value.isnumeric():
            self.current_value = str(value)
            self.firsttime = False
        elif value.isnumeric():
            if self.current_value == "0":
                self.current_value = str(value)
            else:
                self.current_value += str(value)

        if "enter" in value and self.current_value.isnumeric():
            if len(self.current_value) == 0:
                self.current_value = "0"
            if (
                self.min_value
                <= int(self.current_value)
                <= self.max_value
            ):
                self.value_selected.emit(
                    self.name, int(self.current_value)
                )
                self.request_back.emit()

        elif "clear" in value:
            if len(self.current_value) > 1:
                self.current_value = self.current_value[:-1]
            else:
                self.current_value = "0"

        if not (self.min_value <= int(self.current_value) <= self.max_value):
            self.start_glow_animation.emit()
        else:
            self.inserted_value.glow_animation.stop()

        self.inserted_value.setText(str(self.current_value))
            
    def back_button(self):
        self.request_back.emit()

    def set_name(self, name: str) -> None:
        """Sets the header name for the page"""
        self.name = name
        self.numpad_title.setText(name)
        self.update_min_max_label()
        self.update()

    def set_value(self, value: int) -> None:
        self.current_value = str(value)
        self.inserted_value.setText(str(value))

    def set_min_value(self, min_value: int) -> None:
        self.min_value = min_value
        self.update_min_max_label()

    def set_max_value(self, max_value: int) -> None:
        self.max_value = max_value
        self.update_min_max_label()

    def update_min_max_label(self) -> None:
        """Updates the text of the min/max label."""
        self.min_max_label.setText(
            f"Range: {self.min_value} - {self.max_value}"
        )
        
    def setupUI(self) -> None:
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.BlankCursor))

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.setSizePolicy(sizePolicy)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setObjectName("blocks_numpad")
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(800, 480))
        self.main_content_layout = QtWidgets.QVBoxLayout()
        self.main_content_layout.setObjectName("main_content_layout")
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_layout.setSpacing(3)
        self.header_layout = QtWidgets.QHBoxLayout()

        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setObjectName("header_layout")
        self.numpad_title = BlocksLabel(self)
        self.numpad_title.setMinimumSize(QtCore.QSize(500, 60))
        self.numpad_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.numpad_title.setFont(font)
        self.numpad_title.setAutoFillBackground(False)
        self.numpad_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        palette = QtGui.QPalette()
        palette.setColor(palette.ColorRole.Window, QtGui.QColor("#FFFFFF00"))
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.numpad_title.setPalette(palette)
        self.numpad_title.setObjectName("numpad_title")
        self.header_layout.addWidget(
            self.numpad_title,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.numpad_back_btn = IconButton(self)
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
        self.numpad_back_btn.setPixmap(
            QtGui.QPixmap(":ui/media/btn_icons/back.svg")
        )
        self.numpad_back_btn.setObjectName("numpad_back_btn")
        self.header_layout.addWidget(
            self.numpad_back_btn,
            1,
            QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.numpad_back_btn.rect().setX(self.numpad_back_btn.rect().x() + 60)

        self.header_layout.setStretch(0, 1)
        self.header_layout.setStretch(1, 0)
        self.main_content_layout.addLayout(self.header_layout, 1)

        self.value_and_range_layout = QtWidgets.QVBoxLayout()
        self.value_and_range_layout.setSpacing(0)
        self.value_and_range_layout.setContentsMargins(0, 0, 0, 0)

        self.min_max_label = BlocksLabel(self)
        self.min_max_label.setMinimumSize(QtCore.QSize(500, 20))
        self.min_max_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.min_max_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.min_max_label.setStyleSheet("color: gray; font-size: 14px;")

        self.inserted_value = BlocksLabel(self)
        self.inserted_value.setMinimumSize(QtCore.QSize(500, 30))
        self.inserted_value.setMaximumSize(QtCore.QSize(16777215, 40))
        self.inserted_value.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.inserted_value.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self.inserted_value.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.NoTextInteraction
        )
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(20)
        self.inserted_value.setFont(font)
        palette = self.inserted_value.palette()
        palette.setColor(
            palette.ColorGroup.All,
            palette.ColorRole.Window,
            QtGui.QColor("#FFFFFF00"),
        )
        palette.setColor(
            palette.ColorGroup.All,
            palette.ColorRole.WindowText,
            QtGui.QColor("#FFFFFFFF"),
        )
        self.inserted_value.setBackgroundRole(palette.ColorRole.Window)
        self.inserted_value.setPalette(palette)
        self.inserted_value.setAcceptDrops(False)
        self.inserted_value.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.inserted_value.setObjectName("inserted_value")

        self.value_and_range_layout.addWidget(
            self.min_max_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.value_and_range_layout.addWidget(
            self.inserted_value, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )
        
        self.main_content_layout.addLayout(
            self.value_and_range_layout, 1
        )
        
        self.inserted_value.setBackgroundRole(QtGui.QPalette.ColorRole.Window)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.main_content_layout.addWidget(self.line, 1)

        self.button_grid_layout = QtWidgets.QGridLayout()
        self.button_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.button_grid_layout.setObjectName("button_grid_layout")
        self.button_grid_layout.setSpacing(6)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")
        font.setPointSize(28)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.numpad_9 = NumpadButton(self)
        sizePolicy.setHeightForWidth(
            self.numpad_9.sizePolicy().hasHeightForWidth()
        )
        self.numpad_9.setSizePolicy(sizePolicy)
        self.numpad_9.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_9.setFont(font)
        self.numpad_9.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.numpad_9.setFlat(True)
        self.numpad_9.setObjectName("numpad_9")
        self.button_grid_layout.addWidget(
            self.numpad_9, 0, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.numpad_8 = NumpadButton(parent=self)
        sizePolicy.setHeightForWidth(
            self.numpad_8.sizePolicy().hasHeightForWidth()
        )
        self.numpad_8.setSizePolicy(sizePolicy)
        self.numpad_8.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_8.setFont(font)
        self.numpad_8.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_8.setFlat(True)
        self.numpad_8.setObjectName("numpad_8")
        self.button_grid_layout.addWidget(
            self.numpad_8, 0, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.numpad_7 = NumpadButton(self)
        sizePolicy.setHeightForWidth(
            self.numpad_7.sizePolicy().hasHeightForWidth()
        )
        self.numpad_7.setSizePolicy(sizePolicy)
        self.numpad_7.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_7.setFont(font)
        self.numpad_7.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_7.setFlat(True)
        self.numpad_7.setObjectName("numpad_7")
        self.button_grid_layout.addWidget(
            self.numpad_7, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.numpad_6 = NumpadButton(self)
        sizePolicy.setHeightForWidth(
            self.numpad_6.sizePolicy().hasHeightForWidth()
        )
        self.numpad_6.setSizePolicy(sizePolicy)
        self.numpad_6.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_6.setFont(font)
        self.numpad_6.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_6.setFlat(True)
        self.numpad_6.setObjectName("numpad_6")

        self.button_grid_layout.addWidget(
            self.numpad_6, 1, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.numpad_5 = NumpadButton(self)
        sizePolicy.setHeightForWidth(
            self.numpad_5.sizePolicy().hasHeightForWidth()
        )
        self.numpad_5.setSizePolicy(sizePolicy)
        self.numpad_5.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_5.setFont(font)
        self.numpad_5.setFlat(True)
        self.numpad_5.setObjectName("numpad_5")
        self.button_grid_layout.addWidget(
            self.numpad_5, 1, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.numpad_4 = NumpadButton(self)
        sizePolicy.setHeightForWidth(
            self.numpad_4.sizePolicy().hasHeightForWidth()
        )
        self.numpad_4.setSizePolicy(sizePolicy)
        self.numpad_4.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_4.setFont(font)
        self.numpad_4.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_4.setFlat(True)
        self.numpad_4.setObjectName("numpad_4")
        self.button_grid_layout.addWidget(
            self.numpad_4, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.numpad_3 = NumpadButton(parent=self)
        sizePolicy.setHeightForWidth(
            self.numpad_3.sizePolicy().hasHeightForWidth()
        )
        self.numpad_3.setSizePolicy(sizePolicy)
        self.numpad_3.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_3.setFont(font)
        self.numpad_3.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_3.setFlat(True)
        self.numpad_3.setObjectName("numpad_3")
        self.button_grid_layout.addWidget(
            self.numpad_3, 2, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.numpad_2 = NumpadButton(self)
        sizePolicy.setHeightForWidth(
            self.numpad_2.sizePolicy().hasHeightForWidth()
        )
        self.numpad_2.setSizePolicy(sizePolicy)
        self.numpad_2.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_2.setFont(font)
        self.numpad_2.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_2.setFlat(True)
        self.numpad_2.setObjectName("numpad_2")
        self.button_grid_layout.addWidget(
            self.numpad_2, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.numpad_1 = NumpadButton(parent=self)
        sizePolicy.setHeightForWidth(
            self.numpad_1.sizePolicy().hasHeightForWidth()
        )
        self.numpad_1.setSizePolicy(sizePolicy)
        self.numpad_1.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_1.setFont(font)
        self.numpad_1.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_1.setFlat(True)
        self.numpad_1.setObjectName("numpad_1")
        self.button_grid_layout.addWidget(
            self.numpad_1, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.numpad_0 = NumpadButton(parent=self)
        sizePolicy.setHeightForWidth(
            self.numpad_0.sizePolicy().hasHeightForWidth()
        )
        self.numpad_0.setSizePolicy(sizePolicy)
        self.numpad_0.setMinimumSize(QtCore.QSize(150, 60))
        self.numpad_0.setFont(font)
        self.numpad_0.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.numpad_0.setFlat(True)
        self.numpad_0.setObjectName("numpad_0")
        self.button_grid_layout.addWidget(
            self.numpad_0, 3, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.numpad_enter = IconButton(parent=self)
        self.numpad_enter.setEnabled(True)
        sizePolicy.setHeightForWidth(
            self.numpad_enter.sizePolicy().hasHeightForWidth()
        )
        self.numpad_enter.setSizePolicy(sizePolicy)
        self.numpad_enter.setMinimumSize(QtCore.QSize(60, 60))
        self.numpad_enter.setFlat(True)
        self.numpad_enter.setPixmap(
            QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.numpad_enter.setObjectName("numpad_enter")
        self.button_grid_layout.addWidget(
            self.numpad_enter, 3, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.numpad_clear = IconButton(parent=self)
        sizePolicy.setHeightForWidth(
            self.numpad_clear.sizePolicy().hasHeightForWidth()
        )
        self.numpad_clear.setSizePolicy(sizePolicy)
        self.numpad_clear.setMinimumSize(QtCore.QSize(60, 60))
        self.numpad_clear.setFlat(True)
        self.numpad_clear.setPixmap(
            QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.numpad_clear.setObjectName("numpad_clear")
        self.button_grid_layout.addWidget(
            self.numpad_clear, 3, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.button_grid_layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.main_content_layout.addLayout(self.button_grid_layout)

        self.main_content_layout.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.setLayout(self.main_content_layout)

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