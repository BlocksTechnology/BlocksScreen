
from PyQt6 import QtCore, QtGui, QtWidgets


class LoadingOverlayWidget(QtWidgets.QLabel): 
    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self.setupUI()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(16)
        self.label.setText("Loading...")
        self.repaint()

    def set_status_message(self, message: str) -> None:
        self.label.setText(message)


    def close(self) -> bool:
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        return super().close()

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


    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(
            QtGui.QPainter.RenderHint.LosslessImageRendering, True
        )
        painter.setRenderHint(
            QtGui.QPainter.RenderHint.SmoothPixmapTransform, True
        )
        painter.setRenderHint(
            QtGui.QPainter.RenderHint.TextAntialiasing, True
        )
        pen = QtGui.QPen()
        pen.setWidth(8)
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
        span_angle = int(self._span_angle * 16)
        painter.drawArc(arc_rect, 0, span_angle)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)

        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)

        margin = 20
        # Center the GIF
        gifshow_width = self.width() - margin * 2
        gifshow_height = self.height() - (self.height() - label_y) - margin

        self.gifshow.setGeometry(margin, margin, gifshow_width, gifshow_height)

        self.label.setGeometry(label_x, label_y, label_width, label_height)

    def show(self) -> None:
        self.timer.start()
        self.repaint()
        return super().show()

    def setupUI(self) -> None:
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)