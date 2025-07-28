import logging 
import typing 

class UnloadFilament: 
    
    def __init__(self, config): 
        
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.cutter_object = None
        self.custom_boundary_object = None
        self.belay_object = None
        self.min_event_systime = None
        self.toolhead = None
        self.bucket_object = None

        self.printer.register_event_handler("klippy:connect", self.handle_connect)
        self.printer.register_event_handler("klippy:ready", self.handle_ready)

        self.has_cutter = config.getboolean("has_cutter", False)
        self.has_custom_boundary = config.getboolean("has_custom_boundary", False)
        self.has_belay = config.getboolean("has_belay", False)
        self.sensor_name = config.get("filament_sensor_name", default=None)
        self.cutter_name = config.get("cutter_name", default=None)
        self.park = config.getfloatlist("park_xy", None, count=2)
        self.extrude_speed = config.getfloat("extrude_speed", default=10., minval=5., maxval=50.)
        self.purge_speed = config.getfloat("purge_speed", default=5., minval=5., maxval=50.)
        self.purge_max_count = config.getint("purge_max_count", default=2, minval=1, maxval=30)
        self.purge_interval = config.getfloat("purge_interval", default=2., minval=0.1, maxval=5.5)
        self.min_dist_to_nozzle = config.getfloat("minimum_dist_to_nozzle", default=30., minval=20., maxval=3000.)
        self.extrude_speed = config.getfloat("unextrude_speed", default=30., minval=1., maxval=100.)

        self.pre_unload_gcode = self.post_unload_gcode = None
        gcode_macro = self.printer.load_object(config, "gcode_macro")
        if config.get("pre_unload_gcode", None) is not None: 
            self.pre_unload_gcode = gcode_macro.load_template(
                config, "pre_unload_gcode", ""
            )
        if config.get("post_unload_gcode", None) is not None: 
            self.post_unload_gcode = gcode_macro.load_template(
                config, "post_unload_gcode", ""
            )
        
        self.mainsail_prompt_gcode = (
            "\n//action:prompt_begin Load Filament\n"
            + "//action:prompt_text Purging filament, click button to stop.\n"
            + "//action:prompt_button Stop Purge|PURGE_STOP|error\n"
            + "//action:prompt_show\n"
        )
        
        
        self.unload_started: bool = False
        self.current_purge_index: int = 0
        
        
        self.unextrude_timer = self.reactor.register_timer(
            self.unextrude, self.reactor.NEVER
        )
        self.extrude_purge_timer = self.reactor.register_timer(
            self.purge, self.reactor.NEVER
        )
        
        
        if self.has_cutter: 
            self.printer.register_event_handler(
                "cutter_sensor:no-filament", self.handle_cutter_fnp
            )
        
        self.gcode.register_command(
            "UNLOAD_FILAMENT", 
            self.cmd_UNLOAD_FILAMENT, 
            "GCODE Macro to unload filament, takes into account if there is a belay and or a filament cutter with a sensor"
        )
    def handle_connect(self): 
        self.toolhead = self.printer.lookup_object("toolhead")
        self.gcode = self.printer.lookup_object("gcode")

    def handle_ready(self): 
        self.min_event_systime = self.reactor.monotonic() + 2.
        if self.has_custom_boundary: 
            self.custom_boundary_object = self.printer.lookup_object("bed_custom_bound")
            logging.debug("Unload module using custom bed boundary.")
        if self.has_cutter and self.cutter_name is not None: 
            self.cutter_object = self.printer.lookup_object(f"cutter_sensor {self.cutter_name}")        
            logging.debug(f"Unload module using cutter -> {self.cutter_name}.")
        
        if self.printer.lookup_object("bucket") is not None: 
            self.bucket_object = self.printer.lookup_object("bucket")
            logging.debug("There is a bucket object, using it")
        
        if self.sensor_name is not None: 
            self.sensor_object = self.printer.lookup_object(f"filament_switch_sensor {self.sensor_name}")
            logging.debug(f"Unload using filament switch sensor {self.sensor_name} to detect when filament is out of the printer.")

    def handle_cutter_fnp(self, eventtime = None): 
        # * The cutter sensor does not report filament here  
        # * Can extrude to the other sensor 
        if self.unload_started:
            self.reactor.update_timer(self.unextrude_timer, self.reactor.NOW)
            

    def cmd_UNLOAD_FILAMENT(self, gcmd): 
        if self.toolhead is None: 
            return 
        try:
            if self.pre_unload_gcode is not None: 
                self._exec_gcode(self.pre_unload_gcode)

            self.unload_started = True
            # * Increase the max extrude distance if needed 
            extruder = self.toolhead.get_extruder()
            _old_extruder_dist = None
            if extruder.max_e_dist < self.min_dist_to_nozzle: 
                _old_extruder_dist = extruder.max_e_dist
                extruder.max_e_dist = self.min_dist_to_nozzle + 10.
                self.gcode.respond_info(
                    f"Changed extrude distance to {self.min_dist_to_nozzle + 10.} for unload procedure."
                )
                
            if self.cutter_object is not None: 
                # * Just need to perform a cut first, then pull out the filament, 
                # * Cutter additionally indicates when the filament can be pulled.

                pass
        except Exception as e: 
            logging.error(f"Unexpected error while trying to unload filament: {e}.")

    def unextrude(self, eventtime): 
        """Move the extruder to unload"""
        try: 
            self.move_extruder_mm(distance= -10, speed= self.extrude_speed, wait = False)
            return eventtime + float((10/self.extrude_speed))    
        except Exception: 
            logging.error("Error pulling the filament back")
        finally: 
            return self.reactor.NEVER
    
    def move_extruder_mm(self, distance=10.0, speed=30.0, wait=True):
        """Move the extruder

        Args:
            distance (float): The distance in mm to move the extruder.
        """
        if self.toolhead is None: 
            return 

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
        except Exception as e:
            logging.error(f"Exception moving extruder while on Unloading procedure: {e}.")
            raise Exception("fucked up extrusion")
            return False
        return True

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

    def purge(self, eventtime): 
        if self.current_purge_index > self.purge_max_count: 
            self.current_purge_index = 0
            self.gcode.respond_info("Purge limit reached, ending purge.")
            self.reactor.register_callback(self._purge_end)
            return eventtime + self.reactor.NEVER
        

    def _purge_end(self): 
        pass
    
    
    def _exec_gcode(self, template):
        try:
            self.gcode.run_script(template.render() + "\nM400")
        except Exception:
            logging.exception("Error running gcode script on load_filament.py")
        self.min_event_systime = self.reactor.monotonic() + 2.0

def load_config(config): 
    return UnloadFilament(config)