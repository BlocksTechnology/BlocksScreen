"""SpoolInfoPanel action-button matrix and AMUpage gate selection."""

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


def _show(
    panel: SpoolInfoPanel, btn: Spoll_button, *, enabled=True, homed=True, idle=True
) -> None:
    panel.update_for_slot(btn, enabled=enabled, homed=homed, idle=idle)


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
    return widget


class TestSpoolInfoPanelActions:
    def test_active_gate_unloaded_enables_feed_and_check(self, panel):
        _show(panel, _button(1))
        assert _actions(panel) == {
            "load": True,
            "unload": False,
            "eject": True,
            "check": True,
        }

    def test_active_gate_empty_allows_check_only(self, panel):
        # Nothing to load or eject, but MMU_CHECK_GATE is how an EMPTY gate is re-detected.
        _show(panel, _button(1, status=GateStatus.EMPTY))
        assert _actions(panel) == {
            "load": False,
            "unload": False,
            "eject": False,
            "check": True,
        }

    # HH v3 MMU_CHECK_GATE unloads first and reloads a LOADED tool after.
    def test_active_gate_loaded_allows_unload_and_check(self, panel):
        _show(panel, _button(1, pos=FilamentPos.LOADED))
        assert _actions(panel) == {
            "load": False,
            "unload": True,
            "eject": False,
            "check": True,
        }
        assert panel._lbl_status.text() == panel._LOADED_TEXT

    def test_mid_path_filament_shows_stuck_and_allows_unload(self, panel):
        _show(panel, _button(1, pos=FilamentPos.IN_BOWDEN))
        assert _actions(panel)["unload"] is True
        assert _actions(panel)["check"] is True
        assert panel._lbl_status.text() == panel._STUCK_TEXT

    def test_unknown_position_counts_as_loaded(self, panel):
        # UNKNOWN may hide filament in the path, so load and eject stay off.
        _show(panel, _button(1, pos=FilamentPos.UNKNOWN))
        assert _actions(panel) == {
            "load": False,
            "unload": True,
            "eject": False,
            "check": True,
        }

    @pytest.mark.parametrize("pos", [FilamentPos.UNLOADED, FilamentPos.LOADED])
    def test_busy_or_printing_greys_actions(self, panel, pos):
        _show(panel, _button(1, pos=pos), idle=False)
        assert not any(_actions(panel).values())

    def test_spool_bound_gate_is_read_only(self, panel):
        btn = Spoll_button()
        btn.update_entry(
            GateInfo(index=1, status=GateStatus.AVAILABLE, spool_id=7),
            FilamentPos.UNLOADED,
        )
        _show(panel, btn)
        assert not panel._lbl_mat.isEnabled()
        assert "Spool ID 7" in panel._lbl_status.text()

    @pytest.mark.parametrize("pos", [FilamentPos.UNLOADED, FilamentPos.LOADED])
    def test_disabled_mmu_greys_everything(self, panel, pos):
        _show(panel, _button(1, pos=pos), enabled=False)
        assert not any(_actions(panel).values())
        assert not panel._lbl_mat.isEnabled()

    def test_unhomed_mmu_allows_unload_only(self, panel):
        _show(panel, _button(1), homed=False)
        assert not any(_actions(panel).values())
        _show(panel, _button(1, pos=FilamentPos.LOADED), homed=False)
        assert _actions(panel)["unload"] is True


class TestClearSlot:
    @pytest.mark.parametrize("can_unload", [True, False])
    def test_only_unload_follows_the_flag(self, panel, can_unload):
        _show(panel, _button(1))
        panel.clear_slot(can_unload=can_unload)
        assert _actions(panel) == {
            "load": False,
            "unload": can_unload,
            "eject": False,
            "check": False,
        }
        assert panel._lbl_gate.text() == "Gate —"


def _state(
    gate: int, pos: FilamentPos = FilamentPos.UNLOADED, enabled: bool = True
) -> MMUState:
    return MMUState.from_status(
        {
            "enabled": enabled,
            "is_homed": True,
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
    def test_tap_selects_the_gate_immediately(self, page, manager):
        page.carousel.selectionChanged.emit(2)
        manager.select_gate.assert_called_once_with(2)

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
        assert page.carousel.selectedIndex() == -1
        assert _actions(page.info_panel)["unload"] is True
        assert _actions(page.info_panel)["load"] is False

    def test_bypass_on_a_disabled_mmu_cannot_unload(self, page):
        page.on_mmu_state_changed(
            _state(gate=-2, pos=FilamentPos.LOADED, enabled=False)
        )
        assert not any(_actions(page.info_panel).values())

    def test_no_state_clears_the_panel(self, page):
        page.on_mmu_state_changed(None)
        assert page.current_index == -1
        assert page.carousel.selectedIndex() == -1
        assert not any(_actions(page.info_panel).values())

    def test_tap_with_no_active_gate_leaves_nothing_highlighted(self, page):
        page.on_mmu_state_changed(_state(gate=-1))
        page.carousel.buttons[2].click()
        assert page.carousel.selectedIndex() == -1


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

    @pytest.mark.parametrize("text", ["inf", "nan", "1e999"])
    def test_non_finite_temp_sends_nothing(self, page, manager, text):
        page.info_panel._lbl_temp.setText(text)
        page._on_temp_edited()
        manager.set_gate_temp.assert_not_called()

    @pytest.mark.parametrize(
        ("state", "tab"), [("printing", [0]), ("paused", [0]), ("standby", [])]
    )
    def test_back_button_follows_print_state(self, page, state, tab):
        tabs, backs = [], []
        page.request_change_tab.connect(tabs.append)
        page.request_back.connect(lambda: backs.append(1))
        page.on_print_stats_update("state", "printing")
        page.on_print_stats_update("state", state)
        page.main_back_button.click()
        assert (tabs, backs) == (tab, [] if tab else [1])


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

    def test_unchanged_view_skips_selection(self, page, monkeypatch):
        calls = []
        monkeypatch.setattr(page, "_on_selection", calls.append)
        page.on_mmu_state_changed(page.status.apply_diff({"bowden_progress": 42.0}))
        assert calls == []

    @pytest.mark.parametrize(
        ("key", "busy", "idle"),
        [("action", "Loading", "Idle"), ("print_state", "printing", "standby")],
    )
    def test_busy_or_printing_diff_greys_then_restores(self, page, key, busy, idle):
        page.on_mmu_state_changed(page.status.apply_diff({key: busy}))
        assert not any(_actions(page.info_panel).values())
        page.on_mmu_state_changed(page.status.apply_diff({key: idle}))
        assert _actions(page.info_panel)["load"] is True

    def test_selection_follows_a_scalar_diff(self, page):
        page.on_mmu_state_changed(page.status.apply_diff({"gate": 2}))
        assert page.current_index == 2
