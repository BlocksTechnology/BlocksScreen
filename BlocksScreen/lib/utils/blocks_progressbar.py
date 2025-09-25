from PyQt6 import QtWidgets ,QtGui ,QtCore


class CustomProgressBar(QtWidgets.QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self.bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self.set_padding(50)
        self.set_pen_width(20)

    def set_padding(self, value):
        self.padding = value
        self.update()

    def set_pen_width(self, value):
        self.pen_width = value
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        self._draw_circular_bar(painter, self.width(), self.height())

    def _draw_circular_bar(self, painter, width, height):
        size = min(width, height) - (self.padding * 1.3)
        x = (width - size) / 2
        y = (height - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)


        arc1_start = 236* 16  
        arc1_span = -290 * 16  
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self.pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc1_start, arc1_span)

        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)  
            gradient.setColorAt(0.0, self.bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))

            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self.pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)

            # scale only over arc1’s span
            progress_span = int(arc1_span * self.progress_value/100)
            painter.drawArc(arc_rect, arc1_start, progress_span)

        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)

        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)

        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()

        # Draw centered text
        text_rect = QtCore.QRectF(text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40)
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)


            

    def setValue(self, value):
        value*=100
        if 0 <= value <= 101:
            self.progress_value = value
            self.update()
        else:
            raise ValueError("Progress must be between 0.0 and 1.0.")

    def set_bar_color(self, red, green, blue):
        if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
            self.bar_color = QtGui.QColor(red, green, blue)
            self.update()
        else:
            raise ValueError("Color values must be between 0 and 255.")
