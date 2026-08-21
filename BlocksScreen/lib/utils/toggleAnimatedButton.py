import enum
import typing

from PyQt6 import QtCore, QtGui, QtWidgets


class ToggleAnimatedButton(QtWidgets.QAbstractButton):
    class State(enum.Enum):
        ON = True
        OFF = False

    stateChange: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        State, name="state-change"
    )

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(80, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMaximumHeight(80)
        self.setMouseTracking(True)

        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._icon_cache: QtGui.QPixmap = QtGui.QPixmap()
        self._icon_cache_size: QtCore.QSize = QtCore.QSize()
        # Built here too, so paintEvent is safe before the first showEvent.
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect: QtCore.QRectF = QtCore.QRectF()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)

        self._handleONcolor: QtGui.QColor = QtGui.QColor(0, 200, 0)
        self._handleOFFcolor: QtGui.QColor = QtGui.QColor(200, 0, 0)

        self.disable_bg_color: QtGui.QColor = QtGui.QColor("#A9A9A9")
        self.disable_handle_color: QtGui.QColor = QtGui.QColor("#666666")
        self._state = ToggleAnimatedButton.State.OFF
        self._animation_speed: int = 250

        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )

        self.slide_animation = QtCore.QPropertyAnimation(self, b"handle_position")

        self.slide_animation.setDuration(self._animation_speed)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.InOutQuart)
        self.pressed.connect(self.setup_animation)

    def _rebuild_trail(self) -> None:
        """Rebuild the trail path for the current geometry."""
        rect_norm = self.contentsRect().toRectF().normalized()
        radius = rect_norm.height() // 2.0
        self.trailPath = QtGui.QPainterPath()
        self.trailPath.addRoundedRect(
            0,
            0,
            rect_norm.width(),
            rect_norm.height(),
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        self.handle_radius = (
            self.contentsRect().toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_ONPosition = (
            self.contentsRect().toRectF().normalized().height() * 0.20
        ) // 2
        self._handle_OFFPosition = (
            self.contentsRect().width()
            - self._handle_ONPosition
            - self.handle_radius * 2
        )
        self._rebuild_trail()  # trail is geometry-derived, so it must follow a resize
        return super().resizeEvent(a0)

    def sizeHint(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        return QtCore.QSize(80, 40)

    @QtCore.pyqtProperty(int)
    def animation_speed(self) -> int:
        """Widget property animation speed"""
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, new_speed: int) -> None:
        self.slide_animation.setDuration(new_speed)
        self._animation_speed = new_speed

    @property
    def state(self) -> State:
        """Widget property, toggle state"""
        return self._state

    @state.setter
    def state(self, new_state: State) -> None:
        if self._state == new_state:
            return
        self._state = new_state
        if self.isVisible():
            self.stateChange.emit(self._state)
            self.setup_animation()
        self.update()

    @QtCore.pyqtProperty(float)
    def handle_position(self) -> float:
        """Widget property handle position"""
        return self._handle_position

    @handle_position.setter
    def handle_position(self, new_pos: float) -> None:
        self._handle_position = new_pos
        self.update()

    @QtCore.pyqtProperty(QtGui.QColor)
    def backgroundColor(self) -> QtGui.QColor:
        """Widget property background color"""
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, new_color: QtGui.QColor) -> None:
        self._backgroundColor = new_color
        self.update()

    @QtCore.pyqtProperty(QtGui.QColor)
    def handleColor(self) -> QtGui.QColor:
        """Widget property handle color"""
        return self._handleColor

    @handleColor.setter
    def handleColor(self, new_color: QtGui.QColor) -> None:
        self._handleColor = new_color
        self.update()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, widget show"""
        _rect = self.contentsRect()
        self._rebuild_trail()
        self._handle_position = (
            self._handle_ONPosition
            if self.state == ToggleAnimatedButton.State.OFF
            else self._handle_OFFPosition
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = pixmap
        self._icon_cache = QtGui.QPixmap()
        self._icon_cache_size = QtCore.QSize()
        self.update()

    @QtCore.pyqtSlot(name="clicked")
    def setup_animation(self) -> None:
        """Setup widget animation"""
        if not self.slide_animation.state == self.slide_animation.State.Running:
            self.slide_animation.setEndValue(
                self._handle_ONPosition
                if self.state == ToggleAnimatedButton.State.OFF
                else self._handle_OFFPosition
            )
            self.slide_animation.start()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press events"""
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()) and self.underMouse():
                if not self.slide_animation.state == self.slide_animation.State.Running:
                    self._state = ToggleAnimatedButton.State(not self._state.value)
                    self.stateChange.emit(self._state)
                    super().mousePressEvent(e)
        e.ignore()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        rect_norm = self.contentsRect().toRectF().normalized()
        bg_color = self.backgroundColor
        handle_size = rect_norm.height() * 0.80
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((rect_norm.height() * 0.20) // 2),
            handle_size,
            handle_size,
        )
        self.handlePath.clear()
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)

        min_x = rect_norm.x()
        max_x = rect_norm.x() + rect_norm.width() - rect_norm.height() * 0.80
        progress = (self._handle_position - min_x) / (max_x - min_x)
        progress = max(0.0, min(1.0, progress))

        r = (
            self._handleOFFcolor.red()
            + (self._handleONcolor.red() - self._handleOFFcolor.red()) * progress
        )
        g = (
            self._handleOFFcolor.green()
            + (self._handleONcolor.green() - self._handleOFFcolor.green()) * progress
        )
        b = (
            self._handleOFFcolor.blue()
            + (self._handleONcolor.blue() - self._handleOFFcolor.blue()) * progress
        )
        a = (
            self._handleOFFcolor.alpha()
            + (self._handleONcolor.alpha() - self._handleOFFcolor.alpha()) * progress
        )

        computed_handle_color = QtGui.QColor(int(r), int(g), int(b), int(a))
        self._handleColor = computed_handle_color

        painter.fillPath(
            self.trailPath,
            bg_color if self.isEnabled() else self.disable_bg_color,
        )
        painter.fillPath(
            self.handlePath,
            computed_handle_color if self.isEnabled() else self.disable_handle_color,
        )

        if not self.icon_pixmap.isNull():
            painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            target_size = _icon_rect.size().toSize()
            if target_size != self._icon_cache_size:
                self._icon_cache = self.icon_pixmap.scaled(
                    target_size,
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
                self._icon_cache_size = target_size
            _icon_scaled = self._icon_cache
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) // 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) // 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )
        painter.end()
