import typing
import logging
import PyQt6
import PyQt6.QtCore
import PyQt6.QtWidgets
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from utils.ui import BlocksCustomButton, BlocksLabel


# import lib.ui.probeHelperPage_ui as probeHelperUI
# class ProbeHelper(PyQt6.QtWidgets.QWidget, probeHelperUI.Ui_probe_offset_page):
class ProbeHelper(PyQt6.QtWidgets.QWidget):
    request_back: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = pyqtSignal(
        name="request_back"
    )
    run_gcode_signal: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = pyqtSignal(
        str, name="run_gcode"
    )
    on_request_object_config: typing.ClassVar[PyQt6.QtCore.pyqtSignal] = pyqtSignal(
        [str], [list], name="on_request_object_config"
    )

    distances = ["0.01", ".025", ".05", ".01", "1"]
    _commands: dict = {}

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.setObjectName("probe_offset_page")
        self.setupUi(self)

        self._zhop_value: float = 0.0

        self.helper_start: bool = False
        self.calibration_commands: list = []
        self.move_001.toggled.connect(
            lambda: self.handle_zhop_change(new_value=float(self.distances[0]))
        )
        self.move_0025.toggled.connect(
            lambda: self.handle_zhop_change(new_value=float(self.distances[1]))
        )
        self.move_005.toggled.connect(
            lambda: self.handle_zhop_change(new_value=float(self.distances[2]))
        )
        self.move_01.toggled.connect(
            lambda: self.handle_zhop_change(new_value=float(self.distances[3]))
        )
        self.move_1.toggled.connect(
            lambda: self.handle_zhop_change(new_value=float(self.distances[4]))
        )
        self.mb_raise_nozzle.clicked.connect(
            lambda: self.run_gcode_signal.emit(f"TESTZ Z={self._zhop_value}")
        )
        self.mb_lower_nozzle.clicked.connect(
            lambda: self.run_gcode_signal.emit(f"TESTZ Z=-{self._zhop_value}")
        )

        self.po_back_button.clicked.connect(self.request_back)
        self.accept_button.clicked.connect(self.handle_accept)
        self.abort_button.clicked.connect(self.handle_abort)
        self.start_button.clicked.connect(self.handle_start_tool)

        # Hide components before pressing play button
        self._toggle_tool_buttons(False)
        self.update()

    @pyqtSlot(dict, name="on_printer_config")
    def on_printer_config(self, config: dict) -> None:
        _probe_types = ["probe", "bltouch", "smart_effector", "probe_eddy_current"]
        self.on_request_object_config[list].emit(_probe_types)

    @pyqtSlot(list, list, name="on_object_config")
    @pyqtSlot(str, dict, name="on_object_config")
    def on_object_config(self, name: list | str, config: list | dict):
        print("FUCCUUCUCUUCUCJKKKKK")
        if not name:
            print("Name is just empty my man!")

        print(name)
        print(config)

        return

    def determine_z_endstop_method(self):
        ...
        # Get stepper_z config
        # check what is the value of the key endstop_pin
        # if endstop_pin: probe then the printer probe is the endstop, used also for homing
        # if not, a physical switch is used, need to calibrate the z offset with the z_offset_calibrate instead

    def on_add_card_options(self, *options) -> None: ...

    @pyqtSlot(dict, name="handle_available_commands")
    def handle_available_commands(self, commands: dict) -> None:
        _commands = [
            "PROBE_CALIBRATE",
            "PROBE_EDDY_CURRENT_CALIBRATE",
            "LDC_CALIBRATE_DRIVE_CURRENT",
            "MANUAL_PROBE",
        ]
        # Commands that intent to calibrate z offset distances
        if "PROBE_CALIBRATE" in commands.keys():
            self.calibration_commands.append("PROBE_CALIBRATE")
        if "PROBE_EDDY_CURRENT_CALIBRATE" in commands.keys():
            self.calibration_commands.append("PROBE_EDDY_CURRENT_CALIBRATE")
        if "LDC_CALIBRATE_DRIVE_CURRENT" in commands.keys():
            self.calibration_commands.append("LDC_CALIBRATE_DRIVE_CURRENT")
        if "Z_ENDSTOP_CALIBRATE" in commands.keys():
            self.calibration_commands.append("Z_ENDSTOP_CALIBRATE")
        if "MANUAL_PROBE" in commands.keys():
            self.calibration_commands.append("MANUAL_PROBE")
        return

    @pyqtSlot(float, name="handle_zhop_change")
    def handle_zhop_change(self, new_value: float) -> None:
        if new_value == self._zhop_value:
            return
        self._zhop_value = new_value

        # {
        #     "manual_probe": {
        #         "is_active". If it's running
        #         "z_position": the current height of the nozzle (as the printer understands it )
        #         "z_position_lower": last probe attempt just lower than the current height
        #         "z_position_upper": last probe attempt just greater then the current height
        #     }
        # }
        # {
        #     "probe": {
        #         "name": Name of the probe in use
        #         "last_query": returns true if the probe was reported as triggered during the last query probe command
        #         "last_z_result": returns the Z result value of the last PROBE command,
        #     }

        # }

    @pyqtSlot(bool, name="handle_start_tool")
    def handle_start_tool(self) -> None:
        self.helper_start = True

        self.run_gcode_signal.emit("PROBE_CALIBRATE\nM400")
        # self.toggle_tool_buttons(True)

    @pyqtSlot(name="handle_accept")
    def handle_accept(self) -> None:
        self.helper_start = False
        self._toggle_tool_buttons(False)
        self.run_gcode_signal.emit("Z_OFFSET_APPLY_PROBE\nM400")

    @pyqtSlot(name="handle_abort")
    def handle_abort(self) -> None:
        # self.toggle_tool_buttons(False)
        self.run_gcode_signal.emit("ABORT")

    @pyqtSlot(name="handle_gcode_response")
    def handle_gcode_response(self, data: list) -> None:
        """Parses responses from gcodes

        Args:
            data (list): A list containing the gcode that originated the response and the response
        """
        if not self.helper_start:
            return
        ...

    @pyqtSlot(str, list, name="handle_gcode_move_update")
    def handle_gcode_move_update(self, value: dict, name: str) -> None:
        # handle information coming from gcode_move command
        ...

    @pyqtSlot(list, name="handle_error_response")
    def handle_error_response(self, data: list) -> None:
        if not self.helper_start:
            return
        _data, _metadata, *extra = data + [None] * max(0, 2 - len(data))
        if "PROBE_CALIBRATE" in str(_metadata[1]["script"]):
            self.helper_start = False
            self.tool_info_text.setText(f"{_data['message']}")

    def _move_to_pos(self, x, y, speed) -> None:
        self.run_gcode_signal.emit(f"G91\nG1 Z5 F{10 * 60}\nM400")
        self.run_gcode_signal.emit(f"G90\nG1 X{x} Y{y} F{speed * 60}\nM400")
        return

    ###########################################################################
    ############################### UI RELATED ################################
    ###########################################################################
    def show(self) -> None:
        return super().show()

    def _toggle_tool_buttons(self, state: bool) -> None:
        self.mb_lower_nozzle.setEnabled(state)
        self.mb_raise_nozzle.setEnabled(state)
        self.accept_button.setEnabled(state)
        self.abort_button.setEnabled(state)
        if state:
            self.old_offset_box_2.show()
            self.tool_image.show()
            self.current_offset_box_2.show()
            self.tool_info_text.hide()
            self.start_button.hide()
            self.move_intervals.show()
            self.tool_dialog_2.show()
            self.tool_move.show()
        else:
            self.start_button.show()
            self.tool_info_text.show()
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
        sizePolicy.setHeightForWidth(probe_offset_page.sizePolicy().hasHeightForWidth())
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
        self.po_header_title.setStyleSheet("background: transparent; color: white;")
        self.po_header_title.setObjectName("po_header_title")
        self.po_header_layout.addWidget(self.po_header_title)
        self.po_back_button = BlocksCustomButton(parent=probe_offset_page)
        self.po_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.po_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.po_back_button.setFlat(True)
        self.po_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/button_borders/media/btn_icons/back.svg")
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
            "icon_pixmap", QtGui.QPixmap(":/arrow_icons/media/btn_icons/up_arrow.svg")
        )
        self.mb_raise_nozzle.setObjectName("mb_raise_nozzle")
        self.move_buttons.addWidget(self.mb_raise_nozzle)
        self.mb_lower_nozzle = BlocksCustomButton(parent=self.tool_move)
        self.mb_lower_nozzle.setMinimumSize(QtCore.QSize(80, 80))
        self.mb_lower_nozzle.setMaximumSize(QtCore.QSize(80, 80))
        self.mb_lower_nozzle.setFlat(True)
        self.mb_lower_nozzle.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/arrow_icons/media/btn_icons/down_arrow.svg")
        )
        self.mb_lower_nozzle.setObjectName("mb_lower_nozzle")
        self.move_buttons.addWidget(
            self.mb_lower_nozzle,
            0,
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter,
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
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.tool_content_info)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(130, 30, 220, 154))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.tool_content_info_box = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.tool_content_info_box.setContentsMargins(6, 6, 6, 6)
        self.tool_content_info_box.setSpacing(2)
        self.tool_content_info_box.setObjectName("tool_content_info_box")
        self.old_offset_box_2 = QtWidgets.QWidget(parent=self.verticalLayoutWidget)
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
        self.old_offset_info.setStyleSheet("background: transparent; color: white;")
        self.old_offset_info.setObjectName("old_offset_info")
        self.old_offset_box.addWidget(self.old_offset_info)
        self.tool_content_info_box.addWidget(self.old_offset_box_2)
        self.current_offset_box_2 = QtWidgets.QWidget(parent=self.verticalLayoutWidget)
        self.current_offset_box_2.setMinimumSize(QtCore.QSize(200, 70))
        self.current_offset_box_2.setMaximumSize(QtCore.QSize(200, 70))
        self.current_offset_box_2.setObjectName("current_offset_box_2")
        self.current_offset_box = QtWidgets.QHBoxLayout(self.current_offset_box_2)
        self.current_offset_box.setObjectName("current_offset_box")
        self.current_offset_icon = BlocksLabel(parent=self.current_offset_box_2)
        self.current_offset_icon.setMinimumSize(QtCore.QSize(60, 60))
        self.current_offset_icon.setMaximumSize(QtCore.QSize(60, 60))
        self.current_offset_icon.setText("")
        self.current_offset_icon.setPixmap(
            QtGui.QPixmap(":/graphics/media/btn_icons/new_z_offset_icon.svg")
        )
        self.current_offset_icon.setScaledContents(True)
        self.current_offset_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.current_offset_icon.setObjectName("current_offset_icon")
        self.current_offset_box.addWidget(self.current_offset_icon)
        self.current_offset_info = QtWidgets.QLabel(parent=self.current_offset_box_2)
        self.current_offset_info.setMinimumSize(QtCore.QSize(140, 60))
        self.current_offset_info.setMaximumSize(QtCore.QSize(140, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.current_offset_info.setFont(font)
        self.current_offset_info.setStyleSheet("background: transparent; color: white;")
        self.current_offset_info.setObjectName("current_offset_info")
        self.current_offset_box.addWidget(self.current_offset_info)
        self.tool_content_info_box.addWidget(self.current_offset_box_2)
        self.start_button = BlocksCustomButton(parent=self.tool_content_info)
        self.start_button.setGeometry(QtCore.QRect(140, 10, 100, 100))
        self.start_button.setMinimumSize(QtCore.QSize(100, 100))
        self.start_button.setMaximumSize(QtCore.QSize(100, 100))
        self.start_button.setFlat(True)
        self.start_button.setProperty("text_color", QtGui.QColor(255, 255, 255))
        self.start_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/misc/media/btn_icons/start_hugo.svg")
        )
        self.start_button.setObjectName("start_button")
        self.tool_info_text = QtWidgets.QLabel(parent=self.tool_content_info)
        self.tool_info_text.setGeometry(QtCore.QRect(0, 110, 400, 100))
        self.tool_info_text.setMinimumSize(QtCore.QSize(400, 100))
        self.tool_info_text.setMaximumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.tool_info_text.setFont(font)
        self.tool_info_text.setStyleSheet("background: transparent; color: white;")
        self.tool_info_text.setText("")
        self.tool_info_text.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.tool_info_text.setScaledContents(False)
        self.tool_info_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tool_info_text.setWordWrap(False)
        self.tool_info_text.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.NoTextInteraction
        )
        self.tool_info_text.setObjectName("tool_info_text")
        self.tool_options_content.addWidget(
            self.tool_content_info,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
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
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/new_accept_hugo.svg")
        )
        self.accept_button.setProperty("text_color", QtGui.QColor(255, 255, 255))
        self.accept_button.setObjectName("accept_button")
        self.tool_dialog.addWidget(
            self.accept_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.abort_button = BlocksCustomButton(parent=self.tool_dialog_2)
        self.abort_button.setMinimumSize(QtCore.QSize(80, 80))
        self.abort_button.setMaximumSize(QtCore.QSize(80, 80))
        self.abort_button.setFlat(True)
        self.abort_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/new_abort_hugo.svg")
        )
        self.abort_button.setProperty("text_color", QtGui.QColor(255, 255, 255))
        self.abort_button.setObjectName("abort_button")
        self.tool_dialog.addWidget(
            self.abort_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.tool_options_content.addWidget(
            self.tool_dialog_2, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.verticalLayout.addLayout(self.tool_options_content)
        self.move_intervals = QtWidgets.QGroupBox(parent=probe_offset_page)
        self.move_intervals.setMinimumSize(QtCore.QSize(350, 90))
        self.move_intervals.setMaximumSize(QtCore.QSize(16777215, 100))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush
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
        self.move_001 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_001.setMinimumSize(QtCore.QSize(60, 60))
        self.move_001.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_001.setFont(font)
        self.move_001.setStyleSheet("color: white;")
        self.move_001.setCheckable(True)
        self.move_001.setFlat(True)
        self.move_001.setObjectName("move_001")
        self.move_intervals_button_group = QtWidgets.QButtonGroup(probe_offset_page)
        self.move_intervals_button_group.setObjectName("move_intervals_button_group")
        self.move_intervals_button_group.addButton(self.move_001)
        self.horizontalLayout.addWidget(self.move_001)
        self.move_0025 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_0025.setMinimumSize(QtCore.QSize(60, 60))
        self.move_0025.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_0025.setFont(font)
        self.move_0025.setStyleSheet("color: white;")
        self.move_0025.setCheckable(True)
        self.move_0025.setFlat(True)
        self.move_0025.setObjectName("move_0025")
        self.move_intervals_button_group.addButton(self.move_0025)
        self.horizontalLayout.addWidget(self.move_0025)
        self.move_005 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_005.setMinimumSize(QtCore.QSize(60, 60))
        self.move_005.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_005.setFont(font)
        self.move_005.setStyleSheet("color: white;")
        self.move_005.setCheckable(True)
        self.move_005.setFlat(True)
        self.move_005.setObjectName("move_005")
        self.move_intervals_button_group.addButton(self.move_005)
        self.horizontalLayout.addWidget(self.move_005)
        self.move_01 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_01.setMinimumSize(QtCore.QSize(60, 60))
        self.move_01.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_01.setFont(font)
        self.move_01.setStyleSheet("color: white;")
        self.move_01.setCheckable(True)
        self.move_01.setChecked(False)
        self.move_01.setFlat(True)
        self.move_01.setObjectName("move_01")
        self.move_intervals_button_group.addButton(self.move_01)
        self.horizontalLayout.addWidget(self.move_01)
        self.move_1 = QtWidgets.QPushButton(parent=self.move_intervals)
        self.move_1.setMinimumSize(QtCore.QSize(60, 60))
        self.move_1.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.move_1.setFont(font)
        self.move_1.setStyleSheet("color: white;")
        self.move_1.setCheckable(True)
        self.move_1.setChecked(True)
        self.move_1.setFlat(True)
        self.move_1.setObjectName("move_1")
        self.move_intervals_button_group.addButton(self.move_1)
        self.horizontalLayout.addWidget(self.move_1)
        self.verticalLayout.addWidget(self.move_intervals)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)

        self.retranslateUi(probe_offset_page)
        QtCore.QMetaObject.connectSlotsByName(probe_offset_page)

    def retranslateUi(self, probe_offset_page):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("probe_offset_page", "Form"))
        self.po_header_title.setText(
            _translate("probe_offset_page", "Z Probe Offset Calibrate")
        )
        self.po_back_button.setText(_translate("probe_offset_page", "PushButton"))
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
        self.old_offset_info.setText(_translate("probe_offset_page", "TextLabel"))
        self.current_offset_info.setText(_translate("probe_offset_page", "TextLabel"))
        self.start_button.setText(_translate("probe_offset_page", "Start"))
        self.start_button.setProperty(
            "button_type", _translate("probe_offset_page", "icon_text")
        )
        self.start_button.setProperty(
            "text_formatting", _translate("probe_offset_page", "bottom")
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
        self.move_001.setText(_translate("probe_offset_page", "0.01"))
        self.move_0025.setText(_translate("probe_offset_page", "0.025"))
        self.move_005.setText(_translate("probe_offset_page", "0.05"))
        self.move_01.setText(_translate("probe_offset_page", "0.1"))
        self.move_1.setText(_translate("probe_offset_page", "1"))
