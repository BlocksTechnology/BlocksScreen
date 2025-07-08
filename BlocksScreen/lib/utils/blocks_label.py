from PyQt6 import QtWidgets, QtGui, QtCore
import typing


class BlocksLabel(QtWidgets.QLabel):
    def __init__(self, parent: QtWidgets.QWidget, *args, **kwargs):
        if parent is not None:
            super(BlocksLabel, self).__init__(parent, *args, **kwargs)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._border_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = False
        self.timer: QtCore.QTimer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0
        self.paused = False
        self.scroll_speed = 20
        self.scroll_animation_speed = 50
        self.setMouseTracking(True)
        self.setTabletTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )

        self._glow_color: QtGui.QColor = QtGui.QColor("#E9575700")

        self._animation_speed: int = 300
        self.glow_animation = QtCore.QPropertyAnimation(self, b"glow_color")
        self.glow_animation.setEasingCurve(
            QtCore.QEasingCurve().Type.InOutQuart
        )
        self.glow_animation.setDuration(self.animation_speed)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update_text_metrics()
        return super().resizeEvent(a0)

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
        end_color = QtGui.QColor("#E95757")
        self.glow_animation.setEndValue(end_color)
        self.glow_animation.setDirection(
            QtCore.QPropertyAnimation.Direction.Forward
        )
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.finished.connect(self.change_glow_direction)
        # self.glow_animation.finished.connect(self.start_glow_animation)
        self.glow_animation.start()

    @QtCore.pyqtSlot(name="change_glow_direction")
    def change_glow_direction(self) -> None:
        if (
            self.glow_animation.direction()
            == QtCore.QPropertyAnimation.Direction.Forward
        ):
            self.glow_animation.setDirection(
                QtCore.QPropertyAnimation.Direction.Backward
            )
        else:
            self.glow_animation.setDirection(
                QtCore.QPropertyAnimation.Direction.Forward
            )

        print("changing direction")

    def update_text_metrics(self) -> None:
        font_metrics = self.fontMetrics()
        self.text_width = font_metrics.horizontalAdvance(self._text)
        self.label_width = self.contentsRect().width()

        if self.text_width > self.label_width:
            self.start_scrolling()
        else:
            self.stop_scrolling()
            self.scroll_pos = 0

        self.repaint()

    def start_scrolling(self) -> None:
        if not self.timer.isActive():
            self.scroll_pos = 0
            self.timer.start(self.scroll_animation_speed)

    def stop_scrolling(self) -> None:
        if self.timer.isActive():
            self.timer.stop()

    def _scroll_text(self):
        if self.paused:
            return

        p_to_m = int(
            self.scroll_speed * (self.scroll_animation_speed / 1000.0)
        )
        self.scroll_pos -= p_to_m

        if abs(self.scroll_pos) >= self.text_width:
            self.scroll_pos = self.label_width

        self.repaint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtWidgets.QStylePainter(self)
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        _rect = self.rect()
        _style = self.style()

        if not _style or _rect.isNull():
            return

        if self.icon_pixmap:
            qp.setCompositionMode(
                qp.CompositionMode.CompositionMode_SourceOver
            )
            _icon_rect = QtCore.QRectF(0.0, 0.0, self.width(), self.height())
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

        if self.glow_animation.state() == self.glow_animation.State.Running:
            big_rect = QtGui.QPainterPath()
            rect = self.contentsRect().toRectF()
            big_rect.addRoundedRect(
                rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            mini_rect = QtCore.QRectF(
                (rect.width() - rect.width() * 0.99) // 2,
                (rect.height() - rect.height() * 0.85) // 2,
                rect.width() * 0.99,
                rect.height() * 0.85,
            )
            mini_path = QtGui.QPainterPath()
            mini_path.addRoundedRect(
                mini_rect, 10.0, 10.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            subtracted = big_rect.subtracted(mini_path)
            subtracted.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
            qp.fillPath(subtracted, self.glow_color)

        if self.text:
            qp.setCompositionMode(
                qp.CompositionMode.CompositionMode_SourceOver
            )
            text_rect = self.contentsRect()
            text_rect.translate(int(self.scroll_pos), 0)
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            # text_rect.setWidth(self.text_width)
            qp.drawText(
                text_rect.toRectF(),
                self._text,
                text_option,
            )

            if self.text_width > self.label_width and self.scroll_pos < 0:
                second_text_rect = self.rect()
                second_text_rect.translate(
                    int(
                        self.scroll_pos
                        + self.text_width
                        + self.label_width / 2
                    ),
                    0,
                )
                qp.drawText(
                    second_text_rect.toRectF(), self._text, text_option
                )
        qp.end()

    def setProperty(self, name: str, value: typing.Any) -> bool:
        if name == "icon_pixmap":
            self.setPixmap(value)

        return super().setProperty(name, value)
