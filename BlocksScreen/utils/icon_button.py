import typing
from PyQt6 import QtCore, QtGui, QtWidgets


class IconButton(QtWidgets.QPushButton):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def name(self):
        return self._name

    def text(self) -> str:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text
        self.update()
        super().setText(text)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        # bg_color = (
        #     QtGui.QColor(164, 164, 164)
        #     if self.isDown()
        #     else QtGui.QColor(223, 223, 223)
        # )

        # * Build icon
        x = y = 15.0 if self.text_formatting else 5.0
        _icon_rect = QtCore.QRectF(
            0.0, 0.0, (self.width() - x), (self.height() - y)
        )

        _icon_scaled = self.icon_pixmap.scaled(
            _icon_rect.size().toSize(),
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
                adjusted_x = (_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine
                | QtCore.Qt.AlignmentFlag.AlignHCenter
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                str(self.text()),
            )
            painter.setPen(QtCore.Qt.PenStyle.NoPen)

        painter.end()

    def setProperty(self, name: str, value: typing.Any) -> bool:
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
