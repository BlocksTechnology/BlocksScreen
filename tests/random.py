from re import search
import unittest

config = {
    "config": {
        "force_move": {"enable_force_move": "True"},
        "respond": {"default_type": "echo"},
        "gcode_macro G31": {
            "gcode": "\nRUN_SHELL_COMMAND CMD=clear_plr\nSAVE_VARIABLE VARIABLE=was_interrupted VALUE=False"
        },
        "gcode_shell_command clear_plr": {
            "command": "sh /home/mks/clear_plr.sh",
            "timeout": "5.",
        },
        "gcode_macro save_last_file": {
            "gcode": "\n\n{% set svv = printer.save_variables.variables %}\n\n{% set filepath=printer.virtual_sdcard.file_path %}\n\n{% set filename=filepath.split('/')%}\n\nSAVE_VARIABLE VARIABLE=last_file VALUE='\"{ filename[-1] }\"'\nSAVE_VARIABLE VARIABLE=filepath VALUE='\"{ printer.virtual_sdcard.file_path }\"'"
        },
        "gcode_macro clear_last_file": {
            "gcode": "\n{% set filename='' %}\n{% set filepath='' %}\nSAVE_VARIABLE VARIABLE=last_file VALUE='\"{ filename }\"'\nSAVE_VARIABLE VARIABLE=filepath VALUE='\"{ filepath }\"'"
        },
        "gcode_shell_command POWER_LOSS_RESUME": {
            "command": "/home/mks/plr.sh",
            "timeout": "420.",
        },
        "gcode_macro RESUME_INTERRUPTED": {
            "gcode": '\nSET_KINEMATIC_POSITION X=0\nSET_KINEMATIC_POSITION Y=0\nSET_KINEMATIC_POSITION Z=0\n{% set z_height = params.Z_HEIGHT|default(printer.save_variables.variables.power_resume_z)|float %}\n{% set last_file = params.GCODE_FILE|default(printer.save_variables.variables.last_file)|string %}\nm118 {last_file}\n\nRUN_SHELL_COMMAND CMD=POWER_LOSS_RESUME PARAMS="{z_height} \\"{last_file}\\""\nSDCARD_PRINT_FILE FILENAME=plr/"{last_file}"'
        },
        "gcode_macro LOG_Z": {
            "gcode": '\n{% set z_pos = printer.gcode_move.gcode_position.z %}\nRESPOND MSG="Current Z is {z_pos}"\nSAVE_VARIABLE VARIABLE=power_resume_z VALUE={z_pos}'
        },
        "save_variables": {
            "filename": "/home/mks/printer_data/config/saved_variables.cfg"
        },
        "gcode_macro CANCEL_PRINT": {
            "description": "Cancel the actual running print",
            "rename_existing": "CANCEL_PRINT_BASE",
            "gcode": '\nSAVE_VARIABLE VARIABLE=was_interrupted VALUE=False\nRUN_SHELL_COMMAND CMD=clear_plr\nclear_last_file\nG31\nTURN_OFF_HEATERS\nCANCEL_PRINT_BASE\nRESPOND TYPE=echo MSG="Cancel Print Success!"\nG91\nG1 E-2 F500\nG1 E-2 Z0.2 F200\nG1 Z1\nM106 S0\nM104 S0\nM140 S0\nG90\nG1 X10 Y290 F6000\nM84 X Y E',
        },
        "gcode_macro PRINT_START": {
            "gcode": "\n{% set temp = params.EXTRUDER | default(220) | int %}\n{% set b_temp = params.BED | default(60) | int %}\nSAVE_VARIABLE VARIABLE=was_interrupted VALUE=True\n\nM84 E\nSET_HEATER_TEMPERATURE HEATER=heater_bed TARGET={b_temp}\nTEMPERATURE_WAIT SENSOR=heater_bed MINIMUM={b_temp - 5} MAXIMUM={b_temp + 5}\nG28\nBED_MESH_CALIBRATE ADAPTIVE=1\nSET_HEATER_TEMPERATURE HEATER=extruder TARGET={temp}\n\n\nTEMPERATURE_WAIT SENSOR=extruder MINIMUM={temp - 5} MAXIMUM={temp + 5}\n\n\nM400\n\n\nG90\nG92 E0\nG1 E-1\nG92 E0\nM400\n\nG92 E0\nG1 Z1.0 F3000\nG1 X0.1 Y20 Z0.3 F5000.0\nG1 X0.1 Y100.0 Z0.3 F500.0 E15\nG1 X0.4 Y100.0 Z0.3 F5000.0\nG1 X0.4 Y20 Z0.3 F500.0 E30\nG92 E0\nG1 Z1.0 F3000\nM400"
        },
        "gcode_macro PAUSE": {
            "description": "Pause the actual running print",
            "rename_existing": "PAUSE_BASE",
            "gcode": '\nRESPOND TYPE=echo MSG="Pause Print!"\n\n{% set x = params.X|default(10) %}\n{% set y = params.Y|default(290) %}\n{% set z = params.Z|default(10)|float %}\n{% set e = params.E|default(1) %}\n\n{% set max_z = printer.toolhead.axis_maximum.z|float %}\n{% set act_z = printer.toolhead.position.z|float %}\n{% set lift_z = z|abs %}\n{% if act_z < (max_z - lift_z) %}\n{% set z_safe = lift_z %}\n{% else %}\n{% set z_safe = max_z - act_z %}\n{% endif %}\n\nPAUSE_BASE\nG91\n{% if printer.extruder.can_extrude|lower == \'True\' %}\nG1 E-{e} F500\n{% else %}\n{action_respond_info("Extruder not hot enough")}\n{% endif %}\n{% if "xyz" in printer.toolhead.homed_axes %}\nG1 Z{z_safe}\nG90\nG1 X{x} Y{y} F6000\n{% else %}\n{action_respond_info("Printer not homed")}\n{% endif %}',
        },
        "gcode_macro RESUME": {
            "description": "Resume the actual running print",
            "rename_existing": "RESUME_BASE",
            "gcode": '\nRESPOND TYPE=echo MSG="RESUME Print!"\n\n{% if printer["filament_switch_sensor my_sensor"].filament_detected == True %}\nRESPOND TYPE=echo MSG="RESUME Print!"\n{% set e = params.E|default(1) %}\n\n{% if \'VELOCITY\' in params|upper %}\n{% set get_params = (\'VELOCITY=\' + params.VELOCITY) %}\n{%else %}\n{% set get_params = "" %}\n{% endif %}\n\nG91\n{% if printer.extruder.can_extrude|lower == \'True\' %}\nG1 E{e} F400\n{% else %}\n{action_respond_info("Extruder not hot enough")}\n{% endif %}\nRESUME_BASE {get_params}\n{% else %}\nRESPOND TYPE=echo MSG="Please Insert filament in Sensor!"\n{% endif %}',
        },
        "gcode_macro END_PRINT": {
            "gcode": '\nG91\nG1 E-2 F500\nG1 E-2 Z0.2 F200\nG1 X5 Y5 F3000\nG1 Z1\nM106 S0\nM104 S0\nM140 S0\nG90\nG1 X10 Y290\n\nM84 X Y E\nRESPOND TYPE=echo MSG="Finish Print!"'
        },
        "gcode_macro LOAD_FILAMENT": {
            "gcode": "\nSAVE_GCODE_POSITION NAME=LOAD_STATE\nG91\nG1 E30 F300\nG1 E10 F150\nG90\nRESTORE_GCODE_POSITION NAME=LOAD_STATE"
        },
        "gcode_macro UNLOAD_FILAMENT": {
            "gcode": "\nSAVE_GCODE_POSITION NAME=UNLOAD_STATE\nG91\nG1 E-30 F300\nG90\nRESTORE_GCODE_POSITION NAME=UNLOAD_STATE MOVE=0"
        },
        "gcode_macro LED_ON": {"gcode": "\nSET_PIN PIN=my_led VALUE=1"},
        "gcode_macro LED_OFF": {"gcode": "\nSET_PIN PIN=my_led VALUE=0"},
        "gcode_macro M205": {"gcode": "\nM105"},
        "gcode_macro PRINT_END": {
            "gcode": "\nSAVE_VARIABLE VARIABLE=was_interrupted VALUE=False\nRUN_SHELL_COMMAND CMD=clear_plr\nclear_last_file"
        },
        "exclude_object": {},
        "mcu": {
            "serial": "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0",
            "restart_method": "command",
        },
        "printer": {
            "kinematics": "cartesian",
            "max_velocity": "300",
            "max_accel": "10000",
            "max_accel_to_decel": "5000",
            "max_z_velocity": "15",
            "max_z_accel": "100",
            "square_corner_velocity": "6",
        },
        "virtual_sdcard": {"path": "/home/mks/printer_data/gcodes"},
        "pause_resume": {},
        "display_status": {},
        "gcode_arcs": {"resolution": "0.8"},
        "idle_timeout": {
            "gcode": '\nRESPOND TYPE=echo MSG="No operations in 10min!"',
            "timeout": "600",
        },
        "mcu rpi": {"serial": "/tmp/klipper_host_mcu"},
        "adxl345": {"cs_pin": "rpi:None", "spi_bus": "spidev0.0"},
        "verify_heater extruder": {
            "max_error": "60",
            "check_gain_time": "20",
            "hysteresis": "5",
            "heating_gain": "2",
        },
        "verify_heater heater_bed": {
            "max_error": "180",
            "check_gain_time": "120",
            "hysteresis": "5",
            "heating_gain": "2",
        },
        "resonance_tester": {
            "accel_chip": "adxl345",
            "probe_points": "\n150, 150, 20",
            "accel_per_hz": "100",
            "min_freq": "1",
            "max_freq": "100",
            "max_smoothing": "0.2",
            "hz_per_sec": "0.5",
        },
        "stepper_x": {
            "step_pin": "PD15",
            "dir_pin": "PD14",
            "enable_pin": "!PC7",
            "microsteps": "16",
            "rotation_distance": "40",
            "endstop_pin": "tmc2209_stepper_x: virtual_endstop",
            "homing_retract_dist": "0",
            "position_endstop": "-12",
            "position_min": "-12",
            "position_max": "302",
            "homing_speed": "50",
            "step_pulse_duration": "0.000002",
        },
        "tmc2209 stepper_x": {
            "uart_pin": "PE3",
            "run_current": "1.2",
            "uart_address": "3",
            "interpolate": "True",
            "driver_sgthrs": "95",
            "stealthchop_threshold": "0",
            "diag_pin": "^PD10",
        },
        "stepper_y": {
            "step_pin": "PB7",
            "dir_pin": "PB6",
            "enable_pin": "!PB9",
            "microsteps": "16",
            "rotation_distance": "40",
            "endstop_pin": "tmc2209_stepper_y: virtual_endstop",
            "homing_retract_dist": "0",
            "position_endstop": "-6",
            "position_min": "-6",
            "position_max": "302",
            "homing_speed": "50",
            "step_pulse_duration": "0.000002",
        },
        "tmc2209 stepper_y": {
            "uart_pin": "PE4",
            "run_current": "1.2",
            "uart_address": "3",
            "interpolate": "True",
            "driver_sgthrs": "95",
            "stealthchop_threshold": "0",
            "diag_pin": "^PE0",
        },
        "stepper_z": {
            "step_pin": "PB3",
            "dir_pin": "!PD7",
            "enable_pin": "!PB5",
            "microsteps": "16",
            "rotation_distance": "8",
            "endstop_pin": "probe:z_virtual_endstop",
            "position_max": "355",
            "position_min": "-4",
            "homing_speed": "10",
        },
        "stepper_z1": {
            "step_pin": "PA7",
            "dir_pin": "!PA6",
            "enable_pin": "!PC5",
            "microsteps": "16",
            "rotation_distance": "8",
            "endstop_pin": "probe:z_virtual_endstop",
        },
        "extruder": {
            "max_extrude_only_distance": "100.0",
            "step_pin": "PD1",
            "dir_pin": "!PD0",
            "enable_pin": "!PD4",
            "microsteps": "16",
            "rotation_distance": "4.59",
            "nozzle_diameter": "0.400",
            "filament_diameter": "1.750",
            "heater_pin": "PA1",
            "sensor_type": "EPCOS 100K B57560G104F",
            "sensor_pin": "PA4",
            "control": "pid",
            "pressure_advance": "0.02",
            "pressure_advance_smooth_time": "0.035",
            "max_extrude_cross_section": "500",
            "instantaneous_corner_velocity": "10",
            "max_extrude_only_velocity": "2000",
            "max_extrude_only_accel": "10000",
            "pid_kp": "24.522",
            "pid_ki": "1.397",
            "pid_kd": "107.590",
            "min_temp": "0",
            "max_temp": "305",
            "min_extrude_temp": "150",
        },
        "tmc2209 extruder": {
            "uart_pin": "PE7",
            "run_current": "0.6",
            "uart_address": "3",
            "interpolate": "True",
        },
        "heater_bed": {
            "heater_pin": "PA2",
            "sensor_type": "EPCOS 100K B57560G104F",
            "sensor_pin": "PA3",
            "control": "pid",
            "pid_kp": "54.027",
            "pid_ki": "0.770",
            "pid_kd": "948.182",
            "min_temp": "0",
            "max_temp": "105",
        },
        "probe": {
            "pin": "PD13",
            "x_offset": "27",
            "y_offset": "-20",
            "z_offset": "2.465",
        },
        "bltouch": {"#guov": 2039},
        "probe_eddy_current": {"falsk": 329}, 
        "filament_switch_sensor my_sensor": {"switch_pin": "PD11"},
        "safe_z_home": {
            "home_xy_position": "123,170",
            "speed": "80",
            "z_hop": "10",
            "z_hop_speed": "15",
            "move_to_previous": "True",
        },
        "z_tilt": {
            "z_positions": "-8, 170\n260, 170",
            "points": "-8, 170\n260, 170",
            "speed": "200",
            "horizontal_move_z": "5",
            "retries": "20",
            "retry_tolerance": ".005",
        },
        "bed_mesh": {
            "speed": "200",
            "horizontal_move_z": "5",
            "mesh_min": "17,15",
            "mesh_max": "285,282",
            "probe_count": "5,5",
            "algorithm": "bicubic",
            "bicubic_tension": "0.3",
            "fade_start": "0.2",
            "fade_end": "5.0",
            "mesh_pps": "4,4",
            "move_check_distance": "3",
            "adaptive_margin": "5",
        },
        "screws_tilt_adjust": {
            "screw1": "4, 58",
            "screw1_name": "front left screw",
            "screw2": "243, 58",
            "screw2_name": "front right screw",
            "screw3": "243, 290",
            "screw3_name": "rear right screw",
            "screw4": "4, 290",
            "screw4_name": "rear left screw",
            "horizontal_move_z": "5.",
            "speed": "200.",
            "screw_thread": "CW-M4",
        },
        "heater_fan hotend_fan": {"pin": "PE11"},
        "multi_pin fan_pins": {"pins": "PE9,PE13"},
        "fan": {"pin": "multi_pin:fan_pins"},
        "output_pin my_led": {
            "pin": "PC4",
            "pwm": "1",
            "value": "1",
            "cycle_time": "0.010",
        },
        "controller_fan Fan_Board": {
            "pin": "PD3",
            "fan_speed": "1.0",
            "idle_timeout": "120",
            "heater": "heater_bed, extruder",
            "stepper": "stepper_x, stepper_y, stepper_z, stepper_z1",
        },
        "input_shaper": {
            "damping_ratio_x": "0.05",
            "damping_ratio_y": "0.1",
            "shaper_type_x": "zv",
            "shaper_freq_x": "48.8",
            "shaper_type_y": "mzv",
            "shaper_freq_y": "49.0",
        },
        "bed_mesh default": {
            "version": "1",
            "points": "\n-0.190000, -0.125000, 0.010000, 0.095000, 0.122500\n-0.145000, -0.095000, 0.067500, 0.125000, 0.130000\n-0.040000, -0.130000, 0.055000, 0.132500, 0.115000\n0.195000, -0.150000, 0.055000, 0.320000, 0.160000\n-0.240000, -0.110000, 0.067500, 0.197500, 0.222500",
            "x_count": "5",
            "y_count": "5",
            "mesh_x_pps": "4",
            "mesh_y_pps": "4",
            "algo": "bicubic",
            "tension": "0.3",
            "min_x": "17.0",
            "max_x": "285.0",
            "min_y": "15.0",
            "max_y": "282.0",
        },
    },
    "warnings": [
        {
            "type": "deprecated_option",
            "message": "Option 'max_accel_to_decel' in section 'printer' is deprecated.",
            "section": "printer",
            "option": "max_accel_to_decel",
        }
    ],
    "save_config_pending": False,
    "save_config_pending_items": {},
    "settings": {
        "mcu": {
            "serial": "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0",
            "baud": 250000,
            "restart_method": "command",
            "max_stepper_error": 2.5e-05,
        },
        "mcu rpi": {
            "serial": "/tmp/klipper_host_mcu",
            "max_stepper_error": 2.5e-05,
        },
        "force_move": {"enable_force_move": True},
        "respond": {"default_type": "echo", "default_prefix": "echo:"},
        "gcode_macro g31": {
            "gcode": "\nRUN_SHELL_COMMAND CMD=clear_plr\nSAVE_VARIABLE VARIABLE=was_interrupted VALUE=False",
            "description": "G-Code macro",
        },
        "gcode_shell_command clear_plr": {
            "command": "sh /home/mks/clear_plr.sh",
            "timeout": 5.0,
            "verbose": True,
        },
        "gcode_macro save_last_file": {
            "gcode": "\n\n{% set svv = printer.save_variables.variables %}\n\n{% set filepath=printer.virtual_sdcard.file_path %}\n\n{% set filename=filepath.split('/')%}\n\nSAVE_VARIABLE VARIABLE=last_file VALUE='\"{ filename[-1] }\"'\nSAVE_VARIABLE VARIABLE=filepath VALUE='\"{ printer.virtual_sdcard.file_path }\"'",
            "description": "G-Code macro",
        },
        "gcode_macro clear_last_file": {
            "gcode": "\n{% set filename='' %}\n{% set filepath='' %}\nSAVE_VARIABLE VARIABLE=last_file VALUE='\"{ filename }\"'\nSAVE_VARIABLE VARIABLE=filepath VALUE='\"{ filepath }\"'",
            "description": "G-Code macro",
        },
        "gcode_shell_command power_loss_resume": {
            "command": "/home/mks/plr.sh",
            "timeout": 420.0,
            "verbose": True,
        },
        "gcode_macro resume_interrupted": {
            "gcode": '\nSET_KINEMATIC_POSITION X=0\nSET_KINEMATIC_POSITION Y=0\nSET_KINEMATIC_POSITION Z=0\n{% set z_height = params.Z_HEIGHT|default(printer.save_variables.variables.power_resume_z)|float %}\n{% set last_file = params.GCODE_FILE|default(printer.save_variables.variables.last_file)|string %}\nm118 {last_file}\n\nRUN_SHELL_COMMAND CMD=POWER_LOSS_RESUME PARAMS="{z_height} \\"{last_file}\\""\nSDCARD_PRINT_FILE FILENAME=plr/"{last_file}"',
            "description": "G-Code macro",
        },
        "gcode_macro log_z": {
            "gcode": '\n{% set z_pos = printer.gcode_move.gcode_position.z %}\nRESPOND MSG="Current Z is {z_pos}"\nSAVE_VARIABLE VARIABLE=power_resume_z VALUE={z_pos}',
            "description": "G-Code macro",
        },
        "save_variables": {
            "filename": "/home/mks/printer_data/config/saved_variables.cfg"
        },
        "gcode_macro cancel_print": {
            "gcode": '\nSAVE_VARIABLE VARIABLE=was_interrupted VALUE=False\nRUN_SHELL_COMMAND CMD=clear_plr\nclear_last_file\nG31\nTURN_OFF_HEATERS\nCANCEL_PRINT_BASE\nRESPOND TYPE=echo MSG="Cancel Print Success!"\nG91\nG1 E-2 F500\nG1 E-2 Z0.2 F200\nG1 Z1\nM106 S0\nM104 S0\nM140 S0\nG90\nG1 X10 Y290 F6000\nM84 X Y E',
            "rename_existing": "CANCEL_PRINT_BASE",
            "description": "Cancel the actual running print",
        },
        "gcode_macro print_start": {
            "gcode": "\n{% set temp = params.EXTRUDER | default(220) | int %}\n{% set b_temp = params.BED | default(60) | int %}\nSAVE_VARIABLE VARIABLE=was_interrupted VALUE=True\n\nM84 E\nSET_HEATER_TEMPERATURE HEATER=heater_bed TARGET={b_temp}\nTEMPERATURE_WAIT SENSOR=heater_bed MINIMUM={b_temp - 5} MAXIMUM={b_temp + 5}\nG28\nBED_MESH_CALIBRATE ADAPTIVE=1\nSET_HEATER_TEMPERATURE HEATER=extruder TARGET={temp}\n\n\nTEMPERATURE_WAIT SENSOR=extruder MINIMUM={temp - 5} MAXIMUM={temp + 5}\n\n\nM400\n\n\nG90\nG92 E0\nG1 E-1\nG92 E0\nM400\n\nG92 E0\nG1 Z1.0 F3000\nG1 X0.1 Y20 Z0.3 F5000.0\nG1 X0.1 Y100.0 Z0.3 F500.0 E15\nG1 X0.4 Y100.0 Z0.3 F5000.0\nG1 X0.4 Y20 Z0.3 F500.0 E30\nG92 E0\nG1 Z1.0 F3000\nM400",
            "description": "G-Code macro",
        },
        "gcode_macro pause": {
            "gcode": '\nRESPOND TYPE=echo MSG="Pause Print!"\n\n{% set x = params.X|default(10) %}\n{% set y = params.Y|default(290) %}\n{% set z = params.Z|default(10)|float %}\n{% set e = params.E|default(1) %}\n\n{% set max_z = printer.toolhead.axis_maximum.z|float %}\n{% set act_z = printer.toolhead.position.z|float %}\n{% set lift_z = z|abs %}\n{% if act_z < (max_z - lift_z) %}\n{% set z_safe = lift_z %}\n{% else %}\n{% set z_safe = max_z - act_z %}\n{% endif %}\n\nPAUSE_BASE\nG91\n{% if printer.extruder.can_extrude|lower == \'True\' %}\nG1 E-{e} F500\n{% else %}\n{action_respond_info("Extruder not hot enough")}\n{% endif %}\n{% if "xyz" in printer.toolhead.homed_axes %}\nG1 Z{z_safe}\nG90\nG1 X{x} Y{y} F6000\n{% else %}\n{action_respond_info("Printer not homed")}\n{% endif %}',
            "rename_existing": "PAUSE_BASE",
            "description": "Pause the actual running print",
        },
        "gcode_macro resume": {
            "gcode": '\nRESPOND TYPE=echo MSG="RESUME Print!"\n\n{% if printer["filament_switch_sensor my_sensor"].filament_detected == True %}\nRESPOND TYPE=echo MSG="RESUME Print!"\n{% set e = params.E|default(1) %}\n\n{% if \'VELOCITY\' in params|upper %}\n{% set get_params = (\'VELOCITY=\' + params.VELOCITY) %}\n{%else %}\n{% set get_params = "" %}\n{% endif %}\n\nG91\n{% if printer.extruder.can_extrude|lower == \'True\' %}\nG1 E{e} F400\n{% else %}\n{action_respond_info("Extruder not hot enough")}\n{% endif %}\nRESUME_BASE {get_params}\n{% else %}\nRESPOND TYPE=echo MSG="Please Insert filament in Sensor!"\n{% endif %}',
            "rename_existing": "RESUME_BASE",
            "description": "Resume the actual running print",
        },
        "gcode_macro end_print": {
            "gcode": '\nG91\nG1 E-2 F500\nG1 E-2 Z0.2 F200\nG1 X5 Y5 F3000\nG1 Z1\nM106 S0\nM104 S0\nM140 S0\nG90\nG1 X10 Y290\n\nM84 X Y E\nRESPOND TYPE=echo MSG="Finish Print!"',
            "description": "G-Code macro",
        },
        "gcode_macro load_filament": {
            "gcode": "\nSAVE_GCODE_POSITION NAME=LOAD_STATE\nG91\nG1 E30 F300\nG1 E10 F150\nG90\nRESTORE_GCODE_POSITION NAME=LOAD_STATE",
            "description": "G-Code macro",
        },
        "gcode_macro unload_filament": {
            "gcode": "\nSAVE_GCODE_POSITION NAME=UNLOAD_STATE\nG91\nG1 E-30 F300\nG90\nRESTORE_GCODE_POSITION NAME=UNLOAD_STATE MOVE=0",
            "description": "G-Code macro",
        },
        "gcode_macro led_on": {
            "gcode": "\nSET_PIN PIN=my_led VALUE=1",
            "description": "G-Code macro",
        },
        "gcode_macro led_off": {
            "gcode": "\nSET_PIN PIN=my_led VALUE=0",
            "description": "G-Code macro",
        },
        "gcode_macro m205": {"gcode": "\nM105", "description": "G-Code macro"},
        "gcode_macro print_end": {
            "gcode": "\nSAVE_VARIABLE VARIABLE=was_interrupted VALUE=False\nRUN_SHELL_COMMAND CMD=clear_plr\nclear_last_file",
            "description": "G-Code macro",
        },
        "virtual_sdcard": {
            "path": "/home/mks/printer_data/gcodes",
            "on_error_gcode": "\n{% if 'heaters' in printer %}\n   TURN_OFF_HEATERS\n{% endif %}\n",
        },
        "pause_resume": {"recover_velocity": 50.0},
        "gcode_arcs": {"resolution": 0.8},
        "idle_timeout": {
            "timeout": 600.0,
            "gcode": '\nRESPOND TYPE=echo MSG="No operations in 10min!"',
        },
        "adxl345": {
            "axes_map": ["x", "y", "z"],
            "rate": 3200,
            "cs_pin": "rpi:None",
            "spi_speed": 5000000,
            "spi_bus": "spidev0.0",
        },
        "verify_heater extruder": {
            "hysteresis": 5.0,
            "max_error": 60.0,
            "heating_gain": 2.0,
            "check_gain_time": 20.0,
        },
        "verify_heater heater_bed": {
            "hysteresis": 5.0,
            "max_error": 180.0,
            "heating_gain": 2.0,
            "check_gain_time": 120.0,
        },
        "resonance_tester": {
            "move_speed": 50.0,
            "min_freq": 1.0,
            "max_freq": 100.0,
            "accel_per_hz": 100.0,
            "hz_per_sec": 0.5,
            "sweeping_accel": 400.0,
            "sweeping_period": 1.2,
            "accel_chip": "adxl345",
            "max_smoothing": 0.2,
            "probe_points": [[150.0, 150.0, 20.0]],
        },
        "tmc2209 stepper_x": {
            "uart_pin": "PE3",
            "uart_address": 3,
            "diag_pin": "^PD10",
            "run_current": 1.2,
            "hold_current": 2.0,
            "sense_resistor": 0.11,
            "interpolate": True,
            "stealthchop_threshold": 0.0,
            "driver_multistep_filt": True,
            "driver_toff": 3,
            "driver_hstrt": 5,
            "driver_hend": 0,
            "driver_tbl": 2,
            "driver_semin": 0,
            "driver_seup": 0,
            "driver_semax": 0,
            "driver_sedn": 0,
            "driver_seimin": 0,
            "driver_iholddelay": 8,
            "driver_pwm_ofs": 36,
            "driver_pwm_grad": 14,
            "driver_pwm_freq": 1,
            "driver_pwm_autoscale": True,
            "driver_pwm_autograd": True,
            "driver_pwm_reg": 8,
            "driver_pwm_lim": 12,
            "driver_tpowerdown": 20,
            "driver_sgthrs": 95,
        },
        "stepper_x": {
            "microsteps": 16,
            "step_pin": "PD15",
            "dir_pin": "PD14",
            "rotation_distance": 40.0,
            "full_steps_per_rotation": 200,
            "gear_ratio": [],
            "step_pulse_duration": 2e-06,
            "enable_pin": "!PC7",
            "endstop_pin": "tmc2209_stepper_x: virtual_endstop",
            "position_endstop": -12.0,
            "position_min": -12.0,
            "position_max": 302.0,
            "homing_speed": 50.0,
            "second_homing_speed": 25.0,
            "homing_retract_speed": 50.0,
            "homing_retract_dist": 0.0,
            "homing_positive_dir": False,
        },
        "tmc2209 stepper_y": {
            "uart_pin": "PE4",
            "uart_address": 3,
            "diag_pin": "^PE0",
            "run_current": 1.2,
            "hold_current": 2.0,
            "sense_resistor": 0.11,
            "interpolate": True,
            "stealthchop_threshold": 0.0,
            "driver_multistep_filt": True,
            "driver_toff": 3,
            "driver_hstrt": 5,
            "driver_hend": 0,
            "driver_tbl": 2,
            "driver_semin": 0,
            "driver_seup": 0,
            "driver_semax": 0,
            "driver_sedn": 0,
            "driver_seimin": 0,
            "driver_iholddelay": 8,
            "driver_pwm_ofs": 36,
            "driver_pwm_grad": 14,
            "driver_pwm_freq": 1,
            "driver_pwm_autoscale": True,
            "driver_pwm_autograd": True,
            "driver_pwm_reg": 8,
            "driver_pwm_lim": 12,
            "driver_tpowerdown": 20,
            "driver_sgthrs": 95,
        },
        "stepper_y": {
            "microsteps": 16,
            "step_pin": "PB7",
            "dir_pin": "PB6",
            "rotation_distance": 40.0,
            "full_steps_per_rotation": 200,
            "gear_ratio": [],
            "step_pulse_duration": 2e-06,
            "enable_pin": "!PB9",
            "endstop_pin": "tmc2209_stepper_y: virtual_endstop",
            "position_endstop": -6.0,
            "position_min": -6.0,
            "position_max": 302.0,
            "homing_speed": 50.0,
            "second_homing_speed": 25.0,
            "homing_retract_speed": 50.0,
            "homing_retract_dist": 0.0,
            "homing_positive_dir": False,
        },
        "tmc2209 extruder": {
            "uart_pin": "PE7",
            "uart_address": 3,
            "run_current": 0.6,
            "hold_current": 2.0,
            "sense_resistor": 0.11,
            "interpolate": True,
            "driver_multistep_filt": True,
            "driver_toff": 3,
            "driver_hstrt": 5,
            "driver_hend": 0,
            "driver_tbl": 2,
            "driver_semin": 0,
            "driver_seup": 0,
            "driver_semax": 0,
            "driver_sedn": 0,
            "driver_seimin": 0,
            "driver_iholddelay": 8,
            "driver_pwm_ofs": 36,
            "driver_pwm_grad": 14,
            "driver_pwm_freq": 1,
            "driver_pwm_autoscale": True,
            "driver_pwm_autograd": True,
            "driver_pwm_reg": 8,
            "driver_pwm_lim": 12,
            "driver_tpowerdown": 20,
            "driver_sgthrs": 0,
        },
        "extruder": {
            "microsteps": 16,
            "sensor_type": "EPCOS 100K B57560G104F",
            "pullup_resistor": 4700.0,
            "inline_resistor": 0.0,
            "sensor_pin": "PA4",
            "min_temp": 0.0,
            "max_temp": 305.0,
            "min_extrude_temp": 150.0,
            "max_power": 1.0,
            "smooth_time": 1.0,
            "control": "pid",
            "pid_kp": 24.522,
            "pid_ki": 1.397,
            "pid_kd": 107.59,
            "heater_pin": "PA1",
            "pwm_cycle_time": 0.1,
            "nozzle_diameter": 0.4,
            "filament_diameter": 1.75,
            "max_extrude_cross_section": 500.0,
            "max_extrude_only_velocity": 2000.0,
            "max_extrude_only_accel": 10000.0,
            "max_extrude_only_distance": 100.0,
            "instantaneous_corner_velocity": 10.0,
            "step_pin": "PD1",
            "pressure_advance": 0.02,
            "pressure_advance_smooth_time": 0.035,
            "dir_pin": "!PD0",
            "rotation_distance": 4.59,
            "full_steps_per_rotation": 200,
            "gear_ratio": [],
            "enable_pin": "!PD4",
        },
        "heater_bed": {
            "sensor_type": "EPCOS 100K B57560G104F",
            "pullup_resistor": 4700.0,
            "inline_resistor": 0.0,
            "sensor_pin": "PA3",
            "min_temp": 0.0,
            "max_temp": 105.0,
            "min_extrude_temp": 170.0,
            "max_power": 1.0,
            "smooth_time": 1.0,
            "control": "pid",
            "pid_kp": 54.027,
            "pid_ki": 0.77,
            "pid_kd": 948.182,
            "heater_pin": "PA2",
            "pwm_cycle_time": 0.1,
        },
        "probe": {
            "z_offset": 2.465,
            "deactivate_on_each_sample": True,
            "activate_gcode": "",
            "deactivate_gcode": "",
            "pin": "PD13",
            "x_offset": 27.0,
            "y_offset": -20.0,
            "speed": 5.0,
            "lift_speed": 5.0,
            "samples": 1,
            "sample_retract_dist": 2.0,
            "samples_result": "average",
            "samples_tolerance": 0.1,
            "samples_tolerance_retries": 0,
        },
        "filament_switch_sensor my_sensor": {
            "switch_pin": "PD11",
            "pause_on_runout": True,
            "runout_gcode": "",
            "pause_delay": 0.5,
            "event_delay": 3.0,
        },
        "safe_z_home": {
            "home_xy_position": [123.0, 170.0],
            "z_hop": 10.0,
            "z_hop_speed": 15.0,
            "speed": 80.0,
            "move_to_previous": True,
        },
        "z_tilt": {
            "z_positions": [[-8.0, 170.0], [260.0, 170.0]],
            "retries": 20,
            "retry_tolerance": 0.005,
            "points": [[-8.0, 170.0], [260.0, 170.0]],
            "horizontal_move_z": 5.0,
            "speed": 200.0,
        },
        "bed_mesh": {
            "adaptive_margin": 5.0,
            "probe_count": [5, 5],
            "mesh_min": [17.0, 15.0],
            "mesh_max": [285.0, 282.0],
            "mesh_pps": [4, 4],
            "algorithm": "bicubic",
            "bicubic_tension": 0.3,
            "scan_overshoot": 0,
            "horizontal_move_z": 5.0,
            "speed": 200.0,
            "fade_start": 0.2,
            "fade_end": 5.0,
            "split_delta_z": 0.025,
            "move_check_distance": 3.0,
        },
        "bed_mesh default": {
            "version": 1,
            "points": [
                [-0.19, -0.125, 0.01, 0.095, 0.1225],
                [-0.145, -0.095, 0.0675, 0.125, 0.13],
                [-0.04, -0.13, 0.055, 0.1325, 0.115],
                [0.195, -0.15, 0.055, 0.32, 0.16],
                [-0.24, -0.11, 0.0675, 0.1975, 0.2225],
            ],
            "min_x": 17.0,
            "max_x": 285.0,
            "min_y": 15.0,
            "max_y": 282.0,
            "x_count": 5,
            "y_count": 5,
            "mesh_x_pps": 4,
            "mesh_y_pps": 4,
            "algo": "bicubic",
            "tension": 0.3,
        },
        "screws_tilt_adjust": {
            "screw1": [4.0, 58.0],
            "screw1_name": "front left screw",
            "screw2": [243.0, 58.0],
            "screw2_name": "front right screw",
            "screw3": [243.0, 290.0],
            "screw3_name": "rear right screw",
            "screw4": [4.0, 290.0],
            "screw4_name": "rear left screw",
            "screw_thread": "CW-M4",
            "horizontal_move_z": 5.0,
            "speed": 200.0,
        },
        "heater_fan hotend_fan": {
            "heater": ["extruder"],
            "heater_temp": 50.0,
            "max_power": 1.0,
            "kick_start_time": 0.1,
            "off_below": 0.0,
            "cycle_time": 0.01,
            "hardware_pwm": False,
            "shutdown_speed": 1.0,
            "pin": "PE11",
            "fan_speed": 1.0,
        },
        "multi_pin fan_pins": {"pins": ["PE9", "PE13"]},
        "fan": {
            "max_power": 1.0,
            "kick_start_time": 0.1,
            "off_below": 0.0,
            "cycle_time": 0.01,
            "hardware_pwm": False,
            "shutdown_speed": 0.0,
            "pin": "multi_pin:fan_pins",
        },
        "output_pin my_led": {
            "pwm": True,
            "pin": "PC4",
            "cycle_time": 0.01,
            "hardware_pwm": False,
            "scale": 1.0,
            "value": 1.0,
            "shutdown_value": 0.0,
        },
        "controller_fan fan_board": {
            "stepper": ["stepper_x", "stepper_y", "stepper_z", "stepper_z1"],
            "max_power": 1.0,
            "kick_start_time": 0.1,
            "off_below": 0.0,
            "cycle_time": 0.01,
            "hardware_pwm": False,
            "shutdown_speed": 0.0,
            "pin": "PD3",
            "fan_speed": 1.0,
            "idle_speed": 1.0,
            "idle_timeout": 120,
            "heater": ["heater_bed", "extruder"],
        },
        "input_shaper": {
            "shaper_type": "mzv",
            "shaper_type_x": "zv",
            "damping_ratio_x": 0.05,
            "shaper_freq_x": 48.8,
            "shaper_type_y": "mzv",
            "damping_ratio_y": 0.1,
            "shaper_freq_y": 49.0,
        },
        "printer": {
            "max_velocity": 300.0,
            "max_accel": 10000.0,
            "max_accel_to_decel": 5000.0,
            "minimum_cruise_ratio": 0.5,
            "square_corner_velocity": 6.0,
            "kinematics": "cartesian",
            "max_z_velocity": 15.0,
            "max_z_accel": 100.0,
        },
        "stepper_z": {
            "step_pin": "PB3",
            "dir_pin": "!PD7",
            "rotation_distance": 8.0,
            "microsteps": 16,
            "full_steps_per_rotation": 200,
            "gear_ratio": [],
            "enable_pin": "!PB5",
            "endstop_pin": "probe:z_virtual_endstop",
            "position_min": -4.0,
            "position_max": 355.0,
            "homing_speed": 10.0,
            "second_homing_speed": 5.0,
            "homing_retract_speed": 10.0,
            "homing_retract_dist": 5.0,
            "homing_positive_dir": False,
        },
        "stepper_z1": {
            "step_pin": "PA7",
            "dir_pin": "!PA6",
            "rotation_distance": 8.0,
            "microsteps": 16,
            "full_steps_per_rotation": 200,
            "gear_ratio": [],
            "enable_pin": "!PC5",
            "endstop_pin": "probe:z_virtual_endstop",
        },
    },
}


def search_config_sections(section: str) -> list:
    """Retrieve a section or sections from the printers configfile

    Args:
        section (str): Name of the section
        name (str, optional): Name of the section object. Defaults to "".

    Returns:
        dict | None: The entire section with the section as key or None if
                        nothing is found
    """

    if not config or not section:
        return []

    # if "config" not in config.keys():
    if not config.get("config"):
        return []
    _printer_config = config.get("config")
    
    return [
        {key: _printer_config}
        for key in config["config"].keys()
        if key.startswith(section)  # O(s) time per key
    ]
    # Iterates over every key and checks if it starts
    # with the prefix -> Complexity O(n*s)
    # Simple but becomes costly for large n values
    # since the dictionary is not exactly big, it should be ok


def get_probe(config):
    _probe_type = ["probe", "bltouch", "probe_eddy_current", "smart_effector"]
    _add = []
    for probe in _probe_type:
        hit = search_config_sections(probe)
        if hit:
            _add.extend(hit)
    return _add


def search_from_list(search_list: list, _objects: list = []):
    if len(search_list) == 0:
        return _objects
    _objects.extend(search_config_sections(search_list.pop()))
    print(_objects)
    return search_from_list(search_list, _objects)


class test_get_configs(unittest.TestCase):
    # def test_search_all_no_recursion(self):
    #     _probe_type = ["probe", "bltouch", "probe_eddy_current", "smart_effector"]
    #     self.assertEqual(
    #         get_probe(config),
    #         [
    #             {
    #                 "probe": {
    #                     "pin": "PD13",
    #                     "x_offset": "27",
    #                     "y_offset": "-20",
    #                     "z_offset": "2.465",
    #                 }
    #             },
    #             {
    #                 "probe2": {
    #                     "pin": "PD13",
    #                     "x_offset": "27",
    #                     "y_offset": "-20",
    #                     "z_offset": "2.465",
    #                 }
    #             },
    #             {"bltouch": {"#guov": 2039}},
    #         ],
    #     )

    def test_diff_search_one(self):
        _probe_type = _probe_type = ["probe"]
        self.assertEqual(
            search_from_list(_probe_type),
            [
                {
                    "probe": {
                        "pin": "PD13",
                        "x_offset": "27",
                        "y_offset": "-20",
                        "z_offset": "2.465",
                    }
                },
                {
                    "probe2": {
                        "pin": "PD13",
                        "x_offset": "27",
                        "y_offset": "-20",
                        "z_offset": "2.465",
                    },
                },
            ],
        )

    def test_diff_search_two(self):
        _probe_type = ["probe", "bltouch" , "probe_eddy_current", "smart_effector"]
        search_from_list(
            _probe_type,
            [
                {
                    "probe": {
                        "pin": "PD13",
                        "x_offset": "27",
                        "y_offset": "-20",
                        "z_offset": "2.465",
                    }
                },
                
                {"bltouch": {"#guov": 2039}},
            ],
        )

    def test_search_more_than_two(self):
        _list = ["stepper_x", "stepper_y", "probe", "probe_eddy_current", "smart_effector"]
    # def test_diff_search_two(self):
    #     _probe_type = ["probe", "bltouch"]
    #     self.assertEqual(
    #         search_from_list(_probe_type),
    #         [
    #             {
    #                 "probe": {
    #                     "pin": "PD13",
    #                     "x_offset": "27",
    #                     "y_offset": "-20",
    #                     "z_offset": "2.465",
    #                 }
    #             },
    #             {
    #                 "probe2": {
    #                     "pin": "PD13",
    #                     "x_offset": "27",
    #                     "y_offset": "-20",
    #                     "z_offset": "2.465",
    #                 }
    #             },
    #             {"bltouch": {"#guov": 2039}},
    #         ],
    #     )


if __name__ == "__main__":
    unittest.main()
