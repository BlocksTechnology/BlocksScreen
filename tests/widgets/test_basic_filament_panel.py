"""Regression tests for BasicFilamentPanel widget lifetime.

Guards the double-free where a single QSpacerItem was shared between the
filament_control_page and load_page layouts: destroying the panel (e.g. the
AMU swap in FilamentTab) made both layouts delete the same item -> SIGBUS.
This crash class only shows on widget *destruction*, which ordinary tests never
exercise, so these tests force it.
"""

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from PyQt6 import QtWidgets, sip

# Stub the bare lib.* imports BasicFilamentPanel pulls in (the app runs from
# inside BlocksScreen/, so these unprefixed names are not importable under test).


class _Filament:
    def __init__(self, name="", temperature=0):
        self.name = name
        self.temperature = temperature


_filament_stub = MagicMock()
_filament_stub.Filament = _Filament
sys.modules.setdefault("lib.filament", _filament_stub)

_printer_stub = MagicMock()
_printer_stub.Printer = MagicMock
sys.modules.setdefault("lib.printer", _printer_stub)

_popup_stub = MagicMock()
_popup_stub.Popup = QtWidgets.QWidget
sys.modules.setdefault("lib.panels.widgets.popupDialogWidget", _popup_stub)

_button_stub = MagicMock()
_button_stub.BlocksCustomButton = QtWidgets.QPushButton
sys.modules.setdefault("lib.utils.blocks_button", _button_stub)

# Other conftests register session-wide stubs for these (a plain QComboBox and
# a bare MagicMock) that lack the API BasicFilamentPanel uses; force the real ones.
_src = Path(__file__).resolve().parents[2] / "BlocksScreen"
for _name, _rel in (
    ("lib.utils.blocks_combobox", "lib/utils/blocks_combobox.py"),
    ("lib.panels.widgets.Common.basePopup", "lib/panels/widgets/Common/basePopup.py"),
):
    _spec = importlib.util.spec_from_file_location(_name, _src / _rel)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    sys.modules[_name] = _mod

import pytest  # noqa: E402

from devices.amu.models import FilamentPos  # noqa: E402

from BlocksScreen.lib.panels.widgets.FilamentTab.basicFilamentPanel import (  # noqa: E402
    BasicFilamentPanel,
)


@pytest.fixture
def mock_printer():
    return MagicMock()


@pytest.fixture
def mock_cfg():
    cfg = MagicMock()
    cfg.has_section.return_value = False
    return cfg


def _item_addrs(layout):
    """C++ addresses of every QLayoutItem directly held by a layout."""
    return {
        sip.unwrapinstance(layout.itemAt(i))
        for i in range(layout.count())
        if layout.itemAt(i) is not None
    }


def test_pages_do_not_share_layout_items(qtbot, mock_printer, mock_cfg):
    """No QLayoutItem may belong to two layouts (deterministic, no crash)."""
    panel = BasicFilamentPanel(mock_printer, mock_cfg)
    qtbot.addWidget(panel)
    shared = _item_addrs(panel.verticalLayout) & _item_addrs(panel.verticalLayout_2)
    assert not shared, (
        "a QLayoutItem is shared between filament_control_page and load_page "
        "layouts; destroying the panel double-frees it"
    )


def test_destroying_panel_is_clean(qapp, mock_printer, mock_cfg):
    """Force destruction (the AMU-swap path) and confirm no double-free SIGBUS."""
    panel = BasicFilamentPanel(mock_printer, mock_cfg)
    panel.deleteLater()
    qapp.processEvents()
    # Reaching here means ~BasicFilamentPanel ran without a double-free.


def _mmu_state(pos, action="Idle", color=""):
    gate_info = SimpleNamespace(color=color, status=None)
    return SimpleNamespace(
        filament_pos=pos,
        action=action,
        current_gate_info=gate_info,
    )


@pytest.fixture
def panel(qtbot, mock_printer, mock_cfg):
    panel = BasicFilamentPanel(mock_printer, mock_cfg)
    qtbot.addWidget(panel)
    return panel


def test_check_button_enabled_when_loaded(panel):
    panel.on_mmu_state_changed(_mmu_state(FilamentPos.LOADED))
    assert panel.Basic_fp_check_btn.isEnabled()
    panel.on_print_stats_update("state", "printing")
    assert not panel.Basic_fp_check_btn.isEnabled()


def test_sensor_without_mmu_updates_position(panel):
    panel.filament_sensor = "presence"
    panel.on_filament_sensor_update("presence", "filament_detected", True)
    assert panel._lbl_pos.text() == "Loaded"


def test_position_not_editable_while_printing(panel):
    panel.on_mmu_state_changed(_mmu_state(FilamentPos.LOADED))
    assert not panel._lbl_pos._right.isHidden()
    panel.on_print_stats_update("state", "printing")
    assert panel._lbl_pos._right.isHidden()
    panel.on_print_stats_update("state", "paused")
    assert not panel._lbl_pos._right.isHidden()
    panel.on_mmu_state_changed(_mmu_state(FilamentPos.LOADED, action="Loading"))
    assert panel._lbl_pos._right.isHidden()


def test_color_swatch_accepts_names(panel):
    panel._apply_color_swatch("red")
    assert panel._lbl_clr.text() == ""
