import typing

from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_label import BlocksLabel
from lib.utils.blocks_slider import BlocksSlider
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class _ColorWheel(QtWidgets.QWidget):
    """Circular HSV hue/saturation picker."""

    hue_sat_changed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        float, float, name="hue_sat_changed"
    )

    _PADDING = 4

    def __init__(
        self, parent: QtWidgets.QWidget | None = None, diameter: int = 256
    ) -> None:
        super().__init__(parent)
        self._diameter = diameter
        self._hue = 0.0
        self._sat = 0.0
        self._wheel_img: QtGui.QImage | None = None
        self._selector = QtCore.QPointF(diameter / 2.0, diameter / 2.0)
        self.setFixedSize(diameter, diameter)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self._build_image()

    def _build_image(self) -> None:
        s = self._diameter
        img = QtGui.QImage(s, s, QtGui.QImage.Format.Format_ARGB32_Premultiplied)

        painter = QtGui.QPainter(img)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        center_x = s / 2.0
        center_y = s / 2.0
        radious = s / 2.0 - 4

        hue_grad = QtGui.QConicalGradient(center_x, center_y, 0.0)
        for i in range(361):
            hue_grad.setColorAt(i / 360.0, QtGui.QColor.fromHsvF(i / 360.0, 1.0, 1.0))
        painter.setBrush(QtGui.QBrush(hue_grad))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawEllipse(
            QtCore.QRectF(
                center_x - radious, center_y - radious, radious * 2, radious * 2
            )
        )

        sat_grad = QtGui.QRadialGradient(center_x, center_y, radious)
        sat_grad.setColorAt(0.0, QtGui.QColor(255, 255, 255, 255))
        sat_grad.setColorAt(1.0, QtGui.QColor(255, 255, 255, 0))
        painter.setBrush(QtGui.QBrush(sat_grad))
        painter.drawEllipse(
            QtCore.QRectF(
                center_x - radious, center_y - radious, radious * 2, radious * 2
            )
        )
        painter.end()

        self._wheel_img = img
        self._radius = radious
        self._center_x = center_x
        self._center_y = center_y

    def set_color(self, hue: float, sat: float) -> None:
        self._hue = hue
        self._sat = sat
        offset = QtCore.QLineF.fromPolar(self._radius * sat, hue)
        self._selector = QtCore.QPointF(
            self._center_x + offset.dx(), self._center_y + offset.dy()
        )
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        if self._wheel_img:
            painter.drawImage(0, 0, self._wheel_img)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 1.5))
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawEllipse(self._selector, 11, 11)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 2.5))
        painter.drawEllipse(self._selector, 9, 9)
        painter.end()

    def _pick(self, pos: QtCore.QPointF) -> None:
        dx = pos.x() - self._center_x
        dy = pos.y() - self._center_y
        dist = QtCore.QLineF(QtCore.QPointF(), QtCore.QPointF(dx, dy)).length()
        clamped = min(dist, self._radius)
        self._hue = QtCore.QLineF(0, 0, dx, dy).angle()
        self._sat = clamped / self._radius
        if dist > 0:
            scale = clamped / dist
            self._selector = QtCore.QPointF(
                self._center_x + dx * scale, self._center_y + dy * scale
            )
        else:
            self._selector = QtCore.QPointF(self._center_x, self._center_y)
        self.update()
        self.hue_sat_changed.emit(self._hue, self._sat)

    # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #     self._pick(event.position())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() & QtCore.Qt.MouseButton.LeftButton:
            self._pick(event.position())


class ColorWheelWidget(QtWidgets.QWidget):
    color_selected: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="color_selected"
    )
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self._hue = 0.0
        self._sat = 1.0
        self._val = 1.0
        self._build_ui()
        self._sync_all()

    def set_color(self, color: QtGui.QColor) -> None:
        """Pre-select a colour before showing the page."""
        h, s, v, _ = color.getHsvF()
        self._hue = h * 360.0 if h >= 0 else 0.0
        self._sat = max(0.0, s)
        self._val = max(0.0, v)
        self._sync_all()

    def set_color_hex(self, hex_str: str) -> None:
        """Pre-select a colour from a hex string like ``'ff5733'``."""
        self.set_color(QtGui.QColor(f"#{hex_str.lstrip('#')}"))

    def _current_color(self) -> QtGui.QColor:
        return QtGui.QColor.fromHsvF(self._hue / 360.0, self._sat, self._val)

    def _sync_all(self) -> None:
        color = self._current_color()
        full_color = QtGui.QColor.fromHsvF(self._hue / 360.0, self._sat, 1.0)

        self._wheel.set_color(self._hue, self._sat)

        self._brightness_slider.highlight_color = full_color.name()
        self._brightness_slider.blockSignals(True)
        self._brightness_slider.setValue(int(self._val * 100))
        self._brightness_slider.blockSignals(False)
        self._brightness_slider.update()

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(0, 0, 0, 0))
        self._swatch.setPalette(palette)
        self._swatch.background_color = color
        self._swatch.rounded = True
        self._swatch.setText(f"#{color.name().lstrip('#').upper()}")
        self._swatch.update()

    def _on_hue_sat(self, hue: float, sat: float) -> None:
        self._hue = hue
        self._sat = sat
        self._sync_all()

    def _on_brightness(self, value: int) -> None:
        self._val = value / 100.0
        self._sync_all()

    def _on_select(self) -> None:
        self.color_selected.emit(self._current_color().name().lstrip("#"))
        self.request_back.emit()

    def _build_ui(self) -> None:
        def _pal(color: str | QtGui.QColor) -> QtGui.QPalette:
            p = QtGui.QPalette()
            p.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(0, 0, 0, 0))
            p.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor(color))
            return p

        def _lbl(
            text: str,
            pt: int,
            color: str | QtGui.QColor,
            parent: QtWidgets.QWidget,
            height: int = 24,
        ) -> BlocksLabel:
            lbl = BlocksLabel(parent)
            lbl.setText(text)
            f = QtGui.QFont()
            f.setPointSize(pt)
            lbl.setFont(f)
            lbl.setFixedHeight(height)
            lbl.setPalette(_pal(color))
            return lbl

        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(800, 480))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 8)
        root.setSpacing(8)

        # ── Header ──────────────────────────────────────────────────────
        header = QtWidgets.QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)

        spacer = QtWidgets.QWidget(self)
        spacer.setFixedSize(60, 60)
        header.addWidget(spacer)

        title = _lbl("Color Picker", 22, "#FFFFFF", self, height=60)
        title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        header.addWidget(title, 1)

        back_btn = IconButton(self)
        back_btn.setFixedSize(60, 60)
        back_btn.setFlat(True)
        back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        back_btn.clicked.connect(self.request_back)
        header.addWidget(back_btn)
        root.addLayout(header)

        # ── Body ─────────────────────────────────────────────────────────
        body = QtWidgets.QHBoxLayout()
        body.setSpacing(16)

        # Left: colour wheel, vertically centred
        self._wheel = _ColorWheel(self, diameter=260)
        self._wheel.hue_sat_changed.connect(self._on_hue_sat)
        body.addWidget(self._wheel, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        # Right: card containing all controls
        card = BlocksCustomFrame(self)
        card_lay = QtWidgets.QVBoxLayout(card)
        card_lay.setContentsMargins(14, 14, 14, 14)
        card_lay.setSpacing(10)

        # Combined swatch + hex code — one element instead of two
        self._swatch = BlocksLabel(card)
        self._swatch.setFixedHeight(76)
        self._swatch.rounded = True
        self._swatch.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        swatch_font = QtGui.QFont()
        swatch_font.setFamily("Momcake-Bold")
        swatch_font.setPointSize(20)
        self._swatch.setFont(swatch_font)
        card_lay.addWidget(self._swatch)

        # Brightness row
        card_lay.addWidget(
            _lbl("Brightness", 22, QtGui.QColor(160, 160, 160), card, 30)
        )

        self._brightness_slider = BlocksSlider(card)
        self._brightness_slider.setMinimum(0)
        self._brightness_slider.setMaximum(100)
        self._brightness_slider.valueChanged.connect(self._on_brightness)
        card_lay.addWidget(self._brightness_slider)

        card_lay.addStretch(1)

        select_btn = BlocksCustomButton(card)
        select_btn.setFixedSize(200, 70)
        f = QtGui.QFont()
        f.setPointSize(16)
        select_btn.setFont(f)
        select_btn.setText("Select")
        select_btn.clicked.connect(self._on_select)
        card_lay.addWidget(select_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        body.addWidget(card, 1)
        root.addLayout(body, 1)
