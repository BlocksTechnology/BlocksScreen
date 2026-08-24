import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class CustomProgressBar(QtWidgets.QProgressBar):
    """Custom circular progress bar for tracking print jobs

    Args:
        QtWidgets (QtWidget): Parent widget

    Raises:
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
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

        # Paint state, rebuilt only on resize or a style setter
        self._arc_rect: QtCore.QRectF | None = None
        self._text_rect = QtCore.QRectF()
        self._pixmap_target = QtCore.QRectF()
        self._pixmap_source = QtCore.QRectF()
        self._text_font: QtGui.QFont | None = None
        self._bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        self._progress_pen = QtGui.QPen()
        self._text_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        self._apply_pen_width()

    def _apply_pen_width(self) -> None:
        """Push the current pen width onto both arc pens"""
        for pen in (self._bg_pen, self._progress_pen):
            pen.setWidth(self._pen_width)
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)

    def _invalidate(self) -> None:
        """Drop the size dependent paint state and the scaled pixmap"""
        self._arc_rect = None
        self._scale_pixmap()

    def set_padding(self, value) -> None:
        """Set widget padding"""
        self._padding = value
        self._invalidate()
        self.update()

    def set_pen_width(self, value) -> None:
        """Set widget text pen width"""
        self._pen_width = value
        self._apply_pen_width()
        self._invalidate()
        self.update()

    def _scale_pixmap(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = self._pixmap.scaled(
            self._inner_rect.size().toSize(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self._pixmap_source = self._pixmap_cached.rect().toRectF()
        self._pixmap_target = QtCore.QRectF(
            self._inner_rect.x()
            + (self._inner_rect.width() - self._pixmap_cached.width()) // 2.0,
            self._inner_rect.y()
            + (self._inner_rect.height() - self._pixmap_cached.height()) // 2.0,
            self._pixmap_cached.width(),
            self._pixmap_cached.height(),
        )

    def set_inner_pixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set the inner icon pixmap on the progress bar
        circumference.
        """
        self._pixmap = pixmap
        self._scale_pixmap()

    def changeEvent(self, a0: QtCore.QEvent | None) -> None:
        """Re-implemented method, drop the cached text font on a font change"""
        if a0 is not None and a0.type() == QtCore.QEvent.Type.FontChange:
            self._text_font = None
        return super().changeEvent(a0)

    def resizeEvent(self, a0) -> None:
        """Reimplemented method, handle widget resize Events

        Currently rescales the set pixmap so it has the optimal
        size.
        """
        self._invalidate()
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

    def set_progress(self, fraction: float) -> None:
        """Set progress from a 0.0-1.0 fraction (clamped)."""
        self.progress_value = max(0.0, min(fraction, 1.0)) * 100
        self.update()

    def reset(self) -> None:
        """Clear progress back to 0%."""
        self.progress_value = 0
        super().reset()
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
        self._arc_rect = None
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

    def _draw_cached_pixmap(self, painter: QtGui.QPainter) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if self._pixmap_cached.isNull():
            return
        painter.drawPixmap(
            self._pixmap_target, self._pixmap_cached, self._pixmap_source
        )

    def _ensure_arc_geometry(self) -> QtCore.QRectF:
        """Rebuild the arc rect, gradient pen and text rect after a resize or restyle"""
        if self._arc_rect is None:
            size = min(self.width(), self.height()) - (self._padding * 1.3)
            x = (self.width() - size) / 2
            y = (self.height() - size) / 2
            self._arc_rect = QtCore.QRectF(x, y, size, size)
            center = self._arc_rect.center()
            gradient = QtGui.QConicalGradient(center, -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            self._progress_pen.setBrush(QtGui.QBrush(gradient))
            self._text_rect = QtCore.QRectF(
                center.x() - 30, center.y() + size / 2 - 25, 60, 40
            )
        return self._arc_rect

    def _text_font_cached(self) -> QtGui.QFont:
        """Widget font at the fixed progress text size"""
        if self._text_font is None:
            self._text_font = QtGui.QFont(self.font())
            self._text_font.setPointSize(16)
        return self._text_font

    def _draw_circular_bar(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        arc_rect = self._ensure_arc_geometry()
        arc_start = 236 * 16
        arc_span = -290 * 16
        painter.setPen(self._bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            painter.setPen(self._progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        painter.setPen(self._text_pen)
        painter.setFont(self._text_font_cached())
        painter.drawText(
            self._text_rect,
            QtCore.Qt.AlignmentFlag.AlignCenter,
            f"{int(self.progress_value)}%",
        )

    def paintEvent(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter)
        painter.end()
