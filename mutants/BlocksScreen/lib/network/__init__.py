"""Network Manager Package

Architecture:
    NetworkManager (manager.py)
        └── Main thread interface with signals/slots
        └── Non-blocking API
        └── Caches state for quick access

    NetworkManagerWorker (worker.py)
        └── Runs in dedicated Thread
        └── Owns asyncio event loop
        └── Handles all D-Bus async operations

    Models (models.py)
        └── Data classes for type safety
        └── Enums for states and types
"""

from .manager import NetworkManager
from .models import (
    UNSUPPORTED_SECURITY_TYPES,
    ConnectionPriority,
    ConnectionResult,
    ConnectivityState,
    HotspotConfig,
    HotspotSecurity,
    NetworkInfo,
    NetworkState,
    NetworkStatus,
    PendingOperation,
    SavedNetwork,
    SecurityType,
    VlanInfo,
    WifiIconKey,
    is_connectable_security,
    is_hidden_ssid,
    signal_to_bars,
)

__all__ = [
    "NetworkManager",
    "ConnectionPriority",
    "ConnectionResult",
    "ConnectivityState",
    "HotspotConfig",
    "HotspotSecurity",
    "NetworkInfo",
    "NetworkState",
    "NetworkStatus",
    "PendingOperation",
    "SavedNetwork",
    "SecurityType",
    "UNSUPPORTED_SECURITY_TYPES",
    "VlanInfo",
    "WifiIconKey",
    # Utilities
    "is_connectable_security",
    "is_hidden_ssid",
    "signal_to_bars",
]
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore
