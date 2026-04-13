"""Widget test configuration.

Ensures ``BlocksScreen/`` is on sys.path so ``from lib.xxx`` imports
resolve correctly, and clears any empty ``lib.*`` stub packages that
the network conftest may have registered before this directory is loaded.
"""

import sys
from pathlib import Path

_bs_dir = Path(__file__).resolve().parent.parent.parent / "BlocksScreen"
if str(_bs_dir) not in sys.path:
    sys.path.insert(0, str(_bs_dir))

# The network conftest registers empty namespace stubs for lib, lib.panels,
# lib.panels.widgets, and lib.utils. Clear them so the real packages
# from _bs_dir are importable.
for _pkg in ("lib", "lib.panels", "lib.panels.widgets", "lib.utils"):
    mod = sys.modules.get(_pkg)
    if mod is not None and not getattr(mod, "__file__", None):
        del sys.modules[_pkg]
