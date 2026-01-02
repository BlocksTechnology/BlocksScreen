import typing

from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_label import BlocksLabel
from lib.utils.icon_button import IconButton
from lib.utils.check_button import BlocksCustomCheckButton
from PyQt6 import QtCore, QtGui, QtWidgets


class BabystepPage(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    run_gcode: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )

    _z_offset: float = 0.1

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setObjectName("babystepPage")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_MouseTracking, True)
        self.setTabletTracking(True)
        self.setMouseTracking(True)

        self.setupUI()
        self.bbp_mvup.clicked.connect(self.on_move_nozzle_close)
        self.bbp_mvdown.clicked.connect(self.on_move_nozzle_away)
        self.babystep_back_btn.clicked.connect(self.request_back.emit)
        self.bbp_nozzle_offset_01.toggled.connect(self.handle_z_offset_change)
        self.bbp_nozzle_offset_025.toggled.connect(self.handle_z_offset_change)
        self.bbp_nozzle_offset_05.toggled.connect(self.handle_z_offset_change)
        self.bbp_nozzle_offset_1.toggled.connect(self.handle_z_offset_change)

        self.savebutton.clicked.connect(self.save_value)

    @QtCore.pyqtSlot(name="on_move_nozzle_close")
    def on_move_nozzle_close(self) -> None:
        """Move the nozzle closer to the print plate
        by the amount set in **` self._z_offset`**
        """
        self.run_gcode.emit(
            f"SET_GCODE_OFFSET Z_ADJUST=-{self._z_offset}"  # Z_ADJUST adds the value to the existing offset
        )
        self.savebutton.setVisible(True)

    @QtCore.pyqtSlot(name="on_move_nozzle_away")
    def on_move_nozzle_away(self) -> None:
        """Slot for Babystep button to get far from the
        bed by **` self._z_offset`** amount
        """
        self.run_gcode.emit(
            f"SET_GCODE_OFFSET Z_ADJUST=+{self._z_offset}"  # Z_ADJUST adds the value to the existing offset
        )
        self.savebutton.setVisible(True)

    @QtCore.pyqtSlot(name="handle_z_offset_change")
    def handle_z_offset_change(self) -> None:
        """Helper method for changing the value for Babystep.

        When a button is clicked, and the button has the mm value i the text,
        it'll change the internal value **z_offset** to the same has the button

        ***

        Possible values are: 0.01, 0.025, 0.05, 0.1 **mm**
        """
        _possible_z_values: typing.List = [0.01, 0.025, 0.05, 0.1]
        _sender: QtCore.QObject | None = self.sender()
        if self._z_offset == float(_sender.text()[:-3]):
            return
        self._z_offset = float(_sender.text()[:-3])

    def save_value(self):
        """Save new z offset value"""
        self.run_gcode.emit("Z_OFFSET_APPLY_PROBE")
        self.savebutton.setVisible(False)
        self.bbp_z_offset_title_label.setText(self.bbp_z_offset_current_value.text())

    def on_gcode_move_update(self, name: str, value: list) -> None:
        """Handle gcode move updates"""
        if not value:
            return

        if name == "homing_origin":
            self._z_offset_text = value[2]
            self.bbp_z_offset_current_value.setText(f"Z: {self._z_offset_text:.3f}mm")
        if self.bbp_z_offset_title_label.text() == "smth":
            self.bbp_z_offset_title_label.setText(f"Z: {self._z_offset_text:.3f}mm")

    def setupUI(self):
        """Setup babystep page ui"""
        self.bbp_offset_value_selector_group = QtWidgets.QButtonGroup(self)
        self.bbp_offset_value_selector_group.setExclusive(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(
            QtCore.QSize(720, 420)
        )  # This sets the maximum width of the entire page
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        # Main Vertical Layout for the entire page
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        # Header Layout
        self.bbp_header_layout = QtWidgets.QHBoxLayout()
        self.bbp_header_layout.setObjectName("bbp_header_layout")
        self.bbp_header_title = QtWidgets.QLabel(parent=self)
        sizePolicy.setHeightForWidth(
            self.bbp_header_title.sizePolicy().hasHeightForWidth()
        )
        self.bbp_header_title.setSizePolicy(sizePolicy)
        self.bbp_header_title.setMinimumSize(QtCore.QSize(200, 60))
        self.bbp_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.bbp_header_title.setFont(font)
        palette = QtGui.QPalette()
        palette.setColor(
            palette.ColorGroup.All,
            palette.ColorRole.Window,
            QtCore.Qt.GlobalColor.transparent,
        )
        palette.setColor(
            palette.ColorGroup.All,
            palette.ColorRole.WindowText,
            QtGui.QColor("#FFFFFF"),
        )
        self.bbp_header_title.setAutoFillBackground(True)
        self.bbp_header_title.setBackgroundRole(palette.ColorRole.Window)
        self.bbp_header_title.setPalette(palette)
        self.bbp_header_title.setText("Babystep")
        self.bbp_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.bbp_header_title.setObjectName("bbp_header_title")

        self.savebutton = BlocksCustomButton(self)
        self.savebutton.setGeometry(QtCore.QRect(460, 340, 200, 60))
        self.savebutton.setText("Save?")
        self.savebutton.setObjectName("savebutton")
        self.savebutton.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/save.svg"))
        self.savebutton.setVisible(False)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.savebutton.setFont(font)

        spacerItem = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.bbp_header_layout.addItem(spacerItem)

        self.bbp_header_layout.addWidget(
            self.bbp_header_title,
            0,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        self.babystep_back_btn = IconButton(parent=self)
        sizePolicy.setHeightForWidth(
            self.babystep_back_btn.sizePolicy().hasHeightForWidth()
        )
        self.babystep_back_btn.setSizePolicy(sizePolicy)
        self.babystep_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.babystep_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.babystep_back_btn.setText("")
        self.babystep_back_btn.setFlat(True)
        self.babystep_back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.babystep_back_btn.setObjectName("babystep_back_btn")

        self.bbp_header_layout.addWidget(
            self.babystep_back_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.bbp_header_layout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.bbp_header_layout)

        self.main_content_horizontal_layout = QtWidgets.QHBoxLayout()
        self.main_content_horizontal_layout.setObjectName(
            "main_content_horizontal_layout"
        )

        # Offset Steps Buttons Group Box (LEFT side of main_content_horizontal_layout)
        self.bbp_offset_steps_buttons_group_box = QtWidgets.QGroupBox(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.bbp_offset_steps_buttons_group_box.setFont(font)
        self.bbp_offset_steps_buttons_group_box.setFlat(True)
        # Add stylesheet to explicitly remove any border from the QGroupBox
        self.bbp_offset_steps_buttons_group_box.setStyleSheet(
            "QGroupBox { border: none; }"
        )
        self.bbp_offset_steps_buttons_group_box.setObjectName(
            "bbp_offset_steps_buttons_group_box"
        )

        self.bbp_offset_steps_buttons = QtWidgets.QVBoxLayout(
            self.bbp_offset_steps_buttons_group_box
        )
        self.bbp_offset_steps_buttons.setContentsMargins(9, 9, 9, 9)
        self.bbp_offset_steps_buttons.setObjectName("bbp_offset_steps_buttons")

        # 0.1mm button
        self.bbp_nozzle_offset_1 = BlocksCustomCheckButton(
            parent=self.bbp_offset_steps_buttons_group_box
        )
        self.bbp_nozzle_offset_1.setMinimumSize(QtCore.QSize(100, 70))
        self.bbp_nozzle_offset_1.setMaximumSize(QtCore.QSize(100, 70))
        self.bbp_nozzle_offset_1.setText("0.1 mm")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.bbp_nozzle_offset_1.setFont(font)
        self.bbp_nozzle_offset_1.setCheckable(True)
        self.bbp_nozzle_offset_1.setChecked(True)  # Set as initially checked
        self.bbp_nozzle_offset_1.setFlat(True)
        self.bbp_nozzle_offset_1.setProperty("button_type", "")
        self.bbp_nozzle_offset_1.setObjectName("bbp_nozzle_offset_1")
        self.bbp_offset_value_selector_group.addButton(self.bbp_nozzle_offset_1)
        self.bbp_offset_steps_buttons.addWidget(
            self.bbp_nozzle_offset_1,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # Line separator for 0.1mm - set size policy to expanding horizontally

        # 0.01mm button
        self.bbp_nozzle_offset_01 = BlocksCustomCheckButton(
            parent=self.bbp_offset_steps_buttons_group_box
        )
        self.bbp_nozzle_offset_01.setMinimumSize(QtCore.QSize(100, 70))
        self.bbp_nozzle_offset_01.setMaximumSize(
            QtCore.QSize(100, 70)
        )  # Increased max width by 5 pixels
        self.bbp_nozzle_offset_01.setText("0.01 mm")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.bbp_nozzle_offset_01.setFont(font)
        self.bbp_nozzle_offset_01.setCheckable(True)
        self.bbp_nozzle_offset_01.setFlat(True)
        self.bbp_nozzle_offset_01.setProperty("button_type", "")
        self.bbp_nozzle_offset_01.setObjectName("bbp_nozzle_offset_01")
        self.bbp_offset_value_selector_group.addButton(self.bbp_nozzle_offset_01)
        self.bbp_offset_steps_buttons.addWidget(
            self.bbp_nozzle_offset_01,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # 0.05mm button
        self.bbp_nozzle_offset_05 = BlocksCustomCheckButton(
            parent=self.bbp_offset_steps_buttons_group_box
        )
        self.bbp_nozzle_offset_05.setMinimumSize(QtCore.QSize(100, 70))
        self.bbp_nozzle_offset_05.setMaximumSize(
            QtCore.QSize(100, 70)
        )  # Increased max width by 5 pixels
        self.bbp_nozzle_offset_05.setText("0.05 mm")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.bbp_nozzle_offset_05.setFont(font)
        self.bbp_nozzle_offset_05.setCheckable(True)
        self.bbp_nozzle_offset_05.setFlat(True)
        self.bbp_nozzle_offset_05.setProperty("button_type", "")
        self.bbp_nozzle_offset_05.setObjectName("bbp_nozzle_offset_05")
        self.bbp_offset_value_selector_group.addButton(self.bbp_nozzle_offset_05)
        self.bbp_offset_steps_buttons.addWidget(
            self.bbp_nozzle_offset_05,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # 0.025mm button
        self.bbp_nozzle_offset_025 = BlocksCustomCheckButton(
            parent=self.bbp_offset_steps_buttons_group_box
        )
        self.bbp_nozzle_offset_025.setMinimumSize(QtCore.QSize(100, 70))
        self.bbp_nozzle_offset_025.setMaximumSize(
            QtCore.QSize(100, 70)
        )  # Increased max width by 5 pixels
        self.bbp_nozzle_offset_025.setText("0.025 mm")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.bbp_nozzle_offset_025.setFont(font)
        self.bbp_nozzle_offset_025.setCheckable(True)
        self.bbp_nozzle_offset_025.setFlat(True)
        self.bbp_nozzle_offset_025.setProperty("button_type", "")
        self.bbp_nozzle_offset_025.setObjectName("bbp_nozzle_offset_025")
        self.bbp_offset_value_selector_group.addButton(self.bbp_nozzle_offset_025)
        self.bbp_offset_steps_buttons.addWidget(
            self.bbp_nozzle_offset_025,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # Line separator for 0.025mm - set size policy to expanding horizontally

        # Set the layout for the group box
        self.bbp_offset_steps_buttons_group_box.setLayout(self.bbp_offset_steps_buttons)
        # Add the group box to the main content horizontal layout FIRST for left placement
        self.main_content_horizontal_layout.addWidget(
            self.bbp_offset_steps_buttons_group_box
        )

        # Graphic and Current Value Frame (This will now be in the MIDDLE)
        self.frame_2 = QtWidgets.QFrame(parent=self)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(350, 160))
        self.frame_2.setMaximumSize(QtCore.QSize(350, 160))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.bbp_babystep_graphic = QtWidgets.QLabel(parent=self.frame_2)
        self.bbp_babystep_graphic.setGeometry(QtCore.QRect(0, 30, 371, 121))
        self.bbp_babystep_graphic.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.bbp_babystep_graphic.setPixmap(
            QtGui.QPixmap(":/graphics/media/graphics/babystep_graphic.png")
        )
        self.bbp_babystep_graphic.setScaledContents(False)
        self.bbp_babystep_graphic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.bbp_babystep_graphic.setObjectName("bbp_babystep_graphic")

        # === NEW LABEL ADDED HERE ===
        # This is the title label that appears above the red value box.
        self.bbp_z_offset_title_label = QtWidgets.QLabel(parent=self)
        # Position it just above the red box. Red box is at y=70, so y=40 is appropriate.
        self.bbp_z_offset_title_label.setGeometry(QtCore.QRect(100, 40, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)

        self.bbp_z_offset_title_label.setFont(font)
        # Set color to white to be visible on the dark background
        self.bbp_z_offset_title_label.setStyleSheet(
            "color: gray; background: transparent;"
        )
        self.bbp_z_offset_title_label.setText("Z-Offset")
        self.bbp_z_offset_title_label.setObjectName("bbp_z_offset_title_label")
        self.bbp_z_offset_title_label.setText("smth")
        self.bbp_z_offset_title_label.setGeometry(420, 270, 200, 30)

        # === END OF NEW LABEL ===

        self.bbp_z_offset_current_value = BlocksLabel(parent=self.frame_2)
        self.bbp_z_offset_current_value.setGeometry(QtCore.QRect(100, 70, 200, 60))
        sizePolicy.setHeightForWidth(
            self.bbp_z_offset_current_value.sizePolicy().hasHeightForWidth()
        )
        self.bbp_z_offset_current_value.setSizePolicy(sizePolicy)
        self.bbp_z_offset_current_value.setMinimumSize(QtCore.QSize(150, 60))
        self.bbp_z_offset_current_value.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.bbp_z_offset_current_value.setFont(font)
        self.bbp_z_offset_current_value.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.bbp_z_offset_current_value.setText(f"Z: {self._z_offset:.2f}mm")
        self.bbp_z_offset_current_value.setPixmap(
            QtGui.QPixmap(":/graphics/media/btn_icons/z_offset_adjust.svg")
        )
        self.bbp_z_offset_current_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.bbp_z_offset_current_value.setObjectName("bbp_z_offset_current_value")
        # Add graphic frame AFTER the offset buttons group box
        self.main_content_horizontal_layout.addWidget(
            self.frame_2,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # Move Buttons Layout (This will now be on the RIGHT)
        self.bbp_buttons_layout = QtWidgets.QVBoxLayout()
        self.bbp_buttons_layout.setContentsMargins(5, 5, 5, 5)
        self.bbp_buttons_layout.setObjectName("bbp_buttons_layout")
        self.bbp_mvup = IconButton(parent=self)
        sizePolicy.setHeightForWidth(self.bbp_mvup.sizePolicy().hasHeightForWidth())
        self.bbp_mvup.setSizePolicy(sizePolicy)
        self.bbp_mvup.setMinimumSize(QtCore.QSize(80, 80))
        self.bbp_mvup.setMaximumSize(QtCore.QSize(80, 80))
        self.bbp_mvup.setText("")
        self.bbp_mvup.setFlat(True)
        self.bbp_mvup.setPixmap(
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/up_arrow.svg")
        )
        self.bbp_mvup.setObjectName("bbp_away_from_bed")
        self.bbp_option_button_group = QtWidgets.QButtonGroup(self)
        self.bbp_option_button_group.setObjectName("bbp_option_button_group")
        self.bbp_option_button_group.addButton(self.bbp_mvup)
        self.bbp_buttons_layout.addWidget(
            self.bbp_mvup, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.bbp_mvdown = IconButton(parent=self)
        sizePolicy.setHeightForWidth(self.bbp_mvdown.sizePolicy().hasHeightForWidth())
        self.bbp_mvdown.setSizePolicy(sizePolicy)
        self.bbp_mvdown.setMinimumSize(QtCore.QSize(80, 80))
        self.bbp_mvdown.setMaximumSize(QtCore.QSize(80, 80))
        self.bbp_mvdown.setText("")
        self.bbp_mvdown.setFlat(True)
        self.bbp_mvdown.setPixmap(
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/down_arrow.svg")
        )
        self.bbp_mvdown.setObjectName("bbp_close_to_bed")
        self.bbp_option_button_group.addButton(self.bbp_mvdown)
        self.bbp_buttons_layout.addWidget(
            self.bbp_mvdown, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.main_content_horizontal_layout.addItem(spacerItem)

        # Add move buttons layout LAST for right placement
        self.main_content_horizontal_layout.addLayout(self.bbp_buttons_layout)

        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.main_content_horizontal_layout.addItem(spacerItem)

        # Set stretch factors for main content horizontal layout
        # This will distribute space: offset buttons, graphic frame, move buttons
        self.main_content_horizontal_layout.setStretch(
            0, 1
        )  # offset_steps_buttons_group_box
        self.main_content_horizontal_layout.setStretch(
            1, 2
        )  # frame_2 (graphic and current value)
        self.main_content_horizontal_layout.setStretch(
            2, 0
        )  # bbp_buttons_layout (move buttons)

        # Add the main content horizontal layout to the vertical layout
        self.verticalLayout.addLayout(self.main_content_horizontal_layout)

        # Set stretch factors for vertical layout (adjust as needed for overall sizing)
        self.verticalLayout.setStretch(
            1, 1
        )  # This stretch applies to main_content_horizontal_layout

        self.setLayout(self.verticalLayout)
