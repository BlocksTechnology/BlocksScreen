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

# Prep: G28 probes down at 3 mm/s from Z<=506 (~170 s), Z_TILT retries, Z climb.
_PREP_TIMEOUT_MS = 600_000
# FINISH_Z: max_z_velocity 10 caps its F1200, so 6 x 449 mm = 270 s, then G28 from the top.
_CYCLE_TIMEOUT_MS = 600_000
# Klipper errors are broadcast as "!!" (MainWindow popup); -1/503 show ConnectionPage.
_COVERED_ERROR_CODES = frozenset({-1, 400, 503})


class AxisMaintPage(QtWidgets.QWidget):
    """Axis Maintenance page of the utilities tab."""

    request_back = QtCore.pyqtSignal(name="request-back-button")

    call_load_panel = QtCore.pyqtSignal(bool, str, bool, name="call-load-panel")

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        gcode_runner: Callable[..., bool] | None = None,
    ) -> None:
        super().__init__(parent)

        # MoonAPI.run_gcode(script, callback=...); False means the request was not sent
        self.gcode_runner = gcode_runner
        # Bumped on timeout too, so a reply to an abandoned run is dropped.
        self._run_id = 0
        self._safety = QtCore.QTimer(self)
        self._safety.setSingleShot(True)
        self._safety.timeout.connect(self._on_safety_timeout)
        self.current_object: str | None = None
        self.answerPage = BasePopup(self, False, True)
        self.answerPage.accepted.connect(self._run_AXIS_MAINTENANCE_gcode)
        self.error_popup = BasePopup(self, False, False)
        # No buttons on a non-dialog popup, so it must hide itself.
        self._error_hide = QtCore.QTimer(self)
        self._error_hide.setSingleShot(True)
        self._error_hide.setInterval(5000)
        self._error_hide.timeout.connect(self.error_popup.hide)

        self._setup_ui()
        self.axes_back_btn.clicked.connect(self.request_back.emit)
        self.am_execute.clicked.connect(self.axis_maintenance)

    def _run_AXIS_MAINTENANCE_gcode(self):
        axis = self.current_object
        if axis:
            self.call_load_panel.emit(
                True, f"Running maintenance cycle on {axis.upper()} axis...", False
            )
            self._send(
                f"AXIS_MAINTENANCE_FINISH_{axis}\nM400",
                self._on_cycle_done,
                _CYCLE_TIMEOUT_MS,
            )

        else:
            self.answerPage.hide()

    def axis_maintenance(self) -> None:
        """Routine, checks axis movement for printer debugging"""
        axis = self.axis_maintenance_gb.checkedButton().text().lower()
        self.current_object = axis

        self.answerPage.set_message(
            f"Apply oil to the {axis.upper()} axis,\nthen press Confirm to spread it.",
        )

        self.call_load_panel.emit(True, f"Homing {axis.upper()} axis...", False)
        self._send(f"AXIS_MAINTENANCE_{axis}\nM400", self._on_homed, _PREP_TIMEOUT_MS)

    def _send(
        self, script: str, on_done: Callable[[object], None], timeout_ms: int
    ) -> None:
        """Run ``script``; ``on_done`` gets the reply, or an error if unsent."""
        self._run_id += 1
        run_id = self._run_id
        # A second run would queue behind the first in Klipper's gcode mutex.
        self.am_execute.setEnabled(False)

        def on_reply(reply: object) -> None:
            if run_id != self._run_id:
                if not self._safety.isActive():  # Klipper finished the timed-out run
                    _logger.info("Axis maintenance: late reply, Execute unlocked")
                    self.am_execute.setEnabled(True)
                return
            self._safety.stop()
            self.am_execute.setEnabled(True)
            error = reply.get("error") if isinstance(reply, dict) else None
            if error is not None:
                _logger.warning(
                    "Axis maintenance: %s failed: %s", script.split("\n", 1)[0], error
                )
                self._report_error(error)
            on_done(reply)

        # Moonraker replies to gcode.script once Klipper has run the whole script,
        # and fails it with an error when the socket closes, so a reply always comes.
        self._safety.start(timeout_ms)
        run = self.gcode_runner
        if run is None:
            _logger.warning("Axis maintenance: no gcode runner wired, not sending")
        if not (run and run(script, callback=on_reply)):
            on_reply({"error": {"code": -1, "message": "not connected"}})

    def _on_safety_timeout(self) -> None:
        """Close the loading screen; Execute stays locked until the late reply."""
        # Klipper still holds the gcode mutex, so a new run would queue and move later.
        self._run_id += 1
        _logger.warning(
            "Axis maintenance: no reply in %d s, closing the loading screen",
            self._safety.interval() // 1000,
        )
        self._hide_overlay()
        self._report_error(
            {"message": "Klipper is still busy.\nExecute unlocks once it finishes."}
        )

    def _hide_overlay(self) -> None:
        # Hidden page: the overlay now belongs to whichever flow moved the user away.
        if self.isVisible():
            self.call_load_panel.emit(False, "", False)

    def _report_error(self, error: object) -> None:
        """Pop up errors nothing else reports (Moonraker-level, not Klipper's "!!")."""
        code = error.get("code") if isinstance(error, dict) else None
        if code in _COVERED_ERROR_CODES or not self.isVisible():
            return
        message = error.get("message") if isinstance(error, dict) else error
        self.error_popup.set_message(f"Axis maintenance failed: {message}")
        self.error_popup.show()
        self._error_hide.start()

    def _on_homed(self, result: object) -> None:
        """Drop the loading screen and show the oil prompt once homing succeeded."""
        # Confirm moves the axis, so never ask from behind another tab.
        if not self.isVisible():
            _logger.info(
                "Axis maintenance: page left during homing, oil prompt skipped"
            )
            return
        self.call_load_panel.emit(False, "", False)
        if isinstance(result, dict) and "error" in result:
            return
        self.answerPage.show()

    def _on_cycle_done(self, _result: object) -> None:
        """Drop the loading screen when the maintenance cycle ends."""
        self._hide_overlay()

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
