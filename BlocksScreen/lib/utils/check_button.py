from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksCustomCheckButton(QtWidgets.QAbstractButton):
    """Custom Blocks QPushButton
        Rounded button with a hole on the left side where an icon can be inserted

    Args:
        parent (QWidget): Parent of the button
    """

    CHECKED_BG = QtGui.QColor(223, 223, 223)
    CHECKED_TEXT = QtGui.QColor(0, 0, 0)
    DOWN_BG = QtGui.QColor(164, 164, 164, 90)
    IDLE_BG = QtGui.QColor(0, 0, 0, 90)
    IDLE_TEXT = QtGui.QColor(255, 255, 255)

    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self._text: str = ""
        self.font = QtGui.QFont("Momcake", 14)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self._path: QtGui.QPainterPath | None = None

    def setFlat(self, flat) -> None:
        """Disable setFlat behavior"""
        return

    def setAutoDefault(self, _):
        """Disable auto default behavior"""
        return

    def text(self) -> str:
        """returns Widget text"""
        return self._text

    def setFont(self, font: QtGui.QFont):
        self.font = font
        self.update()

    def setText(self, text: str | None) -> None:
        """Set widget text"""
        if text is None:
            return
        self._text = text
        self.update()
        return

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, drop the cached background path"""
        self._path = None
        super().resizeEvent(a0)

    def paintEvent(self, e: QtGui.QPaintEvent | None):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)

        if self.isChecked():
            bg_color = self.CHECKED_BG
            text_color = self.CHECKED_TEXT
        elif self.isDown():
            bg_color = self.DOWN_BG
            text_color = self.IDLE_TEXT
        else:
            bg_color = self.IDLE_BG
            text_color = self.IDLE_TEXT

        if self._path is None:
            radius = rect_f.height() / 5.0
            path = QtGui.QPainterPath()
            path.addRoundedRect(
                rect_f,
                radius,
                radius,
                QtCore.Qt.SizeMode.AbsoluteSize,
            )
            self._path = path

        # fillPath takes its brush as an argument and never strokes, no pen/brush needed
        painter.fillPath(self._path, bg_color)

        if self._text:
            painter.setPen(text_color)
            painter.setFont(self.font)
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                self._text,
            )
