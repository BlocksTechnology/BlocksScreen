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
        hint="Move nozzle within the probe's sensing range",
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
        hint="Inspect probe tip for debris or damage",
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
        hint="Clear the obstruction and retry",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("filament not detected"),
        display="No Filament in MMU",
        hint="Reload filament in MMU",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("too many retries"),
        display="MMU Retry Limit",
        hint="Clear the MMU manually and retry",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("gate empty"),
        display="Spool Empty",
        hint="Replace the empty spool at this gate",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("runout detected on"),
        display="Filament Runout",
        hint="Replace the empty spool and resume",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("flowguard"),
        display="Filament Tangle Detected",
        hint="Clear tangle in filament path and resume",
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
        hint="Check power supply and USB cable",
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
        hint="Clear obstruction at endstop",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_re(r"homing (interrupted|aborted)"),
        display="Homing Interrupted",
        hint="Check for obstructions and retry",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — bed leveling ───────────────────────────────────────────
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

_INDEX: dict[MessageSource, tuple[MessageRule, ...]] = {
    src: tuple(r for r in RULES if r.source is src) for src in MessageSource
}


def match_message(source: MessageSource, text: str) -> MessageRule | None:
    lo = text.lower()
    return next((r for r in _INDEX[source] if r.matcher(lo)), None)
