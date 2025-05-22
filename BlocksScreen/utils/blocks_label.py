from PyQt6 import QtWidgets, QtGui, QtCore
import typing


class BlocksLabel(QtWidgets.QLabel):
    def __init__(self, parent: QtWidgets.QWidget, *args, **kwargs):
        if parent is not None:
            super(BlocksLabel, self).__init__(parent, *args, **kwargs)

        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: str = ""
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False
        self._marquee: bool = False
        self.timer: QtCore.QTimer = QtCore.QTimer()
        self.timer.timeout.connect(self._scroll_text)
        self.scroll_pos = 0
        self.paused = False
        self.scroll_speed = 20
        self.scroll_animation_speed = 50

        self.setMouseTracking(True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )

    def parent(self) -> QtCore.QObject:
        return super().parent()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update_text_metrics()
        return super().resizeEvent(a0)

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        self.icon_pixmap = a0
        self.repaint()

    def setText(self, text: str) -> None:
        self._text = text
        self.update_text_metrics()

    @property
    def background_color(self) -> typing.Optional[QtGui.QColor]:
        return self._background_color

    @background_color.setter
    def background_color(self, color: QtGui.QColor) -> None:
        self._background_color = color
        self.update()

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

    # TODO: Add rounded object according to the size, calculate the edge pixels radius according to the label size
    def construct_animation(self) -> None:
        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        self.animation = QtCore.QPropertyAnimation(self, b"borderColor")  # type: ignore
        self.animation.setDuration(2000)
        self.animation.setLoopCount(-1)

        self.animation.setStartValue(QtGui.QColor("red"))
        self.animation.start()

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
        # opt = QtWidgets.QStylePainter(self)

        _rect = self.rect()
        _style = self.style()

        if _style is None or _rect is None:
            return

        if self.icon_pixmap is not None:
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
        # TODO : Feature Request, add text onto the label, formatted according to the icon,
        #  Add "above" "bellow", "right", "left" this indicates where the text should be drawn

        if self._background_color is not None:
            # Rounded background edges
            path = QtGui.QPainterPath()
            path.addRoundedRect(
                self.rect().toRectF(),
                10.0,
                10.0,
                QtCore.Qt.SizeMode.AbsoluteSize,
            )
            mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
            self.setMask(mask)

            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setRenderHint(painter.RenderHint.Antialiasing)
            painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
            painter.fillPath(path, self._background_color)
            painter.end()

            # qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceIn)

            # _brush = QtGui.QBrush()
            # _brush.setColor(self._background_color)
            # _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            # qp.setBrush(_brush)
            # if self._rounded:
            #     qp.drawRoundedRect(
            #         self.rect(), 15, 15, QtCore.Qt.SizeMode.AbsoluteSize
            #     )
            # else:
            #     qp.drawRect(self.rect())
        # qp.restore()

        if self.text:
            text_rect = self.contentsRect()
            text_rect.translate(int(self.scroll_pos), 0)
            text_option = QtGui.QTextOption(self.alignment())
            text_option.setWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
            text_option.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            painter = QtGui.QPainter(self)
            text_rect.setWidth(self.text_width)
            painter.drawText(
                text_rect.toRectF(),
                self._text,
                text_option,
            )
            if self.text_width > self.label_width and self.scroll_pos < 0:
                second_text_rect = self.contentsRect()
                second_text_rect.translate(
                    int(
                        self.scroll_pos
                        + self.text_width
                        + self.label_width / 2
                    ),
                    0,
                )
                painter.drawText(
                    second_text_rect.toRectF(), self._text, text_option
                )
            painter.end()

    def setProperty(self, name: str, value: typing.Any) -> bool:
        if name == "icon_pixmap":
            self.setPixmap(value)

        return super().setProperty(name, value)
