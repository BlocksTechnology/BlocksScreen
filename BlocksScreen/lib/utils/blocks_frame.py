import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksCustomFrame(QtWidgets.QFrame):
    WHITE = QtGui.QColor("white")

    def __init__(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
        # Constant paint state, the frame styling never varies at runtime
        self._pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        self._pen.setWidth(2)
        self._brush = QtGui.QBrush(QtGui.QColor(50, 50, 50, 100))
        self._font = QtGui.QFont()
        self._font.setPointSize(12)
        self._metrics = QtGui.QFontMetrics(self._font)

    def setRadius(self, radius: int):
        """Set widget frame radius"""
        self._radius = radius
        self.update()

    def setLeftLineWidth(self, width: int):
        """Set widget left line  width"""
        self._left_line_width = width
        self.update()

    def setCentered(self, centered: bool):
        """Set if text is centered or left-aligned"""
        self._is_centered = centered
        self.update()

    def setProperty(self, name: str | None, value: typing.Any) -> bool:
        if name == "text":
            self.text = value
            self.update()
            return True
        return super().setProperty(name, value)

    def paintEvent(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(self.WHITE)
            painter.setFont(self._font)
            fm = self._metrics
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, self.WHITE)
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, self.WHITE)
