import logging
import typing

from lib.utils.blocks_label import BlocksLabel
from lib.utils.check_button import BlocksCustomCheckButton
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)

# Button definitions: (label, value, object_name, initially_checked)
_OFFSET_STEPS: list[tuple[str, float, str, bool]] = [
    ("0.010 mm", 0.01, "bbp_nozzle_offset_01", True),
    ("0.025 mm", 0.025, "bbp_nozzle_offset_025", False),
    ("0.050 mm", 0.05, "bbp_nozzle_offset_05", False),
    ("0.100 mm", 0.1, "bbp_nozzle_offset_1", False),
]


class BabystepPage(QtWidgets.QWidget):
    """Page for adjusting Z offset in small increments during a print."""

    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    run_gcode: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._z_offset: float = _OFFSET_STEPS[0][1]
        self.setObjectName("babystepPage")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_MouseTracking, True)
        self.setTabletTracking(True)
        self.setMouseTracking(True)

        self._baby_stepchange = False
        self._z_offset_text: float = 0.0
        self._pending_z_offset: float = 0.0

        self._setupUI()
        self.bbp_mvup.clicked.connect(self.on_move_nozzle_close)
        self.bbp_mvdown.clicked.connect(self.on_move_nozzle_away)
        self.bbp_mvup.setEnabled(False)
        self.bbp_mvdown.setEnabled(False)
        self.babystep_back_btn.clicked.connect(self.request_back.emit)

    @property
    def baby_stepchange(self):
        """Returns if the babystep was changed during print."""
        return self._baby_stepchange

    @baby_stepchange.setter
    def baby_stepchange(self, value: bool) -> None:
        """Set the babystep-changed flag."""
        self._baby_stepchange = value

    @QtCore.pyqtSlot(name="on_move_nozzle_close")
    def on_move_nozzle_close(self) -> None:
        """Move the nozzle closer to the print plate."""
        self.run_gcode.emit(f"SET_GCODE_OFFSET Z_ADJUST=-{self._z_offset} MOVE=1")
        self._pending_z_offset -= self._z_offset
        self.bbp_z_offset_current_value.setText(
            f"Z: {round(self._pending_z_offset, 3) or 0.0:.3f} mm"
        )
        self._baby_stepchange = True

    @QtCore.pyqtSlot(name="on_move_nozzle_away")
    def on_move_nozzle_away(self) -> None:
        """Move the nozzle away from the print plate."""
        self.run_gcode.emit(f"SET_GCODE_OFFSET Z_ADJUST=+{self._z_offset} MOVE=1")
        self._pending_z_offset += self._z_offset
        self.bbp_z_offset_current_value.setText(
            f"Z: {round(self._pending_z_offset, 3) or 0.0:.3f} mm"
        )
        self._baby_stepchange = True

    @QtCore.pyqtSlot(str, str, name="on_print_state_update")
    def on_print_state_update(self, field: str, value: str) -> None:
        """Enable move buttons only while the printer is actively printing."""
        if "state" in field:
            printing = value == "printing"
            self.bbp_mvup.setEnabled(printing)
            self.bbp_mvdown.setEnabled(printing)

    def _set_z_offset(self, value: float) -> None:
        """Update the active step size."""
        if self._z_offset != value:
            self._z_offset = value

    @QtCore.pyqtSlot(str, list, name="on_gcode_move_update")
    def on_gcode_move_update(self, name: str, value: list) -> None:
        """Handle gcode move updates from Klipper."""
        if not value:
            return

        if name == "homing_origin" and len(value) > 2:
            confirmed = value[2]
            self._z_offset_text = confirmed
            self.bbp_z_offset_title_label.setText(
                f"Z: {round(confirmed, 3) or 0.0:.3f} mm"
            )
            # Always sync pending offset to Klipper's confirmed value
            self._pending_z_offset = confirmed
            self.bbp_z_offset_current_value.setText(
                f"Z: {round(confirmed, 3) or 0.0:.3f} mm"
            )

    def _create_offset_button(
        self,
        parent: QtWidgets.QWidget,
        label: str,
        obj_name: str,
        checked: bool,
        font: QtGui.QFont,
    ) -> BlocksCustomCheckButton:
        """Create a single offset-step check button."""
        btn = BlocksCustomCheckButton(parent=parent)
        btn.setMinimumSize(QtCore.QSize(100, 70))
        btn.setMaximumSize(QtCore.QSize(100, 70))
        btn.setText(label)
        btn.setFont(font)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setFlat(True)
        btn.setProperty("button_type", "")
        btn.setObjectName(obj_name)
        return btn

    def _setupUI(self) -> None:
        """Setup babystep page UI."""
        btn_group = QtWidgets.QButtonGroup(self)
        btn_group.setExclusive(True)

        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        main_vlayout = QtWidgets.QVBoxLayout(self)

        header = QtWidgets.QHBoxLayout()

        title_font = QtGui.QFont()
        title_font.setPointSize(22)
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

        self.bbp_header_title = QtWidgets.QLabel("Babystep", parent=self)
        self.bbp_header_title.setMinimumSize(QtCore.QSize(200, 60))
        self.bbp_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.bbp_header_title.setFont(title_font)
        self.bbp_header_title.setAutoFillBackground(True)
        self.bbp_header_title.setBackgroundRole(palette.ColorRole.Window)
        self.bbp_header_title.setPalette(palette)
        self.bbp_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header.addWidget(self.bbp_header_title, 1)

        self.babystep_back_btn = IconButton(parent=self)
        self.babystep_back_btn.setSizePolicy(size_policy)
        self.babystep_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.babystep_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.babystep_back_btn.setFlat(True)
        self.babystep_back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        header.addWidget(self.babystep_back_btn, 0)
        main_vlayout.addLayout(header)

        # --- Main content (3 columns) ---
        content = QtWidgets.QHBoxLayout()

        # Column 1: offset step buttons (highest → lowest)
        group_box = QtWidgets.QGroupBox(self)
        btn_font = QtGui.QFont()
        btn_font.setPointSize(14)
        group_box.setFont(btn_font)
        group_box.setFlat(True)
        group_box.setStyleSheet("QGroupBox { border: none; }")

        steps_layout = QtWidgets.QVBoxLayout(group_box)
        steps_layout.setContentsMargins(9, 9, 9, 9)

        center = (
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        for label, value, obj_name, checked in _OFFSET_STEPS:
            btn = self._create_offset_button(
                group_box, label, obj_name, checked, btn_font
            )
            btn.toggled.connect(
                lambda checked_state, v=value: checked_state and self._set_z_offset(v)
            )
            setattr(self, obj_name, btn)
            btn_group.addButton(btn)
            steps_layout.addWidget(btn, 0, center)

        content.addWidget(group_box)

        # Column 2: graphic + Z offset labels
        frame = QtWidgets.QFrame(parent=self)
        frame.setSizePolicy(size_policy)
        frame.setMinimumSize(QtCore.QSize(350, 160))
        frame.setMaximumSize(QtCore.QSize(350, 160))
        frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.bbp_babystep_graphic = QtWidgets.QLabel(parent=frame)
        self.bbp_babystep_graphic.setGeometry(QtCore.QRect(0, 30, 371, 121))
        self.bbp_babystep_graphic.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.bbp_babystep_graphic.setPixmap(
            QtGui.QPixmap(":/graphics/media/graphics/babystep_graphic.png")
        )
        self.bbp_babystep_graphic.setScaledContents(False)
        self.bbp_babystep_graphic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        grey_font = QtGui.QFont()
        grey_font.setPointSize(12)
        self.bbp_z_offset_title_label = QtWidgets.QLabel(parent=self)
        self.bbp_z_offset_title_label.setFont(grey_font)
        self.bbp_z_offset_title_label.setStyleSheet(
            "color: gray; background: transparent;"
        )
        self.bbp_z_offset_title_label.setText(
            f"Z: {round(self._z_offset_text, 3) or 0.0:.3f} mm"
        )
        self.bbp_z_offset_title_label.setGeometry(420, 270, 200, 30)

        white_font = QtGui.QFont()
        white_font.setPointSize(14)
        self.bbp_z_offset_current_value = BlocksLabel(parent=frame)
        self.bbp_z_offset_current_value.setGeometry(QtCore.QRect(100, 70, 200, 60))
        self.bbp_z_offset_current_value.setSizePolicy(size_policy)
        self.bbp_z_offset_current_value.setMinimumSize(QtCore.QSize(150, 60))
        self.bbp_z_offset_current_value.setMaximumSize(QtCore.QSize(200, 60))
        self.bbp_z_offset_current_value.setFont(white_font)
        self.bbp_z_offset_current_value.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.bbp_z_offset_current_value.setText(
            f"Z: {round(self._pending_z_offset, 3) or 0.0:.3f} mm"
        )
        self.bbp_z_offset_current_value.setPixmap(
            QtGui.QPixmap(":/graphics/media/btn_icons/z_offset_adjust.svg")
        )
        self.bbp_z_offset_current_value.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

        content.addWidget(frame, 0, center)

        # Spacer before move buttons
        content.addItem(
            QtWidgets.QSpacerItem(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Column 3: move up/down buttons
        move_layout = QtWidgets.QVBoxLayout()
        move_layout.setContentsMargins(5, 5, 5, 5)

        self.bbp_mvup = IconButton(parent=self)
        self.bbp_mvup.setSizePolicy(size_policy)
        self.bbp_mvup.setMinimumSize(QtCore.QSize(80, 80))
        self.bbp_mvup.setMaximumSize(QtCore.QSize(80, 80))
        self.bbp_mvup.setFlat(True)
        self.bbp_mvup.setPixmap(
            QtGui.QPixmap(":/baby_step/media/btn_icons/move_nozzle_close.svg")
        )
        move_layout.addWidget(self.bbp_mvup, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        self.bbp_mvdown = IconButton(parent=self)
        self.bbp_mvdown.setSizePolicy(size_policy)
        self.bbp_mvdown.setMinimumSize(QtCore.QSize(80, 80))
        self.bbp_mvdown.setMaximumSize(QtCore.QSize(80, 80))
        self.bbp_mvdown.setFlat(True)
        self.bbp_mvdown.setPixmap(
            QtGui.QPixmap(":/baby_step/media/btn_icons/move_nozzle_away.svg")
        )
        move_layout.addWidget(self.bbp_mvdown, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        content.addLayout(move_layout)

        # Trailing spacer
        content.addItem(
            QtWidgets.QSpacerItem(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        content.setStretch(0, 1)  # offset buttons
        content.setStretch(1, 2)  # graphic frame
        content.setStretch(2, 0)  # move buttons

        main_vlayout.addLayout(content)
        main_vlayout.setStretch(1, 1)
        self.setLayout(main_vlayout)
