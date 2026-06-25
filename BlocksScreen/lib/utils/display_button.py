import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class DisplayButton(QtWidgets.QPushButton):
    def __init__(self, parent: typing.Optional["QtWidgets.QWidget"] = None) -> None:
        if parent:
            super().__init__(parent=parent)
        else:
            super().__init__()

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.icon_pixmap_secondary: QtGui.QPixmap = QtGui.QPixmap()
        self.highlight_color = "#2AC9F9"
        self._button_type: typing.Literal["display", "display_secondary"] = "display"
        self.display_format: typing.Literal["normal", "upper_downer", "dual"] = "normal"
        self.text_formatting: str = ""
        self._text: str = ""
        self._secondary_text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(0, 0, 0)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self._path_cache: dict[tuple[int, int], QtGui.QPainterPath] = {}
        self._icon_cache: QtGui.QPixmap = QtGui.QPixmap()
        self._icon_cache_size: QtCore.QSize = QtCore.QSize()
        self._icon_secondary_cache: QtGui.QPixmap = QtGui.QPixmap()
        self._icon_secondary_cache_size: QtCore.QSize = QtCore.QSize()
        self._font_cache: dict[int, QtGui.QFont] = {}
        self._color_bg = QtGui.QColor(177, 196, 203, 75)
        self._color_secondary_text = QtGui.QColor("#b6b0b0")
        _hc = QtGui.QColor(self.highlight_color)
        self._highlight_c1 = QtGui.QColor(_hc)
        self._highlight_c1.setAlpha(40)
        self._highlight_c2 = QtGui.QColor(_hc)
        self._highlight_c2.setAlpha(35)
        self._highlight_c3 = QtGui.QColor(_hc)
        self._highlight_c3.setAlpha(1)

    @property
    def name(self):
        """Widget name"""
        return self._name

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = pixmap
        self._icon_cache = QtGui.QPixmap()
        self._icon_cache_size = QtCore.QSize()
        self.repaint()

    def setSecondaryPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set secondary widget pixmap"""
        self.icon_pixmap_secondary = pixmap
        self._icon_secondary_cache = QtGui.QPixmap()
        self._icon_secondary_cache_size = QtCore.QSize()
        self.repaint()

    def _get_font(self, point_size: int) -> QtGui.QFont:
        cached = self._font_cache.get(point_size)
        if cached is None:
            f = QtGui.QFont()
            f.setPointSize(point_size)
            f.setFamily("Momcake-bold")
            self._font_cache[point_size] = cached = f
        return cached

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

    def setSecondaryText(self, text: str) -> None:
        """Set widget secondary text"""
        self._secondary_text = text
        self.update()

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

        _rect = self.rect()
        _style = self.style()

        if not _style or _rect is None:
            return
        margin = _style.pixelMetric(_style.PixelMetric.PM_ButtonMargin, opt, self)
        path_key = (_rect.width(), _rect.height())
        path = self._path_cache.get(path_key)
        if path is None:
            path = QtGui.QPainterPath()
            path.addRoundedRect(
                _rect.toRectF(), 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            self._path_cache[path_key] = path

        painter.fillPath(path, self._color_bg)
        painter.setPen(QtCore.Qt.PenStyle.SolidLine)
        painter.setPen(QtCore.Qt.GlobalColor.white)

        if self.underMouse():
            _pen = QtGui.QPen()
            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            _pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
            _pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            _pen.setColor(self._highlight_c1)
            _rect_f = _rect.toRectF()
            _gradient = QtGui.QRadialGradient(
                QtCore.QPointF(_rect_f.left() + 2, _rect_f.top()),
                150.0,
                _rect_f.center(),
            )
            _gradient.setColorAt(0, self._highlight_c1)
            _gradient.setColorAt(0.5, self._highlight_c2)
            _gradient.setColorAt(1, self._highlight_c3)
            _pen.setBrush(_gradient)
            painter.fillPath(path, _pen.brush())

        _skip_main_icon = (
            "secondary" in self._button_type and self.display_format == "dual"
        )

        if not _skip_main_icon:
            _icon_rect = QtCore.QRectF(
                0.0,
                0.0,
                (_rect.width() * 0.3) - 5.0,
                _rect.height() - 5,
            )

            target_size = QtCore.QSize(
                int(_icon_rect.width()), int(_icon_rect.height())
            )
            if target_size != self._icon_cache_size:
                self._icon_cache = self.icon_pixmap.scaled(
                    target_size,
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
                self._icon_cache_size = target_size
            _icon_scaled = self._icon_cache

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
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, 0.0, 0.0)

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
                    painter.setFont(self._get_font(12))
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
                        _mtl.width() - margin * 2.0,
                        (_mtl.height() * 0.7) // 2,
                    )
                    _downer_rect = QtCore.QRectF(
                        _mtl.left() + margin,
                        (_upper_rect.bottom() + margin + 5),
                        _mtl.width() - margin * 2,
                        (_mtl.height() * 0.5) // 2,
                    )
                    painter.setFont(self._get_font(20))
                    painter.setCompositionMode(
                        painter.CompositionMode.CompositionMode_SourceAtop
                    )
                    _ = painter.drawText(
                        _upper_rect,
                        QtCore.Qt.AlignmentFlag.AlignRight
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        self.text(),
                    )
                    painter.setPen(self._color_secondary_text)
                    painter.setFont(self._get_font(14))

                    _ = painter.drawText(
                        _downer_rect,
                        QtCore.Qt.AlignmentFlag.AlignRight
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        self.secondary_text,
                    )
                elif self.display_format == "dual":
                    #
                    #  _____________________________________
                    # | <primary icon> ------ primary value |
                    # |         -------------------         |
                    # | <second. icon> ------ second. value |
                    # |_____________________________________|
                    #

                    _icon_size = min(_rect.height() * 0.5, _rect.width() * 0.20) - 4.0
                    _row_height = _rect.height() / 2.0
                    _margin = 5.0

                    _first_icon_rect = QtCore.QRectF(
                        _margin,
                        (_row_height - _icon_size) / 2.0,  # vertically centred in row 1
                        _icon_size,
                        _icon_size,
                    )
                    _dual_icon_size = QtCore.QSize(int(_icon_size), int(_icon_size))
                    if _dual_icon_size != self._icon_cache_size:
                        self._icon_cache = self.icon_pixmap.scaled(
                            _dual_icon_size,
                            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                            QtCore.Qt.TransformationMode.SmoothTransformation,
                        )
                        self._icon_cache_size = _dual_icon_size
                    _first_icon_scaled = self._icon_cache
                    _first_adjusted_icon_rect = QtCore.QRectF(
                        _first_icon_rect.x()
                        + (_icon_size - _first_icon_scaled.width()) / 2.0,
                        _first_icon_rect.y()
                        + (_icon_size - _first_icon_scaled.height()) / 2.0,
                        _first_icon_scaled.width(),
                        _first_icon_scaled.height(),
                    )
                    painter.drawPixmap(
                        _first_adjusted_icon_rect,
                        _first_icon_scaled,
                        _first_icon_scaled.rect().toRectF(),
                    )

                    _first_text_rect = QtCore.QRectF(
                        _margin + _icon_size + _margin,  # starts right after the icon
                        0.0,  # top of row 1
                        _rect.width() - _icon_size - _margin * 3,
                        _row_height,
                    )
                    painter.setFont(self._get_font(20))
                    painter.drawText(
                        _first_text_rect,
                        QtCore.Qt.TextFlag.TextShowMnemonic
                        | QtCore.Qt.AlignmentFlag.AlignRight
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str(self.text()) if self.text() else "?",
                    )
                    _second_icon_rect = QtCore.QRectF(
                        _margin,
                        _row_height
                        + (_row_height - _icon_size)
                        / 2.0,  # vertically centred in row 2
                        _icon_size,
                        _icon_size,
                    )
                    if _dual_icon_size != self._icon_secondary_cache_size:
                        self._icon_secondary_cache = self.icon_pixmap_secondary.scaled(
                            _dual_icon_size,
                            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                            QtCore.Qt.TransformationMode.SmoothTransformation,
                        )
                        self._icon_secondary_cache_size = _dual_icon_size
                    _second_icon_scaled = self._icon_secondary_cache
                    _second_adjusted_icon_rect = QtCore.QRectF(
                        _second_icon_rect.x()
                        + (_icon_size - _second_icon_scaled.width()) / 2.0,
                        _second_icon_rect.y()
                        + (_icon_size - _second_icon_scaled.height()) / 2.0,
                        _second_icon_scaled.width(),
                        _second_icon_scaled.height(),
                    )
                    painter.drawPixmap(
                        _second_adjusted_icon_rect,
                        _second_icon_scaled,
                        _second_icon_scaled.rect().toRectF(),
                    )
                    _second_text_rect = QtCore.QRectF(
                        _margin + _icon_size + _margin,
                        _row_height,  # top of row 2
                        _rect.width() - _icon_size - _margin * 3,
                        _row_height,
                    )
                    painter.setPen(self._color_secondary_text)
                    painter.setFont(self._get_font(15))
                    painter.drawText(
                        _second_text_rect,
                        QtCore.Qt.TextFlag.TextShowMnemonic
                        | QtCore.Qt.AlignmentFlag.AlignRight
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str(self.secondary_text) if self.secondary_text else "?",
                    )
            else:
                painter.setFont(self._get_font(12))
                _ = painter.drawText(
                    _mtl,
                    QtCore.Qt.TextFlag.TextShowMnemonic
                    | QtCore.Qt.AlignmentFlag.AlignHCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    str(self.text()) if self.text() else str("?"),
                )
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
        _ = painter.end()
        return

    def setProperty(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        if name == "secondary_pixmap":
            self.icon_pixmap_secondary = value
        elif name == "button_type":
            self._button_type = value
        elif name == "display_format":
            self.display_format = value

        return super().setProperty(name, value)
