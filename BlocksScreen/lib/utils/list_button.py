from PyQt6 import QtCore, QtGui, QtWidgets


class ListCustomButton(QtWidgets.QPushButton):
    def __init__(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.second_icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.pressed_color = "#1A8FBF"
        self._text = ""
        self._right_text = ""

        self._rfontsize = 15
        self._lfontsize = 11

        self._is_pressed = False
        self._is_hovered = False

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )

        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        # Paint caches, invalidated on resize/font/color change
        self._bg_path: QtGui.QPainterPath | None = None
        self._icon_cache: QtGui.QPixmap | None = None
        self._icon_cache_size: QtCore.QSize = QtCore.QSize()
        self._left_icon_cache: QtGui.QPixmap | None = None
        self._left_icon_cache_size: QtCore.QSize = QtCore.QSize()
        self._fonts: (
            tuple[QtGui.QFont, QtGui.QFont, QtGui.QFontMetrics, QtGui.QFontMetrics]
            | None
        ) = None
        self._fill_colors: tuple[QtGui.QColor, QtGui.QColor] | None = None
        self._fill_key: str = ""
        self._right_text_color = QtGui.QColor(160, 160, 160)

    def _invalidate_fonts(self) -> None:
        """Drop the font and metrics caches"""
        self._fonts = None

    def changeEvent(self, a0: QtCore.QEvent | None) -> None:
        """Re-implemented method, drop the font caches when the font changes"""
        if a0 is not None and a0.type() == QtCore.QEvent.Type.FontChange:
            self._invalidate_fonts()
        super().changeEvent(a0)

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, drop every size-dependent cache"""
        self._bg_path = None
        self._icon_cache_size = QtCore.QSize()
        self._left_icon_cache_size = QtCore.QSize()
        super().resizeEvent(a0)

    def setText(self, text: str) -> None:
        """Set widget text"""
        self._text = text
        self.update()

    def text(self) -> str:
        """Widget text"""
        return self._text

    def setRightText(self, text: str) -> None:
        """Set widget right text"""
        self._right_text = text
        self.update()

    def rightText(self) -> str:
        """Widget right text"""
        return self._right_text

    def setLeftFontSize(self, size: int) -> None:
        """Set widget left text font size"""
        self._lfontsize = size
        self._invalidate_fonts()
        self.update()

    def setRightFontSize(self, size: int) -> None:
        """Set widget right text font size"""
        self._rfontsize = size
        self._invalidate_fonts()
        self.update()

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = pixmap
        self._icon_cache_size = QtCore.QSize()
        self.update()

    def setSecondPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget secondary pixmap"""
        self.second_icon_pixmap = pixmap
        self._left_icon_cache_size = QtCore.QSize()
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press event"""
        self._is_pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse release event"""
        self._is_pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        """Re-implemented method, handle leave event"""
        self._is_hovered = False
        self.update()
        super().leaveEvent(event)

    def _text_fonts(
        self,
    ) -> tuple[QtGui.QFont, QtGui.QFont, QtGui.QFontMetrics, QtGui.QFontMetrics]:
        """Cached left/right fonts and their metrics"""
        if self._fonts is None:
            left = QtGui.QFont(self.font())
            left.setPointSize(self._lfontsize)
            right = QtGui.QFont(left)
            right.setPointSize(self._rfontsize)
            self._fonts = (
                left,
                right,
                QtGui.QFontMetrics(left),
                QtGui.QFontMetrics(right),
            )
        return self._fonts

    def _fills(self) -> tuple[QtGui.QColor, QtGui.QColor]:
        """Cached idle/pressed background colors"""
        if self._fill_colors is None or self._fill_key != self.pressed_color:
            idle = QtGui.QColor(self.pressed_color)
            idle.setAlpha(20)
            down = QtGui.QColor(self.pressed_color)
            down.setAlpha(90)
            self._fill_colors = (idle, down)
            self._fill_key = self.pressed_color
        return self._fill_colors

    def paintEvent(self, e: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)

        rect = self.rect()
        radius = rect.height() / 5.0

        # Main rounded rectangle path (using the adjusted rect)
        if self._bg_path is None:
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(rect), radius, radius)
            self._bg_path = path
        path = self._bg_path

        # Ellipse ("hole") for the icon on the right
        ellipse_margin = rect.height() * 0.05
        ellipse_size = rect.height() * 0.90
        ellipse_rect = QtCore.QRectF(
            rect.right() - ellipse_margin - ellipse_size,
            rect.top() + ellipse_margin,
            ellipse_size,
            ellipse_size,
        )
        self.button_ellipse = ellipse_rect

        # Ellipse ("hole") for the icon on the left (only if present)
        left_icon_margin = rect.height() * 0.05
        left_icon_size = rect.height() * 0.50
        left_icon_rect = QtCore.QRectF(
            rect.left() + left_icon_margin,
            rect.top() + left_icon_margin,
            left_icon_size,
            left_icon_size,
        )
        left_margin = 10  # default left margin

        # Gradient background (left to right)
        idle_color, down_color = self._fills()
        fill_color = down_color if self._is_pressed else idle_color
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(fill_color)
        painter.fillPath(path, fill_color)

        # Draw icon inside the ellipse "hole" (on the right)
        if not self.icon_pixmap.isNull():
            icon_margin = ellipse_size * 0.10
            icon_rect = QtCore.QRectF(
                ellipse_rect.left() + icon_margin / 2,
                ellipse_rect.top() + icon_margin / 2,
                ellipse_rect.width() - icon_margin,
                ellipse_rect.height() - icon_margin,
            )
            target = icon_rect.size().toSize()
            if self._icon_cache is None or target != self._icon_cache_size:
                self._icon_cache = self.icon_pixmap.scaled(
                    target,
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
                self._icon_cache_size = target
            icon_scaled = self._icon_cache
            # Center the icon in the ellipse
            adjusted_x = icon_rect.x() + (icon_rect.width() - icon_scaled.width()) / 2.0
            adjusted_y = (
                icon_rect.y() + (icon_rect.height() - icon_scaled.height()) / 2.0
            )
            adjusted_icon_rect = QtCore.QRectF(
                adjusted_x,
                adjusted_y,
                icon_scaled.width(),
                icon_scaled.height(),
            )
            painter.drawPixmap(
                adjusted_icon_rect, icon_scaled, icon_scaled.rect().toRectF()
            )

        # Draw second icon (on the left, if present)
        if not self.second_icon_pixmap.isNull():
            left_target = left_icon_rect.size().toSize()
            if (
                self._left_icon_cache is None
                or left_target != self._left_icon_cache_size
            ):
                self._left_icon_cache = self.second_icon_pixmap.scaled(
                    left_target,
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
                self._left_icon_cache_size = left_target
            left_icon_scaled = self._left_icon_cache
            # Center the icon in the rect
            adjusted_x = (
                left_icon_rect.x()
                + (left_icon_rect.width() - left_icon_scaled.width()) // 2.0
            )
            adjusted_y = (self.height() - left_icon_rect.height()) // 2.0
            adjusted_left_icon_rect = QtCore.QRectF(
                adjusted_x,
                adjusted_y,
                left_icon_scaled.width(),
                left_icon_scaled.height(),
            )
            painter.drawPixmap(
                adjusted_left_icon_rect,
                left_icon_scaled,
                left_icon_scaled.rect().toRectF(),
            )
            left_margin = left_icon_margin + left_icon_size + 8  # 8px gap after icon

        # Draw text, area before the ellipse (adjusted for left icon)
        text_margin = int(
            rect.right() - ellipse_size - ellipse_margin - rect.height() * 0.10
        )
        text_rect = QtCore.QRectF(
            rect.left() + left_margin,
            rect.top(),
            text_margin - rect.left() - left_margin,
            rect.height(),
        )

        # Draw main text (left-aligned)
        painter.setPen(self.text_color)
        _font, right_font, metrics, right_metrics = self._text_fonts()
        painter.setFont(_font)
        main_text_height = metrics.height()

        # Vertically center text
        text_y = rect.top() + (rect.height() + main_text_height) / 2 - metrics.descent()

        # Calculate where to start the right text: just left of the right icon ellipse
        gap = 10  # gap between right text and icon ellipse
        right_text_width = right_metrics.horizontalAdvance(self._right_text)

        # The right text should end at ellipse_rect.left() - gap
        right_text_x = ellipse_rect.left() - gap - right_text_width

        # Draw main text (left-aligned, but don't overlap right text)
        max_main_text_width = (
            right_text_x - text_rect.left() - 10
        )  # 10px gap between main and right text
        elided_main_text = metrics.elidedText(
            self._text,
            QtCore.Qt.TextElideMode.ElideRight,
            int(max_main_text_width),
        )

        painter.drawText(
            int(text_rect.left()),
            int(text_y),
            elided_main_text,
        )

        # Draw right text (smaller, grey, just left of the icon)
        if self._right_text:
            painter.setFont(right_font)
            painter.setPen(self._right_text_color)  # grey color
            right_text_height = right_metrics.height()
            right_text_y = (
                rect.top()
                + (rect.height() + right_text_height) / 2
                - right_metrics.descent()
            )
            painter.drawText(
                int(right_text_x),
                int(right_text_y),
                self._right_text,
            )

        painter.end()
