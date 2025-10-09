import enum
import typing
from PyQt6 import QtCore, QtGui, QtWidgets


class ButtonColors(enum.Enum):
    NORMAL_BG = (223, 223, 223)
    PRESSED_BG = (169, 169, 169)
    DISABLED_BG = (169, 169, 169)
    TEXT_COLOR = (0, 0, 0)
    DISABLED_TEXT_COLOR = (102, 102, 102)
    NOTIFICATION_DOT = (226, 31, 31)


class BlocksCustomButton(QtWidgets.QAbstractButton):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        self.icon_pixmap = QtGui.QPixmap()
        self._text = ""
        self._name = ""
        self._show_notification = False

        self.button_background: typing.Optional[QtGui.QPainterPath] = None
        self.button_ellipse: typing.Optional[QtCore.QRectF] = None

        self.text_color = QtGui.QColor(*ButtonColors.TEXT_COLOR.value)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name
        self.setObjectName(new_name)

    def text(self) -> str:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text
        self.update()

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        self.icon_pixmap = pixmap
        self.update()

    def setShowNotification(self, show: bool) -> None:
        if self._show_notification != show:
            self._show_notification = show
            self.update()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if not self.isEnabled():
            e.ignore()
            return

        if self.button_background and not self.button_background.contains(QtCore.QPointF(e.pos())):
            e.ignore()
            return

        super().mousePressEvent(e)

    def event(self, e: QtCore.QEvent) -> bool:
        match e.type():
            case QtCore.QEvent.Type.TouchBegin:
                self.handleTouchBegin(e)
                return False
            case QtCore.QEvent.Type.TouchUpdate:
                self.handleTouchUpdate(e)
                return False
            case QtCore.QEvent.Type.TouchEnd:
                self.handleTouchEnd(e)
                return False
            case QtCore.QEvent.Type.TouchCancel:
                self.handleTouchCancel(e)
                return False
            case _:
                return super().event(e)


    def paintEvent(self, _: typing.Optional[QtGui.QPaintEvent]) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing
            | QtGui.QPainter.RenderHint.SmoothPixmapTransform
            | QtGui.QPainter.RenderHint.LosslessImageRendering
        )

        rect = self.rect().toRectF()
        style = self.style()
        if style is None:
            return

        bg_color, text_color = self._resolve_colors()
        self._draw_button_background(painter, rect, bg_color)
        self._draw_icon(painter, style, rect)
        self._draw_text(painter, style, rect, text_color)

        if self._show_notification:
            self._draw_notification_dot(painter, rect)

    def _resolve_colors(self) -> tuple[QtGui.QColor, QtGui.QColor]:
        if not self.isEnabled():
            return (
                QtGui.QColor(*ButtonColors.DISABLED_BG.value),
                QtGui.QColor(*ButtonColors.DISABLED_TEXT_COLOR.value),
            )
        if self.isDown():
            return (
                QtGui.QColor(*ButtonColors.PRESSED_BG.value),
                self.text_color,
            )
        return (
            QtGui.QColor(*ButtonColors.NORMAL_BG.value),
            self.text_color,
        )

    def _draw_button_background(self, painter: QtGui.QPainter, rect: QtCore.QRectF, bg_color: QtGui.QColor):
        radius = rect.height() / 2.0
        outer_path = QtGui.QPainterPath()
        outer_path.addRoundedRect(rect, radius, radius, QtCore.Qt.SizeMode.AbsoluteSize)

        ellipse_size = rect.height() * 0.9
        margin = rect.height() * 0.05
        self.button_ellipse = QtCore.QRectF(
            rect.left() + margin,
            rect.top() + margin,
            ellipse_size,
            ellipse_size,
        )

        inner_path = QtGui.QPainterPath()
        inner_path.addEllipse(self.button_ellipse)
        self.button_background = outer_path.subtracted(inner_path)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(self.button_background, bg_color)

    def _draw_icon(self, painter: QtGui.QPainter, style: QtWidgets.QStyle, rect: QtCore.QRectF):
        if self.icon_pixmap.isNull() or not self.button_ellipse:
            return

        icon_rect = QtCore.QRectF(
            self.button_ellipse.left() * 2.8,
            self.button_ellipse.top() * 2.8,
            self.button_ellipse.width() * 0.8,
            self.button_ellipse.height() * 0.8,
        )

        icon_scaled = self.icon_pixmap.scaled(
            icon_rect.size().toSize(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

        adjusted_icon_rect = QtCore.QRectF(
            icon_rect.x() + (icon_rect.width() - icon_scaled.width()) / 2,
            icon_rect.y() + (icon_rect.height() - icon_scaled.height()) / 2,
            icon_scaled.width(),
            icon_scaled.height(),
        )

        final_pixmap = (
            self._tint_icon(icon_scaled)
            if not self.isEnabled()
            else icon_scaled
        )

        painter.drawPixmap(adjusted_icon_rect.topLeft().toPoint(), final_pixmap)

    def _tint_icon(self, pixmap: QtGui.QPixmap) -> QtGui.QPixmap:
        tinted = QtGui.QPixmap(pixmap.size())
        tinted.fill(QtCore.Qt.GlobalColor.transparent)

        icon_painter = QtGui.QPainter(tinted)
        icon_painter.setRenderHints(
            QtGui.QPainter.RenderHint.Antialiasing
            | QtGui.QPainter.RenderHint.SmoothPixmapTransform
        )
        icon_painter.drawPixmap(0, 0, pixmap)
        icon_painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceAtop)
        tint = QtGui.QColor(0, 0, 0, 120)
        icon_painter.fillRect(tinted.rect(), tint)
        icon_painter.end()
        return tinted

    def _draw_text(
        self,
        painter: QtGui.QPainter,
        style: QtWidgets.QStyle,
        rect: QtCore.QRectF,
        text_color: QtGui.QColor,
    ):
        if not self._text:
            return

        font_metrics = self.fontMetrics()
        text_width = font_metrics.horizontalAdvance(self._text)
        ellipse_w = self.button_ellipse.width() if self.button_ellipse else 0

        text_rect = QtCore.QRectF(
            ellipse_w,
            0,
            self.width() - ellipse_w * 2,
            self.height(),
        )

        painter.setPen(QtGui.QPen(text_color))

        align_flags = (
            QtCore.Qt.TextFlag.TextShowMnemonic
            | QtCore.Qt.AlignmentFlag.AlignCenter
            if text_width < text_rect.width()
            else QtCore.Qt.TextFlag.TextShowMnemonic
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        painter.drawText(text_rect, align_flags, self._text)

    def _draw_notification_dot(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        dot_diameter = rect.height() * 0.4
        dot_rect = QtCore.QRectF(
            rect.width() - dot_diameter,
            0,
            dot_diameter,
            dot_diameter,
        )

        painter.setBrush(QtGui.QColor(*ButtonColors.NOTIFICATION_DOT.value))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawEllipse(dot_rect)


    def handleTouchBegin(self, e: QtCore.QEvent): ...
    def handleTouchUpdate(self, e: QtCore.QEvent): ...
    def handleTouchEnd(self, e: QtCore.QEvent): ...
    def handleTouchCancel(self, e: QtCore.QEvent): ...
    def setAutoDefault(self, _: bool): ...
    def setFlat(self, _: bool): ...

    def setProperty(self, name: str, value: typing.Any):
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "name":
            self._name = value
        elif name == "text_color":
            self.text_color = QtGui.QColor(value)
            self.update()
