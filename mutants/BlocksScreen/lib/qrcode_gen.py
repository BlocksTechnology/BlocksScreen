import qrcode

from PyQt6.QtGui import QImage, QColor, QPainter
from PyQt6.QtCore import Qt

BLOCKS_URL = "https://blockstec.com"
RF50_MANUAL_PAGE = "https://blockstec.com/RF50"
RF50_PRODUCT_PAGE = "https://blockstec.com/rf-50"
RF50_DATASHEET_PAGE = "https://www.blockstec.com/assets/downloads/rf50_datasheet.pdf"
RF50_USER_MANUAL_PAGE = "https://blockstec.com/assets/files/rf50_user_manual.pdf"
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def make_qrcode(data: str) -> QImage:
    args = [data]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_make_qrcode__mutmut_orig, x_make_qrcode__mutmut_mutants, args, kwargs, None)


def x_make_qrcode__mutmut_orig(data: str) -> QImage:
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


def x_make_qrcode__mutmut_1(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = None
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


def x_make_qrcode__mutmut_2(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=None,
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


def x_make_qrcode__mutmut_3(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=None,
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


def x_make_qrcode__mutmut_4(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=None,
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


def x_make_qrcode__mutmut_5(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=None,
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


def x_make_qrcode__mutmut_6(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
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


def x_make_qrcode__mutmut_7(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
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


def x_make_qrcode__mutmut_8(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
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


def x_make_qrcode__mutmut_9(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
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


def x_make_qrcode__mutmut_10(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=2,
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


def x_make_qrcode__mutmut_11(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=11,
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


def x_make_qrcode__mutmut_12(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=5,
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


def x_make_qrcode__mutmut_13(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(None)
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


def x_make_qrcode__mutmut_14(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=None)

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


def x_make_qrcode__mutmut_15(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=False)

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


def x_make_qrcode__mutmut_16(data: str) -> QImage:
    """Generate a QR code image from *data* and return it as a QImage."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    matrix = None
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


def x_make_qrcode__mutmut_17(data: str) -> QImage:
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
    box_size = None
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


def x_make_qrcode__mutmut_18(data: str) -> QImage:
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
    box_size = 11
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


def x_make_qrcode__mutmut_19(data: str) -> QImage:
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
    size = None

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


def x_make_qrcode__mutmut_20(data: str) -> QImage:
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
    size = len(matrix) / box_size

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


def x_make_qrcode__mutmut_21(data: str) -> QImage:
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

    image = None
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


def x_make_qrcode__mutmut_22(data: str) -> QImage:
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

    image = QImage(None, size, QImage.Format.Format_RGB32)
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


def x_make_qrcode__mutmut_23(data: str) -> QImage:
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

    image = QImage(size, None, QImage.Format.Format_RGB32)
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


def x_make_qrcode__mutmut_24(data: str) -> QImage:
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

    image = QImage(size, size, None)
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


def x_make_qrcode__mutmut_25(data: str) -> QImage:
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

    image = QImage(size, QImage.Format.Format_RGB32)
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


def x_make_qrcode__mutmut_26(data: str) -> QImage:
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

    image = QImage(size, QImage.Format.Format_RGB32)
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


def x_make_qrcode__mutmut_27(data: str) -> QImage:
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

    image = QImage(size, size, )
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


def x_make_qrcode__mutmut_28(data: str) -> QImage:
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
    image.fill(None)

    painter = QPainter(image)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("black"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_29(data: str) -> QImage:
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
    image.fill(QColor(None))

    painter = QPainter(image)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("black"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_30(data: str) -> QImage:
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
    image.fill(QColor("XXwhiteXX"))

    painter = QPainter(image)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("black"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_31(data: str) -> QImage:
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
    image.fill(QColor("WHITE"))

    painter = QPainter(image)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("black"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_32(data: str) -> QImage:
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

    painter = None
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("black"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_33(data: str) -> QImage:
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

    painter = QPainter(None)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("black"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_34(data: str) -> QImage:
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
    painter.setPen(None)
    painter.setBrush(QColor("black"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_35(data: str) -> QImage:
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
    painter.setBrush(None)

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_36(data: str) -> QImage:
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
    painter.setBrush(QColor(None))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_37(data: str) -> QImage:
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
    painter.setBrush(QColor("XXblackXX"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_38(data: str) -> QImage:
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
    painter.setBrush(QColor("BLACK"))

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_39(data: str) -> QImage:
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

    for y, row in enumerate(None):
        for x, cell in enumerate(row):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_40(data: str) -> QImage:
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
        for x, cell in enumerate(None):
            if cell:
                painter.drawRect(x * box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_41(data: str) -> QImage:
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
                painter.drawRect(None, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_42(data: str) -> QImage:
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
                painter.drawRect(x * box_size, None, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_43(data: str) -> QImage:
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
                painter.drawRect(x * box_size, y * box_size, None, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_44(data: str) -> QImage:
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
                painter.drawRect(x * box_size, y * box_size, box_size, None)

    painter.end()
    return image


def x_make_qrcode__mutmut_45(data: str) -> QImage:
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
                painter.drawRect(y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_46(data: str) -> QImage:
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
                painter.drawRect(x * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_47(data: str) -> QImage:
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
                painter.drawRect(x * box_size, y * box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_48(data: str) -> QImage:
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
                painter.drawRect(x * box_size, y * box_size, box_size, )

    painter.end()
    return image


def x_make_qrcode__mutmut_49(data: str) -> QImage:
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
                painter.drawRect(x / box_size, y * box_size, box_size, box_size)

    painter.end()
    return image


def x_make_qrcode__mutmut_50(data: str) -> QImage:
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
                painter.drawRect(x * box_size, y / box_size, box_size, box_size)

    painter.end()
    return image

x_make_qrcode__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_make_qrcode__mutmut_1': x_make_qrcode__mutmut_1, 
    'x_make_qrcode__mutmut_2': x_make_qrcode__mutmut_2, 
    'x_make_qrcode__mutmut_3': x_make_qrcode__mutmut_3, 
    'x_make_qrcode__mutmut_4': x_make_qrcode__mutmut_4, 
    'x_make_qrcode__mutmut_5': x_make_qrcode__mutmut_5, 
    'x_make_qrcode__mutmut_6': x_make_qrcode__mutmut_6, 
    'x_make_qrcode__mutmut_7': x_make_qrcode__mutmut_7, 
    'x_make_qrcode__mutmut_8': x_make_qrcode__mutmut_8, 
    'x_make_qrcode__mutmut_9': x_make_qrcode__mutmut_9, 
    'x_make_qrcode__mutmut_10': x_make_qrcode__mutmut_10, 
    'x_make_qrcode__mutmut_11': x_make_qrcode__mutmut_11, 
    'x_make_qrcode__mutmut_12': x_make_qrcode__mutmut_12, 
    'x_make_qrcode__mutmut_13': x_make_qrcode__mutmut_13, 
    'x_make_qrcode__mutmut_14': x_make_qrcode__mutmut_14, 
    'x_make_qrcode__mutmut_15': x_make_qrcode__mutmut_15, 
    'x_make_qrcode__mutmut_16': x_make_qrcode__mutmut_16, 
    'x_make_qrcode__mutmut_17': x_make_qrcode__mutmut_17, 
    'x_make_qrcode__mutmut_18': x_make_qrcode__mutmut_18, 
    'x_make_qrcode__mutmut_19': x_make_qrcode__mutmut_19, 
    'x_make_qrcode__mutmut_20': x_make_qrcode__mutmut_20, 
    'x_make_qrcode__mutmut_21': x_make_qrcode__mutmut_21, 
    'x_make_qrcode__mutmut_22': x_make_qrcode__mutmut_22, 
    'x_make_qrcode__mutmut_23': x_make_qrcode__mutmut_23, 
    'x_make_qrcode__mutmut_24': x_make_qrcode__mutmut_24, 
    'x_make_qrcode__mutmut_25': x_make_qrcode__mutmut_25, 
    'x_make_qrcode__mutmut_26': x_make_qrcode__mutmut_26, 
    'x_make_qrcode__mutmut_27': x_make_qrcode__mutmut_27, 
    'x_make_qrcode__mutmut_28': x_make_qrcode__mutmut_28, 
    'x_make_qrcode__mutmut_29': x_make_qrcode__mutmut_29, 
    'x_make_qrcode__mutmut_30': x_make_qrcode__mutmut_30, 
    'x_make_qrcode__mutmut_31': x_make_qrcode__mutmut_31, 
    'x_make_qrcode__mutmut_32': x_make_qrcode__mutmut_32, 
    'x_make_qrcode__mutmut_33': x_make_qrcode__mutmut_33, 
    'x_make_qrcode__mutmut_34': x_make_qrcode__mutmut_34, 
    'x_make_qrcode__mutmut_35': x_make_qrcode__mutmut_35, 
    'x_make_qrcode__mutmut_36': x_make_qrcode__mutmut_36, 
    'x_make_qrcode__mutmut_37': x_make_qrcode__mutmut_37, 
    'x_make_qrcode__mutmut_38': x_make_qrcode__mutmut_38, 
    'x_make_qrcode__mutmut_39': x_make_qrcode__mutmut_39, 
    'x_make_qrcode__mutmut_40': x_make_qrcode__mutmut_40, 
    'x_make_qrcode__mutmut_41': x_make_qrcode__mutmut_41, 
    'x_make_qrcode__mutmut_42': x_make_qrcode__mutmut_42, 
    'x_make_qrcode__mutmut_43': x_make_qrcode__mutmut_43, 
    'x_make_qrcode__mutmut_44': x_make_qrcode__mutmut_44, 
    'x_make_qrcode__mutmut_45': x_make_qrcode__mutmut_45, 
    'x_make_qrcode__mutmut_46': x_make_qrcode__mutmut_46, 
    'x_make_qrcode__mutmut_47': x_make_qrcode__mutmut_47, 
    'x_make_qrcode__mutmut_48': x_make_qrcode__mutmut_48, 
    'x_make_qrcode__mutmut_49': x_make_qrcode__mutmut_49, 
    'x_make_qrcode__mutmut_50': x_make_qrcode__mutmut_50
}
x_make_qrcode__mutmut_orig.__name__ = 'x_make_qrcode'


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
    args = [ssid, password, auth_type, hidden]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_generate_wifi_qrcode__mutmut_orig, x_generate_wifi_qrcode__mutmut_mutants, args, kwargs, None)


def x_generate_wifi_qrcode__mutmut_orig(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_1(
    ssid: str, password: str, auth_type: str, hidden: bool = True
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_2(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = None
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_3(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(None, "WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_4(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), None)
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_5(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get("WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_6(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), )
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_7(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.upper(), "WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_8(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "XXWPAXX")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_9(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "wpa")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_10(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "WPA")
    wifi_data = None
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_11(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).upper()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_12(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(None).lower()};;"
    return make_qrcode(wifi_data)


def x_generate_wifi_qrcode__mutmut_13(
    ssid: str, password: str, auth_type: str, hidden: bool = False
) -> QImage:
    """Build a Wi-Fi QR code for the given SSID/password/auth combination.

    *auth_type* is a NetworkManager key-mgmt value (e.g. ``"wpa-psk"``,
    ``"sae"``).  Unknown values default to WPA.
    """
    qr_auth = _NM_TO_WIFI_QR_AUTH.get(auth_type.lower(), "WPA")
    wifi_data = f"WIFI:T:{qr_auth};S:{ssid};P:{password};H:{str(hidden).lower()};;"
    return make_qrcode(None)

x_generate_wifi_qrcode__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_generate_wifi_qrcode__mutmut_1': x_generate_wifi_qrcode__mutmut_1, 
    'x_generate_wifi_qrcode__mutmut_2': x_generate_wifi_qrcode__mutmut_2, 
    'x_generate_wifi_qrcode__mutmut_3': x_generate_wifi_qrcode__mutmut_3, 
    'x_generate_wifi_qrcode__mutmut_4': x_generate_wifi_qrcode__mutmut_4, 
    'x_generate_wifi_qrcode__mutmut_5': x_generate_wifi_qrcode__mutmut_5, 
    'x_generate_wifi_qrcode__mutmut_6': x_generate_wifi_qrcode__mutmut_6, 
    'x_generate_wifi_qrcode__mutmut_7': x_generate_wifi_qrcode__mutmut_7, 
    'x_generate_wifi_qrcode__mutmut_8': x_generate_wifi_qrcode__mutmut_8, 
    'x_generate_wifi_qrcode__mutmut_9': x_generate_wifi_qrcode__mutmut_9, 
    'x_generate_wifi_qrcode__mutmut_10': x_generate_wifi_qrcode__mutmut_10, 
    'x_generate_wifi_qrcode__mutmut_11': x_generate_wifi_qrcode__mutmut_11, 
    'x_generate_wifi_qrcode__mutmut_12': x_generate_wifi_qrcode__mutmut_12, 
    'x_generate_wifi_qrcode__mutmut_13': x_generate_wifi_qrcode__mutmut_13
}
x_generate_wifi_qrcode__mutmut_orig.__name__ = 'x_generate_wifi_qrcode'
