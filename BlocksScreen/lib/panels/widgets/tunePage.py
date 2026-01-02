import re
import typing

from helper_methods import normalize
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.display_button import DisplayButton
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class TuneWidget(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back_page"
    )

    request_sensorsPage: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_sensorsPage"
    )
    request_bbpPage: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_bbpPage"
    )

    request_sliderPage: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str, int, "PyQt_PyObject"],
        [str, int, "PyQt_PyObject", int, int],
        name="request_sliderPage",
    )
    request_numpad: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str, int, "PyQt_PyObject"],
        [str, int, "PyQt_PyObject", int, int],
        name="request_numpad",
    )
    run_gcode: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )
    speed_factor_override: float = 1.0
    extruder_target: int = 0
    bed_target: int = 0
    tune_display_buttons: dict = {}

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setObjectName("tune_page")
        self._setupUI()
        self.sensors_menu_btn.clicked.connect(self.request_sensorsPage.emit)
        self.tune_babystep_menu_btn.clicked.connect(self.request_bbpPage.emit)
        self.tune_back_btn.clicked.connect(self.request_back)
        self.bed_display.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Bed",
                int(round(self.bed_target)),
                self.on_numpad_change,
                0,
                120,  # TODO: Get this value from printer objects
            )
        )
        self.extruder_display.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Extruder",
                int(round(self.extruder_target)),
                self.on_numpad_change,
                0,
                300,  # TODO: Get this value from printer objects
            )
        )
        self.speed_display.clicked.connect(
            lambda: self.request_sliderPage[str, int, "PyQt_PyObject", int, int].emit(
                "Speed",
                int(self.speed_factor_override * 100),
                self.on_slider_change,
                10,
                300,
            )
        )

    @QtCore.pyqtSlot(str, int, name="on_numpad_change")
    def on_numpad_change(self, name: str, new_value: int) -> None:
        """Handle numpad value inserted"""
        if "bed" in name.lower():
            name = "heater_bed"
        elif "extruder" in name.lower():
            name = "extruder"
        self.run_gcode.emit(f"SET_HEATER_TEMPERATURE HEATER={name} TARGET={new_value}")

    @QtCore.pyqtSlot(str, int, name="on_slider_change")
    def on_slider_change(self, name: str, new_value: int) -> None:
        """Handle slider page value inserted"""
        if "speed" in name.lower():
            self.speed_factor_override = new_value / 100
            self.run_gcode.emit(f"M220 S{new_value}")

        if "fan" in name.lower():
            if name.lower() == "fan":
                self.run_gcode.emit(
                    f"M106 S{int(round((normalize(float(new_value / 100), 0.0, 1.0, 0, 255))))}"
                )  # [0, 255] Range
            else:
                self.run_gcode.emit(
                    f"SET_FAN_SPEED FAN={name} SPEED={float(new_value / 100.00)}"
                )  # [0.0, 1.0] Range

    @QtCore.pyqtSlot(str, str, float, name="on_fan_update")
    @QtCore.pyqtSlot(str, str, int, name="on_fan_update")
    def on_fan_object_update(
        self, name: str, field: str, new_value: int | float
    ) -> None:
        """Slot Method that receives information from fan objects

        Args:
            name (str): fan object name
            field (str): field name
            new_value (int | float): New value for field name
        """
        fields = name.split()
        first_field = fields[0]
        second_field = fields[1].lower() if len(fields) > 1 else None
        if "speed" in field:
            if not self.tune_display_buttons.get(name, None) and first_field in (
                "fan",
                "fan_generic",
            ):
                pattern_blower = r"(?:^|_)(?:blower|auxiliary)(?:_|$)"
                pattern_exhaust = r"(?:^|_)exhaust(?:_|$)"

                _new_display_button = self.create_display_button(name)
                _new_display_button.setParent(self)
                _new_display_button.icon_pixmap = self.path.get("fan")
                if second_field:
                    if re.search(pattern_blower, second_field):
                        _new_display_button.icon_pixmap = self.path.get("blower")
                    elif re.search(pattern_exhaust, second_field):
                        _new_display_button.icon_pixmap = self.path.get("fan_cage")

                self.tune_display_buttons.update(
                    {
                        name: {
                            "display_button": _new_display_button,
                            "speed": 0,
                        }
                    }
                )
                _new_display_button.clicked.connect(
                    lambda: self.request_sliderPage[
                        str, int, "PyQt_PyObject", int, int
                    ].emit(
                        str(name),
                        int(round(self.tune_display_buttons.get(name).get("speed", 0))),
                        self.on_slider_change,
                        0,
                        100,
                    )
                )
                self.tune_display_vertical_child_layout_2.addWidget(_new_display_button)
            _display_button = self.tune_display_buttons.get(name)
            if not _display_button:
                return
            _display_button.update({"speed": int(round(new_value * 100))})
            _display_button.get("display_button").setText(f"{new_value * 100:.0f}%")

    def create_display_button(self, name: str) -> DisplayButton:
        """Create and return a DisplayButton

        Args:
            name (str): Name for the display button

        Returns:
            DisplayButton: The created DisplayButton object
        """
        display_button = DisplayButton()
        display_button.setObjectName(str(name + "_display"))
        display_button.setMinimumSize(QtCore.QSize(150, 50))
        display_button.setMaximumSize(QtCore.QSize(150, 80))
        font = QtGui.QFont()
        font.setPointSize(16)
        display_button.setFont(font)
        return display_button

    @QtCore.pyqtSlot(str, float, name="on_gcode_move_update")
    def on_gcode_move_update(self, field: str, value: float) -> None:
        """Handle gcode move update"""
        if "speed_factor" in field:
            self.speed_factor_override = value
            self.speed_display.setText(str(f"{int(self.speed_factor_override * 100)}%"))

    @QtCore.pyqtSlot(str, str, float, name="on_extruder_update")
    def on_extruder_temperature_change(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        """Processes the information that comes from the printer object "extruder"

        Args:
            extruder_name (str): Name of the extruder object
            field (str): Name of the updated field
            new_value (float): New value for the field
        """
        if field == "temperature":
            self.extruder_display.setText(f"{new_value:.1f}")
        if field == "target":
            self.extruder_target = int(new_value)

    @QtCore.pyqtSlot(str, str, float, name="on_heater_bed_update")
    def on_heater_bed_temperature_change(
        self, name: str, field: str, new_value: float
    ) -> None:
        """Processes the information that comes from the printer object "heater_bed"

        Args:
            name (str): Name of the heater bed object.
            field (str): Name od the updated field.
            new_value (float): New value for the fields.
        """
        if field == "temperature":
            self.bed_display.setText(f"{new_value:.1f}")
        if field == "target":
            self.bed_target = int(new_value)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        if self.isVisible():
            self.speed_display.setText(str(f"{int(self.speed_factor_override * 100)}%"))

    def _setupUI(self) -> None:
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tune_content = QtWidgets.QVBoxLayout(self)
        self.tune_content.setContentsMargins(2, 0, 0, 0)
        self.tune_content.setObjectName("tune_content")
        self.tune_header = QtWidgets.QHBoxLayout()
        self.tune_header.setObjectName("tune_header")
        self.tune_title_label = QtWidgets.QLabel(parent=self)
        self.tune_title_label.setMinimumSize(QtCore.QSize(0, 30))
        self.tune_title_label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Momcake-Bold")

        font.setPointSize(22)
        palette = self.tune_title_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))

        self.tune_title_label.setFont(font)
        self.tune_title_label.setPalette(palette)
        self.tune_title_label.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.tune_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tune_title_label.setObjectName("tune_title_label")
        self.tune_header.addWidget(
            self.tune_title_label,
            0,
        )
        self.tune_back_btn = IconButton(parent=self)
        self.tune_back_btn.setObjectName("tune_back_btn")
        self.tune_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tune_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.tune_back_btn.setFlat(True)
        self.tune_back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.tune_header.addWidget(
            self.tune_back_btn,
            0,
        )
        self.tune_content.addLayout(self.tune_header, 0)
        self.tune_menu_buttons = QtWidgets.QHBoxLayout()
        self.tune_menu_buttons.setObjectName("tune_menu_buttons")
        self.tune_babystep_menu_btn = BlocksCustomButton(parent=self)
        self.tune_babystep_menu_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.tune_babystep_menu_btn.setMaximumSize(QtCore.QSize(250, 80))
        font.setPointSize(18)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tune_babystep_menu_btn.sizePolicy().hasHeightForWidth()
        )
        self.tune_babystep_menu_btn.setSizePolicy(sizePolicy)
        self.tune_babystep_menu_btn.setFont(font)
        self.tune_babystep_menu_btn.setMouseTracking(True)
        self.tune_babystep_menu_btn.setTabletTracking(True)
        self.tune_babystep_menu_btn.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.tune_babystep_menu_btn.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.tune_babystep_menu_btn.setAutoDefault(False)
        self.tune_babystep_menu_btn.setFlat(True)
        self.tune_babystep_menu_btn.setPixmap(
            QtGui.QPixmap(":/z_levelling/media/btn_icons/baby_step_icon.svg")
        )
        self.tune_babystep_menu_btn.setObjectName("tune_babystep_menu_btn")
        self.tune_menu_buttons.addWidget(
            self.tune_babystep_menu_btn,
            0,
        )
        self.tune_change_filament_btn = BlocksCustomButton(parent=self)
        self.tune_change_filament_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.tune_change_filament_btn.setMaximumSize(QtCore.QSize(250, 80))
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.tune_change_filament_btn.sizePolicy().hasHeightForWidth()
        )
        self.tune_change_filament_btn.setSizePolicy(sizePolicy)
        self.tune_change_filament_btn.setFont(font)
        self.tune_change_filament_btn.setMouseTracking(False)
        self.tune_change_filament_btn.setTabletTracking(True)
        self.tune_change_filament_btn.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.tune_change_filament_btn.setAutoDefault(False)
        self.tune_change_filament_btn.setFlat(True)
        self.tune_change_filament_btn.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/change_filament.svg")
        )
        self.tune_change_filament_btn.setObjectName("tune_change_filament_btn")
        self.tune_menu_buttons.addWidget(
            self.tune_change_filament_btn,
            0,
        )
        self.sensors_menu_btn = IconButton(parent=self)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sensors_menu_btn.sizePolicy().hasHeightForWidth()
        )
        self.sensors_menu_btn.setSizePolicy(sizePolicy)
        self.sensors_menu_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.sensors_menu_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.sensors_menu_btn.setMouseTracking(True)
        self.sensors_menu_btn.setTabletTracking(True)
        self.sensors_menu_btn.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.NoContextMenu
        )
        self.sensors_menu_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.sensors_menu_btn.setAutoDefault(False)
        self.sensors_menu_btn.setFlat(True)
        self.sensors_menu_btn.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/filament_sensor.svg")
        )
        self.sensors_menu_btn.setObjectName("sensors_menu_btn")
        self.tune_menu_buttons.addWidget(self.sensors_menu_btn)
        self.tune_content.addLayout(self.tune_menu_buttons, 0)
        self.tune_display_horizontal_parent_layout = QtWidgets.QHBoxLayout()
        self.tune_display_horizontal_parent_layout.setContentsMargins(2, 0, 2, 2)
        self.tune_display_horizontal_parent_layout.setObjectName(
            "tune_display_horizontal_parent_layout"
        )
        self.tune_display_vertical_child_layout_1 = QtWidgets.QVBoxLayout()
        self.tune_display_vertical_child_layout_1.setContentsMargins(2, 0, 2, 2)
        self.tune_display_vertical_child_layout_1.setSpacing(5)
        self.tune_display_vertical_child_layout_1.setObjectName(
            "tune_display_vertical_parent_layout"
        )
        self.tune_display_vertical_child_layout_2 = QtWidgets.QVBoxLayout()
        self.tune_display_vertical_child_layout_2.setContentsMargins(2, 0, 2, 2)
        self.tune_display_vertical_child_layout_2.setSpacing(5)
        self.tune_display_vertical_child_layout_2.setObjectName(
            "tune_display_vertical_parent_layout_2"
        )
        self.tune_display_vertical_child_layout_3 = QtWidgets.QVBoxLayout()
        self.tune_display_vertical_child_layout_3.setContentsMargins(2, 0, 2, 2)
        self.tune_display_vertical_child_layout_3.setSpacing(5)
        self.tune_display_vertical_child_layout_3.setObjectName(
            "tune_display_vertical_parent_layout_3"
        )
        self.tune_display_horizontal_parent_layout.addLayout(
            self.tune_display_vertical_child_layout_1
        )
        self.tune_display_horizontal_parent_layout.addLayout(
            self.tune_display_vertical_child_layout_2
        )
        self.tune_display_horizontal_parent_layout.addLayout(
            self.tune_display_vertical_child_layout_3
        )
        self.tune_display_horizontal_parent_layout.setSpacing(0)
        self.tune_display_horizontal_parent_layout.setContentsMargins(0, 0, 0, 0)
        self.bed_display = DisplayButton(parent=self)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.bed_display.sizePolicy().hasHeightForWidth())
        self.bed_display.setSizePolicy(sizePolicy)
        self.bed_display.setMinimumSize(QtCore.QSize(150, 60))
        self.bed_display.setMaximumSize(QtCore.QSize(150, 60))
        font.setPointSize(16)
        self.bed_display.setFont(font)
        self.bed_display.setText("")
        self.bed_display.setFlat(True)
        self.bed_display.setPixmap(
            QtGui.QPixmap(":/temperature_related/media/btn_icons/temperature_plate.svg")
        )
        self.bed_display.setObjectName("bed_display")
        self.tune_display_vertical_child_layout_1.addWidget(self.bed_display)
        self.extruder_display = DisplayButton(parent=self)
        self.extruder_display.setFont(font)
        sizePolicy.setHeightForWidth(
            self.extruder_display.sizePolicy().hasHeightForWidth()
        )
        self.extruder_display.setSizePolicy(sizePolicy)
        self.extruder_display.setMinimumSize(QtCore.QSize(150, 60))
        self.extruder_display.setMaximumSize(QtCore.QSize(150, 60))
        self.extruder_display.setText("")
        self.extruder_display.setFlat(True)
        self.extruder_display.setPixmap(
            QtGui.QPixmap(":/temperature_related/media/btn_icons/temperature.svg")
        )
        self.extruder_display.setObjectName("extruder_display")
        self.tune_display_vertical_child_layout_1.addWidget(self.extruder_display)
        self.speed_display = DisplayButton(parent=self)
        self.speed_display.setFont(font)
        sizePolicy.setHeightForWidth(
            self.speed_display.sizePolicy().hasHeightForWidth()
        )
        self.speed_display.setSizePolicy(sizePolicy)
        self.speed_display.setMinimumSize(QtCore.QSize(150, 60))
        self.speed_display.setMaximumSize(QtCore.QSize(150, 60))
        self.speed_display.setFont(font)
        self.speed_display.setFlat(True)
        self.speed_display.setPixmap(
            QtGui.QPixmap(":/motion/media/btn_icons/speed.svg")
        )
        self.speed_display.setObjectName("speed_display")
        self.tune_display_vertical_child_layout_3.addWidget(self.speed_display)
        self.tune_content.addLayout(self.tune_display_horizontal_parent_layout, 1)
        self.tune_display_horizontal_parent_layout.setStretch(0, 0)
        self.tune_display_horizontal_parent_layout.setStretch(1, 0)
        self.tune_display_horizontal_parent_layout.setStretch(2, 1)
        self.tune_content.setStretch(0, 0)
        self.tune_content.setStretch(1, 0)
        self.tune_content.setStretch(2, 2)
        self.tune_content.setContentsMargins(2, 0, 2, 0)
        self.setLayout(self.tune_content)
        self.setContentsMargins(2, 2, 2, 2)

        self.path = {
            "fan_cage": QtGui.QPixmap(":/fan_related/media/btn_icons/fan_cage.svg"),
            "blower": QtGui.QPixmap(":/fan_related/media/btn_icons/blower.svg"),
            "fan": QtGui.QPixmap(":/fan_related/media/btn_icons/fan.svg"),
        }
        self._retranslateUI()

    def _retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("printStackedWidget", "StackedWidget"))
        self.tune_title_label.setText(_translate("printStackedWidget", "Tune"))
        self.tune_title_label.setProperty(
            "class", _translate("printStackedWidget", "title_text")
        )
        self.tune_back_btn.setProperty(
            "button_type", _translate("printStackedWidget", "icon")
        )
        self.tune_babystep_menu_btn.setText(
            _translate("printStackedWidget", "Babystep")
        )
        self.tune_babystep_menu_btn.setProperty(
            "class", _translate("printStackedWidget", "menu_btn")
        )
        self.tune_babystep_menu_btn.setProperty(
            "button_type", _translate("printStackedWidget", "normal")
        )
        self.tune_change_filament_btn.setText(
            _translate("printStackedWidget", "Filament\nChange")
        )
        self.tune_change_filament_btn.setProperty(
            "class", _translate("printStackedWidget", "menu_btn")
        )
        self.tune_change_filament_btn.setProperty(
            "button_type", _translate("printStackedWidget", "normal")
        )
        self.sensors_menu_btn.setProperty(
            "class", _translate("printStackedWidget", "menu_btn")
        )
        self.sensors_menu_btn.setProperty(
            "button_type", _translate("printStackedWidget", "icon")
        )
        self.bed_display.setProperty(
            "name", _translate("printStackedWidget", "bed_temperature_display")
        )
        self.bed_display.setProperty(
            "button_type", _translate("printStackedWidget", "display")
        )
        self.extruder_display.setProperty(
            "name",
            _translate("printStackedWidget", "extruder_temperature_display"),
        )
        self.extruder_display.setProperty(
            "button_type", _translate("printStackedWidget", "display")
        )
        self.speed_display.setProperty(
            "name", _translate("printStackedWidget", "print_speed_display")
        )
        self.speed_display.setProperty(
            "button_type", _translate("printStackedWidget", "display")
        )
