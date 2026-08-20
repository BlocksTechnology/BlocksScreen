import enum
import typing

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
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._icon_rect: QtCore.QRectF = QtCore.QRectF()
        self._is_flat: bool = False
        self.button_background = None
        self.button_ellipse = None
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(*ButtonColors.TEXT_COLOR.value)
        self._show_notification: bool = False
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self._icon_cache: QtGui.QPixmap = QtGui.QPixmap()
        self._icon_cache_size: QtCore.QSize = QtCore.QSize()

    def setShowNotification(self, show: bool) -> None:
        """Set notification on button"""
        if self._show_notification != show:
            self._show_notification = show
            self.update()

    @property
    def name(self):
        """Widget name"""
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

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set button pixmap"""
        self.icon_pixmap = pixmap
        self._icon_cache = QtGui.QPixmap()
        self._icon_cache_size = QtCore.QSize()
        self.update()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        """Handle mouse press events"""
        if not self.isEnabled():
            e.ignore()
            return
        if self.button_background:
            pos_f = QtCore.QPointF(e.pos())
            if self.button_background.contains(pos_f):
                super().mousePressEvent(e)
                return
            e.ignore()
            return
        super().mousePressEvent(e)

    def setFlat(self, flat) -> None:
        """Enable 'flat' appearance to the button"""
        if self._is_flat != flat:
            self._is_flat = flat
            self.update()  # Schedule repaint

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        """Recompute cached geometry only when size actually changes"""
        super().resizeEvent(e)
        self._update_geometry()

    def _update_geometry(self) -> None:
        """Rebuild button_ellipse/button_background."""
        rect = self.rect().toRectF().normalized()
        height = rect.height()

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            0,
            0,
            rect.width(),
            height,
            height / 2.0,
            height / 2.0,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        self.button_ellipse = QtCore.QRectF(
            rect.left() + height * 0.05,
            rect.top() + height * 0.05,
            height * 0.90,
            height * 0.90,
        )
        icon_path = QtGui.QPainterPath()
        icon_path.addEllipse(self.button_ellipse)
        self.button_background = path.subtracted(icon_path)

    def setAutoDefault(self, _):
        """Disable auto default behavior"""
        return

    def setProperty(self, name: str, value: typing.Any):
        """Set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        if name == "name":
            self._name = value
        if name == "text_color":
            self.text_color = QtGui.QColor(value)
        self.update()

    def paintEvent(self, e: QtGui.QPaintEvent | None):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        _rect = self.rect()
        _style = self.style()
        if not _style or not _rect:
            return
        opt = QtWidgets.QStyleOptionButton()
        if (
            not self._is_flat
            or self.underMouse()
            or opt.state & QtWidgets.QStyle.StateFlag.State_Sunken
        ):
            _style.drawControl(
                QtWidgets.QStyle.ControlElement.CE_PushButtonLabel, opt, painter, self
            )
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

        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)

        if self.button_background is None:
            self._update_geometry()

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(self.button_background, bg_color)

        if not self.icon_pixmap.isNull():
            self._paint_pixmap(painter, bg_color)

        if self.text():
            self._paint_text(painter, _rect, current_text_color)

        if self._show_notification:
            self._paint_notification(painter)

        painter.end()

    def _paint_pixmap(self, painter: QtGui.QPainter, bg_color: QtGui.QColor) -> None:

        hole = self.button_ellipse
        icon_size = hole.width() * 0.80
        _icon_rect = QtCore.QRectF(
            hole.center().x() - icon_size / 2.0,
            hole.center().y() - icon_size / 2.0,
            icon_size,
            icon_size,
        )
        # Rescale only when the target size changes; it is fixed between resizes
        target_size = _icon_rect.size().toSize()
        if target_size != self._icon_cache_size:
            self._icon_cache = self.icon_pixmap.scaled(
                target_size,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            self._icon_cache_size = target_size
        _icon_scaled = self._icon_cache
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
        if not self.isEnabled():
            tinted_icon_pixmap = QtGui.QPixmap(_icon_scaled.size())
            tinted_icon_pixmap.fill(QtCore.Qt.GlobalColor.transparent)
            icon_painter = QtGui.QPainter(tinted_icon_pixmap)
            icon_painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            icon_painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
            icon_painter.drawPixmap(0, 0, _icon_scaled)
            icon_painter.setCompositionMode(
                QtGui.QPainter.CompositionMode.CompositionMode_SourceAtop
            )
            tint = QtGui.QColor(bg_color.red(), bg_color.green(), bg_color.blue(), 120)
            icon_painter.fillRect(tinted_icon_pixmap.rect(), tint)
            icon_painter.end()
            final_pixmap = tinted_icon_pixmap
        else:
            final_pixmap = _icon_scaled
        destination_point = adjusted_icon_rect.toRect().topLeft()
        painter.drawPixmap(destination_point, final_pixmap)

    def _paint_text(
        self, painter: QtGui.QPainter, rect: QtCore.QRect, text_color: QtGui.QColor
    ) -> None:
        content_left = int(self.button_ellipse.right())
        right_margin = int(rect.height() * 0.25)
        _text_rect = QtCore.QRect(
            content_left,
            rect.top(),
            max(self.width() - content_left - right_margin, 0),
            rect.height(),
        )
        _pen = painter.pen()
        _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
        _pen.setWidth(1)
        _pen.setColor(text_color)
        painter.setPen(_pen)

        text = str(self.text())
        _metrics = painter.fontMetrics()
        text_width = max(
            (_metrics.horizontalAdvance(line) for line in text.split("\n")),
            default=0,
        )
        if text_width <= _text_rect.width():
            align = QtCore.Qt.AlignmentFlag.AlignCenter
        else:
            align = (
                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
            )

        painter.drawText(
            _text_rect,
            QtCore.Qt.TextFlag.TextShowMnemonic
            | QtCore.Qt.TextFlag.TextDontClip
            | align,
            text,
        )
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

    def _paint_notification(self, painter: QtGui.QPainter) -> None:
        dot_diameter = min(14, self.height() * 0.35)
        dot_x = self.width() - dot_diameter
        notification_color = QtGui.QColor(*ButtonColors.NOTIFICATION_DOT.value)
        painter.setBrush(notification_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        dot_rect = QtCore.QRectF(dot_x, 0, dot_diameter, dot_diameter)
        painter.drawEllipse(dot_rect)
