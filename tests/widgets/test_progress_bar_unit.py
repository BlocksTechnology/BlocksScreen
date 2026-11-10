"""Unit tests for CustomProgressBar (blocks_progressbar.py)"""

import pytest

from BlocksScreen.lib.utils.blocks_progressbar import CustomProgressBar


@pytest.fixture()
def bar(qtbot):
    """Create a CustomProgressBar registered with qtbot."""
    w = CustomProgressBar(parent=None)
    qtbot.addWidget(w)
    return w


class TestSetProgress:
    """set_progress maps a 0.0-1.0 fraction onto a 0-100 percent, clamped."""

    def test_fraction_scaled_to_percent(self, bar):
        bar.set_progress(0.5)
        assert bar.progress_value == 50

    def test_full(self, bar):
        bar.set_progress(1.0)
        assert bar.progress_value == 100

    def test_clamps_above_one(self, bar):
        bar.set_progress(1.4)
        progress = bar.progress_value
        assert progress == 100

    def test_clamps_below_zero(self, bar):
        bar.set_progress(-0.2)
        assert bar.progress_value == 0


class TestReset:
    """reset returns the bar to 0%."""

    def test_reset_clears_progress(self, bar):
        bar.set_progress(0.8)
        bar.reset()
        assert bar.progress_value == 0


class TestRepaintGuard:
    """set_progress repaints only when the drawn arc or percent text changes."""

    def test_subpixel_step_skips_update(self, bar, monkeypatch):
        bar.set_progress(0.5)
        calls = []
        monkeypatch.setattr(bar, "update", lambda: calls.append(1))
        bar.set_progress(0.50001)
        assert calls == []
        assert bar.progress_value == pytest.approx(50.001)

    def test_visible_step_updates(self, bar, monkeypatch):
        bar.set_progress(0.5)
        calls = []
        monkeypatch.setattr(bar, "update", lambda: calls.append(1))
        bar.set_progress(0.51)
        assert calls == [1]

    def test_leaving_zero_updates(self, bar, monkeypatch):
        calls = []
        monkeypatch.setattr(bar, "update", lambda: calls.append(1))
        bar.set_progress(0.00001)
        assert calls == [1]
