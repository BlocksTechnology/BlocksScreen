"""Unit tests for CustomProgressBar (blocks_progressbar.py)"""

import pytest

from lib.utils.blocks_progressbar import CustomProgressBar


@pytest.fixture()
def bar(qtbot):
    """Create a CustomProgressBar registered with qtbot."""
    w = CustomProgressBar()
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
        assert bar.progress_value == 100

    def test_clamps_below_zero(self, bar):
        bar.set_progress(-0.2)
        assert bar.progress_value == 0


class TestReset:
    """reset returns the bar to 0%."""

    def test_reset_clears_progress(self, bar):
        bar.set_progress(0.8)
        bar.reset()
        assert bar.progress_value == 0
