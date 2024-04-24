from PyQt6.QtWidgets import QPushButton, QStyle
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
    # TODO: Button size cannot be small so it overflows over to other buttons when in a collumn layout
    def __init__(self, parent, x: int = 0, y: int = 0, *args, **kwargs):
        super(CustomQPushButton, self).__init__(parent, *args, **kwargs)

        self._icon = self.icon()
        if not self._icon.isNull():
            super().setIcon(QtGui.QIcon())

        # * Make the button accept touch events
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        self.iconPosition = QtCore.QPoint(0, 0)
        self.iconPixmap: QtGui.QPixmap | None = None
        self.borderIconLeft: QtGui.QPixmap | None = None
        self.borderIconCenter: QtGui.QPixmap | None = None
        self.borderIconRight: QtGui.QPixmap | None = None
        self.borderLeftRect: QtCore.QRect = QtCore.QRect()
        self.borderCenterRect: QtCore.QRect = QtCore.QRect()
        self.borderRightRect: QtCore.QRect = QtCore.QRect()
        self.buttonPixmapRects = []
        self._colorSet = False
        self.buttonText: str | None = None

    def sizeHint(self):
        # TODO: Set icon pressable size
        hint = super().sizeHint()
        if not self.text() or self._icon.isNull():
            return hint
        style = self.style()
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        margin = style.pixelMetric(style.PixelMetric.PM_ButtonMargin, opt, self)
        spacing = style.pixelMetric(
            style.PixelMetric.PM_LayoutVerticalSpacing, opt, self
        )

        # * get the possible rect required for the current label
        labelRect = self.fontMetrics().boundingRect(
            0, 0, 5000, 5000, QtCore.Qt.TextFlag.TextShowMnemonic, self.text()
        )
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

    def setText(self, text: str) -> None:
        self.buttonText = text
        return super().setText(text)

    def paintEvent(self, event):
        # if self._icon.isNull() or not self.text():
        #     super().paintEvent(event)
        #     return

        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)

        opt.text = ""
        qp = QtWidgets.QStylePainter(self)

        # * draw the button without any text or icon
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)

        rect = self.rect()
        style = self.style()

        margin = style.pixelMetric(style.PixelMetric.PM_ButtonMargin, opt, self)

        # * Draw the Button control
        qp.drawControl(QStyle.ControlElement.CE_PushButton, opt)

        # * Draw border image
        self.buttonPixmapRects = self.setButtonBorder(qp, margin)
        if self.iconPixmap is not None:

            self._iconColored = self.setIconColor(self.iconPixmap, qp)

        # *  Draw Text stuff over the button    DONE
        if self.buttonPixmapRects and self.buttonText is not None:
            labelRect = QtCore.QRect(rect)
            _start_text_position = int(self.buttonPixmapRects[0].width())
            labelRect.setLeft(_start_text_position + margin)
            # labelRect.setRight(int(self.buttonPixmapRects[1].width() + _start_text_position))
            qp.drawText(
                labelRect,
                QtCore.Qt.TextFlag.TextShowMnemonic
                | QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self.buttonText,
            )

        # qp.drawRect(labelRect)

    def setIconColor(
        self,
        pixmap: QtGui.QPixmap,
        qp: QtWidgets.QStylePainter,
        iconColor: QtGui.QColor | None = None,
    ) -> QtGui.QIcon:  # ,

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

        if self.buttonPixmapRects:
            _iconParentRect = self.buttonPixmapRects[0]

            pixmapSize = pixmap.size()

            # * Icon Coloring and drawing

            iconRect = QtCore.QRectF(
                _iconParentRect.width() * 0.20,
                _iconParentRect.height() * 0.185,
                pixmapSize.width() - _iconParentRect.width() * 0.5,
                pixmapSize.height() - _iconParentRect.height() * 0.5,
            )

            # * Save previous Painter state
            qp.save()

            # * Create new icon with color
            qp.setRenderHints(qp.RenderHint.Antialiasing)
            qp.setRenderHints(qp.RenderHint.LosslessImageRendering)
            qp.setRenderHints(qp.RenderHint.SmoothPixmapTransform)

            qp.drawPixmap(
                iconRect,
                pixmap.scaled(
                    int(pixmapSize.width()),
                    int(pixmapSize.height()),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                ),
                pixmap.rect().toRectF(),
            )

            # TODO: Icon color
            # qp.drawRect(iconRect)
            # if iconColor is not None:
            #     # * alpha
            #     _iconMask = QtGui.QPixmap(iconRect.x(), iconRect.y())
            #     _iconMask.fill(_transparentColor)
            #     _iconColor = QtGui.QPixmap(iconRect.x(), iconRect.y())
            #     _iconColor.fill(iconColor)

            #     # *Clear Inside of the icon
            #     qp.drawPixmap(iconRect, _iconMask)

            #     qp.setCompositionMode(
            #         qp.CompositionMode.CompositionMode_Xor)
            #     qp.drawPixmap(iconRect, _iconColor)

            #     qp.drawPixmap(iconRect, self._icon.pixmap(
            #         iconSize, 2.0, mode=mode, state=state))

            #     # * Paint the Icon Color
            #     qp.setCompositionMode(
            #         qp.CompositionMode.CompositionMode_Overlay)

            #     # ? This makes the icon be grayer when i click it
            #     self._icon.addPixmap(_iconMask.scaled(_iconMask.size(),
            #                                         QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            #                                         QtCore.Qt.TransformationMode.SmoothTransformation
            #                                         ), mode=mode, state=state)

            # else:

            # * Restore previous Painter State
            qp.restore()
        return QtGui.QIcon(pixmap)

    def setButtonBorder(
        self, qp: QtWidgets.QStylePainter, margin
    ) -> list[QtCore.QRectF] | None:

        if (
            self.borderIconRight is None
            or self.borderIconCenter is None
            or self.borderIconLeft is None
        ):
            return None
        qp.save()
        buttonRect = self.rect()
        ## * Calculate Pixmaps Rects
        # * Left part
        _leftBorderRectF: QtCore.QRectF = QtCore.QRectF(
            0.0, 0.0, buttonRect.width(), buttonRect.height()
        )
        _scaledLeftPixmap = self.borderIconLeft.scaled(
            int(_leftBorderRectF.size().width()),
            int(_leftBorderRectF.size().height()),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        _leftBorderRectF.setWidth(_scaledLeftPixmap.width())
        # * Center part
        _centerBorderRectF: QtCore.QRectF = QtCore.QRectF(
            _scaledLeftPixmap.size().width(),
            0.0,
            buttonRect.width()
            - _scaledLeftPixmap.width()
            - self.borderIconRight.width(),
            _scaledLeftPixmap.height(),
        )
        _scaledCenterPixmap = self.borderIconCenter.scaled(
            int(_centerBorderRectF.size().width()),
            int(_centerBorderRectF.size().height()),
            QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        # * Right part
        _rightBorderRectF: QtCore.QRectF = QtCore.QRectF(
            _scaledCenterPixmap.width() + _scaledLeftPixmap.width(),
            0.0,
            buttonRect.width()
            - (_scaledCenterPixmap.width() + _scaledLeftPixmap.width()),
            buttonRect.height(),
        )
        _scaledRightPixmap = self.borderIconRight.scaled(
            int(_rightBorderRectF.size().width()),
            int(_rightBorderRectF.size().height()),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        _rightBorderRectF.setWidth(_scaledRightPixmap.width())
        # * Set composition mode
        qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
        # * Set Render Hints
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering)
        qp.setRenderHint(qp.RenderHint.Antialiasing)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform)
        ## * Draw the borders
        qp.drawPixmap(
            _scaledLeftPixmap.rect().toRectF(),
            _scaledLeftPixmap,
            _scaledLeftPixmap.rect().toRectF(),
        )
        qp.drawPixmap(
            _centerBorderRectF,
            _scaledCenterPixmap,
            _scaledCenterPixmap.rect().toRectF(),
        )
        qp.drawPixmap(
            _rightBorderRectF, _scaledRightPixmap, _scaledRightPixmap.rect().toRectF()
        )

        qp.restore()
        return [_leftBorderRectF, _centerBorderRectF, _rightBorderRectF]

    def setProperty(self, name: str, value: typing.Any) -> bool:

        if name == "iconPixmap":
            self.iconPixmap = value
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
        # print("PRESSED")
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
