from PyQt6 import QtCore, QtGui, QtWidgets
import enum
import os
from configfile import BlocksScreenConfig, get_configparser


class LoadingOverlayWidget(QtWidgets.QLabel):
    """
    A full-overlay widget to display a loading animation (GIF or spinning arc).
    """

    class AnimationGIF(enum.Enum):
        """Animation type"""

        DEFAULT = None
        PLACEHOLDER = "placeholder"

    def __init__(
        self,
        parent: QtWidgets.QWidget,
        initial_anim_type: AnimationGIF = AnimationGIF.DEFAULT,
    ) -> None:
        super().__init__(parent)

        self._angle = 0
        self._span_angle = 90.0
        self._is_span_growing = True
        self.min_length = 5.0
        self.max_length = 150.0
        self.length_step = 2.5

        self._setupUI()

        config: BlocksScreenConfig = get_configparser()
        animation_path = None

        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            animation_path = (
                "~/BlocksScreen/BlocksScreen/lib/ui/resources/intro_blocks.gif"
            )
            self.anim_type = initial_anim_type

        else:
            try:
                loading_config = config.loading
                animation_path = loading_config.get(
                    str(initial_anim_type.name),
                )
                self.anim_type = initial_anim_type
            except Exception:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT

        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and animation_path
        ):
            abs_animation_path = os.path.expanduser(animation_path)

            self.movie = QtGui.QMovie(abs_animation_path)

            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
            else:
                self.anim_type = LoadingOverlayWidget.AnimationGIF.DEFAULT
                self.gifshow.hide()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_animation)

        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
            self.timer.start(16)
            self.gifshow.hide()

        self.label.setText("Loading...")
        self.repaint()

    def set_animation_path(self, path: str) -> None:
        """Set widget animation path"""
        abs_animation_path = os.path.expanduser(path)
        if os.path.isfile(abs_animation_path):
            self.movie = QtGui.QMovie(abs_animation_path)
            if self.movie.isValid():
                self.gifshow.setMovie(self.movie)
                self.gifshow.setScaledContents(True)
                self.movie.start()
                self.gifshow.show()
                self.anim_type = LoadingOverlayWidget.AnimationGIF.PLACEHOLDER
                if self.timer.isActive():
                    self.timer.stop()

    def set_status_message(self, message: str) -> None:
        """Set widget message"""
        self.label.setText(message)

    def close(self) -> bool:
        """Re-implemented method, close widget"""
        self.timer.stop()
        self.label.setText("Loading...")
        self._angle = 0
        if (
            self.anim_type != LoadingOverlayWidget.AnimationGIF.DEFAULT
            and hasattr(self, "movie")
            and self.movie.isValid()
        ):
            self.movie.stop()
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

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        if self.anim_type == LoadingOverlayWidget.AnimationGIF.DEFAULT:
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

        super().paintEvent(a0)

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(a0)
        label_width = self.width()
        label_height = 100
        label_x = (self.width() - label_width) // 2
        label_y = int(self.height() * 0.65)
        margin = 20
        self.label.setGeometry(label_x, label_y, label_width, label_height)
        gifshow_max_height = label_y - margin
        size = min(self.width() - margin * 2, gifshow_max_height)

        gifshow_x = (self.width() - size) // 2
        gifshow_y = (gifshow_max_height - size) // 2

        self.gifshow.setGeometry(gifshow_x, gifshow_y, size, size)

    def show(self) -> None:
        """Re-implemented method, show widget"""
        self.repaint()
        return super().show()

    def _setupUI(self) -> None:
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.gifshow = QtWidgets.QLabel("", self)
        self.gifshow.setObjectName("gifshow")
        self.gifshow.setStyleSheet("background: transparent;")
        self.gifshow.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gifshow.hide()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
