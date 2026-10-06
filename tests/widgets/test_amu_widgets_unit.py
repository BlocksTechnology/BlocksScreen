"""SpoolInfoPanel action-button matrix and AMUpage gate-select debounce."""

import sys
from unittest.mock import MagicMock

import pytest

import devices.amu.manager as amu_manager_module
from devices.amu.models import FilamentPos, GateInfo, GateStatus, MMUState

# conftest stubs devices.amu as a bare namespace; amuPage imports these from it.
vars(sys.modules["devices.amu"]).update(
    AMUManager=amu_manager_module.AMUManager,
    FilamentPos=FilamentPos,
    MMUState=MMUState,
)
# Other tests leave plain-Qt stand-ins for these session-wide; the panel needs the real API.
for _real in ("icon_button", "blocks_button", "blocks_label", "blocks_linedit"):
    sys.modules.pop(f"lib.utils.{_real}", None)
for _stale in [
    m for m in sys.modules if m.startswith("lib.panels.widgets.FilamentTab")
]:
    sys.modules.pop(_stale, None)

from lib.panels.widgets.FilamentTab.amuPage import AMUpage  # noqa: E402
from lib.panels.widgets.FilamentTab.amuWidgets import (  # noqa: E402
    SpoolInfoPanel,
    Spoll_button,
)


def _button(
    index: int,
    status: GateStatus = GateStatus.AVAILABLE,
    pos: FilamentPos = FilamentPos.UNLOADED,
) -> Spoll_button:
    btn = Spoll_button()
    btn.update_entry(GateInfo(index=index, status=status, material="PLA"), pos)
    return btn


def _actions(panel: SpoolInfoPanel) -> dict[str, bool]:
    return {
        "load": panel._btn_load.isEnabled(),
        "unload": panel._btn_unload.isEnabled(),
        "eject": panel._btn_purge.isEnabled(),
        "check": panel._btn_cut.isEnabled(),
    }


@pytest.fixture
def panel(qtbot):
    widget = SpoolInfoPanel(amu_manager=MagicMock())
    qtbot.addWidget(widget)
    widget.Gate = 1
    return widget


class TestSpoolInfoPanelActions:
    def test_active_gate_unloaded_enables_feed_and_check(self, panel):
        panel.update_for_slot(1, _button(1))
        assert _actions(panel) == {
            "load": True,
            "unload": False,
            "eject": True,
            "check": True,
        }

    def test_active_gate_empty_allows_check_only(self, panel):
        # Nothing to load or eject, but MMU_CHECK_GATE is how an EMPTY gate is re-detected.
        panel.update_for_slot(1, _button(1, status=GateStatus.EMPTY))
        assert _actions(panel) == {
            "load": False,
            "unload": False,
            "eject": False,
            "check": True,
        }

    def test_active_gate_loaded_allows_unload_only(self, panel):
        panel.update_for_slot(1, _button(1, pos=FilamentPos.LOADED))
        assert _actions(panel) == {
            "load": False,
            "unload": True,
            "eject": False,
            "check": False,
        }
        assert panel._lbl_status.text() == panel._LOADED_TEXT

    def test_mid_path_filament_shows_stuck_and_allows_unload(self, panel):
        panel.update_for_slot(1, _button(1, pos=FilamentPos.IN_BOWDEN))
        assert _actions(panel)["unload"] is True
        assert panel._lbl_status.text() == panel._STUCK_TEXT

    def test_unknown_position_counts_as_loaded(self, panel):
        # UNKNOWN may hide filament in the path, so only unload is safe.
        panel.update_for_slot(1, _button(1, pos=FilamentPos.UNKNOWN))
        assert _actions(panel) == {
            "load": False,
            "unload": True,
            "eject": False,
            "check": False,
        }

    @pytest.mark.parametrize("pos", [FilamentPos.UNLOADED, FilamentPos.LOADED])
    def test_non_active_gate_disables_everything(self, panel, pos):
        # Happy-Hare's bare MMU_LOAD/EJECT/CHECK_GATE act on the selected gate, not this one.
        panel.update_for_slot(2, _button(2, pos=pos))
        assert not any(_actions(panel).values())

    def test_no_active_gate_disables_everything(self, panel):
        panel.Gate = -1
        panel.update_for_slot(0, _button(0))
        assert not any(_actions(panel).values())

    def test_spool_bound_gate_is_read_only(self, panel):
        btn = Spoll_button()
        btn.update_entry(
            GateInfo(index=1, status=GateStatus.AVAILABLE, spool_id=7),
            FilamentPos.UNLOADED,
        )
        panel.update_for_slot(1, btn)
        assert not panel._lbl_mat.isEnabled()
        assert "Spool ID 7" in panel._lbl_status.text()


class TestClearSlot:
    @pytest.mark.parametrize("can_unload", [True, False])
    def test_only_unload_follows_the_flag(self, panel, can_unload):
        panel.update_for_slot(1, _button(1))
        panel.clear_slot(can_unload=can_unload)
        assert _actions(panel) == {
            "load": False,
            "unload": can_unload,
            "eject": False,
            "check": False,
        }
        assert panel._lbl_gate.text() == "Gate —"


def _state(gate: int, pos: FilamentPos = FilamentPos.UNLOADED) -> MMUState:
    return MMUState.from_status(
        {
            "enabled": True,
            "num_gates": 4,
            "gate": gate,
            "tool": gate,
            "filament_pos": int(pos),
            "gate_status": [1, 1, 1, 1],
        }
    )


@pytest.fixture
def manager():
    mgr = MagicMock()
    mgr.get_state.return_value = None
    return mgr


@pytest.fixture
def page(qtbot, manager):
    widget = AMUpage(manager)
    qtbot.addWidget(widget)
    widget.on_mmu_state_changed(_state(gate=1))
    return widget


class TestAMUpageSelect:
    def test_rapid_taps_send_one_select_for_the_last_gate(self, page, manager, qtbot):
        for gate in (0, 2, 3):
            page.carousel.selectionChanged.emit(gate)
        qtbot.waitUntil(lambda: manager.select_gate.called, timeout=2000)
        manager.select_gate.assert_called_once_with(3)

    def test_tap_keeps_the_active_gate_highlighted_until_state_confirms(self, page):
        page.carousel.selectionChanged.emit(2)
        assert page.carousel.selectedIndex() == 1

    def test_state_update_follows_the_selected_gate(self, page):
        page.on_mmu_state_changed(_state(gate=2))
        assert page.current_index == 2
        assert page.carousel.selectedIndex() == 2

    def test_bypass_clears_the_panel(self, page):
        # gate -2 is Happy-Hare's bypass: no gate is targeted by bare commands.
        page.on_mmu_state_changed(_state(gate=-2, pos=FilamentPos.LOADED))
        assert page.current_index == -1
        assert _actions(page.info_panel)["unload"] is True
        assert _actions(page.info_panel)["load"] is False

    def test_no_state_clears_the_panel(self, page):
        page.on_mmu_state_changed(None)
        assert page.current_index == -1
        assert not any(_actions(page.info_panel).values())


class TestAMUpageActions:
    def test_load_shows_popup_when_command_sent(self, manager, qtbot):
        popup = MagicMock()
        widget = AMUpage(manager, load_popup=popup)
        qtbot.addWidget(widget)
        manager.load_gate.return_value = True
        widget.info_panel.loadRequested.emit()
        popup.show.assert_called_once()

    def test_refused_load_shows_no_popup(self, manager, qtbot):
        popup = MagicMock()
        widget = AMUpage(manager, load_popup=popup)
        qtbot.addWidget(widget)
        manager.load_gate.return_value = False
        widget.info_panel.loadRequested.emit()
        popup.show.assert_not_called()

    def test_unload_without_popup_does_not_crash(self, page, manager):
        manager.unload.return_value = True
        page.info_panel.unloadRequested.emit()
        manager.unload.assert_called_once()

    def test_temp_edit_with_placeholder_sends_nothing(self, page, manager):
        page.info_panel._lbl_temp.setText("—")
        page._on_temp_edited()
        manager.set_gate_temp.assert_not_called()

    def test_temp_edit_strips_degree_sign(self, page, manager):
        page.info_panel._lbl_temp.setText("215º")
        page._on_temp_edited()
        manager.set_gate_temp.assert_called_once_with(1, 215)


class TestAMUpageRedraw:
    @staticmethod
    def _spy(page, monkeypatch) -> list:
        calls = []
        monkeypatch.setattr(page.carousel, "addSpool", lambda *a: calls.append(a))
        return calls

    # A diff with no gate_* key keeps the gates tuple, so nothing to repaint.
    def test_scalar_diff_skips_carousel(self, page, monkeypatch):
        calls = self._spy(page, monkeypatch)
        page.on_mmu_state_changed(page.status.apply_diff({"action": "Loading"}))
        assert calls == []

    def test_gate_diff_redraws_carousel(self, page, monkeypatch):
        calls = self._spy(page, monkeypatch)
        page.on_mmu_state_changed(page.status.apply_diff({"gate_status": [0, 1, 1, 1]}))
        assert len(calls) == 4

    # The spool buttons render filament_pos, so a position change must repaint.
    def test_filament_pos_change_redraws_carousel(self, page, monkeypatch):
        calls = self._spy(page, monkeypatch)
        diff = {"filament_pos": int(FilamentPos.LOADED)}
        page.on_mmu_state_changed(page.status.apply_diff(diff))
        assert len(calls) == 4

    def test_selection_follows_a_scalar_diff(self, page):
        page.on_mmu_state_changed(page.status.apply_diff({"gate": 2}))
        assert page.current_index == 2
