import typing
from PyQt6 import QtCore, QtGui, QtWidgets


class IconButton(QtWidgets.QPushButton):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223,70)  # Set to solid white
    @property
    def name(self):
        """Widget name"""
        return self._name

    def text(self) -> str:
        """Widget text"""
        return self._text

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = pixmap
        self.repaint()

    def setText(self, text: str) -> None:
        """Set widget text"""
        self._text = text
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(2.5, 2.5, (self.width() - 5 ), (self.height() - 5 - y))
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
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

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine
                | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def setProperty(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)
