"""Guard: compiled deps must stay at the field-validated aarch64 known-good pins.

These packages need an aarch64 wheel (or a clean source build) to install on the
Pi 5 field hardware. Bumping them silently - as automated dependency PRs have
done before - breaks the on-device ``pip install`` (PyQt6 6.10.0 has no aarch64
wheel, sdbus 0.14.1's wheel imports broken), which then thrashes the boot and
post-merge paths. This test fails if any compiled pin drifts away from the
known-good set, forcing an explicit on-hardware import test before the bump.
"""

from __future__ import annotations

import re
from pathlib import Path

_REQS = Path(__file__).resolve().parents[2] / "scripts" / "requirements.txt"

# Field-validated on Pi 5 aarch64 (see updater deployment notes). Do NOT bump
# without an on-hardware `pip install` + import test for the new version.
_KNOWN_GOOD = {
    "numpy": "2.1.0",
    "sdbus": "0.12.0",
    "PyQt6": "6.7.1",
    "PyQt6-Qt6": "6.7.2",
    "PyQt6_sip": "13.8.0",
}

_PIN_RE = re.compile(r"^\s*([A-Za-z0-9_.\-]+)\s*==\s*([^\s#]+)")


def _normalize(name: str) -> str:
    """Canonicalize a distribution name (PEP 503 - case/underscore-insensitive)."""
    return name.replace("_", "-").lower()


def _parse_pins(text: str) -> dict[str, str]:
    pins: dict[str, str] = {}
    for line in text.splitlines():
        match = _PIN_RE.match(line)
        if match:
            pins[_normalize(match.group(1))] = match.group(2)
    return pins


def test_compiled_pins_match_known_good() -> None:
    pins = _parse_pins(_REQS.read_text(encoding="utf-8"))
    for name, expected in _KNOWN_GOOD.items():
        key = _normalize(name)
        assert key in pins, f"{name} must stay exactly pinned (==) in requirements.txt"
        assert pins[key] == expected, (
            f"{name} pinned to {pins[key]}, expected field known-good {expected}. "
            "Bumping a compiled dep needs an on-hardware aarch64 import test first; "
            "update _KNOWN_GOOD here only after that passes."
        )
