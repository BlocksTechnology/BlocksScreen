"""Unit test for Blockcsreen.lib.klipper_message_filter"""

import pytest

from BlocksScreen.lib.klipper_message_filter import (
    MessageRule,
    MessageSource,
    Severity,
    RULES,
    _INDEX,
    _re,
    _sub,
    match_message,
)


def test_severity_info_is_1() -> None:
    assert Severity.INFO == 1


def test_severity_warning_is_2() -> None:
    assert Severity.WARNING == 2


def test_severity_error_is_3() -> None:
    assert Severity.ERROR == 3


def test_index_covers_all_sources() -> None:
    assert set(_INDEX.keys()) == set(MessageSource)


def test_message_rule_is_hashable() -> None:
    rule = RULES[0]
    s: set[MessageRule] = {rule}
    assert rule in s


def test_sub_matches_lowercase() -> None:
    m = _sub("filament runout")
    assert m("filament runout")


def test_sub_matches_uppercase() -> None:
    m = _sub("filament runout")
    assert m("FILAMENT RUNOUT")


def test_sub_matches_mixed_case_input() -> None:
    m = _sub("filament runout")
    assert m("Filament Runout detected at sensor")


def test_sub_no_match() -> None:
    m = _sub("filament runout")
    assert not m("no filament")


def test_re_matches_pattern() -> None:
    m = _re(r"temp exceeded \d+")
    assert m("temp exceeded 300")


def test_re_matches_case_insensitive() -> None:
    m = _re(r"temp exceeded \d+")
    assert m("TEMP EXCEEDED 250")


def test_re_no_match() -> None:
    m = _re(r"temp exceeded \d+")
    assert not m("temp is fine")


@pytest.mark.parametrize(
    "source, text, expected_display, expected_severity",
    [
        # CPU THROTTLE
        (
            MessageSource.CPU_THROTTLE,
            "Under-Voltage Detected",
            "Low Voltage",
            Severity.WARNING,
        ),
        (
            MessageSource.CPU_THROTTLE,
            "Frequency Capped",
            "CPU Throttled",
            Severity.WARNING,
        ),
        (
            MessageSource.CPU_THROTTLE,
            "Currently Throttled",
            "CPU Throttled",
            Severity.WARNING,
        ),
        (
            MessageSource.CPU_THROTTLE,
            "Temperature Limit Active",
            "High CPU Temp",
            Severity.WARNING,
        ),
        # GCODEs Errors - Heater / Temperature
        (
            MessageSource.GCODE_ERROR,
            "ADC out of range",
            "Temp Sensor Error",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Heater extruder not heating at expected rate",
            "Heater Failure",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Extrude below minimum temp",
            "Extruder Too Cold",
            Severity.WARNING,
        ),
        # GCODEs Errors - MCU / Timing
        (
            MessageSource.GCODE_ERROR,
            "Lost communication with MCU 'mcu'",
            "MCU Offline",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Timer too close",
            "MCU Overload",
            Severity.ERROR,
        ),
        # GCODEs Errors - Homing
        (
            MessageSource.GCODE_ERROR,
            "Timeout during homing move",
            "Homing Timeout",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Must home axis first: 1.000 500.000 5.000 [0.000]",
            "Axis Not Homed",
            Severity.ERROR,
        ),
        (
            MessageSource.MOONRAKER_ERROR,
            "Must home axis first: 1.000 500.000 5.000 [0.000]",
            "Axis Not Homed",
            Severity.ERROR,
        ),
        # GCODEs Errors - General
        (
            MessageSource.GCODE_ERROR,
            "filament runout detected",
            "Filament Runout",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "no filament in sensor",
            "No Filament",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "printer not ready",
            "Printer Not Ready",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Move out of range: X 250.0",
            "Move Out of Range",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "endstop not triggered after 5mm",
            "Homing Failed",
            Severity.ERROR,
        ),
        # GCODEs Errors - Beacon
        (
            MessageSource.GCODE_ERROR,
            "sensor not in valid range",
            "Probe Not Ready",
            Severity.WARNING,
        ),
        (
            MessageSource.GCODE_ERROR,
            "No model loaded in for beacon",
            "No Probe Model",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "model coefficient error in calibration",
            "Probe Calibration Error",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "scan not supported in this mode",
            "Probe Scan Unavailable",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "contact not supported",
            "Contact Mode Unavailable",
            Severity.WARNING,
        ),
        (
            MessageSource.GCODE_ERROR,
            "contact probe triggered before expected",
            "Probe Triggered Early",
            Severity.WARNING,
        ),
        (
            MessageSource.GCODE_ERROR,
            "unable to start resonance test",
            "Probe Start Failed",
            Severity.ERROR,
        ),
        # GCODEs Errors - Happy Hare
        (
            MessageSource.GCODE_ERROR,
            "mmu not enabled",
            "MMU Not Enabled",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Filament stuck in extruder",
            "Filament Jammed",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "filament jammed at nozzle",
            "Filament Jammed",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "filament not detected at gate 2",
            "No Filament in MMU",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "too many retries loading filament",
            "MMU Retry Limit",
            Severity.ERROR,
        ),
        (MessageSource.GCODE_ERROR, "gate empty", "Spool Empty", Severity.WARNING),
        # Gcode Echo
        (
            MessageSource.GCODE_ECHO,
            "Recommended shaper_type_x = mzv, shaper_freq_x = 75.3 Hz",
            "Resonance Test Done",
            Severity.INFO,
        ),
        (
            MessageSource.GCODE_ECHO,
            "The SAVE_CONFIG command will update the printer config file",
            "Config Needs Saving",
            Severity.INFO,
        ),
        # Moonraker Errors
        (
            MessageSource.MOONRAKER_ERROR,
            "beacon: sensor not in valid range",
            "Probe Error",
            Severity.ERROR,
        ),
        # GCODEs Errors - Eddy probe
        (
            MessageSource.GCODE_ERROR,
            "Must calibrate probe_eddy_current first",
            "Eddy Not Calibrated",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "probe_eddy_current sensor outage on mcu",
            "Eddy Sensor Offline",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Unable to obtain probe_eddy_current sensor readings",
            "Eddy No Readings",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "tap detected too close to start of move",
            "Eddy Early Trigger",
            Severity.WARNING,
        ),
        (
            MessageSource.GCODE_ERROR,
            "unable to detect tap: no trigger",
            "Eddy Tap Failed",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "frequency stops decreasing at step 1.250",
            "Eddy Calibration Failed",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "frequency too noisy at step 2.000 -> 3.500",
            "Eddy Frequency Noise",
            Severity.WARNING,
        ),
        (
            MessageSource.GCODE_ERROR,
            "eddy: gaps in the data: 0.123 > 0.050",
            "Eddy Data Gap",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "eddy: clkin frequency too low: 1000 < 2000",
            "Eddy Clock Error",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "insufficient lift (0.000050 vs 0.000100)",
            "Eddy Low Lift",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "invalid free air slope (s=0.001 s2=0.002)",
            "Eddy Bad Baseline",
            Severity.ERROR,
        ),
        # GCODEs Errors - Bed leveling
        (
            MessageSource.GCODE_ERROR,
            "Must run Z_TILT_ADJUST before bed_mesh",
            "Z Tilt Required",
            Severity.WARNING,
        ),
        # GCODEs Errors - Resonance tester
        (
            MessageSource.GCODE_ERROR,
            "no accelerometers specified to measure",
            "No Accelerometer",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "measured no data on the accelerometer",
            "Accelerometer No Data",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Insufficient maximum z velocity for the test",
            "Z Speed Too Low",
            Severity.WARNING,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Insufficient maximum z acceleration for the test",
            "Z Accel Too Low",
            Severity.WARNING,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Invalid adxl345 id (got 0x00 vs 0xe5)",
            "ADXL Chip Not Found",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Failed to set adxl345 register",
            "ADXL Connection Error",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "no accelerometer measurements found",
            "No Measurements",
            Severity.ERROR,
        ),
        # GCODEs Errors - General (macro / LED)
        (
            MessageSource.GCODE_ERROR,
            "Error loading template 'gcode_macro START_PRINT'",
            "Macro Syntax Error",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "Macro called recursively",
            "Macro Loop Detected",
            Severity.ERROR,
        ),
        (
            MessageSource.GCODE_ERROR,
            "neopixel chain too long for mcu bitbang",
            "Too Many LEDs",
            Severity.ERROR,
        ),
        # GCODEs Errors - Kalico / Danger Klipper
        (
            MessageSource.GCODE_ERROR,
            "error on unused option 'extruder' 'pressure_advance_smooth_time'",
            "Unused Config Option",
            Severity.WARNING,
        ),
        # No Match
        (MessageSource.GCODE_ERROR, "unknown gcode error xyz", None, None),
        (MessageSource.GCODE_ECHO, "some echo message", None, None),
        (MessageSource.MOONRAKER_ERROR, "some moonraker error", None, None),
    ],
)
def test_match_message(
    source: MessageSource,
    text: str,
    expected_display: str | None,
    expected_severity: Severity | None,
) -> None:
    rule = match_message(source, text)
    if expected_display is None:
        assert rule is None
    else:
        assert rule is not None
        assert rule.display == expected_display
        assert rule.severity == expected_severity


def test_match_message_case_insensitive() -> None:
    rule = match_message(MessageSource.GCODE_ERROR, "FILAMENT RUNOUT")
    assert rule is not None
    assert rule.display == "Filament Runout"


def test_match_message_no_match_retuns_none() -> None:
    rule = match_message(MessageSource.GCODE_ERROR, "something completely unrelated")
    assert rule is None


def test_match_message_source_isolation() -> None:
    rule = match_message(MessageSource.GCODE_ECHO, "filament runout")
    assert rule is None


def test_message_rule_hint_defaults_to_none() -> None:
    rule = MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("x"),
        display="x",
        severity=Severity.INFO,
    )
    assert rule.hint is None


def test_full_display_without_hint() -> None:
    rule = MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("x"),
        display="No Hint",
        severity=Severity.INFO,
    )
    assert rule.full_display == "No Hint"


def test_full_display_with_hint() -> None:
    rule = MessageRule(
        source=MessageSource.GCODE_ERROR,
        matcher=_sub("x"),
        display="Title",
        hint="Action",
        severity=Severity.INFO,
    )
    assert rule.full_display == "Title\nAction"
