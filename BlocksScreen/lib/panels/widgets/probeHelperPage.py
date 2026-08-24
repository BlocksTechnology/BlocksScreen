import enum
import logging
import typing

from lib.panels.widgets.optionCardWidget import OptionCard
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_label import BlocksLabel
from lib.utils.check_button import BlocksCustomCheckButton
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)

_PROBE_MOVE_STEPS: list[tuple[str, float, str, bool]] = [
    ("0.010 mm", 0.010, "move_option_1", True),
    ("0.025 mm", 0.025, "move_option_2", False),
    ("0.100 mm", 0.100, "move_option_3", False),
    ("0.500 mm", 0.500, "move_option_4", False),
    ("1.000 mm", 1.000, "move_option_5", False),
]

_TRACKED_GCODES: frozenset[str] = frozenset(
    {
        "PROBE_CALIBRATE",
        "PROBE_EDDY_CURRENT_CALIBRATE",
        "LDC_CALIBRATE_DRIVE_CURRENT",
        "Z_ENDSTOP_CALIBRATE",
        "MANUAL_PROBE",
        "CLEAN_NOZZLE",
    }
)


class _CalibPhase(enum.Enum):
    IDLE = "idle"
    PROBE_ACTIVE = "probe_active"  # non-eddy: CLEAN_NOZZLE/homing before probe session
    EDDY_PHASE1 = "eddy_phase1"  # LDC drive-current calibration → first SAVE_CONFIG
    EDDY_PHASE1_RESTART = "eddy_phase1_restart"  # post-Phase1 restart, awaiting standby
    EDDY_PHASE2 = "eddy_phase2"  # Z offset calibration → second SAVE_CONFIG
    SAVE_RESTART = "save_restart"  # non-eddy SAVE_CONFIG restart


class ProbeHelper(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )

    query_printer_object: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="query_object"
    )
    subscribe_config: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [
            list,
            "PyQt_PyObject",
        ],
        [
            str,
            "PyQt_PyObject",
        ],
        name="on_subscribe_config",
    )
    request_page_view: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_page_view"
    )
    call_load_panel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, str, bool, name="call-load-panel"
    )
    toggle_conn_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="toggles-conn-panel"
    )

    disable_popups: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="disable-popups"
    )
    lock_ui: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="lock-ui"
    )
    show_notifications: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, int, bool, name="show-notifications"
    )

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.helper_start: bool = False
        self.helper_initialize: bool = False
        self._zhop_height: float = _PROBE_MOVE_STEPS[0][1]
        self.z_offset_method_type: str = ""
        self.z_offset_config_method: tuple = ()
        self.z_offset_calibration_speed: int = 100
        self.z_offsets: tuple = ()
        self._calibration_commands: set = set()
        self.card_options: dict = {}
        self.z_offset_config_type: str = ""
        self._eddy_command: str = ""

        self.setObjectName("probe_offset_page")
        self._setupUi()
        self.inductive_icon = QtGui.QPixmap(
            ":/z_levelling/media/btn_icons/inductive.svg"
        )
        self.bltouch_icon = QtGui.QPixmap(":/z_levelling/media/btn_icons/bltouch.svg")
        self.endstop_icon = QtGui.QPixmap(
            ":/extruder_related/media/btn_icons/switch_zoom.svg"
        )
        self.eddy_icon = QtGui.QPixmap(":/z_levelling/media/btn_icons/eddy_mech.svg")
        self._toggle_tool_buttons(False)
        self.mb_raise_nozzle.clicked.connect(lambda: self.handle_nozzle_move("raise"))
        self.mb_lower_nozzle.clicked.connect(lambda: self.handle_nozzle_move("lower"))
        self.po_back_button.clicked.connect(self.request_back)
        self.accept_button.clicked.connect(self.handle_accept)
        self.abort_button.clicked.connect(self.handle_abort)
        self.block_z = False
        self.block_list = False
        self.target_temp = 0
        self.current_temp = 0
        self._calib_phase = _CalibPhase.IDLE
        self._active_calibration_tool: str = ""

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """Handle print stats object update"""
        if isinstance(value, str) and "state" in field and value == "standby":
            if self._calib_phase in (
                _CalibPhase.EDDY_PHASE1,
                _CalibPhase.EDDY_PHASE1_RESTART,
            ):
                self.call_load_panel.emit(
                    True, "Running Z offset calibration\nMoving to position...", False
                )
                self.run_gcode_signal.emit(self._eddy_command)
                self.request_page_view.emit()
                self.disable_popups.emit(False)
                self.toggle_conn_page.emit(True)
                self._calib_phase = _CalibPhase.IDLE
            elif self._calib_phase in (
                _CalibPhase.EDDY_PHASE2,
                _CalibPhase.SAVE_RESTART,
            ):
                self._calib_phase = _CalibPhase.IDLE
                self.run_gcode_signal.emit("G28")
                self.request_page_view.emit()
                self._restore_ui()

    def on_klippy_status(self, state: str) -> None:
        """Handle Klippy status event change"""
        _state = state.lower()
        if _state == "disconnected":
            if self._calib_phase in (
                _CalibPhase.EDDY_PHASE1,
                _CalibPhase.EDDY_PHASE1_RESTART,
                _CalibPhase.EDDY_PHASE2,
                _CalibPhase.SAVE_RESTART,
            ):
                self.helper_start = False
                self.helper_initialize = False
                match self._calib_phase:
                    case _CalibPhase.EDDY_PHASE2:
                        msg = "Saving calibration data\nRestarting Klipper..."
                    case _CalibPhase.SAVE_RESTART:
                        msg = "Saving configuration\nRestarting Klipper..."
                    case _:
                        msg = "Restarting Klipper..."
                self.call_load_panel.emit(True, msg, False)
            else:
                self._cancel_calibration()
        elif _state == "ready":
            match self._calib_phase:
                case _CalibPhase.EDDY_PHASE1:
                    self._calib_phase = _CalibPhase.EDDY_PHASE1_RESTART
                    self.call_load_panel.emit(
                        True,
                        "Wait for the toolhead to park.\nPlace a sheet of paper under the nozzle."
                        "\nAdjust until it drags slightly.",
                        False,
                    )
                case _CalibPhase.EDDY_PHASE2:
                    self.call_load_panel.emit(
                        True, "Calibration saved\nHoming printer...", False
                    )
                case _CalibPhase.SAVE_RESTART:
                    self.call_load_panel.emit(
                        True, "Configuration saved\nHoming printer...", False
                    )
        elif _state == "shutdown":
            if self._calib_phase != _CalibPhase.IDLE:
                self._cancel_calibration()
        elif _state == "standby":
            self.block_z = False
            self.block_list = False
            for card in list(self.card_options.values()):
                self.main_content_horizontal_layout.removeWidget(card)
                card.setParent(None)
                card.deleteLater()
            self.card_options.clear()

    def handle_nozzle_move(self, direction: str) -> None:
        """Handle move z buttons click"""
        if direction == "raise":
            _gcode = f"TESTZ Z={self._zhop_height}"
        elif direction == "lower":
            _gcode = f"TESTZ Z=-{self._zhop_height}"
        else:
            return

        self.accept_button.show()
        self.abort_button.show()
        self.run_gcode_signal.emit(_gcode)
        self.update()

    def _configure_option_cards(self, probes_list: list[str]) -> None:
        """`Internal use only!` Add option cards to the initial probe
        helper page each card contains a tool probe or switch tool
        that can be calibrated.
            ---

            Args:
                probes (list[str]): Available printer config tools list
        """
        for probe in probes_list:
            if "eddy" in probe.lower():
                _card_text = "Eddy Current Calibration"
                _icon = self.eddy_icon
            elif "probe" in probe.lower():
                _card_text = "Inductive Probe Calibration"
                _icon = self.inductive_icon
            elif "bltouch" in probe.lower():
                _card_text = "BLTouch Calibration"
                _icon = self.bltouch_icon
            else:
                _card_text = "Endstop Calibration"
                _icon = self.endstop_icon

            _card = OptionCard(self, _card_text, probe, _icon)  # type: ignore
            if not hasattr(_card, "continue_clicked"):
                _card.deleteLater()
                continue
            _card.setObjectName(probe)
            self.card_options[probe] = _card
            self.main_content_horizontal_layout.addWidget(
                _card, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
            )
            _card.continue_clicked.connect(self.handle_start_tool)  # type: ignore
        self.update()

    def _hide_option_cards(self) -> None:
        """Hide all probe option cards."""
        for card in self.card_options.values():
            card.hide()

    def _show_option_cards(self) -> None:
        """Show and re-enable all probe option cards."""
        for card in self.card_options.values():
            card.setEnabled(True)
            card.show()

    def _init_probe_config(self) -> None:
        """Initialize internal probe tracking"""
        if not self.z_offset_config_method:
            return
        if self.z_offset_config_type != "endstop":
            self.z_offsets = tuple(
                self.z_offset_config_method[0].get(f"{axis}_offset")
                for axis in ("x", "y", "z")
            )
            self.z_offset_calibration_speed = self.z_offset_config_method[0].get(
                "speed"
            )

    @QtCore.pyqtSlot(list, name="on_object_config")
    @QtCore.pyqtSlot(dict, name="on_object_config")
    def on_object_config(self, config: dict | list) -> None:
        """Executed when a subscribed printer config
        is received

        Args:
            config (dict): Printer object configuration(s)
        """
        if not config:
            return

        if isinstance(config, list):
            if self.block_list:
                return
            self.block_list = True

            _keys = [k for item in config for k in item]

            probe, *_ = config[0].items()
            self.z_offset_method_type = probe[0]  # The one found first
            self.z_offset_config_method = (
                probe[1],
                "PROBE_CALIBRATE",
                "Z_OFFSET_APPLY_PROBE",
            )
            self._init_probe_config()
            if not _keys:
                return
            self._configure_option_cards(_keys)

        elif isinstance(config, dict):
            if _config := config.get("stepper_z"):
                if self.block_z:
                    return
                self.block_z = True

                _virtual_endstop = "probe:z_virtual_endstop"
                if _config.get("endstop_pin") == _virtual_endstop:  # home with probe
                    return
                self.z_offset_config_type = "endstop"
                self.z_offset_config_method = (
                    _config,
                    "Z_ENDSTOP_CALIBRATE",
                    "Z_OFFSET_APPLY_ENDSTOP",
                )
                self._configure_option_cards(["endstop"])

    @QtCore.pyqtSlot(dict, name="on_printer_config")
    def on_printer_config(self, _config: dict) -> None:
        """Handle received printer config"""
        _probe_types = [
            "probe",
            "bltouch",
            "smart_effector",
            "probe_eddy_current",
        ]

        self.subscribe_config[list, "PyQt_PyObject"].emit(
            _probe_types, self.on_object_config
        )
        self.subscribe_config[str, "PyQt_PyObject"].emit(
            "stepper_z", self.on_object_config
        )

    @QtCore.pyqtSlot(dict, name="on_available_gcode_cmds")
    def on_available_gcode_cmds(self, gcode_cmds: dict) -> None:
        """Setup available probe calibration commands"""
        self._calibration_commands = gcode_cmds.keys() & _TRACKED_GCODES

    def _verify_gcode(self, gcode: str) -> bool:
        """Check if the specified gcode exists
        and can be called

        Args:
            gcode (str): Gcode to check the existence

        Returns:
            bool: If the gcode exists
        """
        if not gcode:
            return False
        return gcode in self._calibration_commands

    def _build_calibration_command(self, tool: str) -> str:
        """Return the calibration gcode command for the given tool name, or empty string if unavailable."""
        if not tool:
            return ""
        if tool == "endstop":
            if self._verify_gcode("Z_ENDSTOP_CALIBRATE"):
                return "Z_ENDSTOP_CALIBRATE"
        elif "eddy" in tool:
            parts = tool.split(" ", 1)
            if len(parts) < 2 or not parts[1]:
                return ""
            if self._verify_gcode("LDC_CALIBRATE_DRIVE_CURRENT"):
                return f"LDC_CALIBRATE_DRIVE_CURRENT CHIP={parts[1]}"
        elif "probe" in tool or "bltouch" in tool or "smart_effector" in tool:
            if self._verify_gcode("PROBE_CALIBRATE"):
                if self.z_offset_calibration_speed:
                    return f"PROBE_CALIBRATE SPEED={self.z_offset_calibration_speed}"
                return "PROBE_CALIBRATE"
        return ""

    @QtCore.pyqtSlot(float, name="handle_zhopHeight_change")
    def handle_zhopHeight_change(self, new_value: float) -> None:
        """Handle move_option_**x** toggled buttons,
        changes the z movement value that will be used
        for raising or lowering the toolhead during
        calibration.
        Receives the value from the toggle button and
        makes the internal instance variable `_zhop_height`
        to the value of the button.

        Args:
            new_value (float): zhop Value obtained from the toggled button
        """
        if new_value == self._zhop_height:
            return
        self._zhop_height = new_value

    @QtCore.pyqtSlot("PyQt_PyObject", name="handle_start_tool")
    def handle_start_tool(self, sender: OptionCard) -> None:
        """Handle probe tool helper start by sending
        the correct gcode command according to the
        clicked option card. This is achieved by
        receiving the sender (the OptionCard) that was
        clicked inside this slot.
        The correct command to send is  verified by
        checking the instance variable `name` from the
        sender.

        Args:
            sender (OptionCard): The clicked OptionCard instance
        """
        if not sender:
            return

        _name: str = sender.name  # type: ignore
        _cmd = self._build_calibration_command(_name)
        if not _cmd:
            return

        self._active_calibration_tool = _name
        for i in self.card_options.values():
            i.setDisabled(True)
        self.helper_initialize = True
        QtCore.QTimer.singleShot(
            300, lambda: self.query_printer_object.emit({"manual_probe": None})
        )
        self.disable_popups.emit(True)
        self.lock_ui.emit(True)
        _clean_nozzle = self._verify_gcode("CLEAN_NOZZLE")
        if "eddy" in _name:
            _name_parts = _name.split(" ", 1)
            if len(_name_parts) < 2:
                return
            if _clean_nozzle:
                self.call_load_panel.emit(
                    True, "Cleaning nozzle...\nPlease wait", False
                )
                self.run_gcode_signal.emit("CLEAN_NOZZLE")
            else:
                self.call_load_panel.emit(
                    True, "Calibrating drive current\nHoming axes...", False
                )
            self.toggle_conn_page.emit(False)
            self.run_gcode_signal.emit(_cmd)
            self._eddy_command = f"PROBE_EDDY_CURRENT_CALIBRATE CHIP={_name_parts[1]}"
            self._calib_phase = _CalibPhase.EDDY_PHASE1
            return
        if _clean_nozzle and _cmd != "Z_ENDSTOP_CALIBRATE":
            self.call_load_panel.emit(True, "Cleaning nozzle...\nPlease wait", False)
            self.run_gcode_signal.emit("CLEAN_NOZZLE")
        else:
            self.call_load_panel.emit(
                True, "Starting calibration\nHoming axes...", False
            )
        self._calib_phase = _CalibPhase.PROBE_ACTIVE
        self.run_gcode_signal.emit(_cmd)

    @QtCore.pyqtSlot(str, str, float, name="on_extruder_update")
    def on_extruder_update(
        self, _extruder_name: str, field: str, new_value: float
    ) -> None:
        """Handle extruder update"""
        if self._calib_phase == _CalibPhase.IDLE:
            return
        if field == "target":
            prev_temp = self.target_temp
            self.target_temp = round(new_value, 0)
            if self.isVisible():
                if self.target_temp > 0:
                    self.call_load_panel.emit(
                        True, "Heating nozzle\nCleaning before calibration...", False
                    )
                elif prev_temp > 0:
                    # Heater turned off - brushing is starting
                    self.call_load_panel.emit(
                        True, "Cleaning nozzle...\nPlease wait", False
                    )
            return
        if self.target_temp != 0:
            if self.current_temp == self.target_temp:
                if self.isVisible():
                    self.call_load_panel.emit(
                        True, "Nozzle at temperature\nCleaning nozzle...", False
                    )
                return
            if field == "temperature":
                self.current_temp = round(new_value, 0)
                if self.isVisible():
                    self.call_load_panel.emit(
                        True,
                        f"Heating nozzle ({new_value}/{self.target_temp}°C)\nPlease wait...",
                        False,
                    )

    @QtCore.pyqtSlot(name="handle_accept")
    def handle_accept(self) -> None:
        """Accepts the configured value from the calibration"""
        if not self.helper_start:
            return
        self.helper_start = False
        self._toggle_tool_buttons(False)
        if "eddy" in self.z_offset_method_type.lower():
            self._calib_phase = _CalibPhase.EDDY_PHASE2
            self.call_load_panel.emit(
                True,
                "Finalising Eddy calibration...\nThis may take a few minutes",
                False,
            )
        else:
            self._show_option_cards()
            self._calib_phase = _CalibPhase.SAVE_RESTART
            self.call_load_panel.emit(
                True,
                "Saving configuration...\nMachine will restart",
                False,
            )
        self.toggle_conn_page.emit(False)
        self.run_gcode_signal.emit("ACCEPT")
        self.run_gcode_signal.emit("SAVE_CONFIG")

    @QtCore.pyqtSlot(name="handle_abort")
    def handle_abort(self) -> None:
        """Aborts the calibration procedure"""
        if not self.helper_start:
            return
        self._cancel_calibration()
        self.run_gcode_signal.emit("ABORT")

    @QtCore.pyqtSlot(str, list, name="on_gcode_move_update")
    def on_gcode_move_update(self, _name: str, _value: list) -> None:
        """Update loading message once homing completes after nozzle cleaning."""
        if (
            self._calib_phase
            not in (
                _CalibPhase.EDDY_PHASE1,
                _CalibPhase.PROBE_ACTIVE,
            )
            or self.target_temp != 0
        ):
            return
        if _name == "homing_origin" and self.isVisible():
            if self._calib_phase == _CalibPhase.EDDY_PHASE1:
                self.call_load_panel.emit(
                    True, "Calibrating drive current\nPlease wait...", False
                )
            else:
                self.call_load_panel.emit(
                    True, "Moving to calibration position\nPlease wait...", False
                )

    @QtCore.pyqtSlot(dict, name="on_manual_probe_update")
    def on_manual_probe_update(self, update: dict) -> None:
        """Handle manual probe update"""
        if not update:
            return

        is_active = update.get("is_active")
        if (z_upper := update.get("z_position_upper")) is not None:
            self.old_offset_info.setText(f"{round(z_upper, 3) or 0.0:.3f} mm")
        if (z_pos := update.get("z_position")) is not None:
            self.current_offset_info.setText(f"{round(z_pos, 3) or 0.0:.3f} mm")

        if is_active is None:
            return
        if not self.isVisible():
            self.request_page_view.emit()
        # Shared state updates
        self.helper_initialize = False
        _was_active = self.helper_start
        self.helper_start = is_active
        if is_active and self._calib_phase == _CalibPhase.PROBE_ACTIVE:
            # Probe session started - CLEAN_NOZZLE/homing phase is over.
            self._calib_phase = _CalibPhase.IDLE
        elif not is_active and _was_active:
            # A manual probe session ended (external abort or normal completion).
            self._calib_phase = _CalibPhase.IDLE
        # UI updates
        self._toggle_tool_buttons(is_active)
        if is_active:
            self._hide_option_cards()
        elif self._calib_phase == _CalibPhase.IDLE:
            self._show_option_cards()

    @QtCore.pyqtSlot(list, name="handle_gcode_response")
    def handle_gcode_response(self, data: list) -> None:
        """Parses responses from gcodes

        Args:
            data (list): A list containing the gcode that originated
                    the response and the response
        """
        if not data:
            return
        if self.isVisible():
            if data[0].startswith("!!"):  # An error occurred
                if (
                    "already in a manual z probe"
                    in data[0].removeprefix("!!").strip().lower()
                ):
                    self._hide_option_cards()
                    self.helper_start = True
                    self._toggle_tool_buttons(True)
                    return
                self._show_option_cards()
                self.helper_start = False
                self._toggle_tool_buttons(False)
                error_msg = data[0].removeprefix("!! ")
                self.show_notifications.emit("probe_helper", error_msg, 3, True)

    @QtCore.pyqtSlot(list, name="handle_error_response")
    def handle_error_response(self, data: list) -> None:
        """Handle received error response"""
        if not data:
            return
        raw = data[0]
        if isinstance(raw, dict):
            error_msg = raw.get("message", "Unknown error")
        else:
            error_msg = str(raw)
        # Eddy phase 1 and phase 2 both end with SAVE_CONFIG which restarts Klipper.
        if (
            not self.helper_start
            and self._calib_phase != _CalibPhase.IDLE
            and (self._calib_phase != _CalibPhase.EDDY_PHASE1 or self._eddy_command)
        ):
            logger.debug(
                "Suppressing error during eddy phase-1 SAVE_CONFIG restart: %s",
                error_msg,
            )
            return
        # Not calibrating - mainWindow already handles the notification.
        if not self.helper_start and self._calib_phase == _CalibPhase.IDLE:
            return
        logger.error("Error Response: %s", error_msg)
        self._cancel_calibration()
        self.show_notifications.emit("probe_helper", error_msg, 3, True)

    def _reset_calibration_state(self) -> None:
        """Reset all calibration state and temp tracking to idle."""
        self.helper_start = False
        self.helper_initialize = False
        self._calib_phase = _CalibPhase.IDLE
        self._eddy_command = ""
        self._active_calibration_tool = ""
        self.target_temp = 0
        self.current_temp = 0

    def _restore_ui(self) -> None:
        """Dismiss loading overlay and re-enable navigation."""
        self._show_option_cards()
        self.call_load_panel.emit(False, "", False)
        self.disable_popups.emit(False)
        self.lock_ui.emit(False)
        self.toggle_conn_page.emit(True)

    def _cancel_calibration(self) -> None:
        """Full reset: clear state, hide tool buttons, restore UI."""
        self._reset_calibration_state()
        self._toggle_tool_buttons(False)
        self._restore_ui()

    def _toggle_tool_buttons(self, state: bool) -> None:
        """Show/hide and enable/disable calibration tool buttons based on active state."""
        self.mb_lower_nozzle.setEnabled(state)
        self.mb_raise_nozzle.setEnabled(state)
        self.accept_button.setEnabled(state)
        self.abort_button.setEnabled(state)
        self.accept_button.hide()
        self.abort_button.hide()
        if state:
            for i in self.card_options.values():
                i.setDisabled(False)
            self.lock_ui.emit(True)
            self.call_load_panel.emit(False, "", False)
            self.po_back_button.setEnabled(False)
            self.po_back_button.hide()
            self.po_header_title.setEnabled(False)
            self.po_header_title.hide()
            self.separator_line.hide()
            self.old_offset_info.show()
            self.bbp_offset_steps_buttons_group_box.show()
            self.current_offset_info.show()
            self.abort_button.show()
            self.tool_image.show()
            self.mb_raise_nozzle.show()
            self.mb_lower_nozzle.show()
            self.frame_2.show()
            self.spacerItem.changeSize(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )

        else:
            self.po_back_button.setEnabled(True)
            self.po_back_button.show()
            self.po_header_title.setEnabled(False)
            self.po_header_title.show()
            self.separator_line.show()
            self.bbp_offset_steps_buttons_group_box.hide()
            self.old_offset_info.setText("0.000 mm")
            self.old_offset_info.hide()
            self.current_offset_info.setText("0.000 mm")
            self.current_offset_info.hide()
            self.tool_image.hide()
            self.mb_raise_nozzle.hide()
            self.mb_lower_nozzle.hide()
            self.frame_2.hide()
            self.spacerItem.changeSize(
                0,
                0,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )

        self.update()

    def _create_move_button(
        self,
        parent: QtWidgets.QWidget,
        label: str,
        obj_name: str,
        checked: bool,
        font: QtGui.QFont,
    ) -> BlocksCustomCheckButton:
        """Create a single move-step check button."""
        btn = BlocksCustomCheckButton(parent=parent)
        btn.setMinimumSize(QtCore.QSize(100, 60))
        btn.setMaximumSize(QtCore.QSize(100, 60))
        btn.setText(label)
        btn.setFont(font)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setFlat(True)
        btn.setProperty("button_type", "")
        btn.setObjectName(obj_name)
        return btn

    def _setupUi(self) -> None:
        """Build and lay out all UI elements for the probe helper page."""
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
        self.po_header_title = QtWidgets.QLabel(parent=self)
        sizePolicy.setHeightForWidth(
            self.po_header_title.sizePolicy().hasHeightForWidth()
        )
        self.po_header_title.setSizePolicy(sizePolicy)
        self.po_header_title.setMinimumSize(QtCore.QSize(400, 60))
        self.po_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.po_header_title.setFont(font)
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
        self.po_header_title.setAutoFillBackground(True)
        self.po_header_title.setBackgroundRole(palette.ColorRole.Window)
        self.po_header_title.setPalette(palette)
        self.po_header_title.setText("Z Probe Offset Calibrate")
        self.po_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.po_header_title.setObjectName("po_header_title")

        self.accept_button = BlocksCustomButton(self)
        self.accept_button.setGeometry(QtCore.QRect(480, 340, 170, 60))
        self.accept_button.setText("Accept")
        self.accept_button.setObjectName("accept_button")
        self.accept_button.setPixmap(QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg"))
        self.accept_button.setVisible(False)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.accept_button.setFont(font)

        self.abort_button = BlocksCustomButton(self)
        self.abort_button.setGeometry(QtCore.QRect(300, 340, 170, 60))
        self.abort_button.setText("Abort")
        self.abort_button.setObjectName("abort_button")
        self.abort_button.setPixmap(QtGui.QPixmap(":/dialog/media/btn_icons/no.svg"))
        self.abort_button.setVisible(False)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.abort_button.setFont(font)

        spacerItem = QtWidgets.QSpacerItem(
            60,
            0,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.bbp_header_layout.addItem(spacerItem)

        self.bbp_header_layout.addWidget(
            self.po_header_title,
            0,
            QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        self.po_back_button = IconButton(parent=self)
        sizePolicy.setHeightForWidth(
            self.po_back_button.sizePolicy().hasHeightForWidth()
        )
        self.po_back_button.setSizePolicy(sizePolicy)
        self.po_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.po_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.po_back_button.setText("")
        self.po_back_button.setFlat(True)
        self.po_back_button.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.po_back_button.setObjectName("po_back_button")

        self.bbp_header_layout.addWidget(
            self.po_back_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.bbp_header_layout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.bbp_header_layout)

        self.main_content_horizontal_layout = QtWidgets.QHBoxLayout()
        self.main_content_horizontal_layout.setObjectName(
            "main_content_horizontal_layout"
        )

        self.separator_line = QtWidgets.QFrame(parent=self)
        self.separator_line.setMaximumHeight(2)
        self.separator_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.separator_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.separator_line.setObjectName("separator_line")
        self.verticalLayout.addWidget(self.separator_line)

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

        move_font = QtGui.QFont()
        move_font.setPointSize(14)
        center = (
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        for label, value, obj_name, checked in _PROBE_MOVE_STEPS:
            btn = self._create_move_button(
                self.bbp_offset_steps_buttons_group_box,
                label,
                obj_name,
                checked,
                move_font,
            )
            btn.toggled.connect(
                lambda checked_state, v=value: (
                    checked_state and self.handle_zhopHeight_change(new_value=v)
                )
            )
            setattr(self, obj_name, btn)
            self.bbp_offset_value_selector_group.addButton(btn)
            self.bbp_offset_steps_buttons.addWidget(btn, 0, center)

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
        self.tool_image = QtWidgets.QLabel(parent=self.frame_2)
        self.tool_image.setGeometry(QtCore.QRect(0, 30, 371, 121))
        self.tool_image.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.tool_image.setPixmap(
            QtGui.QPixmap(":/graphics/media/graphics/babystep_graphic.png")
        )
        self.tool_image.setScaledContents(False)
        self.tool_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tool_image.setObjectName("tool_image")

        # === NEW LABEL ADDED HERE ===
        # This is the title label that appears above the red value box.
        self.old_offset_info = QtWidgets.QLabel(parent=self.frame_2)
        # Position it just above the red box. Red box is at y=70, so y=40 is appropriate.
        self.old_offset_info.setGeometry(QtCore.QRect(240, 95, 200, 60))
        font = QtGui.QFont()
        font.setPointSize(12)

        self.old_offset_info.setFont(font)
        # Set color to white to be visible on the dark background
        self.old_offset_info.setStyleSheet("color: gray; background: transparent;")
        self.old_offset_info.setObjectName("old_offset_info")
        self.old_offset_info.setText("0 mm")

        # === END OF NEW LABEL ===

        self.current_offset_info = BlocksLabel(parent=self.frame_2)
        self.current_offset_info.setGeometry(QtCore.QRect(100, 70, 200, 60))
        sizePolicy.setHeightForWidth(
            self.current_offset_info.sizePolicy().hasHeightForWidth()
        )
        self.current_offset_info.setSizePolicy(sizePolicy)
        self.current_offset_info.setMinimumSize(QtCore.QSize(150, 60))
        self.current_offset_info.setMaximumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.current_offset_info.setFont(font)
        self.current_offset_info.setStyleSheet("background: transparent; color: white;")
        self.current_offset_info.setText("Z:0.000mm")
        self.current_offset_info.setPixmap(
            QtGui.QPixmap(":/graphics/media/btn_icons/z_offset_adjust.svg")
        )
        self.current_offset_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.current_offset_info.setObjectName("current_offset_info")
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
        self.mb_lower_nozzle = IconButton(parent=self)
        sizePolicy.setHeightForWidth(
            self.mb_lower_nozzle.sizePolicy().hasHeightForWidth()
        )
        self.mb_lower_nozzle.setSizePolicy(sizePolicy)
        self.mb_lower_nozzle.setMinimumSize(QtCore.QSize(80, 80))
        self.mb_lower_nozzle.setMaximumSize(QtCore.QSize(80, 80))
        self.mb_lower_nozzle.setText("")
        self.mb_lower_nozzle.setFlat(True)
        self.mb_lower_nozzle.setPixmap(
            QtGui.QPixmap(":/baby_step/media/btn_icons/move_nozzle_close.svg")
        )
        self.mb_lower_nozzle.setObjectName("bbp_away_from_bed")
        self.bbp_option_button_group = QtWidgets.QButtonGroup(self)
        self.bbp_option_button_group.setObjectName("bbp_option_button_group")
        self.bbp_option_button_group.addButton(self.mb_lower_nozzle)
        self.bbp_buttons_layout.addWidget(
            self.mb_lower_nozzle, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.mb_raise_nozzle = IconButton(parent=self)
        sizePolicy.setHeightForWidth(
            self.mb_raise_nozzle.sizePolicy().hasHeightForWidth()
        )
        self.mb_raise_nozzle.setSizePolicy(sizePolicy)
        self.mb_raise_nozzle.setMinimumSize(QtCore.QSize(80, 80))
        self.mb_raise_nozzle.setMaximumSize(QtCore.QSize(80, 80))
        self.mb_raise_nozzle.setText("")
        self.mb_raise_nozzle.setFlat(True)
        self.mb_raise_nozzle.setPixmap(
            QtGui.QPixmap(":/baby_step/media/btn_icons/move_nozzle_away.svg")
        )
        self.mb_raise_nozzle.setObjectName("bbp_close_to_bed")
        self.bbp_option_button_group.addButton(self.mb_raise_nozzle)
        self.bbp_buttons_layout.addWidget(
            self.mb_raise_nozzle, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        # Add move buttons layout LAST for right placement
        self.main_content_horizontal_layout.addLayout(self.bbp_buttons_layout)

        self.main_content_horizontal_layout.addItem(self.spacerItem)

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
