import typing
from PyQt6 import QtCore, QtGui, QtWidgets


class GroupButton(QtWidgets.QPushButton):
    """Custom Blocks QPushButton
        Rounded button with a hole on the left side where an icon can be inserted

    Args:
        parent (QWidget): Parent of the button
    """

    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super(GroupButton, self).__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._icon_rect: QtCore.QRectF = QtCore.QRectF()
        self.button_background = None
        self.button_ellipse = None
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(0, 0, 0)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def name(self):
        """Widget name"""
        return self._name

    @name.setter
    def name(self, new_name) -> None:
        self._name = new_name
        self.setObjectName(new_name)

    def text(self) -> str | None:
        """Widget text"""
        return self._text

    def setText(self, text: str) -> None:
        """Set widget text"""
        self._text = text
        self.update()  # Force button update
        return

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = pixmap
        self.repaint()

    def paintEvent(self, e: typing.Optional[QtGui.QPaintEvent]):
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

        bg_color = (
            QtGui.QColor(223, 223, 223)
            if self.isChecked()
            else QtGui.QColor(164, 164, 164, 90)
            if self.isDown()
            else QtGui.QColor(0, 0, 0, 90)
        )

        path = QtGui.QPainterPath()
        xRadius = self.rect().toRectF().normalized().height() / 5.0
        yRadius = self.rect().toRectF().normalized().height() / 5.0
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        path.addRoundedRect(
            0,
            0,
            self.rect().toRectF().normalized().width(),
            self.rect().toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        self.button_ellipse = QtCore.QRectF(
            self.rect().toRectF().normalized().left()
            + self.rect().toRectF().normalized().height() * 0.05,
            self.rect().toRectF().normalized().top()
            + self.rect().toRectF().normalized().height() * 0.05,
            (self.rect().toRectF().normalized().height() * 0.40),
            (self.rect().toRectF().normalized().height() * 0.40),
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            if self.isChecked():
                painter.setPen(QtGui.QColor(0, 0, 0))
            else:
                painter.setPen(QtGui.QColor(255, 255, 255))
            _start_text_position = int(self.button_ellipse.width() / 2)
            _text_rect = _rect
            _pen = painter.pen()
            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            _pen.setWidth(1)
            painter.setPen(_pen)
            painter.setFont(QtGui.QFont("Momcake-Thin", 14))

            painter.drawText(
                _text_rect,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )
            painter.setPen(QtCore.Qt.PenStyle.NoPen)

    def setProperty(self, name: str, value: typing.Any):
        """Re-implemented method, set widget properties"""
        if name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = QtGui.QColor(value)
        # return super().setProperty(name, value)

    def event(self, e: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
        if e.type() == QtCore.QEvent.Type.TouchBegin:
            self.handleTouchBegin(e)
            return False
        elif e.type() == QtCore.QEvent.Type.TouchUpdate:
            self.handleTouchUpdate(e)
            return False
        elif e.type() == QtCore.QEvent.Type.TouchEnd:
            self.handleTouchEnd(e)
            return False
        elif e.type() == QtCore.QEvent.Type.TouchCancel:
            self.handleTouchCancel(e)
            return False
        return super().event(e)
