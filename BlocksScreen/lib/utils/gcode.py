from __future__ import annotations


def fan_speed_gcode(name: str, percentage: int) -> str:
    """Return Klipper gcode for a fan speed change."""
    if name.lower() == "fan":
        return f"M106 S{round(percentage * 255 / 100)}"
    gcode_name = name.replace(" ", "_")
    return f"SET_FAN_SPEED FAN={gcode_name} SPEED={percentage / 100}"
