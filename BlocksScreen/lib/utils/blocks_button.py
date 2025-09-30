import typing
from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksCustomButton(QtWidgets.QPushButton):
    """Custom Blocks QPushButton
        Rounded button with a hole on the left side where an icon can be inserted

    Args:
        parent (QWidget): Parent of the button
    """

    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
    ) -> None:
        if parent:
            super(BlocksCustomButton, self).__init__(parent)
        else:
            super(BlocksCustomButton, self).__init__()

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._icon_rect: QtCore.QRectF = QtCore.QRectF()
        self.button_background = None
        self.button_ellipse = None
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(0, 0, 0)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name) -> None:
        self._name = new_name
        self.setObjectName(new_name)

    def text(self) -> str | None:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text
        self.update()  # Force button update
        return

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        self.icon_pixmap = pixmap
        self.repaint()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        """Overwritten method so 'normal' buttons can only be
        pressed in the visible area
        """
        if not self.button_background:
            if self.button_background.contains(e.pos()):  # type:ignore
                super().mousePressEvent(e)
                return
            else:
                e.ignore()
                return
        return super().mousePressEvent(e)

    def paintEvent(self, e: typing.Optional[QtGui.QPaintEvent]):
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        _rect = self.rect()
        _style = self.style()

        if _style is None or _rect is None:
            return
        margin = _style.pixelMetric(
            _style.PixelMetric.PM_ButtonMargin, opt, self
        )
        bg_color = (
            QtGui.QColor(164, 164, 164)
            if self.isDown()
            else QtGui.QColor(223, 223, 223)
        )

        # bg_color = (
        #     QtGui.QColor(164, 164, 164)
        #     if self.isDown()
        #     else QtGui.QColor(
        #         *(
        #             map(
        #                 lambda component: int(component + component * 0.365),
        #                 (164,164,164),
        #             )
        #         )
        #     )
        # )

        path = QtGui.QPainterPath()
        xRadius = self.rect().toRectF().normalized().height() / 2.0
        yRadius = self.rect().toRectF().normalized().height() / 2.0
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        path.addRoundedRect(
            0,
            0,
            self.rect().toRectF().normalized().width(),
            self.rect().toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        icon_path = QtGui.QPainterPath()
        self.button_ellipse = QtCore.QRectF(
            self.rect().toRectF().normalized().left()
            + self.rect().toRectF().normalized().height() * 0.05,
            self.rect().toRectF().normalized().top()
            + self.rect().toRectF().normalized().height() * 0.05,
            (self.rect().toRectF().normalized().height() * 0.90),
            (self.rect().toRectF().normalized().height() * 0.90),
        )
        icon_path.addEllipse(self.button_ellipse)
        self.button_background = path.subtracted(icon_path)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(self.button_background, bg_color)

        # Draw Icon
        _parent_rect = self.button_ellipse.toRect()
        _icon_rect = QtCore.QRectF(
            _parent_rect.left() * 2.8,
            _parent_rect.top() * 2.8,
            _parent_rect.width() * 0.80,
            _parent_rect.height() * 0.80,
        )
        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )

            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )

        if self.text():
            _start_text_position = int(self.button_ellipse.width())
            _text_rect = _rect
            _text_rect.setLeft(_start_text_position + margin)
            _text_rect.setWidth(
                self.width() - int(self.button_ellipse.width())
            )
            _pen = painter.pen()
            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            _pen.setWidth(1)
            _pen.setColor(QtGui.QColor(self.text_color))
            painter.setPen(_pen)

            painter.drawText(
                _text_rect,
                QtCore.Qt.TextFlag.TextShowMnemonic
                # | QtCore.Qt.AlignmentFlag.AlignHCenter
                | QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                str(self.text()),
            )
            painter.setPen(QtCore.Qt.PenStyle.NoPen)

    def setProperty(self, name: str, value: typing.Any):
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = QtGui.QColor(value)
        # return super().setProperty(name, value)

    def handleTouchBegin(self, e: QtCore.QEvent):
        ...
        # if not self.button_background:
        #     if self.button_background.contains(e.pos()):  # type: ignore
        #         # super().mousePressEvent(e)
        #         self.mousePressEvent(e)  # type: ignore
        #         return
        #     else:
        #         e.ignore()
        #         return

    def handleTouchUpdate(self, e: QtCore.QEvent): ...
    def handleTouchEnd(self, e: QtCore.QEvent): ...
    def handleTouchCancel(self, e: QtCore.QEvent): ...

    def event(self, e: QtCore.QEvent) -> bool:
        if e.type() == QtCore.QEvent.Type.TouchBegin:
            self.handleTouchBegin(e)
            return False
        elif e.type() == QtCore.QEvent.Type.TouchUpdate:
            self.handleTouchUpdate(e)
            return False
        elif e.type() == QtCore.QEvent.Type.TouchEnd:
            self.handleTouchEnd(e)
            return False
        elif e.type() == QtCore.QEvent.Type.TouchCancel:
            self.handleTouchCancel(e)
            return False
        return super().event(e)
