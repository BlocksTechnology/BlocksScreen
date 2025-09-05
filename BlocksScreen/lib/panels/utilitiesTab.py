from lib.utils.blocks_button import BlocksCustomButton


from lib.ui.utilitiesStackedWidget_ui import Ui_utilitiesStackedWidget
from PyQt6.QtCore import pyqtSignal, QTimer, Qt, pyqtSlot

from PyQt6.QtWidgets import QStackedWidget
from PyQt6 import QtGui, QtCore ,QtWidgets

import csv
from functools import partial
from lib.moonrakerComm import MoonWebSocket




class UtilitiesTab(QStackedWidget):
    request_back_button_pressed = pyqtSignal(
        name="request_back_button_pressed"
    )

    request_change_page = pyqtSignal(int, int, name="request_change_page")

    request_available_objects_signal = pyqtSignal(name="get_available_objects")

    run_gcode_signal = pyqtSignal(str, name="run_gcode")

    request_numpad_signal = pyqtSignal(
        int,
        str,
        str,
        "PyQt_PyObject",
        QStackedWidget,
        name="request_numpad",
    )

    def __init__(
        self,parent: QtWidgets.QWidget, ws: MoonWebSocket
    ) -> None:
        super().__init__(parent)

        self.panel = Ui_utilitiesStackedWidget()
        self.panel.setupUi(self)

        self.objects = {
            "fans": {},
            "axis": {"x": "indf", "y": "indf", "z": "indf"},
            "bheat": {"Bed_Heater": "indf"},
            "extrude": {"extruder": "indf"},
            "leds": {},
        }
        self.x_inputshaper = {
            "am_zv": {},
            "am_mzv": {},
            "am_ei": {},
            "am_2hump_ei": {},
            "am_3hump_ei": {},
            "am_user_input": {},
        }

        self.ws = ws

        self.current_object = None
        self.current_process = None
        self.resonance_test_state = "x"
        self.index_count = 0
        self.ammount = 1

        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)


        # self.run_gcode_signal.connect(self.ws.api.run_gcode)


        self.panel.leds_r_slider.valueChanged.connect(self.update_led_values)
        self.panel.leds_g_slider.valueChanged.connect(self.update_led_values)
        self.panel.leds_b_slider.valueChanged.connect(self.update_led_values)
        self.panel.leds_w_slider.valueChanged.connect(self.update_led_values)
        self.panel.leds_off_btn.clicked.connect(self.offonbutton)
        self.panel.leds_on_btn.clicked.connect(self.offonbutton)
        self.panel.axes_back_btn.clicked.connect(lambda: self.change_page(0))
        self.panel.am_confirm.clicked.connect(self.is_select)
        self.panel.is_back_btn.clicked.connect(lambda: self.change_page(7))
        self.panel.is_confirm_btn.clicked.connect(lambda: self.change_page(0))
        self.panel.leds_back_btn.clicked.connect(lambda: self.change_page(0))
        self.panel.info_back_btn.clicked.connect(lambda: self.change_page(0))
        self.panel.rc_fans.clicked.connect(lambda: self.routines("fans"))
        self.panel.rc_bheat.clicked.connect(lambda: self.routines("bheat"))
        self.panel.rc_ext.clicked.connect(lambda: self.routines("extrude"))
        self.panel.rc_axis.clicked.connect(lambda: self.routines("axis"))
        self.panel.rc_no.clicked.connect(self.rc_answer)
        self.panel.rc_yes.clicked.connect(self.rc_answer)
        self.panel.am_cancel.clicked.connect(lambda: self.change_page(0))

        self.panel.leds_slider_back_btn.clicked.connect(
            lambda: self.change_page(2)
        )
        self.panel.utilities_axes_btn.clicked.connect(
            lambda: self.change_page(5)
        )
        self.panel.axis_x_btn.clicked.connect(
            lambda: self.axis_maintenance("x")
        )
        self.panel.axis_y_btn.clicked.connect(
            lambda: self.axis_maintenance("y")
        )
        self.panel.axis_z_btn.clicked.connect(
            lambda: self.axis_maintenance("z")
        )
        self.panel.utilities_input_shaper_btn.clicked.connect(
            lambda: self.change_page(6)
        )
        self.panel.input_shaper_back_btn.clicked.connect(
            lambda: self.change_page(0)
        )
        self.panel.is_X_startis_btn.clicked.connect(
            lambda: self.run_resonance_test("x")
        )
        self.panel.is_Y_startis_btn.clicked.connect(
            lambda: self.run_resonance_test("y")
        )
        self.panel.utilities_info_btn.clicked.connect(
            lambda: self.change_page(1)
        )
        self.panel.utilities_routine_check_btn.clicked.connect(
            lambda: self.change_page(3)
        )
        self.panel.routine_check_back_btn.clicked.connect(
            lambda: self.change_page(0)
        )
        self.panel.utilities_leds_btn.clicked.connect(
            lambda: self.change_page(2)
        )
        self.panel.isc_btn_group.buttonClicked.connect(self.braed)

        self.panel.isui_fq.clicked.connect(
            lambda: self.request_numpad_signal.emit(
                3,
                "frequency",
                "Frequency",
                self.handle_numpad_change,
                self,
            )
        )
        self.panel.isui_sm.clicked.connect(
            lambda: self.request_numpad_signal.emit(
                3,
                "smoothing",
                "Smoothing",
                self.handle_numpad_change,
                self,
            )
        )

    def braed(self, button):
        self.ammount = int(button.text())

    def handle_numpad_change(self, name: str, new_value: int | float):
        print(name)
        if name == "frequency":
            self.panel.isui_fq.setText("Frequency: "+str(new_value) + " Hz")
        if name == "smoothing":
            self.panel.isui_sm.setText("Smoothing: "+str(new_value))

    def routines(self, routine: str):
        axis_list = list(self.objects.get("axis", {}).keys())
        fan_list = list(self.objects.get("fans", {}).keys())
        if routine == "fans":
            self.current_process = "fan"

            if (
                self.current_object is None
                or self.current_object not in fan_list
            ):
                self.current_object = fan_list[0]
            else:
                current_index = fan_list.index(self.current_object)
                if current_index + 1 < len(fan_list):
                    self.current_object = fan_list[current_index + 1]
                else:
                    self.setCurrentIndex(3)
                    self.current_object = None
                    self.run_gcode_signal.emit("M107\nM400")
                    return

            self.rc_page(f"Running routine for: {self.current_object}", "")
            self.waiting_page(
                4,
                f"Running routine for: {self.current_object}",
                "Please check if the fan is spinning",
                5000,
            )
            self.rc_gcode("fans", self.current_object, 0.5)

        elif routine == "axis":
            self.current_process = "axis"

            if (
                self.current_object is None
                or self.current_object not in axis_list
            ):
                self.run_gcode_signal.emit("G28\nM400")
                self.current_object = axis_list[0]
            else:
                current_index = axis_list.index(self.current_object)
                if current_index + 1 < len(axis_list):
                    self.current_object = axis_list[current_index + 1]
                else:
                    self.setCurrentIndex(3)
                    self.current_object = None
                    return
            self.rc_page(f"Running routine for: {self.current_object}", "")
            self.waiting_page(
                4,
                f"Running routine for: {self.current_object}",
                "Please check if the axis is moving",
                10000,
            )
            self.rc_gcode("axis", self.current_object, 0.5)
        elif routine == "bheat":
            self.current_process = "bheat"

            if self.current_object is None:
                self.current_object = "heater_bed"
                self.rc_page("Running Routine for: Bed Heater", "")
                self.waiting_page(
                    4,
                    "Heating the Bed",
                    "Please wait while the bed is heating",
                    10000,
                )
                self.rc_gcode("bheat", self.current_object, 0)
            else:
                self.setCurrentIndex(3)
                self.current_object = None
                return

        elif routine == "extrude":
            self.current_process = "extrude"

            if self.current_object is None:
                self.current_object = "extruder"
                self.rc_page("Running Routine for: Extruder", "")
                self.waiting_page(
                    4,
                    "Extruding Test",
                    "Please wait while extruder is being tested",
                    10000,
                )
                self.rc_gcode("extrude", self.current_object, 0)
            else:
                self.setCurrentIndex(3)
                self.current_object = None
                return

    def rc_answer(self) -> None:
        if self.current_process == "fan":
            if self.sender() == self.panel.rc_yes:
                self.objects["fans"][self.current_object] = "yes"
            elif self.sender() == self.panel.rc_no:
                self.objects["fans"][self.current_object] = "no"
            self.routines("fans")

        elif self.current_process == "axis":
            if self.sender() == self.panel.rc_yes:
                self.objects["axis"][self.current_object] = "yes"
            elif self.sender() == self.panel.rc_no:
                self.objects["axis"][self.current_object] = "no"
            self.routines("axis")

        elif self.current_process == "bheat":
            if self.sender() == self.panel.rc_yes:
                self.objects["bheat"]["Bed_Heater"] = "yes"
            elif self.sender() == self.panel.rc_no:
                self.objects["bheat"]["Bed_Heater"] = "no"
            self.current_object = True
            self.routines("bheat")
            self.run_gcode_signal.emit("TURN_OFF_HEATERS\nM400")

        elif self.current_process == "extrude":
            if self.sender() == self.panel.rc_yes:
                self.objects["extrude"]["extruder"] = "yes"
            elif self.sender() == self.panel.rc_no:
                self.objects["extrude"]["extruder"] = "no"
            self.current_object = True
            self.routines("extrude")
            self.run_gcode_signal.emit("TURN_OFF_HEATERS\nM400")

        elif self.current_process == "axismaintenec":
            if self.sender() == self.panel.rc_yes:
                if self.current_object == "x":
                    distance = int(self.cg["stepper_x"]["position_max"]) - 20
                    self.run_gcode_signal.emit(f"G1 X{distance}\nM400")
                    self.run_gcode_signal.emit("G28 X\nM400")
                    self.waiting_page(
                        5,
                        "axis maintence",
                        "this is waitng page the moment where the x axis move up and dow",
                        5000,
                    )
                elif self.current_object == "y":
                    distance = int(self.cg["stepper_y"]["position_max"]) - 20
                    self.run_gcode_signal.emit(f"G1 Y{distance}\nM400")
                    self.run_gcode_signal.emit("G28 Y\nM400")

                    self.waiting_page(
                        5,
                        "axis maintence",
                        "this is waitng page the moment where the y axis move up and dow",
                        5000,
                    )
                elif self.current_object == "z":
                    distance = int(self.cg["stepper_z"]["position_max"]) - 20
                    self.run_gcode_signal.emit(f"G1 Z{distance}\nM400")
                    self.run_gcode_signal.emit("G28 Z\nM400")

                    self.waiting_page(
                        5,
                        "axis maintence",
                        "this is waitng page the moment where the z axis move up and dow",
                        5000,
                    )

            elif self.sender() == self.panel.rc_no:
                self.change_page(5)

    def rc_gcode(self, process: str, name: str, value: float):
        if process == "fans":
            self.run_gcode_signal.emit("M106 S80")
        elif process == "axis":
            if name == "x":
                distance = int(self.cg["stepper_x"]["position_max"]) - 20
                self.run_gcode_signal.emit(f"G0 X{distance}\nM400")
            if name == "y":
                distance = int(self.cg["stepper_y"]["position_max"]) - 20
                self.run_gcode_signal.emit(f"G0 Y{distance}\nM400")
            if name == "z":
                distance = int(self.cg["stepper_z"]["position_max"]) - 20
                self.run_gcode_signal.emit(f"G0 Z{distance}\nM400")

        elif process == "bheat":
            self.run_gcode_signal.emit(
                "SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=60\nM400"
            )

        elif process == "extrude":
            self.run_gcode_signal.emit(
                "SET_HEATER_TEMPERATURE HEATER=extruder TARGET=60\nM400"
            )

    def rc_page(self, tittle: str, label: str):
        self.panel.rc_tittle.setText(tittle)
        self.panel.rc_label.setText(label)

    def update_led_values(self) -> None:
        # First, get the stored LED values for this object
        self.leds = self.objects["leds"][self.current_object][-1]
        rgb = self.objects["leds"][self.current_object][0]

        self.panel.leds_r_value_label.setText(
            str(self.panel.leds_r_slider.value())
        )
        self.panel.leds_g_value_label.setText(
            str(self.panel.leds_g_slider.value())
        )
        self.panel.leds_b_value_label.setText(
            str(self.panel.leds_b_slider.value())
        )
        self.panel.leds_w_value_label.setText(
            str(self.panel.leds_w_slider.value())
        )

        if rgb == "rgb":
            self.ledslist = [
                self.objects["leds"][self.current_object][0],
                self.panel.leds_r_slider.value(),
                self.panel.leds_g_slider.value(),
                self.panel.leds_b_slider.value(),
                self.panel.leds_w_slider.value(),
                self.leds,
            ]
        elif rgb == "white":
            self.ledslist = [
                self.objects["leds"][self.current_object][0],
                self.objects["leds"][self.current_object][1],
                self.objects["leds"][self.current_object][2],
                self.objects["leds"][self.current_object][3],
                self.panel.leds_w_slider.value(),
                self.leds,
            ]

    def offonbutton(self) -> None:
        if self.objects["leds"][self.current_object][5] == "off":
            self.objects["leds"][self.current_object][5] = "on"
        else:
            self.objects["leds"][self.current_object][5] = "off"
        self.update_led_values()

    def handle_led_button(self, name: str) -> None:
        self.panel.leds_slider_tittle_label.setText(name)
        self.current_object = name
        rgb = self.objects["leds"][self.current_object][0]
        if rgb == "rgb":
            self.panel.leds_w_slider.hide()
            self.panel.leds_r_slider.show()
            self.panel.leds_g_slider.show()
            self.panel.leds_b_slider.show()
            self.panel.leds_r_value_label.show()
            self.panel.leds_g_value_label.show()
            self.panel.leds_b_value_label.show()
            self.panel.leds_w_value_label.hide()

        elif rgb == "white":
            self.panel.leds_r_slider.hide()
            self.panel.leds_g_slider.hide()
            self.panel.leds_b_slider.hide()
            self.panel.leds_w_slider.show()

            self.panel.leds_r_value_label.hide()
            self.panel.leds_g_value_label.hide()
            self.panel.leds_b_value_label.hide()
            self.panel.leds_w_value_label.show()

        self.panel.leds_r_slider.setValue(
            self.objects["leds"][self.current_object][1]
        )
        self.panel.leds_g_slider.setValue(
            self.objects["leds"][self.current_object][2]
        )
        self.panel.leds_b_slider.setValue(
            self.objects["leds"][self.current_object][3]
        )
        self.panel.leds_w_slider.setValue(
            self.objects["leds"][self.current_object][4]
        )

        self.change_page(10)

    def run_resonance_test(self, axis: str) -> None:
        self.axis_in = axis

        for i in range(self.ammount):
            if axis == "x":
                csv_path = "/tmp/resonances_x_axis_data.csv"
                self.run_gcode_signal.emit("SHAPER_CALIBRATE AXIS=X")

            elif axis == "y":
                csv_path = "/tmp/resonances_y_axis_data.csv"
                self.run_gcode_signal.emit("SHAPER_CALIBRATE AXIS=Y")
        self.data = self.parse_shaper_csv(csv_path)
        for entry in self.data:
            shaper = entry["shaper"]
            frequency = entry["frequency"]
            vibrations = entry["vibrations"]
            smoothing = entry["smoothing"]
            max_accel = entry["max_accel"]

            self.panel_attr = f"am_{shaper}"
            if hasattr(self.panel, self.panel_attr):
                getattr(self.panel, self.panel_attr).setText(
                    f"Shaper: {shaper}, Frequency: {frequency}Hz, Vibrations: {vibrations}%\n"
                    f"Smoothing: {smoothing}, Max Accel: {max_accel}mm/sec"
                )
                self.x_inputshaper[self.panel_attr] = {
                    "frequency": frequency,
                    "vibrations": vibrations,
                    "smoothing": smoothing,
                    "max_accel": max_accel,
                }

        self.change_page(7)

    def parse_shaper_csv(self, file_path):
        results = []
        try:
            with open(file_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row.get("shaper") and row.get("freq"):
                        results.append(
                            {
                                "shaper": row["shaper"],
                                "frequency": row["freq"],
                                "vibrations": row.get("vibrations", "N/A"),
                                "smoothing": row.get("smoothing", "N/A"),
                                "max_accel": row.get("max_accel", "N/A"),
                            }
                        )
        except Exception as e:
            print(f"Error parsing CSV {file_path}: {e}")
        return results

    def is_select(self) -> None:
        checked = self.panel.is_btn_group.checkedButton()
        if not checked:
            return

        selected = checked.objectName()

        if selected == "am_user_input":
            self.change_page(8)

        self.x_inputshaper["am_user_input"] = {
            "frequency": self.panel.isui_fq.objectName(),
            "smoothing": self.panel.isui_sm.objectName(),
        }

        for entry in self.data:
            shaper = entry["shaper"]
            frequency = entry["frequency"]
            smoothing = entry["smoothing"]

            self.panel_attr = f"am_{shaper}"
            if selected == self.panel_attr:
                if self.axis_in == "x":
                    self.run_gcode_signal.emit(
                        f"SET_INPUT_SHAPER SHAPER_TYPE={shaper} SHAPER_FREQ_X={frequency} SHAPER_DAMPING_X={smoothing}"
                    )
                elif self.axis_in == "y":
                    self.run_gcode_signal.emit(
                        f"SET_INPUT_SHAPER SHAPER_TYPE={shaper} SHAPER_FREQ_Y={frequency} SHAPER_DAMPING_Y={smoothing}"
                    )
                self.change_page(0)

    def axis_maintenance(self, axis_am: str) -> None:
        self.current_process = "axismaintenec"
        self.current_object = axis_am

        if axis_am == "x":
            self.run_gcode_signal.emit("G28 X\nM400")
            self.current_object = "x"
            self.rc_page(
                "Axis Maintenece",
                "Insert oil on the X axis before confimating",
            )
            self.waiting_page(4, "Axis Maintenece", "homing X axis", 5000)
        elif axis_am == "y":
            self.run_gcode_signal.emit("G28 Y\nM400")
            self.current_object = "y"
            self.rc_page(
                "Axis Maintenece",
                "Insert oil on the Y axis before confimating",
            )
            self.waiting_page(4, "Axis Maintenece", "homing Y axis", 5000)
        elif axis_am == "z":
            self.run_gcode_signal.emit("G28 Z\nM400")
            self.current_object = "z"
            self.rc_page(
                "Axis Maintenece",
                "Insert oil on the Z axis before confimating",
            )
            self.waiting_page(4, "Axis Maintenece", "homing Z axis", 5000)

    # ptg = page to go
    def waiting_page(self, ptg: int, tittle: str, label: str, time: int):
        self.panel.wp_title.setText(tittle)
        self.panel.wp_label.setText(label)
        self.change_page(9)
        QTimer.singleShot(time, lambda: self.change_page(ptg))

    def change_page(self, index: int):
        if index == 10:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.saveleds)
            self.timer.start(3000)

        if index != 10:
            if hasattr(self, "timer") and self.timer.isActive():
                self.timer.stop()

        if index < self.count():
            self.request_change_page.emit(3, index)

    def saveleds(self):
        self.objects["leds"][self.current_object] = self.ledslist

        if self.ledslist[0] == "white":
            if self.ledslist[5] == "off":
                self.run_gcode_signal.emit(
                    f"SET_LED LED={self.current_object} WHITE=0"
                )
            else:
                self.run_gcode_signal.emit(
                    f"SET_LED LED={self.current_object} WHITE={self.ledslist[4] / 255:.2f}"
                )
            print(self.ledslist)
        elif self.ledslist[0] == "rgb":
            if self.ledslist[5] == "off":
                self.run_gcode_signal.emit(
                    "SET_LED LED={self.current_object} RED=0 GREEN=0 BLUE=0 WHITE=0"
                )
            else:
                self.run_gcode_signal.emit(
                    f"SET_LED LED={self.current_object} RED={self.ledslist[1] / 255:.2f} GREEN={self.ledslist[2] / 255:.2f} BLUE={self.ledslist[3] / 255:.2f} WHITE={self.ledslist[4] / 255:.2f}"
                )

    @pyqtSlot(list, name="on_object_list")
    def on_object_list(self, config: dict) -> None:
        self.cg = config
        self.leds_update()
        self.fans_update()

    def fans_update(self):
        for obj in self.cg:
            if "fan" in obj and "pin" not in obj and "controller" not in obj:
                self.objects["fans"][obj] = "indf"

    def leds_update(self):
        layout = self.panel.leds_content_layout
        row = 0
        col = 0
        max_columns = 3
        self.ledslist = ["white", 0, 0, 0, 0, "on"]

        for obj in self.cg:
            if "led" in obj:
                # find a way to check if the ligth is rgb or white and send it to handle led button as "rgb" or "white"
                # if change rgb to white or something else you need to change rgb on "self.ledslist=["rgb",0, 0, 0, 0,"off"]"
                name = obj.split()[1]

                self.objects["leds"][name] = self.ledslist

        # Now add buttons for each LED
        led_objects = list(self.objects["leds"].keys())
        for i, obj in enumerate(led_objects):
            _translate = QtCore.QCoreApplication.translate
            layout = self.panel.leds_content_layout
            button = BlocksCustomButton(parent=self.panel.leds_widget)
            button.setFixedSize(200, 70)
            button.setText(obj)
            button.setProperty(
                "class", _translate("utilitiesStackedWidget", "menu_btn")
            )
            button.setProperty("icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/LEDs.svg"))

            row = i // max_columns
            col = i % max_columns
            layout.addWidget(button, row, col)

            button.clicked.connect(partial(self.handle_led_button, obj))

