from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksSlider(QtWidgets.QSlider):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.highlight_color = "#2AC9F9"
        self.gradient_pos = QtCore.QPointF(0.0, 0.0)
        self.setMinimumSize(300, 100)
        self.setMaximumSize(400, 100)
        self.setMouseTracking(True)
        self.setTracking(True)
        self.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.setTickInterval(20)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setPageStep(0)
        self._groove_rect: QtCore.QRect = QtCore.QRect()
        self._handle_rect: QtCore.QRect = QtCore.QRect()
        # Paint caches keyed by the rect they were built for
        self._groove_path: QtGui.QPainterPath | None = None
        self._groove_key: QtCore.QRect = QtCore.QRect()
        self._handle_path: QtGui.QPainterPath | None = None
        self._handle_key: QtCore.QRect = QtCore.QRect()
        self._font_metrics: QtGui.QFontMetrics | None = None
        self._gradient_stops: tuple[QtGui.QColor, ...] = ()
        self._gradient_key: str = ""
        self._groove_color = QtGui.QColor(164, 164, 164)
        self._groove_color.setAlphaF(0.5)
        self._handle_down_color = QtGui.QColor(164, 164, 164)
        self._handle_up_color = QtGui.QColor(223, 223, 223)
        self._tick_color = QtGui.QColor(255, 255, 255)

    def changeEvent(self, a0: QtCore.QEvent | None) -> None:
        """Re-implemented method, drop the metrics cache when the font changes"""
        if a0 is not None and a0.type() == QtCore.QEvent.Type.FontChange:
            self._font_metrics = None
        super().changeEvent(a0)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        """Re-implemented method, Handle mouse press events"""
        if (ev.button() == QtCore.Qt.MouseButton.LeftButton) and self.hit_test(
            ev.position().toPoint().toPointF()
        ):
            self.setSliderDown(True)
            ev.accept()
        else:
            return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        """Handle mouse release events"""
        if self.isSliderDown():
            self.setSliderDown(False)
        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        """Handle mouse move events"""
        if self.isSliderDown():
            self._set_slider_pos(ev.position().toPoint().toPointF())
            self.gradient_pos = ev.position().toPoint().toPointF()
            self.update()
            ev.accept()
        else:
            return super().mouseMoveEvent(ev)

    def hit_test(self, pos: QtCore.QPointF) -> bool:
        """Hit test to allow dragging larger handle area

        Args:
            pos (QtCore.QPointF): _description_

        Returns:
            bool: If the handle contains the specified position
        """
        _handle_path = QtGui.QPainterPath()
        _hit_rect = QtCore.QRect(self._handle_rect)
        _hit_rect.setSize(QtCore.QSize(60, 55))
        _handle_path.addRoundedRect(_hit_rect.toRectF(), 5, 5)
        return _handle_path.contains(pos)

    def _set_slider_pos(self, pos: QtCore.QPointF):
        min_val = self.minimum()
        max_val = self.maximum()
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            slider_length = self._groove_rect.width()
            slider_start = self._groove_rect.x()
            pos_x = pos.x()
            new_val = (
                min_val + (max_val - min_val) * (pos_x - slider_start) // slider_length
            )
        else:
            slider_length = self._groove_rect.height()
            slider_start = self._groove_rect.y()
            pos_y = pos.y()
            new_val = (
                min_val + (max_val - min_val) * (pos_y - slider_start) / slider_length
            )
        self.setSliderPosition(int(round(new_val)))
        self.setValue(int(round(new_val)))
        self.update()

    @staticmethod
    def _rounded_path(rect: QtCore.QRect, radius: float) -> QtGui.QPainterPath:
        """Build a rounded-rect path"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect.toRectF(), radius, radius)
        return path

    def _gradient(self) -> QtGui.QRadialGradient:
        """Radial glow around the handle, colors recomputed only on highlight change"""
        if self._gradient_key != self.highlight_color:
            stops = []
            for alpha in (110, 50, 10):
                color = QtGui.QColor(self.highlight_color)
                color.setAlpha(alpha)
                stops.append(color)
            self._gradient_stops = tuple(stops)
            self._gradient_key = self.highlight_color
        center = self._handle_rect.center().toPointF()
        gradient = QtGui.QRadialGradient(center, 200.0, center)
        gradient.setColorAt(0, self._gradient_stops[0])
        gradient.setColorAt(0.5, self._gradient_stops[1])
        gradient.setColorAt(1, self._gradient_stops[2])
        return gradient

    def paintEvent(self, ev: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        _style = self.style()

        # Clip the opt rect inside, so the handle and
        # groove doesn't exceed the limits
        opt.rect = opt.rect.adjusted(12, 10, -18, 20)  # This is a bit hardcoded

        # Groove is fully positioned below, so the subControlRect lookup is skipped
        _groove_w = self.width() - 25
        _groove_h = 30
        self._groove_rect = QtCore.QRect(
            (self.width() - _groove_w) // 2,
            (self.height() - _groove_h) // 2,
            _groove_w,
            _groove_h,
        )

        self._handle_rect = _style.subControlRect(
            QtWidgets.QStyle.ComplexControl.CC_Slider,
            opt,
            QtWidgets.QStyle.SubControl.SC_SliderHandle,
            self,
        )
        self._handle_rect.setSize(QtCore.QSize(20, 50))
        self._handle_rect.moveTop((self.height() - self._handle_rect.height()) // 2)

        _handle_color = (
            self._handle_down_color if self.isSliderDown() else self._handle_up_color
        )

        if self._groove_path is None or self._groove_key != self._groove_rect:
            self._groove_path = self._rounded_path(self._groove_rect, 15)
            self._groove_key = QtCore.QRect(self._groove_rect)
        if self._handle_path is None or self._handle_key != self._handle_rect:
            self._handle_path = self._rounded_path(self._handle_rect, 5)
            self._handle_key = QtCore.QRect(self._handle_rect)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.TextAntialiasing, True)
        painter.fillPath(
            self._groove_path, self._groove_color
        )  # Primary groove background color

        if self._font_metrics is None:
            self._font_metrics = QtGui.QFontMetrics(painter.font())
        fm = self._font_metrics
        min_v, max_v = self.minimum(), self.maximum()
        label_offset = 4

        _style.drawComplexControl(
            QtWidgets.QStyle.ComplexControl.CC_Slider, opt, painter, self
        )

        painter.setPen(self._tick_color)
        for v in (min_v, max_v):
            x = (
                QtWidgets.QStyle.sliderPositionFromValue(
                    min_v, max_v, v, self._groove_rect.width()
                )
                + self._groove_rect.x()
            )
            y1 = self._groove_rect.bottom()
            y2 = y1 + 15  # tick length
            label = str(v)
            text_x = x - fm.horizontalAdvance(label) // 2
            text_y = y2 + fm.ascent() + label_offset
            painter.drawLine(x, y1, x, y2)
            painter.drawText(text_x, text_y, label)

        # Paint the elements with colors
        painter.setBrush(self._gradient())
        painter.fillPath(self._groove_path, painter.brush())
        painter.fillPath(self._handle_path, _handle_color)
        painter.end()
