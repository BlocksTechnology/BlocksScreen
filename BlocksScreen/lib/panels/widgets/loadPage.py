import enum
from configfile import BlocksScreenConfig, get_configparser
from PyQt6 import QtCore, QtGui, QtWidgets


class LoadScreen(QtWidgets.QDialog):
    class AnimationGIF(enum.Enum):
        """Animation type"""

        DEFAULT = None
        PLACEHOLDER = ""

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self.anim_type = anim_type
        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self.setStyleSheet(
            "background-image: url(:/background/media/1st_background.png);"
        )

        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        config: BlocksScreenConfig = get_configparser()
        try:
            if config:
                loading_config = config["loading"]
                animation = loading_config.get(
                    str(self.anim_type.name),
                    default=LoadScreen.AnimationGIF.DEFAULT,
                )
        except Exception:
            self.anim_type = LoadScreen.AnimationGIF.DEFAULT

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadScreen.AnimationGIF.PLACEHOLDER:
            self.movie = QtGui.QMovie(animation)  # Create QMovie object
            self.gifshow.setMovie(self.movie)  # Set QMovie to QLabel
            self.movie.start()  # Start the QMovie

        # Only start the animation timer if no GIF is provided
        if self.anim_type == LoadScreen.AnimationGIF.DEFAULT:
            self.timer.start(16)

        self.repaint()

    def set_status_message(self, message: str) -> None:
        """Set widget status message"""
        self.label.setText(message)

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

    def close(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        # Stop the GIF animation if it was started
        if self.anim_type != LoadScreen.AnimationGIF.DEFAULT:
            self.gifshow.movie().stop()
        return super().close()

    def _update_animation(self) -> None:
        self._angle = (self._angle + 5) % 360
        if self._is_span_growing:
            self._span_angle += self.length_step
            if self._span_angle >= self.max_length:
                self._span_angle = self.max_length
                self._is_span_growing = False
        else:
            self._span_angle -= self.length_step
            if self._span_angle <= self.min_length:
                self._span_angle = self.min_length
                self._is_span_growing = True
        self.update()

    def sizeHint(self) -> QtCore.QSize:
        """Re-implemented method, size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        # loading circle draw
        if self.anim_type == LoadScreen.AnimationGIF.DEFAULT:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(
                QtGui.QPainter.RenderHint.LosslessImageRendering, True
            )
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QtGui.QPainter.RenderHint.TextAntialiasing, True)
            pen = QtGui.QPen()
            pen.setWidth(8)
            pen.setColor(QtGui.QColor("#ffffff"))
            pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)

            center_x = self.width() // 2
            center_y = int(self.height() * 0.4)
            arc_size = 150

            painter.translate(center_x, center_y)
            painter.rotate(self._angle)

            arc_rect = QtCore.QRectF(-arc_size / 2, -arc_size / 2, arc_size, arc_size)
            span_angle = int(self._span_angle * 16)
            painter.drawArc(arc_rect, 0, span_angle)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        # Center the GIF
        gifshow_width = self.width() - margin * 2
        gifshow_height = self.height() - (self.height() - label_y) - margin

        self.gifshow.setGeometry(margin, margin, gifshow_width, gifshow_height)

        self.label.setGeometry(label_x, label_y, label_width, label_height)

    def show(self) -> None:
        """Re-implemented method, show widget"""
        self._geometry_calc()
        # Start the animation timer only if no GIF is present
        if self.anim_type == LoadScreen.AnimationGIF.DEFAULT:
            self.timer.start()
        self.repaint()
        return super().show()

    def _setupUI(self) -> None:
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("Test", self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
