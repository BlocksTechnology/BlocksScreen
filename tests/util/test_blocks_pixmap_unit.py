"""Unit tests for BlocksPixmap; Qt turns an unknown key into a silent null pixmap."""

import importlib
from pathlib import Path

import pytest
from PyQt6 import QtCore, QtGui

from BlocksScreen.lib.utils.blocks_pixmap import BlocksPixmap, Icon

_RC_PACKAGE = "BlocksScreen.lib.ui.resources"
_RESOURCES = Path(__file__).resolve().parents[2] / "BlocksScreen/lib/ui/resources"


@pytest.fixture(autouse=True)
def _resources(qapp):
    """Register the compiled blobs, then leave the caches empty for the next test."""
    for blob in sorted(_RESOURCES.glob("*_rc.py")):
        importlib.import_module(f"{_RC_PACKAGE}.{blob.stem}")
    BlocksPixmap.clear()
    yield
    BlocksPixmap.clear()


def _bytes(pixmap: QtGui.QPixmap) -> int:
    return pixmap.width() * pixmap.height() * pixmap.depth() // 8


@pytest.mark.parametrize("icon", list(Icon), ids=lambda i: i.name)
def test_every_icon_member_resolves(icon):
    """Each Icon value names a real resource, so nothing paints blank."""
    pixmap = BlocksPixmap.get(icon, QtCore.QSize(64, 64))
    assert not pixmap.isNull(), f"{icon.name} -> {icon.value} is not a declared key"


def test_get_returns_the_same_pixmap_twice():
    """A repeat get() hands back the cached surface rather than re-rendering."""
    size = QtCore.QSize(48, 48)
    first = BlocksPixmap.get(Icon.BACK, size)
    second = BlocksPixmap.get(Icon.BACK, size)
    assert first.cacheKey() == second.cacheKey()


def test_icon_objects_are_shared():
    """Two QIcons over one path do not share a render cache, so the QIcon is held."""
    assert BlocksPixmap.icon(Icon.BACK) is BlocksPixmap.icon(Icon.BACK)


def test_pixmap_cache_is_bounded():
    """A widget resizing on every paint cannot grow the cache without limit."""
    for edge in range(16, 16 + BlocksPixmap._MAX_PIXMAPS * 2):
        BlocksPixmap.get(Icon.BACK, QtCore.QSize(edge, edge))
    assert len(BlocksPixmap._pixmaps) <= BlocksPixmap._MAX_PIXMAPS


def test_clear_empties_both_caches():
    """clear() releases every QPixmap while qApp is still alive."""
    BlocksPixmap.get(Icon.BACK, QtCore.QSize(32, 32))
    BlocksPixmap.clear()
    assert not BlocksPixmap._icons
    assert not BlocksPixmap._pixmaps


def test_get_costs_far_less_than_source():
    """The whole point: rendering at 64px must beat the intrinsic buffers 5x over."""
    scaled = sum(_bytes(BlocksPixmap.get(i, QtCore.QSize(64, 64))) for i in Icon)
    BlocksPixmap.clear()
    intrinsic = sum(_bytes(BlocksPixmap.source(i)) for i in Icon)
    assert scaled * 5 < intrinsic, f"{scaled} B scaled vs {intrinsic} B intrinsic"


@pytest.mark.parametrize(
    ("bars", "protected", "expected"),
    [
        (0, False, Icon.WIFI_0BAR),
        (3, True, Icon.WIFI_3BAR_PROTECTED),
        (4, False, Icon.WIFI_4BAR),
        (-1, False, Icon.WIFI_0BAR),
        (9, True, Icon.WIFI_4BAR_PROTECTED),
    ],
)
def test_wifi_clamps_to_the_declared_assets(bars, protected, expected):
    """Only 0..4 bar assets exist, so out-of-range signal must clamp, not raise."""
    assert Icon.wifi(bars, protected) is expected
