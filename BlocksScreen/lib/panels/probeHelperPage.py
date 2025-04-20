import typing

from lib.panels.optionCard import OptionCard
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from utils.ui import BlocksCustomButton, BlocksLabel


class ProbeHelper(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = pyqtSignal(
        name="request_back"
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = pyqtSignal(
        str, name="run_gcode"
    )

    on_subscribe_config: typing.ClassVar[QtCore.pyqtSignal] = pyqtSignal(
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

    distances = ["0.01", ".025", ".05", ".01", "1"]
    _calibration_commands: list = []
    probe_type: str = ""
    probe_config: tuple = ()
    helper_start: bool = False

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.setObjectName("probe_offset_page")
        self.setupUi(self)

        self.inductive_icon = QtGui.QPixmap(
            ":/probe/media/btn_icons/1inductive zoom.svg"
        )
        self.bltouch_icon = QtGui.QPixmap(
            ":/probe/media/btn_icons/1bltouch zoom.svg"
        )
        self.endstop_icon = QtGui.QPixmap(
            ":/probe/media/btn_icons/1switch zoom.svg"
        )
        self.eddy_icon = QtGui.QPixmap(
            ":/probe/media/btn_icons/1eddy mech zoom.svg"
        )

        self._zhop_height: float = 0.0
        self.current_probe: str = ""
        self.card_options: dict = {}
        # Hide components before pressing play button
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
        self.mb_raise_nozzle.clicked.connect(
            lambda: self.run_gcode_signal.emit(f"TESTZ Z={self._zhop_height}")
        )
        self.mb_lower_nozzle.clicked.connect(
            lambda: self.run_gcode_signal.emit(f"TESTZ Z=-{self._zhop_height}")
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
                probes (list[dict]): Available printer config tools list
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
        if not self.probe_config:
            return
        self.probe_offsets = tuple(
            map(
                lambda axis: self.probe_config[1].get(f"{axis}_offset"),
                ["x", "y", "z"],
            )
        )
        self.z_probe_speed = self.probe_config[1].get("speed")

    @pyqtSlot(list, name="on_config_subscription")
    def on_config_subscription(self, config_list: list):
        if not config_list:
            return
        if not self.probe_config:
            _keys = []
            if not isinstance(config_list, list):
                return
            list(map(lambda item: _keys.extend(item.keys()), config_list))
        unpacked, *_ = config_list[0].items()
        self.probe_config = unpacked
        self.init_probe_config()
        self._configure_option_cards(_keys)

    @pyqtSlot(dict, name="on_config_subscription")
    def determine_home_method(self, config: dict):
        """Called when the `stepper_z` configuration is
        received. Method that subscribes to the stepper_z
        configuration.

        Checks if the z homing method is done via probe
        or endstop. By capturing the  `endstop pin` field,
        if string `probe:z_virtual_endstop` is captured,
        it means a probe is used to home the z endstop.
        Conversely if the string is not present it means
        a switch endstop is used to home the z axis.

        If z homing is achieved via switch endstop
        an additional card (**OptionCard**) is added
        to the tool helper. This card adds calibration
        of the z offset using the switch endstop.


        Args:
            config (dict): The `stepper_z`
                printer object configuration.

        """
        if not config:
            return
        _virtual_endstop = "probe:z_virtual_endstop"
        if config.get("endstop_pin") == _virtual_endstop:  # home with probe
            return
        self._configure_option_cards(["Z_ENDSTOP_CALIBRATE"])

    @pyqtSlot(dict, name="on_printer_config")
    def on_printer_config(self, config: dict) -> None:
        _probe_types = [
            "probe",
            "bltouch",
            "smart_effector",
            "probe_eddy_current",
        ]
        self.on_subscribe_config[list, "PyQt_PyObject"].emit(
            _probe_types, self.on_config_subscription
        )
        self.on_subscribe_config[str, "PyQt_PyObject"].emit(
            str("stepper_z"), self.determine_home_method
        )

    @pyqtSlot(dict, name="on_available_gcode_cmds")
    def on_available_gcode_cmds(self, gcode_cmds: dict) -> None:
        _available_commands = gcode_cmds.keys()
        _card_names = list(
            map(lambda card: card[1].name, self.card_options.items())
        )

        _manual_probe_cmd = [
            "MANUAL_PROBE",  # SPEED=<speed>
            "Z_ENDSTOP_CALIBRATE",  # SPEED=<speed>
            "Z_OFFSET_APPLY_ENDSTOP",  # REQUIRES A SAVE_CONFIG to take effect
        ]
        _eddy_cmd = [
            "PROBE_EDDY_CURRENT_CALIBRATE",  # CHIP=<config_name>
            "LDC_CALIBRATE_DRIVE_CURRENT",  # CHIP=<config_name>
        ]
        _probe_cmd = [
            "PROBE",  # PROBE_SPEED=<mm/s> LIFT_SPEED=<mm/s> SAMPLES=<count> SAMPLE_RETRACT_DIST=<mm> SAMPLES_TOLERANCE=<mm> SAMPLES_TOLERANCE_RETRIES=<count> SAMPLES_RESULT=<median|average>
            "QUERY_PROBE",  # Just reports stuff
            "PROBE_ACCURACY",  # PROBE_SPEED=<mm/s> SAMPLES=<count> SAMPLE_RETRACT_DIST=<mm>
            "PROBE_CALIBRATE",  # SPEED=<speed> PROBE_PARAMETERS=<value>
            "Z_OFFSET_APPLY_PROBE",  # REQUIRES SAVE_CONFIG to take effect
        ]
        # self._calibration_commands = list(filter(lambda command:  , _available_commands))

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
        return

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

    def _build_calibration_command(self, probe: str) -> str:
        if not probe:
            return ""
        # TODO Move to a certain position first
        if probe == "Z_ENDSTOP_CALIBRATE":
            if self._verify_gcode("Z_ENDSTOP_CALIBRATE"):
                return "Z_ENDSTOP_CALIBRATE"
        elif "eddy" in probe:
            if self._verify_gcode("PROBE_EDDY_CURRENT_CALIBRATE"):
                _name = probe.split(" ")[1]
                if not _name:
                    return ""
                return (
                    f"PROBE_EDDY_CURRENT_CALIBRATE CHIP={probe.split(' ')[1]}"
                )
        elif "probe" in probe or "bltouch" in probe:
            if self._verify_gcode("PROBE_CALIBRATE"):
                if self.z_probe_speed:
                    return f"PROBE_CALIBRATE SPEED={self.z_probe_speed}"
                return "PROBE_CALIBRATE"
        return ""

    @pyqtSlot(float, name="handle_zhopHeight_change")
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

    @pyqtSlot("PyQt_PyObject", name="handle_start_tool")
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
        _cmd = self._build_calibration_command(sender.name)
        if not _cmd:
            return
        print(_cmd)
        self._hide_option_cards()
        self.helper_start = True
        self._toggle_tool_buttons(True)
        self.run_gcode_signal.emit(self._build_calibration_command(sender.name))

    @pyqtSlot(name="handle_accept")
    def handle_accept(self) -> None:
        """Send the appropriate gcode command that
        saves the calculated probe configuration value
        considering the tool that is currently being
        calibrated. Finishing the tool helper and resetting
        the Probe helper page.
        This method runs when the probe tool helper `accept`
        button is clicked.
        """
        if not self.helper_start: 
            return 
        self.helper_start = False
        self._toggle_tool_buttons(False)
        self._show_option_cards()
        # self.run_gcode_signal.emit("Z_OFFSET_APPLY_PROBE\nM400")

    @pyqtSlot(name="handle_abort")
    def handle_abort(self) -> None:
        if not self.helper_start:
            return
        self._toggle_tool_buttons(False)
        self._show_option_cards()
        self.run_gcode_signal.emit("ABORT")

    @pyqtSlot(list, name="handle_gcode_response")
    def handle_gcode_response(self, data: list) -> None:
        """Parses responses from gcodes

        Args:
            data (list): A list containing the gcode that originated
                    the response and the response
        """
        # This is where i capture and parse information about the running
        # gcode calibration command
        
        # ['!! No trigger on probe after full movement']
        # {'code': 400, 'message': 'No trigger on probe after full movement'}
        
        print(data)
        if not self.helper_start:
            return
        
        ...

    @pyqtSlot(str, list, name="handle_gcode_move_update")
    def handle_gcode_move_update(self, value: dict, name: str) -> None:
        # handle information coming from gcode_move command
        # I can capture information about the toolhead xyz positions
        # in here
        print(value)
        ...

    @pyqtSlot(list, name="handle_error_response")
    def handle_error_response(self, data: list) -> None:
        # I also receive information about errors here,
        # including probe helper did not actually start because
        # could not probe, another type of error
        # klipper screen does this i i find it good aswell,
        # The thing is, the tool helper should stop when an error appers
        # either before it actually starts, middle or end
        # the error could appear in any stage of the helper
        
        
        # i send the start calibrate gcode, i might receive a error before i should show the calibration screen 
        # I SHOULD ONLY DISPLAY THE CALIBRATION SCREEN AFTER I CRESEIVE THE FOLLOWING MESSAGE 
        
        """
        Z position: ?????? --> 5.263 <-- ??????
        
        Starting manual Z probe. Use TESTZ to adjust position.
        Finish with ACCEPT or ABORT command.
        
        
        """
        
        if not self.helper_start:
            return
        _data, _metadata, *extra = data + [None] * max(0, 2 - len(data))
        print(_data)
        print(_metadata)
        
        if "PROBE_CALIBRATE" in str(_metadata[1]["script"]):
            self.helper_start = False
            # self.tool_info_text.setText(f"{_data['message']}")

    def _move_to_pos(self, x, y, speed) -> None:
        self.run_gcode_signal.emit(f"G91\nG1 Z5 F{10 * 60}\nM400")
        self.run_gcode_signal.emit(f"G90\nG1 X{x} Y{y} F{speed * 60}\nM400")
        return

    ###########################################################################
    ############################### UI RELATED ################################
    ###########################################################################
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
        self.mb_lower_nozzle.setEnabled(state)
        self.mb_raise_nozzle.setEnabled(state)
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
        self.po_back_button = BlocksCustomButton(parent=probe_offset_page)
        self.po_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.po_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.po_back_button.setFlat(True)
        self.po_back_button.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/button_borders/media/btn_icons/back.svg"),
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
        self.mb_raise_nozzle = BlocksCustomButton(parent=self.tool_move)
        self.mb_raise_nozzle.setMinimumSize(QtCore.QSize(80, 80))
        self.mb_raise_nozzle.setMaximumSize(QtCore.QSize(80, 80))
        self.mb_raise_nozzle.setFlat(True)
        self.mb_raise_nozzle.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/up_arrow.svg"),
        )
        self.mb_raise_nozzle.setObjectName("mb_raise_nozzle")
        self.move_buttons.addWidget(self.mb_raise_nozzle)
        self.mb_lower_nozzle = BlocksCustomButton(parent=self.tool_move)
        self.mb_lower_nozzle.setMinimumSize(QtCore.QSize(80, 80))
        self.mb_lower_nozzle.setMaximumSize(QtCore.QSize(80, 80))
        self.mb_lower_nozzle.setFlat(True)
        self.mb_lower_nozzle.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/down_arrow.svg"),
        )
        self.mb_lower_nozzle.setObjectName("mb_lower_nozzle")
        self.move_buttons.addWidget(
            self.mb_lower_nozzle,
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
        self.accept_button = BlocksCustomButton(parent=self.tool_dialog_2)
        self.accept_button.setMinimumSize(QtCore.QSize(80, 80))
        self.accept_button.setMaximumSize(QtCore.QSize(80, 80))
        self.accept_button.setFlat(True)
        self.accept_button.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/dialog/media/btn_icons/new_accept_hugo.svg"),
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
        self.abort_button = BlocksCustomButton(parent=self.tool_dialog_2)
        self.abort_button.setMinimumSize(QtCore.QSize(80, 80))
        self.abort_button.setMaximumSize(QtCore.QSize(80, 80))
        self.abort_button.setFlat(True)
        self.abort_button.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/dialog/media/btn_icons/new_abort_hugo.svg"),
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
        self.mb_raise_nozzle.setText(_translate("probe_offset_page", "bb"))
        self.mb_raise_nozzle.setProperty(
            "button_type", _translate("probe_offset_page", "icon")
        )
        self.mb_lower_nozzle.setText(_translate("probe_offset_page", "bb"))
        self.mb_lower_nozzle.setProperty(
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
