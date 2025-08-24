from PyQt6 import QtCore, QtGui, QtWidgets
import numpy as np


class CustomScrollBar(QtWidgets.QScrollBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(40)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        if handle_percentage < 15:
            base_handle_length = int(
                (groove.height() * page_step / (max_val - min_val + page_step))
                + np.interp(handle_percentage, [0, 15], [0, 40])
            )
            handle_pos = 0

        elif handle_percentage > 85:
            base_handle_length = int(
                (groove.height() * page_step / (max_val - min_val + page_step))
                + np.interp(handle_percentage, [85, 100], [40, 0])
            )
            handle_pos = int(
                (groove.height() - base_handle_length)
                * (max_val - min_val)
                / (max_val - min_val)
            )
        else:
            val = (
                np.interp((handle_percentage), [15, 85], [0, 100])
                / 100
                * max_val
            )

            base_handle_length = int(
                (groove.height() * page_step / (max_val - min_val + page_step))
                + 40
            )
            handle_pos = int(
                (groove.height() - base_handle_length)
                * (val - min_val)
                / (max_val - min_val)
            )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)
