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
    def __init__(self, name="", htemp=0, btemp=0):
        self.name = name
        self.htemp = htemp
        self.btemp = btemp


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
    panel = BasicFilamentPanel(mock_printer, mock_cfg, amu_manager=MagicMock())
    qtbot.addWidget(panel)
    shared = _item_addrs(panel.verticalLayout) & _item_addrs(panel.verticalLayout_2)
    assert not shared, (
        "a QLayoutItem is shared between filament_control_page and load_page "
        "layouts; destroying the panel double-frees it"
    )


def test_destroying_panel_is_clean(qapp, mock_printer, mock_cfg):
    """Force destruction (the AMU-swap path) and confirm no double-free SIGBUS."""
    panel = BasicFilamentPanel(mock_printer, mock_cfg, amu_manager=MagicMock())
    panel.deleteLater()
    qapp.processEvents()
    # Reaching here means ~BasicFilamentPanel ran without a double-free.


def _mmu_state(pos, action="Idle", color="", tool=0, gate=0):
    gate_info = SimpleNamespace(color=color, status=None)
    return SimpleNamespace(
        filament_pos=pos,
        action=action,
        tool=tool,
        gate=gate,
        current_gate_info=gate_info,
    )


@pytest.fixture
def panel(qtbot, mock_printer, mock_cfg):
    panel = BasicFilamentPanel(mock_printer, mock_cfg, amu_manager=MagicMock())
    qtbot.addWidget(panel)
    return panel


def test_check_button_enabled_when_loaded(panel):
    panel.on_mmu_state_changed(_mmu_state(FilamentPos.LOADED))
    assert panel.Basic_fp_check_btn.isEnabled()
    panel.on_print_stats_update("state", "printing")
    assert not panel.Basic_fp_check_btn.isEnabled()


# Happy-Hare refuses MMU_LOAD from a mid-path position; a sensorless printer must still load.
@pytest.mark.parametrize(("mmu", "enabled"), [(True, False), (False, True)])
def test_load_button_in_unknown_position(panel, mmu, enabled):
    panel.mmu_configured = mmu
    panel.filament_state = panel.FilamentStates.UNKNOWN
    assert panel.Basic_fp_load_btn.isEnabled() is enabled


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


# A fresh save_variables file has no filament_type; that used to raise AttributeError.
@pytest.mark.parametrize(
    ("variables", "expected"),
    [
        ({}, "UNKNOWN"),
        ({"filament_type": ""}, "UNKNOWN"),
        ({"filament_type": "TPU"}, "UNKNOWN"),
        ({"filament_type": 5}, "UNKNOWN"),
        ({"filament_type": "PETG"}, "PETG"),
        ({"filament_type": "PLA+"}, "PLA"),
    ],
)
def test_save_variables_material_label(panel, variables, expected):
    panel.on_save_variables_update({"variables": variables})
    assert panel._lbl_mat._right.text() == expected


def test_save_variables_without_variables_key(panel):
    panel.on_save_variables_update({})
    assert panel._lbl_mat._right.text() == "UNKNOWN"


def test_accepted_position_change_recovers_through_manager(panel):
    panel.on_mmu_state_changed(_mmu_state(FilamentPos.LOADED))
    emitted = []
    panel.run_gcode.connect(emitted.append)
    panel._lbl_pos.select_option("Unloaded")
    panel.on_pos_change()
    panel.confirm_pos_popup.accepted.emit()
    panel.amu_manager.recover_single_gate.assert_called_once_with(False)
    assert emitted == []


def test_rejected_position_change_reverts_without_gcode(panel):
    panel.on_mmu_state_changed(_mmu_state(FilamentPos.LOADED))
    emitted = []
    panel.run_gcode.connect(emitted.append)
    panel._lbl_pos.select_option("Unloaded")
    panel.on_pos_change()
    panel.confirm_pos_popup.rejected.emit()
    assert emitted == []
    assert panel._lbl_pos.text() == "Loaded"


@pytest.fixture
def mmu_panel(qtbot, mock_printer, mock_cfg):
    load_popup = MagicMock()
    panel = BasicFilamentPanel(
        mock_printer, mock_cfg, amu_manager=MagicMock(), load_popup=load_popup
    )
    qtbot.addWidget(panel)
    panel.mmu_configured = True
    panel.show()
    return panel


@pytest.mark.parametrize("sent", [True, False])
def test_load_goes_through_manager(mmu_panel, monkeypatch, sent):
    mmu_panel.filament_state = mmu_panel.FilamentStates.UNLOADED
    mmu_panel.amu_manager.load_gate.return_value = sent
    mmu_panel.amu_manager.load_refusal.return_value = "MMU is not homed."
    monkeypatch.setattr(mmu_panel.popup, "new_message", MagicMock())
    emitted = []
    mmu_panel.run_gcode.connect(emitted.append)
    mmu_panel.load_filament()
    mmu_panel.amu_manager.load_gate.assert_called_once_with()
    # A refused load tells the user why instead of doing nothing.
    assert mmu_panel.popup.new_message.called is not sent
    if not sent:
        assert mmu_panel.popup.new_message.call_args.kwargs["message"] == (
            "MMU is not homed."
        )
    # A refused load must not leave the popup up or the type label saying loaded.
    assert mmu_panel.load_popup.show.called is sent
    assert [g.startswith("SAVE_VARIABLE") for g in emitted] == ([True] if sent else [])


@pytest.mark.parametrize("sent", [True, False])
def test_unload_goes_through_manager(mmu_panel, monkeypatch, sent):
    mmu_panel.filament_state = mmu_panel.FilamentStates.LOADED
    mmu_panel.amu_manager.unload.return_value = sent
    mmu_panel.amu_manager.unload_refusal.return_value = "Not available while printing."
    monkeypatch.setattr(mmu_panel.popup, "new_message", MagicMock())
    emitted = []
    mmu_panel.run_gcode.connect(emitted.append)
    mmu_panel.unload_filament()
    mmu_panel.amu_manager.unload.assert_called_once_with(eject=True)
    assert mmu_panel.popup.new_message.called is not sent
    if not sent:
        assert mmu_panel.popup.new_message.call_args.kwargs["message"] == (
            "Not available while printing."
        )
    assert mmu_panel.load_popup.show.called is sent
    assert [g.startswith("SAVE_VARIABLE") for g in emitted] == ([True] if sent else [])
