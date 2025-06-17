import typing
from PyQt6 import QtWidgets, QtCore, QtGui
import enum
import sys


class ToggleAnimatedButton(QtWidgets.QAbstractButton):
    class State(enum.Enum):
        ON = True
        OFF = False

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(100, 40))
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self.setMaximumHeight(80)
        self.setMouseTracking(True)
        self.setMinimumSize(
            QtCore.QSize(self.parent().height(), self.parent().height())  # type: ignore
        )
        self.setMaximumSize(
            QtCore.QSize(self.parent().height(), self.parent().height())  # type: ignore
        )
        self._handle_position = float(
            (self.contentsRect().toRectF().normalized().width() * 0.20) // 2
        )
        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._backgroundColor: QtGui.QColor = QtGui.QColor(223, 223, 223)
        self._handleColor: QtGui.QColor = QtGui.QColor(255, 100, 10)
        self._state = ToggleAnimatedButton.State.OFF

        self.slide_animation = QtCore.QPropertyAnimation(
            self, b"handle_position"
        )  # type: ignore
        self.slide_animation.setDuration(500)
        self.slide_animation.setEasingCurve(QtCore.QEasingCurve().Type.OutQuad)
        self.clicked.connect(self.setup_animation)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(80, 40)

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, new_state: State) -> None:
        self._state = ToggleAnimatedButton.State(new_state)
        self.update()

    @QtCore.pyqtProperty(float)  # type: ignore
    def handle_position(self) -> float:  # type: ignore
        return self._handle_position

    @handle_position.setter
    def handle_position(self, new_pos: float) -> None:
        self._handle_position = new_pos
        self.update()

    @QtCore.pyqtProperty(QtGui.QColor)  # type: ignore
    def backgroundColor(self) -> QtGui.QColor:  # type: ignore
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, new_color: QtGui.QColor) -> None:
        self._backgroundColor = new_color
        self.update()

    @QtCore.pyqtProperty(QtGui.QColor)
    def handleColor(self) -> QtGui.QColor:
        return self._handleColor

    @handleColor.setter
    def handleColor(self, new_color: QtGui.QColor) -> None:
        self._handleColor = new_color
        self.update()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        _rect = self.contentsRect()
        self.trailPath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        xRadius = _rect.toRectF().normalized().height() // 2.0
        yRadius = _rect.toRectF().normalized().height() // 2.0
        self.trailPath.addRoundedRect(
            0,
            0,
            _rect.toRectF().normalized().width(),
            _rect.toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        self.handle_radius = (
            _rect.toRectF().normalized().height() * 0.80
        ) // 2
        self._handle_position = float(
            (_rect.toRectF().normalized().height() * 0.20) // 2
        )
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        return super().showEvent(a0)

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        self.icon_pixmap = pixmap
        self.repaint()

    @QtCore.pyqtSlot(name="clicked")
    def setup_animation(self) -> None:
        if (
            self.slide_animation.state() == self.slide_animation.State.Stopped
            or self.slide_animation.state()
            == self.slide_animation.State.Paused
        ):
            self.slide_animation.setEndValue(
                int(
                    (
                        self.contentsRect().toRectF().normalized().height()
                        * 0.20
                    )
                    // 2
                )
                if self._state == ToggleAnimatedButton.State.ON
                else int(
                    self.contentsRect().width()
                    - self._handle_position
                    - self.handle_radius * 2
                ),
            )
            self.slide_animation.start()
            self._state = ToggleAnimatedButton.State(not self._state.value)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if self.trailPath:
            if self.trailPath.contains(e.pos().toPointF()):
                super().mousePressEvent(e)
            else:
                e.ignore()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        option = QtWidgets.QStyleOptionButton()
        option.initFrom(self)
        option.state |= QtWidgets.QStyle.StateFlag.State_Off  # Add off effect
        option.state |= QtWidgets.QStyle.StateFlag.State_On  # Add on effect
        option.state |= QtWidgets.QStyle.StateFlag.State_Active
        _rect = self.contentsRect()
        bg_color = (
            self.backgroundColor.darker(160)
            if self.isDown()
            else self.backgroundColor
        )
        self.handlePath: QtGui.QPainterPath = QtGui.QPainterPath()
        self.handle_ellipseRect = QtCore.QRectF(
            self._handle_position,
            ((_rect.toRectF().normalized().height() * 0.20) // 2),
            (_rect.toRectF().normalized().height() * 0.80),
            (_rect.toRectF().normalized().height() * 0.80),
        )
        self.handlePath.addEllipse(self.handle_ellipseRect)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setBackgroundMode(QtCore.Qt.BGMode.TransparentMode)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)
        painter.fillPath(self.trailPath, bg_color)
        painter.fillPath(self.handlePath, self.handleColor)
        if not self.icon_pixmap.isNull():
            _icon_rect = QtCore.QRectF(
                self.handle_ellipseRect.left() * 2.8,
                self.handle_ellipseRect.top() * 2.8,
                self.handle_ellipseRect.width() * 0.90,
                self.handle_ellipseRect.height() * 0.90,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Calculate the actual QRect for the scaled pixmap (centering it if needed)
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
                adjusted_icon_rect,  # Target area (center adjusted)
                _icon_scaled,  # Scaled pixmap
                _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
            )
        painter.end()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.setGeometry(QtCore.QRect(0, 0, 720, 410))
        self.slider = ToggleAnimatedButton(self)
        self.slider.setMinimumSize(QtCore.QSize(100, 40))
        self.slider.setMaximumSize(QtCore.QSize(100, 40))
        center_x = (self.width() - self.slider.width()) // 2
        center_y = (self.height() - self.slider.height()) // 2

        self.slider.move(QtCore.QPoint(center_x, center_y))

        # self.slider.handle.setState(ToggleHandle.State.ON)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
