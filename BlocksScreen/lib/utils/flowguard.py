from PyQt6 import QtCore, QtGui, QtWidgets


class FlowguardWidget(QtWidgets.QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0.0  # Store as -1.0 to 1.0

        self._bar_color = QtGui.QColor(223, 223, 223)

        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding
        )

        self.max_tangle = 0.0
        self.max_clog = 0.0

        # Font for labels
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)

        # Constant paint state
        self._track_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        self._dark_brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
        self._marker_pen = QtGui.QPen(QtGui.QColor(223, 223, 223), 1)
        self._center_pen = QtGui.QPen(
            QtGui.QColor(100, 100, 100), 1, QtCore.Qt.PenStyle.DashLine
        )
        self._danger_pen = QtGui.QPen(QtGui.QColor(226, 31, 31), 1)
        self._danger_brush = QtGui.QBrush(QtGui.QColor(226, 31, 31, 75))
        self._label_pen = QtGui.QPen(QtGui.QColor(180, 180, 180))
        self._fill_brush = QtGui.QBrush(self._bar_color)

        # Size dependent paint state, rebuilt on resize
        self._geometry_valid = False
        self._bar_x = 0
        self._bar_y = 0
        self._bar_width = 30
        self._bar_height = 0
        self._center_y = 0.0
        self._track_rect = QtCore.QRectF()
        self._center_line = QtCore.QLineF()
        self._top_danger_rect = QtCore.QRect()
        self._bottom_danger_rect = QtCore.QRect()
        self._clog_rect = QtCore.QRectF()
        self._tangle_rect = QtCore.QRectF()

        # Marker lines, also invalidated by the max clog/tangle setters
        self._clog_line: QtCore.QLineF | None = None
        self._tangle_line: QtCore.QLineF | None = None

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, drop the size dependent paint state"""
        self._geometry_valid = False
        super().resizeEvent(a0)

    def _ensure_geometry(self) -> None:
        """Rebuild the bar, marker and label geometry after a resize or a new limit"""
        if self._geometry_valid:
            return

        top_margin = 30
        bottom_margin = 30
        bar_width = self._bar_width
        self._bar_x = int(self.width() / 2 - bar_width / 2)
        self._bar_y = top_margin
        self._bar_height = self.height() - top_margin - bottom_margin
        bar_x, bar_y, bar_height = self._bar_x, self._bar_y, self._bar_height

        self._track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        self._center_y = bar_y + bar_height / 2

        self._clog_line = None
        if abs(self.max_clog) > 0.01:
            clog_y = self._center_y - (abs(self.max_clog) * (bar_height / 2))
            self._clog_line = QtCore.QLineF(bar_x, clog_y, bar_x + bar_width, clog_y)

        self._tangle_line = None
        if abs(self.max_tangle) > 0.01:
            tangle_y = self._center_y + (abs(self.max_tangle) * (bar_height / 2))
            self._tangle_line = QtCore.QLineF(
                bar_x, tangle_y, bar_x + bar_width, tangle_y
            )

        self._center_line = QtCore.QLineF(
            bar_x - 5, self._center_y, bar_x + bar_width + 5, self._center_y
        )

        danger_height = int(0.35 * (bar_height / 2))
        self._top_danger_rect = QtCore.QRect(bar_x, bar_y, bar_width, danger_height)
        self._bottom_danger_rect = QtCore.QRect(
            bar_x, bar_y + bar_height - danger_height, bar_width, danger_height
        )

        self._clog_rect = QtCore.QRectF(0, top_margin - 25, self.width(), 20)
        self._tangle_rect = QtCore.QRectF(
            0, top_margin + bar_height + 5, self.width(), 20
        )
        self._geometry_valid = True

    def setValue(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between -1.0 and 1.0
                          -1.0 = maximum clog (top)
                           0.0 = normal flow (center)
                          +1.0 = maximum tangle (bottom)


        """
        if not (-1.0 <= value <= 1.0):
            raise ValueError("Argument `value` expected value between -1.0 and 1.0")
        self.progress_value = value
        self.update()

    def set_max_clog(self, value: float) -> None:
        """Set maximum clog value for display

        Args:
            value (float): Maximum clog value (typically negative, e.g., -0.134)
        """
        self.max_clog = value
        self._geometry_valid = False
        self.update()

    def set_max_tangle(self, value: float) -> None:
        """Set maximum tangle value for display

        Args:
            value (float): Maximum tangle value (typically positive, e.g., 0.186)
        """
        self.max_tangle = value
        self._geometry_valid = False
        self.update()

    def _draw_vertical_bar(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical flow indicator bar"""
        painter.setPen(self._track_pen)
        painter.setBrush(self._dark_brush)
        painter.drawRect(self._track_rect)

        painter.setPen(self._marker_pen)
        if self._clog_line is not None:
            painter.drawLine(self._clog_line)
        if self._tangle_line is not None:
            painter.drawLine(self._tangle_line)

        painter.setPen(self._center_pen)
        painter.drawLine(self._center_line)

        if abs(self.progress_value) > 0.01:
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_brush)
            fill_height = abs(self.progress_value) * (self._bar_height / 2)
            fill_y = (
                self._center_y - fill_height
                if self.progress_value > 0
                else self._center_y
            )
            painter.drawRect(
                QtCore.QRectF(self._bar_x, fill_y, self._bar_width, fill_height)
            )

        painter.setPen(self._danger_pen)
        painter.setBrush(self._danger_brush)
        painter.drawRect(self._top_danger_rect)
        painter.drawRect(self._bottom_danger_rect)

        # Draw labels
        painter.setPen(self._label_pen)
        painter.setFont(self._label_font)
        painter.drawText(self._clog_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "CLOG")
        painter.drawText(
            self._tangle_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "TANGLE"
        )

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        self._ensure_geometry()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        self._draw_vertical_bar(painter)
        painter.end()
