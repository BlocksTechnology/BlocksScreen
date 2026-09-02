"""Guards Qt resource keys: no broken ':/' literal, no stale blob, no font fallback."""

import importlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG_ROOT = REPO_ROOT / "BlocksScreen"
RESOURCES = PKG_ROOT / "lib" / "ui" / "resources"
RC_PACKAGE = "BlocksScreen.lib.ui.resources"

# Known-broken keys, may only shrink; emptied 2026-09-01 when Icon replaced the templates.
XFAIL_KEYS: dict[str, str] = {}

# Text scan not AST (misses .ui XML); '/' drops ": %s", spaces admit Momcake keys.
_PY_LITERAL = re.compile(r'["\'](:/?[^"\'\s][^"\']*/[^"\']*)["\']')

# .ui keys are unquoted element text: <normaloff>:/x/y.svg</normaloff>.
_UI_LITERAL = re.compile(r">(:/?[^<\s][^<]*/[^<]*)<")

# Stylesheet keys carry no quote next to the ':', so the two patterns above miss them.
_CSS_URL = re.compile(r"url\((:/?[^)\s][^)]*/[^)]*)\)")

# CSS in an .svg <style> block; assets are minified, so the family name carries, not the line.
_FONT_FAMILY = re.compile(r"font-family:\s*([^;}\"']+)")


def _canonical(key: str) -> str:
    """Normalize a bare ':' prefix to ':/', the two forms Qt treats as equivalent."""
    return key if key.startswith(":/") else f":/{key[1:]}"


def _qrc_entries() -> list[tuple[str, Path]]:
    """Return every (resource key, on-disk path) pair declared by the .qrc files."""
    entries = []
    for qrc in sorted(RESOURCES.glob("*.qrc")):
        for qresource in ET.parse(qrc).getroot().findall("qresource"):
            prefix = (qresource.get("prefix") or "").strip("/")
            for element in qresource.findall("file"):
                path = (element.text or "").strip()
                key = f":/{prefix}/{element.get('alias') or path}"
                entries.append((key, qrc.parent / path))
    return entries


def _qrc_keys() -> set[str]:
    """Return the resource keys declared by the .qrc XML, the developer-facing source."""
    return {key for key, _ in _qrc_entries()}


def _literal_sites() -> dict[str, list[str]]:
    """Map every ':/' key under BlocksScreen/lib to its 'file:line' sites, .py and .ui alike."""
    sites: dict[str, list[str]] = {}
    scans = (
        (_PY_LITERAL, "*.py"),
        (_UI_LITERAL, "*.ui"),
        (_CSS_URL, "*.py"),
        (_CSS_URL, "*.ui"),
    )
    for pattern, suffix in scans:
        for source in sorted((PKG_ROOT / "lib").rglob(suffix)):
            if source.name.endswith("_rc.py"):
                continue
            text = source.read_text(errors="replace")
            for number, line in enumerate(text.splitlines(), 1):
                for match in pattern.finditer(line):
                    where = f"{source.relative_to(REPO_ROOT)}:{number}"
                    # An iconset repeats its path on one line.
                    seen = sites.setdefault(match.group(1), [])
                    if where not in seen:
                        seen.append(where)
    return sites


def _qrc_prefix_roots() -> set[str]:
    """Return the top-level ':/<prefix>' roots the .qrc files claim."""
    return {f":/{key.split('/')[1]}" for key in _qrc_keys()}


def _import_blobs() -> None:
    """Import every _rc.py, which is what registers its resources into Qt's tree."""
    for blob in sorted(RESOURCES.glob("*_rc.py")):
        importlib.import_module(f"{RC_PACKAGE}.{blob.stem}")


def _svg_font_families() -> dict[str, list[str]]:
    """Map every font-family declared by an .svg under resources to its 'file:line' sites."""
    families: dict[str, list[str]] = {}
    for svg in sorted(RESOURCES.rglob("*.svg")):
        text = svg.read_text(errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            for match in _FONT_FAMILY.finditer(line):
                where = f"{svg.relative_to(REPO_ROOT)}:{number}"
                families.setdefault(match.group(1).strip(), []).append(where)
    return families


def _compiled_keys() -> set[str]:
    """Return the resource keys compiled into the _rc.py blobs, under our prefixes only."""
    from PyQt6.QtCore import QDir, QDirIterator

    _import_blobs()

    # Walk our own prefixes, never ':/': Qt registers its own resources into the same tree.
    keys = set()
    for root in _qrc_prefix_roots():
        walk = QDirIterator(
            root, QDir.Filter.Files, QDirIterator.IteratorFlag.Subdirectories
        )
        while walk.hasNext():
            keys.add(walk.next())
    return keys


def _report(header: str, detail: dict[str, list[str]]) -> str:
    """Build a multi-line failure message naming every key and its sites."""
    lines = [header]
    for key in sorted(detail):
        lines.append(f"  {key}")
        lines.extend(f"      {item}" for item in detail[key])
    return "\n".join(lines)


def test_resources_dir_is_findable():
    """Fail loudly if the path derivation breaks, so the other tests cannot pass empty."""
    assert RESOURCES.is_dir(), f"resources dir not found at {RESOURCES}"
    assert list(RESOURCES.glob("*.qrc")), f"no .qrc files under {RESOURCES}"


def test_no_broken_resource_literals():
    """Every ':/' key under BlocksScreen/lib, .py or .ui, resolves to a declared .qrc key."""
    keys = _qrc_keys()
    broken = {
        key: sites
        for key, sites in _literal_sites().items()
        if _canonical(key) not in keys and _canonical(key) not in XFAIL_KEYS
    }
    assert not broken, _report(
        "resource keys that no .qrc declares (Qt renders these blank):", broken
    )


def test_xfail_keys_are_still_broken():
    """XFAIL_KEYS only shrinks: a key that got fixed must be deleted from the dict."""
    keys = _qrc_keys()
    sites = {_canonical(key) for key in _literal_sites()}
    stale = {}
    for key in XFAIL_KEYS:
        if key in keys:
            stale[key] = ["now declared by a .qrc - delete this XFAIL_KEYS entry"]
        elif key not in sites:
            stale[key] = [
                "no longer referenced anywhere - delete this XFAIL_KEYS entry"
            ]
    assert not stale, _report("stale XFAIL_KEYS entries:", stale)


def test_qrc_declared_files_exist_on_disk():
    """Every <file> a .qrc declares is present, so `make rcc` cannot fail silently."""
    missing = {
        key: [str(path.relative_to(REPO_ROOT))]
        for key, path in _qrc_entries()
        if not path.is_file()
    }
    assert not missing, _report("declared in a .qrc but absent from disk:", missing)


def test_compiled_blobs_match_the_qrc_xml():
    """The _rc.py blobs match the .qrc XML, i.e. nobody skipped `make rcc`."""
    declared = _qrc_keys()
    compiled = _compiled_keys()
    drift = {}
    if declared - compiled:
        drift["declared in XML but not compiled (run `make rcc`)"] = sorted(
            declared - compiled
        )
    if compiled - declared:
        drift["compiled but no longer in XML (run `make rcc`)"] = sorted(
            compiled - declared
        )
    assert not drift, _report("the .qrc XML and the _rc.py blobs disagree:", drift)


def test_compiled_blobs_match_the_asset_bytes():
    """The blobs carry the current asset bytes, which the key-set check above cannot see."""
    from PyQt6.QtCore import QFile, QIODevice

    _import_blobs()

    # `make rcc` skips unmodified .qrc, so an edited asset leaves the blob silently stale.
    stale = {}
    for key, path in _qrc_entries():
        handle = QFile(key)
        if not handle.open(QIODevice.OpenModeFlag.ReadOnly):
            stale[key] = ["absent from every compiled blob"]
            continue
        compiled = bytes(handle.readAll())
        handle.close()
        if compiled != path.read_bytes():
            stale[key] = [
                f"{path.relative_to(REPO_ROOT)} changed after the blob was built"
            ]
    assert not stale, _report(
        "assets edited without recompiling the blob (rerun pyrcc5 by hand):", stale
    )


def test_svg_font_families_resolve_exactly(qapp):
    """Every font-family an .svg declares matches a real face, so nothing falls back."""
    from PyQt6.QtGui import QFont, QFontInfo

    from BlocksScreen.lib.utils.fonts import MOMCAKE_FAMILY, register_momcake

    _import_blobs()
    register_momcake.cache_clear()
    assert register_momcake() == MOMCAKE_FAMILY, (
        "the bundled .ttf files no longer file under MOMCAKE_FAMILY; the .svg "
        "assets and lib/utils/fonts.py have to name the same family"
    )

    # Qt logs nothing when it substitutes, so ask it what it actually resolved to.
    fallbacks = {
        family: sites
        for family, sites in _svg_font_families().items()
        if QFontInfo(QFont(family)).family() != family
    }
    assert not fallbacks, _report(
        "font families no loaded face matches (Qt paints these in the system font):",
        fallbacks,
    )
