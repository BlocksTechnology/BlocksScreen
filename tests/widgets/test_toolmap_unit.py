"""Unit tests for MmuToolmapWidget.set_temps (toolmap.py)"""

from BlocksScreen.lib.utils.toolmap import MmuToolmapWidget


def test_set_temps_repaints_only_on_whole_degree_change(qtbot, monkeypatch):
    w = MmuToolmapWidget()
    qtbot.addWidget(w)
    calls = []
    monkeypatch.setattr(w, "update", lambda: calls.append(1))
    w.set_temps(214.8, 215.0)
    w.set_temps(215.2, 215.0)
    assert calls == [1]
    assert w._current_temp == 215.2
    w.set_temps(216.0, 215.0)
    assert calls == [1, 1]
