"""Guards Qt resource keys: Qt renders an unknown ':/' key blank, silently."""

import importlib
import re
from collections import Counter
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG_ROOT = REPO_ROOT / "BlocksScreen"
RESOURCES = PKG_ROOT / "lib" / "ui" / "resources"
RC_PACKAGE = "BlocksScreen.lib.ui.resources"

# Known-broken keys; may only shrink, enforced by the stale-entry test.
XFAIL_KEYS: dict[str, str] = {}

# Text scan, not AST: AST misses f-strings; '/?' also matches ':ui/...'.
# Spaces admit 'fonts for text/...'; a folder-less key needs an extension, and
# a ':', '%' or '/' after the prefix rejects '::1/128', ':/%s/%s' and '://'.
_LITERAL = re.compile(
    r'["\'](:/?(?:[^"\'\s:%/][^"\']*/[^"\']*'
    r'|[\w.-][\w .-]*\.[A-Za-z][A-Za-z0-9]{1,4}))["\']'
)


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
                name = element.get("alias") or path
                # A prefix-less <qresource> roots its files at ':/' itself.
                key = f":/{prefix}/{name}" if prefix else f":/{name}"
                entries.append((key, qrc.parent / path))
    return entries


def _qrc_keys() -> set[str]:
    """Return the resource keys declared by the .qrc XML."""
    return {key for key, _ in _qrc_entries()}


def _literal_sites() -> dict[str, list[str]]:
    """Map every ':/' literal under BlocksScreen/lib to its 'file:line' call sites."""
    sites: dict[str, list[str]] = {}
    for module in sorted((PKG_ROOT / "lib").rglob("*.py")):
        if module.name.endswith("_rc.py"):
            continue
        text = module.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            for match in _LITERAL.finditer(line):
                where = f"{module.relative_to(REPO_ROOT)}:{number}"
                sites.setdefault(match.group(1), []).append(where)
    return sites


def _qrc_prefix_roots() -> set[str]:
    """Return the top-level ':/<folder>' roots of the .qrc keys that have a folder."""
    return {f":/{key.split('/')[1]}" for key in _qrc_keys() if key.count("/") > 1}


def _import_blobs() -> None:
    """Import every _rc.py, which registers its resources into Qt's tree."""
    for blob in sorted(RESOURCES.glob("*_rc.py")):
        importlib.import_module(f"{RC_PACKAGE}.{blob.stem}")


def _compiled_keys() -> set[str]:
    """Return the resource keys compiled into the _rc.py blobs, our prefixes only."""
    from PyQt6.QtCore import QDir, QDirIterator, QFile

    _import_blobs()

    # Skip walking ':/': Qt's own resources land there, import-order dependent.
    keys = {key for key in _qrc_keys() if key.count("/") == 1 and QFile.exists(key)}
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
    """Fail loudly if path derivation breaks, so the other tests cannot pass empty."""
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
        drift["declared in XML but not compiled (run `make rcc-all`)"] = sorted(
            declared - compiled
        )
    if compiled - declared:
        drift["compiled but no longer in XML (run `make rcc-all`)"] = sorted(
            compiled - declared
        )
    assert not drift, _report("the .qrc XML and the _rc.py blobs disagree:", drift)


def test_compiled_blobs_match_the_asset_bytes():
    """The blobs carry the current asset bytes, which the key-set check cannot see."""
    from PyQt6.QtCore import QFile, QIODevice

    _import_blobs()
    # `make rcc` skips unchanged .qrc files, so an edited asset keeps a stale blob.
    entries = _qrc_entries()
    counts = Counter(key for key, _ in entries)
    stale = {}
    for key, path in entries:
        # A recompile cannot fix a duplicate; test_no_duplicate_qrc_keys reports it.
        if counts[key] > 1:
            continue
        handle = QFile(key)
        if not handle.open(QIODevice.OpenModeFlag.ReadOnly):
            stale[key] = ["absent from every compiled blob"]
            continue
        compiled = bytes(handle.readAll())
        handle.close()
        # A missing file is test_qrc_declared_files_exist_on_disk's to report.
        if path.is_file() and compiled != path.read_bytes():
            stale[key] = [
                f"{path.relative_to(REPO_ROOT)} changed after the blob was built"
                " (run `make rcc-all`)"
            ]
    assert not stale, _report("assets edited without recompiling the blob:", stale)


def test_no_duplicate_qrc_keys():
    """No key is declared twice, since Qt then serves one file and hides the other."""
    seen: dict[str, list[str]] = {}
    for key, path in _qrc_entries():
        seen.setdefault(key, []).append(str(path.relative_to(REPO_ROOT)))
    dupes = {key: paths for key, paths in seen.items() if len(paths) > 1}
    assert not dupes, _report("resource keys declared more than once:", dupes)


def test_literal_scanner_shapes():
    """The scanner keeps folder-less keys and drops IPv6 and format-string lookalikes."""
    found = [
        m.group(1)
        for m in _LITERAL.finditer(
            "\":/logo.svg\" ':/a b/c.svg' \"::1/128\" ':%s/%s' \": %s\" ':ui/x.png'"
            ' ":/%s/%s" "://" ":/font.woff2" ":/my logo.svg" ": a.b"'
        )
    ]
    assert found == [
        ":/logo.svg",
        ":/a b/c.svg",
        ":ui/x.png",
        ":/font.woff2",
        ":/my logo.svg",
    ]


def test_folder_less_keys_are_not_walked_as_roots(monkeypatch):
    """A prefix-less ':/logo.svg' is a file, so only foldered keys yield walk roots."""
    module = importlib.import_module(__name__)
    monkeypatch.setattr(module, "_qrc_keys", lambda: {":/a/b.svg", ":/top.svg"})
    assert _qrc_prefix_roots() == {":/a"}
