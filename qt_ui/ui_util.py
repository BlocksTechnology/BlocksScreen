from PyQt6.QtWidgets import (
    QPushButton, QStyle)
from PyQt6 import QtGui, QtWidgets, QtCore, QtSvg
import typing


class CustomQPushButton(QPushButton):
    """CustomQPushButton Custom QPushButton where icon position can be set.

    Args:
        parent (QWidget): parent of the button
        QPushButton (_type_): 
    """
    # TODO: Icon image quality fix
    # TODO: Icon Transparency

    def __init__(self, parent,  x: int = 0, y: int = 0, *args, **kwargs):
        super(CustomQPushButton, self).__init__(parent, *args, **kwargs)

        self._icon = self.icon()
        if not self._icon.isNull():
            super().setIcon(QtGui.QIcon())

        self.iconPosition = QtCore.QPoint(0, 0)
        self.iconPixmap: QtGui.QPixmap | None = None
        self.borderIconLeft: QtGui.QPixmap | None = None
        self.borderIconCenter: QtGui.QPixmap | None = None
        self.borderIconRight: QtGui.QPixmap | None = None
        self.borderLeftRect: QtCore.QRect = QtCore.QRect()
        self.borderCenterRect: QtCore.QRect = QtCore.QRect()
        self.borderRightRect: QtCore.QRect = QtCore.QRect()
        self._colorSet = False

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

        # * get the possible rect required for the current label
        labelRect = self.fontMetrics().boundingRect(
            0, 0, 5000, 5000, QtCore.Qt.TextFlag.TextShowMnemonic, self.text())
        iconHeight = self.iconSize().height()
        height = iconHeight + spacing + labelRect.height() + margin * 2
        if height > hint.height():
            hint.setHeight(iconHeight)

        hint.setHeight(iconHeight)
        hint.setWidth(self.iconSize().width())

        # * For the button only where ther eis an image
        # self.pixmap.size()

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


        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)

        opt.text = ''
        qp = QtWidgets.QStylePainter(self)

        # * draw the button without any text or icon
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(
            qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(
            qp.RenderHint.LosslessImageRendering, True)
        rect = self.rect()
        style = self.style()

        margin = style.pixelMetric(
            style.PixelMetric.PM_ButtonMargin, opt, self)
        
        # * Icon Coloring and drawing
        iconSize = self.iconSize()
        iconCenter = QtCore.QPoint(
            self.iconPosition.x() + int(iconSize.width() / 2), self.iconPosition.y() + int(iconSize.height() / 2))
        iconRect = QtCore.QRect(iconCenter, iconSize)

        if self.iconPixmap is not None:

            # self._iconColored = self.setIconColor(
            #     # self.iconPixmap, QtGui.QColor(188, 188, 188, 255), qp, iconSize, iconCenter, iconRect)
            #     self.iconPixmap, QtGui.QColor(188, 1, 188, 255), qp, iconSize, iconCenter, iconRect)
            # self._icon = self._iconColored

            # * Draw border image
            self.setButtonBorder(qp, margin)

        # * Draw the Button
        qp.drawControl(QStyle.ControlElement.CE_PushButton, opt)

        # *  Draw Text stuff over the button
        labelRect = QtCore.QRect(rect)
        labelRect.setLeft(iconRect.width())
        qp.drawText(labelRect,
                    QtCore.Qt.TextFlag.TextShowMnemonic | QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    self.text())

        # qp.drawRect(labelRect)

    def setIconColor(self, pixmap: QtGui.QPixmap, iconColor: QtGui.QColor, qp: QtWidgets.QStylePainter, iconSize, iconCenter, iconRect) -> QtGui.QIcon:  # ,

        # TODO: Button States is funky
        state = QtGui.QIcon.State.Off
        if self.isEnabled() and not self.isDown():
            mode = QtGui.QIcon.Mode.Normal
        elif self.isDown():
            mode = QtGui.QIcon.Mode.Normal
            state = QtGui.QIcon.State.On
            # super().pressed.emit()
        else:
            mode = QtGui.QIcon.Mode.Disabled
            state = QtGui.QIcon.State.Off
        _transparentColor = QtGui.QColor(0, 0, 0, 0)

        # * alpha
        _iconMask = QtGui.QPixmap(iconRect.x(), iconRect.y())
        _iconMask.fill(_transparentColor)
        _iconColor = QtGui.QPixmap(iconRect.x(), iconRect.y())
        _iconColor.fill(iconColor)

        # * Save previous Painter state
        qp.save()

        # * Create new icon with color
        qp.setRenderHints(qp.RenderHint.Antialiasing)
        qp.setRenderHints(qp.RenderHint.LosslessImageRendering)
        qp.setRenderHints(qp.RenderHint.SmoothPixmapTransform)
        # *Clear Inside of the icon
        qp.drawPixmap(iconRect, _iconMask)
        qp.setCompositionMode(
            qp.CompositionMode.CompositionMode_Xor)
        qp.drawPixmap(iconRect, self._icon.pixmap(
            iconSize, 2.0, mode=mode, state=state))

        # * Paint the Icon Color
        qp.setCompositionMode(
            qp.CompositionMode.CompositionMode_Overlay)
        qp.drawPixmap(iconRect, _iconColor)
        # ? This makes the icon be grayer when i click it
        self._icon.addPixmap(_iconMask.scaled(_iconMask.size(),
                                              QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                              QtCore.Qt.TransformationMode.SmoothTransformation
                                              ), mode=mode, state=state)
        # * Draw the Icon
        qp.drawPixmap(iconRect, self._icon.pixmap(
            iconSize, mode=mode, state=state))

        # * Restore previous Painter State
        qp.restore()
        return QtGui.QIcon(pixmap)

    def setButtonBorder(self,  qp: QtWidgets.QStylePainter, margin):

        if self.borderIconRight is None or \
                self.borderIconCenter is None or \
                self.borderIconLeft is None:
            return False
        qp.save()
        
        # * Calculate Pixmaps Rects
        buttonRect = self.rect()
        _leftBorderRect: QtCore.QRect = QtCore.QRect(0, 0, int(
            float(buttonRect.right()) * 0.37),  buttonRect.height())
        _leftBorderRectF: QtCore.QRectF = QtCore.QRectF(0.0, 0.0, 
            float(buttonRect.right()) * 0.37,  float(buttonRect.height()))
        _centerBorderRect: QtCore.QRect = QtCore.QRect(_leftBorderRect.width() , 0, int(
            float(buttonRect.right()) * 0.44), buttonRect.height())

        _rightBorderRect: QtCore.QRect = QtCore.QRect(_centerBorderRect.width() + _centerBorderRect.left(), 0, int(
            float(buttonRect.right()) * 0.19), buttonRect.height())

        print(_leftBorderRect)
        print(_centerBorderRect)

        # * Set composition mode
        qp.setCompositionMode(
            qp.CompositionMode.CompositionMode_SourceOver)
        
        # * Set Render Hints
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering)
        qp.setRenderHint(qp.RenderHint.Antialiasing)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform)
        rect = self.rect()

        # * Draw left portion
        _scaledLeftPixmap =self.borderIconLeft.scaled(_leftBorderRect.size(),
                                       QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                       QtCore.Qt.TransformationMode.SmoothTransformation)

        qp.drawItemPixmap(
            _leftBorderRect, QtCore.Qt.AlignmentFlag.AlignBaseline,
            _scaledLeftPixmap
        )
        # qp.drawPixmap(_leftBorderRectF, _scaledLeftPixmap, _leftBorderRectF)
        
        # * Draw middle portion
        qp.drawItemPixmap(
            _centerBorderRect, QtCore.Qt.AlignmentFlag.AlignCenter,
            self.borderIconCenter.scaledToHeight(_centerBorderRect.size().height(),
                                        #  QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding)
                                         QtCore.Qt.TransformationMode.SmoothTransformation)
        )
        # * Draw right portion
        qp.drawItemPixmap(
            _rightBorderRect, QtCore.Qt.AlignmentFlag.AlignRight,
            self.borderIconRight.scaled(_rightBorderRect.size(),
                                        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                        QtCore.Qt.TransformationMode.SmoothTransformation)
        )

        qp.restore()
        return _leftBorderRect

    def setProperty(self, name: str, value: typing.Any) -> bool:
        if name == "setIconPosition":
            self.iconPosition.setX(value.x())
            self.iconPosition.setY(value.y())
        elif name == "iconPixmap":
            # self._icon.addPixmap(value)
            self.iconPixmap = value
            # super().setIcon(QtGui.QIcon())
        elif name == "borderLeftPixmap":
            self.borderIconLeft = value
        elif name == "borderCenterPixmap":
            self.borderIconCenter = value
        elif name == "borderRightPixmap":
            self.borderIconRight = value
       
        return super().setProperty(name, value)

    def hitButton(self, pos: QtCore.QPoint) -> bool:
        return super().hitButton(pos)

    def mouseMoveEvent(self, a0: typing.Optional[QtGui.QMouseEvent]) -> None:
        return super().mouseMoveEvent(a0)

    def mousePressEvent(self, e: typing.Optional[QtGui.QMouseEvent]) -> None:
        print("PRESSED")
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
