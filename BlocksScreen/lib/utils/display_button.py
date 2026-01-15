import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class DisplayButton(QtWidgets.QPushButton):
    def __init__(self, parent: typing.Optional["QtWidgets.QWidget"] = None) -> None:
        if parent:
            super().__init__(parent=parent)
        else:
            super().__init__()

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.highlight_color = "#2AC9F9"
        self._button_type = "display"
        self.text_formatting: str = ""
        self._text: str = ""
        self._secondary_text: str = ""
        self._name: str = ""
        self.display_format: typing.Literal["normal", "upper_downer"] = "normal"
        self.text_color: QtGui.QColor = QtGui.QColor(0, 0, 0)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def name(self):
        """Widget name"""
        return self._name

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = pixmap
        self.repaint()

    @property
    def button_type(self) -> str:
        """Widget button type"""
        return self._button_type

    @button_type.setter
    def button_type(self, type) -> None:
        if type not in ("display", "display_secondary"):
            return
        self._button_type = type

    def text(self) -> str:
        """Widget text"""
        return self._text

    def setText(self, text: str) -> None:
        """Set widget text"""
        self._text = text
        self.update()
        super().setText(text)

    @property
    def secondary_text(self) -> str:
        """Widget secondary text"""
        return self._secondary_text

    @secondary_text.setter
    def secondary_text(self, text: str) -> None:
        """Set secondary text"""
        self._secondary_text = text
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
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
        margin = _style.pixelMetric(_style.PixelMetric.PM_ButtonMargin, opt, self)
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

        _icon_rect = QtCore.QRectF(  # x,y, width * size reduction factor, height
            0.0,
            0.0,
            (_rect.width() * 0.3) - 5.0,
            _rect.height() - 5,
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

        if _rect is not None and self.text():
            _ptl_rect = None
            _stl_rect = None
            _mtl = QtCore.QRectF(
                int(_icon_rect.width()) + margin,
                0.0,
                int(_rect.width() - _icon_rect.width() - margin),
                _rect.height(),
            )
            if "secondary" in self._button_type:
                if self.display_format == "normal":
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
                    font = QtGui.QFont()
                    font.setPointSize(12)
                    font.setFamily("Momcake-bold")
                    painter.setFont(font)
                    painter.drawText(
                        _ptl_rect,
                        QtCore.Qt.TextFlag.TextShowMnemonic
                        | QtCore.Qt.AlignmentFlag.AlignHCenter
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str(self.text()) if self.text() else str("?"),
                    )
                    painter.drawText(
                        _stl_rect,
                        QtCore.Qt.TextFlag.TextShowMnemonic
                        | QtCore.Qt.AlignmentFlag.AlignHCenter
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str(self.secondary_text) if self.secondary_text else str("?"),
                    )
                    painter.drawText(
                        _mtl_rect,
                        QtCore.Qt.TextFlag.TextShowMnemonic
                        | QtCore.Qt.AlignmentFlag.AlignHCenter
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str("/"),
                    )
                elif self.display_format == "upper_downer":
                    _mtl = QtCore.QRectF(
                        int(_icon_rect.width()) + margin,
                        0.0,
                        int(_rect.width() - _icon_rect.width() - margin),
                        _rect.height(),
                    )
                    _upper_rect = QtCore.QRectF(
                        _mtl.left() + margin,
                        _mtl.top() + margin,
                        _mtl.width() - margin * 2,
                        (_mtl.height() * 0.7) // 2,
                    )
                    _downer_rect = QtCore.QRectF(
                        _mtl.left() + margin,
                        (_upper_rect.bottom() + margin + 5),
                        _mtl.width() - margin * 2,
                        (_mtl.height() * 0.5) // 2,
                    )
                    font = QtGui.QFont()
                    font.setPointSize(20)
                    font.setFamily("Momcake-bold")
                    painter.setFont(font)
                    painter.setCompositionMode(
                        painter.CompositionMode.CompositionMode_SourceAtop
                    )
                    painter.drawText(
                        _upper_rect,
                        # QtCore.Qt.AlignmentFlag.AlignCenter,
                        QtCore.Qt.AlignmentFlag.AlignRight
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        self.text(),
                    )
                    font.setPointSize(15)
                    painter.setPen(QtGui.QColor("#b6b0b0"))
                    painter.setFont(font)

                    painter.drawText(
                        _downer_rect,
                        QtCore.Qt.AlignmentFlag.AlignRight
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        self.secondary_text,
                    )

            else:
                font = QtGui.QFont()
                font.setPointSize(12)
                font.setFamily("Momcake-bold")
                painter.setFont(font)
                painter.drawText(
                    _mtl,
                    QtCore.Qt.TextFlag.TextShowMnemonic
                    | QtCore.Qt.AlignmentFlag.AlignHCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    str(self.text()) if self.text() else str("?"),
                )
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.end()
        return

    def setProperty(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "button_type":
            self._button_type = value

        return super().setProperty(name, value)
