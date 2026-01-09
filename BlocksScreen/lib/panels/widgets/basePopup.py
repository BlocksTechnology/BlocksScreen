import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class BasePopup(QtWidgets.QDialog):
    """Simple  popup with custom message and Confirm/Back buttons

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
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog | 
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def _update_button_style(self) -> None:
        """Applies the current color variables and adds the central border to the stylesheets."""
        if not self.dialog:
            return



        if not self.floating:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border: none;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border: none;
                padding: 10px;
                """
            )
        else:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border-top: none; 
                border-left: 2px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 1px solid #80807e; 
                border-bottom-left-radius: 16px;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border-left: 1px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 2px solid #80807e; 
                border-bottom-right-radius: 16px;
                padding: 10px;
                """
            )

    def set_message(self, message: str) -> None:
        self.label.setText(message)

    def cancel_button_text(self, text: str) -> None:
        if not self.dialog:
            return
        self.cancel_button.setText(text)

    def confirm_button_text(self, text: str) -> None:
        if not self.dialog:
            return
        self.confirm_button.setText(text)

    def cancel_background_color(self, color: str) -> None:
        if not self.dialog:
            return
        self.cancel_bk_color = color
        self._update_button_style()

    def confirm_background_color(self, color: str) -> None:
        if not self.dialog:
            return
        self.confirm_bk_color = color
        self._update_button_style()

    def cancel_font_color(self, color: str) -> None:
        if not self.dialog:
            return
        self.cancel_ft_color = color
        self._update_button_style()

    def confirm_font_color(self, color: str) -> None:
        if not self.dialog:
            return
        self.confirm_ft_color = color
        self._update_button_style()

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        layout = self.vlayout
        index = layout.indexOf(self.label)
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(index, widget)
        widget.show()

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
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

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

    def open(self):
        """Re-implemented method, open widget"""
        self._geometry_calc()
        return super().open()

    def show(self) -> None:
        self._geometry_calc()
        return super().show()

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def setupUI(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()
