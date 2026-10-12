"""AMU / Happy-Hare MMU package.

Architecture:
    AMUManager (manager.py)
        └── AMU backend
    Models (models.py)
        └── Typed dataclasses and state enums
    ConfigToggler (config_toggler.py)
        └── AMU/non-AMU printer.cfg switch
"""

from .config_toggler import ConfigToggler, ToggleResult
from .manager import AMUManager
from .models import (
    FilamentPos,
    GateInfo,
    GateStatus,
    MMUState,
    SpoolmanSupport,
)

__all__: list[str] = [
    "AMUManager",
    "ConfigToggler",
    "ToggleResult",
    "FilamentPos",
    "GateInfo",
    "GateStatus",
    "MMUState",
    "SpoolmanSupport",
]
