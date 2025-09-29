# This file contains some methods derived from KlipperScreen
# Original source: https://github.com/KlipperScreen/KlipperScreen
# License: GNU General Public License v3
# Modifications made by Hugo Costa <h.costa@blockstec.com> (2025) for BlocksScreen 


import ctypes
import os
import enum
import logging
import pathlib
import struct
import typing


try:
    ctypes.cdll.LoadLibrary("libXext.so.6")
    libxext = ctypes.CDLL("libXext.so.6")

    class DPMSState(enum.Enum):
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

                    if libxext.DPMSGetTimeouts(
                        display, standby_p, suspend_p, off_p
                    ):
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

                    if libxext.DPMSGetTimeouts(
                        display, standby_p, suspend_p, off_p
                    ):
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
        set_dpms_mode(DPMSState.OFF)

except OSError as e:
    logging.exception(f"OSError couldn't load DPMS library: {e}")
except Exception as e:
    logging.exception(f"Unexpected exception occurred {e}")


def convert_bytes_to_mb(self, bytes: int | float) -> float:
    """Converts byte size to megabyte size

    Args:
        bytes (int | float): bytes

    Returns:
        mb: float that represents the number of mb
    """
    _relation = 2 ** (-20)
    return bytes * _relation


def calculate_current_layer(
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
    _current_layer = 1 + (z_position - first_layer_height) / layer_height

    return int(_current_layer)


def estimate_print_time(seconds: int) -> list:
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


def normalize(value, r_min=0.0, r_max=1.0, t_min=0.0, t_max=100):
    # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
    c1 = (value - r_min) / (r_max - r_min)
    c2 = (t_max - t_min) + t_min
    return c1 * c2


def check_filepath_permission(filepath, access_type: int = os.R_OK) -> bool:
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


def check_dir_existence(
    directory: typing.Union[str, pathlib.Path],
) -> bool:
    if isinstance(directory, pathlib.Path):
        return bool(directory.is_dir())
    return bool(os.path.isdir(directory))


def check_file_on_path(
    path: typing.Union[typing.LiteralString, pathlib.Path],
    filename: typing.Union[typing.LiteralString, pathlib.Path],
) -> bool:
    _filepath = os.path.join(path, filename)
    return os.path.exists(_filepath)


def get_file_loc(filename) -> pathlib.Path:
    ...


# def get_hash(data) -> hashlib._Hash:
#     hash = hashlib.sha256()
#     hash.update(data.encode())
#     hash.digest()
#     return hash



def digest_hash() -> None: ...
