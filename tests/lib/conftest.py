import sys
from unittest.mock import MagicMock

import pytest

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


class _SdBusBaseError(Exception):
    pass


@pytest.fixture(scope="module", autouse=True)
def mock_sdbus():
    mock = MagicMock()
    mock.sd_bus_open_user = MagicMock(return_value=MagicMock())
    mock.SdBusBaseError = _SdBusBaseError
    with pytest.MonkeyPatch.context() as mp:
        for key in (
            "sdbus",
            "updater.dbus_service",
            "BlocksScreen.lib.updater_worker",
        ):
            mp.delitem(sys.modules, key, raising=False)
        mp.setitem(sys.modules, "sdbus", mock)
        mp.setitem(sys.modules, "updater.dbus_service", MagicMock())
        yield mock
