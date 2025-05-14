import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class DisplayButton(QtWidgets.QPushButton):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.highlight_color = "#2AC9F9"
        self.text_formatting: str = ""
        self._text: str = ""
        self._secondary_text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(0, 0, 0)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def name(self):
        return self._name

    def text(self) -> str:
        return self._text

    def secondary_text(self) -> str:
        return self._secondary_text

    def setText(self, text: str) -> None:
        self._text = text
        self.update()
        super().setText(text)

    def set_secondary_text(self, text: str) -> None:
        self._secondary_text = text
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        return super().resizeEvent(a0)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        return super().mousePressEvent(e)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)
        _rect = self.rect()
        _style = self.style()

        if not _style or _rect is None:
            return
        margin = _style.pixelMetric(
            _style.PixelMetric.PM_ButtonMargin, opt, self
        )
        # Rounded background edges
        path = QtGui.QPainterPath()
        path.addRoundedRect(
            self.rect().toRectF(),
            10.0,
            10.0,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.fillPath(path, QtGui.QColor(177, 196, 203, 75))
        painter.setPen(QtCore.Qt.PenStyle.SolidLine)
        painter.setPen(QtCore.Qt.GlobalColor.white)
        if self.underMouse():
            _pen = QtGui.QPen()
            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            _pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
            _pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            _color = QtGui.QColor(self.highlight_color)
            _color2 = QtGui.QColor(self.highlight_color)
            _color3 = QtGui.QColor(self.highlight_color)
            _color.setAlpha(40)
            _color2.setAlpha(35)
            _color3.setAlpha(1)
            _pen.setColor(_color)
            _gradient = QtGui.QRadialGradient(
                QtCore.QPointF(
                    self.rect().toRectF().left() + 2,
                    self.rect().toRectF().top(),
                ),
                150.0,
                self.rect().toRectF().center(),
            )
            _gradient.setColorAt(0, _color)
            _gradient.setColorAt(0.5, _color2)
            _gradient.setColorAt(1, _color3)
            _pen.setBrush(_gradient)
            painter.fillPath(path, _pen.brush())

        _icon_rect = (
            QtCore.QRectF(  # x,y, width * size reduction factor, height
                0.0,
                0.0,
                (_rect.width() * 0.3) - 5.0,
                _rect.height() - 5,
            )
        )

        _icon_scaled = self.icon_pixmap.scaled(
            int(_icon_rect.width()),
            int(_icon_rect.height()),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

        # Calculate the actual QRect for the scaled pixmap (centering it if needed)
        scaled_width = _icon_scaled.width()
        scaled_height = _icon_scaled.height()

        adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
        adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
        adjusted_icon_rect = QtCore.QRectF(
            _icon_rect.x() + adjusted_x,
            _icon_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )

        painter.drawPixmap(
            adjusted_icon_rect,  # Target area (center adjusted)
            _icon_scaled,  # Scaled pixmap
            _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
        )

        if _rect is not None and self.text() is not None:
            _ptl_rect = None
            _stl_rect = None
            _mtl = QtCore.QRectF(
                int(_icon_rect.width()) + margin,
                0.0,
                int(_rect.width() - _icon_rect.width() - margin),
                _rect.height(),
            )
            if "secondary" in self.button_type:
                _ptl_rect = QtCore.QRectF(
                    int(_mtl.left()),
                    0.0,
                    int((_mtl.width() / 2.0) - 5),
                    _rect.height(),
                )
                _mtl_rect = QtCore.QRectF(
                    int(_ptl_rect.right()), 0.0, 10, _rect.height()
                )
                _stl_rect = QtCore.QRectF(
                    int(_mtl.center().x() + 3.0),
                    0.0,
                    int(_mtl.width() / 2.0),
                    _rect.height(),
                )
                painter.drawText(
                    _ptl_rect,
                    QtCore.Qt.TextFlag.TextShowMnemonic
                    | QtCore.Qt.AlignmentFlag.AlignHCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    str(self.text()) if self.text() is not None else str("?"),
                )
                painter.drawText(
                    _stl_rect,
                    QtCore.Qt.TextFlag.TextShowMnemonic
                    | QtCore.Qt.AlignmentFlag.AlignHCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    str(self.secondary_text())
                    if self.secondary_text() is not None
                    else str("?"),
                )
                painter.drawText(
                    _mtl_rect,
                    QtCore.Qt.TextFlag.TextShowMnemonic
                    | QtCore.Qt.AlignmentFlag.AlignHCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    str("/"),
                )
            else:
                painter.drawText(
                    _mtl,
                    QtCore.Qt.TextFlag.TextShowMnemonic
                    | QtCore.Qt.AlignmentFlag.AlignHCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    str(self.text()) if self.text() is not None else str("?"),
                )
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.end()
        return

    def setProperty(self, name: str, value: typing.Any) -> bool:
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "button_type":
            self.button_type = value

        return super().setProperty(name, value)
