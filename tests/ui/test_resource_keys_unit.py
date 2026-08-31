"""Guards Qt resource keys: no broken ':/' literal, no stale compiled blob.

Qt resolves an unknown ':/' key to a null QPixmap with no exception, no warning
and no log line. The only feedback is a blank rectangle on the panel, which is
how the keys in XFAIL_KEYS survived for months. These tests turn that silent
failure into a red test.
"""

import importlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG_ROOT = REPO_ROOT / "BlocksScreen"
RESOURCES = PKG_ROOT / "lib" / "ui" / "resources"
RC_PACKAGE = "BlocksScreen.lib.ui.resources"

# Known-broken keys, measured 2026-08-31. This dict may only ever shrink:
# test_xfail_keys_are_still_broken fails once an entry stops being broken.
XFAIL_KEYS = {
    ":/background/media/graphics/scroll_list_window.svg": (
        "asset is on disk but declared by no .qrc; retired by PR 3"
    ),
    ":/button_borders/media/btn_icons/back.svg": (
        "wrong prefix, real key is :/ui/media/btn_icons/back.svg; "
        "lives in a generated _ui.py so the .ui file is the fix; retired by PR 3"
    ),
    ":/graphics/media/btn_icons/z_offset_adjust.svg": (
        "asset deleted from the qrc in 927e43c (2025-06-04) and absent from "
        "disk, yet 3 call sites still request it; retired by PR 3"
    ),
    ":/network/media/btn_icons/network/{b}bar_wifi{": (
        "not broken at runtime: an f-string template the scanner cannot "
        "evaluate, whose real keys are the 0bar..3bar matrix; the literal "
        "disappears when the Icon enum replaces it in PR 8"
    ),
    ":/ui/background/media/1st_background.png": (
        "duplicated prefix segment, real key is "
        ":/background/media/1st_background.png; retired by PR 3"
    ),
    ":/ui/media/btn_icons/indf_svg.svg": (
        "no such file in any .qrc or on disk; retired by PR 3"
    ),
    ":/ui/media/btn_icons/warning.svg": (
        "no such file in any .qrc or on disk, so the warning popup renders a "
        "blank icon; needs a new asset, not just a key fix; retired by PR 3"
    ),
}

# Deliberately a text scan, not an AST walk: an AST walk only sees ast.Constant,
# so it would silently drop the wifi f-string template above. The optional slash
# catches ":ui/..." too, which Qt resolves the same as ":/ui/..." (verified) and
# which 6 sites in this package use. The trailing + excludes a bare ":".
_LITERAL = re.compile(r'["\'](:/?[^"\'\s]+)["\']')


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
    """Map every ':/' literal under BlocksScreen/lib to its 'file:line' call sites."""
    sites: dict[str, list[str]] = {}
    for module in sorted((PKG_ROOT / "lib").rglob("*.py")):
        if module.name.endswith("_rc.py"):
            continue
        text = module.read_text(errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            for match in _LITERAL.finditer(line):
                where = f"{module.relative_to(REPO_ROOT)}:{number}"
                sites.setdefault(match.group(1), []).append(where)
    return sites


def _qrc_prefix_roots() -> set[str]:
    """Return the top-level ':/<prefix>' roots the .qrc files claim."""
    return {f":/{key.split('/')[1]}" for key in _qrc_keys()}


def _compiled_keys() -> set[str]:
    """Return the resource keys compiled into the _rc.py blobs, under our prefixes only."""
    from PyQt6.QtCore import QDir, QDirIterator

    for blob in sorted(RESOURCES.glob("*_rc.py")):
        importlib.import_module(f"{RC_PACKAGE}.{blob.stem}")

    # Walk our own prefixes, never ':/'. Qt registers its own style and PDF
    # resources into the same tree as soon as QtGui/QtWidgets is imported, and
    # which of those appear depends on what the rest of the suite imported first.
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
    """Every ':/' literal under BlocksScreen/lib resolves to a declared .qrc key."""
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
