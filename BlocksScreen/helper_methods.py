# Collection of useful methods
#
# This file contains some methods derived from KlipperScreen
# Original source: https://github.com/KlipperScreen/KlipperScreen
# License: GNU General Public License v3
# Modifications made by Hugo Costa <h.costa@blockstec.com> (2025) for BlocksScreen


import ctypes
import enum
import logging
import math
import os
import pathlib
import struct

logger = logging.getLogger(__name__)

try:
    ctypes.cdll.LoadLibrary("libXext.so.6")
    libxext = ctypes.CDLL("libXext.so.6")

    class DPMSState(enum.Enum):
        """Available DPMS states."""

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

    def get_dpms_timeouts() -> dict:
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

    def set_dpms_timeouts(suspend: int = 0, standby: int = 0, off: int = 0) -> dict:
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

    def get_dpms_info() -> dict:
        """Get DPMS information

        Returns:
            dict: Dpms state
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


def convert_bytes_to_mb(size_bytes: int | float) -> float:
    """Converts byte size to megabyte size.

    Args:
        size_bytes: Value in bytes.

    Returns:
        Equivalent value in megabytes.
    """
    _relation = 2 ** (-20)
    return size_bytes * _relation


def calculate_current_layer(
    z_position: float,
    layer_height: float,
    first_layer_height: float,
    max_layers: int = 0,
) -> int:
    """Calculate current layer from Z position (fallback when Klipper
    does not provide ``print_stats.info.current_layer``).

    Formula ported from Mainsail ``getPrintCurrentLayer`` getter:
    ``src/store/printer/getters.ts`` in ``mainsail-crew/mainsail``.

    Uses ``ceil((z - first_layer_height) / layer_height + 1)``
    and clamps the result to ``[0, max_layers]``.

    Returns:
        int: Current layer number (0 when not yet printing).
    """
    if layer_height <= 0 or first_layer_height < 0:
        return 0

    layer = math.ceil((z_position - first_layer_height) / layer_height + 1)
    if max_layers > 0 and layer > max_layers:
        return max_layers
    return max(0, layer)


def calculate_max_layers(
    object_height: float,
    layer_height: float,
    first_layer_height: float,
) -> int:
    """Calculate total layers from metadata dimensions (fallback when
    Klipper does not provide ``print_stats.info.total_layer``).

    Formula ported from Mainsail ``getPrintMaxLayers`` getter:
    ``src/store/printer/getters.ts`` in ``mainsail-crew/mainsail``.

    Uses ``ceil((object_height - first_layer_height) / layer_height + 1)``.

    Returns:
        int: Total layer count, or 0 if metadata is insufficient.
    """
    if layer_height <= 0 or object_height <= 0:
        return 0
    return max(1, math.ceil((object_height - first_layer_height) / layer_height + 1))


def estimate_print_time(seconds: int) -> list[int]:
    """Convert *seconds* to ``[days, hours, minutes, seconds]``."""
    num_min, secs = divmod(seconds, 60)
    num_hours, mins = divmod(num_min, 60)
    days, hours = divmod(num_hours, 24)
    return [days, hours, mins, secs]


def normalize(
    value: float,
    r_min: float = 0.0,
    r_max: float = 1.0,
    t_min: float = 0.0,
    t_max: float = 100.0,
) -> float:
    """Scale *value* from range [r_min, r_max] into [t_min, t_max]."""
    return (value - r_min) / (r_max - r_min) * (t_max - t_min) + t_min


def check_filepath_permission(
    filepath: str | pathlib.Path, access_type: int = os.R_OK
) -> bool:
    """Check whether *filepath* exists and has the requested access.

    Args:
        filepath: Path to file.
        access_type: ``os.F_OK`` (existence), ``os.R_OK`` (read),
            ``os.W_OK`` (write), or ``os.X_OK`` (execute).

    Returns:
        ``True`` if the file exists and satisfies *access_type*.
    """
    path = pathlib.Path(filepath)
    return path.is_file() and os.access(path, access_type)


def check_dir_existence(directory: str | pathlib.Path) -> bool:
    """Return ``True`` if *directory* exists and is a directory."""
    return pathlib.Path(directory).is_dir()


def check_file_on_path(
    path: str | pathlib.Path,
    filename: str | pathlib.Path,
) -> bool:
    """Return ``True`` if *filename* exists under *path*."""
    return (pathlib.Path(path) / filename).exists()


def get_file_name(filename: str | None) -> str:
    """Extract the basename from a file path (handles ``/`` and ``\\``).

    Returns:
        The last path component, or ``""`` if *filename* is falsy.
    """
    if not filename:
        return ""
    return pathlib.PurePosixPath(filename.replace("\\", "/")).name
