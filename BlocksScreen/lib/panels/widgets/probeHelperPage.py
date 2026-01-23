import typing
from lib.panels.widgets.optionCardWidget import OptionCard
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_label import BlocksLabel
from lib.utils.check_button import BlocksCustomCheckButton
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


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
    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")

    distances = ["0.01", ".025", "0.1", "0.5", "1"]
    _calibration_commands: list = []
    helper_start: bool = False
    helper_initialize: bool = False
    _zhop_height: float = float(distances[4])
    card_options: dict = {}
    z_offset_method_type: str = ""
    z_offset_config_method: tuple = ()
    z_offset_calibration_speed: int = 100

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

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
        self._setup_move_option_buttons()
        self.move_option_1.toggled.connect(
            lambda: self.handle_zhopHeight_change(new_value=float(self.distances[0]))
        )
        self.move_option_2.toggled.connect(
            lambda: self.handle_zhopHeight_change(new_value=float(self.distances[1]))
        )
        self.move_option_3.toggled.connect(
            lambda: self.handle_zhopHeight_change(new_value=float(self.distances[2]))
        )
        self.move_option_4.toggled.connect(
            lambda: self.handle_zhopHeight_change(new_value=float(self.distances[3]))
        )
        self.move_option_5.toggled.connect(
            lambda: self.handle_zhopHeight_change(new_value=float(self.distances[4]))
        )
        self.mb_raise_nozzle.clicked.connect(lambda: self.handle_nozzle_move("raise"))
        self.mb_lower_nozzle.clicked.connect(lambda: self.handle_nozzle_move("lower"))
        self.po_back_button.clicked.connect(self.request_back)
        self.accept_button.clicked.connect(self.handle_accept)
        self.abort_button.clicked.connect(self.handle_abort)
        self.update()
        self.block_z = False
        self.block_list = False

    def on_klippy_status(self, state: str):
        """Handle Klippy status event change"""
        if state.lower() == "standby":
            self.block_z = False
            self.block_list = False
            # Safely remove all items (widgets, spacers, sub-layouts) from the layout.
            layout = self.main_content_horizontal_layout
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    if item is None:
                        continue
                    widget = item.widget()
                    if widget is not None:
                        # Remove widget from layout and schedule for deletion
                        widget.setParent(None)
                        widget.deleteLater()
                        continue
                    child_layout = item.layout()
                    if child_layout is not None:
                        # Clear child layouts recursively
                        while child_layout.count():
                            child_item = child_layout.takeAt(0)
                            if child_item is None:
                                continue
                            child_widget = child_item.widget()
                            if child_widget is not None:
                                child_widget.setParent(None)
                                child_widget.deleteLater()

    def handle_nozzle_move(self, direction: str):
        """Handle move z buttons click"""
        if direction == "raise":
            self._pending_gcode = f"TESTZ Z={self._zhop_height}"
        elif direction == "lower":
            self._pending_gcode = f"TESTZ Z=-{self._zhop_height}"

        self.accept_button.show()
        self.abort_button.show()
        self.run_gcode_signal.emit(self._pending_gcode)
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

            _card = OptionCard(self, _card_text, str(probe), _icon)  # type: ignore
            _card.setObjectName(str(probe))
            self.card_options.update({str(probe): _card})
            self.main_content_horizontal_layout.addWidget(
                _card, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
            )
            if not hasattr(self.card_options.get(probe), "continue_clicked"):
                del _card
                self.card_options.pop(probe)
                return

            self.card_options.get(probe).continue_clicked.connect(  # type: ignore
                self.handle_start_tool
            )
            self.update()

    def _hide_option_cards(self) -> None:
        list(map(lambda x: x[1].hide(), self.card_options.items()))

    def _show_option_cards(self) -> None:
        list(map(lambda x: x[1].show(), self.card_options.items()))

    def _init_probe_config(self) -> None:
        """Initialize internal probe tracking"""
        if not self.z_offset_config_method:
            return
        if self.z_offset_config_type != "endstop":
            self.z_offsets = tuple(
                map(
                    lambda axis: self.z_offset_config_method[1].get(f"{axis}_offset"),
                    ["x", "y", "z"],
                )
            )
            self.z_offset_calibration_speed = self.z_offset_config_method[1].get(
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

        # BUG: If i don't add if not self.probe_config i'll just receive the configuration a bunch of times
        if isinstance(config, list):
            ...
        # if self.block_list:
        #     return
        # else:
        #     self.block_list = True

        # _keys = []
        # if not isinstance(config, list):
        #     return

        # list(map(lambda item: _keys.extend(item.keys()), config))

        # probe, *_ = config[0].items()
        # self.z_offset_method_type = probe[0]  # The one found first
        # self.z_offset_method_config = (
        #     probe[1],
        #     "PROBE_CALIBRATE",
        #     "Z_OFFSET_APPLY_PROBE",
        # )
        # self.init_probe_config()
        # if not _keys:
        #     return
        # self._configure_option_cards(_keys)

        elif isinstance(config, dict):
            if config.get("stepper_z"):
                if self.block_z:
                    return
                else:
                    self.block_z = True

                _virtual_endstop = "probe:z_virtual_endstop"
                _config = config.get("stepper_z")
                if not _config:
                    return
                if _config.get("endstop_pin") == _virtual_endstop:  # home with probe
                    return
                self.z_offset_config_type = "endstop"
                self.z_offset_config_method = (
                    _config,
                    "Z_ENDSTOP_CALIBRATE",
                    "Z_OFFSET_APPLY_ENDSTOP",
                )
                self._configure_option_cards(["endstop"])

            if config.get("safe_z_home"):
                _config = config.get("safe_z_home")
                if not _config:
                    return
                if _config.get("home_xy_position"):
                    if not _config.get("home_xy_position"):
                        return
                    self.z_offset_safe_xy = tuple(
                        map(
                            lambda value: float(value),
                            _config.get("home_xy_position").split(","),
                        )
                    )
                return
            if config.get("bed_mesh"):
                # TODO: This configuration needs to be prioritized over the safe_z_home
                # If available always use the zero reference xy
                # position for the probe calibration
                _config = config.get("bed_mesh")
                if not _config:
                    return
                if not _config.get("zero_reference_position"):
                    return
                self.z_offset_safe_xy = tuple(
                    map(
                        lambda value: float(value),
                        _config.get("zero_reference_position").split(","),
                    )
                )
                return

    @QtCore.pyqtSlot(dict, name="on_printer_config")
    def on_printer_config(self, config: dict) -> None:
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
            str("stepper_z"), self.on_object_config
        )
        self.subscribe_config[str, "PyQt_PyObject"].emit(
            str("safe_z_home"), self.on_object_config
        )
        self.subscribe_config[str, "PyQt_PyObject"].emit(
            str("bed_mesh"), self.on_object_config
        )

    @QtCore.pyqtSlot(dict, name="on_available_gcode_cmds")
    def on_available_gcode_cmds(self, gcode_cmds: dict) -> None:
        """Setup available probe calibration commands"""
        _available_commands = gcode_cmds.keys()
        if "PROBE_CALIBRATE" in _available_commands:
            self._calibration_commands.append("PROBE_CALIBRATE")
        if "PROBE_EDDY_CURRENT_CALIBRATE" in _available_commands:
            self._calibration_commands.append("PROBE_EDDY_CURRENT_CALIBRATE")
        if "LDC_CALIBRATE_DRIVE_CURRENT" in _available_commands:
            self._calibration_commands.append("LDC_CALIBRATE_DRIVE_CURRENT")
        if "Z_ENDSTOP_CALIBRATE" in _available_commands:
            self._calibration_commands.append("Z_ENDSTOP_CALIBRATE")
        if "MANUAL_PROBE" in _available_commands:
            self._calibration_commands.append("MANUAL_PROBE")

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
        if not tool:
            return ""
        if tool == "endstop":
            if self._verify_gcode("Z_ENDSTOP_CALIBRATE"):
                return "Z_ENDSTOP_CALIBRATE"
        elif "eddy" in tool:
            if self._verify_gcode("PROBE_EDDY_CURRENT_CALIBRATE"):
                _name = tool.split(" ")[1]
                # if not _name:
                #     return ""
                # return (
                #     f"PROBE_EDDY_CURRENT_CALIBRATE CHIP={tool.split(' ')[1]}"
                # )
                return (
                    f"PROBE_EDDY_CURRENT_CALIBRATE CHIP={tool.split(' ')[1]}"
                    * bool(_name)
                ) + ("" * ~bool(_name))

        elif "probe" in tool or "bltouch" in tool:
            if self._verify_gcode("PROBE_CALIBRATE"):
                return "PROBE_CALIBRATE" + (
                    str(" ") + f"SPEED={self.z_offset_calibration_speed}"
                ) * bool(self.z_offset_calibration_speed)
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
    def handle_start_tool(self, sender: typing.Type[OptionCard]) -> None:
        """Handle probe tool helper start by sending
        the correct gcode command according to the
        clicked option card. This is achieved by
        receiving the sender (the OptionCard) that was
        clicked inside this slot.
        The correct command to send is  verified by
        checking the instance variable `name` from the
        sender.

        Args:
            sender (typing.Type[OptionCard]): The clicked OptionCard object
        """
        if not sender:
            return

        for i in self.card_options.values():
            i.setDisabled(True)

        self.call_load_panel.emit(True, "Homing Axes...")
        if self.z_offset_safe_xy:
            self.run_gcode_signal.emit("G28\nM400")
            self._move_to_pos(self.z_offset_safe_xy[0], self.z_offset_safe_xy[1], 100)
        self.helper_initialize = True
        _timer = QtCore.QTimer()
        _timer.setSingleShot(True)
        _timer.timeout.connect(
            lambda: self.query_printer_object.emit({"manual_probe": None})
        )
        _timer.start(int(300))
        # self.query_printer_object.emit({"manual_probe": None})
        _cmd = self._build_calibration_command(sender.name)  # type:ignore
        if not _cmd:
            return
        self.run_gcode_signal.emit(_cmd)

    @QtCore.pyqtSlot(name="handle_accept")
    def handle_accept(self) -> None:
        """Accepts the configured value from the calibration"""
        if not self.helper_start:
            return
        self.helper_start = False
        self._toggle_tool_buttons(False)
        self._show_option_cards()
        self.run_gcode_signal.emit(self.z_offset_config_method[2])
        self.run_gcode_signal.emit("M400")
        self.run_gcode_signal.emit(
            "SAVE_CONFIG"
        )  # Immediately save the new value and restart the host

    @QtCore.pyqtSlot(name="handle_abort")
    def handle_abort(self) -> None:
        """Aborts the calibration procedure"""
        if not self.helper_start:
            return
        self.helper_start = False
        self._toggle_tool_buttons(False)
        self._show_option_cards()
        self.run_gcode_signal.emit("ABORT")

    @QtCore.pyqtSlot(str, list, name="on_gcode_move_update")
    def on_gcode_move_update(self, name: str, value: list) -> None:
        """Handle gcode move update"""
        if not value:
            return

        _fields = [
            "absolute_coordinates",
            "absolute_extrude",
            "homing_origin",
            "position",
            "gcode_position",
        ]
        ...

    @QtCore.pyqtSlot(dict, name="on_manual_probe_update")
    def on_manual_probe_update(self, update: dict) -> None:
        """Handle manual probe update"""
        if not update:
            return

        # if update.get("z_position_lower"):
        # f"{update.get('z_position_lower'):.4f} mm"
        if update.get("is_active"):
            if not self.isVisible():
                self.request_page_view.emit()

            self.helper_initialize = False
            self.helper_start = True
            self._hide_option_cards()
            self._toggle_tool_buttons(True)

        if update.get("z_position_upper"):
            self.old_offset_info.setText(f"{update.get('z_position_upper'):.4f} mm")
        if update.get("z_position"):
            self.current_offset_info.setText(f"{update.get('z_position'):.4f} mm")

    @QtCore.pyqtSlot(list, name="handle_gcode_response")
    def handle_gcode_response(self, data: list) -> None:
        """Parses responses from gcodes

        Args:
            data (list): A list containing the gcode that originated
                    the response and the response
        """
        if self.isVisible():
            if data[0].startswith("!!"):  # An error occurred
                if "already in a manual z probe" in data[0].strip("!! ").lower():
                    self._hide_option_cards()
                    self.helper_start = True
                    self._toggle_tool_buttons(True)
                    return
                self._show_option_cards()
                self.helper_start = False
                self._toggle_tool_buttons(False)

            # elif data[0].startswith("// "): ...

    @QtCore.pyqtSlot(list, name="handle_error_response")
    def handle_error_response(self, data: list) -> None:
        """Handle received error response"""
        ...
        # _data, _metadata, *extra = data + [None] * max(0, 2 - len(data))

    def _move_to_pos(self, x, y, speed) -> None:
        self.run_gcode_signal.emit(f"G91\nG1 Z5 F{10 * 60}\nM400")
        self.run_gcode_signal.emit(f"G90\nG1 X{x} Y{y} F{speed * 60}\nM400")
        return

    def _setup_move_option_buttons(self) -> None:
        """Change move_option_x buttons text for configured
        zhop values in stored in the class variable `distances`

        `distances` Has the values from lowest to maximum zhop
        """
        if self.distances:
            return
        self.move_option_1.setText(str(self.distances[0]))
        self.move_option_2.setText(str(self.distances[1]))
        self.move_option_3.setText(str(self.distances[2]))
        self.move_option_4.setText(str(self.distances[3]))
        self.move_option_5.setText(str(self.distances[4]))

    def _toggle_tool_buttons(self, state: bool) -> None:
        self.mb_lower_nozzle.setEnabled(state)
        self.mb_raise_nozzle.setEnabled(state)
        self.accept_button.setEnabled(state)
        self.abort_button.setEnabled(state)
        self.accept_button.hide()
        self.abort_button.hide()
        if state:
            for i in self.card_options.values():
                i.setDisabled(False)
            self.call_load_panel.emit(False, "")
            self.po_back_button.setEnabled(False)
            self.po_back_button.hide()
            self.po_header_title.setEnabled(False)
            self.po_header_title.hide()
            self.separator_line.hide()
            self.old_offset_info.show()
            self.bbp_offset_steps_buttons_group_box.show()
            self.current_offset_info.show()
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
            self.old_offset_info.hide()
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
        return

    def _setupUi(self) -> None:
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
        self.abort_button.setObjectName("accept_button")
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

        # 0.1mm button
        self.move_option_1 = BlocksCustomCheckButton(
            parent=self.bbp_offset_steps_buttons_group_box
        )
        self.move_option_1.setMinimumSize(QtCore.QSize(100, 60))
        self.move_option_1.setMaximumSize(QtCore.QSize(100, 60))
        self.move_option_1.setText("0.01 mm")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.move_option_1.setFont(font)
        self.move_option_1.setCheckable(True)
        self.move_option_1.setChecked(True)  # Set as initially checked
        self.move_option_1.setFlat(True)
        self.move_option_1.setProperty("button_type", "")
        self.move_option_1.setObjectName("move_option_1")
        self.bbp_offset_value_selector_group.addButton(self.move_option_1)
        self.bbp_offset_steps_buttons.addWidget(
            self.move_option_1,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # 0.01mm button
        self.move_option_2 = BlocksCustomCheckButton(
            parent=self.bbp_offset_steps_buttons_group_box
        )
        self.move_option_2.setMinimumSize(QtCore.QSize(100, 60))
        self.move_option_2.setMaximumSize(
            QtCore.QSize(100, 60)
        )  # Increased max width by 5 pixels
        self.move_option_2.setText("0.25 mm")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.move_option_2.setFont(font)
        self.move_option_2.setCheckable(True)
        self.move_option_2.setFlat(True)
        self.move_option_2.setProperty("button_type", "")
        self.move_option_2.setObjectName("move_option_2")
        self.bbp_offset_value_selector_group.addButton(self.move_option_2)
        self.bbp_offset_steps_buttons.addWidget(
            self.move_option_2,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # 0.05mm button
        self.move_option_3 = BlocksCustomCheckButton(
            parent=self.bbp_offset_steps_buttons_group_box
        )
        self.move_option_3.setMinimumSize(QtCore.QSize(100, 60))
        self.move_option_3.setMaximumSize(
            QtCore.QSize(100, 60)
        )  # Increased max width by 5 pixels
        self.move_option_3.setText("0.1 mm")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.move_option_3.setFont(font)
        self.move_option_3.setCheckable(True)
        self.move_option_3.setFlat(True)
        self.move_option_3.setProperty("button_type", "")
        self.move_option_3.setObjectName("move_option_3")
        self.bbp_offset_value_selector_group.addButton(self.move_option_3)
        self.bbp_offset_steps_buttons.addWidget(
            self.move_option_3,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # 0.025mm button
        self.move_option_4 = BlocksCustomCheckButton(
            parent=self.bbp_offset_steps_buttons_group_box
        )
        self.move_option_4.setMinimumSize(QtCore.QSize(100, 60))
        self.move_option_4.setMaximumSize(
            QtCore.QSize(100, 60)
        )  # Increased max width by 5 pixels
        self.move_option_4.setText("0.5 mm")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.move_option_4.setFont(font)
        self.move_option_4.setCheckable(True)
        self.move_option_4.setFlat(True)
        self.move_option_4.setProperty("button_type", "")
        self.move_option_4.setObjectName("move_option_4")
        self.bbp_offset_value_selector_group.addButton(self.move_option_4)
        self.bbp_offset_steps_buttons.addWidget(
            self.move_option_4,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # 0.01mm button
        self.move_option_5 = BlocksCustomCheckButton(
            parent=self.bbp_offset_steps_buttons_group_box
        )
        self.move_option_5.setMinimumSize(QtCore.QSize(100, 60))
        self.move_option_5.setMaximumSize(
            QtCore.QSize(100, 60)
        )  # Increased max width by 5 pixels
        self.move_option_5.setText("1 mm")

        font = QtGui.QFont()
        font.setPointSize(14)
        self.move_option_5.setFont(font)
        self.move_option_5.setCheckable(True)
        self.move_option_5.setFlat(True)
        self.move_option_5.setProperty("button_type", "")
        self.move_option_5.setObjectName("move_option_4")
        self.bbp_offset_value_selector_group.addButton(self.move_option_5)
        self.bbp_offset_steps_buttons.addWidget(
            self.move_option_5,
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
        self.old_offset_info.setText("Z-Offset")
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
        self.main_content_horizontal_layout.addItem(self.spacerItem)

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
