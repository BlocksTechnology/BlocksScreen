"""Every user-facing 'contact support' text must carry the support address."""

from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SUPPORT = "support@blockstec.com"


def test_contact_support_carries_address() -> None:
    bad = [
        f"{path.relative_to(_REPO)}:{n}"
        for root in ("BlocksScreen", "updater")
        for path in sorted((_REPO / root).rglob("*.py"))
        if not path.name.endswith("_rc.py")
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if "contact support" in line.lower() and _SUPPORT not in line
    ]
    assert not bad, f"lack {_SUPPORT}: {bad}"
