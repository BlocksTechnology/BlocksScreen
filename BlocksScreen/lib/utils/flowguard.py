from PyQt6 import QtWidgets, QtGui, QtCore


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
        self.update()

    def set_max_tangle(self, value: float) -> None:
        """Set maximum tangle value for display

        Args:
            value (float): Maximum tangle value (typically positive, e.g., 0.186)
        """
        self.max_tangle = value
        self.update()

    def _draw_vertical_bar(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical flow indicator bar"""
        rect = self.rect()

        top_margin = 30
        bottom_margin = 30

        bar_width = 30
        bar_x = int(self.rect().width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin

        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))

        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)

        center_y = bar_y + bar_height / 2

        pen = QtGui.QPen(QtGui.QColor(223, 223, 223), 1)
        painter.setPen(pen)
        if abs(self.max_clog) > 0.01:
            clog_y = center_y - (abs(self.max_clog) * (bar_height / 2))
            painter.drawLine(
                QtCore.QPointF(bar_x, clog_y), QtCore.QPointF(bar_x + bar_width, clog_y)
            )

        if abs(self.max_tangle) > 0.01:
            tangle_y = center_y + (abs(self.max_tangle) * (bar_height / 2))
            painter.drawLine(
                QtCore.QPointF(bar_x, tangle_y),
                QtCore.QPointF(bar_x + bar_width, tangle_y),
            )
        center_pen = QtGui.QPen(
            QtGui.QColor(100, 100, 100), 1, QtCore.Qt.PenStyle.DashLine
        )
        painter.setPen(center_pen)
        painter.drawLine(
            QtCore.QPointF(bar_x - 5, center_y),
            QtCore.QPointF(bar_x + bar_width + 5, center_y),
        )
        if abs(self.progress_value) > 0.01:
            bar_color = self._bar_color
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(bar_color)
            if self.progress_value > 0:
                fill_height = self.progress_value * (bar_height / 2)
                fill_y = center_y - fill_height
                fill_rect = QtCore.QRectF(bar_x, fill_y, bar_width, fill_height)

            else:
                fill_height = abs(self.progress_value) * (bar_height / 2)
                fill_rect = QtCore.QRectF(bar_x, center_y, bar_width, fill_height)

            painter.drawRect(fill_rect)

        fill_height = int(0.35 * (bar_height / 2))

        pen = QtGui.QPen(QtGui.QColor(226, 31, 31), 1)
        brush = QtGui.QBrush(QtGui.QColor(226, 31, 31, 75))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(bar_x, bar_y, bar_width, fill_height)

        fill_y = center_y - fill_height
        painter.drawRect(
            bar_x, bar_y + bar_height - fill_height, bar_width, fill_height
        )

        # Draw labels
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)

        x1 = top_margin - 25
        x2 = top_margin + bar_height + 5

        # "CLOG" label (top)
        clog_rect = QtCore.QRectF(0, x1, self.width(), 20)
        painter.drawText(clog_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "CLOG")

        # "TANGLE" label (bottom)
        tangle_rect = QtCore.QRectF(0, x2, self.width(), 20)
        painter.drawText(tangle_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "TANGLE")

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        self._draw_vertical_bar(painter)
        painter.end()
