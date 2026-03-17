import typing
from enum import Enum, auto


from lib.moonrakerComm import MoonWebSocket

from lib.printer import Printer

# from lib.ui.utilitiesStackedWidget_ui import Ui_utilitiesStackedWidget
from lib.utils.blocks_button import BlocksCustomButton
from PyQt6 import QtCore, QtGui, QtWidgets

from lib.panels.widgets.optionCardWidget import OptionCard
from lib.panels.widgets.basePopup import BasePopup


from lib.panels.widgets.UtilitiesTab.infoPage import InfoPage
from lib.panels.widgets.UtilitiesTab.ledsPage import LedsPage
from lib.panels.widgets.UtilitiesTab.ledssliderPage import LedsSliderPage
from lib.panels.widgets.UtilitiesTab.troubleshootPage import TroubleshootPage
from lib.panels.widgets.UtilitiesTab.inputshaperPage import InputShaperPage
from lib.panels.widgets.UtilitiesTab.inputshaperResultPage import InputShaperResultsPage
from lib.panels.widgets.UtilitiesTab.axismaintPage import AxisMaintenancePage
from lib.panels.widgets.UtilitiesTab.routineCheckPage import RoutineCheckPage
class Process(Enum):
    FAN = auto()
    AXIS = auto()
    BED_HEATER = auto()
    EXTRUDER = auto()
    AXIS_MAINTENANCE = auto()


class UtilitiesTab(QtWidgets.QStackedWidget):
    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    request_change_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, int, name="request-change-page"
    )
    request_available_objects_signal: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="get-available-objects")
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    request_numpad_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int,
        str,
        str,
        "PyQt_PyObject",
        QtWidgets.QStackedWidget,
        name="request-numpad",
    )
    subscribe_config: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [list, "PyQt_PyObject"],
        [str, "PyQt_PyObject"],
        name="on-subscribe-config",
    )
    on_update_message: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="handle-update-message"
    )

    update_available: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="update-available"
    )

    show_update_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="show-update-page"
    )

    on_object_list  = QtCore.pyqtSignal(list, name="on-object-list")

    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")

    def __init__(
        self, parent: QtWidgets.QWidget, ws: MoonWebSocket, printer: Printer
    ) -> None:
        super().__init__(parent)

        self._setupUi()

        self.ws = ws
        self.printer: Printer = printer
        self.troubleshoot_page: TroubleshootPage = TroubleshootPage(self)

        # --- State Variables ---
        self.objects: dict = {
            "fans": {},
            "axis": {"x": "indf", "y": "indf", "z": "indf"},
            "bheat": {"Bed_Heater": "indf"},
            "extrude": {"extruder": "indf"},
            "leds": {},
        }
        self.x_inputshaper: dict = {}
        self.stepper_limits: dict = {}

        self.current_object: typing.Optional[str] = None
        self.current_process: typing.Optional[Process] = None
        self.axis_in: str = "x"
        self.amount: int = 1
        self.tb: bool = False
        self.cg = None
        self.aut: bool = False

        # --- UI Setup ---

        self.run_gcode_signal.connect(self.ws.api.run_gcode)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self.info_page = InfoPage(self)
        self.addWidget(self.info_page)
        self.info_page.request_back.connect(self.request_back_button)


        self.leds_slider_page = LedsSliderPage(self)
        self.addWidget(self.leds_slider_page)
        self.leds_slider_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.leds_slider_page.request_back.connect(lambda:self.request_back_button.emit())
        self.leds_slider_page.request_change_page.connect(self.change_page)


        self.leds_page = LedsPage(self)
        self.addWidget(self.leds_page)
        self.on_object_list.connect(self.leds_page.on_object_list)
        self.leds_page.request_ledslider_page.connect(self.on_leds_slider_request)
        self.leds_page.request_back.connect(lambda:self.request_back_button.emit())


        self.is_page = InputShaperResultsPage(self)
        self.addWidget(self.is_page)
        self.printer.gcode_response.connect(self.is_page.handle_gcode_response)
        self.is_page.call_load_panel.connect(self.call_load_panel)
        self.is_page.run_gcode_signal.connect(self.run_gcode_signal)


        self.input_shaper_page = InputShaperPage(self)
        self.addWidget(self.input_shaper_page)
        self.input_shaper_page.request_is_results_page.connect(lambda:self.change_page(self.indexOf(self.is_page)))
        self.input_shaper_page.request_back_button.connect(lambda:self.change_page(0))
        self.input_shaper_page.run_gcode_signal.connect(self.run_gcode_signal)
        self.input_shaper_page.call_load_panel.connect(self.call_load_panel)
        self.input_shaper_page.set_aut.connect(self.is_page.set_aut)

        self.axis_page = AxisMaintenancePage(self)
        self.addWidget(self.axis_page)
        self.axis_page.request_back_button.connect(self.request_back_button)
        self.axis_page.set_dialog_popup.connect(self.set_dialog_axismaintenace_popup)
        self.axis_page.show_waiting_page.connect(self.show_waiting_page)
        self.axis_page.call_load_panel.connect(self.call_load_panel)


        self.routine_check_page = RoutineCheckPage(self)
        self.addWidget(self.routine_check_page)
        self.routine_check_page.request_back_button.connect(self.request_back_button)

        self.utilities_info_btn.clicked.connect(lambda:self.change_page(self.indexOf(self.info_page)))
        self.utilities_leds_btn.clicked.connect(lambda:self.change_page(self.indexOf(self.leds_page)))
        self.utilities_axes_btn.clicked.connect(lambda:self.change_page(self.indexOf(self.axis_page)))
        self.utilities_routine_check_btn.clicked.connect(lambda: self.change_page(self.indexOf(self.routine_check_page)))
        self.utilities_input_shaper_btn.clicked.connect(lambda:self.change_page(self.indexOf(self.input_shaper_page)))

        self.update_btn.clicked.connect(
            lambda: self.show_update_page[bool].emit(False)
        )

        self.is_page.action_btn.clicked.connect(
            lambda: self.change_page(self.indexOf(self.input_shaper_page))
        )


        self.dialogpopup = BasePopup(self,False,True)
        self.addWidget(self.dialogpopup)




        # # --- Routines ---
        # self.panel.rc_fans.clicked.connect(partial(self.run_routine, Process.FAN))
        # self.panel.rc_bheat.clicked.connect(
        #     partial(self.run_routine, Process.BED_HEATER)
        # )
        # self.panel.rc_ext.clicked.connect(partial(self.run_routine, Process.EXTRUDER))
        # self.panel.rc_axis.clicked.connect(partial(self.run_routine, Process.AXIS))
        # self.panel.rc_no.clicked.connect(self.on_routine_answer)
        # self.panel.rc_yes.clicked.connect(self.on_routine_answer)

        # # --- Axis Maintenance ---
        # self.panel.axis_x_btn.clicked.connect(partial(self.axis_maintenance, "x"))
        # self.panel.axis_y_btn.clicked.connect(partial(self.axis_maintenance, "y"))
        # self.panel.axis_z_btn.clicked.connect(partial(self.axis_maintenance, "z"))


        # --- Websocket/Printer Signals ---

        # self.is_page.run_gcode_signal.connect(self.ws.api.run_gcode)
        self.subscribe_config[str, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )
        self.subscribe_config[list, "PyQt_PyObject"].connect(
            self.printer.on_subscribe_config
        )

        # --- Initialize Printer Communication ---
        self.printer.printer_config.connect(self.on_printer_config_received)
        self.printer.gcode_move_update.connect(self.on_gcode_move_update)



    def on_leds_slider_request(self,led: any,name=str,single=bool):
        self.change_page(self.indexOf(self.leds_slider_page))
        print(led,name)
        self.leds_slider_page.set_slider(led_state=led,name=name,single=single)


    # @QtCore.pyqtSlot(list, name="on_object_list")
    # def on_object_list(self, object_list: list) -> None:
    #     """Handle receiving printer object list"""
    #     self.cg = object_list
    #     for obj in self.cg:
    #         base_name = obj.split()[0]

    #         # Only accept 'fan_generic' or 'fan'
    #         if base_name == "fan_generic" or base_name == "fan":
    #             self.objects["fans"][obj] = "indef"
    #     # self._update_leds_from_config()

    @QtCore.pyqtSlot(dict, name="on_object_config")
    @QtCore.pyqtSlot(list, name="on_object_config")
    def on_object_config(self, config: typing.Union[dict, list]) -> None:
        """Handle receiving printer object configurations"""
        if not config:
            return
        config_items = [config] if isinstance(config, dict) else config
        for item in config_items:
            for key, value in item.items():
                if (
                    key.startswith("stepper_")
                    and isinstance(value, dict)
                    and key not in self.stepper_limits
                ):
                    pos_min = value.get("position_min")
                    pos_max = value.get("position_max")
                    if pos_min is not None or pos_max is not None:
                        self.stepper_limits[key] = {
                            "min": float(pos_min)
                            if pos_min is not None
                            else -float("inf"),
                            "max": float(pos_max)
                            if pos_max is not None
                            else float("inf"),
                        }

    def on_printer_config_received(self, config: dict) -> None:
        """Handle printer configuration"""
        for axis in ("x", "y", "z"):
            self.subscribe_config[str, "PyQt_PyObject"].emit(
                f"stepper_{axis}", self.on_object_config
            )

    @QtCore.pyqtSlot(str, list, name="on_gcode_move_update")
    def on_gcode_move_update(self, name: str, value: list) -> None:
        """Handle gcode move"""
        if not value:
            return
        if name == "gcode_position":
            ...

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
                self.troubleshoot_request()
                self.tb = False
            else:
                ...
                # self.change_page(self.indexOf(self.panel.utilities_page))

            if process == Process.FAN:
                self.run_gcode_signal.emit("M107")
            return

        message = f"Please check if the {self.current_object} is functioning correctly."
        if process == Process.AXIS:
            message = f"Please ensure the {self.current_object} axis moves correctly."
        elif process in [Process.BED_HEATER, Process.EXTRUDER]:
            message = "Please check if the temperature reaches 60°C. \n you may need to wait a few moments."

        # self.set_routine_check_page(
        #     f"Running routine for: {self.current_object}", message
        # )
        # self.show_waiting_page(
        #     self.indexOf(self.panel.rc_page),
        #     f"Please check if the {message}",
        #     10000 if process == Process.AXIS else 0,
        # )
        # self._send_routine_gcode()

    def _advance_routine_object(self, obj_list: list) -> bool:
        if not obj_list:
            is_first_run = self.current_object is None
            self.current_object = obj_list[0] if is_first_run and obj_list else "done"
            return is_first_run
        if self.current_object not in obj_list:
            if self.current_process == Process.AXIS:
                self.run_gcode_signal.emit("G28")
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

    # def on_routine_answer(self) -> None:
    #     """Handle routine ongoing process"""
    #     if self.current_process is None or self.current_object is None:
    #         return
    #     if self.sender() == self.panel.rc_yes:
    #         answer = "yes"
    #     else:
    #         answer = "no"
    #         self.tb = True
    #     process_map = {
    #         Process.FAN: ("fans", self.current_object),
    #         Process.AXIS: ("axis", self.current_object),
    #         Process.BED_HEATER: ("bheat", "Bed_Heater"),
    #         Process.EXTRUDER: ("extrude", "extruder"),
    #     }
    #     if self.current_process in process_map:
    #         obj_key, item_key = process_map[self.current_process]
    #         self.objects[obj_key][item_key] = answer
    #         if self.current_process in [Process.BED_HEATER, Process.EXTRUDER]:
    #             self.run_gcode_signal.emit("TURN_OFF_HEATERS")
    #         self.run_routine(self.current_process)
    #     elif self.current_process == Process.AXIS_MAINTENANCE:
    #         if answer == "yes":
    #             self._run_axis_maintenance_gcode(self.current_object)
    #         else:
    #             self.change_page(self.indexOf(self.panel.axes_page))

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
            (Process.AXIS, "y"): "G91\nG1 Y50 F700\nG1 Y-50 F700",
            (Process.AXIS, "z"): "G91\nG1 Z50 F600\nG1 Z-50 F600",
        }

        key = (
            (self.current_process, self.current_object)
            if self.current_process == Process.AXIS
            else self.current_process
        )

        if gcode := gcode_map.get(key):
            self.run_gcode_signal.emit(f"{gcode}\nM400")

    @QtCore.pyqtSlot(str,"PyQt_PyObject",name="set-dialog-popup")
    def set_dialog_axismaintenace_popup(self,label: str,accept:"PyQt_PyObject",):
        """Set text on routine page"""
        self.dialogpopup.set_message(label)
        self.dialogpopup.accepted.connect(lambda:
            accept
        )


    @QtCore.pyqtSlot(int,str,int,bool,name="show-waiting-page")
    def show_waiting_page(self, page_to_go_to: int, label: str, time_ms: int , popup:bool):
        """Show placeholder page"""
        self.call_load_panel.emit(True, label)
        if popup:
            QtCore.QTimer.singleShot(time_ms, lambda: self.dialogpopup.show())
        else:
            QtCore.QTimer.singleShot(time_ms, lambda: self.change_page(page_to_go_to))






    # def axis_maintenance(self, axis: str) -> None:
    #     """Routine, checks axis movement for printer debugging"""
    #     self.current_process = Process.AXIS_MAINTENANCE
    #     self.current_object = axis
    #     self.run_gcode_signal.emit(f"G28 {axis.upper()}\nM400")
    #     self.set_routine_check_page(
    #         "Axis Maintenance",
    #         f"Insert oil on the {axis.upper()} axis before confirming.",
    #     )
    #     self.show_waiting_page(
    #         self.indexOf(self.panel.rc_page),
    #         f"Homing {axis.upper()} axis...",
    #         5000,
    #     )

    # def _run_axis_maintenance_gcode(self, axis: str):
    #     stepper_key = f"stepper_{axis}"
    #     if stepper_key in self.stepper_limits:
    #         max_pos = self.stepper_limits[stepper_key].get("max", 20)
    #         distance = int(max_pos) - 20
    #         self.run_gcode_signal.emit(
    #             f"G1 {axis.upper()}{distance} F3000\nM400\nG28 {axis.upper()}\nM400"
    #         )
    #         self.show_waiting_page(
    #             self.indexOf(self.panel.axes_page),
    #             f"Running maintenance cycle on {axis.upper()} axis...",
    #             5000,
    #         )
    #     else:
    #         self.change_page(self.indexOf(self.panel.axes_page))

    def troubleshoot_request(self) -> None:
        """Show troubleshoot page"""
        self.troubleshoot_page.show()



    def change_page(self, index: int):
        """Request change page by index"""
        self.request_change_page.emit(3, index)


    def _setupUi(self):
        self.resize(710, 410)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 410))
        self.setMaximumSize(QtCore.QSize(710, 410))
        
        widget = QtWidgets.QWidget()
        widget.setMinimumSize(QtCore.QSize(710, 410))
        widget.setMaximumSize(QtCore.QSize(710, 410))
        widget.setObjectName("utilities_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)

        self.utilities_header_layout = QtWidgets.QHBoxLayout()
        self.utilities_header_layout.setObjectName("utilities_header_layout")

        self.utilities_title_label = QtWidgets.QLabel(parent=self)
        self.utilities_title_label.setSizePolicy(sizePolicy)
        self.utilities_title_label.setMinimumSize(QtCore.QSize(0, 60))
        self.utilities_title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.utilities_title_label.setFont(font)
        self.utilities_title_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.utilities_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.utilities_title_label.setObjectName("utilities_title_label")

        self.utilities_header_layout.addWidget(self.utilities_title_label)
        self.verticalLayout.addLayout(self.utilities_header_layout)
        self.utilities_content_layout = QtWidgets.QGridLayout()

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)

        self.utilities_content_layout.setObjectName("utilities_content_layout")
        self.utilities_axes_btn = BlocksCustomButton(parent=self)
        self.utilities_axes_btn.setSizePolicy(sizePolicy)
        self.utilities_axes_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_axes_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_axes_btn.setFont(font)
        self.utilities_axes_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/motion/media/btn_icons/axis_maintenance.svg"),
        )
        self.utilities_axes_btn.setObjectName("utilities_axes_btn")

        self.utilities_content_layout.addWidget(self.utilities_axes_btn, 1, 1, 1, 1)

        self.update_btn = BlocksCustomButton(parent=self)
        self.update_btn.setSizePolicy(sizePolicy)
        self.update_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.update_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.update_btn.setFont(font)
        self.update_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/system/media/btn_icons/update-software-icon.svg")
        )

        self.update_btn.setObjectName("update_btn")

        self.utilities_content_layout.addWidget(self.update_btn, 2, 0, 1, 1)
        self.utilities_routine_check_btn = BlocksCustomButton(
            parent=self
        )
        self.utilities_routine_check_btn.setSizePolicy(sizePolicy)
        self.utilities_routine_check_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_routine_check_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_routine_check_btn.setFont(font)
        self.utilities_routine_check_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/routine.svg")
        )
        self.utilities_routine_check_btn.setObjectName("utilities_routine_check_btn")

        self.utilities_content_layout.addWidget(
            self.utilities_routine_check_btn, 1, 0, 1, 1
        )

        self.utilities_input_shaper_btn = BlocksCustomButton(parent=self)
        self.utilities_input_shaper_btn.setSizePolicy(sizePolicy)
        self.utilities_input_shaper_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_input_shaper_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_input_shaper_btn.setFont(font)
        self.utilities_input_shaper_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/input_shaper/media/btn_icons/input_shaper.svg"),
        )
        self.utilities_input_shaper_btn.setObjectName("utilities_input_shaper_btn")

        self.utilities_content_layout.addWidget(
            self.utilities_input_shaper_btn, 2, 1, 1, 1
        )

        self.utilities_info_btn = BlocksCustomButton(parent=self)
        self.utilities_info_btn.setSizePolicy(sizePolicy)
        self.utilities_info_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_info_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_info_btn.setFont(font)
        self.utilities_info_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/info.svg")
        )

        self.utilities_info_btn.setObjectName("utilities_info_btn")

        self.utilities_content_layout.addWidget(self.utilities_info_btn, 0, 0, 1, 1)
        self.utilities_leds_btn = BlocksCustomButton(parent=self)
        self.utilities_leds_btn.setSizePolicy(sizePolicy)
        self.utilities_leds_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.utilities_leds_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.utilities_leds_btn.setFont(font)
        self.utilities_leds_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/LEDs.svg")
        )
        self.utilities_leds_btn.setObjectName("utilities_leds_btn")
        self.utilities_content_layout.addWidget(self.utilities_leds_btn, 0, 1, 1, 1)

        self.verticalLayout.addLayout(self.utilities_content_layout)
        
        widget.setLayout(self.verticalLayout)
        self.addWidget(widget)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "StackedWidget"))
        self.utilities_title_label.setText(_translate("self", "Utilities"))
        self.utilities_axes_btn.setText(_translate("self", "Axis\nMaint."))
        self.update_btn.setText(_translate("self", "Update"))
        self.utilities_routine_check_btn.setText(_translate("self", "Routine\nCheck"))
        self.utilities_input_shaper_btn.setText(_translate("self", "Input\nShaper"))
        self.utilities_info_btn.setText(_translate("self", "Info"))
        self.utilities_leds_btn.setText(_translate("self", "LED's"))
