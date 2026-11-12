"""LoadingOverlayWidget animates only while visible; five overlays ticking hidden cost the Pi idle CPU."""

import importlib.util
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets

# tests/panels/conftest.py stubs this module, so load the real one under another name
_spec = importlib.util.spec_from_file_location(
    "_real_loadWidget",
    Path(__file__).resolve().parents[2]
    / "BlocksScreen/lib/panels/widgets/Common/loadWidget.py",
)
_load_widget = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_load_widget)
_INTRO_GIF = _load_widget._INTRO_GIF
LoadingOverlayWidget = _load_widget.LoadingOverlayWidget

_GIF = LoadingOverlayWidget.AnimationGIF


def _overlay(qapp, anim: _GIF) -> tuple[QtWidgets.QWidget, LoadingOverlayWidget]:
    """Build an overlay inside a hidden parent, as BasePopup holds it."""
    parent = QtWidgets.QWidget()
    overlay = LoadingOverlayWidget(parent, anim)
    overlay.resize(800, 480)
    return parent, overlay


def test_intro_gif_path_exists():
    """The widget moved into Common/, so a stale parents[] index silently drops the gif."""
    assert _INTRO_GIF.is_file()


def test_spinner_idles_until_shown_and_stops_with_its_parent(qapp):
    """The spinner timer follows the ancestor's visibility, not the widget's lifetime."""
    parent, overlay = _overlay(qapp, _GIF.DEFAULT)
    assert not overlay.timer.isActive()
    parent.show()
    assert overlay.timer.isActive()
    parent.hide()
    assert not overlay.timer.isActive()


def test_intro_gif_plays_only_while_shown(qapp):
    """A hidden QMovie keeps decoding frames, so hiding the popup must stop it."""
    parent, overlay = _overlay(qapp, _GIF.PLACEHOLDER)
    assert overlay.movie is not None
    assert overlay.movie.state() == QtGui.QMovie.MovieState.NotRunning
    parent.show()
    assert overlay.movie.state() == QtGui.QMovie.MovieState.Running
    assert not overlay.timer.isActive()
    parent.hide()
    assert overlay.movie.state() == QtGui.QMovie.MovieState.NotRunning


def test_unlaid_out_overlay_keeps_the_gif_alive(qapp):
    """An empty scaled size stops a QMovie for good, so a tiny overlay must not set one."""
    parent = QtWidgets.QWidget()
    overlay = LoadingOverlayWidget(parent, _GIF.PLACEHOLDER)
    overlay.resize(10, 10)
    parent.show()
    assert overlay.movie.state() == QtGui.QMovie.MovieState.Running


def test_missing_gif_keeps_the_spinner(qapp, tmp_path):
    """A bad path must leave a working spinner, not an empty overlay."""
    parent, overlay = _overlay(qapp, _GIF.DEFAULT)
    overlay.set_animation_path(tmp_path / "missing.gif")
    assert overlay.movie is None
    parent.show()
    assert overlay.timer.isActive()


def test_unknown_gif_size_stretches_instead_of_cropping(qapp):
    """Without a frame size QMovie plays at native size, cropped by the label."""
    parent, overlay = _overlay(qapp, _GIF.PLACEHOLDER)
    overlay._movie_size = QtCore.QSize()
    overlay._fit_movie()
    assert overlay.gifshow.hasScaledContents()
