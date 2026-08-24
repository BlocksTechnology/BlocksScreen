import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksLabel(QtWidgets.QLabel):
    """Custom QLabel with marquee scrolling, glow animation, and icon overlay support."""

    def __init__(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        """Initialise the label and configure default scroll/animation state."""
        super().__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: QtGui.QPixmap | None = None
        self._text: str = ""
        self._background_color: QtGui.QColor | None = None
        self._border_color: QtGui.QColor | None = None
        self._rounded: bool = False
        self._marquee: bool = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0.0
        self.marquee_spacing = 40
        self.scroll_speed = 40
        self.scroll_animation_speed = 30
        self.max_loops = 2
        self.loop_count = 0
        self.paused = False
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.update)
        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.icon_margin: int = 5
        self.first_run = True
        # Paint caches, invalidated on resize/font change
        self._font_metrics: QtGui.QFontMetrics | None = None
        self._baseline_offset: float = 0.0
        self._background_path: QtGui.QPainterPath | None = None
        self._glow_path: QtGui.QPainterPath | None = None
        self._icon_cache: QtGui.QPixmap | None = None
        self._icon_cache_size: QtCore.QSize = QtCore.QSize()
        self._icon_target: QtCore.QRectF = QtCore.QRectF()

    def _invalidate_geometry_cache(self) -> None:
        """Drop every cache whose value depends on the widget size"""
        self._background_path = None
        self._glow_path = None
        self._icon_cache = None
        self._icon_cache_size = QtCore.QSize()

    def _metrics(self) -> QtGui.QFontMetrics:
        """Cached QFontMetrics, rebuilt only on font change"""
        if self._font_metrics is None:
            self._font_metrics = self.fontMetrics()
            self._baseline_offset = (
                self._font_metrics.ascent() - self._font_metrics.descent()
            ) / 2.0
        return self._font_metrics

    def changeEvent(self, a0: QtCore.QEvent | None) -> None:
        """Re-implemented method, invalidate the metrics cache when the font changes"""
        if a0 is not None and a0.type() == QtCore.QEvent.Type.FontChange:
            self._font_metrics = None
            self.update_text_metrics()
        super().changeEvent(a0)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self._invalidate_geometry_cache()
        self.update_text_metrics()
        return super().resizeEvent(a0)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press event"""
        if (
            ev.button() == QtCore.Qt.MouseButton.LeftButton
            and not self.timer.isActive()
            and self._marquee
        ):
            self.start_scroll()

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = a0
        self._icon_cache = None
        self._icon_cache_size = QtCore.QSize()
        self.update()

    def clearPixmap(self) -> None:
        """Clear the current pixmap."""
        self.icon_pixmap = None
        self._icon_cache = None
        self._icon_cache_size = QtCore.QSize()
        self.update()

    def setText(self, text: str) -> None:
        """Set widget text"""
        self._text = text
        self.scroll_pos = 0.0
        self.update_text_metrics()

    @property
    def background_color(self) -> QtGui.QColor | None:
        """Widget background color"""
        return self._background_color

    @background_color.setter
    def background_color(self, color: QtGui.QColor) -> None:
        self._background_color = color

    @property
    def border_color(self) -> QtGui.QColor | None:
        """Widget border color"""
        return self._border_color

    @border_color.setter
    def border_color(self, color: QtGui.QColor) -> None:
        self._border_color = color

    @property
    def rounded(self) -> bool:
        """Widget rounded property"""
        return self._rounded

    @rounded.setter
    def rounded(self, on: bool) -> None:
        self._rounded = on

    @property
    def marquee(self) -> bool:
        """Widget enable marquee effect"""
        return self._marquee

    @marquee.setter
    def marquee(self, activate: bool) -> None:
        self._marquee = activate
        self.update_text_metrics()

    @QtCore.pyqtProperty(int)
    def animation_speed(self) -> int:
        """Widget animation speed property"""
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, new_speed: int) -> None:
        self._animation_speed = new_speed

    @QtCore.pyqtProperty(QtGui.QColor)
    def glow_color(self) -> QtGui.QColor:
        """Widget glow color property"""
        return self._glow_color

    @glow_color.setter
    def glow_color(self, color: QtGui.QColor) -> None:
        self._glow_color = color
        self.update()

    @QtCore.pyqtSlot(name="start_glow_animation")
    def start_glow_animation(self) -> None:
        """Start glow animation"""
        self.glow_animation.setDuration(self.animation_speed)
        start_color = QtGui.QColor("#00000000")
        end_color = QtGui.QColor("#E95757")
        self.glow_animation.setStartValue(start_color)
        self.glow_animation.setEndValue(end_color)
        self.glow_animation.setDirection(QtCore.QPropertyAnimation.Direction.Forward)
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.start()

    @QtCore.pyqtSlot(name="change_glow_direction")
    def change_glow_direction(self) -> None:
        """Handle Change glow direction"""
        current_direction = self.glow_animation.direction()
        if current_direction == self.glow_animation.Direction.Forward:
            self.glow_animation.setDirection(self.glow_animation.Direction.Backward)
        else:
            self.glow_animation.setDirection(self.glow_animation.Direction.Forward)

    def update_text_metrics(self) -> None:
        """Handle widget text metrics"""
        font_metrics = self._metrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, self.start_scroll)
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def start_scroll(self) -> None:
        """Start or restart the scrolling."""
        if not self.timer.isActive():
            self.scroll_pos = 0
            self.loop_count = 0
            self.timer.start(self.scroll_animation_speed)

    def stop_scroll(self) -> None:
        """Stop marquee text scroll effect"""
        self.timer.stop()
        self.update()

    @QtCore.pyqtSlot()
    def _scroll_text(self) -> None:
        """Smoothly scroll the text leftwards."""
        if not self._marquee or self.paused:
            return
        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m
        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= self.max_loops:
                self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def _background(self, rect: QtCore.QRect) -> QtGui.QPainterPath:
        """Cached rounded background path for the current size"""
        if self._background_path is None:
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
            self._background_path = path
        return self._background_path

    def _glow(self, rect: QtCore.QRectF) -> QtGui.QPainterPath:
        """Cached glow ring path; the boolean subtract only depends on the size"""
        if self._glow_path is None:
            big_rect = QtGui.QPainterPath()
            big_rect.addRoundedRect(rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize)
            sub_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) / 2,
                (rect.height() - rect.height() * 0.85) / 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            sub_path = QtGui.QPainterPath()
            sub_path.addRoundedRect(
                sub_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(sub_path)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            self._glow_path = subtracted
        return self._glow_path

    def _paint_icon(self, qp: QtGui.QPainter) -> None:
        """Draw the overlay icon, rescaling only when the target size changes"""
        icon_rect = QtCore.QRectF(
            0.0 + self.icon_margin,
            0.0 + self.icon_margin,
            self.width() - self.icon_margin,
            self.height() - self.icon_margin,
        )
        target_size = icon_rect.size().toSize()
        if self._icon_cache is None or target_size != self._icon_cache_size:
            self._icon_cache = self.icon_pixmap.scaled(
                target_size,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            self._icon_cache_size = target_size
            scaled_width = self._icon_cache.width()
            scaled_height = self._icon_cache.height()
            adjusted_x = (icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (icon_rect.height() - scaled_height) // 2.0
            self._icon_target = QtCore.QRectF(
                icon_rect.x() + adjusted_x,
                icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
        _icon_scaled = self._icon_cache
        qp.drawPixmap(self._icon_target, _icon_scaled, _icon_scaled.rect().toRectF())

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                qp.fillPath(self._background(rect), self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            self._paint_icon(qp)

        if self.glow_animation.state() == self.glow_animation.State.Running:
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            qp.fillPath(self._glow(rect.toRectF()), self.glow_color)

        if self._text:
            qp.save()
            qp.setClipRect(rect)
            self._metrics()
            baseline_y = rect.y() + rect.height() / 2 + self._baseline_offset

            if self.text_width > self.label_width:
                qp.drawText(
                    QtCore.QPointF(rect.x() + self.scroll_pos, baseline_y), self._text
                )
                # Draw scrolling repeater text
                qp.drawText(
                    QtCore.QPointF(
                        rect.x() + self.scroll_pos + self.total_scroll_width, baseline_y
                    ),
                    self._text,
                )
            else:
                center_x = rect.x() + (rect.width() - self.text_width) / 2

                qp.drawText(QtCore.QPointF(center_x, baseline_y), self._text)
            qp.restore()

        qp.end()

    def setProperty(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.setPixmap(value)
        return super().setProperty(name, value)
