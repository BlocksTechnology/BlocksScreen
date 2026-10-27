"""FilamentTab handling of the AMU manager's state stream."""

import sys
from unittest.mock import MagicMock

import devices.amu.manager as amu_manager_module
from devices.amu.models import FilamentPos, MMUState

vars(sys.modules["devices.amu"]).update(
    AMUManager=amu_manager_module.AMUManager,
    FilamentPos=FilamentPos,
    MMUState=MMUState,
)
# Other test modules leave session-wide stand-ins for these; the tab needs the real API.
_STUBBED = (
    "lib.utils.icon_button",
    "lib.utils.blocks_button",
    "lib.utils.blocks_label",
    "lib.utils.blocks_linedit",
    "lib.utils.blocks_Scrollbar",
    "lib.panels.widgets.Common",
    "lib.panels.widgets.FilamentTab",
    "lib.panels.filamentTab",
)
_saved = {m: sys.modules.pop(m) for m in list(sys.modules) if m.startswith(_STUBBED)}

# loadWidget imports configfile at import time; the conftest fixture only stubs it later.
_had_configfile = "configfile" in sys.modules
sys.modules.setdefault("configfile", MagicMock())
from lib.panels.filamentTab import FilamentTab  # noqa: E402

if not _had_configfile:
    sys.modules.pop("configfile", None)
# Put the other modules' stand-ins back so this import leaves sys.modules as found.
for _real in [m for m in sys.modules if m.startswith(_STUBBED)]:
    del sys.modules[_real]
sys.modules.update(_saved)


def test_none_state_after_klipper_restart_is_ignored() -> None:
    # AMUManager.on_klippy_state emits None on every non-ready Klippy state.
    tab = MagicMock()
    FilamentTab.on_mmu_state_changed(tab, None)
    assert tab.mock_calls == []


def test_hide_load_popup_clears_load_state_and_hides() -> None:
    tab = MagicMock(load_state=True)
    FilamentTab.hide_load_popup(tab)
    assert tab.load_state is False
    tab.load_popup.hide.assert_called_once_with()
