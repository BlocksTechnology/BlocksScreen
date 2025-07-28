import logging
import typing


class LoadFilamentError(Exception):
    """Raised when there was an error during filament loading"""

    def __init__(self, message, errors):
        super(LoadFilamentError, self).__init__(message)
        self.errors = errors


class LoadFilament:
    def __init__(self, config):
        # self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.gcode = self.printer.lookup_object("gcode")

        # * Register Event handlers
        self.printer.register_event_handler("klippy:connect", self.handle_connect)
        self.printer.register_event_handler("klippy:ready", self.handle_ready)

        # * Get configs
        self.has_cutter = config.getboolean("cutter_present", False)
        if self.has_cutter:
            self.cutter_name = config.get("cutter_name")
        self.has_custom_boundary = config.getboolean("has_custom_boundary", False)

        self.min_dist_to_nozzle = config.getfloat(
            "minimum_distance_to_nozzle", 0.1, minval=0.1, maxval=5000.0
        )

        self.park = config.getfloatlist("park_xy", None, count=2)

        self.bucket_position = config.getfloatlist("bucket_position", count=2)
        self.travel_speed = config.getfloat(
            "travel_speed", default=50.0, minval=20.0, maxval=500.0
        )
        self.extrude_speed = config.getfloat(
            "extrude_speed", default=10.0, minval=5.0, maxval=100.0
        )
        self.purge_speed = config.getfloat(
            "purge_speed", default=5.0, minval=2.0, maxval=50.0
        )
        self.purge_distance = config.getfloat(
            "purge_distance", default=1.5, minval=0.5, maxval=20.0
        )
        self.purge_max_retries = config.getint(
            "purge_max_count", default=10, minval=2, maxval=30
        )
        self.belay_present = config.getboolean("belay_present", default=False)
        self.cutter_handles_rest = config.getboolean(
            "cutter_handles_rest", default=False
        )
        self.purge_interval = config.getfloat(
            "purge_timeout", default=3.0, minval=0.1, maxval=5.5
        )
        self.pre_load_gcode = self.post_load_gcode = None
        gcode_macro = self.printer.load_object(config, "gcode_macro")
        if config.get("pre_load_gcode", None) is not None:
            self.pre_load_gcode = gcode_macro.load_template(
                config, "pre_load_gcode", ""
            )
        if config.get("post_load_gcode", None) is not None:
            self.post_load_gcode = gcode_macro.load_template(config, "post_load_gcode")

        self.mainsail_prompt_gcode = (
            "\n//action:prompt_begin Load Filament\n"
            + "//action:prompt_text Purging filament, click button to stop.\n"
            + "//action:prompt_button Stop Purge|PURGE_STOP|error\n"
            + "//action:prompt_show\n"
        )

        self.load_started: bool = False
        if self.has_cutter:
            self.printer.register_event_handler(
                "cutter_sensor:filament_present", self.handle_cutter_filament_present
            )
            self.printer.register_event_handler(
                "cutter_sensor:no_filament", self.handle_cutter_no_filament
            )

        self.current_purge_index: int = 0
        self.extrude_purge_timer = self.reactor.register_timer(
            self.purge_extrude, self.reactor.NEVER
        )
        # self.timer_handler_extrude_to_cutter = self.reactor.register_timer(
        #     self.extruder_alot, self.reactor.NEVER
        # )
        self.extrude_to_cutter_sensor_timer = self.reactor.register_timer(
            self.extrude_to_cutter_sensor, self.reactor.NEVER
        )

        self.gcode.register_command(
            "LOAD_FILAMENT",
            self.cmd_LOAD_FILAMENT,
            "GCODE MACRO to load filament, takes into account if there is a belay and or a filament cutter with a sensor.",
        )
        self.gcode.register_command(
            "PURGE_STOP",
            self.cmd_PURGE_STOP,
            "Helper gcode command that stop filament purging",
        )

    def handle_connect(self):
        self.toolhead = self.printer.lookup_object("toolhead")

    def handle_ready(self):
        self.min_event_systime = self.reactor.monotonic() + 2.0
        if self.has_cutter and self.cutter_name is not None:
            self.cutter_object = self.printer.lookup_object(
                f"cutter_sensor {self.cutter_name}"
            )
        if self.has_custom_boundary:
            self.custom_boundary_object = self.printer.lookup_object("bed_custom_bound")

    def handle_cutter_filament_present(self, eventtime=None):
        # * The cutter sensor detected the filament, i can now extrude to the nozzle and perform the purge loop
        if self.load_started:
            self.gcode.respond_info(
                "Cutter sensor on loading -> filament present, stopping extrude to cutter sensor"
            )
            # TODO: ! Experimental
            # self.toolhead.lookahead.flush()
            # self.toolhead.lookahead.reset()
            # self.toolhead.lookahead.set_flush_time(self.reactor.NOW)

            # * Filament is present here so i can extrude a good amount first
            self.reactor.update_timer(
                self.extrude_to_cutter_sensor_timer, self.reactor.NEVER
            )

            self.toolhead.wait_moves()
            # * Purge little by little for convenience
            self.gcode.respond_info("Starting purge loop")
            self.reactor.update_timer(self.extrude_purge_timer, self.reactor.NOW)

    def handle_cutter_no_filament(self, eventtime=None):
        if self.load_started:
            self.gcode.respond_info("Cutter sensor on loading -> starting purge loop")
            self.reactor.update_timer(self.extrude_purge_timer, self.reactor.NOW)

    def extrude_to_cutter_sensor(self, eventtime):
        if self.cutter_object is not None and not self.cutter_object.filament_present:
            self.move_extruder_mm(distance=10, speed=self.extrude_speed, wait=False)
        return eventtime + float((10 / self.extrude_speed))

    def purge_extrude(self, eventtime):
        if self.current_purge_index > self.purge_max_retries:
            self.current_purge_index = 0
            self.gcode.respond_info("Purge limit reached, ending load routine.")
            self.reactor.register_callback(self._purge_end)
            return eventtime + self.reactor.NEVER
        # * Extrude continuously until someone says to stop it
        self.move_extruder_mm(distance=self.purge_distance, speed=self.purge_speed)
        self.current_purge_index += 1
        return eventtime + float(self.purge_interval)

    def create_mainsail_prompt(self):
        # * create gcode template
        self._exec_gcode(self.mainsail_prompt_gcode)

    def cmd_PURGE_STOP(self, gcmd):
        self._purge_end()

    def _purge_end(self, eventtime=None):
        self.reactor.update_timer(
            self.extrude_purge_timer, self.reactor.NEVER
        )  # Stop purging
        self.load_started = False
        # * Move to zero position
        if self.park is not None:
            self.toolhead.manual_move([self.park[0], self.park[1]], self.travel_speed)
            self.toolhead.wait_moves()

        self.heat_and_wait(0, wait=False)
        if (
            self.has_custom_boundary
            and self.custom_boundary_object is not None
            and self.custom_boundary_object.get_status()["status"] == "default"
        ):
            # * Restore the boundary to the custom one
            self.custom_boundary_object.set_custom_boundary()

        # * stop mainsail prompt
        self._exec_gcode("//action:prompt_end")
        self._exec_gcode("RESTORE_GCODE_STATE NAME=LOAD_FILAMENT_state")
        # * Run post load filament gcode
        if self.post_load_gcode is not None:
            self._exec_gcode(self.post_load_gcode)
            self.toolhead.wait_moves()

        if self.printer.lookup_object("gcode_macro CLEAN_NOZZLE") is not None:
            # * Clean the nozzle after the loading if there is gcode macro for that
            self.gcode.run_script_from_command("CLEAN_NOZZLE")

    def cmd_LOAD_FILAMENT(self, gcmd):     
        # * Save printer gcode state
        temp = gcmd.get("TEMPERATURE", 220.0, parser=float, minval=210, maxval=250)
        try:
            self.home_if_needed()
            self._exec_gcode("SAVE_GCODE_STATE NAME=LOAD_FILAMENT_state\nM400")
            self.load_started = True

            self.printer.send_event("load_filament:start")

            if self.has_custom_boundary:
                self.gcode.respond_info("has custom boundary restoring default ")
                # * The limits might be set and there is no way to reach the bucket, restore the default boundary here then set the custom one later
                self.custom_boundary_object.restore_default_boundary()
                 

            # * Run pre load filament gcode commands
            if self.pre_load_gcode is not None:
                self._exec_gcode(self.pre_load_gcode)
                # self.toolhead.wait_moves()

            # * Start heating the extruder.
            self.heat_and_wait(temp, wait=False)
            # * Home if needed

            # * Go to bucket position
            self.move_to_bucket()

            # * Actually wait for the temperature here
            self.heat_and_wait(temp, wait=True)
            self.toolhead.wait_moves()

            # * Increase max extrude distance if needed
            extruder = self.toolhead.get_extruder()
            _old_extrude_min_dist = None
            if extruder.max_e_dist < self.min_dist_to_nozzle:
                _old_extrude_min_dist = extruder.max_e_dist
                extruder.max_e_dist = self.min_dist_to_nozzle + 10.0
                self.gcode.respond_info(
                    f"Changed extrude distance to {self.min_dist_to_nozzle + 10.0}"
                )

            if self.cutter_handles_rest:
                self.reactor.update_timer(
                    self.extrude_to_cutter_sensor_timer, self.reactor.NOW
                )
            self.toolhead.wait_moves()
            self.create_mainsail_prompt()

            if not self.cutter_handles_rest:
                # * Restore printer gcode state
                self._exec_gcode("RESTORE_GCODE_STATE NAME=LOAD_FILAMENT_state")

                # * Run post load filament gcode
                if self.post_load_gcode is not None:
                    self._exec_gcode(self.post_load_gcode)
                    self.toolhead.wait_moves()

            # * Restore extruder min extrude distance
            if _old_extrude_min_dist is not None:
                extruder.max_e_dist = _old_extrude_min_dist

        except LoadFilamentError as e:
            logging.error(f"Error loading filament : {e}")

    def move_extruder_mm(self, distance=10.0, speed=30.0, wait=True):
        """Move the extruder

        Args:
            distance (float): The distance in mm to move the extruder.
        """
        try:
            eventtime = self.reactor.monotonic()
            gcode_move = self.printer.lookup_object("gcode_move")

            prev_pos = self.toolhead.get_position()

            v = distance * gcode_move.get_status(eventtime)["extrude_factor"]
            # new_distance = v + gcode_move.get_status(eventtime)["position"][3]
            new_distance = v + prev_pos[3]

            self.toolhead.move(
                [prev_pos[0], prev_pos[1], prev_pos[2], new_distance], speed
            )
            self.gcode.respond_info(f"Extruding -> {distance} mm. Speed -> {speed}")
            if wait:
                self.toolhead.wait_moves()
        except Exception:
            raise Exception("fucked up extrusion")
            return False
        return True

    def move_to_bucket(self, split: typing.Optional["bool"] = False):
        """Moves to bucket position"""
        if self.toolhead is None:
            return

        # * Maybe check if the move is within the printers boundaries

        if not split:
            self.toolhead.manual_move(
                [self.bucket_position[0], self.bucket_position[1]], self.travel_speed
            )
        else:
            self.toolhead.manual_move([self.bucket_position[0]], self.travel_speed)
            self.toolhead.wait_moves()
            self.toolhead.manual_move([self.bucket_position[1]], self.travel_speed)

        self.toolhead.wait_moves()

    def move_to_home_pos(self):
        if self.toolhead is None:
            return

        self.toolhead.manual_move([self.park[0], self.park[1]], self.travel_speed)
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
        except Exception as e:
            logging.error(f"Unable to home for somereason on load filament: {e}")

    def heat_and_wait(self, temp, wait: typing.Optional["bool"] = False):
        """Heats the extruder and wait.

        Method returns when  temperature is [temp - 5 ; temp + 5].
        Args:
            temp (float):
                Target temperature in Celsios.
            wait (bool, optional):
                Weather to wait or not for the temperature to reach the interval . Defaults to True
        """

        eventtime = self.reactor.monotonic()
        extruder = self.toolhead.get_extruder()
        pheaters = self.printer.lookup_object("heaters")
        self.gcode.respond_info(f"Setting hotend temperature to : {temp}ºC")
        pheaters.set_temperature(extruder.get_heater(), temp, False)

        extruder_heater = extruder.get_heater()

        while not self.printer.is_shutdown() and wait:
            self.gcode.respond_info("Waiting for temperature to stabilize.")
            heater_temp, target = extruder_heater.get_temp(eventtime)
            if heater_temp >= (temp - 5) and heater_temp <= (temp + 5):
                return

            print_time = self.toolhead.get_last_move_time()
            eventtime = self.reactor.pause(eventtime + 1.0)

    def _exec_gcode(self, template):
        try:
            self.gcode.run_script(template.render() + "\nM400")
        except Exception:
            logging.exception("Error running gcode script on load_filament.py")
        self.min_event_systime = self.reactor.monotonic() + 2.0


def load_config(config):
    return LoadFilament(config)
