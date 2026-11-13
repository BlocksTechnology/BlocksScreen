from PyQt6 import QtCore, QtGui, QtWidgets


class NotificationTabBar(QtWidgets.QTabBar):
    """Re-implemented QTabBar so that the widget can have notifications"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._notifications = {}  # {tab_index: bool}
        self._dot_brush = QtGui.QBrush(QtGui.QColor(226, 31, 31))

    def setNotification(self, index: int, show: bool):
        """Set notification"""
        if index < 0 or index >= self.count():
            return
        self._notifications[index] = show
        self.update(self.tabRect(index))  # repaint only that tab

    def paintEvent(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        # Skip the painter entirely while no tab is flagged, the common case
        if not any(self._notifications.values()):
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBrush(self._dot_brush)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        count = self.count()
        for index, show in self._notifications.items():
            if not show or index >= count:
                continue
            rect = self.tabRect(index)
            dot_diameter = min(10, rect.height() * 0.3)
            dot_x = rect.right() - dot_diameter - 4
            dot_y = rect.top() + 30
            painter.drawEllipse(int(dot_x), dot_y, int(dot_diameter), int(dot_diameter))


class NotificationQTabWidget(QtWidgets.QTabWidget):
    """Re-implemented QTabWidget so that we can have notifications"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._custom_tabbar = NotificationTabBar()
        self.setTabBar(self._custom_tabbar)

    def setNotification(self, index: int, show: bool):
        """Set tab notification"""
        self._custom_tabbar.setNotification(index, show)
