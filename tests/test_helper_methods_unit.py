"""helper_methods.parse_materials edge cases."""

import importlib.util
from pathlib import Path

import pytest

# Some conftests stub helper_methods, so load the real file under a private name.
_hm_path = Path(__file__).resolve().parents[1] / "BlocksScreen/helper_methods.py"
_spec = importlib.util.spec_from_file_location("_real_helper_methods", _hm_path)
_hm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hm)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("PLA", ["PLA"]),
        ("PLA, PETG,PLA", ["PLA", "PETG"]),
        ("PLA;PETG;PLA", ["PLA", "PETG"]),
        ('["PLA", "PETG", "PLA"]', ["PLA", "PETG"]),
        (["PLA", None, "PLA"], ["PLA"]),
        ("[1, null]", ["1"]),
        ("[bad", ["[bad"]),
        ('["Unknown", "Unknown"]', []),
        ("Unknown", []),
        ("", []),
        (None, []),
    ],
)
def test_parse_materials(raw, expected):
    assert _hm.parse_materials(raw) == expected
