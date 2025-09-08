import typing

from lib.panels.widgets.optionCardWidget import OptionCard
from lib.utils.blocks_label import BlocksLabel
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class ProbeHelper(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )

    query_printer_object: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(dict, name="query_object")
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

    distances = ["0.01", ".025", ".05", ".01", "1"]
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
        self.setupUi(self)

        self.inductive_icon = QtGui.QPixmap(
            ":/z_levelling/media/btn_icons/inductive.svg"
        )
        self.bltouch_icon = QtGui.QPixmap(
            ":/z_levelling/media/btn_icons/bltouch.svg"
        )
        self.endstop_icon = QtGui.QPixmap(
            ":/extruder_related/media/btn_icons/switch_zoom.svg"
        )
        self.eddy_icon = QtGui.QPixmap(
            ":/z_levelling/media/btn_icons/eddy_mech.svg"
        )

        self._toggle_tool_buttons(False)
        self._setup_move_option_buttons()
        self.move_option_1.toggled.connect(
            lambda: self.handle_zhopHeight_change(
                new_value=float(self.distances[0])
            )
        )
        self.move_option_2.toggled.connect(
            lambda: self.handle_zhopHeight_change(
                new_value=float(self.distances[1])
            )
        )
        self.move_option_3.toggled.connect(
            lambda: self.handle_zhopHeight_change(
                new_value=float(self.distances[2])
            )
        )
        self.move_option_4.toggled.connect(
            lambda: self.handle_zhopHeight_change(
                new_value=float(self.distances[3])
            )
        )
        self.move_option_5.toggled.connect(
            lambda: self.handle_zhopHeight_change(
                new_value=float(self.distances[4])
            )
        )
        self.mb_arrow_up.clicked.connect(  # Move bed closer to nozzle
            lambda: self.run_gcode_signal.emit(f"TESTZ Z=-{self._zhop_height}")
        )
        self.mb_arrow_down.clicked.connect(  # Move bed away from the nozzle
            lambda: self.run_gcode_signal.emit(f"TESTZ Z={self._zhop_height}")
        )
        self.po_back_button.clicked.connect(self.request_back)
        self.accept_button.clicked.connect(self.handle_accept)
        self.abort_button.clicked.connect(self.handle_abort)
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
            self.po_main_content_layout.addWidget(_card)

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

    def init_probe_config(self) -> None:
        if not self.z_offset_config_method:
            return
        if self.z_offset_config_type != "endstop":
            self.z_offsets = tuple(
                map(
                    lambda axis: self.z_offset_config_method[1].get(
                        f"{axis}_offset"
                    ),
                    ["x", "y", "z"],
                )
            )
            self.z_offset_calibration_speed = self.z_offset_config_method[
                1
            ].get("speed")

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
            _keys = []
            if not isinstance(config, list):
                return

            list(map(lambda item: _keys.extend(item.keys()), config))

            probe, *_ = config[0].items()
            self.z_offset_method_type = probe[0]  # The one found first
            self.z_offset_method_config = (
                probe[1],
                "PROBE_CALIBRATE",
                "Z_OFFSET_APPLY_PROBE",
            )
            self.init_probe_config()
            if not _keys:
                return
            self._configure_option_cards(_keys)

        elif isinstance(config, dict):
            if config.get("stepper_z"):
                _virtual_endstop = "probe:z_virtual_endstop"
                _config = config.get("stepper_z")
                if not _config:
                    return
                if (
                    _config.get("endstop_pin") == _virtual_endstop
                ):  # home with probe
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

        if self.z_offset_safe_xy:
            self.run_gcode_signal.emit("G28\nM400")
            self._move_to_pos(
                self.z_offset_safe_xy[0], self.z_offset_safe_xy[1], 100
            )
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
        # TODO: catch the z distances and update the values on the window
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
        if not update:
            return
        # print("Received ´manual_probe´ object update...")
        # print(update)

        # if update.get("z_position_lower"):
        # f"{update.get('z_position_lower'):.4f} mm"
        # print(update)
        if update.get("is_active"):
            if not self.isVisible():
                print("Requested probe helper page view")
                self.request_page_view.emit()

            self.helper_initialize = False
            self.helper_start = True
            self._hide_option_cards()
            self._toggle_tool_buttons(True)

        if update.get("z_position_upper"):
            self.old_offset_info.setText(
                f"{update.get('z_position_upper'):.4f} mm"
            )
        if update.get("z_position"):
            self.current_offset_info.setText(
                f"{update.get('z_position'):.4f} mm"
            )

    @QtCore.pyqtSlot(list, name="handle_gcode_response")
    def handle_gcode_response(self, data: list) -> None:
        """Parses responses from gcodes

        Args:
            data (list): A list containing the gcode that originated
                    the response and the response
        """
        # TODO: Only check for messages if we are in the tool otherwise ignore them
        if self.isVisible():
            if data[0].startswith("!!"):  # An error occurred
                print(
                    f"Calibration aborted, gcode message: {data[0].strip('!! ')}"
                )
                if (
                    "already in a manual z probe"
                    in data[0].strip("!! ").lower()
                ):
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
        ...
        # _data, _metadata, *extra = data + [None] * max(0, 2 - len(data))

    def _move_to_pos(self, x, y, speed) -> None:
        self.run_gcode_signal.emit(f"G91\nG1 Z5 F{10 * 60}\nM400")
        self.run_gcode_signal.emit(f"G90\nG1 X{x} Y{y} F{speed * 60}\nM400")
        return

    ###############################################################################
    ################################# UI RELATED ##################################
    ###############################################################################
    def show(self) -> None:
        return super().show()

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
        self.mb_arrow_down.setEnabled(state)
        self.mb_arrow_up.setEnabled(state)
        self.accept_button.setEnabled(state)
        self.abort_button.setEnabled(state)
        if state:
            self.po_back_button.setEnabled(False)
            self.po_back_button.hide()
            self.po_header_title.setEnabled(False)
            self.po_header_title.hide()
            self.separator_line.hide()
            self.old_offset_box_2.show()
            self.tool_content_info.show()
            self.tool_image.show()
            self.current_offset_box_2.show()
            self.move_intervals.show()
            self.tool_dialog_2.show()
            self.tool_move.show()

        else:
            self.po_back_button.setEnabled(True)
            self.po_back_button.show()
            self.po_header_title.setEnabled(False)
            self.po_header_title.show()
            self.separator_line.show()
            self.tool_content_info.hide()
            self.old_offset_box_2.hide()
            self.current_offset_box_2.hide()
            self.tool_image.hide()
            self.move_intervals.hide()
            self.tool_dialog_2.hide()
            self.tool_move.hide()
        self.update()
        return

    def setupUi(self, probe_offset_page):
        probe_offset_page.setObjectName("probe_offset_page")
        probe_offset_page.resize(710, 410)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            probe_offset_page.sizePolicy().hasHeightForWidth()
        )
        probe_offset_page.setSizePolicy(sizePolicy)
        probe_offset_page.setMinimumSize(QtCore.QSize(700, 410))
        probe_offset_page.setMaximumSize(QtCore.QSize(720, 420))
        self.verticalLayout = QtWidgets.QVBoxLayout(probe_offset_page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.po_header_layout = QtWidgets.QHBoxLayout()
        self.po_header_layout.setObjectName("po_header_layout")
        self.po_header_title = QtWidgets.QLabel(parent=probe_offset_page)
        self.po_header_title.setMinimumSize(QtCore.QSize(200, 60))
        self.po_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.po_header_title.setFont(font)
        self.po_header_title.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.po_header_title.setObjectName("po_header_title")
        self.po_header_layout.addWidget(self.po_header_title)
        self.po_back_button = IconButton(parent=probe_offset_page)
        self.po_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.po_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.po_back_button.setFlat(True)
        self.po_back_button.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/ui/media/btn_icons/back.svg"),
        )
        self.po_back_button.setObjectName("po_back_button")
        self.po_header_layout.addWidget(self.po_back_button)
        self.verticalLayout.addLayout(self.po_header_layout)
        self.separator_line = QtWidgets.QFrame(parent=probe_offset_page)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.separator_line.setFont(font)
        self.separator_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.separator_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.separator_line.setObjectName("separator_line")
        self.verticalLayout.addWidget(self.separator_line)
        self.po_main_content_layout = QtWidgets.QHBoxLayout()
        self.po_main_content_layout.setObjectName("po_main_content_layout")
        self.po_tool_content_layout = QtWidgets.QVBoxLayout()
        self.po_tool_content_layout.setContentsMargins(5, 5, 5, 5)
        self.po_tool_content_layout.setObjectName("po_tool_content_layout")
        self.tool_options_content = QtWidgets.QHBoxLayout()
        self.tool_options_content.setContentsMargins(5, 5, 5, 5)
        self.tool_options_content.setObjectName("tool_options_content")
        self.tool_move = QtWidgets.QWidget(parent=probe_offset_page)
        self.tool_move.setObjectName("tool_move")
        self.move_buttons = QtWidgets.QVBoxLayout(self.tool_move)
        self.move_buttons.setContentsMargins(9, 9, 9, 9)
        self.move_buttons.setObjectName("move_buttons")
        self.mb_arrow_up = IconButton(parent=self.tool_move)
        self.mb_arrow_up.setMinimumSize(QtCore.QSize(80, 80))
        self.mb_arrow_up.setMaximumSize(QtCore.QSize(80, 80))
        self.mb_arrow_up.setFlat(True)
        self.mb_arrow_up.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/up_arrow.svg"),
        )
        self.mb_arrow_up.setObjectName("mb_raise_nozzle")
        self.move_buttons.addWidget(self.mb_arrow_up)
        self.mb_arrow_down = IconButton(parent=self.tool_move)
        self.mb_arrow_down.setMinimumSize(QtCore.QSize(80, 80))
        self.mb_arrow_down.setMaximumSize(QtCore.QSize(80, 80))
        self.mb_arrow_down.setFlat(True)
        self.mb_arrow_down.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/down_arrow.svg"),
        )
        self.mb_arrow_down.setObjectName("mb_lower_nozzle")
        self.move_buttons.addWidget(
            self.mb_arrow_down,
            0,
            QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.tool_options_content.addWidget(
            self.tool_move, 0, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.tool_content_info = QtWidgets.QFrame(parent=probe_offset_page)
        self.tool_content_info.setMinimumSize(QtCore.QSize(400, 200))
        self.tool_content_info.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tool_content_info.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.tool_content_info.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.tool_content_info.setObjectName("tool_content_info")
        self.tool_image = QtWidgets.QLabel(parent=self.tool_content_info)
        self.tool_image.setGeometry(QtCore.QRect(20, 30, 346, 211))
        self.tool_image.setText("")
        self.tool_image.setPixmap(
            QtGui.QPixmap(":/graphics/media/graphics/babystep_graphic.png")
        )
        self.tool_image.setObjectName("tool_image")
        self.verticalLayoutWidget = QtWidgets.QWidget(
            parent=self.tool_content_info
        )
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(130, 30, 220, 154))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.tool_content_info_box = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget
        )
        self.tool_content_info_box.setContentsMargins(6, 6, 6, 6)
        self.tool_content_info_box.setSpacing(2)
        self.tool_content_info_box.setObjectName("tool_content_info_box")
        self.old_offset_box_2 = QtWidgets.QWidget(
            parent=self.verticalLayoutWidget
        )
        self.old_offset_box_2.setMinimumSize(QtCore.QSize(200, 70))
        self.old_offset_box_2.setMaximumSize(QtCore.QSize(200, 70))
        self.old_offset_box_2.setObjectName("old_offset_box_2")
        self.old_offset_box = QtWidgets.QHBoxLayout(self.old_offset_box_2)
        self.old_offset_box.setObjectName("old_offset_box")
        self.old_offset_icon = BlocksLabel(parent=self.old_offset_box_2)
        self.old_offset_icon.setMinimumSize(QtCore.QSize(60, 60))
        self.old_offset_icon.setMaximumSize(QtCore.QSize(60, 60))
        self.old_offset_icon.setText("")
        self.old_offset_icon.setPixmap(
            QtGui.QPixmap(":/graphics/media/btn_icons/old_z_offset_icon.svg")
        )
        self.old_offset_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.old_offset_icon.setObjectName("old_offset_icon")
        self.old_offset_box.addWidget(self.old_offset_icon)
        self.old_offset_info = QtWidgets.QLabel(parent=self.old_offset_box_2)
        self.old_offset_info.setMinimumSize(QtCore.QSize(140, 60))
        self.old_offset_info.setMaximumSize(QtCore.QSize(140, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.old_offset_info.setFont(font)
        self.old_offset_info.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.old_offset_info.setObjectName("old_offset_info")
        self.old_offset_box.addWidget(self.old_offset_info)
        self.tool_content_info_box.addWidget(self.old_offset_box_2)
        self.current_offset_box_2 = QtWidgets.QWidget(
            parent=self.verticalLayoutWidget
        )
        self.current_offset_box_2.setMinimumSize(QtCore.QSize(200, 70))
        self.current_offset_box_2.setMaximumSize(QtCore.QSize(200, 70))
        self.current_offset_box_2.setObjectName("current_offset_box_2")
        self.current_offset_box = QtWidgets.QHBoxLayout(
            self.current_offset_box_2
        )
        self.current_offset_box.setObjectName("current_offset_box")
        self.current_offset_icon = BlocksLabel(
            parent=self.current_offset_box_2
        )
        self.current_offset_icon.setMinimumSize(QtCore.QSize(60, 60))
        self.current_offset_icon.setMaximumSize(QtCore.QSize(60, 60))
        self.current_offset_icon.setText("")
        self.current_offset_icon.setPixmap(
            QtGui.QPixmap(":/graphics/media/btn_icons/new_z_offset_icon.svg")
        )
        self.current_offset_icon.setScaledContents(True)
        self.current_offset_icon.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.current_offset_icon.setObjectName("current_offset_icon")
        self.current_offset_box.addWidget(self.current_offset_icon)
        self.current_offset_info = QtWidgets.QLabel(
            parent=self.current_offset_box_2
        )
        self.current_offset_info.setMinimumSize(QtCore.QSize(140, 60))
        self.current_offset_info.setMaximumSize(QtCore.QSize(140, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.current_offset_info.setFont(font)
        self.current_offset_info.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.current_offset_info.setObjectName("current_offset_info")
        self.current_offset_box.addWidget(self.current_offset_info)
        self.tool_content_info_box.addWidget(self.current_offset_box_2)
        self.tool_options_content.addWidget(
            self.tool_content_info,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.tool_dialog_2 = QtWidgets.QWidget(parent=probe_offset_page)
        self.tool_dialog_2.setObjectName("tool_dialog_2")
        self.tool_dialog = QtWidgets.QVBoxLayout(self.tool_dialog_2)
        self.tool_dialog.setContentsMargins(9, 9, 9, 9)
        self.tool_dialog.setObjectName("tool_dialog")
        self.accept_button = IconButton(parent=self.tool_dialog_2)
        self.accept_button.setMinimumSize(QtCore.QSize(80, 80))
        self.accept_button.setMaximumSize(QtCore.QSize(80, 80))
        self.accept_button.setFlat(True)
        self.accept_button.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg"),
        )
        self.accept_button.setProperty(
            "text_color", QtGui.QColor(255, 255, 255)
        )
        self.accept_button.setObjectName("accept_button")
        self.tool_dialog.addWidget(
            self.accept_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.abort_button = IconButton(parent=self.tool_dialog_2)
        self.abort_button.setMinimumSize(QtCore.QSize(80, 80))
        self.abort_button.setMaximumSize(QtCore.QSize(80, 80))
        self.abort_button.setFlat(True)
        self.abort_button.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/dialog/media/btn_icons/no.svg"),
        )
        self.abort_button.setProperty(
            "text_color", QtGui.QColor(255, 255, 255)
        )
        self.abort_button.setObjectName("abort_button")
        self.tool_dialog.addWidget(
            self.abort_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.tool_options_content.addWidget(
            self.tool_dialog_2, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.po_tool_content_layout.addLayout(self.tool_options_content)
        self.move_intervals_button_group = QtWidgets.QButtonGroup(
            parent=probe_offset_page
        )
        self.move_intervals = QtWidgets.QGroupBox(parent=probe_offset_page)
        self.move_intervals.setMinimumSize(QtCore.QSize(350, 90))
        self.move_intervals.setMaximumSize(QtCore.QSize(16777215, 100))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.WindowText,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.ButtonText,
            brush,
        )
        self.move_intervals.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.move_intervals.setFont(font)
        self.move_intervals.setFlat(True)
        self.move_intervals.setObjectName("move_intervals")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.move_intervals)
        self.horizontalLayout.setContentsMargins(9, 4, -1, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.move_option_1 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_option_1.setMinimumSize(QtCore.QSize(60, 60))
        self.move_option_1.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_option_1.setFont(font)
        self.move_option_1.setStyleSheet("color: white;")
        self.move_option_1.setCheckable(True)
        self.move_option_1.setFlat(True)
        self.move_option_1.setObjectName("move_option_1")
        self.horizontalLayout.addWidget(self.move_option_1)
        self.move_intervals_button_group.addButton(self.move_option_1)
        self.move_option_2 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_option_2.setMinimumSize(QtCore.QSize(60, 60))
        self.move_option_2.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_option_2.setFont(font)
        self.move_option_2.setStyleSheet("color: white;")
        self.move_option_2.setCheckable(True)
        self.move_option_2.setFlat(True)
        self.move_option_2.setObjectName("move_option_2")
        self.move_intervals_button_group.addButton(self.move_option_2)
        self.horizontalLayout.addWidget(self.move_option_2)
        self.move_option_3 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_option_3.setMinimumSize(QtCore.QSize(60, 60))
        self.move_option_3.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_option_3.setFont(font)
        self.move_option_3.setStyleSheet("color: white;")
        self.move_option_3.setCheckable(True)
        self.move_option_3.setFlat(True)
        self.move_option_3.setObjectName("move_option_3")
        self.move_intervals_button_group.addButton(self.move_option_3)
        self.horizontalLayout.addWidget(self.move_option_3)
        self.move_option_4 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_option_4.setMinimumSize(QtCore.QSize(60, 60))
        self.move_option_4.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_option_4.setFont(font)
        self.move_option_4.setStyleSheet("color: white;")
        self.move_option_4.setCheckable(True)
        self.move_option_4.setChecked(False)
        self.move_option_4.setFlat(True)
        self.move_option_4.setObjectName("move_option_4")
        self.horizontalLayout.addWidget(self.move_option_4)
        self.move_intervals_button_group.addButton(self.move_option_4)
        self.move_option_5 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_option_5.setMinimumSize(QtCore.QSize(60, 60))
        self.move_option_5.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_option_5.setFont(font)
        self.move_option_5.setStyleSheet("color: white;")
        self.move_option_5.setCheckable(True)
        self.move_option_5.setChecked(True)
        self.move_option_5.setFlat(True)
        self.move_option_5.setObjectName("move_option_5")
        self.horizontalLayout.addWidget(self.move_option_5)
        self.move_intervals_button_group.addButton(self.move_option_5)
        self.po_tool_content_layout.addWidget(self.move_intervals)
        self.po_main_content_layout.addLayout(self.po_tool_content_layout)
        self.verticalLayout.addLayout(self.po_main_content_layout)

        self.retranslateUi(probe_offset_page)
        QtCore.QMetaObject.connectSlotsByName(probe_offset_page)

    def retranslateUi(self, probe_offset_page):
        _translate = QtCore.QCoreApplication.translate
        probe_offset_page.setWindowTitle(
            _translate("probe_offset_page", "Form")
        )
        self.po_header_title.setText(
            _translate("probe_offset_page", "Z Probe Offset Calibrate")
        )
        self.po_back_button.setText(
            _translate("probe_offset_page", "PushButton")
        )
        self.po_back_button.setProperty(
            "button_type", _translate("probe_offset_page", "icon")
        )
        self.mb_arrow_up.setText(_translate("probe_offset_page", "bb"))
        self.mb_arrow_up.setProperty(
            "button_type", _translate("probe_offset_page", "icon")
        )
        self.mb_arrow_down.setText(_translate("probe_offset_page", "bb"))
        self.mb_arrow_down.setProperty(
            "button_type", _translate("probe_offset_page", "icon")
        )
        self.old_offset_info.setText(
            _translate("probe_offset_page", "TextLabel")
        )
        self.current_offset_info.setText(
            _translate("probe_offset_page", "TextLabel")
        )
        self.accept_button.setText(_translate("probe_offset_page", "Accept"))
        self.accept_button.setProperty(
            "button_type", _translate("probe_offset_page", "icon_text")
        )
        self.accept_button.setProperty(
            "text_formatting", _translate("probe_offset_page", "bottom")
        )
        self.abort_button.setText(_translate("probe_offset_page", "Abort"))
        self.abort_button.setProperty(
            "button_type", _translate("probe_offset_page", "icon_text")
        )
        self.abort_button.setProperty(
            "text_formatting", _translate("probe_offset_page", "bottom")
        )
        self.move_intervals.setTitle(
            _translate("probe_offset_page", "Move Distance (mm)")
        )
        self.move_option_1.setText(
            _translate("probe_offset_page", self.distances[0])
        )
        self.move_option_2.setText(
            _translate("probe_offset_page", self.distances[1])
        )
        self.move_option_3.setText(
            _translate("probe_offset_page", self.distances[2])
        )
        self.move_option_4.setText(
            _translate("probe_offset_page", self.distances[3])
        )
        self.move_option_5.setText(
            _translate("probe_offset_page", self.distances[4])
        )
        self.move_option_5.setAutoDefault(True)
