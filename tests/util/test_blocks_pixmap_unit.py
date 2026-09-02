"""Unit tests for the BlocksPixmap registry and the Icon key enum."""

import importlib

import pytest
from PyQt6 import QtCore, QtGui

from BlocksScreen.lib.utils.blocks_pixmap import (
    BlocksPixmap,
    Icon,
    _cost,
    _PixmapCache,
)

_RC_PACKAGE = "BlocksScreen.lib.ui.resources"
_RC_MODULES = (
    "background_resources_rc",
    "font_rc",
    "graphic_resources_rc",
    "icon_resources_rc",
    "main_menu_resources_rc",
    "top_bar_resources_rc",
)


@pytest.fixture(autouse=True)
def _resources(qapp):
    """Register the compiled blobs, then leave the caches empty for the next test."""
    for module in _RC_MODULES:
        importlib.import_module(f"{_RC_PACKAGE}.{module}")
    BlocksPixmap.clear()
    yield
    BlocksPixmap.clear()


def _bytes(pixmap: QtGui.QPixmap) -> int:
    """Return the pixmap's buffer size in bytes."""
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
    """A widget resizing on every paint cannot grow the cache past its byte budget."""
    for edge in range(16, 400):
        BlocksPixmap.get(Icon.BACK, QtCore.QSize(edge, edge))
    assert BlocksPixmap._pixmaps._bytes <= BlocksPixmap._pixmaps._budget


def test_clear_empties_every_cache():
    """clear() releases every QPixmap while qApp is still alive."""
    source = BlocksPixmap.get(Icon.BACK, QtCore.QSize(32, 32))
    BlocksPixmap.tinted(source, QtGui.QColor("white"))
    BlocksPixmap.clear()
    assert not BlocksPixmap._icons
    assert not BlocksPixmap._pixmaps
    assert not BlocksPixmap._scaled
    assert not BlocksPixmap._tints


def test_get_resamples_a_surface_once():
    """A repeat get() on a surface hands back the cache rather than rescaling per paint."""
    source = BlocksPixmap.get(Icon.BACK)
    size = QtCore.QSize(40, 40)
    assert (
        BlocksPixmap.get(source, size).cacheKey()
        == BlocksPixmap.get(source, size).cacheKey()
    )


def test_get_keys_on_the_aspect_mode():
    """Distort-to-fill and fit-inside must not collide on one key."""
    source = BlocksPixmap.get(Icon.BACK)
    size = QtCore.QSize(80, 20)
    keep = BlocksPixmap.get(source, size)
    ignore = BlocksPixmap.get(source, size, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio)
    assert keep.size() != ignore.size()


def test_derived_cache_is_bounded():
    """One 400x300 thumbnail costs 30 icon rescales, so the budget counts bytes not entries."""
    source = BlocksPixmap.get(Icon.BACK)
    for edge in range(16, 400):
        BlocksPixmap.get(source, QtCore.QSize(edge, edge))
    assert BlocksPixmap._scaled._bytes <= BlocksPixmap._scaled._budget


def test_eviction_drops_the_least_recently_used():
    """FIFO would drop the startup icons first, which are the hottest entries of all."""
    cache = _PixmapCache(2 * _cost(BlocksPixmap.get(Icon.BACK, QtCore.QSize(32, 32))))
    for key in ("a", "b"):
        cache.put(key, BlocksPixmap.get(Icon.BACK, QtCore.QSize(32, 32)))
    cache.get("a")
    cache.put("c", BlocksPixmap.get(Icon.BACK, QtCore.QSize(32, 32)))
    assert cache.get("a") is not None
    assert cache.get("b") is None


@pytest.mark.parametrize(
    "size",
    [
        QtCore.QSize(40, 40),
        QtCore.QSizeF(40.4, 40.4),
        QtCore.QRect(0, 0, 40, 40),
        QtCore.QRectF(0.0, 0.0, 40.4, 40.4),
    ],
    ids=["QSize", "QSizeF", "QRect", "QRectF"],
)
def test_get_accepts_whatever_the_caller_holds(size):
    """Every Qt size or rect normalises to one target, so no call site converts by hand."""
    reference = BlocksPixmap.get(Icon.BACK, QtCore.QSize(40, 40))
    assert BlocksPixmap.get(Icon.BACK, size).cacheKey() == reference.cacheKey()


def test_tinted_recolours_through_the_alpha():
    """A tint keeps the glyph shape, so a painted pixel takes the colour and a clear one stays clear."""
    source = BlocksPixmap.get(Icon.BACK, QtCore.QSize(32, 32))
    image = BlocksPixmap.tinted(source, QtGui.QColor("red")).toImage()
    painted = [
        image.pixelColor(x, y)
        for x in range(image.width())
        for y in range(image.height())
        if image.pixelColor(x, y).alpha() > 0
    ]
    assert painted, "the source glyph painted nothing"
    assert all(c.red() > 250 and not c.green() and not c.blue() for c in painted)


def test_tinted_returns_the_same_surface_twice():
    """A repeat tint hands back the cache rather than allocating a pixmap per paint."""
    source = BlocksPixmap.get(Icon.BACK, QtCore.QSize(32, 32))
    assert (
        BlocksPixmap.tinted(source, "white").cacheKey()
        == BlocksPixmap.tinted(source, "white").cacheKey()
    )


def test_tinted_keys_on_the_colour():
    """Two colours over one surface must not collide on one key."""
    source = BlocksPixmap.get(Icon.BACK, QtCore.QSize(32, 32))
    assert (
        BlocksPixmap.tinted(source, "white").cacheKey()
        != BlocksPixmap.tinted(source, "red").cacheKey()
    )


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
