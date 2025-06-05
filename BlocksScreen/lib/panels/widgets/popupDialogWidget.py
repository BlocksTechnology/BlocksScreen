import enum
from collections import deque
import typing
from typing import Deque
from PyQt6 import QtCore, QtGui, QtWidgets
from lib.utils.blocks_label import BlocksLabel

BASE_POPUP_TIMEOUT = 6000


class Popup(QtWidgets.QDialog):
    class MessageType(enum.Enum):
        INFO = enum.auto()
        WARNING = enum.auto()
        ERROR = enum.auto()
        UNKNOWN = enum.auto()

        def __repr__(self) -> str:
            return "<%s.%s>" % (self.__class__.__name__, self._name_)

    class ColorCode(enum.Enum):
        INFO = QtGui.QColor("#446CDB")
        WARNING = QtGui.QColor("#E7E147")
        ERROR = QtGui.QColor("#CA4949")

    popup_timeout = BASE_POPUP_TIMEOUT
    timeout_timer = QtCore.QTimer()
    messages: Deque = deque()
    persistent_notifications: Deque = deque()

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.message_type: Popup.MessageType = Popup.MessageType.INFO
        self.default_background_color = QtGui.QColor(164, 164, 164)
        self.info_icon = QtGui.QPixmap(":ui/media/btn_icons/info.svg")
        self.warning_icon = QtGui.QPixmap(":ui/media/btn_icons/warning.svg")
        self.error_icon = QtGui.QPixmap(":ui/media/btn_icons/error.svg")

        self.setupUI()
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_MouseTracking, True)
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup  # Acts like a popup, click outside closes it
            | QtCore.Qt.WindowType.FramelessWindowHint  # No border or title bar
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.fade_in_animation: QtCore.QPropertyAnimation = (
            QtCore.QPropertyAnimation(self.opacity_effect, b"opacity", self)  # type: ignore
        )
        self.fade_in_animation.setDuration(1500)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(
            QtCore.QEasingCurve.Type.BezierSpline
        )
        self.fade_out_animation: QtCore.QPropertyAnimation = (
            QtCore.QPropertyAnimation(self.opacity_effect, b"opacity", self)  # type: ignore
        )
        self.fade_out_animation.setDuration(1500)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(
            QtCore.QEasingCurve.Type.BezierSpline
        )
        self.opacity_effect.setOpacity(0.0)
        self.fade_out_animation.finished.connect(self.close_popup)
        self.timeout_timer.timeout.connect(self.fade_out_animation.start)

    def sizeHint(self) -> QtCore.QSize:
        available_rect = self.parent().geometry()  # type: ignore
        adjusted_rect = QtCore.QRect(
            available_rect.x(),
            available_rect.y() + 10,
            int(available_rect.width() * 0.80),
            int(available_rect.height() * 0.30),
        )
        centered_x = (available_rect.width() - adjusted_rect.width()) // 2
        self.move(adjusted_rect.x() + centered_x, adjusted_rect.y())
        self.setFixedSize(adjusted_rect.width(), adjusted_rect.height())
        self.setMinimumSize(adjusted_rect.width(), adjusted_rect.height())
        self.repaint()
        return super().sizeHint()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.fade_out_animation.start()

    def set_timeout(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Expected type int ")
        self.popup_timeout = value

    def new_message(
        self,
        message_type: MessageType = MessageType.INFO,
        message: str = "",
        persistent: bool = False,
        timeout: int = 0,
    ):
        self.messages.append(
            {"message": message, "type": message_type, "timeout": timeout}
        )
        return self.add_popup()

    def add_popup(self) -> None:
        if (
            self.messages
            and self.fade_in_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
            and self.fade_out_animation.state()
            == QtCore.QPropertyAnimation.State.Stopped
        ):
            message_entry = self.messages.popleft()
            self.message_type = message_entry.get("type")
            self.message = message_entry.get("message")
            self.timeout = message_entry.get("timeout")
            self.text_label.setText(self.message)
            match self.message_type:
                case Popup.MessageType.INFO:
                    self.icon_label.setPixmap(self.info_icon)
                case Popup.MessageType.WARNING:
                    self.icon_label.setPixmap(self.warning_icon)
                case Popup.MessageType.ERROR:
                    self.icon_label.setPixmap(self.error_icon)
            self.timeout_timer.setInterval(
                self.popup_timeout if not self.timeout else self.timeout
            )
            self.timeout_timer.start()

            self.open()
            self.repaint()

    def close_popup(self):
        if not self.messages:
            self.close()
            self.message_type = self.MessageType.INFO
            self.message = ""
            self.popup_timeout = BASE_POPUP_TIMEOUT
            self.timeout_timer.setInterval(self.popup_timeout)
            return
        self.close()
        return self.add_popup()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        if (
            self.fade_out_animation.state()
            == QtCore.QPropertyAnimation.State.Running
        ):
            self.fade_out_animation.stop()

        super().showEvent(a0)
        self.fade_in_animation.start()

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        if (
            not self.isVisible()
            or self.fade_out_animation.state()
            == QtCore.QPropertyAnimation.State.Running
        ):
            return

        if (
            self.fade_in_animation.state()
            == QtCore.QPropertyAnimation.State.Running
        ):
            self.fade_in_animation.stop()
        self.fade_out_animation.start()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        popup_path = QtGui.QPainterPath()
        popup_path.addRoundedRect(self.rect().toRectF(), 10, 10)
        _background_color = self.default_background_color
        if self.message_type:
            if self.message_type == Popup.MessageType.INFO:
                _background_color = Popup.ColorCode.INFO.value
            elif self.message_type == Popup.MessageType.ERROR:
                _background_color = Popup.ColorCode.ERROR.value
            elif self.message_type == Popup.MessageType.WARNING:
                _background_color = Popup.ColorCode.WARNING.value
        _gradient = QtGui.QRadialGradient(
            self.icon_label.contentsRect().toRectF().center(),
            self.rect().width() // 2 + 50,
            self.icon_label.contentsRect().toRectF().center(),
        )
        _gradient.setColorAt(0, QtGui.QColor(_background_color))
        _gradient.setColorAt(0.9, QtGui.QColor(_background_color).darker(160))
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.TextAntialiasing, True)
        painter.setBrush(_gradient)
        painter.fillPath(popup_path, painter.brush())
        painter.end()

    def setupUI(self) -> None:
        self.setContentsMargins(5, 5, 5, 5)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)
        self.horizontal_layout.addSpacing(6)
        self.horizontal_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.icon_label = BlocksLabel(self)
        self.icon_label.setMinimumSize(QtCore.QSize(80, self.height()))
        self.icon_label.setMaximumSize(QtCore.QSize(80, self.height()))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.icon_label.sizePolicy().hasHeightForWidth()
        )
        self.icon_label.setSizePolicy(sizePolicy)
        self.horizontal_layout.addWidget(
            self.icon_label,
            QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setMinimumSize(QtCore.QSize(300, self.height()))
        sizePolicy.setHeightForWidth(
            self.text_label.sizePolicy().hasHeightForWidth()
        )
        self.text_label.setSizePolicy(sizePolicy)
        self.text_label.setWordWrap(True)
        self.text_label.setMargin(5)
        self.text_label.setContentsMargins(5, 5, 5, 5)
        self.text_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignVCenter
            | QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("mooncake")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)
        self.horizontal_layout.addWidget(
            self.text_label,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.setLayout(self.horizontal_layout)
