from PyQt6.QtWidgets import (
    QPushButton, QStyle, )
from PyQt6 import QtGui, QtWidgets, QtCore
import typing


class CustomQPushButton(QPushButton):
    """CustomQPushButton Custom QPushButton where icon position can be set.

    Args:
        parent (QWidget): parent of the button
        QPushButton (_type_): 
    """

    def __init__(self, parent, *args, **kwargs):
        super(CustomQPushButton, self).__init__(parent, *args, **kwargs)
        self._icon = self.icon()
        if not self._icon.isNull():
            super().setIcon(QtGui.QIcon())

    def sizeHint(self):
        hint = super().sizeHint()
        if not self.text() or self._icon.isNull():
            return hint
        style = self.style()
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        margin = style.pixelMetric(
            style.PixelMetric.PM_ButtonMargin, opt, self)
        spacing = style.pixelMetric(
            style.PixelMetric.PM_LayoutVerticalSpacing, opt, self)

        
        # get the possible rect required for the current label
        labelRect = self.fontMetrics().boundingRect(
            0, 0, 5000, 5000, QtCore.Qt.TextFlag.TextShowMnemonic, self.text())
        iconHeight = self.iconSize().height()
        height = iconHeight + spacing + labelRect.height() + margin * 2
        if height > hint.height():
            hint.setHeight(iconHeight)

        return hint

    def setIcon(self, icon):
        # setting an icon might change the horizontal hint, so we need to use a
        # "local" reference for the actual icon and go on by letting Qt to *think*
        # that it doesn't have an icon;
        if icon == self._icon:
            return
        self._icon = icon
        self.updateGeometry()

    def paintEvent(self, event):
        if self._icon.isNull() or not self.text():
            super().paintEvent(event)
            return

        with QtGui.QPainter(self) as painter:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            opt = QtWidgets.QStyleOptionButton()
            self.initStyleOption(opt)
            opt.text = ''
            qp = QtWidgets.QStylePainter(self)

            # draw the button without any text or icon
            qp.drawControl(QStyle.ControlElement.CE_PushButton, opt)

            rect = self.rect()
            style = self.style()

            print(type(style))
            margin = style.pixelMetric(
                style.PixelMetric.PM_ButtonMargin, opt, self)

            iconSize = self.iconSize()
            # iconRect = QtCore.QRect(int((int(rect.width()) - int(iconSize.width())) / 2), int(margin),
            #                         int(iconSize.width()), int(iconSize.height()))
            # iconRect = QtCore.QRect(QtCore.QPoint(15, 15), QtCore.QSize(
            #     int(iconSize.width() / 4), int(iconSize.height())))
            iconRect = QtCore.QRect(QtCore.QPoint(15, 15), QtCore.QSize(
                int(iconSize.width()),int( iconSize.height())))

            state = QtGui.QIcon.State.Off
            if self.underMouse():
                mode = QtGui.QIcon.Mode.Active
            elif self.isEnabled():
                mode = QtGui.QIcon.Mode.Normal
            elif self.mousePressEvent:
                #     mode = QtGui.QIcon.Mode.Normal
                #     state = QtGui.QIcon.State.On
                print("ELLE")
            else:
                state = QtGui.QIcon.Mode.Disabled

            qp.drawPixmap(iconRect, self._icon.pixmap(
                iconSize, mode=mode, state=state))

            spacing = style.pixelMetric(
                style.PixelMetric.PM_LayoutHorizontalSpacing, opt, self)

            lineIconMargin = style.pixelMetric(
                style.PixelMetric.PM_LineEditIconMargin, opt, self
            )
            # Text stuff
            labelRect = QtCore.QRect(rect)
            labelRect.setTop(iconRect.bottom() + spacing)
            qp.drawText(labelRect,
                        QtCore.Qt.TextFlag.TextShowMnemonic | QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
                        self.text())

    def hitButton(self, pos: QtCore.QPoint) -> bool:
        print("HitButton positiongon")
        return super().hitButton(pos)

    def mouseMoveEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        return super().mouseMoveEvent(a0)

    def mousePressEvent(self, e: typing.Optional[QtGui.QMouseEvent]) -> None:
        print("MousePressEvent")
        return super().mousePressEvent(e)

    def mouseDoubleClickEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        return super().mouseDoubleClickEvent(a0)

    def keyPressEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        return super().keyPressEvent(a0)

    def event(self, e: typing.Optional[QtCore.QEvent]) -> bool:
        return super().event(e)

    def focusInEvent(self, a0: typing.Optional[QtGui.QFocusEvent]) -> None:
        return super().focusInEvent(a0)

    def focusOutEvent(self, a0: typing.Optional[QtGui.QFocusEvent]) -> None:
        return super().focusOutEvent(a0)
