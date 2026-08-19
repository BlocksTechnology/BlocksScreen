"""Regression tests for BasicFilamentPanel widget lifetime.

Guards the double-free where a single QSpacerItem was shared between the
filament_control_page and load_page layouts: destroying the panel (e.g. the
AMU swap in FilamentTab) made both layouts delete the same item -> SIGBUS.
This crash class only shows on widget *destruction*, which ordinary tests never
exercise, so these tests force it.
"""

import sys
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
sys.modules.setdefault("lib.panels.widgets.common.popupDialogWidget", _popup_stub)

_button_stub = MagicMock()
_button_stub.BlocksCustomButton = QtWidgets.QPushButton
sys.modules.setdefault("lib.utils.blocks_button", _button_stub)

import pytest

from BlocksScreen.lib.panels.widgets.FilamentTab.basicFilamentPanel import (
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
