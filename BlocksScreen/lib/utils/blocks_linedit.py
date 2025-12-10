import typing
from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksCustomLinEdit(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()

    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super(BlocksCustomLinEdit, self).__init__(parent)

        self.button_background = None
        self.button_ellipse = None
        self._text: str = ""
        self.placeholder_str = "Type here"
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(0, 0, 0)
        self.secret: bool = False
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def name(self):
        """Widget name"""
        return self._name

    @name.setter
    def name(self, new_name) -> None:
        self._name = new_name
        self.setObjectName(new_name)

    def setText(self, text: str) -> None:
        """Set widget text"""
        super().setText(text)

    def setHidden(self, hidden: bool) -> None:
        """Hide widget text"""
        self.secret = hidden
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        self.clicked.emit()
        super().mousePressEvent(event)

    def paintEvent(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)

        # Draw background
        bg_color = QtGui.QColor(223, 223, 223)
        painter.setBrush(bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 8, 8)

        margin = 5
        display_text = self.text()
        if self.secret and display_text:
            display_text = "*" * len(display_text)

        if self.text():
            painter.setPen(self.text_color)
            painter.drawText(
                self.rect().adjusted(margin, 0, 0, 0),
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            painter.setPen(QtGui.QColor(150, 150, 150))
            painter.drawText(
                self.rect().adjusted(margin, 0, 0, 0),
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self.placeholder_str,
            )
