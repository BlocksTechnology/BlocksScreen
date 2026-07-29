# Collection of useful methods
#
# This file contains some methods derived from KlipperScreen
# Original source: https://github.com/KlipperScreen/KlipperScreen
# License: GNU General Public License v3
# Modifications made by Hugo Costa <h.costa@blockstec.com> (2025) for BlocksScreen


import ctypes
import enum
import logging
import os
import pathlib
import struct
import typing

logger = logging.getLogger(__name__)

try:
    ctypes.cdll.LoadLibrary("libXext.so.6")
    libxext = ctypes.CDLL("libXext.so.6")

    class DPMSState(enum.Enum):
        """Available DPMS states"""

        FAIL = -1
        ON = 0
        STANDBY = 1
        SUSPEND = 2
        OFF = 3

    # X11/extensions/dpms.h
    # CARD16 -> unsigned 16-bit integer

    libxext.DPMSForceLevel.argtypes = [
        ctypes.c_uint,
        ctypes.c_int,
        ctypes.c_uint,
    ]
    libxext.DPMSForceLevel.restype = ctypes.c_int

    def get_dpms_state():
        """Gets and returns DPMS state"""
        _dpms_state = DPMSState.FAIL
        _display_name = ctypes.c_char_p(b":0")
        libxext.XOpenDisplay.restype = ctypes.c_void_p
        display = ctypes.c_void_p(
            libxext.XOpenDisplay(_display_name)
        )  # void* in C void pointer
        major_opcode_p = ctypes.create_string_buffer(8)
        first_event_p = ctypes.create_string_buffer(8)
        if display.value:
            try:
                if libxext.DPMSQueryExtension(
                    display, major_opcode_p, first_event_p
                ) and libxext.DPMSCapable(display):
                    onoff_p = ctypes.create_string_buffer(1)
                    state_p = ctypes.create_string_buffer(2)
                    if libxext.DPMSInfo(display, state_p, onoff_p):
                        onoff = struct.unpack("B", onoff_p.raw)[0]
                        if onoff:
                            _dpms_state = struct.unpack("H", state_p.raw)[0]
            finally:
                libxext.XCloseDisplay(display)
        return _dpms_state

    def set_dpms_mode(mode: DPMSState) -> None:
        """Set DPMS state

        Args:
            mode (DPMSState): State to set DPMS. Check available state on `DPMSState`
        """
        _display_name = ctypes.c_char_p(b":0")
        libxext.XOpenDisplay.restype = ctypes.c_void_p
        display = ctypes.c_void_p(
            libxext.XOpenDisplay(_display_name)
        )  # void* in C void pointer
        major_opcode_p = ctypes.create_string_buffer(8)
        first_event_p = ctypes.create_string_buffer(8)
        if display.value:
            try:
                if libxext.DPMSQueryExtension(
                    display, major_opcode_p, first_event_p
                ) and libxext.DPMSCapable(display):
                    libxext.DPMSForceLevel(display.value, mode.value, 0)
            finally:
                libxext.XCloseDisplay(display)

    def get_dpms_timeouts() -> typing.Dict:
        """Get current DPMS timeouts"""
        _display_name = ctypes.c_char_p(b":0")
        libxext.XOpenDisplay.restype = ctypes.c_void_p
        display = ctypes.c_void_p(
            libxext.XOpenDisplay(_display_name)
        )  # void* in C void pointer
        _standby_timeout = _suspend_timeout = _off_timeout = -1
        major_opcode_p = ctypes.create_string_buffer(8)
        first_event_p = ctypes.create_string_buffer(8)
        if display.value:
            try:
                if libxext.DPMSQueryExtension(
                    display, major_opcode_p, first_event_p
                ) and libxext.DPMSCapable(display):
                    standby_p = ctypes.create_string_buffer(2)
                    suspend_p = ctypes.create_string_buffer(2)
                    off_p = ctypes.create_string_buffer(2)

                    if libxext.DPMSGetTimeouts(display, standby_p, suspend_p, off_p):
                        _standby_timeout = struct.unpack("H", standby_p.raw)[0]
                        _suspend_timeout = struct.unpack("H", suspend_p.raw)[0]
                        _off_timeout = struct.unpack("H", off_p.raw)[0]
            finally:
                libxext.XCloseDisplay(display)

        return {
            "standby_seconds": _standby_timeout,
            "suspend_seconds": _suspend_timeout,
            "off_seconds": _off_timeout,
        }

    def set_dpms_timeouts(
        suspend: int = 0, standby: int = 0, off: int = 0
    ) -> typing.Dict:
        """Set DPMS timeout"""
        _display_name = ctypes.c_char_p(b":0")
        libxext.XOpenDisplay.restype = ctypes.c_void_p
        display = ctypes.c_void_p(
            libxext.XOpenDisplay(_display_name)
        )  # void* in C void pointer
        _standby_timeout = _suspend_timeout = _off_timeout = -1
        major_opcode_p = ctypes.create_string_buffer(8)
        first_event_p = ctypes.create_string_buffer(8)

        if display.value:
            try:
                if libxext.DPMSQueryExtension(
                    display, major_opcode_p, first_event_p
                ) and libxext.DPMSCapable(display):
                    libxext.DPMSSetTimeouts(display, suspend, standby, off)

                    standby_p = ctypes.create_string_buffer(2)
                    suspend_p = ctypes.create_string_buffer(2)
                    off_p = ctypes.create_string_buffer(2)

                    if libxext.DPMSGetTimeouts(display, standby_p, suspend_p, off_p):
                        _standby_timeout = struct.unpack("H", standby_p.raw)[0]
                        _suspend_timeout = struct.unpack("H", suspend_p.raw)[0]
                        _off_timeout = struct.unpack("H", off_p.raw)[0]
            finally:
                libxext.XCloseDisplay(display)

        return {
            "standby_seconds": _standby_timeout,
            "suspend_seconds": _suspend_timeout,
            "off_seconds": _off_timeout,
        }

    def get_dpms_info() -> typing.Dict:
        """Get DPMS information

        Returns:
            typing.Dict: Dpms state
        """
        _dpms_state = DPMSState.FAIL
        onoff = 0
        _display_name = ctypes.c_char_p(b":0")
        libxext.XOpenDisplay.restype = ctypes.c_void_p
        display = ctypes.c_void_p(
            libxext.XOpenDisplay(_display_name)
        )  # void* in C void pointer

        major_opcode_p = ctypes.create_string_buffer(8)
        first_event_p = ctypes.create_string_buffer(8)

        if display.value:
            try:
                if libxext.DPMSQueryExtension(
                    display, major_opcode_p, first_event_p
                ) and libxext.DPMSCapable(display):
                    onoff_p = ctypes.create_string_buffer(1)
                    state_p = ctypes.create_string_buffer(2)
                    if libxext.DPMSInfo(display, state_p, onoff_p):
                        onoff = struct.unpack("B", onoff_p.raw)[0]
                        if onoff:
                            _dpms_state = struct.unpack("H", state_p.raw)[0]

            finally:
                libxext.XCloseDisplay(display)

        return {"power_level": onoff, "state": DPMSState(_dpms_state)}

    def check_dpms_capable(display: int):
        """Check if device has DPMS

        Args:
            display (int): Display index

        """
        _display_name = ctypes.c_char_p(b":%d" % (display))

        libxext.XOpenDisplay.restype = ctypes.c_void_p
        _display = ctypes.c_void_p(
            libxext.XOpenDisplay(_display_name)
        )  # void* in C void pointer

        major_opcode_p = ctypes.create_string_buffer(8)
        first_event_p = ctypes.create_string_buffer(8)
        _capable = False
        if _display.value:
            try:
                if libxext.DPMSQueryExtension(
                    _display, major_opcode_p, first_event_p
                ) and libxext.DPMSCapable(_display):
                    _capable = True

            finally:
                libxext.XCloseDisplay(display)
        return _capable

    def disable_dpms() -> None:
        """Disable DPMS"""
        set_dpms_mode(DPMSState.OFF)

except OSError as e:
    logger.exception(f"OSError couldn't load DPMS library: {e}")
except Exception as e:
    logger.exception(f"Unexpected exception occurred {e}")
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def convert_bytes_to_mb(self, bytes: int | float) -> float:
    args = [self, bytes]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_convert_bytes_to_mb__mutmut_orig, x_convert_bytes_to_mb__mutmut_mutants, args, kwargs, None)


def x_convert_bytes_to_mb__mutmut_orig(self, bytes: int | float) -> float:
    """Converts byte size to megabyte size

    Args:
        bytes (int | float): bytes

    Returns:
        mb: float that represents the number of mb
    """
    _relation = 2 ** (-20)
    return bytes * _relation


def x_convert_bytes_to_mb__mutmut_1(self, bytes: int | float) -> float:
    """Converts byte size to megabyte size

    Args:
        bytes (int | float): bytes

    Returns:
        mb: float that represents the number of mb
    """
    _relation = None
    return bytes * _relation


def x_convert_bytes_to_mb__mutmut_2(self, bytes: int | float) -> float:
    """Converts byte size to megabyte size

    Args:
        bytes (int | float): bytes

    Returns:
        mb: float that represents the number of mb
    """
    _relation = 2 * (-20)
    return bytes * _relation


def x_convert_bytes_to_mb__mutmut_3(self, bytes: int | float) -> float:
    """Converts byte size to megabyte size

    Args:
        bytes (int | float): bytes

    Returns:
        mb: float that represents the number of mb
    """
    _relation = 3 ** (-20)
    return bytes * _relation


def x_convert_bytes_to_mb__mutmut_4(self, bytes: int | float) -> float:
    """Converts byte size to megabyte size

    Args:
        bytes (int | float): bytes

    Returns:
        mb: float that represents the number of mb
    """
    _relation = 2 ** (+20)
    return bytes * _relation


def x_convert_bytes_to_mb__mutmut_5(self, bytes: int | float) -> float:
    """Converts byte size to megabyte size

    Args:
        bytes (int | float): bytes

    Returns:
        mb: float that represents the number of mb
    """
    _relation = 2 ** (-21)
    return bytes * _relation


def x_convert_bytes_to_mb__mutmut_6(self, bytes: int | float) -> float:
    """Converts byte size to megabyte size

    Args:
        bytes (int | float): bytes

    Returns:
        mb: float that represents the number of mb
    """
    _relation = 2 ** (-20)
    return bytes / _relation

x_convert_bytes_to_mb__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_convert_bytes_to_mb__mutmut_1': x_convert_bytes_to_mb__mutmut_1, 
    'x_convert_bytes_to_mb__mutmut_2': x_convert_bytes_to_mb__mutmut_2, 
    'x_convert_bytes_to_mb__mutmut_3': x_convert_bytes_to_mb__mutmut_3, 
    'x_convert_bytes_to_mb__mutmut_4': x_convert_bytes_to_mb__mutmut_4, 
    'x_convert_bytes_to_mb__mutmut_5': x_convert_bytes_to_mb__mutmut_5, 
    'x_convert_bytes_to_mb__mutmut_6': x_convert_bytes_to_mb__mutmut_6
}
x_convert_bytes_to_mb__mutmut_orig.__name__ = 'x_convert_bytes_to_mb'


def calculate_current_layer(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    args = [z_position, object_height, layer_height, first_layer_height]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_calculate_current_layer__mutmut_orig, x_calculate_current_layer__mutmut_mutants, args, kwargs, None)


def x_calculate_current_layer__mutmut_orig(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position == 0:
        return -1
    if z_position <= first_layer_height:
        return 1

    _current_layer = (z_position) / layer_height

    return int(_current_layer)


def x_calculate_current_layer__mutmut_1(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position != 0:
        return -1
    if z_position <= first_layer_height:
        return 1

    _current_layer = (z_position) / layer_height

    return int(_current_layer)


def x_calculate_current_layer__mutmut_2(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position == 1:
        return -1
    if z_position <= first_layer_height:
        return 1

    _current_layer = (z_position) / layer_height

    return int(_current_layer)


def x_calculate_current_layer__mutmut_3(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position == 0:
        return +1
    if z_position <= first_layer_height:
        return 1

    _current_layer = (z_position) / layer_height

    return int(_current_layer)


def x_calculate_current_layer__mutmut_4(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position == 0:
        return -2
    if z_position <= first_layer_height:
        return 1

    _current_layer = (z_position) / layer_height

    return int(_current_layer)


def x_calculate_current_layer__mutmut_5(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position == 0:
        return -1
    if z_position < first_layer_height:
        return 1

    _current_layer = (z_position) / layer_height

    return int(_current_layer)


def x_calculate_current_layer__mutmut_6(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position == 0:
        return -1
    if z_position <= first_layer_height:
        return 2

    _current_layer = (z_position) / layer_height

    return int(_current_layer)


def x_calculate_current_layer__mutmut_7(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position == 0:
        return -1
    if z_position <= first_layer_height:
        return 1

    _current_layer = None

    return int(_current_layer)


def x_calculate_current_layer__mutmut_8(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position == 0:
        return -1
    if z_position <= first_layer_height:
        return 1

    _current_layer = (z_position) * layer_height

    return int(_current_layer)


def x_calculate_current_layer__mutmut_9(
    z_position: float,
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculated the current printing layer given the GCODE z position received by the
        gcode_move object update.
        Also updates the label where the current layer should be displayed

    Returns:
        int: Current layer
    """
    if z_position == 0:
        return -1
    if z_position <= first_layer_height:
        return 1

    _current_layer = (z_position) / layer_height

    return int(None)

x_calculate_current_layer__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_calculate_current_layer__mutmut_1': x_calculate_current_layer__mutmut_1, 
    'x_calculate_current_layer__mutmut_2': x_calculate_current_layer__mutmut_2, 
    'x_calculate_current_layer__mutmut_3': x_calculate_current_layer__mutmut_3, 
    'x_calculate_current_layer__mutmut_4': x_calculate_current_layer__mutmut_4, 
    'x_calculate_current_layer__mutmut_5': x_calculate_current_layer__mutmut_5, 
    'x_calculate_current_layer__mutmut_6': x_calculate_current_layer__mutmut_6, 
    'x_calculate_current_layer__mutmut_7': x_calculate_current_layer__mutmut_7, 
    'x_calculate_current_layer__mutmut_8': x_calculate_current_layer__mutmut_8, 
    'x_calculate_current_layer__mutmut_9': x_calculate_current_layer__mutmut_9
}
x_calculate_current_layer__mutmut_orig.__name__ = 'x_calculate_current_layer'


def estimate_print_time(seconds: int) -> list:
    args = [seconds]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_estimate_print_time__mutmut_orig, x_estimate_print_time__mutmut_mutants, args, kwargs, None)


def x_estimate_print_time__mutmut_orig(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_1(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = None
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_2(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(None, 60)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_3(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, None)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_4(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(60)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_5(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, )
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_6(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 61)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_7(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = None
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_8(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(None, 60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_9(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, None)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_10(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_11(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, )
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_12(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, 61)
    days, hours = divmod(num_hours, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_13(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = None
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_14(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(None, 24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_15(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, None)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_16(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(24)
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_17(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, )
    return [days, hours, minutes, seconds]


def x_estimate_print_time__mutmut_18(seconds: int) -> list:
    """Convert time in seconds format to days, hours, minutes, seconds.

    Args:
        seconds (int): Seconds

    Returns:
        list: list that contains the converted information [days, hours, minutes, seconds]
    """
    num_min, seconds = divmod(seconds, 60)
    num_hours, minutes = divmod(num_min, 60)
    days, hours = divmod(num_hours, 25)
    return [days, hours, minutes, seconds]

x_estimate_print_time__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_estimate_print_time__mutmut_1': x_estimate_print_time__mutmut_1, 
    'x_estimate_print_time__mutmut_2': x_estimate_print_time__mutmut_2, 
    'x_estimate_print_time__mutmut_3': x_estimate_print_time__mutmut_3, 
    'x_estimate_print_time__mutmut_4': x_estimate_print_time__mutmut_4, 
    'x_estimate_print_time__mutmut_5': x_estimate_print_time__mutmut_5, 
    'x_estimate_print_time__mutmut_6': x_estimate_print_time__mutmut_6, 
    'x_estimate_print_time__mutmut_7': x_estimate_print_time__mutmut_7, 
    'x_estimate_print_time__mutmut_8': x_estimate_print_time__mutmut_8, 
    'x_estimate_print_time__mutmut_9': x_estimate_print_time__mutmut_9, 
    'x_estimate_print_time__mutmut_10': x_estimate_print_time__mutmut_10, 
    'x_estimate_print_time__mutmut_11': x_estimate_print_time__mutmut_11, 
    'x_estimate_print_time__mutmut_12': x_estimate_print_time__mutmut_12, 
    'x_estimate_print_time__mutmut_13': x_estimate_print_time__mutmut_13, 
    'x_estimate_print_time__mutmut_14': x_estimate_print_time__mutmut_14, 
    'x_estimate_print_time__mutmut_15': x_estimate_print_time__mutmut_15, 
    'x_estimate_print_time__mutmut_16': x_estimate_print_time__mutmut_16, 
    'x_estimate_print_time__mutmut_17': x_estimate_print_time__mutmut_17, 
    'x_estimate_print_time__mutmut_18': x_estimate_print_time__mutmut_18
}
x_estimate_print_time__mutmut_orig.__name__ = 'x_estimate_print_time'


def normalize(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    args = [value, r_min, r_max, t_min, t_max]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_normalize__mutmut_orig, x_normalize__mutmut_mutants, args, kwargs, None)


def x_normalize__mutmut_orig(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_1(value, r_min=1.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_2(value, r_min=0.0, r_max=2.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_3(value, r_min=0.0, r_max=1.0, t_min=1.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_4(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=101):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_5(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = None
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_6(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) * (r_max - r_min)
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_7(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value + r_min) / (r_max - r_min)
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_8(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max + r_min)
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_9(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = None
    return c1 * c2


def x_normalize__mutmut_10(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = (t_max - t_min) - t_min
    return c1 * c2


def x_normalize__mutmut_11(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = (t_max + t_min) + t_min
    return c1 * c2


def x_normalize__mutmut_12(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    """Normalize values between a rage"""
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = (t_max - t_min) + t_min
    return c1 / c2

x_normalize__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_normalize__mutmut_1': x_normalize__mutmut_1, 
    'x_normalize__mutmut_2': x_normalize__mutmut_2, 
    'x_normalize__mutmut_3': x_normalize__mutmut_3, 
    'x_normalize__mutmut_4': x_normalize__mutmut_4, 
    'x_normalize__mutmut_5': x_normalize__mutmut_5, 
    'x_normalize__mutmut_6': x_normalize__mutmut_6, 
    'x_normalize__mutmut_7': x_normalize__mutmut_7, 
    'x_normalize__mutmut_8': x_normalize__mutmut_8, 
    'x_normalize__mutmut_9': x_normalize__mutmut_9, 
    'x_normalize__mutmut_10': x_normalize__mutmut_10, 
    'x_normalize__mutmut_11': x_normalize__mutmut_11, 
    'x_normalize__mutmut_12': x_normalize__mutmut_12
}
x_normalize__mutmut_orig.__name__ = 'x_normalize'


def check_filepath_permission(filepath, access_type: int = os.R_OK) -> bool:
    args = [filepath, access_type]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_filepath_permission__mutmut_orig, x_check_filepath_permission__mutmut_mutants, args, kwargs, None)


def x_check_filepath_permission__mutmut_orig(filepath, access_type: int = os.R_OK) -> bool:
    # if not isinstance(filepath, pathlib.Path):
    """Checks for file path access

    Args:
        filepath (str | pathlib.Path): path to file
        access_type (int, optional): _description_. Defaults to os.R_OK.

    ***

    #### **Access type can be:**

     - F_OK -> Checks file existence on path
     - R_OK -> Checks if file is readable
     - W_OK -> Checks if file is Writable
     - X_OK -> Checks if file can be executed

    ***
    Returns:
        bool: _description_
    """  #     return False
    if not os.path.isfile(filepath):
        return False
    return os.access(filepath, access_type)


def x_check_filepath_permission__mutmut_1(filepath, access_type: int = os.R_OK) -> bool:
    # if not isinstance(filepath, pathlib.Path):
    """Checks for file path access

    Args:
        filepath (str | pathlib.Path): path to file
        access_type (int, optional): _description_. Defaults to os.R_OK.

    ***

    #### **Access type can be:**

     - F_OK -> Checks file existence on path
     - R_OK -> Checks if file is readable
     - W_OK -> Checks if file is Writable
     - X_OK -> Checks if file can be executed

    ***
    Returns:
        bool: _description_
    """  #     return False
    if os.path.isfile(filepath):
        return False
    return os.access(filepath, access_type)


def x_check_filepath_permission__mutmut_2(filepath, access_type: int = os.R_OK) -> bool:
    # if not isinstance(filepath, pathlib.Path):
    """Checks for file path access

    Args:
        filepath (str | pathlib.Path): path to file
        access_type (int, optional): _description_. Defaults to os.R_OK.

    ***

    #### **Access type can be:**

     - F_OK -> Checks file existence on path
     - R_OK -> Checks if file is readable
     - W_OK -> Checks if file is Writable
     - X_OK -> Checks if file can be executed

    ***
    Returns:
        bool: _description_
    """  #     return False
    if not os.path.isfile(None):
        return False
    return os.access(filepath, access_type)


def x_check_filepath_permission__mutmut_3(filepath, access_type: int = os.R_OK) -> bool:
    # if not isinstance(filepath, pathlib.Path):
    """Checks for file path access

    Args:
        filepath (str | pathlib.Path): path to file
        access_type (int, optional): _description_. Defaults to os.R_OK.

    ***

    #### **Access type can be:**

     - F_OK -> Checks file existence on path
     - R_OK -> Checks if file is readable
     - W_OK -> Checks if file is Writable
     - X_OK -> Checks if file can be executed

    ***
    Returns:
        bool: _description_
    """  #     return False
    if not os.path.isfile(filepath):
        return True
    return os.access(filepath, access_type)


def x_check_filepath_permission__mutmut_4(filepath, access_type: int = os.R_OK) -> bool:
    # if not isinstance(filepath, pathlib.Path):
    """Checks for file path access

    Args:
        filepath (str | pathlib.Path): path to file
        access_type (int, optional): _description_. Defaults to os.R_OK.

    ***

    #### **Access type can be:**

     - F_OK -> Checks file existence on path
     - R_OK -> Checks if file is readable
     - W_OK -> Checks if file is Writable
     - X_OK -> Checks if file can be executed

    ***
    Returns:
        bool: _description_
    """  #     return False
    if not os.path.isfile(filepath):
        return False
    return os.access(None, access_type)


def x_check_filepath_permission__mutmut_5(filepath, access_type: int = os.R_OK) -> bool:
    # if not isinstance(filepath, pathlib.Path):
    """Checks for file path access

    Args:
        filepath (str | pathlib.Path): path to file
        access_type (int, optional): _description_. Defaults to os.R_OK.

    ***

    #### **Access type can be:**

     - F_OK -> Checks file existence on path
     - R_OK -> Checks if file is readable
     - W_OK -> Checks if file is Writable
     - X_OK -> Checks if file can be executed

    ***
    Returns:
        bool: _description_
    """  #     return False
    if not os.path.isfile(filepath):
        return False
    return os.access(filepath, None)


def x_check_filepath_permission__mutmut_6(filepath, access_type: int = os.R_OK) -> bool:
    # if not isinstance(filepath, pathlib.Path):
    """Checks for file path access

    Args:
        filepath (str | pathlib.Path): path to file
        access_type (int, optional): _description_. Defaults to os.R_OK.

    ***

    #### **Access type can be:**

     - F_OK -> Checks file existence on path
     - R_OK -> Checks if file is readable
     - W_OK -> Checks if file is Writable
     - X_OK -> Checks if file can be executed

    ***
    Returns:
        bool: _description_
    """  #     return False
    if not os.path.isfile(filepath):
        return False
    return os.access(access_type)


def x_check_filepath_permission__mutmut_7(filepath, access_type: int = os.R_OK) -> bool:
    # if not isinstance(filepath, pathlib.Path):
    """Checks for file path access

    Args:
        filepath (str | pathlib.Path): path to file
        access_type (int, optional): _description_. Defaults to os.R_OK.

    ***

    #### **Access type can be:**

     - F_OK -> Checks file existence on path
     - R_OK -> Checks if file is readable
     - W_OK -> Checks if file is Writable
     - X_OK -> Checks if file can be executed

    ***
    Returns:
        bool: _description_
    """  #     return False
    if not os.path.isfile(filepath):
        return False
    return os.access(filepath, )

x_check_filepath_permission__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_filepath_permission__mutmut_1': x_check_filepath_permission__mutmut_1, 
    'x_check_filepath_permission__mutmut_2': x_check_filepath_permission__mutmut_2, 
    'x_check_filepath_permission__mutmut_3': x_check_filepath_permission__mutmut_3, 
    'x_check_filepath_permission__mutmut_4': x_check_filepath_permission__mutmut_4, 
    'x_check_filepath_permission__mutmut_5': x_check_filepath_permission__mutmut_5, 
    'x_check_filepath_permission__mutmut_6': x_check_filepath_permission__mutmut_6, 
    'x_check_filepath_permission__mutmut_7': x_check_filepath_permission__mutmut_7
}
x_check_filepath_permission__mutmut_orig.__name__ = 'x_check_filepath_permission'


def check_dir_existence(
    directory: typing.Union[str, pathlib.Path],
) -> bool:
    args = [directory]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_dir_existence__mutmut_orig, x_check_dir_existence__mutmut_mutants, args, kwargs, None)


def x_check_dir_existence__mutmut_orig(
    directory: typing.Union[str, pathlib.Path],
) -> bool:
    """Check if a directory exists. Returns a true if it exists"""
    if isinstance(directory, pathlib.Path):
        return bool(directory.is_dir())
    return bool(os.path.isdir(directory))


def x_check_dir_existence__mutmut_1(
    directory: typing.Union[str, pathlib.Path],
) -> bool:
    """Check if a directory exists. Returns a true if it exists"""
    if isinstance(directory, pathlib.Path):
        return bool(None)
    return bool(os.path.isdir(directory))


def x_check_dir_existence__mutmut_2(
    directory: typing.Union[str, pathlib.Path],
) -> bool:
    """Check if a directory exists. Returns a true if it exists"""
    if isinstance(directory, pathlib.Path):
        return bool(directory.is_dir())
    return bool(None)


def x_check_dir_existence__mutmut_3(
    directory: typing.Union[str, pathlib.Path],
) -> bool:
    """Check if a directory exists. Returns a true if it exists"""
    if isinstance(directory, pathlib.Path):
        return bool(directory.is_dir())
    return bool(os.path.isdir(None))

x_check_dir_existence__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_dir_existence__mutmut_1': x_check_dir_existence__mutmut_1, 
    'x_check_dir_existence__mutmut_2': x_check_dir_existence__mutmut_2, 
    'x_check_dir_existence__mutmut_3': x_check_dir_existence__mutmut_3
}
x_check_dir_existence__mutmut_orig.__name__ = 'x_check_dir_existence'


def check_file_on_path(
    path: typing.Union[typing.LiteralString, pathlib.Path],
    filename: typing.Union[typing.LiteralString, pathlib.Path],
) -> bool:
    args = [path, filename]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_check_file_on_path__mutmut_orig, x_check_file_on_path__mutmut_mutants, args, kwargs, None)


def x_check_file_on_path__mutmut_orig(
    path: typing.Union[typing.LiteralString, pathlib.Path],
    filename: typing.Union[typing.LiteralString, pathlib.Path],
) -> bool:
    """Check if file exists on path. Returns true if file exists on that specified directory"""
    _filepath = os.path.join(path, filename)
    return os.path.exists(_filepath)


def x_check_file_on_path__mutmut_1(
    path: typing.Union[typing.LiteralString, pathlib.Path],
    filename: typing.Union[typing.LiteralString, pathlib.Path],
) -> bool:
    """Check if file exists on path. Returns true if file exists on that specified directory"""
    _filepath = None
    return os.path.exists(_filepath)


def x_check_file_on_path__mutmut_2(
    path: typing.Union[typing.LiteralString, pathlib.Path],
    filename: typing.Union[typing.LiteralString, pathlib.Path],
) -> bool:
    """Check if file exists on path. Returns true if file exists on that specified directory"""
    _filepath = os.path.join(None, filename)
    return os.path.exists(_filepath)


def x_check_file_on_path__mutmut_3(
    path: typing.Union[typing.LiteralString, pathlib.Path],
    filename: typing.Union[typing.LiteralString, pathlib.Path],
) -> bool:
    """Check if file exists on path. Returns true if file exists on that specified directory"""
    _filepath = os.path.join(path, None)
    return os.path.exists(_filepath)


def x_check_file_on_path__mutmut_4(
    path: typing.Union[typing.LiteralString, pathlib.Path],
    filename: typing.Union[typing.LiteralString, pathlib.Path],
) -> bool:
    """Check if file exists on path. Returns true if file exists on that specified directory"""
    _filepath = os.path.join(filename)
    return os.path.exists(_filepath)


def x_check_file_on_path__mutmut_5(
    path: typing.Union[typing.LiteralString, pathlib.Path],
    filename: typing.Union[typing.LiteralString, pathlib.Path],
) -> bool:
    """Check if file exists on path. Returns true if file exists on that specified directory"""
    _filepath = os.path.join(path, )
    return os.path.exists(_filepath)


def x_check_file_on_path__mutmut_6(
    path: typing.Union[typing.LiteralString, pathlib.Path],
    filename: typing.Union[typing.LiteralString, pathlib.Path],
) -> bool:
    """Check if file exists on path. Returns true if file exists on that specified directory"""
    _filepath = os.path.join(path, filename)
    return os.path.exists(None)

x_check_file_on_path__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_check_file_on_path__mutmut_1': x_check_file_on_path__mutmut_1, 
    'x_check_file_on_path__mutmut_2': x_check_file_on_path__mutmut_2, 
    'x_check_file_on_path__mutmut_3': x_check_file_on_path__mutmut_3, 
    'x_check_file_on_path__mutmut_4': x_check_file_on_path__mutmut_4, 
    'x_check_file_on_path__mutmut_5': x_check_file_on_path__mutmut_5, 
    'x_check_file_on_path__mutmut_6': x_check_file_on_path__mutmut_6
}
x_check_file_on_path__mutmut_orig.__name__ = 'x_check_file_on_path'


def get_file_loc(filename) -> pathlib.Path: ...


def get_file_name(filename: typing.Optional[str]) -> str:
    args = [filename]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_file_name__mutmut_orig, x_get_file_name__mutmut_mutants, args, kwargs, None)


def x_get_file_name__mutmut_orig(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_1(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_2(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return "XXXX"
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_3(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = None

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_4(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip(None)

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_5(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.lstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_6(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("XX/\\XX")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_7(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = None

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_8(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace(None, "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_9(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", None)

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_10(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_11(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", )

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_12(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("XX\\XX", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_13(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "XX/XX")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_14(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = None

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_15(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split(None)

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_16(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("XX/XX")

    # Split and return the last path component
    return parts[-1] if filename else ""


def x_get_file_name__mutmut_17(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[+1] if filename else ""


def x_get_file_name__mutmut_18(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-2] if filename else ""


def x_get_file_name__mutmut_19(filename: typing.Optional[str]) -> str:
    # If filename is None or empty, return empty string instead of None
    if not filename:
        return ""
    # Remove trailing slashes or backslashes
    filename = filename.rstrip("/\\")

    # Normalize Windows backslashes to forward slashes
    filename = filename.replace("\\", "/")

    parts = filename.split("/")

    # Split and return the last path component
    return parts[-1] if filename else "XXXX"

x_get_file_name__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_file_name__mutmut_1': x_get_file_name__mutmut_1, 
    'x_get_file_name__mutmut_2': x_get_file_name__mutmut_2, 
    'x_get_file_name__mutmut_3': x_get_file_name__mutmut_3, 
    'x_get_file_name__mutmut_4': x_get_file_name__mutmut_4, 
    'x_get_file_name__mutmut_5': x_get_file_name__mutmut_5, 
    'x_get_file_name__mutmut_6': x_get_file_name__mutmut_6, 
    'x_get_file_name__mutmut_7': x_get_file_name__mutmut_7, 
    'x_get_file_name__mutmut_8': x_get_file_name__mutmut_8, 
    'x_get_file_name__mutmut_9': x_get_file_name__mutmut_9, 
    'x_get_file_name__mutmut_10': x_get_file_name__mutmut_10, 
    'x_get_file_name__mutmut_11': x_get_file_name__mutmut_11, 
    'x_get_file_name__mutmut_12': x_get_file_name__mutmut_12, 
    'x_get_file_name__mutmut_13': x_get_file_name__mutmut_13, 
    'x_get_file_name__mutmut_14': x_get_file_name__mutmut_14, 
    'x_get_file_name__mutmut_15': x_get_file_name__mutmut_15, 
    'x_get_file_name__mutmut_16': x_get_file_name__mutmut_16, 
    'x_get_file_name__mutmut_17': x_get_file_name__mutmut_17, 
    'x_get_file_name__mutmut_18': x_get_file_name__mutmut_18, 
    'x_get_file_name__mutmut_19': x_get_file_name__mutmut_19
}
x_get_file_name__mutmut_orig.__name__ = 'x_get_file_name'


# def get_hash(data) -> hashlib._Hash:
#     hash = hashlib.sha256()
#     hash.update(data.encode())
#     hash.digest()
#     return hash


def digest_hash() -> None: ...
