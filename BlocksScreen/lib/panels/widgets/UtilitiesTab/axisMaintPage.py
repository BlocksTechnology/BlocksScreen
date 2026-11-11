import logging
import typing
from collections.abc import Callable

from lib.panels.widgets.Common.basePopup import BasePopup
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.check_button import BlocksCustomCheckButton
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


_logger = logging.getLogger(__name__)

# FINISH_Z: max_z_velocity 10 caps its F1200, so 6 x 449 mm = 270 s, then G28 from the top.
_SAFETY_TIMEOUT_MS = 600_000


class AxisMaintPage(QtWidgets.QWidget):
    """Axis Maintenance page of the utilities tab."""

    request_back = QtCore.pyqtSignal(name="request-back-button")

    call_load_panel = QtCore.pyqtSignal(bool, str, bool, name="call-load-panel")

    def __init__(self, parent: typing.Optional["QtWidgets.QWidget"]) -> None:
        super().__init__(parent)

        self.gcode_runner: Callable[..., bool] | None = None
        self._run_id = 0
        self._timed_out = False
        self._safety = QtCore.QTimer(self)
        self._safety.setSingleShot(True)
        self._safety.setInterval(_SAFETY_TIMEOUT_MS)
        self._safety.timeout.connect(self._on_safety_timeout)
        self.current_object: str | None = None
        self.answerPage = BasePopup(self, False, True)
        self.answerPage.accepted.connect(self._run_AXIS_MAINTENANCE_gcode)

        self._setup_ui()
        self.axes_back_btn.clicked.connect(self.request_back.emit)
        self.am_execute.clicked.connect(self.axis_maintenance)

    def _run_AXIS_MAINTENANCE_gcode(self):
        axis = self.current_object
        if axis:
            self.call_load_panel.emit(
                True, f"Running maintenance cycle on {axis.upper()} axis...", False
            )
            self._send(f"AXIS_MAINTENANCE_FINISH_{axis}\nM400", self._on_cycle_done)

        else:
            self.answerPage.hide()

    def axis_maintenance(self) -> None:
        """Routine, checks axis movement for printer debugging"""
        axis = self.axis_maintenance_gb.checkedButton().text().lower()
        self.current_object = axis

        self.answerPage.set_message(
            f"Apply oil to the {axis.upper()} axis, then press Confirm.",
        )

        self.call_load_panel.emit(True, f"Homing {axis.upper()} axis...", False)
        self._send(f"AXIS_MAINTENANCE_{axis}\nM400", self._on_homed)

    def _send(self, script: str, on_done: Callable[[object], None]) -> None:
        """Run ``script``; ``on_done`` gets the reply, or an error if unsent."""
        self._run_id += 1
        run_id = self._run_id
        self._timed_out = False
        # A second run would queue behind the first in Klipper's gcode mutex.
        self.am_execute.setEnabled(False)

        def on_reply(reply: object) -> None:
            if run_id != self._run_id:
                return
            self._safety.stop()
            self.am_execute.setEnabled(True)
            if isinstance(reply, dict) and "error" in reply:
                _logger.warning(
                    "Axis maintenance: %s failed: %s",
                    script.split("\n", 1)[0],
                    reply["error"],
                )
            if self._timed_out:
                # Too late for the oil prompt; drop any overlay the timeout left.
                self.call_load_panel.emit(False, "", False)
                return
            on_done(reply)

        # Moonraker replies to gcode.script once Klipper has run the whole script,
        # and fails it with an error when the socket closes, so a reply always comes.
        self._safety.start()
        run = self.gcode_runner
        if run is None:
            _logger.warning("Axis maintenance: no gcode runner wired, not sending")
        if not (run and run(script, callback=on_reply)):
            on_reply({"error": {"code": -1, "message": "not connected"}})

    def _on_safety_timeout(self) -> None:
        """Close the loading screen when Klipper never replied."""
        self._timed_out = True
        _logger.warning(
            "Axis maintenance: no reply in %d s, closing the loading screen",
            _SAFETY_TIMEOUT_MS // 1000,
        )
        # Hidden page: the overlay now belongs to whichever flow moved the user away.
        if self.isVisible():
            self.call_load_panel.emit(False, "", False)

    def _on_homed(self, result: object) -> None:
        """Drop the loading screen and show the oil prompt once homing succeeded."""
        self.call_load_panel.emit(False, "", False)
        # No popup here: MainWindow pops up Klipper's "!!", ConnectionPage covers unsent
        if isinstance(result, dict) and "error" in result:
            return
        # Confirm moves the axis, so never ask from behind another tab.
        if not self.isVisible():
            _logger.info(
                "Axis maintenance: page left during homing, oil prompt skipped"
            )
            return
        self.answerPage.show()

    def _on_cycle_done(self, _result: object) -> None:
        """Drop the loading screen when the maintenance cycle ends."""
        self.call_load_panel.emit(False, "", False)

    def _setup_ui(self) -> None:
        self.setObjectName("axes_page")

        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem12 = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout_7.addItem(spacerItem12)
        self.lcd_settings_header_layout = QtWidgets.QHBoxLayout()
        self.lcd_settings_header_layout.setObjectName("lcd_settings_header_layout")
        spacerItem13 = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.lcd_settings_header_layout.addItem(spacerItem13)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )

        self.lcd_settings_title_label = QtWidgets.QLabel(parent=self)
        self.lcd_settings_title_label.setSizePolicy(sizePolicy)
        self.lcd_settings_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.lcd_settings_title_label.setFont(font)
        self.lcd_settings_title_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.lcd_settings_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lcd_settings_header_layout.addWidget(self.lcd_settings_title_label)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        self.axes_back_btn = IconButton(parent=self)
        self.axes_back_btn.setSizePolicy(sizePolicy)
        self.axes_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.axes_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.axes_back_btn.setFont(font)
        self.axes_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.axes_back_btn.setObjectName("axes_back_btn")

        self.lcd_settings_header_layout.addWidget(self.axes_back_btn)
        self.verticalLayout_7.addLayout(self.lcd_settings_header_layout)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.frame_2 = BlocksCustomFrame(parent=self)
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(650, 0))
        self.frame_2.setObjectName("frame_2")

        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")

        self.axis_maintenance_gb = QtWidgets.QButtonGroup(self)
        self.axis_maintenance_gb.setObjectName("axis_maintenance_gb")

        self.am_execute = BlocksCustomButton(parent=self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)

        self.am_execute.setSizePolicy(sizePolicy)
        self.am_execute.setMinimumSize(QtCore.QSize(250, 80))
        self.am_execute.setMaximumSize(QtCore.QSize(250, 80))
        self.am_execute.setFont(font)
        self.am_execute.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.am_execute.setObjectName("am_execute")
        self.gridLayout.addWidget(self.am_execute, 2, 1, 1, 1)

        font = QtGui.QFont()
        font.setPointSize(20)

        self.am_y = BlocksCustomCheckButton(parent=self.frame_2)
        self.am_y.setMinimumSize(QtCore.QSize(60, 80))
        self.am_y.setMaximumSize(QtCore.QSize(250, 80))
        self.am_y.setFont(font)
        self.am_y.setCheckable(True)
        self.am_y.setChecked(True)
        self.am_y.setAutoExclusive(True)
        self.am_y.setFlat(True)
        self.am_y.setObjectName("am_y")
        self.axis_maintenance_gb.addButton(self.am_y)

        self.gridLayout.addWidget(self.am_y, 1, 0, 1, 1)

        self.am_z = BlocksCustomCheckButton(parent=self.frame_2)
        self.am_z.setMinimumSize(QtCore.QSize(60, 80))
        self.am_z.setMaximumSize(QtCore.QSize(250, 80))
        self.am_z.setFont(font)
        self.am_z.setCheckable(True)
        self.am_z.setAutoExclusive(True)
        self.axis_maintenance_gb.addButton(self.am_z)
        self.gridLayout.addWidget(self.am_z, 2, 0, 1, 1)

        self.am_x = BlocksCustomCheckButton(parent=self.frame_2)
        self.am_x.setMinimumSize(QtCore.QSize(250, 80))
        self.am_x.setMaximumSize(QtCore.QSize(250, 80))
        self.am_x.setFont(font)
        self.am_x.setCheckable(True)
        self.am_x.setAutoExclusive(True)
        self.axis_maintenance_gb.addButton(self.am_x)
        self.gridLayout.addWidget(self.am_x, 0, 0, 1, 1)

        self.verticalLayout_7.addWidget(
            self.frame_2, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.lcd_settings_title_label.setText("Axis Maintenance")

        self.axes_back_btn.setText("Back")
        self.am_execute.setText("Execute")

        self.am_z.setText("Z")
        self.am_x.setText("X")
        self.am_y.setText("Y")
