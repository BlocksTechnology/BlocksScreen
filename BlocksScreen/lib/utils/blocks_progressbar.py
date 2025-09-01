from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QConicalGradient, QBrush
from PyQt6 import QtWidgets


class CustomProgressBar(QtWidgets.QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0.0
        self.bar_color = QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self.set_padding(20)
        self.set_pen_width(15)

    def set_padding(self, value):
        self.padding = value
        self.update()

    def set_pen_width(self, value):
        self.pen_width = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self._draw_circular_bar(painter, self.width(), self.height())

    def _draw_circular_bar(self, painter, width, height):
        size = min(width, height) - (self.padding * 2)
        x = (width - size) / 2
        y = (height - size) / 2
        arc_rect = QRectF(x, y, size, size)

        # Draw the background circle (the "track")
        bg_pen = QPen(QColor(40, 40, 40))  # A darker color for the background
        bg_pen.setWidth(self.pen_width)
        bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(arc_rect)

        # Draw the progress arc with a gradient
        if self.progress_value > 0:
            # Create a conical gradient for the progress arc
            gradient = QConicalGradient(arc_rect.center(), 90)
            gradient.setColorAt(0, self.bar_color)  # Start color
            gradient.setColorAt(1, QColor(224, 225, 225))  # End color

            # Create the pen for the progress arc and set its brush to the gradient
            progress_pen = QPen()
            progress_pen.setWidth(self.pen_width)
            progress_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QBrush(gradient))

            painter.setPen(progress_pen)

            start_angle = 90 * 16
            span_angle = int(self.progress_value * -360 * 16)
            painter.drawArc(arc_rect, start_angle, span_angle)

    def setValue(self, value):
        if 0.0 <= value <= 1.0:
            self.progress_value = value
            self.update()
        else:
            raise ValueError("Progress must be between 0.0 and 1.0.")

    def set_style(self, style):
        if style in ["round", "line"]:
            self.style = style
            self.update()
        else:
            raise ValueError("Invalid style. Must be 'round' or 'line'.")

    def set_bar_color(self, red, green, blue):
        if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
            self.bar_color = QColor(red, green, blue)
            self.update()
        else:
            raise ValueError("Color values must be between 0 and 255.")
