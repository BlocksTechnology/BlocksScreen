from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksCustomLinEdit(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()

    # Layout constants
    TEXT_MARGIN = 10
    CORNER_RADIUS = 8
    TEXT_ALIGNMENT = (
        QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
    )

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Size dependent paint state, rebuilt on resize
        self._widget_rect = QtCore.QRect()
        self._text_rect = QtCore.QRect()

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

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, rebuild the cached paint rects"""
        self._widget_rect = self.rect()
        self._text_rect = self._widget_rect.adjusted(
            self.TEXT_MARGIN, 0, -self.TEXT_MARGIN, 0
        )
        super().resizeEvent(a0)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse press"""
        self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse release"""
        super().mouseReleaseEvent(event)

    def paintEvent(self, event: QtGui.QPaintEvent | None) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(
            self._widget_rect, self.CORNER_RADIUS, self.CORNER_RADIUS
        )

        # Text
        self._draw_text(painter)

        painter.end()

    def _draw_text(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
        else:
            display_text = self._placeholder_str
            painter.setPen(self._placeholder_color)

        painter.setFont(self.font())
        painter.drawText(self._text_rect, self.TEXT_ALIGNMENT, display_text)
