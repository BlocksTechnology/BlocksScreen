import qrcode
from PIL import ImageQt

BLOCKS_URL = "https://blockstec.com"
RF50_MANUAL_PAGE = "https://blockstec.com/RF50"
RF50_PRODUCT_PAGE = "https://blockstec.com/rf-50"
RF50_DATASHEET_PAGE = "https://www.blockstec.com/assets/downloads/rf50_datasheet.pdf"
RF50_USER_MANUAL_PAGE = "https://blockstec.com/assets/files/rf50_user_manual.pdf"


def make_qrcode(data) -> ImageQt.ImageQt:
    """Generate a QR code image from *data* and return it as a Qt-compatible image."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    pil_image = img.get_image()
    return ImageQt.toqimage(pil_image)


_NM_TO_WIFI_QR_AUTH: dict[str, str] = {
    "wpa-psk": "WPA",
    "wpa2-psk": "WPA",
    "sae": "WPA",
    "wep": "WEP",
    "open": "nopass",
    "nopass": "nopass",
    "owe": "nopass",
}


def generate_wifi_qrcode(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> ImageQt.ImageQt:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)
