import typing
from enum import Enum, auto
from lib.utils.icon_button import IconButton

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.blocks_button import BlocksCustomButton


class Process(Enum):
    FAN = auto()
    AXIS = auto()
    BED_HEATER = auto()
    EXTRUDER = auto()
    AXIS_MAINTENANCE = auto()


class RoutineCheckPage(QtWidgets.QWidget):
    request_troubleshoot_page = QtCore.pyqtSignal(name="request-troubleshoot-page")

    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    show_waiting_page = QtCore.pyqtSignal(str, int, bool, name="show-waiting-page")

    set_rc_page = QtCore.pyqtSignal(str, str, name="set-rc-page")

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(RoutineCheckPage, self).__init__(parent)

        self.objects: dict = {
            "fans": {},
            "axis": {"x": "indf", "y": "indf", "z": "indf"},
            "bheat": {"Bed_Heater": "indf"},
            "extrude": {"extruder": "indf"},
            "leds": {},
        }
        self.tb = False

        self._setup_ui()

        self.current_object: typing.Optional[str] = None
        self.routine_check_back_btn.clicked.connect(self.request_back_button)

        self.rc_fans.clicked.connect(lambda: self.run_routine(Process.FAN))
        self.rc_bheat.clicked.connect(lambda: self.run_routine(Process.BED_HEATER))
        self.rc_ext.clicked.connect(lambda: self.run_routine(Process.EXTRUDER))
        self.rc_axis.clicked.connect(lambda: self.run_routine(Process.AXIS))

    @QtCore.pyqtSlot(list, name="on_object_list")
    def on_object_list(self, object_list: list) -> None:
        """Handle receiving printer object list"""
        self.cg = object_list
        for obj in self.cg:
            base_name = obj.split()[0]
            # Only accept 'fan_generic' or 'fan'
            if base_name == "fan_generic" or base_name == "fan":
                self.objects["fans"][obj.split()[1]] = "indef"

    def run_routine(self, process: Process):
        """Run check routine for available processes"""
        self.current_process = process
        routine_configs = {
            Process.FAN: ("fans", "fan is spinning"),
            Process.AXIS: ("axis", "axis is moving"),
            Process.BED_HEATER: ("bheat", "bed is heating"),
            Process.EXTRUDER: ("extrude", "extruder is being tested"),
        }
        if process not in routine_configs:
            return
        obj_key, message = routine_configs[process]
        obj_list = list(self.objects.get(obj_key, {}).keys())
        if not self._advance_routine_object(obj_list):
            if self.tb:
                self.request_troubleshoot_page.emit()
                self.tb = False
            else:
                self.request_back_button.emit

            if process == Process.FAN:
                self.run_gcode_signal.emit("M107")
            return

        message = f"Please check if the {self.current_object} is functioning correctly."
        if process == Process.AXIS:
            message = f"Please ensure the {self.current_object} axis moves correctly."
        elif process in [Process.BED_HEATER, Process.EXTRUDER]:
            message = "Please check if the temperature reaches 60°C. \n you may need to wait a few moments."

        self.set_rc_page.emit(f"Running routine for: {self.current_object}", message)
        self.show_waiting_page.emit(
            f"Please check if the {message}",
            10000 if process == Process.AXIS else 0,
            False,
        )
        self._send_routine_gcode()

    @QtCore.pyqtSlot(str, name="on_rc_asnwer")
    def on_routine_answer(self, answer: str) -> None:
        """Handle routine ongoing process"""
        if self.current_process is None or self.current_object is None:
            return
        if answer == "no":
            self.tb = True

        process_map = {
            Process.FAN: ("fans", self.current_object),
            Process.AXIS: ("axis", self.current_object),
            Process.BED_HEATER: ("bheat", "Bed_Heater"),
            Process.EXTRUDER: ("extrude", "extruder"),
        }
        if self.current_process in process_map:
            obj_key, item_key = process_map[self.current_process]
            self.objects[obj_key][item_key] = answer
            if self.current_process in [Process.BED_HEATER, Process.EXTRUDER]:
                self.run_gcode_signal.emit("TURN_OFF_HEATERS")

            if self.current_process is Process.FAN:
                for i in self.objects["fans"]:
                    self.run_gcode_signal.emit(f"SET_FAN_SPEED FAN={i} SPEED=0\nM400")

            self.run_routine(self.current_process)

    def _advance_routine_object(self, obj_list: list) -> bool:
        if not obj_list:
            is_first_run = self.current_object is None
            self.current_object = obj_list[0] if is_first_run and obj_list else "done"
            return is_first_run
        if self.current_object not in obj_list:
            if self.current_process == Process.AXIS:
                self.run_gcode_signal.emit("G28")
                self.run_gcode_signal.emit("G91\nG1 X60 F700")
            self.current_object = obj_list[0]
            return True
        try:
            current_index = obj_list.index(self.current_object)
            if current_index + 1 < len(obj_list):
                self.current_object = obj_list[current_index + 1]
                return True
            else:
                self.current_object = None
                return False
        except ValueError:
            self.current_object = obj_list[0]
            return True

    def _send_routine_gcode(self):
        """Send the correct G-code for the current process and object."""
        if self.current_process == Process.FAN:
            fan_name = self.current_object or next(iter(self.objects["fans"]), None)
            if fan_name:
                if fan_name == "fan":
                    self.run_gcode_signal.emit("M106 S255\nM400")
                else:
                    self.run_gcode_signal.emit(
                        f"SET_FAN_SPEED FAN={fan_name} SPEED=0.8\nM400"
                    )

            return

        gcode_map = {
            Process.BED_HEATER: "SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=60",
            Process.EXTRUDER: "SET_HEATER_TEMPERATURE HEATER=extruder TARGET=60",
            (Process.AXIS, "x"): "G91\nG1 X50 F700\nG1 X-50 F700",
            (Process.AXIS, "y"): "G91\nG1 Y-50 F700\nG1 Y50 F700",
            (Process.AXIS, "z"): "G91\nG1 Z50 F600\nG1 Z-50 F600",
        }

        key = (
            (self.current_process, self.current_object)
            if self.current_process == Process.AXIS
            else self.current_process
        )

        if gcode := gcode_map.get(key):
            self.run_gcode_signal.emit(f"{gcode}\nM400")

    def _setup_ui(self) -> None:
        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))

        self.routines_page = QtWidgets.QWidget()
        self.routines_page.setObjectName("routines_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.routines_page)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem6)
        self.routines_header_layout = QtWidgets.QHBoxLayout()
        self.routines_header_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinimumSize
        )
        self.routines_header_layout.setObjectName("routines_header_layout")
        spacerItem7 = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.routines_header_layout.addItem(spacerItem7)
        self.routines_page_title = QtWidgets.QLabel(parent=self.routines_page)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.routines_page_title.sizePolicy().hasHeightForWidth()
        )
        self.routines_page_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.routines_page_title.setFont(font)
        self.routines_page_title.setStyleSheet("background: transparent; color: white;")
        self.routines_page_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.routines_page_title.setObjectName("routines_page_title")
        self.routines_header_layout.addWidget(self.routines_page_title)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.routine_check_back_btn = IconButton(parent=self.routines_page)
        self.routine_check_back_btn.setSizePolicy(sizePolicy)
        self.routine_check_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.routine_check_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.routine_check_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.routine_check_back_btn.setObjectName("routine_check_back_btn")
        self.routines_header_layout.addWidget(self.routine_check_back_btn)
        self.verticalLayout.addLayout(self.routines_header_layout)

        spacerItem8 = QtWidgets.QSpacerItem(
            20,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem8)
        self.routines_content_layout = QtWidgets.QGridLayout()
        self.routines_content_layout.setVerticalSpacing(20)
        self.routines_content_layout.setObjectName("routines_content_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        self.rc_bheat = BlocksCustomButton(parent=self.routines_page)
        self.rc_bheat.setSizePolicy(sizePolicy)
        self.rc_bheat.setFont(font)
        self.rc_bheat.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_bheat.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_bheat.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(
                ":/temperature_related/media/btn_icons/temperature_plate.svg"
            ),
        )
        self.rc_bheat.setObjectName("rc_bheat")
        self.routines_content_layout.addWidget(self.rc_bheat, 0, 1, 1, 1)

        self.rc_fans = BlocksCustomButton(parent=self.routines_page)
        self.rc_fans.setSizePolicy(sizePolicy)
        self.rc_fans.setFont(font)
        self.rc_fans.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_fans.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_fans.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/fan_related/media/btn_icons/fan_cage.svg")
        )
        self.rc_fans.setObjectName("rc_fans")
        self.routines_content_layout.addWidget(self.rc_fans, 0, 0, 1, 1)

        self.rc_axis = BlocksCustomButton(parent=self.routines_page)
        self.rc_axis.setSizePolicy(sizePolicy)
        self.rc_axis.setFont(font)
        self.rc_axis.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_axis.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_axis.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/motion/media/btn_icons/axis_maintenance.svg"),
        )
        self.rc_axis.setObjectName("rc_axis")
        self.routines_content_layout.addWidget(self.rc_axis, 1, 1, 1, 1)

        self.rc_ext = BlocksCustomButton(parent=self.routines_page)
        self.rc_ext.setSizePolicy(sizePolicy)
        self.rc_ext.setFont(font)
        self.rc_ext.setMinimumSize(QtCore.QSize(250, 80))
        self.rc_ext.setMaximumSize(QtCore.QSize(250, 80))
        self.rc_ext.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/extruder_related/media/btn_icons/nozzle.svg"),
        )
        self.rc_ext.setObjectName("rc_ext")
        self.routines_content_layout.addWidget(self.rc_ext, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.routines_content_layout)
        spacerItem9 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout.addItem(spacerItem9)

        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.routines_page_title.setText(
            _translate("utilitiesStackedWidget", "Routine Check")
        )
        self.routines_page_title.setProperty(
            "class", _translate("utilitiesStackedWidget", "title_text")
        )
        self.routine_check_back_btn.setText(
            _translate("utilitiesStackedWidget", "Back")
        )
        self.routine_check_back_btn.setProperty(
            "class", _translate("utilitiesStackedWidget", "menu_btn")
        )
        self.routine_check_back_btn.setProperty(
            "button_type", _translate("utilitiesStackedWidget", "icon")
        )
        self.rc_bheat.setText(_translate("utilitiesStackedWidget", "Bed Heater"))
        self.rc_bheat.setProperty(
            "class", _translate("utilitiesStackedWidget", "menu_btn")
        )
        self.rc_fans.setText(_translate("utilitiesStackedWidget", "Fans"))
        self.rc_fans.setProperty(
            "class", _translate("utilitiesStackedWidget", "menu_btn")
        )
        self.rc_axis.setText(_translate("utilitiesStackedWidget", "Axis"))
        self.rc_axis.setProperty(
            "class", _translate("utilitiesStackedWidget", "menu_btn")
        )
        self.rc_ext.setText(_translate("utilitiesStackedWidget", "Extruder"))
        self.rc_ext.setProperty(
            "class", _translate("utilitiesStackedWidget", "menu_btn")
        )
