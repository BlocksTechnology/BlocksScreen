import typing
from PyQt6 import QtWidgets, QtGui, QtCore


class CustomProgressBar(QtWidgets.QProgressBar):
    """Custom circular progress bar for tracking print jobs

    Args:
        QtWidgets (QtWidget): Parent widget

    Raises:
        ValueError: Thrown when setting progress is not between 0.0 and 1.0
        ValueError: Thrown when setting bar color is not between 0 and 255.

    """

    thumbnail_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="thumbnail-clicked"
    )

    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def set_padding(self, value) -> None:
        """Set widget padding"""
        self._padding = value
        self.update()

    def set_pen_width(self, value) -> None:
        """Set widget text pen width"""
        self._pen_width = value
        self.update()

    def _scale_pixmap(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = self._pixmap.scaled(
            self._inner_rect.size().toSize(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

    def set_inner_pixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set the inner icon pixmap on the progress bar
        circumference.
        """
        self._pixmap = pixmap
        self._scale_pixmap()

    def resizeEvent(self, a0) -> None:
        """Reimplemented method, handle widget resize Events

        Currently rescales the set pixmap so it has the optimal
        size.
        """
        self._scale_pixmap()
        self.update()

    def sizeHint(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, 100)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, check if thumbnail was clicked,
        filter clicks inside inner section of the widget,
        if a mouse event happens there we know that the thumbnail
        was pressed.
        """
        if self._inner_rect.contains(a0.pos().x(), a0.pos().y()):
            self.thumbnail_clicked.emit()
        return super().mousePressEvent(a0)

    def minimumSizeHint(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, 100)

    def setValue(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value *= 100
        self.progress_value = value
        self.update()

    def set_bar_color(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def _calculate_inner_geometry(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def _draw_cached_pixmap(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            print("Pixmap is still null ")
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def _draw_circular_bar(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def paintEvent(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter, self._pixmap_cached, self._inner_rect)
        painter.end()
