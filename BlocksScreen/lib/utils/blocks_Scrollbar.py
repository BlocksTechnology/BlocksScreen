from PyQt6 import QtCore, QtGui, QtWidgets


class CustomScrollBar(QtWidgets.QScrollBar):
    HANDLE_EDGE = QtGui.QColor(164, 164, 164, 100)
    HANDLE_CENTER = QtGui.QColor(164, 164, 164, 164)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(40)

    def paintEvent(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        # Linear remap of 15..85 onto 0..100, clamped outside that band
        if handle_percentage <= 15:
            val = 0.0
        elif handle_percentage >= 85:
            val = float(max_val)
        else:
            val = (handle_percentage - 15) / 70.0 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
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

        gradient.setColorAt(0.0, self.HANDLE_EDGE)  # Top
        gradient.setColorAt(0.5, self.HANDLE_CENTER)  # Center
        gradient.setColorAt(1.0, self.HANDLE_EDGE)  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)
