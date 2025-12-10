import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class NumpadButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._position: str = ""

    def get_position(self):
        """Get numpad button position"""
        return self._position

    def set_position(self, value):
        """Set position"""
        self._position = str(value).lower()

    def paintEvent(self, e: QtGui.QPaintEvent | None):
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        _rect = self.rect()
        _style = self.style()

        if _style is None or _rect is None:
            return
        margin = _style.pixelMetric(_style.PixelMetric.PM_ButtonMargin, opt, self)
        bg_color = (
            QtGui.QColor(164, 164, 164)
            if self.isDown()
            else QtGui.QColor(223, 223, 223)
        )

        path = QtGui.QPainterPath()
        xRadius = self.rect().toRectF().normalized().height() / 2.0
        yRadius = self.rect().toRectF().normalized().height() / 2.0
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        if self._position == "left":
            path.addRect(
                0 + self.rect().toRectF().normalized().height(),
                0,
                self.rect().toRectF().normalized().width(),
                self.rect().toRectF().normalized().height(),
            )
            painter.fillPath(path, bg_color)

            path.addRoundedRect(
                0,
                0,
                self.rect().toRectF().normalized().width(),
                self.rect().toRectF().normalized().height(),
                xRadius,
                yRadius,
                QtCore.Qt.SizeMode.AbsoluteSize,
            )
            painter.fillPath(path, bg_color)
        elif self._position == "right":
            path.addRect(
                0,
                0,
                self.rect().toRectF().normalized().width() / 2,
                self.rect().toRectF().normalized().height(),
            )
            painter.fillPath(path, bg_color)

            path.addRoundedRect(
                0,
                0,
                self.rect().toRectF().normalized().width(),
                self.rect().toRectF().normalized().height(),
                xRadius,
                yRadius,
                QtCore.Qt.SizeMode.AbsoluteSize,
            )
            painter.fillPath(path, bg_color)

        elif self._position == "down":
            path.addRoundedRect(
                0,
                0,
                self.rect().toRectF().normalized().width(),
                self.rect().toRectF().normalized().height(),
                xRadius,
                yRadius,
                QtCore.Qt.SizeMode.AbsoluteSize,
            )
            painter.fillPath(path, bg_color)

        else:
            path.addRect(
                0,
                0,
                self.rect().toRectF().normalized().width(),
                self.rect().toRectF().normalized().height(),
            )
            painter.fillPath(path, bg_color)
        icon_path = QtGui.QPainterPath()

        self.button_ellipse = QtCore.QRectF(
            self.rect().toRectF().normalized().left()
            + self.rect().toRectF().normalized().height() * 0.05,
            self.rect().toRectF().normalized().top()
            + self.rect().toRectF().normalized().height() * 0.05,
            (self.rect().toRectF().normalized().height() * 0.90),
            (self.rect().toRectF().normalized().height() * 0.90),
        )
        icon_path.addEllipse(self.button_ellipse)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)

        # Draw Icon
        _parent_rect = self.button_ellipse.toRect()
        _icon_rect = QtCore.QRectF(
            _parent_rect.left() * 2.8,
            _parent_rect.top() * 2.8,
            _parent_rect.width() * 0.80,
            _parent_rect.height() * 0.80,
        )

        if self.text():
            _start_text_position = int(self.button_ellipse.right())
            _rect.setLeft(_start_text_position + margin)
            _pen = painter.pen()
            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            _pen.setWidth(1)
            _pen.setColor(QtGui.QColor(0, 0, 0))
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
