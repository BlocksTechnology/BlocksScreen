import typing
from functools import partial

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QPushButton, QStackedWidget, QStyle, QWidget
from ui.customNumpad_ui import Ui_customNumpad

class CustomQPushButton(QPushButton):
    """CustomQPushButton Custom QPushButton where icon position can be set.

    Args:
        parent (QWidget): parent of the button
        QPushButton (_type_):
    """

    # TODO: Icon image quality fix
    # TODO: Icon Transparency
    # TODO: Button size cannot be small so it overflows over to other buttons when in a collumn layout
    def __init__(
        self,
        parent: typing.Optional["QWidget"],
        x: int = 0,
        y: int = 0,
        *args,
        **kwargs,
    ):
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
        if style is None:
            return None

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

        if style is None:
            return None

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


class CustomNumpad(QWidget):
    """CustomNumpad
        A custom numpad for inserting integer values.

    Args:
        QFrame (_type_): _description_
    """

    inserted_new_value = pyqtSignal([str, int], [str, float], name="numpad_new_value")
    request_change_page = pyqtSignal(int, int, name="request_change_page")
    request_back_button_pressed = pyqtSignal(name="request_back_button_pressed")

    def __init__(
        self,
        widget_ui,
    ) -> None:
        super(CustomNumpad, self).__init__()

        self.panel = Ui_customNumpad()
        # self.panel = widget_ui
        self.panel.setupUi(self)
        # TODO: Add the current temperature to display the user the current temperature of the extruder for example or just leave it as nothing in the begining
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        
        self.global_panel_index: int = -1
        self.current_number: str = ""
        self.current_object: str | None = None
        self.slot_method = None
        self.numpad_window_index: int = -1
        self.previous_window_index: int = -1
        self.caller_panel: QStackedWidget | None = None
        self.panel.numpad_0.clicked.connect(partial(self.insert_number, 0))
        self.panel.numpad_1.clicked.connect(partial(self.insert_number, 1))
        self.panel.numpad_2.clicked.connect(partial(self.insert_number, 2))
        self.panel.numpad_3.clicked.connect(partial(self.insert_number, 3))
        self.panel.numpad_4.clicked.connect(partial(self.insert_number, 4))
        self.panel.numpad_5.clicked.connect(partial(self.insert_number, 5))
        self.panel.numpad_6.clicked.connect(partial(self.insert_number, 6))
        self.panel.numpad_7.clicked.connect(partial(self.insert_number, 7))
        self.panel.numpad_8.clicked.connect(partial(self.insert_number, 8))
        self.panel.numpad_9.clicked.connect(partial(self.insert_number, 9))
        self.panel.numpad_enter.clicked.connect(partial(self.insert_number, "enter"))
        self.panel.numpad_clear.clicked.connect(partial(self.insert_number, "clear"))

        self.panel.numpad_back_btn.clicked.connect(self.back_button)

    def insert_number(self, value: int | str) -> None:
        if isinstance(value, int):
            #
            self.current_number = self.current_number + str(value)
            self.panel.inserted_value.setText(self.current_number)
        elif isinstance(value, str):
            if (
                "enter" in value
                and self.current_number.isnumeric()
                and self.current_object is not None
            ):
                if self.current_object.startswith("fan"):
                    if 0 <= int(self.current_number) <= 100:
                        # * For the fan i'll the user will only be able to insert a value between 0 and 100
                        ("Sending the new value for the fan")
                        self.inserted_new_value[str, float].emit(
                            self.current_object, float(self.current_number)
                        )
                else:
                    self.inserted_new_value[str, int].emit(
                        self.current_object, int(self.current_number)
                    )
                self.reset_numpad()
                self.hide()
            elif "clear" in value:
                self.current_number = self.current_number[
                    : len(self.current_number) - 1
                ]
                self.panel.inserted_value.setText(self.current_number)

    def back_button(self):
        """back_button
        Controls what the numpad page does when the back button is pressed.
        """
        self.reset_numpad()
        self.request_back_button_pressed.emit()

    @pyqtSlot(int, str, str, "PyQt_PyObject", QStackedWidget, name="call_numpad")
    def call_numpad(
        self,
        global_panel_index: int,
        printer_object: str,
        current_temperature: str,
        callback_slot,  # Add: type here
        caller: QStackedWidget,
    ) -> None:
        self.caller_panel = caller
        # _logger.info(
        #     f"Numpad panel was called from global panel index: {global_panel_index} | Caller object name: {caller.__class__.__name__}."
        # )
        if callable(callback_slot):
            self.slot_method = callback_slot
            if "fan" in printer_object:
                self.inserted_new_value[str, float].connect(callback_slot)
            else:
                self.inserted_new_value[str, int].connect(callback_slot)

        self.global_panel_index = global_panel_index
        self.previous_window_index = self.caller_panel.currentIndex()
        self.numpad_window_index = self.caller_panel.addWidget(self)

        self.request_change_page.emit(global_panel_index, self.numpad_window_index)

        # * Reset the displayed temperature
        self.panel.inserted_value.setText(current_temperature)
        self.current_object = printer_object

        # _logger.info(
        #     f"Panel {self.global_panel_index} Called numpad \n"
        #     f"Caller panel name {self.caller_panel.__class__.__name__}"
        #     f"Previous panel index was {self.previous_window_index}\n"
        #     f"Numpad inserted at index {self.numpad_window_index}\n"
        # )

    def reset_numpad(self) -> bool:
        try:
            self.current_number = ""
            if self.slot_method is not None and callable(self.slot_method):
                if self.current_object is not None and "fan" in self.current_object:
                    self.inserted_new_value[str, float].disconnect(self.slot_method)
                else:
                    self.inserted_new_value[str, int].disconnect(self.slot_method)
                self.slot_method = None
                if self.caller_panel is not None:
                    self.caller_panel.setCurrentIndex(self.previous_window_index)
                    self.caller_panel.removeWidget(self)
                    self.window_index = -1
                    self.caller_panel = None
            self.global_panel_index = -1
            self.numpad_window_index = -1
            self.previous_window_index = -1
            self.panel.inserted_value.setText(self.current_number)
            return True
        except Exception as e:
            raise Exception(f"Could not reset numpad, error message caught : {e}")

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        """paintEvent
            Repaints the widget with custom controls

        Args:
            a0 (QtGui.QPaintEvent | None): The event for repainting

        Returns:
            Nothing: Nothing
        """
        if self.current_object is not None:
            self.panel.heater.setText(self.current_object)
        if self.isVisible():
            # painter = QtGui.QPainter()
            # painter.begin(self)

            # * The are where the numpad was called

            if self.current_object is not None and "fan" in self.current_object:
                pass

                # painter = QtGui.QPainter(self.panel.inserted_value)

                # painter.begin(self)
                # painter.setCompositionMode(
                #     painter.CompositionMode.CompositionMode_SourceOver
                # )
                # painter.setRenderHint(painter.RenderHint.Antialiasing, True)
                # painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
                # painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)
                # # * We have a fan so i need to verify that the inserted value is between 0 and 100
                # _label_rect: QRect = self.panel.inserted_value.rect()
                # _new_rect: QRect = _label_rect
                # _margins: QtCore.QMargins = QtCore.QMargins(1, 1, 1, 1)

                # TODO: Add limits to what the user can input for the fan speed 0 to 100
                # TODO: Also add limitis for speed parameter, the value should also be between 0 and 100
                # TODO: The field (QLabel) where the value is inserted, should flash red when the value is not between 0 and 100
                # # print(f"The current number for the fan value: {self.current_number}")
                # # if not 0 <= int(self.current_number) <= 100:
                # #     _red_color: QtGui.QColor = QtGui.QColor(255, 30, 30, 1)
                # #     _new_rect = _new_rect.marginsAdded(_margins)

                # #     painter.setCompositionMode(
                # #         painter.CompositionMode.CompositionMode_SourceIn
                # #     )
                # #     painter.fillRect(_new_rect, _red_color)

                # #     painter.drawRoundedRect(_new_rect.toRectF(), 5.0, 5.0)

                # # else:
                # #     _new_rect = _new_rect.marginsRemoved(_margins)

                # painter.end()
            # painter.end()
        # return super().paintEvent(a0)

    def sizeHint(self) -> QtCore.QSize:
        return super().sizeHint()

    def event(self, e: QtCore.QEvent | None) -> bool:
        return super().event(e)


class CustomTopBarInfo(QWidget):
    def __init__(self, parent, x: int = 0, y: int = 0, *args, **kwargs):
        super(CustomTopBarInfo, self).__init__(parent, *args, **kwargs)

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        return super().paintEvent(a0)

    def sizeHint(self) -> QtCore.QSize:
        return super().sizeHint()

    def event(self, a0: QtCore.QEvent | None) -> bool:
        return super().event(a0)
