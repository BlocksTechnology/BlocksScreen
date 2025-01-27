import logging
import typing


class CutterSensor:
    def __init__(self, config):
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.gcode = self.printer.lookup_object("gcode")

        # * Register Event handlers
        self.printer.register_event_handler("klippy:connect", self.handle_connect)
        self.printer.register_event_handler("klippy:ready", self.handle_ready)
        # self.printer.register_event_handler(
        #     "idle_timeout:printing", self.handle_printing
        # )

        # * Get Cutter Module parameters / define variables
        self.extrude_length_mm = config.getfloat(
            "extrude_length_mm", 5.0, minval=0.0, maxval=50.0
        )
        self.retract_length_mm = config.getfloat(
            "retract_length_mm", -5.0, minval=-50.0, maxval=-0.5
        )
        self.retract_to_cutter_sensor = config.getfloat(
            "retract_to_sensor_mm", -10.0, minval=-50.0, maxval=-0.5
        )
        self.extrude_speed = config.getfloat(
            "extrude_speed", 2.0, above=0.0, minval=1.0, maxval=50.0
        )
        self.travel_speed = config.getfloat(
            "travel_speed", 100.0, above=0.0, minval=30.0, maxval=600.0
        )
        self.cut_speed = config.getfloat(
            "cut_speed", 100.0, above=50.0, minval=50.0, maxval=300.0
        )
        self.cutter_position = config.getfloatlist("cutter_position_xy", count=2)
        self.pre_cutter_position = config.getfloatlist(
            "pre_cutter_position_xy", count=2
        )
        self.bucked_position_xy = config.getfloatlist(
            "bucket_position_xy", default=None, count=2
        )

        self.runout_gcode = self.insert_gcode = None
        gcode_macro = self.printer.load_object(config, "gcode_macro")
        if config.get("runout_gcode", None) is not None:
            self.runout_gcode = gcode_macro.load_template(config, "runout_gcode", "")
        if config.get("insert_gcode", None) is not None:
            self.insert_gcode = gcode_macro.load_template(config, "insert_gcode")
        self.event_delay = config.getfloat("event_delay", 0.3, above=0.0)

        self.pause_delay = config.getfloat("pause_delay", 0.5, above=0)
        self.runout_pause = config.getboolean("pause_on_runout", False)

        if self.bucked_position_xy is not None:
            self.bucked_position_x, self.bucked_position_y = self.bucked_position_xy
        self.cutter_position_x, self.cutter_position_y = self.cutter_position
        self.pre_cutter_position_x, self.pre_cutter_position_y = (
            self.pre_cutter_position
        )

        self.filament_present: bool = False
        self.sensor_enabled: bool = True
        self.min_event_systime = self.reactor.NEVER

        # * Register button sensor for the cutter filament sensor
        cutter_sensor_pin = config.get("cutter_sensor_pin")
        buttons = self.printer.load_object(config, "buttons")
        buttons.register_buttons([cutter_sensor_pin], self.cutter_sensor_callback)

        # * Register Gcode Commands

        self.gcode.register_mux_command(
            "CUT", "SENSOR", self.name, self.cmd_CUT, self.cmd_CUT_helper
        )
        self.gcode.register_mux_command(
            "QUERY_FILAMENT_SENSOR",
            "SENSOR",
            self.name,
            self.cmd_QUERY_FILAMENT_SENSOR,
            self.cmd_QUERY_FILAMENT_SENSOR_helper,
        )
        self.gcode.register_mux_command(
            "SET_FILAMENT_SENSOR",
            "SENSOR",
            self.name,
            self.cmd_SET_FILAMENT_SENSOR,
            self.cmd_SET_FILAMENT_SENSOR_helper,
        )
       

    cmd_QUERY_FILAMENT_SENSOR_helper = "Query the status of the cutter sensor"
    cmd_SET_FILAMENT_SENSOR_helper = "Query the status of the cutter sensor"

    def handle_connect(self):
        self.toolhead = self.printer.lookup_object("toolhead")

    def handle_ready(self):
        self.min_event_systime = self.reactor.monotonic() + 2.0
        self.custom_boundary_object = self.printer.lookup_object("bed_custom_bound")
        self.load_filament_object = self.printer.lookup_object("load_filament")

    def cmd_QUERY_FILAMENT_SENSOR(self, gcmd):
        if self.filament_present:
            msg = "Cutter Filament Sensor: filament Detected"
        else:
            msg = "Cutter Filament Sensor: filament not detected"
        gcmd.respond_info(msg)

    def cmd_SET_FILAMENT_SENSOR(self, gcmd):
        self.sensor_enabled = gcmd.get_int("ENABLE", 1)

    cmd_CUT_helper = "Routine that handles a cutter on the printer toolhead"

    def cmd_CUT(self, gcmd):
        """Gcode command for the Cutter module

        Call CUT gcode command to perform the filament cutting
        """
        self.home_if_needed()
        self.toolhead.wait_moves()
        eventtime = self.reactor.monotonic()
        kin_status = self.toolhead.get_kinematics().get_status(eventtime)
        return_to_last_pos = gcmd.get("MOVE_TO_LAST_POS", False, parser=bool)
        turn_off_heater = gcmd.get("TURN_OFF_HEATER", False, parser=bool)
        temp = gcmd.get("TEMP", 220.0, parser=float, minval=200, maxval=250)

        if "xyz" not in kin_status["homed_axes"]:
            # Require the printer to be homed
            gcmd.respond_info("Cut requires printer to be homed.", log=True)
            return

        self.prev_pos = (
            self.toolhead.get_position()
        )  # The position where the cutter was called

        # * Heat the extruder
        gcmd.respond_info("Heating Extruder. Waiting.")
        self.heat_and_wait(temp, wait=True)

        if self.bucked_position_xy is not None:
            self.move_to_bucket()

        # * Extrude
        gcmd.respond_info(f"Extruder {self.extrude_length_mm}")
        self.move_extruder_mm(self.extrude_length_mm)
        gcmd.respond_info(f"Extruder {self.retract_length_mm}")
        self.move_extruder_mm(self.retract_length_mm)

        # * Move to cutting pos
        gcmd.respond_info(f"Moving to cutter position: {self.pre_cutter_position}")
        self.move_to_cutter_pos()
        gcmd.respond_info(f"Performing cut: {self.cutter_position}")
        self.cut_move()

        if self.bucked_position_xy is not None:
            self.move_to_bucket()

        # * Push the filament a little down do not to
        gcmd.respond_info(f"Extruding {self.extrude_length_mm} to push filament out.")
        self.move_extruder_mm(-2.0)  # Aliviate the pressure on the blade

        self.move_extruder_mm(self.extrude_length_mm + 2)

        self.move_extruder_mm(float(self.retract_to_cutter_sensor))

        # * Push the filament out of the cutter pos
        if self.prev_pos is not None and return_to_last_pos:
            gcmd.respond_info(
                f"Filament cutting done, moving back to initial position: {self.prev_pos}."
            )
            self.move_back()
            self.toolhead.wait_moves()
            if self.custom_boundary_object is not None:
                self.custom_boundary_object.set_custom_boundary()

        self.toolhead.wait_moves()
        # Cooldown extruder
        gcmd.respond_info("Cut done. Turning off Extruder heater.")

        if turn_off_heater:
            self.heat_and_wait(0, wait=False)

    def move_extruder_mm(self, dist):
        """Move the extruder.

        Args:
            dist (float in mm): The distance in a certain amount.
        """
        curtime = self.reactor.monotonic()
        gcode_move = self.printer.lookup_object("gcode_move")
        # last_move_time = self.toolhead.get_last_move_time()
        v = dist * gcode_move.get_status(curtime)["extrude_factor"]
        new_dist = v + gcode_move.get_status(curtime)["position"][3]
        prev_pos = self.toolhead.get_position()
        self.toolhead.move(
            [prev_pos[0], prev_pos[1], prev_pos[2], new_dist], self.extrude_speed
        )
        self.toolhead.wait_moves()

    def home_if_needed(self):
        if self.toolhead is None:
            return
        try:
            eventtime = self.reactor.monotonic()

            kin = self.toolhead.get_kinematics()
            _homed_axes = kin.get_status(eventtime)["homed_axes"]

            if "xyz" in _homed_axes.lower():
                return
            else:
                self.gcode.respond_info("Homing machine.")
                # completion = self.reactor.register_callback(self._exec_gcode("G28"))
                self.gcode.run_script_from_command("G28")

            self.gcode.respond_info("Waiting for homing.")
            # self.toolhead.wait_moves()
        except Exception as e:
            logging.error(f"Unable to home for somereason on load filament: {e}")

    def heat_and_wait(self, temp, wait: typing.Optional["bool"] = True):
        """Heats the extruder and wait.

        Method returns when  temperature is [temp - 5 ; temp + 5].
        Args:
            temp (float):
                Target temperature in Celsius.
            wait (bool, optional):
                Weather to wait or not for the temperature to reach the interval . Defaults to True
        """
        eventtime = self.reactor.monotonic()
        extruder = self.toolhead.get_extruder()
        pheaters = self.printer.lookup_object("heaters")
        pheaters.set_temperature(extruder.get_heater(), temp, False)

        extruder_heater = extruder.get_heater()

        while not self.printer.is_shutdown() and wait:
            self.gcode.respond_info("Waiting for temperature to stabilize.")
            heater_temp, target = extruder_heater.get_temp(eventtime)
            if heater_temp >= (temp - 5) and heater_temp <= (temp + 5):
                return

            print_time = self.toolhead.get_last_move_time()
            eventtime = self.reactor.pause(eventtime + 1.0)

    def cut_move(self):
        """Performs the cut movement"""
        self.toolhead.manual_move(
            [self.cutter_position_x, self.cutter_position_y], self.travel_speed
        )
        self.toolhead.manual_move(
            [self.pre_cutter_position_x, self.pre_cutter_position_y], self.cut_speed
        )
        self.toolhead.wait_moves()

    def move_to_cutter_pos(self):
        """Moves the toolhead to the pre cutting position"""
        curtime = self.reactor.monotonic()
        kin_status = self.toolhead.get_kinematics().get_status(curtime)

        if "xyz" not in kin_status["homed_axes"]:
            # need to home
            return
        self.toolhead.manual_move(
            [self.pre_cutter_position_x, self.pre_cutter_position_y], self.travel_speed
        )
        self.toolhead.wait_moves()

    def move_to_home(self):
        """Moves to the homing position"""
        gcode_move = self.printer.lookup_object("gcode_move")
        homing_origin = gcode_move.get_status()["homing_origin"]
        self.toolhead.manual_move(homing_origin, self.travel_speed)

    def move_to_bucket(self, split=False):
        """Moves to the bucket position"""
        if self.custom_boundary_object is not None:
            # * Restore original
            self.gcode.respond_info("Restoring original printer Boundaries.")
            self.custom_boundary_object.restore_default_boundary()

        if not split:
            self.toolhead.manual_move(
                [self.bucked_position_x, self.bucked_position_y], self.travel_speed
            )
        else:
            self.toolhead.manual_move([self.bucked_position_x], self.travel_speed)
            self.toolhead.wait_moves()
            self.toolhead.manual_move([self.bucked_position_y], self.travel_speed)

        self.toolhead.wait_moves()

    def move_back(self):
        """Moves back to the original position where the CUT gcode command was called"""
        if self.prev_pos is None:
            return

        self.toolhead.manual_move(
            [self.prev_pos[0], self.prev_pos[1], self.prev_pos[2]], self.travel_speed
        )
        self.toolhead.wait_moves()

    def cutter_sensor_callback(self, eventtime, state):
        """Callback for the change state"""
        # if the state is true, the callback
        if state == self.filament_present:
            return

        self.filament_present = state
        eventtime = self.reactor.monotonic()

        if eventtime < self.min_event_systime or not self.sensor_enabled:
            return

        if self.insert_gcode is None or self.insert_gcode is None:
            return

        # * Determine the printing status
        idle_timeout = self.printer.lookup_object("idle_timeout")
        is_printing = idle_timeout.get_status(eventtime)["state"] == "Printing"

        # * Perform filament action associated with status change (if any)
        # if self.load_filament_object is not None:
        if (
          self.load_filament_object is not None 
          and self.load_filament_object.load_started  
        ):
            if state: 
                self.printer.send_event("cutter_sensor:filament_present")
            else: 
                self.printer.send_event("cutter_sensor:no_filament")

        elif state:
            if (
                not is_printing and self.insert_gcode is not None         
            ):  # Not printing and there is an insert gcode
                self.printer.send_event("cutter_sensor:filament_present")
                # filament inserted detected
                self.min_event_systime = self.reactor.NEVER
                logging.info(
                    f"Cutter filament sensor insert detected, time : {eventtime}"
                )
                self.reactor.register_callback(self._insert_event_handler)

            
        elif (
            not is_printing and self.runout_gcode is not None
        ):  # When not printing and there is a runout gcode
            self.printer.send_event("cutter_sensor:no_filament")
            # Act During printing
            self.min_event_systime = self.reactor.NEVER
            logging.info(
                f"Cutter filament sensor runout detected, while not printing, time: {eventtime}"
            )
            self.reactor.register_callback(self._runout_event_handler)

        elif (
            is_printing and self.runout_gcode is not None
        ):  # When printing and there is a runout gcode
            self.printer.send_event("cutter_sensor:no_filament")
            self.min_event_systime = self.reactor.NEVER
            logging.info(f"Cutter filament sensor runout detected, time: {eventtime}")
            self.reactor.register_callback(self._runout_event_handler)
        

    def _insert_event_handler(self, eventtime):
        self._exec_gcode("", self.insert_gcode)

    def _runout_event_handler(self, eventtime):
        pause_prefix = ""
        if self.runout_pause:
            pause_resume = self.printer.lookup_object("pause_resume")
            pause_resume.send_pause_command()
            pause_prefix = "PAUSE\n"
            self.printer.get_reactor().pause(eventtime + self.pause_delay)
        self._exec_gcode(pause_prefix, self.runout_gcode)

    def _exec_gcode(self, prefix, template):
        """Internal Executes a gcode just like what's in the klipper filament_switch_sensor.py"""

        try:
            self.gcode.run_script(prefix + template.render() + "\nM400")
        except Exception:
            logging.exception("Script running error")
        self.min_event_systime = self.reactor.monotonic() + self.event_delay

    def get_status(self, eventtime):
        """Gets the status of the sensor of the cutter"""
        return {
            "filament_detect": self.filament_present,
            "enabled": self.sensor_enabled,
        }
        

def load_config_prefix(config):
    return CutterSensor(config)
