import sys
from unittest.mock import MagicMock

sys.modules.setdefault("events", MagicMock())
sys.modules.setdefault("lib", MagicMock())
sys.modules.setdefault("lib.moonrakerComm", MagicMock())


_mocks = [
    "events",
    "helper_methods",
    "configfile",
    "lib",
    "lib.moonrakerComm",
    "lib.moonrest",
    "lib.utils",
    "lib.utils.RepeatedTimer",
    "websocket",
]


for _mod in _mocks:
    sys.modules.setdefault(_mod, MagicMock())
