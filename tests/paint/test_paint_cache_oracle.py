"""Cache-invalidation oracle for the paint-caching widgets on perf/button-paint-loop-fix.

Those caches fail as stale visuals, never as crashes, so a profiler cannot see them.
Oracle: a widget driven through a mutation history into state S must render identically
to a fresh instance placed directly into S. The fresh instance has no cache history, so
any pixel difference is a cache that failed to invalidate.

Runs two ways, deliberately: `pytest tests/paint` for CI, or `python
test_paint_cache_oracle.py` standalone so it needs nothing installed on the printer.

Green here proves nothing on its own: after changing a cache key, run `make mutants` to
confirm these oracles still turn red on a deliberately broken widget.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import logging
import os
import sys
from collections.abc import Callable
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":
    pytest = None  # run directly: take the printer's path even where pytest exists
else:
    try:
        import pytest
    except ImportError:  # standalone on the printer, where pytest is absent
        pytest = None  # type: ignore[assignment]

logger = logging.getLogger("paint_oracle")

# BS_PAINT_UTILS points the oracle at another checkout, e.g. a branch exported to /tmp.
_UTILS = Path(
    os.environ.get("BS_PAINT_UTILS")
    or Path(__file__).resolve().parents[2] / "BlocksScreen" / "lib" / "utils"
)

SIZE_A = QtCore.QSize(240, 84)
SIZE_B = QtCore.QSize(180, 120)
SIZE_C = QtCore.QSize(240, 120)  # A's width, B's height: catches a width-only cache key
SIZE_D = QtCore.QSize(180, 84)  # B's width, A's height: catches a height-only key

SPEC_IDS = [
    "display_button",
    "icon_button",
    "blocks_button",
    "blocks_label",
    "list_button",
    "blocks_progressbar",
    "toggle_animated",
]


class _Skipped(Exception):
    """Raised in standalone mode where pytest would have skipped."""


def _skip(msg: str) -> None:
    """Skip under pytest, or record a skip in standalone mode."""
    if pytest is not None:
        pytest.skip(msg)
    raise _Skipped(msg)


def _parametrize(values: list[str]):
    """Parametrize under pytest and record the values for the standalone runner."""

    def deco(fn):
        fn._bs_params = list(values)
        if pytest is not None:
            return pytest.mark.parametrize("spec_id", values)(fn)
        return fn

    return deco


class _Bot:
    """Minimal qtbot stand-in so this file runs with or without pytest-qt."""

    def __init__(self) -> None:
        self._widgets: list[QtWidgets.QWidget] = []

    def addWidget(self, w: QtWidgets.QWidget) -> None:
        """Register a widget for teardown; name matches qtbot's."""
        self._widgets.append(w)

    def wait(self, ms: int) -> None:
        """Spin the event loop for ms so animations and deferred paints land."""
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(ms, loop.quit)
        loop.exec()

    def cleanup(self) -> None:
        """Stop animations before destroying widgets; a live animation on a dead target crashes."""
        for w in self._widgets:
            for anim in w.findChildren(QtCore.QAbstractAnimation):
                anim.stop()
            for val in list(vars(w).values()):
                if isinstance(val, QtCore.QAbstractAnimation):
                    val.stop()
            w.close()
        self._widgets.clear()
        QtWidgets.QApplication.processEvents()


# Module-global: an unreferenced QApplication is garbage-collected and Qt then aborts.
_APP: QtWidgets.QApplication | None = None


def _app() -> QtWidgets.QApplication:
    """Return the process QApplication, creating it in standalone mode."""
    global _APP
    existing = QtWidgets.QApplication.instance()
    if isinstance(existing, QtWidgets.QApplication):
        _APP = existing
        return existing
    _APP = QtWidgets.QApplication([])
    return _APP


if pytest is not None:

    @pytest.fixture
    def bot():
        """qtbot-shaped fixture that does not require pytest-qt to be installed."""
        _app()
        b = _Bot()
        yield b
        b.cleanup()


def _load(mod: str):
    """Import a lib/utils module by path; all of these depend only on PyQt6."""
    path = _UTILS / f"{mod}.py"
    if not path.exists():
        _skip(f"{path} not present on this branch")
    spec = importlib.util.spec_from_file_location(f"_pc_{mod}", path)
    if spec is None or spec.loader is None:
        _skip(f"cannot load {path}")
        raise AssertionError  # unreachable, narrows the type
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _pixmap(color: str, size: int) -> QtGui.QPixmap:
    """Solid pixmap with a corner notch so wrong-scale cache reuse stays visible."""
    pm = QtGui.QPixmap(size, size)
    pm.fill(QtGui.QColor(color))
    painter = QtGui.QPainter(pm)
    painter.fillRect(0, 0, size // 3, size // 3, QtGui.QColor("black"))
    painter.end()
    return pm


def _render(
    w: QtWidgets.QWidget, size: QtCore.QSize, settle_ms: int, bot: _Bot
) -> QtGui.QImage:
    """Force a real paintEvent into an image."""
    w.resize(size)
    # Some widgets build paint state in showEvent, so grabbing unshown gives a false diff.
    if not w.isVisible():
        w.show()
        QtWidgets.QApplication.processEvents()
    if settle_ms:
        bot.wait(settle_ms)
    return w.grab().toImage()


def _diff(a: QtGui.QImage, b: QtGui.QImage) -> int:
    """Count differing pixels; -1 when the two images are not even comparable."""
    if a.size() != b.size():
        return -1
    fmt = QtGui.QImage.Format.Format_ARGB32
    a, b = a.convertToFormat(fmt), b.convertToFormat(fmt)
    return sum(
        1
        for y in range(a.height())
        for x in range(a.width())
        if a.pixel(x, y) != b.pixel(x, y)
    )


@dataclasses.dataclass
class _Spec:
    """One widget under test: how to build it and a ladder of complete states."""

    factory: Callable[[], QtWidgets.QWidget]
    states: list[Callable[[QtWidgets.QWidget], None]]
    settle_ms: int = 0


def _build(spec_id: str, bot: _Bot) -> _Spec:
    """Construct the spec for one widget; each state sets EVERY cached input."""
    _app()
    red, blue, green = _pixmap("red", 64), _pixmap("blue", 32), _pixmap("green", 96)

    def track(w):
        bot.addWidget(w)
        return w

    if spec_id == "display_button":
        cls = _load("display_button").DisplayButton

        def dstate(text, sec, pm):
            def apply(w):
                w.setText(text)
                w.setSecondaryText(sec)
                w.setPixmap(pm)
                w.setSecondaryPixmap(pm)

            return apply

        return _Spec(
            factory=lambda: track(cls()),
            states=[
                dstate("100", "0C", red),
                dstate("205", "210C", blue),
                dstate("60", "60C", green),
            ],
        )

    if spec_id == "list_button":
        lb = _load("list_button").ListCustomButton

        def lstate(text, right, pm):
            def apply(w):
                w.setText(text)
                w.setRightText(right)
                w.setPixmap(pm)
                w.setSecondPixmap(pm)

            return apply

        return _Spec(
            factory=lambda: track(lb()),
            states=[
                lstate("model_a.gcode", "1h 20m", red),
                lstate("a-much-longer-filename.gcode", "12h 04m", blue),
                lstate("b.gcode", "4m", green),
            ],
        )

    if spec_id == "blocks_progressbar":
        pb = _load("blocks_progressbar").CustomProgressBar

        def pstate(frac, pm):
            def apply(w):
                w.set_inner_pixmap(pm)
                w.set_progress(frac)

            return apply

        return _Spec(
            factory=lambda: track(pb()),
            states=[pstate(0.0, red), pstate(0.5, blue), pstate(1.0, green)],
        )

    if spec_id == "toggle_animated":
        tb = _load("toggleAnimatedButton").ToggleAnimatedButton

        # stateChange is pyqtSignal(State), so assigning a bool segfaults PyQt6.
        def tstate(on, pm):
            def apply(w):
                w.setPixmap(pm)
                w.state = tb.State.ON if on else tb.State.OFF

            return apply

        def make_toggle():
            # The ctor requires a parent, but a child of a hidden parent never gets shown.
            holder = QtWidgets.QWidget()  # must outlive the call or it takes the child
            w = tb(holder)
            w.setParent(None)
            return track(w)

        return _Spec(
            factory=make_toggle,
            states=[tstate(False, red), tstate(True, blue), tstate(False, green)],
            settle_ms=400,
        )

    if spec_id == "icon_button":
        cls = _load("icon_button").IconButton
    elif spec_id == "blocks_button":
        cls = _load("blocks_button").BlocksCustomButton
    elif spec_id == "blocks_label":
        cls = _load("blocks_label").BlocksLabel
    else:
        _skip(f"unknown spec {spec_id}")
        raise AssertionError  # unreachable, narrows the type

    def bstate(text, pm):
        def apply(w):
            w.setText(text)
            w.setPixmap(pm)

        return apply

    return _Spec(
        factory=lambda: track(cls()),
        states=[
            bstate("Load", red),
            bstate("Unload filament", blue),
            bstate("Ok", green),
        ],
    )


@_parametrize(SPEC_IDS)
def test_fresh_instance_equivalence(bot, spec_id):
    """A mutated widget must match a fresh one in the same state: the core cache oracle."""
    spec = _build(spec_id, bot)
    seq = spec.factory()
    for k, apply_state in enumerate(spec.states):
        apply_state(seq)
        got = _render(seq, SIZE_A, spec.settle_ms, bot)

        fresh = spec.factory()
        apply_state(fresh)
        want = _render(fresh, SIZE_A, spec.settle_ms, bot)

        n = _diff(got, want)
        assert n == 0, f"{spec_id}: state {k} differs by {n}px after mutation history"


@_parametrize(SPEC_IDS)
def test_state_round_trip(bot, spec_id):
    """Returning to a previous state must restore its exact pixels."""
    spec = _build(spec_id, bot)
    w = spec.factory()
    spec.states[0](w)
    before = _render(w, SIZE_A, spec.settle_ms, bot)
    for apply_state in spec.states[1:]:
        apply_state(w)
        _render(w, SIZE_A, spec.settle_ms, bot)
    spec.states[0](w)
    after = _render(w, SIZE_A, spec.settle_ms, bot)
    n = _diff(before, after)
    assert n == 0, f"{spec_id}: round trip back to state 0 differs by {n}px"


@_parametrize(SPEC_IDS)
def test_resize_round_trip(bot, spec_id):
    """Size-keyed caches must survive a resize away and back.

    The ladder varies width and height independently, so a key that drops either
    dimension collides and returns the wrong cached geometry.
    """
    spec = _build(spec_id, bot)
    w = spec.factory()
    spec.states[-1](w)
    before = _render(w, SIZE_A, spec.settle_ms, bot)
    for size in (SIZE_B, SIZE_C, SIZE_D):
        _render(w, size, spec.settle_ms, bot)
    after = _render(w, SIZE_A, spec.settle_ms, bot)
    n = _diff(before, after)
    assert n == 0, f"{spec_id}: resize round trip differs by {n}px"


@_parametrize(SPEC_IDS)
def test_resize_ladder_matches_fresh(bot, spec_id):
    """Every rung of a resize walk must match a fresh instance built at that size.

    The round trip only checks the size it returns to, where a partial key happens to
    be right again; the stale geometry it serves on the way through shows up here.
    """
    spec = _build(spec_id, bot)
    w = spec.factory()
    spec.states[-1](w)
    _render(w, SIZE_A, spec.settle_ms, bot)
    for size in (SIZE_B, SIZE_C, SIZE_D):
        walked = _render(w, size, spec.settle_ms, bot)
        fresh = spec.factory()
        spec.states[-1](fresh)
        expected = _render(fresh, size, spec.settle_ms, bot)
        n = _diff(walked, expected)
        assert n == 0, (
            f"{spec_id}: at {size.width()}x{size.height()} the resized widget "
            f"differs from a fresh one by {n}px"
        )


@_parametrize(SPEC_IDS)
def test_repeat_render_stable(bot, spec_id):
    """Two consecutive paints with no mutation must be identical."""
    spec = _build(spec_id, bot)
    w = spec.factory()
    spec.states[0](w)
    a = _render(w, SIZE_A, spec.settle_ms, bot)
    b = _render(w, SIZE_A, spec.settle_ms, bot)
    n = _diff(a, b)
    assert n == 0, f"{spec_id}: consecutive paints differ by {n}px (nondeterministic)"


def _cache_sizes(w) -> dict[str, int]:
    """Sizes of every dict cache hanging off a widget."""
    return {
        name: len(val)
        for name, val in vars(w).items()
        if "cache" in name and isinstance(val, dict)
    }


@_parametrize(SPEC_IDS)
def test_caches_do_not_grow_per_paint(bot, spec_id):
    """Caches may hold one entry per distinct state, but must not grow on every paint.

    Geometry-keyed caches are intentionally unbounded; the real leak signature is growth
    at CONSTANT geometry and state, which is what this measures.
    """
    spec = _build(spec_id, bot)
    w = spec.factory()
    spec.states[0](w)
    _render(w, SIZE_A, spec.settle_ms, bot)
    baseline = _cache_sizes(w)
    for _ in range(200):
        w.update()
        w.grab()
    grew = {k: (baseline[k], v) for k, v in _cache_sizes(w).items() if v > baseline[k]}
    assert not grew, f"{spec_id}: caches grew over 200 identical paints {grew}"


PALETTE_A = ("red", "blue", "green", "yellow")
PALETTE_B = ("cyan", "magenta", "black", "white")  # same geometry, different pixels


def _make_items(cls, count: int, palette: tuple[str, ...] = PALETTE_A) -> list:
    """Build ListItems varying in every delegate-cached dimension: text, size, icon, tint."""
    names = {f.name for f in dataclasses.fields(cls)}
    icons = [_pixmap(c, 32) for c in palette]
    items = []
    for i in range(count):
        tail = "-with-a-long-tail" if i % 3 else ""
        kwargs: dict[str, object] = {"text": f"row-{i:03d}{tail}"}
        if "right_text" in names:
            kwargs["right_text"] = f"{i}m"
        if "height" in names:
            kwargs["height"] = 48 + (i % 4) * 12
        if "left_icon" in names:
            kwargs["left_icon"] = icons[i % len(icons)]
        if "color_left_icon" in names:
            kwargs["color_left_icon"] = bool(i % 2)
        if "color" in names:
            kwargs["color"] = "#dfdfdf" if i % 2 else "#44aa88"
        items.append(cls(**kwargs))
    return items


def test_list_delegate_recycling(bot):
    """Scrolling a long list and back must not bleed one row's cached paint into another."""
    _app()
    lm = _load("list_model")
    try:
        items = _make_items(lm.ListItem, 60)
    except (TypeError, ValueError) as exc:
        _skip(f"ListItem signature not introspectable: {exc}")

    def make_view(scroll: bool) -> QtGui.QImage:
        view = QtWidgets.QListView()
        bot.addWidget(view)
        view.setItemDelegate(lm.EntryDelegate())
        model = lm.EntryListModel(list(items))
        view.setModel(model)
        view.resize(420, 300)
        view.show()  # an unshown view lays out differently, which is not a cache fault
        QtWidgets.QApplication.processEvents()
        if scroll:
            view.scrollTo(model.index(len(items) - 1, 0))
            view.grab()
        # Pin both views to the identical offset so only cached paint can differ.
        bar = view.verticalScrollBar()
        if bar is not None:
            bar.setValue(0)
        return view.grab().toImage()

    n = _diff(make_view(scroll=True), make_view(scroll=False))
    assert n == 0, f"list delegate: top of list differs by {n}px after scrolling away"


def test_list_delegate_icon_identity(bot):
    """One delegate reused across two item sets must not serve the first set's icons.

    Both sets share every geometry and differ only in icon pixels, so a scaled-pixmap
    key that omits the source identity collides and the second render stays stale.
    """
    _app()
    lm = _load("list_model")
    try:
        _make_items(lm.ListItem, 1)
    except (TypeError, ValueError) as exc:
        _skip(f"ListItem signature not introspectable: {exc}")

    def render(delegate, palette: tuple[str, ...]) -> QtGui.QImage:
        view = QtWidgets.QListView()
        bot.addWidget(view)
        view.setItemDelegate(delegate)
        view.setModel(lm.EntryListModel(_make_items(lm.ListItem, 12, palette)))
        view.resize(420, 300)
        view.show()  # an unshown view lays out differently, which is not a cache fault
        QtWidgets.QApplication.processEvents()
        return view.grab().toImage()

    shared = (
        lm.EntryDelegate()
    )  # must outlive both views; setItemDelegate takes no ownership
    render(shared, PALETTE_A)  # warms the scaled and tinted caches with set A
    reused = render(shared, PALETTE_B)
    fresh = render(lm.EntryDelegate(), PALETTE_B)
    n = _diff(reused, fresh)
    assert n == 0, f"list delegate: reused delegate kept stale icons, {n}px differ"


def main() -> int:
    """Standalone runner: no pytest, no pytest-qt, prints a per-case report."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    _app()
    tests = [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]
    passed = skipped = 0
    failures: list[str] = []
    for name, fn in tests:
        for param in getattr(fn, "_bs_params", [None]):
            label = f"{name}[{param}]" if param else name
            b = _Bot()
            try:
                fn(b, param) if param else fn(b)
            except _Skipped as exc:
                skipped += 1
                logger.info("SKIP %s: %s", label, exc)
            except AssertionError as exc:
                failures.append(f"{label}: {exc}")
                logger.info("FAIL %s\n     %s", label, exc)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{label}: {type(exc).__name__}: {exc}")
                logger.info("ERROR %s\n      %s: %s", label, type(exc).__name__, exc)
            else:
                passed += 1
                logger.info("PASS %s", label)
            finally:
                b.cleanup()
    logger.info("\n%d passed, %d failed, %d skipped", passed, len(failures), skipped)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
