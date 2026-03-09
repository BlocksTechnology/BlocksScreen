import enum
from collections import deque
from typing import Deque

from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class BannerPopup(QtWidgets.QWidget):
    class MessageType(enum.Enum):
        """Popup Message type (level)"""

        CONNECT = enum.auto()
        DISCONNECT = enum.auto()
        CORRUPTED = enum.auto()
        UNKNOWN = enum.auto()

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.messages: Deque = deque()
        self.isShown = False
        self.default_background_color = QtGui.QColor(164, 164, 164)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.setMouseTracking(True)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.Tool |
            QtCore.Qt.WindowType.X11BypassWindowManagerHint
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

        self.timeout_timer.setInterval(4000)

        self.slide_out_animation.finished.connect(self.on_slide_out_finished)
        self.slide_in_animation.finished.connect(self.on_slide_in_finished)
        self.timeout_timer.timeout.connect(lambda: self.slide_out_animation.start())
        self.actionbtn.clicked.connect(self.slide_out_animation.start)

    def event(self, a0):
        if a0.type() in (
            QtCore.QEvent.Type.MouseButtonPress,
        ):
            if self.rect().contains(a0.position().toPoint()):
                self.timeout_timer.stop()
                self.slide_out_animation.setStartValue(self.slide_in_animation.currentValue())
                self.slide_in_animation.stop()
                self.slide_out_animation.start()

        return super().event(a0)

    def on_slide_in_finished(self):
        """Handle slide in animation finished"""
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

        width = int(parent_rect.width() * 0.35)
        height = (80
        )

        x = parent_rect.x() + parent_rect.width() - width + 50
        y = parent_rect.y() + 30

        return QtCore.QRect(x, y, width, height)

    def updateMask(self) -> None:
        """Update widget mask properties"""
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 10)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def mousePressEvent(self, a0: QtGui.QMouseEvent | None) -> None:
        """Re-implemented method, handle mouse press events"""
        return

    def new_message(
        self,
        message_type: MessageType = MessageType.CONNECT,
    ):
        """Create new popup message

        Args:
            message_type (MessageType, optional): Message Level, See `MessageType` Types. Defaults to MessageType.CONNECT .
        Returns:
            _type_: _description_
        """
        if len(self.messages) == 4:
            return

        self.messages.append(
            {
                "type": message_type,
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
            message_type = message_entry.get("type")
            
            message = "Unknown Event"
            icon= ":ui/media/btn_icons/info.svg"

            #TODO: missing usb icons
            match message_type:
                case BannerPopup.MessageType.CONNECT:
                     message = "Usb Connected"
                     #icon = ""
                case BannerPopup.MessageType.DISCONNECT:
                     message = "Usb Disconnected"
                     #icon = ""
                case BannerPopup.MessageType.CORRUPTED:
                     message = "Usb Corrupted"
                     icon = ":/ui/media/btn_icons/troubleshoot.svg"
            end_rect = self._calculate_target_geometry()
            start_rect = end_rect.translated(end_rect.width() * 2,0) 

            self.icon_label.setPixmap(QtGui.QPixmap(icon))

            self.slide_in_animation.setStartValue(start_rect)
            self.slide_in_animation.setEndValue(end_rect)
            self.slide_out_animation.setStartValue(end_rect)
            self.slide_out_animation.setEndValue(start_rect)
            self.setGeometry(end_rect)
            self.text_label.setText(message)
            self.show()

    def showEvent(self, a0: QtGui.QShowEvent|None) -> None:
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

        center_point = QtCore.QPointF(self.rect().center())
        gradient = QtGui.QRadialGradient(center_point, self.rect().width() / 2.0)

        gradient.setColorAt(0, _base_color.darker(160))
        gradient.setColorAt(1.0, _base_color.darker(200))

        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 50, 70)

    def _setupUI(self) -> None:
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(5, 5, 5, 5)

        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(60, 60))
        self.icon_label.setMaximumSize(QtCore.QSize(60, 60))
        self.icon_label.setScaledContents(True)

        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setStyleSheet("background: transparent; color:white")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(True)
        font = self.text_label.font()
        font.setPixelSize(18)
        font.setFamily("sans-serif")
        palette = self.text_label.palette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white
        )
        self.text_label.setPalette(palette)
        self.text_label.setFont(font)

        self.actionbtn = IconButton(self)
        self.actionbtn.setMaximumSize(QtCore.QSize(60, 60))

        self.horizontal_layout.addWidget(self.icon_label)
        self.horizontal_layout.addWidget(self.text_label)
        self.horizontal_layout.addWidget(self.actionbtn)
