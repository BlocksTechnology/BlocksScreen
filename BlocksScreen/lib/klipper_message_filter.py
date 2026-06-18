from __future__ import annotations

import enum
import re
from dataclasses import dataclass
from typing import Callable


class MessageSource(enum.Enum):
    GCODE_ERROR = "gcode_error"
    GCODE_ECHO = "gcode_echo"
    MOONRAKER_ERROR = "moonraker_error"
    CPU_THROTTLE = "cpu_throttle"
    KLIPPY_STATE = "klippy_state"


class Severity(enum.IntEnum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    IGNORE = 4


@dataclass(frozen=True, kw_only=True, slots=True)
class MessageRule:
    source: MessageSource
    matcher: Callable[[str], bool]
    display: str
    hint: str | None = None
    severity: Severity

    @property
    def full_display(self) -> str:
        return f"{self.display}\n{self.hint}" if self.hint else self.display


def _sub(needle: str) -> Callable[[str], bool]:
    lower = needle.lower()
    return lambda text: lower in text.lower()


def _re(pattern: str) -> Callable[[str], bool]:
    compiled_text = re.compile(pattern, re.I)
    return lambda text: compiled_text.search(text) is not None


RULES: tuple[MessageRule, ...] = (
    # ── CPU throttle ───────────────────────────────────────────────────────────
    MessageRule(
        source=MessageSource.CPU_THROTTLE,
        matcher=_sub("under-voltage"),
        display="Low Voltage",
        hint="Check power supply",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.CPU_THROTTLE,
        matcher=_sub("frequency capped"),
        display="CPU Throttled",
        hint="Check board cooling",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.CPU_THROTTLE,
        matcher=_sub("currently throttled"),
        display="CPU Throttled",
        hint="Check board cooling",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.CPU_THROTTLE,
        matcher=_sub("temperature limit"),
        display="High CPU Temp",
        hint="Check board cooling",
        severity=Severity.WARNING,
    ),
    # ── Gcode errors — Beacon probe ────────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("sensor not in valid range"),
        display="Probe Not Ready",
        hint="Move nozzle closer to the bed",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("no model loaded"),
        display="No Probe Model",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("model coefficient"),
        display="Probe Calibration Error",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("scan not supported"),
        display="Probe Scan Unavailable",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("contact not supported"),
        display="Contact Mode Unavailable",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("contact probe triggered"),
        display="Probe Triggered Early",
        hint="Check probe tip for debris",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("unable to start"),
        display="Probe Start Failed",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("scan height"),
        display="Beacon Scan Height Invalid",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — BLTouch probe ──────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("failed to verify sensor state"),
        display="BLTouch Verify Failed",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — Eddy probe ─────────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("must calibrate probe_eddy_current"),
        display="Eddy Not Calibrated",
        hint="Calibrate the Eddy probe first",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("probe_eddy_current sensor outage"),
        display="Eddy Sensor Offline",
        hint="Check probe cable",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("unable to obtain probe_eddy_current"),
        display="Eddy No Readings",
        hint="Check the probe cable",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("tap detected too close to start of move"),
        display="Eddy Early Trigger",
        hint="Adjust probe clearance",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("unable to detect tap"),
        display="Eddy Tap Failed",
        hint="Check the probe dock",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("frequency stops decreasing"),
        display="Eddy Calibration Failed",
        hint="Recalibrate the Eddy probe",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("frequency too noisy"),
        display="Eddy Frequency Noise",
        hint="Keep probe cables away from power cables",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("eddy: gaps in the data"),
        display="Eddy Data Gap",
        hint="Restart Klipper",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("eddy: clkin frequency too low"),
        display="Eddy Clock Error",
        hint="Restart Klipper",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("insufficient lift"),
        display="Eddy Low Lift",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("invalid free air slope"),
        display="Eddy Bad Baseline",
        hint="Recalibrate the probe",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — probe calibration ─────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("manual probe failed"),
        display="Manual Probe Incomplete",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("25 microns"),
        display="Probe Accuracy Poor",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("location bias"),
        display="Probe Location Bias",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("samples_tolerance"),
        display="Probe Spread Too High",
        hint="Clean the probe tip and retry",
        severity=Severity.WARNING,
    ),
    # ── Gcode errors — Happy Hare MMU ──────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("mmu not enabled"),
        display="MMU Not Enabled",
        hint="Restart Klipper",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_re(r"filament.*(stuck|jammed)"),
        display="Filament Jammed",
        hint="Clear the obstruction",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("filament not detected"),
        display="No Filament in MMU",
        hint="Reload filament",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("too many retries"),
        display="MMU Retry Limit",
        hint="Clear the MMU manually",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("gate empty"),
        display="Spool Empty",
        hint="Replace the empty spool",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("runout detected on"),
        display="Filament Runout",
        hint="Replace the empty spool",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("flowguard"),
        display="Filament Tangle Detected",
        hint="Clear the tangle",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — heater / temperature ───────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("adc out of range"),
        display="Temp Sensor Error",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("not heating at expected rate"),
        display="Heater Failure",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("below minimum temp"),
        display="Extruder Too Cold",
        hint="Heat up the nozzle first",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("temperature overshoot"),
        display="Heater Overshoot",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("will exceed max_duration"),
        display="Heater PWM Fault",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("cooling at unexpected rate"),
        display="Heater Decoupled",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — MCU / timing ────────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("lost communication with mcu"),
        display="MCU Offline",
        hint="Check USB cable",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("spontaneous restart"),
        display="MCU Restarted",
        hint="Check power and USB cable",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("spi_transfer"),
        display="SPI Communication Error",
        hint="Restart Klipper",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("timer too close"),
        display="MCU Overload",
        hint="Restart Klipper",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("step pulse duration"),
        display="Stepper Timing Error",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_re(r"tmc.*reports error"),
        display="Stepper Driver Error",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — homing ──────────────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("timeout during homing"),
        display="Homing Timeout",
        hint="Check for obstructions",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("must home axis first"),
        display="Axis Not Homed",
        hint="Home all axes first",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_re(r"endstop .* still triggered"),
        display="Endstop Stuck",
        hint="Clear the endstop area",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_re(r"homing (interrupted|aborted)"),
        display="Homing Interrupted",
        hint="Check for obstructions",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — bed leveling ───────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_re(r"must.*z_tilt_adjust"),
        display="Z Tilt Required",
        hint="Adjust Z tilt first",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("unable to probe bed point"),
        display="Bed Mesh Point Failed",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_re(r"unable to converge|max_adjust"),
        display="Leveling Failed",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — resonance tester ──────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("no accelerometers specified"),
        display="No Accelerometer",
        hint="Connect an accelerometer first",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("measured no data"),
        display="Accelerometer No Data",
        hint="Check sensor wiring",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("insufficient maximum z velocity"),
        display="Z Speed Too Low",
        hint="Increase max Z speed",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("insufficient maximum z acceleration"),
        display="Z Accel Too Low",
        hint="Increase max Z acceleration",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("invalid adxl345 id"),
        display="ADXL Chip Not Found",
        hint="Check sensor wiring",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("failed to set adxl345 register"),
        display="ADXL Connection Error",
        hint="Check sensor wiring",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("no accelerometer measurements found"),
        display="No Measurements",
        hint="Check sensor connection",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — general ─────────────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("filament runout"),
        display="Filament Runout",
        hint="Load new filament",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("no filament"),
        display="No Filament",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("printer not ready"),
        display="Printer Not Ready",
        hint="Restart Klipper",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("move out of range"),
        display="Move Out of Range",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("endstop not triggered"),
        display="Homing Failed",
        hint="Check for obstructions",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("kinematically unreachable"),
        display="Position Unreachable",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("emergency button"),
        display="Emergency Stop",
        hint="Clear E-stop and restart Klipper",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("webhooks request"),
        display="Shutdown via Webhook",
        hint="Restart Klipper",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("error loading template"),
        display="Macro Syntax Error",
        hint="Check macros for syntax errors",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("called recursively"),
        display="Macro Loop Detected",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("neopixel chain too long"),
        display="Too Many LEDs",
        hint="Reduce the LED chain length",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — Kalico / Danger Klipper ───────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("error on unused option"),
        display="Unused Config Option",
        hint="Remove unknown settings from printer.cfg",
        severity=Severity.WARNING,
    ),
    # ── Gcode echo ─────────────────────────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ECHO,
        matcher=_sub("filament_switch_sensor"),
        display="MMU Sensor Conflict",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ECHO,
        matcher=_re(r"recommended shaper_type_\w+ = \w+"),
        display="Resonance Test Done",
        hint="Save config to apply",
        severity=Severity.INFO,
    ),
    MessageRule(
        source=MessageSource.GCODE_ECHO,
        matcher=_re(r"recommended shaper_freq(?:uency)?"),
        display="Shaper Frequency Ready",
        hint="Save config to apply",
        severity=Severity.INFO,
    ),
    MessageRule(
        source=MessageSource.GCODE_ECHO,
        matcher=_sub("save_config command will update"),
        display="Config Needs Saving",
        hint="Save config then restart",
        severity=Severity.INFO,
    ),
    # ── Moonraker errors ───────────────────────────────────────────────────────
    MessageRule(
        source=MessageSource.MOONRAKER_ERROR,
        matcher=_re(r"mcu\b.*shutdown"),
        display="MCU Shutdown",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.MOONRAKER_ERROR,
        matcher=_sub("must home axis first"),
        display="Axis Not Homed",
        hint="Home all axes first",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.MOONRAKER_ERROR,
        matcher=_sub("beacon"),
        display="Probe Error",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.MOONRAKER_ERROR,
        matcher=_re(r"tmc.*(overtemp|ot=1)"),
        display="Stepper Overheating",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.MOONRAKER_ERROR,
        matcher=_re(r"unable to read tmc uart"),
        display="Stepper Driver Offline",
        severity=Severity.ERROR,
    ),
    # ── Klippy state ───────────────────────────────────────────────────────────
    MessageRule(
        source=MessageSource.KLIPPY_STATE,
        matcher=_sub("shutdown"),
        display="Klipper Shutdown",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.KLIPPY_STATE,
        matcher=_sub("error"),
        display="Klipper Error",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.KLIPPY_STATE,
        matcher=_sub("disconnected"),
        display="Klipper Disconnected",
        hint="Restart Klipper",
        severity=Severity.WARNING,
    ),
)

IGNORED_RULE = MessageRule(
    source=MessageSource.GCODE_ECHO,  # placeholder, wont mater
    matcher=lambda _: False,
    display="",
    severity=Severity.IGNORE,
)

_IGNORED: tuple[re.Pattern, ...] = (
    re.compile(r"REMOVED log_path=", re.I),
    # add more patterns as needed,
)

_INDEX: dict[MessageSource, tuple[MessageRule, ...]] = {
    src: tuple(r for r in RULES if r.source is src) for src in MessageSource
}


def match_message(source: MessageSource, text: str) -> MessageRule | None:
    if any(p.search(text) for p in _IGNORED):
        return IGNORED_RULE
    lo = text.lower()
    return next((r for r in _INDEX[source] if r.matcher(lo)), None)
