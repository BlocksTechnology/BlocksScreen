import typing
from PyQt6 import QtWidgets, QtGui, QtCore


class BlocksLabel(QtWidgets.QLabel):
    def __init__(self, parent: QtWidgets.QWidget = None, *args, **kwargs):
        super(BlocksLabel, self).__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
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
        self.glow_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.glow_animation.setDuration(self.animation_speed)

        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)

        self.total_scroll_width: float = 0.0
        self.text_width: float = 0.0
        self.label_width: float = 0.0
        self.first_run = True

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update_text_metrics()
        return super().resizeEvent(a0)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if (
            ev.button() == QtCore.Qt.MouseButton.LeftButton
            and not self.timer.isActive()
            and self._marquee
        ):
            self.start_scroll()

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        self.icon_pixmap = a0
        self.update()

    def setText(self, text: str) -> None:
        self._text = text
        self.scroll_pos = 0.0
        self.update_text_metrics()

    @property
    def background_color(self) -> typing.Optional[QtGui.QColor]:
        return self._background_color

    @background_color.setter
    def background_color(self, color: QtGui.QColor) -> None:
        self._background_color = color

    @property
    def border_color(self) -> typing.Optional[QtGui.QColor]:
        return self._border_color

    @border_color.setter
    def border_color(self, color: QtGui.QColor) -> None:
        self._border_color = color

    @property
    def rounded(self) -> bool:
        return self._rounded

    @rounded.setter
    def rounded(self, on: bool) -> None:
        self._rounded = on

    @property
    def marquee(self) -> bool:
        return self._marquee

    @marquee.setter
    def marquee(self, activate: bool) -> None:
        self._marquee = activate
        self.update_text_metrics()

    @QtCore.pyqtProperty(int)
    def animation_speed(self) -> int:
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, new_speed: int) -> None:
        self._animation_speed = new_speed

    @QtCore.pyqtProperty(QtGui.QColor)
    def glow_color(self) -> QtGui.QColor:
        return self._glow_color

    @glow_color.setter
    def glow_color(self, color: QtGui.QColor) -> None:
        self._glow_color = color
        self.repaint()

    @QtCore.pyqtSlot(name="start_glow_animation")
    def start_glow_animation(self) -> None:
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
        current_direction = self.glow_animation.direction()
        if current_direction == self.glow_animation.Direction.Forward:
            self.glow_animation.setDirection(self.glow_animation.Direction.Backward)
        else:
            self.glow_animation.setDirection(self.glow_animation.Direction.Forward)

    def update_text_metrics(self) -> None:
        """Recalculate text width and control marquee start/stop behavior."""
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)

        if self._marquee and self.text_width > self.label_width:
            self.scroll_pos = 0.0
            QtCore.QTimer.singleShot(2000, lambda: self.start_scroll())
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
        """Stop all marquee timers."""
        self.timer.stop()
        self.repaint()

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
                self.scroll_pos = 0
                return
            else:
                self.scroll_pos = 0

        self.update()
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.contentsRect()
        if self._background_color:
            qp.setBrush(self._background_color)
            qp.setPen(QtCore.Qt.PenStyle.NoPen)
            if self._rounded:
                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
                qp.fillPath(path, self._background_color)
            else:
                qp.fillRect(rect, self._background_color)

        if self.icon_pixmap:
            icon_rect = QtCore.QRectF(0, 0, self.height(), self.height())
            scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            qp.drawPixmap(icon_rect.toRect(), scaled)
        if self.glow_animation.state() == self.glow_animation.State.Running:
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(rect), 10, 10)
            qp.fillPath(path, self.glow_color)
        if self._text:
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            qp.save()
            qp.setClipRect(rect)
            baseline_y = (
                rect.y()
                + (rect.height() + self.fontMetrics().ascent() - self.fontMetrics().descent())
                / 2
            )
            
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
                
                qp.drawText(
                    QtCore.QPointF(center_x, baseline_y), 
                    self._text
                )
            qp.restore()

        qp.end()

    def setProperty(self, name: str, value: typing.Any) -> bool:
        if name == "icon_pixmap":
            self.setPixmap(value)
        return super().setProperty(name, value)