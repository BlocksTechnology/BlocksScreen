#!/usr/bin/env python3
"""Offscreen UI selftest emitting TSV STATUS/name/detail rows for bs-healthcheck.sh: catches render breaks (stale/missing generated forms, icons) a running D-Bus-answering process can hide; side-effect-free (no MainWindow/socket/D-Bus/file writes); unused forms WARN not FAIL."""

from __future__ import annotations

import io
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET  # nosec B405 - only ever fed our own repo's .qrc files
from collections.abc import Callable, Iterable
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

# Walk up to the repo root instead of counting directories, so this script survives being moved.
_HERE = Path(__file__).resolve()
ROOT = next(
    (p for p in _HERE.parents if (p / "BlocksScreen").is_dir()), _HERE.parent.parent
)
PKG = ROOT / "BlocksScreen"
UIDIR = PKG / "lib" / "ui"
RESDIR = UIDIR / "resources"
MOONRAKER = os.environ.get("BS_MOONRAKER", "http://localhost:7125")

if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

_FAILED = 0
_APP = None


def emit(status: str, name: str, detail: str = "") -> None:
    """Write one TSV assertion row."""
    global _FAILED
    if status == "FAIL":
        _FAILED += 1
    detail = " ".join(str(detail).split())[:400]
    sys.stdout.write(f"{status}\t{name}\t{detail}\n")
    sys.stdout.flush()


def guard(name: str, fn: Callable[[], tuple[str, str]]) -> None:
    """Run one assertion, turning any escaping exception into a FAIL rather than killing the run."""
    try:
        status, detail = fn()
    except Exception as exc:  # noqa: BLE001 - a crashing probe is itself the finding
        emit("FAIL", name, f"{type(exc).__name__}: {exc}")
        return
    emit(status, name, detail)


def _qapp():
    """One shared offscreen QApplication, kept in a global so PyQt cannot collect it mid-run."""
    global _APP
    if _APP is None:
        from PyQt6 import QtWidgets

        _APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    return _APP


def _load_module(path: Path):
    """Import a file by path under a private name, so it cannot collide with the app's own modules."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(f"_bsselftest_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"{path.name}: no loader")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_RES_LOADED: list[str] = []
_RES_KEEPALIVE: list[object] = []


def _load_resources() -> list[str]:
    """Register every compiled resource bundle once (so :/ lookups work later); keeps module objects alive on purpose since Qt holds a pointer into their bytes and GC'ing one segfaults the next :/ read."""
    if _RES_LOADED:
        return _RES_LOADED
    _qapp()
    for m in sorted(RESDIR.glob("*_rc.py")):
        try:
            _RES_KEEPALIVE.append(_load_module(m))
            _RES_LOADED.append(m.name)
        except Exception as exc:  # noqa: BLE001
            _RES_LOADED.append(f"!{m.name}: {type(exc).__name__}: {exc}")
    return _RES_LOADED


def _py_sources() -> list[Path]:
    return [p for p in PKG.rglob("*.py") if "__pycache__" not in p.parts]


_LIVE_UI: set[str] | None = None


def _live_ui_modules() -> set[str]:
    """Generated modules some other source file imports: only those can break the real UI."""
    global _LIVE_UI
    if _LIVE_UI is not None:
        return _LIVE_UI
    stems = {g.stem for g in UIDIR.glob("*_ui.py")}
    live: set[str] = set()
    for py in _py_sources():
        if py.parent == UIDIR:
            continue
        try:
            text = py.read_text(errors="replace")
        except OSError:
            continue
        live |= {
            s for s in stems if re.search(rf"(?<![A-Za-z0-9_]){re.escape(s)}\b", text)
        }
    _LIVE_UI = live
    return live


def _is_dead_ui(path: Path) -> bool:
    return (
        path.parent == UIDIR
        and path.stem.endswith("_ui")
        and path.stem not in _live_ui_modules()
    )


# --------------------------------------------------------------------------- resources


def t_rc_import() -> tuple[str, str]:
    """Every compiled resource bundle imports and registers."""
    loaded = _load_resources()
    if not loaded:
        return "FAIL", f"no *_rc.py bundles under {RESDIR}"
    bad = [x[1:] for x in loaded if x.startswith("!")]
    if bad:
        return "FAIL", "; ".join(bad)
    return "PASS", f"{len(loaded)} bundle(s) registered"


def t_qrc_assets() -> tuple[str, str]:
    """Every file listed in a .qrc still exists, so the next rcc rebuild cannot silently drop it."""
    qrcs = sorted(RESDIR.glob("*.qrc"))
    if not qrcs:
        return "SKIP", "no .qrc files"
    missing = []
    total = 0
    for q in qrcs:
        try:
            root = ET.parse(q).getroot()  # nosec B314 - only ever fed our own repo's .qrc files
        except ET.ParseError as exc:
            missing.append(f"{q.name}: malformed ({exc})")
            continue
        for f in root.iter("file"):
            total += 1
            rel = (f.text or "").strip()
            if rel and not (q.parent / rel).exists():
                missing.append(f"{q.name}:{rel}")
    if missing:
        return "FAIL", f"{len(missing)}/{total} listed asset(s) missing: " + ", ".join(
            missing[:8]
        )
    return "PASS", f"{total} asset(s) present"


_RES_REF = re.compile(r'["\'](:/[A-Za-z0-9_\-./]+)["\']')


def _resource_refs() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Literal :/ paths in source, split into refs from live code and refs from dead generated forms."""
    live: dict[str, set[str]] = {}
    dead: dict[str, set[str]] = {}
    for py in _py_sources():
        try:
            text = py.read_text(errors="replace")
        except OSError:
            continue
        bucket = dead if _is_dead_ui(py) else live
        for path in _RES_REF.findall(text):
            if "{" in path or "%" in path:
                continue
            bucket.setdefault(path, set()).add(py.name)
    return live, dead


def t_resource_refs_resolve() -> tuple[str, str]:
    """Every literal :/icon path live code asks for resolves, otherwise that control renders blank."""
    from PyQt6 import QtCore

    _load_resources()
    live, _ = _resource_refs()
    if not live:
        return "SKIP", "no literal resource references found"
    missing = [p for p in live if not QtCore.QFile(p).exists()]
    if missing:
        detail = ", ".join(
            f"{p} (in {','.join(sorted(live[p]))})" for p in sorted(missing)[:8]
        )
        return "FAIL", f"{len(missing)}/{len(live)} unresolved: {detail}"
    return "PASS", f"{len(live)} reference(s) resolve"


def t_dead_resource_refs() -> tuple[str, str]:
    """Unresolved :/ paths inside generated forms nothing imports: dead weight, not a field fault."""
    from PyQt6 import QtCore

    _load_resources()
    _, dead = _resource_refs()
    missing = [p for p in dead if not QtCore.QFile(p).exists()]
    if missing:
        return "WARN", f"{len(missing)} unresolved in unused forms: " + ", ".join(
            sorted(missing)[:6]
        )
    return "PASS", ""


def t_fonts_loadable() -> tuple[str, str]:
    """The bundled fonts actually load, otherwise Qt silently substitutes and the layout shifts."""
    from PyQt6 import QtCore, QtGui

    _qapp()
    _load_resources()
    it = QtCore.QDirIterator(
        ":", QtCore.QDir.Filter.Files, QtCore.QDirIterator.IteratorFlag.Subdirectories
    )
    fonts = []
    while it.hasNext():
        p = it.next()
        if p.lower().endswith((".ttf", ".otf")):
            fonts.append(p)
    if not fonts:
        return "SKIP", "no fonts in the resource tree"
    bad = [f for f in fonts if QtGui.QFontDatabase.addApplicationFont(f) == -1]
    if bad:
        return "FAIL", f"rejected by Qt: {', '.join(bad[:6])}"
    return "PASS", f"{len(fonts)} font(s) loaded"


# --------------------------------------------------------------------------- ui layer


def _ui_pairs() -> list[tuple[Path, Path]]:
    return [(u, u.with_name(u.stem + "_ui.py")) for u in sorted(UIDIR.glob("*.ui"))]


def t_ui_generated_present() -> tuple[str, str]:
    """Every .ui the app uses has its generated counterpart, or that tab comes up blank."""
    live = _live_ui_modules()
    missing = [
        u.name for u, g in _ui_pairs() if not g.exists() and u.stem + "_ui" in live
    ]
    if missing:
        return "FAIL", "no generated _ui.py for: " + ", ".join(missing)
    return "PASS", f"{len(_ui_pairs())} form(s)"


def t_orphan_ui_files() -> tuple[str, str]:
    """.ui files with no generated module and no importer: leftovers, and they blur the real set."""
    live = _live_ui_modules()
    orphan = [
        u.name for u, g in _ui_pairs() if not g.exists() and u.stem + "_ui" not in live
    ]
    if orphan:
        return "WARN", "never compiled and never imported: " + ", ".join(orphan)
    return "PASS", ""


_SHAPE = re.compile(
    r'setObjectName\("([^"]+)"\)|(Qt\w+\.Q\w+)\(|["\'](:/[A-Za-z0-9_\-./]+)["\']'
)


def _shape(src: str) -> list[str]:
    """Structural fingerprint (object names, widget classes, resource paths) instead of a text diff, since pyuic6 embeds its own version and the generating machine's absolute path into every output."""
    return sorted(next(g for g in m.groups() if g) for m in _SHAPE.finditer(src))


def t_ui_generated_current() -> tuple[str, str]:
    """The generated _ui.py still matches its .ui, so an edited form cannot ship uncompiled."""
    from PyQt6 import uic

    stale = []
    checked = 0
    for u, g in _ui_pairs():
        if not g.exists():
            continue
        buf = io.StringIO()
        try:
            uic.compileUi(str(u), buf)  # type: ignore[attr-defined]
        except Exception as exc:  # noqa: BLE001
            stale.append(f"{u.name}: will not compile ({type(exc).__name__}: {exc})")
            continue
        checked += 1
        want, have = _shape(buf.getvalue()), _shape(g.read_text(errors="replace"))
        if want != have:
            delta = set(want) ^ set(have)
            stale.append(f"{u.name} ({len(delta)} element(s) differ)")
    if stale:
        return "WARN", f"{len(stale)}/{checked} need a pyuic6 rerun: " + ", ".join(
            stale[:8]
        )
    return "PASS", f"{checked} form(s) up to date"


def _build_forms(paths: Iterable[Path]) -> tuple[int, list[str]]:
    """Build every Ui_* class in the given generated modules onto a host widget."""
    from PyQt6 import QtWidgets

    _qapp()
    _load_resources()
    built = 0
    bad: list[str] = []
    for g in paths:
        try:
            mod = _load_module(g)
        except Exception as exc:  # noqa: BLE001
            bad.append(f"{g.name}: import {type(exc).__name__}: {exc}")
            continue
        for attr in dir(mod):
            if not attr.startswith("Ui_"):
                continue
            cls = getattr(mod, attr)
            if getattr(cls, "setupUi", None) is None:
                continue
            # setupUi's base class is whatever the form was drawn on; try each plausible host, keep the first error (later ones are just wrong-host noise).
            first: Exception | None = None
            ok = False
            for host in (
                QtWidgets.QWidget,
                QtWidgets.QStackedWidget,
                QtWidgets.QMainWindow,
                QtWidgets.QDialog,
                QtWidgets.QTabWidget,
            ):
                try:
                    cls().setupUi(host())
                    built += 1
                    ok = True
                    break
                except Exception as exc:  # noqa: BLE001
                    first = first or exc
            if not ok:
                bad.append(f"{g.name}:{attr}: {type(first).__name__}: {first}")
    return built, bad


def t_widgets_build() -> tuple[str, str]:
    """Every form the app imports builds onto a host widget: the real render path, minus the app."""
    live = sorted(g for g in UIDIR.glob("*_ui.py") if g.stem in _live_ui_modules())
    if not live:
        return (
            "FAIL",
            "no generated form is imported anywhere, the UI cannot be assembled",
        )
    built, bad = _build_forms(live)
    if bad:
        return "FAIL", f"{len(bad)} failed: " + "; ".join(bad[:6])
    if not built:
        return "FAIL", "no Ui_* classes found to build"
    return "PASS", f"{built} widget class(es) build from {len(live)} module(s)"


def t_orphan_forms() -> tuple[str, str]:
    """Generated forms nothing imports: harmless in the field, but they mask real breakage here."""
    dead = sorted(
        g.stem for g in UIDIR.glob("*_ui.py") if g.stem not in _live_ui_modules()
    )
    if dead:
        return "WARN", f"{len(dead)} unused generated form(s): " + ", ".join(dead)
    return "PASS", ""


def t_stylesheets_parse() -> tuple[str, str]:
    """Qt swallows malformed stylesheet rules silently, so an unbalanced brace loses whole themes."""
    sheets = list(PKG.rglob("*.qss")) + list(PKG.rglob("*.css"))
    if not sheets:
        return "SKIP", "no stylesheet files"
    bad = []
    for s in sheets:
        text = s.read_text(errors="replace")
        if text.count("{") != text.count("}"):
            bad.append(
                f"{s.name}: {text.count('{')} open vs {text.count('}')} close braces"
            )
    if bad:
        return "FAIL", "; ".join(bad)
    return "PASS", f"{len(sheets)} stylesheet(s) balanced"


# --------------------------------------------------------------------------- runtime


def _moon(path: str, timeout: float = 6.0) -> dict:
    url = f"{MOONRAKER}{path}"
    if urllib.parse.urlsplit(url).scheme not in ("http", "https"):
        raise ValueError(f"refusing non-http(s) BS_MOONRAKER scheme: {url}")
    with urllib.request.urlopen(url, timeout=timeout) as fh:  # nosec B310 - scheme checked above
        return json.load(fh)


def t_moonraker_ready() -> tuple[str, str]:
    """Moonraker is up and klippy is ready, which is the state the UI needs to leave its splash."""
    try:
        res = _moon("/server/info")["result"]
    except (urllib.error.URLError, OSError, KeyError, ValueError) as exc:
        return "SKIP", f"moonraker not answering: {type(exc).__name__}"
    state = res.get("klippy_state", "?")
    if res.get("klippy_connected") is not True:
        return (
            "FAIL",
            f"moonraker is up but klippy_connected=false, klippy_state={state}",
        )
    if state != "ready":
        return "FAIL", f"klippy_state={state}, the UI will sit on the connection screen"
    return "PASS", f"klippy_state={state}"


def t_moonraker_objects() -> tuple[str, str]:
    """The printer objects the UI reads must exist, or those panels show placeholders forever."""
    required = (
        "toolhead",
        "extruder",
        "print_stats",
        "virtual_sdcard",
        "idle_timeout",
        "gcode_move",
    )
    try:
        objs = _moon("/printer/objects/list")["result"]["objects"]
    except (urllib.error.URLError, OSError, KeyError, ValueError) as exc:
        return "SKIP", f"moonraker not answering: {type(exc).__name__}: {exc}"
    missing = [o for o in required if o not in objs]
    if missing:
        return "FAIL", "klipper is not exposing: " + ", ".join(missing)
    return "PASS", f"{len(objs)} object(s) exposed"


def t_moonraker_optional_objects() -> tuple[str, str]:
    """Objects whose panels degrade rather than break when the printer does not define them."""
    optional = (
        "heater_bed",
        "display_status",
        "fan",
        "filament_switch_sensor",
        "bed_mesh",
    )
    try:
        objs = _moon("/printer/objects/list")["result"]["objects"]
    except (urllib.error.URLError, OSError, KeyError, ValueError) as exc:
        return "SKIP", f"moonraker not answering: {type(exc).__name__}"
    absent = [
        o for o in optional if not any(x == o or x.startswith(o + " ") for x in objs)
    ]
    if absent:
        return "WARN", "not defined on this printer: " + ", ".join(absent)
    return "PASS", ""


def t_config_parses() -> tuple[str, str]:
    """BlocksScreen.cfg parses, so the UI is not silently falling back to untested defaults."""
    import configparser

    env = os.environ.get("BS_CONFIG")
    cands = [Path(env)] if env else []
    cands += [
        Path.home() / "printer_data" / "config" / "BlocksScreen.cfg",
        ROOT / "BlocksScreen.cfg",
    ]
    cfg_path = next((c for c in cands if c.is_file()), None)
    if cfg_path is None:
        return "SKIP", "BlocksScreen.cfg not found"
    parser = configparser.ConfigParser(strict=False, inline_comment_prefixes=(";", "#"))
    try:
        parser.read(cfg_path)
    except configparser.Error as exc:
        return "FAIL", f"{cfg_path}: {exc}"
    return "PASS", f"{cfg_path.name}: {len(parser.sections())} section(s)"


def t_no_dev_flag() -> tuple[str, str]:
    """BLOCKSCREEN_DEV shipping enabled would leave debug affordances on a customer machine."""
    val = os.environ.get("BLOCKSCREEN_DEV")
    unit = Path("/etc/systemd/system/BlocksScreen.service")
    in_unit = ""
    if unit.is_file():
        for ln in unit.read_text(errors="replace").splitlines():
            if "BLOCKSCREEN_DEV" in ln and not ln.strip().startswith("#"):
                in_unit = ln.strip()
    if val not in (None, "", "0") or in_unit:
        return "WARN", f"env={val!r} unit={in_unit!r}"
    return "PASS", ""


TESTS: tuple[tuple[str, Callable[[], tuple[str, str]]], ...] = (
    ("compiled resource bundles register", t_rc_import),
    ("qrc-listed assets present on disk", t_qrc_assets),
    ("literal :/ resource references resolve", t_resource_refs_resolve),
    ("bundled fonts load", t_fonts_loadable),
    ("every .ui has a generated _ui.py", t_ui_generated_present),
    ("generated forms the app imports build", t_widgets_build),
    ("generated _ui.py match their .ui", t_ui_generated_current),
    ("stylesheets balanced", t_stylesheets_parse),
    ("klippy ready via moonraker", t_moonraker_ready),
    ("required printer objects exposed", t_moonraker_objects),
    ("optional printer objects", t_moonraker_optional_objects),
    ("BlocksScreen.cfg parses", t_config_parses),
    ("BLOCKSCREEN_DEV not enabled", t_no_dev_flag),
    ("no unused generated forms", t_orphan_forms),
    ("no orphan .ui files", t_orphan_ui_files),
    ("no unresolved icons in unused forms", t_dead_resource_refs),
)


def main() -> int:
    """Run every assertion and return 1 if any of them failed."""
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    for name, fn in TESTS:
        if only and only not in name:
            continue
        guard(name, fn)
    return 1 if _FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
