from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor
from PyQt6.QtCore import QRectF


class BlocksCustomFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._radius = 20

    def setRadius(self, radius: int):
        """Set widget frame radius"""
        self._radius = radius
        self.update()

    def radius(self):
        """Get widget frame radius"""
        return self._radius

    def paintEvent(self, event):
        """Re-implemented method, paint widget"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect())
        pen = QPen(QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)
