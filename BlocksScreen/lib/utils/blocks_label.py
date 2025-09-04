import sys
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
        self.delay_timer = QtCore.QTimer()
        self.delay_timer.setSingleShot(True)
        self.delay_timer.timeout.connect(self._start_marquee)
        
        self.scroll_pos = 0.0
        self.marquee_spacing = 20
        self.paused = False
        self.scroll_speed = 20
        self.scroll_animation_speed = 50
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )

        self._glow_color: QtGui.QColor = QtGui.QColor("#E95757")
        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(
            QtCore.QEasingCurve().Type.InOutQuart
        )
        self.glow_animation.setDuration(self.animation_speed)

        self.text_width: int = 0
        self.label_width: int = 0
        self.total_scroll_width: float = 0.0
        self.marquee_delay = 5000
        self.loop_count = 0
        self.first_run = True

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update_text_metrics()
        return super().resizeEvent(a0)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if ev.button() == QtCore.Qt.MouseButton.LeftButton and not self.timer.isActive() and self._marquee:
            self.start_scroll()

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        self.icon_pixmap = a0
        self.update()

    def setText(self, text: str) -> None:
        self._text = text
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
    def marquee(self, activate) -> None:
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
        start_color = QtGui.QColor("#E9575700")
        self.glow_animation.setStartValue(start_color)
        end_color = QtGui.QColor(self.glow_color)
        self.glow_animation.setEndValue(end_color)
        self.glow_animation.setDirection(
            QtCore.QPropertyAnimation.Direction.Forward
        )
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.finished.connect(self.change_glow_direction)
        self.glow_animation.finished.connect(self.repaint)
        self.glow_animation.start()

    @QtCore.pyqtSlot(name="change_glow_direction")
    def change_glow_direction(self) -> None:
        self.glow_animation.setDirection(
            self.glow_animation.Direction.Backward
            if self.glow_animation.direction()
            == self.glow_animation.Direction.Forward
            else self.glow_animation.Direction.Forward
        )

    def update_text_metrics(self) -> None:
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()
        self.total_scroll_width = float(self.text_width + self.marquee_spacing)
        
        if self._marquee and self.text_width > self.label_width:
            self.start_scroll()
        else:
            self.stop_scroll()
            self.scroll_pos = 0.0
        self.update()

    def start_scroll(self) -> None:
        if not self.delay_timer.isActive() and not self.timer.isActive():
            self.scroll_pos = 0
            self.loop_count = 0
            if self.first_run:
                self.delay_timer.start(self.marquee_delay)
                self.first_run = False
            else:
                self._start_marquee()

    def _start_marquee(self) -> None:
        """Starts the actual marquee animation after the delay or immediately."""
        if not self.timer.isActive():
            self.timer.start(self.scroll_animation_speed)

    def stop_scroll(self) -> None:
        self.timer.stop()
        self.delay_timer.stop()

    def _scroll_text(self) -> None:
        if self.paused:
            return

        p_to_m = self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        self.scroll_pos -= p_to_m

        if self.scroll_pos <= -self.total_scroll_width:
            self.loop_count += 1
            if self.loop_count >= 2:
                self.stop_scroll()
            else:
                self.scroll_pos = 0

        self.repaint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)

        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        _rect = self.rect()
        _style = self.style()

        icon_margin = _style.pixelMetric(
            _style.PixelMetric.PM_HeaderMargin, opt, self
        )
        if not _style or _rect.isNull():
            return

        if self.icon_pixmap:
            qp.setCompositionMode(
                qp.CompositionMode.CompositionMode_SourceOver
            )
            _icon_rect = QtCore.QRectF(
                0.0 + icon_margin,
                0.0 + icon_margin,
                self.width() - icon_margin,
                self.height() - icon_margin,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(
                adjusted_icon_rect, _icon_scaled, _icon_scaled.rect().toRectF()
            )

        big_rect = QtGui.QPainterPath()
        rect = self.contentsRect().toRectF()
        big_rect.addRoundedRect(
            rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
        )
        mini_rect = QtCore.QRectF(
            (rect.width() - rect.width() * 0.99) / 2,
            (rect.height() - rect.height() * 0.85) / 2,
            rect.width() * 0.99,
            rect.height() * 0.85,
        )
        mini_path = QtGui.QPainterPath()
        mini_path.addRoundedRect(
            mini_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
        )
        subtracted = big_rect.subtracted(mini_path)

        if self.glow_animation.state() == self.glow_animation.State.Running:
            qp.setCompositionMode(
                qp.CompositionMode.CompositionMode_SourceAtop
            )
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)

        if self._text:
            qp.setCompositionMode(
                qp.CompositionMode.CompositionMode_SourceOver
            )
            
            # Create a painter path for clipping
            text_path = QtGui.QPainterPath()
            text_path.addRect(self.contentsRect().toRectF())
            qp.setClipPath(text_path)

            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)

            if self._marquee and self.text_width > self.label_width:
                # Draw the main text instance
                draw_rect = QtCore.QRectF(
                    self.contentsRect().x() + self.scroll_pos,
                    self.contentsRect().y(),
                    self.text_width,
                    self.contentsRect().height()
                )
                qp.drawText(draw_rect, self._text, text_option)

                # Draw the second text instance with spacing for a continuous loop
                draw_rect2 = QtCore.QRectF(
                    self.contentsRect().x() + self.scroll_pos + self.text_width + self.marquee_spacing,
                    self.contentsRect().y(),
                    self.text_width,
                    self.contentsRect().height()
                )
                qp.drawText(draw_rect2, self._text, text_option)
            else:
                text_rect = self.contentsRect().toRectF()
                qp.drawText(text_rect, self._text, text_option)

        qp.end()

    def setProperty(self, name: str, value: typing.Any) -> bool:
        if name == "icon_pixmap":
            self.setPixmap(value)
        return super().setProperty(name, value)

