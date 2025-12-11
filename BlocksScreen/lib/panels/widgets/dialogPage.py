import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class DialogPage(QtWidgets.QDialog):
    """Simple confirmation dialog with custom message and Confirm/Back buttons

    To assert if the user accepted or rejected the dialog connect to the **accepted()** or **rejected()** signals.

    The `finished()` signal can also be used to get the result of the dialog. This is emitted after
    the accepted and rejected signals.


    """

    x_offset: float = 0.7
    y_offset: float = 0.7
    border_radius: int = 20
    border_margin: int = 5

    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self._setupUI()
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )  # Make background transparent
        self.setWindowModality(  # Force window modality to block input to other windows
            QtCore.Qt.WindowModality.WindowModal
        )
        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.setModal(True)
        self.update()

    def set_message(self, message: str) -> None:
        """Set dialog text message"""
        self.label.setText(message)

    def _get_mainWindow_widget(self) -> typing.Optional[QtWidgets.QMainWindow]:
        """Get the main application window"""
        app_instance = QtWidgets.QApplication.instance()
        if not app_instance:
            return None
        main_window = app_instance.activeWindow()
        if main_window is None:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        return main_window if isinstance(main_window, QtWidgets.QMainWindow) else None

    def _geometry_calc(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        width = int(main_window.width() * self.x_offset)
        height = int(main_window.height() * self.y_offset)
        x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
        y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        self.setGeometry(x, y, width, height)

    def sizeHint(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle resize event"""
        super().resizeEvent(event)
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return
        width = int(main_window.width() * self.x_offset)
        height = int(main_window.height() * self.y_offset)
        label_x = (self.width() - width) // 2
        label_y = int(height / 4) - 20  # Move the label to the top (adjust as needed)
        self.label.setGeometry(label_x, -label_y, width, height)
        self.confirm_button.setGeometry(
            int(0), self.height() - 70, int(self.width() / 2), 70
        )
        self.cancel_button.setGeometry(
            int(self.width() / 2),
            self.height() - 70,
            int(self.width() / 2),
            70,
        )

    def show(self) -> None:
        """Re-implemented method, show widget"""
        self._geometry_calc()
        return super().show()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(
            QtGui.QBrush(QtGui.QColor(63, 63, 63))
        )  # Semi-transparent dark gray
        border_color = QtGui.QColor(128, 128, 128)  # Gray color
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def _setupUI(self) -> None:
        self.label = QtWidgets.QLabel("Test", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.confirm_button = QtWidgets.QPushButton("Confirm", self)
        self.cancel_button = QtWidgets.QPushButton("Back", self)
        button_font = QtGui.QFont()
        button_font.setPointSize(14)
        self.confirm_button.setFont(button_font)
        self.cancel_button.setFont(button_font)
        self.confirm_button.setStyleSheet(
            """
            background-color: #4CAF50;
            color: white;
            border: none;
            border-bottom-left-radius: 20px;
            padding: 10px;
            """
        )
        self.cancel_button.setStyleSheet(
            """
            background-color: #F44336;
            color: white;
            border: none;
            border-bottom-right-radius: 20px;
            padding: 10px;
            """
        )
        # Position buttons
        self.confirm_button.setGeometry(
            int(0), self.height() - 70, int(self.width() / 2), 70
        )
        self.cancel_button.setGeometry(
            int(self.width() / 2),
            self.height() - 70,
            int(self.width() / 2),
            70,
        )
