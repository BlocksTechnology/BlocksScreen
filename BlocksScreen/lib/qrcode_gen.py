import qrcode
from PIL import ImageQt

BLOCKS_URL = "https://blockstec.com"
RF50_MANUAL_PAGE = "https://blockstec.com/RF50"
RF50_PRODUCT_PAGE = "https://blockstec.com/rf-50"
RF50_DATASHEET_PAGE = (
    "https://www.blockstec.com/assets/downloads/rf50_datasheet.pdf"
)
RF50_DATASHEET_PAGE = "https://blockstec.com/assets/files/rf50_user_manual.pdf"


def make_qrcode(data) -> ImageQt.ImageQt:
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
    pil_image.show()
    return pil_image.toqimage()


def generate_wifi_qrcode(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> ImageQt.ImageQt:
    wifi_data = f"WIFI:T:{auth_type};S:{ssid};P:{password};{'H:true;' if hidden else ''};"
    return make_qrcode(wifi_data)
