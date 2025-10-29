from PyQt6 import QtCore, QtGui, QtWidgets


class DialogPage(QtWidgets.QDialog):
    button_clicked = QtCore.pyqtSignal(
        str
    )  # Signal to emit which button was clicked

    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)

        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )  # Make background transparent

        self.setupUI()
        self.repaint()

    def set_message(self, message: str) -> None:
        self.label.setText(message)

    def geometry_calc(self) -> None:
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget

        x_offset = 0.7
        y_offset = 0.7

        width = int(main_window.width() * x_offset)
        height = int(main_window.height() * y_offset)
        self.testwidth = width
        self.testheight = height
        x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
        y = int(
            main_window.geometry().y() + (main_window.height() - height) / 2
        )

        self.setGeometry(x, y, width, height)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        self.geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        rect = self.rect()
        radius = 20  # Adjust the radius for rounded corners

        # Set background color
        painter.setBrush(
            QtGui.QBrush(QtGui.QColor(63, 63, 63))
        )  # Semi-transparent dark gray

        # Set border color and width
        border_color = QtGui.QColor(128, 128, 128)  # Gray color
        border_width = 5  # Reduced border thickness

        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, border_width))

        painter.drawRoundedRect(rect, radius, radius)

        painter.end()

    def sizeHint(self) -> QtCore.QSize:
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        return

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)

        label_width = self.testwidth
        label_height = self.testheight
        label_x = (self.width() - label_width) // 2
        label_y = (
            int(label_height / 4) - 20
        )  # Move the label to the top (adjust as needed)

        self.label.setGeometry(label_x, -label_y, label_width, label_height)

        # Adjust button positions on resize
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
        self.geometry_calc()
        return super().show()

    def setupUI(self) -> None:
        self.label = QtWidgets.QLabel("Test", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        # Create Confirm and Cancel buttons
        self.confirm_button = QtWidgets.QPushButton("Confirm", self)
        self.cancel_button = QtWidgets.QPushButton("Back", self)

        # Set button styles
        button_font = QtGui.QFont()
        button_font.setPointSize(14)
        self.confirm_button.setFont(button_font)
        self.cancel_button.setFont(button_font)

        # Apply styles for rounded corners
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

        # Connect button signals
        self.confirm_button.clicked.connect(
            lambda: self.on_button_clicked("Confirm")
        )
        self.cancel_button.clicked.connect(
            lambda: self.on_button_clicked("Cancel")
        )

    def on_button_clicked(self, button_name: str) -> None:
        self.button_clicked.emit(
            button_name
        )  # Emit the signal with the button name
        if button_name == "Confirm":
            self.accept()  # Close the dialog with an accepted state
        elif button_name == "Cancel":
            self.reject()  # Close the dialog with a rejected state
