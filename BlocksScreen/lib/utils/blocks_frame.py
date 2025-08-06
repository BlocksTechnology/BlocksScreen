from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import QRectF


class BlocksCustomFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._radius = 10

    def setRadius(self, radius: int):
        self._radius = radius
        self.update()

    def radius(self):
        return self._radius

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        pen = QPen(QColor(190, 190, 190, 50))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(84, 84, 84, 0)))
        painter.drawRoundedRect(
            rect.adjusted(1, 1, -1, -1), self._radius, self._radius
        )
