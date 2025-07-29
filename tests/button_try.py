import sys


from PyQt6 import QtCore, QtWidgets, QtGui


class Button(QtWidgets.QPushButton):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._icon_center = None

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        return super().resizeEvent(a0)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        # qp = QtGui.QPainter(self)
        qp= QtWidgets.QStylePainter(self)

        qp.setPen(QtCore.Qt.PenStyle.NoPen)
        qp.setRenderHint(qp.RenderHint.Antialiasing)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering)
        
        bg_color = (
            QtGui.QColor(175, 175, 175)
            if not self.isDown()
            else QtGui.QColor(120, 120, 120)
        )

        path = QtGui.QPainterPath()
        xRadius = self.rect().toRectF().normalized().height() / 2.0
        yRadius = self.rect().toRectF().normalized().height() / 2.0
        path.addRoundedRect(
            0,
            0,
            self.rect().toRectF().normalized().width(),
            self.rect().toRectF().normalized().height(),
            xRadius,
            yRadius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        # path.addEllipse(
        #     (self.rect().toRectF().normalized().height() * 0.1 / 2.0),
        #     (self.rect().toRectF().normalized().height() * 0.1 / 2.0),
        #     self.rect().toRectF().normalized().height() * 0.90,
        #     self.rect().toRectF().normalized().height() * 0.90,
        # )
        icon_path = QtGui.QPainterPath()
        icon_path.addEllipse(
            self.rect().toRectF().normalized().left()
            + self.rect().toRectF().normalized().height() * 0.05,
            self.rect().toRectF().normalized().top()
            + self.rect().toRectF().normalized().height() * 0.05,
            (self.rect().toRectF().normalized().height() * 0.90),
            (self.rect().toRectF().normalized().height() * 0.90),
        )
        self._icon_center = icon_path.boundingRect().center()
        icon_path.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
        cutout = path.subtracted(icon_path)
        path.connectPath(icon_path)
        qp.fillPath(cutout, bg_color)
        # mask = QtGui.QRegion(cutout.toFillPolygon().toPolygon())

        # self.setMask(mask)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumSize(1000, 800)
        # self.setMaximumSize(500, 800)
        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.GlobalColor.blue)

        self.setPalette(p)

        self.button = Button(self)
        self.button.show()

        self.button.setGeometry(QtCore.QRect(50, 100, 600, 240))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()

    app.processEvents()
    main_window.showNormal()

    sys.exit(app.exec())


# path.addRoundedRect(
#             0,
#             0,
#             self.rect().toRectF().width(),
#             self.rect().toRectF().height(),
#             self.rect().toRectF().height() * 1.1
#             - self.rect().toRectF().height() / 2,
#             self.rect().toRectF().height() * 1.1
#             - self.rect().toRectF().height() / 2,
#             QtCore.Qt.SizeMode.AbsoluteSize,
#         )
#         path.setFillRule(QtCore.Qt.FillRule.OddEvenFill)
#         path.addEllipse(
#             (
#                 self.rect().toRectF().height() * 0.1
#                 - self.rect().toRectF().height() * 0.1 / 2.0
#             ),
#             (
#                 self.rect().toRectF().height() * 0.1
#                 - self.rect().toRectF().height() * 0.1 / 2.0
#             ),
#             self.rect().toRectF().height() * 0.90,
#             self.rect().toRectF().height() * 0.90,
#         )
#         mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
