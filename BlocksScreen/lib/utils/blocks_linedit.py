import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksCustomLinEdit(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()

    # Layout constants
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

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

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

    def _get_text_rect(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 0, -right_margin, 0)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse press """
        self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse release"""
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
