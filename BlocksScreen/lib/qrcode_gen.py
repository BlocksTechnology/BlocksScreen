import qrcode

from PyQt6.QtGui import QImage, QColor, QPainter
from PyQt6.QtCore import Qt

BLOCKS_URL = "https://blockstec.com"
RF50_MANUAL_PAGE = "https://blockstec.com/RF50"
RF50_PRODUCT_PAGE = "https://blockstec.com/rf-50"
RF50_DATASHEET_PAGE = "https://www.blockstec.com/assets/downloads/rf50_datasheet.pdf"
RF50_USER_MANUAL_PAGE = "https://blockstec.com/assets/files/rf50_user_manual.pdf"


def make_qrcode(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    box_size = 10
    size = len(matrix) * box_size

    image = QImage(size, size, QImage.Format.Format_RGB32)
    image.fill(QColor("white"))

    painter = QPainter(image)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("black"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


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
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)
