"""Spoolman error surfacing, gating and stale-list handling in the filament UI."""

import sys
from unittest.mock import MagicMock

import pytest
from PyQt6 import QtCore

import devices.amu.manager as amu_manager_module
from devices.amu.models import FilamentPos, GateInfo, MMUState

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
for _stale in [m for m in sys.modules if m.startswith(_STUBBED)]:
    sys.modules.pop(_stale, None)

# loadWidget imports configfile at import time; the conftest fixture only stubs it later.
_had_configfile = "configfile" in sys.modules
sys.modules.setdefault("configfile", MagicMock())
from lib.panels.filamentTab import FilamentTab  # noqa: E402
from lib.panels.widgets.FilamentTab.addFilamentPage import AddFilamentPage  # noqa: E402
from lib.panels.widgets.FilamentTab.addSpoolPage import (  # noqa: E402
    AddSpoolPage,
    spoolman_color,
)
from lib.panels.widgets.FilamentTab.spoolmanPage import SpoolmanPage  # noqa: E402
from lib.utils.list_model import ListItem  # noqa: E402

if not _had_configfile:
    sys.modules.pop("configfile", None)

UNREACHABLE = {"error": {"code": 503, "message": "Spoolman server not available"}}
SPOOL = {"id": 7, "filament": {"name": "PLA Red", "material": "PLA"}}


def _spools(*spools: dict) -> dict:
    return {"response": list(spools), "error": None}


def _rows(model) -> list[str]:
    return [model.entries[i].text for i in range(model.rowCount())]


@pytest.fixture
def tab(qtbot):
    ws = MagicMock()
    widget = FilamentTab(None, MagicMock(), ws, MagicMock(), MagicMock())
    qtbot.addWidget(widget)
    widget.handle_moonraker_components(["spoolman"])
    ws.api.spoolman_proxy.reset_mock()
    return widget


class TestFilamentTabSpools:
    def test_failed_fetch_drops_the_previous_list(self, tab):
        tab.on_spools_received(_spools(SPOOL))
        assert tab._spool_id_map
        tab.on_spools_received(UNREACHABLE)
        assert tab._spool_model.rowCount() == 0
        assert tab._spool_id_map == {}
        assert tab._no_spools_label.text() == "Could not reach Spoolman"

    @pytest.mark.parametrize("reply", [UNREACHABLE, {"response": None, "error": None}])
    def test_failed_fetch_hides_the_list(self, tab, reply):
        tab.on_spools_received(reply)
        assert tab._spool_list_view.isHidden()
        assert not tab._no_spools_label.isHidden()

    def test_popup_clears_the_list_before_fetching(self, tab):
        tab.on_spools_received(_spools(SPOOL))
        tab.handle_popup(True)
        assert tab._spool_model.rowCount() == 0
        assert not tab._spool_load_widget.isHidden()
        tab.ws.api.spoolman_proxy.assert_called_once_with(
            "GET", "/v1/spool", callback=tab.on_spools_received
        )

    def test_popup_skips_spoolman_when_not_configured(self, tab):
        tab.handle_moonraker_components(["history"])
        tab.handle_popup(True)
        tab.ws.api.spoolman_proxy.assert_not_called()
        assert tab._popup_stack.currentWidget() is tab._popup_form_page

    def test_added_spool_refetches_the_list(self, tab):
        tab._add_spool_page.accepted.emit()
        tab.ws.api.spoolman_proxy.assert_called_once()

    def test_add_spool_row_resets_the_add_page(self, tab, monkeypatch):
        reset = MagicMock()
        monkeypatch.setattr(tab._add_spool_page, "reset", reset)
        tab._on_list_item_tapped(ListItem(text="+ Add Spool"))
        reset.assert_called_once()

    def test_offline_fetch_shows_the_error(self, tab):
        tab.ws.api.spoolman_proxy.return_value = False
        tab.handle_popup(True)
        assert tab._spool_load_widget.isHidden()
        assert tab._no_spools_label.text() == "Could not reach Spoolman"

    def test_weight_is_whole_grams(self, tab):
        tab.on_spools_received(_spools({**SPOOL, "remaining_weight": 812.6}))
        tab._on_list_item_tapped(tab._spool_model.entries[1])
        assert tab.weight_label.text() == "813 g"

    def test_pregate_filter_does_not_fetch(self, tab):
        requests = []
        tab._add_spool_page.request_filaments.connect(lambda: requests.append(1))
        tab._add_spool_page.setFilter("PETG")
        assert requests == []

    def test_amu_swap_rewires_control_button_quietly(self, tab, qtlog, monkeypatch):
        gates = tuple(GateInfo(index=i) for i in range(2))
        state = MMUState(num_gates=2, gates=gates)
        tab.amu_manager.get_state.return_value = state
        tab.on_mmu_state_changed(state)
        pages = []
        monkeypatch.setattr(tab, "change_page", pages.append)
        tab.fp_button_1.click()
        assert pages == [tab.indexOf(tab.amupage)]
        assert not [r for r in qtlog.records if "disconnect" in r.message]

    def test_idle_after_amu_swap_skips_the_deleted_panel(self, tab):
        two = MMUState(num_gates=2, gates=tuple(GateInfo(index=i) for i in range(2)))
        tab.amu_manager.get_state.return_value = two
        tab.on_mmu_state_changed(two)
        QtCore.QCoreApplication.sendPostedEvents(
            None, QtCore.QEvent.Type.DeferredDelete.value
        )
        tab.load_state = True
        tab.on_mmu_state_changed(
            MMUState(num_gates=1, gates=(GateInfo(index=0),), action="Idle")
        )
        assert tab._basic_panel is None
        assert tab.load_state is False


class TestFilamentTabGates:
    @staticmethod
    def _state(**status) -> MMUState:
        return MMUState.from_status({"num_gates": 1, "gate": 0, **status})

    # Happy Hare owns the gate map; a runout must not wipe the user's entry.
    def test_runout_keeps_the_gate_map(self, tab):
        tab.on_mmu_state_changed(self._state(gate_status=[1]))
        tab.on_mmu_state_changed(self._state(gate_status=[0]))
        tab.amu_manager.clear_gate.assert_not_called()

    def test_load_popup_uses_happy_hare_rgb(self, tab, monkeypatch):
        monkeypatch.setattr(tab.load_popup, "isVisible", lambda: True)
        colors = []
        monkeypatch.setattr(tab.load_status_widget, "set_gate_color", colors.append)
        tab.on_mmu_state_changed(
            self._state(gate_color=["red"], gate_color_rgb=[[1.0, 0.0, 0.0]])
        )
        assert colors[-1].name() == "#ff0000"


class TestVendorLookup:
    @staticmethod
    def _reply(tab, reply: dict) -> list:
        def proxy(*_args, callback):
            callback(reply)
            return True

        tab.ws.api.spoolman_proxy.side_effect = proxy
        got = []
        tab._find_or_add_vendor({"name": "Acme"}, got.append)
        return got

    def test_exact_name_is_reused(self, tab):
        vendors = [{"id": 4, "name": "Acme Pro"}, {"id": 3, "name": "Acme"}]
        got = self._reply(tab, {"response": vendors, "error": None})
        assert got == [{"response": {"id": 3, "name": "Acme"}, "error": None}]
        assert tab.ws.api.spoolman_proxy.call_args.args == (
            "GET",
            "/v1/vendor",
            "name=Acme",
        )
        tab.ws.api.add_manufacturer.assert_not_called()

    def test_missing_name_is_created(self, tab):
        got = self._reply(tab, {"response": [{"id": 4, "name": "Acme Pro"}]})
        tab.ws.api.add_manufacturer.assert_called_once_with(
            {"name": "Acme"}, callback=got.append
        )

    def test_failed_lookup_creates_nothing(self, tab):
        got = self._reply(tab, UNREACHABLE)
        assert got[0]["error"] is not None
        tab.ws.api.add_manufacturer.assert_not_called()


@pytest.mark.parametrize(
    ("hex_text", "rgba"),
    [
        ("ff0000", (255, 0, 0, 255)),
        ("ff000080", (255, 0, 0, 128)),
        ("#00ff00", (0, 255, 0, 255)),
    ],
)
def test_spoolman_hex_alpha_is_trailing(hex_text, rgba):
    assert spoolman_color(hex_text).getRgb() == rgba


@pytest.fixture
def add_spool(qtbot):
    page = AddSpoolPage()
    qtbot.addWidget(page)
    return page


class TestAddSpoolPage:
    def test_unreachable_shows_error(self, add_spool):
        add_spool.on_filaments_received(UNREACHABLE)
        assert add_spool._fil_list_view.isHidden()
        assert add_spool._no_filaments_label.text() == "Could not reach Spoolman"

    def test_same_name_filaments_select_their_own_id(self, add_spool):
        fils = [{"id": 1, "name": "PLA"}, {"id": 2, "name": "PLA"}]
        add_spool.on_filaments_received({"response": fils, "error": None})
        add_spool._on_filament_selected(add_spool._fil_model.entries[1])
        assert add_spool._selected_filament_id == 1

    def test_failed_add_shows_toast(self, add_spool, monkeypatch):
        toast = MagicMock()
        monkeypatch.setattr(add_spool._popup, "new_message", toast)
        accepted = []
        add_spool.accepted.connect(lambda: accepted.append(1))
        add_spool.on_add_spool_result(UNREACHABLE)
        assert accepted == []
        assert toast.call_args.kwargs["message"] == "Could not add spool"

    def test_submit_waits_for_the_reply(self, add_spool, monkeypatch):
        monkeypatch.setattr(add_spool._popup, "new_message", MagicMock())
        add_spool.on_filaments_received(_spools({"id": 1, "name": "PLA"}))
        add_spool._on_filament_selected(add_spool._fil_model.entries[1])
        sent = []
        add_spool.request_add_spool.connect(lambda *a: sent.append(a))
        add_spool._submit_btn.click()
        add_spool._submit_btn.click()
        assert len(sent) == 1
        add_spool.on_add_spool_result(UNREACHABLE)
        assert add_spool._submit_btn.isEnabled()


class TestAddFilamentPage:
    @pytest.fixture
    def page(self, qtbot, monkeypatch):
        widget = AddFilamentPage()
        qtbot.addWidget(widget)
        monkeypatch.setattr(widget._popup, "new_message", MagicMock())
        widget.reset()
        return widget

    def test_failed_add_shows_toast(self, page):
        page.on_add_filament_result(UNREACHABLE)
        assert page._popup.new_message.call_args.kwargs["message"] == (
            "Could not add filament"
        )

    def test_failed_vendor_drops_pending_filament(self, page):
        page._vendor_field.setText("Acme")
        page._submit_btn.click()
        page.on_add_manufacturer_result(UNREACHABLE)
        assert page.request_filament_body is None
        assert page._submit_btn.isEnabled()

    def test_submit_waits_for_the_reply(self, page):
        sent = []
        page.request_add_filament.connect(sent.append)
        page._submit_btn.click()
        page._submit_btn.click()
        assert len(sent) == 1
        page.on_add_filament_result(UNREACHABLE)
        assert page._submit_btn.isEnabled()

    def test_reset_drops_a_pending_submit(self, page):
        page._vendor_field.setText("Acme")
        page._submit_btn.click()
        page.reset()
        assert page.request_filament_body is None
        assert page._submit_btn.isEnabled()


class TestSpoolmanPage:
    @pytest.fixture
    def page(self, qtbot):
        widget = SpoolmanPage()
        qtbot.addWidget(widget)
        return widget

    def test_unreachable_clears_list_and_says_so(self, page):
        page.on_spools_received(_spools(SPOOL))
        page.on_spools_received(UNREACHABLE)
        assert _rows(page.model) == [" Add Spool"]
        assert page._no_spools_label.text() == "Could not reach Spoolman"

    @pytest.mark.parametrize(
        "reply",
        [
            lambda page: page.on_spools_received(UNREACHABLE),
            lambda page: page.on_delete_spool_result({"response": {}, "error": None}),
        ],
        ids=["unreachable", "deleted"],
    )
    def test_reply_clears_the_selected_spool(self, page, reply):
        page._selected_spool = SPOOL
        page._refresh_info_box()
        assert page.filament_name_label.text() == "PLA Red"
        reply(page)
        assert page._selected_spool is None
        assert page.filament_name_label.text() == "—"

    def test_failed_delete_shows_toast(self, page, monkeypatch):
        toast = MagicMock()
        monkeypatch.setattr(page._popup, "new_message", toast)
        page.on_delete_spool_result(UNREACHABLE)
        assert toast.call_args.kwargs["message"] == "Could not delete spool"
