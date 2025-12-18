from PyQt6 import QtWidgets, QtGui, QtCore


class CustomProgressBar(QtWidgets.QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self.pen_width = 20
        self.padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self.bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def set_padding(self, value) -> None:
        """Set widget padding"""
        self.padding = value
        self.update()

    def set_pen_width(self, value) -> None:
        """Set widget text pen width"""
        self.pen_width = value
        self.update()

    def set_inner_pixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set the inner icon pixmap on the progress bar
        circumference.
        """
        self._pixmap = pixmap
        self._pixmap_dirty = True
        self.update()

    def resizeEvent(self, a0) -> None:
        """Re-implemented method, handle widget resize Events

        Currently rescales the set pixmap so it has the optimal
        size.
        """
        self._pixmap_dirty = True
        self._inner_rect = self._calculate_inner_geometry()
        if not self._pixmap.isNull():
            self._pixmap_cached = self._pixmap.scaled(
                self._inner_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
        self.update()
        return super().resizeEvent(a0)

    def sizeHint(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, 100)

    def minimumSizeHint(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, 100)

    def _calculate_inner_geometry(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self.padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self.pen_width // 2,
            y + self.pen_width // 2,
            size - self.pen_width,
            size - self.pen_width,
        )

    def paintEvent(self, event) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._inner_rect: QtCore.QRectF = self._draw_circular_bar(painter)
        # if self._pixmap_dirty:
        self._draw_cached_pixmap(painter, self._inner_rect)
        painter.end()

    def _draw_cached_pixmap(
        self, painter: QtGui.QPainter, inner_rect: QtCore.QRectF
    ) -> None:
        if self._pixmap_cached.isNull():
            return
        # inner_rect = self._calculate_inner_geometry()
        scaled_width = self._pixmap_cached.width()
        scaled_height = self._pixmap_cached.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(
            adjusted_icon, self._pixmap_cached, self._pixmap_cached.rect().toRectF()
        )
        self._pixmap_dirty = False

    def _draw_circular_bar(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self.padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc1_start = 236 * 16
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
            progress_span = int(arc1_span * self.progress_value / 100)
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
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def setValue(self, value):
        """Set value"""
        value *= 100
        if 0 <= value <= 101:
            self.progress_value = value
            self.update()
        else:
            raise ValueError("Progress must be between 0.0 and 1.0.")

    def set_bar_color(self, red, green, blue):
        """Set bar color"""
        if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
            self.bar_color = QtGui.QColor(red, green, blue)
            self.update()
        else:
            raise ValueError("Color values must be between 0 and 255.")
