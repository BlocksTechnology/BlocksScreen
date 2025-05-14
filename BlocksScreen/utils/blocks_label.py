from PyQt6 import QtWidgets, QtGui, QtCore
import typing


class BlocksLabel(QtWidgets.QLabel):
    def __init__(self, parent: QtWidgets.QWidget, *args, **kwargs):
        if parent is not None:
            super(BlocksLabel, self).__init__(parent, *args, **kwargs)

        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: typing.Optional[str] = None
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False

    def parent(self) -> QtCore.QObject:
        return super().parent()

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        self.icon_pixmap = a0
        self.update()
        return

    def setText(self, a0: str) -> None:
        self._text = a0
        self.update()

        return super().setText(a0)

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

    def border_color(self, color):
        self.setStyleSheet(f"border: 2px solid {color.name()};")

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtWidgets.QStylePainter(self)
        # qp.save()
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
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

    def setProperty(self, name: str, value: typing.Any) -> bool:
        if name == "icon_pixmap":
            self.setPixmap(value)

        return super().setProperty(name, value)
