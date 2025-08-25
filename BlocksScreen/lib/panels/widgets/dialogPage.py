from PyQt6 import QtCore, QtGui, QtWidgets
from lib.utils.blocks_button import BlocksCustomButton


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

        app_instance = QtWidgets.QApplication.instance()
        self.main_window = (
            app_instance.activeWindow() if app_instance else None
        )
        if self.main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    self.main_window = widget

        offset = 0.7
        self.testwidth = int(self.main_window.width() * offset)
        self.testheight = int(self.main_window.height() * offset)

        self.setupUI()

    def set_message(self, message: str) -> None:
        self.label.setText(message)

    def geometry_calc(self) -> None:
        x = int(
            self.main_window.geometry().x()
            + (self.main_window.width() - self.testwidth) / 2
        )

        y = int(
            self.main_window.geometry().y()
            + (self.main_window.height() - self.testheight) / 2
        )

        self.setGeometry(x, y, self.testwidth, self.testheight)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        rect = self.rect()
        radius = 20  # Adjust the radius for rounded corners

        # Convert the QPoint returned by rect.center() to a QPointF
        center_f = QtCore.QPointF(rect.center())

        # Create a radial gradient
        gradient = QtGui.QRadialGradient(
            center_f, max(rect.width(), rect.height())
        )
        gradient.setColorAt(
            0.0, QtGui.QColor(50, 50, 50)
        )  # Light gray in the center
        gradient.setColorAt(1.0, QtGui.QColor(0, 0, 0))  # Black on the outside

        painter.setBrush(QtGui.QBrush(gradient))

        # Set border color and width
        border_color = QtGui.QColor(128, 128, 128)  # Gray color
        border_width = 1  # Reduced border thickness

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
            int(15), self.height() - 110, int(self.width() / 2) - 40, 70
        )
        self.cancel_button.setGeometry(
            int(self.width() / 2) + 15,
            self.height() - 110,
            int(self.width() / 2) - 40,
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
        self.confirm_button = BlocksCustomButton(self)
        self.cancel_button = BlocksCustomButton(self)

        self.confirm_button.setText("Confirm")
        self.cancel_button.setText("Cancel")

        # Set button styles
        button_font = QtGui.QFont()
        button_font.setPointSize(20)
        self.confirm_button.setFont(button_font)
        self.cancel_button.setFont(button_font)

        self.confirm_button.setPixmap(
            QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.cancel_button.setPixmap(
            QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
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
