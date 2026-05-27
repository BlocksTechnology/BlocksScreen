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
        hint="Check cooling",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.CPU_THROTTLE,
        matcher=_sub("currently throttled"),
        display="CPU Throttled",
        hint="Check cooling",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.CPU_THROTTLE,
        matcher=_sub("temperature limit"),
        display="High CPU Temp",
        hint="Check cooling",
        severity=Severity.WARNING,
    ),
    # ── Gcode errors — Beacon probe ────────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("sensor not in valid range"),
        display="Probe Not Ready",
        hint="Reposition probe",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("no model loaded"),
        display="No Probe Model",
        hint="Calibrate probe first",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("model coefficient"),
        display="Probe Calibration Error",
        hint="Recalibrate probe",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("scan not supported"),
        display="Probe Scan Unavailable",
        hint="Check probe config",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("contact not supported"),
        display="Contact Mode Unavailable",
        hint="Check probe config",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("contact probe triggered"),
        display="Probe Triggered Early",
        hint="Inspect probe",
        severity=Severity.WARNING,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("unable to start"),
        display="Probe Start Failed",
        hint="Check probe",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — Happy Hare MMU ──────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("mmu not enabled"),
        display="MMU Not Enabled",
        hint="Check MMU connection",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_re(r"filament.*(stuck|jammed)"),
        display="Filament Jammed",
        hint="Clear MMU path",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("filament not detected"),
        display="No Filament in MMU",
        hint="Check filament path",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("too many retries"),
        display="MMU Retry Limit",
        hint="Manual intervention needed",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("gate empty"),
        display="Spool Empty",
        hint="Change filament",
        severity=Severity.WARNING,
    ),
    # ── Gcode errors — heater / temperature ───────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("adc out of range"),
        display="Temp Sensor Error",
        hint="Check thermistor wiring",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("not heating at expected rate"),
        display="Heater Failure",
        hint="Check wiring and thermistor",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("below minimum temp"),
        display="Extruder Too Cold",
        hint="Heat up before extruding",
        severity=Severity.WARNING,
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
        matcher=_sub("timer too close"),
        display="MCU Overload",
        hint="Reduce CPU load",
        severity=Severity.ERROR,
    ),
    # ── Gcode errors — homing ──────────────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("timeout during homing"),
        display="Homing Timeout",
        hint="Check axis movement",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("must home axis first"),
        display="Axis Not Homed",
        hint="Home all axes first",
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
        hint="Check filament sensor",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("printer not ready"),
        display="Printer Not Ready",
        hint="Check connection",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("move out of range"),
        display="Move Out of Range",
        hint="Check print limits",
        severity=Severity.ERROR,
    ),
    MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("endstop not triggered"),
        display="Homing Failed",
        hint="Check endstop wiring",
        severity=Severity.ERROR,
    ),
    # ── Gcode echo ─────────────────────────────────────────────────────────────
    MessageRule(
        source=MessageSource.GCODE_ECHO,
        matcher=_re(r"recommended shaper_type_\w+ = \w+"),
        display="Resonance Test Done",
        hint="Run SAVE_CONFIG to apply",
        severity=Severity.INFO,
    ),
    MessageRule(
        source=MessageSource.GCODE_ECHO,
        matcher=_sub("save_config command will update"),
        display="Config Needs Saving",
        hint="Restart after SAVE_CONFIG",
        severity=Severity.INFO,
    ),
    # ── Moonraker errors ───────────────────────────────────────────────────────
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
        hint="Check probe connection",
        severity=Severity.ERROR,
    ),
)

_INDEX: dict[MessageSource, tuple[MessageRule, ...]] = {
    src: tuple(r for r in RULES if r.source is src) for src in MessageSource
}


def match_message(source: MessageSource, text: str) -> MessageRule | None:
    lo = text.lower()
    return next((r for r in _INDEX[source] if r.matcher(lo)), None)
