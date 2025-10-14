from PyQt6 import QtWidgets, QtGui, QtCore


class NotificationTabBar(QtWidgets.QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._notifications = {}  # {tab_index: bool}

    def setNotification(self, index: int, show: bool):
        if index < 0 or index >= self.count():
            return
        self._notifications[index] = show
        self.update(self.tabRect(index))  # repaint only that tab

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )


class NotificationQTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._custom_tabbar = NotificationTabBar()
        self.setTabBar(self._custom_tabbar)

    def setNotification(self, index: int, show: bool):
        self._custom_tabbar.setNotification(index, show)
