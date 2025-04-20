from pickle import NONE
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

    # TODO: Icon Transparency
    # TODO: Button size cannot be small so it overflows over to other buttons when in a collumn layout

    def __init__(
        self,
        parent: typing.Optional["QWidget"] = None,
        *args,
        **kwargs,
    ) -> None:
        if parent is not None:
            super(BlocksCustomButton, self).__init__(parent, *args, **kwargs)
            self.parent_object = parent
        else:
            super(BlocksCustomButton, self).__init__(*args, **kwargs)

        self._icon = self.icon()
        if not self._icon.isNull():
            super().setIcon(QtGui.QIcon())

        self.iconPosition = QtCore.QPoint(0, 0)
        self.icon_pixmap: QtGui.QPixmap | None = None
        self.adjusted_icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._icon_rectF: typing.Optional[QtCore.QRectF] = QtCore.QRectF()

        self.borderIconLeft: QtGui.QPixmap | None = None
        self.borderIconCenter: QtGui.QPixmap | None = None
        self.borderIconRight: QtGui.QPixmap | None = None
        self.borderLeftRect: QtCore.QRect = QtCore.QRect()
        self.borderCenterRect: QtCore.QRect = QtCore.QRect()
        self.borderRightRect: QtCore.QRect = QtCore.QRect()

        self.button_background_pixmap_rects = []
        self.button_background_pixmap: typing.Optional[QtGui.QPixmap] = QtGui.QPixmap()

        self.button_type = None
        self.text_formatting: str | None = None
        self._text: str | None = None
        self.pt_rect: QtCore.QRect | None = None
        self._secondary_text: str | None = None
        self.st_rect: QtCore.QRect | None = None
        self._name: str | None = None
        self.text_color: QtGui.QColor = QtGui.QColor(0, 0, 0, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        if self.button_type == "normal":
            self.button_background_pixmap_rects = self._build_background_pixmap()
        if self.icon_pixmap is not None:
            self._icon_rectF = self._build_icon_pixmap()

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

    # def sizeHint(self):
    #     # TODO: Set the icons pressed size
    #     if self.button_type is None:
    #         return
    #     hint = super().sizeHint()
    # if hint is None:
    #     return
    # if not self.text or self._icon.isNull():
    #     return hint

    # style = self.style()
    # opt = QtWidgets.QStyleOptionButton()
    # self.initStyleOption(opt)
    # if style is None:
    #     return None

    # margin = style.pixelMetric(style.PixelMetric.PM_ButtonMargin, opt, self)
    # spacing = style.pixelMetric(
    #     style.PixelMetric.PM_LayoutVerticalSpacing, opt, self
    # )
    # if self.button_type == "normal":
    #     if self._text is None:
    #         return hint
    #     labelRect = self.fontMetrics().boundingRect(
    #         0, 0, 5000, 5000, QtCore.Qt.TextFlag.TextShowMnemonic, self._text
    #     )
    #     iconHeight = self.iconSize().height()
    #     height = iconHeight + spacing + labelRect.height() + margin * 2
    #     if height > hint.height():
    #         hint.setHeight(iconHeight)
    #     hint.setHeight(iconHeight)
    #     hint.setWidth(self.iconSize().width())
    #     return hint
    # elif "icon" in self.button_type:
    #     return
    # elif "secondary" in self.button_type:
    #     ...
    # elif "display" in self.button_type:
    #     if not self._text or self.icon_pixmap is None:
    #         return
    #     _label_rect = self.fontMetrics().boundingRect(
    #         0, 0, 5000, 5000, QtCore.Qt.TextFlag.TextShowMnemonic, self._text
    #     )
    #     _icon_height = self.iconSize().height()
    #     _height = _icon_height + spacing + _label_rect.height() + margin * 2
    #     if _height > hint.height():
    #         hint.setHeight(_icon_height)
    #     hint.setHeight(_icon_height)
    #     hint.setWidth(self.iconSize().width())
    #     if hint is None:
    #         return
    #     return hint

    # return hint

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        if self.button_type == "normal":
            self.button_background_pixmap_rects = (
                self._build_background_pixmap()
            )  # Draw the normal buttons background

        if self.icon_pixmap is not None:
            self._icon_rectF = self._build_icon_pixmap()

        return super().resizeEvent(a0)

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
        _rect = self.rect()
        _style = self.style()

        if _style is None or _rect is None:
            return
        margin = _style.pixelMetric(_style.PixelMetric.PM_ButtonMargin, opt, self)
        qp.drawControl(QStyle.ControlElement.CE_PushButton, opt)
        if self.button_type == "normal":
            if (
                self.button_background_pixmap is not None
                and self.button_background_pixmap_rects is not None
            ):
                scaled_width = self.button_background_pixmap.width()
                scaled_height = self.button_background_pixmap.height()
                adjusted_x = (
                    self.button_background_pixmap.width() - scaled_width
                ) / 2.0
                adjusted_y = (
                    self.button_background_pixmap.height() - scaled_height
                ) / 2.0
                adjusted_background_rect = QtCore.QRectF(
                    self.button_background_pixmap.rect().x() + adjusted_x,
                    self.button_background_pixmap.rect().y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
                qp.drawPixmap(
                    adjusted_background_rect,
                    self.button_background_pixmap,
                    self.button_background_pixmap.rect().toRectF(),
                )
            if self.button_background_pixmap_rects and self.text() is not None:
                _start_text_position = int(
                    self.button_background_pixmap_rects[0].width()
                )
                _rect.setLeft(_start_text_position + margin)
                qp.drawText(
                    _rect,
                    QtCore.Qt.TextFlag.TextShowMnemonic
                    | QtCore.Qt.AlignmentFlag.AlignLeft
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    str(self.text()),
                )
        elif "icon" in self.button_type:
            if "text" in self.button_type and self.text() is not None:
                qp.setCompositionMode(qp.CompositionMode.CompositionMode_Difference)
                # qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceIn)
                if self._icon_rectF is not None:
                    if self.text_formatting is None:
                        scaled_width = self._icon_rectF.width()
                        scaled_height = self._icon_rectF.height()

                        adjusted_x = (self._icon_rectF.width() - scaled_width) / 2.0
                        adjusted_y = (self._icon_rectF.height() - scaled_height) / 2.0
                        adjusted_rectF = QtCore.QRectF(
                            self._icon_rectF.x() + adjusted_x,
                            self._icon_rectF.y() + adjusted_y,
                            scaled_width,
                            scaled_height,
                        )
                    elif self.text_formatting == "bottom":
                        adjusted_x = (
                            self._icon_rectF.width() - self.width() + 5.0
                        ) / 2.0
                        adjusted_rectF = QtCore.QRectF(
                            self._icon_rectF.x() + adjusted_x,
                            self._icon_rectF.height() ,
                            self.width(),
                            self.height() - self._icon_rectF.height(),
                        )

                    _font = QtGui.QFont()
                    _font.setBold(True)
                    _palette = self.palette()
                    _palette.setColor(
                        QtGui.QPalette.ColorRole.WindowText, self.text_color
                    )
                    _palette.setColor(
                        QtGui.QPalette.ColorRole.PlaceholderText, self.text_color
                    )
                    _palette.setColor(QtGui.QPalette.ColorRole.Text, self.text_color)
                    _palette.setColor(
                        QtGui.QPalette.ColorRole.ButtonText, self.text_color
                    )
                    self.setFont(_font)
                    self.setPalette(_palette)
                    qp.drawText(
                        adjusted_rectF,
                        QtCore.Qt.TextFlag.TextSingleLine
                        | QtCore.Qt.AlignmentFlag.AlignHCenter
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str(self.text()),
                    )

        elif "display" in self.button_type:
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceAtop)
            _brush = QtGui.QBrush()
            _brush.setColor(QtGui.QColor(177, 196, 203, 75))
            _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            qp.setBrush(_brush)
            qp.drawRoundedRect(
                self.contentsRect(), 15, 15, QtCore.Qt.SizeMode.AbsoluteSize
            )
            _palette = self.palette()
            _palette.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColor("white"))
            _palette.setColor(
                QtGui.QPalette.ColorRole.ButtonText, QtGui.QColor("white")
            )
            self.setPalette(_palette)
            if (
                _rect is not None
                and self.text() is not None
                and self._icon_rectF is not None
            ):
                _ptl_rect = None
                _stl_rect = None
                _mtl = QtCore.QRectF(
                    int(self._icon_rectF.width()) + margin,
                    0.0,
                    int(_rect.width() - self._icon_rectF.width() - margin),
                    _rect.height(),
                )
                if "secondary" in self.button_type:
                    _ptl_rect = QtCore.QRectF(
                        int(_mtl.left()),
                        0.0,
                        int((_mtl.width() / 2.0) - 5),
                        _rect.height(),
                    )
                    _mtl_rect = QtCore.QRectF(
                        int(_ptl_rect.right()), 0.0, 10, _rect.height()
                    )
                    _stl_rect = QtCore.QRectF(
                        int(_mtl.center().x() + 3.0),
                        0.0,
                        int(_mtl.width() / 2.0),
                        _rect.height(),
                    )
                    qp.drawText(
                        _ptl_rect,
                        QtCore.Qt.TextFlag.TextShowMnemonic
                        | QtCore.Qt.AlignmentFlag.AlignHCenter
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str(self.text()) if self.text() is not None else str("?"),
                    )
                    qp.drawText(
                        _stl_rect,
                        QtCore.Qt.TextFlag.TextShowMnemonic
                        | QtCore.Qt.AlignmentFlag.AlignHCenter
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str(self.secondary_text())
                        if self.secondary_text() is not None
                        else str("?"),
                    )
                    qp.drawText(
                        _mtl_rect,
                        QtCore.Qt.TextFlag.TextShowMnemonic
                        | QtCore.Qt.AlignmentFlag.AlignHCenter
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str("/"),
                    )

                else:
                    qp.drawText(
                        _mtl,
                        QtCore.Qt.TextFlag.TextShowMnemonic
                        | QtCore.Qt.AlignmentFlag.AlignHCenter
                        | QtCore.Qt.AlignmentFlag.AlignVCenter,
                        str(self.text()) if self.text() is not None else str("?"),
                    )

        if self.adjusted_icon_pixmap is not None:
            if self._icon_rectF is not None:
                qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceAtop)
                scaled_width = self.adjusted_icon_pixmap.width()
                scaled_height = self.adjusted_icon_pixmap.height()
                adjusted_x = (
                    (self.adjusted_icon_pixmap.width() - scaled_width) + 5
                ) / 2.0
                adjusted_y = (
                    (self.adjusted_icon_pixmap.height() - scaled_height) + 5
                ) / 2.0
                adjusted_icon_rect = QtCore.QRectF(
                    self.adjusted_icon_pixmap.rect().x() + adjusted_x,
                    self.adjusted_icon_pixmap.rect().y() + adjusted_y,
                    scaled_width - 5,
                    scaled_height - 5,
                )
                qp.drawPixmap(
                    adjusted_icon_rect,
                    self.adjusted_icon_pixmap,
                    self.adjusted_icon_pixmap.rect().toRectF(),
                )
        qp.restore()
        if e is None:
            return
        return super().paintEvent(e)

    def _build_icon_pixmap(
        self,
    ) -> typing.Optional[QtCore.QRectF]:
        if self.icon_pixmap is None or self.button_type is None:
            return None
        if "normal" == self.button_type:
            if self.button_background_pixmap_rects:
                _iconParentRect = self.button_background_pixmap_rects[0]
                _icon_rect = QtCore.QRectF(
                    _iconParentRect.width() * 0.20,
                    _iconParentRect.height() * 0.185,
                    _iconParentRect.width() * 0.5,
                    _iconParentRect.height() * 0.5,
                )
                _icon_scaled = self.icon_pixmap.scaled(
                    int(_icon_rect.width()),
                    int(_icon_rect.height()),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )

        elif "icon" in self.button_type:
            if self.text_formatting is None:
                _icon_rect = QtCore.QRectF(  # x, y, width , height
                    0.0, 0.0, self.width() - 5.0, self.height() - 5.0
                )
                _icon_scaled = self.icon_pixmap.scaled(
                    _icon_rect.size().toSize(),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )
            else:
                _icon_rect = QtCore.QRectF(
                    0.0, 0.0, (self.width() - 15.0), (self.height() - 15.0)
                )
                _icon_scaled = self.icon_pixmap.scaled(
                    _icon_rect.size().toSize(),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation,
                )

        elif "display" in self.button_type:
            _parent_rect: QtCore.QRect = self.rect()
            _icon_rect = QtCore.QRectF(  # x,y, width * size reduction factor, height
                0.0,
                0.0,
                (_parent_rect.width() * 0.3) - 5.0,
                _parent_rect.height() - 5,
            )
            _icon_scaled = self.icon_pixmap.scaled(
                int(_icon_rect.width()),
                int(_icon_rect.height()),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )

        # Calculate the actual QRect for the scaled pixmap (centering it if needed)
        scaled_width = _icon_scaled.width()
        scaled_height = _icon_scaled.height()
        adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
        adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
        adjusted_icon_rect = QtCore.QRectF(
            _icon_rect.x() + adjusted_x,
            _icon_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )

        # * Compose the pixmap and save it in order to decrease paintings during runtime
        _icon_pixmap = QtGui.QPixmap(
            _icon_rect.toRect().width(), _icon_rect.toRect().height()
        )
        _icon_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(_icon_pixmap)
        painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceOver)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(
            adjusted_icon_rect,  # Target area (adjusted for centering)
            _icon_scaled,  # Scaled pixmap
            _icon_scaled.rect().toRectF(),  # Entire source (scaled) pixmap
        )
        self.adjusted_icon_pixmap = _icon_pixmap

        return _icon_rect

    def _build_background_pixmap(self) -> typing.Optional[list[QtCore.QRectF]]:
        if (
            self.borderIconRight is None
            or self.borderIconCenter is None
            or self.borderIconLeft is None
        ):
            return None
        background_pixmap = QtGui.QPixmap(self.width(), self.height())
        background_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(background_pixmap)
        painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceOver)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
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
        painter.drawPixmap(
            _scaledLeftPixmap.rect().toRectF(),
            _scaledLeftPixmap,
            _scaledLeftPixmap.rect().toRectF(),
        )
        painter.drawPixmap(
            _centerBorderRectF,
            _scaledCenterPixmap,
            _scaledCenterPixmap.rect().toRectF(),
        )
        painter.drawPixmap(
            _rightBorderRectF, _scaledRightPixmap, _scaledRightPixmap.rect().toRectF()
        )
        painter.restore()
        painter.end()
        self.button_background_pixmap = background_pixmap
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
        elif name == "font":
            self.setFont(QtGui.QFont(value))
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "text_color":
            self.text_color = QtGui.QColor(value)
        return super().setProperty(name, value)


class BlocksLabel(QtWidgets.QLabel):
    def __init__(self, parent: typing.Optional["QWidget"] = None, *args, **kwargs):
        if parent is not None:
            super(BlocksLabel, self).__init__(parent, *args, **kwargs)

        self.icon_pixmap: typing.Optional[QtGui.QPixmap] = None
        self._text: typing.Optional[str] = None
        self._background_color: typing.Optional[QtGui.QColor] = None
        self._rounded: bool = False

    def parent(self) -> QtCore.QObject:
        return super().parent()

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        self.icon_pixmap = a0
        self.update()
        return

    def setText(self, a0: str) -> None:
        self._text = a0
        self.update()

        return super().setText(a0)

    @property
    def background_color(self) -> typing.Optional[QtGui.QColor]:
        return self._background_color

    @background_color.setter
    def background_color(self, color: QtGui.QColor) -> None:
        self._background_color = color
        self.update()

    @property
    def rounded(self) -> bool:
        return self._rounded

    @rounded.setter
    def rounded(self, on: bool) -> None:
        self._rounded = on

    # TODO: Add rounded object acording to the size, calculate the edge pixels radius according to the label size

    def construct_animation(self) -> None:
        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        self.animation = QtCore.QPropertyAnimation(self, b"borderColor")
        self.animation.setDuration(2000)
        self.animation.setLoopCount(-1)

        self.animation.setStartValue(QtGui.QColor("red"))
        self.animation.start()

    def border_color(self, color):
        self.setStyleSheet(f"border: 2px solid {color.name()};")

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtWidgets.QStylePainter(self)
        qp.save()
        qp.setRenderHint(qp.RenderHint.Antialiasing, True)
        qp.setRenderHint(qp.RenderHint.SmoothPixmapTransform, True)
        qp.setRenderHint(qp.RenderHint.LosslessImageRendering, True)
        _rect = self.rect()
        _style = self.style()
        if _style is None or _rect is None:
            return
        if self.icon_pixmap is not None:
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceOver)
            _icon_rect = QtCore.QRectF(0.0, 0.0, self.width(), self.height())
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )
            qp.drawPixmap(
                adjusted_icon_rect, _icon_scaled, _icon_scaled.rect().toRectF()
            )
        # TODO : Feature Request, add text onto the label, formatted according to the icon,
        #  Add "above" "bellow", "right", "left" this indicates where the text should be drawn

        if self._background_color is not None:
            qp.setCompositionMode(qp.CompositionMode.CompositionMode_SourceIn)

            _brush = QtGui.QBrush()
            _brush.setColor(self._background_color)
            _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            qp.setBrush(_brush)
            if self._rounded:
                qp.drawRoundedRect(self.rect(), 15, 15, QtCore.Qt.SizeMode.AbsoluteSize)
            else:
                qp.drawRect(self.rect())
        qp.restore()
        return super().paintEvent(a0)

    def setProperty(self, name: str, value: typing.Any) -> bool:
        if name == "icon_pixmap":
            self.setPixmap(value)

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
