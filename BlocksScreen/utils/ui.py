import typing
from functools import partial

from lib.ui.customNumpad_ui import Ui_customNumpad
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QPushButton, QStackedWidget, QStyle, QWidget


class BlocksCustomButton(QPushButton):
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
        *args,
        **kwargs,
    ):
        super(BlocksCustomButton, self).__init__(parent, *args, **kwargs)

        self.parent_object = parent

        self._icon = self.icon()
        if not self._icon.isNull():
            super().setIcon(QtGui.QIcon())

        self.iconPosition = QtCore.QPoint(0, 0)
        self.icon_pixmap: QtGui.QPixmap | None = None
        self.borderIconLeft: QtGui.QPixmap | None = None
        self.borderIconCenter: QtGui.QPixmap | None = None
        self.borderIconRight: QtGui.QPixmap | None = None
        self.borderLeftRect: QtCore.QRect = QtCore.QRect()
        self.borderCenterRect: QtCore.QRect = QtCore.QRect()
        self.borderRightRect: QtCore.QRect = QtCore.QRect()

        self.buttonPixmapRects = []
        self.button_type = None
        self._text: str | None = None
        self.pt_rect: QtCore.QRect | None = None
        self._secondary_text: str | None = None
        self.st_rect: QtCore.QRect | None = None
        self._name: str | None = None

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def name(self):
        return self._name

    def setIcon(self, icon):
        # setting an icon might change the horizontal hint, so we need to use a
        # "local" reference for the actual icon and go on by letting Qt to *think*
        # that it doesn't have an icon;
        if icon == self._icon:
            return
        self._icon = icon
        self.updateGeometry()
        self.update()

    def text(self) -> str | None:
        return self._text

    def secondary_text(self) -> str | None:
        return self._secondary_text

    def setText(self, text: str) -> None:
        self._text = text
        self.update()  # Force button update
        return

    def setSecondaryText(self, text: str) -> None:
        self._secondary_text = text
        self.update()  # Force button update
        return

    def sizeHint(self):
        # TODO: Set the icons pressed size
        if self.button_type is None:
            return
        hint = super().sizeHint()
        if not self.text or self._icon.isNull():
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
        if self.button_type == "normal":
            labelRect = self.fontMetrics().boundingRect(
                0, 0, 5000, 5000, QtCore.Qt.TextFlag.TextShowMnemonic, self._text
            )
            iconHeight = self.iconSize().height()
            height = iconHeight + spacing + labelRect.height() + margin * 2
            if height > hint.height():
                hint.setHeight(iconHeight)
            hint.setHeight(iconHeight)
            hint.setWidth(self.iconSize().width())
            return hint
        elif "secondary" in self.button_type:
            ...
        elif "display" in self.button_type:
            if not self._text or self.icon_pixmap is None:
                return hint
            _label_rect = self.fontMetrics().boundingRect(
                0, 0, 5000, 5000, QtCore.Qt.TextFlag.TextShowMnemonic, self._text
            )
            _icon_height = self.iconSize().height()
            _height = _icon_height + spacing + _label_rect.height() + margin * 2
            if _height > hint.height():
                hint.setHeight(_icon_height)
            hint.setHeight(_icon_height)
            hint.setWidth(self.iconSize().width())

            return hint

    def paintEvent(self, e: QtGui.QPaintEvent | None):
        if self.button_type is None:
            return
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        qp = QtWidgets.QStylePainter(self)
        qp.save()
        # * draw the button without any text or icon
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        rect = self.rect()
        style = self.style()
        if style is None or rect is None:
            return
        margin = style.pixelMetric(style.PixelMetric.PM_ButtonMargin, opt, self)
        qp.drawControl(QStyle.ControlElement.CE_PushButton, opt)

        qp.setPen(QtGui.QColor(255, 255, 0, 255))
        qp.drawRect(rect)

        if self.button_type == "normal":
            self.buttonPixmapRects = self.set_button_graphics(qp, margin)
            if self.icon_pixmap is not None:
                _, self._icon_rectF = self.paint_icon(qp)

            # *  Draw Text stuff over the button
            if self.buttonPixmapRects and self.text is not None:
                labelRect = QtCore.QRect(rect)
                _start_text_position = int(self.buttonPixmapRects[0].width())
                labelRect.setLeft(_start_text_position + margin)
                # labelRect.setRight(
                #     int(self.buttonPixmapRects[1].width() + _start_text_position)
                # )  # Set the right limit for the button rect
                qp.drawText(
                    labelRect,
                    QtCore.Qt.TextFlag.TextShowMnemonic
                    | QtCore.Qt.AlignmentFlag.AlignLeft
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    self.text(),
                )

        elif "display" in self.button_type:
            _icon_rectF = None
            if self.icon_pixmap is not None:
                _, _icon_rectF = self.paint_icon(qp)

            if rect is not None and self.text() is not None and _icon_rectF is not None:
                _ptl_rect = None
                _stl_rect = None
                _mtl = QtCore.QRectF(
                    int(_icon_rectF.width()) + margin,
                    0.0,
                    int(rect.width() - _icon_rectF.width() - margin),
                    rect.height(),
                )

                if "secondary" in self.button_type:
                    _ptl_rect = QtCore.QRectF(
                        int(_mtl.left()),
                        0.0,
                        int((_mtl.width() / 2) - 5),
                        rect.height(),
                    )
                    _mtl_rect = QtCore.QRectF(
                        int(_ptl_rect.right()), 0.0, 10, rect.height()
                    )
                    _stl_rect = QtCore.QRectF(
                        int(_mtl.center().x() + 5),
                        0.0,
                        int(_mtl.width() / 2),
                        rect.height(),
                    )
                    # TEST The following lines are to be deleted, this is being used to test the buttons limits
                    qp.setPen(QtGui.QColor(255, 0, 255, 255))
                    qp.drawRect(_ptl_rect)
                    qp.setPen(QtGui.QColor(0, 0, 255, 255))
                    qp.drawRect(_stl_rect)
                    qp.setPen(QtGui.QColor(255, 255, 255, 255))

                qp.drawText(
                    _mtl,
                    QtCore.Qt.TextFlag.TextShowMnemonic
                    | QtCore.Qt.AlignmentFlag.AlignHCenter
                    if "secondary" in self.button_type
                    else QtCore.Qt.AlignmentFlag.AlignLeft
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    self.text(),
                )

        elif "icon":
            
            # TODO: icon type button  paintEvent
            _icon_rectF = None
            if self.icon_pixmap is not None: 
                _, _icon_rectF = self.paint_icon(qp)
            
            
                

        qp.restore()
        return super().paintEvent(e)

    def paint_icon(
        self,
        qp: QtWidgets.QStylePainter,
    ) -> typing.Tuple[QtGui.QIcon, QtCore.QRectF] | None:
        if self.icon_pixmap is None or self.button_type is None:
            return None
        if "normal" == self.button_type:
            if self.buttonPixmapRects:
                _iconParentRect = self.buttonPixmapRects[0]
                _pixmap_size = self.icon_pixmap.size()
                _icon_rect = QtCore.QRectF(
                    _iconParentRect.width() * 0.20,
                    _iconParentRect.height() * 0.185,
                    _pixmap_size.width() - _iconParentRect.width() * 0.5,
                    _pixmap_size.height() - _iconParentRect.height() * 0.5,
                )
                qp.setRenderHints(qp.RenderHint.Antialiasing)
                qp.setRenderHints(qp.RenderHint.LosslessImageRendering)
                qp.setRenderHints(qp.RenderHint.SmoothPixmapTransform)
                _icon_scaled = self.icon_pixmap.scaled(
                    int(_pixmap_size.width()),
                    int(_pixmap_size.height()),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
                qp.drawPixmap(
                    _icon_rect, _icon_scaled, self.icon_pixmap.rect().toRectF()
                )
                return (QtGui.QIcon(_icon_scaled), _icon_rect)

        elif "display" in self.button_type:
            _parent_rect: QtCore.QRect = self.rect()
            _icon_rect = QtCore.QRectF(  # x,y, width, height
                0.0,
                0.0,
                _parent_rect.width() * 0.4,
                _parent_rect.height(),
            )
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            qp.setRenderHint(qp.RenderHint.Antialiasing)
            qp.setRenderHint(qp.RenderHint.LosslessImageRendering)
            qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform)
            _icon_scaled = self.icon_pixmap.scaled(
                int(self.icon_pixmap.width()),
                int(self.icon_pixmap.height()),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            qp.drawPixmap(_icon_rect, _icon_scaled, self.icon_pixmap.rect().toRectF())
            # print(_icon_scaled.size())
            return (QtGui.QIcon(_icon_scaled), _icon_rect)
        elif self.button_type == "icon":
            _parent_rect = QtCore.QRect = self.rect()
            _icon_rect = QtCore.QRectF(
                0.0, 0.0, _parent_rect.width(), _parent_rect.height()
            )
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            qp.setRenderHint(qp.RenderHint.Antialiasing)
            qp.setRenderHint(qp.RenderHint.LosslessImageRendering)
            qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform)

            _icon_scaled = self.icon_pixmap.scaled(
                int(self.icon_pixmap.width()),
                int(self.icon_pixmap.height()),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            qp.drawPixmap(_icon_rect, _icon_scaled, self.icon_pixmap.rect().toRectF())
            return (QtGui.QIcon(_icon_scaled), _icon_rect)

    def set_button_graphics(
        self, qp: QtWidgets.QStylePainter, margin
    ) -> list[QtCore.QRectF] | None:
        if (
            self.borderIconRight is None
            or self.borderIconCenter is None
            or self.borderIconLeft is None
        ):
            return None
        buttonRect = self.rect()
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
        qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering)
        qp.setRenderHint(qp.RenderHint.Antialiasing)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform)
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
        return [_leftBorderRectF, _centerBorderRectF, _rightBorderRectF]

    def setProperty(self, name: str, value: typing.Any):
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "borderLeftPixmap":
            self.borderIconLeft = value
        elif name == "borderCenterPixmap":
            self.borderIconCenter = value
        elif name == "borderRightPixmap":
            self.borderIconRight = value
        elif name == "name":
            self._name = name
        elif name == "button_type":
            self.button_type = value

        return super().setProperty(name, value)


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
        callback_slot,
        caller: QStackedWidget,
    ) -> None:
        self.caller_panel = caller

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
            self.panel.value_name.setText(self.current_object)
            self.panel.numpad_title.setText(self.current_object)

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
