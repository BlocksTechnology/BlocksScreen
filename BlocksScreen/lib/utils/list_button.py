from PyQt6 import QtCore, QtGui, QtWidgets


class ListCustomButton(QtWidgets.QPushButton):
    def __init__(self, parent) -> None:
        super(ListCustomButton, self).__init__(parent)
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

    def setText(self, text: str) -> None:
        self._text = text
        self.update()

    def setRightText(self, text: str) -> None:
        self._right_text = text
        self.update()

    def setLeftFontSize(self, size: int) -> None:
        self._lfontsize = size
        self.update()

    def setRightFontSize(self, size: int) -> None:
        self._rfontsize = size
        self.update()

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        self.icon_pixmap = pixmap
        self.update()

    def setSecondPixmap(self, pixmap: QtGui.QPixmap) -> None:
        self.second_icon_pixmap = pixmap
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self._is_pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self._is_pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self._is_hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, e: QtGui.QPaintEvent | None) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        rect = self.rect()
        radius = rect.height() / 5.0

        # Main rounded rectangle path
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(rect), radius, radius)

        # Ellipse ("hole") for the icon on the right
        ellipse_margin = rect.height() * 0.05
        ellipse_size = rect.height() * 0.90
        ellipse_rect = QtCore.QRectF(
            rect.right() - ellipse_margin - ellipse_size,
            rect.top() + ellipse_margin,
            ellipse_size,
            ellipse_size,
        )
        ellipse_path = QtGui.QPainterPath()
        ellipse_path.addEllipse(ellipse_rect)
        self.button_ellipse = ellipse_rect

        # Ellipse ("hole") for the icon on the left (only if present)
        left_icon_margin = rect.height() * 0.05
        left_icon_size = rect.height() * 0.90
        left_icon_rect = QtCore.QRectF(
            rect.left() + left_icon_margin,
            rect.top() + left_icon_margin,
            left_icon_size,
            left_icon_size,
        )
        left_margin = 10  # default left margin

        # Gradient background (left to right)
        if not self._is_pressed:
            pressed_color = QtGui.QColor(self.pressed_color)
            pressed_color.setAlpha(20)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(pressed_color)
            painter.fillPath(path, pressed_color)
        else:
            pressed_color = QtGui.QColor(self.pressed_color)
            pressed_color.setAlpha(100)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(pressed_color)
            painter.fillPath(path, pressed_color)

        # Draw icon inside the ellipse "hole" (on the right)
        if not self.icon_pixmap.isNull():
            icon_margin = ellipse_size * 0.10
            icon_rect = QtCore.QRectF(
                ellipse_rect.left() + icon_margin / 2,
                ellipse_rect.top() + icon_margin / 2,
                ellipse_rect.width() - icon_margin,
                ellipse_rect.height() - icon_margin,
            )
            icon_scaled = self.icon_pixmap.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Center the icon in the ellipse
            adjusted_x = (
                icon_rect.x() + (icon_rect.width() - icon_scaled.width()) / 2.0
            )
            adjusted_y = (
                icon_rect.y()
                + (icon_rect.height() - icon_scaled.height()) / 2.0
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
            left_icon_scaled = self.second_icon_pixmap.scaled(
                left_icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Center the icon in the rect
            adjusted_x = (
                left_icon_rect.x()
                + (left_icon_rect.width() - left_icon_scaled.width()) / 2.0
            )
            adjusted_y = (
                left_icon_rect.y()
                + (left_icon_rect.height() - left_icon_scaled.height()) / 2.0
            )  # <-- FIXED HERE
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
            left_margin = (
                left_icon_margin + left_icon_size + 8
            )  # 8px gap after icon

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
        _font = painter.font()
        _font.setPointSize(self._lfontsize)
        painter.setFont(_font)
        metrics = QtGui.QFontMetrics(_font)
        main_text_height = metrics.height()

        # Vertically center text
        text_y = (
            rect.top()
            + (rect.height() + main_text_height) / 2
            - metrics.descent()
        )

        # Calculate where to start the right text: just left of the right icon ellipse
        gap = 10  # gap between right text and icon ellipse
        right_font = QtGui.QFont(_font)
        right_font.setPointSize(self._rfontsize)
        right_metrics = QtGui.QFontMetrics(right_font)
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

        painter.setFont(_font)
        painter.drawText(
            int(text_rect.left()),
            int(text_y),
            elided_main_text,
        )

        # Draw right text (smaller, grey, just left of the icon)
        if self._right_text:
            painter.setFont(right_font)
            painter.setPen(QtGui.QColor(160, 160, 160))  # grey color
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
