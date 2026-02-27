"""Unit tests for BlocksScreen.lib.qrcode_gen."""

import sys
from types import ModuleType
from unittest.mock import MagicMock, patch

import pytest

# PIL and qrcode are not available in the test environment; stub them before
# the module under test is imported.
_pil_stub = ModuleType("PIL")
_pil_stub.ImageQt = MagicMock()  # type: ignore[attr-defined]
sys.modules.setdefault("PIL", _pil_stub)
sys.modules.setdefault("PIL.ImageQt", _pil_stub.ImageQt)

_qrcode_stub = MagicMock()
sys.modules.setdefault("qrcode", _qrcode_stub)

from BlocksScreen.lib.qrcode_gen import generate_wifi_qrcode  # noqa: E402


@pytest.fixture(autouse=True)
def _patch_make_qrcode():
    """Patch make_qrcode so tests do not exercise the QR library."""
    with patch(
        "BlocksScreen.lib.qrcode_gen.make_qrcode", return_value=MagicMock()
    ) as mock:
        yield mock


@pytest.mark.unit
@pytest.mark.parametrize(
    "nm_type,expected_qr_auth",
    [
        ("wpa-psk", "WPA"),
        ("WPA-PSK", "WPA"),  # case folding
        ("wpa2-psk", "WPA"),
        ("sae", "WPA"),
        ("wep", "WEP"),
        ("open", "nopass"),
        ("nopass", "nopass"),
        ("owe", "nopass"),
        ("unknown-future-type", "WPA"),  # fallback for unknown types
    ],
)
def test_auth_type_normalization(nm_type, expected_qr_auth, _patch_make_qrcode):
    """NM auth strings must be normalized to WiFi QR standard values."""
    generate_wifi_qrcode("Net", "pass", nm_type)
    data = _patch_make_qrcode.call_args[0][0]
    assert f"T:{expected_qr_auth};" in data


@pytest.mark.unit
def test_wifi_data_format(_patch_make_qrcode):
    """QR string must follow WIFI:T:...;S:...;P:...;H:...;; format."""
    generate_wifi_qrcode("MySSID", "secret", "wpa-psk", hidden=True)
    data = _patch_make_qrcode.call_args[0][0]
    assert data == "WIFI:T:WPA;S:MySSID;P:secret;H:true;;"


@pytest.mark.unit
def test_hidden_defaults_to_false(_patch_make_qrcode):
    """hidden parameter defaults to False."""
    generate_wifi_qrcode("Net", "pass", "wpa-psk")
    data = _patch_make_qrcode.call_args[0][0]
    assert "H:false" in data
