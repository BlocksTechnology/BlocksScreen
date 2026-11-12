import enum
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets

_INTRO_GIF = (
    Path(__file__).resolve().parents[3] / "ui" / "resources" / "intro_blocks.gif"
)


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

        self._setup_ui()

        self.movie: QtGui.QMovie | None = None
        self._movie_size = QtCore.QSize()
        # Started by showEvent: five overlays ticking at 60 Hz while hidden cost the Pi idle CPU.
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self._update_animation)
        if initial_anim_type == LoadingOverlayWidget.AnimationGIF.PLACEHOLDER:
            self.set_animation_path(_INTRO_GIF)
        self.label.setText("Loading...")

    def set_animation_path(self, path: str | Path) -> None:
        """Swap the spinner for the gif at *path*; a missing or corrupt file keeps the spinner."""
        gif = str(Path(path).expanduser())
        movie = QtGui.QMovie(gif)
        if not movie.isValid():
            return
        self.movie = movie
        # Header-only read; QMovie reports no size until a frame is decoded.
        self._movie_size = QtGui.QImageReader(gif).size()
        if self._movie_size.isEmpty() and movie.jumpToFrame(0):
            self._movie_size = movie.frameRect().size()
        self.timer.stop()
        self.gifshow.setMovie(movie)
        self.gifshow.show()
        self._fit_movie()
        if self.isVisible():
            movie.start()

    def set_status_message(self, message: str) -> None:
        """Set widget message"""
        self.label.setText(message)

    def close(self) -> bool:
        """Re-implemented method; hideEvent stops the animation, this resets its state."""
        self.label.setText("Loading...")
        self._angle = 0
        return super().close()

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        """Run the animation only while on screen; a hidden QMovie keeps decoding frames."""
        super().showEvent(a0)
        if self.movie is not None:
            self.movie.start()
        else:
            self.timer.start()

    def hideEvent(self, a0: QtGui.QHideEvent | None) -> None:
        """Stop the animation as soon as the overlay, or any ancestor, is hidden."""
        super().hideEvent(a0)
        self.timer.stop()
        if self.movie is not None:
            self.movie.stop()

    def _update_animation(self) -> None:
        """Advance the spinner one 16 ms step: rotate and breathe the arc length."""
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
        if self.movie is None:
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
        self.gifshow.setGeometry(margin, 0, self.width() - margin * 2, label_y - margin)
        self._fit_movie()

    def _fit_movie(self) -> None:
        """Decode frames at the on-screen size; QMovie scales once per frame, not per paint."""
        # An empty scaled size stops the QMovie for good, so skip until laid out.
        if self.movie is None or self.gifshow.size().isEmpty():
            return
        if self._movie_size.isEmpty():
            # Unknown frame size: let QLabel stretch it rather than crop at native size.
            self.gifshow.setScaledContents(True)
            return
        self.movie.setScaledSize(
            self._movie_size.scaled(
                self.gifshow.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )
        )

    def _setup_ui(self) -> None:
        """Build the gif label and the status text label."""
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
