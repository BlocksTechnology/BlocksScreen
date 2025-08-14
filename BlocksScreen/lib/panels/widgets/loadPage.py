from PyQt6 import QtCore, QtGui, QtWidgets


class LoadScreen(QtWidgets.QDialog):
    def __init__(
        self, parent: QtWidgets.QWidget, main_window: QtWidgets.QWidget
    ) -> None:
        super().__init__(parent)
        self.main_window = main_window
        self.default_background_color = QtGui.QColor(0, 0, 0, 150)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self.setupUI()

        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )

        # Safely try to set the 'always on top' flag for better compatibility
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
        )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(16)

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

    def set_status_message(self, message: str) -> None:
        self.label.setText(message)

    def sizeHint(self) -> QtCore.QSize:
        # Use the explicitly passed main_window to get geometry
        parent_rect = self.main_window.geometry()

        popup_width = int(parent_rect.width() * 0.90)
        popup_height = int(parent_rect.height() * 0.90)

        # Centering logic
        popup_x = parent_rect.x() + (parent_rect.width() - popup_width) // 2
        popup_y = parent_rect.y() + (parent_rect.height() - popup_height) // 2

        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.close()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.TextAntialiasing, True)

        popup_path = QtGui.QPainterPath()
        popup_path.addRoundedRect(self.rect().toRectF(), 10, 10)
        _background_color = self.default_background_color
        painter.setBrush(_background_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.fillPath(popup_path, painter.brush())

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

    def setupUI(self) -> None:
        self.setObjectName("Popup")
        self.label = QtWidgets.QLabel("Test", self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
