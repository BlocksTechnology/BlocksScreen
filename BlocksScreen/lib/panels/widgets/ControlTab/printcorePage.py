from lib.utils.blocks_button import BlocksCustomButton
from PyQt6 import QtCore, QtGui, QtWidgets


class SwapPrintcorePage(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "background-image: url(:/background/media/1st_background.png);"
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.repaint()

    def setText(self, text: str) -> None:
        """Set widget text"""
        self.label.setText(text)
        self.repaint()

    def text(self) -> str:
        """Return current widget text"""
        return self.label.text()

    def _geometry_calc(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def sizeHint(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def show(self) -> None:
        """Re-implemented method, widget show"""
        self._geometry_calc()
        self.repaint()
        return super().show()

    def _setupUI(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")
