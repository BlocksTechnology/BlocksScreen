"""Repo-wide guard against the double-free bug class in panels/.

Adding one widget/spacer/layout object to two layouts (or twice to one) double-
frees it when the panel is destroyed -> SIGBUS. This statically scans every
panel for that antipattern; see tools/check_layout_double_add.py and
tests/widgets/test_basic_filament_panel.py for the concrete case it caught.
"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "tools"))

from check_layout_double_add import find_double_adds  # noqa: E402


def test_no_double_added_layout_items():
    panels = _ROOT / "BlocksScreen" / "lib" / "panels"
    files = [str(p) for p in sorted(panels.rglob("*.py"))]
    findings = find_double_adds(files)
    assert not findings, (
        "double-added layout items (double-free on destroy):\n"
        + "\n".join(f"  {f}::{fn} '{k}' @ lines {a},{b}" for f, fn, k, a, b in findings)
    )
