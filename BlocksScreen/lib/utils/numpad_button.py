import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class NumpadButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._position: str = ""
        self.button_ellipse: QtCore.QRectF = QtCore.QRectF()
        # Paint caches, invalidated on resize and position change
        self._path: QtGui.QPainterPath | None = None
        self._margin: int = -1
        self._down_color = QtGui.QColor(164, 164, 164)
        self._up_color = QtGui.QColor(223, 223, 223)
        self._text_color = QtGui.QColor(0, 0, 0)

    def get_position(self):
        """Get numpad button position"""
        return self._position

    def set_position(self, value):
        """Set position"""
        self._position = str(value).lower()
        self._path = None
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, drop every size-dependent cache"""
        self._path = None
        self._margin = -1
        super().resizeEvent(a0)

    def _shape(self, rect_f: QtCore.QRectF) -> QtGui.QPainterPath:
        """Cached background path, winding fill so subpaths union instead of cancel"""
        if self._path is not None:
            return self._path
        width = rect_f.width()
        height = rect_f.height()
        radius = height / 2.0
        path = QtGui.QPainterPath()
        path.setFillRule(QtCore.Qt.FillRule.WindingFill)
        if self._position == "left":
            path.addRect(height, 0, width, height)
            path.addRoundedRect(
                0, 0, width, height, radius, radius, QtCore.Qt.SizeMode.AbsoluteSize
            )
        elif self._position == "right":
            path.addRect(0, 0, width / 2, height)
            path.addRoundedRect(
                0, 0, width, height, radius, radius, QtCore.Qt.SizeMode.AbsoluteSize
            )
        elif self._position == "down":
            path.addRoundedRect(
                0, 0, width, height, radius, radius, QtCore.Qt.SizeMode.AbsoluteSize
            )
        else:
            path.addRect(0, 0, width, height)
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            height * 0.90,
            height * 0.90,
        )
        self._path = path
        return path

    def paintEvent(self, e: QtGui.QPaintEvent | None):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)

        _rect = self.rect()
        _style = self.style()

        if _style is None or _rect is None:
            return
        bg_color = self._down_color if self.isDown() else self._up_color

        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.fillPath(self._shape(_rect.toRectF().normalized()), bg_color)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)

        if self.text():
            if self._margin < 0:
                opt = QtWidgets.QStyleOptionButton()
                self.initStyleOption(opt)
                self._margin = _style.pixelMetric(
                    _style.PixelMetric.PM_ButtonMargin, opt, self
                )
            _rect.setLeft(int(self.button_ellipse.right()) + self._margin)
            _pen = painter.pen()
            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            _pen.setWidth(1)
            _pen.setColor(self._text_color)
            painter.setPen(_pen)

            painter.drawText(
                _rect,
                QtCore.Qt.TextFlag.TextShowMnemonic
                | QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                str(self.text()),
            )
            painter.setPen(QtCore.Qt.PenStyle.NoPen)

    def setProperty(self, name: str, value: typing.Any):
        """Re-implemented method, set widget properties"""
        if name == "position":
            self.set_position(value)

        return super().setProperty(name, value)
