import typing
from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksCustomCheckButton(QtWidgets.QAbstractButton):
    """Custom Blocks QPushButton
        Rounded button with a hole on the left side where an icon can be inserted

    Args:
        parent (QWidget): Parent of the button
    """

    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = None
        self._text: str = ""
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    def setFlat(self, flat) -> None:
        """Disable setFlat behavior"""
        return

    def setAutoDefault(self, _):
        """Disable auto default behavior"""
        return
    def text(self) -> str :
        """returns Widget text"""
        return self._text

    def setText(self, text: str|None) -> None:
        """Set widget text"""
        if text is None:
            return
        self._text = text
        self.update()
        return

    def paintEvent(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,  
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )
