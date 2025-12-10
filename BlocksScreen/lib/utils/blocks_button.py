import typing
import enum
from PyQt6 import QtCore, QtGui, QtWidgets


class ButtonColors(enum.Enum):
    """Standard button colors"""

    NORMAL_BG = (223, 223, 223)
    PRESSED_BG = (169, 169, 169)
    DISABLED_BG = (169, 169, 169)
    TEXT_COLOR = (0, 0, 0)
    DISABLED_TEXT_COLOR = (102, 102, 102)
    NOTIFICATION_DOT = (226, 31, 31)


class BlocksCustomButton(QtWidgets.QAbstractButton):
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
        self.text_color: QtGui.QColor = QtGui.QColor(*ButtonColors.TEXT_COLOR.value)
        self._show_notification: bool = False
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    def setShowNotification(self, show: bool) -> None:
        """Set notification on button"""
        if self._show_notification != show:
            self._show_notification = show
            self.repaint()
            self.update()

    @property
    def name(self):
        """Button name"""
        return self._name

    @name.setter
    def name(self, new_name) -> None:
        self._name = new_name
        self.setObjectName(new_name)

    def text(self) -> str | None:
        """Button text"""
        return self._text

    def setText(self, text: str) -> None:
        """Set button text"""
        self._text = text
        self.update()
        return

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set button pixmap"""
        self.icon_pixmap = pixmap
        self.repaint()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        """Handle mouse press events"""
        if not self.isEnabled():
            e.ignore()
            return

        if self.button_background is not None:
            pos_f = QtCore.QPointF(e.pos())
            if self.button_background.contains(pos_f):
                super().mousePressEvent(e)
                return
            else:
                e.ignore()
                return
        return super().mousePressEvent(e)

    def paintEvent(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        _rect = self.rect()
        _style = self.style()

        if _style is None or _rect is None:
            return

        # Determine background and text colors based on state
        if not self.isEnabled():
            bg_color_tuple = ButtonColors.DISABLED_BG.value
            current_text_color = QtGui.QColor(*ButtonColors.DISABLED_TEXT_COLOR.value)
        elif self.isDown():
            bg_color_tuple = ButtonColors.PRESSED_BG.value
            current_text_color = self.text_color
        else:
            bg_color_tuple = ButtonColors.NORMAL_BG.value
            current_text_color = self.text_color

        bg_color = QtGui.QColor(*bg_color_tuple)

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

            tinted_icon_pixmap = QtGui.QPixmap(_icon_scaled.size())
            tinted_icon_pixmap.fill(QtCore.Qt.GlobalColor.transparent)

            if not self.isEnabled():
                tinted_icon_pixmap = QtGui.QPixmap(_icon_scaled.size())
                tinted_icon_pixmap.fill(QtCore.Qt.GlobalColor.transparent)

                icon_painter = QtGui.QPainter(tinted_icon_pixmap)
                icon_painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
                icon_painter.setRenderHint(
                    QtGui.QPainter.RenderHint.SmoothPixmapTransform
                )

                icon_painter.drawPixmap(0, 0, _icon_scaled)

                icon_painter.setCompositionMode(
                    QtGui.QPainter.CompositionMode.CompositionMode_SourceAtop
                )
                tint = QtGui.QColor(
                    bg_color.red(), bg_color.green(), bg_color.blue(), 120
                )
                icon_painter.fillRect(tinted_icon_pixmap.rect(), tint)
                icon_painter.end()

                final_pixmap = tinted_icon_pixmap
            else:
                final_pixmap = _icon_scaled

            destination_point = adjusted_icon_rect.toRect().topLeft()
            painter.drawPixmap(destination_point, final_pixmap)

        if self.text():
            font_metrics = self.fontMetrics()
            self.text_width = font_metrics.horizontalAdvance(self._text)
            self.label_width = self.contentsRect().width()

            # _start_text_position = int(self.button_ellipse.width())
            _text_rect = _rect

            _text_rect2 = _rect
            _text_rect2.setWidth(self.width() - int(self.button_ellipse.width()))
            _text_rect2.setLeft(int(self.button_ellipse.width()))

            _text_rect.setWidth(self.width() - int(self.button_ellipse.width()))
            _text_rect.setLeft(int(self.button_ellipse.width()))
            _pen = painter.pen()
            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            _pen.setWidth(1)
            _pen.setColor(current_text_color)
            painter.setPen(_pen)

            # if self.text_width < _text_rect2.width()*0.6:
            _text_rect.setWidth(self.width() - int(self.button_ellipse.width() * 1.4))
            _text_rect.setLeft(int(self.button_ellipse.width()))

            painter.drawText(
                _text_rect,
                QtCore.Qt.TextFlag.TextShowMnemonic
                | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )
            # else:
            #     _text_rect.setLeft(_start_text_position + margin)

            #     _text_rect.setWidth(self.width() - int(self.button_ellipse.width()))

            #     painter.drawText(
            #         _text_rect,
            #         QtCore.Qt.TextFlag.TextShowMnemonic
            #         | QtCore.Qt.AlignmentFlag.AlignLeft
            #         | QtCore.Qt.AlignmentFlag.AlignVCenter,
            #         str(self.text()),
            #     )
            painter.setPen(QtCore.Qt.PenStyle.NoPen)

        if self._show_notification:
            dot_diameter = self.height() * 0.4
            dot_x = self.width() - dot_diameter
            notification_color = QtGui.QColor(*ButtonColors.NOTIFICATION_DOT.value)
            painter.setBrush(notification_color)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            dot_rect = QtCore.QRectF(dot_x, 0, dot_diameter, dot_diameter)
            painter.drawEllipse(dot_rect)

        painter.end()

    def setProperty(self, name: str, value: typing.Any):
        """Set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = QtGui.QColor(value)
            self.update()

    def event(self, e: QtCore.QEvent) -> bool:
        """Re-implemented method, filter events"""
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
