"""AMU / HAPPY-Hare MMU package

Architecture:
    AMUManager (manager.py)
        └── Main AMU manager its responsible for the AMU backend
    Models (models.py)
        └── Data classes for type safety
        └── Enums for states and types
"""

from .manager import AMUManager
from .models import (
    FilamentPos,
    GateInfo,
    GateStatus,
    MMUState,
    SpoolmanSupport,
)
from .config_toggler import ConfigToggler

__all__: list[str] = [
    # manager
    "AMUManager",
    # config_toggler
    "ConfigToggler",
    # models
    "FilamentPos",
    "GateInfo",
    "GateStatus",
    "MMUState",
    "SpoolmanSupport",
]
