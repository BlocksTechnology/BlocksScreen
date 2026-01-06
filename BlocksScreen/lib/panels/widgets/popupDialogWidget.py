import enum
from collections import deque
from typing import Deque
from PyQt6 import QtCore, QtGui, QtWidgets
from lib.utils.icon_button import IconButton


class Popup(QtWidgets.QDialog):
    class MessageType(enum.Enum):
        """Popup Message type (level)"""

        INFO = enum.auto()
        WARNING = enum.auto()
        ERROR = enum.auto()
        UNKNOWN = enum.auto()

    class ColorCode(enum.Enum):
        """Popup message-color code"""

        INFO = QtGui.QColor("#446CDB")
        WARNING = QtGui.QColor("#E7E147")
        ERROR = QtGui.QColor("#CA4949")

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.persistent_notifications: Deque = deque()
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )
        self._setupUI()
        self.slide_in_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_in_animation.setDuration(1000)
        self.slide_in_animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.slide_out_animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.slide_out_animation.setDuration(200)
        self.slide_out_animation.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)

        self.SingleTime = QtCore.QTimer(self)
        self.SingleTime.setInterval(5000)
        self.SingleTime.setSingleShot(True)
        self.SingleTime.timeout.connect(self._add_popup)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def on_slide_in_finished(self):
        """Handle slide in animation finished"""
        if self.userInput:
            return
        print(self.userInput)
        print(self.text_label.text())
        self.timeout_timer.start()

    def on_slide_out_finished(self):
        """Handle slide out animation finished"""
        self.hide()
        self.isShown = False
        self.timeout_timer.stop()
        self._add_popup()

    def _calculate_target_geometry(self) -> QtCore.QRect:
        """Calculate on end posisition rect for popup"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break

        parent_rect = main_window.geometry()

        width = int(parent_rect.width() * 0.85)
        height = min(self.text_label.rect().height(), self.icon_label.rect().height())

        x = parent_rect.x() + (parent_rect.width() - width) // 2
        y = parent_rect.y() + 20

        return QtCore.QRect(x, y, width, height)

    def updateMask(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.userInput:
            return
        self.timeout_timer.stop()
        self.slide_out_animation.setStartValue(self.slide_in_animation.currentValue())
        self.slide_in_animation.stop()
        self.slide_out_animation.start()

    def new_message(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        timeout: int = 6000,
        userInput: bool = False,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.INFO.
            message (str, optional): The message. Defaults to "".
            timeout (int, optional): How long the message stays for, in milliseconds. Defaults to 0.
            userInput (bool,optional): If the user is required to click to make the popup disappear. Defaults to False.

        Returns:
            _type_: _description_
        """
        self.messages.append(
            {
                "message": message,
                "type": message_type,
                "timeout": timeout,
                "userInput": userInput,
            }
        )
        return self._add_popup()

    def _add_popup(self) -> None:
        """Add popup to queue"""
        if self.isShown:
            if self.SingleTime.isActive():
                return
            self.SingleTime.start()
            return

        if (
            self.messages
            and self.slide_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.slide_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            message = message_entry.get("message")
            timeout = message_entry.get("timeout")
            self.timeout_timer.setInterval(timeout)
            if message == self.text_label.text():
                self.messages = deque(
                    m for m in self.messages if m.get("message") != message
                )
                return
            self.userInput = message_entry.get("userInput")

            self.text_label.setText(message)

            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)

            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(0, -end_rect.height() * 2)

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            if not self.userInput:
                self.actionbtn.clearPixmap()
            else:
                self.actionbtn.setPixmap(
                    QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
                )
            self.setGeometry(end_rect)
            self.show()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        """Re-implementation, widget show"""
        self.slide_in_animation.start()
        self.isShown = True
        super().showEvent(a0)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implementation, handle resize event"""
        self.updateMask()
        super().resizeEvent(a0)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        _base_color = self.default_background_color
        if self.message_type == Popup.MessageType.INFO:
            _base_color = Popup.ColorCode.INFO.value
        elif self.message_type == Popup.MessageType.ERROR:
            _base_color = Popup.ColorCode.ERROR.value
        elif self.message_type == Popup.MessageType.WARNING:
            _base_color = Popup.ColorCode.WARNING.value

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color)
        gradient.setColorAt(1.0, _base_color.darker(160))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def _setupUI(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.horizontal_layout.addWidget(self.icon_label)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.spacer = QtWidgets.QSpacerItem(60, 60)
        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)
