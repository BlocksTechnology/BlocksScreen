import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksCustomLinEdit(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()
    visibilityChanged = QtCore.pyqtSignal(bool)

    # Layout constants
    ICON_SIZE = 48
    ICON_MARGIN = 8
    TEXT_MARGIN = 10
    CORNER_RADIUS = 8

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False
        self._icon_pressed = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)
        self._icon_bg_hover = QtGui.QColor(180, 180, 180, 100)

        # Pre-allocated rect for icon (reused in paint)
        self._icon_rect = QtCore.QRectF()

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    @property
    def name(self) -> str:
        """Widget name property."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        self.setObjectName(value)

    def placeholderText(self) -> str:
        """Get placeholder text."""
        return self._placeholder_str

    def setPlaceholderText(self, text: str) -> None:
        """Set placeholder text displayed when empty."""
        self._placeholder_str = text
        self.update()

    def showToggleButton(self) -> bool:
        """Check if toggle button is enabled."""
        return self._show_toggle

    def _create_fallback_icons(self) -> None:
        """Create simple fallback icons if resource files unavailable."""
        size = 32

        # Create "see" icon (simple eye shape)
        self._icon_see = QtGui.QPixmap(size, size)
        self._icon_see.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(self._icon_see)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(80, 80, 80), 2))
        painter.drawEllipse(8, 12, 16, 8)  # Eye outline
        painter.setBrush(QtGui.QColor(80, 80, 80))
        painter.drawEllipse(13, 13, 6, 6)  # Pupil
        painter.end()

        # Create "unsee" icon (eye with line through)
        self._icon_unsee = QtGui.QPixmap(size, size)
        self._icon_unsee.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(self._icon_unsee)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(80, 80, 80), 2))
        painter.drawEllipse(8, 12, 16, 8)
        painter.drawLine(6, 6, 26, 26)  # Strike through
        painter.end()

    def setHidden(self, hidden: bool) -> None:
        """
        Set whether text is hidden (password mode).

        Args:
            hidden: True to show bullets, False to show actual text
        """
        if self._secret == hidden:
            return

        self._secret = hidden
        self._is_password_visible = not hidden
        self.update()

    def isPasswordVisible(self) -> bool:
        """Check if password is currently visible."""
        return self._is_password_visible

    def setPasswordVisible(self, visible: bool) -> None:
        """Set password visibility state."""
        if self._is_password_visible == visible:
            return

        self._is_password_visible = visible
        self._secret = not visible
        self.visibilityChanged.emit(visible)
        self.update()

    def togglePasswordVisibility(self) -> None:
        """Toggle between visible and hidden password."""
        self.setPasswordVisible(not self._is_password_visible)

    def _calculate_icon_rect(self) -> QtCore.QRectF:
        """Calculate the bounding rectangle for the toggle icon."""
        if not self._show_toggle:
            return QtCore.QRectF()

        x = self.width() - self.ICON_SIZE - self.ICON_MARGIN
        y = (self.height() - self.ICON_SIZE) / 2
        return QtCore.QRectF(x, y, self.ICON_SIZE, self.ICON_SIZE)

    def _get_text_rect(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        if self._show_toggle:
            # Reserve space for icon button
            right_margin = self.ICON_SIZE + self.ICON_MARGIN * 2

        return self.rect().adjusted(left_margin, 0, -right_margin, 0)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse press - detect icon clicks."""
        if self._show_toggle:
            self._icon_rect = self._calculate_icon_rect()

            if self._icon_rect.contains(event.position()):
                # Click on toggle icon
                self._icon_pressed = True
                self.update()
                event.accept()
                return

        # Click on text area - emit signal for keyboard
        self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse release - trigger toggle if on icon."""
        if self._icon_pressed:
            self._icon_pressed = False

            if self._icon_rect.contains(event.position()):
                self.togglePasswordVisibility()

            self.update()
            event.accept()
            return

        super().mouseReleaseEvent(event)

    def focusInEvent(self, event: QtGui.QFocusEvent) -> None:
        """Handle focus in - emit clicked for virtual keyboard."""
        self.clicked.emit()
        super().focusInEvent(event)

    def paintEvent(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()

    def _draw_text(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )
