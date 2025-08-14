from PyQt6 import QtCore, QtGui, QtWidgets


class LoadScreen(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True

        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(16)

        self.setupUI()

    def setupUI(self) -> None:
        self.setObjectName("LoadScreen")
        # self.setStyleSheet("background-color: #e0e0e0;")

        self.label = QtWidgets.QLabel("Test", self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def _update_animation(self) -> None:
        self._angle = (self._angle + 5) % 360

        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True

        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.TextAntialiasing, True)

        pen = QtGui.QPen()
        pen.setWidth(5)
        pen.setColor(QtGui.QColor("#ffffff"))
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        center_x = self.width() // 2
        center_y = int(self.height() * 0.4)
        arc_size = 150

        painter.translate(center_x, center_y)
        painter.rotate(self._angle)

        arc_rect = QtCore.QRectF(
            -arc_size / 2, -arc_size / 2, arc_size, arc_size
        )

        start_angle = 0
        span_angle = int(self._span_angle * 16)
        painter.drawArc(arc_rect, start_angle, span_angle)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)

        label_width = 500
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        self.label.setGeometry(label_x, label_y, label_width, label_height)

    def set_status_message(self, message: str) -> None:
        self.label.setText(message)
